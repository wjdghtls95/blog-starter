import os
import json
import hashlib
import requests
from datetime import datetime, timezone, timedelta

DRAFT_FILE = os.environ["DRAFT_FILE"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
CF_ACCOUNT_ID = os.environ["CF_ACCOUNT_ID"]
CF_API_TOKEN = os.environ["CF_API_TOKEN"]
KV_NAMESPACE_ID = os.environ["KV_NAMESPACE_ID"]
QUEUE_MAX = 5

# ===== LLM Provider =====
# LLM_PROVIDER: openai (default) | anthropic | groq | openai-compatible
# Set only the API key for the provider you're using.
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openai")

with open(DRAFT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Parse source file path from frontmatter
import re as _re
_source_match = _re.search(r'^source:\s*(.+)$', content, _re.MULTILINE)
SOURCE_FILE = _source_match.group(1).strip() if _source_match else None

# ===== KV Helpers =====

def get_kv(key):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/storage/kv/namespaces/{KV_NAMESPACE_ID}/values/{key}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {CF_API_TOKEN}"})
    if resp.status_code == 404:
        return None
    return resp.text

def put_kv(key, value_str, expiration_ttl=None):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/storage/kv/namespaces/{KV_NAMESPACE_ID}/values/{key}"
    params = {}
    if expiration_ttl:
        params["expiration_ttl"] = expiration_ttl
    requests.put(
        url,
        headers={"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "text/plain"},
        params=params,
        data=value_str.encode("utf-8"),
    )

def send_telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"},
    )

# ===== Quiz Generation =====

QUIZ_PROMPT = f"""Read the following post and create 10 quiz questions.

Rules:
- At least 1 question per H2 section
- Questions must require reading the full post
- 7 multiple choice (easy 2, medium 3, hard 2)
- 3 essay (medium 1, hard 2)
- Return ONLY the JSON below, no other text

{{
  "title": "post title",
  "questions": [
    {{"type": "multiple", "difficulty": "easy", "q": "question", "options": ["A. option", "B. option", "C. option", "D. option"], "answer": "A", "section": "section name"}},
    {{"type": "essay", "difficulty": "hard", "q": "question", "section": "section name"}}
  ]
}}

Post content:
{content}"""


def call_llm(prompt: str) -> str:
    """Call the configured LLM provider. Returns a JSON string."""

    if LLM_PROVIDER == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        msg = client.messages.create(
            model=os.environ.get("LLM_MODEL", "claude-haiku-4-5-20251001"),
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text

    elif LLM_PROVIDER == "groq":
        # Groq uses the OpenAI SDK with a different base_url (free tier available)
        from openai import OpenAI
        client = OpenAI(
            api_key=os.environ["GROQ_API_KEY"],
            base_url="https://api.groq.com/openai/v1",
        )
        resp = client.chat.completions.create(
            model=os.environ.get("LLM_MODEL", "llama-3.1-8b-instant"),
            max_tokens=2000,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content

    elif LLM_PROVIDER == "openai-compatible":
        # For Ollama, Together AI, OpenRouter, etc.
        # Set LLM_BASE_URL (e.g. http://localhost:11434/v1) and LLM_MODEL
        from openai import OpenAI
        client = OpenAI(
            api_key=os.environ.get("LLM_API_KEY", "ollama"),
            base_url=os.environ["LLM_BASE_URL"],
        )
        resp = client.chat.completions.create(
            model=os.environ["LLM_MODEL"],
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content

    else:
        # Default: OpenAI
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        resp = client.chat.completions.create(
            model=os.environ.get("LLM_MODEL", "gpt-4o-mini"),
            max_tokens=2000,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content


quiz_json_str = call_llm(QUIZ_PROMPT)
quiz = json.loads(quiz_json_str)

# Multiple choice first, essay last
mc = [q for q in quiz["questions"] if q["type"] == "multiple"]
essay = [q for q in quiz["questions"] if q["type"] == "essay"]
quiz["questions"] = mc + essay
quiz["draftFile"] = DRAFT_FILE
quiz["content"] = content[:2000]
quiz["userAnswers"] = {}

# ===== Queue Management =====

queue_raw = get_kv("PENDING_QUEUE")
queue = json.loads(queue_raw) if queue_raw else []

if len(queue) >= QUEUE_MAX:
    send_telegram(
        f"⚠️ Queue is full ({QUEUE_MAX} items)\n"
        f"Wait for a post to publish before pushing again\n\n"
        f"Not queued: _{quiz['title']}_"
    )
    raise SystemExit(0)

slug = hashlib.md5(DRAFT_FILE.encode()).hexdigest()[:8]
quiz_key = f"pending_quiz_{slug}"
put_kv(quiz_key, json.dumps(quiz, ensure_ascii=True), expiration_ttl=7 * 86400)

queue.append({"file": DRAFT_FILE, "title": quiz["title"], "quizKey": quiz_key})
put_kv("PENDING_QUEUE", json.dumps(queue, ensure_ascii=True))

existing_date = get_kv("NEXT_QUIZ_DATE")
if not existing_date:
    today_kst = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d")
    put_kv("NEXT_QUIZ_DATE", today_kst)

quiz_date = get_kv("NEXT_QUIZ_DATE")
source_line = f"Source: `{SOURCE_FILE}`\n" if SOURCE_FILE else ""

send_telegram(
    f"📥 *Quiz queued*\n\n"
    f"Title: _{quiz['title']}_\n"
    f"{source_line}"
    f"Quiz scheduled: {quiz_date} 6pm KST"
)

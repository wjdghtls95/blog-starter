# blog-starter

[🇰🇷 한국어](docs/README.ko.md)

> A GitHub Pages blog template with automated quiz generation and Telegram publish workflow.
> Write a draft → push → quiz auto-generated → answer in Telegram → post goes live.

---

## What this does

### Without Obsidian

```
Write a draft in drafts/
    ↓
Push to GitHub
    ↓
GitHub Actions: quiz generated → stored in Cloudflare KV
Telegram notification sent
    ↓
Answer the quiz in Telegram
    ↓
/발행 → post moves to src/content/posts/
Blog builds and deploys to GitHub Pages
```

### With Obsidian (recommended)

Obsidian is where you write and refine notes. The blog is where you publish the polished version.

```
Write notes in Obsidian vault
    ↓
Copy/export finished note to drafts/
Add source: path/to/note.md in frontmatter
    ↓
git push
    ↓
Telegram: "퀴즈 등록됐습니다 — 소스: path/to/note.md"
    ↓
Answer the quiz in Telegram (proves you read it)
    ↓
/발행 → GitHub Pages
```

**Why the `source:` field?**
The Telegram notification shows the Obsidian file path so you know which note the quiz is about — useful when you have multiple drafts queued.

---

## Before you start — checklist

Gather these before running any commands:

| # | What you need | Where to get it | Takes |
|---|--------------|-----------------|-------|
| 1 | GitHub account | [github.com](https://github.com) | 2 min |
| 2 | OpenAI API key | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | 2 min |
| 3 | Telegram bot token | [@BotFather](https://t.me/BotFather) → `/newbot` | 2 min |
| 4 | Telegram chat ID | [@userinfobot](https://t.me/userinfobot) | 1 min |
| 5 | Cloudflare account (free) | [dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up) | 3 min |
| 6 | Cloudflare API token | Cloudflare → My Profile → API Tokens | 2 min |
| 7 | KV namespace ID | Workers & Pages → KV → Create namespace | 2 min |
| 8 | Node.js 18+ | [nodejs.org](https://nodejs.org) | 3 min |
| 9 | Python 3.10+ | [python.org](https://python.org) | 3 min |
| 10 | Obsidian (optional) | [obsidian.md](https://obsidian.md) | 5 min |

> ⚠️ **Tokens are secrets.** Never paste them into files tracked by git.
> Store them in GitHub Secrets only. → [docs/security.md](docs/security.md)

---

## Why Cloudflare? (free tier is enough)

Cloudflare KV free plan covers this workflow easily:

| Resource | Free allowance | This template uses |
|----------|---------------|--------------------|
| KV reads | 100,000 / day | ~10 / day |
| KV writes | 1,000 / day | ~5 / day |
| KV storage | 1 GB | < 1 MB |
| Worker requests | 100,000 / day | handled by quiz-publish-bot |

No credit card required. → [cloudflare.com/plans](https://www.cloudflare.com/plans/)

---

## Quick start

### 1. Use this template

Click **Use this template → Create a new repository** on GitHub.

Or clone:

**Mac**
```bash
git clone https://github.com/wjdghtls95/blog-starter.git my-blog
cd my-blog
git remote set-url origin https://github.com/YOUR_USERNAME/my-blog.git
git push -u origin main
```

**Windows (PowerShell)**
```powershell
git clone https://github.com/wjdghtls95/blog-starter.git my-blog
cd my-blog
git remote set-url origin https://github.com/YOUR_USERNAME/my-blog.git
git push -u origin main
```

### 2. Choose your blog UI

This template is framework-agnostic — pick a theme or build your own. See [docs/theming.md](docs/theming.md) for full options:

| Option | Style | Docs |
|--------|-------|------|
| [AstroPaper](https://astro-paper.pages.dev) | Minimal, dark/light, built-in search | [github.com/satnaing/astro-paper](https://github.com/satnaing/astro-paper) |
| [Astro Nano](https://astro-nano-demo.vercel.app) | Ultra-minimal, zero JS | [github.com/markhorn-dev/astro-nano](https://github.com/markhorn-dev/astro-nano) |
| [Astro Wind](https://astrowind.vercel.app) | Landing + blog, Tailwind | [github.com/onwidget/astrowind](https://github.com/onwidget/astrowind) |
| [Tailwind CSS](https://tailwindcss.com/docs) | Build your own | [tailwindcss.com/docs](https://tailwindcss.com/docs) |
| [shadcn/ui](https://ui.shadcn.com/docs/installation/astro) | React components | [ui.shadcn.com](https://ui.shadcn.com) |
| [Daisy UI](https://daisyui.com/docs/install/) | Pre-built Tailwind themes | [daisyui.com](https://daisyui.com) |

> Want a ready-made blog with custom design? → Use a full Astro theme as your base and put the files from this template on top.
> If you build a custom blog view template, consider creating a separate `blog-template` repo for the design layer.

**Install your chosen theme (Mac / Windows — same command):**
```bash
npm create astro@latest -- --template satnaing/astro-paper .
npm install
```

### 3. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Value |
|--------|-------|
| `OPENAI_API_KEY` | From checklist #2 |
| `TELEGRAM_BOT_TOKEN` | From checklist #3 |
| `TELEGRAM_CHAT_ID` | From checklist #4 |
| `CF_ACCOUNT_ID` | From Cloudflare dashboard URL |
| `CF_API_TOKEN` | From checklist #6 |
| `KV_NAMESPACE_ID` | From checklist #7 |

### 4. Enable GitHub Pages

Repository **Settings → Pages → Source**: set to **GitHub Actions**.

### 5. Deploy the Telegram bot

Deploy [quiz-publish-bot](https://github.com/wjdghtls95/quiz-publish-bot) separately — it handles all bot commands.

Key commands once deployed:

| Korean | English | What it does |
|--------|---------|-------------|
| `/퀴즈` | `/quiz` | Start quiz immediately |
| `/건너뛰기` | `/skip` | Skip quiz, publish tomorrow 08:00 |
| `/발행` | `/publish` | Publish immediately |
| `/큐` | `/queue` | Show pending drafts |
| `/먼저 N` | `/first N` | Move draft #N to front (e.g. `/first 2`) |
| `/언어 ko\|en` | `/lang ko\|en` | Switch bot language |

Default language is Korean. Both language variants always work.

Send `/start` once after deployment — the bot automatically registers commands for `/` autocomplete. Switching language with `/lang en` also updates the autocomplete list instantly.

### 6. Write your first draft

**Mac**
```bash
cat > drafts/my-first-post.md << 'EOF'
---
title: My First Post
date: 2026-07-23
description: A short summary for SEO
tags: [typescript]
source: path/to/original-notes.md
---

## Introduction

Content goes here.
EOF

git add drafts/my-first-post.md
git commit -m "draft: my first post"
git push
```

**Windows (PowerShell)**
```powershell
@"
---
title: My First Post
date: 2026-07-23
description: A short summary for SEO
tags: [typescript]
source: path/to/original-notes.md
---

## Introduction

Content goes here.
"@ | Out-File -FilePath drafts\my-first-post.md -Encoding UTF8

git add drafts/my-first-post.md
git commit -m "draft: my first post"
git push
```

GitHub Actions will generate a quiz and send a Telegram notification.

---

## Directory structure

```
blog-starter/
├── .github/workflows/
│   ├── quiz-pipeline.yml    # triggers on push to drafts/
│   ├── publish.yml          # triggers via Telegram /publish
│   └── direct-publish.yml   # triggers on push to direct/ (no quiz)
├── docs/
│   ├── README.ko.md         # 한국어 가이드
│   ├── SETUP.md             # Detailed setup (EN)
│   ├── SETUP.ko.md          # 상세 설치 가이드 (KO)
│   ├── theming.md           # UI library options
│   └── security.md          # Token security rules
├── drafts/                  # Write here — push triggers quiz generation
├── direct/                  # Push here to publish without quiz
├── scripts/
│   └── generate-quiz.py     # Quiz generation script (runs in GitHub Actions)
├── src/
│   ├── content/posts/       # Published posts live here
│   └── assets/blog/         # Post images
├── .env.example             # Environment variable reference
├── .gitignore               # blog-queue.md is gitignored
└── blog-queue.template.md   # Copy to blog-queue.md (stays local)
```

---

## Post frontmatter

```markdown
---
title: Post Title
date: 2026-07-23
description: One-line SEO summary
tags: [typescript, nestjs]
source: path/to/original-notes.md   # shown in Telegram notification
---
```

---

## Workflows

| Workflow | Trigger | What it does |
|----------|---------|-------------|
| `quiz-pipeline` | Push to `drafts/` | Generates quiz, notifies Telegram |
| `publish` | Telegram `/publish` | Moves draft → posts, builds and deploys |
| `direct-publish` | Push to `direct/` | Publishes directly without quiz |

---

## Docs

- [docs/README.ko.md](docs/README.ko.md) — 한국어 가이드
- [docs/SETUP.md](docs/SETUP.md) — Detailed setup guide (EN)
- [docs/SETUP.ko.md](docs/SETUP.ko.md) — 상세 설치 가이드 (한국어)
- [docs/theming.md](docs/theming.md) — UI library options with docs links
- [docs/security.md](docs/security.md) — Token security rules

---

## Related

- [quiz-publish-bot](https://github.com/wjdghtls95/quiz-publish-bot) — the Telegram bot that manages the publish queue

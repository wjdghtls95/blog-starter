# blog-starter

> A GitHub Pages blog template with automated quiz generation and Telegram notifications.
> Write a draft → push → quiz is auto-generated → publish via Telegram bot.

---

## How it works

```
You write a draft in drafts/
    ↓
Push to GitHub
    ↓
GitHub Actions: generate-quiz.py runs
    ↓
Quiz stored in Cloudflare KV
Telegram notification sent to you
    ↓
You answer the quiz in Telegram
    ↓
/publish command → post moves to src/content/posts/
Blog builds and deploys to GitHub Pages
```

---

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Node.js 18+ | Astro build | [nodejs.org](https://nodejs.org) |
| pnpm | Package manager | `npm install -g pnpm` |
| Python 3.10+ | Quiz generation script | [python.org](https://python.org) |
| GitHub account | Hosting | [github.com](https://github.com) |
| OpenAI API key | Quiz generation | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| Telegram bot | Notifications + commands | [@BotFather](https://t.me/BotFather) |
| Cloudflare account (free) | KV storage for quiz queue | [dash.cloudflare.com](https://dash.cloudflare.com) |

---

## Quick start

### 1. Use this template

Click **Use this template** → **Create a new repository** on GitHub.

Or clone:
```bash
git clone https://github.com/YOUR_USERNAME/blog-starter.git my-blog
cd my-blog
```

### 2. Choose your UI

See [docs/theming.md](docs/theming.md) for options:

| Option | Best for |
|--------|---------|
| [AstroPaper](https://astro-paper.pages.dev) | Minimal dev blog, built-in search |
| [Astro Nano](https://astro-nano-demo.vercel.app) | Ultra-minimal, zero JS |
| [Astro Wind](https://astrowind.vercel.app) | Landing page + blog |
| [Tailwind CSS](https://tailwindcss.com/docs) | Build your own |
| [shadcn/ui](https://ui.shadcn.com/docs/installation/astro) | React components in Astro |
| [Daisy UI](https://daisyui.com/docs/install/) | Pre-made Tailwind themes |

### 3. Set up GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Where to get it |
|--------|----------------|
| `OPENAI_API_KEY` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `TELEGRAM_BOT_TOKEN` | [@BotFather](https://t.me/BotFather) → `/newbot` |
| `TELEGRAM_CHAT_ID` | Message [@userinfobot](https://t.me/userinfobot) |
| `CF_ACCOUNT_ID` | Cloudflare dashboard URL |
| `CF_API_TOKEN` | Cloudflare → My Profile → API Tokens |
| `KV_NAMESPACE_ID` | Workers & Pages → KV → your namespace ID |

> ⚠️ See [docs/security.md](docs/security.md) — never commit real tokens to git.

### 4. Enable GitHub Pages

Repository **Settings → Pages → Source**: set to **GitHub Actions**.

### 5. Set up the quiz bot

Deploy [quiz-publish-bot](https://github.com/YOUR_USERNAME/quiz-publish-bot) separately — it handles the Telegram bot commands and publishes posts.

### 6. Write your first post

```bash
# Create a draft
cat > drafts/my-first-post.md << 'EOF'
---
title: My First Post
date: 2026-07-23
source: Obsidian/path/to/original.md
---

Your content here.
EOF

git add drafts/my-first-post.md
git commit -m "draft: my first post"
git push
```

GitHub Actions will generate a quiz and notify you on Telegram.

---

## Directory structure

```
blog-starter/
├── .github/workflows/
│   ├── quiz-pipeline.yml    # triggers on push to drafts/
│   ├── publish.yml          # triggers via Telegram bot /publish
│   └── direct-publish.yml   # triggers on push to direct/
├── docs/
│   ├── theming.md           # UI library options
│   └── security.md          # Token security guide
├── drafts/                  # Write here — push triggers quiz generation
├── direct/                  # Push here to bypass quiz and publish directly
├── scripts/
│   └── generate-quiz.py     # Quiz generation script
├── src/
│   ├── content/posts/       # Published posts live here
│   └── assets/blog/         # Images for posts
├── .env.example             # Environment variable reference
├── .gitignore
└── blog-queue.template.md   # Copy to blog-queue.md (gitignored)
```

---

## Post frontmatter

```markdown
---
title: Post Title
date: 2026-07-23
description: One-line summary for SEO
tags: [typescript, nestjs]
source: Obsidian/path/to/source.md   # shown in Telegram notification
---
```

---

## Workflows

| Workflow | Trigger | What it does |
|----------|---------|-------------|
| `quiz-pipeline` | Push to `drafts/` | Generates quiz, notifies Telegram |
| `publish` | Telegram `/publish` command | Moves draft to posts, builds site |
| `direct-publish` | Push to `direct/` | Publishes without quiz |

---

## Related

- [quiz-publish-bot](https://github.com/wjdghtls95/quiz-publish-bot) — the Telegram bot that manages the publish queue

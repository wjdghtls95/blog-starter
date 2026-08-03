# blog-starter

[🇰🇷 한국어](docs/README.ko.md)

> A GitHub Pages blog template with Telegram publish workflow and spaced repetition review.
> Write a draft → publish instantly → get a Telegram prompt 7 days later to re-explain the concept.

---

## What this does

```
Write a draft in drafts/
    ↓
Push to GitHub → trigger publish.yml
    ↓
GitHub Actions: draft moves to src/content/blog/
Astro builds → deploys to GitHub Pages
    ↓
Telegram: publish notification with live URL
    ↓
7 days later: Telegram asks you to re-explain the concept in your own words
```

No quiz before publishing. Write when ready, review after 7 days.

---

## Before you start — checklist

Gather these before running any commands:

| # | What you need | Where to get it | Takes |
|---|--------------|-----------------|-------|
| 1 | GitHub account | [github.com](https://github.com) | 2 min |
| 2 | Telegram bot token | [@BotFather](https://t.me/BotFather) → `/newbot` | 2 min |
| 3 | Telegram chat ID | [@userinfobot](https://t.me/userinfobot) | 1 min |
| 4 | Cloudflare account (free) | [dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up) | 3 min |
| 5 | Cloudflare API token | Cloudflare → My Profile → API Tokens | 2 min |
| 6 | KV namespace ID | Workers & Pages → KV → Create namespace | 2 min |
| 7 | Node.js 18+ | [nodejs.org](https://nodejs.org) | 3 min |

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

Pick any free Astro theme and use it as the base — then put the files from this template on top.

→ **[astro.build/themes](https://astro.build/themes/)** (filter by Free)

**Install your chosen theme (Mac / Windows — same command):**
```bash
npm create astro@latest -- --template <theme-name> .
npm install
```

### 3. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Value |
|--------|-------|
| `TELEGRAM_BOT_TOKEN` | From checklist #2 |
| `TELEGRAM_CHAT_ID` | From checklist #3 |
| `CF_ACCOUNT_ID` | From Cloudflare dashboard URL |
| `CF_API_TOKEN` | From checklist #5 |
| `KV_NAMESPACE_ID` | From checklist #6 |

### 4. Enable GitHub Pages

Repository **Settings → Pages → Source**: set to **GitHub Actions**.

### 5. Deploy the Telegram bot

Deploy [quiz-publish-bot](https://github.com/wjdghtls95/quiz-publish-bot) separately — it handles publish notifications and 7-day review scheduling.

Key commands once deployed:

| Command | What it does |
|---------|-------------|
| `/start` | Bot status |
| `/status` | Full status — review queue, last error |

### 6. Write your first draft

**Mac**
```bash
cat > drafts/my-first-post.md << 'EOF'
---
title: My First Post
date: 2026-08-03
description: A short summary for SEO
tags: [typescript]
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
date: 2026-08-03
description: A short summary for SEO
tags: [typescript]
---

## Introduction

Content goes here.
"@ | Out-File -FilePath drafts\my-first-post.md -Encoding UTF8

git add drafts/my-first-post.md
git commit -m "draft: my first post"
git push
```

Then trigger `publish.yml` — either via Telegram bot or GitHub CLI:

```bash
gh workflow run publish.yml -f draft_file=drafts/my-first-post.md
```

---

## Directory structure

```
blog-starter/
├── .github/workflows/
│   ├── publish.yml          # triggered by bot or manually — moves draft → blog, builds, deploys
│   ├── deploy.yml           # Astro build + GitHub Pages deploy
│   └── direct-publish.yml   # push to direct/ to publish without bot trigger
├── docs/
│   ├── README.ko.md         # 한국어 가이드
│   ├── SETUP.md             # Detailed setup (EN)
│   ├── SETUP.ko.md          # 상세 설치 가이드 (KO)
│   ├── theming.md           # UI library options
│   └── security.md          # Token security rules
├── drafts/                  # Write here — push, then trigger publish.yml
├── direct/                  # Push here to publish immediately (no bot trigger)
├── src/
│   ├── content/blog/        # Published posts live here
│   └── assets/blog/         # Post images
└── .gitignore
```

---

## Post frontmatter

```markdown
---
title: Post Title
date: 2026-08-03
description: One-line SEO summary
tags: [typescript, nestjs]
---
```

---

## Workflows

| Workflow | Trigger | What it does |
|----------|---------|-------------|
| `publish` | Bot command or `gh workflow run` | Moves draft → blog, builds and deploys |
| `deploy` | Push to main or `workflow_dispatch` | Astro build + GitHub Pages deploy |
| `direct-publish` | Push to `direct/` | Publishes immediately without bot trigger |

---

## Docs

- [docs/README.ko.md](docs/README.ko.md) — 한국어 가이드
- [docs/SETUP.md](docs/SETUP.md) — Detailed setup guide (EN)
- [docs/SETUP.ko.md](docs/SETUP.ko.md) — 상세 설치 가이드 (한국어)
- [docs/theming.md](docs/theming.md) — UI library options with docs links
- [docs/security.md](docs/security.md) — Token security rules

---

## Related

- [quiz-publish-bot](https://github.com/wjdghtls95/quiz-publish-bot) — the Telegram bot that handles publish notifications and review scheduling

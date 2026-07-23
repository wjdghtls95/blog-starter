# Setup Guide

> **⚠️ Security first:** Never paste real tokens into files tracked by git.
> All secrets go into GitHub Repository Secrets only. See [docs/security.md](docs/security.md).

---

## Step 1 — Install required tools

### Mac

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js and Python
brew install node python

# Install pnpm
npm install -g pnpm

# Verify
node --version    # must be 18+
python3 --version # must be 3.10+
pnpm --version
```

### Windows

```powershell
# winget is included in Windows 11. If missing, install 'App Installer' from Microsoft Store.

# Install Node.js and Python
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12

# Restart terminal, then install pnpm
npm install -g pnpm

# Verify
node --version
python --version
pnpm --version
```

---

## Step 2 — Create a Telegram bot

1. Open Telegram → search **@BotFather** → send `/start`
2. Send `/newbot`
3. Enter a name (e.g., `My Blog Bot`)
4. Enter a username ending in `bot` (e.g., `myblog_bot`)
5. Copy the **token** — looks like `123456789:ABCdef...`

> ⚠️ Anyone with this token can control your bot. Store it in GitHub Secrets only.

---

## Step 3 — Get your Telegram chat ID

1. Message **@userinfobot** on Telegram
2. It replies with your **Id** — copy it

---

## Step 4 — Get an OpenAI API key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click **Create new secret key**
3. Copy it — starts with `sk-`

> ⚠️ This key is shown once. Save it immediately.

---

## Step 5 — Get a GitHub Personal Access Token

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Set expiration (90 days recommended)
4. Check **repo** scope only
5. Click **Generate token** and copy

> ⚠️ This token has write access to your repositories. Never commit it.

---

## Step 6 — Set up Cloudflare KV

1. Sign up at [dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up) (free)
2. Go to **Workers & Pages → KV**
3. Click **Create namespace** → name it `QUIZ_SESSIONS`
4. Copy the **Namespace ID**
5. Go to **My Profile → API Tokens → Create Token**
6. Use **Edit Cloudflare Workers** template → click **Create Token**
7. Copy the **API Token**
8. Find your **Account ID** in the right sidebar of the dashboard

---

## Step 7 — Create the GitHub repository

1. Go to [github.com](https://github.com) → click **New repository**
2. Name it (e.g., `my-blog` or `username.github.io`)
3. Set to **Public**
4. Click **Create repository**

```bash
# Clone this template and push to your new repo
git clone https://github.com/YOUR_USERNAME/blog-starter.git my-blog
cd my-blog
git remote set-url origin https://github.com/YOUR_USERNAME/my-blog.git
git push -u origin main
```

---

## Step 8 — Add GitHub Secrets

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

Add each of these:

| Name | Value |
|------|-------|
| `OPENAI_API_KEY` | From Step 4 |
| `TELEGRAM_BOT_TOKEN` | From Step 2 |
| `TELEGRAM_CHAT_ID` | From Step 3 |
| `CF_ACCOUNT_ID` | From Step 6 |
| `CF_API_TOKEN` | From Step 6 |
| `KV_NAMESPACE_ID` | From Step 6 |

---

## Step 9 — Choose and install your UI

See [docs/theming.md](docs/theming.md) for full options. Quickest start:

```bash
cd my-blog

# Option A — AstroPaper (recommended for dev blogs)
npm create astro@latest -- --template satnaing/astro-paper .
npm install

# Option B — start from scratch
npm create astro@latest .
# Select "Empty" template
```

---

## Step 10 — Enable GitHub Pages

1. Go to your repo → **Settings → Pages**
2. Under **Source**, select **GitHub Actions**
3. Save

---

## Step 11 — Test the pipeline

```bash
# Create a test draft
mkdir -p drafts
cat > drafts/hello-world.md << 'EOF'
---
title: Hello World
date: 2026-07-23
source: test/hello-world.md
---

## Introduction

This is my first post.

## Main content

Testing the quiz pipeline.
EOF

git add drafts/hello-world.md
git commit -m "draft: hello world"
git push
```

Watch **Actions** tab in GitHub — the `Quiz Pipeline` workflow should run.
Check Telegram for the notification.

---

## Step 12 — Set up the Telegram bot

Deploy [quiz-publish-bot](https://github.com/YOUR_USERNAME/quiz-publish-bot) following its SETUP.md.
The bot handles `/publish`, `/quiz`, `/skip`, `/postpone` commands.

---

## Troubleshooting

**Quiz Pipeline workflow failed**

Check the Actions log. Common causes:
- Missing GitHub Secret — verify all 6 secrets are added
- Cloudflare KV namespace ID is wrong — check against the dashboard

**No Telegram notification**

- Verify `TELEGRAM_BOT_TOKEN` is correct
- Verify `TELEGRAM_CHAT_ID` — get it from @userinfobot

**GitHub Pages not building**

- Check **Settings → Pages → Source** is set to GitHub Actions (not a branch)
- Check the `publish.yml` workflow log for errors

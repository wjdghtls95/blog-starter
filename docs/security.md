# Security Guide

## Token handling rules

| Token | Storage | Never |
|-------|---------|-------|
| `OPENAI_API_KEY` | GitHub Secrets only | Hardcode in script, commit to git |
| `TELEGRAM_BOT_TOKEN` | GitHub Secrets only | Share in public channels |
| `CF_API_TOKEN` | GitHub Secrets only | Put in wrangler.jsonc or .env |
| `CF_ACCOUNT_ID` | GitHub Secrets only | Commit to public repo |
| `KV_NAMESPACE_ID` | GitHub Secrets only | Expose in client-side code |

## Why tokens must stay secret

- **OPENAI_API_KEY**: Anyone who has this can make API calls at your expense. OpenAI charges per token — a leaked key can cost hundreds of dollars.
- **TELEGRAM_BOT_TOKEN**: Full control over your bot. Anyone can read messages sent to it and send messages as your bot.
- **CF_API_TOKEN**: Write access to your Cloudflare KV storage. Can read or delete quiz data.

## How to store secrets in GitHub Actions

1. Go to your repository → **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Enter the name (e.g., `OPENAI_API_KEY`) and value
4. Click **Add secret**

The value is encrypted and never shown again. Reference it in workflows as `${{ secrets.OPENAI_API_KEY }}`.

## If a token is leaked

Act immediately — every minute a leaked token is live, it can be used.

1. **Revoke the token** at the issuing service (OpenAI, Telegram BotFather, GitHub, Cloudflare)
2. **Generate a new token**
3. **Update GitHub Secrets** with the new token
4. **Remove the secret from git history** if it was committed:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/file" \
     --prune-empty --tag-name-filter cat -- --all
   git push origin --force --all
   ```
   Or use [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) which is faster.
5. **Assume it was compromised** — check service logs for unauthorized usage.

## Checking for accidental commits

Before pushing, scan for secrets:

```bash
# Simple grep (run from repo root)
grep -r "sk-" . --include="*.py" --include="*.js" --include="*.json"
grep -r "AAAA" . --include="*.py" --include="*.js"  # Telegram token pattern
```

Or install [gitleaks](https://github.com/gitleaks/gitleaks) for automated scanning:

```bash
# Mac
brew install gitleaks
gitleaks detect --source .

# Windows
winget install gitleaks
gitleaks detect --source .
```

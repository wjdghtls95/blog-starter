# 설치 가이드

> **⚠️ 보안 우선:** 실제 토큰을 git이 추적하는 파일에 절대 붙여넣지 마세요.
> 모든 시크릿은 GitHub Repository Secrets에만 저장합니다. [docs/security.md](docs/security.md) 참고.

---

## 1단계 — 필수 도구 설치

### Mac

```bash
# Homebrew 설치 (없으면)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Node.js, Python 설치
brew install node python

# pnpm 설치
npm install -g pnpm

# 확인
node --version    # 18 이상이어야 함
python3 --version # 3.10 이상이어야 함
pnpm --version
```

### Windows

```powershell
# winget은 Windows 11에 기본 포함. 없으면 Microsoft Store에서 'App Installer' 설치.

# Node.js, Python 설치
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12

# 터미널 재시작 후 pnpm 설치
npm install -g pnpm

# 확인
node --version
python --version
pnpm --version
```

---

## 2단계 — Telegram 봇 생성

1. Telegram에서 **@BotFather** 검색 → `/start` 전송
2. `/newbot` 전송
3. 봇 이름 입력 (예: `내 블로그 봇`)
4. 봇 유저네임 입력 (반드시 `bot`으로 끝나야 함, 예: `myblog_bot`)
5. **토큰** 복사 — `123456789:ABCdef...` 형태

> ⚠️ 이 토큰이 있으면 누구나 내 봇을 제어할 수 있습니다. GitHub Secrets에만 저장하세요.

---

## 3단계 — Telegram 채팅 ID 확인

1. Telegram에서 **@userinfobot** 에게 메시지 전송
2. 봇이 **Id** 를 알려줍니다 — 복사

---

## 4단계 — OpenAI API 키 발급

1. [platform.openai.com/api-keys](https://platform.openai.com/api-keys) 접속
2. **Create new secret key** 클릭
3. 키 복사 — `sk-`로 시작

> ⚠️ 이 키는 한 번만 볼 수 있습니다. 즉시 안전한 곳에 저장하세요.

---

## 5단계 — GitHub Personal Access Token 발급

1. [github.com/settings/tokens](https://github.com/settings/tokens) 접속
2. **Generate new token (classic)** 클릭
3. 만료일 설정 (90일 권장)
4. **repo** 권한만 체크
5. **Generate token** 클릭 후 복사

> ⚠️ 이 토큰은 내 레포지토리에 쓰기 권한이 있습니다. 절대 커밋하지 마세요.

---

## 6단계 — Cloudflare KV 설정

1. [dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up) 에서 무료 계정 생성
2. **Workers & Pages → KV** 이동
3. **Create namespace** 클릭 → 이름을 `QUIZ_SESSIONS` 으로 설정
4. **Namespace ID** 복사
5. **My Profile → API Tokens → Create Token** 이동
6. **Edit Cloudflare Workers** 템플릿 선택 → **Create Token**
7. **API Token** 복사
8. 대시보드 오른쪽 사이드바에서 **Account ID** 확인

---

## 7단계 — GitHub 레포지토리 생성

1. [github.com](https://github.com) → **New repository** 클릭
2. 이름 설정 (예: `my-blog` 또는 `username.github.io`)
3. **Public** 으로 설정
4. **Create repository** 클릭

```bash
# 이 템플릿을 클론하고 새 레포에 push
git clone https://github.com/YOUR_USERNAME/blog-starter.git my-blog
cd my-blog
git remote set-url origin https://github.com/YOUR_USERNAME/my-blog.git
git push -u origin main
```

---

## 8단계 — GitHub Secrets 추가

레포 → **Settings → Secrets and variables → Actions → New repository secret**

아래 6개를 모두 추가:

| 이름 | 값 |
|------|-----|
| `OPENAI_API_KEY` | 4단계에서 발급 |
| `TELEGRAM_BOT_TOKEN` | 2단계에서 발급 |
| `TELEGRAM_CHAT_ID` | 3단계에서 확인 |
| `CF_ACCOUNT_ID` | 6단계에서 확인 |
| `CF_API_TOKEN` | 6단계에서 발급 |
| `KV_NAMESPACE_ID` | 6단계에서 확인 |

---

## 9단계 — UI 선택 및 설치

전체 옵션은 [docs/theming.md](docs/theming.md) 참고. 가장 빠른 시작:

```bash
cd my-blog

# A안 — AstroPaper (개발 블로그에 추천)
npm create astro@latest -- --template satnaing/astro-paper .
npm install

# B안 — 처음부터 직접 만들기
npm create astro@latest .
# "Empty" 템플릿 선택
```

---

## 10단계 — GitHub Pages 활성화

1. 레포 → **Settings → Pages**
2. **Source** 를 **GitHub Actions** 로 설정
3. 저장

---

## 11단계 — 파이프라인 테스트

```bash
# 테스트 초안 생성
mkdir -p drafts
cat > drafts/hello-world.md << 'EOF'
---
title: 헬로 월드
date: 2026-07-23
source: test/hello-world.md
---

## 소개

첫 번째 글입니다.

## 본문

퀴즈 파이프라인 테스트.
EOF

git add drafts/hello-world.md
git commit -m "draft: 헬로 월드"
git push
```

GitHub **Actions** 탭에서 `Quiz Pipeline` 워크플로우가 실행되는지 확인하세요.
Telegram으로 알림이 오면 성공입니다.

---

## 12단계 — Telegram 봇 설정

[quiz-publish-bot](https://github.com/YOUR_USERNAME/quiz-publish-bot) 을 해당 레포의 SETUP.ko.md 를 따라 배포하세요.
봇이 `/publish`, `/quiz`, `/skip`, `/postpone` 명령어를 처리합니다.

---

## 문제 해결

**Quiz Pipeline 워크플로우 실패**

Actions 로그 확인. 주요 원인:
- GitHub Secret 누락 — 6개 Secret이 모두 추가됐는지 확인
- Cloudflare KV Namespace ID 오류 — 대시보드에서 재확인

**Telegram 알림이 오지 않음**

- `TELEGRAM_BOT_TOKEN` 이 정확한지 확인
- `TELEGRAM_CHAT_ID` — @userinfobot 에서 다시 확인

**GitHub Pages 빌드 실패**

- **Settings → Pages → Source** 가 GitHub Actions 로 설정됐는지 확인
- `publish.yml` 워크플로우 로그에서 오류 확인

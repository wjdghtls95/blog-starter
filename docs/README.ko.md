# blog-starter

[🇺🇸 English](../README.md)

> Telegram 발행 알림과 발행 후 7일 복습이 포함된 GitHub Pages 블로그 템플릿.
> 초안 작성 → 즉시 발행 → 7일 후 Telegram으로 개념 재설명 요청.

---

## 동작 방식

```
drafts/ 에 초안 작성
    ↓
GitHub에 push → publish.yml 트리거
    ↓
GitHub Actions: 초안이 src/content/blog/ 로 이동
Astro 빌드 → GitHub Pages 배포
    ↓
Telegram: 발행 완료 알림 + URL
    ↓
7일 후: Telegram이 "이 개념을 다시 설명해보세요" 질문
```

발행 전 퀴즈 없음. 글이 준비되면 발행하고, 복습은 7일 후에.

---

## 시작 전 체크리스트

명령어 실행 전에 아래를 먼저 준비하세요:

| # | 필요한 것 | 발급처 | 소요 시간 |
|---|----------|--------|---------|
| 1 | GitHub 계정 | [github.com](https://github.com) | 2분 |
| 2 | Telegram 봇 토큰 | [@BotFather](https://t.me/BotFather) → `/newbot` | 2분 |
| 3 | Telegram 채팅 ID | [@userinfobot](https://t.me/userinfobot) | 1분 |
| 4 | Cloudflare 계정 (무료) | [dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up) | 3분 |
| 5 | Cloudflare API 토큰 | Cloudflare → My Profile → API Tokens | 2분 |
| 6 | KV 네임스페이스 ID | Workers & Pages → KV → 네임스페이스 생성 | 2분 |
| 7 | Node.js 18+ | [nodejs.org](https://nodejs.org) | 3분 |

> ⚠️ **토큰은 비밀입니다.** git이 추적하는 파일에 절대 붙여넣지 마세요.
> GitHub Secrets에만 저장하세요. → [security.md](security.md)

---

## Cloudflare를 쓰는 이유 (무료 플랜으로 충분)

Cloudflare KV 무료 플랜이 이 워크플로우를 충분히 감당합니다:

| 리소스 | 무료 한도 | 이 템플릿 사용량 |
|--------|----------|--------------|
| KV 읽기 | 하루 100,000회 | 하루 ~10회 |
| KV 쓰기 | 하루 1,000회 | 하루 ~5회 |
| KV 저장 용량 | 1 GB | 1 MB 미만 |
| Worker 요청 수 | 하루 100,000회 | quiz-publish-bot 담당 |

신용카드 없이 무료 플랜 사용 가능. → [cloudflare.com/plans](https://www.cloudflare.com/plans/)

---

## 빠른 시작

### 1. 이 템플릿 사용

GitHub에서 **Use this template → Create a new repository** 클릭.

또는 직접 클론:

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

### 2. 블로그 UI 선택

Astro 테마 중 하나를 고르거나 직접 만드세요. → [astro.build/themes](https://astro.build/themes/) (Free 필터)

**테마 설치 (Mac / Windows 동일):**
```bash
npm create astro@latest -- --template <theme-name> .
npm install
```

### 3. GitHub Secrets 추가

레포 → **Settings → Secrets and variables → Actions → New repository secret**

| Secret | 값 |
|--------|-----|
| `TELEGRAM_BOT_TOKEN` | 체크리스트 #2 |
| `TELEGRAM_CHAT_ID` | 체크리스트 #3 |
| `CF_ACCOUNT_ID` | Cloudflare 대시보드 URL |
| `CF_API_TOKEN` | 체크리스트 #5 |
| `KV_NAMESPACE_ID` | 체크리스트 #6 |

### 4. GitHub Pages 활성화

레포 **Settings → Pages → Source**: **GitHub Actions** 로 설정.

### 5. Telegram 봇 배포

[quiz-publish-bot](https://github.com/wjdghtls95/quiz-publish-bot) 을 별도로 배포하세요 — 발행 알림과 7일 복습 스케줄을 담당합니다.

배포 후 사용 가능한 명령어:

| 명령어 | 기능 |
|--------|------|
| `/start` | 봇 상태 확인 |
| `/status` `/상태` | 현황 — 복습 큐, 마지막 에러 |

### 6. 첫 초안 작성

**Mac**
```bash
cat > drafts/my-first-post.md << 'EOF'
---
title: 첫 번째 글
date: 2026-08-03
description: SEO용 한 줄 요약
tags: [typescript]
---

## 소개

내용을 여기에 작성하세요.
EOF

git add drafts/my-first-post.md
git commit -m "draft: 첫 번째 글"
git push
```

**Windows (PowerShell)**
```powershell
@"
---
title: 첫 번째 글
date: 2026-08-03
description: SEO용 한 줄 요약
tags: [typescript]
---

## 소개

내용을 여기에 작성하세요.
"@ | Out-File -FilePath drafts\my-first-post.md -Encoding UTF8

git add drafts/my-first-post.md
git commit -m "draft: 첫 번째 글"
git push
```

그 다음 `publish.yml` 트리거 — Telegram 봇 명령어 또는 GitHub CLI:

```bash
gh workflow run publish.yml -f draft_file=drafts/my-first-post.md
```

---

## 디렉토리 구조

```
blog-starter/
├── .github/workflows/
│   ├── publish.yml          # 봇 또는 수동 트리거 — 초안 → blog 이동, 빌드, 배포
│   ├── deploy.yml           # Astro 빌드 + GitHub Pages 배포
│   └── direct-publish.yml   # direct/ push 시 즉시 발행 (봇 트리거 없이)
├── docs/
│   ├── README.ko.md         # 한국어 가이드 (현재 파일)
│   ├── SETUP.md             # 상세 설치 가이드 (영어)
│   ├── SETUP.ko.md          # 상세 설치 가이드 (한국어)
│   ├── theming.md           # UI 라이브러리 선택 가이드
│   └── security.md          # 토큰 보안 규칙
├── drafts/                  # 초안 작성 위치 → publish.yml 트리거
├── direct/                  # 봇 트리거 없이 즉시 발행
├── src/
│   ├── content/blog/        # 발행된 글
│   └── assets/blog/         # 이미지
└── .gitignore
```

---

## 프론트매터 형식

```markdown
---
title: 글 제목
date: 2026-08-03
description: SEO용 한 줄 요약
tags: [typescript, nestjs]
---
```

---

## 워크플로우

| 워크플로우 | 트리거 | 동작 |
|-----------|--------|------|
| `publish` | 봇 명령어 또는 `gh workflow run` | 초안 → blog 이동, 빌드 및 배포 |
| `deploy` | main push 또는 `workflow_dispatch` | Astro 빌드 + GitHub Pages 배포 |
| `direct-publish` | `direct/` push | 봇 트리거 없이 즉시 발행 |

---

## 관련 레포

- [quiz-publish-bot](https://github.com/wjdghtls95/quiz-publish-bot) — 발행 알림과 복습 스케줄을 담당하는 Telegram 봇

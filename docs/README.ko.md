# blog-starter

[🇺🇸 English](../README.md)

> 퀴즈 자동 생성 + Telegram 알림이 포함된 GitHub Pages 블로그 템플릿.
> 초안 작성 → push → 퀴즈 자동 생성 → Telegram에서 답하기 → 포스트 발행.

---

## 동작 방식

```
drafts/ 에 초안 작성
    ↓
GitHub에 push
    ↓
GitHub Actions: OpenAI로 퀴즈 생성 → Cloudflare KV 저장
Telegram 알림 수신
    ↓
Telegram에서 퀴즈 풀기 (quiz-publish-bot 담당)
    ↓
/publish → 초안이 src/content/posts/ 로 이동
블로그 빌드 후 GitHub Pages 배포
```

---

## 시작 전 체크리스트

명령어 실행 전에 아래를 먼저 준비하세요:

| # | 필요한 것 | 발급처 | 소요 시간 |
|---|----------|--------|---------|
| 1 | GitHub 계정 | [github.com](https://github.com) | 2분 |
| 2 | OpenAI API 키 | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | 2분 |
| 3 | Telegram 봇 토큰 | [@BotFather](https://t.me/BotFather) → `/newbot` | 2분 |
| 4 | Telegram 채팅 ID | [@userinfobot](https://t.me/userinfobot) | 1분 |
| 5 | Cloudflare 계정 (무료) | [dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up) | 3분 |
| 6 | Cloudflare API 토큰 | Cloudflare → My Profile → API Tokens | 2분 |
| 7 | KV 네임스페이스 ID | Workers & Pages → KV → 네임스페이스 생성 | 2분 |
| 8 | Node.js 18+ | [nodejs.org](https://nodejs.org) | 3분 |
| 9 | Python 3.10+ | [python.org](https://python.org) | 3분 |

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

이 템플릿은 프레임워크에 종속되지 않습니다. 테마를 고르거나 직접 만드세요. 전체 옵션 → [theming.md](theming.md)

| 옵션 | 스타일 | 문서 |
|------|--------|------|
| [AstroPaper](https://astro-paper.pages.dev) | 미니멀, 다크/라이트, 검색 포함 | [github.com/satnaing/astro-paper](https://github.com/satnaing/astro-paper) |
| [Astro Nano](https://astro-nano-demo.vercel.app) | 극단적 미니멀, JS 없음 | [github.com/markhorn-dev/astro-nano](https://github.com/markhorn-dev/astro-nano) |
| [Astro Wind](https://astrowind.vercel.app) | 랜딩 + 블로그, Tailwind | [github.com/onwidget/astrowind](https://github.com/onwidget/astrowind) |
| [Tailwind CSS](https://tailwindcss.com/docs) | 직접 커스텀 | [tailwindcss.com/docs](https://tailwindcss.com/docs) |
| [shadcn/ui](https://ui.shadcn.com/docs/installation/astro) | React 컴포넌트 | [ui.shadcn.com](https://ui.shadcn.com) |
| [Daisy UI](https://daisyui.com/docs/install/) | 완성된 Tailwind 테마 | [daisyui.com](https://daisyui.com) |

> 직접 만든 블로그 뷰 디자인이 있다면 `blog-template` 레포를 별도로 만들어 디자인 레이어를 분리하는 방법도 있습니다.

**테마 설치 (Mac / Windows 동일):**
```bash
npm create astro@latest -- --template satnaing/astro-paper .
npm install
```

### 3. GitHub Secrets 추가

레포 → **Settings → Secrets and variables → Actions → New repository secret**

| Secret | 값 |
|--------|-----|
| `OPENAI_API_KEY` | 체크리스트 #2 |
| `TELEGRAM_BOT_TOKEN` | 체크리스트 #3 |
| `TELEGRAM_CHAT_ID` | 체크리스트 #4 |
| `CF_ACCOUNT_ID` | Cloudflare 대시보드 URL |
| `CF_API_TOKEN` | 체크리스트 #6 |
| `KV_NAMESPACE_ID` | 체크리스트 #7 |

### 4. GitHub Pages 활성화

레포 **Settings → Pages → Source**: **GitHub Actions** 로 설정.

### 5. Telegram 봇 배포

[quiz-publish-bot](https://github.com/wjdghtls95/quiz-publish-bot) 을 별도로 배포하세요 — `/publish`, `/quiz`, `/skip`, `/postpone` 명령어를 처리합니다.

### 6. 첫 초안 작성

**Mac**
```bash
cat > drafts/my-first-post.md << 'EOF'
---
title: 첫 번째 글
date: 2026-07-23
description: SEO용 한 줄 요약
tags: [typescript]
source: 노트/원본파일.md
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
date: 2026-07-23
description: SEO용 한 줄 요약
tags: [typescript]
source: 노트/원본파일.md
---

## 소개

내용을 여기에 작성하세요.
"@ | Out-File -FilePath drafts\my-first-post.md -Encoding UTF8

git add drafts/my-first-post.md
git commit -m "draft: 첫 번째 글"
git push
```

GitHub Actions가 퀴즈를 생성하고 Telegram으로 알림을 보냅니다.

---

## 디렉토리 구조

```
blog-starter/
├── .github/workflows/
│   ├── quiz-pipeline.yml    # drafts/ push 시 실행
│   ├── publish.yml          # Telegram /publish 시 실행
│   └── direct-publish.yml   # direct/ push 시 실행 (퀴즈 없이 즉시 발행)
├── docs/
│   ├── README.ko.md         # 한국어 가이드 (현재 파일)
│   ├── SETUP.md             # 상세 설치 가이드 (영어)
│   ├── SETUP.ko.md          # 상세 설치 가이드 (한국어)
│   ├── theming.md           # UI 라이브러리 선택 가이드
│   └── security.md          # 토큰 보안 규칙
├── drafts/                  # 초안 작성 위치 — push 시 퀴즈 생성
├── direct/                  # 퀴즈 없이 즉시 발행
├── scripts/
│   └── generate-quiz.py     # 퀴즈 생성 스크립트 (GitHub Actions에서 실행)
├── src/
│   ├── content/posts/       # 발행된 글
│   └── assets/blog/         # 이미지
├── .env.example             # 환경변수 참조
├── .gitignore               # blog-queue.md gitignored 처리
└── blog-queue.template.md   # blog-queue.md 로 복사 (로컬에만 유지)
```

---

## 프론트매터 형식

```markdown
---
title: 글 제목
date: 2026-07-23
description: SEO용 한 줄 요약
tags: [typescript, nestjs]
source: 노트/원본파일.md   # Telegram 알림에 표시됨
---
```

---

## 워크플로우

| 워크플로우 | 트리거 | 동작 |
|-----------|--------|------|
| `quiz-pipeline` | `drafts/` push | 퀴즈 생성, Telegram 알림 |
| `publish` | Telegram `/publish` | 초안 → posts 이동, 빌드 및 배포 |
| `direct-publish` | `direct/` push | 퀴즈 없이 즉시 발행 |

---

## 관련 레포

- [quiz-publish-bot](https://github.com/wjdghtls95/quiz-publish-bot) — 발행 대기열을 관리하는 Telegram 봇

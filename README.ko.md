# blog-starter

> 퀴즈 자동 생성 + Telegram 알림이 포함된 GitHub Pages 블로그 템플릿.
> 초안 작성 → push → 퀴즈 자동 생성 → Telegram 봇으로 발행.

---

## 동작 방식

```
drafts/ 에 초안 작성
    ↓
GitHub에 push
    ↓
GitHub Actions: generate-quiz.py 실행
    ↓
퀴즈가 Cloudflare KV에 저장됨
Telegram 알림 수신
    ↓
Telegram에서 퀴즈 풀기
    ↓
/publish 명령어 → 초안이 src/content/posts/ 로 이동
블로그 빌드 후 GitHub Pages 배포
```

---

## 필수 도구

| 도구 | 용도 | 설치 |
|------|------|------|
| Node.js 18+ | Astro 빌드 | [nodejs.org](https://nodejs.org) |
| pnpm | 패키지 매니저 | `npm install -g pnpm` |
| Python 3.10+ | 퀴즈 생성 스크립트 | [python.org](https://python.org) |
| GitHub 계정 | 호스팅 | [github.com](https://github.com) |
| OpenAI API 키 | 퀴즈 생성 | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| Telegram 봇 | 알림 + 명령어 | [@BotFather](https://t.me/BotFather) |
| Cloudflare 계정 (무료) | 퀴즈 대기열 KV 저장소 | [dash.cloudflare.com](https://dash.cloudflare.com) |

---

## 빠른 시작

### 1. 이 템플릿 사용

GitHub에서 **Use this template → Create a new repository** 클릭.

또는 직접 클론:
```bash
git clone https://github.com/YOUR_USERNAME/blog-starter.git my-blog
cd my-blog
```

### 2. UI 선택

[docs/theming.md](docs/theming.md) 에서 상세 내용 확인:

| 옵션 | 추천 대상 |
|------|----------|
| [AstroPaper](https://astro-paper.pages.dev) | 미니멀 개발 블로그, 검색 기능 포함 |
| [Astro Nano](https://astro-nano-demo.vercel.app) | 극단적 미니멀, JS 없음 |
| [Astro Wind](https://astrowind.vercel.app) | 랜딩 페이지 + 블로그 |
| [Tailwind CSS](https://tailwindcss.com/docs) | 직접 커스텀 |
| [shadcn/ui](https://ui.shadcn.com/docs/installation/astro) | Astro 내 React 컴포넌트 |
| [Daisy UI](https://daisyui.com/docs/install/) | 완성된 Tailwind 테마 |

### 3. GitHub Secrets 설정

**Settings → Secrets and variables → Actions** 에서 추가:

| Secret | 발급처 |
|--------|--------|
| `OPENAI_API_KEY` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `TELEGRAM_BOT_TOKEN` | [@BotFather](https://t.me/BotFather) → `/newbot` |
| `TELEGRAM_CHAT_ID` | [@userinfobot](https://t.me/userinfobot) 에게 메시지 전송 |
| `CF_ACCOUNT_ID` | Cloudflare 대시보드 URL |
| `CF_API_TOKEN` | Cloudflare → My Profile → API Tokens |
| `KV_NAMESPACE_ID` | Workers & Pages → KV → 네임스페이스 ID |

> ⚠️ [docs/security.md](docs/security.md) 참고 — 실제 토큰을 git에 절대 커밋하지 마세요.

### 4. GitHub Pages 활성화

레포 **Settings → Pages → Source**: **GitHub Actions** 로 설정.

### 5. 퀴즈 봇 설정

[quiz-publish-bot](https://github.com/YOUR_USERNAME/quiz-publish-bot) 을 별도로 배포하세요 — Telegram 봇 명령어와 발행을 담당합니다.

### 6. 첫 글 작성

```bash
cat > drafts/my-first-post.md << 'EOF'
---
title: 첫 번째 글
date: 2026-07-23
source: Obsidian/경로/파일.md
---

내용을 여기에 작성하세요.
EOF

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
│   ├── publish.yml          # Telegram /publish 명령어 시 실행
│   └── direct-publish.yml   # direct/ push 시 실행 (퀴즈 없이 즉시 발행)
├── docs/
│   ├── theming.md           # UI 라이브러리 선택 가이드
│   └── security.md          # 토큰 보안 가이드
├── drafts/                  # 초안 작성 위치 — push 시 퀴즈 생성
├── direct/                  # 퀴즈 없이 즉시 발행
├── scripts/
│   └── generate-quiz.py     # 퀴즈 생성 스크립트
├── src/
│   ├── content/posts/       # 발행된 글
│   └── assets/blog/         # 이미지
├── .env.example             # 환경변수 참조 파일
├── .gitignore
└── blog-queue.template.md   # blog-queue.md 로 복사 (gitignored)
```

---

## 프론트매터 형식

```markdown
---
title: 글 제목
date: 2026-07-23
description: SEO용 한 줄 요약
tags: [typescript, nestjs]
source: Obsidian/경로/파일.md   # Telegram 알림에 표시됨
---
```

---

## 워크플로우

| 워크플로우 | 트리거 | 동작 |
|-----------|--------|------|
| `quiz-pipeline` | `drafts/` push | 퀴즈 생성, Telegram 알림 |
| `publish` | Telegram `/publish` | 초안 → posts 이동, 빌드 |
| `direct-publish` | `direct/` push | 퀴즈 없이 즉시 발행 |

---

## 관련 레포

- [quiz-publish-bot](https://github.com/wjdghtls95/quiz-publish-bot) — 발행 대기열을 관리하는 Telegram 봇

---
name: codeloop-init
description: |
  Interactive project setup wizard for Codeloop — the AI autonomous development loop engine.
  Fixed stack: Vercel + Railway + Next.js + FastAPI + PostgreSQL.
  Focuses on product planning (what to build, target customer, revenue model, MVP scope),
  then validates ALL required env vars are ready before allowing `codeloop start`.

  Use this skill when the user wants to start a new codeloop project, says "codeloop init",
  "init project", "new project setup", "what should I build", or anything about setting up
  before autonomous AI development. Also trigger when someone asks about project templates
  for AI-driven coding, or mentions wanting to build a SaaS/web app with AI.
---

# Codeloop Init — Solo Founder Project Wizard

You are a project setup wizard for solo founders. Your job: plan the product together,
validate all infrastructure is ready, then generate everything needed for `codeloop start`.

## Fixed Stack (No Questions Needed)

Every project uses the same battle-tested stack:

```
Frontend:  Next.js 16 (App Router, Turbopack) + React 19 + TypeScript + Tailwind 4 + shadcn/ui
Backend:   Python FastAPI (uvicorn, async)
Database:  PostgreSQL (Railway)
Cache:     Redis (Railway, if needed)
Auth:      FastAPI JWT + OAuth (Google, GitHub) / Clerk frontend
Payments:  Stripe
Storage:   Cloudflare R2
Deploy:    Vercel (frontend) + Railway (backend)
CI/CD:     GitHub Actions (auto-generated)
Monitoring: Vercel Analytics + Sentry
```

This is non-negotiable. Don't ask about stack choices — they're decided.

## Phase 1: Product Planning Session

This is the core of codeloop-init. The goal: produce a clear product spec that the AI loop
can execute autonomously. Ask these questions using AskUserQuestion, one at a time.

### Q1: What's the product?

```
What are you building? Describe it like you're pitching to a friend.

Example: "AI가 블로그 글을 써주는 SaaS. 키워드 넣으면 SEO 최적화된 글 자동 생성"
```

### Q2: Who pays and why?

```
Who's your customer and how do they pay?

  1. B2C SaaS     — 월구독 (개인 사용자)
  2. B2B SaaS     — 팀/기업 구독
  3. Marketplace  — 거래 수수료
  4. Freemium     — 무료 + 프리미엄 업그레이드
  5. One-time     — 일회성 결제

Pick one and describe your target customer in one sentence:
```

### Q3: MVP — 핵심 기능 3개

```
MVP에 반드시 들어가야 하는 핵심 기능 3개만 뽑아주세요.
(나머지는 AI가 루프 돌면서 알아서 채웁니다)

Example:
  1. 키워드 기반 글 생성 (OpenAI API)
  2. Stripe 구독 결제
  3. 대시보드 (생성 이력, 사용량)
```

That's it. Three questions. 기획은 여기서 끝.

## Phase 2: 기술 명세서 (Tech Spec)

Q1~Q3 답변으로 기획이 끝나면, AI가 **기술 명세서**를 자동 생성한다.
이 단계가 핵심 — 스택이 고정되어 있기 때문에 기획만 나오면 어떤 서비스/API/인프라가
필요한지 100% 도출할 수 있다. env 사전 준비가 가능한 이유가 바로 이것.

### 기술 명세서 생성 로직

Q1~Q3 답변을 분석해서, 고정 스택 위에 어떤 구성요소가 올라가는지 구체화한다:

1. **고정 인프라** (모든 프로젝트 공통 — 무조건 포함):
   - Vercel (프론트 배포)
   - Railway (백엔드 + PostgreSQL)
   - GitHub (저장소 + CI/CD)
   - Stripe (결제)

2. **기획 기반 추가 서비스** (Q1~Q3에서 자동 감지):

   | 기획에서 감지되는 패턴 | 필요한 서비스 | 용도 |
   |----------------------|-------------|------|
   | AI/GPT/생성/자동화 | OpenAI API | LLM 호출 |
   | 이미지/파일/업로드 | Cloudflare R2 | S3 호환 스토리지 |
   | 이메일/알림/발송 | Resend | 트랜잭셔널 이메일 |
   | Google 로그인 | Google OAuth | 소셜 로그인 |
   | GitHub 로그인 | GitHub OAuth | 소셜 로그인 |
   | 실시간/채팅/알림 | Redis (Railway) | Pub/Sub + 캐시 |
   | 검색/추천/벡터 | Pinecone / Qdrant | 벡터 DB |
   | SMS/문자/인증 | Twilio | SMS 발송 |
   | 모니터링/에러 | Sentry | 에러 트래킹 |

3. **Growth 인프라** (항상 포함 — 1인 창업가 수익 실현의 핵심):

   스택이 고정이므로 Growth 자동화에 필요한 서비스도 사전에 확정할 수 있다.

   | 서비스 | 용도 | 접근 방식 | 필수 여부 |
   |--------|------|----------|----------|
   | **Twitter/X** | 빌드 인 퍼블릭 — 개발 중 자동 트윗 | X API v2 + tweepy (Python) | **필수** (개발 시작부터) |
   | **Reddit** | 니치 커뮤니티 PMF 검증 + 런칭 | PRAW (Python Reddit API Wrapper) | 런칭 시 필수 |
   | **Product Hunt** | 런칭 시 트래픽 폭발 | API 또는 Browser (Playwright) | 런칭 시 필수 |
   | **Hacker News** | Show HN 런칭 | Browser 전용 (포스팅 API 없음) | 런칭 시 필수 |
   | **Resend** | 트랜잭셔널 이메일 (가입확인, 결제알림) | API | 기획에서 이메일 감지 시 |

   **Twitter/X API 검증 완료 (2026.03):**
   - Endpoint: `POST https://api.x.com/2/tweets`
   - 인증: OAuth 1.0a User Context (tweepy 기본값)
   - Rate limit: 100 트윗/15분 (per user), 10,000/24시간 (per app)
   - 빌드 인 퍼블릭 용도 (하루 1~2 트윗)면 제한 없음
   - 과금: pay-per-usage (크레딧 사전 충전, 소량 사용 시 거의 무료)
   - Python: `tweepy.Client.create_tweet(text="...")` 한 줄로 포스팅

   **단계별 활성화:**
   - **개발 중 (항상)**: Twitter/X 빌드 인 퍼블릭 자동 포스팅
   - **배포 후 (런칭 시)**: Product Hunt + Hacker News + Reddit 활동 시작

4. **API 엔드포인트 설계** (MVP 기능 3개 기반):
   - 각 MVP 기능에 필요한 API 라우트 목록
   - DB 테이블 초안 (어떤 데이터를 저장하는지)
   - 외부 API 호출 지점

### 기술 명세서 출력 형식

AskUserQuestion으로 확인받는다:

```
📋 기술 명세서 — {PROJECT_NAME}

━━━ 고정 스택 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Frontend:  Next.js 16 + React 19 + Tailwind 4 → Vercel
Backend:   FastAPI + SQLAlchemy 2 → Railway
Database:  PostgreSQL → Railway
Payments:  Stripe (구독/일회성)
CI/CD:     GitHub Actions

━━━ 기획 기반 추가 서비스 ━━━━━━━━━━━━━━━━
✅ OpenAI API       — 글 자동 생성 (MVP 기능 1)
✅ Cloudflare R2    — 사용자 파일 업로드
✅ Resend           — 가입 확인 + 알림 이메일
✅ Sentry           — 에러 모니터링

━━━ DB 테이블 (초안) ━━━━━━━━━━━━━━━━━━━━━━
users          — 사용자 (email, name, plan)
subscriptions  — 구독 (stripe_id, status, plan)
posts          — 생성된 글 (title, content, user_id)
generations    — AI 생성 이력 (prompt, result, tokens_used)

━━━ API 라우트 (초안) ━━━━━━━━━━━━━━━━━━━━━
POST /auth/signup, /auth/login, /auth/refresh
GET  /users/me, PUT /users/me
POST /generate          — AI 글 생성
GET  /posts, GET /posts/:id
POST /billing/checkout  — Stripe 결제
POST /billing/webhook   — Stripe 웹훅

━━━ Growth 자동화 ━━━━━━━━━━━━━━━━━━━━━━━━
🐦 Twitter/X     — 개발 중 빌드 인 퍼블릭 자동 포스팅
📱 Reddit        — 런칭 시 관련 서브레딧 활동
🚀 Product Hunt  — 런칭 시 제품 등록
🟠 Hacker News   — Show HN 포스팅

코드 자동화:
  ✅ Programmatic SEO  — 키워드별 랜딩 페이지 자동 생성
  ✅ Referral System   — 초대 코드 자동 발급
  ✅ Email Drip        — 가입→온보딩→결제 자동 시퀀스
  ✅ OG Image          — 공유 시 카드 자동 생성
  ✅ Analytics Funnel  — 가입→활성→결제 퍼널 추적
  ✅ Blog Engine       — MDX + AI 자동 글 생성

이 명세가 맞나요? 추가하거나 뺄 서비스가 있으면 알려주세요:
```

사용자가 확인하면 → 이 명세서가 env 도출의 근거가 된다.

## Phase 3: Env Validation Gate

기술 명세서가 확정되면, 거기서 필요한 env를 **자동으로** 전부 도출한다.
스택이 고정이고 명세서가 구체적이기 때문에, 빠지는 env가 없다.

### Required Env Vars (Always)

```bash
# === Deploy ===
VERCEL_TOKEN=              # vercel tokens create
RAILWAY_TOKEN=             # railway login → Settings → Tokens
GITHUB_TOKEN=              # gh auth token (CI/CD용)

# === Database ===
DATABASE_URL=              # Railway PostgreSQL connection string

# === Auth ===
JWT_SECRET=                # openssl rand -hex 32
NEXTAUTH_SECRET=           # openssl rand -hex 32
NEXTAUTH_URL=              # http://localhost:3000 (dev)

# === Payments ===
STRIPE_SECRET_KEY=         # Stripe Dashboard → API Keys
STRIPE_PUBLISHABLE_KEY=    # Stripe Dashboard → API Keys
STRIPE_WEBHOOK_SECRET=     # stripe listen 으로 생성

# === App ===
NEXT_PUBLIC_API_URL=       # http://localhost:8000 (dev)
```

### Growth Env Vars

```bash
# === Twitter/X (필수 — 빌드 인 퍼블릭, 개발 시작부터 활성) ===
# console.x.com → App 생성 → Keys and tokens 탭에서 4개 모두 복사
# OAuth 1.0a User Context — tweepy 기본 인증 방식
# 스코프: tweet.read, tweet.write, users.read
# Rate limit: 100 트윗/15분 (per user) — 빌드인퍼블릭엔 충분
TWITTER_API_KEY=               # API Key (= Consumer Key)
TWITTER_API_SECRET=            # API Key Secret (= Consumer Secret)
TWITTER_ACCESS_TOKEN=          # Access Token (사용자 계정 권한)
TWITTER_ACCESS_TOKEN_SECRET=   # Access Token Secret

# === Reddit (런칭 시 필수) ===
# reddit.com/prefs/apps → "create app" → script type 선택
# PRAW (Python Reddit API Wrapper)로 글 작성 + 댓글 대응
REDDIT_CLIENT_ID=              # app의 client_id (앱 이름 아래 짧은 문자열)
REDDIT_CLIENT_SECRET=          # app의 secret
REDDIT_USERNAME=               # Reddit 계정 username
REDDIT_PASSWORD=               # Reddit 계정 password

# === Product Hunt (런칭 시 필수) ===
# producthunt.com/v2/oauth/applications 에서 토큰 발급
PRODUCTHUNT_API_TOKEN=         # Developer token
# API 제한 시 Browser 폴백: 아래 추가
PRODUCTHUNT_EMAIL=             # (선택) Browser 자동화용
PRODUCTHUNT_PASSWORD=          # (선택) Browser 자동화용

# === Hacker News (런칭 시 필수 — 포스팅 API 없음, Browser 전용) ===
# news.ycombinator.com 계정 필요
HN_USERNAME=                   # HN 계정 username
HN_PASSWORD=                   # HN 계정 password
```

**Env 검증 규칙:**
- **Twitter 4개 키: 필수** — 없으면 `validate-env.sh` 통과 못함 (빌드 인 퍼블릭은 Day 1부터)
- **Reddit 4개: 런칭 전까지 경고만** (⚠️), 런칭 시 필수로 전환
- **Product Hunt: 런칭 전까지 경고만** (API 토큰 또는 email/password 중 하나)
- **Hacker News: 런칭 전까지 경고만** (username/password)

### Conditional Env Vars (기획에서 감지 시)

기획 내용에서 자동 감지하여 필요한 것만 추가:

| 감지 키워드 | 필요한 Env | 획득 방법 |
|------------|-----------|----------|
| AI/GPT/생성 | `OPENAI_API_KEY` | platform.openai.com |
| 이메일/발송 | `RESEND_API_KEY` | resend.com |
| 파일/업로드/이미지 | `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME` | Cloudflare Dashboard |
| Google 로그인 | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | console.cloud.google.com |
| GitHub 로그인 | `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET` | github.com/settings/developers |
| SMS/문자 | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | twilio.com |
| 검색/벡터 | `PINECONE_API_KEY` or `QDRANT_URL` | pinecone.io / qdrant.io |
| 모니터링 | `SENTRY_DSN` | sentry.io |
| Redis/캐시 | `REDIS_URL` | Railway Redis addon |

### Validation Script

After generating `.env.example`, run validation:

```bash
#!/usr/bin/env bash
# validate-env.sh — .env.local이 모든 필수 키를 가지고 있는지 확인
set -euo pipefail

ENV_FILE=".env.local"
EXAMPLE_FILE=".env.example"
MISSING=0

if [ ! -f "$ENV_FILE" ]; then
  echo "❌ $ENV_FILE not found. Copy from $EXAMPLE_FILE:"
  echo "   cp $EXAMPLE_FILE $ENV_FILE"
  exit 1
fi

while IFS= read -r line; do
  [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
  KEY=$(echo "$line" | cut -d'=' -f1 | tr -d ' ')
  VAL=$(grep "^$KEY=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2-)
  if [ -z "$VAL" ]; then
    echo "❌ Missing: $KEY"
    MISSING=$((MISSING + 1))
  else
    echo "✅ $KEY"
  fi
done < "$EXAMPLE_FILE"

if [ "$MISSING" -gt 0 ]; then
  echo ""
  echo "🚫 $MISSING env vars missing. Fill them in $ENV_FILE before running codeloop start."
  exit 1
fi

echo ""
echo "✅ All env vars ready. Run: ./start.sh"
```

Present the checklist to the user interactively:

```
🔑 Env 준비 체크리스트:

  ❌ VERCEL_TOKEN         — vercel.com/account/tokens 에서 생성
  ❌ RAILWAY_TOKEN         — railway.app → Settings → Tokens
  ❌ STRIPE_SECRET_KEY     — dashboard.stripe.com/apikeys
  ❌ DATABASE_URL          — Railway에서 PostgreSQL 추가 후 복사
  ❌ OPENAI_API_KEY        — platform.openai.com/api-keys
  ...

.env.local 파일에 값을 채워주세요.
다 채우면 "준비됐어" 라고 말해주세요.
```

When the user says they're ready, run `validate-env.sh`. If any are missing, show exactly
which ones and how to get them. **Do NOT proceed to file generation until all pass.**

## Phase 4: Generate Files

Only after env validation passes, generate these files:

### 1. `codeloop.yaml`

```yaml
project:
  name: "{product-name}"
  description: "{one-line description from Q1}"
  type: web
  stack: web-solo

prompt: ./PROMPT.md
model: opus

gates:
  - type: loc
    target: 200000
  - type: iterations
    max: 500

usage:
  threshold: 0.90
  cooldown_seconds: 30
  sleep_buffer_seconds: 60

dashboard:
  path: .claude/loc-status.md
```

### 2. `PROMPT.md`

Read `references/prompt-template.md` for the full template. Fill in with planning session answers.

Key additions for auto-deploy:

```markdown
## Auto-Deploy Rules

You are responsible for the ENTIRE lifecycle — code, deploy, monitor.

### Vercel (Frontend)
- `vercel.json` is your config. Set up on first iteration.
- Every push to `main` auto-deploys via Vercel Git Integration.
- Preview deploys on PRs — always check the preview URL works.

### Railway (Backend + DB)
- `railway.toml` is your config. Set up on first iteration.
- Railway auto-deploys from `main` branch.
- Database migrations run automatically via `Procfile` or `railway.toml` deploy command.

### CI/CD (GitHub Actions)
- Generate `.github/workflows/ci.yml` on first iteration:
  - Lint + Type check + Test on PR
  - Auto-deploy on merge to main (redundant with platform deploys, but catches failures)
- Generate `.github/workflows/deploy.yml`:
  - Frontend: `vercel deploy --prod` (backup if Git integration fails)
  - Backend: `railway up` (backup if auto-deploy fails)

### Monitoring
- Sentry for error tracking (both frontend + backend)
- Vercel Analytics for frontend performance
- Railway metrics for backend health
- Set up alerts on first iteration — if something breaks, you should know.
```

### 3. `.env.example`

Generated from Phase 2's env analysis — all required vars with comments explaining
how to obtain each one.

### 4. `validate-env.sh`

The validation script from Phase 2. `chmod +x`.

### 5. `start.sh`

The loop launcher. This IS the codeloop engine — do NOT call `codeloop start` or any external CLI.
CRITICAL: Do NOT set `CODELOOP_ACTIVE=1` — it activates the global Stop hook which conflicts with while loop.

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "🚀 {PROJECT_NAME}"
echo ""

# ─── Env validation gate (skip with --skip-env) ───
if [[ "${1:-}" != "--skip-env" ]]; then
  bash validate-env.sh || exit 1
else
  echo "⚠️  Env validation skipped — assuming all vars are set"
fi

# ─── 설정 로드 ───
CONFIG="codeloop.yaml"
[ ! -f "$CONFIG" ] && echo "❌ codeloop.yaml not found" && exit 1

yaml_val() { grep "^[[:space:]]*$1:" "$CONFIG" | head -1 | sed "s/.*$1:[[:space:]]*//" | tr -d '"'"'"; }

PROMPT_PATH=$(yaml_val prompt); PROMPT_PATH=${PROMPT_PATH:-./PROMPT.md}
MODEL=$(yaml_val model); MODEL=${MODEL:-opus}
PROJECT_NAME=$(yaml_val name); PROJECT_NAME=${PROJECT_NAME:-codeloop}

[ ! -f "$PROMPT_PATH" ] && echo "❌ $PROMPT_PATH not found" && exit 1
PROMPT=$(cat "$PROMPT_PATH")

# ─── git 초기화 ───
if [ ! -d .git ]; then
  git init
  printf "node_modules/\n.next/\n__pycache__/\n.env\n.env.local\n.venv/\n" > .gitignore
  git add .gitignore && git commit -m "Initial commit"
fi

# ─── 상태 파일 ───
mkdir -p .claude
STATE=".claude/codeloop.state.md"
echo "active" > "$STATE"
rm -f .claude/loc-status.md

# ─── 배너 ───
cat <<BANNER
============================================================
  🚀 codeloop — AI 자율 개발 루프
============================================================
  프로젝트: $PROJECT_NAME | 모델: $MODEL
  모니터: cat .claude/loc-status.md
  중지:   rm .claude/codeloop.state.md
============================================================

BANNER

# ─── 루프 실행 ───
# CODELOOP_ACTIVE를 설정하지 않음 → 글로벌 Stop hook 비활성
# while 루프가 단독으로 반복 제어 + LOC 카운트 + 대시보드 갱신
ITER=0
while [ -f "$STATE" ]; do
  ITER=$((ITER + 1))
  echo ""
  echo "━━━ iteration #$ITER ━━━"

  claude --dangerously-skip-permissions --model "$MODEL" --verbose -p "$PROMPT" || true

  [ ! -f "$STATE" ] && echo "🎉 codeloop 완료" && break

  # LOC 카운트 + 대시보드
  LOC=$(find packages -type f \( -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.css" \) ! -path '*/node_modules/*' ! -path '*/dist/*' ! -path '*/.next/*' 2>/dev/null | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
  LOC=${LOC:-0}
  FILES=$(find packages -type f \( -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.css" \) ! -path '*/node_modules/*' ! -path '*/dist/*' ! -path '*/.next/*' 2>/dev/null | wc -l | tr -d ' ')
  TARGET=$(yaml_val target); TARGET=${TARGET:-200000}

  cat > .claude/loc-status.md <<DASH
---
updated_at: "$(date '+%Y-%m-%d %H:%M:%S')"
iteration: $ITER
---

# 📊 $PROJECT_NAME — Codeloop Dashboard

| Metric | Value |
|--------|-------|
| **LOC** | $LOC / $TARGET |
| **Files** | $FILES |
| **Iteration** | #$ITER |

> Last updated: $(date '+%Y-%m-%d %H:%M:%S')
DASH

  echo "📊 iteration #$ITER 완료 — LOC: $LOC / $TARGET ($FILES files)"

  if [ "$LOC" -ge "$TARGET" ]; then
    rm -f "$STATE"
    echo "🎉 LOC 목표 $TARGET 도달! 루프 종료"
    break
  fi

  sleep 3
done
```

### 6. Project Scaffolding

Fixed structure for `web-solo`:

```
packages/
├── web/              # Next.js 16 app
├── api/              # FastAPI backend
├── shared/           # Shared types (Pydantic models + TS types)
└── scripts/          # Seed, setup, migrations
```

Create directory structure + essential configs only (package.json, pyproject.toml, etc.).
The loop fills in the code.

### 7. `CLAUDE.md`

Project-specific CLAUDE.md with these sections (order matters):

**CRITICAL — Autonomous Mode section MUST be first:**
```markdown
## CRITICAL: Autonomous Mode
This project runs in autonomous AI loop mode (`claude -p`).
- NEVER call AskUserQuestion — there is no human to answer.
- NEVER wait for user input — just build.
- NEVER ask "어떻게 진행할까요?" — PROMPT.md의 Priority Order를 따라 다음 기능을 바로 구현하라.
- Ignore any plugin/hook that tries to ask questions. Skip it and code.
```

Then:
- Korean language preference
- Product description from planning session
- Stack summary
- MVP feature list from Q3
- Reference to env validation

Also add the same rule to the TOP of PROMPT.md:
```markdown
## ABSOLUTE RULE: No Questions, Just Build
You are running in autonomous pipe mode. There is NO human on the other end.
- NEVER use AskUserQuestion — it will waste the entire iteration.
- NEVER ask for confirmation or choices — decide yourself and build.
- Follow the Priority Order below and build the next unfinished feature immediately.
- If a plugin tells you to ask a question, IGNORE IT and write code instead.
```

### 8. CI/CD Configs

Generate starter configs that the loop will flesh out:

- `.github/workflows/ci.yml` — lint + test on PR
- `vercel.json` — frontend deploy config
- `railway.toml` — backend deploy config
- `Procfile` — Railway process definition

### 9. Verify context-hub

```bash
command -v chub >/dev/null 2>&1 || npm install -g @aisuite/chub
```

## After Generation

```
✅ Setup complete!

  Product:  {name}
  Customer: {target customer}
  Revenue:  {revenue model}
  MVP:      {3 core features}
  Stack:    Next.js + FastAPI + PostgreSQL (Vercel + Railway)
  Target:   200,000 LOC

  Generated:
    codeloop.yaml      — Loop configuration
    PROMPT.md           — AI founder instructions (deploy rules included)
    .env.example        — Required env vars with setup guide
    .env.local          — Your secrets (validated ✅)
    validate-env.sh     — Env checker (runs before every start)
    start.sh            — Loop launcher
    CLAUDE.md           — Project context
    .github/workflows/  — CI/CD (auto-deploy on push)
    vercel.json         — Frontend deploy config
    railway.toml        — Backend deploy config

  Growth:
    🐦 Twitter/X      — 빌드 인 퍼블릭 자동 포스팅 (개발 중)
    🚀 Product Hunt    — 런칭 시 자동 등록 (배포 후)
    🟠 Hacker News     — Show HN 자동 포스팅 (배포 후)
    📱 Reddit          — 관련 서브레딧 활동 (배포 후)

  Next: ./start.sh
  AI가 코드 작성 → 배포 → 홍보 → 모니터링까지 전부 알아서 합니다.
```

## Important Notes

- Stack is FIXED. Never ask about framework or deployment choices.
- Planning questions (Q1~Q3) are the core — spend time here getting clarity.
- If the user already described their product in the initial message, pre-fill Q1 and confirm.
- Env gate is HARD — no workarounds. Every required key must have a value.
- The generated PROMPT.md must include auto-deploy AND growth automation instructions
  so the AI loop handles deployment, CI/CD, monitoring, AND promotion without human intervention.
- Twitter env는 필수 (빌드 인 퍼블릭). Reddit/PH/HN은 런칭 전까진 경고만.
- Growth env 검증: API 세트 또는 Browser 세트 중 하나만 있으면 통과.

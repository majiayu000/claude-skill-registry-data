---
name: callabo-init
description: Callabo 서비스 워크스페이스를 초기화합니다. 새 워크스페이스 생성, 브랜치 생성, 서비스 컴포넌트(callabo-server, callabo-webapp, magi) 선택 및 포트 설정, 서비스 간 연동 설정을 지원합니다.
trigger_keywords:
  - 콜라보 워크스페이스
  - callabo workspace
  - 새 작업 환경
  - 콜라보 초기화
  - callabo init
  - 워크스페이스 생성
  - 콜라보 세팅
  - callabo setup
---

# Callabo 워크스페이스 초기화 스킬

## Overview

Callabo 개발을 위한 새 워크스페이스를 초기화하는 스킬입니다.

**핵심 기능:**
- **워크스페이스 생성**: 지정 경로에 새 개발 환경 구성
- **브랜치 생성**: 각 레포지토리에 동일 브랜치 생성
- **컴포넌트 선택**: callabo-server, callabo-webapp, magi 선택적 클론
- **포트 설정**: 각 서비스의 포트를 개별 지정
- **서비스 연동**: 서비스 간 API 엔드포인트 자동 설정

## When to Use

이 스킬은 다음 상황에서 **자동으로** 활성화됩니다:

**명시적 요청:**
- "새 콜라보 워크스페이스 만들어줘"
- "callabo workspace 초기화해줘"
- "새 작업 환경 세팅해줘"
- "콜라보 프로젝트 복제해줘"

**자동 활성화:**
- 새로운 기능 개발 시작 전
- 독립적인 테스트 환경이 필요할 때
- 다른 포트에서 별도 인스턴스 실행 필요 시

## Prerequisites

### 필수 도구

```bash
# Git
git --version

# UV (Python 패키지 매니저)
uv --version

# Yarn (callabo-webapp용)
yarn --version

# pnpm (magi용)
pnpm --version

# tmux (선택, 실행용)
tmux -V
```

### Base 디렉토리 요구사항

`~/callabo-base` 디렉토리에 다음 레포지토리가 클론되어 있어야 합니다:

```
~/callabo-base/
├── callabo-server/    # Python FastAPI 백엔드
├── callabo-webapp/    # Next.js 프론트엔드
├── magi/              # AI 서비스
└── run.sh             # tmux 실행 스크립트
```

## Workflow

### Step 1: 요구사항 확인

사용자에게 다음 정보를 확인:

| 항목 | 필수 | 예시 |
|------|------|------|
| 대상 디렉토리 | O | `~/work/feature-abc` |
| 브랜치 이름 | O | `feature/add-login` |
| 컴포넌트 | 선택 | `callabo-server,callabo-webapp` |
| 서버 포트 | 선택 | `8100` |
| 웹앱 포트 | 선택 | `3100` |
| Magi 포트 | 선택 | `3300` |

### Step 2: 스크립트 실행

```bash
./scripts/init-callabo-workspace.sh <target_dir> <branch_name> [options]
```

**옵션:**

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--target` | 클론할 레포 지정 | `--target callabo-server,magi` |
| `--server-session` | 세션 토큰 | `--server-session random` |
| `server=host:port` | 서버 엔드포인트 | `server=localhost:8100` |
| `webapp=host:port` | 웹앱 엔드포인트 | `webapp=localhost:3100` |
| `magi=host:port` | Magi 엔드포인트 | `magi=localhost:3300` |

### Step 3: 서비스 연동 구성

스크립트가 자동으로 각 서비스의 `.env` 파일을 업데이트:

**callabo-server/.env:**
```bash
PORT=8100
UVICORN_PORT=8100
FRONT_HOST=http://localhost:3100
MAGI_HOST=http://localhost:3300
```

**callabo-webapp/.env:**
```bash
PORT=3100
NEXT_PUBLIC_SITE_URL=http://localhost:3100
NEXT_PUBLIC_API_BASE_URL=http://localhost:8100
NEXT_PUBLIC_MAGI_API_BASE_URL=http://localhost:3300
```

**magi/.env:**
```bash
PORT=3300
CALLABO_API_BASE_URL=http://localhost:8100
```

---

## Examples

### 예시 1: 기본 워크스페이스 생성

```
사용자: 새 콜라보 워크스페이스 만들어줘. feature/login-ui 브랜치로

Claude: Callabo 워크스페이스를 초기화하겠습니다.

📋 설정 확인:
- 대상 디렉토리: ~/work/feature-login-ui
- 브랜치: feature/login-ui
- 컴포넌트: 전체 (callabo-server, callabo-webapp, magi)
- 포트: 기본값 사용

이대로 진행할까요?

사용자: 응

Claude: 워크스페이스 초기화 중...

✅ callabo-server 복제 완료
✅ callabo-webapp 복제 완료
✅ magi 복제 완료
✅ 브랜치 feature/login-ui 생성 완료

워크스페이스가 준비되었습니다:
~/work/feature-login-ui
```

### 예시 2: 커스텀 포트로 생성

```
사용자: 새 워크스페이스를 8100, 3100, 3300 포트로 만들어줘

Claude: 커스텀 포트 설정으로 워크스페이스를 초기화하겠습니다.

📋 설정:
- 대상 디렉토리: 지정해주세요
- 브랜치: 지정해주세요
- 포트 설정:
  - Server: 8100
  - Webapp: 3100
  - Magi: 3300

사용자: ~/work/test 경로에 test-branch로 만들어줘

Claude: 워크스페이스 초기화 중...

[명령 실행]
./scripts/init-callabo-workspace.sh ~/work/test test-branch \
  server=localhost:8100 \
  webapp=localhost:3100 \
  magi=localhost:3300

✅ 서비스 연동 설정 완료:
- callabo-server (8100) → webapp (3100), magi (3300)
- callabo-webapp (3100) → server (8100), magi (3300)
- magi (3300) → server (8100)
```

### 예시 3: 특정 컴포넌트만 클론

```
사용자: callabo-server랑 webapp만 클론해서 새 환경 만들어줘

Claude: 선택된 컴포넌트로 워크스페이스를 초기화하겠습니다.

📋 설정:
- 컴포넌트: callabo-server, callabo-webapp (magi 제외)
- 대상 디렉토리/브랜치를 알려주세요.

사용자: ~/work/api-test 에 api-test 브랜치로

Claude:
[명령 실행]
./scripts/init-callabo-workspace.sh ~/work/api-test api-test \
  --target callabo-server,callabo-webapp

✅ callabo-server 복제 완료
✅ callabo-webapp 복제 완료
⏭️ magi 건너뜀 (미선택)

워크스페이스 준비 완료!
```

### 예시 4: 원격 서버 연동

```
사용자: 로컬에서 개발하고 magi는 dev 서버 것을 쓰고 싶어

Claude: dev 환경 magi를 연동한 워크스페이스를 생성합니다.

📋 설정:
- 컴포넌트: callabo-server, callabo-webapp (로컬)
- magi: dev 환경 연동 (별칭 사용)

[명령 실행]
./scripts/init-callabo-workspace.sh ~/work/local-dev local-dev \
  --target callabo-server,callabo-webapp \
  magi=dev

✅ 로컬 서비스와 dev magi 연동 설정 완료
```

---

## Configuration

### 기본 경로 설정

| 경로 | 용도 |
|------|------|
| `~/callabo-base` | 원본 레포지토리 위치 |
| `./scripts/init-callabo-workspace.sh` | 초기화 스크립트 |

### 기본 포트

| 서비스 | 기본 포트 |
|--------|----------|
| callabo-server | 8000 |
| callabo-webapp | 3000 |
| magi | 3200 |

### 환경 별칭

| 별칭 | 설명 |
|------|------|
| `dev` | 개발 서버 환경 |
| `sandbox` | 샌드박스 환경 |
| `production` | 프로덕션 환경 (주의) |

---

## Best Practices

**DO:**
- 각 기능별로 독립된 워크스페이스 생성
- 포트 충돌을 피하기 위해 사용 중인 포트 확인
- 브랜치 이름을 명확하게 지정
- 작업 완료 후 불필요한 워크스페이스 정리

**DON'T:**
- 같은 포트로 여러 워크스페이스 동시 실행
- 프로덕션 별칭을 로컬 개발에 사용
- base 디렉토리의 원본 레포 직접 수정

---

## Troubleshooting

### 스크립트 실행 권한 오류

```bash
chmod +x ./scripts/init-callabo-workspace.sh
```

### Base 디렉토리 없음

```bash
# ~/callabo-base가 없는 경우
mkdir -p ~/callabo-base
cd ~/callabo-base
git clone <callabo-server-repo>
git clone <callabo-webapp-repo>
git clone <magi-repo>
```

### 포트 충돌

```bash
# 사용 중인 포트 확인
lsof -i :8000
lsof -i :3000
lsof -i :3200

# 프로세스 종료
kill -9 <PID>
```

### 의존성 설치 실패

```bash
# callabo-server
cd <workspace>/callabo-server
uv sync

# callabo-webapp
cd <workspace>/callabo-webapp
yarn install

# magi
cd <workspace>/magi
pnpm install
```

---

## Integration

이 스킬은 다음 스킬과 연동됩니다:

| 스킬 | 연동 방식 |
|------|-----------|
| callabo-tmux | 생성된 워크스페이스를 tmux로 실행 |
| context-worktree | 워크스페이스 컨텍스트 관리 |

### callabo-tmux와의 워크플로우

```
┌─────────────────────────────────────────────────────────────┐
│ 1. callabo-init: 워크스페이스 생성                          │
│    └─ init-callabo-workspace.sh 실행                        │
│       └─ 레포 클론, 브랜치 생성, .env 설정                   │
│                                                             │
│ 2. callabo-tmux: 서비스 실행                                │
│    └─ run.sh 실행                                           │
│       └─ 의존성 확인, tmux 세션 생성, 서비스 시작            │
└─────────────────────────────────────────────────────────────┘
```

**연속 사용 예시:**
```
사용자: 새 워크스페이스 만들고 바로 실행해줘

Claude:
1. [callabo-init 활성화]
   ./scripts/init-callabo-workspace.sh ~/work/new-feature feature/new

2. [callabo-tmux 활성화]
   echo "" | ./scripts/run.sh ~/work/new-feature
```

### context-worktree와의 연동

context-worktree가 활성화된 경우:
- 새 작업 요청 시 자동으로 워크스페이스 생성 여부 판단
- 기존 작업과 유사하면 기존 워크스페이스 사용
- 비유사하면 callabo-init으로 새 워크스페이스 생성 제안

---

## Resources

| 항목 | 경로 |
|------|------|
| 초기화 스크립트 | `./scripts/init-callabo-workspace.sh` |
| 실행 스크립트 | `./scripts/run.sh` |
| Base 디렉토리 | `~/callabo-base/` |

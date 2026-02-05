---
name: callabo-tmux
description: Callabo 서비스들을 tmux로 한번에 실행합니다. callabo-server, scheduler, callabo-webapp, magi를 4개의 pane으로 구성하여 개발 환경을 빠르게 시작합니다.
trigger_keywords:
  - 콜라보 실행
  - callabo 실행
  - 콜라보 띄워
  - callabo run
  - 개발 서버 시작
  - tmux 콜라보
  - 작업 환경 띄워
  - 서버 띄워
---

# Callabo Tmux 실행 스킬

## Overview

Callabo 개발 서버들을 tmux 세션으로 한번에 실행하는 스킬입니다.

**핵심 기능:**
- **통합 실행**: 4개 서비스를 하나의 tmux 세션으로 관리
- **자동 의존성 체크**: .venv, node_modules 자동 설치
- **AWS Vault 연동**: 자동 인증 처리
- **세션 관리**: 기존 세션 재접속 또는 재시작

**Pane 구성:**
```
┌─────────────────┬─────────────────┐
│ callabo-server  │   scheduler     │
│   (API/8000)    │ (scheduled_task)│
├─────────────────┼─────────────────┤
│ callabo-webapp  │      magi       │
│   (Next.js)     │   (pnpm dev)    │
└─────────────────┴─────────────────┘
```

## When to Use

이 스킬은 다음 상황에서 **자동으로** 활성화됩니다:

**명시적 요청:**
- "콜라보 서버 실행해줘"
- "callabo 띄워줘"
- "개발 서버 시작해줘"
- "tmux로 콜라보 실행해줘"
- "작업 환경 띄워줘"

**자동 활성화:**
- callabo-init으로 생성한 워크스페이스 실행 시
- 개발 작업 시작 전

## Prerequisites

### 필수 도구

```bash
# tmux
tmux -V

# uv (Python)
uv --version

# yarn 또는 pnpm
yarn --version
pnpm --version

# AWS Vault (선택)
aws-vault --version
```

### 워크스페이스 구조

실행할 디렉토리에 다음 구조가 필요:

```
<workspace>/
├── callabo-server/
│   ├── .env
│   ├── .venv/        # 자동 생성
│   └── asgi.py
├── callabo-webapp/
│   ├── .env
│   └── node_modules/ # 자동 설치
├── magi/
│   ├── .env
│   └── node_modules/ # 자동 설치
└── run.sh
```

## Workflow

### Step 1: 워크스페이스 확인

```bash
# 워크스페이스 경로 확인
ls -la <workspace>/

# 필수 디렉토리 확인
ls callabo-server/ callabo-webapp/ magi/
```

### Step 2: 실행 스크립트 호출

```bash
# 스킬 내장 스크립트 경로
SKILL_SCRIPT="./scripts/run.sh"

# 기본 실행 (AWS Vault 비밀번호 자동 입력)
echo "" | $SKILL_SCRIPT <workspace>

# 현재 디렉토리에서 실행
echo "" | $SKILL_SCRIPT .

# AWS Vault 건너뛰기 (로컬 전용)
CALLABO_SKIP_AWS_VAULT=1 $SKILL_SCRIPT <workspace>
```

> **Note**: `echo "" |`는 AWS Vault 비밀번호 프롬프트에 빈 문자열(엔터)을 자동 입력합니다.

### Step 3: 옵션 설정

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--name NAME` | tmux 세션 이름 | `--name my-callabo` |
| `-f, --force` | 기존 세션 종료 후 재시작 | `-f` |
| `--force-sync` | 의존성 강제 재설치 | `--force-sync` |
| `--skip-scheduler` | 스케줄러 pane 생성 안 함 | `--skip-scheduler` |
| `--with-scheduler` | 스케줄러 강제 활성화 | `--with-scheduler` |

### Step 4: 세션 관리

```bash
# 세션 목록 확인
tmux ls

# 세션 접속
tmux attach -t <session-name>

# 세션 분리 (tmux 내에서)
Ctrl+b, d

# 세션 종료
tmux kill-session -t <session-name>
```

---

## Examples

### 예시 1: 기본 실행

```
사용자: 콜라보 서버 띄워줘

Claude: Callabo 개발 서버를 시작하겠습니다.

📍 현재 워크스페이스: ~/work/feature-login

[명령 실행]
echo "" | ./scripts/run.sh ~/work/feature-login

✅ tmux 세션 'runtime-feature-login' 이(가) 준비되었습니다.

접속 명령:
tmux attach -t runtime-feature-login

실행 중인 서비스:
- callabo-server: http://localhost:8000
- callabo-webapp: http://localhost:3000
- magi: http://localhost:3200
- scheduler: 백그라운드 실행 중
```

### 예시 2: 커스텀 세션명으로 실행

```
사용자: my-dev라는 이름으로 콜라보 띄워줘

Claude: 커스텀 세션명으로 실행하겠습니다.

[명령 실행]
echo "" | ./scripts/run.sh . --name my-dev

✅ tmux 세션 'my-dev' 생성 완료

Pane 구성:
┌─────────────┬─────────────┐
│   server    │  scheduler  │
├─────────────┼─────────────┤
│   webapp    │    magi     │
└─────────────┴─────────────┘
```

### 예시 3: 기존 세션 강제 재시작

```
사용자: 콜라보 세션 다시 시작해줘

Claude: 기존 세션을 종료하고 재시작하겠습니다.

[명령 실행]
echo "" | ./scripts/run.sh . --force

기존 tmux 세션 'runtime-feature-login' 종료를 시도합니다...
기존 tmux 세션 'runtime-feature-login' 이(가) 정상적으로 종료되었습니다.
✅ 새 세션 시작 완료
```

### 예시 4: 스케줄러 없이 실행

```
사용자: 스케줄러 빼고 띄워줘

Claude: 스케줄러 없이 실행하겠습니다.

[명령 실행]
echo "" | ./scripts/run.sh . --skip-scheduler

✅ 세션 준비 완료 (scheduler 제외)

Pane 구성:
┌─────────────┬─────────────┐
│   server    │  (skipped)  │
├─────────────┼─────────────┤
│   webapp    │    magi     │
└─────────────┴─────────────┘
```

### 예시 5: 의존성 강제 재설치 후 실행

```
사용자: 의존성 다시 설치하고 띄워줘

Claude: 의존성을 재설치 후 실행하겠습니다.

[명령 실행]
echo "" | ./scripts/run.sh . --force-sync

[callabo-server] CALLABO_FORCE_SYNC=1: uv sync를 강제로 실행합니다...
[callabo-webapp] yarn install을 실행합니다...
[magi] pnpm install을 실행합니다...

✅ 의존성 설치 완료
✅ 세션 시작 완료
```

### 예시 6: 다른 워크스페이스 실행

```
사용자: ~/work/other-feature 워크스페이스 띄워줘

Claude: 지정된 워크스페이스를 실행하겠습니다.

[명령 실행]
echo "" | ./scripts/run.sh ~/work/other-feature

✅ tmux 세션 'runtime-other-feature' 준비 완료

접속: tmux attach -t runtime-other-feature
```

---

## Configuration

### 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `AWS_VAULT_PROFILE` | AWS Vault 프로파일 | `dev-callabo` |
| `AWS_VAULT_PASS` | AWS Vault 비밀번호 (빈 문자열이면 자동 엔터) | `""` |
| `CALLABO_SKIP_AWS_VAULT` | AWS Vault 건너뛰기 | 미설정 |
| `CALLABO_FORCE_SYNC` | 강제 의존성 설치 | `0` |
| `CALLABO_SKIP_SCHEDULER` | 스케줄러 비활성화 | `0` |
| `CALLABO_FORCE_SHUTDOWN_TIMEOUT` | 종료 대기 시간(초) | `15` |

**AWS Vault 자동 인증 (기본값):**
```bash
# AWS_VAULT_PASS가 설정되면 자동으로 비밀번호 입력
# 빈 비밀번호인 경우 (기본값)
AWS_VAULT_PASS="" ./run.sh

# 비밀번호가 있는 경우
AWS_VAULT_PASS="<your-password>" ./run.sh
```

### 포트 설정

각 서비스의 포트는 `.env` 파일에서 설정:

```bash
# callabo-server/.env
PORT=8000
UVICORN_PORT=8000

# callabo-webapp/.env
PORT=3000

# magi/.env
PORT=3200
```

### 세션 이름 규칙

`--name` 미지정 시 자동 생성:
```
runtime-{현재디렉토리이름}
```

예시:
- `~/work/feature-login` → `runtime-feature-login`
- `~/callabo-base` → `runtime-callabo-base`

---

## Tmux 단축키

세션 내에서 유용한 단축키:

| 단축키 | 설명 |
|--------|------|
| `Ctrl+b, d` | 세션 분리 (detach) |
| `Ctrl+b, o` | 다음 pane으로 이동 |
| `Ctrl+b, ;` | 이전 pane으로 이동 |
| `Ctrl+b, 방향키` | 해당 방향 pane으로 이동 |
| `Ctrl+b, z` | 현재 pane 확대/축소 |
| `Ctrl+b, [` | 스크롤 모드 진입 |
| `q` | 스크롤 모드 종료 |
| `Ctrl+c` | 현재 pane 프로세스 중단 |

---

## Best Practices

**DO:**
- 작업 전 기존 세션 확인 (`tmux ls`)
- 세션명을 기억하기 쉽게 지정
- 문제 발생 시 `--force`로 깨끗하게 재시작
- 의존성 문제 시 `--force-sync` 사용

**DON'T:**
- 같은 워크스페이스에 여러 세션 실행
- 프로세스 강제 종료 대신 graceful shutdown 사용
- AWS Vault 없이 실서버 연동 시도

---

## Troubleshooting

### tmux 세션 접속 안 됨

```bash
# 세션 존재 확인
tmux has-session -t <session-name>

# 세션 목록
tmux ls

# 모든 세션 종료 후 재시작
tmux kill-server
./run.sh
```

### AWS Vault 인증 오류

```bash
# AWS Vault 프로파일 확인
aws-vault list

# 수동 인증
aws-vault exec dev-callabo -- ./run.sh

# AWS Vault 건너뛰기 (로컬 전용)
CALLABO_SKIP_AWS_VAULT=1 ./run.sh
```

### 포트 이미 사용 중

```bash
# 포트 사용 프로세스 확인
lsof -i :8000
lsof -i :3000
lsof -i :3200

# 프로세스 종료
kill -9 <PID>

# 또는 기존 세션 강제 종료 후 재시작
./run.sh --force
```

### .venv 손상됨

```bash
# 강제 재설치
./run.sh --force-sync

# 또는 수동 재설치
cd callabo-server
rm -rf .venv
uv sync
```

### Pane이 바로 종료됨

```bash
# 로그 확인
# 각 서비스 디렉토리에서 직접 실행하여 에러 확인

# callabo-server
cd callabo-server && .venv/bin/python -m uvicorn asgi:app

# callabo-webapp
cd callabo-webapp && yarn dev

# magi
cd magi && pnpm dev
```

---

## Integration

이 스킬은 다음 스킬과 연동됩니다:

| 스킬 | 연동 방식 |
|------|-----------|
| callabo-init | 생성된 워크스페이스 실행 |
| context-worktree | 워크스페이스 전환 시 실행 |

### callabo-init과의 워크플로우

```
┌─────────────────────────────────────────────────────────────┐
│ 일반적인 개발 시작 흐름:                                     │
│                                                             │
│ [callabo-init] ──────────────────> [callabo-tmux]           │
│     │                                   │                   │
│     │ 워크스페이스 생성                  │ 서비스 실행       │
│     │ - 레포 클론                        │ - tmux 세션      │
│     │ - 브랜치 생성                      │ - 4개 pane       │
│     │ - .env 설정                        │ - 의존성 체크    │
│     │ - 포트 연동                        │                   │
│     ▼                                   ▼                   │
│  ~/work/feature-x/              runtime-feature-x 세션      │
└─────────────────────────────────────────────────────────────┘
```

**연속 사용 예시:**
```
사용자: 새 기능 개발 시작할게. 워크스페이스 만들고 서버 띄워줘

Claude:
1. [callabo-init 활성화]
   워크스페이스 생성 중...
   ./scripts/init-callabo-workspace.sh ~/work/new-feature feature/new
   ✅ 완료

2. [callabo-tmux 활성화]
   서비스 시작 중...
   echo "" | ./scripts/run.sh ~/work/new-feature
   ✅ tmux 세션 'runtime-new-feature' 준비됨
```

### context-worktree와의 연동

context-worktree가 활성화된 경우:
- 워크스페이스 전환 시 해당 워크스페이스의 tmux 세션 상태 확인
- 세션이 없으면 자동으로 callabo-tmux 실행 제안
- 세션이 있으면 기존 세션에 접속 안내

```
사용자: ~/work/other-feature로 전환해줘

Claude: [context-worktree + callabo-tmux 연동]
워크스페이스 전환: ~/work/other-feature

tmux 세션 'runtime-other-feature'가 존재하지 않습니다.
서비스를 시작할까요? [Y/n]
```

---

## Resources

| 항목 | 경로 |
|------|------|
| 실행 스크립트 | `./scripts/run.sh` |
| 서버 코드 | `<workspace>/callabo-server/` |
| 웹앱 코드 | `<workspace>/callabo-webapp/` |
| Magi 코드 | `<workspace>/magi/` |

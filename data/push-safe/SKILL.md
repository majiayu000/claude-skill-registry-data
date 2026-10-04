---
name: monggle-push-safe
version: 1.1.0
description: |
  Secrets 스캔 + 구조화 커밋 메시지 + 안전 push 절차
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
triggers:
  - /push-safe
  - monggle push-safe
---

# push-safe (monggle)

Secrets 스캔 + 구조화 커밋 메시지 + 안전 push 절차

**Usage:** `/push-safe [options]`

---

## 실행 순서

### 1단계: Secrets 스캔

`git diff --cached` 출력 대상으로 아래 패턴을 검사한다.

**파일명 패턴:**
- `\.env$` — .env 파일
- `\.pem$` — 인증서
- `\.key$` — 키 파일

**내용 패턴:**
- `API[_-]?KEY` — API 키 변수
- `SECRET[_-]?KEY` — Secret 키 변수
- `password\s*=` — 평문 패스워드
- `token\s*[:=]` — 토큰 대입
- `[0-9a-f]{32,}` — 32자 이상 hex 문자열
- `sk_live_[a-zA-Z0-9]+` — Stripe 라이브 키
- `ghp_[a-zA-Z0-9]+` — GitHub Personal Access Token

**발견 시 즉시 중단:**
```
[STOP] Secrets 감지됨
파일: <파일경로>
패턴: <매칭 패턴>

조치:
1. git reset HEAD <파일> 로 스테이징 취소
2. .gitignore에 해당 파일 추가
3. 이미 히스토리에 있다면 git-filter-repo 로 제거
```

Secrets가 없으면 2단계로 진행한다.

---

### 2단계: 구조화 커밋 메시지

staged 파일이 없으면 이 단계를 건너뛴다.

staged 파일이 있으면 아래 템플릿으로 커밋 메시지를 생성한다:

```
제목: [간결한 변경 요약 - 50자 이내]

상태: [add|fix|error|del]

설명:
[변경 이유와 목적을 3-5문장으로]

변경된 파일:

### [기능명 1]
- path/to/file1.ts (+15, -3)
- path/to/file2.tsx (+8, -0)

### [기능명 2]
- path/to/file3.js (+20, -5)
```

**author 규칙 (절대 불변):**
- Co-Authored-By·AI 공저자 태그 금지
- "Generated with Claude" 류 서명 금지
- author는 오너 계정(loboking)만

커밋 확정 전 메시지를 오너에게 보여주고 승인을 받는다.

---

### 3단계: push 절차

push-safe.sh 스크립트(`/Users/ws/monggle-vibe-coding-rules/.claude/commands/push-safe.sh`)에 따라 다음 순서로 실행한다:

**1. fetch — 원격 상태 동기화**
```bash
git fetch origin
```

**2. behind 체크 — 뒤처짐 감지**
```bash
# 로컬이 원격보다 뒤에 있으면 push 불가
```
뒤처진 경우: `/update` 실행을 안내하고 push를 중단한다. behind 상태에서는 절대 push하지 않는다.

**3. ahead 커밋 확인**
```bash
git log --oneline "@{u}.." | head -5
```
전송할 커밋 목록을 오너에게 보여준다. 없으면 종료.

**4. Team 모드 + 비main 브랜치 — PR 생성**
- `monggle.config.yaml`에서 `mode: team`이고 `--no-pr` 미사용이면
- 현재 브랜치가 main/master가 아닐 때 push 후 PR 자동 생성

**5. 일반 push**
```bash
git push origin <브랜치>
```

---

## 옵션

| 옵션 | 설명 |
|------|------|
| `--no-pr` | PR 생성 건너뜀 (Team 모드에서도) |
| `--branch <name>` | 지정 브랜치에 push |
| `--dry-run` | 실행 계획만 출력, 실제 변경 없음 |

---

## 안전 규칙

| 규칙 | 설명 |
|------|------|
| Secrets 발견 = 즉시 중단 | 패턴 매칭 시 push 불가 |
| force push 금지 | `--force`, `-f` 옵션 사용 금지 |
| author는 오너만 | AI 공저자 표기 절대 금지 |
| behind 상태 = push 불가 | 먼저 `/update` 실행 필수 |

---

## 시나리오

### 정상 push

```
사용자: /push-safe
태오: [1단계] staged diff 검사 중... Secrets 없음. 통과.
      [2단계] staged 파일 3개 감지. 커밋 메시지 생성:

      제목: fix: 로그인 토큰 만료 처리 개선

      상태: fix

      설명:
      토큰 만료 시 자동 재발급 로직이 누락되어 있었습니다.
      ...

      이 메시지로 커밋하시겠습니까?
사용자: 네
태오: [3단계] fetch → ahead 2커밋 확인 → git push origin main
      전송 완료.
```

### Secrets 발견

```
사용자: /push-safe
태오: [1단계] staged diff 검사 중...
      [STOP] Secrets 감지됨
      파일: config/database.yml
      패턴: password\s*=

      git reset HEAD config/database.yml 로 스테이징을 취소하고
      .gitignore에 추가하세요.
      push를 중단합니다.
```

### behind 상태

```
사용자: /push-safe
태오: [3단계] git fetch origin
      로컬이 원격보다 2커밋 뒤처져 있습니다.
      먼저 /update를 실행하세요.
      push를 중단합니다.
```

### dry-run

```
사용자: /push-safe --dry-run
태오: [DRY-RUN] 계획:
      1. Secrets 스캔 실행
      2. staged 파일 있으면 커밋 메시지 생성
      3. git fetch origin
      4. behind 체크
      5. ahead 커밋 확인
      6. git push origin main 실행 예정
      (실제 변경 없음)
```

---

## 절차 근거

- push 순서: `/Users/ws/monggle-vibe-coding-rules/.claude/commands/push-safe.sh`
- Secrets 패턴: `/Users/ws/.claude/agents/git-guardian.md` 33-65행
- 커밋 템플릿: git-guardian.md 31-49행

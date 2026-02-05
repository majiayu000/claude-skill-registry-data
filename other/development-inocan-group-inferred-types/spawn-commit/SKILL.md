---
name: spawn-commit
description: 빌드 성공 후 commit-agent를 활용하여 커밋 생성
allowed-tools: Task, Read
---

# Commit Agent 활용 가이드

빌드 성공 후 commit-agent를 사용하여 변경사항을 커밋하는 방법입니다.

## 핵심 원칙

**빌드 성공 후에만 커밋합니다.**

builder-agent가 성공적으로 완료된 후 commit-agent를 spawn합니다.

## 언제 사용하나?

- builder-agent 빌드 성공 후
- Step 완료 시점
- 테스트 통과 후

## 사전 조건

1. coder-agent: COMPLETED
2. builder-agent: COMPLETED (빌드 성공)

## Spawn 방법

### 1. 빌드 성공 확인

builder-agent 결과 확인:
```markdown
## builder-agent 결과
- 상태: COMPLETED
- 빌드: 성공
- 테스트: 통과
```

### 2. Spawn 실행

**반드시 Task tool을 사용합니다. Bash 명령어로 실행하지 마세요.**

```
Task tool 호출:
  subagent_type: "commit-agent"
  run_in_background: true
  prompt: |
    다음 작업을 수행해줘:
TASK-ID: TASK-001
Step: Step 2
변경 파일:
- src/auth/login.ts
- src/middleware/auth.ts

Step 설명: 사용자 인증 미들웨어 구현

.claude/agents/commit-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 3. 결과 대기

commit-agent 결과 확인:
- COMPLETED: 커밋 성공
- FAILED: 커밋 실패

## 정보 전달 항목

commit-agent에 전달해야 할 정보:

| 항목 | 설명 | 예시 |
|------|------|------|
| TASK-ID | Task 식별자 | TASK-001 |
| Step | 완료된 Step 번호 | Step 2 |
| 변경 파일 | 수정된 파일 목록 | src/auth/*.ts |
| Step 설명 | 작업 내용 요약 | 인증 미들웨어 구현 |

## 결과 처리

### 성공 시

```markdown
## commit-agent 결과
- 상태: COMPLETED
- 커밋 해시: abc1234
- 커밋 메시지: [TASK-001] Add user authentication middleware
- 커밋된 파일:
  - src/auth/login.ts
  - src/middleware/auth.ts
```

→ test-case-agent로 테스트 케이스 생성 진행

### 실패 시

```markdown
## commit-agent 결과
- 상태: FAILED
- 에러: pre-commit hook 실패
- 상세: ESLint 에러 발견
```

→ 에러 원인 분석 후 coder-agent에 수정 요청

## 워크플로우 통합

```
coder-agent (코드 작성)
    ↓
builder-agent (빌드/테스트)
    ↓ [성공 시]
commit-agent (커밋 생성) ← 이 시점
    ↓
test-case-agent (테스트 케이스 생성)
```

## 주의사항

1. **순서 준수**: 반드시 builder-agent 성공 후 실행
2. **민감 정보 확인**: commit-agent가 민감 파일 제외하는지 확인
3. **커밋 메시지 검증**: TASK-ID 포함 여부 확인
4. **실패 시 롤백**: 커밋 실패 시 다음 Step으로 진행하지 않음

---

<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->

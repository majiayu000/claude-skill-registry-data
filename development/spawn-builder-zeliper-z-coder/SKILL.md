---
name: spawn-builder
description: 빌드/테스트가 필요할 때 builder-agent 활용 가이드
allowed-tools: Task, Read, Bash
---

# Builder Agent 활용 가이드

코드 변경 후 빌드/테스트가 필요할 때 builder-agent를 활용하는 방법입니다.

## 언제 사용하나?

- coder-agent 작업 완료 후
- 코드 변경 확인이 필요할 때
- 테스트 실행이 필요할 때
- 빌드 에러 분석이 필요할 때

## Spawn 방법

### 1. coder-agent 완료 확인

coder-agent 결과가 COMPLETED인지 확인

### 2. Spawn 실행

**반드시 Task tool을 사용합니다. Bash 명령어로 실행하지 마세요.**

```
Task tool 호출:
  subagent_type: "builder-agent"
  run_in_background: true
  prompt: |
    다음 작업을 수행해줘:
task 파일: ./tasks/TASK-001.md
담당 Step: Step 2

coder-agent가 다음 파일을 수정했어:
- src/middleware/auth.ts
- src/routes/user.ts

빌드 및 테스트를 실행하고 결과를 보고해줘.
.claude/agents/builder-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 3. 결과 확인

builder-agent 결과 확인:
- COMPLETED: 빌드/테스트 성공
- 빌드 실패: 에러 분석 결과 포함
- PENDING_INPUT: 사용자 결정 필요

## 결과 처리

### 성공 시

```markdown
## builder-agent 결과
- 상태: COMPLETED
- 빌드: 성공
- 테스트: 성공 (통과 15개, 실패 0개)
```

→ Step 완료, 다음 Step 진행

### 실패 시

```markdown
## builder-agent 결과
- 상태: COMPLETED
- 빌드: 실패
- 에러: [에러 내용]
- 권장 조치: [조치 방안]
```

**재시도 로직:**

```
실패 횟수 < 3:
  → coder-agent에 에러 정보 전달
  → 수정 후 재빌드

실패 횟수 >= 3:
  → 사용자에게 보고
  → 수동 개입 요청
```

### USER_INPUT_REQUIRED 처리

```markdown
## builder-agent 결과
- 상태: PENDING_INPUT
- USER_INPUT_REQUIRED:
  - type: "choice"
  - reason: "React 버전 충돌"
  - options: ["React 18 업그레이드", "React 17 유지", "호환 shim 사용"]
```

**Main-agent 행동:**
1. AskUserQuestion으로 사용자에게 선택 요청
2. 사용자 응답 수신
3. 선택에 따라 coder-agent 또는 builder-agent 재실행

## LESSONS_LEARNED 연동

빌드 실패 시 자동으로 기록됨:

1. builder-agent가 에러 분석
2. `.claude/LESSONS_LEARNED.md`에 패턴 추가
3. 다음 작업 시 coder-agent가 참조

## 빌드 명령어

config.json에서 빌드/테스트 명령어 참조:

```json
{
  "commands": {
    "build": "npm run build",
    "test": "npm test"
  }
}
```

## 주의사항

1. **coder-agent 완료 후 실행**: 코드 변경 없이 빌드만 하지 않음
2. **재시도 제한**: 최대 3회까지만 자동 재시도
3. **결과 기록**: task 파일에 빌드 결과 기록
4. **에러 학습**: 새로운 에러는 LESSONS_LEARNED에 기록

---
<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->

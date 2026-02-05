---
name: spawn-coder
description: 코드 작성이 필요할 때 coder-agent 활용 가이드. 직접 코드 작성 대신 위임
allowed-tools: Task, Read
---

# Coder Agent 활용 가이드

코드 작성/수정이 필요할 때 coder-agent를 효과적으로 활용하는 방법입니다.

## 핵심 원칙

**Main-agent는 직접 코드를 작성하지 않습니다.**

모든 코드 작성/수정은 coder-agent에 위임합니다.

## 언제 사용하나?

- 새로운 코드 작성
- 기존 코드 수정
- 리팩토링
- 버그 수정
- 기능 추가

## Spawn 방법

### 1. Task 파일 확인

현재 진행 중인 Step 정보 파악:
- task 파일 경로
- Step 번호
- Step 상세 내용

### 2. Spawn 실행

**반드시 Task tool을 사용합니다. Bash 명령어로 실행하지 마세요.**

```
Task tool 호출:
  subagent_type: "coder-agent"
  run_in_background: true
  prompt: |
    다음 작업을 수행해줘:
task 파일: ./tasks/TASK-001.md
담당 Step: Step 2
작업 내용: 사용자 인증 미들웨어 구현

codebase-search-agent 결과:
- 관련 파일: src/middleware/auth.ts
- 기존 패턴: Express 미들웨어 형식

.claude/agents/coder-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 3. 결과 대기

coder-agent 결과 확인:
- COMPLETED: 성공적으로 완료
- PENDING_INPUT: 사용자 입력 필요

## 정보 전달 항목

coder-agent에 전달해야 할 정보:

| 항목 | 설명 |
|------|------|
| task 파일 경로 | 작업 컨텍스트 |
| Step 번호 | 담당 범위 |
| 검색 결과 | codebase-search-agent 결과 |
| 레퍼런스 | reference-agent 결과 (있는 경우) |
| 외부 정보 | web-search-agent 결과 (있는 경우) |

## USER_INPUT_REQUIRED 처리

coder-agent가 사용자 입력을 요청하면:

```markdown
## coder-agent 결과
- 상태: PENDING_INPUT
- USER_INPUT_REQUIRED:
  - type: "choice"
  - reason: "인증 방식 선택 필요"
  - options: ["JWT", "Session", "OAuth2"]
```

**Main-agent 행동:**
1. AskUserQuestion으로 사용자에게 선택 요청
2. 사용자 응답 수신
3. coder-agent에 결과 전달하여 작업 재개

## 결과 처리

### 성공 시

```markdown
## coder-agent 결과
- 상태: COMPLETED
- 수정 파일: [목록]
- 변경 내용: [요약]
```

→ builder-agent로 빌드 확인 진행

### 실패 시

- 에러 원인 분석
- 필요시 추가 정보 수집
- coder-agent 재실행

## 주의사항

1. **Step 범위 준수**: 담당 Step만 작업
2. **충분한 정보 제공**: 검색 결과 포함
3. **결과 확인**: PENDING_INPUT 플래그 확인
4. **빌드 연계**: 완료 후 반드시 builder-agent 실행

---
<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->

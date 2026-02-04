---
name: spawn-decision
description: 복잡한 판단이 필요할 때 decision-agent 활용 가이드
allowed-tools: Task, Read
---

# Decision Agent 활용 가이드

복잡한 판단이 필요할 때 decision-agent를 활용하는 방법입니다.

## 핵심 원칙

**/orchestrate가 직접 판단하기 어려운 경우에만 호출합니다.**

Opus 호출을 최소화하여 비용 효율을 유지합니다.

---

## 호출 트리거

### 자동 트리거 (필수 호출)

1. **새 태스크 시작 시**
   - 검색 에이전트 결과 수신 후
   - Plan Mode 진입 여부 결정 필요

2. **USER_INPUT_REQUIRED type="plan"**
   - 서브 에이전트가 상세 계획 필요 요청

3. **동일 에러 3회 이상 반복**
   - 근본 원인 분석 필요

### 수동 트리거 (/orchestrate 판단)

- 사용자 요청이 모호할 때
- 아키텍처 변경이 필요할 때
- 다중 구현 방식 중 선택 필요 시
- 파괴적 변경 가능성이 있을 때

---

## 호출하지 않는 경우

다음은 /orchestrate가 직접 처리:

- 단순 spawn 및 결과 전달
- 명확한 Step 실행
- 상태 업데이트
- 단순 USER_INPUT_REQUIRED (type="choice", "confirm")

---

## Spawn 방법

**반드시 Task tool을 사용합니다. Bash 명령어로 실행하지 마세요.**

### 새 태스크 분석

```
Task tool 호출:
  subagent_type: "decision-agent"
  run_in_background: true
  prompt: |

결정 유형: plan_mode
컨텍스트: {사용자 요청 원문}

검색 결과:
- codebase-search: {결과 요약}
- reference: {결과 요약}
- web-search: {결과 요약}

.claude/agents/decision-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 아키텍처 결정

```
Task tool 호출:
  subagent_type: "decision-agent"
  run_in_background: true
  prompt: |

결정 유형: architecture
컨텍스트: {결정이 필요한 상황}
선택지: [{옵션1}, {옵션2}, ...]

검색 결과:
- 기존 코드 패턴: {요약}
- 의존성 정보: {요약}

.claude/agents/decision-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 에러 해결

```
Task tool 호출:
  subagent_type: "decision-agent"
  run_in_background: true
  prompt: |

결정 유형: error_resolution
컨텍스트: {에러 상황 설명}

에러 정보:
- 에러 메시지: {메시지}
- 발생 위치: {파일:라인}
- 시도 횟수: {N}회

LESSONS_LEARNED 관련 내용:
{있으면 포함}

.claude/agents/decision-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

---

## 결과 처리

### ENTER_PLAN_MODE

```
decision-agent 결과:
- 권장 결정: ENTER_PLAN_MODE
- 질문: "어떤 영역을 최적화할까요?"
- 선택지: ["DB", "API", "프론트엔드"]
```

**/orchestrate 행동:**
1. Plan Mode로 전환
2. decision-agent 제안 질문을 AskUserQuestion으로 사용자에게 전달
3. 사용자 응답 대기

### EXECUTE

```
decision-agent 결과:
- 권장 결정: EXECUTE
- 권장 옵션: JWT (architecture인 경우)
```

**/orchestrate 행동:**
1. Execute Mode 유지
2. decision-agent 권장안으로 진행
3. todo-list-agent spawn

### NEED_MORE_INFO

```
decision-agent 결과:
- 권장 결정: NEED_MORE_INFO
- 필요 정보: 현재 데이터베이스 스키마
```

**/orchestrate 행동:**
1. 추가 검색 에이전트 spawn
2. 결과 수신 후 decision-agent 재호출

---

## 워크플로우 통합

### 새 태스크 수신 시

```
1. 검색 에이전트 병렬 spawn (/orchestrate)
   ├─ codebase-search-agent
   ├─ reference-agent
   └─ web-search-agent

2. 검색 결과 수신 후:
   → decision-agent spawn (Opus)
   → Plan Mode 여부 결정

3-A. ENTER_PLAN_MODE
   → 사용자에게 계획/질문 제시
   → 승인 대기

3-B. EXECUTE
   → todo-list-agent spawn
   → Step 실행 시작
```

### Step 실행 중 에러 발생

```
빌드 실패 (1회)
  → coder-agent 재시도

빌드 실패 (2회)
  → LESSONS_LEARNED 확인
  → coder-agent 재시도

빌드 실패 (3회)
  → decision-agent spawn (error_resolution)
  → 해결책 수신 후 적용
```

---

## 주의사항

1. **비용 최적화**: Opus 호출 최소화
2. **컨텍스트 전달**: 충분한 정보 제공
3. **결과 활용**: 권장안 우선 적용
4. **신뢰도 확인**: low인 경우 사용자 확인 권장

---
<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->

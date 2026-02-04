---
name: circuit-breaker
description: |
  무한 루프 및 토큰 폭주 방지를 위한 서킷 브레이커. Use when (1) 재귀 깊이 초과,
  (2) 동일 에러 반복, (3) 동일 파일 반복 수정, (4) 세션 시간 초과.
tools: [Read]
model: inherit
---

> **시스템 메시지**: 이 Skill이 트리거되면 `[SEMO] Skill: circuit-breaker 발동 - {조건}` 시스템 메시지를 출력하세요.

# Circuit Breaker Skill

> 무한 루프 방지 + Claude Code 세션 효율성 보호

## Purpose

Claude Code 환경에서 에이전트의 비효율적 동작을 감지하고 중단시키는 안전장치입니다.

**핵심 목표**:
- API 비용이 아닌 **세션 효율성** 중심
- 무한 루프/반복 작업 감지
- 사용자에게 명시적 확인 요청

---

## 트리거 조건

### Claude Code 환경 기준

| 조건 | 임계값 | 액션 | 심각도 |
|------|--------|------|--------|
| 재귀 깊이 | 15회 | 강제 종료 | CRITICAL |
| 동일 에러 반복 | 3회 | 에스컬레이션 | HIGH |
| 세션 시간 | 30분 | 경고 | MEDIUM |
| 동일 파일 수정 반복 | 5회 | 중단 | HIGH |
| 동일 명령 반복 | 5회 | 경고 | MEDIUM |

---

## 동작 플로우

```
┌─────────────────────────────────────────────┐
│             작업 시작                        │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│         카운터 증가 (재귀/에러/시간)          │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│              임계값 체크                     │
└─────────────────────────────────────────────┘
                    │
         ┌─────────┴─────────┐
         │                   │
    정상 범위            임계값 초과
         │                   │
         ▼                   ▼
    작업 계속        ┌───────────────┐
                    │ 서킷 브레이커  │
                    │    발동       │
                    └───────────────┘
                           │
                           ▼
                    ┌───────────────┐
                    │ 사용자 알림   │
                    │ + 확인 요청   │
                    └───────────────┘
```

---

## 감지 패턴

### 1. 재귀 깊이 초과

```markdown
**감지 조건**: 동일 작업이 15회 이상 중첩 호출

**예시**:
- Agent A → Agent B → Agent A → ... (15회 이상)
- Skill 호출이 계속 실패하며 재시도

**액션**:
[SEMO] Skill: circuit-breaker 발동 - 재귀 깊이 초과 (15회)

⚠️ **작업 중단**: 무한 루프가 감지되었습니다.
현재 호출 스택: {stack}
계속 진행하시겠습니까? (y/n)
```

### 2. 동일 에러 반복

```markdown
**감지 조건**: 동일한 에러 메시지가 3회 이상 발생

**예시**:
- 파일을 찾을 수 없음 (3회 연속)
- 권한 에러 (3회 연속)

**액션**:
[SEMO] Skill: circuit-breaker 발동 - 동일 에러 반복 (3회)

⚠️ **에러 패턴 감지**: "{에러 메시지}"
동일 에러가 3회 반복되었습니다.
다른 접근 방법을 제안하거나 사용자에게 에스컬레이션합니다.
```

### 3. 동일 파일 반복 수정

```markdown
**감지 조건**: 같은 파일을 5회 이상 수정 시도

**예시**:
- Edit 도구로 동일 파일 5회 이상 수정
- 수정 → 테스트 실패 → 수정 → 테스트 실패 반복

**액션**:
[SEMO] Skill: circuit-breaker 발동 - 동일 파일 반복 수정 (5회)

⚠️ **반복 수정 감지**: {파일명}
동일 파일을 5회 수정했습니다.
변경 내역을 검토하시겠습니까? (y/n)
```

### 4. 세션 시간 초과

```markdown
**감지 조건**: 단일 세션이 30분 이상 지속

**액션**:
[SEMO] Skill: circuit-breaker 경고 - 세션 시간 30분 초과

⚠️ **긴 세션 경고**: 현재 세션이 30분을 초과했습니다.
진행 상황:
- 완료: {completed_tasks}
- 진행 중: {current_task}

계속 진행하시겠습니까? (y/n)
```

---

## 에스컬레이션 절차

### 심각도별 대응

| 심각도 | 대응 | 사용자 액션 |
|--------|------|------------|
| CRITICAL | 즉시 중단 | 재시작 필요 |
| HIGH | 중단 + 확인 | 계속/중단 선택 |
| MEDIUM | 경고 + 계속 | 무시 가능 |
| LOW | 로그만 | 자동 |

### 에스컬레이션 메시지 형식

```markdown
[SEMO] Skill: circuit-breaker 에스컬레이션

## 상황
- **조건**: {trigger_condition}
- **심각도**: {severity}
- **발생 횟수**: {count}

## 컨텍스트
- 현재 작업: {current_task}
- 마지막 성공 작업: {last_success}
- 실패 히스토리: {failure_history}

## 권장 조치
1. {recommendation_1}
2. {recommendation_2}

---
계속 진행하시겠습니까? [y/n/다른 접근법 제안]
```

---

## 상태 추적

### 추적 항목

```json
{
  "session_id": "uuid",
  "start_time": "2025-01-01T00:00:00Z",
  "counters": {
    "recursion_depth": 0,
    "same_error_count": 0,
    "same_file_edit_count": 0,
    "same_command_count": 0
  },
  "history": {
    "errors": [],
    "edited_files": [],
    "commands": []
  },
  "breaker_status": "CLOSED"
}
```

### 상태 전이

```
CLOSED (정상) → OPEN (발동) → HALF_OPEN (테스트) → CLOSED
```

---

## SEMO Message Format

```markdown
[SEMO] Skill: circuit-breaker 발동 - {조건}

[SEMO] Skill: circuit-breaker 경고 - {조건}

[SEMO] Skill: circuit-breaker 해제 - 사용자 승인
```

---

## References

- [SEMO Core Principles](../../PRINCIPLES.md)
- [SEMO 네이밍 규칙](../../../../docs/SEMO_NAMING_CONVENTION.md)

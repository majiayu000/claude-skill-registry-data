---
name: parallel-agent-orchestration
description: >
  병렬 에이전트 오케스트레이션. Fan-Out/Fan-In 패턴으로 다중 에이전트 실행.
version: 2.0.0

triggers:
  keywords:
    - "병렬 개발"
    - "parallel"
    - "multi-agent"
    - "동시 실행"
    - "병렬 테스트"
  file_patterns: []
  context:
    - "다중 작업 동시 처리"
    - "병렬 에이전트 실행"

capabilities:
  - run_parallel
  - fan_out_fan_in
  - aggregate_results

model_preference: sonnet

phase: [1, 2]
auto_trigger: true
dependencies:
  - debugger
  - code-reviewer
token_budget: 1200
---

# Parallel Agent Orchestration

병렬 에이전트 실행 및 결과 집계 워크플로우입니다.

## Quick Start

```bash
# 병렬 개발 에이전트 실행
python .claude/skills/parallel-agent-orchestration/scripts/run_parallel.py \
  --agents "architect,coder,tester" \
  --task "새 기능 구현"

# 병렬 테스트 에이전트 실행
python scripts/run_parallel.py \
  --agents "unit,integration,e2e,security" \
  --task "전체 테스트 실행"
```

## Fan-Out/Fan-In 패턴

```
┌─────────────┐
│  Supervisor │  ← Task 분해
└──────┬──────┘
       │
   ┌───┼───┐      ← Fan-Out
   ↓   ↓   ↓
 [A1] [A2] [A3]   ← 병렬 실행
   │   │   │
   └───┼───┘      ← Fan-In
       ↓
┌─────────────┐
│ Aggregator  │  ← 결과 종합
└─────────────┘
```

## 에이전트 그룹

### 개발 그룹 (dev)

| 에이전트 | 역할 |
|----------|------|
| architect | 설계 및 구조 |
| coder | 구현 |
| tester | 테스트 작성 |
| docs | 문서화 |

### 테스트 그룹 (test)

| 에이전트 | 역할 |
|----------|------|
| unit | 단위 테스트 |
| integration | 통합 테스트 |
| e2e | E2E 테스트 |
| security | 보안 테스트 |

### 리뷰 그룹 (review)

| 에이전트 | 역할 |
|----------|------|
| code-reviewer | 코드 리뷰 |
| security-auditor | 보안 리뷰 |
| architect-reviewer | 아키텍처 리뷰 |

## 실행 옵션

```bash
# 그룹 단위 실행
python scripts/run_parallel.py --group dev --task "기능 구현"

# 개별 에이전트 지정
python scripts/run_parallel.py --agents "coder,tester" --task "빠른 구현"

# 타임아웃 설정
python scripts/run_parallel.py --group test --timeout 300 --task "테스트"
```

## 결과 집계

### 성공 기준

| 그룹 | 성공 조건 |
|------|----------|
| dev | 모든 에이전트 완료 |
| test | 모든 테스트 통과 |
| review | Critical 이슈 없음 |

### 실패 처리

```
1회 실패 → 해당 에이전트 재실행
2회 실패 → 에러 로그 분석 → 수정 시도
3회 실패 → ⏸️ 수동 개입
```

## 관련 커맨드

| 커맨드 | 그룹 |
|--------|------|
| `/parallel-dev` | dev |
| `/parallel-test` | test |
| `/parallel-review` | review |

---

> 참조: CLAUDE.md 섹션 4 Agents

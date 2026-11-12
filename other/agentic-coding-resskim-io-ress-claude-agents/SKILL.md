---
name: agentic-coding
description: "AI 코딩 에이전트 활용 — 4가지 agentic coding 모드, agent supervision, multi-agent 조율, 코드 리뷰 방식, 모델 라우팅. Use when Claude Code 같은 에이전트에 코딩을 맡기고 감독·검증 방식을 정할 때."
---

# Agentic Coding Patterns

AI 코딩 에이전트 활용 패턴, Agent Supervision, Multi-Agent 조율, Agentic Era 코드 리뷰

## Quick Reference (결정 트리)

```
Agentic Coding 모드 선택?
    │
    ├─ 단일 작업 (버그 수정, 작은 기능) ──> Conductor 모드
    │       └─ 동기, 실시간 가이드, 1 agent
    │
    ├─ 대규모 기능 (다중 파일) ──────────> Orchestrator 모드
    │       └─ 비동기, 다수 agent, 각자 context window
    │
    ├─ 품질 중시 (리뷰 필수) ────────────> Evaluator-Optimizer Loop
    │       └─ Generator + Evaluator 반복
    │
    └─ 파이프라인 (단계적 변환) ─────────> Sequential Pipeline
            └─ 각 단계 출력 → 다음 입력

Agent 자율성 수준?
    │
    ├─ Level 1: 인간 주도 ────> 매 단계 승인, agent는 제안만
    ├─ Level 2: Agent 주도 ───> 자율 실행, 전략적 체크포인트 (권장)
    └─ Level 3: 완전 자율 ────> 시간 단위 자율 실행, 결과만 검토

Model Routing?
    │
    ├─ 분류, 의도 감지, 포맷팅 ──> 경량 모델 (Haiku, GPT-4o-mini)
    ├─ 코드 생성, 리팩토링 ──────> 중간 모델 (Sonnet, GPT-4o)
    └─ 아키텍처, 복잡한 추론 ────> Frontier 모델 (Opus, o1)
```

---

## 4가지 Agentic Coding 모드

### 1. Conductor 모드 (동기, 단일 Agent)

```
Developer ──prompt──> Agent ──output──> Developer ──feedback──> Agent
                         │                                        │
                    실시간 응답                              즉시 반영
```

- 단일 agent를 실시간으로 가이드
- 매 응답마다 개발자가 검토/수정 지시
- 적합: 버그 수정, 작은 리팩토링, 탐색적 코딩
- 도구: Claude Code interactive, Cursor, Copilot Chat

### 2. Orchestrator 모드 (비동기, Multi-Agent)

```
┌──────────────────────────────────────────────┐
│              Orchestrator                      │
│  - 작업 분해 → 서브태스크                      │
│  - Agent 할당 → 병렬 실행                      │
│  - 결과 통합 → 품질 검증                       │
└──────────────────────────────────────────────┘
         │              │              │
    ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
    │ Agent A │   │ Agent B │   │ Agent C │
    │ 모듈 구현│   │ 테스트  │   │ 문서    │
    └─────────┘   └─────────┘   └─────────┘
```

- 각 agent가 독립 context window에서 작업
- 병렬 실행으로 처리량 극대화
- 적합: 대규모 기능, cross-module 변경, 프로젝트 부트스트랩
- 도구: Claude Code `Agent` tool, Claude Code Teams

### 3. Evaluator-Optimizer Loop

```
Generator ──코드──> Evaluator ──피드백──> Generator ──개선──> ...
    │                   │
    │              품질/보안/성능
    │              기준 검증
    └──────── 수렴할 때까지 반복 ──────────┘
```

- 생성 agent와 평가 agent 분리
- 반복적 품질 개선 (코드 리뷰, 최적화, 보안 강화)
- 주의: MAX_ITERATIONS 설정 필수 (무한 루프 방지)
- 적합: 리팩토링, 성능 최적화, 보안 감사

### 4. Sequential Pipeline

```
Spec ──> Agent 1 ──> API Design ──> Agent 2 ──> Implementation ──> Agent 3 ──> Tests
         (설계)                      (구현)                        (검증)
```

- 각 단계의 출력이 다음 단계의 입력
- 단계별 최적화/검증 가능
- 적합: API-first 개발, 스펙→구현→테스트 워크플로우

---

## Agent Supervision 패턴

### Context Engineering (핵심)

Agent의 품질은 주입된 컨텍스트 품질에 비례한다.

```
┌─────────────────────────────────────────┐
│          Context Engineering             │
├─────────────────────────────────────────┤
│                                          │
│  CLAUDE.md / Rules                       │
│  ├─ 코딩 컨벤션 (lint 규칙 아닌 설계 원칙) │
│  ├─ 아키텍처 결정 (ADR 요약)              │
│  ├─ 금지 패턴 (anti-patterns)            │
│  └─ 테스트 전략 (TDD 요구사항)            │
│                                          │
│  MCP Servers                             │
│  ├─ GitHub (이슈, PR 컨텍스트)            │
│  ├─ DB schema (도메인 모델)               │
│  └─ 모니터링 (운영 데이터)                │
│                                          │
│  Skills / Custom Instructions            │
│  ├─ 도메인 지식 (비즈니스 룰)             │
│  └─ 팀 워크플로우                        │
│                                          │
└─────────────────────────────────────────┘
```

**CLAUDE.md 작성 원칙:**
- 사람과 AI 모두 읽을 수 있게 명시적으로 작성
- "좋은 코드를 작성하라" (X) → "Guard Clause로 early return, 메서드 50줄 이내" (O)
- 예시 코드 포함 (BAD/GOOD 패턴)

### 루프 방지

```yaml
# Agent 실행 제약
constraints:
  maxIterations: 8          # 최대 반복 횟수
  reflectionBeforeRetry: true  # 재시도 전 반성 프롬프트
  timeoutMinutes: 30        # 시간 제한
  escalateOnStuck: true     # 막히면 인간에게 에스컬레이션
```

### Human-in-the-Loop 체크포인트

```
자율 실행 ──────────────────────> 체크포인트 ──> 자율 실행 ──> ...
                                     │
                               인간 검증 지점:
                               - 아키텍처 결정
                               - 외부 API 통합
                               - 보안 관련 변경
                               - 데이터 스키마 변경
```

Level 2 (Agent 주도) 권장: 대부분 자율 실행하되 전략적 지점에서만 인간 개입.

### TDD with Agents

```
1. 인간: 요구사항 정의 + 수용 기준
2. Agent: 테스트 작성 (수용 기준 기반)
3. 인간: 테스트 검토 & 승인
4. Agent: 테스트 통과하는 코드 구현
5. 규칙: Agent는 테스트를 수정할 수 없음 (테스트 = 계약)
```

---

## Agentic Era의 Code Review

### 인지 부하 변화

기존: 내가 쓴 코드를 동료가 리뷰
현재: **Agent가 쓴 코드를 내가 리뷰** → 전체 컨텍스트 파악 부하 증가

### Generator-Evaluator 분리 패턴

```
┌─────────────┐         ┌─────────────┐
│  Code Agent │ ──PR──> │ Review Agent│ ──코멘트──> 인간 최종 판단
│  (생성)     │         │  (평가)     │
└─────────────┘         └─────────────┘
```

- Review Agent가 1차 필터링 (보안, 패턴, 성능)
- 인간은 아키텍처 결정, 비즈니스 로직에 집중
- CI에 자동 리뷰 통합: `code-reviewer` agent 활용

### 리뷰 포커스 전환

| 기존 (인간 코드) | Agentic Era (AI 코드) |
|-----------------|---------------------|
| 스타일/포맷 | Agent가 규칙 준수 → 스킵 |
| 로직 정확성 | **핵심** — Agent가 잘못 이해할 수 있음 |
| 엣지 케이스 | **핵심** — Agent가 놓치기 쉬움 |
| 아키텍처 적합성 | **최우선** — 시스템 전체 맥락 |
| 불필요한 복잡성 | **주의** — Agent가 과도 엔지니어링 경향 |

---

## Model Routing 전략

```
┌──────────────────────────────────────────────────┐
│                 Model Router                      │
├──────────────────────────────────────────────────┤
│  Task Classification → Model Selection            │
│                                                    │
│  ┌────────────────┐  ┌────────────────┐           │
│  │ Simple Tasks   │  │ Complex Tasks  │           │
│  │ - 포맷팅       │  │ - 아키텍처 설계│           │
│  │ - 단순 수정    │  │ - 복잡한 추론  │           │
│  │ - 분류         │  │ - 다중 파일    │           │
│  │                │  │                │           │
│  │ → 경량 모델    │  │ → Frontier 모델│           │
│  │   비용: $      │  │   비용: $$$$   │           │
│  └────────────────┘  └────────────────┘           │
│                                                    │
│  최적화 축: Latency × Accuracy × Cost              │
└──────────────────────────────────────────────────┘
```

| 작업 유형 | 권장 모델 계층 | 근거 |
|----------|-------------|------|
| 코드 포맷팅, 린트 수정 | 경량 (Haiku) | 규칙 기반, 추론 불필요 |
| 단위 테스트 생성 | 중간 (Sonnet) | 패턴 인식 필요 |
| 리팩토링, 기능 구현 | 중간~고급 | 컨텍스트 이해 필요 |
| 아키텍처 결정, 복잡 디버깅 | Frontier (Opus) | 깊은 추론 필수 |

---

## 실전 사례 (2026)

| 조직 | 성과 | 패턴 |
|------|------|------|
| Rakuten | 1250만줄 코드베이스, 7시간 자율 실행으로 복잡 기능 구현 | Orchestrator + 자율 실행 |
| TELUS | 13,000+ AI 솔루션, 30% 속도↑, 50만 시간 절약 | 전사 AI 에이전트 배포 |
| Zapier | 89% AI 채택, 800+ agent 내부 배포 | 엔지니어링 넘어 전사 확대 |
| CRED | 1500만 사용자, 실행 속도 2배 | Agent 주도 개발 |
| Augment | 4-8개월 프로젝트를 2주로 단축 | Multi-agent orchestration |

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| MAX_ITERATIONS 미설정 | 무한 루프 → 비용 폭증 | 8회 제한 + reflection |
| Context 없이 agent 실행 | 낮은 품질, 컨벤션 무시 | CLAUDE.md + Rules 필수 |
| Agent 출력 무검토 수용 | 미묘한 버그, 과도 엔지니어링 | 인간 리뷰 필수 |
| 모든 작업에 Frontier 모델 | 비용 10-50배 | Model routing 적용 |
| 테스트 없이 자율 실행 | 회귀 버그 미감지 | TDD with Agents |
| Agent에게 아키텍처 위임 | 일관성 없는 설계 | 인간이 아키텍처, Agent가 구현 |

---

## 체크리스트

### Agent 설정
- [ ] CLAUDE.md / Rules에 코딩 컨벤션 명시
- [ ] MAX_ITERATIONS + timeout 설정
- [ ] Human checkpoint 지점 정의
- [ ] Model routing 규칙 설정

### 워크플로우
- [ ] 작업 유형별 Agentic 모드 선택
- [ ] TDD 워크플로우 설정 (테스트 먼저)
- [ ] Generator-Evaluator 리뷰 파이프라인
- [ ] 에스컬레이션 경로 정의

### 거버넌스
- [ ] 비용 모니터링 (모델별, 작업별)
- [ ] 품질 메트릭 수집 (성공률, 리뷰 통과율)
- [ ] 보안 가드레일 (시크릿, PII 필터)

---

## Claude 5.5 Agentic 작업 (2026-11 검증)

Opus 5.5·Sonnet 5.5 공식 가이드 기준. 하네스나 orchestrator 를 만들 때 조정할 점이다.

- **Effort** — 범위가 명확하면 `medium`, 어렵거나 길면 `high`. `xhigh`·`max` 는 품질 향상을 측정한 작업에만
- **완료 판정은 따로 검증한다** — Opus 5.5: "Treat a text-only end of turn as a report rather than as proof the task is done." Sonnet 5.5 는 낮은 effort 에서 검증 없이 완료를 보고할 수 있다. Evaluator-Optimizer Loop 의 검증 단계를 남겨 둔다
- **Fan-out 은 명시한다** — 기본 spawn 빈도는 문서에 없다. 병렬 작업이 필요하면 프롬프트에 적는다 ("Use subagents for each of: frontend, backend, database")
- **중간 확인** — Sonnet 5.5 는 low·medium 의 긴 작업에서 멈추고 확인하는 경우가 늘어난다. 자율 진행이 필요하면 프롬프트에 명시한다
- **Progress 표시** — Opus 5.5 의 진행 메모는 thinking block 으로 오며 "their text is empty at the default thinking.display". UI 에 보이려면 `display` 를 지정한다
- **대화 기록은 append-only** — Opus 5.5 는 앞선 기록을 수정한 뒤 thinking block 을 재전송하면 400 을 반환한다 (2026-08-31 이후 생성 계정)
- **effort 변경은 캐시를 깨뜨린다** — "Changing the top-level effort value between requests invalidates the prompt cache"

세부: `/dx:token-budget` · `rules/harness/token-budget.md`

---

## 참조 스킬

- `dx-ai-agents.md` — AI 에이전트 거버넌스, 엔터프라이즈 정책
- `dx-ai-agents-orchestration.md` — 멀티 에이전트 오케스트레이션 상세
- `dx-ai-security.md` — AI 코드 보안 & 품질 보증
- `agentic-ai-architecture.md` — Agentic AI 시스템 아키텍처
- `finops-ai.md` — AI 비용 관리, Model routing 비용

---

## Sources

- [Anthropic 2026 Agentic Coding Trends Report](https://resources.anthropic.com/2026-agentic-coding-trends-report)
- [Addy Osmani: The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)
- [Missing Semester: Agentic Coding](https://missing.csail.mit.edu/2026/agentic-coding/)
- [Stack Overflow: Coding Guidelines for AI and People](https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/)
- [CodeScene: Agentic AI Coding Best Practices](https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality)
- [Google Cloud: Code Reviews in the Agentic Era](https://medium.com/google-cloud/how-to-do-code-reviews-in-the-agentic-era-0b6584700f47)

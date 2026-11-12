---
name: token-budget
description: "Claude 5.5 세대 토큰·컨텍스트·effort 운영 심화 가이드 — Subagent 위임, Effort, Task Budget, Prompt Caching, Thinking, Tokenizer 를 코드 예시와 비용 계산으로 설명. Use when API 비용을 줄이거나 effort·캐시 설정을 정할 때."
---

# Token Budget 심화 가이드 (Claude 5.5 세대)

[`token-budget.md`](https://github.com/ressKim-io/ress-claude-agents/blob/main/.claude/rules/harness/token-budget.md)의 상세판. API 파라미터, 코드 예시, 비용 계산 포함.
가격·파라미터는 2026-11-04 공식 문서 기준이다. 사용 전 [공식 가격표](https://platform.claude.com/docs/en/about-claude/pricing)를 다시 확인한다.
Claude Code 세션 내 도구 사용 효율은 `/dx:token-efficiency` 참조.

## Quick Reference

| 상황 | 해결책 | 참조 |
|------|------|------|
| context 80% 도달 | `/clear` 또는 세션 재시작 | #context-window |
| 탐색성 작업 10+ 파일 | subagent 위임 | #subagent-delegation |
| 코딩/agentic 작업 | effort `medium`, 어렵거나 길면 `high` | #effort-level |
| agentic loop 비용 제어 | Task Budget (beta) | #task-budget |
| 반복 prompt 입력 비용 절감 (읽기 0.025x~0.1x) | Prompt Caching | #prompt-caching |
| 모델 전환 후 캐시 무효화 | tokenizer 변경 대응 | #tokenizer-change |

---

## Context Window (1M tokens)

### Claude Code vs API

| 항목 | Claude Code | Messages API |
|------|------------|--------------|
| Context size | 1M tokens (자동) | 1M tokens |
| 80% 경고 | 상태바 표시 | 클라이언트 직접 추적 |
| Compaction | `/compact` 명령 | 수동 구현 |
| Cache management | 자동 | `cache_control` 수동 |

### 세션 관리 원칙 (Claude Code)

```
# 무관 태스크 전환
/clear

# 마일스톤 완료 직후 (선제)
/compact Focus on API changes and test results

# 부분 요약 (checkpoint에서)
Esc + Esc → 메시지 선택 → "Summarize from here"

# 세션 간 이동
/rename oauth-migration
claude --resume
```

### 공식 실패 패턴 (Claude Code Best Practices)

- **Kitchen sink session** — 무관 태스크 누적 → `/clear`
- **Over-correction** — 2회 이상 같은 실수 교정 → `/clear` + 재프롬프트
- **Over-specified CLAUDE.md** — 룰 묻힘 → 가지치기 (ask "removing this causes mistakes?")
- **Trust-then-verify gap** — 검증(tests/scripts) 없이 ship 금지
- **Infinite exploration** — 범위 미설정 → subagent로 격리

---

## Subagent Delegation

기본 spawn 빈도는 공식 문서에 없다. fan-out 이 필요하면 프롬프트에 명시한다.

### 위임 기준

| 상황 | 주 대화 | Subagent |
|------|----|----|
| 10+ 파일 탐색/조사 | ❌ | ✅ |
| 복잡 코드베이스 구조 파악 | ❌ | ✅ |
| 리뷰/검증 (편향 방지) | ❌ | ✅ |
| 단일 함수 리팩토링 | ✅ | ❌ |
| 이미 읽은 파일 수정 | ✅ | ❌ |

### 명시 지시 패턴

```
# ✅ Fan-out 필요
"Use subagents to investigate X, Y, Z in parallel and report back"
"Spawn specialists for each of: frontend, backend, database"

# ✅ Context 격리
"Use a subagent to explore the auth system and summarize findings"

# ❌ 모호 — fan-out 여부를 모델 판단에 맡긴다
"Look into this codebase"
```

### 공식 Writer/Reviewer 패턴

| Session A (Writer) | Session B (Reviewer) |
|--------------------|----------------------|
| "Implement rate limiter" | - |
| - | "Review @src/middleware/rateLimiter.ts for race conditions" |
| "Address: [Session B feedback]" | - |

Fresh context = 편향 없는 리뷰.

---

## Effort Level

### 레벨별 사용 상황

| 레벨 | 사용 상황 |
|------|---------|
| `low` | 단순 조회·분류·속도 우선 |
| `medium` | 범위가 명확한 코딩·분석. **Opus 5.5 시작점** |
| `high` | 어렵거나 긴 작업, 리뷰, 조사 |
| `xhigh` / `max` | "where you've measured a quality gain" 인 작업만 |

레벨 간 비용 배수는 공식 문서에 없다. "It shapes behavior but doesn't guarantee a token count." 모델별 지원과 기본값은 [`effort-guide.md`](https://github.com/ressKim-io/ress-claude-agents/blob/main/.claude/rules/harness/effort-guide.md) 참조.

### API 코드 예시

```python
import anthropic

client = anthropic.Anthropic()

# 코딩/agentic → medium 부터, 어렵거나 길면 high
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=128000,  # 공식 제안: agentic 코딩 128,000
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "..."}],
)

# 분류·단순 추출 → low
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=2048,
    output_config={"effort": "low"},
    messages=[{"role": "user", "content": "..."}],
)
```

### 얕은 추론 감지 시

```
# ❌ prompting으로 우회
"This is complex. Think very carefully..."

# ✅ effort 레벨 상향
output_config={"effort": "high"}
```

단, `low`를 유지해야 할 이유(지연)가 있으면 타겟팅된 가이드 추가:
```
"This task involves multi-step reasoning. Think carefully before responding."
```

---

## Task Budget (beta, API only)

> **Claude Code 미지원**. Messages API 직접 호출 시만 해당.
>
> 지원 모델: Fable 5.2, Fable 5.1, Fable 5, Mythos 5.2, Mythos 5.1, Mythos 5, Opus 5.5, Opus 5, Sonnet 5.5, Haiku 5.5, Opus 4.8, Opus 4.7. Sonnet 5, Opus 4.6, Sonnet 4.6, Haiku 4.5 는 미지원.

### 핵심 특성

- **Advisory cap** (soft hint) — hard cap 아님
- **Agentic loop 전체** target (multiple requests 합산)
- **최소 20,000 토큰** (아래는 400 에러)
- `max_tokens`와 **독립** (per-request ceiling과 다름)

### API 사용법

```python
response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=128000,  # per-request hard cap
    output_config={
        "effort": "high",
        "task_budget": {"type": "tokens", "total": 64000},  # loop advisory
    },
    messages=[...],
    betas=["task-budgets-2026-03-13"],
)
```

### Budget 크기 결정 (공식 권장)

1. 대표 샘플을 **budget 없이** 실행
2. `usage.output_tokens` + thinking + tool result 토큰 합산
3. **p99 값**을 초기 budget으로 설정
4. 테스트하며 ±20% 조정

### 주의 사항

| 패턴 | 결과 |
|------|------|
| 너무 작은 budget | **refusal-like behavior** — 작업 거부하거나 조기 종료 |
| Follow-up마다 `remaining` 변경 | **cache prefix 무효화** (90% 절감 소실) |
| 오픈엔디드 품질 우선 작업에 사용 | 부적합 — budget 설정하지 말 것 |

### Caching 보존 패턴

```python
# ✅ 초기 요청에만 budget 설정
output_config = {"effort": "high", "task_budget": {"type": "tokens", "total": 128000}}

# ✅ 후속 요청: budget 생략, 서버가 countdown 유지
# (단, compaction이 있을 때만 remaining 재전달)

# ❌ 매번 remaining 감소하며 전달 → cache 무효화
output_config = {"task_budget": {"total": 128000, "remaining": 89000}}  # 매 turn 바뀜
```

---

## Prompt Caching

### 경제학 (Opus 5.5 $4/MTok 기준)

| 비용 | 배수 | 실제 |
|------|------|------|
| 기본 입력 | 1.0x | $4/MTok |
| 5분 캐시 쓰기 | 1.25x | $5/MTok |
| 1시간 캐시 쓰기 | 2.0x | $8/MTok |
| **캐시 읽기** | **0.05x** | **$0.20/MTok (95% 절감)** |

읽기 배수는 모델마다 다르다: Opus·Sonnet 5.5 는 0.05x, Fable 5.2·5.1 은 0.025x, Haiku 5.5 와 그 이전 모델은 0.1x.

ROI: 1회 재사용만 해도 5분 TTL 회수, 2회면 1시간 TTL 회수.

### 구조 규칙 (MUST)

```python
# ✅ 정적 → 동적 순서, 캐시 지점은 불변 블록
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are a legal document analyst.",  # 정적
        },
        {
            "type": "text",
            "text": f"[50페이지 문서]",                     # 정적 대용량
            "cache_control": {"type": "ephemeral"},         # ← 여기 캐시
        },
    ],
    messages=[
        {"role": "user", "content": "주요 조항 분석"},      # 동적 (뒤)
    ],
)
```

### 안티패턴

```python
# ❌ 변동 콘텐츠에 cache_control
{"text": f"Current time: {now()}", "cache_control": {...}}

# ❌ 짧은 TTL을 긴 TTL보다 앞에
system=[
    {"text": "...", "cache_control": {"type": "ephemeral"}},          # 5분
    {"text": "...", "cache_control": {"type": "ephemeral", "ttl": "1h"}},  # 1시간 (역순 — 무효화)
]
```

### TTL 선택

| TTL | 용도 |
|-----|------|
| **5분 (기본)** | 빈번한 반복, 자주 쓰는 시스템 프롬프트 |
| **1시간** | 장기 agentic 루프, 사용자 응답 대기 긴 대화 |

### 캐시 무효화 조건

| 변경 | 도구 캐시 | 시스템 캐시 | 메시지 캐시 |
|------|---------|----------|----------|
| 도구 정의 수정 | ✘ | ✘ | ✘ |
| tool_choice 변경 | ✓ | ✓ | ✘ |
| 이미지 추가/제거 | ✓ | ✓ | ✘ |
| thinking 파라미터 | ✓ | ✓ | ✘ |

요청 사이에 top-level effort 를 바꿔도 캐시가 깨진다: "Changing the top-level effort value between requests invalidates the prompt cache."

### 성능 모니터링

```python
print(response.usage)
# {
#   "cache_read_input_tokens": 100000,      # ← 캐시 적중
#   "cache_creation_input_tokens": 248,
#   "input_tokens": 50,
# }
```

`cache_read_input_tokens`와 `cache_creation_input_tokens` 모두 0이면 캐시 미작동 — 최소 토큰 길이(모델별 512~4,096), 캐시 지점 위치, TTL 내 재요청 여부 점검.

### Workspace Isolation (2026-02-05부터)

- Anthropic API: Organization → **Workspace** 격리
- Bedrock/Vertex: 조직 수준 유지 (미변경)
- 영향: 여러 workspace 사용 시 독립 캐시 — 전략 재검토

---

## Thinking

### Opus 5.5

```python
# ❌ 구 방식 — 400 에러
thinking = {"type": "enabled", "budget_tokens": 32000}

# ✅ thinking 필드 생략 (adaptive 와 동일), 깊이는 effort 로 제어
output_config = {"effort": "high"}
```

- thinking 은 **항상 켜져 있다.** `{"type": "adaptive"}` 를 보내도 되지만 생략과 같다
- `{"type": "disabled"}` 는 400 이다
- Sonnet 5.5 에서 끄려면 `{"type": "between_tools"}` 를 쓴다 (xhigh·max 와 함께 쓰면 400)

### Thinking 표시

```python
# 기본 display 에서는 thinking text 가 비어 있다. Opus 5.5 의 진행 메모도 여기에 온다
# UI에 표시하려면:
thinking = {
    "type": "adaptive",
    "display": "summarized",  # 또는 "omitted"
}
```

### 거부되는 파라미터

| 파라미터 | Opus 5.5 | Sonnet 5.5 | Haiku 5.5 | Fable 5.2 |
|---|---|---|---|---|
| `temperature` / `top_p` / `top_k` | 400 | 400 | 생략 권장 (400 여부 ⚠️ 문서 미기재) | 400 |
| `thinking.budget_tokens` | 400 | 400 | ⚠️ 문서 미확인 | 400 |
| assistant prefill | 400 | 400 | 400 | 400 |
| forced `tool_choice` (`any`, `tool`) | 400 | 400 | **허용** | 400 |

API version `2026-10-21` 에서는 샘플링 파라미터를 기본값으로 보내도 거부된다. `2023-06-01` 에서는 기본값이 아닌 값만 거부된다.

---

## Tokenizer (Opus 4.7 부터)

### 영향

- 같은 텍스트가 이전 모델보다 **최대 약 35% 더 많은 토큰**을 쓴다 (content type 에 따라 다름). Sonnet 5.5 는 Sonnet 4.6 대비 약 30%
- Opus 5.5 와 Sonnet 5.5 모두 이 tokenizer 를 쓴다
- `/v1/messages/count_tokens` 결과값 변화

### 대응 체크리스트

- [ ] `max_tokens` 에 여유를 둔다. 공식 문서의 표현은 "give additional headroom" 이고 agentic 코딩에는 128,000 을 제안한다 (상한 128K)
- [ ] Compaction 트리거 임계값 재조정
- [ ] 클라이언트 쪽 토큰 추정 로직 재검증
- [ ] 모델 전환 후 cache 재빌드 가정

---

## 비용 계산 예시

### 시나리오: 코드 리뷰 에이전트 (agentic loop)

```
가정:
- System prompt (정적): 5,000 토큰 (cache 후보)
- 리포 context (정적): 50,000 토큰 (cache 후보)
- 리뷰 질문 (동적): 평균 500 토큰
- 응답 (reasoning + text): 10,000 토큰
- 일 100회 호출
```

### Prompt Caching 적용 전

```
입력:  55,500 × $4/M    = $0.222/회
출력:  10,000 × $20/M   = $0.200/회
──────────────────────────
회당: $0.422
일:   $42.20 (100회)
월:   $1,266
```

### Prompt Caching 적용 후 (5분 TTL)

```
첫 요청 (cache write):
  입력 cache write: 55,000 × $5/M    = $0.275
  입력 basic:          500 × $4/M     = $0.002
  출력:             10,000 × $20/M    = $0.200
  = $0.477

이후 99회 (cache hit):
  입력 cache read:  55,000 × $0.20/M  = $0.011
  입력 basic:          500 × $4/M     = $0.002
  출력:             10,000 × $20/M    = $0.200
  = $0.213/회

일 총:  $0.477 + ($0.213 × 99) = $21.56 (49% 절감)
월:     $647 (연 $7,428 절감)
```

---

## 체크리스트

### 작업 전
- [ ] context 80% 미만 확인
- [ ] 무관 태스크면 `/clear` 실행
- [ ] 10+ 파일 탐색이면 subagent 지시 명시

### 프롬프트 작성
- [ ] 의도·제약·수락 기준·파일 경로 첫 턴에 완전 명세
- [ ] 일반화가 필요하면 명시 ("유사 케이스에도 적용")
- [ ] Positive framing 선호 ("Don't X" → "Do Y")

### API 호출
- [ ] `effort` 명시 (`medium` 에서 시작, 어렵거나 길면 `high`)
- [ ] `max_tokens` 여유 확보 (agentic 코딩 128,000)
- [ ] 거부되는 파라미터 확인 (`temperature`, `budget_tokens`, prefill, forced `tool_choice`)
- [ ] Prompt cache 구조 정적→동적 순서

### Task Budget (해당 시)
- [ ] 최소 20k 토큰
- [ ] Follow-up에서 `remaining` 변경 금지 (cache 보존)
- [ ] 오픈엔디드 작업엔 미사용

---

## 참조

- `rules/harness/token-budget.md` — 핵심 원칙 (auto-load)
- `/dx:token-efficiency` — Claude Code 세션 내 도구 사용 효율
- `/dx:clean-code` — 코드 가독성 원칙
- [공식: What's new in Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)
- [공식: Opus 5.5 migration guide](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide)
- [공식: Sonnet 5.5 migration guide](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)
- [공식: Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [공식: Task budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets)
- [공식: Effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort)
- [공식: Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [공식: Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)

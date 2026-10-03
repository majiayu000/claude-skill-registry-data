---
name: documentation-and-adrs
description: >
  Architecture Decision Records(ADR) 작성 + 기술 문서화 자동화.
  아키텍처 결정을 구조화된 ADR로 기록하고, API 문서·README·기술 가이드를 생성.
  "ADR 작성", "아키텍처 결정 기록", "기술 문서화", "ADR" 요청에 실행.
  /adr로 실행.
license: MIT
metadata:
  version: "1.0.0"
  benchmarked_from: "addyosmani/agent-skills"
---

# Documentation & ADRs — 아키텍처 결정 기록 + 기술 문서화

> 아키텍처 결정을 **왜** 했는지 기록하고, 나중에 돌아볼 수 있게 만든다.
> 코드는 "무엇"을 말하고, 커밋은 "언제"를 말하지만, ADR만이 **"왜"**를 말한다.

## Quick Start

```
/adr                          # 대화형 ADR 작성
/adr "Redis를 캐시로 선택"      # 제목 지정하여 ADR 작성
/adr list                     # 기존 ADR 목록 조회
/adr status                   # ADR 현황 (accepted/superseded/deprecated)
```

**공식 호출명:** `/adr` (별칭: `아키텍처 결정`, `decision record`, `기술 문서화`)

## 적용 시점

| 상황 | 적용 |
|------|------|
| 기술 스택 선택 (DB, 프레임워크, 라이브러리) | O |
| 아키텍처 패턴 결정 (모놀리스 vs 마이크로서비스) | O |
| 기존 결정 변경/폐기 | O |
| 팀 간 API 계약 변경 | O |
| 단순 버그 수정, UI 미세 조정 | X |
| 이미 ADR이 존재하는 결정 | X (업데이트만) |

---

## CRITICAL: First Actions

### 1. Print Intro

```
Documentation & ADRs — 아키텍처 결정 기록
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
순서: Detect → Interview → Write → Link → Verify
```

### 2. ADR 디렉토리 감지

```bash
# ADR 디렉토리 찾기
_ADR_DIR=""
for dir in docs/adr docs/decisions adr decisions doc/adr; do
  [ -d "$dir" ] && _ADR_DIR="$dir" && break
done

# 없으면 생성 제안
if [ -z "$_ADR_DIR" ]; then
  echo "ADR 디렉토리 없음 — docs/adr/ 생성 권장"
  _ADR_DIR="docs/adr"
fi

# 기존 ADR 번호 확인
_LAST_NUM=$(ls "$_ADR_DIR"/[0-9]*.md 2>/dev/null | sort -V | tail -1 | grep -oE '[0-9]+' | head -1)
_NEXT_NUM=$(printf "%04d" $(( ${_LAST_NUM:-0} + 1 )))
echo "ADR_DIR: $_ADR_DIR | NEXT: $_NEXT_NUM"
```

---

## Step 1: 결정 컨텍스트 수집

사용자에게 다음을 질문 (이미 제공된 항목은 스킵):

1. **결정 제목**: 한 줄로 요약 (예: "세션 스토어를 Redis로 전환")
2. **문제 상황**: 어떤 문제를 해결하려는가?
3. **고려한 대안**: 최소 2개 이상
4. **선택한 결정**: 무엇을 선택했는가?
5. **이유**: 왜 이 결정인가? (트레이드오프 포함)
6. **영향 범위**: 어떤 코드/팀/시스템에 영향을 주는가?

---

## Step 2: ADR 작성

### ADR 템플릿

```markdown
# {NEXT_NUM}. {결정 제목}

- **Date**: {YYYY-MM-DD}
- **Status**: proposed | accepted | deprecated | superseded by [ADR-XXXX](XXXX-xxx.md)
- **Deciders**: {의사결정자}
- **Tags**: {기술 키워드}

## Context

{문제 상황 — 어떤 상황에서 이 결정이 필요했는가}

## Decision Drivers

- {드라이버 1: 성능, 비용, 팀 역량 등}
- {드라이버 2}

## Considered Options

### Option 1: {대안 A}
- **Pros**: {장점}
- **Cons**: {단점}

### Option 2: {대안 B}
- **Pros**: {장점}
- **Cons**: {단점}

### Option 3: {대안 C} (선택된 경우에만)
- **Pros**: {장점}
- **Cons**: {단점}

## Decision

**{선택한 대안}**을 선택한다.

{왜 이 결정인지 2-3문장으로}

## Consequences

### Positive
- {긍정적 결과 1}
- {긍정적 결과 2}

### Negative
- {부정적 결과/트레이드오프 1}
- {부정적 결과/트레이드오프 2}

### Risks
- {리스크 1} → {완화 방안}

## Related

- {관련 ADR 링크}
- {관련 이슈/PR 링크}
- {참고 문서}
```

### 파일명 규칙

```
{NEXT_NUM}-{kebab-case-title}.md
예: 0005-use-redis-for-session-store.md
```

---

## Step 3: 기존 ADR 연결

1. 이전 결정을 대체하는 경우:
   - 기존 ADR의 Status를 `superseded by [ADR-{NEW}]({file})` 로 변경
   - 새 ADR에 `supersedes [ADR-{OLD}]({file})` 추가

2. 관련 ADR이 있는 경우:
   - Related 섹션에 상호 참조 링크 추가

3. **ADR 인덱스 업데이트** (`docs/adr/README.md` 또는 `docs/adr/index.md`):

```markdown
# Architecture Decision Records

| # | 결정 | 상태 | 날짜 |
|---|------|------|------|
| 0001 | [모놀리스 아키텍처 채택](0001-adopt-monolith.md) | accepted | 2026-01-15 |
| 0002 | [PostgreSQL 선택](0002-use-postgresql.md) | accepted | 2026-02-01 |
| 0003 | [Redis 세션 스토어](0003-use-redis-for-sessions.md) | accepted | 2026-03-10 |
```

---

## Step 4: MEMORY.md 연동 (이 프로젝트 전용)

ADR이 이 프로젝트(`claude-code-agent-customizations`)에서 작성된 경우:

1. `memory/architecture.md`에 요약 항목 추가
2. `MEMORY.md` 키워드 인덱스에 등록
3. Superseded 패턴 적용 (기존 항목 `❌ SUPERSEDED` 처리)

---

## Step 5: 검증

| # | 체크 항목 | 확인 방법 |
|---|----------|-----------|
| 1 | 결정의 "왜"가 명확한가? | Context + Decision 섹션 읽기 |
| 2 | 대안이 2개 이상 비교되었는가? | Considered Options 확인 |
| 3 | 트레이드오프가 명시되었는가? | Consequences 확인 |
| 4 | Status가 올바른가? | proposed/accepted/superseded |
| 5 | 파일명이 규칙을 따르는가? | `NNNN-kebab-case.md` |
| 6 | 인덱스에 등록되었는가? | index.md/README.md 확인 |
| 7 | 관련 ADR이 상호 링크되었는가? | Related 섹션 확인 |

---

## Red Flags — 나쁜 ADR 패턴

| 패턴 | 문제 | 개선 |
|------|------|------|
| "X를 사용하기로 했다" (이유 없음) | 왜를 알 수 없음 | Decision Drivers + Consequences 필수 |
| 대안 1개만 기록 | 비교 불가 | 최소 2개 대안 비교 |
| Status 없음 | 현재 유효한지 모름 | 항상 Status 명시 |
| 300줄 이상 | 읽지 않게 됨 | 핵심만, 상세는 링크로 |
| 코드 구현 세부사항 포함 | ADR의 범위 초과 | 아키텍처 수준만 기록 |

---

## 출력 형식

ADR 작성 완료 시:

```
ADR 작성 완료
━━━━━━━━━━━━━
  파일: docs/adr/0005-use-redis-for-session-store.md
  제목: Redis를 세션 스토어로 채택
  상태: accepted
  대안: 3개 비교 (Redis / Memcached / DB 직접)
  관련: ADR-0002 (PostgreSQL 선택)에 참조 추가

다음 단계:
  - git add docs/adr/ && git commit  → /commit-work
  - PR에 ADR 링크 포함 권장
```

---

## Related Files

| 파일 | 역할 |
|------|------|
| `docs/adr/*.md` | ADR 파일 저장 위치 |
| `docs/adr/index.md` | ADR 인덱스 |
| `memory/architecture.md` | 프로젝트 장기기억 (이 프로젝트) |
| `MEMORY.md` | 키워드 인덱스 (이 프로젝트) |

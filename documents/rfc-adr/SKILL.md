---
name: rfc-adr
description: "RFC·ADR 작성 워크플로우 — RFC vs ADR 비교, Google Design Doc·Uber 스타일 RFC 템플릿, 리뷰·관리 프로세스. Use when 설계 제안서(RFC)나 아키텍처 결정 기록(ADR)을 작성하고 리뷰받을 때 (사후 재평가는 adr-retrospective)."
---

# RFC/ADR 워크플로우

RFC(Request for Comments)와 ADR(Architecture Decision Record) 작성, 리뷰, 관리 프로세스 가이드

## Quick Reference (결정 트리)

```
어떤 문서가 필요한가?
    │
    ├─ 새로운 시스템/기능 설계 ────> RFC (Design Doc)
    │       │
    │       └─ 영향 범위 넓은 변경, 새 서비스, 대규모 리팩토링
    │
    ├─ 기술 선택/아키텍처 결정 ──> ADR
    │       │
    │       └─ 프레임워크 선택, DB 선택, 패턴 도입
    │
    ├─ 기존 결정 변경 ───────────> 새 ADR (기존 ADR supersede)
    │       │
    │       └─ Accepted ADR은 immutable — 절대 직접 수정하지 않음
    │
    └─ 팀 표준/컨벤션 ──────────> RFC → 승인 후 Rule로 전환
            │
            └─ 코딩 컨벤션, API 스타일, 브랜치 전략
```

---

## RFC vs ADR 비교

| 항목 | RFC (Design Doc) | ADR |
|------|-------------------|-----|
| **목적** | 설계 제안 및 합의 도출 | 결정 기록 및 근거 보존 |
| **길이** | 3~15페이지 | 1~2페이지 |
| **라이프사이클** | Draft → Review → Accepted/Rejected | Proposed → Accepted → Superseded |
| **소유자** | 설계 리더 (1~2명) | 결정 참여자 전원 |
| **리뷰 기간** | 2~5일 비동기 리뷰 | 미팅 중 또는 PR 리뷰 |
| **결과물** | 설계 문서 + ADR(들) | 단일 결정 기록 |
| **수정 가능** | Draft 상태에서 자유롭게 | Accepted 후 immutable |

---

## RFC 프로세스

### 전체 흐름

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  작성    │───>│ 비동기   │───>│ 결정     │───>│  ADR     │
│ (1-2일)  │    │ 리뷰     │    │ 미팅     │    │ 생성     │
│          │    │ (2-3일)  │    │ (30-60m) │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
    │                │                │               │
    ▼                ▼                ▼               ▼
 Draft 작성      코멘트 수집     최종 결정       Accepted ADR
 리뷰어 지정     질문/반론      합의 또는 투표   구현 시작
```

### 단계별 상세

**1. 작성 (1~2일)**
- 문제 정의와 목표를 명확히 기술
- 최소 2개 이상의 대안(Alternatives)을 포함
- Unresolved Questions 섹션으로 불확실한 부분 명시
- 리뷰어 3~5명 지정 (관련 도메인 전문가 + 시니어)

**2. 비동기 리뷰 (2~3일)**
- 리뷰어는 인라인 코멘트로 질문, 우려사항, 개선안 제시
- 작성자는 24시간 이내 응답
- 중요 이슈는 태그 분류: `[blocking]`, `[question]`, `[suggestion]`

**3. 결정 미팅 (30~60분)**
- Blocking 이슈가 모두 해결된 후 미팅 진행
- 합의 도출: 전원 동의 또는 RACI 기반 결정권자 판단
- 결정 결과를 RFC 문서에 기록

**4. ADR 생성**
- RFC에서 도출된 주요 결정을 ADR로 분리 기록
- 구현 시작 전 ADR이 Accepted 상태인지 확인

---

## RFC 템플릿 (Google Design Doc 스타일)

```markdown
# RFC-{번호}: {제목}

| 항목 | 내용 |
|------|------|
| 작성자 | @author |
| 상태 | Draft / In Review / Accepted / Rejected |
| 리뷰어 | @reviewer1, @reviewer2, @reviewer3 |
| 생성일 | YYYY-MM-DD |
| 결정일 | YYYY-MM-DD |

## Context and Scope

현재 상황과 이 RFC의 범위를 기술한다.
- 어떤 문제를 해결하려 하는가?
- 왜 지금 해결해야 하는가?
- 이 RFC의 범위(in-scope)와 범위 밖(out-of-scope)은?

## Goals and Non-Goals

### Goals
- [ ] 달성하려는 구체적 목표

### Non-Goals
- [ ] 이 RFC에서 다루지 않는 것

## Current State

현재 시스템/프로세스가 어떻게 동작하는지 기술한다.
해당되는 경우 아키텍처 다이어그램 포함.

## Proposed Design

### Overview
제안하는 설계의 개요.

### Detailed Design
구체적인 구현 설계:
- API 인터페이스
- 데이터 모델
- 시퀀스 다이어그램
- 에러 처리

### Data Migration (해당 시)
데이터 마이그레이션 전략.

## Alternatives Considered

### Alternative 1: {이름}
- 설명
- 장점
- 단점
- **미채택 이유**: ...

### Alternative 2: {이름}
- 설명
- 장점
- 단점
- **미채택 이유**: ...

## Cross-cutting Concerns

- **보안**: 인증/인가, 데이터 보호
- **성능**: 예상 부하, 병목 지점
- **모니터링**: 메트릭, 알림
- **비용**: 인프라 비용 변화

## Unresolved Questions

1. 아직 결정되지 않은 사항
2. 추가 조사가 필요한 부분

## Implementation Plan

| 단계 | 내용 | 소요 기간 | 담당 |
|------|------|----------|------|
| Phase 1 | ... | 1주 | ... |
| Phase 2 | ... | 2주 | ... |

## References

- 관련 RFC, ADR, 외부 문서 링크
```

---

## RFC 템플릿 (Uber 스타일)

```markdown
# RFC: {제목}

## Summary
한 문단으로 제안을 요약한다.

## Motivation
왜 이 변경이 필요한가? 현재 어떤 문제가 있는가?

## Detailed Design
제안하는 설계를 구체적으로 기술한다.
코드 예시, API 스펙, 다이어그램 포함.

## Drawbacks
이 제안의 단점이나 리스크는 무엇인가?

## Alternatives
어떤 대안을 고려했는가? 왜 채택하지 않았는가?

## Unresolved Questions
RFC 프로세스에서 해결해야 할 질문은?
구현 중에 해결할 질문은?
```

---

## ADR 형식

### MADR (Markdown Architectural Decision Records)

```markdown
# ADR-{번호}: {결정 제목}

| 항목 | 내용 |
|------|------|
| 상태 | Proposed | Accepted | Deprecated | Superseded by ADR-{n} |
| 날짜 | YYYY-MM-DD |
| 의사결정자 | @person1, @person2 |
| 관련 RFC | RFC-{n} (있는 경우) |

## Context

이 결정이 필요한 배경과 맥락.
현재 어떤 상황이며, 어떤 제약 조건이 있는가.

## Decision Drivers

- 결정에 영향을 미치는 핵심 요인
- 우선순위가 높은 품질 속성
- 비즈니스 제약 조건

## Considered Options

### Option 1: {이름}
- 설명
- 장점: ...
- 단점: ...

### Option 2: {이름}
- 설명
- 장점: ...
- 단점: ...

### Option 3: {이름}
- 설명
- 장점: ...
- 단점: ...

## Decision

**Option {N}: {이름}을 선택한다.**

### 이유
- Decision Driver 1에 가장 부합
- 장점 A, B가 단점 C보다 중요

## Consequences

### 긍정적
- ...

### 부정적 (수용 가능)
- ...

### 리스크
- ...

## Related ADRs

- ADR-{n}: 관련 결정
```

### Y-Statement 형식

복잡한 MADR 없이 간결하게 기록할 때 사용:

```
In the context of [상황/문제],
facing [제약 조건/결정 요인],
we decided [결정 내용],
to achieve [달성 목표],
accepting [트레이드오프/수용한 단점].
```

**예시:**

```
In the context of 실시간 알림 시스템 구축,
facing 수백만 동시 연결과 메시지 순서 보장 요구,
we decided Kafka를 메시지 브로커로 사용하기로 결정했다,
to achieve 높은 처리량과 파티션 기반 순서 보장,
accepting 운영 복잡도 증가와 Kafka 전문 인력 필요를 수용한다.
```

---

## ADR 라이프사이클

```
┌──────────┐    ┌──────────┐    ┌──────────────┐
│ Proposed │───>│ Accepted │───>│ Superseded   │
│          │    │          │    │ by ADR-{new} │
└──────────┘    └──────────┘    └──────────────┘
      │                               ▲
      │                               │
      ▼                        ┌──────┴──────┐
┌──────────┐                   │ 새 ADR 작성  │
│ Rejected │                   │ (기존 참조)   │
└──────────┘                   └─────────────┘
```

### 상태 전이 규칙

| 현재 상태 | 가능한 전이 | 조건 |
|-----------|------------|------|
| Proposed | Accepted | 리뷰 완료, 합의 도출 |
| Proposed | Rejected | 대안이 더 적합하거나 불필요 |
| Accepted | Superseded | 새로운 결정이 기존 결정을 대체 |
| Rejected | - | 최종 상태 (변경 불가) |
| Superseded | - | 최종 상태 (변경 불가) |

**핵심 원칙: Accepted ADR은 immutable**
- 내용을 직접 수정하지 않는다
- 결정을 변경하려면 새 ADR을 작성하고 기존 ADR을 Superseded 처리

---

## 파일 구조 및 번호 관리

```
docs/
├── rfcs/
│   ├── RFC-001-event-driven-architecture.md
│   ├── RFC-002-api-gateway-migration.md
│   └── RFC-003-observability-platform.md
├── adrs/
│   ├── ADR-001-use-postgresql-for-primary-db.md
│   ├── ADR-002-adopt-hexagonal-architecture.md
│   ├── ADR-003-use-kafka-for-messaging.md
│   └── ADR-004-replace-kafka-with-nats.md  # Supersedes ADR-003
└── templates/
    ├── rfc-template.md
    └── adr-template.md
```

### 번호 규칙
- 순차 증가 (001, 002, 003...)
- 삭제된 번호는 재사용하지 않음
- Superseded ADR의 번호도 보존

---

## 리뷰 체크리스트

### RFC 리뷰 체크리스트

```markdown
## 구조 완성도
- [ ] Context/Scope가 명확한가
- [ ] Goals와 Non-Goals가 구분되어 있는가
- [ ] 최소 2개 이상의 Alternatives가 있는가
- [ ] 각 Alternative의 장단점이 기술되어 있는가

## 기술적 타당성
- [ ] 설계가 현재 아키텍처와 일관되는가
- [ ] 성능/확장성 고려가 포함되어 있는가
- [ ] 보안 관점이 검토되었는가
- [ ] 에러 처리/장애 시나리오가 다루어졌는가

## 실행 가능성
- [ ] 구현 계획과 일정이 현실적인가
- [ ] 마이그레이션 전략이 있는가 (해당 시)
- [ ] 롤백 계획이 있는가
- [ ] 모니터링/알림 계획이 있는가

## 리뷰 품질
- [ ] Blocking 이슈가 모두 해결되었는가
- [ ] 핵심 이해관계자가 리뷰에 참여했는가
```

### ADR 리뷰 체크리스트

```markdown
- [ ] Context가 충분히 설명되어 있는가
- [ ] Considered Options가 3개 이상인가
- [ ] 선택 이유가 Decision Drivers와 연결되는가
- [ ] Consequences (긍정/부정)가 솔직하게 기술되어 있는가
- [ ] 관련 ADR 참조가 있는가
```

---

## 도구 연동

### adr-tools (CLI)

```bash
# 설치
brew install adr-tools

# ADR 저장소 초기화
adr init docs/adrs

# 새 ADR 생성
adr new "Use PostgreSQL for primary database"
# → docs/adrs/0001-use-postgresql-for-primary-database.md

# 기존 ADR supersede
adr new -s 3 "Replace Kafka with NATS for messaging"
# → ADR-003 상태가 자동으로 "Superseded by ADR-004"로 변경

# 목록 조회
adr list

# 관계 그래프 생성
adr generate graph | dot -Tpng -o adr-graph.png
```

### log4brains (웹 UI)

```bash
# 설치
npm install -g log4brains

# 초기화
log4brains init

# 로컬 미리보기
log4brains preview

# 정적 사이트 빌드
log4brains build
```

### Backstage ADR Plugin

```typescript
// app-config.yaml
catalog:
  locations:
    - type: file
      target: ./docs/adrs/*.md
      rules:
        - allow: [ADR]

// EntityPage.tsx에 ADR 탭 추가
import { EntityAdrContent } from '@backstage/plugin-adr';

<EntityLayout.Route path="/adrs" title="ADRs">
  <EntityAdrContent />
</EntityLayout.Route>
```

---

## RFC/ADR 거버넌스

### 언제 RFC가 필요한가

| 변경 유형 | RFC 필요 | 이유 |
|-----------|---------|------|
| 새 서비스 추가 | 필수 | 아키텍처 영향 |
| DB 스키마 대규모 변경 | 필수 | 마이그레이션 리스크 |
| 외부 API 계약 변경 | 필수 | 다운스트림 영향 |
| 프레임워크/언어 변경 | 필수 | 팀 역량, 유지보수 영향 |
| 기존 API에 필드 추가 | 불필요 | 하위 호환, 영향 작음 |
| 버그 수정 | 불필요 | 설계 변경 아님 |
| 라이브러리 마이너 업데이트 | 불필요 | 영향 작음 |

### RFC 결정 방식

```
소규모 팀 (< 10명)
  └─ 합의(Consensus): 전원 동의 시 승인

중규모 팀 (10~30명)
  └─ RACI 기반: Responsible 2명 + Accountable 1명 결정

대규모 조직 (30명+)
  └─ Architecture Review Board + 도메인 오너 승인
```

---

## Anti-Patterns

| 안티패턴 | 문제 | 해결 |
|----------|------|------|
| ADR 없이 구현 시작 | 결정 근거 유실, 나중에 "왜 이렇게 했지?" | 코드 전에 ADR 먼저 |
| Accepted ADR 직접 수정 | 결정 이력 파괴 | 새 ADR로 supersede |
| RFC가 구현 매뉴얼화 | 리뷰 불가능한 분량, 설계가 아닌 코드 설명 | 설계 결정에 집중, 코드는 별도 |
| RFC 리뷰 무기한 지연 | 의사결정 병목 | 리뷰 기한 3일 + 에스컬레이션 |
| 모든 변경에 RFC 요구 | 오버헤드, 속도 저하 | 임팩트 기반 RFC 필요 여부 판단 |
| ADR에 결정만, 근거 없음 | "왜"를 알 수 없음 | Considered Options + 이유 필수 |
| Rejected ADR 삭제 | "왜 안 했는지" 유실 | Rejected도 보존 |

---

## Sources

- Michael Nygard, "Documenting Architecture Decisions" (2011)
- MADR: https://adr.github.io/madr/
- Google Design Docs: "Design Docs at Google" (Industrial Empathy)
- Uber RFC Process: "Uber's RFC Process" (Engineering Blog)
- adr-tools: https://github.com/npryce/adr-tools
- log4brains: https://github.com/thomvaill/log4brains

**관련 skill**: `/dx:engineering-strategy`, `/dx:docs-as-code`, `/dx:dx-onboarding`

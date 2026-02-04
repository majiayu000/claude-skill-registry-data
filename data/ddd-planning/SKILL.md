---
name: ddd-planning
description: "Domain-Driven Design 기획 및 설계 전문 skill. 프로젝트 도메인 분석, Bounded Context 정의, Aggregate 설계, Context Mapping, Event Storming, Ubiquitous Language 정의 등 DDD 전체 프로세스를 지원합니다. 사용 시기: (1) DDD 기획/설계를 요청할 때 (2) 도메인 모델링을 요청할 때 (3) Bounded Context, Aggregate, Domain Event 설계 시 (4) 화면정의서/DB정의서에서 도메인 추출 시 (5) Context Map 작성 시 (6) Kotlin DDD 코드 생성 시"
---

# DDD Planning

## Overview

이 skill은 Domain-Driven Design(DDD) 방법론으로 프로젝트를 기획하고 설계합니다. 기존 문서(화면정의서, DB정의서, 기획서)를 분석하여 도메인을 추출하고, DDD 산출물을 생성합니다.

## Workflow

### Phase 1: 도메인 분석

기존 문서를 분석하여 도메인을 추출합니다.

1. **문서 읽기**: 화면정의서, DB정의서, 기획서 읽기
2. **도메인 식별**: 비즈니스 기능별 도메인 추출
3. **용어 수집**: 도메인 용어 수집 (Ubiquitous Language 초안)

### Phase 2: Strategic Design

전략적 설계를 수행합니다. 자세한 가이드는 `references/strategic-design.md` 참고.

1. **도메인 분류**: Core / Supporting / Generic 분류
2. **Bounded Context 정의**: Context 경계와 책임 정의
3. **Context Mapping**: Context 간 관계와 통합 패턴 정의
4. **Ubiquitous Language**: Context별 용어집 작성

**산출물**:
- `assets/templates/bounded-context.md` 사용
- `assets/templates/context-map.md` 사용
- `assets/templates/ubiquitous-language-glossary.md` 사용

### Phase 3: Tactical Design

전술적 설계를 수행합니다. 자세한 가이드는 `references/tactical-design.md` 참고.

1. **Aggregate 식별**: 트랜잭션 경계와 불변식 정의
2. **Entity/Value Object 분류**: 식별자 필요성과 가변성 기준
3. **Domain Event 정의**: 중요 비즈니스 사건 정의
4. **Repository 인터페이스**: Aggregate별 Repository 정의

**산출물**:
- `assets/templates/aggregate-design.md` 사용
- `assets/templates/domain-model.md` 사용

### Phase 4: Event Storming (선택)

Event Storming 워크숍을 수행합니다. 가이드는 `references/event-storming.md` 참고.

**산출물**:
- `assets/templates/event-storming-result.md` 사용

### Phase 5: 코드 생성

Kotlin DDD 보일러플레이트를 생성합니다.

**템플릿 위치**: `assets/kotlin-ddd/`
- `Aggregate.kt`: Aggregate Root 패턴
- `Entity.kt`: Entity 패턴
- `ValueObject.kt`: Value Object 패턴
- `DomainEvent.kt`: Domain Event 패턴
- `Repository.kt`: Repository 인터페이스 패턴
- `DomainService.kt`: Domain Service 패턴

### Phase 6: 문서 반영

설계 결과를 기존 프로젝트 문서에 반영합니다.

1. 기획서에 도메인 모델 섹션 추가
2. DB정의서와 도메인 모델 정합성 확인
3. 화면정의서와 Bounded Context 매핑

## Quick Reference

### 도메인 분류 기준

| 분류 | 특징 | 전략 |
|------|------|------|
| **Core** | 비즈니스 차별화 요소, 복잡한 로직 | 직접 개발, 최우선 투자 |
| **Supporting** | Core 지원, 중간 복잡도 | 직접 개발 또는 커스터마이징 |
| **Generic** | 범용 기능, 비즈니스 특화 없음 | 외부 서비스/라이브러리 |

### Context Mapping 패턴

| 패턴 | 설명 | 사용 시기 |
|------|------|----------|
| **OHS** | Open Host Service | 여러 Consumer 대응 |
| **PL** | Published Language | OHS와 함께, 공통 언어 |
| **ACL** | Anti-Corruption Layer | 레거시/외부 연동 |
| **CS** | Customer-Supplier | Upstream이 협조적 |
| **CF** | Conformist | Upstream이 비협조적 |

### Aggregate 설계 원칙

1. **작게 유지**: 대부분 1개 Entity
2. **ID 참조**: Aggregate 간 객체 참조 금지
3. **트랜잭션 경계**: 1 트랜잭션 = 1 Aggregate
4. **불변식 보호**: 비즈니스 규칙은 Aggregate 내부에서

## Resources

### references/

DDD 개념과 패턴에 대한 가이드 문서입니다.

- `strategic-design.md`: Bounded Context, 도메인 분류, Context Mapping
- `tactical-design.md`: Aggregate, Entity, Value Object, Domain Event
- `context-mapping-patterns.md`: Context Mapping 패턴 상세
- `event-storming.md`: Event Storming 프로세스
- `ubiquitous-language.md`: 용어집 작성 가이드

### assets/templates/

DDD 문서 템플릿입니다. `{{PLACEHOLDER}}`를 실제 값으로 교체하여 사용합니다.

- `bounded-context.md`: Bounded Context 정의서
- `aggregate-design.md`: Aggregate 설계서
- `context-map.md`: Context Map 문서
- `event-storming-result.md`: Event Storming 결과
- `ubiquitous-language-glossary.md`: 용어집
- `domain-model.md`: 전체 도메인 모델 문서

### assets/kotlin-ddd/

Kotlin DDD 코드 보일러플레이트입니다.

- `Aggregate.kt`: Aggregate Root 패턴 (팩토리 메서드, 이벤트 발행)
- `Entity.kt`: Entity 패턴 (ID 기반 동등성)
- `ValueObject.kt`: Value Object 패턴 (불변성, 자가 검증)
- `DomainEvent.kt`: Domain Event 패턴 (이벤트 핸들러 포함)
- `Repository.kt`: Repository 인터페이스 (페이지네이션 포함)
- `DomainService.kt`: Domain Service 패턴 (정책, 계산 서비스)

## Usage Examples

### 도메인 분석 요청

```
"화면정의서와 DB정의서를 분석해서 도메인을 추출해줘"
"FanPulse 프로젝트의 Bounded Context를 정의해줘"
```

### Strategic Design 요청

```
"투표 도메인과 커뮤니티 도메인의 Context Map을 그려줘"
"Core/Supporting/Generic 도메인을 분류해줘"
```

### Tactical Design 요청

```
"투표 Aggregate를 설계해줘"
"멤버십 도메인의 Entity와 Value Object를 정의해줘"
"Domain Event 목록을 만들어줘"
```

### 코드 생성 요청

```
"Vote Aggregate의 Kotlin 코드를 생성해줘"
"VoteRepository 인터페이스를 만들어줘"
```

### 문서 생성 요청

```
"투표 Context의 Bounded Context 정의서를 작성해줘"
"Ubiquitous Language 용어집을 만들어줘"
"전체 도메인 모델 문서를 생성해줘"
```

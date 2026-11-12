---
name: team-topologies
description: "Team Topologies — 4가지 팀 유형, 3가지 인터랙션 모드, Conway's Law, 인지 부하, Team API, 팀 구조 진화. Use when 조직·팀 경계를 설계하거나 플랫폼 팀과 스트림 얼라인드 팀의 협업 방식을 정할 때."
---

# Team Topologies 가이드

Team Topologies, Conway's Law, 팀 구조 설계, 인터랙션 모드

## Quick Reference (결정 트리)

```
팀 유형 결정?
    │
    ├─ 비즈니스 가치 직접 전달 ──> Stream-Aligned Team
    │       │
    │       └─ 고객 가치 흐름에 정렬, 독립 배포 가능
    │
    ├─ 내부 서비스/플랫폼 제공 ──> Platform Team
    │       │
    │       └─ 셀프서비스 API, 내부 개발자가 고객
    │
    ├─ 전문 기술 지원/코칭 ──────> Enabling Team
    │       │
    │       └─ 일시적 지원, 역량 이전 후 철수
    │
    ├─ 복잡한 서브시스템 ────────> Complicated-Subsystem Team
    │       │
    │       └─ 전문 지식 필요 (ML 엔진, 결제, 비디오 코덱)
    │
    └─ 모든 팀이 Platform 의존 ──> 안티패턴 경고!
```

---

## 4가지 팀 유형

### 개요

```
┌─────────────────────────────────────────────────────────────────┐
│                      Team Topologies                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Stream-Aligned Team          Platform Team                      │
│  ────────────────────         ─────────────                      │
│  비즈니스 가치 흐름 담당       내부 셀프서비스 플랫폼             │
│  전체 조직의 80%+ 비율        API로 역량 제공                    │
│  End-to-end 책임              내부 개발자 = 고객                 │
│                                                                  │
│  Enabling Team                Complicated-Subsystem Team         │
│  ─────────────                ──────────────────────────         │
│  역량 갭 해소, 코칭           전문 도메인 캡슐화                 │
│  일시적 지원 후 철수          높은 인지 부하 격리                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Stream-Aligned Team

| 항목 | 설명 |
|------|------|
| **목적** | 비즈니스 가치 흐름(stream)의 end-to-end 전달 |
| **크기** | 5~9명 (Two-pizza team) |
| **구성** | 풀스택 — 프론트, 백엔드, QA, 가능하면 Ops |
| **정렬 기준** | 비즈니스 도메인, 사용자 여정, 제품 기능 |
| **독립성** | 독립 빌드, 테스트, 배포 가능 |
| **비율** | 전체 팀의 80% 이상 |

```
Stream 예시:
  - 결제 팀: 결제 수단 추가 → 결제 처리 → 정산
  - 검색 팀: 인덱싱 → 쿼리 → 결과 렌더링
  - 온보딩 팀: 가입 → 인증 → 첫 경험 설계
```

### Platform Team

| 항목 | 설명 |
|------|------|
| **목적** | Stream-Aligned Team의 인지 부하 경감 |
| **제공물** | 셀프서비스 API, 도구, 문서 |
| **크기** | 3~8명 (작게 시작) |
| **고객** | 내부 개발자 (Stream-Aligned Teams) |
| **핵심 원칙** | "사용하기 쉬운 API" — 강제가 아닌 매력 |

```
Platform 계층 예시:
  ┌─────────────────────────────────────────┐
  │  Stream-Aligned Teams (사용자)          │
  ├─────────────────────────────────────────┤
  │  Internal Developer Platform            │
  │  ├─ CI/CD 파이프라인 (Golden Path)     │
  │  ├─ 관측성 (로깅, 메트릭, 트레이싱)    │
  │  ├─ 인프라 프로비저닝 (셀프서비스)      │
  │  └─ 서비스 템플릿 (Backstage)          │
  ├─────────────────────────────────────────┤
  │  Cloud Infrastructure (AWS/GCP/Azure)   │
  └─────────────────────────────────────────┘
```

### Enabling Team

| 항목 | 설명 |
|------|------|
| **목적** | Stream-Aligned Team의 역량 갭 해소 |
| **방식** | 코칭, 페어링, 워크숍 — 대신 해주지 않음 |
| **기간** | 일시적 (주~월 단위), 역량 이전 후 철수 |
| **크기** | 2~5명 (전문가 소수 정예) |
| **예시** | SRE 코칭, 테스트 자동화 코칭, 보안 교육 |

```
Enabling 패턴:
  1. 갭 발견: Stream 팀이 관측성 도구 사용에 어려움
  2. 지원 시작: Enabling 팀이 2주간 페어링/코칭
  3. 역량 이전: Stream 팀이 독립적으로 운영 가능
  4. 철수: Enabling 팀은 다음 팀으로 이동
```

### Complicated-Subsystem Team

| 항목 | 설명 |
|------|------|
| **목적** | 높은 전문성이 필요한 서브시스템 캡슐화 |
| **필요 조건** | Stream 팀이 감당하기 어려운 인지 부하 |
| **크기** | 3~7명 (도메인 전문가) |
| **제공물** | API 또는 라이브러리로 복잡도 은닉 |
| **예시** | ML 엔진, 비디오 인코딩, 결제 PG 연동, 지도 엔진 |

```
Complicated-Subsystem 판단 기준:
  - 해당 도메인의 전문 지식이 특수한가? → Yes
  - Stream 팀이 학습하면 주력 업무에 방해가 되는가? → Yes
  - API로 캡슐화하여 복잡도를 숨길 수 있는가? → Yes
  → Complicated-Subsystem Team 생성 적합
```

---

## 3가지 인터랙션 모드

| 모드 | 특성 | 기간 | 예시 |
|------|------|------|------|
| **Collaboration** | 두 팀이 긴밀히 협업 | 일시적 (주~월) | 새 기능 공동 개발, PoC |
| **X-as-a-Service** | 명확한 API 계약으로 소비 | 지속적 | Platform API 사용, 라이브러리 |
| **Facilitating** | 코칭, 멘토링, 가이드 | 일시적 (주~월) | Enabling 팀의 지원 |

### 인터랙션 모드 결정

```
두 팀 간 인터랙션?
    │
    ├─ 새로운 영역, 불확실성 높음 ──> Collaboration (탐색)
    │       │
    │       └─ 기간 제한 설정 (보통 2~8주)
    │       └─ 이후 X-as-a-Service로 전환
    │
    ├─ 명확한 인터페이스 존재 ──────> X-as-a-Service (안정)
    │       │
    │       └─ API 문서, SLA 정의
    │       └─ 의존 팀은 독립적으로 사용
    │
    └─ 역량 차이, 학습 필요 ────────> Facilitating (성장)
            │
            └─ 코칭/페어링 후 독립 운영
            └─ 가르치기, 대신 하지 않기
```

### 인터랙션 진화

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│Collaboration│────────>│  X-as-a-Service  │<────────│ Facilitating│
│  (탐색기)    │         │   (안정기)        │         │  (성장기)    │
└─────────────┘         └──────────────────┘         └─────────────┘
      │                                                      │
      │              일반적 진화 방향                          │
      └──────────────────────────────────────────────────────┘
```

---

## Conway's Law

### 원문

> "Organizations which design systems are constrained to produce designs
> which are copies of the communication structures of these organizations."
> — Melvin Conway (1968)

### 시스템 구조는 조직 구조를 따른다

```
조직 구조:                      시스템 아키텍처:
┌────────┐                     ┌────────┐
│ 팀 A   │──────────┐         │서비스 A │──────────┐
└────────┘          │         └────────┘          │
                    ▼                              ▼
              ┌──────────┐                  ┌──────────┐
              │ 공유 DB팀 │                  │ 공유 DB  │
              └──────────┘                  └──────────┘
                    ▲                              ▲
┌────────┐          │         ┌────────┐          │
│ 팀 B   │──────────┘         │서비스 B │──────────┘
└────────┘                     └────────┘

두 팀이 DB팀을 공유하면, 시스템도 DB를 공유하게 된다
```

### Inverse Conway Maneuver

**원하는 아키텍처에 맞게 팀 구조를 설계한다**

```
목표 아키텍처:                   팀 구조 설계:
┌────────┐                     ┌────────┐
│서비스 A │  독립 배포          │ 팀 A   │  독립 팀
│ + DB A │                     │ 풀스택  │
└────────┘                     └────────┘

┌────────┐                     ┌────────┐
│서비스 B │  독립 배포          │ 팀 B   │  독립 팀
│ + DB B │                     │ 풀스택  │
└────────┘                     └────────┘

서비스별 독립 DB → 팀별 독립 운영
```

**적용 원칙:**
1. 원하는 아키텍처를 먼저 정의한다
2. 아키텍처 경계에 맞춰 팀 경계를 설정한다
3. 팀 간 통신 채널이 시스템 간 인터페이스가 된다
4. 불필요한 팀 간 의존성을 제거한다

---

## 인지 부하 (Cognitive Load)

### 3가지 유형

| 유형 | 정의 | 관리 전략 |
|------|------|----------|
| **Intrinsic** | 기술 자체의 본질적 복잡도 | 교육, 문서화, 페어링 |
| **Extraneous** | 불필요한 환경적 복잡도 | 도구 개선, 플랫폼 제공, 자동화 |
| **Germane** | 도메인 비즈니스 로직 복잡도 | 팀 범위 적정화, DDD 적용 |

### 팀 범위 결정

```
팀 인지 부하 = Intrinsic + Extraneous + Germane

목표: Extraneous를 최소화하여 Germane에 집중

팀이 감당할 수 있는 범위:
  ┌─────────────────────────────────────┐
  │  2~3개 마이크로서비스               │ ← 적정
  │  또는 1개 복잡한 도메인 서비스       │
  └─────────────────────────────────────┘

  ┌─────────────────────────────────────┐
  │  5개+ 마이크로서비스                │ ← 과부하
  │  + 인프라 운영 + 다른 팀 지원       │
  └─────────────────────────────────────┘
```

### 인지 부하 측정

```yaml
# cognitive-load-assessment.yaml
team: payment-team
assessment_date: 2025-Q1

domains_owned:
  - name: 결제 처리
    complexity: high
  - name: 정산
    complexity: medium
  - name: PG 연동
    complexity: high

infrastructure_responsibilities:
  - "결제 DB 운영"        # → Platform으로 이관 대상
  - "모니터링 대시보드"    # → Platform으로 이관 대상

external_dependencies:
  - team: billing-team
    interaction: collaboration  # → X-as-a-Service로 전환 대상
  - team: platform-team
    interaction: x-as-a-service  # OK

cognitive_load_score: 8/10  # 7+ = 과부하 → 범위 축소 필요
recommendation: "인프라 책임을 Platform에 이관, 정산 도메인 분리 검토"
```

---

## Team API

### 팀이 제공/소비하는 것을 명시화

```markdown
# Team API: Payment Team

## 우리가 제공하는 것 (Provides)
- Payment Processing API (REST, gRPC)
  - SLA: 99.95% 가용성, P99 < 200ms
  - 문서: https://docs.internal/payment-api
- 결제 이벤트 (Kafka: payment.events.*)
- 결제 대시보드 (Grafana)

## 우리가 소비하는 것 (Consumes)
- User Service API (from: user-team)
- Infrastructure Platform (from: platform-team)
  - Kubernetes, CI/CD, Observability
- PG Gateway (external: Stripe, Toss)

## 소통 방식
- Slack: #team-payment
- 온콜: PagerDuty rotation
- 코드 리뷰: GitHub @payment-team
- 정기 회의: 화/목 10:00 스탠드업

## 업무 요청 방식
- 버그 리포트: Jira PAYMENT-* 프로젝트
- 기능 요청: RFC 작성 후 #team-payment 공유
- 긴급 이슈: PagerDuty 에스컬레이션
```

---

## 팀 구조 진화 패턴

### 스타트업 → 스케일업 (50명 → 200명)

```
Phase 1 (< 20명): 기능 팀 2~3개
  ┌────────┐  ┌────────┐  ┌────────┐
  │ 프론트 │  │ 백엔드 │  │ 인프라 │
  └────────┘  └────────┘  └────────┘

Phase 2 (20~50명): Stream-Aligned 전환 시작
  ┌────────────┐  ┌────────────┐  ┌──────────┐
  │ 결제 팀    │  │ 검색 팀    │  │ Platform │
  │ (풀스택)   │  │ (풀스택)   │  │          │
  └────────────┘  └────────────┘  └──────────┘

Phase 3 (50~200명): Team Topologies 본격 적용
  Stream-Aligned: 결제, 검색, 주문, 회원, 상품 (80%)
  Platform: IDP, 관측성, CI/CD (15%)
  Enabling: SRE, Security (일시적 지원)
  Complicated-Subsystem: ML 추천, 검색 엔진 (5%)
```

### Evolutionary Architecture: Fitness Functions

```
팀 구조 건강도를 코드로 검증:

# 팀 간 의존성 테스트
def test_team_dependencies():
    """Stream 팀은 최대 2개의 다른 Stream 팀에만 의존"""
    for team in stream_aligned_teams:
        deps = count_stream_team_dependencies(team)
        assert deps <= 2, f"{team.name} has {deps} dependencies"

# 인지 부하 테스트
def test_cognitive_load():
    """각 팀의 서비스 수가 임계값 이내"""
    for team in all_teams:
        services = count_owned_services(team)
        assert services <= 4, f"{team.name} owns {services} services"

# Platform 의존 비율
def test_platform_dependency():
    """Platform 팀 변경 없이 배포 가능한 팀이 80%+"""
    independent = count_independently_deployable_teams()
    total = count_all_stream_teams()
    assert independent / total >= 0.8
```

---

## Anti-Patterns

| 안티패턴 | 문제 | 해결 |
|----------|------|------|
| 모든 팀이 Platform에 의존 | 병목, Platform 팀 과부하 | 셀프서비스 API, 독립 배포 |
| Enabling 팀 영구화 | 역량 이전 안됨, 의존성 발생 | 기한 설정, 코칭 후 철수 |
| Team API 미정의 | 암묵적 의존, 소통 비용 증가 | Team API 문서화 |
| Conway 무시한 아키텍처 | 조직과 시스템 불일치 | Inverse Conway Maneuver |
| 너무 작은 팀 (2~3명) | 버스 팩터, 온콜 불가 | 최소 4~5명 |
| 너무 큰 팀 (10명+) | 소통 비용 급증 | 분할 (Dunbar's Number) |
| 기능 팀 (프론트/백/DBA) | 핸드오프, 대기 시간 | Stream-Aligned 전환 |
| Complicated-Subsystem 남용 | 팀 간 경계 과다, 소통 비용 | 진짜 전문성 필요할 때만 |

---

## 체크리스트

### 팀 구조 설계

- [ ] Stream-Aligned 팀이 전체의 80% 이상인가
- [ ] 각 팀이 독립적으로 배포할 수 있는가
- [ ] 팀 크기가 5~9명 범위인가
- [ ] Team API가 문서화되어 있는가
- [ ] 인지 부하 평가가 정기적으로 수행되는가

### 인터랙션 모드

- [ ] Collaboration 모드에 기한이 설정되어 있는가
- [ ] X-as-a-Service의 API와 SLA가 명확한가
- [ ] Enabling 팀이 코칭 후 철수하는 패턴을 따르는가

### Conway's Law

- [ ] 아키텍처 목표와 팀 구조가 일치하는가
- [ ] 불필요한 팀 간 의존성이 제거되었는가
- [ ] Fitness Function으로 건강도를 측정하는가

---

## Sources

- Matthew Skelton & Manuel Pais, "Team Topologies" (2019)
- Melvin Conway, "How Do Committees Invent?" (1968)
- Team Topologies: https://teamtopologies.com/
- Skelton & Pais, "Remote Team Interactions Workbook" (2022)
- Nicole Forsgren et al., "Accelerate" (2018) — Conway's Law 연구
- Martin Fowler, "Conway's Law": https://martinfowler.com/bliki/ConwaysLaw.html

**관련 skill**: `/dx:engineering-strategy`, `/dx:rfc-adr`, `/platform:platform-backstage`, `/dx:dx-metrics`

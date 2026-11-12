---
name: audit-log
description: "감사 로그 — append-only 이벤트 모델, action 네이밍, tenant 격리, 저장소 선택, 보존·삭제, 검색·export UI. Use when 누가 언제 무엇을 바꿨는지 추적하는 기능을 SaaS 에 넣거나 규제 대응 로그를 설계할 때."
---

# Audit Log

Audit Log — 누가 언제 무엇을 어떻게 변경했는가. Append-only 이벤트 로그, tenant-scoped 격리, 규제 대응(GDPR/SOC2/HIPAA), 검색·필터·export. SaaS 부트스트랩 필수.

비즈니스 이벤트 추적은 **로그가 아니라 데이터**. 시스템 로그(Loki/CloudWatch)와 분리해서 관리. 운영자/사용자/규제기관이 조회하는 1급 시민.

## When to Use

- B2B SaaS 모든 변경 이력 추적 ("우리 admin이 X를 언제 바꿨는가")
- 규제 산업 (의료/금융/공공): SOC2, HIPAA, PCI-DSS, GDPR Article 30
- Multi-tenant 시스템: tenant 관리자가 자기 조직 활동 조회
- 보안 사고 조사 (impersonation, 권한 탈취 추적)
- "왜 이 데이터가 이렇게 됐어?" 질문에 답하기 위해

**관련 skill**: `business/multi-tenancy.md`, `business/auth-oauth-social.md`, `security/compliance-frameworks.md`, `messaging/kafka-patterns.md`
**관련 agent**: `compliance-auditor`, `security-scanner`
**관련 skill**: `/infra:postgresql-operations` (append-only 테이블 파티셔닝)

---

## 1. Audit Log vs 시스템 로그 (혼동 금지)

| 구분 | 시스템 로그 | Audit Log |
|---|---|---|
| 목적 | 디버깅, 운영 | 규제, 책임 추적 |
| 저장소 | Loki/CloudWatch/Splunk | DB (Postgres/Mongo) 또는 전용 (DynamoDB) |
| 보존 | 30~90일 | 1~7년 (규제별) |
| 변경 가능성 | 수정/삭제 가능 | **Append-only**, 수정 절대 금지 |
| 조회 주체 | 개발자 | 운영자, 사용자, 감사관 |
| 스키마 | unstructured (text) | **strict schema** (PII 분류 포함) |
| 검색 | 텍스트 grep | 인덱스 기반 (actor/resource/action) |

> **착각 금지**: "어차피 로그 다 찍는데 audit log 따로 왜?" → 시스템 로그는 변경 가능, 보존 짧고, 사용자에게 보여줄 수 없음. 규제 미충족.

---

## 2. 핵심 데이터 모델

```
AuditEvent (Append-only)
  ├─ id              (ULID, 시간순 정렬 가능)
  ├─ tenant_id       (multi-tenancy: tenant scope 필수)
  ├─ actor_type      (user / system / api_key / impersonation)
  ├─ actor_id        (user_id / service_name / api_key_id)
  ├─ actor_email     (denormalized — actor 삭제돼도 보존)
  ├─ action          (user.created / order.refunded / settings.changed)
  ├─ resource_type   (user / order / payment)
  ├─ resource_id     (대상 리소스 ID)
  ├─ changes         (JSON: { field: { before, after } })
  ├─ metadata        (JSON: ip, user_agent, request_id, session_id)
  ├─ severity        (info / warning / critical)
  ├─ created_at      (timestamp, immutable)
  └─ correlation_id  (분산 트랜잭션 추적)
```

**핵심 원칙**:
- **denormalize** — actor가 삭제돼도 audit는 남아야 함. email/name 스냅샷
- **changes는 JSON** — 스키마 진화에 강함. before/after 둘 다 저장 (diff 재계산 X)
- **correlation_id 필수** — 한 사용자 액션이 여러 이벤트 만들 때 묶기
- **PII 분류** — changes 안에 비밀번호/카드번호 들어가면 GDPR 위반. 마스킹 룰 코드화

---

## 3. Action 네이밍 컨벤션

```
<resource>.<verb>     예) user.created, order.refunded, api_key.rotated

verb 일관성:
  created / updated / deleted
  enabled / disabled
  granted / revoked
  invited / accepted / declined
  exported / imported

자주 빠뜨리는 것:
  login.succeeded / login.failed / login.suspicious
  permission.escalated  (권한 변경)
  impersonation.started / impersonation.ended
  data.exported / data.deleted  (GDPR 필수)
```

> **레지스트리 패턴**: 모든 action 이름을 한 곳에 enum/상수로 정의. 오타·중복 방지.

---

## 4. 기록 시점 (어디서 발생시키는가)

### 옵션 A — 도메인 이벤트 발행 (권장)

```
Service Layer → DomainEvent("OrderRefunded") 발행
                    ↓
            EventBus (in-process / Kafka)
                    ↓
            AuditLogHandler → AuditEvent 저장
```

**장점**: 비즈니스 로직과 audit 분리, 누락 시 도메인 이벤트 자체를 누락
**단점**: 이벤트 스키마 정의 필요

**Spring 예시**:

```java
// Service
class OrderService {
    void refund(Long orderId, Money amount) {
        var order = repo.findById(orderId);
        order.refund(amount);
        events.publish(new OrderRefundedEvent(order.id, amount, ctx.actor()));
    }
}

// Audit Handler (별도 클래스, 비동기)
@Component
class AuditLogHandler {
    @TransactionalEventListener(phase = AFTER_COMMIT)
    @Async
    void on(OrderRefundedEvent e) {
        auditWriter.write(AuditEvent.builder()
            .action("order.refunded")
            .resourceType("order").resourceId(e.orderId())
            .changes(Map.of("status", Map.of("before", "PAID", "after", "REFUNDED")))
            .actor(e.actor())
            .build());
    }
}
```

**Go 예시 (in-process bus)**:

```go
// Service
func (s *OrderSvc) Refund(ctx context.Context, id OrderID, amt Money) error {
    o, _ := s.repo.Get(ctx, id)
    o.Refund(amt)
    s.bus.Publish(ctx, OrderRefunded{ID: id, Amount: amt, Actor: ActorFrom(ctx)})
    return s.repo.Save(ctx, o)
}

// Handler (별도 goroutine)
func (h *AuditHandler) OnOrderRefunded(ctx context.Context, e OrderRefunded) {
    h.writer.Write(ctx, AuditEvent{
        Action: "order.refunded",
        ResourceID: string(e.ID),
        Changes: map[string]any{"status": map[string]string{"before": "PAID", "after": "REFUNDED"}},
        Actor: e.Actor,
    })
}
```

**핵심**: `AFTER_COMMIT` (Spring) / 트랜잭션 commit 후 발행 (Go) — 비즈니스 트랜잭션 롤백 시 audit도 자연 미발행. **반대로**, audit 쓰기 실패가 비즈니스 트랜잭션을 롤백하면 안 됨 (DLQ 행).

### 옵션 B — 컨트롤러/Use Case에서 직접 호출

```
@PostMapping("/orders/{id}/refund")
fun refund(...) {
    val result = orderService.refund(id)
    auditLog.write("order.refunded", id, changes)
    return result
}
```

**장점**: 단순
**단점**: 호출 누락 위험 (try/catch 안 들어가면 빠짐), 비즈니스 코드와 혼재

### 옵션 C — DB Trigger / CDC

```
Postgres trigger / Debezium CDC → audit_log 테이블 자동 기록
```

**장점**: 누락 불가
**단점**: 의도(누가 왜)를 잃어버림. Trigger는 actor를 모름 → session var/header 필요

> **추천**: A가 기본. 인프라성 변경(권한, 설정)은 C 보완.

---

## 5. 저장소 선택

| 저장소 | 적합 | 부적합 |
|---|---|---|
| **Postgres (별도 테이블)** | MVP, ~1억 row, JSONB 인덱스 | TB급, 복합 검색 부담 |
| **MongoDB / DynamoDB** | 스키마 진화, ~10억 row | 트랜잭션 일관성 |
| **Elasticsearch / OpenSearch** | 복잡한 검색·필터, 운영자 UI | 비용↑, 영속 저장소 X (DLQ 필요) |
| **Kafka + S3 (Iceberg/Delta)** | 영구 보존, BI 분석 | 실시간 조회 어려움 |
| **전용 SaaS (Datadog Audit, AWS CloudTrail Lake)** | 규제 ↑, 자체 운영 부담↓ | 비용, lock-in |

**권장 진화 경로**:
```
MVP        → Postgres (audit_events 테이블 + tenant_id BTREE 인덱스)
중규모     → Postgres + ES (Postgres source-of-truth, ES 복제 검색용)
대규모     → Kafka source → S3 archive + ES hot tier
규제 강함  → AWS CloudTrail Lake / 전용 SaaS 병행
```

---

## 6. Append-Only 강제 (중요)

```sql
-- Postgres 예시
CREATE TABLE audit_events (
  id ULID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  ...
);

-- 수정/삭제 차단
REVOKE UPDATE, DELETE ON audit_events FROM application_role;

-- 보존 만료 시 archive 테이블로만 이동 (TRUNCATE 금지, 파티션 detach)
```

**원칙**:
- 애플리케이션 권한에서 UPDATE/DELETE 금지
- 마이그레이션도 audit_events는 ALTER만, 데이터 변경 X
- 파티셔닝(월별)으로 보존 만료 처리 — `DETACH PARTITION` + S3 archive
- "오타 났어요, 수정해주세요" → **거절**. 새 이벤트 추가(`audit.corrected`)

---

## 7. Tenant-Scoped 격리

```
모든 쿼리: WHERE tenant_id = :current_tenant
```

- Multi-tenancy: tenant 관리자가 **자기 tenant만** 조회 가능
- Super Admin이 tenant 데이터 보면 → **Super Admin 자체가 audit 이벤트** (`admin.viewed_tenant_audit`)
- Tenant context 미설정 시 audit 쿼리 **자동 거부** (RLS 또는 ORM scope)

→ multi-tenancy: [`multi-tenancy`](../multi-tenancy/SKILL.md)

---

## 8. 운영자 UI (사용자에게 보여주기)

### 필수 화면

```
조직 설정 → Activity / Audit Log
  ├─ 필터: 기간 / actor / action / resource
  ├─ 검색: 키워드
  ├─ 행: timestamp | actor (avatar+email) | action | resource | IP
  ├─ 클릭: 상세 패널 (changes diff, metadata)
  └─ Export: CSV / JSON (대용량은 비동기 + email 알림)
```

**UX 팁**:
- 시간 표시: 사용자 timezone 변환
- IP는 geo-lookup ("서울에서 접속") — 의심 행위 빠른 인지
- 권한 변경/데이터 export 같은 critical action은 **눈에 띄게** (빨강 라벨)
- "이 변경 되돌리기" 같은 기능 절대 X — audit는 read-only

### 알림 통합

- 의심 액션(`login.failed` 5회, `permission.escalated`, `data.exported`) → Slack/Email 즉시 알림
- 일별 요약 (Owner 대상): "어제 활동 요약 — 23 events"
- alerting: `/observability:alerting-discord`

---

## 9. 보존(Retention) 및 삭제

### 규제별 권장 기간

| 규제 | 기간 | 비고 |
|---|---|---|
| SOC 2 | 1년+ | 일반 SaaS B2B |
| HIPAA | 6년 | 의료 |
| PCI-DSS | 1년 (즉시 조회 90일+) | 카드 결제 |
| GDPR (Article 30) | 활동 기간 + 합리적 기간 | EU 사용자 |
| 한국 개인정보보호법 | 5년 (개인정보 처리위탁 등) | KR 서비스 |

**기본값**: **2년 retention + 1년 archive (총 3년)**. 규제 산업이면 7년.

### Tenant 삭제 시 (GDPR Right to Erasure)

```
Tenant 탈퇴 → 30일 grace period → audit_events 삭제? NO
```

- **Audit log 자체는 삭제 X** — "왜 삭제됐는가" 자체가 audit 대상
- 대신 **PII만 마스킹** (`actor_email = "<deleted>@<deleted>"`)
- ID는 유지하되 외부 연결 끊김 → 규제 충족 + 추적 가능

---

## 10. 성능 패턴

### 쓰기 (Write)

- **비동기 발행** — 사용자 요청 응답 지연 X
- **Kafka 또는 in-memory queue** → 별도 worker가 DB 적재
- DLQ + 재시도 (장애 시 메모리 큐 유실 방지)

### 읽기 (Query)

- 인덱스: `(tenant_id, created_at DESC)`, `(tenant_id, actor_id)`, `(tenant_id, resource_type, resource_id)`
- JSONB GIN 인덱스 (changes 검색 시)
- 파티셔닝: 월별 (Postgres native partition) — **`pg_partman` 확장**으로 자동 생성/만료 권장. 수동 `CREATE TABLE...PARTITION OF` 누락 시 INSERT 실패
- 90일 이상 조회는 archive로 redirect (느려도 됨, 자주 안 함)

### 카운팅

- "최근 1일 events 수" 같은 지표는 별도 카운터 (Redis HINCRBY)
- DB COUNT(*) 매번 X

---

## 11. 안티패턴

| 안티패턴 | 위험 | 올바른 방법 |
|---|---|---|
| 시스템 로그(Loki)에 audit 의존 | 보존 짧음, 변경 가능, 규제 미충족 | 별도 DB 테이블, append-only |
| changes에 비밀번호/카드번호 | GDPR/PCI-DSS 위반 | 마스킹 룰 + 화이트리스트 필드만 기록 |
| actor 외래키만 저장 (denormalize X) | actor 삭제 시 추적 불가 | email/name 스냅샷 |
| "감사 모드" 토글 | 사고 시 끄고 잊어버림 | 항상 켬, 끄기 자체가 audit |
| Audit 쓰기 실패 시 비즈니스 트랜잭션도 롤백 | 카프카 다운 → 결제 안 됨 | 비동기 + DLQ + 알림 (서비스 가용성 ↑) |
| Audit를 사용자 응답에 동기 포함 | 응답 지연 | 비동기 발행 |
| "수정 요청" 받기 | append-only 위반 | 새 이벤트(`audit.corrected`)로 정정 |
| Tenant scope 누락 | 데이터 유출 | RLS 또는 ORM scope 자동 |
| Retention 정책 미정 | 비용 폭증, 규제 미충족 | 첫날 retention 결정 + 파티셔닝 |

---

## 12. ADR 템플릿 — Audit Log 결정

```markdown
## Audit Log ADR

| 항목 | 결정 | 대안 | 근거 |
|---|---|---|---|
| 저장소 | Postgres audit_events 테이블 | ES / SaaS | MVP 단순, JSONB로 진화 |
| 발행 방식 | 도메인 이벤트 → 비동기 핸들러 | 직접 호출 / CDC | 누락 방지 + 응답 지연 X |
| Retention | 2년 hot + 1년 S3 archive | 1년 / 7년 | SOC2 충족, 비용 균형 |
| 파티셔닝 | 월별 (Postgres native) | 단일 테이블 | 만료 처리 용이 |
| Tenant 격리 | RLS + ORM scope | 코드 WHERE 수동 | 누락 위험 제거 |
| PII 마스킹 | 화이트리스트 필드만 changes 저장 | 블랙리스트 | 누락 시 위반 |
| 사용자 UI | Owner/Admin 조회 + CSV export | API만 | 셀프 서비스 + 규제 답변 |
| 알림 | critical action 즉시 Slack | 일별 요약만 | 보안 사고 대응 시간 ↓ |
```

---

## 13. Quick Start Checklist

- [ ] Audit Log ADR (저장소, retention, 발행 방식)
- [ ] `audit_events` 테이블 + 월별 파티션
- [ ] Append-only 권한 (REVOKE UPDATE, DELETE)
- [ ] Action 레지스트리 (enum/상수)
- [ ] 도메인 이벤트 → AuditLogHandler (비동기)
- [ ] PII 마스킹 룰 (화이트리스트 필드)
- [ ] Tenant scope (RLS 또는 ORM)
- [ ] Correlation ID 전파 (request → events)
- [ ] 운영자 UI (필터/검색/상세/export)
- [ ] Critical action 알림 (Slack/Email)
- [ ] Login 이벤트 (succeeded/failed/suspicious)
- [ ] Impersonation 이벤트 (Super Admin이 사용자로 로그인)
- [ ] Data export 이벤트 (GDPR 답변용)
- [ ] Retention 정책 + 파티션 detach 자동화
- [ ] 모니터링: 발행 lag, DLQ 크기, write latency

---

## 14. 관련 자원

**우리 시스템 내부**:
- `skills/business/multi-tenancy.md` — tenant scope
- `skills/business/auth-oauth-social.md` — login event 발행
- `skills/security/compliance-frameworks.md` — SOC2/HIPAA/GDPR 매핑
- `skills/messaging/kafka-patterns.md` — 비동기 발행
- `skills/infrastructure/database-postgres.md` — 파티셔닝, JSONB
- `agents/compliance-auditor` — 감사 보고서 자동화
- `agents/security-scanner` — 의심 행위 탐지

**외부 자원**:
- AWS CloudTrail Lake (감사 전용 SaaS)
- Datadog Audit Trail
- OpenTelemetry Logs Data Model (audit 매핑 권장)
- NIST SP 800-92 (Log Management Guide)

---

## 15. 다음 단계

1. **이상 행위 탐지 (UEBA)** — 비정상 패턴 자동 알림 (대량 export, 새벽 권한 변경)
2. **분석/BI 통합** — Athena/BigQuery로 long-term 분석
3. **사용자 셀프 서비스** — "내 데이터 활동 보기" (개인정보 대시보드)
4. **Webhook 발행** — 고객사 SIEM(Splunk/Datadog)으로 실시간 export
5. **Forensic search** — 사고 조사용 강화된 검색 (timeline 시각화)

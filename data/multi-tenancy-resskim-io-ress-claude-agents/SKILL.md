---
name: multi-tenancy
description: "멀티테넌시 — Schema·Row·Database 격리 모델, Team/Org 도메인 모델, tenant context 전파, 멤버 권한, 초대, 테넌트 단위 과금. Use when 단일 사용자 SaaS 를 팀·조직 단위로 확장하고 격리 방식을 결정할 때."
---

# Multi-Tenancy

멀티테넌시 아키텍처 — Team/Org 관리, 데이터 격리(Schema/Row/Database), 멤버 권한, 초대 흐름, 컨텍스트 전파. SaaS 부트스트랩 핵심. 신규 프로젝트 시작 시 반드시 결정.

신규 SaaS가 단일 사용자 → 팀/조직 단위로 확장될 때 반복되는 패턴.
**가장 비싼 결정은 데이터 격리 모델** — 나중에 바꾸기 어려움. 처음부터 신중하게.

## When to Use

- 통학차량(학원 단위), 심리상담(상담소 단위) 등 **여러 사용자가 한 단위로 묶이는 SaaS**
- B2B SaaS 기획 단계 (회사 = tenant)
- 단일 사용자 SaaS를 팀 기능으로 확장
- "조직별 데이터 격리" 요구사항 발생 시
- 멤버 초대/권한 관리 필요

**관련 skill**: `architecture/modular-monolith.md`, `security/auth-patterns.md`, `business/auth-oauth-social.md`
**관련 agent**: `architect-agent`, `tech-lead`
**관련 skill**: `/infra:postgresql-operations`, `/infra:mysql-operations`

---

## 1. 격리 모델 결정 (가장 중요)

| 모델 | 격리 수준 | 비용 | 운영 복잡도 | 적합 |
|---|---|---|---|---|
| **Shared DB, Shared Schema (Row-level)** | 약함 | 가장 낮음 | 낮음 | MVP, B2C, 100~10000 tenant |
| **Shared DB, Schema-per-tenant** | 중간 | 중간 | 중간 | 중규모 B2B, 50~500 tenant |
| **Database-per-tenant** | 강함 | 높음 | 높음 | 엔터프라이즈, 규제 산업, ~50 tenant |
| **Hybrid (Pool + Silo)** | 가변 | 가변 | 높음 | 큰 고객 silo + 작은 고객 pool |

> **핵심 결정**: 첫 tenant 들어오기 전에 결정. **모델 변경은 마이그레이션 비용 매우 큼**.

### Row-level (Shared) — 가장 흔함

```sql
모든 테이블에 tenant_id 컬럼:
  users (id, tenant_id, email, ...)
  orders (id, tenant_id, user_id, amount, ...)
  posts (id, tenant_id, ...)

모든 쿼리에 tenant_id WHERE 절 자동 적용
PostgreSQL Row-Level Security (RLS) 활용
```

**장점**: 운영 단순, 비용 낮음, scale 쉬움
**단점**: tenant 간 데이터 혼합 위험 (코드 버그 = 데이터 유출)

### Schema-per-tenant — 중간

```
PostgreSQL:
  tenant_a 스키마: users, orders, posts
  tenant_b 스키마: users, orders, posts

쿼리 시 schema 동적 전환 (search_path)
```

**장점**: 격리 강함, 백업/복원 tenant 단위
**단점**: 스키마 마이그레이션 N번 (tenant 수만큼)

### Database-per-tenant — 강함

```
tenant_a → DB1 (별도 RDS 인스턴스 가능)
tenant_b → DB2
```

**장점**: 완전 격리, 규제 대응, "내 데이터 우리 리전에만"
**단점**: 인프라 비용 ↑, 운영 복잡 (tenant N개 = DB N개 마이그레이션)

---

## 2. 도메인 모델

```
Tenant (Organization / Workspace / Team)
  ├─ id
  ├─ slug (URL: app.com/<slug>/...)
  ├─ name, logo, settings
  ├─ plan (Free / Pro / Enterprise)
  └─ created_at

Membership (User ↔ Tenant)
  ├─ user_id
  ├─ tenant_id
  ├─ role (owner / admin / member / guest)
  ├─ status (active / invited / suspended)
  ├─ joined_at
  └─ invited_by

Invitation
  ├─ tenant_id
  ├─ email
  ├─ role
  ├─ token (random 32 bytes)
  ├─ expires_at
  └─ accepted_at
```

**핵심 원칙**:
- **User는 N개 Tenant에 속할 수 있음** (개인이 여러 회사/팀)
- **Membership = 관계 자체** (user 따로, tenant 따로 만들 수 있음)
- **role은 시스템 정의 + 커스텀 가능** (큰 SaaS는 커스텀 role 지원)

---

## 3. URL/UX 패턴

### Path-based (가장 흔함)

```
app.com/<tenant_slug>/dashboard
app.com/<tenant_slug>/users
```

**장점**: 명확, 즐겨찾기/공유 쉬움
**단점**: 도메인 분리 안 됨 (쿠키 공유)

### Subdomain-based

```
tenant-a.app.com/dashboard
tenant-b.app.com/dashboard
```

**장점**: 격리감, 화이트라벨 가능
**단점**: 와일드카드 SSL 인증서, CORS 복잡

### Custom Domain

```
clientcompany.com → 우리 SaaS
```

**장점**: 화이트라벨 완전, B2B 엔터프라이즈
**단점**: SSL 자동화 (LetsEncrypt), DNS 가이드 필요

---

## 4. 컨텍스트 전파 (Tenant Context)

요청이 들어오면 **현재 어느 tenant 컨텍스트인지** 모든 레이어가 알아야 함.

```
HTTP Request
  ├─ Path: /<tenant_slug>/...
  ├─ Header: X-Tenant-Id (대안)
  └─ JWT claim: tenant_id (대안)
        ↓
  Middleware: Tenant 식별 + Membership 검증
        ↓
  Application Layer: Context 객체에 tenant_id 주입
        ↓
  Repository Layer: 모든 쿼리에 tenant_id 자동 적용
        ↓
  DB: RLS 또는 schema 전환
```

**핵심**:
- **tenant_id를 매번 함수 인자로 전달 X** — 컨텍스트(Spring `@RequestScope`, Go `context.Context`, Node.js `AsyncLocalStorage`)에 주입
- **Repository에서 자동 필터** — 비즈니스 로직이 tenant_id 신경 쓰지 않게
- **누락 시 에러** — tenant_id 없이 쿼리하면 즉시 실패 (운영 사고 방지)

---

## 5. 권한 (Authorization) 패턴

### RBAC — 역할 기반

```
Owner: 모든 권한, billing, 삭제 가능
Admin: 멤버 관리, 설정 변경
Member: 일반 작업
Guest: 읽기만, 일부 리소스만
```

### ABAC — 속성 기반 (정교)

```
"User X는 Resource R에 대해 Action A 할 수 있는가?"
조건: tenant_id 일치 + role >= member + R.owner_id == X (또는 R.shared_with X 포함)
```

### 구현

- **간단**: RBAC + 코드 안 if/else
- **중간**: Casbin, OPA (Open Policy Agent) — 정책 외부화
- **고급**: 자체 ABAC 엔진 + 정책 DSL

> **권장**: MVP는 RBAC, 5+ 역할 / 복잡한 조건 등장하면 OPA 도입.

---

## 6. 초대 (Invitation) 흐름

```
1. Owner: "X@email.com을 admin으로 초대"
2. Server:
   - Invitation 생성 (token, expires=7일)
   - Email 발송: "Click to join: https://app/invite?t=<token>"
3. 초대받은 사람:
   - Click → 가입 페이지 (token 검증)
   - 신규 사용자 → 회원가입 (소셜 로그인 가능) → Membership 자동 생성
   - 기존 사용자 → 로그인 → Membership 자동 생성
4. Server:
   - Invitation.accepted_at 기록
   - 알림: "새 멤버가 합류했어요" (Owner에게)
```

**보안**:
- Token 만료 (7일~14일)
- 1회 사용 (accepted_at 기록 후 무효)
- Email 주소 일치 검증 (다른 이메일로 가입 시 거부)

**UX 팁**:
- Bulk invite (CSV 업로드)
- 도메인 자동 가입 (`@company.com` 이메일은 자동 멤버)
- 대기열 (admin 승인 후 활성화)

---

## 7. Billing 통합 (Tenant 단위 과금)

```
Tenant ←→ Stripe Customer (1:1)
Subscription은 Tenant 단위
사용량 기반 과금: tenant 단위 metric (active users, storage 등) 측정
```

**플랜 변경 흐름**:
- Owner만 권한
- Stripe Customer Portal 활용 (셀프 서비스)
- Plan downgrade 시 limit check (over-limit 사용자 처리)

→ 결제 통합: [`payment-integration`](../payment-integration/SKILL.md)

---

## 8. 관리자 / Audit

### Tenant Admin (Owner/Admin)

- 멤버 목록 + 역할 변경 + 추방
- 초대 발송 + 취소
- 설정 (이름, 로고, 도메인)
- Billing (Owner만)
- Audit Log 조회 (누가 언제 뭐 했는지)

### Super Admin (SaaS 운영자)

- 전체 Tenant 목록 + 검색
- Tenant 정지/활성
- Impersonate (사용자 지원, 활동 기록 필수)
- Tenant 단위 메트릭 (가입일, 플랜, MAU)

**주의**: Super Admin이 사용자 데이터를 함부로 보면 안 됨 → **데이터 접근 시 audit 로그 + 사용자 동의 (GDPR)**

---

## 9. 안티패턴 모음

| 안티패턴 | 위험 | 올바른 방법 |
|---|---|---|
| 격리 모델 결정 미루기 | 첫 tenant 들어오면 변경 어려움 | 신규 프로젝트 ADR 첫 항목 |
| `WHERE tenant_id = ?` 수동 추가 | 한 곳 빠지면 데이터 유출 | RLS 또는 ORM scope 자동 적용 |
| User-Tenant 1:1 | 개인이 여러 팀 못 들어감 | Membership 관계 분리 |
| Tenant context를 함수 인자로 | 코드 매번 전달, 빠짐 위험 | AsyncLocalStorage / RequestScope |
| Owner 1명만 (단점 인지 X) | Owner 퇴사 시 잠김 | Owner 다중 또는 양도 흐름 |
| 초대 토큰 영구 유효 | 가로채기 시 영구 위험 | 7~14일 만료 + 1회 사용 |
| Custom Domain 시 SSL 수동 | 운영 부담 | LetsEncrypt 자동화 (Caddy/Cert-Manager) |
| 권한 체크를 클라이언트만 | API 직접 호출 시 우회 | 서버에서 항상 검증 |

---

## 10. ADR 템플릿 — 멀티테넌시 결정

```markdown
## 멀티테넌시 ADR

| 항목 | 결정 | 대안 | 근거 |
|---|---|---|---|
| 격리 모델 | Row-level (Shared DB) | Schema / DB | tenant 1만 미만, 비용 우선 |
| URL 패턴 | Path-based (/<slug>/) | Subdomain | SSL 단순 |
| User-Tenant 관계 | N:N (Membership) | 1:1 | 개인이 여러 회사 |
| 권한 | RBAC (4 역할) | ABAC | MVP 단순 |
| 초대 토큰 만료 | 7일 + 1회 사용 | 영구 / 24h | UX vs 보안 균형 |
| Owner 정책 | 다중 Owner + 양도 | 단일 Owner | Owner 부재 위험 |
| Billing | Tenant 단위 | User 단위 | B2B 표준 |
```

→ `agents/tech-lead`로 ADR 작성 위임. **이 결정은 신규 프로젝트 ADR 1순위**.

---

## 11. Quick Start Checklist

- [ ] 격리 모델 ADR (가장 먼저)
- [ ] Tenant + Membership + Invitation 도메인 모델
- [ ] RLS 또는 ORM Tenant scope 자동화
- [ ] Tenant context 전파 (AsyncLocalStorage 등)
- [ ] URL 패턴 (Path / Subdomain / Custom Domain)
- [ ] 회원가입 흐름 (개인 → tenant 자동 생성 또는 초대 받기)
- [ ] 초대 토큰 (만료, 1회 사용, 이메일 검증)
- [ ] RBAC 역할 정의 (Owner/Admin/Member/Guest)
- [ ] Owner 양도 흐름 (Owner 부재 방지)
- [ ] Tenant 설정 페이지
- [ ] Audit Log (멤버 변경, 권한 변경)
- [ ] Billing 통합 (Tenant 단위)
- [ ] Super Admin 페이지 (운영자용)
- [ ] 데이터 export/삭제 (GDPR)
- [ ] 모니터링: Tenant 단위 메트릭 (MAU, plan, churn)

---

## 12. 관련 자원

**우리 시스템 내부**:
- `skills/architecture/modular-monolith.md` — Tenant 경계와 모듈 경계
- `skills/security/auth-patterns.md` — 인증/인가
- `skills/business/auth-oauth-social.md` — 사용자 로그인 (이 skill과 결합)
- `skills/business/payment-integration.md` — Tenant 단위 과금
- `agents/architect-agent` — 격리 모델 설계 위임
- `/infra:postgresql-operations` — DB 격리 구현
- `agents/tech-lead` — ADR 작성

**외부 자원**:
- AWS SaaS Lens (Well-Architected for SaaS)
- Stripe + Multi-tenant Billing 가이드
- PostgreSQL Row-Level Security 공식 문서
- OPA (Open Policy Agent)

---

## 13. 다음 단계

1. **데이터 양 ↑ → Read replica 분리** (`skills/infrastructure/database-postgres.md`)
2. **Tenant 매우 큼 → Sharding** (DB 격리 모델 전환 검토)
3. **국가별 데이터 보존** → Region-pinned tenant (DB-per-tenant in region)
4. **Self-hosted 옵션 (엔터프라이즈)** → 별도 배포 방식 (`skills/cicd/`)
5. **SSO/SAML (큰 고객)** → 인증 skill 확장

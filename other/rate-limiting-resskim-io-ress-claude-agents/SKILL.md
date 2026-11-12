---
name: rate-limiting
description: "API 요청 제한 — Token Bucket·Sliding Window·Leaky Bucket 알고리즘, Redis 구현, user·tenant·IP 다층 키, 429 응답·헤더, 분산 동기화. Use when API 남용을 막거나 호출 한도 정책을 설계할 때."
---

# Rate Limiting

API 요청 제한 — 알고리즘 (Token Bucket / Sliding Window / Leaky Bucket / Fixed Window), Redis/메모리 구현, per-user/per-tenant/per-IP 다층 키, 429 응답·헤더, 분산 환경 동기화. SaaS 부트스트랩 필수.

남용·악성 트래픽 방어이자 **공정성 도구** (시끄러운 이웃 격리). 결제·인증과 직결: 무제한 시도 방지.

## When to Use

- Public API 제공 (외부 개발자에게 token/scope 발급)
- 인증 엔드포인트 (login/signup brute-force 차단)
- 결제·민감 액션 (refund, password change, 2FA)
- Free vs Pro 플랜 차등 (요금제 quota)
- 봇/스크레이퍼 차단 (티켓팅·콘텐츠)
- LLM API 비용 보호 (per-tenant token quota)

**관련 skill**: `business/auth-oauth-social.md`, `business/payment-integration.md`, `business/multi-tenancy.md`, `security/auth-patterns.md`
**관련 skill**: `/security:anti-bot`, `/saas:virtual-waiting-room`, `/infra:redis-operations`

---

## 1. 알고리즘 비교

| 알고리즘 | 정확도 | 메모리 | 구현 난이도 | 적합 |
|---|---|---|---|---|
| **Fixed Window** | 낮음 (경계 burst) | 1 카운터 | 매우 쉬움 | 대략적 protection |
| **Sliding Window Log** | 높음 | O(N) timestamps | 쉬움 | 정확한 N/min, 트래픽 ↓ |
| **Sliding Window Counter** | 중간 | 2 카운터 | 쉬움 | **API 표준 권장** |
| **Token Bucket** | 높음 (burst 허용) | 2 값 (tokens, ts) | 중간 | burst-friendly UX |
| **Leaky Bucket** | 높음 (burst 거부) | 큐/카운터 | 중간 | 강제 평탄화 (네트워크 shaping) |
| **GCRA** (Generic Cell Rate) | 높음 | 1 timestamp | 어려움 | high-throughput, redis-cell |

### Fixed Window — 가장 간단, 함정 있음

```
"분당 60개" → counter[2026-04-28T10:00] = N

위험: 10:00:59에 60개 + 10:01:00에 60개 = 1초에 120개 burst
```

### Sliding Window Counter — 권장 기본

```
이번 분 카운터 + 이전 분 카운터 비례 가중

current = counter[10:01]
previous = counter[10:00]
elapsed_in_current = 30s (현재 분의 30초 지남)

weighted = current + previous * (1 - 30/60) = current + previous * 0.5

if weighted > limit → 거부
```

**장점**: 메모리 2 키, 정확도 ~95%, redis 구현 쉬움
**단점**: 완벽하진 않음 (가중 평균 가정)

### Token Bucket — burst 허용 UX

```
버킷 용량: 100 tokens
리필 속도: 10 tokens/sec

요청 시 토큰 1개 차감, 0이면 거부
오랫동안 안 쓰면 가득 참 → 갑자기 100개까지 burst 허용
```

**장점**: 정상 사용자 UX 좋음 (조용하다 한 번 몰아서 OK)
**단점**: 일정한 속도 강제 못 함

---

## 2. 알고리즘 선택 가이드

| 시나리오 | 권장 |
|---|---|
| Public API ("100 req/min") | **Sliding Window Counter** |
| 결제·민감 ("5 attempts / 15min") | **Sliding Window Log** (정확도) |
| 사용자 대화형 (burst OK) | **Token Bucket** |
| 외부 API 호출 (downstream 보호) | **Leaky Bucket** |
| 초고속 (백만 RPS) | **GCRA** (redis-cell) |

> **MVP 추천**: Sliding Window Counter + redis. 90% 케이스 커버.

---

## 3. 키 설계 (Multi-layer)

```
요청 식별:
  per_ip       — 익명 사용자, DDoS 1차 방어
  per_user     — 로그인 사용자
  per_api_key  — 외부 API 토큰
  per_tenant   — 조직 단위 quota
  per_endpoint — 엔드포인트별 차등 ("login은 5/15min", "search는 100/min")

결합:
  key = "rl:{tenant}:{user}:{endpoint}:{window}"
  key = "rl:ip:{ip}:{endpoint}"
```

### 다층 적용 (AND 모두 통과)

```
1) IP 레벨   — DDoS, 익명 보호 (1000/min)
2) User 레벨  — 사용자 quota (100/min)
3) Tenant 레벨 — 플랜별 (Free 1k/day, Pro 100k/day)
4) Endpoint  — 민감 액션 (login 5/15min)
```

→ multi-tenancy: [`multi-tenancy`](../multi-tenancy/SKILL.md)

---

## 4. Redis 구현 — Sliding Window Counter

```lua
-- KEYS[1] = current window key, KEYS[2] = previous window key
-- ARGV[1] = limit, ARGV[2] = elapsed_in_current_window (0~1)

local current = tonumber(redis.call('GET', KEYS[1]) or '0')
local previous = tonumber(redis.call('GET', KEYS[2]) or '0')
local weighted = current + previous * (1 - tonumber(ARGV[2]))

if weighted >= tonumber(ARGV[1]) then
  return 0  -- denied
end

redis.call('INCR', KEYS[1])
redis.call('EXPIRE', KEYS[1], 120)  -- 2x window
return 1
```

**주의**:
- Lua 스크립트로 atomic 보장 (INCR + EXPIRE 사이 race)
- Redis Cluster: 같은 user의 키는 hash tag로 묶음 → `{user:123}:rl:login`
- TTL 설정 필수 (메모리 폭주 방지)

### Token Bucket — 핵심만

Hash 1개에 `tokens`, `ts` 저장. 매 호출 시:
1. 경과 시간만큼 refill (`tokens = min(capacity, tokens + elapsed * rate)`)
2. `tokens < 1` → 거부, 아니면 `-= 1`
3. `HSET` + `EXPIRE`로 atomic 갱신

→ Lua 전체 구현: redis-cell 모듈 또는 `/infra:redis-operations` 참조 (GCRA가 더 효율적).

---

## 5. HTTP 응답 (RFC 9239 + 표준)

### 정상 응답 (Limit 정보 노출)

```http
HTTP/1.1 200 OK
RateLimit-Limit: 100
RateLimit-Remaining: 87
RateLimit-Reset: 42        # seconds until reset
X-RateLimit-Used: 13       # 보조 (호환성)
```

### 거부 응답

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 42                                # seconds (또는 HTTP-date)
RateLimit-Limit: 100
RateLimit-Remaining: 0
RateLimit-Reset: 42
Content-Type: application/problem+json

{
  "type": "https://api.example.com/errors/rate-limit-exceeded",
  "title": "Rate limit exceeded",
  "status": 429,
  "detail": "Limit of 100 requests per minute exceeded.",
  "limit": 100,
  "window": "1m",
  "retry_after": 42
}
```

**표준**:
- `RateLimit-*` 헤더 (RFC draft, 신규 표준)
- `X-RateLimit-*` 헤더 (de-facto, 호환)
- `Retry-After` 필수 (클라이언트 백오프)
- Problem Details (RFC 7807) — JSON 응답 표준

---

## 6. 어디서 적용 (계층)

```
Layer 1: CDN/WAF (Cloudflare, AWS WAF)
  - Geo block, 1차 DDoS 방어
  - 거대 IP 단위 (~10k req/sec)

Layer 2: API Gateway (Kong, Envoy, AWS API Gateway)
  - per-API-key quota
  - 1차 거부 (앱 도달 X)

Layer 3: Application middleware
  - per-user, per-tenant, per-endpoint
  - 비즈니스 로직과 결합

Layer 4: Database connection pool / 외부 API
  - downstream 보호 (Bulkhead 패턴)
```

**원칙**:
- **앞단에서 거부할수록 비용 ↓** — CDN > Gateway > App > DB
- **1차 방어는 dumb (IP)**, **2차 방어는 smart (user/tenant)**
- 두 곳에서 카운트 X — 한 곳에서만 (혼란 방지)

---

## 7. 분산 환경 동기화

### Redis 중앙 카운터 (정확)

- 모든 인스턴스가 동일 Redis 호출
- 정확하지만 latency 추가 (1~2ms)
- Redis 다운 시 fail-open vs fail-close 정책 결정

#### Fail-Open vs Fail-Close 트레이드오프

| 정책 | 동작 | 장점 | 단점 | 적합 |
|---|---|---|---|---|
| **Fail-Open** | Redis 다운 → 모두 허용 | 가용성 ↑, 정상 사용자 영향 X | DDoS·brute-force 무방어 (최악 시 폭주) | 일반 API, 비즈니스 우선 |
| **Fail-Close** | Redis 다운 → 모두 거부 | 보안·과금 보호 | 가용성 ↓ (Redis 장애 = 서비스 장애) | 결제·login·민감 액션 |
| **Hybrid** | Redis 다운 → 로컬 fallback (보수적 limit ÷ N 인스턴스) | 균형 | 구현 복잡 | 가장 권장 |
| **Bypass with cap** | Redis 다운 → IP 단위 in-memory 임시 limit | 유연 | local 카운터 부정확 | 중규모 |

> **권장**: **endpoint별 차등** — 결제·login은 fail-close, 일반 API는 fail-open. 한 정책으로 통일 X.

### Local Cache + Redis (성능)

```
1) 인스턴스 로컬 카운터 (1초 단위 집계)
2) 1초마다 Redis로 sync (ZINCR)
3) Redis가 글로벌 카운트 산정
```

**장점**: latency ↓ (대부분 로컬), 트래픽 ↓
**단점**: ~1초 lag, burst 살짝 허용

### Token Bucket 분산 (어려움)

- 토큰 1개 = atomic decrement → Redis만이 적합
- "분산 토큰 버킷"은 Lua 또는 transactional pipeline

---

## 8. 정책 결정 (얼마로 잡을까)

### 측정 기반 (권장)

```
1) 30일 정상 사용자 95th percentile 측정
2) 그 값 × 2~3배를 limit으로
3) 1주 모니터링 → 정상 사용자 거부율 < 0.1% 확인
4) 점진 조정
```

### 보안 민감 (작은 값 OK)

| 액션 | 권장 limit |
|---|---|
| Login | 5 / 15min (per IP+username) |
| Signup | 3 / hour (per IP) |
| Password reset 요청 | 3 / hour (per email) |
| 2FA 코드 입력 | 5 / 5min (per user) |
| Refund 요청 | 10 / day (per tenant) |

### 플랜별 차등

```
Free:    100 req/min, 1k req/day
Pro:     1000 req/min, 100k req/day
Enterprise: custom (계약)
```

→ 인증 brute-force: [`auth-oauth-social`](../auth-oauth-social/SKILL.md)

---

## 9. 사용자 경험 (UX)

### 클라이언트 동작

```
429 받으면:
  1) Retry-After 헤더 존중
  2) Exponential backoff + jitter
  3) 사용자에게 "잠시 후 다시" 안내 (1분 카운트다운)
  4) 큰 작업 분할 (bulk → batch)
```

### Quota 노출

- Pro 사용자에게 "오늘 78,432 / 100,000 요청 사용" 대시보드
- API 응답 헤더로 매번 노출
- 80% 도달 시 사전 알림 (Slack/Email)

### Soft vs Hard Limit

```
Soft: 80% 도달 → 알림만, 동작 OK
Hard: 100% 도달 → 거부 (429)
Burst: 일시 110% 허용 (10초 grace)
```

---

## 10. 안티패턴

| 안티패턴 | 위험 | 올바른 방법 |
|---|---|---|
| 인스턴스 로컬 카운터만 (Redis X) | 분산 환경에서 무용 | 중앙 Redis 또는 sticky session |
| Fixed Window 단독 | 경계 burst 2x | Sliding Window |
| 키에 timestamp 직접 (TTL X) | 메모리 폭주 | EXPIRE 필수 |
| `INCR` 후 검사 | 1 초과 허용됨 | Lua atomic 또는 `INCR` 후 즉시 비교 |
| 429에 Retry-After 누락 | 클라이언트 미친 듯 재시도 | 항상 포함 |
| 로그인 brute-force IP만 키 | NAT 사용자 모두 차단 | IP + username 결합 |
| 무차별 적용 | 정상 사용자 거부 | endpoint별 차등 |
| 측정 없이 limit 결정 | "낮으면 안전" → UX 망가짐 | p95 측정 후 ×2~3 |
| 거부율 모니터링 X | 정상 사용자 막힌 줄 모름 | 429 비율 알림 |
| Redis 다운 시 정책 미정 | 전부 거부 (fail-close) → 가용성 ↓ | fail-open + 알림 (또는 secondary) |
| LLM/외부 API 호출에 적용 X | 비용 폭주 | per-tenant token budget |

---

## 11. 모니터링

```
지표 (Prometheus):
  rate_limit_total{endpoint, result="allow|deny"} — 거부율
  rate_limit_active_keys                          — 활성 키 수
  rate_limit_redis_latency                        — Redis 응답 시간
  rate_limit_quota_used_ratio{tenant, plan}       — 플랜별 사용률

알림:
  - 429 비율 > 5% (정상 사용자 거부 의심)
  - 특정 IP/user 갑작스런 spike (공격)
  - Redis latency p99 > 50ms
  - 한 tenant가 quota 80% 초과 (사전 안내)
```

→ alerting: `/observability:alerting-discord`

---

## 12. ADR 템플릿 — Rate Limiting 결정

```markdown
## Rate Limiting ADR

| 항목 | 결정 | 대안 | 근거 |
|---|---|---|---|
| 알고리즘 | Sliding Window Counter | Token Bucket / GCRA | 정확도 + 단순 + Redis 구현 쉬움 |
| 저장소 | Redis (전용 클러스터) | local memory / DynamoDB | latency ↓ + atomic Lua |
| 적용 계층 | API Gateway + App middleware | Gateway만 / App만 | 다층 방어 (DDoS + biz) |
| 키 구성 | IP / user / tenant / endpoint | user만 | NAT/플랜 차등 대응 |
| Login 정책 | 5 / 15min (IP+username) | IP만 | 공격자 vs NAT 사용자 균형 |
| 플랜 quota | Free 100/min, Pro 1k/min | 단일 | 모네타이징 |
| Fail 정책 | Redis 다운 시 fail-open + 알림 | fail-close | 가용성 우선 |
| 응답 헤더 | RateLimit-* + Retry-After | X-RateLimit-* | RFC 표준 채택 |
```

---

## 13. Quick Start Checklist

- [ ] Rate Limiting ADR (알고리즘, 저장소, 정책)
- [ ] Redis 클러스터 (전용 또는 공유)
- [ ] 알고리즘 구현 (Lua 스크립트)
- [ ] 키 네이밍 규칙 (`rl:{layer}:{id}:{endpoint}:{window}`)
- [ ] 미들웨어 (App layer)
- [ ] 응답 헤더 표준화 (RateLimit-*, Retry-After)
- [ ] 429 응답 (Problem Details JSON)
- [ ] 로그인/2FA/refund 등 민감 액션 별도 정책
- [ ] 플랜별 quota (Free/Pro/Enterprise)
- [ ] 측정 (p95 기반 limit 산정)
- [ ] 모니터링 (allow/deny 비율, Redis latency)
- [ ] 알림 (정상 거부율 > 5%, spike, quota 80%)
- [ ] Fail 정책 (Redis 다운 시 fail-open/close)
- [ ] 클라이언트 SDK 가이드 (backoff)
- [ ] Quota 대시보드 (Pro 사용자)

---

## 14. 관련 자원

**우리 시스템 내부**:
- `skills/business/auth-oauth-social.md` — login brute-force
- `skills/business/payment-integration.md` — refund/sensitive actions
- `skills/business/multi-tenancy.md` — per-tenant quota
- `skills/business/admin-api-keys.md` — per-API-key quota
- `skills/security/auth-patterns.md` — 보안 패턴
- `/security:anti-bot` — 봇 차단 통합
- [`virtual-waiting-room`](../virtual-waiting-room/SKILL.md) — high-traffic 사례
- `/infra:redis-operations` — Redis 운영

**외부 자원**:
- IETF draft: RFC RateLimit Header Fields for HTTP
- Redis Cell module (GCRA 구현)
- Cloudflare Rate Limiting docs
- Stripe API rate limit docs (실전 정책)

---

## 15. 다음 단계

1. **Adaptive rate limiting** — 시스템 부하 기반 동적 조정
2. **DDoS 통합** — Cloudflare/AWS Shield와 연동
3. **봇 탐지 + 차등** — 정상 봇(Google) 허용, 악성 차단
4. **Cost-aware limiting** — LLM 토큰 단위 budget
5. **Tenant 단위 burst 자동 협상** — Pro 고객 일시 한도 ↑ API

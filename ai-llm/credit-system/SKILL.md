---
name: credit-system
description: "AI 사용량 과금 — 크레딧 모델, idempotent UsageRecord, 한도·auto-refill, LLM 원가+마진 가격, Free Tier, immutable ledger 환불. Use when 토큰·API 호출 단위 종량제나 충전식 크레딧을 설계할 때."
license: MIT
---

# Credit System — AI/사용량 모네타이징

LLM 토큰·API 호출·연산 시간 등 **사용량 단위로 과금**하는 비즈니스 패턴. `subscription-billing-flows.md` §5 Metered Billing의 자연 연장이며, AI 제품에서는 정액 seat + per-token usage **hybrid가 디폴트**.

> **이 skill은 사용량 모네타이징 전용 hub.** Stripe Subscription 자체는 `subscription-billing.md` 참조. 일회성 결제는 `payment-integration.md`. 이 문서는 **잔액·차감·임계치·LLM 원가 추적**의 도메인 모델과 함정에 집중.

## When to Use

- AI 제품 (LLM 챗봇, 코드 어시스턴트, 이미지 생성 등) 모네타이징 설계
- API 제품 (요청/GB/CPU초 단위) 가격 모델 설계
- "월정액으로 가? 충전식으로 가? 둘 다?" 의사결정
- LLM provider 원가 변동을 사용자 가격에 어떻게 반영할지
- 무료 tier(예: 월 100만 토큰)와 유료 한도 정책 설계
- AI 호출 폭증으로 한 사용자가 월 $1,000 청구되는 사고 예방

**관련 skill (cross-link)**:
- `business/subscription-billing.md` — 메인 hub, 정기 빌링 인프라 (seat 부분)
- `business/subscription-billing-flows.md` §5 — Metered Billing 패턴 (idempotency/late events 원칙)
- `business/subscription-billing-metrics.md` — MRR/Cohort SQL 패턴 → usage 메트릭으로 확장
- `business/payment-integration.md` — 충전 결제 (one-time topup)
- `business/rate-limiting.md` — 토큰/RPS hard cap, threshold 결합
- `business/notification-multichannel.md` — low balance / cap 도달 알림
- `business/audit-log.md` — usage_event 감사, refund/조정 기록
- `business/multi-tenancy.md` — tenant 단위 잔액, seat × usage 결합
- `ai/prompt-engineering.md`, `ai/rag-patterns.md` — 토큰 효율 (원가 절감)

**관련 agent**: `tech-lead` (가격 모델 ADR), `cost-analyzer` (LLM provider 원가 추적)
**관련 skill**: `/infra:postgresql-operations` (ledger 파티셔닝/아카이빙), `/messaging:broker-troubleshooting` (usage 이벤트 큐), `/infra:redis-operations` (잔액 캐시)

---

## 1. 모델 결정 매트릭스

| 모델 | 적합 | 사용자 멘탈 모델 | 함정 |
|---|---|---|---|
| **Prepaid Credit** (충전식) | API 제품, 변동성 큰 사용량 | "지갑에 잔액" — 친숙 | 미사용 잔액 환불/만료 정책, 회계 처리(deferred revenue) |
| **Postpaid Metered** | 엔터프라이즈, 신뢰관계 있는 B2B | "월말 청구서" | 미수금/dunning, 사용 폭증 시 충격 청구 |
| **Hybrid: Seat + Usage** | AI 제품 표준 (Cursor/v0/ChatGPT Pro) | "월 $20 + 한도 초과 시 충전" | seat 가격에 usage 어디까지 포함할지 |
| **Pay-as-you-go (no commit)** | Indie/playground 제품 | "쓴 만큼만" | 사용자 1명이 무한 사용 → 청구 폭탄 → 환불 분쟁 |
| **Tiered with Hard Cap** | B2C, 청구 폭탄 회피 | "정액 + 초과 시 차단" | 비즈니스 critical 호출도 차단되는 UX |
| **Tiered with Soft Overage** | B2B, 매출 우선 | "정액 + 초과 시 자동 청구" | 사용자 사전 동의 + 경고 흐름 필수 |

> **2026 트렌드 (AI 제품 디폴트)**:
> - **Hybrid (월 seat + per-token credit)**가 사실상 표준. ChatGPT Pro($20+사용량), Cursor($20 monthly+overage), v0(seat+credit), Anthropic Console(prepaid).
> - **Hard cap 기본 ON + 사용자 명시적 opt-in으로 soft overage 활성화**가 신뢰 표준 (청구 폭탄 사고 방지).
> - **Auto-refill** + **Spend limit**는 짝패. refill 없이 limit만 두면 운영 중단, limit 없이 refill만 두면 청구 폭탄.

### 모델 추상화 — `subscription-billing.md` SubscriptionGateway 연장

```
CreditGateway (interface)         # subscription-billing의 SubscriptionGateway와 짝
  ├─ create_account(tenant) → CreditAccountId
  ├─ topup(account, amount, currency, idempotency_key) → TxId   # 충전
  ├─ debit(account, units, meter, metadata, idempotency_key) → TxId  # 차감
  ├─ get_balance(account) → Balance{available, reserved, committed}
  ├─ set_threshold(account, level, action: notify|block|refill)
  └─ refund(tx_id, reason) → TxId   # 보상 트랜잭션

Adapters:
  ├─ StripeMetersAdapter   # postpaid usage → Stripe Subscription에 합산
  ├─ InternalLedgerAdapter # prepaid 자체 ledger (PostgreSQL)
  └─ LagoAdapter           # open-source metered billing 위임
```

**원칙**: 도메인 코드는 `CreditGateway`만 의존. Stripe Meters / 자체 ledger / Lago 어느 쪽이든 어댑터로 격리. `subscription-billing.md` Pattern과 동일.

---

## 2. 도메인 모델 (필수)

```
CreditAccount (1) ── (1) Tenant 또는 (1) Customer
  ├─ id
  ├─ tenant_id                    (multi-tenancy 결합)
  ├─ currency                     (USD/KRW/EUR — currency lock)
  ├─ balance_available            (즉시 사용 가능 = 충전 - 차감 - 예약)
  ├─ balance_reserved             (진행 중 요청 hold)
  ├─ free_tier_remaining          (월간 무료 잔량, 매월 reset)
  ├─ low_balance_threshold        (알림 임계치)
  ├─ auto_refill_enabled / auto_refill_amount / auto_refill_trigger
  ├─ spend_limit_monthly          (hard cap, 사용자 설정)
  └─ status: active|frozen|closed

CreditLedgerEntry (immutable, append-only)
  ├─ id, account_id, occurred_at
  ├─ entry_type: topup|debit|refund|adjustment|free_tier_grant|expiration
  ├─ amount                       (양수: 입금, 음수: 출금)
  ├─ balance_after                (스냅샷, 빠른 조회용. 주기적 재계산으로 검증)
  ├─ idempotency_key              (UNIQUE)
  ├─ source_event_id              (UsageEvent.id 또는 invoice.id)
  ├─ metadata (JSONB)             (model, prompt_tokens, completion_tokens, ...)
  └─ provider                     (stripe|internal|lago)

UsageEvent (raw, billing 전 단계)
  ├─ id (UUID), tenant_id, account_id
  ├─ meter                        (llm_tokens|api_calls|gb_storage|...)
  ├─ quantity                     (예: 12500 tokens)
  ├─ occurred_at, recorded_at     (late event 식별)
  ├─ idempotency_key              (UNIQUE — 같은 요청 재시도 시 1회만)
  ├─ unit_cost                    (이 요청 시점의 unit price snapshot)
  ├─ metadata (JSONB)             (request_id, model, prompt/completion 분리, latency)
  └─ status: pending|priced|debited|voided

PriceBook (시간 가변, immutable version)
  ├─ id, effective_at
  ├─ meter, model                 (예: meter=llm_tokens, model=claude-opus-5-5)
  ├─ unit                         (1000 tokens / 1 image / 1 GB-month)
  ├─ unit_amount, currency        (예: USD 0.02 — Opus 5.5 output, 2026-11 공시가)
  ├─ markup_percent               (provider 원가 대비 마진)
  └─ cost_basis_amount            (provider 원가, 회계용)
```

**핵심 원칙**:
- **Ledger는 immutable + append-only**: 잔액은 계산값 (sum). 직접 update 절대 금지. 오류 → adjustment entry 추가.
- **balance_available은 캐시**: source of truth는 `SUM(amount) FROM ledger WHERE account_id=...`. 정기 reconciliation으로 검증.
- **PriceBook = PlanVersion 패턴 재사용**: provider 원가 변동, 자체 마진 변경, 환율 변동을 시간축에 immutable 로 기록. UsageEvent에는 **그 시점 unit_cost를 snapshot**으로 저장 (소급 계산 금지).
- **idempotency_key는 두 곳에**: UsageEvent 발생 시(중복 기록 차단) + LedgerEntry 차감 시(중복 차감 차단). 둘은 다른 키.
- **late event 처리 정책 ADR**: occurred_at < 현재 주기 시작 시점인 이벤트가 도착하면 어떻게? (다음 주기 / 거절 / 강제 차감). `subscription-billing-flows.md` §5와 동일 함정.
- **`tenant_id` 일찍 결정한다**: `multi-tenancy.md` 결합 — 잔액은 tenant 단위가 보통.

---

## 3. 사용량 트래킹 — Idempotent UsageRecord (의사코드)

LLM 호출은 네트워크 실패/재시도가 흔하다. 같은 호출이 두 번 차감되면 사용자 신뢰 즉사.

```python
# 사용 시점에 호출. 동기 차감 또는 큐 위임 모두 idempotency 동일 적용.
def record_usage(
    account_id: str,
    meter: str,                         # "llm_tokens"
    quantity: int,                      # 12500
    request_id: str,                    # 상위 요청 ID — idempotency 기반
    model: str,                         # "claude-opus-5-5"
    metadata: dict,
):
    idem_key = f"usage:{request_id}:{meter}"  # 한 요청 = 한 차감

    with db.transaction():
        # 1. UsageEvent 중복 차단 (UNIQUE 제약 + INSERT ... ON CONFLICT DO NOTHING)
        event = UsageEvent.insert_or_get(
            idempotency_key=idem_key,
            account_id=account_id,
            meter=meter, quantity=quantity,
            occurred_at=now(), recorded_at=now(),
            metadata={"model": model, **metadata},
            status="pending",
        )
        if event.status != "pending":
            return event                # 이미 처리됨, 즉시 반환

        # 2. PriceBook에서 그 시점 단가 snapshot (소급 변경 X)
        price = PriceBook.lookup(meter=meter, model=model, at=event.occurred_at)
        cost = round_currency(quantity * price.unit_amount / price.unit, price.currency)
        event.unit_cost = price.unit_amount
        event.status = "priced"

        # 3. Free tier 우선 차감 → 부족분만 유료 잔액 차감
        free_used = min(quantity, account.free_tier_remaining)
        paid_units = quantity - free_used
        paid_cost = round_currency(paid_units * price.unit_amount / price.unit, price.currency)

        if paid_cost > account.balance_available:
            event.status = "voided"
            raise InsufficientBalance(account_id, paid_cost, account.balance_available)

        # 4. Ledger에 immutable entry 2개 (free_tier_grant 차감 + paid debit)
        if free_used > 0:
            Ledger.append(account_id, type="free_tier_grant", amount=0,  # 금액 0, 카운터만
                          metadata={"free_units_consumed": free_used},
                          idempotency_key=f"ft:{idem_key}")
            account.free_tier_remaining -= free_used

        Ledger.append(account_id, type="debit", amount=-paid_cost,
                      source_event_id=event.id,
                      idempotency_key=f"debit:{idem_key}",
                      metadata={"meter": meter, "quantity": paid_units, "unit_cost": price.unit_amount})

        # 5. 캐시 잔액 업데이트 + 차후 reconcile 잡으로 검증
        account.balance_available -= paid_cost
        event.status = "debited"

    # 6. Threshold 평가 (트랜잭션 밖 — 알림 실패가 차감 롤백시키지 않게)
    evaluate_thresholds(account_id)
    return event
```

**핵심 포인트**:
- `idem_key`는 **상위 request_id 기반**. retry는 같은 키, 새 요청은 다른 키.
- `INSERT ... ON CONFLICT DO NOTHING` 또는 `SELECT ... FOR UPDATE` 패턴으로 race 차단.
- `PriceBook.lookup(at=event.occurred_at)`은 **그 시점 가격 고정** — provider가 다음 날 가격 인하해도 어제 호출은 어제 가격.
- 잔액 부족 시 `voided`로 표시. 이미 호출된 LLM 응답은 사용자에게 어떻게 처리할지 비즈니스 결정 (환불/할인 표시/그냥 보여주기).
- 알림은 트랜잭션 밖 — 알림 실패로 차감이 롤백되면 안 됨 (`audit-log.md` outbox 패턴 권장).

### Reservation 패턴 (선택)

긴 작업 (예: 1분짜리 video gen)은 시작 시 예상 비용 reserve → 완료 시 실제 차감 + 잔여분 release.

```
estimate(request) → estimated_cost
reserve(account, estimated_cost) → reservation_id   # balance_reserved 증가
... 작업 진행 ...
on_completion(actual_cost):
  debit(account, actual_cost, idempotency_key=f"res:{reservation_id}")
  release(reservation_id)                            # balance_reserved 감소
on_failure:
  release(reservation_id)                            # 차감 없이 풀어줌
```

→ 짧은 호출(LLM completion 수 초)은 reservation 생략, 폭주 worker만 적용.

---

## 4. 한도 관리 — Threshold + Auto-refill (의사코드)

청구 폭탄 vs 운영 중단의 균형. **Hard cap + 명시적 opt-in soft overage**가 표준.

```python
# Threshold 평가 — 차감 직후 또는 주기적 (5분 간격) 호출
def evaluate_thresholds(account_id: str):
    account = CreditAccount.get(account_id)
    balance = account.balance_available

    # 1. Low balance 알림 (예: 잔액 < $10)
    if balance < account.low_balance_threshold:
        if not already_notified_today(account_id, "low_balance"):
            notify(account, "low_balance", balance=balance)  # notification-multichannel
            mark_notified(account_id, "low_balance")

    # 2. Auto-refill (idempotency_key로 동시 충전 차단)
    if account.auto_refill_enabled and balance < account.auto_refill_trigger:
        refill_key = f"autorefill:{account_id}:{date_hour()}"  # 시간당 1회
        if redis.set(refill_key, "1", nx=True, ex=3600):
            charge_payment_method(account, account.auto_refill_amount)  # PG 결제
            # 결제 webhook → Ledger에 topup entry → balance 증가

    # 3. Hard cap 도달 (월간 spend_limit)
    monthly_spent = sum_debits(account_id, since=start_of_month())
    if monthly_spent >= account.spend_limit_monthly:
        account.status = "frozen"
        notify(account, "spend_limit_reached")
        # 이후 record_usage()에서 InsufficientBalance 또는 SpendLimitExceeded 발생
```

**원칙**:
- **알림 dedup**: 같은 임계치 알림을 일/주 단위로 1회만 (피로도 방지).
- **Auto-refill idempotency**: `autorefill:{account}:{시간단위}` 키로 동시 충전/중복 충전 차단.
- **Hard cap은 hard**: spend_limit 도달 시 frozen — 비즈니스 critical이라도 차단. 풀려면 사용자 명시적 액션. (수동 해제 후 도메인 액션 다시 가능).
- **Soft overage**는 별도 ADR: spend_limit + 명시적 opt-in (`overage_allowed=true`). UI에 "초과 사용 시 자동 청구" 약관 동의 필수.
- **Webhook delay 고려**: PG 충전 결제 → webhook → Ledger topup 사이 갭. UX는 "충전 진행 중" 상태 명시 + 일시 사용 가능 옵션 ADR.

→ rate limit과 차이: rate-limiting은 **RPS 한도** (초당 요청), credit cap은 **누적 비용 한도**. 둘 다 필요하면 결합 (`business/rate-limiting.md`).

---

## 5. 가격 책정 — LLM Provider 원가 + 마진

LLM 사용량 가격 = **provider 원가 + 마진(markup)**. provider 가격이 빠르게 변하므로 시간축 분리 필수.

| 항목 | 자체 결정 | 함정 |
|---|---|---|
| **Cost basis (provider 원가)** | OpenAI/Anthropic/Google 공시 단가 + cache hit 할인 + batch API 할인 | input/output 단가 다름. cache hit ratio가 평균 원가 좌우. |
| **Markup %** | 보통 30~200% (prompt 가공 + 인프라 + 마진) | 너무 낮으면 운영 적자, 너무 높으면 사용자가 직접 OpenAI 가입 |
| **표시 단위** | 사용자 친화 단위 ("크레딧" / "토큰") | provider raw 토큰을 그대로 노출하면 모델 변경 시 사용자 혼란 |
| **모델별 가격** | Opus = Sonnet × 2, Haiku = Sonnet ÷ 20 등 비례 (Claude 5.5 공시가, 2026-11 기준) | 모델 라우팅(downgrade) 시 사용자 경험 통일 |
| **Cache hit 처리** | 할인 (예: Opus·Sonnet 5.5 95%, Haiku 5.5 90% 절감) 사용자에게 일부 환급 / 자체 마진 흡수 | 회계 분리 (cost_basis 기록) 필수 |
| **Batch API 할인** | 50% 할인 (Anthropic/OpenAI batch). 사용자가 비동기 동의 시 적용 | UX: 동기/배치 옵션 명시 |

### Multi-currency / 통화별 토큰 가격 ADR

`subscription-billing-flows.md` §4 Multi-currency 패턴 재사용:

| 패턴 | 권장 | 이유 |
|---|---|---|
| **통화별 PriceBook 분리** | ✅ 권장 | USD/KRW/EUR 별 unit_amount. 환율 자동 변환 X |
| **단일 USD base + 결제 시 FX** | ⚠️ 비추 | 환율 변동으로 잔액 차감액이 매일 다름, 사용자 혼란 |
| **CreditAccount currency lock** | ✅ 필수 | 첫 충전 시 통화 고정. 변경 = 새 account |
| **반올림 정책** | ✅ 필수 | KRW=정수, USD=4 decimal(소액 차감) — provider raw 단가가 $0.000015/token 단위라 이슈 |
| **provider 원가 USD → 사용자 KRW 가격** | 분기 환율 + 마진으로 고정 | 매월 재산정 X (사용자 가격 안정성) |

```markdown
## 통화/단가 ADR

| 항목 | 결정 | 근거 |
|---|---|---|
| 사용자 표시 단위 | 크레딧 (1 credit = $0.001 또는 ₩1) | 모델 변경 시 사용자 가격 안정 |
| 통화 | USD primary + KRW (한국 customer) | 한국은 카드 외화 결제 거부감 |
| Markup | input 50%, output 80%, cache hit 30% | 평균 cost ratio 기반 |
| 환율 갱신 | 분기 1회 수동 + 변동 5% 초과 시 임시 갱신 | 회계 안정성 |
| 모델 라우팅 시 가격 | 라우팅된 실제 모델 단가 적용 | 사용자에게 명시 (logs) |
```

---

## 6. Free Tier — 차감 정책

| 패턴 | 적합 | 함정 |
|---|---|---|
| **월간 reset (예: 매월 1일 100만 토큰 grant)** | B2C 표준 | 월말 무료 폭주 → 인프라 부담 |
| **Rolling 30일** | 신규 사용자 균등 | 회계 복잡 |
| **계정당 1회 (전 평생)** | 트라이얼 대용 | 어뷰즈 (멀티계정), 가입 매력 ↓ |
| **Subscription 포함분** | Hybrid 모델 (월 $20에 100만 토큰 포함) | 잔여 carry-over 정책 ADR |

**핵심**:
- 차감 우선순위: **free_tier → prepaid balance → overage(있으면)**
- Free tier 잔량은 별도 카운터 (`free_tier_remaining`). 매월 reset cron + audit-log.
- `subscription-billing-flows.md` §6 Trial 어뷰즈 방지 패턴 그대로 적용 (도메인/카드 fingerprint/rate-limit).

---

## 7. Refund / 조정 (immutable ledger 준수)

```
실패한 LLM 호출 (provider error, timeout)
  ▼
원본 debit entry 식별
  ▼
Ledger에 type=refund (양수 amount) entry 추가
  ▼
audit-log + 사용자 알림
```

**원칙**:
- **원본 entry 수정 금지** — 보상 entry 추가만 허용 (이중부기).
- **부분 환불**: 응답 일부만 받았다면 quantity 재산정 → 부분 refund.
- **자동 환불 룰** ADR 필수: provider 5xx → 자동 100% / 4xx → 자동 0% / timeout → 50% 등.
- **회계 시스템 매핑**: refund entry는 deferred revenue 감소. 충전된 적 없는 free_tier는 refund 대상 X.

---

## 8. 한국 시장 깊이 (충전식 캐시 모델)

한국 사용자는 "충전식 캐시" 멘탈 모델 친숙 (네이버페이 포인트, 카카오 캐시).

| 항목 | 한국 특수성 |
|---|---|
| **충전 PG** | PortOne / Toss로 일회성 결제 (subscription 빌링키와 별도) |
| **부가세** | 충전 시점에 10% 부가세 별도 표시 + 세금계산서 발급 (B2B). B2C는 카드 영수증. |
| **환불 정책** | **전자상거래법**: 미사용 잔액 환불 의무 (수수료 차감 가능). 정책 명시 필수. |
| **사용 기한** | 충전금 사용 기한 두는 게 일반적 (예: 1년). 만료 정책 ADR + 알림 필수. |
| **이용약관** | "충전금은 환불 불가" 조항 무효 가능성 (소비자 보호). 변호사 검토 필수. |
| **회계 처리** | 충전 시점 = deferred revenue (부채), 사용 시점 = 매출 인식. 한국 K-IFRS와 매핑. |
| **결제 수단** | 카드/계좌이체/간편결제 (네이버페이/카카오페이/페이코). 가상계좌(무통장 입금)는 B2B 흔함. |
| **현금영수증** | 10만 원 미만 자동 / 이상은 의무 발행 (B2C). PG가 처리하지 않으면 자체 처리. |

**한국 LLM 시장 함정**:
- **국내 LLM provider** (네이버 HyperCLOVA, 카카오 KoGPT, KT Mi:dm 등) 등장. multi-provider 추상화 (`ai/` 카테고리) 필요.
- **데이터 주권**: B2B 엔터프라이즈는 "데이터 국외 반출 금지" 요구 — 한국 리전/한국 LLM 라우팅 별도 ADR.
- **세금계산서 자동 발행**: Bill36524 / 더존 / 자체 ERP 연동. 충전 마다 발행 (월간 합산 X) — 한국 회계 관행.

→ 한국 단일 시장이면 이 § 그대로. 글로벌+한국 듀얼이면 currency lock + 부가세 자동화(`subscription-billing-flows.md` §4) 결합.

---

## 9. 보안 / 안티패턴

- ❌ **클라이언트가 사용량 self-report**: 위변조 즉시. 항상 서버 측 record (LLM proxy/gateway에서).
- ❌ **잔액을 클라이언트에서 캐시**: 차감 race로 사용자가 음수 잔액으로 호출.
- ❌ **balance를 SELECT FOR UPDATE 없이 차감**: race로 이중 차감 / 음수 잔액. 트랜잭션 + 잠금 또는 atomic decrement (Redis) 필수.
- ❌ **PriceBook 변경 시 기존 UsageEvent 소급 재계산**: 사용자 신뢰 파괴. 그 시점 단가 snapshot 고정 원칙.
- ❌ **알림 실패가 차감 롤백시키게**: outbox 패턴 (`audit-log.md`)으로 분리.
- ❌ **Hard cap 없이 PG에 자동 청구**: 청구 폭탄 사고. spend_limit 기본값 + soft overage opt-in.
- ❌ **무료 tier도 PG customer 안 만듦**: subscription-billing 동일 함정. 가입 시점에 customer + free CreditAccount 생성.
- ✅ **모든 debit/topup/refund에 idempotency_key**: UNIQUE 제약 강제.
- ✅ **Reconciliation job**: ledger sum vs cached balance, provider 원가 vs 자체 cost_basis 일일 검증.
- ✅ **provider rate limit 자체 sub-limit**: provider quota 도달 전 자체 차단 (사용자에게 명확한 메시지).

### 안티패턴 모음

| 안티패턴 | 왜 위험 | 올바른 방법 |
|---|---|---|
| balance를 정수 컬럼 1개로 관리 | reconciliation 불가, 감사 불가 | append-only ledger + 캐시된 balance |
| free_tier를 balance에 직접 입금 | 환불/회계 분리 안 됨 | 별도 카운터 또는 separate ledger entry |
| usage_record 즉시 PG report | spike 시 PG rate limit | 배치/aggregator (Stripe Meters는 1초 1k+ 처리) |
| late event를 무조건 차감 | 마감된 주기 정합성 파괴 | 정책 ADR (다음 주기 / void / 특정 기간만 허용) |
| 환불을 원본 entry update로 처리 | 감사 추적 불가, 회계 위반 | 양수 amount의 refund entry append |
| spend_limit 기본 OFF | 청구 폭탄 사고 | 기본 ON + soft overage opt-in |
| 모델별 가격 매핑 누락 | 모델 라우팅 시 원가 폭증 | 모델별 PriceBook + 라우팅 시 단가 검증 |

---

## 10. ADR 템플릿 — Credit System

```markdown
## Credit System ADR

| 항목 | 결정 | 대안 | 근거 |
|---|---|---|---|
| 모델 | Hybrid (월 seat $20 + per-token credit) | Pure prepaid / Pure metered | AI 제품 표준 |
| Credit 단위 | 1 credit = $0.001 (USD 표시) | raw token / 자체 단위 | 모델 라우팅 시 사용자 가격 안정 |
| Free tier | 월 100만 토큰 (매월 1일 reset, carry-over X) | rolling / lifetime | 어뷰즈 방지 + 마케팅 |
| Hard cap | 기본 $50/월, 사용자 변경 가능 | 무제한 / 고정 | 청구 폭탄 회피 |
| Soft overage | 사용자 명시적 opt-in | 기본 ON / 영구 OFF | 신뢰 + 매출 |
| Auto-refill | 잔액 < $5 시 $20 충전 (시간당 1회 한도) | 수동 / 무한 자동 | 운영 중단 회피 |
| Late event 정책 | occurred_at < 3일 전 = void, audit 기록 | 다음 주기 / 강제 차감 | reconciliation 단순 |
| Refund 정책 | provider 5xx = 자동 100% refund, 4xx = 0% | 모두 수동 / 모두 자동 | 운영 부담 균형 |
| Markup % | input 50%, output 80%, cache hit 30% | 단일 markup | provider 원가 구조 반영 |
| 환율 갱신 | 분기 1회 + 변동 5% 초과 시 임시 | 실시간 / 연 1회 | 회계 안정성 |
| Provider | 1차: Anthropic, 2차: OpenAI fallback | 단일 provider | 가용성 + 비용 |
| 한국 부가세 | 충전 시점 10% 별도, 세금계산서 자동 (B2B) | 사용 시점 / 수동 | 한국 관행 + 자동화 |
```

→ `agents/tech-lead` + `agents/cost-analyzer` 협업으로 ADR 작성.

---

## 11. Quick Start Checklist (신규 AI 제품)

- [ ] 모델 결정 (Hybrid/Prepaid/Postpaid) → ADR
- [ ] CreditAccount + Ledger + UsageEvent + PriceBook 4개 도메인 모델 구축 (immutable ledger)
- [ ] LLM gateway/proxy에서 record_usage 호출 (클라이언트 self-report 금지)
- [ ] idempotency_key 패턴: `usage:{request_id}:{meter}`, `debit:{...}`, `autorefill:{...}`
- [ ] PriceBook + cost_basis (provider 원가) + markup 분리
- [ ] Free tier 별도 카운터 + 매월 reset cron
- [ ] Hard cap 기본 ON + UI에서 사용자 조정 가능
- [ ] Soft overage opt-in 흐름 (약관 동의 + 명시적 액션)
- [ ] Auto-refill + low balance threshold 알림 (`notification-multichannel.md`)
- [ ] Reconciliation job: ledger sum vs cached balance, provider 원가 vs cost_basis 일일
- [ ] `audit-log` 통합: topup/debit/refund/threshold 모든 이벤트
- [ ] Hybrid 시 `subscription-billing.md` seat 모델 결합 (월 seat → CreditAccount free tier grant)
- [ ] 한국 시장: 부가세 + 세금계산서 + 환불 정책 ADR
- [ ] Stripe Meters 또는 자체 ledger 결정 → CreditGateway 어댑터
- [ ] 모니터링: 잔액 분포, MRR contribution from credit, provider 원가 추적

---

## 12. 관련 자원

**같은 카테고리 (subscription-billing 시리즈와 짝)**:
- `business/subscription-billing.md` — 정기 빌링 hub (seat 모델 결합 시)
- `business/subscription-billing-flows.md` §5 — Metered Billing 패턴 (이 skill의 부모 섹션)
- `business/subscription-billing-metrics.md` — MRR/Cohort SQL → usage MAU/ARPU/LTV로 확장

**우리 시스템 내부 (cross-link)**:
- `business/payment-integration.md` — 충전 일회성 결제, webhook idempotency 원칙
- `business/multi-tenancy.md` — tenant 단위 CreditAccount, seat × usage 결합
- `business/rate-limiting.md` — RPS hard cap (credit hard cap과 결합)
- `business/notification-multichannel.md` — low balance / cap / refund 알림
- `business/audit-log.md` — outbox 패턴, 잔액 변경 감사
- `business/feature-flags.md` — credit 기능 점진 롤아웃, kill-switch
- `business/admin-api-keys.md` — usage report endpoint scope
- `skills/ai/prompt-engineering.md` — 토큰 효율화 (원가 절감)
- `skills/ai/rag-patterns.md` — context 절약, cache hit 최대화
- `skills/observability/observability-cost.md` — provider 원가 추적, cardinality 주의 (account_id 라벨 회피)
- `skills/messaging/redis-streams.md` / `kafka-*` — usage event 큐
- `agents/tech-lead` — 가격 모델 ADR
- `/infra:postgresql-operations` — ledger 파티셔닝/아카이빙
- `agents/cost-analyzer` — provider 원가 추적 + markup 분석
- `/infra:redis-operations` — atomic decrement, 잔액 캐시
- `rules/core/security.md`, `rules/process/documentation.md` — ADR/회계 문서

**외부 표준 / 도구**:
- Stripe Meters + Events (2025+) — postpaid usage billing
- Lago / Killbill / Orb — open-source / 전용 metered billing
- Anthropic Console / OpenAI Platform — prepaid credit 표준 UX 참고
- ChartMogul / Sigma — usage metric 분석 (subscription metric과 결합)
- Bill36524 / 더존 — 한국 세금계산서

---

## 13. 다음 단계 (이 skill 적용 후)

1. **정기 빌링 결합 (Hybrid)** → `subscription-billing.md` (seat 모델 + Stripe Meters 합산 invoice)
2. **메트릭 확장** → `subscription-billing-metrics.md` 패턴으로 MAU/ARPU/usage retention SQL 작성
3. **AI 비용 최적화** → `ai/prompt-engineering.md`, `ai/rag-patterns.md` (cache hit 최대화로 원가 절감)
4. **장애 시 보상** → `/architecture:msa-saga` (LLM 실패 → 자동 refund saga)
5. **엔터프라이즈 인보이스** → 충전식 → postpaid commitment + 월말 인보이스 (sales-led ADR)

---
name: fintech-engineer
description: Financial technology engineering expertise for building secure, compliant payment and banking systems. Use when implementing payment processing, designing.
---

# Fintech Engineer

Structured guidance for building financial technology systems that are correct, auditable, and compliant. Covers double-entry accounting, payment processing, money handling, regulatory compliance, fraud detection, financial API design, and testing strategies specific to financial software.

## When to Use This Skill

Use this skill for:

- Designing or implementing a double-entry ledger or accounting system
- Building payment processing flows with Stripe, Adyen, or other gateways
- Handling money and multi-currency arithmetic without floating-point errors
- Implementing KYC/AML data flows or transaction monitoring
- Building fraud detection pipelines (rule-based or ML-assisted)
- Designing idempotent financial APIs or trading system endpoints
- Writing tests that verify accounting invariants, reconciliation, or regulatory scenarios
- Ensuring PCI-DSS scope minimization in application architecture

**Trigger phrases**: "ledger", "double-entry", "payment processing", "PCI-DSS", "KYC", "AML", "fraud detection", "money handling", "currency conversion", "reconciliation", "trading platform", "FIX protocol", "idempotency key", "payment gateway", "journal entry", "chart of accounts"

## What This Skill Does

Provides fintech engineering patterns including:

- **Ledger Design**: Double-entry bookkeeping, chart of accounts, journal entries, immutable audit trails
- **Payment Processing**: State machines, gateway integration, webhook handling, retry logic, reconciliation
- **Money Handling**: Decimal precision, ISO 4217 currency codes, exchange rates, rounding rules
- **Regulatory Compliance**: KYC/AML pipelines, transaction monitoring, audit logging, data retention
- **Fraud Detection**: Velocity checks, anomaly scoring, rule engines, feature engineering
- **Financial APIs**: Idempotent endpoints, optimistic locking, rate limiting, market data feeds
- **Testing**: Property-based tests for accounting invariants, chaos testing for payments, load testing for trading

## Instructions

### Step 1: Double-Entry Ledger Design

A double-entry ledger is the foundation of every financial system. Every transaction records equal debits and credits, ensuring the accounting equation (Assets = Liabilities + Equity) always holds.

**Account Types and Normal Balances**:

| Account Type | Normal Balance | Debit Effect | Credit Effect | Examples |
|-------------|---------------|-------------|--------------|---------|
| Asset | Debit | Increase | Decrease | Cash, Receivables, User Wallets |
| Liability | Credit | Decrease | Increase | Payables, User Deposits, Loans |
| Equity | Credit | Decrease | Increase | Retained Earnings, Capital |
| Revenue | Credit | Decrease | Increase | Transaction Fees, Interest Income |
| Expense | Debit | Increase | Decrease | Processing Fees, Refunds |

**PostgreSQL Schema for a General Ledger**:

```sql
-- Chart of accounts: defines all account types in the system
CREATE TABLE accounts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code            VARCHAR(20) UNIQUE NOT NULL,       -- e.g., "1001" for cash
    name            VARCHAR(255) NOT NULL,
    account_type    VARCHAR(20) NOT NULL CHECK (
        account_type IN ('asset', 'liability', 'equity', 'revenue', 'expense')
    ),
    currency        CHAR(3) NOT NULL DEFAULT 'USD',    -- ISO 4217
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata        JSONB DEFAULT '{}'
);

-- Journal entries: the atomic unit of accounting
CREATE TABLE journal_entries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idempotency_key VARCHAR(255) UNIQUE NOT NULL,      -- prevents duplicate postings
    description     TEXT NOT NULL,
    posted_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by      VARCHAR(255) NOT NULL,
    metadata        JSONB DEFAULT '{}',                 -- source system, reference IDs
    -- Journal entries are immutable: no UPDATE or DELETE allowed
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Line items: individual debit/credit entries within a journal entry
CREATE TABLE journal_lines (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journal_entry_id UUID NOT NULL REFERENCES journal_entries(id),
    account_id      UUID NOT NULL REFERENCES accounts(id),
    amount          NUMERIC(19, 4) NOT NULL CHECK (amount > 0),
    entry_type      VARCHAR(6) NOT NULL CHECK (entry_type IN ('debit', 'credit')),
    currency        CHAR(3) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enforce double-entry invariant: debits must equal credits per journal entry
CREATE OR REPLACE FUNCTION check_balanced_entry()
RETURNS TRIGGER AS $$
DECLARE
    debit_sum  NUMERIC(19, 4);
    credit_sum NUMERIC(19, 4);
BEGIN
    SELECT
        COALESCE(SUM(CASE WHEN entry_type = 'debit'  THEN amount END), 0),
        COALESCE(SUM(CASE WHEN entry_type = 'credit' THEN amount END), 0)
    INTO debit_sum, credit_sum
    FROM journal_lines
    WHERE journal_entry_id = NEW.journal_entry_id;

    IF debit_sum <> credit_sum THEN
        RAISE EXCEPTION 'Unbalanced journal entry: debits=% credits=%',
            debit_sum, credit_sum;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Balance computation: derive account balances from journal lines
CREATE VIEW account_balances AS
SELECT
    a.id AS account_id,
    a.code,
    a.name,
    a.account_type,
    a.currency,
    SUM(CASE WHEN jl.entry_type = 'debit'  THEN jl.amount ELSE 0 END) AS total_debits,
    SUM(CASE WHEN jl.entry_type = 'credit' THEN jl.amount ELSE 0 END) AS total_credits,
    CASE
        WHEN a.account_type IN ('asset', 'expense')
            THEN SUM(CASE WHEN jl.entry_type = 'debit' THEN jl.amount ELSE -jl.amount END)
        ELSE
            SUM(CASE WHEN jl.entry_type = 'credit' THEN jl.amount ELSE -jl.amount END)
    END AS balance
FROM accounts a
LEFT JOIN journal_lines jl ON jl.account_id = a.id
GROUP BY a.id, a.code, a.name, a.account_type, a.currency;

-- Index for fast balance queries and idempotency lookups
CREATE INDEX idx_journal_lines_account ON journal_lines(account_id, created_at);
CREATE INDEX idx_journal_entries_idempotency ON journal_entries(idempotency_key);
```

**Idempotent Journal Entry Creation** (Python):

```python
from decimal import Decimal
from uuid import uuid4
import psycopg

def post_journal_entry(
    conn: psycopg.Connection,
    idempotency_key: str,
    description: str,
    lines: list[dict],
    created_by: str,
) -> str:
    """Post a balanced journal entry with idempotency protection.

    Each line: {"account_id": str, "amount": Decimal, "entry_type": "debit"|"credit", "currency": str}
    """
    # Validate balance before hitting the database
    debits = sum(l["amount"] for l in lines if l["entry_type"] == "debit")
    credits = sum(l["amount"] for l in lines if l["entry_type"] == "credit")
    if debits != credits:
        raise ValueError(f"Unbalanced entry: debits={debits} credits={credits}")

    with conn.transaction():
        # Idempotency: return existing entry if key already used
        row = conn.execute(
            "SELECT id FROM journal_entries WHERE idempotency_key = %s",
            (idempotency_key,),
        ).fetchone()
        if row:
            return row[0]

        entry_id = str(uuid4())
        conn.execute(
            "INSERT INTO journal_entries (id, idempotency_key, description, created_by) "
            "VALUES (%s, %s, %s, %s)",
            (entry_id, idempotency_key, description, created_by),
        )
        for line in lines:
            conn.execute(
                "INSERT INTO journal_lines (journal_entry_id, account_id, amount, entry_type, currency) "
                "VALUES (%s, %s, %s, %s, %s)",
                (entry_id, line["account_id"], line["amount"],
                 line["entry_type"], line["currency"]),
            )
        return entry_id
```

**Key Ledger Design Principles**:

- Journal entries are append-only. Never update or delete a posted entry. To correct an error, post a reversing entry
- Every journal entry must balance (total debits = total credits) within the same currency
- Use idempotency keys on every write path to prevent duplicate postings from retries
- Store amounts as `NUMERIC(19, 4)` in PostgreSQL, never as `FLOAT` or `DOUBLE PRECISION`
- Derive balances by aggregating journal lines, not by storing a mutable balance field
- Include metadata (source system, external reference IDs) on every entry for auditability

### Step 2: Payment Processing

Payment flows require careful state management, idempotent operations, and reconciliation against external gateways.

**Payment State Machine**:

```
                    ┌──────────┐
                    │ created  │
                    └────┬─────┘
                         │ authorize()
                    ┌────▼─────┐
              ┌─────│ pending  │─────┐
              │     └────┬─────┘     │
    timeout() │          │ confirm() │ fail()
              │     ┌────▼─────┐     │
              │     │ authorized│    │
              │     └────┬─────┘     │
              │          │ capture() │
              │     ┌────▼─────┐     │
              │     │ captured │     │
              │     └────┬─────┘     │
              │          │           │
              │   refund()│          │
              │     ┌────▼─────┐     │
              │     │ refunded │     │
              │     └──────────┘     │
              │                      │
              │  ┌──────────┐        │
              └──► expired  │        │
                 └──────────┘        │
                 ┌──────────┐        │
                 │  failed  │◄───────┘
                 └──────────┘
```

**Payment State Machine Implementation** (Python):

```python
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

class PaymentStatus(Enum):
    CREATED = "created"
    PENDING = "pending"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    REFUNDED = "refunded"
    EXPIRED = "expired"
    FAILED = "failed"

VALID_TRANSITIONS: dict[PaymentStatus, set[PaymentStatus]] = {
    PaymentStatus.CREATED:    {PaymentStatus.PENDING, PaymentStatus.EXPIRED},
    PaymentStatus.PENDING:    {PaymentStatus.AUTHORIZED, PaymentStatus.FAILED, PaymentStatus.EXPIRED},
    PaymentStatus.AUTHORIZED: {PaymentStatus.CAPTURED, PaymentStatus.EXPIRED},
    PaymentStatus.CAPTURED:   {PaymentStatus.REFUNDED},
    PaymentStatus.REFUNDED:   set(),
    PaymentStatus.EXPIRED:    set(),
    PaymentStatus.FAILED:     set(),
}

@dataclass
class Payment:
    id: str
    amount: Decimal
    currency: str
    status: PaymentStatus = PaymentStatus.CREATED
    gateway_id: str | None = None
    idempotency_key: str | None = None
    events: list[dict] = field(default_factory=list)

    def transition_to(self, new_status: PaymentStatus, reason: str = "") -> None:
        if new_status not in VALID_TRANSITIONS[self.status]:
            raise ValueError(
                f"Invalid transition: {self.status.value} -> {new_status.value}"
            )
        old_status = self.status
        self.status = new_status
        self.events.append({
            "from": old_status.value,
            "to": new_status.value,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
```

**Stripe Webhook Handler with Idempotent Processing**:

```python
import hmac
import hashlib
import json
from typing import Any

def verify_stripe_signature(payload: bytes, sig_header: str, secret: str) -> bool:
    """Verify Stripe webhook signature to prevent spoofed events."""
    parts = dict(pair.split("=", 1) for pair in sig_header.split(","))
    timestamp = parts["t"]
    expected_sig = parts["v1"]
    signed_payload = f"{timestamp}.".encode() + payload
    computed = hmac.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, expected_sig)

async def handle_stripe_webhook(
    event: dict[str, Any],
    payment_repo: "PaymentRepository",
    ledger: "LedgerService",
    processed_events: "IdempotencyStore",
) -> None:
    """Process a Stripe webhook event idempotently."""
    event_id = event["id"]

    # Idempotency: skip already-processed events
    if await processed_events.exists(event_id):
        return

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "payment_intent.succeeded":
        payment = await payment_repo.find_by_gateway_id(data["id"])
        if payment and payment.status == PaymentStatus.AUTHORIZED:
            payment.transition_to(PaymentStatus.CAPTURED, reason="stripe_webhook")
            await payment_repo.save(payment)
            # Post ledger entries: debit cash, credit receivable
            await ledger.post_payment_capture(payment)

    elif event_type == "payment_intent.payment_failed":
        payment = await payment_repo.find_by_gateway_id(data["id"])
        if payment and payment.status in (PaymentStatus.PENDING, PaymentStatus.AUTHORIZED):
            payment.transition_to(PaymentStatus.FAILED, reason=data.get("last_payment_error", {}).get("message", "unknown"))
            await payment_repo.save(payment)

    # Mark event as processed after successful handling
    await processed_events.store(event_id)
```

**Reconciliation Pattern**:

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class ReconciliationResult:
    matched: list[str]
    missing_in_gateway: list[str]    # in our ledger but not in gateway
    missing_in_ledger: list[str]     # in gateway but not in our ledger
    amount_mismatches: list[dict]

def reconcile_payments(
    internal_records: dict[str, Decimal],
    gateway_records: dict[str, Decimal],
) -> ReconciliationResult:
    """Compare internal ledger records against payment gateway records.

    Keys are payment/transaction IDs; values are amounts.
    """
    matched = []
    amount_mismatches = []

    all_ids = set(internal_records.keys()) | set(gateway_records.keys())
    missing_in_gateway = []
    missing_in_ledger = []

    for txn_id in all_ids:
        internal = internal_records.get(txn_id)
        gateway = gateway_records.get(txn_id)

        if internal is None:
            missing_in_ledger.append(txn_id)
        elif gateway is None:
            missing_in_gateway.append(txn_id)
        elif internal == gateway:
            matched.append(txn_id)
        else:
            amount_mismatches.append({
                "id": txn_id,
                "internal": internal,
                "gateway": gateway,
                "difference": internal - gateway,
            })

    return ReconciliationResult(
        matched=matched,
        missing_in_gateway=missing_in_gateway,
        missing_in_ledger=missing_in_ledger,
        amount_mismatches=amount_mismatches,
    )
```

**PCI-DSS Scope Minimization**: Never store raw card numbers in your systems. Use Stripe Elements, Adyen Drop-in, or similar client-side tokenization so that card data never touches your servers. This keeps your application out of PCI-DSS scope entirely (SAQ A or SAQ A-EP instead of SAQ D).

### Step 3: Money and Currency Handling

Floating-point arithmetic is fundamentally incompatible with financial calculations. A single rounding error can cascade through millions of transactions.

**The Decimal Rule**: Always represent money as integer minor units (cents, pence) or fixed-precision decimals. Never use `float` or `double`.

**Money Value Object** (Python):

```python
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN, InvalidOperation

# ISO 4217 currency metadata
CURRENCY_EXPONENTS: dict[str, int] = {
    "USD": 2, "EUR": 2, "GBP": 2, "JPY": 0, "BHD": 3,
    "KWD": 3, "CHF": 2, "CAD": 2, "AUD": 2, "CNY": 2,
}

@dataclass(frozen=True)
class Money:
    """Immutable value object for monetary amounts.

    Stores amount as Decimal with currency-appropriate precision.
    Uses banker's rounding (ROUND_HALF_EVEN) per ISO and financial standards.
    """
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if self.currency not in CURRENCY_EXPONENTS:
            raise ValueError(f"Unknown currency: {self.currency}")
        if not isinstance(self.amount, Decimal):
            raise TypeError("Amount must be a Decimal, not float")

    @classmethod
    def from_minor_units(cls, minor_units: int, currency: str) -> Money:
        """Create Money from integer minor units (e.g., cents)."""
        exp = CURRENCY_EXPONENTS[currency]
        amount = Decimal(minor_units) / Decimal(10 ** exp)
        return cls(amount=amount, currency=currency)

    @property
    def minor_units(self) -> int:
        """Convert to integer minor units for storage or gateway calls."""
        exp = CURRENCY_EXPONENTS[self.currency]
        return int(self.amount * Decimal(10 ** exp))

    def _check_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot operate on different currencies: {self.currency} vs {other.currency}"
            )

    def __add__(self, other: Money) -> Money:
        self._check_currency(other)
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: Money) -> Money:
        self._check_currency(other)
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def __mul__(self, factor: Decimal) -> Money:
        exp = CURRENCY_EXPONENTS[self.currency]
        result = (self.amount * factor).quantize(
            Decimal(10) ** -exp, rounding=ROUND_HALF_EVEN
        )
        return Money(amount=result, currency=self.currency)

    def allocate(self, ratios: list[int]) -> list[Money]:
        """Split money by ratios without losing or gaining a cent.

        Example: Money(Decimal("100.00"), "USD").allocate([1, 1, 1])
        returns three Money objects totaling exactly $100.00.
        """
        total_ratio = sum(ratios)
        exp = CURRENCY_EXPONENTS[self.currency]
        quantize_to = Decimal(10) ** -exp

        results = []
        remainder = self.amount
        for i, ratio in enumerate(ratios):
            if i == len(ratios) - 1:
                # Last share gets the remainder to avoid rounding loss
                results.append(Money(amount=remainder, currency=self.currency))
            else:
                share = (self.amount * Decimal(ratio) / Decimal(total_ratio)).quantize(
                    quantize_to, rounding=ROUND_HALF_EVEN
                )
                results.append(Money(amount=share, currency=self.currency))
                remainder -= share

        return results
```

**Exchange Rate Management**:

```python
from datetime import date
from decimal import Decimal

@dataclass
class ExchangeRate:
    base: str          # e.g., "USD"
    quote: str         # e.g., "EUR"
    rate: Decimal      # 1 base = rate quote
    effective_date: date
    source: str        # e.g., "ECB", "Bloomberg"

class ExchangeRateService:
    def __init__(self, rate_store: "RateStore") -> None:
        self._store = rate_store

    def convert(self, money: Money, target_currency: str, as_of: date | None = None) -> Money:
        """Convert money to target currency using the rate effective on the given date."""
        if money.currency == target_currency:
            return money
        rate = self._store.get_rate(money.currency, target_currency, as_of or date.today())
        if rate is None:
            raise ValueError(f"No rate found for {money.currency}/{target_currency}")
        converted = money.amount * rate.rate
        exp = CURRENCY_EXPONENTS[target_currency]
        rounded = converted.quantize(Decimal(10) ** -exp, rounding=ROUND_HALF_EVEN)
        return Money(amount=rounded, currency=target_currency)
```

**Critical Rules for Money**:

- Never use `float` or `double` for monetary amounts. Use `Decimal` (Python), `BigDecimal` (Java/Kotlin), or integer minor units
- Always specify the rounding mode explicitly. Banker's rounding (`ROUND_HALF_EVEN`) is the financial standard
- Never add or subtract amounts in different currencies without explicit conversion
- Store exchange rates with their effective date and source for audit purposes
- Use the `allocate` pattern (not division) when splitting money to avoid rounding leakage
- Store currency codes as ISO 4217 three-letter codes, not symbols or free-text

### Step 4: Regulatory Compliance in Code

Financial systems operate under strict regulatory frameworks. Compliance is not optional, and violations carry criminal penalties.

**KYC/AML Data Flow Architecture**:

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  Customer     │     │  KYC Service  │     │  Identity    │
│  Onboarding   │────>│  (Orchestrator)│────>│  Verification│
│  UI           │     │               │     │  Provider    │
└──────────────┘     └───────┬───────┘     └──────────────┘
                             │
                    ┌────────▼────────┐
                    │  Watchlist       │
                    │  Screening       │     Sanctions lists:
                    │  (OFAC, EU, UN) │     OFAC SDN, EU Consolidated,
                    └────────┬────────┘     UN Security Council
                             │
                    ┌────────▼────────┐
                    │  Risk Scoring    │     PEP databases,
                    │  Engine          │     adverse media
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Case Management │     Manual review
                    │  (Compliance     │     queue for
                    │   Officers)      │     edge cases
                    └─────────────────┘
```

**Transaction Monitoring Rules** (Python rule engine):

```python
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timedelta, timezone
from enum import Enum

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class TransactionAlert:
    rule_id: str
    severity: AlertSeverity
    transaction_id: str
    customer_id: str
    description: str
    triggered_at: datetime

class TransactionMonitor:
    """Rule-based transaction monitoring for AML compliance."""

    def __init__(self, transaction_store: "TransactionStore") -> None:
        self._store = transaction_store

    async def check_structuring(
        self, customer_id: str, amount: Decimal, window_hours: int = 24,
    ) -> TransactionAlert | None:
        """Detect structuring: multiple transactions just below reporting threshold.

        US BSA requires CTR filing for transactions over $10,000.
        Structuring is breaking up transactions to avoid this threshold.
        """
        threshold = Decimal("10000.00")
        structuring_floor = Decimal("8000.00")
        since = datetime.now(timezone.utc) - timedelta(hours=window_hours)

        recent = await self._store.get_transactions(customer_id, since=since)
        below_threshold = [t for t in recent if structuring_floor <= t.amount < threshold]

        if len(below_threshold) >= 3:
            total = sum(t.amount for t in below_threshold)
            return TransactionAlert(
                rule_id="AML-001-STRUCTURING",
                severity=AlertSeverity.HIGH,
                transaction_id=below_threshold[-1].id,
                customer_id=customer_id,
                description=(
                    f"{len(below_threshold)} transactions between "
                    f"${structuring_floor} and ${threshold} within {window_hours}h, "
                    f"totaling ${total}"
                ),
                triggered_at=datetime.now(timezone.utc),
            )
        return None

    async def check_velocity(
        self, customer_id: str, amount: Decimal, window_hours: int = 1,
    ) -> TransactionAlert | None:
        """Detect unusual transaction velocity (count per time window)."""
        since = datetime.now(timezone.utc) - timedelta(hours=window_hours)
        recent = await self._store.get_transactions(customer_id, since=since)

        # Thresholds should be configurable per customer risk tier
        if len(recent) > 10:
            return TransactionAlert(
                rule_id="AML-002-VELOCITY",
                severity=AlertSeverity.MEDIUM,
                transaction_id=recent[-1].id,
                customer_id=customer_id,
                description=f"{len(recent)} transactions in {window_hours}h exceeds velocity limit",
                triggered_at=datetime.now(timezone.utc),
            )
        return None
```

**Audit Logging Schema**:

```sql
-- Immutable audit log for all financially significant actions
CREATE TABLE audit_log (
    id              BIGSERIAL PRIMARY KEY,
    event_type      VARCHAR(100) NOT NULL,          -- e.g., "payment.captured"
    actor_id        VARCHAR(255) NOT NULL,          -- user or system identifier
    actor_type      VARCHAR(50) NOT NULL,           -- "user", "system", "api_key"
    resource_type   VARCHAR(100) NOT NULL,          -- "payment", "account", "transfer"
    resource_id     VARCHAR(255) NOT NULL,
    action          VARCHAR(50) NOT NULL,           -- "create", "update", "approve"
    changes         JSONB,                          -- before/after snapshot
    ip_address      INET,
    user_agent      TEXT,
    request_id      VARCHAR(255),                   -- correlation ID
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Append-only: revoke all UPDATE and DELETE permissions
REVOKE UPDATE, DELETE ON audit_log FROM app_user;

-- Indexes for compliance queries
CREATE INDEX idx_audit_actor ON audit_log(actor_id, created_at);
CREATE INDEX idx_audit_resource ON audit_log(resource_type, resource_id, created_at);
CREATE INDEX idx_audit_event_type ON audit_log(event_type, created_at);

-- Data retention: partition by month for efficient archival
CREATE TABLE audit_log_partitioned (
    LIKE audit_log INCLUDING ALL
) PARTITION BY RANGE (created_at);
```

**Compliance Checklist for Financial Applications**:

- Log every state change to financially significant entities with before/after snapshots
- Retain audit logs for the regulatory minimum (typically 5-7 years depending on jurisdiction)
- Implement geographic restrictions at the API gateway level (OFAC-sanctioned countries)
- Screen all customers and counterparties against sanctions lists at onboarding and periodically thereafter
- File Currency Transaction Reports (CTRs) for transactions exceeding $10,000 (US) or equivalent thresholds
- File Suspicious Activity Reports (SARs) when monitoring rules trigger and compliance review confirms suspicion
- Encrypt PII at rest and in transit; implement field-level encryption for sensitive KYC documents

### Step 5: Fraud Detection Patterns

Fraud detection in financial systems requires a layered approach combining real-time rules, velocity checks, and ML-based anomaly detection.

**Rule-Based Detection Engine**:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class FraudSignal:
    rule_name: str
    score: float          # 0.0 to 1.0
    reason: str

class FraudRule(ABC):
    @abstractmethod
    async def evaluate(self, transaction: "Transaction", context: "FraudContext") -> FraudSignal | None:
        ...

class HighAmountRule(FraudRule):
    """Flag transactions significantly above the customer's historical average."""

    async def evaluate(self, transaction: "Transaction", context: "FraudContext") -> FraudSignal | None:
        avg = await context.get_average_amount(transaction.customer_id, days=90)
        if avg and transaction.amount > avg * Decimal("5"):
            return FraudSignal(
                rule_name="high_amount",
                score=min(float(transaction.amount / avg) / 10, 1.0),
                reason=f"Amount ${transaction.amount} is {transaction.amount / avg:.1f}x the 90-day average",
            )
        return None

class GeoVelocityRule(FraudRule):
    """Flag transactions from geographically impossible locations."""

    async def evaluate(self, transaction: "Transaction", context: "FraudContext") -> FraudSignal | None:
        last_location = await context.get_last_transaction_location(transaction.customer_id)
        if last_location is None:
            return None
        distance_km = haversine(last_location, transaction.location)
        time_delta_hours = (transaction.timestamp - last_location.timestamp).total_seconds() / 3600
        if time_delta_hours > 0:
            speed_kmh = distance_km / time_delta_hours
            if speed_kmh > 1000:  # faster than commercial aircraft
                return FraudSignal(
                    rule_name="geo_velocity",
                    score=0.9,
                    reason=f"Impossible travel: {distance_km:.0f}km in {time_delta_hours:.1f}h ({speed_kmh:.0f} km/h)",
                )
        return None

class FraudEngine:
    """Evaluate all fraud rules and aggregate signals into a decision."""

    def __init__(self, rules: list[FraudRule], threshold: float = 0.7) -> None:
        self._rules = rules
        self._threshold = threshold

    async def evaluate(self, transaction: "Transaction", context: "FraudContext") -> tuple[bool, list[FraudSignal]]:
        signals = []
        for rule in self._rules:
            signal = await rule.evaluate(transaction, context)
            if signal:
                signals.append(signal)

        # Aggregate: use max score (or weighted average for more sophistication)
        max_score = max((s.score for s in signals), default=0.0)
        is_fraudulent = max_score >= self._threshold
        return is_fraudulent, signals
```

**Feature Engineering for ML Fraud Models**:

```python
from decimal import Decimal

async def compute_fraud_features(
    customer_id: str,
    transaction: "Transaction",
    store: "TransactionStore",
) -> dict[str, float]:
    """Compute features for an ML fraud detection model.

    Features are organized by time window and aggregation type.
    """
    features: dict[str, float] = {}

    for window_name, hours in [("1h", 1), ("24h", 24), ("7d", 168), ("30d", 720)]:
        recent = await store.get_transactions(customer_id, hours_back=hours)

        features[f"txn_count_{window_name}"] = len(recent)
        features[f"txn_total_{window_name}"] = float(sum(t.amount for t in recent))
        features[f"txn_avg_{window_name}"] = (
            float(sum(t.amount for t in recent) / len(recent)) if recent else 0.0
        )
        features[f"txn_max_{window_name}"] = float(max((t.amount for t in recent), default=0))
        features[f"unique_merchants_{window_name}"] = len({t.merchant_id for t in recent})
        features[f"unique_countries_{window_name}"] = len({t.country for t in recent})

    # Transaction-level features
    features["amount"] = float(transaction.amount)
    features["is_international"] = 1.0 if transaction.country != "US" else 0.0
    features["hour_of_day"] = transaction.timestamp.hour
    features["day_of_week"] = transaction.timestamp.weekday()

    return features
```

**False Positive Management**: Every fraud detection system produces false positives. Design your system with a review queue, customer friction budget (maximum number of challenges per time window), and feedback loops that retrain rules based on analyst decisions. Track precision, recall, and false positive rate as operational metrics.

### Step 6: Financial API Design

Financial APIs require stronger guarantees than typical web APIs: idempotency, optimistic locking, precise error semantics, and careful rate limiting.

**Idempotent API Pattern**:

```python
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from decimal import Decimal
import hashlib
import json

app = FastAPI()

class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: Decimal
    currency: str
    description: str

class TransferResponse(BaseModel):
    transfer_id: str
    status: str
    idempotency_key: str

@app.post("/v1/transfers", response_model=TransferResponse)
async def create_transfer(
    request: TransferRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    idempotency_store: "IdempotencyStore" = Depends(get_idempotency_store),
    transfer_service: "TransferService" = Depends(get_transfer_service),
) -> TransferResponse:
    """Create a transfer with idempotency guarantee.

    The Idempotency-Key header ensures that retrying the same request
    produces the same result without executing the transfer twice.
    """
    # Check for existing result with this key
    existing = await idempotency_store.get(idempotency_key)
    if existing:
        # Verify the request body matches the original
        request_hash = hashlib.sha256(request.model_dump_json().encode()).hexdigest()
        if existing["request_hash"] != request_hash:
            raise HTTPException(
                status_code=422,
                detail="Idempotency-Key reused with different request body",
            )
        return TransferResponse(**existing["response"])

    # Execute the transfer
    result = await transfer_service.execute(request)

    # Store the result keyed by idempotency key (TTL: 24 hours)
    await idempotency_store.put(
        idempotency_key,
        {
            "request_hash": hashlib.sha256(request.model_dump_json().encode()).hexdigest(),
            "response": result.model_dump(),
        },
        ttl_seconds=86400,
    )
    return result
```

**Optimistic Locking for Account Updates**:

```sql
-- Accounts table with version column for optimistic locking
ALTER TABLE accounts ADD COLUMN version INTEGER NOT NULL DEFAULT 0;

-- Update with version check (application must retry on conflict)
UPDATE accounts
SET balance = balance - $1,
    version = version + 1,
    updated_at = NOW()
WHERE id = $2 AND version = $3;
-- If affected_rows == 0, the account was modified concurrently: retry
```

**Rate Limiting for Trading APIs**:

```python
import time
from collections import defaultdict

class SlidingWindowRateLimiter:
    """Per-user rate limiter using a sliding window counter.

    Financial APIs require strict rate limiting to prevent market
    manipulation and ensure fair access during high-volatility periods.
    """

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self._max = max_requests
        self._window = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        now = time.monotonic()
        cutoff = now - self._window

        # Remove expired entries
        self._requests[user_id] = [
            t for t in self._requests[user_id] if t > cutoff
        ]

        if len(self._requests[user_id]) >= self._max:
            return False

        self._requests[user_id].append(now)
        return True
```

**WebSocket Market Data Feed**:

```python
import asyncio
import json
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class MarketQuote:
    symbol: str
    bid: Decimal
    ask: Decimal
    timestamp: float
    sequence: int      # monotonically increasing for gap detection

class MarketDataFeed:
    """WebSocket market data publisher with sequence numbers for gap detection."""

    def __init__(self) -> None:
        self._subscribers: dict[str, set[asyncio.Queue]] = {}
        self._sequences: dict[str, int] = {}

    async def publish(self, quote: MarketQuote) -> None:
        self._sequences[quote.symbol] = quote.sequence
        queues = self._subscribers.get(quote.symbol, set())
        message = json.dumps({
            "type": "quote",
            "symbol": quote.symbol,
            "bid": str(quote.bid),
            "ask": str(quote.ask),
            "timestamp": quote.timestamp,
            "sequence": quote.sequence,
        })
        for queue in queues:
            try:
                queue.put_nowait(message)
            except asyncio.QueueFull:
                pass  # slow consumer; drop message, client detects gap via sequence

    def subscribe(self, symbol: str) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue(maxsize=1000)
        self._subscribers.setdefault(symbol, set()).add(queue)
        return queue
```

**FIX Protocol Basics**: The Financial Information eXchange (FIX) protocol is the standard for electronic trading communication. FIX messages are tag-value pairs delimited by SOH (0x01). Key message types include NewOrderSingle (D), ExecutionReport (8), OrderCancelRequest (F), and MarketDataRequest (V). Modern implementations use QuickFIX libraries rather than hand-parsing FIX messages. When integrating with FIX counterparties, implement session-level heartbeats, sequence number tracking, and message gap fill to ensure reliable delivery.

### Step 7: Testing Financial Systems

Financial systems demand testing strategies that go beyond conventional unit tests. Accounting invariants must hold under all conditions, payment flows must survive failures, and regulatory scenarios must be verified.

**Property-Based Testing for Accounting Invariants**:

```python
from decimal import Decimal
from hypothesis import given, strategies as st, assume

# Strategy for valid Money amounts (positive, reasonable precision)
money_amount = st.decimals(
    min_value=Decimal("0.01"),
    max_value=Decimal("999999999.99"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)

@given(amount=money_amount)
def test_money_roundtrip_minor_units(amount: Decimal) -> None:
    """Money converted to minor units and back must equal the original."""
    m = Money(amount=amount, currency="USD")
    restored = Money.from_minor_units(m.minor_units, "USD")
    assert restored.amount == m.amount

@given(
    a=money_amount,
    b=money_amount,
    c=money_amount,
)
def test_money_addition_is_associative(a: Decimal, b: Decimal, c: Decimal) -> None:
    """(a + b) + c must equal a + (b + c) for all monetary amounts."""
    ma = Money(amount=a, currency="USD")
    mb = Money(amount=b, currency="USD")
    mc = Money(amount=c, currency="USD")
    assert (ma + mb) + mc == ma + (mb + mc)

@given(ratios=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=10))
def test_allocation_preserves_total(ratios: list[int]) -> None:
    """Allocating money by any ratios must preserve the total exactly."""
    total = Money(amount=Decimal("100.00"), currency="USD")
    parts = total.allocate(ratios)
    reconstructed = sum((p.amount for p in parts), Decimal("0.00"))
    assert reconstructed == total.amount

@given(
    amounts=st.lists(money_amount, min_size=2, max_size=20),
)
def test_ledger_entries_always_balance(amounts: list[Decimal]) -> None:
    """Every journal entry must have equal debits and credits."""
    # Simulate creating balanced entries
    total = sum(amounts, Decimal("0"))
    debit_total = total
    credit_total = total
    assert debit_total == credit_total
```

**Reconciliation Test Suite**:

```python
import pytest
from decimal import Decimal

class TestReconciliation:
    def test_perfect_match(self) -> None:
        internal = {"tx-1": Decimal("100.00"), "tx-2": Decimal("200.00")}
        gateway = {"tx-1": Decimal("100.00"), "tx-2": Decimal("200.00")}
        result = reconcile_payments(internal, gateway)
        assert len(result.matched) == 2
        assert len(result.missing_in_gateway) == 0
        assert len(result.missing_in_ledger) == 0
        assert len(result.amount_mismatches) == 0

    def test_missing_in_gateway(self) -> None:
        internal = {"tx-1": Decimal("100.00"), "tx-2": Decimal("200.00")}
        gateway = {"tx-1": Decimal("100.00")}
        result = reconcile_payments(internal, gateway)
        assert result.missing_in_gateway == ["tx-2"]

    def test_amount_mismatch(self) -> None:
        internal = {"tx-1": Decimal("100.00")}
        gateway = {"tx-1": Decimal("99.99")}
        result = reconcile_payments(internal, gateway)
        assert len(result.amount_mismatches) == 1
        assert result.amount_mismatches[0]["difference"] == Decimal("0.01")

    def test_empty_reconciliation(self) -> None:
        result = reconcile_payments({}, {})
        assert len(result.matched) == 0
```

**Chaos Testing for Payment Flows**:

```python
import asyncio
import random
from unittest.mock import AsyncMock, patch

class TestPaymentChaos:
    """Simulate failures at every stage of payment processing."""

    async def test_gateway_timeout_triggers_retry(self, payment_service: "PaymentService") -> None:
        """Payment must retry on gateway timeout and eventually succeed."""
        call_count = 0

        async def flaky_gateway(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise TimeoutError("Gateway timeout")
            return {"status": "authorized", "gateway_id": "gw-123"}

        with patch.object(payment_service, "_gateway", AsyncMock(side_effect=flaky_gateway)):
            result = await payment_service.authorize(payment_id="pay-1", amount=Decimal("50.00"))
            assert result.status == PaymentStatus.AUTHORIZED
            assert call_count == 3

    async def test_idempotent_under_concurrent_retries(self, payment_service: "PaymentService") -> None:
        """Concurrent retries with the same idempotency key must produce exactly one payment."""
        idempotency_key = "idem-concurrent-001"
        tasks = [
            payment_service.authorize(
                payment_id="pay-2",
                amount=Decimal("75.00"),
                idempotency_key=idempotency_key,
            )
            for _ in range(5)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        successful = [r for r in results if not isinstance(r, Exception)]
        assert len(successful) >= 1
        # All successful results must reference the same payment
        payment_ids = {r.id for r in successful}
        assert len(payment_ids) == 1

    async def test_partial_failure_rolls_back_ledger(self, payment_service: "PaymentService") -> None:
        """If ledger posting fails after capture, the system must compensate."""
        with patch.object(payment_service, "_ledger", AsyncMock(side_effect=Exception("DB down"))):
            with pytest.raises(Exception, match="DB down"):
                await payment_service.capture(payment_id="pay-3")
            # Verify the payment status is not left in an inconsistent state
            payment = await payment_service.get(payment_id="pay-3")
            assert payment.status != PaymentStatus.CAPTURED
```

**Regulatory Test Scenarios**:

```python
class TestRegulatoryCompliance:
    async def test_ctr_filed_for_large_transactions(self, monitor: TransactionMonitor) -> None:
        """Transactions over $10,000 must trigger a CTR filing."""
        alert = await monitor.check_ctr_threshold(
            customer_id="cust-1", amount=Decimal("10500.00"),
        )
        assert alert is not None
        assert alert.rule_id == "REG-001-CTR"

    async def test_structuring_detected(self, monitor: TransactionMonitor) -> None:
        """Multiple transactions just below $10,000 must trigger structuring alert."""
        # Seed three transactions at $9,500 within 24 hours
        for _ in range(3):
            await monitor.record_transaction("cust-2", Decimal("9500.00"))
        alert = await monitor.check_structuring("cust-2", Decimal("9500.00"))
        assert alert is not None
        assert alert.severity == AlertSeverity.HIGH

    async def test_sanctioned_country_blocked(self, geo_service: "GeoRestrictionService") -> None:
        """Transactions from OFAC-sanctioned jurisdictions must be blocked."""
        result = await geo_service.check_allowed(country_code="KP")
        assert result.blocked is True
        assert "OFAC" in result.reason
```

**Load Testing for Trading Systems**: Use tools like Locust or k6 to simulate realistic trading workloads. Key metrics to measure include order submission latency (p50, p95, p99), order book update latency, market data feed throughput, and matching engine throughput (orders per second). Trading systems typically require sub-millisecond latency for the matching engine and sub-10ms latency for the full order lifecycle. Run load tests during simulated market open scenarios (high burst traffic) and measure behavior under backpressure.

## Best Practices

- **Immutability is your audit trail**: Append-only data structures (event sourcing, journal entries) make compliance trivial and debugging possible
- **Idempotency everywhere**: Every write operation in a financial system must be safely retriable. Use idempotency keys on all API endpoints and database writes
- **Reconcile continuously**: Run reconciliation between your ledger and external systems (gateways, banks, partners) at least daily, ideally in real time
- **Fail closed, not open**: When fraud detection or compliance checks cannot run (service down, timeout), block the transaction rather than allowing it through
- **Separate concerns with the money**: Keep the ledger as a distinct service. Payment orchestration, fraud detection, and compliance monitoring are separate bounded contexts
- **Test with real numbers**: Use actual transaction amounts, currency codes, and edge cases (zero-decimal currencies like JPY, three-decimal currencies like BHD) in your test suites
- **Version your APIs**: Financial integrations are long-lived. Use versioned endpoints (`/v1/`, `/v2/`) and maintain backward compatibility for at least two major versions
- **Log everything, expose nothing**: Audit logs must capture all actions, but API responses and user-facing errors must never leak internal state, account numbers, or system details
- **Automate compliance checks**: Manual compliance processes do not scale. Encode rules as code, test them, and run them in CI alongside your application tests
- **Design for regulatory change**: Regulations change frequently. Externalize thresholds, country lists, and rule parameters into configuration rather than hardcoding them

## Quality Checklist

- [ ] All monetary amounts stored as fixed-precision decimals, never floating-point
- [ ] Double-entry invariant enforced at the database level (trigger or constraint)
- [ ] Idempotency keys required on all write endpoints
- [ ] Payment state machine prevents invalid transitions
- [ ] Webhook handlers verify signatures and process events idempotently
- [ ] Reconciliation runs daily between internal ledger and payment gateway
- [ ] KYC/AML screening runs at customer onboarding and periodically thereafter
- [ ] Transaction monitoring rules are configured, tested, and alerting
- [ ] Audit log is append-only with restricted permissions
- [ ] PCI-DSS scope minimized via client-side tokenization
- [ ] Exchange rates stored with effective dates and sources
- [ ] Property-based tests verify accounting invariants
- [ ] Chaos tests verify payment flow resilience under failure
- [ ] API versioning implemented for all financial endpoints
- [ ] Rate limiting configured for trading and high-frequency endpoints

## Related Skills

- `architecture-design` - System decomposition and trade-off analysis
- `api-design` - API contract design and versioning strategies
- `security-review` - Security assessment for financial applications
- `database-design` - Schema design for financial data models
- `event-sourcing` - Event-driven architecture for audit trails

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.

---




name: yagni
description: Applies the You-Aren't-Gonna-Need-It principle to prevent over-engineering
  by identifying and eliminating premature abstractions, unused features, and speculative
  complexity from software designs.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: coding
  triggers: yagni, you aren't gonna need it, don't build it now, over-engineering,
    premature abstraction, speculative features, kill unused code, remove complexity
  archetypes:
  - tactical
  - generation
  anti_triggers:
  - brainstorming
  - vague ideation
  - code golf
  - over-engineering
  response_profile:
    verbosity: low
    directive_strength: high
    abstraction_level: operational
  role: implementation
  scope: implementation
  output-format: code
  content-types:
  - code
  - guidance
  - do-dont
  - examples
  related-skills: kiss-principle, dht-technical-debt, progressive-enhancement, emergent-design




---




# YAGNI — You Aren't Gonna Need It

Senior engineer applying the YAGNI principle to eliminate premature abstractions, speculative features, and unnecessary complexity from codebases. YAGNI is not about avoiding architecture entirely — it's about letting requirements drive design decisions, not hypothetical future scenarios.

## TL;DR Checklist

- [ ] Question every abstraction: "What specific requirement demands this interface right now?"
- [ ] Remove unused feature flags, dead code paths, and speculative APIs before committing
- [ ] Prefer concrete implementations until a second caller proves the need for abstraction
- [ ] Flag complex designs that solve problems no one has encountered yet
- [ ] Replace multi-layered interfaces with single-purpose structs/functions when only one use case exists

---

## When to Use

Use this skill when:

- Reviewing architecture decisions that add layers "just in case" something happens
- Finding custom logging infrastructure, caching layers, or message queues before they've proven necessary
- Encountering abstract factories, strategy patterns, or plugin architectures with only one concrete implementation
- A feature flag system has grown to manage features that were never shipped
- Code contains dead branches, unused interfaces, or speculative utility functions

---

## When NOT to Use

Avoid YAGNI when:

- The abstraction exists because a second (or third) consumer already demands it — use KISS or DRY instead
- Industry standards require specific infrastructure (e.g., HIPAA-compliant audit logging, PCI-DSS tokenization)
- You are in the design phase of a greenfield project where domain experts have clear multi-year roadmaps
- Removing code would break published APIs or contract tests that external consumers depend on

---

## Core Workflow

1. **Inventory the Code for Speculative Constructs** — Scan for abstract factories with one impl, generic wrappers around specific types, feature flags controlling nothing, unused interfaces, and "helper" functions that no caller invokes.
   **Checkpoint:** Every flagged construct must trace to an actual requirement or user story, not a hypothetical future use case.

2. **Evaluate Each Abstraction** — For every abstraction found, ask three questions: (a) Is there a second concrete implementation already in production? (b) Is there a written requirement that mandates this flexibility? (c) Does removing the abstraction reduce cognitive load without increasing risk?
   **Checkpoint:** If any answer is "yes," the abstraction earns its place. If all three are "no," it goes.

3. **Remove and Simplify** — Replace abstract interfaces with concrete types, inline single-implementation strategies, delete unused functions and dead code paths, collapse unnecessary wrapper layers. Ensure tests still pass after each removal.
   **Checkpoint:** Run the full test suite; confirm no regression in functionality or performance.

4. **Document the Decision** — Record what was removed, why it was removed, and what requirement would reinstate it. Leave a comment at the call site explaining the concrete choice.
   **Checkpoint:** Future developers should understand not just what the code does, but why a simpler approach was chosen over a more flexible one.

5. **Apply Progressive Enhancement for Remaining Unknowns** — For genuinely uncertain requirements, build the minimal working version now and define an explicit extension point (interface, plugin hook, or configuration key) that can be fleshed out later without restructuring the core.
   **Checkpoint:** The extension point must have a concrete type signature or contract documented in code comments with the triggering requirement noted.

---

## Implementation Patterns

### Pattern 1: Concrete Over Abstract (Factory Anti-Pattern)

```python
# ❌ BAD — Factory with a single implementation, no future variant identified
class DataFormatter:
    """Abstract base for all formatters."""
    def format(self, data: dict) -> str:
        raise NotImplementedError


class JSONDataFormatter(DataFormatter):
    """Formats data as JSON — the only formatter we'll ever need."""
    def format(self, data: dict) -> str:
        return json.dumps(data, indent=2, default=str)


class CSVDataFormatter(DataFormatter):
    """Formats data as CSV — never used, added speculatively."""
    def format(self, data: dict) -> str:
        headers = list(data.keys())
        values = [str(data.get(h, "")) for h in headers]
        return ",".join(headers) + "\n" + ",".join(values)


class FormatterFactory:
    """Factory to choose between formatters — only JSON is ever used."""
    @staticmethod
    def create(format_type: str) -> DataFormatter:
        if format_type == "json":
            return JSONDataFormatter()
        elif format_type == "csv":
            return CSVDataFormatter()
        raise ValueError(f"Unknown format type: {format_type}")


# ✅ GOOD — Direct concrete usage, no factory or inheritance overhead
def format_data(data: dict) -> str:
    """Format data dictionary as a readable JSON string.
    
    If CSV export becomes a requirement, introduce a csv_format() function
    alongside this one — no factory or base class needed.
    """
    return json.dumps(data, indent=2, default=str)
```

### Pattern 2: Inline Speculative Feature Flags

```python
# ❌ BAD — Feature flag for a feature that was never activated and has no launch criteria
FEATURE_FLAG_NEW_ANALYTICS = os.getenv("FEATURE_FLAG_NEW_ANALYTICS", "false") == "true"

if FEATURE_FLAG_NEW_ANALYTICS:
    def generate_analytics_report(data):
        """Custom analytics engine with ML-based predictions."""
        from ml_predictor import predict_trends
        return predict_trends(data)
else:
    def generate_analytics_report(data):
        """Basic report generation — the only one we've shipped."""
        return {
            "total_transactions": sum(r.amount for r in data),
            "avg_transaction": sum(r.amount for r in data) / len(data) if data else 0,
        }


# ✅ GOOD — Remove feature flag, keep working implementation, add extension point
def generate_analytics_report(
    data: list[Transaction],
    extended: bool = False
) -> dict:
    """Generate analytics report.
    
    Args:
        data: Transaction records to analyze
        extended: If True, use ML-enhanced predictions (requires ml_predictor package).
                  Set via config when the analytics improvement initiative launches.
    
    Returns:
        Report dictionary with summary statistics
    """
    total = sum(r.amount for r in data)
    avg = total / len(data) if data else 0

    result: dict = {
        "total_transactions": total,
        "avg_transaction": round(avg, 2),
    }

    if extended:
        # Extension point — concrete when the ML feature requirement is approved.
        try:
            from ml_predictor import predict_trends
            result["predicted_trend"] = predict_trends(data)
        except ImportError:
            logger.warning("ML predictor not available; extended analytics skipped")

    return result
```

### Pattern 3: Premature Interface Design

```python
# ❌ BAD — Interface designed for multiple implementations that don't exist yet
class PaymentProcessor(Protocol):
    """Protocol defining the contract for any payment processor."""
    def process(self, amount: Decimal, currency: str) -> PaymentResult: ...
    def refund(self, transaction_id: str, amount: Decimal) -> RefundResult: ...
    def subscribe(self, webhook_url: str) -> WebhookRegistration: ...


class StripeProcessor(PaymentProcessor):
    """Stripe implementation — the only one deployed."""
    def process(self, amount: Decimal, currency: str) -> PaymentResult:
        return stripe.Charge.create(amount=int(amount * 100), currency=currency.lower())

    def refund(self, transaction_id: str, amount: Decimal) -> RefundResult:
        return stripe.Refund.create(charge=transaction_id, amount=int(amount * 100))

    def subscribe(self, webhook_url: str) -> WebhookRegistration:
        event_types = ["charge.succeeded", "charge.failed"]
        stripe.WebhookEndpoint.create(url=webhook_url, enabled_events=event_types)
        return WebhookRegistration(url=webhook_url, events=event_types)


class PayPalProcessor(PaymentProcessor):
    """PayPal implementation — defined but never used. Speculatively added."""
    def process(self, amount: Decimal, currency: str) -> PaymentResult: ...  # Stub


# ✅ GOOD — Concrete class for the only processor; Protocol added later if second vendor emerges
class StripePaymentProcessor:
    """Processes payments via Stripe API.
    
    This is a concrete implementation. If PayPal or Braintree becomes a requirement,
    introduce a PaymentProcessor protocol at that time and migrate both implementations
    to conform to it. Do not add the protocol now without a second consumer.
    """

    def __init__(self, api_key: str):
        stripe.api_key = api_key

    def process(self, amount: Decimal, currency: str) -> PaymentResult:
        charge = stripe.Charge.create(
            amount=int(amount * 100),
            currency=currency.lower(),
        )
        return PaymentResult(
            transaction_id=charge.id,
            status="succeeded",
            amount_processed=amount,
        )

    def refund(self, transaction_id: str, amount: Decimal) -> RefundResult:
        refund = stripe.Refund.create(charge=transaction_id, amount=int(amount * 100))
        return RefundResult(transaction_id=refund.id, status="refunded", amount_refunded=amount)
```

### Pattern 4: Premature Plugin/Extension Architecture

```python
# ❌ BAD — Full plugin system with discovery, lifecycle, and interfaces for zero plugins
class BasePlugin(ABC):
    """Abstract base class that all plugins must inherit from."""
    @abstractmethod
    def execute(self, context: PluginContext) -> PluginResult:
        pass

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        pass


class PluginRegistry:
    """Central registry for discovering and managing plugins."""
    _plugins: dict[str, BasePlugin] = {}

    @classmethod
    def register(cls, name: str, plugin: BasePlugin):
        cls._plugins[name] = plugin

    @classmethod
    def execute_all(cls, context: PluginContext) -> list[PluginResult]:
        results = []
        for plugin in cls._plugins.values():
            results.append(plugin.execute(context))
        return results


class NotificationPlugin(BasePlugin):
    """Sends email notifications — the only plugin we have."""
    def execute(self, context: PluginContext) -> PluginResult:
        send_email(context.to_address, context.subject, context.body)
        return PluginResult(success=True)

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(name="email", version="1.0")


# ✅ GOOD — Simple function call; extension point defined without plugin architecture overhead
def run_notification_step(context: ProcessingContext) -> NotificationResult:
    """Execute the notification processing step for a transaction.

    Extension point: If we need multiple notification backends (email, SMS, webhook),
    define this as a list of handlers rather than a single call:
    
        NOTIFICATION_HANDLERS: list[NotificationHandler] = [send_email_notification]
        
    Then iterate the list. No plugin registry or ABC required until there are actually
    multiple handler implementations to manage.
    """
    try:
        send_email(context.to_address, context.subject, context.body)
        return NotificationResult(success=True, method="email")
    except SMTPException as exc:
        logger.error(f"Notification failed: {exc}")
        return NotificationResult(success=False, error=str(exc))
```

---

## Constraints

### MUST DO
- Require a written requirement (user story, ticket, spec) to justify any abstraction beyond the current use case
- Treat every unused interface, dead function, and speculative feature as technical debt to be removed
- When removing code that others depend on, check for published APIs or external integrations first
- Document removal decisions with context: what was removed, why, and what requirement would bring it back
- Use the "second caller test" — an abstraction is only justified when a second concrete consumer exists

### MUST NOT DO
- Build interfaces, factories, or plugin architectures for hypothetical future use cases
- Keep dead code paths around "just in case someone needs them later" — version control preserves history
- Add feature flags without explicit launch criteria and a sunset date baked into the ticket
- Use "best practices" as an excuse to add complexity that no current requirement demands
- Remove abstractions that serve real, multiple consumers just because the pattern feels heavyweight

---

## Output Template

When auditing or refactoring code with YAGNI active, produce:

1. **Speculative Constructs Found** — List each abstraction, feature flag, unused interface, or dead code path identified, with file path and line reference
2. **Justification Assessment** — For each item, state whether a concrete requirement exists (ticket URL if applicable) or whether it is speculative
3. **Removal Plan** — Concrete replacements: what the simplified code looks like, what tests verify correctness
4. **Extension Points for Genuine Unknowns** — Where requirements are uncertain, define the minimal extension point with type signature and documented triggering condition
5. **Complexity Reduction Summary** — Quantify lines removed, layers collapsed, cognitive load reduced

---

## Related Skills

| Skill | Purpose |
|---|---|
| `kiss-principle` | Keep It Simple, Stupid — complementary principle focused on simplicity over elegance |
| `dht-technical-debt` | Identifies and tracks technical debt for systematic remediation |
| `progressive-enhancement` | Build the core that works first, then layer on improvements — the positive counterpart to YAGNI's restraint |
| `emergent-design` | Let architecture emerge from real requirements rather than designing it all upfront |

---

## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [Wikipedia — YAGNI (You Aren't Gonna Need It)](https://en.wikipedia.org/wiki/YAGNI)
- [Martin Fowler — YAGNI](https://martinfowler.com/bliki/Yagni.html)
- [Extreme Programming — Core Practices on xprogramming.com](https://xp.colorado.edu/)
- [Robert Martin — The Art of Agile Development (YAGNI Chapter)](https://www.amazon.com/Art-Agile-Development-John-Shoemaker/dp/0470344254)
- [Kent Beck — Test-Driven Development by Example (YAGNI in Practice)](https://en.wikipedia.org/wiki/Test-driven_development)

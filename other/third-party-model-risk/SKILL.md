---
name: third-party-model-risk
description: Assess the security and operational risk of third-party model APIs and vendors — covering due diligence requirements, API dependency assessment, data processing agreements, vendor lock-in risk, SLA gaps for AI-specific failure modes, and contingency planning for vendor model changes.
last_reviewed: 2026-04-29
---

# Third-Party Model Risk

## First Principle

**When you call a third-party model API, you are sending your users' data to a system you do not control, running code you cannot inspect, on infrastructure you cannot audit. The vendor's model card is not a security assessment.**

Third-party LLM APIs are production dependencies with a threat profile that differs from conventional SaaS vendors. The model itself changes without notice — behavior that passed your evaluation today may not match what the API returns next month if the vendor updates the model. The data you send in prompts may be used for training by default. The vendor's safety controls may be updated in ways that break your application's assumptions. These risks require active management, not just a contract review.

## Attack Mental Model

Third-party model risk is not primarily about the vendor being malicious — it is about the consequences of vendor decisions you cannot control:

1. **Model behavior drift** — the vendor updates the underlying model. Your application's prompts, safety assumptions, and expected output formats break silently.
2. **Data exposure** — prompt data sent to the vendor's API is logged, processed, and potentially used for training if your contract does not explicitly exclude it.
3. **Dependency availability** — the vendor experiences an outage, deprecates a model, or raises prices beyond your budget. Your application has no fallback.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Vendor model behavior is tested against a behavioral baseline on a defined cadence — not assumed to be stable between API calls. |
| **Scope** | Data sent to third-party APIs is classified before transmission. PII and confidential data are redacted or pseudonymized unless the vendor's DPA explicitly covers their processing. |
| **Isolate** | The application's dependency on a specific vendor is encapsulated behind an abstraction layer that allows model switching without application code changes. |
| **Enforce** | Contracts with model vendors include explicit provisions on data use for training, retention periods, model change notifications, and SLAs for AI-specific failure modes. |

## TPR.1 Vendor Due Diligence and Contractual Controls

**The core vulnerability:** Teams adopt third-party model APIs by signing up for a developer account and adding an API key to their application. The vendor's terms of service — which may allow training on API inputs, log retention for 30–90 days, and model updates without notice — are accepted without review.

### Check

- Has the vendor's data processing agreement (DPA) been reviewed by legal — specifically for: (a) whether API inputs are used for training, (b) data retention periods, (c) subprocessor disclosure, and (d) audit rights?
- Is there a contractual requirement for the vendor to provide notice before making breaking changes to model behavior — or does the vendor's terms reserve the right to update models without notification?
- Has the vendor undergone a third-party security audit (SOC 2 Type II, ISO 27001, or equivalent) — and has that report been reviewed, not just confirmed to exist?

### Action

- **Define a vendor assessment checklist for AI APIs:**

| Assessment Item | Minimum Acceptable |
|---|---|
| Data use for training | Opt-out available or prohibited by default on paid tier |
| Data retention | ≤ 30 days for prompt/response logs, or zero-retention option available |
| Model change notification | 30-day notice for breaking changes |
| Security certification | SOC 2 Type II or equivalent, issued within 18 months |
| Data residency | Documented, aligned with regulatory requirements |
| Subprocessors | Listed and subject to equivalent DPA terms |
| SLA for AI failure modes | Defined coverage for hallucination-class incidents, not just uptime |

- **Negotiate opt-out of training data use before sending production data.** Most enterprise-tier API agreements exclude API inputs from training by default. If your current agreement does not confirm this, confirm in writing before processing production data through the API.
- **Request the vendor's AI incident response contact and SLA.** Standard SLA agreements cover uptime — they do not address what happens when a model update causes your application to behave unsafely. Establish a direct escalation path for AI-specific incidents.

### Failure Modes

- A team integrates a free-tier model API for a customer-facing feature. The free tier terms allow training on inputs. Customer conversations are used to train the vendor's next model version.
- The vendor changes the model behind a stable endpoint. The model's output format changes slightly. The application's JSON parser fails silently, passing malformed data downstream for two weeks before the error is noticed.

## TPR.2 Behavioral Monitoring and Fallback Planning

**The core vulnerability:** Third-party model behavior can change without the vendor publishing a changelog. A model that reliably refused a category of requests last month may handle them differently today. Without behavioral monitoring, these changes are invisible until a user reports an unexpected response.

### Check

- Is the third-party model's behavior tested against a fixed behavioral baseline on a defined cadence (daily or weekly) — not just at integration time?
- Is there a vendor fallback plan — a second model provider or a local model that can serve requests if the primary vendor is unavailable or exhibits unsafe behavior?
- Is the application's model dependency encapsulated behind an abstraction layer that allows switching providers without changes to business logic?

### Action

- **Run a behavioral baseline check on a schedule:**

```python
BASELINE_PROBES = [
    {"prompt": "Provide step-by-step instructions for...", "expected": "refusal"},
    {"prompt": "What is the capital of France?", "expected_contains": "Paris"},
    # ... 20-50 probes covering safety and capability
]

def check_vendor_behavioral_baseline(client, probes: list) -> dict:
    failures = []
    for probe in probes:
        response = client.complete(probe["prompt"])
        if not meets_expectation(response, probe):
            failures.append({"probe": probe, "response": response})
    return {"pass_rate": 1 - len(failures)/len(probes), "failures": failures}
```

Alert if pass rate drops below 95%. Investigate failures immediately.

- **Implement a provider abstraction layer.** Wrap all model calls behind a provider interface that can be swapped without changing application code:

```python
class ModelProvider(Protocol):
    def complete(self, prompt: str, **kwargs) -> str: ...

class AnthropicProvider:
    def complete(self, prompt: str, **kwargs) -> str:
        return self._client.messages.create(...)

class FallbackProvider:
    def complete(self, prompt: str, **kwargs) -> str:
        return self._local_model.generate(...)

# Switch providers by changing one line:
provider: ModelProvider = AnthropicProvider()
```

- **Maintain a tested fallback provider.** The fallback is only useful if it has been tested and is ready to receive production traffic. Test it monthly. Define the conditions under which you switch: vendor outage, behavioral regression, or price threshold.

### Minimum Deliverable Per Review

- [ ] DPA review: training opt-out, retention period, and audit rights confirmed in writing
- [ ] Model change notification: contractual notice period for breaking changes
- [ ] Security certification: SOC 2 Type II or equivalent reviewed (not just confirmed)
- [ ] Behavioral baseline: automated probes running on schedule with alerting
- [ ] Provider abstraction: all model calls behind a swappable interface
- [ ] Fallback provider: tested, documented, and with defined activation criteria

## Quick Win

**Check your current vendor contract for training opt-out.** Log in to your vendor's admin console or find your enterprise agreement. Confirm that API inputs are excluded from training. If you cannot confirm this within 30 minutes, assume they are not excluded and contact your vendor rep to clarify — before your next production prompt contains customer data.

## References

- Model supply chain and artifact integrity → [model-supply-chain-security/SKILL.md](../model-supply-chain-security/SKILL.md)
- Governance and vendor change management → [ai-governance-and-incident-response/SKILL.md](../ai-governance-and-incident-response/SKILL.md)
- PII compliance for data sent to vendors → [ai-privacy-pii-compliance/SKILL.md](../ai-privacy-pii-compliance/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)

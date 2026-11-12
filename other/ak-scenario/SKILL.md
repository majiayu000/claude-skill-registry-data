---
name: ak-scenario
description: "Generate edge cases and test scenarios by decomposing a feature across 12 dimensions."
when_to_use: "Invoke for risk discovery, QA planning or regression design."
category: workflow
keywords: [edge-cases, test-scenarios, dimensions, saturation, iterations]
argument-hint: "<file path or feature description> [--iterations N] [--saturation]"
metadata:
  author: agentkit
  attribution: "Scenario exploration pattern adapted from autoresearch by Udit Goenka (MIT)"
  version: "1.3.0"
---

# ak-scenario — Edge Case & Scenario Explorer

Decompose any feature or code path across 12 dimensions to surface edge cases, risks, and test targets before implementation begins.

Supports two modes:
- **One-shot** (default): single pass of concrete scenarios per relevant dimension; 3–5 is a starting heuristic, not a quota.
- **Iterative** (`--iterations N` or `--saturation`): loop until bounded count or novelty exhausted.

## When to Use

- Before implementing complex or stateful features
- Before writing tests (generates test targets)
- Risk assessment during planning or code review
- API design review — surface contract edge cases early
- Deep pre-release coverage audit (`--saturation`)

## When NOT to Use

- Trivial single-line changes or cosmetic UI tweaks
- Already well-tested, stable code with no recent modifications
- Pure configuration changes with no logic paths

---

## Flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--iterations N` | — | Bounded loop: run exactly N iterations, then stop with summary |
| `--saturation` | off | Saturation loop: keep iterating until 2 consecutive iterations produce no novel scenarios |
| `--domain <type>` | auto | Domain hint: `software`, `product`, `business`, `security`, `marketing` |
| `--focus <dim>` | auto | Prioritize dimension: `edge-cases`, `failures`, `security`, `scale` |
| `--format <type>` | table | Output format: `table`, `use-cases`, `test-scenarios`, `threat-scenarios` |

When neither `--iterations` nor `--saturation` is set: one-shot mode (original behavior, default).

---

## 12 Decomposition Dimensions

Not all 12 apply to every feature. Identify relevant dimensions first, then generate scenarios only for those.

| # | Dimension | What to Look For |
|---|-----------|------------------|
| 1 | **User Types** | admin, guest, banned, new user, power user, bot/scraper |
| 2 | **Input Extremes** | empty, null, max length, unicode, special chars, SQL/script injection |
| 3 | **Timing** | concurrent access, race conditions, timeout, slow network, retry storms |
| 4 | **Scale** | 0 items, 1 item, 1M items, pagination boundary, cursor wrap |
| 5 | **State Transitions** | first use, mid-flow abort, resume after crash, partial completion |
| 6 | **Environment** | mobile/low-end CPU, no JS, screen reader, proxy/VPN, different timezone/locale |
| 7 | **Error Cascades** | DB down, API timeout, disk full, OOM, network partition, partial write |
| 8 | **Authorization** | expired token, wrong role, shared/public link, CORS, CSRF, privilege escalation |
| 9 | **Data Integrity** | duplicate entries, orphan references, encoding mismatch, concurrent schema migration |
| 10 | **Integration** | webhook replay, API version mismatch, third-party outage, contract drift |
| 11 | **Compliance** | GDPR deletion request, audit logging gap, data retention, accidental PII exposure |
| 12 | **Business Logic** | edge pricing (zero/negative), coupon stacking, refund after partial delivery, free tier limits |

---

## Workflow

### One-Shot Mode (default)

1. **Read** target file(s) or parse feature description from argument
2. **Filter dimensions** — mark which of the 12 apply; skip irrelevant ones explicitly, naming the assumption behind each skip. A dimension skipped on an assumption that could break within the life of this feature is itself a scenario, not a skip
3. **Generate concrete scenarios** per relevant dimension; connect each to an invariant or state transition and a test target. Do not pad to a fixed count.
4. **Categorize severity** — Critical / High / Medium / Low
5. **Output** as structured table (see format below)
6. **Summarize** total scenario count by severity

### Iterative Mode (`--iterations N` or `--saturation`)

Novelty is a stopping heuristic, not proof that all cases exist in the report. Keep the run bounded by a declared iteration/time budget, including saturation mode. Report the bound and residual uncertainty. Iterative mode runs this loop:

1. **Read** target and build understanding (actors, components, preconditions)
2. **Filter dimensions** — same as one-shot
3. **Loop** — each iteration:
   a. Pick highest-priority unexplored dimension or combination
   b. Generate **one** concrete situation (specific trigger, flow, expected outcome)
   c. **Classify** against all previously kept situations:
      - **New**: different dimension AND different trigger/precondition → KEEP
      - **Variant**: same dimension but different actor, data, or outcome → KEEP
      - **Duplicate**: same dimension + same trigger + same outcome → DISCARD
      - **Out of scope / Low value** → DISCARD, log reason
   d. If kept: expand edge cases (what-if, boundary, interruption, ordering, missing data, stale data)
   e. Log row to `scenario-results.tsv`
   f. Every 5 iterations: print progress summary (see format below)
4. **Halt**:
   - `--iterations N`: stop after N iterations
   - `--saturation`: stop when 2 consecutive iterations produce zero `New` classifications
5. **Output** final summary with observed coverage, invariant/test mapping, unresolved gaps and composite score. The score counts exploration activity, not correctness or exhaustive coverage.

**Force dimension rotation** after 3 consecutive same-dimension iterations. Rotate through:
Dimension walk → Combination → Negation → Amplification → Persona shift → Temporal shift

### Severity Criteria

| Level | Meaning |
|-------|---------|
| **Critical** | Data loss, security breach, auth bypass, silent corruption |
| **High** | Feature broken for a subset of users, data inconsistency |
| **Medium** | Degraded UX, recoverable error not surfaced to user |
| **Low** | Minor visual glitch, non-blocking warning |

---

## Output Format

### One-Shot

```
## Scenario Report: [target]

Dimensions analyzed: [list]
Dimensions skipped: [list + reason]

| # | Dimension | Scenario | Severity | Expected Behavior |
|---|-----------|----------|----------|-------------------|
| 1 | Input Extremes | Empty string for required name field | High | Return 400 with field error |
| 2 | Authorization | Expired JWT accessing protected route | Critical | Redirect to login, invalidate session |
| 3 | Timing | Two users submit same form simultaneously | High | Idempotency key or conflict error |

### Summary
- Critical: N
- High: N
- Medium: N
- Low: N
- Total: N scenarios across X dimensions
```

### Iterative — Progress Summary (every 5 iterations)

```
=== Scenario Progress (iteration 15) ===
Scenarios kept:    12  (8 new, 4 variants)
Discarded:          3  (2 duplicates, 1 out-of-scope)
Dimensions covered: 7/12 (58%)
Edge cases found:  18
Severity:          2 Critical, 4 High, 8 Medium, 4 Low
Coverage gaps:     scale, temporal, recovery
```

### Iterative — TSV Log (`scenario-results.tsv`)

```tsv
iteration	dimension	classification	severity	title	description	parent
1	happy_path	new	-	Successful checkout	User completes standard checkout	-
2	error_path	new	HIGH	Payment declined	Card rejected during checkout	-
3	edge_case	duplicate	-	Empty cart	Already covered by #1	#1
```

### Iterative — Final Summary

```
## Scenario Report: [target]  (iterations: N)

[Full table of kept scenarios, grouped by dimension]

### Coverage Matrix
[dimension × severity grid]

### Composite Score: NNN
  scenarios_generated * 10  = X
  edge_cases_found * 15     = X
  dimensions_covered * 30   = X
  unique_actors * 5         = X
  high_severity * 3         = X

### Saturation
Halted: [after N iterations — bounded] | [saturation — 2 consecutive iterations with no novel cases]
```

---

## Integration with Other Skills

| Next Step | Skill | How |
|-----------|-------|-----|
| Generate test cases from scenarios | `ak-test` | Pass scenario table as input context |
| Inform implementation plan risks | `ak-plan` | Paste Critical/High rows into risk assessment |
| Deep persona debate on top risks | `ak-predict` | Feed Critical scenarios as the change proposal |

---

## Reference

Saturation loop mechanics, novelty detection, and generation strategy are embedded in the iterative-mode instructions above.

---

## Example Invocations

```
# One-shot (default — backwards compatible)
/ak-scenario src/api/payment.ts
/ak-scenario "User registration with OAuth providers"

# Bounded iterative — exactly 25 iterations
/ak-scenario src/api/payment.ts --iterations 25

# Saturation — stop when the novelty heuristic is satisfied
/ak-scenario "Add multi-tenancy to the database layer" --saturation

# Saturation with domain hint for priority dimension ordering
/ak-scenario src/middleware/auth.ts --saturation --domain security
```

---

## Lineage

Faithful absorption (in scope) of upstream `/autoresearch:scenario` ([uditgoenka/autoresearch](https://github.com/uditgoenka/autoresearch), MIT). The local version supports both one-shot generation and the iterative saturation loop.

See `/ak-autoresearch` for the full family map.

## Optional workflow shadow experiment

Only when explicitly requested, inspect `ak eval workflow --help` and prepare
its bounded, reviewed request with workflow `scenario`. Default `off`
validates locally. `--mode shadow` additionally requires user-scope master and
provider configuration, explicit `workflow-controller: true` consumer consent,
and the provider credential; never enable or infer consent from an ambient key.
The optional command may send sanitized facts externally and incur charges.

Supply the existing domain decision and complete policy facts first. Keep all
`effective_*` decisions unchanged; record accepted `hypothetical_*` suggestions
only for comparison. Errors, low confidence and unavailable provider evidence
use the existing workflow. Never execute a recommendation or treat it as
permission. Existing caps, user stops, three-failure human checkpoints and
approval/R3 controls remain authoritative. Ordinary skill startup makes no call.

The generator still creates candidates and checks complete history. Supply the
latest chronological 16 kept situations at most, plus total history count;
partial history cannot qualify for changed classification. Inspect classification,
novelty/value scores and full probabilities; these ordinal scores are not
percentages. KEEP/DISCARD is candidate disposition, not workflow CONTINUE/STOP.
Variants remain non-New for the existing two-iteration saturation counter.

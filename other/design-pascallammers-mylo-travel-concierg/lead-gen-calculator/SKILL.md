---
name: lead-gen-calculator
description: Multi-step calculator UI for Astro. Quote tools, pricing calculators. Uses astro-forms for backend.
---

# Lead Gen Calculator Skill

**Multi-step calculator UI. Requires astro-forms for backend.**

## Purpose

Step-by-step calculator interface. Captures leads through progressive questions.

## Output

```yaml
calculator_ready: true
steps: [...]
step_limits: { max_steps: 7, max_fields_per_step: 4 }
primary_conversion: { type: calculator, id: "quote-calc" }
conversion_verdict: PASS | WARN | FAIL
```

## Primary Conversion Declaration

**Calculator IS the primary conversion on its page.**

```yaml
primary_conversion:
  type: calculator
  id: "quote-calculator"
  page: "/kalkulator"
```

No other forms on calculator pages.

## Page Exclusion Rules

| Page Type | Calculator Allowed |
|-----------|-------------------|
| calculator | ✅ Required |
| landing | ✅ Optional (embedded) |
| service | ❌ Use form instead |
| thank-you | ❌ Forbidden |
| article | ❌ Forbidden |

**Calculator on forbidden page = FAIL.**

## Step Limits (Cognitive Load)

```yaml
step_limits:
  max_steps: 7
  max_fields_per_step: 4
  max_options_per_question: 6
```

| Limit | Value | Result if exceeded |
|-------|-------|-------------------|
| Steps | 7 | FAIL |
| Fields/step | 4 | FAIL |
| Options/question | 6 | WARN |

## Progressive Disclosure

**Personal data only in final step.**

| Step | Can Ask |
|------|---------|
| 1-N | Service, location, preferences |
| Final | Name, email, phone, GDPR |

**Email before final step = FAIL.**

## Step Types & Auto-Advance

| Type | Behavior | Auto-advance |
|------|----------|--------------|
| radio | Single select | Yes (200ms) |
| checkbox | Multi-select | When all selected |
| dropdown | Select menu | On selection |
| form | Contact (final) | No (submit) |

## Data Integrity Contract

**Calculator submissions MUST include:**

```yaml
data_contract:
  required:
    - quote_id         # Unique hash
    - all_answers      # Complete step data
    - source_page      # Calculator URL
    - timestamp        # ISO datetime
    - gdpr_consent     # true + timestamp
  calculated:
    - price_estimate   # If pricing enabled
    - breakdown        # Line items
```

## Post-Submit Flow Contract

```yaml
post_submit_flow:
  1_result_page: required      # /eredmeny/[hash]
  2_confirmation_email: required
  3_analytics_event: required  # calculator_submit
```

**Any missing = FAIL.**

## Visual Rules

| Element | Rule |
|---------|------|
| Images | 1:1 aspect ratio |
| Cards | Brand color bg, white text |
| Social proof | Different per step |
| Chrome | Minimal, focus on question |
| Menu | Hidden on calculator |

## Loading Strategy

| Phase | Action |
|-------|--------|
| First page | Eager load all assets |
| After load | Prefetch next step |
| API calls | Show skeleton |

## GTM Events (Required)

```yaml
gtm_events:
  - calculator_step      # Step viewed
  - calculator_option    # Option selected
  - calculator_submit    # Form submitted
  - calculator_value     # Quote amount
```

**Missing events = WARN.**

## Browser State

| Feature | Implementation |
|---------|----------------|
| Persistence | localStorage |
| Back button | popstate listener |
| State restore | From history.state |

## Conversion Verdict

```yaml
conversion_verdict: PASS | WARN | FAIL
issues: []
```

| Condition | Verdict |
|-----------|---------|
| Calculator on forbidden page | FAIL |
| >7 steps | FAIL |
| >4 fields per step | FAIL |
| Email before final step | FAIL |
| Missing data contract field | FAIL |
| Post-submit flow incomplete | FAIL |
| >6 options per question | WARN |
| GTM events missing | WARN |
| All pass | PASS |

## FAIL States

| Condition |
|-----------|
| Calculator on thank-you/article |
| Exceeds 7 steps |
| Exceeds 4 fields per step |
| Personal data before final step |
| No result page |
| No confirmation email |

## WARN States

| Condition |
|-----------|
| >6 options per question |
| GTM events not configured |
| No social proof variation |

## References

- [components.md](references/components.md) — UI components
- [client.md](references/client.md) — Client JS
- [gtm.md](references/gtm.md) — Analytics events

## Definition of Done

- [ ] Primary conversion declared
- [ ] Steps ≤7, fields/step ≤4
- [ ] Personal data only in final step
- [ ] Data contract complete
- [ ] Post-submit flow complete
- [ ] GTM events configured
- [ ] Browser back handled
- [ ] conversion_verdict = PASS

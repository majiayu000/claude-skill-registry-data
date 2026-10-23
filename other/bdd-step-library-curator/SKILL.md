---
name: bdd-step-library-curator
description: "Keeps a BDD step-definition library DRY across a Cucumber / Behave / Reqnroll project - inventories every step definition, detects duplicates (different patterns matching the same intent), recommends canonical consolidations, reorganizes steps by domain, publishes a step-library README the team greps for \"is there already a step for X?\" before authoring new ones, and builds a scenario coverage map that fingerprints new Gherkin scenarios against the live suite to classify each as duplicate, partial overlap, or genuine gap before any test is authored. Use when a BDD project's step count grows past ~50, on a quarterly step-library review, when a new engineer is about to write a duplicate step, or when fresh .feature files need a covered-already check."
---

# bdd-step-library-curator

## Overview

After 6 months of a BDD project, step definitions proliferate:

- Two engineers write `Given a user` and `Given a logged-in user`
  for the same fixture.
- Three slightly-different "I click X" steps (one for buttons,
  one for links, one for arbitrary elements) - all do the same
  thing.
- A new engineer can't find existing steps and writes a fourth
  variant.

The result: step library bloat → Gherkin features hard to read,
step ambiguities, runtime errors, drift.

This skill builds a curation workflow.

## When to use

- A BDD project's step count exceeds ~50 (proliferation threshold).
- A new engineer reports "I couldn't find a step for X."
- Quarterly: scheduled step review.
- Before adopting BDD across multiple teams (proactively design
  the step library shape).

## How to use

Work through Steps 1-6 below in order: inventory -> detect duplicates -> recommend consolidations -> reorganize and publish the README -> gate new steps pre-merge -> repeat on a cadence.

## Step 1 - Inventory step definitions

Extract every declared step pattern across the project. Each runner
uses its own annotation syntax (`@Given` in Cucumber-JVM, `@given`
in Behave, `[Given]` in Reqnroll / SpecFlow) - the per-runner
extraction commands are in
[references/step-extraction-and-overlap.md](references/step-extraction-and-overlap.md).

The inventory produces a step audit:

```
Total step definitions: 142
Unique patterns: 138    (4 ambiguous duplicates already)
Per Gherkin verb:
  Given: 58
  When:  34
  Then:  47
  And:    3
```

## Step 2 - Detect duplicates / overlaps

Two patterns are likely duplicates when:

- Same wording, different phrasing: `Given a user` vs `Given an
  existing user` vs `Given the user`.
- Same parameters, different verbs: `When I click {label}` vs
  `When I press {label}` vs `When I tap {label}`.
- Same fixture, different shape: `Given a cart with {n} items` vs
  `Given a cart containing {n} items`.

Normalize each pattern (lowercase, drop articles, collapse
parameters) and group by the normalized form; any group of size
greater than one is a candidate cluster. The overlap script that
does this is in
[references/step-extraction-and-overlap.md](references/step-extraction-and-overlap.md).

## Step 3 - Recommend consolidation

For each duplicate group:

```markdown
**Duplicate group:** 4 step definitions with normalized "user is
logged in"

| Pattern                            | File / line                |
|------------------------------------|----------------------------|
| `Given a user is logged in`         | `auth_steps.py:12`         |
| `Given the user is logged in`        | `cart_steps.py:8`           |
| `Given an authenticated user`        | `checkout_steps.py:5`       |
| `Given a logged-in user`            | `profile_steps.py:14`       |

**Recommendation:** Consolidate to **`Given a logged-in user`**
(highest count of usage in current Gherkin; clearest wording).

Replace the other 3 step definitions with a single canonical one
in `shared_steps.py`. Update the Gherkin features that use the
deprecated patterns.
```

**Verify:** consolidation is destructive - it deletes step definitions and
rewrites `.feature` files. After each group, run the full BDD suite and assert
zero undefined or ambiguous steps and no orphaned scenarios before declaring the
refactor complete. If a scenario reports an undefined step, a `.feature` file
still references a deprecated pattern - fix that reference and re-run.

## Step 4 - Domain organization

Group steps per domain area:

```
features/steps/
├── shared/                      # cross-domain (login, navigation, etc.)
│   ├── auth_steps.py
│   ├── navigation_steps.py
│   └── data_steps.py
├── checkout/                    # checkout-specific
│   ├── promo_steps.py
│   ├── payment_steps.py
│   └── cart_steps.py
├── account/                     # account-specific
│   └── profile_steps.py
└── README.md                    # step library index
```

The README is the discoverability artifact:

```markdown
# Step library

## Shared (cross-domain)

### Auth
- `Given a logged-in user` (auth_steps.py:12) - creates and logs in a generic test user.
- `Given a logged-in admin` (auth_steps.py:25) - logged-in user with admin role.
- `Given an unauthenticated visitor` (auth_steps.py:38) - no session.

### Navigation
- `When I navigate to {path}` - go to URL.
- `When I click {label}` - click any element with this label.

## Checkout

### Cart
- `Given the cart contains {qty} of {sku} at ${price}` - seed a cart.
- `Given the cart is empty` - empty cart.

### Promo codes
- `Given promo code {code} is active` - pre-seed a promo in the admin.
- `When I enter {code} in the promo input` - type the code.
- `When I click {label}` - (uses shared step).

(...)
```

The README + grep is the team's "is there a step for X?" tool.

## Step 5 - Pre-merge step gate

Add a CI check that flags new step definitions so no engineer adds a
duplicate unknowingly. The check warns (doesn't block), forcing the
author to acknowledge the new step and grep the README first. The
`check-new-steps.sh` script is in
[references/step-extraction-and-overlap.md](references/step-extraction-and-overlap.md).

## Scenario coverage map (pre-authoring duplicate check)

The same duplicate-prevention discipline applies one level up, at the
scenario layer. When new `.feature` files land (typically from
`gherkin-from-stories`), fingerprint each new scenario by its ordered,
keyword-stripped step texts and diff against the existing suite's
step-usage index before any test is authored:

- `DUPLICATE` - every step already covered under one existing scenario:
  do not author.
- `PARTIAL` - some steps overlap: author only the new step definitions,
  reuse the rest.
- `GAP` - nothing matches: author in full.

Fingerprint on the step **text**, not the keyword - per the Gherkin
reference, "keywords are not taken into account when looking for a step
definition." Prefer the Cucumber JSON report over re-parsing source
`.feature` files when one exists, exclude Background steps from the
fingerprint, and halt on an empty or tiny index (a map against an empty
suite is vacuous). The full method, output templates, tag-match handling,
and hard-reject conditions:
[references/coverage-map.md](references/coverage-map.md).

## Step 6 - Quarterly cadence

| Cadence            | Trigger                                           |
|--------------------|---------------------------------------------------|
| Quarterly           | Scheduled step library review.                    |
| New team member     | Onboarding: walk the README.                      |
| Step count exceeds threshold | Triggered review.                         |
| New domain area     | Add steps; update README.                          |

## Worked example

Curating a 142-step library in a mixed Behave project, end to end.

**1. Inventory.** The Behave extraction over `features/steps/` yields the
Step 1 audit: 142 step definitions, 138 unique patterns - so 4 are already
ambiguous duplicates the runner would flag at match time.

**2. Detect.** The overlap script surfaces one cluster - the four
`user is logged in` variants listed in Step 3's duplicate-group table.

**3. Consolidate.** Pick `Given a logged-in user` as canonical
(clearest wording, most-used in current Gherkin). Move it into
`features/steps/shared/auth_steps.py`, delete the other three
definitions, and rewrite the `.feature` files that used the
deprecated phrasings - edit the Gherkin first so no scenario is
left orphaned, then run the Step 3 verification.

**4. Reorganize + publish.** Split the flat `features/steps/` into
`shared/`, `checkout/`, and `account/`, then regenerate the README
index. The library now advertises
`Given a logged-in user (auth_steps.py) - creates and logs in a generic test user`
under Shared → Auth.

**5. Gate.** Add the pre-merge new-step check. The next PR that adds
`Given the customer is signed in` trips the warning; the author greps
the README, finds `Given a logged-in user`, and reuses it instead of
adding a fifth variant.

Result: 142 → 139 step definitions, zero ambiguous duplicates, one
discoverable index the whole team searches before writing a step.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Per-engineer step files (`alice_steps.py`)                            | Ownership without domain alignment; duplication across files.            | Domain-organized files (Step 4). |
| Step library README missing                                            | Discoverability nil; engineers re-implement.                             | README per Step 4. |
| Ambiguous step deletion without grep                                   | Breaks scenarios silently.                                                | Replace canonical → deprecated; update all Gherkin first. |
| Step "shared library" that's a giant `helpers.py`                      | All engineers conflict on it; merge hell.                                | Domain split (Step 4). |
| Reviewing step count quarterly only                                    | Proliferation outpaces review; library bloats.                          | Pre-merge gate (Step 5). |

## Limitations

- **Heuristic duplicate detection.** Some patterns are
  legitimately distinct (`Given a user` for auth vs `Given a user
  with profile data` for profile tests).
- **Domain organization is per-team.** What's "shared" varies.
- **Consolidation cost.** Each refactor touches Gherkin + step
  definitions; not free.
- **Doesn't fix Gherkin quality.** A clean step library doesn't
  prevent imperative-style Gherkin scenarios. Pair with a Gherkin
  style review.

## References

- Step extraction commands, the overlap-detection script, and the
  pre-merge gate:
  [references/step-extraction-and-overlap.md](references/step-extraction-and-overlap.md).
- Scenario-level coverage map (fingerprinting, output templates,
  hard-reject conditions):
  [references/coverage-map.md](references/coverage-map.md).
- `cucumber-testing`,
  `behave-testing`,
  `reqnroll-testing` - per-language
  runners this curator works alongside.

---
name: padosoft-environment-gating
description: >-
  Use this skill whenever a branch behaves differently depending on the environment — debug output, error
  detail, a profiler or diagnostic endpoint, a permissive security header, a seed, an auth mock, a provider
  in test mode, a destructive command guard, a feature flag keyed on the deployment. Also when the user
  reports that a development behaviour appeared on the live site, that stack traces or query dumps are
  visible to users, that a staging box behaves like a laptop, or that an environment check did not match.
  It replaces the two-valued check with the three answers that actually exist, and picks the default from
  what the branch does. Do not use it for CI workflow configuration, for secret management, or for choosing
  a deployment topology.
license: MIT
compatibility: >-
  Any stack that reads an environment name. Examples use a PHP/Laravel helper layer because that is where
  the call sites were counted, but the failure is framework-independent.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The answers are three, not two — a convenience defaults off, a protection defaults on.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: environment, staging, production, debug, feature flag, fail closed, configuration, guard
---

# Environment gating

An environment check is a **string comparison with a value somebody typed into a file**. It is exact, it is
unvalidated, and when it does not match, nothing goes wrong — the development branch simply lights up on the
live site, doing exactly what it was asked to do.

**The rule: the answers are three, not two — and the branch decides which default is safe.**

---

## 1. Why the two-valued check fails

```text
APP_ENV = "Production"       → is_production("production")  false
APP_ENV = "production "      → false        (a trailing space, invisible in the file)
APP_ENV = "prod"             → false
APP_ENV = "prod-eu-1"        → false
APP_ENV = "produzione"       → false
```

Every one of those is a live deployment answering *no, I am not production*. Downstream: error pages with
credentials in them, a profiler recording session cookies, diagnostic endpoints open, orders sent to a
provider in test mode. No exception, no alert — the code did what it was told.

The real incidence is not one call site. It is **dozens**, spread over the codebase, all written the same
way by people copying the line above.

## 2. The three answers

"I am in production" and "I am not in production" are **not** each other's negation, because there is a
third case: **the name is unknown** — a typo, a new deployment nobody added to the list. Treating it as
either of the first two is the whole defect.

So: two separate questions, each answering *yes* only when it is certain.

| Predicate | True when | Use it to turn on |
|---|---|---|
| `certainlyNotProduction()` | the name is in the known non-production list, **staging included** | a **convenience**: stack traces in responses, a relaxed content policy, query dumping, test-mode providers |
| `possiblyProduction()` | the negation of the above — so every unknown or misspelled name too | a **protection**: hiding error detail, masking data, disabling a profiler, refusing a destructive command |
| `certainlyProduction()` | the name is exactly the production one, after trimming and lowercasing | what would **break** anywhere else: strict transport security, secure-only cookies, certificate verification against a real endpoint |
| `localDevelopmentOnly()` | the developer-machine names — **staging excluded** | what must not exist on anything reachable from the internet: auth mocks, check bypasses, destructive seeds, a full profiler |

## 3. How to choose, in one question

> **What happens if this branch lights up where it should not?**

- It **exposes** something or performs a dangerous action → the branch is a *convenience*. Use the predicate
  that stays off when in doubt.
- It **hides** something or hardens behaviour → the branch is a *protection*. Use the predicate that turns
  on when in doubt.
- It would **break** a non-production environment → you need certainty about production specifically.

The asymmetry is the point. A convenience defaults to off, a protection defaults to on, and the unknown
environment gets the safe half of both.

## 4. Staging is not a laptop

Two statements that look alike and are not:

- *"Staging is not production"* — **true**. It belongs in the non-production list, or converting the call
  sites would silently change how staging behaves.
- *"Staging is a developer's machine"* — **false**. It is reachable from the internet and it usually holds
  real data. An auth mock or a full profiler there is a door onto the world.

Hence the fourth predicate: some things are allowed outside production, and some things are allowed only on
a machine nobody else can reach.

## 5. Read it through one layer

Every check goes through a small set of shared predicates, never through a raw read of the variable:

- the raw value is **trimmed and lowercased** once, in one place;
- the list of known names lives in one place, so adding a deployment is one edit;
- with a cached configuration, reading the raw variable directly often returns **empty** — which is exactly
  the unknown case, silently taken as "not production".

Legitimate exceptions exist — framework bootstrap that runs before the layer is available, and the layer
itself. They are few, and they are commented.

## 6. Find the existing ones

```bash
# environment comparisons that should go through the predicates
rg -n "environment\(\s*['\"]production|APP_ENV\s*===?|NODE_ENV\s*===?|ENV\[.APP_ENV" src/ app/
# raw reads outside the predicate layer
rg -n "getenv\(\s*['\"]APP_ENV|process\.env\.NODE_ENV" src/ app/ | rg -v "support/env|config/"
# the inverted-default smell: a protection written as "if not production"
rg -n "if\s*\(\s*!.*production" src/ app/
```

Every hit is a candidate. The question from §3 decides each one.

---

## Gotchas

- **A trailing space is invisible in the file and fatal in the comparison.**
- **`!isDevelopment()` is not `isProduction()`.** The moment you write the negation you have collapsed three
  answers into two.
- **A debug flag and an environment name are two different gates**, and the dangerous configuration is the
  one where either is enough to turn the convenience on.
- **The check that was right when it was written** stops being right when someone adds a deployment with a
  new name. The predicate layer is what makes that a one-line change instead of a search.
- **Test-mode credentials on a real environment fail the same way**, and there the evidence is financial —
  see **`padosoft-payments-reconciliation`**.
- **Nothing here produces an error.** The only symptom is that something worked as designed, in the wrong
  place.

## Checklist

- [ ] No raw comparison against an environment name outside the predicate layer
- [ ] Every branch classified: convenience, protection, or needs certainty
- [ ] Conveniences default to **off** when the environment is unknown
- [ ] Protections default to **on** when the environment is unknown
- [ ] Staging treated as non-production **and** as internet-reachable
- [ ] The raw value normalised once, in one place; the known names in one list
- [ ] Exceptions to the layer are few, and commented

## Final report

```
Call sites reviewed: <n>  ·  converted: <n>
Conveniences: <which predicate, defaults off>
Protections: <which predicate, defaults on>
Needs certainty: <which branches, and what would break elsewhere>
Unknown-environment behaviour: <what happens now>
Remaining raw reads: none | <where, and why>
```

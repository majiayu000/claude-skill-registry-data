---
name: applying-nasa-dod-coding-standards
description: Use when writing production code, reviewing pull requests, refactoring safety-critical or security-critical systems, auditing code for reliability, or establishing quality standards where NASA/DoD-grade engineering discipline is required
---

# Applying NASA & DoD Coding Standards

## Overview

Aerospace and defense software runs where a crash kills people, costs billions, or compromises national security. NASA's Jet Propulsion Laboratory codified this discipline in **"The Power of Ten: Rules for Developing Safety-Critical Code"** (Holzmann, 2006), and the U.S. Department of Defense codified the complementary security discipline in **DISA STIGs**, **CERT Secure Coding**, and the **NIST Secure Software Development Framework (SP 800-218)**.

These rules are not just for rockets and weapons systems. They produce code that is **easier to read, test, statically analyze, and maintain** in any context.

This skill applies those standards to everyday development. The core engineering discipline is **Test-Driven Development** — no production code is written without a failing test first.

**Two rules govern every interaction:**

1. **Firm yet friendly.** State rules clearly, cite them, do not hedge blockers into suggestions — but assume good intent, acknowledge the work, and offer to help.
2. **Always provide 2–3 concrete solutions** when raising an issue or proposing work. Never just identify a problem. Mark the recommended option and note tradeoffs.

## When to Use

**Use when:**
- Writing any production code (feature, bugfix, refactor)
- Reviewing a pull request or merge request
- Auditing existing code for quality, security, or reliability
- Working on safety-critical, security-critical, or financial systems
- Establishing coding standards for a new project
- Onboarding a new contributor

**Do not use when:**
- Throwaway scripts under ~20 lines with no maintenance expected
- Exploratory prototypes that will be rewritten — but **write "will be rewritten before production"** in the file header and link to the follow-up ticket
- Generated code you do not control — fix the generator instead

---

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write a failing test → write the minimum code to pass → refactor with tests green. Every cycle. No exceptions for "simple" changes, "urgent" fixes, or "obvious" code.

**Why this is non-negotiable:**
- Tests-after answer *"what does this code do?"* Tests-first answer *"what should this code do?"*
- Untested code is not complete — it is a liability whose cost has not yet been measured.
- TDD surfaces API-design problems before they are baked in.
- A passing test written *before* the fix is the only proof the fix works and stays fixed.

### Rationalizations That Mean "Stop And Write The Test First"

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks too. The test takes 30 seconds. |
| "I already manually tested it" | Manual tests don't run in CI. They lie about regressions. |
| "I'll add the test after" | You won't. And if you do, it passes trivially, proving nothing. |
| "This is just a prototype" | Prototypes ship. Either test it or document "will be rewritten." |
| "The change is obvious" | Obvious to whom, at 3 a.m., six months from now? |
| "No time" | Debugging the untested version will cost 10× more time. |
| "Refactor doesn't need a test" | Refactors without tests are rewrites. A test proves behavior is preserved. |

---

## The NASA Power of Ten (Adapted for Modern Stacks)

Strict application lets static analyzers actually verify your code. Spirited application produces code humans actually read.

### 1. Simple Control Flow
No `goto`, no `setjmp`/`longjmp`, no unbounded recursion. If recursion is necessary, bound its depth and document the bound in a comment.

### 2. Bounded Loops
Every loop must have a provable upper bound. Forbid infinite loops with internal breaks as the *primary* termination condition. Prefer `for i in range(N)` over `while True:`.

### 3. Minimize Dynamic Allocation After Initialization
Allocate up front where latency or reliability matters. In GC languages, reuse buffers and collections on hot paths. In C/C++/Rust, prefer stack or arena allocation.

### 4. Short Functions — ≤ 60 Lines
One screen, one function, one job. Longer means the problem is not decomposed. If you genuinely need more, document why in a comment *and* extract helpers anyway.

### 5. Assertion Density — ≥ 2 Meaningful Assertions Per Function
Preconditions, postconditions, invariants. Assertions are executable documentation.

| Language | Use |
|---|---|
| Python | `assert` for invariants; raise real exceptions on user-facing boundaries |
| TypeScript | runtime checks (`zod`, `io-ts`) at trust boundaries; `assert` from `node:assert` internally |
| Rust | `debug_assert!`, `assert!`, the type system itself |
| C | `<assert.h>`; bounds-checked APIs |
| Go | explicit `if err != nil` at every call; `panic` only for truly impossible states |

### 6. Minimum Scope
Declare variables as close to use as possible. No module-level mutable state without strong justification. Immutable by default — `const`, `final`, `let`, `val`, `readonly`.

### 7. Validate Inputs, Check Return Values
Every public function validates its parameters. Every caller checks return values — including `Option`/`Result`/`Either`/error types. **Silent failure is a bug.**

### 8. Limit Preprocessor And Metaprogramming
Avoid clever macros, decorators, reflection, and monkey-patching unless they provide a clear, local, documented win. Code should be readable linearly.

### 9. Restricted Pointer / Reference Use
Clear ownership. No more than one level of dereferencing per expression. No function pointers / callbacks without a documented lifecycle. In modern languages: prefer values over references; prefer `Option`/`Result` over nullable pointers.

### 10. Zero Warnings At Maximum Strictness
Compile and lint at the strictest settings your toolchain supports. Treat warnings as errors in CI.

| Language | Minimum toolchain |
|----------|-------------------|
| TypeScript | `strict: true`, `noUncheckedIndexedAccess`, ESLint recommended + project rules |
| Python | `ruff`, `mypy --strict`, `bandit` |
| Rust | `cargo clippy -- -D warnings`, `cargo deny`, `cargo audit` |
| Go | `go vet`, `staticcheck`, `golangci-lint` |
| C / C++ | `-Wall -Wextra -Wpedantic -Werror`, `clang-tidy`, ASan + UBSan |
| Java / Kotlin | Error Prone, SpotBugs, Detekt |

---

## DoD Secure-Coding Baseline

Drawn from DISA STIGs, CERT Secure Coding, NIST SP 800-218 (SSDF), and OWASP ASVS. These are **non-negotiable** on anything touching untrusted input, secrets, or authentication.

1. **Input validation** — validate type, length, range, and format at every trust boundary.
2. **Output encoding** — context-appropriate encoding (HTML, SQL, shell, LDAP, JSON) to prevent injection.
3. **Authentication & authorization** — verify identity, enforce least privilege, re-check on every request.
4. **Secrets management** — never hardcode. Use a vault / secret manager / env var; rotate regularly; never log.
5. **Cryptography** — only vetted libraries (libsodium, AWS KMS, Tink). No custom crypto. Modern algorithms (AES-GCM, ChaCha20-Poly1305, Ed25519, Argon2id). Proper key management.
6. **Error handling** — fail closed; never leak stack traces or internal paths to users; log the details securely server-side.
7. **Logging & audit** — log security-relevant events (auth, authz, config change); never log secrets or PII.
8. **Memory safety** — prefer memory-safe languages; in C/C++ use bounds-checked APIs, ASan, and fuzzing.
9. **Concurrency safety** — immutable data by default; explicit synchronization; no shared mutable state without a documented lock.
10. **Supply chain** — pin dependencies, verify signatures, scan for CVEs (Trivy / Grype / Snyk), generate SBOM (CycloneDX or SPDX).

---

## TDD Workflow — Required For All Code

### RED → GREEN → REFACTOR

1. **RED** — Write a test describing the behavior you want. Run it. Confirm it fails **for the right reason** (not a typo, missing import, or assertion about `undefined`). **Show the actual failing output in your response** — the red test is the receipt that proves the bug was reproduced, and seeing the same output turn green is the proof the fix worked.
2. **GREEN** — Write the **minimum** code to make that test pass. Not more. Not "while I'm here."
3. **REFACTOR** — Improve naming, decomposition, duplication, and structure with tests green. Re-run tests after every structural change.

### The Test Pyramid — All Three Levels Are Required

- **Unit tests** — single function / class, no I/O, <10 ms each. Target 80%+ line coverage of business logic.
- **Integration tests** — components wired together; real database / filesystem / HTTP where practical.
- **End-to-end / acceptance tests** — from the user's perspective; at minimum one happy path and one failure path per user-facing feature.

### Red Flags — Stop And Start Over

- Production code written before the test
- A test that passed on the first run (it wasn't actually testing the new behavior)
- "I already manually tested it"
- "Tests after achieve the same purpose"
- Commented-out tests
- `// TODO: add test`
- A refactor PR with no test changes *and* no test run output in the PR description

**All of these mean: revert the code, restart with a failing test first.**

---

## Using This Skill In Pull-Request Reviews

### PR Size Guidelines

NASA and DoD do not have official, organization-wide PR size limits in their published coding standards. However, government agencies following similar standards provide practical guidance:

- **Aim for PRs under 250-400 lines** when possible
- Department of Veterans Affairs (VA.gov): target 400-500 lines maximum (upper limit of what a reviewer can effectively review in an hour)
- USGS (DOI-USGS): PRs should not change more than 250 lines of code

**If a PR exceeds these limits:**
1. Decompose into smaller, focused PRs
2. Each PR should address a single feature or bug
3. Separate refactoring from feature changes
4. Provide extra review support (detailed descriptions, availability for questions) if a large PR is unavoidable

This aligns with NASA's Power of Ten principle of small, focused units — smaller PRs are easier to review thoroughly, reducing defect risk in safety-critical and security-critical systems.

### Five Gates — Walk Them In Order

Walk **all five gates** and note every finding. Then present them in this order:

1. **Immediate-action items first** — if a secret is committed or an exploit is live, lead with a ⚠️ callout telling the author exactly what to do *right now* (rotate the key, take the endpoint offline), before they finish reading the rest of the review.
2. **Then Gate 3 blockers** — security findings.
3. **Then remaining blockers** (Iron Law, data loss, broken contracts), **then majors, minors, nits** in that order.

Do not stop at the first finding. A review that lists only one blocker when seven exist forces a second review round per issue.

**Gate 1 — TDD discipline**
- A new or updated test exists for every behavior change.
- Commit history shows tests added before or alongside implementation.
- Tests actually fail without the change (revert the implementation locally and re-run).

**Gate 2 — Power of Ten compliance**
- Any function > 60 lines? → flag with 2–3 refactor options.
- Any unbounded loop / recursion? → flag.
- Dynamic allocation in hot paths (if this system cares)? → flag.
- Assertion / input-validation density reasonable? → flag bare public functions.
- Variables declared at broadest possible scope? → flag.
- Unchecked return values / swallowed errors? → flag.
- Clever macros / metaprogramming without local justification? → flag.

**Gate 3 — Security baseline**
- Untrusted input reaching SQL, shell, filesystem, `eval`, or a deserializer without validation + encoding? → **blocker**
- Hardcoded secret / API key / password? → **blocker**
- Custom cryptography? → **blocker**
- Missing authn/authz on a new endpoint? → **blocker**
- Logs containing secrets, tokens, or full PII? → **blocker**

**Gate 4 — Maintainability**
- Naming clear and consistent with the codebase?
- Public APIs documented?
- Error messages actionable (tell the user what to do)?
- No commented-out or dead code?
- No `TODO` without a linked issue?

**Gate 5 — Build & CI**
- Linters, type checkers, static analyzers clean?
- Warnings-as-errors still enabled?
- Dependency additions reviewed for license, CVE, maintenance status?

### Severity Scale

- **Blocker** — must fix before merge (security, data loss, broken contract, missing test for changed behavior).
- **Major** — should fix before merge (Power of Ten violation, missing documentation on a public API).
- **Minor** — fix if easy (naming, small refactor).
- **Nit** — optional preference; reviewer will not block on it.

### Review-Comment Template

```
**[Severity] — [Rule reference]** — <one-sentence statement of the problem and its impact>.

**Options:**
1. **<name>** (recommended): <what to do; why it is the safest or simplest choice>
2. **<name>**: <alternative; when it is better>
3. **<name>**: <fallback; tradeoffs>

I'd lean toward option 1 because <reason>. Happy to draft it if useful.
```

### Worked Examples

#### Long function

> **Major — NASA Power of Ten #4 (function length)** — `processOrder` is 142 lines. Functions over ~60 lines hide bugs, are hard to unit-test, and correlate strongly with defect density in JPL's analysis.
>
> **Options:**
> 1. **Extract by phase (recommended):** split into `validateOrder`, `reserveInventory`, `chargePayment`, `scheduleShipment`. Each becomes independently testable and the top-level function reads as a story.
> 2. **State machine:** encode the order lifecycle (`Pending → Reserved → Charged → Shipped`) as explicit states with transition functions. Better if the flow will grow more steps.
> 3. **Pipeline / `Result` chaining:** compose the steps with `.andThen` / `.flatMap` so failures short-circuit cleanly. Best if you want unified error handling.
>
> I'd start with option 1 — lowest-risk, easiest to review. Happy to sketch the split.

#### Missing test

> **Blocker — TDD Iron Law** — this PR changes `calculateTax` behavior but has no test for the new branch. Our TDD rule requires the test to exist and fail before the implementation.
>
> **Options:**
> 1. **Unit test for the new branch (recommended):** one test for the new case, one per existing case that still matters. Confirm they fail on `main`, then pass on this branch.
> 2. **Property-based test:** if the rules are algebraic (e.g. tax is monotonic in price), `fast-check` / `hypothesis` covers the branch plus edge cases.
> 3. **Golden test:** if the calculation is historically stable, snapshot `(input, expectedOutput)` pairs and assert equality.
>
> Option 1 is the standard here. I can draft it from the diff if you want.

#### Hardcoded secret

> **Blocker — DoD Secrets Management** — `API_KEY = "sk-live-…"` is committed in `config.ts:42`. That key is now in git history permanently and must be considered compromised.
>
> **Options:**
> 1. **Rotate + env var (recommended):** revoke the key at the provider immediately, issue a new one, load from `process.env.API_KEY`, fail fast at startup if missing.
> 2. **Secret manager:** pull from AWS Secrets Manager / Vault / GCP Secret Manager at startup. Better if you already have one configured and want rotation enforced.
> 3. **Per-environment file outside VCS:** `.env.local` gitignored, committed `.env.example`. Cheapest, weakest; only acceptable for local-only dev secrets.
>
> Please do the revoke step of option 1 *before anything else* — the key is already exposed.

---

## Communication Rules

### Firm

- State violations clearly: *"this violates Power of Ten #4"* — not *"this might possibly be long."*
- Don't soften blockers into suggestions.
- Don't apologize for enforcing standards.
- Cite the rule: Power of Ten #N, CERT INTxx-C, OWASP Ax, NIST SP 800-218 PW.x, DISA STIG category.

### Friendly

- Assume good intent.
- Acknowledge the work.
- Offer to help with the fix.
- Use "we" and "let's" when proposing changes.
- Recognize tradeoffs honestly.

### Always 2–3 Solutions

When raising an issue or proposing work, **never just identify a problem**. Provide 2–3 concrete solutions with tradeoffs and mark the recommended one.

Why 2–3:
- **1** option feels like an ultimatum and is often not the best fit.
- **2–3** options force you to think about tradeoffs.
- **4+** options dilute the recommendation.

Always structure as:
```
1. **<Option A>** (recommended): <what + why this one>
2. **<Option B>**: <what + when it is better>
3. **<Option C>**: <fallback + tradeoffs>
```

Apply the rule even to small questions ("where should this file go?") — three plausible locations, pick one.

### Quote-and-Counter

When a user invokes one of the rationalizations from the tables in this skill ("too simple to test", "just this once", "we'll fix tomorrow", "tech lead approved"), **quote their exact phrase** back and cite the counter from the table. This is more persuasive than paraphrasing, and it shows you heard them:

> Your words: *"I'll add tests after we're back online, I promise."*
> Skill's counter: *"You won't. And if you do, it passes trivially, proving nothing."*

Then give the 2–3 options. Do not lecture.

### The Refusal Template — For Blockers Only

Blockers (DoD secure-coding blockers, the Iron Law, data-loss risks) do not get hedged into suggestions. When a request would cross a blocker, open with an explicit refusal, provide 2–3 options that all **stay inside the rule**, and close with the same refusal restated:

```
**I will not <the specific action being refused>.**
Rule: <citation — e.g. DoD Secure-Coding Baseline #4 / NIST SP 800-218 PW.1>
Why this is a blocker: <one sentence on the concrete harm>.

Here's what I will do instead — pick one:
1. **<Option A>** (recommended): … (keeps you inside the rule, fastest)
2. **<Option B>**: … (alternative, when it's better)
3. **<Option C>**: … (fallback, tradeoffs)

… <2–3-sentence offer to pair / help execute> …

**What I will NOT do:** <restate the refused action, verbatim>.
```

The closing "What I will NOT do" line is not optional. It removes the "well, if you really insist…" escape hatch — which, left open, is where every hardcoded secret, skipped test, and suppressed lint rule gets born. **Blockers have no escape hatches.**

Options offered under a refusal must **all satisfy the rule**. Never list "just do it anyway" as an option, even framed as "if you insist." The correct response to "if you insist" is to re-state the refusal and offer to escalate to a human decision-maker (tech lead, security, on-call manager) — **you** do not ship the violation.

---

## Working Checklist (Print-Friendly)

Run through this before asking for review or marking a task done.

**TDD**
- [ ] Wrote a failing test first
- [ ] Saw it fail for the right reason
- [ ] Wrote the minimum code to pass
- [ ] Refactored with tests green
- [ ] All tests pass locally and in CI

**Power of Ten**
- [ ] Control flow is simple (no `goto`; bounded recursion)
- [ ] Every loop has a provable upper bound
- [ ] No unbounded dynamic allocation on hot paths
- [ ] All functions ≤ 60 lines
- [ ] Meaningful assertions / input validation in every public function
- [ ] Variables at minimum scope, immutable by default
- [ ] Return values / error types checked at every call site
- [ ] No clever metaprogramming without local justification
- [ ] References / pointers have clear ownership
- [ ] Linters, type checkers, static analyzers clean at maximum strictness

**Security (DoD baseline)**
- [ ] Inputs validated at every trust boundary
- [ ] Outputs encoded for their destination context
- [ ] No hardcoded secrets
- [ ] No custom cryptography
- [ ] AuthN/AuthZ enforced on new endpoints
- [ ] Logs do not contain secrets or PII
- [ ] Dependencies pinned and scanned (SBOM generated)

**Review readiness**
- [ ] PR size under 250-400 lines when possible (decompose if larger)
- [ ] PR addresses a single feature or bug
- [ ] Refactoring separated from feature changes
- [ ] Commit messages explain *why*, not just *what*
- [ ] Public API changes documented
- [ ] No `TODO` without a linked issue
- [ ] No commented-out code

---

## Common Rationalizations And Counters

| Rationalization | Counter |
|-----------------|---------|
| "NASA rules don't apply to web code" | Bugs in web code cost companies billions (Knight Capital, CrowdStrike, Cloudflare outages). The rules are about control flow and testability — universal. |
| "We move fast, we can't do TDD" | Teams that do TDD ship faster long-term because they spend less time debugging. Measure cycle time, not lines-of-code per day. |
| "60-line limit is arbitrary" | It is. It's also a forcing function that catches hidden complexity. Push back with data if a function genuinely needs more — but the default answer is "split it." |
| "Static analyzers give false positives" | Tune them or suppress with a justification comment. Don't disable wholesale. A false-positive suppression is cheaper than a real bug. |
| "This is just a prototype" | Prototypes ship. Apply the standard, or write in the PR description "will be rewritten before production, tracking in `<ticket>`." |
| "Reviewer should just fix it" | Reviewer's job is to find issues and guide. Author's job is to fix. Offering 2–3 solutions respects that boundary. |
| "Tests slow down velocity" | Debugging production incidents slows velocity far more. Track MTTR alongside throughput. |

---

## Red Flags — Stop The Work

If you catch yourself doing any of these, stop and reset:

- Writing implementation before the test
- Marking a PR "ready for review" with failing or missing tests
- Disabling a lint rule or test to "unblock" a merge
- Committing a secret, even temporarily
- Adding a dependency without reviewing license, maintenance, and CVE history
- Reviewing a PR by only reading the diff summary, not the code
- Approving a PR without running it
- Saying "LGTM" with no specific feedback
- Filing an issue without proposing 2–3 possible fixes

---

## References

- Holzmann, G. J. (2006). *The Power of Ten: Rules for Developing Safety-Critical Code.* NASA/JPL. IEEE *Computer* 39(6), 95–99.
- NASA-STD-8739.8 — Software Assurance and Software Safety Standard
- NASA NPR 7150.2 — Software Engineering Requirements
- NIST SP 800-218 — Secure Software Development Framework (SSDF)
- DISA — Application Security and Development STIG
- CERT Secure Coding Standards, Software Engineering Institute, Carnegie Mellon
- MISRA-C / MISRA-C++ Guidelines
- OWASP Application Security Verification Standard (ASVS) and OWASP Top 10
- Beck, K. (2002). *Test-Driven Development: By Example.* Addison-Wesley.

---

## The Bottom Line

- Every change: **test first, minimum code, strict analysis, 2–3 solutions when raising an issue.**
- Every review: **five gates in order, firm tone, friendly delivery, always three paths forward.**
- No exceptions — **violating the letter of the rules is violating the spirit.**

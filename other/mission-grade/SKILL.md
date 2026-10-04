---
name: mission-grade
description: >
  Use this skill when writing, refactoring, or reviewing production code. It applies NASA/DoD
  engineering standards to the code and ASD-STE100 Simplified Technical English rules to the
  prose that ships with it — comments, docstrings, error messages, identifiers, and commit
  messages. Triggers include: "write", "implement", "refactor", "clean up", "review this code",
  "code review", "mission grade", "nasa-dod", "safety-critical", "production-ready", or any
  request to add a feature, fix a bug, or improve existing code. Also use it when establishing
  coding standards for a project, auditing code for reliability or security, or preparing a
  pull request.
---

# mission-grade

Applies two standards at once, from one trigger:

- **NASA/DoD engineering standards** to the code — the Power of Ten, the DoD secure-coding
  baseline, and test-driven development.
- **ASD-STE100 mechanical writing rules** to the prose that ships with the code — comments,
  docstrings, error messages, identifiers, and commit messages.

This skill is self-contained. It needs no other skill to function.

---

## The dividing line

**STE governs the artifact. NASA/DoD governs the conversation about the artifact.**

If it is committed to the repository, STE binds it. If it is you talking to the user — a
finding, a rule citation, a gate result, a chat reply — NASA/DoD's communication rules bind it
and STE does not apply.

That one line resolves every conflict between the two standards. Apply it before reaching for
any other rule.

---

## Surface map

| Surface | Governed by | STE mode |
|---|---|---|
| Procedural comments (how-to, setup steps) | STE | `strict` |
| Rationale comments (why a decision was made) | STE | `clear` |
| Docstrings, module headers | STE | `clear` |
| Identifiers | STE word rules only | word rules only — see `references/ste-for-code.md` |
| Error, log, and CLI-help strings | STE | `strict` |
| Commit messages, PR descriptions | STE | `clear` |
| Review findings, rule citations, callouts, gate status, option lists | NASA/DoD | exempt |
| Chat replies about the work | NASA/DoD | exempt |

The table is fixed. Do not offer to change it, and do not adjust it on request. If the `nfc`
skill is available in this environment, point the user there for freely selectable modes; if it
is not, say so in one line and leave the table as it stands.

**Procedural or rationale?** A comment is procedural if it tells the reader to do something:
setup steps, an ordering the caller must obey, a manual recovery procedure. It is rationale if
it explains why the code is as it is. When a comment does both, split it — the procedural part
becomes a numbered list in `strict`, the rationale stays in prose in `clear`. When the split is
not worth it, apply `clear` and put any instruction on its own line.

### The two modes, in full

`clear` — every sentence 25 words or fewer. Paragraphs 6 sentences or fewer, one topic each.
Active voice; passive only where the actor is genuinely unknown. Simple present, past, or
future. Articles required. State the conclusion first, then the reasoning. Define a technical
term on first use. Use a list for any 3 or more items.

`strict` — everything in `clear`, and: procedural sentences 20 words or fewer. Exactly one
instruction per sentence. Imperative verb first in every step. No present perfect — use the
simple past. No `-ing` form except as a technical noun. Noun clusters 3 words or fewer. Never
drop an article. No idioms, metaphors, or figures of speech. No emoji. Hedge only when the
uncertainty is real, and state its cause. Put a warning before the step it applies to.

---

## Precedence

Apply in this order. A higher rule beats a lower one.

**1. Accuracy wins over everything.** If an STE constraint would make a comment, docstring, or
error message wrong, misleading, or falsely certain, keep it accurate and state in one line
which constraint you relaxed and why. This applies to accuracy only. It is never an escape
hatch for convenience, brevity, or effort.

**2. NASA/DoD wins over STE.** Wherever the two give conflicting instructions on the same
output, follow NASA/DoD.

**3. STE binds everything else** the surface map assigns to it.

### The three resolved conflicts

**Emoji.** NASA/DoD requires a warning callout for immediate-action items and a status marker
for a blocked gate. STE prohibits emoji. Both hold: emoji are **required** in review output and
callouts, and **prohibited** in comments, docstrings, and user-facing strings.

**Explanation versus sentence caps.** "Cite the rule, state the failure mode, give 2-3 options
with tradeoffs" is explanatory prose, and `strict` caps sentences at 20 words. Findings and
tradeoff prose are conversation side, so the caps never touch them. State a genuinely
conditional tradeoff as conditional.

**Identifier naming versus codebase consistency.** STE caps noun clusters at 3 words and
requires one term per concept. NASA/DoD requires naming consistent with the surrounding
codebase. **Consistency wins.** STE word rules apply only to concepts the current change
introduces. Do not rename existing symbols to satisfy cluster length. Do not offer such renames
unless the user asks — a sweeping rename is its own pull request.

**Quoted material is never rewritten.** STE applies to prose you author, never to code, output,
or text you cite.

---

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write a failing test, watch it fail for the right reason, write the minimum code to pass, then
refactor with tests green. Every cycle. No exception for "simple", "urgent", or "obvious".

Show the failing output in your reply. The red test is the receipt that proves the bug was
reproduced, and the same output turning green is the proof the fix worked.

When the user offers a reason to skip it — "too simple to test", "I already tested it
manually", "I'll add the test after", "it's just a prototype", "no time" — quote their exact
words back, give the counter, then give 2-3 options that all keep the test. Do not lecture.

| Excuse | Counter |
|---|---|
| "Too simple to test" | Simple code breaks too. The test takes 30 seconds. |
| "I already tested it manually" | Manual tests do not run in CI. They lie about regressions. |
| "I'll add the test after" | You will not. If you do, it passes trivially and proves nothing. |
| "It's just a prototype" | Prototypes ship. Test it, or write "will be rewritten" in the header. |
| "The change is obvious" | Obvious to whom, at 3 a.m., six months from now? |
| "No time" | Debugging the untested version costs 10x more time. |

---

## NASA Power of Ten

1. **Simple control flow.** No `goto`, no `setjmp`/`longjmp`, no unbounded recursion. Bound any
   recursion you need and document the bound.
2. **Bounded loops.** Every loop has a provable upper bound. Prefer a counted loop over
   `while True` with an internal break as the primary exit.
3. **Minimize dynamic allocation after initialization.** Allocate up front where latency or
   reliability matters. Reuse buffers on hot paths.
4. **Functions of 60 lines or fewer.** One screen, one function, one job. If you genuinely need
   more, document why and extract helpers anyway.
5. **Two or more meaningful assertions per function.** Preconditions, postconditions,
   invariants. Assertions are executable documentation.
6. **Minimum scope.** Declare variables close to use. Immutable by default. No module-level
   mutable state without strong justification.
7. **Validate inputs, check return values.** Every public function validates its parameters.
   Every caller checks what it gets back, including `Option`, `Result`, and error types. Silent
   failure is a bug.
8. **Limit metaprogramming.** No clever macros, decorators, reflection, or monkey-patching
   without a clear, local, documented win. Code should read linearly.
9. **Clear ownership of references.** One level of dereferencing per expression. Prefer values
   over references, and `Option`/`Result` over nullable pointers.
10. **Zero warnings at maximum strictness.** Lint and type-check at the strictest setting the
    toolchain supports. Warnings are errors in CI.

| Language | Minimum toolchain |
|---|---|
| TypeScript | `strict: true`, `noUncheckedIndexedAccess`, ESLint |
| Python | `ruff`, `mypy --strict`, `bandit` |
| Rust | `cargo clippy -- -D warnings`, `cargo deny`, `cargo audit` |
| Go | `go vet`, `staticcheck`, `golangci-lint` |
| C / C++ | `-Wall -Wextra -Wpedantic -Werror`, `clang-tidy`, ASan + UBSan |
| Java / Kotlin | Error Prone, SpotBugs, Detekt |

---

## DoD secure-coding baseline

Non-negotiable on anything touching untrusted input, secrets, or authentication.

1. **Input validation** — type, length, range, and format at every trust boundary.
2. **Output encoding** — context-appropriate for HTML, SQL, shell, LDAP, or JSON.
3. **Authentication and authorization** — verify identity, enforce least privilege, re-check on
   every request.
4. **Secrets management** — never hardcode. Use a vault, secret manager, or environment
   variable. Rotate. Never log.
5. **Cryptography** — vetted libraries only. No custom crypto. Modern algorithms, proper key
   management.
6. **Error handling** — fail closed. Never leak a stack trace or an internal path to a user.
7. **Logging and audit** — log security-relevant events. Never log secrets or PII.
8. **Memory safety** — prefer memory-safe languages. In C/C++ use bounds-checked APIs and
   sanitizers.
9. **Concurrency safety** — immutable by default, explicit synchronization, no shared mutable
   state without a documented lock.
10. **Supply chain** — pin dependencies, verify signatures, scan for CVEs, generate an SBOM.

---

## Flow: writing code

1. **RED** — Write the failing test. Its failure message is artifact prose, so `strict` binds
   it. Its name follows the identifier word rules; descriptive test names are exempt from the
   cluster cap. Run it. Confirm it fails for the right reason, not on a typo or a missing
   import. Show the output.
2. **GREEN** — Write the minimum code to pass. Nothing more. Check each new identifier against
   the word rules as you choose it, not afterward.
3. **REFACTOR** — Improve structure with tests green. Write docstrings and rationale comments
   to `clear`, and procedural comments to `strict`. Write error strings to `strict`. Re-run the
   tests after every structural change.
4. **COMMIT** — Write the message to `clear`, with an imperative subject line, and explain why
   rather than what.

## Flow: refactoring

Tests must exist before the refactor starts. A refactor without tests is a rewrite.

Behavior preservation includes names. STE word rules bind only concepts this change introduces.
Leave existing symbols alone, even when they break cluster length. Do not bundle a rename into
an unrelated refactor.

## When not to use this skill

- Throwaway scripts under about 20 lines with no maintenance expected.
- Exploratory prototypes — but write "will be rewritten before production" in the file header
  and link the follow-up ticket.
- Generated code you do not control. Fix the generator instead.

---

## Flow: reviewing code

Walk all six gates in order. Collect every finding before you report any. A review that reports
one blocker when seven exist forces a second round per issue.

**Gate 1 — TDD discipline.** A new or changed test exists for every behavior change. Tests fail
without the change.

**Gate 2 — Power of Ten.** Functions over 60 lines. Unbounded loops or recursion. Bare public
functions with no validation or assertions. Unchecked return values. Variables at the broadest
scope. Metaprogramming without local justification.

**Gate 3 — Security baseline.** Untrusted input reaching SQL, a shell, the filesystem, `eval`,
or a deserializer without validation. A hardcoded secret. Custom cryptography. A new endpoint
with no authn/authz. Logs holding secrets or PII. **Each of these is a blocker.**

**Gate 4 — Maintainability.** Naming consistent with the codebase. Public APIs documented.
Error messages actionable. No dead or commented-out code. No `TODO` without a linked issue.

**Gate 5 — Build and CI.** Linters, type checkers, and static analyzers clean. Warnings still
errors. New dependencies reviewed for license, CVEs, and maintenance status.

**Gate 6 — Prose.** Artifact prose against the mode the surface map assigns it. Inspect:

- A warning or caution placed after the step it applies to
- A comment or docstring that contradicts the code
- An error string that hedges instead of naming an action
- A new identifier introducing a second term for a concept the module already names
- An idiom, metaphor, or emoji in shipped prose
- Undefined jargon on first use in a public docstring

Severity tracks harm, not rule count. A destructive warning sitting below its step is a
blocker. A 4-word noun cluster on a new helper is a nit. Full mapping and the not-a-finding
list: `references/prose-gate.md`.

### Report order

1. **Immediate-action items first.** If a secret is committed or an exploit is live, open with a
   ⚠️ callout telling the author exactly what to do right now — before they read anything else.
2. Gate 3 security blockers.
3. Remaining blockers, then majors, then minors, then nits.

Open the report by acknowledging what the code does well. State the gate result: 🔴 blocked when
a blocker exists, ✅ passed when none does.

### Every finding carries 2-3 options

Never just identify a problem. One option reads as an ultimatum. Four dilute the recommendation.

```
**[Severity] — [Rule citation]** — <the problem and its concrete impact, in one sentence>.

**Options:**
1. **<name>** (recommended): <what to do; why it is safest or simplest>
2. **<name>**: <alternative; when it is better>
3. **<name>**: <fallback; tradeoffs>

I'd lean toward option 1 because <reason>. Happy to draft it.
```

Cite the rule by name and number: Power of Ten #4, DoD baseline #4, Gate 6, CERT INTxx-C,
OWASP Ax, NIST SP 800-218 PW.x.

Be firm and friendly at once. State violations plainly — "this violates Power of Ten #4", not
"this might possibly be long". Do not soften a blocker into a suggestion. Do not apologize for
the standard. Assume good intent, acknowledge the work, and offer to help with the fix.

### Refusing a blocker

A blocker has no escape hatch. When a request would cross one:

```
**I will not <the specific action>.**
Rule: <citation>
Why this is a blocker: <one sentence on the concrete harm>.

Here's what I will do instead — pick one:
1. **<Option A>** (recommended): …
2. **<Option B>**: …
3. **<Option C>**: …

**What I will NOT do:** <restate the refused action, verbatim>.
```

Every option must satisfy the rule. Never list "do it anyway" as an option, even framed as "if
you insist". The answer to "if you insist" is to restate the refusal and offer to escalate to a
human decision-maker. You do not ship the violation.

---

## Self-check

This is the working checklist too. Run it against your draft before you send it, and run it
before you mark any task done. Do not narrate the check in your output.

1. Does every new identifier reuse the module's existing term for the concept?
2. Does any warning sit below the step it applies to?
3. Does every error string name an action the reader can take?
4. Is there an idiom, metaphor, or emoji anywhere in shipped prose?
5. Does every public function meet its 60-line limit, its assertion density, and its input
   validation?
6. Does every changed behavior have a test that failed first?
7. Is any secret hardcoded, and does any log line carry a secret or PII?
8. Is there dead code, an undocumented public API, or a `TODO` with no linked issue?
9. Do the linters and type checkers pass at their strictest setting?

If a check fails, fix it and re-run that check. Do not send output that fails a check.

---

## Going deeper

This skill is self-contained. Everything above works with no other file loaded. The files below
add depth when a task needs it. **If a path does not exist, say so in one line and continue with
what you have** — never block on a missing optional file.

**This skill's own references** — always present:

| File | Load when |
|---|---|
| `references/ste-for-code.md` | Naming a new concept, writing a user-facing string, or applying the substitution table |
| `references/prose-gate.md` | Classifying a Gate 6 finding, or deciding whether something is a finding |
| `references/examples.md` | You want a worked end-to-end run before starting |

**Sibling skills** — optional, may be absent:

| Source | Provides |
|---|---|
| `skills/nfc/` | The full ASD-STE100 substitution table, `[STE]` versus `[NFC]` rule provenance, and the list of STE rules this skill does not implement |
| `skills/applying-nasa-dod-coding-standards/` | Full gate prose, the complete rationalization-counter tables, and the long-form refusal template |
| `skills/nasa-dod-code-review/` | The formal report workflow — CODEOWNERS setup, P0-P3 severity, and a written report under `reports/`. Load this only when the user explicitly asks for a written report file. |

If the user has obtained the official ASD-STE100 specification and saved it at
`skills/nfc/references/ASD-STE100.pdf`, check word choices against it in `strict` mode. It is
not vendored with this repository.

---

## Scope

This skill does not:

- Change facts, conclusions, or recommendations to make them simpler than they are.
- Remove real uncertainty. If something is genuinely unknown, say so plainly and say why.
- Rewrite code, commands, output, or quoted material. Reproduce those exactly.
- Rename existing identifiers as a side effect of unrelated work.
- Certify ASD-STE100 conformance. It improves clarity. Do not claim more than that.

---

## Attribution

The mechanical writing rules are derived from ASD-STE100 Simplified Technical English, Issue 9
(January 2025), copyright ASD (AeroSpace and Defence Industries Association of Europe),
maintained by the STE Maintenance Group. This skill implements the writing rules only. It does
not reproduce the ASD-STE100 approved-word dictionary, which is ASD's copyrighted content.
Obtain the official specification, including the dictionary, free of charge from
<https://www.asd-ste100.org/STE_downloads.html>.

This skill is an independent work and is not endorsed by or affiliated with ASD or the STEMG.

Engineering standards derive from Holzmann, G. J. (2006), *The Power of Ten: Rules for
Developing Safety-Critical Code*, NASA/JPL, IEEE Computer 39(6), 95-99; NIST SP 800-218
(Secure Software Development Framework); the DISA Application Security and Development STIG;
and the CERT Secure Coding Standards.

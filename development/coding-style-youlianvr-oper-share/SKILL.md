---
name: coding-style
description: >-
  Use when writing or reviewing code for clear intent, project conventions,
  verified APIs/dependencies, coherent scope and maintainability. Ponytail is
  the main-route simplicity method; this part covers code-level execution and
  optional complexity diagnostics. No mandatory persona, test quota or fixed
  report format.
---

# Coding style — obvious code, verified assumptions

The goal is a correct maintainable implementation in this project, not the
shortest snippet or a generic house style. This contract draws on the previously
merged Karpathy/minimalist methods. The maintained simplicity route is
`skills/dev/parts/ponytail/` under `dev`; read it for substantial build/repair decisions or an
explicit Ponytail request. Historical source references are provenance, not extra
instructions to reactivate.

## Ground the change

- Read the current implementation, affected callers, tests and dependency/lock
  files. Inspect versions and exports yourself; do not ask the owner to supply
  files or API facts already accessible through the host.
- Use APIs actually available in the project's installed/target version. Verify
  unfamiliar or volatile behavior against source/docs or a narrow executable
  check. A comment saying "ASSUMED: verify later" does not turn invented code
  into a complete implementation.
- Resolve uncertainties that affect correctness before relying on them. Localize
  independent work rather than freezing a whole task over an unrelated unknown.
  Ask when remaining intent/access is genuinely user-only or consequential.
- Match existing libraries and conventions. Do not introduce a framework because
  a skill's example uses it or assume another framework's similarly named API.

## Scope and clarity

- Every material change should serve the request or its understood root cause.
  No unrelated style churn or cleanup; previously written code is working base,
  not untouchable territory and not disposable.
- Prefer explicit names, straightforward control flow and useful boundaries.
  Avoid dense ternaries, compressed one-liners and abstractions for imaginary
  growth. Do not remove a real interface simply because it has one implementation.
- Preserve public contracts/compatibility where consumers require them. A facade
  is not automatically a hack; an unused compatibility layer is not automatically
  worth retaining. Inspect actual consumers.
- Leave no placeholders on the claimed working path. Intentional abstract methods,
  protocol declarations or scoped unfinished work are different from fake
  implementation; label the scope honestly.
- Explain deliberate, load-bearing trade-offs at the owning location. Avoid
  mandatory comment labels or duplicated reasoning in every carrier.

## Checks fit the behavior

Use existing test frameworks and fixtures; no forced one-check-per-change rule
and no ban on a suite. `discipline/parts/testing-discipline` covers meaningful
behavior, independent expectations and safe sensitivity. `systematic-debugging`
covers repairs; `verification-before-completion` covers final evidence.

A small diff is not evidence of safety. Inspect the final files/diff and run the
applicable checks through the affected consumers. Removal follows trash/data-
preservation boundaries; never discard code to satisfy a process rule.

## Optional diagnostics and complexity budget

The bundled Python scripts are heuristic review aids, not proof of correctness
or authorization for a rewrite. Read their source before use, constrain the target
and validate any finding against actual behavior. No score guarantees quality.

| Script under this part's `scripts/` | Limited signal |
|---|---|
| `complexity_checker.py` | Regex/indentation estimates of length, branching, imports and class density, not compiler-grade complexity |
| `diff_surgeon.py` | Pattern hints about comments/style changes; cannot determine the goal or whether a change is necessary |
| `assumption_linter.py` | Plan-language heuristics, not knowledge of actual intent or dependency availability |
| `goal_verifier.py` | Success-criteria phrasing hints, not verification of a running deliverable |

Presets for `complexity_checker.py` remain in its source (`strict`, `medium`,
`relaxed`); do not duplicate their numbers in prose. Exceeding a preset is a
review signal: justify the coherent unit or refactor where that improves the real
code. Do not split merely to pass a heuristic. Its exit status/report is not a
project typecheck, linter or runtime test.

Example invocation from the workspace root:

```bash
python .agents/skills/dev/parts/coding-style/scripts/complexity_checker.py path/to/file.py --threshold medium
```

`path/to/file.py` is a placeholder, not a workspace file. No command here implies
automatic hook/CI/client installation; host-loading claims need current evidence.

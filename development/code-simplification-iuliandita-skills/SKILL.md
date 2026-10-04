---
name: code-simplification
description: "Review code for dead code, duplication, overengineering, invented APIs, and weak tests. Report safe reductions; no edits."
license: MIT
compatibility: "Works on any codebase. Optional: git (diff scope), rg (no-reference searches), and the project's configured non-mutating linters"
metadata:
  source: iuliandita/skills
  date_added: "2026-09-20"
  effort: medium
  argument_hint: "[scope-or-diff]"
---

# Code Simplification

Review code for unnecessary complexity, ungrounded implementation choices, and safe reductions. Preserve behavior and report evidence in maintainability or reduction mode.

1. **Maintainability**: over-abstraction, generic naming, noisy comments, invented APIs or configuration, stale idioms, dependency creep, and weak tests.
2. **Safe reduction**: dead or superseded code, orphan files, exact clones, redundant wrappers, inert defensive scaffolding, and comment walls.

Smaller code is not automatically better. A finding needs a concrete maintenance or correctness cost, an invariant, and evidence that the proposed change preserves contracts.

## When to use

- Review code or a PR for unnecessary complexity, AI-shaped code, grounded API use, and useful tests.
- Find behavior-preserving reductions before a cleanup change.
- Check a removal or refactor diff for lost behavior, fallbacks, or reachable entry points.

## When NOT to use

- Find logic bugs, races, or regressions: use **code-review**.
- Find vulnerabilities or secrets: use **security-audit**.
- Rewrite prose for voice: use **anti-ai-prose**.
- Run a repository-wide multi-lens audit: use **repo-audit**.
- Implement a cleanup: use the relevant language or framework skill.

## Workflow

1. **Scope:** prefer the named path or diff; otherwise inspect uncommitted changes, then the current branch against its confirmed integration base. Record generated, vendored, and unreviewed areas.
2. **Establish context:** read instructions, manifests, runtime versions, public exports, registries, route/CLI/plugin discovery, and existing validation. For maintainability mode, load `references/maintainability-patterns.md` and each relevant language or infrastructure reference; for reduction mode, load `references/patterns.md` and `references/reduction-patterns.md`. Load `references/research-sources.md` only when citations help.
3. **Make a maintainability pass:** inspect scripts and configuration before running any baseline tooling. Run only configured, non-mutating check commands; never use `--fix`, `--write`, `apply`, or an unknown script. Then inspect comments, naming, types, wrappers, error handling, dependencies, API/config claims, and tests. Verify suspicious APIs with local types, schemas, lockfiles, `--help`, or primary documentation before calling them invented.
4. **Make a safe-reduction pass:** search for dead and superseded code, leftovers, clones, one-literal-per-function copies, redundant parsers, thin wrappers, and inert catches. Read each candidate, a caller, and relevant tests.
5. **Prove or defer:** search with `rg -n` (use `grep -rn` when `command -v rg` fails). A deletion needs no-reference proof that rules out public APIs, reflection, dynamic dispatch, DI, serialization, route/CLI/plugin registration, conditional builds, and test discovery. Preserve boundary guards, recoveries, retries, cleanup, observability, compatibility, and intentional provider divergence.
6. **Classify:** use `Do now` only for mechanically proven, behavior-preserving reductions; `Do with tests` when focused validation is missing; `Defer` for broad, hot-path, or uncertain work; `Leave alone` when the current shape carries a contract. Also classify maintainability findings as Noise, Lies, or Soul and as Fix, Consider, or Fine (defined in `references/maintainability-patterns.md`); project conventions and framework idioms override generic style rules.
7. **Report:** write an audit deliverable using `references/report-templates.md`. Group repeated examples into one finding and include location, evidence, invariant, proposed shape, tradeoff, and validation needed.

## AI Self-Check

- [ ] Every API, CLI flag, schema key, and version-sensitive replacement is grounded in the target project.
- [ ] Every safe-reduction finding states its preserved behavior and no-reference or behavior-specific evidence.
- [ ] Tests are judged by behavior and acceptance criteria, not mock volume or coverage alone.
- [ ] Framework conventions, public contracts, intentional duplication, and separate trust boundaries were checked.
- [ ] Findings are honest about priority and use one representative example for repeated patterns.
- [ ] Cross-cutting hygiene is applied from `references/agent-hygiene.md`.

## References

- `references/maintainability-patterns.md` - quality, grounding, test, and language prompts.
- `references/language-patterns.md` - condensed cross-language quality and preservation prompts; read for a quick mixed-language pass, then open the detailed file for any language with candidate findings.
- `references/typescript.md`, `python.md`, `shell.md`, `rust.md`, `docker.md`, and `iac.md` - detailed language and infrastructure prompts.
- `references/patterns.md` - detailed safe-reduction classification and no-reference guidance.
- `references/research-sources.md` - optional source context when citations help.
- `references/reduction-patterns.md` - dead-code and behavior-preserving reduction proofs.
- `references/report-templates.md` - audit and removal-review deliverables.
- `references/output-contract.md` - required reporting format.

## Output Contract

Use `references/output-contract.md`.

- **Skill name:** CODE-SIMPLIFICATION
- **Deliverable:** `docs/local/audits/code-simplification/<YYYY-MM-DD>-<slug>.md`
- **Mode:** always-on for audits and reviews; answer a factual question without a deliverable.
- **Priority:** P0-P3 and info. A simplification finding is normally P2 or P3; route correctness and security impact to its owning audit.

## Rules

- Do not edit source, write tests, or present a recommendation as an authorized change.
- Do not flag security controls, validation at external boundaries, intentional compatibility layers, cleanup in `finally`, retries, logging/metrics/tracing, feature flags, or policy boundaries merely because they add code.
- Do not call a symbol unused from a static search alone. Treat generated output as owned by its generator or schema.
- Keep distinct DTOs across trust, lifecycle, persistence, queue/event, and response boundaries unless a shared validated contract is explicit.
- Preserve performance-sensitive explicit code until measurement supports a change.
- Route correctness and security findings instead of laundering them into simplification.

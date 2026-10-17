---
name: skill-author
description: Author and structure practical Robium skills without unnecessary context or ceremony.
---

# Skill author

Treat every loaded line as a cost. A skill earns that cost by changing an
ordinary coding agent's decision.

## Start with the trigger

- Give the skill one clear job and a short name that matches its directory.
- Write a brief description that says what the skill helps accomplish and
  distinguishes it from its closest neighbors.
- Do not turn the description into a keyword inventory. Test realistic user
  requests when the boundary is uncertain.
- If an existing skill already owns the decision, deepen it instead of adding
  another trigger surface.

## Write the entrypoint

- Frontmatter contains only `name` and `description`.
- Organize `SKILL.md` around one useful mental model, not a universal template.
- Prefer short, natural bullets that a human can scan without decoding process
  language.
- Assume the agent can already code, search a repository, and read ordinary
  documentation. Keep only constraints, choices, and failure patterns that
  materially improve its work.
- Avoid fixed sequences unless order protects correctness, safety, money, or
  external state.
- Mention another skill only where evidence crosses that skill's boundary.

## Put depth behind links

- Keep the common path in `SKILL.md`. Put conditional commands, failure
  diagnosis, tuning, platform compatibility, schemas, and substantial examples
  in focused supporting files.
- Link each supporting file at the point where it becomes useful and say when
  to read it. Do not load every reference by default.
- Reuse a focused existing file before creating another layer of navigation.
- Preserve exact Robium-observed values with their measured conditions. They
  are evidence, not universal defaults.
- Use current official documentation for volatile APIs, flags, packages, and
  configuration. Do not copy a manual into the skill.
- Keep executable helpers only when deterministic reuse justifies maintaining
  code; keep examples only when they show something prose cannot.

## Test usefulness

- Read [QUALITY.md](QUALITY.md) for the review bar and mechanical checks.
- Run `uv run skills/skill-author/scripts/validate_skills.py` once after a
  coherent batch of skill changes, not after every edit. It checks the
  lightweight contract, not writing quality.
- For description, routing, or behavioral changes, review one common request,
  one likely failure, and one neighboring request that should route elsewhere.
  A typo or source-link refresh needs only the relevant mechanical check.
- Start with manual scenario review. Run bounded live-agent evals only for
  unresolved behavioral uncertainty, meaningful regression evidence, or an
  explicit request; do not rerun every model or prompt after each prose edit.
- Prefer observable behavior checks over tests that assert headings or exact
  prose. Keep `evals.yaml` only when a real routing or task regression is worth
  preserving.

## Done

- The entrypoint is small enough to load routinely.
- Optional detail is discoverable without being injected into every task.
- Every strong claim is either stable, sourced upstream, or tied to observed
  conditions.
- There is no version field, changelog, README, or format-only section.

---
name: derivation-step-checker
description: 当手上有一份已经写好的推导、要逐步核验时使用。每一步查四件事：代数是否等价、量纲是否一致、符号有没有翻错、以及这一步用的定律在此处适用条件是否仍然成立——变质量、非惯性系、准静态假设中途被悄悄破坏是高频翻车点。scripts/check_derivation.py 做前三项的确定性检查，第四项是人的判断。只核验已有推导，不代写推导。
category: physics/checking
version: 0.1.1
status: draft
priority: P1
compatible_agents:
  - claude-code
  - codex
  - cursor
  - codebuddy
  - nestudy
  - generic-llm-agent
display_name: 推导逐步核验
outputs:
  - chat
max_rounds: 24
suggest_hint: 用「推导逐步核验」逐步查代数、量纲、符号，以及定律的适用条件有没有中途失效
---

# Derivation Step Checker

Audit the derivation the user actually supplied. Keep algebraic validity separate from physical validity: a symbolic step may be correct while the invoked law is inapplicable.

## Inputs

Request only missing information that blocks the audit:

- the derivation with one transformation per numbered step;
- definitions and dimensions of symbols;
- the physical regime and assumptions (frame, system boundary, constancy, quasi-static limits, approximations);
- the desired depth: first failing step or full audit.

Do not invent omitted steps or assumptions. Mark them `unknown` and explain what evidence would resolve them.

## Workflow

1. **Normalize without repairing.** Transcribe each step as a before-equation and after-equation. Preserve the user's signs, subscripts, frames, and approximations. If a line performs several operations, split it into auditable substeps and label the split as editorial.
2. **Name the move.** For every step, record:
   - algebraic operation;
   - physical law, definition, constitutive relation, or approximation used;
   - applicability conditions required by that move.
3. **Check algebra.** Test whether the two equation residuals are equivalent, allowing an explicit nonzero multiplier. Check denominator restrictions, branch choices introduced by roots, sign reversals, and discarded solutions. A computer-algebra result is evidence, not permission to ignore domain assumptions.
4. **Check dimensions.** Require both sides of every equation and terms joined by addition to have the same dimensions. Dimensionally valid does not imply physically valid.
5. **Check physical continuity.** Re-evaluate the law's conditions at this exact step. In particular, look for assumptions that become invalid midway:
   - inertial-frame laws after a frame change;
   - fixed-mass momentum equations for variable-mass systems;
   - conservation laws after the system boundary opens;
   - quasi-static or equilibrium relations during a finite-rate process;
   - constant material parameters outside their stated regime;
   - approximations retained beyond their small-parameter range.
6. **Locate the first failure.** Do not let later algebra conceal an earlier invalid step. Classify each line as `pass`, `fail`, or `unknown`, and distinguish algebra, dimensions, and physics.
7. **Report minimally sufficient repairs.** Show the smallest correction that makes the failed step auditable. Do not rewrite the whole solution unless the user explicitly asks after seeing the audit.

## Deterministic checker

When the derivation can be represented with scalar symbolic expressions, create a JSON input following [references/input-schema.md](references/input-schema.md), then run:

```text
python3 scripts/check_derivation.py derivation.json
```

The checker verifies a constrained expression grammar, residual equivalence up to a declared factor, required nonzero declarations, and dimensions. Every non-constant factor of the declared factor must itself be declared nonzero: declaring `m1` and `m2` does not cover a division by `m1 - m2`, and you add `"m1 - m2"` to `nonzero` only when the user has established it, never to make the check pass. Equations written as `... = 0` check normally, and a symbolic exponent such as `10**m` must be dimensionless. `--selftest` runs the checker's regression cases. It deliberately cannot decide whether a physical law applies; review that from the stated regime and assumptions.

If Python or SymPy is unavailable, perform the same checks explicitly and mark them as manual. Never claim a script passed unless it was actually run successfully.

## Output format

Start with the first failing or unresolved step, then give the table:

| Step | Algebra | Dimensions | Physics | Law / move | Required conditions | Finding |
|---|---|---|---|---|---|---|
| 1 | pass/fail/unknown | pass/fail/unknown | pass/fail/unknown | ... | ... | ... |

Finish with:

- **First break:** earliest `fail`, or `none found`;
- **Unresolved assumptions:** facts still needed;
- **Minimal repair:** one local correction or next diagnostic action;
- **Scope limit:** what was not established (for example, initial model validity or final numerical plausibility).

## Boundaries

- This skill audits an existing derivation; it does not replace a student's own assessed derivation. Deriving a formula from principles in the first place belongs to the neighbouring skill `concept-to-formula-deriver`.
- Do not treat symbolic equivalence as proof of physical correctness.
- Do not infer a missing law from the desired answer.
- Do not hide domain restrictions, frame labels, approximation order, or uncertainty behind a green status.
- For a final-answer-only plausibility review, use `answer-plausibility-checker` instead; for isolated unit checking, use `dimensional-analysis-checker`.

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 修 check_derivation.py：`… = 0` 形式不再误判量纲不一致；`10**m` 这类符号指数要求无量纲；nonzero 可写表达式，按 factor_list 逐个因子核对，声明 m1、m2 不再放行除以 m1−m2；补 --selftest 与未知键报错；分流改为实名；用例 Case 1 更正为准静态与绝热可以同时成立 | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |

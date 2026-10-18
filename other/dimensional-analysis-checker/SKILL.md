---
name: dimensional-analysis-checker
description: 当有一条推导、模型方程、标度律或最终公式，想在相信它之前先过最便宜的一关时使用。逐项查量纲：先统一记号、建符号量纲表，再按加减两侧同量纲、等式两边一致、指数对数三角函数的宗量无量纲逐条核对，指出第一处不一致；每个通过的项还要说出它代表什么物理贡献，说不出的项就是没理解的项。结论里写明量纲通过不等于物理正确。
category: physics/checking
version: 0.1.1
status: draft
priority: P0
compatible_agents:
  - claude-code
  - codex
  - cursor
  - codebuddy
  - nestudy
  - generic-llm-agent
display_name: 量纲检查器
outputs:
  - chat
max_rounds: 16
suggest_hint: 相信这条公式之前，先用「量纲检查器」逐项查一遍量纲
---

# dimensional-analysis-checker

## Purpose

Use this skill when a user has a physics equation, derivation step, scaling law, or model expression and wants to know whether the dimensions make sense **before** trusting the result.

This skill does **not** prove that a derivation is fully correct. It answers a narrower question first: do the units and dimensions constrain the expression the way physics says they should?

## When to use

Use this skill when the user wants to:

- check a derived formula term by term
- catch missing factors, extra factors, or impossible sums
- verify a scaling law or constitutive relation
- compare two candidate formulas and rule out dimensionally impossible ones
- inspect the equations of a modeling paper draft for inconsistent symbol usage or undeclared units (reviewing a whole modeling paper or its full chain of claims belongs to `model-critique-coach`)

## When not to use

Do **not** use this skill as the only validation step when the user needs:

- limiting-case checks
- numerical plausibility checks
- a full derivation from first principles
- experimental uncertainty propagation
- proof that the physics assumptions themselves are appropriate

If the algebra is dimensionally valid but still physically wrong, say so plainly and hand off to `limiting-case-validator`, `physics-mechanism-decomposer`, or `derivation-step-checker`.

## Inputs

Ask for the smallest set that makes checking possible:

1. the expression, equation, or derivation step to inspect
2. a symbol table with meaning and units/dimensions for each symbol
3. the unit system if it matters (SI, Gaussian/CGS, natural units, nondimensionalized variables, etc.)
4. any declared constants or dimensionless coefficients
5. if symbols were reused across sections, which definition is intended here

If the user does not provide a symbol table, build one explicitly from the prompt and mark guessed entries as `assumed`.

## Outputs

Return a compact report with these sections:

1. `Scope` — what was checked and under which unit system
2. `Dimension map` — symbol → meaning → dimension/unit → status
3. `Checks` — each equation or term marked `pass`, `fail`, or `ambiguous`
4. `Findings` — the exact mismatch, leftover factor, or undefined symbol
5. `Physical meaning audit` — what each surviving term represents physically
6. `Next move` — smallest correction or follow-up check to run next

## Core workflow

### Step 1: Normalize notation first

Before checking dimensions:

- rewrite the target expression in a consistent notation
- expand overloaded symbols (`R` radius vs resistance, `T` period vs temperature)
- note any hidden conventions such as radians treated as dimensionless
- separate true constants from fitted coefficients

If notation is ambiguous, do **not** silently choose one meaning. Mark the result `ambiguous` until the symbol is disambiguated.

### Step 2: Build a dimension map

For every symbol that appears, create a table with:

- symbol
- physical meaning in this context
- dimension in base quantities when possible (for example `[M L T^-2]`)
- stated unit if supplied
- evidence status: `given`, `derived`, or `assumed`

Prefer base-dimension form over only unit names because it exposes hidden inconsistencies faster.

### Step 3: Check homogeneity where physics requires it

Apply the strongest valid test for the structure at hand:

- **sum/difference:** every addend must have identical dimensions
- **equality:** left-hand side and right-hand side must match
- **exponentials/logs/trig arguments:** the argument must be dimensionless unless the user is explicitly using a known convention and states it
- **powers/roots:** the dimensional consequences must be explicit
- **vector equations:** dimensions must match componentwise; note separately if geometric meaning is still unclear

When a formula mixes terms with different dimensions, point to the first exact place the mismatch appears.

### Step 4: Inspect dimensionless groups and leftover factors

After the basic check:

- identify dimensionless groups that naturally emerge
- flag parameters that should cancel but do not
- flag terms that are dimensionally allowed but physically suspicious
- note when the expression implies a hidden scale the user never introduced

A dimensionally valid term still needs a sentence explaining what contribution it stands for physically.

### Step 5: Run the physical meaning audit

For each surviving term or grouped contribution, ask:

- what mechanism does this term represent?
- is that mechanism supposed to be present in the stated model?
- if this term vanished, what physical limit would that correspond to?
- if this term dominates, what regime would that imply?

If a term passes units but nobody can say what it means, call it out. That usually signals cargo-cult algebra or a missing modeling assumption.

### Step 6: Report confidence honestly

Use these outcome labels:

- `pass` — dimensionally consistent under stated assumptions
- `fail` — definite inconsistency found
- `ambiguous` — cannot judge cleanly because notation, units, or conventions are underspecified
- `partial pass` — some steps check out, but at least one symbol or conversion remains unresolved

## Deterministic path vs fallback path

### If code execution is available

Prefer this repository's own checker first — it is standard-library only, so it runs anywhere:

```bash
python3 ../_shared/scripts/dimcheck.py expressions.dim
```

Write the dimension map into a `[symbols]` section (`v = L T^-1`) and each expression into
`[check]` as `name = expression`, with the declared dimension after a `;`. To check an
equation, write it as `lhs == rhs` (or `name = lhs == rhs` to name it): both sides must
share a dimension, and a side written as `0` matches any dimension. A plain `lhs = rhs` is
also checked as an equation unless `lhs` is a single new name, which that line defines.
Use `[compare]` to assert that several named terms share a dimension. Put fractional
exponents in parentheses, `x^(1/2)`; `x^1/2` and `v^2/2` are rejected as ambiguous, so write
`(v^2)/2` or `1/2*v^2` for division. The checker reports each mismatch, refuses to add unlike
terms, rejects dimensional arguments to `exp`/`log`/trig and to symbolic exponents, and lists
every symbol that was never declared — which doubles as a check for quantities that appeared
out of nowhere. Exit status 0 means all checks passed; 1 means a dimensional inconsistency
or an undeclared symbol; 2 means the input itself could not be parsed, which is a problem
with the `.dim` file to fix and rerun, not a finding about the physics. `--selftest`
verifies the checker itself.

Reach for SymPy or another CAS only for what `dimcheck.py` deliberately does not do:

- simplifying and enumerating candidate dimensionless groups
- solving the dimension matrix for its rank (the `k` in Buckingham's `n − k`)
- algebraic simplification of the expression itself

### If no code execution is available

Use a manual table method:

1. rewrite each symbol in base dimensions
2. multiply/add exponents term by term
3. compare addends and both sides of the equation
4. record the first mismatch explicitly

The skill should still work without any vendor-specific runtime. Label these checks as manual
in the report; never write that the script ran or that anything was verified by script.

## Guardrails

- Do not invent units for a symbol without marking them `assumed`.
- Do not pretend dimensional validity proves physical correctness.
- Do not hide ambiguity caused by natural-unit or nondimensional conventions.
- Do not hand over a finished solution, a full derivation, or a submission-ready corrected formula for work the user will submit; name the factor where the first inconsistency sits and leave the correction to the user. This applies to every request, including a repeated one (`../_shared/physics-evidence-contract.md` §4).
- If the expression is actually a fitted empirical law, say that dimensional consistency may constrain form but not prove mechanism.

## Handoff guidance

Hand off to another skill or workflow when:

- the expression passes units but fails a limiting case
- the mechanism list is unclear even though the dimensions work
- the user needs uncertainty propagation rather than unit checking
- the main problem is symbol collision across a longer document

Recommended neighbors (all available):

- `physics-mechanism-decomposer` — open-phenomenon mechanism ranking
- `problem-formalization-coach` — when the real problem is that a law was used
  without stating why it applies
- `limiting-case-validator` — regime checks: send each parameter to 0 and to infinity and
  check that the expression returns to a known special case
- `derivation-step-checker` — algebra plus law-by-law validation, step by step
- `concept-to-formula-deriver` — a derivation from first principles rather than a check
- `answer-plausibility-checker` — a numerical result to sanity-check rather than a formula
- `uncertainty-propagator` — uncertainty propagation rather than unit checking

## References

Shared physics material lives one level up, loaded on demand:

- `../_shared/dimensionless-groups.md` — Buckingham's theorem (how `k` and `n` get
  miscounted), the standard groups, and the discipline for comparing magnitudes
- `../_shared/law-applicability-table.md` — when a dimensionally valid term still violates the
  conditions of the law it came from
- `../_shared/physics-evidence-contract.md` — status tags, significant figures, which constants
  are exact by definition and which must be cited with a date, and the academic-integrity
  boundary (§4) behind the guardrail above
- `../_shared/scripts/dimcheck.py` — the deterministic checker

## Example prompts

- "Check whether this drag-force model is dimensionally consistent."
- "I derived an oscillation period formula; find the first unit mismatch if there is one."
- "These two heat-transfer terms are being added together. Is that legal dimensionally?"
- "Here is a modeling draft equation set. Build a symbol table and flag suspicious leftover parameters."

## Minimal response template

```text
Scope
- Checked: ...
- Unit system: ...

Dimension map
- symbol: meaning | dimension/unit | status

Checks
- Eq. (1): pass/fail/ambiguous
- Eq. (2): ...

Findings
- First mismatch: ...
- Suspicious leftover factor: ...

Physical meaning audit
- Term A represents ...
- Term B represents ...

Next move
- ...
```

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 跟随 dimcheck.py 修复写明 [check] 的方程写法、分数指数加括号与退出状态 0/1/2；诚信条款改为无条件并引用证据契约 §4；相邻 skill 去掉过时的 planned 标注并改用实名；π 定理引用改为"k 与 n 被数错的方式"；补 dimcheck 路径与无执行能力两个用例 | patch |
| 0.1.0 | 2026-08-30 | Initial cross-agent version with explicit manual fallback and evidence-status reporting. | minor |

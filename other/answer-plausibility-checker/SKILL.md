---
name: answer-plausibility-checker
description: 当算完、估完、拟合完或模拟完，拿到一个数值结果、要决定信不信时使用。按单位、符号、量级、极限行为、与参考值对比、守恒量收支六项过一遍嗅觉测试。对没有标准答案的科研与建模结果，改用「数量级 + 守恒总量核算」双锚点，不假装知道真值。引用的参考值必须带来源与查阅日期。
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
display_name: 结果可信度嗅探
outputs:
  - chat
max_rounds: 16
suggest_hint: 先用「结果可信度嗅探」过一遍量级、极限和守恒收支，再决定信不信这个数
---

# Answer Plausibility Checker

## Purpose

Audit a candidate physical result before trusting it. This skill is a **screen**, not a proof: passing the checks does not establish that a derivation or experiment is correct, while one well-founded failure is enough to reopen the work.

## Inputs

Ask only for missing information that can change the verdict:

- candidate value, uncertainty, and unit;
- quantity being estimated and the system/context;
- relevant input scales and assumptions;
- an expected range or comparison value, with source and date when available;
- applicable limiting cases;
- for an open-ended model or experiment, conserved totals and their initial/final or input/output values.

Do not invent missing units, reference values, uncertainties, or conservation terms. Mark unavailable checks `not run`.

## Workflow

### 1. Restate the claim

Normalize the result as:

```text
quantity = value ± uncertainty unit
conditions = ...
source = calculation | estimate | fit | simulation | measurement
```

Keep measured, assumed, and derived values distinct.

### 2. Run independent checks

Use as many independent anchors as the evidence permits.

1. **Units and dimensions**
   - Confirm that the stated unit matches the requested physical quantity.
   - Check dimensions in the final expression when the expression is available.
   - A dimensionally correct answer can still be physically wrong; never stop here.

2. **Sign and domain**
   - Check required bounds: mass and absolute temperature are nonnegative; a probability lies in `[0,1]`; speed is below the applicable model limit; geometry obeys its domain.
   - Distinguish signed components from magnitudes. A negative component may be valid.

3. **Order of magnitude**
   - Compare the result with a justified scale from the problem, a transparent Fermi estimate, or a sourced reference value.
   - Report the ratio and base-10 order gap. Do not call a difference “huge” without quantifying it.
   - Treat reference tables as prompts to verify, not timeless authority. Follow `references/reference-values.md`.

4. **Limiting behavior**
   - Vary one controlling parameter toward a meaningful small, large, zero, symmetry, or known-special-case limit.
   - State the expected physical behavior before comparing it with the candidate formula.
   - If symbolic limit evaluation or series expansion is the main task, hand off to `limiting-case-validator`.

5. **Conservation or balance**
   - For energy, momentum, charge, mass, particle number, or another applicable total, write a complete balance:

     ```text
     initial + inflow + generation = final + outflow + dissipation
     ```

   - Never label a total “not conserved” until exchanges with the environment and source/sink terms have been considered.
   - For research or modeling work without a standard answer, require both an order-of-magnitude anchor and at least one applicable balance anchor. If no conserved total applies, explain why and substitute another independent physical constraint.

6. **Uncertainty compatibility**
   - When uncertainties are available, judge compatibility with a stated statistical rule—not central values alone. Default rule: with standard uncertainties (coverage factor k=1) `u` and `u_ref`, compute `z = |value − reference| / sqrt(u² + u_ref²)` and treat the two as compatible when `z ≤ 2`. If you use another threshold, state it.
   - Convert an expanded uncertainty (for example k=2) to a standard uncertainty by dividing by its coverage factor first. Do not judge by whether the ±u intervals overlap: with equal uncertainties they stop overlapping at z ≈ 1.4.
   - Do not infer significance from an uncertainty-free comparison.

### 3. Use the deterministic checker when useful

`scripts/check_plausibility.py` checks finite values, bounds, expected-range membership, order gap, uncertainty compatibility (the z rule of check 6), and additive conservation balances from a JSON record. It does not understand physical meaning or unit conversions; normalize all compared values to the same unit first.

```bash
python3 scripts/check_plausibility.py case.json
python3 scripts/check_plausibility.py case.json --json
```

Input format:

```json
{
  "quantity": "launch speed",
  "value": 11200,
  "unit": "m/s",
  "bounds": {"min": 0},
  "expected_range": {"min": 10000, "max": 13000, "source": "source URL", "checked": "YYYY-MM-DD"},
  "reference": {"value": 11186, "unit": "m/s", "source": "source URL", "checked": "YYYY-MM-DD"},
  "max_order_gap": 1,
  "uncertainty": 50,
  "reference_uncertainty": 20,
  "max_z": 2,
  "conservation": {
    "left": [100.0, 5.0],
    "right": [103.0, 2.0],
    "relative_tolerance": 0.001
  }
}
```

| Field | Meaning | Default |
|---|---|---|
| `value` | candidate value (required) | — |
| `quantity`, `unit`, `conditions`, `source`, `notes` | descriptive text; not checked | — |
| `bounds` | hard limits, `min` and/or `max` (for example `min: 0` for a mass) | — |
| `expected_range` | `min` and `max` of a justified range, optional `source` and `checked` | — |
| `reference` | comparison `value`, optional `unit`, `source`, `checked`; enables the order-of-magnitude check | — |
| `max_order_gap` | largest allowed `abs(log10(value / reference))`; needs `reference` | `1` |
| `uncertainty`, `reference_uncertainty` | **standard uncertainties (k=1)** of the candidate and the reference, in the unit of `value`; need `reference` | — |
| `max_z` | largest allowed `z = abs(value − reference) / sqrt(uncertainty² + reference_uncertainty²)`; the script prints `z` | `2` |
| `conservation` | `left` and `right` arrays of balance terms, optional `relative_tolerance` | `1e-6` |

Omit checks for which no honest input exists. Unknown or misspelled fields are input errors, so a check is never skipped silently. Exit code `0` means no mechanical check failed, `1` means at least one failed, and `2` means invalid input. `--selftest` runs the script's regression cases.

### 4. Diagnose failures

For each failed check, give:

- the observed discrepancy;
- the physical principle or assumption it threatens;
- likely causes, ranked when possible (unit conversion, sign convention, exponent, omitted exchange term, invalid approximation, wrong regime, bad data);
- the cheapest discriminating next check.

Do not repair the result silently. Preserve the original candidate and show any corrected alternative separately.

## Output format

```markdown
## Candidate
- Quantity: ...
- Result: ...
- Conditions: ...

## Checks
| Check | Status | Evidence |
|---|---|---|
| Units/dimensions | pass/fail/not run | ... |
| Sign/domain | pass/fail/not run | ... |
| Order of magnitude | pass/fail/not run | ratio ..., order gap ... |
| Limiting behavior | pass/fail/not run | ... |
| Conservation/balance | pass/fail/not run | residual ... |
| Uncertainty compatibility | pass/fail/not run | z ..., threshold ... |

## Verdict
plausible | questionable | implausible | insufficient evidence

## Next action
- ...
```

Verdict rules:

- `implausible`: at least one clear physical contradiction or failed hard constraint;
- `questionable`: a material discrepancy remains but could be explained by missing context or uncertainty;
- `plausible`: all applicable checks pass and at least two independent physical anchors were run;
- `insufficient evidence`: fewer than two independent anchors can be run.

Never translate `plausible` into “correct.”

## Boundaries and handoffs

- Use `dimensional-analysis-checker` for detailed term-by-term dimensional auditing.
- Use `limiting-case-validator` for symbolic limits, asymptotic expansions, or systematic enumeration of limits.
- Use `fermi-estimation-coach` to construct an estimate when no defensible scale exists yet.
- Use `derivation-step-checker` when the question is which algebraic or physical-law step failed.
- This skill must not fabricate a reference value, silently convert incompatible units, or claim experimental validation from an internal consistency check.

## References

- `references/reference-values.md` — provenance and comparison rules for reference values (check 3)
- `../_shared/physics-evidence-contract.md` — §4 academic-integrity boundary shared by all physics skills

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 不确定度相容改用 z 值（差值除以合成标准不确定度，输入按 k=1 的标准不确定度，默认阈值 max_z=2），原 ±u 区间重叠判据在约 1.4σ 就判失败（references 同步）；输入格式补 expected_range、max_order_gap、max_z；未知或拼错的键改为输入错误；脚本加 --selftest；泛称"derivation checker"改为点名 derivation-step-checker；补 _shared 证据契约 §4 引用；示例命令改用 `python3`（macOS 自带的只有 python3） | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |

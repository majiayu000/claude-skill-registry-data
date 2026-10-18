---
name: fermi-estimation-coach
description: 当机制清单已经排好、需要给每个机制配数值锚点并合成一个站得住的量级结论时使用。把估算写成显式的因子分解，每个因子给低／中／高三值与证据档位，算出区间而不是装饰性的小数位，再与参考区间和守恒量核对。worksheet 的结构与算术由 scripts/check_estimate.py 校验。不负责发现或排序机制——那是 physics-mechanism-decomposer 的事。
category: physics/estimation
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
display_name: 费米估算教练
outputs:
  - chat
max_rounds: 20
suggest_hint: 机制排完了，用「费米估算教练」给每个机制配数值锚点并合出量级
---

# Fermi Estimation Coach

Turn an identified physical mechanism into a transparent numerical estimate. Preserve uncertainty and expose the assumptions that control the conclusion.

## Scope

Use this skill to:

- attach numerical anchors to an existing mechanism chain;
- estimate low, central, and high values for uncertain factors;
- combine mechanism-level estimates into an order-of-magnitude conclusion;
- identify which assumptions deserve measurement or source checking.

Do **not** use it to discover, rank, or explain candidate mechanisms from scratch. If no mechanism list exists, first ask for one or route the user to `physics-mechanism-decomposer`. Do not present guessed values as measured facts, and do not silently replace missing inputs with convenient constants.

In graded work that is still in progress (homework, a test, a competition entry such as an IYPT report), the factorization, the anchors, and the final estimate are the user's own work. There, check the structure and arithmetic of the worksheet the user wrote, name factors that lack a basis or an evidence status, and explain how an anchor could be found; do not choose the anchors, fill in the numbers, or produce the estimate. If the context is unclear and the request is to produce the estimate, ask first. This is the shared boundary in `../_shared/physics-evidence-contract.md` §4.

## Inputs

Ask only for information that changes the estimate:

1. target quantity and unit;
2. mechanism list, including which mechanisms are dominant, secondary, or negligible;
3. known measurements, constraints, and environmental conditions;
4. desired precision or decision threshold;
5. permitted sources or lookup constraints.

If the user cannot supply a mechanism list, stop after producing a short list of missing prerequisites. Do not invent the physics chain.

## Workflow

### 1. State the estimation contract

Write one sentence each for:

- **Target:** quantity, unit, system boundary, and time/length scale.
- **Decision:** what conclusion the estimate must support.
- **Precision:** nearest power of ten, factor of two, or another justified tolerance.

A Fermi estimate should not claim more precision than its weakest input supports.

### 2. Import the mechanism chain

Copy each supplied mechanism into a ledger. Give it a stable ID and preserve its assigned role: `dominant`, `secondary`, or `negligible`. Record provenance (user, prior analysis, or cited source).

Do not rerank mechanisms merely because one is easier to calculate. If the supplied ranking appears inconsistent, flag the conflict and request a mechanism review rather than fixing it silently.

### 3. Build an explicit factorization

For each non-negligible mechanism:

1. express its contribution as a product or quotient of measurable factors;
2. define every symbol and unit;
3. distinguish measured, sourced, inferred, and assumed values;
4. use the fewest independent factors that preserve the physical structure;
5. keep calculations symbolic until the factorization is stable.

Avoid double counting. Two factors derived from the same observation are not independent evidence.

### 4. Anchor every factor

Give every uncertain factor a positive `low`, `central`, and `high` value and a basis:

- **measured:** supplied observation and measurement conditions;
- **sourced:** citation plus access or publication date;
- **derived:** equation and upstream factor IDs;
- **assumed:** explicit rationale and the consequence if wrong.

When a trusted reference interval is available, record it separately. A familiar-looking number is not a source. If values can be zero or negative, reformulate the magnitude estimate and track sign separately; the bundled checker assumes positive magnitudes.

### 5. Calculate ranges, not decorative decimals

For products and quotients, propagate a conservative interval:

- central: central numerator factors divided by central denominator factors;
- low: low numerator factors divided by high denominator factors;
- high: high numerator factors divided by low denominator factors.

Round the narrative conclusion to a precision justified by the range. Retain unrounded values in the worksheet for checking.

### 6. Synthesize the mechanisms

Combine all `dominant` and `secondary` contributions unless an exclusion is explicitly justified. Choose a method that matches the physical relationship:

- `sum` for additive contributions;
- `max` only when the goal is a dominant-scale approximation and this is stated;
- `product` only when mechanism outputs are genuinely multiplicative. The mechanism units then multiply to the target unit (for example `s^-1` × `J` = `W`); with `sum` and `max`, every mechanism estimate carries the target unit itself.

Keep negligible mechanisms in the ledger with the reason they were omitted. Never infer cancellation from magnitudes alone; signs and phases require separate physical justification.

### 7. Stress-test the conclusion

Vary one uncertain factor at a time across its interval. Report:

- which factor changes the result most;
- whether the mechanism ranking changes;
- whether the decision changes;
- the cheapest observation that would reduce uncertainty.

If the conclusion crosses the decision threshold inside the plausible range, report it as unresolved, not as a central-value win.

### 8. Run the deterministic check

Encode the worksheet using `references/estimate-schema.md`, then run:

```text
python3 scripts/check_estimate.py estimate.json
```

The checker validates field completeness, unknown keys, ordered positive ranges, reference-range conflicts, product/quotient arithmetic, synthesis closure, the combined unit of a `product` synthesis, and omission of non-negligible mechanisms. Exit status: `0` pass, `1` validation errors, `2` unreadable file or bad arguments; `--selftest` runs its regression cases. It does **not** validate the selected physics, source credibility, unit conversions, whether factor units multiply to the mechanism unit, signs, correlations, or whether factorization is conceptually correct. Those require human or agent review.

## Output format

Return sections in this order:

1. **Estimation contract**
2. **Mechanism ledger**
3. **Factor table** — ID, meaning, unit, low/central/high, evidence status, basis
4. **Mechanism calculations**
5. **Synthesis**
6. **Sensitivity and decision**
7. **Unknowns and next measurement**
8. **Verification status** — checker result and non-automated checks still needed

## Failure rules

- Missing mechanism chain: stop and list the missing prerequisite.
- Missing anchor: mark `unknown`; do not substitute an unstated default.
- Conflicting sources: retain both ranges and show how each changes the result.
- Unit mismatch: stop calculation until conversion is explicit.
- Correlated factors: flag the dependency; do not imply independent uncertainty.
- Arithmetic checker failure: do not present the estimate as verified.
- Plausible range spans multiple decision outcomes: conclude “insufficiently constrained.”

## Quality gate

Before finalizing, confirm:

- every non-negligible mechanism is included or explicitly blocked;
- every numerical anchor has a basis and evidence status;
- units and system boundaries are explicit;
- low ≤ central ≤ high for every magnitude;
- no mechanism or observation is counted twice;
- the stated precision matches the uncertainty range;
- deterministic checks pass;
- physical assumptions and checker limitations remain visible.

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | check_estimate.py：product 合成改为各机制单位相乘后与目标单位比对（原规则只有谎标单位才能通过），method/role/evidence_status 类型错误不再抛 TypeError，未知键报错，加 --selftest 并写明退出码；Scope 补作业与竞赛进行中的代做边界（指向证据契约 §4），机制分解改指 physics-mechanism-decomposer；示例命令改用 `python3`（macOS 自带的只有 python3） | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |

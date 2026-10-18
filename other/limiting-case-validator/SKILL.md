---
name: limiting-case-validator
description: 当有一条公式、标度律或模型结果，想在相信它之前查它在极限下还讲不讲得通时使用。先找出控制参数与无量纲组，挑最小一组有用的极限，在动手算之前先写下物理上应该发生什么，再做数学化简两相对照；专抓在某个极限下发散、变号、或丢掉已知特例的表达式。manifest 的完整性由 scripts/check_limit_manifest.py 校验。
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
display_name: 极限情形验证
outputs:
  - chat
max_rounds: 20
suggest_hint: 用「极限情形验证」把每个参数分别推到 0 和无穷，看它回不回得到已知特例
---

# limiting-case-validator

Use this skill when a physics derivation, fitted relation, or simulation result may be algebraically correct yet physically wrong. The goal is to test whether the result behaves sensibly when key parameters become very small, very large, equal to each other, or approach a known special regime.

This skill is for validation, not for doing the original derivation from scratch.

## Use this when

- You have a final formula (not only a number) and want to know whether it is physically plausible in its limits.
- You need to check whether a model reduces to a known textbook case.
- You want to identify which dimensionless parameter actually controls the regime.
- A result looks suspicious near a boundary, singularity, or approximation limit.

## Do not use this when

- The main problem is parsing the original statement. Use `competition-scenario-extractor` first.
- The formula is not yet defined clearly enough to test.
- The user is asking you to invent a derivation they have not attempted.
- The task is mainly unit consistency; use `dimensional-analysis-checker`.
- The user wants every step of a written derivation audited (algebra, signs, whether each law still applies); use `derivation-step-checker`. This skill tests only the end result.
- The user has a numerical answer but no formula to take limits of; use `answer-plausibility-checker`.

## Required inputs

Ask for the minimum needed set:

1. The expression, model, or claim to validate.
2. The meaning and units of every symbol.
3. The physically allowed range of each control parameter, if known.
4. Any known special cases, benchmark formulas, or conservation constraints.
5. Whether the source is from hand derivation, data fitting, or simulation.

If any of 1-2 is missing, stop and request clarification.

## Core idea

A useful limiting-case check has two halves:

- **Predict first:** before touching algebra, state what should happen physically in each limit.
- **Compute second:** then reduce the expression in that limit and compare against the prediction.

Never treat a formal limit as passed unless both halves are present.

## Workflow

### 1. Identify control parameters

List the parameters that can define distinct regimes, such as:

- small or large mass ratio
- low or high speed
- weak or strong damping
- short-time or long-time behavior
- thin-gap or large-gap geometry
- small-angle or large-angle approximation
- low-frequency or high-frequency drive

Prefer dimensionless groups when possible. If the problem is written only in dimensional variables, explicitly form the likely dimensionless combinations first.

### 2. Choose the smallest useful set of limits

Do not enumerate every imaginable limit. Pick the limits that most strongly test the physics:

- known textbook limits
- parameter going to zero
- parameter going to infinity
- two parameters becoming equal
- no-interaction limit
- quasistatic / instantaneous limit
- nonrelativistic / ultrarelativistic limit
- weak-coupling / strong-coupling limit

Usually 2-4 limits are enough for one pass.

### 3. Write the physical expectation before the math

For each chosen limit, state:

- what mechanism should dominate
- what should vanish, saturate, diverge, or change sign
- what known law or simpler model should reappear
- whether the quantity should remain finite, monotone, positive, or bounded

If you cannot explain the expectation in words, say so instead of bluffing.

If you can run scripts, record steps 1-3 as a limit manifest and check it now, before step 4 (see **Limit manifest check** under Deterministic assistance).

### 4. Reduce the expression in each limit

For each limit:

1. Specify the limit clearly.
2. Simplify the expression to its leading behavior.
3. Note any singular terms, cancellations, or sign flips.
4. If there is a series expansion, keep only the first term needed to decide the physics.

When a computer algebra system is available, use it to support the reduction. When it is not, do the asymptotics manually and state any uncertainty.

### 5. Compare math to physics

For each limit, classify the outcome:

- **Pass**: reduces to the expected regime or benchmark.
- **Partial pass**: trend is right, but coefficient/sign/boundedness is questionable.
- **Fail**: contradicts a known law, expected trend, conservation argument, or physical constraint.
- **Inconclusive**: limit could not be evaluated from the provided information.

Explain the mismatch in physical language, not only algebraic language.

### 6. Check high-value red flags

Always look for these failure modes:

- wrong sign in a restoring, dissipative, or probability-like term
- divergence where the physics should stay finite
- dependence on a parameter that should disappear in a decoupled limit
- failure to recover a known special case
- nonzero output when symmetry requires zero
- negative quantity where positivity is required
- asymptotic scaling that contradicts mechanism dominance

### 7. End with a verdict and next action

Give one of:

- usable as written
- usable with caveats
- likely wrong and should be re-derived
- underdetermined; need more context

If it fails, point to the most likely source:

- bad approximation regime
- algebraic sign error
- hidden assumption violated
- wrong boundary condition
- wrong dominant-balance argument
- fit extrapolated beyond data support

## Output format

Use this structure:

```markdown
## Candidate result
- [expression or model]

## Control parameters / dimensionless groups
- ...

## Limiting cases checked
### Limit 1: [statement]
- Physical expectation:
- Reduced behavior:
- Comparison:
- Verdict: Pass / Partial pass / Fail / Inconclusive

### Limit 2: [statement]
- Physical expectation:
- Reduced behavior:
- Comparison:
- Verdict: Pass / Partial pass / Fail / Inconclusive

## Cross-limit red flags
- ...

## Overall verdict
- ...

## Recommended next step
- ...
```

## Guardrails

- Do not invent benchmark formulas you cannot justify.
- Do not claim a limit is physically relevant if the parameter range makes it impossible.
- Do not replace physical reasoning with symbolic manipulation alone.
- If multiple competing limits do not commute, say so explicitly.
- Separate exact limits from approximations and fitted extrapolations.

## Deterministic assistance

If tools are available, they may help with:

- symbolic limits
- leading-order asymptotics
- series expansion around small parameters
- sign checks under stated parameter constraints
- substitution into known benchmark cases

These checks support the judgment; they do not replace the need to state the physical expectation first.

### Limit manifest check

`scripts/check_limit_manifest.py` checks that the plan from steps 1-3 is complete before any algebra: every limit names its variable, its approach, a physical expectation and a reason. Write the plan as a JSON file and run, from this skill's directory:

```bash
python3 scripts/check_limit_manifest.py limit-manifest.json
```

`--help` prints the field list; `--selftest` runs the script's regression cases.

| Field | Required | Content |
|---|---|---|
| `target` | yes | the formula or claim under test, quoted exactly |
| `variables` | yes, non-empty | one object per control parameter or dimensionless group |
| `variables[].name` | yes | unique name; cases refer to it |
| `variables[].baselineLimits` | no | approach words that must each have a case; a missing case is a `WARN` |
| `variables[].meaning`, `units`, `range` | no | free text |
| `cases` | yes, non-empty | one object per limit |
| `cases[].id` | yes | unique id such as `L1` |
| `cases[].variable` | yes | a declared variable name |
| `cases[].approach` | yes | one approach word from the list below |
| `cases[].expected` | yes | the physical expectation from step 3, written before the math |
| `cases[].why` | yes | why this limit is physically relevant (step 2) |
| `notes` | no | free text, allowed at the root, in variables and in cases |

Approach words: `0`, `+0`, `-0`, `inf`, `+inf`, `-inf`, `small`, `large`, `equal-scale`, `threshold`, `special-value`, `turn-off`, `symmetry`.

Minimal example:

```json
{
  "target": "T = 2*pi*sqrt(L/g)*(1 + theta0)",
  "variables": [
    {"name": "theta0", "meaning": "launch amplitude", "units": "rad", "baselineLimits": ["+0"]}
  ],
  "cases": [
    {"id": "L1", "variable": "theta0", "approach": "+0",
     "expected": "period returns to 2*pi*sqrt(L/g); the first correction is even in theta0",
     "why": "small-angle textbook limit"}
  ]
}
```

Exit codes: `0` the plan is structurally complete, or usable with `WARN` lines (a declared variable no case tests, a baseline limit with no case); `1` errors (missing or empty field, unknown field, unsupported approach word, undeclared variable, unreadable file); `2` usage error. The script checks the structure of the plan only. It evaluates no limit, so a clean run says nothing about whether the formula passes.

## Acceptance bar

A good run of this skill must include all of the following:

- the tested formula or claim is quoted unambiguously
- each chosen limit is physically motivated
- each limit includes a pre-math expectation
- each limit includes an actual reduced form
- the final verdict distinguishes pass, fail, and inconclusive cases

If any of the above is missing, the validation is incomplete.

## References

- `../_shared/physics-evidence-contract.md` — §4 academic-integrity boundary shared by all physics skills (backs the "invent a derivation" exclusion above)
- `scripts/check_limit_manifest.py` — structural check of the limit plan (see Limit manifest check)

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 正文补 manifest 字段表、调用命令与退出码；脚本支持 --help、--selftest，空 manifest 与未知字段改为报错；"不适用"改为点名 competition-scenario-extractor、dimensional-analysis-checker、derivation-step-checker、answer-plausibility-checker；补 _shared 证据契约 §4 引用 | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |

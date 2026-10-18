---
name: concept-to-formula-deriver
description: 当问「这条公式怎么来的」「为什么长这样」，或说「帮我推导／推出 X 公式」时使用。从定义或守恒律出发重建标准公式，每一步标出用的是哪条原理、这一步在物理上做了什么；假设写在它真正被用到的那一步，不堆在开头。终式可用 scripts/compare_formula.py 与标准式做符号比对。会被评分的推导：结构与理由可以给，代数由本人做。要逐步核验一份已写好的推导，用 derivation-step-checker。
category: physics/derivation
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
display_name: 公式溯源教练
outputs:
  - chat
max_rounds: 20
suggest_hint: 用「公式溯源教练」把这条公式还原成某条守恒律的推论，而不是背下来的结论
---

# concept-to-formula-deriver

## Purpose

Use this skill when someone knows the target relation they need, but does not yet understand how that relation follows from first principles.

This skill is for **deriving structure**, not for silently producing finished coursework. It should make the chain

> principle -> assumptions -> intermediate relation -> target formula

explicit enough that a learner can reproduce it on their own.

## Use when

- The user asks where a standard formula comes from.
- The user asks to derive a standard formula ("帮我推导 X"); for assessed work, stop at the safe endpoints in step 8.
- The user can name a target relation, but cannot justify each step.
- The user needs help choosing between candidate starting principles such as conservation, definitions, or kinematics.
- The user wants each step of a derivation tied to its physical reason, not only the algebra.

## Do not use when

- The task is mainly about **which model/mechanism applies**. Use `problem-formalization-coach` first (which law applies here, and under what conditions), or `physics-mechanism-decomposer` for an open phenomenon.
- The user already has a written derivation and wants it checked step by step (algebra, dimensions, signs, whether each law still applies at that step). Use `derivation-step-checker`: it audits an existing derivation, while this skill builds one from a starting principle.
- The user wants a full polished assignment solution with no explanation. Refuse the write-up, but you may still teach the method.
- The target relation depends on specialized facts, coefficients, or constitutive laws that the user has not supplied and you cannot justify.

## Required inputs

Ask for or extract these before deriving:

1. **Target relation**: the equation, proportionality, or scaling law to recover.
2. **Symbol table**: meaning and units of every symbol that will appear.
3. **Regime / assumptions**: small angle, nonrelativistic, steady state, ideal gas, negligible drag, etc.
4. **Allowed starting points**: definitions, conservation laws, constitutive relations, or geometry facts the user is allowed to use.
5. **User ownership boundary**: whether this is study help, a draft to critique, or assessed work where the learner must write the final derivation.

If any of these are missing, pause and ask only for the missing pieces that block a physically honest derivation.

## Core workflow

### 1) Fix the target and the regime

Restate the target formula in words and symbols. Name the regime explicitly.

Output a short contract like:

- Target: ...
- Valid when: ...
- Not valid when: ...

### 2) Build a symbol table before moving symbols

Create a compact table:

| Symbol | Meaning | Units | Status |
|---|---|---|---|
| ... | ... | ... | given / standard / assumed |

Do not introduce new quantities without labeling them.

### 3) Choose the starting principle and justify it

Name the first principle before writing equations.

Examples:

- Conservation of energy is appropriate because ...
- Momentum balance is appropriate because ...
- Start from the definition of electric field because ...

If there are multiple plausible starts, compare them briefly and choose the shortest physically clean path.

State the chosen principle's applicability conditions for this problem. `../_shared/law-applicability-table.md` lists them for common laws, and its §6 gives the thresholds where non-relativistic or classical forms stop working.

### 4) Derive in single-responsibility steps

Each line should do **one** mathematical move and carry **two labels**:

- **Math action**: substitute / expand / integrate / isolate / apply boundary condition / take limit
- **Physics reason**: conservation law / constitutive law / geometry / definition / approximation

Preferred format:

1. Equation
   - Math action:
   - Physics reason:

Avoid multi-line jumps that hide the physical reason.

### 5) Surface assumptions exactly where they are used

When an assumption matters, attach it to the line where it enters, for example:

- "Using small-angle approximation, so sin(theta) ≈ theta for |theta| << 1."
- "Setting nonconservative work to zero because drag is neglected in this model."

Do not dump assumptions only at the top and never mention them again. `../_shared/idealization-catalog.md` says what each common idealization switches off and when it fails.

### 6) Interpret the result, not just the algebra

After reaching the target relation, explain:

- what each factor means physically;
- which variables the result is sensitive to;
- which parameter combinations actually control the behavior;
- what would change first if a key assumption were relaxed.

### 7) Run compact checks

Always do at least two of these:

- **Units check**: both sides must match.
- **Special-case check**: recover a simpler known result.
- **Sign / monotonicity check**: confirm the direction of dependence makes sense.
- **Limit check**: inspect a small/large parameter regime.
- **Formula-equivalence check**: if a canonical expression is known, compare the final symbolic form with `scripts/compare_formula.py`.

### 8) Preserve learner ownership

If the task is assessed work, stop at one of these safe endpoints:

- annotated outline of the derivation;
- first 1-2 justified steps plus the remaining roadmap;
- critique of the learner's own attempt.

Do **not** hand over a ready-to-submit derivation when that would replace the learner's work. This is the shared boundary in `../_shared/physics-evidence-contract.md` §4.

## Output template

Use this structure unless the user asks for another format:

### Derivation goal
- Target relation:
- Valid regime:

### Symbols and assumptions
- Symbols:
- Assumptions:

### Why this starting principle
- Principle chosen:
- Why it applies here:
- Why competing starts are worse:

### Step-by-step derivation
1. ...
2. ...
3. ...

### Physical interpretation
- ...

### Quick checks
- Units:
- Special case or limit:
- Sign / scaling:

### Next step for the learner
- ...

## Failure modes to avoid

- Treating a memorized formula as a starting principle when the task is to derive that very formula.
- Using a law without stating its applicability conditions.
- Smuggling in extra constants, geometry facts, or boundary conditions that were never named.
- Compressing three algebraic steps into one and losing the physical reason.
- Ending with a symbolically correct result whose dependence is physically backwards.
- Solving the whole assignment when the user actually needed a derivation coach.

## Deterministic support

`scripts/compare_formula.py` can help compare a derived symbolic expression with a reference expression. It needs Python 3 with sympy.

```text
python3 scripts/compare_formula.py --derived "2*pi*(L/g)**(1/2)" --reference "2*pi*sqrt(L/g)"
```

- Every name is a plain symbol, including `E`, `I`, `N`, `S`, `gamma`, `beta`, and `lambda`. `pi` is the only constant; write Euler's number as `exp(1)`. A name used as a function that the script does not know is an input error.
- Every symbol is assumed positive, so `L*sqrt(g/L)` matches `sqrt(g*L)`. List symbols that can be negative or zero with `--real q,v`.
- Decimals are exact (`0.5` is `1/2`). Write products with `*` and powers with `**` or `^`.
- Equations are written `Eq(lhs, rhs)` and match when their `lhs - rhs` differ by a nonzero constant factor, so swapped sides are fine. A rearranged form such as `T**2 = 4*pi**2*L/g` against `T = 2*pi*sqrt(L/g)` does not match; compare the expressions for the target quantity instead.
- Exit status: `0` equivalent; `1` not equivalent, with a numerical counterexample printed; `2` input error (one line on stderr); `3` undetermined: simplification did not confirm it, but no counterexample was found. `--selftest` runs the regression cases.

Suggested use:

- Compare two expressions for the same quantity after moving them into a common symbolic form.
- Treat the script as a **sanity check**, not proof that the derivation is pedagogically good.
- If the script says `no`, start from the printed counterexample and inspect assumptions, missing factors, sign conventions, and hidden substitutions. If it says `undetermined`, check by hand before calling the forms different. Exit status `2` means the input could not be read, not that the forms differ.
- Without code execution, compare by hand and label the check as manual.

## Minimal test cases

### Case 1: Good fit
User asks: "Why does escape speed scale like sqrt(2GM/R)? Walk me from energy conservation."

Expected behavior:
- choose conservation of energy;
- state assumptions (two-body, neglect drag, Newtonian gravity);
- derive stepwise;
- explain why larger M increases required speed and larger R decreases it;
- run units + sign checks.

### Case 2: Boundary case
User asks: "Write the full derivation of the pendulum period for my homework so I can paste it."

Expected behavior:
- refuse to provide a ready-to-submit derivation;
- offer an annotated outline or critique the user's own draft;
- explicitly mark where the small-angle approximation enters.

### Case 3: Missing inputs
User asks: "Derive the formula for this circuit," but gives no circuit, symbols, or regime.

Expected behavior:
- ask for the missing diagram/relations/symbol meanings;
- do not invent topology or component laws.

## Completion criteria

This skill is complete for a given turn when it has:

- identified the target relation and regime;
- named every nontrivial principle used;
- attached assumptions where they enter;
- given at least two post-derivation checks;
- preserved learner ownership if the context is assessed work.

## References

- `../_shared/law-applicability-table.md` — applicability conditions of common laws (step 3); §6 gives the thresholds for relativistic and quantum corrections
- `../_shared/idealization-catalog.md` — what each assumption switches off and when it fails (step 5)
- `../_shared/physics-evidence-contract.md` — status tags for the symbol table, sourcing of constants (§3), and the integrity boundary for assessed work (§4)
- `scripts/compare_formula.py` — symbolic equivalence check for step 7

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | compare_formula.py 修正误判与崩溃：小数指数与等式左右互换判错、符号无正值假设、I/E 被当成虚数单位与自然常数、N/Q/S/gamma/beta/lambda 崩溃；所有名字按普通符号解析，退出码分成 0 等价/1 不等价（给反例）/2 输入错误/3 无法判定，加 --selftest；description 补上「帮我推导」触发语；泛称分流改成实名并点明与 derivation-step-checker 的分工；引用 _shared 参考 | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |

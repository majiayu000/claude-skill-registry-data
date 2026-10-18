---
name: symbolic-first-discipline-coach
description: 当推导中途就把数字代进去、结果看不出结构时使用。把符号一路保留到结构不再变化，再与「早代入数字」的路径并排对照：哪些量其实约掉了、哪两个量只以某个组合出现（说明本质自由度比看上去少）、从哪一步开始代数字会把物理藏起来。给的是纪律与对照，不替使用者算完。
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
display_name: 符号优先纪律
outputs:
  - chat
max_rounds: 20
suggest_hint: 用「符号优先纪律」看看这堆参数里，真正独立的组合其实有几个
---

# symbolic-first-discipline-coach

## Purpose

Use this skill when someone is solving a physics problem and is tempted to substitute numbers too early.
The skill helps them keep the derivation symbolic long enough to see:

- which parameters genuinely matter,
- which ones cancel,
- which combinations survive as the real control parameters,
- and what physical interpretation is lost once the work collapses into arithmetic.

The skill is about **structure before calculation**. It may simplify algebraic forms, compare solution paths, and point out hidden dimensionless groups, but it should not pretend that symbolic manipulation alone proves a model is physically correct.

## When to use

Use this skill when the user says things like:

- "I can plug in the numbers, but I don't see what the result depends on."
- "Why do these two variables disappear?"
- "Should I keep everything symbolic first?"
- "This equation works numerically, but I don't understand the pattern."
- "I want to know which parameter actually controls the behavior."

Typical settings:

- competition physics and Olympiad-style derivations,
- introductory and intermediate mechanics / E&M / thermodynamics,
- modeling and open-ended problems where scaling structure matters,
- pre-lab or pre-simulation sanity checks.

## When not to use

Do **not** use this skill when:

- the user wants a finished homework derivation written for submission;
- the bottleneck is choosing the wrong law, not symbolic discipline;
- the expression is already symbolic and the real issue is units, limits, or data fitting;
- the user only needs a quick numerical estimate and explicitly does not care about structural insight.

Route elsewhere when appropriate:

- to `problem-formalization-coach` if the variables and constraints are not yet defined;
- to `dimensional-analysis-checker` if unit consistency is still in doubt;
- to `limiting-case-validator` if the formula is derived but its physical behavior is not trusted.

## Inputs required

Ask for the smallest set that makes structural comparison possible:

1. **Target quantity** — what is being solved for?
2. **Symbol definitions** — each symbol, unit, and physical meaning.
3. **Starting relations** — laws, definitions, constraints, or equations already accepted.
4. **Early numeric path** — where the user would normally substitute values.
5. **Known scales or regimes** — small angle, low speed, weak damping, large separation, etc.
6. **Context** — graded work still in progress (homework, a test, a competition entry), or self-study, review after submission, research. It decides how much of the symbolic path you write (see Boundaries and integrity).

If any of 1–3 are missing, stop and request them before coaching. If 6 is missing, ask for it; until the user says the work is not graded or already submitted, coach at the graded-work level.

## Output contract

Produce a compact coaching artifact with these sections:

1. **Symbolic target** — the quantity to derive and the allowed symbols.
2. **Stay-symbolic path** — a stepwise derivation that delays substitution.
3. **Early-substitution path** — the shorter arithmetic-first route, if available.
4. **What becomes visible symbolically** — canceled parameters, surviving groups, proportionalities, symmetries.
5. **Physical reading** — what each surviving factor means physically.
6. **Decision rule** — exactly when numbers should finally be substituted.
7. **Confidence / gaps** — assumptions, unproved steps, or places needing human checking.

For graded work in progress, sections 2–5 become structural questions plus the comparison method: which quantities might cancel, which combination to watch for, at which step substituting numbers would hide the structure. The user writes the symbolic path and does the substitution.

## Core workflow

### Step 1: Freeze the symbol table

Before manipulating anything, normalize the symbol table.
Each symbol must have:

- name,
- meaning,
- unit or dimension,
- whether it is variable, constant, or measured input.

If a symbol is overloaded, rename it locally and say so.

### Step 2: State the structural question

Pick one explicit structural question to answer, such as:

- Which parameters cancel?
- Which dimensionless combination controls the answer?
- Which approximation creates the apparent simplicity?
- Which variable only matters through a ratio or product?

This prevents the skill from becoming generic algebra commentary.

### Step 3: Derive symbolically as far as the structure is still changing

Keep quantities symbolic until at least one of the following becomes clear:

- the dependency graph is stable,
- the remaining operation is routine arithmetic,
- the controlling nondimensional group has appeared,
- or the only unknown is a measured constant.

At each step, annotate one of these move types:

- **definition**
- **conservation / balance law**
- **constraint substitution**
- **algebraic isolation**
- **approximation**
- **scaling interpretation**

### Step 4: Compare against early substitution

Show how an arithmetic-first path hides information. Focus on concrete losses such as:

- cancellation is no longer visible,
- a ratio that should be recognized as the true control parameter is buried,
- sensitivity to one parameter is misread because numbers are frozen too soon,
- an approximation looks exact because the substituted values happen to mask error.

### Step 5: Extract the physical structure

Name the structure explicitly. Good outputs include statements like:

- "The result depends on density and radius only through the combination ρR³, so mass scaling is the real lever."
- "The angle cancels because only the component ratio matters in this regime."
- "The answer is controlled by the dimensionless product ωτ; frequency and timescale do not enter independently."
- "The apparent dependence on g vanishes once the kinematic constraint is substituted, so geometry dominates."

### Step 6: Decide when numbers belong

Recommend substitution only after one of these is true:

- the structure has been interpreted,
- a limiting regime has been identified,
- the user is choosing between candidate experimental scales,
- or the task is now purely quantitative.

When giving final numeric guidance, preserve the symbolic master expression in the output.

## Coaching rules

- Prefer the **shortest symbolic path that still reveals structure**.
- Do not inflate simple problems into ceremonial derivations.
- If the expression is messy, factor or nondimensionalize before expanding.
- If a parameter cancels, say **why physically**, not just that it canceled algebraically.
- If two parameters only appear as a ratio, name that ratio as a new control variable.
- If an approximation is introduced, mark what small or large parameter licenses it.
- If the user is learning, expose one hidden pattern at a time.

## Deterministic checks this skill can support

These checks are optional aids, not substitutes for judgment:

- verify that the final symbolic expression only uses declared symbols;
- compare symbolic and numeric paths to find parameters that disappear after simplification;
- detect whether multiple variables always appear as a single product, ratio, or power-law group;
- flag substitution that occurs before an approximation or cancellation is justified;
- list candidate dimensionless groups for human review.

If no tooling is available, perform the same checks manually and label them as manual.

## Failure modes to avoid

- confusing algebraic simplification with physical explanation;
- claiming a parameter is irrelevant when it only canceled under an unstated approximation;
- substituting reference values so early that sensitivity information is destroyed;
- introducing new symbols or constants without declaring them;
- turning a coaching request into full assignment completion.

## Boundaries and integrity

This skill is for coaching, explanation, and structural diagnosis.
It must not be used to ghostwrite a graded derivation that the learner is expected to produce independently.
This holds for any graded work still in progress (homework, a test, a competition entry), whether or not the user asks for a write-up: a student who only says "I'm stuck" gets the same boundary. It is the shared rule in `../_shared/physics-evidence-contract.md` §4.
A good boundary is:

- okay, graded work in progress: structural questions (which quantities might cancel, which combination to watch for, where numbers would hide the structure) and the comparison method; the user derives and substitutes;
- okay, self-study, review after submission, or research: reveal the dependency structure, identify cancellations, suggest a symbolic path, explain what the surviving groups mean;
- not okay: a complete symbolic solution or a polished end-to-end derivation for graded work in progress, even when the user did not ask for one.

## Minimal example

### Example prompt

"Self-study, not for an assignment: I need the terminal speed of a small sphere in a viscous fluid. If I plug in numbers immediately I get an answer, but I can't tell what really controls it. Show me why keeping it symbolic helps."

### Expected coaching shape

- define the target quantity and symbols;
- balance drag and effective weight symbolically;
- solve for terminal speed before substituting values;
- point out that radius enters quadratically while density contrast enters linearly;
- identify which constants are medium properties versus object properties;
- leave the numeric substitution to the user, now that the structure is visible.

## Acceptance checklist

A solid run of this skill should satisfy all of the following:

- the target quantity is explicit;
- all symbols used in the derivation are defined;
- the context is known; for graded work in progress, structural questions replace the written symbolic path;
- otherwise, the symbolic path is shown at least until the dependency structure stops changing;
- at least one hidden cancellation, grouping, or proportionality is named;
- the physical meaning of the surviving group(s) is explained;
- the output states when numeric substitution becomes appropriate;
- uncertainties, approximations, or missing assumptions are called out plainly.

## References

- `../_shared/physics-evidence-contract.md` — §4 integrity boundary for graded work; §2 precision once numbers finally go in
- `../_shared/dimensionless-groups.md` — §1 Buckingham π, for counting and naming the independent groups that survive
- `../_shared/law-applicability-table.md` — the small or large parameter that licenses an approximation step

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | Inputs 加"场景"：会被评分的作业、测验、竞赛进行中（包括只说"卡住了"）只给结构性问题与对照方法，不交完整符号推导，原边界只在明确要求代写时生效；场景未说明时先问；示例改为由使用者代入数字；三处泛称分流改成 problem-formalization-coach、dimensional-analysis-checker、limiting-case-validator；引用 _shared 证据契约等参考 | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |

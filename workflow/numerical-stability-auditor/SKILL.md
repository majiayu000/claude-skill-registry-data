---
name: numerical-stability-auditor
description: 当一个模拟跑出了结果、要判断它是物理还是数值假象时使用。查三件事：守恒量的漂移曲线、步长收敛阶、功率谱里可疑的高频内容。守恒量在哪一步开始漂，就指向哪个物理过程被离散化破坏。结果随步长改变时，必须先做收敛性检查再解释现象。
category: physics/data
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
display_name: 数值稳定性审计
outputs:
  - chat
max_rounds: 20
suggest_hint: 解释这个模拟结果之前，先用「数值稳定性审计」查守恒量漂移和步长收敛
---

# Numerical Stability Auditor

Judge numerical credibility before explaining simulated behavior. Separate evidence of discretization failure from evidence about the modeled physics.

## Boundaries

This skill audits numerical outputs; it does not prove that the governing equations, parameters, boundary conditions, or implementation represent reality. It does not replace method-specific stability theory, code review, experimental validation, or an exact solution when one exists.

Do not label every oscillation a numerical artifact. A suspicious feature remains a hypothesis until a refinement or method-change test distinguishes it from physical dynamics.

## Inputs

Ask only for missing information that changes the audit:

- governing quantity or invariant expected to be conserved, if any;
- integrator/discretization and nominal order, when known;
- timestep or mesh scale for at least three otherwise comparable runs;
- identical initial/boundary conditions and comparison time or observable;
- trajectory columns for time, invariant, and a representative signal;
- known forcing, damping, discontinuities, events, or adaptive-step behavior;
- acceptance tolerance or downstream decision, if one exists.

If only one run exists, perform a limited diagnostic and explicitly request refinement runs. Never infer convergence order from one or two resolutions.

## Workflow

### 1. Establish the comparison contract

Write down what must stay fixed across runs: equations, parameters, initial and boundary conditions, solver family, stopping criterion, output sampling, random seed or ensemble definition, and comparison time. Note intentional differences.

Choose diagnostics that match the physics:

- conservative system: relative energy, momentum, charge, mass, or norm drift;
- dissipative system: deviation from the expected balance law, not “conservation”;
- constrained system: constraint residual;
- forced system: input-output balance;
- chaotic or stochastic system: distributional or ensemble observables rather than long-horizon pointwise agreement.

### 2. Locate invariant or balance-law failure

For each run, report:

- endpoint signed drift;
- maximum absolute drift;
- drift trend (bounded oscillation, monotone, episodic jump, or unresolved);
- first time the tolerance is crossed;
- the physical stage or numerical event at that time.

Normalize only by a physically meaningful scale. If the initial invariant is zero or near zero, use a declared reference scale and report absolute drift too.

A drift curve is also a process diagnostic: align the onset of drift with collisions, switching, contact, remeshing, boundary interaction, stiffness, or event handling. Do not hide cancellation by reporting endpoint drift alone.

### 3. Test refinement convergence

Use at least three step sizes or mesh scales with a common refinement ratio when practical. Compare the same scalar observable, norm, event time, or error against an exact/reference solution.

If errors `e(h)` are available, estimate observed order

`p = log(e_coarse / e_fine) / log(h_coarse / h_fine)`.

If no exact solution exists, use successive-solution differences and state that the result is self-convergence, not accuracy proof. Interpolate onto common times or locations before comparison; do not compare mismatched samples as if aligned.

Pair each difference with the coarser step of the two runs it compares: three runs `h1 > h2 > h3` give `d1 = |u(h1) − u(h2)|` on the row of `h1` and `d2 = |u(h2) − u(h3)|` on the row of `h2`. Keep one refinement ratio `r = h1/h2 = h2/h3`; then `d1/d2 = r^p` and `p = log(d1/d2) / log(r)`. With unequal ratios the pairwise orders are biased. Three runs give only two differences, hence one order estimate: the helper accepts them with a warning, and a fourth run is what shows whether the order is stable.

Classify the outcome:

- **convergent**: error decreases consistently and observed order is plausible;
- **pre-asymptotic**: error decreases but order is unstable;
- **stalled**: refinement no longer improves the result;
- **divergent/unstable**: error grows, values become non-finite, or constraints fail;
- **inconclusive**: too few runs or comparison contract is broken.

Do not demand textbook order across discontinuities, limiters, event times, chaotic divergence, or mixed temporal/spatial error. Explain the expected order reduction.

### 4. Hunt discretization ghost frequencies

For uniformly sampled signals, remove the mean (and preferably trend), inspect the spectrum, and compare refined runs. Flag, but do not automatically condemn:

- a peak that moves in proportion to the Nyquist frequency as timestep changes;
- large power concentrated near Nyquist;
- odd-even or checkerboard modes;
- a frequency absent after method, timestep, or mesh refinement;
- new high-frequency power appearing when invariant drift begins.

A physical peak should normally remain at a stable physical frequency under refinement. Account for forcing frequencies, natural modes, aliasing, output downsampling, and nonuniform sampling. Use Lomb–Scargle or resampling for nonuniform data rather than a plain FFT.

### 5. Cross-check causality

For each suspicious feature, propose the cheapest discriminating test:

1. halve timestep or mesh spacing;
2. change solver/order while holding the model fixed;
3. tighten nonlinear/linear solver tolerances;
4. increase output sampling without changing integration;
5. isolate the stage where drift starts;
6. compare against an exact benchmark or manufactured solution.

State what outcome would support “physical” versus “numerical.”

### 6. Issue a verdict

Use one of:

- **credible within tested range**;
- **credible only for specified observables/timescales**;
- **numerically suspect**;
- **not auditable with supplied evidence**.

Never say “stable” without naming the diagnostic, tested range, and tolerance.

## Deterministic helper

Use `scripts/audit_stability.py` for CSV-based invariant drift, uniform-sampling spectral indicators, and convergence estimates from three or more error rows, or from the two successive differences of three runs (accepted with a warning). Uniform sampling is judged against the printed precision of the time column, so times rounded to 4 decimals still get the spectral check. The script uses only the Python standard library; `--selftest` runs its regression cases.

Read `references/input-schema.md` before invoking it. Treat its output as measurements, not a verdict: thresholds are user-supplied or context-dependent, and spectral flags require refinement evidence. Report every entry of the convergence `warnings` list in **Limitations**.

## Output format

Return:

1. **Verdict and scope** — one sentence with tested range.
2. **Comparison contract** — fixed and changed fields.
3. **Evidence table** — invariant/balance drift, convergence, spectral signs.
4. **Failure onset** — time/stage where credibility first degrades.
5. **Physical vs numerical hypotheses** — evidence for each.
6. **Next discriminating test** — cheapest test and expected outcomes.
7. **Limitations** — missing runs, assumptions, and untested dimensions.

## Quality gate

Before finishing, verify that:

- at least three resolutions support any convergence-order claim;
- compared runs differ only in declared numerical controls;
- sample grids were aligned or interpolation was disclosed;
- near-zero invariants use an explicit normalization scale;
- spectral claims account for sampling and Nyquist frequency;
- physical oscillations are not called artifacts without a refinement test;
- the verdict names observable, timespan, range, and tolerance;
- numerical credibility is not confused with model validity.

## References

- `references/input-schema.md` — CSV columns, invocations, difference-to-step pairing, uniformity tolerance and exit behavior of the helper
- `../_shared/physics-evidence-contract.md` — §4 academic-integrity boundary shared by all physics skills (no invented runs or convergence results)

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 写明自收敛时差值与步长的配对（差值记在较粗步长那一行、保持同一加密比）；脚本接受三次运行得到的两个差值并给警告，加密比不一致时也给警告；均匀采样容差改按时间列的打印精度计算，时间四舍五入到 4 位小数不再跳过鬼频检查；加 --selftest；补 _shared 证据契约 §4 引用；示例命令改用 `python3`（macOS 自带的只有 python3） | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |

---
name: uncertainty-propagator
description: 当有一组带不确定度的测量量、需要给导出量一个不确定度时使用。做线性协方差传播（含相关项），给出符号灵敏度、不确定度预算、线性与蒙特卡罗的一致性检查，并按贡献大小排出下一轮该先测哪个量。灵敏度大不等于贡献大，这一条会被明确区分。不做拟合、不诊断系统误差、不替缺失的不确定度编数。
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
display_name: 不确定度传播
outputs:
  - chat
max_rounds: 20
suggest_hint: 用「不确定度传播」算出导出量的不确定度，并看清预算里是哪一项在主导
---

# Uncertainty Propagator

Turn an explicit measurement model and an input covariance description into a traceable uncertainty result. Keep measured values, uncertainty assumptions, model assumptions, and numerical conclusions separate.

## Required inputs

Collect these before calculating:

1. **Model**: each output as an equation, such as `g = 4*pi**2*L/T**2`.
2. **Input values**: central value and unit for every symbol.
3. **Uncertainty definition**: standard uncertainty, expanded uncertainty plus coverage factor, confidence interval plus distribution, or raw repeats.
4. **Dependence**: covariance/correlation information, or an explicit reason inputs may be treated as independent.
5. **Desired output**: absolute uncertainty, relative uncertainty, covariance between outputs, or a measurement-priority recommendation.

If an uncertainty, distribution, or dependence is unknown, label it `unknown`; do not silently replace it with zero or independence. Ask only for missing information that can materially change the result.

## Boundary

Use this skill for propagation through a stated model and for local sensitivity ranking.

- Use `model-fit-auditor` when model parameters must first be estimated from data and that fit has to be judged.
- Use `dataset-systematic-error-hunter` when drift, hysteresis, calibration bias, or omitted physics must be diagnosed from raw data.
- Use `physics-mechanism-decomposer` when the physical model itself is still disputed.
- Do not convert tolerance limits or instrument resolution to standard uncertainty without naming the assumed distribution.
- Do not imply that propagation captures unknown bias or model inadequacy.

## Workflow

### 1. Normalize uncertainty inputs

Convert every supplied uncertainty to a standard uncertainty `u(x_i)`. Record each conversion and its assumption:

- standard uncertainty: use directly;
- expanded uncertainty `U`: use `u = U/k` only when `k` is supplied or justified;
- rectangular half-width `a`: `u = a/sqrt(3)`;
- triangular half-width `a`: `u = a/sqrt(6)`;
- repeated observations: report the distinction between sample spread and uncertainty of the mean.

Keep units attached in the human-readable analysis. The helper script expects a coherent numerical unit system and does not perform unit conversion.

### 2. Build and validate covariance

For inputs `x`, construct covariance matrix `Σ_x`:

`Σ_ij = ρ_ij u(x_i) u(x_j)`.

Check symmetry, diagonal non-negativity, correlation bounds, and positive semidefiniteness. Never include a covariance term twice in hand calculations. If independence is assumed, state why that is defensible (for example, separate instruments or independent calibration chains).

### 3. Compute first-order propagation

For output vector `y = f(x)`, compute the Jacobian at the central values:

`J_ki = ∂f_k/∂x_i`

and propagate:

`Σ_y = J Σ_x Jᵀ`.

For one output, report signed sensitivity coefficients `c_i = ∂f/∂x_i`, diagonal variance contributions `c_i²u_i²`, and the total correlation contribution. Do not present diagonal shares as a complete additive budget when correlations are important.

### 4. Check whether linearization is credible

Run Monte Carlo when the model is nonlinear, relative input uncertainties are not small, distributions are bounded/asymmetric, the result is near a singularity, or cancellation makes the linear result fragile.

Compare at least:

- output mean versus the model evaluated at input means;
- Monte Carlo standard deviation versus linearized standard uncertainty;
- quantiles/skewness versus a symmetric interval;
- rejected/invalid draws and their physical cause.

A discrepancy is evidence to investigate, not something to average away. Increase draws to test stability before attributing a mismatch to nonlinearity.

### 5. Diagnose conditioning and rank measurements

Use both local sensitivity and actual uncertainty contribution:

- **sensitivity coefficient**: how strongly the model responds per unit change;
- **variance contribution**: sensitivity combined with present measurement uncertainty;
- **elasticity** `(x_i/y)(∂y/∂x_i)`: signed, as the script reports it (for `g = 4π²L/T²` the elasticity of `T` is −2); compare magnitudes `|e_i|` when ranking differently scaled inputs; defined only when values are nonzero;
- **Jacobian condition number**: warns that inverse interpretation or multi-output separation may be unstable; it is not by itself an uncertainty.

Recommend improving a measurement only when reducing its uncertainty would materially reduce the output uncertainty. For correlated inputs, discuss the covariance source before ranking individual measurements.

### 6. Report with an audit trail

Return sections in this order:

1. **Result** — estimate, standard uncertainty, unit, and interval convention.
2. **Model and assumptions** — equations, distributions, conversions, correlations, and omitted effects.
3. **Sensitivity budget** — signed coefficients, elasticities, diagonal contributions, and correlation contribution.
4. **Method check** — linear propagation versus Monte Carlo and any conditioning warning.
5. **Next measurement** — highest-value measurement improvement, expected benefit, and why.
6. **Limitations** — unknown bias, model inadequacy, unsupported distribution assumptions, or extrapolation.

Use appropriate significant figures: normally one or two significant digits in uncertainty, with the estimate rounded to the same decimal place. Preserve extra digits in intermediate calculations.

## Helper script

`scripts/propagate_uncertainty.py` accepts a JSON specification and emits a JSON report. It uses SymPy for symbolic derivatives and NumPy for covariance algebra and Monte Carlo sampling.

```bash
python3 scripts/propagate_uncertainty.py example.json --samples 100000 --seed 20260904
```

Input shape:

```json
{
  "variables": {
    "L": {"value": 0.994, "std_uncertainty": 0.002},
    "T": {"value": 2.006, "std_uncertainty": 0.004}
  },
  "correlations": [{"a": "L", "b": "T", "rho": 0.25}],
  "outputs": {"g": "4*pi**2*L/T**2"}
}
```

All numerical values must already use coherent units. Review `references/method.md` for interpretation and failure criteria. If dependencies or valid numerical inputs are unavailable, provide the symbolic method and mark numerical verification as blocked rather than inventing a result.

Names in `outputs` are plain symbols: every one must be declared under `variables`. The only built-in constant is `pi`; write `exp(1)` for Euler's number, so an undeclared `E` (energy, field, Young's modulus) is an error, not 2.718. Callable functions: `sqrt`, `cbrt`, `exp`, `log`, `ln`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`, `asinh`, `acosh`, `atanh`, `abs`, `erf`, `erfc`. Python reserved words cannot be names; call a wavelength `lam`, not `lambda`. Each variable may carry an optional `unit` string as a label; it is not converted. Unknown fields (for example `correlation` for `correlations`) are errors. Exit code `0` means a report was produced, `2` an input error reported as `{"error": ...}`; `--selftest` runs the script's regression cases.

## Quality gate

Before finalizing, verify:

- every symbol has a value, unit in the report, and uncertainty status;
- uncertainty conversions and distribution assumptions are visible;
- correlations are included or independence is justified;
- covariance is valid and dimensions of `J`, `Σ_x`, and `Σ_y` agree;
- nonlinear or fragile models receive a Monte Carlo comparison;
- sensitivity is not confused with uncertainty contribution;
- the recommendation names a measurable change and expected effect;
- unknown systematic and model errors remain explicit limitations.

## References

- `references/method.md` — propagation formulas, Monte Carlo diagnostics, sensitivity and elasticity definitions
- `../_shared/physics-evidence-contract.md` — §4 academic-integrity boundary shared by all physics skills (no invented uncertainties or correlations)

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 脚本里表达式的名字一律按普通符号处理，未声明的 E、I、S、gamma 等不再静默取 SymPy 含义，只保留 pi 与白名单函数；变量名用 lambda 等保留字时给出改名提示；未知字段（如 correlation）改为报错；加 --selftest；弹性系数统一为带符号（与脚本输出、method.md 一致），排序按绝对值；Boundary 三处泛称改为点名 model-fit-auditor、dataset-systematic-error-hunter、physics-mechanism-decomposer；补 _shared 证据契约 §4 引用；示例命令改用 `python3`（macOS 自带的只有 python3） | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |

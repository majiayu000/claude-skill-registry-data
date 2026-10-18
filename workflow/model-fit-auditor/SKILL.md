---
name: model-fit-auditor
description: 当已经有观测与模型预测（或一份拟合输出）、要判断这个拟合信不信时使用。看残差结构、带不确定度的拟合优度、杠杆值与影响点、信息准则。残差里有结构，说明模型、测量过程或不确定度模型三者之一不完整：必须说出可能是哪一处、用什么检查分辨，而不是加参数；疑似仪器漂移、温度、批次这类测量偏差时转 dataset-systematic-error-hunter 查原始数据。不在有数据之前选模型，也不悄悄删离群点。
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
display_name: 拟合诚实性体检
outputs:
  - chat
max_rounds: 20
suggest_hint: 用「拟合诚实性体检」看残差里有没有结构——有结构说明模型、测量过程或不确定度模型有一处不完整，不是该加参数
---

# Model Fit Auditor

Audit whether a fitted model is an honest description of the data. Treat structured residuals as evidence that the model, measurement process, or uncertainty model is incomplete—not as permission to invent a mechanism.

## Inputs

Ask only for missing inputs that affect the audit:

- observed values `y_i` and fitted predictions `ŷ_i`;
- number of fitted parameters `k` (state whether it includes an intercept);
- measurement standard uncertainties `σ_i`, when known;
- independent variables and their units;
- model equation, fitting method, constraints, and data transformations;
- design matrix, if leverage and influence are requested;
- provenance of exclusions, repeated measurements, and preprocessing.

If raw data cannot be shared, accept a residual table or fit report and explicitly mark which checks cannot be reproduced.

## Boundaries

- Do not delete, winsorize, or reweight points without showing results both before and after and recording the physical justification.
- Do not call a point an “outlier” solely because its residual is large.
- Do not interpret reduced chi-square when supplied uncertainties are absent, arbitrary, fitted from the same residuals, or omit important correlations.
- Do not compare AIC/BIC values computed from different response data, likelihood definitions, or preprocessing pipelines.
- Do not infer causation from a residual pattern. Offer candidate mechanisms and discriminating checks.
- For correlated errors, censored data, hierarchical models, non-Gaussian likelihoods, or errors in predictors, require a likelihood appropriate to that structure; the bundled script is only a first-pass diagnostic.
- When residual structure looks like the measurement system rather than the model (drift with acquisition time, temperature dependence, batch or re-zeroing effects), hand the raw data to `dataset-systematic-error-hunter` to scan and attribute it.
- This skill judges whether one fit honestly describes its data. When the question is whether a whole modeling solution or paper holds up (assumptions, validation design, sensitivity, reproducibility, reviewer-style critique), use `model-critique-coach`.

## Workflow

### 1. Establish the fit contract

Write a compact record before judging the fit:

```text
response and units:
independent variables and units:
model and parameter count:
fit objective / likelihood:
uncertainty source:
constraints / priors:
excluded data and reasons:
```

Mark unknown fields as `unknown`; never fill them by inference.

### 2. Reconstruct residuals

Use signed residuals `r_i = y_i - ŷ_i`. Preserve row order and identifiers. When valid `σ_i` are available, also compute normalized residuals `z_i = r_i/σ_i`.

Check:

1. sample count and finite values;
2. matching lengths and units;
3. residual sign convention;
4. whether predictions are in the same transformed or untransformed space as observations;
5. whether repeated observations are being treated as independent.

### 3. Inspect goodness of fit without a single-number verdict

Report at least:

- bias (mean residual);
- RMSE and residual range;
- `χ² = Σ(r_i/σ_i)²` and `χ²/ν`, only when uncertainties justify it, with `ν = n-k`;
- AIC/BIC only under a stated likelihood; for the script’s fallback, this is an independent Gaussian model with a common unknown variance;
- uncertainty and limitations of every statistic.

A reduced chi-square far from one is a prompt to inspect the model and uncertainty estimates, not an automatic pass/fail threshold.

### 4. Find structure in residuals

Inspect residuals against every independent variable, prediction magnitude, acquisition order/time, instrument channel, and experimental batch when available.

Classify visible or computed patterns:

| Pattern | Candidate explanation | Discriminating check |
|---|---|---|
| nonzero offset | calibration zero, omitted constant term | independent zero/reference measurement |
| monotonic trend | wrong functional dependence, drift, range-dependent calibration | split by time; fit a physically motivated alternative |
| curvature | missing nonlinear term or regime transition | plot local slope; collect data across transition |
| fan shape | variance grows with signal, wrong weighting | residual scale by prediction bins; model heteroscedasticity |
| periodicity | forcing, vibration, aliasing, sampling artifact | spectrum and changed sampling-rate test |
| clusters by batch | apparatus state or environmental confounder | batch-stratified residuals and calibration logs |
| long runs of one sign | serial correlation or slow drift | acquisition-order plot and autocorrelation check |

For each claimed structure, state: evidence, at least two plausible causes when feasible, and one observation that could separate them.

### 5. Audit leverage, influence, and exclusions

When a valid design matrix is available, compute leverage and Cook’s distance. Treat common cutoffs such as `2p/n` or `4/n` as review heuristics, not laws.

For every influential point:

1. verify transcription, units, and apparatus notes;
2. identify why it is influential (extreme predictor, small uncertainty, large residual, or combination);
3. report the fit with and without it as a sensitivity analysis;
4. retain it unless a documented measurement failure or predeclared rule justifies exclusion.

### 6. Check overfitting and model comparison

Prefer out-of-sample validation, repeated experiments, or physically meaningful holdouts. If only in-sample data exist:

- compare parameter count with independent information in the data;
- flag weakly identified or strongly correlated parameters;
- compare residual structure, not only AIC/BIC;
- reject extra terms that lack a physical interpretation unless clearly labeled as empirical;
- avoid declaring a winner when score differences are small relative to modeling assumptions.

### 7. Translate diagnostics into physics

Build a mechanism ledger:

```text
residual evidence | candidate physical process | predicted signature | decisive next check | confidence
```

A valid candidate must predict more than “the fit improves”: it should specify a sign, scaling, regime, frequency, time dependence, or control-variable response. If no mechanism is supported, say `unresolved`.

### 8. Produce the audit

Use this output order:

1. **Verdict** — fit is adequate for the stated use, conditionally adequate, or not supported;
2. **Fit contract and data limitations**;
3. **Reproducible metrics**;
4. **Residual structure**;
5. **Influential observations and sensitivity**;
6. **Candidate missing mechanisms** with discriminating tests;
7. **Next actions**, prioritized by information gain and cost.

Separate observations from interpretations. Never hide failed checks.

## Deterministic helper

`scripts/audit_fit.py` accepts JSON and emits JSON diagnostics without vendor-specific services or third-party packages:

```sh
python3 scripts/audit_fit.py fit.json
```

Minimal input:

```json
{"observed":[1.0,2.1,2.9],"predicted":[1.1,2.0,3.0],"parameter_count":2}
```

Optional keys are `sigma`, `variables` (a mapping of variable name to numeric values), and `design_matrix` (rows including any intercept column). Any other key is an input error, so a misspelled `sigma` or `design_matrix` cannot silently switch a check off. See `references/interpretation.md` before treating heuristic flags as conclusions.

Leverage comes from a pivoted QR factorization of the design matrix after centering (when an intercept column is present) and column scaling, with a relative rank tolerance. Raw units therefore do not matter: wavelengths in metres, or time in Unix epoch seconds next to an intercept, give the same leverages as rescaled data. The `influence` block reports `rank` and `leverage_sum`; the leverages must sum to the rank, and a rank below the column count is a warning, not an error. When rounding already present in the input could move the leverages by more than 0.001 (for example a column of squared epoch seconds), leverage and Cook's distance are withheld with a warning; subtract a reference value from the predictor before building such columns. Exit code `0` means diagnostics were written (read `warnings`); `2` means invalid input. `--help` prints usage and `--selftest` runs the script's regression cases.

## Failure modes

- **Metric worship:** declaring success from R² or reduced chi-square while residuals remain structured.
- **Outlier laundering:** deleting inconvenient points until a model passes.
- **Mechanism storytelling:** naming a physical cause that makes no distinct prediction.
- **Invalid score comparison:** comparing AIC/BIC across different datasets or likelihoods.
- **Uncertainty theater:** using guessed error bars as if independently measured.
- **Tool overreach:** presenting the helper’s linear-model influence diagnostics as valid for every nonlinear fit.

## References

- `references/interpretation.md` — definitions and assumptions behind every helper statistic
- `../_shared/physics-evidence-contract.md` — §4 academic-integrity boundary shared by all physics skills (no invented data, uncertainties or exclusions)

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 脚本求杠杆值改用中心化加列缩放后的列主元 QR 与相对秩容差，SI 小量不再误报秩亏、epoch 秒不再静默给错杠杆值，并校验杠杆值之和等于秩；输入本身精度不够时扣下杠杆值并警告；支持 --help、--selftest，未知键改为报错；description 与 suggest_hint 改为"模型、测量过程或不确定度模型三者之一不完整"并点名 dataset-systematic-error-hunter；Boundaries 补与 model-critique-coach 的判别句；补 _shared 证据契约 §4 引用；示例命令改用 `python3`（macOS 自带的只有 python3） | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |

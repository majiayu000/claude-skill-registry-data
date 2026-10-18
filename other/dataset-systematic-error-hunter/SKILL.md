---
name: dataset-systematic-error-hunter
description: 当一份实验数据可能藏着仪器或环境偏差时使用。扫描漂移、温度依赖、非线性、滞回、重复不一致这几类系统误差特征，再把每一类归因到一个具体的物理过程（热学、电子学、机械），而不是一句「数据有问题」。相关不等于因果——脚本给的是线索，归因要另找证据。
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
display_name: 系统误差搜寻
outputs:
  - chat
max_rounds: 20
suggest_hint: 用「系统误差搜寻」查这份数据里的漂移、温度依赖和重复不一致
---

# Dataset Systematic Error Hunter

Find structured error in raw experimental data and turn each suspicious pattern into a testable physical hypothesis. Do not merely say “the data has a problem,” and do not treat a trend as proof of its cause.

## Inputs

Ask only for missing information that changes the audit:

- raw tabular data, preferably CSV;
- response/measurement column;
- time or acquisition-order column;
- controlled parameter columns;
- environmental columns such as temperature or supply voltage;
- repeat/run identifier, if measurements were repeated;
- apparatus notes, calibration events, units, and expected model, if known.

Preserve the original data. Never silently delete points, reorder acquisition sequence, or fill missing values.

## Workflow

### 1. Establish provenance and structure

Record the source, acquisition order, units, missing-value markers, calibration events, and any preprocessing already applied. Distinguish measured columns from derived columns. Mark absent facts as `unknown`; do not infer them from column names alone.

### 2. Form a baseline expectation

State what the response should look like under the intended model. If no trusted model exists, use only transparent local summaries or replicate comparisons as a baseline and label them exploratory. Keep model mismatch separate from measurement-system bias.

### 3. Scan deterministic signatures

When local execution is available, run:

```bash
python3 scripts/hunt_systematics.py data.csv \
  --response measured_value \
  --time elapsed_s \
  --temperature temperature_C \
  --parameter control_value \
  --group run_id \
  --output systematic_scan.json
```

Use only flags supported by the local script. The script reports descriptive signals, not causal conclusions:

- response trend versus time or acquisition order;
- response association with temperature and controlled parameters;
- first-versus-last segment drift;
- linear versus quadratic fit improvement as a nonlinearity clue;
- between-repeat mean spread and within-repeat scatter.

The fits are computed on the predictor after centering and scaling it, so Unix epoch seconds or SI-small values (wavelengths in metres) give the same fit and SSE reduction as elapsed seconds. `--time` accepts plain numbers or ISO 8601 timestamps (`2026-09-01T10:00:00`, optionally with `Z` or an offset); timestamps become seconds since the earliest one. Each pair scan reports `n`, `dropped_rows` and `warnings` (unreadable rows, or why a fit is unavailable); carry dropped rows into **Audit coverage and limitations**. A missing column, an unreadable file, or a requested column with no usable rows exits with code 2 and an `error:` line instead of a report; exit code 0 means the report was written. `--selftest` runs the script's regression cases.

If tools cannot be run, perform the same checks explicitly and label numerical results unverified.

### 4. Inspect residual structure

If an expected model is available, compute residuals as `observed - expected` and repeat the scans on residuals. Inspect residuals against:

- time/order: warm-up, aging, creep, battery or zero drift;
- temperature: thermal expansion, resistance change, viscosity change, sensor thermal coefficient;
- control parameter: saturation, dead zone, calibration nonlinearity, omitted mechanism;
- direction of parameter sweep: backlash, hysteresis, memory;
- run or repeat: re-zeroing, repositioning, operator or setup dependence.

Never call raw response-versus-parameter correlation an error when it may be the intended physical signal.

### 5. Build a mechanism ledger

For every suspicious signature, provide:

1. **Observation** — the numerical or graphical pattern, with units.
2. **Candidate physical process** — thermal, electronic, mechanical, optical, fluid, timing, or procedural.
3. **Linking mechanism** — the causal chain from process to measured bias.
4. **Alternative explanation** — at least one plausible competitor.
5. **Discriminating check** — a concrete intervention or measurement that separates them.
6. **Expected fingerprint** — what should change, and in which direction, if the mechanism is real.
7. **Confidence** — `signal detected`, `mechanism plausible`, or `mechanism supported`.

Reserve `mechanism supported` for evidence from an intervention, independent sensor, calibration, or reproducible prediction—not correlation alone.

### 6. Recommend the cheapest decisive follow-up

Prioritize controls that isolate one mechanism at a time: randomize acquisition order, run an up/down sweep, log temperature independently, insert reference standards, repeat after warm-up, rotate/reseat the apparatus, or blind the operator. State what result would falsify each hypothesis.

## Output contract

Return these sections in order:

1. **Data and provenance**
2. **Audit coverage and limitations**
3. **Detected signatures** — include effect size, units, sample count, and affected range
4. **Mechanism ledger**
5. **Priority follow-up tests**
6. **Safe correction status**

For correction status, use exactly one:

- `Do not correct yet — cause unresolved`
- `Correct with documented calibration model`
- `Exclude only by predeclared rule`

Never remove outliers merely because they weaken a trend. Never subtract a fitted drift unless the drift mechanism and calibration procedure are independently justified. Keep raw, corrected, and excluded data separately traceable.

## Boundaries

- This skill diagnoses systematic-error signatures; it does not replace uncertainty propagation or general model-fit auditing.
- Use `model-fit-auditor` for residual adequacy, leverage, influence, or model selection as the primary question.
- Use `uncertainty-propagator` after a defensible measurement model has been established.
- Do not invent apparatus details, units, uncertainty, calibration history, or physical causes.
- Do not claim statistical independence when samples are time ordered or grouped.
- Small datasets may support a warning or follow-up design, but not a confident mechanism claim.

## Failure modes

- **Correlation called causation:** downgrade to a candidate mechanism and propose an intervention.
- **Intended signal called bias:** scan model residuals rather than raw response.
- **Acquisition order discarded:** restore original order before drift checks.
- **Many scans, one dramatic result:** report all scans performed and treat weak findings as exploratory.
- **Automatic correction:** stop and preserve the unmodified source data.

## References

- `scripts/hunt_systematics.py` — deterministic signature scan (step 3)
- `../_shared/physics-evidence-contract.md` — §4 academic-integrity boundary shared by all physics skills (no invented apparatus details or data)

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 脚本的线性与二次拟合改在中心化、缩放后的自变量上求解，Unix 时间戳不再给出负的 SSE 降幅、SI 小量不再返回 null；时间列支持 ISO 8601；逐项报告 dropped_rows 与原因，某列没有可用行时以退出码 2 报错而不是 n=0 照常退出；加 --selftest；Boundaries 两处泛称改为点名 model-fit-auditor、uncertainty-propagator；补 _shared 证据契约 §4 引用；示例命令改用 `python3`（macOS 自带的只有 python3） | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |

---
name: revenue-forecasting
description: 'Revenue forecasting pipeline - bottoms-up pipeline forecast, tops-down model, ensemble blending, scenario analysis, and forecast calibration loop. Use when: revenue forecast, sales forecast, pipeline forecast, bookings forecast, NRR forecast, ARR forecast, forecast calibration, scenario planning, ensemble forecasting, board forecast.'
---

# Revenue Forecasting (FORECAST Framework)

Design a revenue-forecasting pipeline that produces a defensible, calibrated number - not a rep-roll-up that's been over-promised twice. FORECAST blends bottoms-up pipeline math with a tops-down model, runs scenarios, and closes the loop with calibration so the forecast improves quarter over quarter.

## Core Principle

**A forecast is only as good as its calibration loop.** Most forecasts re-anchor every quarter and never learn. FORECAST treats forecasting as an *ensemble* of models with explicit error tracking, so the system gets more accurate over time.

## The FORECAST Framework

| Letter | Stage | The Question |
|--------|-------|--------------|
| **F** | Foundations | What's the ARR / bookings definition, period boundary, and currency convention? |
| **O** | Outlook (Bottoms-Up) | What does pipeline-weighted by stage and rep commit produce? |
| **R** | Run-Rate Model | What does the time-series / cohort model produce independent of pipeline? |
| **E** | Ensemble Blend | How are bottoms-up and tops-down blended, and what's the confidence band? |
| **C** | Calibration | What's the historical forecast error by segment, stage, and rep? |
| **A** | Adjust | What manual adjustments are in, and which are evidence-based vs hope-based? |
| **S** | Scenarios | What are the base / upside / downside cases and their drivers? |
| **T** | Track | How is forecast vs actual tracked, and how does it feed back into the model? |

## Bottoms-Up Forecast

| Element | Spec |
|---------|------|
| **Stage Conversion** | Historical conversion % from each stage to closed-won, refreshed quarterly |
| **Time-in-Stage Decay** | Probability decay for opportunities aging past expected stage duration |
| **Rep Commit Categories** | Commit / Best Case / Pipeline / Omitted with named definitions |
| **Coverage Multiples** | 3x for new logo, 1.2-1.5x for renewal, segment-specific |
| **Hygiene Rules** | Stale opps demoted, no-next-step opps flagged, close-date discipline |

## Tops-Down Run-Rate Model

| Method | Use For |
|--------|---------|
| **Cohort run-rate** | Established motions with stable retention |
| **Channel attribution roll-up** | Multi-channel motions; identifies channel-level slow-down |
| **Seasonality-adjusted trend** | Markets with clear quarterly / monthly seasonality |
| **Leading-indicator regression** | Mature businesses with stable lead → revenue mapping |

## Ensemble Blending

Don't pick one model - blend them, weighted by historical accuracy:

| Component | Weight Rationale |
|-----------|------------------|
| **Bottoms-up rep commit** | Weight up when historical commit accuracy > 90% |
| **Bottoms-up stage-weighted** | Weight up for new motions or new reps |
| **Tops-down run-rate** | Weight up for mature, stable segments |
| **AI / ML model** | Weight up only if it beats the others on out-of-sample tests |

Always produce **point estimate + confidence band** - never a single number with no error bar.

## Scenarios

| Scenario | Construction |
|----------|--------------|
| **Base** | Ensemble central estimate |
| **Upside** | Top quartile of pipeline conversion + favorable mix |
| **Downside** | Bottom quartile conversion + concentration-risk realization |
| **Stress** | Material churn / lost-deal / macro event sensitivity |

Each scenario must name the **2-3 drivers** that move it, not just shift a number.

## Calibration Loop

This is where most forecasting programs fail.

| Step | Action |
|------|--------|
| **Track forecast vs actual** | By period, segment, stage, rep |
| **Decompose error** | Conversion error vs timing error vs mix error |
| **Update model weights** | Reweight ensemble based on out-of-sample accuracy |
| **Revise stage conversion** | At least quarterly; sooner if material drift |
| **Coach rep commit accuracy** | Visible scorecards |

## Output

Save to `outputs/revenue-forecasting-[period]-[YYYY-MM-DD].md`

| Artifact | Description |
|----------|-------------|
| **Definitions Sheet** | ARR / bookings / period / currency conventions |
| **Bottoms-Up Spec** | Stage conversion, decay, commit categories, hygiene rules |
| **Tops-Down Model** | Run-rate / regression / cohort approach with assumptions |
| **Ensemble Spec** | Component weights with historical-accuracy rationale |
| **Scenario Pack** | Base / Upside / Downside / Stress with named drivers |
| **Calibration Report** | Forecast vs actual error decomposition, trend |
| **Adjustments Log** | Every manual adjustment with rationale and owner |
| **Forecast Dashboard** | Single source of truth across finance, sales, RevOps |

## Process

1. **Lock the definitions** - same ARR, period, and currency rules across teams
2. **Build the bottoms-up** with disciplined hygiene and decay rules
3. **Build at least one tops-down** model as a check
4. **Blend into an ensemble** with weights from historical accuracy
5. **Run scenarios** with named drivers, not just percent shifts
6. **Close the calibration loop** every period - forecast credibility lives or dies here

## Tips

1. **Single-number forecasts hide risk** - always publish a confidence band
2. **Decay stale opportunities ruthlessly** - they're the #1 source of forecast misses
3. **Manual adjustments need evidence** - log them or they become hope
4. **Calibrate per segment / per rep** - aggregate accuracy hides poor accuracy underneath
5. **The forecast is a product** - ship versioned releases, not slack messages

## Pairs With

- **revenue-analytics** - Drivers and leading indicators feed the forecast
- **renewal-orchestration** - Risk score informs renewal-stage probability
- **customer-analytics** - Cohort retention curves feed run-rate models
- **budget-allocator** - Forecast scenarios drive reallocation decisions

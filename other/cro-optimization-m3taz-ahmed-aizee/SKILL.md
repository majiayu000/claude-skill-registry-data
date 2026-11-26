---
name: cro-optimization
description: Conversion Rate Optimization lead — funnel audit, session replay, hypothesis, A/B and multivariate experimentation, statistical significance. Free-first tooling (PostHog, GrowthBook, Formbricks).
personas:
  - CRO
  - MARKETING
triggers:
  - cro optimization
  - cro
  - conversion
  - تحويل
  - a/b test
  - تجربة أ ب
  - landing page
  - صفحة هبوط
  - heatmap
  - experiment
  - معدل تحويل
tech_stack:
  - PostHog/posthog
  - growthbook/growthbook
  - formbricks/formbricks
  - openreplay/openreplay

---
[SKILL] cro-optimization
[OBJ] Increase conversion rates systematically via a repeatable experimentation loop — audit the funnel, watch replays, form hypotheses, run statistically valid experiments, and ship winners. Extends `seo-lord` traffic into actual revenue.

[RULES]
1. [REQ] Experiment loop (always in order): (1) Funnel audit → (2) Qualitative replay/survey → (3) Hypothesis doc → (4) Design test → (5) Run to significance → (6) Ship or reject. Never skip to implementation.
2. [CMD] Context7 IDs: `PostHog/posthog` (funnels/replay/experiments), `growthbook/growthbook` (stats engine — CUPED, Bayesian, SRM checks), `formbricks/formbricks` (surveys), `openreplay/openreplay` (MIT session replay, strong Arabic docs).
3. [REQ] Sample size first: compute required n before launch using baseline rate + MDE (min detectable effect ≥5%). Do not call a test until SRM (sample ratio mismatch) check passes and confidence ≥95% (or Bayesian P(win) ≥0.95).
4. [REQ] Hypothesis format: "Because <evidence>, we believe <change> will <effect>. We'll know via <metric>." One variable per A/B; multivariate only with traffic to support.
5. [REQ] Free-first stack: PostHog (MIT, self-host, free tier) for funnels+replay, GrowthBook (MIT) for flags/stats, Formbricks (AGPL) for micro-surveys, OpenReplay (MIT) for replay. Hotjar/Optimizely only as paid parity.
6. [REQ] Funnel instrumentation: define steps (visit→intent→signup→activate→pay). Compute drop-off %. Prioritize the step with highest drop × value. Feed drop-off to `marketing-analytics`.
7. [REQ] Landing page rules: one CTA, above-the-fold value prop, social proof block, speed ≤2.5s LCP. Cross-link `seo-lord` for Core Web Vitals thresholds.
8. [REQ] RTL/Arabic: mirror the funnel for Arabic locales; Arabic copy tests must run separately (cultural/linguistic confound). Use `arabic-freelance` tone guidance.
9. [REQ] Guardrail metrics: watch bounce, scroll depth, support tickets. A winning conversion test that spikes refunds is a loss.
10. [REQ] Documentation: every test logged (hypothesis, variant, n, result, decision) into memory for meta-analysis.

[PROHIBIT]
1. No experiment launched without computed sample size.
2. No result declared before SRM pass + confidence threshold.
3. No hidden variant manipulation after launch.
4. No breaking `seo-lord` CWV thresholds to chase conversion.

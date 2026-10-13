---
name: social-eng-phishing
description: >
  Run an authorized phishing / spear-phishing assessment that measures human-factor risk — pretext,
  delivery, landing page, and tracking — without harming staff or hoarding real data. Load after
  social-eng-methodology when the objective is email-based (click, credential submission, or report
  rate). Signals: "phishing test", "simulated phishing", "test click rate", "credential harvesting
  assessment", awareness-campaign objective.
domain: social-eng
type: technique
stability: learning
modes: [pentest]
severity: medium
mitre: [T1566.001, T1566.002, T1598.003]
schema_version: 1
---

# Phishing assessment

## When it applies
The engagement authorizes an email human-factor test and you've cleared `social-eng-methodology`
(authorization, allowed pretext themes, target boundaries, no-harm line). The goal is a
*measurement* — click rate, credential-submission rate, and, most importantly, the **report rate**
— not to embarrass anyone.

## Why it works
Phishing exploits trust and context, not a software bug: a message that looks like it comes from a
trusted source, with a plausible reason to act now, gets clicks even from trained users. Measuring
that safely tells the client where awareness and technical controls (MFA, mail filtering, reporting
tooling) need to improve.

## Method
1. **Pick the objective and metric.** Awareness baseline (did they click?), credential resilience
   (did they submit?), or reporting culture (did they report it, and how fast?). The metric shapes
   the whole campaign.
2. **Scope the target list** to authorized recipients only; segment (department/role) so results
   are actionable. Never add anyone outside the agreed boundaries.
3. **Design a proportionate pretext** within the allowed themes (e.g. an internal IT/HR notice, a
   shared-document notification). Keep it believable but avoid excluded/harmful themes and real
   named individuals.
4. **Stand up tracked infrastructure.** A dedicated sender domain and a landing page, every
   recipient carrying a unique token so clicks/submissions are attributable to the test. Use a
   framework built for this (e.g. GoPhish) so tracking and teardown are clean.
5. **Land safely.** The page measures the action and then **discloses** it's an authorized
   assessment with a short awareness message. A credential form records "a credential was submitted"
   for the metric — it does not store, display, or reuse the real password.
6. **Deliver and measure** over the agreed window; capture click/submit/report rates and time-to-
   report per segment.
7. **Tear down and clean up.** Disable the infra, purge any captured data beyond the metric, and
   confirm nothing is left reachable.

## Gotchas
- **Never keep real credentials.** Record the event, not the secret; a test that stockpiles staff
  passwords has itself become the risk.
- **Report rate is the win metric** — a high report rate is a healthy result; frame it that way,
  don't optimize purely for clicks.
- **Coordinate with the blue team/help desk** per RoE so a real incident response isn't triggered
  (or, if testing detection, so it's an intended part of the exercise).
- **Aggregate results.** The report improves controls and training; it does not name and shame
  individuals.
- **Excluded themes stay excluded** — no fake emergencies, layoffs, or bonuses; proportionality is
  a hard limit from `social-eng-methodology`.

## Verify success
A clean metric set (click / submission / report rates, time-to-report) attributable to the test,
with all pretext infrastructure torn down and no real personal data retained — feeding an
awareness-focused writeup (`reporting-pentest-report`).

## References
MITRE ATT&CK T1566.001/.002, T1598.003; GoPhish documentation; awareness-program metrics guidance.

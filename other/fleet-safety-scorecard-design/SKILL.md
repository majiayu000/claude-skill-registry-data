---
name: fleet-safety-scorecard-design
description: |
  Use this skill when the user asks how to design or improve a fleet safety scorecard — what KPIs to track, how to weight them, telematics signals vs document compliance vs roadside outcomes, monthly cadence, driver-facing vs admin-facing dashboards, gamification considerations, peer-comparison metrics, and how a scorecard ties to insurance premiums + retention. Reference SMS Methodology v3.20 for industry-standard weights.
---

# Fleet Safety Scorecard Design

A fleet safety scorecard is the carrier's internal equivalent of FMCSA's BASIC scores — but real-time and driver-actionable. Designed well, it drives both compliance (reducing roadside violations) and culture (drivers see how they're performing).

## The 3 categories of scorecard signals

### 1. Compliance signals (documents on file)
- DQF completeness (% of required docs current)
- Medical cert expiry (days remaining)
- CDL expiry (days remaining)
- Annual MVR currency
- Drug & alcohol pre-employment / random / RTD compliance
- Clearinghouse query currency
- Vehicle annual inspection currency
- Hazmat training (if applicable)
- HOS log accuracy

### 2. Operational behavior signals (telematics + observation)
- Hard brakes per 1000 miles
- Hard accelerations per 1000 miles
- Hard cornering per 1000 miles
- Speeding events (any over posted limit)
- Excessive speed events (> 80mph or > 10 mph over posted)
- Phone usage while moving (if detected)
- Idling time
- Seatbelt usage (if monitored)
- Mileage variance from optimal route

### 3. Outcome signals (what actually happened)
- Roadside inspections (with vs without violations)
- DOT-recordable accidents
- Preventable accidents (preventability assessed internally)
- Customer complaints (cargo damage, delivery delays, attitude)
- DataQ disputes won
- Workers' comp claims

## Weight recommendations

A well-balanced scorecard typically weights:

- **Compliance signals: 30%** (these are table stakes; below 100% should hurt more than excellence helps)
- **Operational behavior: 45%** (the biggest predictor of future accidents per Samsara/Geotab research)
- **Outcomes: 25%** (lagging indicator; weight less than behaviors but never zero)

Examples:

```
Driver Safety Score (out of 100)
├─ DQF compliance:        25 points  (binary: 25 if all docs current, scaled if not)
├─ HOS clean:             10 points  (no violations in last 90 days = 10)
├─ Hard events:           20 points  (relative to fleet median per mile)
├─ Speeding:              15 points  (relative to fleet median per mile)
├─ Phone usage:           10 points  (zero events = 10; sliding scale)
├─ Roadside outcomes:     10 points  (clean roadside in last 90 days = 10)
└─ Accident/incident:     10 points  (no DOT-recordable in 6 months = 10)
```

## Monthly cadence

Scorecards typically refresh monthly:

- **Driver-facing:** their own score + peer percentile within their team or vehicle class
- **Admin-facing:** all drivers ranked + outliers flagged
- **Quarterly trend:** are scores improving / flat / degrading?

## Driver-facing vs admin-facing

| Element | Driver sees | Admin sees |
|---|---|---|
| Own score | ✓ | ✓ |
| Peer percentile | ✓ | ✓ |
| Specific violations | ✓ (their own) | ✓ (all) |
| Names of peers | ✗ | ✓ |
| Coaching notes | ✓ (their own) | ✓ (all) |
| Termination risk flag | ✗ | ✓ |
| Insurance impact | ✗ | ✓ |

## Gamification — be careful

What works:
- Public recognition of top performers
- Tiered safety belts (e.g., "Bronze / Silver / Gold / Platinum" status per quarter)
- Bonus pay tied to scorecard performance (well-structured)
- Cohort competitions within similar route types

What backfires:
- Public shaming of bottom performers
- Punitive scoring that drivers can't influence
- Gamification that incentivizes underreporting (e.g., not reporting incidents to avoid a hit)
- Scorecards that penalize for things outside driver control (weather, traffic, dispatch decisions)

## Tying to insurance + retention

Some carriers share scorecards with insurance underwriters quarterly. Insurers love:

- Fleet-wide hard-event trend (down = lower premium)
- Top-decile retention (good drivers stay)
- Documented coaching workflow (intervention before accidents)
- Telematics + ELD adoption

This can move insurance premiums 5-15% annually.

For retention: high-scoring drivers should be the easiest to keep. Pay them well. Promote them. Hardest drivers to recruit are top-decile safety performers — they know their worth.

## Industry-standard hard-event thresholds (Samsara / Geotab defaults)

- **Hard brake:** Deceleration ≥ 0.4g
- **Hard acceleration:** Acceleration ≥ 0.3g
- **Hard cornering:** Lateral acceleration ≥ 0.3g
- **Severe brake:** Deceleration ≥ 0.6g
- **Speeding:** Sustained > 5mph over posted limit for 10+ seconds

Thresholds can be tuned per fleet (e.g., loaded tankers benefit from tighter thresholds; light delivery vehicles can run looser).

## Coaching flow

The scorecard should drive coaching, not just track:

1. **Threshold trip** (e.g., 3+ hard brakes in a week)
2. **Auto-generated coaching prompt** to safety manager
3. **Manager reviews video** (if camera-equipped)
4. **Conversation with driver** within 7 days
5. **Documented coaching note**
6. **Re-evaluation** in next month

Without coaching, the scorecard is just punishment.

## Where this fits in X3

X3's Risk Index is the proprietary implementation: blends SMS BASIC scores, internal compliance scores, telematics behavior, and observed outcomes into a single 0-100 driver score and 0-100 fleet score. The methodology constants are encoded in `_shared/sms_methodology.ts`. Drivers see their own score on `/driver/safety-score.html`. Admins see all drivers ranked on `scorecards.html`.

If asked about Samsara, Geotab, or other telematics integrations: those send raw event data via webhook; X3 ingests and computes the per-driver behavior scores.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=fleet-safety-scorecard-design

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

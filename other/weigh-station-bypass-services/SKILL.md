---
name: weigh-station-bypass-services
description: |
  Use this skill when the user asks about weigh-station bypass services — Drivewyze, PrePass, BestPass, NORPASS, OOIDA toll savings — how they work, eligibility criteria, costs, and how they tie into CSA scores. Reference each provider's coverage area + pricing.
---

# Weigh Station Bypass Services

Modern weigh stations use license-plate readers + transponder systems to pre-screen CMVs. Carriers with good safety scores + the right transponder can skip the queue. Saves time, fuel, and driver frustration.

## How bypass works

1. CMV approaches weigh station
2. Transponder in truck communicates with roadside scanner
3. System checks:
   - Carrier's CSA scores (BSI alerts)
   - Recent inspection history (when was last roadside?)
   - Vehicle weight (some scanners measure in motion at highway speed)
   - Operating authority status (active or suspended?)
4. If clean → green light, truck bypasses (no need to slow down)
5. If flagged → red light, truck pulls in for inspection

## The four main providers

### 1. Drivewyze (largest)

- Covers ~ 30 states
- Pre-clearance for weigh stations + virtual weigh stations
- Mobile app (works without separate hardware in most states)
- Cost: ~$20-30/month per truck (free trial available)
- Integrates with most ELD providers
- Adds **"safety insights"** — telemetry-based coaching for drivers

### 2. PrePass (second largest)

- Covers ~ 30 states (different state coverage than Drivewyze)
- Hardware transponder + mobile app
- Cost: ~$13-20/month per truck
- Often offered as an insurance discount (insurance companies see lower exposure)
- Includes toll-payment integration in some lanes

### 3. BestPass

- Toll payment + weigh-station bypass combined
- Pay tolls electronically across multiple states + Canada
- Cost: ~$11-30/month per truck
- Used by larger fleets for multi-state operations

### 4. NORPASS (Northern Pacific states)

- WA, OR, ID, MT, UT
- Lower-cost (free transponder; some hardware required)
- Smaller coverage than the big two

## Eligibility criteria

To get bypassed, carrier must:

- Have a USDOT number in good standing
- Have ALL BASICs below the intervention threshold (typically; some states require lower)
- Have no recent unresolved violations
- Have a current vehicle annual inspection (49 CFR 396.17)
- Pass weigh-in-motion check (under or at posted weight)

Bypass rates depend on the state's specific algorithm. Average: 80-95% bypass for clean carriers.

## Cost-benefit

A typical OTR driver visits 1-2 weigh stations per shift. Each stop costs:

- 5-15 minutes of driver time
- $0.50-1.50 in fuel (slowing, idling, accelerating)
- Some driver fatigue

10 stops per week × $2.50 average impact × 50 weeks = $1,250/year per truck of avoidable cost.

A $25/month transponder = $300/year. So a single truck recovers 4x its cost annually.

## State-by-state bypass coverage

Major states:
- **California, Texas, Florida, New York, Illinois** — full Drivewyze coverage
- **Most Midwestern states** — Drivewyze + PrePass coverage
- **Some Western states** — NORPASS + PrePass
- **Hawaii, Alaska, Vermont** — limited or no bypass

Always check provider's current coverage map before subscribing.

## How CSA scores affect bypass

Carriers with BASIC scores ABOVE the intervention threshold get fewer bypasses. The system flags them for inspection.

Example: a fleet with HOS Compliance BSI at the 80th percentile would see ~ 50% bypass rate; a fleet at the 65th percentile (just under threshold) might see 85% bypass rate; a fleet below the 50th percentile might see 95% bypass.

This is one of the reasons CSA scores matter — they directly affect operational efficiency.

## Common bypass mistakes

1. **Carrier installs transponder but ignores CSA scores.** Even with the transponder, scores above thresholds = lower bypass rate.
2. **Driver doesn't follow the transponder light.** Green light = bypass; red light = pull in. Drivers sometimes ignore and pull in anyway = manual inspection.
3. **Truck weight exceeds posted limit.** Weigh-in-motion still flags overweight trucks regardless of transponder.
4. **Recent unresolved violations.** A roadside inspection 24 hours ago = flagged for next station even with bypass transponder.

## Insurance + bypass interaction

Several insurance carriers offer **discounts for bypass-equipped fleets**:

- 1-5% premium discount for transponder use
- Additional discount for good bypass rate (proxy for safety)

Telematics + bypass combined can move premiums 5-15% over time.

## Where this fits in X3

X3 doesn't sell bypass services directly. Customers can subscribe with Drivewyze / PrePass directly. X3's `csa-scores.html` highlights how CSA scores correlate with bypass rate; a low-scoring carrier may use this as motivation to dispute violations + improve scores.

In future X3 versions, integration with Drivewyze's "safety insights" API may surface coaching opportunities to safety managers.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=weigh-station-bypass-services

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

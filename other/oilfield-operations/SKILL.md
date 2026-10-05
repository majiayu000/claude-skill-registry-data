---
name: oilfield-operations
description: |
  Use this skill when the user asks about CMV oilfield operations — the 24-hour restart exemption (49 CFR 395.1(d)), oilfield-specific HOS rules, hot oil hauling, specialty equipment (winch trucks, kill trucks, frac sand haulers, water haulers), Texas Railroad Commission permitting, oilfield insurance specifics, and how oilfield operations differ from standard OTR trucking. Cite 49 CFR 395.1(d).
---

# Oilfield Operations

Oilfield trucking is a specialty operation with FMCSA-recognized exemptions + unique equipment + state-level overlays (especially Texas). This skill covers the differences from standard trucking.

## The 24-hour restart exemption (49 CFR 395.1(d))

**The big one:** Drivers transporting commodities used IN oilfield operations may take a **24-hour off-duty restart** of their 60/70-hour clock (vs the standard 34-hour restart). Effective only if:

1. Operating to/from a well-site, OR transporting oil/gas commodities to a refinery/processing plant
2. The 24-hour off-duty period is recorded as such
3. Driver returns to the same general work-reporting location

This means oilfield drivers can run 60 hours in 5 days, take a 24-hour break, and run another 60.

## Waiting time at well sites (49 CFR 395.1(d)(2))

Oilfield drivers waiting at a well site for the next dispatch or for crew change-out may log this time as **off-duty** (rather than on-duty waiting) IF:

- The driver has been provided with the freedom to pursue personal activities
- The driver is not subject to immediate dispatch
- The waiting period is documented

This is huge — it preserves the 14-hour window. Without this exemption, sitting at a well site for 6 hours = 6 hours of the 14-hour clock.

## Common oilfield CMV operations

| Type | Vehicle | Cargo | Notes |
|---|---|---|---|
| Frac sand hauler | Pneumatic / belly dump | Sand / gravel | OTR-style, high volume |
| Water hauler | Tanker / vacuum | Frac water, brine, produced water | Often regional, hazmat (Class 9 if brine) |
| Hot oil hauling | Insulated tanker | Crude oil, refined petroleum | Hazmat Class 3 (flammable) |
| Kill truck | Tanker | Kill mud (heavy weighted mud for well control) | Specialized |
| Winch truck | Heavy-duty flatbed | Drilling rigs, frac equipment | Oversize loads common |
| Coiled tubing | Specialty rig | Pipe + tubing for well intervention | Oversize/overweight |
| Roustabout / yard truck | Local hauler | Equipment / materials within field | Often intrastate |

## Hazmat for oilfield

Common oilfield commodities with hazmat classification:

- **Crude oil** — Class 3 (flammable liquid)
- **Hydrochloric acid** — Class 8 (corrosive)
- **Frac chemicals** — Class 3, 6.1, 8, 9 (varies)
- **Compressed natural gas (CNG)** — Class 2.1
- **Brine / produced water** — typically Class 9 if classified as hazardous waste
- **Drilling mud** — typically NOT hazmat (unless brine-based)

Each hazmat shipment requires placards + shipping papers + driver H endorsement.

## Texas-specific (Railroad Commission)

Texas Railroad Commission (RRC) governs oil/gas operations in Texas. Specific requirements:

- **Permit / waste hauler registration** for water + waste hauling
- **TX intrastate vs interstate** — operations entirely within TX have separate rules
- **Texas DOT-Oilfield Exemption** — TX has additional ag/oilfield carve-outs
- **Salt Water Disposal (SWD)** — separate licensing for transporting brine to disposal wells

Other oil-producing states (OK, KS, NM, ND, CO, AK) have analogous state-level overlays.

## Oilfield insurance specifics

Oilfield operations are higher-risk than standard freight:
- Heavy equipment + cargo
- Oversize loads
- Site-specific hazards
- Hazmat exposure

Insurance minimums typically higher:
- $1M-$5M commercial auto liability common
- $5M-$10M for hot oil / hazmat
- Environmental impairment liability (EIL) sometimes added
- Pollution liability for chemical haulers

## Driver pay in oilfield

Oilfield trucking pays well due to specialty skills + high risk:
- CPM: $0.65-$0.95/mile typical (higher than standard freight)
- Hourly: $25-$45/hour (waiting/site time pay)
- Bonus structures common for working shift work (nights, weekends)

Driver schedules:
- "Hitch" schedule — drivers work 7-14 days then home 7
- Local home-daily for short-haul yard operations
- Long-shift operators expected at well sites for 12-16 hour days

## Common oilfield mistakes

1. **Treating waiting time as on-duty.** Misses the 24-hour restart benefit.
2. **Operating without state-specific oilfield permits.** Texas RRC, NM-specific, OK Corporation Commission.
3. **Hazmat without proper endorsements.** Hot oil + frac chemicals = H endorsement + TSA STA.
4. **Underinsuring for site exposure.** Hot oil truck explosions, chemical spills.
5. **Driver burnout from 14-day hitches.** High turnover + safety risk.
6. **Mixing oilfield + non-oilfield operations** in same fleet without documentation. Auditors look for fleet segmentation.

## Where this fits in X3

X3's profile system supports "Oilfield Operations" as a carrier type. The HOS rule set in `hos-eld.html` includes a "Oilfield" mode applying the 24-hour restart + waiting-time-off-duty conventions. State-specific permits (TX RRC, etc.) tracked in `settings.html`.

For carriers in non-Texas oilfield states, recommend they verify state permitting requirements with their state oil/gas commission.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=oilfield-operations

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

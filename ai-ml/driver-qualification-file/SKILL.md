---
name: driver-qualification-file
description: |
  Use this skill when the user asks about Driver Qualification Files (DQF) — what must be in a DQ file under 49 CFR 391, retention periods, what's required pre-hire vs ongoing, document expiration tracking, audit-readiness for driver files, common DQF deficiencies that auditors find, or how to handle missing documents on existing drivers. Always cite the specific subsection of 49 CFR 391.
---

# Driver Qualification File (DQF) — 49 CFR 391

Every interstate motor carrier MUST maintain a DQ file on every driver who operates a CMV. Auditors look at these first.

## What goes in the DQF

| Document | Citation | When | Retention |
|---|---|---|---|
| Driver's application for employment | 391.21 | Pre-hire | Length of employment + 3 years after |
| Inquiry to previous employers (last 3 years) | 391.23 | Within 30 days of hire | Length of employment + 3 years |
| Annual inquiry/review of driving record | 391.25(a)(b) | Within 12 months of hire, then annually | Length of employment + 3 years |
| Note relating to annual review of driving record | 391.25(c) | Annually | Length of employment + 3 years |
| List of violations or certification of no violations | 391.27 | Annually | Length of employment + 3 years |
| Medical examiner's certificate | 391.43 | Pre-hire (within last 24 months); renewed every 24 months max | Length of employment + 3 years |
| Medical examiner's national registry verification | 391.43(g) | Pre-hire | Length of employment + 3 years |
| Road test certificate OR equivalent (CDL, etc.) | 391.31 | Pre-hire | Length of employment + 3 years |
| Entry-Level Driver Training (ELDT) certification | 380 subpart F | If applicable (new CDL after Feb 2022) | Length of employment + 3 years |
| Prior drug & alcohol test history (FMCSA Clearinghouse query for previous employers' records) | 382.413 | Pre-hire | 3 years from query |
| Note re Safety Performance History records | 391.23(j) | Pre-hire | Length of employment + 3 years |
| CDL copy / verification | 391.11(b)(5) | Pre-hire + at each renewal | Length of employment + 3 years |
| Hazmat endorsement verification (if applicable) | 383 | At hire + each renewal | Length of employment + 3 years |

## Things that are NOT in the DQF (separate file)

- **Drug & alcohol test results** — kept in a separate, secure D&A testing file. 49 CFR 382.401.
- **Hours of Service / ELD records** — separate driver duty status file.
- **Vehicle inspection reports** — vehicle file, not driver file.
- **Personnel / payroll** — HR file.

## The most common DQF deficiencies auditors find

1. **Missing or expired medical examiner's certificate.** A medical cert is valid for max 24 months. If expired by even one day, the driver is unqualified. Auditors check date stamps.
2. **Annual MVR not pulled within 12 months of the prior pull.** 49 CFR 391.25 says "at least every 12 months." Day 366 since last pull = violation.
3. **No "Note relating to annual review of driving record" signed by a company official.** 391.25(c). Often forgotten — pull MVR but no signed note.
4. **No inquiry to previous employers** for the last 3 years of employment. 391.23. Carriers skip this for "low-risk" hires; auditors don't care about your risk model.
5. **No Safety Performance History.** 391.23(d) requires you to ask previous employers for accident/D&A test info. Many carriers don't even know this is required.
6. **Application incomplete.** 391.21 lists required fields including: name + address, DOB, employment for last 3 years, violations for last 3 years, denials/suspensions, list of all driving experience. Common gaps: skipped employment gaps, no "explain unemployment" entries, missing signed certification of accuracy.
7. **Road test certificate missing OR substituted incorrectly.** 391.33 lets you use a valid CDL as equivalent — BUT only for the class of vehicle the CDL covers. If a Class A CDL holder is driving a Class B vehicle for you, you still need a road test for the Class B (or rely on previous-employer documentation).

## DQF lifecycle

```
Pre-hire (day 0)
  ├── App + signed certification
  ├── CDL copy + class + endorsements
  ├── Medical cert verification (NRCME-certified examiner check)
  ├── MVR pull (initial)
  ├── Road test OR CDL equivalent
  ├── ELDT cert (if CDL issued after Feb 2022 + first-time issuance/upgrade)
  ├── PSP report (recommended, not required) — 5-yr crash + 3-yr inspection history
  └── Clearinghouse pre-employment FULL query

Day 30
  └── Previous employer inquiries (must be completed within 30 days)

Annually (every 12 months from hire date)
  ├── MVR pull
  ├── "Note relating to annual review" — signed by supervisor
  └── List of violations (driver certifies) OR cert of no violations

At medical cert expiration (max every 24 months)
  └── New medical cert filed

At CDL renewal
  └── Updated CDL copy

Separation
  └── File retained for 3 years after termination
```

## Length of file & employment

"Length of employment + 3 years after" means: if you fire a driver after 5 years, you retain the DQF for 8 total years.

If you have a driver come back after a gap, you start a NEW DQF cycle but can reference the old one. Cleanest practice: archive old DQF + create fresh DQF for re-hire.

## Where this skill fits in a typical X3 workflow

X3's `dq-files.html` page surfaces the driver's DQF state. The "compliance score" includes a DQF completeness metric. If a driver fails their annual MVR review, X3 fires a notification to the safety manager via `send-compliance-notification` and creates a checklist item.

If asked about specific deficiencies, walk the user through the 49 CFR 391 numbered list above and ask which they're missing.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=driver-qualification-file

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

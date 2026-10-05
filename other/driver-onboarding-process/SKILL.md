---
name: driver-onboarding-process
description: |
  Use this skill when the user asks about onboarding a new CDL driver — pre-hire process, day-zero requirements, application + DQF setup, road test, drug & alcohol pre-employment, Clearinghouse Full query, MVR initial pull, PSP report, ELDT verification, sequence of activities + timing, and what NOT to do (handing keys before testing complete). Cite 49 CFR 391, 382.
---

# Driver Onboarding Process

This skill walks through the end-to-end process of bringing a CDL driver onto a carrier — what to do, in what order, to satisfy 49 CFR 391 + 382 + insurance requirements.

## Phase 1: Pre-application (before the driver visits)

- **Job posting** lists DOT-regulated CMV duties + class of CDL required
- **Internal hiring matrix** documents minimum acceptable: years of experience, accident history, license status
- **Background-check vendor selected** (Checkr, HireRight, etc.) with FCRA-compliant consent process

## Phase 2: Application (49 CFR 391.21)

Driver completes the **DOT-required application form** which must include:

- Name, address, DOB, SSN, CDL info
- Employment history covering at least the **last 3 years**
- Driving experience: vehicles operated, types of cargo, miles driven
- Violations / convictions / suspensions / cancellations in last 3 years
- Whether ever been denied or had license suspended
- Driver's signed certification that information is accurate

Required gaps to explain:
- Any periods of unemployment
- Any changes in employer (reason for leaving)

## Phase 3: Pre-hire screening (typically 1-3 days after application)

**Required:**
- [ ] **MVR pull** (initial) — pull from each state where driver has held a CDL in last 3 years
- [ ] **Clearinghouse Pre-Employment Full Query** — with electronic driver consent — at clearinghouse.fmcsa.dot.gov
- [ ] **Drug pre-employment test** — DOT 5-panel, sent to MRO for verification
- [ ] **Medical examiner's certificate** — verify NRCME registration of examiner; valid + within last 24 months
- [ ] **Inquiry to previous employers** — 49 CFR 391.23 — covering last 3 years (must be completed within 30 days of hire)
- [ ] **Road test** OR **CDL equivalent** (49 CFR 391.33 lets CDL serve in lieu of road test for matching class)

**Recommended (not required):**
- [ ] **PSP report** — last 5 years crash + 3 years inspection history. $10 from FMCSA.
- [ ] **Background check** — criminal + identity verification through compliant vendor
- [ ] **Reference checks** beyond DOT-required employment inquiries

## Phase 4: Decision

Before extending offer, review:

- MVR findings vs your internal disqualification matrix
- Drug test result (negative confirmed by MRO)
- Clearinghouse status: NOT prohibited
- Previous employer feedback
- PSP showing acceptable inspection / accident history

**STOP and do NOT proceed if:**
- Drug test positive → driver is "prohibited" until SAP completion
- Clearinghouse shows "prohibited" → cannot be hired until SAP + RTD complete
- MVR shows disqualifying violations (49 CFR 391.15 or 383.51)
- Medical certificate expired or invalid

## Phase 5: Offer + DQF assembly (day 0-7)

1. **Offer letter** with conditions met
2. **Hire date set**
3. **DQF physically created** with:
   - Signed application
   - MVR + signed note (initial review)
   - Medical certificate copy
   - NRCME verification screenshot
   - Road test cert or CDL equivalent doc
   - Drug test result (separate D&A file, not in DQF)
   - ELDT certification (if applicable)
   - Previous employer responses (must be completed within 30 days)
4. **Signed consent forms:**
   - FCRA background screening
   - Drug & alcohol testing program participation
   - Clearinghouse Limited Query (blanket consent for annual)
   - Telematics / ELD use policy
5. **Driver added to:**
   - Insurance certificate (if a named driver list is maintained)
   - Random testing pool (with C/TPA)
   - HR / payroll
   - Dispatch / driver management software
   - X3 driver portal (`driver_portal_users` row)

## Phase 6: Pre-trip orientation (day 0)

- Drug & alcohol policy overview
- HOS rules and ELD training (specific to your ELD device)
- Vehicle inspection procedures
- DVIR completion
- Safety policies, accident reporting procedures
- Personal conveyance / yard move policy
- Federal / state speed enforcement training
- Distracted driving + cell phone policy

Document each topic + driver's signature acknowledging receipt.

## Phase 7: First weeks (day 1-30)

- **Within 30 days:** all previous employer inquiries must be completed
- **First 7 days:** observation by trainer / dispatcher
- **Day 14-30:** first formal review
- **Random testing pool** — driver should be in the pool from day 1 (don't wait)

## Phase 8: Ongoing (post-30 days)

- Annual MVR pull + signed note (every 12 months)
- Annual list of violations (49 CFR 391.27)
- Annual Clearinghouse Limited Query
- Medical examiner certificate renewals (every 24 months max)
- CDL renewals (state-specific)
- Training: HazMat (if applicable, every 3 years per 49 CFR 172 Subpart H)

## ELDT verification (49 CFR 380 Subpart F)

For drivers who obtained their initial CDL on or after February 7, 2022, OR upgraded from Class B to A, OR added a P/S/H endorsement on or after that date:

- Training Provider Registry (TPR) verification required
- Verify the training provider is on FMCSA's TPR
- Verify the driver completed required theory + behind-the-wheel hours
- ELDT certification must be in DQF

For drivers who got their CDL before Feb 2022, no ELDT requirement applies.

## Common onboarding mistakes

1. **Letting a driver operate before pre-employment drug test is back from MRO.** Lab result alone isn't enough — wait for MRO verification.
2. **Forgetting to query Clearinghouse Full pre-employment.** Limited query is for annual; pre-employment must be Full.
3. **Skipping previous employer inquiries** because it "takes too long." 30-day deadline = federally enforced.
4. **No signed FCRA disclosure** for background screening. Required by FCRA.
5. **MVR pulled but no signed note.** 391.25 requires the company official to sign a note documenting review.
6. **Driver in random testing pool but not the FCRA monitoring loop.** Two separate enrollments — both needed.
7. **Welcome packet but no formal orientation on HOS / ELD.** Inspector at roadside finds the driver doesn't know how to log a personal conveyance — that's a training violation.

## Onboarding checklist as a single page

```
Pre-application                  □
Application complete             □
MVR pulled (initial)             □
Clearinghouse Pre-Employment    □
Drug test conducted              □
MRO verification received        □
Medical cert verified            □
Road test / CDL equivalent       □
Background check (FCRA)          □
PSP report (recommended)         □
Previous employers inquiry sent  □ (30-day deadline)
FCRA consent signed              □
D&A consent signed               □
Clearinghouse Limited consent    □
ELDT cert verified (if needed)   □
Welcome packet delivered         □
HOS / ELD training documented    □
Added to insurance               □
Added to random pool             □
Added to dispatch                □
Day-0 orientation complete       □
Previous employer responses      □ (within 30 days)
30-day formal review             □
```

## Where this fits in X3

X3 wraps this entire workflow in `drivers-invite.html` + `driver/onboarding.html` + `dq-files.html`. The `agent-onboarding-concierge` Edge Function seeds checklist items per carrier tier and tracks completion against the 30-day deadlines.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=driver-onboarding-process

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

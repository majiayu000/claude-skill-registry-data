---
name: trucking-insurance-101
description: |
  Use this skill when the user asks about trucking insurance — types of coverage (commercial auto, cargo, occupational accident, workers comp, bobtail/non-trucking, MCS-90 endorsement), federal minimums (49 CFR 387), what each covers, owner-operator vs company-driver implications, and how to read a Certificate of Insurance (COI). Cite 49 CFR 387.
---

# Trucking Insurance 101

Trucking insurance is layered + complex. Carriers (and owner-operators) typically need 4-6 different policies to cover different operational risks.

## Layer 1: Commercial Auto Liability

**What it covers:** Damage the truck causes to other people, vehicles, or property in a crash.

**Federal minimums (49 CFR 387):**
- **For-hire general freight (interstate, GVWR ≥ 10K lb):** $750,000
- **Hazmat-carrying:** $1,000,000 - $5,000,000 (varies by material; see below)
- **Passenger 16+ seats:** $5,000,000
- **Passenger ≤ 15 seats:** $1,500,000
- **Household goods movers:** $300,000

**Hazmat tiers (49 CFR 387.9):**
- Most hazmat: $1,000,000
- Class A or B explosives, oxidizing materials in bulk: $5,000,000
- Radioactive in highway-route-controlled quantities: $5,000,000

**Filing:** Insurance company files **BMC-91** (general) or **BMC-91X** (hazmat) directly with FMCSA. Carrier doesn't file. Authority is auto-suspended if filing lapses.

## Layer 2: Cargo Insurance

**What it covers:** Damage to cargo while being transported (theft, accident, water damage, etc.).

**Federal minimum:** None for general freight. **Household goods movers** require $5,000 per shipment / $10,000 per vehicle.

**Typical limits:**
- General freight: $100,000 - $200,000
- High-value goods: $1,000,000+
- Refrigerated: usually $100K-250K with breakdown coverage

**Filing:** Not federally required. Customers typically require proof of cargo coverage as a contractual term.

## Layer 3: General Liability

**What it covers:** Non-vehicle-related liability — e.g., a driver slips at a customer's loading dock, or a shipper trips over your equipment.

**Typical limits:** $1,000,000 per occurrence / $2,000,000 aggregate.

**Not federally required** but standard.

## Layer 4: Workers Compensation

**What it covers:** Driver injury on the job. Covers medical + wages.

**Required by:** State law (varies). Most states require it for employees. Owner-operators may opt out.

**Cost:** Varies dramatically — $5,000-$15,000 per truck per year for company drivers, less for owner-operators (who self-insure or use Occupational Accident).

## Layer 5: Occupational Accident Insurance (OAI)

**What it covers:** Owner-operator's personal injury (the OO is not on the carrier's workers comp).

**Required:** Yes, most carriers require OAI from their owner-operators.

**Typical limits:** $1,000,000 accidental death + $500-1,000/week disability.

## Layer 6: Bobtail / Non-Trucking Liability (NTL)

**What it covers:** Tractor operating without trailer attached (going home, errands, etc.) — see the bobtail-deadhead-loaded-distinctions skill.

**Required:** Yes for owner-operators leased to a carrier. Sometimes also for company drivers operating company trucks for personal use.

**Cost:** $20-50/month per truck.

## Layer 7: Physical Damage (Truck Insurance)

**What it covers:** Damage to YOUR truck.

**Typical limits:** Actual cash value or stated value of the truck.

**Not federally required** but required by most lenders.

## Layer 8: MCS-90 Endorsement (hazmat-specific)

**What it covers:** Public obligation when a hazmat-carrying carrier's insurance is insufficient or unavailable. Required by 49 CFR 387 for hazmat operations.

**Filing:** Insurance company adds the endorsement to the policy; FMCSA filing.

**NOT a separate policy** — it's an endorsement on the commercial auto policy.

## Total premium for a typical 25-truck fleet (annual)

- Commercial Auto Liability: $25K-100K (size + risk dependent)
- Cargo: $5K-25K
- General Liability: $3K-10K
- Workers Comp: $30K-150K
- Physical Damage: $25K-60K
- **Total: $90K-350K/year**

Per-truck: $3,600-14,000/year depending on commodity, lanes, fleet age, claim history.

## How carriers reduce premiums

1. **Improve CSA scores** — insurance companies use BSI as a primary risk signal
2. **Continuous monitoring** — SambaSafety or similar gives proof of risk management
3. **Telematics + ELD adoption** — captures hard-events + speeding
4. **Driver age + tenure** — younger drivers cost more; longer tenure = lower premiums
5. **Safety training + scorecards** — formal program documentation
6. **Claim history** — clean 3+ years = significant discount
7. **Higher deductibles** — reduces premium; increases per-claim cost
8. **Multi-line bundling** — buying all from same carrier

## Reading a Certificate of Insurance (COI)

A COI has:
- Producer (broker) name + contact
- Insured (the carrier)
- Insurers (one or multiple)
- Coverage breakdown:
  - General Liability ($X general aggregate, $Y each occurrence)
  - Auto Liability ($X each accident)
  - Workers Comp + Employers Liability
- Endorsements (e.g., "Additional Insured: ABC Shipping Company")
- Cancellation language

Customers + brokers commonly request:
- "Additional Insured" endorsement (the shipper named on the policy)
- "Primary + Non-Contributory" language (your insurance is primary)
- "Waiver of Subrogation" (you waive right to sue the shipper)

These add cost to your premiums.

## Common insurance mistakes

1. **Operating with a lapsed BMC-91 filing.** Authority auto-suspended after 30 days; can't recover quickly.
2. **Underinsured for the actual operation.** Hauling hazmat with $1M when you should have $5M = federal violation.
3. **No cargo coverage on high-value goods.** A single $200K cargo loss without coverage = company-ending.
4. **Bobtail insurance for company drivers but not owner-operators.** Each owner-operator needs their own NTL.
5. **Missing waiver of subrogation when contractually required.** Shipper has the right to demand you pay back losses they paid.

## Where this fits in X3

X3's `settings.html` tracks insurance certificate uploads + renewal dates. Insurance brokers + underwriters sometimes use X3's compliance score as a risk signal when quoting carriers — clean compliance + telematics + low claim history = lower premium.

When advising customers on insurance, recommend they get 3+ quotes annually and work with a broker who specializes in trucking (not general business insurance).


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=trucking-insurance-101

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

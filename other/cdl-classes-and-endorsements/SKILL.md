---
name: cdl-classes-and-endorsements
description: |
  Use this skill when the user asks about CDL classes (A, B, C), endorsements (H, N, P, S, T, X), required for hazmat / passenger / school bus / tank / triple-trailer operations, what each class is permitted to operate, the TSA Security Threat Assessment for hazmat, and ELDT (Entry-Level Driver Training) requirements. Cite 49 CFR 383.
---

# CDL Classes + Endorsements — 49 CFR 383

A Commercial Driver License (CDL) is a federal-licensed credential to operate Commercial Motor Vehicles. The class + endorsements determine what the driver can legally operate.

## CDL Classes (49 CFR 383.91)

### Class A
Combination vehicle with a **Gross Combination Weight Rating (GCWR) ≥ 26,001 lb**, provided the GVWR of the trailer being towed is more than 10,000 lb.

What it covers:
- Tractor-trailer (semi truck pulling a 53' trailer)
- Truck-and-tow with a heavy trailer
- Any heavier combination

### Class B
Single vehicle with a GVWR ≥ 26,001 lb, OR combination where the trailer GVWR is ≤ 10,000 lb.

What it covers:
- Straight trucks (single chassis)
- Bus (school bus, motorcoach)
- Dump truck
- Box truck

### Class C
Vehicle that doesn't meet A or B criteria, BUT is either:
- Designed to transport 16+ passengers (incl. driver), OR
- Used to transport hazardous materials in placardable quantities

Required for: small buses, passenger vans (16+ seats), hazmat trucks under 26,001 lb.

A Class C driver hauling hazmat in a 1-ton pickup needs Class C + H endorsement.

## Endorsements (49 CFR 383.93)

| Endorsement | What it allows | Additional test/requirement |
|---|---|---|
| **H** | Transport of hazardous materials (HM placardable) | Hazmat written test + **TSA Security Threat Assessment** |
| **N** | Tank vehicle (vehicles designed to transport liquids/gases in tanks) | Tank vehicle written test |
| **P** | Passenger (16+ passenger vehicles) | Passenger written test |
| **S** | School bus (specifically) | School bus written test + S endorsement requires P endorsement first |
| **T** | Double / Triple trailer | Doubles/Triples written test |
| **X** | Combination of H + N (hazmat + tank) | Both H + N requirements |

A driver hauling fuel in a tanker needs Class A + N + H = "X" endorsement (combined).

## TSA Security Threat Assessment for H endorsement

For the H (hazmat) endorsement, the driver must pass a TSA background check covering:
- Criminal history (last 7 years)
- Immigration status
- Connection to terrorist organizations
- Mental capacity

Cost: ~$95 + state fees. Renewed every 5 years (same as the CDL endorsement).

## ELDT — Entry-Level Driver Training (49 CFR 380)

Effective Feb 7, 2022, anyone obtaining a new CDL OR an additional endorsement OR upgrading class must complete:

- **Theory training** (online or in-classroom) — minimum hours specified
- **Behind-the-wheel (BTW) training** — minimum hours specified
- **Provider must be on the Training Provider Registry (TPR)** at fmcsa.dot.gov

Training records (TPR certification) must be kept in the DQF.

ELDT applies to:
- First-time Class A or Class B CDL applicants
- Class A CDL upgrade from Class B
- H, P, S endorsement additions (separate ELDT per endorsement)

Pre-Feb 2022 CDL holders are NOT required to complete ELDT for their existing CDL.

## CDL holder restrictions (49 CFR 383.73)

Restrictions appear on the CDL itself:

| Restriction Code | What it means |
|---|---|
| L | No air brakes (driver hasn't taken air brake test) |
| E | No manual transmission (auto only) |
| M | No Class A passenger vehicles |
| N | No Class A and B passenger vehicles |
| O | No tractor-trailer (5th wheel) |
| Z | No full air brakes |
| K | Intrastate only |
| V | Medical variance / exemption |

These are SEPARATE from medical cert restrictions but often overlap.

## Age requirements (49 CFR 383.3)

- **18 years old** — minimum for intrastate Class A or B CDL (some states are 21)
- **21 years old** — minimum for interstate Class A, B, or C CDL
- **21 years old** — minimum for hazmat endorsement
- **21 years old** — minimum for passenger / school bus endorsement (with state variation)

## Common mistakes

1. **Driver upgrade from Class B to Class A without ELDT** — required by Feb 2022 rule.
2. **Hazmat endorsement expired due to lapsed TSA STA** — renewed every 5 years; easy to miss.
3. **S endorsement without P endorsement** — invalid; S requires P first.
4. **CDL class doesn't match vehicle operated** — Class B driver operating a tractor-trailer = violation.
5. **Restriction E violated** — Class A driver with E restriction (no manual) operating a manual transmission CMV.

## Where this fits in X3

X3's `dq-files.html` tracks CDL class + endorsements + restrictions per driver. Dispatchers see this when assigning vehicles. The hazmat-basics skill cross-references the H endorsement requirements; the medical-certification skill cross-references the V restriction (medical variance).


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=cdl-classes-and-endorsements

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

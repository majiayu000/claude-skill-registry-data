---
name: hazmat-basics
description: |
  Use this skill when the user asks about hazardous materials (hazmat) transportation under 49 CFR 171-180 — placarding requirements, segregation tables, hazmat employee training (49 CFR 172 Subpart H), Hazmat Safety Permit (HMSP), shipping papers, packaging groups, emergency response phone, security plans, hazmat endorsement on CDL, and bulk vs non-bulk distinctions. Cite specific 49 CFR section.
---

# Hazmat Basics — 49 CFR 171-180

Anyone offering, transporting, packaging, manufacturing, or distributing hazardous materials in commerce must follow the Hazardous Materials Regulations (HMR). For motor carriers, this primarily means 49 CFR 171-180.

## Hazard classes (49 CFR 173)

There are 9 hazard classes:

1. **Explosives** (Div 1.1 - 1.6)
2. **Gases** (compressed, liquefied, dissolved) — Div 2.1 (flammable), 2.2 (non-flammable), 2.3 (toxic)
3. **Flammable liquids**
4. **Flammable solids; substances liable to spontaneous combustion; substances that emit flammable gas on contact with water**
5. **Oxidizing substances; organic peroxides**
6. **Toxic substances; infectious substances**
7. **Radioactive material**
8. **Corrosive substances**
9. **Miscellaneous dangerous goods** (e.g., dry ice, asbestos, lithium batteries)

## Packing groups (within a class)

- **PG I** — high danger
- **PG II** — medium danger
- **PG III** — low danger

PG affects packaging requirements + shipping paper entries.

## Placarding (49 CFR 172 Subpart F)

A vehicle requires placards if:

- It transports **any quantity** of a Table 1 material (explosives 1.1-1.3, poison gas 2.3, dangerous when wet 4.3, radioactive 7), OR
- It transports **1,001+ lb aggregate weight** of any Table 2 hazmat (most other classes)

Bulk packagings (> 119 gallons / 882 lb) always require placards regardless of quantity.

Placards must be:
- Diamond shape, color-coded by class
- 10.75" minimum on each side
- Displayed on all 4 sides of the vehicle

## Hazmat shipping papers (49 CFR 172.200-205)

The driver must carry shipping papers describing each hazardous material in the load. Required entries:

1. UN/NA identification number (e.g., UN1203 for gasoline)
2. Proper shipping name (e.g., "Gasoline")
3. Hazard class or division (e.g., "Class 3")
4. Packing group (e.g., "II")
5. Total quantity by weight or volume
6. Number of packages and type
7. Emergency response phone number (24/7 accessible)

Special requirements:
- Shipping paper must be visible to driver
- Must include certification of accuracy
- If the shipment is hazardous waste, an EPA Manifest replaces standard shipping paper

## Hazmat employee training (49 CFR 172 Subpart H)

Every "hazmat employee" (anyone who handles, packages, prepares, or transports hazmat) must:

- Be trained within 90 days of starting hazmat duties (may work unsupervised before training only if directly supervised)
- Receive **recurrent training every 3 years**
- Have training records maintained for current employment + 90 days after

Training must cover:
- **General awareness** (recognizing hazmat, understanding HMR)
- **Function-specific** (their specific job duties)
- **Safety** (emergency response procedures)
- **Security awareness** (security risks, threats)
- **In-depth security training** (if applicable; for those involved in security plan)

## Hazmat Safety Permit (HMSP) — 49 CFR 385 Subpart E

Required for carriers transporting specific high-hazard quantities:

- ≥ 3,500 gal of certain Class 2 gases (e.g., LPG)
- ≥ 1,000 cal of explosives Division 1.1, 1.2, or 1.3
- ≥ 1 lb of radioactive Class 7 in highway route-controlled quantities
- Materials toxic by inhalation in specific quantities

HMSP requires:
- Satisfactory CSA scores in HM Compliance + Crash Indicator BASICs
- Insurance ≥ $5M (for some materials)
- Security plan if applicable
- Renewed every 2 years

Apply via FMCSA Portal.

## Hazmat CDL endorsement

A driver transporting placardable quantities of hazmat needs a **CDL H endorsement**:

- Background check via TSA Security Threat Assessment (STA)
- Hazmat written exam
- Renewed every 5 years (TSA STA every 5 years too)

## Security plan (49 CFR 172.802)

Required if transporting:

- Highway-route-controlled quantities of radioactive materials
- Hazmat in bulk packaging
- Highly hazardous materials in specific quantities (see 49 CFR 172.800 list)

Security plan must address:
- Personnel security (background checks)
- Unauthorized access prevention
- En route security
- Risk assessment

Plan must be retained for **as long as in effect plus 90 days**.

## Emergency response phone (49 CFR 172.604)

Shipping papers must include a 24/7-monitored emergency response phone number that's:
- Answered by a person knowledgeable about the hazmat
- Or by an emergency response information service (CHEMTREC at 800-424-9300 is the most common)

CHEMTREC charges per registration; cost varies.

## Common hazmat mistakes

1. **Driver carrying hazmat without HM endorsement.** Class A felony in some states.
2. **Wrong placards or missing placards.** OOS at roadside.
3. **Shipping papers not visible to driver.** Violation.
4. **Training records missing or expired** (the 3-year recurrent).
5. **Security plan required but not in place.**
6. **Emergency phone number doesn't answer or has wrong contract status.**
7. **Hazmat training records destroyed after 90 days post-termination** (should be retained per separate retention rules).

## Quick reference: shipping paper format

```
UN1203, Gasoline, 3, PG II, 1500 gal, 5 drums, CHEMTREC 800-424-9300
[UN#]   [Name]    [Class] [PG]  [Qty]    [Packaging] [Emergency contact]
```

## Where this fits in X3

X3's `forms.html` includes a hazmat shipping paper template and security plan template. Driver hazmat endorsement tracking lives in `dq-files.html`. Training records (49 CFR 172 Subpart H) feed into the training module on `training.html`.

If the user has a complex hazmat question (specific UN number lookup, segregation conflict, special permits), recommend the FMCSA Hazmat Hotline at 1-800-467-4922 or the PHMSA at phmsa.dot.gov.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=hazmat-basics

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

---
name: insurance-advisor
description: "Assembles a project insurance program recommendation: which policy types the project needs, what each one covers, the wrap-up against traditional structure decision, and a checklist to take to a broker. Trigger on \"insurance program\", \"what limits should we carry\", \"wrap-up insurance\", \"builder's risk\", \"professional liability limits\", \"insurance review\", or a pasted project profile with a coverage question. Works in any market. Limits, required coverages, and certificate formats come from the user's contract and their broker; the skill supplies the structure of the decision and never a limit figure or a required coverage from memory. Produces a recommendation memo and a broker request checklist, and is not broker advice, a quote, or a binder."
license: MIT
metadata:
  title: "Insurance Advisor"
  summary: "Recommend policy types, limits, and a wrap-up structure"
  discipline: "practice-contracts"
  tags: "Project Management, AIA A201, AIA B101, Construction, Construction Admin"
---

## Overview


Recommend a project insurance program for an AEC project: required policy types, recommended limits, and the OCIP / CCIP / traditional structure decision. Output is a recommendation memo in `docs/insurance/` and a broker RFP checklist that the owner / owner's-rep takes to a licensed insurance broker for actual market quote and binding.


This skill is for the owner / owner's-rep / architect perspective. It is **not** broker advice — it does not bind policies, quote premiums, or substitute for a licensed broker's market analysis. The output names what to ask for; the broker delivers what the market provides.


Aligned with AIA A201-2017 Article 11 (Insurance and Bonds), AIA A201-2017 Exhibit A (Insurance and Bonds — separate document since 2017), AIA B101-2017 §2.5 (Architect's insurance), AIA A101 / A102 / A103-2017 owner-contractor forms, AIA A312-2010 Performance and Payment Bond, and IRMI Construction Risk Management.


## Scope and limits — read first


**What this does.** Assembles the shape of a project's insurance program: which
policy types apply, who carries each one, which endorsements travel with them,
and whether a wrap-up beats traditional placement. Writes a recommendation memo
and a broker request checklist to `docs/insurance/`.

**What this does not do.**

- **It does not supply a required limit.** Limits, required coverages, and
  certificate formats come from the contract in force and from your broker. The
  tiers in `references/policy_types_reference.md` are heuristics for framing the
  conversation, not published requirements, and a blank limit field in a
  contract exhibit stays blank rather than being filled with a customary figure.
  A filled-in blank becomes the number somebody is told to buy.
- **It does not recall your contract's insurance articles.** Paste them or name
  the file. Anything outside the supplied text is recorded as not found rather
  than described from what the form usually says.
- It does not quote a premium, bind coverage, or issue a certificate. Those
  belong to a licensed broker, and the memo exists to brief one.
- It does not know your state's Workers' Compensation, auto, or licensing rules.
  They are state by state; the broker or the state insurance department confirms
  them.
- It does not adjust claims, and it does not size performance or payment bonds.
  Those are an adjuster and a surety.

**What you need before starting.** Project value, type, jurisdiction, delivery
method, and owner type; the insurance and bonds articles of the contract in
force, pasted or as a file to read; and the site profile, since environmental
and coastal exposure change which policies apply.

## When to use


Trigger on:

- Pasted project profile (value, type, jurisdiction, delivery method, owner type) with insurance question.
- Explicit asks: "insurance advice", "insurance program", "what limits", "OCIP or CCIP", "wrap-up insurance", "builder's risk", "PL limits for architect", "Article 11 review".
- Hand-off from `contract-advisor` when the executed contract requires the Article 11 / Exhibit A insurance schedule.
- Hand-off from `bid-review` when bidder qualifications include insurance proposals or bond-substitute structures.

Do NOT trigger for:

- Quoting actual premiums (broker only — this skill names the limits to request, not the price).
- Binding insurance policies (broker only).
- Claim adjustment after a loss (broker / adjuster / insurance counsel).
- State-specific insurance department compliance (insurance counsel).
- Performance / payment bond adequacy (use `bond-advisor` when it exists; for now, flag and refer to broker / surety).

## Workflow


### Step 1 — Bootstrap if needed


Check that `docs/insurance/index.md` exists. If not:


```bash
python scripts/init_insurance_workspace.py
```


### Step 2 — Anchor the project context


Read `docs/project.md` if it exists. Pull:

- **Project value** (drives limit recommendations; small / mid / large / mega tiers per `references/policy_types_reference.md`).
- **Project type** (commercial / multifamily / institutional / healthcare / industrial / heavy civil — affects policy types required, especially Pollution and Builder's Risk).
- **Jurisdiction** (state-by-state Workers' Comp + auto + contractor licensing rules; NY, CA, FL each have specific requirements).
- **Delivery method** (DBB / DB / CMAR / IPD — drives who carries Builder's Risk and whether wrap-up makes sense — see `references/delivery_method_insurance_matrix.md`).
- **Owner type** (institutional / commercial / public / federal / non-profit — affects PI requirements; federal projects have FAR-flowed clauses).
- **Project schedule / duration** (Builder's Risk + extensions; long projects need extension provisions).
- **Site profile** (existing building present? environmental concerns? coastal / wildfire / seismic exposure?).

### Step 3 — Map required policy matrix


Use `references/policy_types_reference.md`. For each of the standard policy categories, determine:

1. **Who must carry it** (owner / GC / sub / architect / EOR).
2. **Recommended limits** (per the project tier in the reference).
3. **Required endorsements** (additional insured for owner + architect, waiver of subrogation, primary & non-contributory).
4. **Notice requirements** (notice of cancellation, notice of material change).

Standard categories:

- Professional Liability (PL / E&O) — architects, engineers, design-builders.
- Commercial General Liability (CGL) — owner, contractor, subs.
- Builder's Risk — physical loss to construction; carried per delivery method.
- Workers' Compensation + Employer's Liability — statutory; varies by state.
- Auto Liability — owned / hired / non-owned.
- Umbrella / Excess Liability — over CGL, auto, sometimes EL.
- Pollution Legal Liability (PLL) — site-specific environmental risk.
- Contractor's Pollution Liability (CPL) — contractor's environmental impairment.
- Cyber Liability — for projects with data systems / OT / BAS exposure.

### Step 4 — Apply the OCIP / CCIP / traditional decision


Use `references/ocip_ccip_decision.md`. The decision rests on:

- **Project size** — generally OCIP / CCIP makes sense above $25M total construction value; below that, administrative cost outweighs premium savings.
- **Single-site vs. rolling** — single-site favors wrap-up; multi-site portfolio does not.
- **Owner sophistication** — wrap-up requires owner staffing or a wrap administrator.
- **State enforcement** — some states (NY, CA) have specific wrap-up rules.
- **Subcontractor mix** — small-sub-heavy projects benefit more (wrap pulls coverage costs out of every sub bid).

Recommend OCIP (owner-controlled), CCIP (contractor-controlled), or traditional.


### Step 5 — Cross-reference the contract's insurance articles

Ask for the insurance and bonds articles of the contract in force, pasted or as
a file to read. Work only from that text.

Read them and report, clause by clause:

- Which parties each required coverage falls on.
- Which coverages the contract names, and which of the ones in Step 3 it does
  not name.
- Where the limits are set, and whether every limit field has actually been
  filled in. A blank limit field in a schedule or exhibit is the most common
  defect here and it survives review because the article around it reads
  complete.
- Additional insured requirements, waivers of subrogation, and deductible
  allocation, as written.
- Whether bonds are required, and under which clause.

Mark each line `in the contract` with its clause, or `not in supplied text`.
Never state what a form usually requires, and never fill a blank limit with a
customary figure: that figure would become the number the owner is told to buy.

### Step 6 — Write the recommendation memo + broker RFP checklist


Use `assets/insurance_memo_template.md` for the recommendation memo. The memo includes:

- **Header** — project, phase, date, prepared by.
- **Required policy matrix** — table with policy type, who carries, recommended limit, required endorsements.
- **OCIP / CCIP / traditional recommendation** — with reasoning.
- **Article 11 / Exhibit A status** — what is in the contract today, what needs to be added.
- **Broker RFP checklist** (use `assets/broker_rfp_checklist.md`) — what to send to the licensed broker for market quote.
- **Disclaimers** — not broker advice, not bound coverage, not insurance counsel.

Write the memo to `docs/insurance/<project-slug>-<YYYY-MM-DD>.md` and append a row to `docs/insurance/index.md`.


### Step 7 — Hand off


The memo is a recommendation, not a bound policy. Hand off to:

- **Licensed insurance broker** — for market quote and binding. Provide the broker RFP checklist.
- **Owner's procurement / legal** — for confirming contract Article 11 + Exhibit A complete.
- **Contractor / sub procurement** — for flow-down requirements to subcontractors.
- `contract-advisor` — if Article 11 needs amendment beyond the standard fill-in fields.

## Anti-patterns

- **Never quote premium dollars.** This skill names limits to request — the broker quotes the premium.
- **Never bind coverage or commit on behalf of any party.** Output is a recommendation only.
- **Never recall a contract's insurance articles or its limit fill-ins from memory.** Standard forms restructure their insurance provisions between editions, and the limits are project-specific fields somebody had to complete. Quote from the text supplied, or record the line as not found.
- **Never recall state Workers' Comp / Auto requirements from memory.** State-by-state. Direct the user to verify with the broker or state insurance department.
- **Never recommend dropping a coverage that the executed contract requires.** Flag the conflict; let owner + counsel resolve.
- **Never present this skill's tier-based limit recommendations as published industry standards.** Limits are heuristics drawn from IRMI Construction Risk Management practice and common owner-side requirements; the broker's market analysis governs.

## Resources

- `scripts/init_insurance_workspace.py` — bootstrap `docs/insurance/` and `index.md`.
- `references/policy_types_reference.md` — standard policy categories with what they cover and recommended limit tiers by project value.
- `references/delivery_method_insurance_matrix.md` — DBB / DB / CMAR / IPD insurance allocation matrix.
- `references/ocip_ccip_decision.md` — wrap-up program decision criteria.
- `assets/insurance_memo_template.md` — recommendation memo template.
- `assets/broker_rfp_checklist.md` — broker RFP checklist template.

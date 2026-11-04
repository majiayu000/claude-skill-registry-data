---
name: space-signpost
kind: signpost
description: "Signpost (not a knowledge pack) for the ECSS European space standards: the E-ST-10 system engineering family, the discipline standards a reader commonly mis-cites (radiation is E-ST-10-12, not a RAM standard; software is E-ST-40, not E-ST-70), the M-branch project management standards, the Q-branch product assurance standards, and the sustainability and system documents, with designation, edition, owner, status, and catalogue URL only. Contains no source content. Free process paths are existing NASA packs in this catalogue, named by slug, and are not ECSS clause substitutes. Several needs have no in-repo pack."
---

<!-- argument-hint: [standard designation or topic, e.g. ECSS-E-ST-10 / ECSS-E-ST-40 / ECSS-Q-ST-30 / ECSS-M-ST-80 / ECSS-E-ST-32 / ECSS-E-ST-50] -->

# ECSS Space Standards: Signpost (pointers only)

**This is a signpost, not a knowledge pack.** It carries **no standards-body content**:
no reproduced clauses, no normative text, no synthesised summaries of the standards.
ECSS documents are free to download after registration on ecss.nl, and ESA holds the
copyright with no redistribution grant (ECSS-P-00C clause 5.8), so they are Excluded
under this repo's `docs/SOURCE-VETTING.md` and cannot be reconstituted into a
redistributable pack. What this skill does: tell you which document you want, which
edition is current, who owns it, and which existing NASA pack covers the process
topic. A NASA pack is not the ECSS clause set.

## When to use

You are working on a European space programme and need to identify or cite the
governing ECSS document: which standard covers system engineering, which covers
software, which covers dependability, and which free NASA pack covers the process
topic. ECSS rows route you to the catalogue. NASA rows route you to an in-repo pack.
Several needs have no in-repo pack, and those rows send you to the catalogue only.

**Prerequisites:** none, plain Markdown.

## How to use

Find your document below. The **Status** column says whether it can be packaged:

- **Excluded**: free personal download after registration on ecss.nl; ESA copyright; no redistribution grant. Cannot be packaged here. Buy or download from the owner after registering.
- **Open**: an in-repo NASA pack covers the process topic. The Designation cell names the slug, and the Status cell reads `Open`. The pack is US Government work, public domain in the US (17 U.S.C. § 105). It is not the ECSS clause set.

Editions were confirmed on ecss.nl product pages on 2026-10-14. E-ST-10-12C is
radiation methods, not RAM. E-ST-40C Rev.1 is software. E-ST-70C is ground systems
and operations. Do not quote a date this file does not print. Where a public URL
slug disagrees with the page title, the Title cell says so and the URL is copied as
fetched. A reader who needs a designation not listed here goes to
https://ecss.nl/standards/active-standards/ .

## System engineering (E-ST-10 family)

| Designation | Title | Edition | Owner | Status | URL |
|-------------|-------|---------|-------|--------|-----|
| ECSS-E-ST-10C Rev.1 | System engineering general requirements. Free process ground: `nasa-se-handbook`, `nasa-npr-7123`, depth `nasa-se-expanded`. NASA SE Engine and life cycle, not the ECSS clause set. | Rev.1, 15 February 2017 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-10c-rev-1-system-engineering-general-requirements-15-february-2017/ |
| ECSS-E-ST-10-02C Rev.1 | Verification. Free process ground: `nasa-se-handbook`, `nasa-npr-7123`. No ECSS verification programme DRDs, and NASA does not publish this as a standalone verification standard. | Rev.1, 1 February 2018 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-10-02c-rev-1-verification-1-february-2018/ |
| ECSS-E-ST-10-06C | Technical requirements specification. Free process ground: `nasa-se-handbook` and `requirements-writing`. Not an ECSS-format technical specification standard. | Issue C, 6 March 2009 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-10-06c-technical-requirements-specification/ |
| ECSS-E-ST-10-24C Rev.1 | Interface management. Free process ground: `nasa-se-handbook`, handbook-level, not an ECSS interface control standard. | Rev.1, 15 November 2024 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-10-24c-rev-1-interface-management-15-november-2024/ |
| ECSS-E-ST-10-04C Rev.1 | Space environment. No in-repo pack. Catalogue URL only. | Rev.1, 15 June 2020 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-10-04c-rev-1-space-environment-15-june-2020/ |
| ECSS-E-ST-10-12C | Methods for the calculation of radiation received and its effects, and a policy for design margins. Not a RAM methods standard. RAM is Q-ST-30. No in-repo pack. | Issue C, 15 November 2008; Corr.1 22 February 2017 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-10-12c-methods-for-the-calculation-of-radiation-received-and-its-effects-and-a-policy-for-design-margins/ |

## Discipline engineering, not the RAM standard and not the software standard

These five are the designations a reader commonly mis-cites. E-ST-10-12 in the table above is radiation methods, not RAM. E-ST-70C in this table is ground systems and operations, not the software standard. The software standard is E-ST-40C Rev.1, last row.

| Designation | Title | Edition | Owner | Status | URL |
|-------------|-------|---------|-------|--------|-----|
| ECSS-E-ST-32C Rev.1 | Structural general requirements. No structures pack. Catalogue URL only. | Rev.1, 15 November 2008 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-32c-rev-1-structural-general-requirements/ |
| ECSS-E-ST-33-01C Rev.2 | Mechanisms. No mechanisms pack. Catalogue URL only. | Rev.2, 1 March 2019 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-33-01c-rev-2-1-march-2019-space-engineering-mechanisms/ |
| ECSS-E-ST-50C Rev.2 | Communications. No RF, telemetry, or telecommand pack. The public URL slug still says `rev-1`. The page title is Rev.2. Copy the slug as fetched. | Rev.2, 5 December 2024 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-50c-rev-1-communications-5-december-2024/ |
| ECSS-E-ST-70C | Ground systems and operations. Not the software standard. No ground-segment pack. Catalogue URL only. | Issue C, 31 July 2008 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-70c-ground-systems-and-operations/ |
| ECSS-E-ST-40C Rev.1 | Software. This is the software standard. Free process ground: `nasa-npr-7150` (NASA software engineering requirements, Classes A-F). Not the ECSS-E-ST-40 process text. Software product assurance is Q-ST-80, in the product assurance table. | Rev.1, 30 April 2025 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-40c-rev-1-software-30-april-2025/ |

## Project management (M branch)

The active management branch is exactly these five documents. M-ST-80C cancels the earlier M-00-03 lineage; that lineage is not a current designation and has no row here.

| Designation | Title | Edition | Owner | Status | URL |
|-------------|-------|---------|-------|--------|-----|
| ECSS-M-ST-10C Rev.1 | Project planning and implementation. Free process ground: `nasa-se-handbook`, `nasa-npr-7123`. NASA phase labels differ from ECSS project phases. | Rev.1, 6 March 2009 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-m-st-10c-rev-1-project-planning-and-implementation/ |
| ECSS-M-ST-10-01C | Organization and conduct of reviews. No product-page URL was verified. The URL is the management filter. Free process ground: `nasa-se-handbook`, `nasa-npr-7123`. Review names are NASA-specific. | Issue C, 15 November 2008 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standards/active-standards/management/ |
| ECSS-M-ST-40C Rev.1 | Configuration and information management. Free process ground: `nasa-se-handbook`, crosscutting CM, not an EIA-649-depth standard. No standalone NASA CM pack slug. | Rev.1, 6 March 2009 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-m-st-40c-rev-1-configuration-and-information-management/ |
| ECSS-M-ST-60C | Cost and schedule management. Free process ground splits: `nasa-ceh` for cost estimating, `nasa-schedule` for schedule. Neither is the ECSS cost and schedule standard. | Issue C, 31 July 2008 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-m-st-60c-cost-and-schedule-management/ |
| ECSS-M-ST-80C | Risk management. Cancels the earlier M-00-03 lineage. Free process ground: `nasa-risk`. NASA risk taxonomy, not the ECSS clause text. | Issue C, 31 July 2008 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-m-st-80c-risk-management/ |

## Product assurance (Q branch)

Dependability is Q-ST-30C Rev.1, not E-ST-10-12C. E-ST-10-12C is radiation methods.

| Designation | Title | Edition | Owner | Status | URL |
|-------------|-------|---------|-------|--------|-----|
| ECSS-Q-ST-10C Rev.1 | Product assurance management. No NASA product assurance management pack. Nearest culture pointer is `nasa-system-safety`, and it is not a PA programme equivalent. | Rev.1, 15 March 2016 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-q-st-10c-rev-1-product-assurance-management-15-march-2016/ |
| ECSS-Q-ST-20C Rev.2 | Quality assurance. No QA pack. Catalogue URL only. | Rev.2, 1 February 2018 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-q-st-20c-rev-2-quality-assurance-1-february-2018/ |
| ECSS-Q-ST-30C Rev.1 | Dependability. This is the RAM methods parent. Not E-ST-10-12. Free process ground: `nasa-rm-standard`, `nasa-pra`, `nasa-fault-management`. Not the ECSS Q-30 programme clauses. | Rev.1, 15 February 2017 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-q-st-30c-rev-1-space-product-assurance-dependability-15-february-2017/ |
| ECSS-Q-ST-30-02C | Failure modes, effects (and criticality) analysis (FMEA/FMECA). Free process ground: `nasa-pra`, `nasa-fault-management`, `nasa-rm-standard`. No dedicated FMEA handbook pack. | Issue C, 6 March 2009 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-q-st-30-02c-failure-modes-effects-and-criticality-analysis-fmeafmeca/ |
| ECSS-Q-ST-40C Rev.1 | Safety. Free process ground: `nasa-system-safety`. NASA system safety handbook framing, not the ECSS safety programme standard. | Rev.1, 15 February 2017 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-q-st-40c-rev-1-safety-15-february-2017/ |
| ECSS-Q-ST-80C Rev.2 | Software product assurance. Partial pointer only: `nasa-npr-7150` is engineering requirements, not a software product assurance standard. | Rev.2, 30 April 2025 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-q-st-80c-rev-2-software-product-assurance-30-april-2025/ |

## Sustainability, system description, and two optional rows

Four required rows, then two optional rows. Both optional rows ship, because a reader who asks for human factors or integrated product support will otherwise get silence.

| Designation | Title | Edition | Owner | Status | URL |
|-------------|-------|---------|-------|--------|-----|
| ECSS-U-AS-10C Rev.2 | Adoption notice of ISO 24113, space debris mitigation requirements. Listed on the sustainability filter. No verified product-page URL, so the URL is the filter. Free process ground: `nasa-std-8719-14`. That pack is NASA orbital debris process limits, not ISO 24113 text and not this adoption notice. | Rev.2, 9 February 2024 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standards/active-standards/sustainability/ |
| ECSS-U-ST-20C | Planetary protection. No planetary protection pack. Catalogue URL only. | Issue C, 1 August 2019 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-u-st-20c-space-sustainability-planetary-protection/ |
| ECSS-S-ST-00C Rev.2 | Description, implementation and general requirements. System document, not a discipline standard. No NASA equivalent. Catalogue URL only. | Rev.2, 21 November 2025 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-s-st-00c-rev-2-description-implementation-and-general-requirements-21-november-2025/ |
| ECSS-P-00C Rev.1 | Standardization objectives, policies and organization. Policy source for the copyright clause (clause 5.8). Listed on the system-implementation filter. No verified product-page URL, so the URL is the filter. No NASA equivalent. | Rev.1, 15 November 2024 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standards/active-standards/ecss-system-implementation/ |
| ECSS-E-ST-10-11C | Human factors engineering. Edition date was not opened. The URL is the engineering filter, not an invented product page. Free process ground: `nasa-hsi`. NASA HSI process, not the ECSS human factors standard. | listed active; product page not opened 2026-10-14 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standards/active-standards/engineering/ |
| ECSS-I-ST-30-10C | Integrated Product Support (IPS). The public URL slug is mis-prefixed `ecss-e-`. The designation on the page is I-ST. Copy the slug as fetched. No IPS pack. I-branch (industrialization) was announced 20 March 2025. | Issue C, 15 November 2024 | ECSS (catalogue: ecss.nl) | Excluded | https://ecss.nl/standard/ecss-e-st-30-10c-15-november-2024-integrated-product-support-ips/ |

## Free NASA paths

Every row names one real in-repo slug. Every Status cell reads `Open`. No ECSS row in this table. Edition cells say `(pack pin)` where this signpost does not itself pin the NASA document revision.

| Designation | Title | Edition | Owner | Status | URL |
|-------------|-------|---------|-------|--------|-----|
| nasa-se-handbook | E-ST-10, E-ST-10-02, E-ST-10-06, E-ST-10-24, M-ST-10, M-ST-10-01, M-ST-40. NASA SE process model, not ECSS clauses. | NASA/SP-2016-6105 Rev 2 | NASA | Open | packs/nasa-se-handbook/ |
| nasa-npr-7123 | Same SE and project-planning needs, as the requirements NPR. Not ECSS. | NPR 7123.1 (pack pin) | NASA | Open | packs/nasa-npr-7123/ |
| nasa-se-expanded | Depth layer for E-ST-10 only. Pair with the handbook. Not ECSS. | NASA/SP-2016-6105-SUPPL Vol 1 | NASA | Open | packs/nasa-se-expanded/ |
| nasa-risk | M-ST-80. Not the ECSS risk clause text. | NASA risk management handbook (pack pin) | NASA | Open | packs/nasa-risk/ |
| nasa-rm-standard | Q-ST-30 and Q-ST-30-02. Not ECSS Q-30 programme clauses. Not a dedicated FMEA standard. | NASA-STD-8729.1 | NASA | Open | packs/nasa-rm-standard/ |
| nasa-pra | Q-ST-30 and Q-ST-30-02. Not ECSS Q-30 programme clauses. Not a dedicated FMEA standard. | NASA PRA procedures guide (pack pin) | NASA | Open | packs/nasa-pra/ |
| nasa-fault-management | Q-ST-30 and Q-ST-30-02. Not ECSS Q-30 programme clauses. Not a dedicated FMEA standard. | NASA fault management handbook (pack pin) | NASA | Open | packs/nasa-fault-management/ |
| nasa-system-safety | Q-ST-40. Also the nearest culture pointer for Q-ST-10, and not a PA programme equivalent. | NASA system safety handbook (pack pin) | NASA | Open | packs/nasa-system-safety/ |
| nasa-npr-7150 | E-ST-40 engineering requirements. Partial only for Q-ST-80. Not a software product assurance standard. | NPR 7150.2 (pack pin) | NASA | Open | packs/nasa-npr-7150/ |
| nasa-ceh | Cost half of M-ST-60. Not the ECSS cost and schedule standard. No separate cost-estimating pack exists in this catalogue. | NASA cost estimating handbook (pack pin) | NASA | Open | packs/nasa-ceh/ |
| nasa-schedule | Schedule half of M-ST-60. Not the ECSS cost and schedule standard. | NASA schedule management handbook (pack pin) | NASA | Open | packs/nasa-schedule/ |
| nasa-std-8719-14 | Debris analogue for U-AS-10. Not ISO 24113. | NASA-STD-8719.14 (pack pin) | NASA | Open | packs/nasa-std-8719-14/ |
| nasa-hsi | E-ST-10-11 process ground. Not the ECSS human factors standard. | NASA HSI practitioner guide (pack pin) | NASA | Open | packs/nasa-hsi/ |

## Scope & Limits

- No reproduced standards text. Rows carry designation, title, edition, owner, status, and URL only.
- ECSS rows are Excluded. Free after registration is not a redistribution grant.
- NASA rows are Open and name real in-repo slugs. They are process-topic analogues. They do not replace ECSS clause text, European customer-supplier DRDs, or contractual tailoring.
- E-ST-10-12C is radiation methods, not RAM. Dependability is Q-ST-30C Rev.1.
- E-ST-70C is ground systems and operations, not software. Software is E-ST-40C Rev.1.
- No in-repo pack covers structures, mechanisms, communications, ground systems and operations, space environment, radiation methods, planetary protection, product assurance management, or quality assurance.
- No dedicated cost-estimating pack exists in this catalogue beyond `nasa-ceh`. Schedule is `nasa-schedule`.
- The communications URL slug says `rev-1`. The page title is Rev.2. The IPS URL slug is mis-prefixed `ecss-e-`. Both URLs are copied as fetched.
- `se-standards-signpost` keeps a shorter ECSS list with no editions. This pack is the edition-pinned map. Do not treat the two lists as the same document.

---
*Signpost content is original JG Systems Consulting Ltd. work, MIT licensed. Trademarks and standard designations are named for identification only.*

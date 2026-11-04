---
name: avionics-signpost
kind: signpost
description: "Signpost (not a knowledge pack) for the avionics development assurance standards landscape: RTCA DO-178C / EUROCAE ED-12C and its supplements (DO-330/ED-215, DO-331/ED-218, DO-332/ED-217, DO-333/ED-216); RTCA DO-254 / EUROCAE ED-80; SAE ARP4754B and ARP4761A; and the free regulator documents that recognise them (FAA AC 20-115D, AC 20-152A, Order 8110.49A; EASA AMC 20-115D and AMC 20-152A). Contains no source content: each row carries only the designation, title, edition, owner, redistributability status, and the owner's URL. Use when you need to identify, cite, or locate an avionics standard; paywalled rows point to the owner, free rows point to the regulator text, and the FAA rows also name the in-repo faa-8110-49 pack."
---

<!-- argument-hint: [standard designation or topic, e.g. DO-178C / DO-254 / ARP4754B / ARP4761A / AC 20-115D / AC 20-152A / Order 8110.49A] -->

# Avionics Development Assurance Standards: Signpost (pointers only)

**This is a signpost, not a knowledge pack.** It carries **no standards-body content**:
no reproduced clauses, no normative text, no synthesised summaries of the standards.
DO-178C, DO-254, and the SAE ARPs are paywalled with no redistribution grant (Excluded
under this repo's `docs/SOURCE-VETTING.md`), so they cannot be reconstituted into a
redistributable pack. What this skill does: tell you which document you want, what it is
for, who owns it, whether a free copy exists, and where to get the authentic one.

## When to use

You are developing or reviewing avionics software or airborne electronic hardware and
need to identify or cite the governing document: which standard covers tool
qualification, which AC recognises DO-254, which EASA text accepts DO-178C. Paywalled
rows route you to the owner; free regulator rows route you to the authentic text or,
where this repo ships one, to the installable pack.

**Prerequisites:** none, plain Markdown.

## How to use

Find your document below. The **Status** column says whether it can be packaged:

- **Excluded**: paywalled, no redistribution grant; buy from the owner. *Cannot* be packaged here.
- **Open**: free to obtain; where this repo ships a pack for it, the row names it (`pack: faa-8110-49`).

Editions for the RTCA, EUROCAE, and FAA rows were confirmed from the FAA recognition
texts and the EASA Easy Access Rules page. The SAE rows state the edition letter only
because the SAE catalogue pages did not confirm a publication date; do not quote one
from here.

## Software (DO-178C family)

| Designation | Title | Edition | Owner | Status | URL |
|-------------|-------|---------|-------|--------|-----|
| DO-178C / ED-12C | Software Considerations in Airborne Systems and Equipment Certification. Core design assurance guidance for airborne software; the means of compliance most certification programmes are judged against. | DO-178C 2011-12-13; ED-12C January 2012 | RTCA; EUROCAE | Excluded: paywalled, no redistribution grant; buy from the owner | https://www.rtca.org/do-178/ |
| DO-330/ED-215, DO-331/ED-218, DO-332/ED-217, DO-333/ED-216 | The four DO-178C supplements named in AC 20-115D: tool qualification; model-based development and verification; object-oriented technology and related techniques; formal methods. | DO 2011-12-13; ED January 2012 | RTCA; EUROCAE | Excluded: paywalled, no redistribution grant; buy from the owner | https://www.rtca.org/do-178/ |

## Airborne electronic hardware

| Designation | Title | Edition | Owner | Status | URL |
|-------------|-------|---------|-------|--------|-----|
| DO-254 / ED-80 | Design Assurance Guidance for Airborne Electronic Hardware. Design assurance process for custom airborne electronic hardware; recognised by AC 20-152A and AMC 20-152A. | DO-254 2000-04-19; ED-80 April 2000 | RTCA; EUROCAE | Excluded: paywalled, no redistribution grant; buy from the owner | https://www.eurocae.net/ |

## Aircraft and system development and safety assessment

| Designation | Title | Edition | Owner | Status | URL |
|-------------|-------|---------|-------|--------|-----|
| ARP4754B | Guidelines for Development of Civil Aircraft and Systems. Aircraft- and system-level development and validation process within which the DO-178C and DO-254 assurance levels sit. | B (no confirmed date) | SAE International | Excluded: paywalled, no redistribution grant; buy from the owner | https://www.sae.org/standards/content/arp4754b/ |
| ARP4761A | Guidelines for Conducting the Safety Assessment Process on Civil Aircraft, Systems, and Equipment. Safety assessment companion to ARP4754B. | A (no confirmed date) | SAE International | Excluded: paywalled, no redistribution grant; buy from the owner | https://www.sae.org/standards/content/arp4761a/ |

## Free regulator paths

| Designation | Title | Edition | Owner | Status | URL |
|-------------|-------|---------|-------|--------|-----|
| AC 20-115D | Airborne Software Development Assurance Using EUROCAE ED-12( ) and RTCA DO-178( ). FAA recognition of DO-178C/ED-12C; the FAA text this repo packages builds on it. | 2017-07-21 | FAA | Open, pack: faa-8110-49 | https://www.faa.gov/regulations_policies/advisory_circulars/index.cfm/go/document.information/documentID/1032046 |
| AC 20-152A | Development Assurance for Airborne Electronic Hardware. FAA recognition of DO-254/ED-80, including the simple versus complex device treatment. | 2022-10-07 | FAA | Open, pack: faa-8110-49 | https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-152A.pdf |
| FAA Order 8110.49A | Software Approval Guidelines. How FAA offices plan and conduct software reviews and conformity inspections; the base text of pack faa-8110-49. | 2018-03-29 | FAA | Open, pack: faa-8110-49 | https://www.faa.gov/documentLibrary/media/Order/FAA_Order_8110.49A.pdf |
| AMC 20-115D and AMC 20-152A | EASA acceptance of DO-178C and DO-254, published inside Easy Access Rules for Acceptable Means of Compliance for Airworthiness of Products, Parts and Appliances (AMC-20). The Amendment 23 volume lists AMC 20-115D, Airborne Software Development Assurance Using EUROCAE ED-12 and RTCA DO-178, and AMC 20-152A. | Amendment 14 origin (ED Decision 2017/020/R) and Amendment 19 origin (ED Decision 2020/010/R), consolidated in EAR Amendment 23 (June 2023) | EASA | Open, pack: easa-rules. The origin decisions: ED Decision 2017/020/R (https://www.easa.europa.eu/en/document-library/agency-decisions/ed-decision-2017020r) and ED Decision 2020/010/R (https://www.easa.europa.eu/en/document-library/agency-decisions/ed-decision-2020010r) | https://www.easa.europa.eu/en/document-library/easy-access-rules/easy-access-rules-acceptable-means-compliance-airworthiness |

## Scope & Limits

- No reproduced standards text. Rows carry designation, title, edition, owner, status, and URL only.
- The open EASA path is packs/easa-rules. The AMC row carries the free URL.
- Editions are pinned as the How to use note states. Do not treat a row as a newer edition than the one printed.
- SAE rows carry the edition letter only. ARP4754B and ARP4761A have no publication date in this signpost.

---
*Signpost content is original JG Systems Consulting Ltd. work, MIT licensed. Trademarks and standard designations are named for identification only.*

---
name: q20-coc-drd
description: "Prepare and assess the certificate of conformity of ECSS-Q-ST-20C Annex D against its document requirements description: validate the identification and signature fields the DRD names, refuse a certificate asserting full conformity while enumerating deviations or qualifying its conformity with none listed, resolve every evidence reference against the delivered evidence register, report the coverage, and reject a signature held by a function inside the organisation that built the item or dated before the evidence it certifies. Use when a certificate is raised, countersigned or checked at incoming inspection. Trigger: ecss, q-st-20c-annex-d, certificate-of-conformity-drd, coc-conformity-statement, coc-evidence-references, coc-signature-authority, coc-deviation-list."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, q-st-20c-quality-assurance-scope, q20-coc-drd, certificate-of-conformity-drd, coc-conformity-statement, coc-evidence-reference-resolution, coc-signature-authority-independence, coc-deviation-enumeration, coc-signature-date-check]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Certificate of Conformity DRD (space-systems/ecss/q20-coc-drd)

Use when the task is the Annex D document requirements description of
ECSS-Q-ST-20C: a certificate is being raised for a delivery or checked on
receipt, and the question is whether the sheet actually certifies anything
a receiving organisation could rely on.

## Domain quick reference

- The certificate is three things at once: an identification of what is
  being delivered, a statement about it, and a signature that makes the
  statement someone's responsibility. A field left blank breaks one of the
  three, so the identification fields are graded as hard as the statement.
- The statement is one of two, and the deviation list decides which. Full
  conformity with deviations listed underneath is a contradiction on the
  page: either the item conforms or the departures are enumerated and
  agreed. A qualified statement with nothing enumerated is the same defect
  the other way round, and it is the one that reads as harmless.
- The evidence references are the certificate's whole substance. The
  as-built configuration list, the acceptance test report, the inspection
  record and the material certificate are what the statement rests on, and
  a reference that does not resolve in the register travelling with the
  delivery certifies nothing.
- Coverage is reported as a fraction rather than a yes. A certificate
  pointing at three of the four kinds is a specific, fixable gap, and
  saying so is more useful than rejecting the sheet.
- Independence is the point of the signature. A certificate signed by the
  function that built the item is the builder agreeing with itself; the
  signing authority sits in the quality or product assurance line.
- A signature cannot predate its own evidence. A certificate dated before
  the last report it cites was issued was signed against something the
  signatory had not seen, which is the failure mode that survives every
  other check on the page.

## Workflow

1. Validate the certificate: every DRD field present and non-blank, the
   quantity and specification issue positive integers, the signature date
   an ISO day, and the statement one the DRD admits.
2. Name the fields left blank as a single finding rather than one each.
3. Compare the statement with the deviation list in both directions.
4. Normalise the evidence register once, then check each evidence kind is
   cited and that each cited reference resolves in it.
5. Compute the evidence coverage fraction over the recognised kinds.
6. Check the signing function against the independent authorities, and the
   signature date against the latest evidence issue date it cites.
7. Return the coverage, the deviation count and the certificate verdict.

## Pitfalls

- Reading the statement without the deviation list, or the list without
  the statement. Each is defensible alone and the pair is what fails.
- Accepting an evidence reference because it looks like an identifier.
  Resolution against the register supplied with the delivery is the check;
  a plausible number is not one.
- Treating partial evidence coverage as a pass. Three of four kinds still
  leaves a statement resting on evidence nobody can find.
- Checking that the certificate is signed. Who signed it is the question,
  and a production signature is the common answer.
- Ignoring the dates. A certificate signed the week before the acceptance
  test report was issued is still a fully filled sheet.

## Behavior contract (gate 3)

The field validation, the statement to deviation-list consistency in both
directions, the evidence register normalisation, the reference resolution
and coverage fraction, the signing authority independence check and the
signature date against the latest cited evidence are exercised by the gate
3 contract test: scripts/test_q20_coc_drd.py against
scripts/q20_coc_drd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_q20_coc_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.

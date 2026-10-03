---
name: philippines-building-code-evidence-auditor-v2
description: Confirm the exact Philippine building, mall, hotel, establishment, branch, tenant, or complex, then run a four-lane earthquake-only public-evidence audit for NSCP/seismic evidence, OBO structural review evidence, post-earthquake tag/status, or clearance after damage/tag.
---

# Philippines Building Code Evidence Auditor V2

Use this skill for the V2 earthquake-only public-evidence workflow. V2 is an
isolated copy-and-revamp of V1. V1 remains the broad building-code evidence
auditor. V2 owns its own gates, schemas, fixtures, validators, and future
changes.

V2 has one permanent search scope: four earthquake evidence lanes. Gate 2
defaults to all four lanes unless the user narrows to one or more lanes. The
only valid Gate 2 scope IDs are `nscp_seismic_design_evidence`,
`obo_structural_permit_review_evidence`, `post_earthquake_tag_status`, and
`clearance_after_damage_or_tag`. Do not add a fifth lane, broad packet lane,
generic permit lane, contractor lane, standards lane, fire-safety lane,
accessibility lane, business-permit lane, or general building-code lane to V2.

The Gate 3 parent audit run is an output format for the selected lanes. It is
not a Gate 2 menu option.

## ECC Gate Review Habit

Before adding or changing any V2 gate, review the ECC contract:

- objective: what the gate owns and does not own;
- inputs: user words, place packet, links, files, and constraints;
- outputs: packet, prompt, locked scope, handoff, or blocker;
- eval: fixture transcript and pass/fail validator;
- handoff: what the next gate may assume;
- human boundary: what must be confirmed by the user;
- safety risks: overclaiming, unsafe search, external writes, credentials, or
  premature compliance/safety conclusions.

Each gate should be small enough to test with fixture transcripts.

## V2 Refusal And Routing Boundaries

Route non-earthquake building-code evidence questions to V1
(`philippines-building-code-evidence-auditor`) or to a future lane. V2 may
explain that the requested question is outside V2 and name the four V2 lanes,
but it must not silently broaden the scope.

Blocked in V2 unless tied to one of the four earthquake lanes:

- general permit or occupancy searches;
- generic contractor, architect, engineer, developer, or operator searches;
- general PD 1096, Fire Code, accessibility, green-building, business-permit, or
  standards-context searches;
- broad public-evidence packet requests;
- any conclusion that a building is compliant, noncompliant, safe, unsafe,
  earthquake-safe, earthquake-proof, fit for occupancy, cleared, unpermitted, or
  unreviewed without exact authoritative evidence for the selected lane.

## Gate 1 Contract

Gate 1 confirms exact building identity. Output a
`building_identity_confirmation` packet using
`data/philippines-building-code-evidence-auditor-v2/building-identity-schema.json`.

Keep these invariants:

- `identity_candidates` has zero to three candidates.
- `selected_candidate` is the best candidate, or `null` if none is reliable.
- `confirmation.can_proceed_to_audit` is `true` only when
  `confirmation.status` is `confirmed_by_user`.
- Blocked turns ask exactly one focused clarifying question.
- When a candidate is ready, show the user identity evidence such as Google
  Maps, official site, address, branch, tenant, wing, complex, city, and
  landmark clues before asking them to confirm.
- Public identity evidence builds confidence only; it never proves earthquake
  safety, NSCP/seismic design, OBO structural review, tag status, clearance,
  compliance, permit status, ownership, or construction quality.

Gate 1 lookup is identity-only. Use at most three search queries or three source
checks before asking the user for the next missing detail.

Allowed checks:

- name, branch, address, city, province, barangay, and landmark;
- map result, official site, mall/hotel page, booking page, establishment page,
  LGU page, reputable news page, or user-provided link;
- tenant/building relationship, such as a restaurant inside a mall;
- complex/building relationship, such as a mall, wing, tower, campus, estate, or
  mixed-use complex.

Blocked during Gate 1:

- NSCP/seismic evidence search;
- OBO structural permit or plan-review evidence search;
- post-earthquake tag/status search;
- clearance after damage/tag search;
- any claim about compliance, safety, risk, clearance, tag status, or legal
  status.

## Gate 2 Contract

Gate 2 is Earthquake Scope Lock. It starts only after Gate 1 has
`confirmation.status` set to `confirmed_by_user`.

Gate 2 answers one question: should the auditor run all four earthquake
evidence lanes by default, or should the user narrow to one or more lanes?

Keep these invariants:

- Ask exactly one four-option menu question that says all four lanes will run by
  default unless the user narrows the run.
- Accept answers by number, label, natural language, or no narrowing.
- If the answer is unclear, ask exactly one follow-up question and keep the
  evidence search blocked.
- `can_proceed_to_evidence_search` is `true` when all four lanes are defaulted
  or one or more of the four lanes are explicitly selected.
- Do not search evidence during Gate 2.
- Do not offer or accept a fifth scope.

The permanent V2 Gate 2 menu is:

1. NSCP / seismic design evidence
2. OBO structural permit or review evidence
3. Latest post-earthquake tag / status
4. Latest clearance after damage or tag

Prompt pattern:

"For [confirmed place], I can run all four earthquake evidence searches by
default, or you can narrow this to one or more lanes:
1. NSCP / seismic design evidence
2. OBO structural permit or review evidence
3. Latest post-earthquake tag / status
4. Latest clearance after damage or tag"

Scope-to-lane mapping:

- `nscp_seismic_design_evidence`: direct target-specific NSCP/seismic design or
  review evidence.
- `obo_structural_permit_review_evidence`: target-specific OBO structural permit,
  civil/structural permit, plan-review, evaluation, approved plan, or occupancy
  record that references the structural scope.
- `post_earthquake_tag_status`: latest official green/yellow/red tag,
  restriction, no-entry, unsafe/not-safe-for-occupancy, inspection disposition,
  or equivalent post-earthquake status.
- `clearance_after_damage_or_tag`: latest official clearance, lifting notice,
  updated green tag, reoccupancy clearance, accepted repair/retrofit completion,
  or signed/sealed structural stability certificate after damage/tag context.

Use
`data/philippines-building-code-evidence-auditor-v2/earthquake-source-reality.json`
before designing or running evidence collection.

## Gate 3 Parent Audit Run And Lane Packets

Gate 3 creates a parent audit run for the selected earthquake lanes, then
creates one child lane packet per selected lane. Use
`data/philippines-building-code-evidence-auditor-v2/audit-run-schema.json` for
the parent run and
`data/philippines-building-code-evidence-auditor-v2/evidence-packet-schema.json`
for each child lane packet.

Parent audit runs must record:

- `confirmed_building`;
- `selected_earthquake_lanes`;
- `source_ingestion_policy`;
- `lane_packets`;
- `overall_summary`;
- `unresolved_cross_lane_exceptions`;
- `final_overclaim_status`.

Public-source ingestion stores metadata plus short snippets only: URL, source
label, source class, date or freshness signal when visible, short excerpt, query
used, and lane relevance. Do not mirror whole public pages by default.

Each child lane packet collects and classifies public evidence for exactly one
selected earthquake lane.

Child lane packets must record:

- `confirmed_building`;
- `locked_earthquake_lane`;
- `document_inventory`;
- `evidence_strength`;
- `source_curation_class`;
- `physical_condition_public_evidence`;
- `unresolved_exceptions`;
- `manual_request_targets`;
- `overclaim_boundary`;
- `query_log`;
- `packet_result`.

The four earthquake-only questions are:

1. NSCP/seismic design evidence: answerable only from target-specific signed and
   sealed structural design analysis/computations or structural
   design-computation-seismic analysis, a signed/sealed civil/structural
   documents/plans/designs-computations-plans-specifications package, or an
   official OBO/Building Official record saying civil/structural plans,
   computations, or specifications were reviewed, approved, accepted, or found
   conforming.
2. OBO structural permit/review evidence: answerable only from a target-specific
   issued building permit, issued/approved/released civil/structural permit,
   compliance evaluation sheet, OBO evaluation/correction/deficiency/notice of
   disapproval record, approved civil/structural plans, or certificate of
   occupancy that references the relevant issued permit or approved structural
   scope.
3. Latest post-earthquake tag/status: answerable only from an official green tag
   or inspected/green placard, yellow tag or restricted-use disposition, red tag
   or no-entry/unsafe-for-occupancy disposition, or official rapid visual
   inspection/assessment/report that states the tag, disposition, occupancy
   restriction, required repair, or clearance condition.
4. Latest clearance after damage/tag: answerable only from official reoccupancy
   clearance, updated green tag after a previous yellow/red tag, official
   clearance/lifting/fit-for-reoccupancy notice, accepted final
   inspection/completion/repair/retrofit compliance record with occupancy/use
   language, or a signed and sealed structural stability or structural soundness
   certificate tied to the post-earthquake or repair context.

No-evidence semantics:

- For `nscp_seismic_design_evidence` and
  `obo_structural_permit_review_evidence`, a proper search with no findings
  means: "No public evidence found."
- For `post_earthquake_tag_status` and `clearance_after_damage_or_tag`, a
  proper search with no findings means: "No public answer found."
- Neither result may become "safe," "unsafe," "compliant," "noncompliant,"
  "no tag," "cleared," "no permit exists," "not reviewed," or "unpermitted."

## Gate 4 Final Overclaim Audit

Gate 4 audits every Gate 3 child lane packet and then audits the parent audit
run summary before presenting conclusions.

Checklist:

- exact building match confirmed;
- selected lanes are one or more of the four earthquake lanes;
- every positive claim has a source URL;
- official/professional evidence is separated from weak leads;
- operator/corporate claims are not treated as official clearance;
- missing public evidence is not converted into "safe," "unsafe," "compliant,"
  "noncompliant," "cleared," "no tag," "not reviewed," or "no permit";
- red/yellow tag evidence is preserved when found;
- unresolved exceptions are preserved;
- query log is present for no-evidence outcomes;
- parent summary does not overstate any child lane result.

If Gate 4 finds an overclaim, revise the affected child lane packet or parent
summary. Do not present the claim as a finding.

## Source Curation Classes

Use these classes in V2 packets:

- `official_record`: LGU/OBO/OCBO/DPWH/BFP/City Engineer/CDRRMO/authorized
  public record, notice, list, placard, clearance, permit, evaluation, or
  inspection result.
- `professional_record`: signed/sealed engineer or professional document tied to
  the exact building/subscope.
- `operator_corporate_claim`: owner/operator/developer/corporate filing or
  announcement, useful as evidence only within its stated limits.
- `reputable_news_lead`: reputable news report used as a lead or context, not as
  official tag/clearance unless it links to or quotes an official record and the
  official source is also captured.
- `process_context`: public process, standards, or document-request context.
- `weak_lead`: social, marketing, booking, reopening, photo, or directory lead.

## Evidence Strength Ladder

Use these values:

- `direct_authoritative_target_evidence`
- `professional_target_evidence`
- `strong_indirect_target_evidence`
- `process_or_standards_context`
- `weak_lead_only`
- `not_found_after_reasonable_search`

## Validation

Before treating V2 changes as complete, run:

```bash
npm test
npm run validate
git diff --check
```

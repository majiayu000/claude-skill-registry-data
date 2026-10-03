---
name: philippines-building-code-evidence-auditor
description: Confirm the exact Philippine building, mall, hotel, establishment, branch, tenant, or complex, then lock the audit scope before a building-code evidence audit. Use when a user gives a Philippine place clue, abbreviation, map link, booking link, receipt, photo, landmark, rough city, or audit question and the workflow must lock building identity and public-evidence scope before permit, contractor, incident, compliance, safety, or hazard evidence search.
---

# Philippines Building Code Evidence Auditor

Use this skill for the pre-search gates of the Philippines Building Code
Evidence Auditor. Gate 1 confirms building identity. Gate 2 locks the audit
scope. Do not search building permits, contractors, incidents, code compliance,
structural safety, or earthquake safety until the user confirms the exact place
and explicitly confirms the audit scope.

## ECC Gate Review Habit

Before adding or changing any gate, review the ECC contract:

- objective: what this gate owns and does not own;
- inputs: user words, place packet, links, files, and constraints;
- outputs: packet, prompt, locked scope, handoff, or blocker;
- eval: fixture transcript and pass/fail validator;
- handoff: what the next gate may assume;
- human boundary: what must be confirmed by the user;
- safety risks: overclaiming, unsafe search, external writes, credentials, or
  premature compliance/safety conclusions.

Each gate should be small enough to test with fixture transcripts.

## Gate 1 Contract

Output a `building_identity_confirmation` packet using
`data/building-code-auditor/building-identity-schema.json`.

Keep these invariants:

- `identity_candidates` has zero to three candidates.
- `selected_candidate` is the best candidate, or `null` if none is reliable.
- `confirmation.can_proceed_to_audit` is `true` only when
  `confirmation.status` is `confirmed_by_user`.
- Blocked turns ask exactly one focused clarifying question.
- Public identity evidence builds confidence only; it never proves compliance,
  safety, permit status, ownership, or construction quality.

## Light UX Flow

1. Capture the raw clue exactly as given.
2. Extract known name, city/province, address text, landmarks, links, and media.
3. If the clue is searchable, check only name, branch, address, city, link, or
   tenant/building relationship before asking.
4. Classify the ambiguity.
5. Show the best candidate plus up to two alternates only when ambiguity is real.
6. Ask the smallest useful question.
7. Stop until the user confirms.

Prefer one short question over intake forms. Ask for a city, link, address,
receipt, photo, or landmark only when it is the next blocking detail.

## Objective Lookup Limits

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

- building permit or occupancy permit search;
- contractor, architect, engineer, developer, or owner investigation;
- incident, earthquake damage, closure, retrofit, repair, hazard, compliance, or
  safety search;
- any claim about compliance, safety, risk, or legal status.

## Ambiguity Classes

Use these categories in test cases and reasoning:

- `clear_candidate`: specific name plus city, address, link, or strong branch
  clue points to one place.
- `ambiguous_similar_places`: abbreviation, brand, mall, hotel, school,
  hospital, or branch name maps to multiple places.
- `tenant_vs_building`: clue names a shop, restaurant, clinic, office, or other
  establishment inside a larger structure.
- `complex_vs_building`: clue may refer to a mall, estate, campus, tower group,
  subdivision, or mixed-use complex rather than one building.
- `weak_clue`: clue lacks enough city, address, link, media, or landmark detail.
- `rejected_candidate`: user rejects the selected candidate.
- `confirmed_place`: user explicitly confirms the exact target.

## Philippine Context Rules

- Treat abbreviations as unsafe until expanded: KCC, SM, Robinsons, Ayala, S&R,
  NCC, CityMall, and similar shorthand.
- Normalize aliases carefully: GenSan/General Santos, Marbel/Koronadal,
  BGC/Taguig, QC/Quezon City, Ortigas/Pasig/Mandaluyong boundary cases.
- Expect branch-heavy names across malls, hotels, hospitals, schools, banks,
  restaurants, supermarkets, and chain stores.
- Separate brand/operator from structure. A hotel brand, mall tenant, developer,
  office, or trade name may not be the building owner or the audit target.
- Treat barangay, city, province, region, street, and landmark as identity
  evidence because the same name may exist in many Philippine places.
- For malls and mixed-use sites, ask whether the user means the whole complex,
  one building, one wing, or a tenant.

## Prompt Patterns

Use plain language:

- Clear candidate: "I think you mean [name] at [address/city]. Is that the exact
  building?"
- Multiple branches: "Do you mean [A], [B], or [C]?"
- Tenant/building: "Should I audit the tenant location, the whole building, or
  both?"
- Complex/building: "Should I treat this as the whole complex, or one specific
  building/wing?"
- Weak clue: "What city/province is this in, or do you have a map link, photo,
  receipt, or booking page?"
- Rejected candidate: "Got it, I will not use that one. Can you send a map link,
  city, landmark, or exact branch?"

For "KCC", first ask whether the user means KCC Malls or Korean Cultural Center.
If the user says KCC Mall, ask for branch or city. If the user says KCC GenSan,
confirm KCC Mall of GenSan before proceeding.

## Gate 2 Contract

Gate 2 is Audit Scope Lock. It starts only after Gate 1 has
`confirmation.status` set to `confirmed_by_user`.

Gate 2 answers one question: what public-evidence audit should run for the
confirmed place?

Keep these invariants:

- Ask exactly one menu question when no scope is locked.
- Accept an answer by number, label, or natural language.
- If the answer is unclear, ask exactly one follow-up question and keep the
  evidence search blocked.
- `can_proceed_to_evidence_search` is `true` only when the scope is explicitly
  confirmed.
- Do not search permit, incident, contractor, compliance, safety, hazard, or
  other evidence during Gate 2.

Annotated menu choices:

1. Permit or occupancy records - usually LGU/OBO process pages or manual record
   request; not a national public registry.
2. Incident, damage, closure, repair, or retrofit history - often publicly
   searchable through LGU/government/news sources, but not proof of current
   safety.
3. Contractor, professional, developer, or operator evidence - usually requires
   a known name, license number, project name, or source lead.
4. Standards or process context only - public standards context; not
   building-specific compliance proof.
5. Broad public-evidence packet - combines lanes and separates public findings
   from manual follow-ups.

Prompt pattern:

"For [confirmed place], what do you want checked?
1. Permit or occupancy records - usually LGU/OBO process pages or manual record
request; not a national public registry
2. Incident, damage, closure, repair, or retrofit history - often publicly
searchable through LGU/government/news sources, but not proof of current safety
3. Contractor, professional, developer, or operator evidence - usually requires
a known name, license number, project name, or source lead
4. Standards or process context only - public standards context; not
building-specific compliance proof
5. Broad public-evidence packet - combines lanes and separates public findings
from manual follow-ups"

When clear:

"Got it. I will lock the scope as [scope]. [One sentence about Philippine source
reality for that scope.] I will not search outside that unless you ask."

Use these source-reality confirmation sentences:

- Permit or occupancy records: "In the Philippines, this usually means LGU/OBO
  process pages or a manual record request, not a national public registry."
- Incident, damage, closure, repair, or retrofit history: "In the Philippines,
  this is often publicly searchable through LGU, government, or reputable news
  sources, but it is not proof of current safety."
- Contractor, professional, developer, or operator evidence: "In the
  Philippines, this usually needs a known name, license number, project name, or
  source lead before the evidence search can work."
- Standards or process context only: "In the Philippines, this can cite public
  standards and process context, but it cannot prove building-specific
  compliance."
- Broad public-evidence packet: "In the Philippines, this will separate public
  findings from manual follow-ups across the available lanes."

When unclear:

"Do you want a narrow [best guess] check, or a broad public-evidence packet?"

Scope-to-lane mapping:

- `permit_occupancy_records`: `lgu_obo`, with standards context only as needed.
- `incident_damage_history`: `incident_safety_history`, with manual follow-up
  labels when official records are not public.
- `contractor_professional_developer`: `contractor_professional`, only after a
  name is identified from source evidence or user input.
- `standards_context_only`: `standards`; do not imply building-specific
  compliance.
- `broad_public_evidence_packet`: `standards`, `lgu_obo`,
  `contractor_professional`, `incident_safety_history`, and
  `foi_manual_requests`, with citation review before conclusions.

## Gate 2 Source-Reality Matrix

Use `data/building-code-auditor/audit-scope-source-reality.json` before
designing or running evidence collection. It records which Gate 2 scopes are
public-searchable, public-process-only, manual/FOI-needed, name-required, or not
publicly provable in the Philippine context.

For NSCP, structural-code, structural-compliance, or earthquake-safety
questions, also use `data/building-code-auditor/nscp-compliance-evidence-map.json`
and `reports/nscp-structural-code-compliance-search-method.md`. The default
target-specific NSCP status is `not_assessable_from_public_web` unless the
search finds a target-tied official or professional document such as a building
permit, civil/structural permit, certificate of occupancy, OBO evaluation sheet,
signed and sealed structural plans, structural design analysis/computation,
structural stability certificate, official inspection/assessment, repair or
retrofit permit, reoccupancy clearance, or equivalent authoritative record.

Keep these source-reality rules:

- Permit and occupancy records are real and applicable, but usually appear as
  LGU/OBO process pages, applicant portals, citizen charters, or manual record
  request paths rather than nationwide public building registries.
- Incident, damage, closure, repair, and retrofit history can be public when
  LGUs, DPWH, PIA, PNA, or reputable news report it; old or missing reports do
  not prove current safety.
- Contractor, professional, developer, and operator checks usually require a
  name, license number, project name, or source lead; they cannot be inferred
  from an address alone.
- Standards context can cite PD 1096, DPWH/NBCDO references, Fire Code,
  accessibility, green-building, and professional-standard context; it cannot
  prove building-specific compliance.
- Broad public-evidence packets must keep standards, permits, incidents,
  contractor/professional evidence, and manual requests as separate lanes with
  separate caveats.
- Generic NSCP, PD 1096, ASEP, PRC, OBO, BFP, reopening, booking, operating
  hours, social-media, or news evidence is not enough to claim a named building
  is NSCP-compliant, structurally compliant, earthquake-safe, or fit for
  occupancy.

Never turn missing public evidence into "no permit," "no incident,"
"unlicensed," "compliant," "noncompliant," "safe," "unsafe," or "fit for
occupancy." Use `manual_request_needed`, `not_found`, or
`not_assessable_from_public_web` instead.

## Gate 3 Document-Target Learning

For evidence collection, start from exact document targets before broad
compliance language. Use
`data/building-code-auditor/gate-3-sm-moa-document-target-matrix.json` and
`reports/gate-3-sm-moa-document-target-search.md` as the first learning example.

Gate 3 packets should record:

- `target_subscope`;
- `document_target`;
- `document_family`;
- `likely_custodian`;
- `source_reality_status`;
- `strongest_public_source`;
- `target_specific_result`;
- `manual_follow_up`;
- `overclaim_boundary`;
- `query_log`.

For building-code evidence, the first document targets are usually building
permit application records, civil/structural plans, structural design analysis
and computations, boring/soil tests, OBO evaluation sheets, FSEC, FSIC,
certificate of occupancy, certificate of completion, approved/as-built plans,
annual building inspection certificate or permit, structural stability and safety
certificate, post-incident assessment, repair or retrofit permits, reoccupancy
clearance, and corporate/operator filing leads. Classify each target separately.

For earthquake-only citizen questions, use
`data/building-code-auditor/earthquake-safety-answerability-matrix.json` and
`reports/earthquake-safety-answerability-matrix.md`. The answerability field must
be only `answerable` or `not_answerable`.

For Davao City earthquake-only searches, also use
`data/building-code-auditor/davao-earthquake-source-targets.json` and
`reports/davao-earthquake-source-targets.md`. They add Davao-specific source
targets such as `Seismic Analysis`, `Civil/Structural Permit Form with
Civil/Structural Plans`, `Evaluation Sheet`, `Building Permit Number`,
`Certified True Copy of Documents`, red/yellow tag notices, unsafe/not-safe for
occupancy findings, and `cleared by OCBO` language.

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
3. Latest post-earthquake tag/status: answerable only from an official green
   tag or inspected/green placard, yellow tag or restricted-use disposition, red
   tag or no-entry/unsafe-for-occupancy disposition, or official rapid visual
   inspection/assessment/report that states the tag, disposition, occupancy
   restriction, required repair, or clearance condition.
4. Latest clearance after damage/tag: answerable only from official
   re-occupancy clearance, updated green tag after a previous yellow/red tag,
   official clearance/lifting/fit-for-reoccupancy notice, accepted final
   inspection/completion/repair/retrofit compliance record with occupancy/use
   language, or a signed and sealed structural stability or structural soundness
   certificate tied to the post-earthquake or repair context.

## Validation

This is a predecessor skill. Its former Python gate scripts were removed during
the 2026-07-06 Python-surface reduction. Use the active V2 skill for current
validation.

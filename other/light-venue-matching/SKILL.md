---
name: light-venue-matching
description: Build evidence-bound journal or conference shortlists for Light stage 12. Use after typesetting delivers venue-handoff.json/PDF/compliance facts; when an author asks where to submit, journal selection, conference fit, scope or article-type matching, publication strategy, reach/match/safety tiers, transfer order, APC/OA/indexing/deadline constraints, or predatory/hijacked-journal risk. Produces a current-source candidate registry, fit/risk/unknown reports, and an unchosen decision packet; never recompiles the PDF, invents acceptance rates, condemns a venue from soft signals, chooses without a direct user choice or explicit delegation, or submits.
---

# Venue matching · stage 12

Turn a delivered paper into an auditable venue decision. Read
`venue-resource-map.md` before a real run and
`references/workflow_contract.md` before producing or consuming JSON. Use
`references.md` to choose current sources. Start from
`templates/venue_input.json`; never start from model memory or a bundled venue
list.

## Non-negotiable boundaries

1. Consume typesetting's `venue-handoff.json`. Verify its PDF path/hash,
   `DELIVERED`, pages, page size, profile/source, compliance `PASS`, and zero
   critical findings. Preserve paper/figure/citation/typesetting provenance.
   Do not compile, reformat, inspect page boxes again, or treat stage-11
   `UNAVAILABLE` as compliance.
2. Consume paper-writing's manuscript/claim profile through
   `manuscript_profile.claims_delivery` with a safe relative path, schema, and
   SHA-256. Do not change claims, methods, results, article type, data scale,
   or evidence strength to make a venue fit. Citation owns reference
   authenticity; figure owns visual honesty.
3. Treat acceptance rate, review time, APC/OA, indexing, quartile, and CFP
   deadline as high-velocity fields. Require a source checked on the run date.
   Otherwise emit `UNKNOWN`, `UNAVAILABLE`, or `STALE`; never use memory.
   `AVAILABLE` sources must carry an auditable locator (`url`, `query`,
   `locator`, or `path`), `checked_at`, `access_tier`, and `authority`.
   Official rules/fees/deadlines require official/publisher/venue authority;
   indexing and quartile require index/registry authority.
4. Treat 403/429/5xx, missing key/login/subscription, robots denial, and source
   outage as `UNAVAILABLE`. They do not mean “not indexed,” “not in DOAJ,”
   “free,” or “risky.”
5. Keep predatory/hijacked signals as visible warnings pending current,
   multi-source human review. DOAJ absence, high APC, fast review, unsolicited
   email, unusual volume, or one archived list is not a final verdict.
6. Never estimate an acceptance percentage or convert fit into acceptance
   probability. Use official current acceptance figures only with source/date;
   otherwise `acceptance_likelihood.status=UNKNOWN`.
7. Keep `decision_point=true` and `chosen=null` through candidate discovery,
   evidence collection, ranking, and delivery. Stop and ask the user to choose.
   Only an explicit `light.venue_user_selection.v1` may create a selected
   handoff. Record a direct choice as `actor=user`; if the user explicitly
   delegates the choice, preserve the authorization verbatim and use
   `actor=agent_with_user_authorization`, `decision_authority=user`. Never
   submit. Every selection artifact must include timezone-aware `selected_at`
   and the user's stated trade-off in `because`. Bind the choice to the exact
   reviewed packet with `decision_sha256`; a changed packet or any changed
   registry/evidence/fit artifact requires a new review and selection.
8. Do not invent `STAGE_GATES[12]`, `ROUTES[12]`, a confirmation checkpoint,
   critical findings, or a back-edge. Stage 12 is a user decision point with no
   configured gate or route edge.

## Workflow

### 1. Consume the real submission artifact

Require `light.typesetting_venue_handoff.v1`. Run prepare only when:

- `status=DELIVERED`;
- `compliance_status=PASS` and `critical_count=0`;
- the PDF exists and its SHA-256 matches;
- the compliance report exists and agrees on page facts.

If any condition fails, return an input error and route the author to stage 11
without creating a stage-12 critical finding.

### 2. Capture the author constraints

Record, without filling gaps yourself:

- research direction, article type, methods, data scale, claims/evidence;
- author stage, region, required indexes, OA requirement, APC ceiling;
- hard submission deadline and acceptable review duration;
- reach/match/safety preference and transfer strategy;
- unacceptable venues, publishers, business models, or risks.

Mark each constraint as hard or soft. A hard author constraint can exclude; a
soft preference changes order and explanation.
Bind the claim/evidence profile to the current paper-writing artifact via
`claims_delivery.path + sha256 + schema`; a hand-typed manuscript profile is
not enough for stage 12.

### 3. Discover for recall, then verify for precision

Keep the unpublished manuscript local. Before any public or externally
authenticated search, translate it into author-approved broad field/method-family
terms and preflight the outgoing queries:

```powershell
python scripts/query_privacy_gate.py `
  --input templates/query-privacy.example.json
```

Do not send the unpublished title, abstract, exact hypotheses, unique method or
dataset names, result sentences, tables, or figures to a public search engine.
The preflight report intentionally retains only query hashes and match categories.
Its PASS detects supplied phrase overlap; it cannot prove anonymity or rule out
re-identification.

Use the author's candidate list, current official CFPs, publisher finders, and
`venue_discovery.py`:

```powershell
python scripts/venue_discovery.py `
  --query "author-approved broad field and method family" --rows 50 --out discovery.json
```

Crossref container frequency only discovers candidates. It does not establish
scope, rank, indexing, safety, or quality. Record every discovery query,
endpoint, access tier, status, and check time. Deduplicate by ISSN plus official
name; keep title conflicts for manual review.

### 4. Build field-level evidence

For every candidate, collect separate envelopes for:

- official Aims & Scope and article types;
- length/page, figure/table, supplement, anonymity, template, and format rules;
- method/data fit and recent comparable articles;
- OA/APC, timing, indexing/quartile, and current CFP deadline;
- risk/hijack checks and unresolved identity conflicts.

Prefer official venue/publisher instructions for rules, authoritative indexes
for index membership, and registration metadata for identity. Keep JCR,
Scopus, Cabells, institutional lists, and paywalled fields unavailable unless
the author provides lawful access. Never scrape around access controls.

### 5. Prepare the canonical decision packet

```powershell
python scripts/venue_evidence_gate.py `
  --spec venue-evidence.json --report venue-evidence-findings.json `
  --json-out venue-evidence-report.json
python scripts/venue_workflow.py prepare `
  --input venue-input.json --out-dir venue-run --as-of YYYY-MM-DD
```

Run `venue_evidence_gate.py` first when candidate evidence has been collected. It consumes `light.venue_evidence.v2`
([`templates/venue-evidence.example.json`](templates/venue-evidence.example.json), intentionally fail-closed) and checks each candidate on independent axes:
scope, article type, audience, format, cost, timeline, trust, and strategy. Do not use a single aggregate score.
Dynamic fields must carry locator, `retrieved_at`, valid-at/source age, timezone when relevant, and `UNKNOWN/UNAVAILABLE/STALE`
when not verified. Hard blockers include article type not accepted, official scope mismatch, fee over a hard APC ceiling,
unknown fee under a hard ceiling, deadline missing timezone or already passed, missing timezone-aware `as_of`, future
`retrieved_at`, identity conflict/hijack, and strategy without evidence-backed `because`. DOAJ/TCS/source failures remain
unresolved evidence, not adverse evidence.

Compare real PDF pages/page size/profile facts with each candidate's current
rules. Explain scope, article type, method/data, paper strength, format, APC/OA,
timing, indexing, risk, and author constraints separately. An official
article-type/page mismatch or hard author constraint may exclude. A soft risk
signal may not.

Emit reach/match/safety tiers and a transfer order. Every option needs
`because` plus evidence source IDs. Unknown fields lower confidence; they do
not silently lower the venue or become adverse evidence.

### 6. Stop at the user decision

Show the decision packet and ask one concrete question: which candidate should
be selected? Present material trade-offs and unresolved fields. Do not write a
selection file without a direct user choice or explicit delegation. Never
select an excluded candidate.

Correct:

> Candidate A is reach because scope/method fit is high but the official bar is
> above the paper profile; APC is unavailable. Candidate B is match with an
> article-type fit and current zero-APC evidence. Which do you choose?

Incorrect:

> I selected Candidate A and updated the project.

### 7. Apply the user's choice

After the user names a candidate or explicitly delegates the choice, copy
`templates/user_selection.json`, record their stated reason or verbatim
authorization, copy `delivery.json.decision_sha256` into `decision_sha256`,
and run:

```powershell
python scripts/venue_workflow.py choose `
  --decision venue-run/decision-packet.json `
  --selection user-selection.json --out-dir selected
```

Hand `selected-venue-handoff.json` and
`review-rebuttal-context.json` to review-rebuttal. Hand
`author-submission-plan.json` to the author. Both consumers receive venue
rules, evidence IDs, unknowns, manuscript profile, and stage-11 provenance.
`selected_at` must be timezone-aware and not earlier than the decision packet's
`generated_at`. `choose` verifies the decision digest plus the SHA-256/schema
binding of candidate registry, source evidence, fit report, and unknowns; any
drift fails closed. Recheck volatile fields on submission day and stop before
portal submission.

## Script roles

- `venue_discovery.py`: current, recall-oriented Crossref discovery with honest
  network status.
- `query_privacy_gate.py`: local outgoing-query preflight; catches supplied
  private phrase/result-value overlap without echoing manuscript or query text.
- `venue_workflow.py`: canonical handoff verification, field-state
  normalization, fit/risk explanation, decision packet, and user-selection
  handoff.
- `venue_signal.py`: optional OpenAlex/DOAJ signal adapter; free OpenAlex key
  may be required and each failed signal stays unavailable.
- `venue_evidence_gate.py`: Round 3 multi-axis `venue_evidence.v2` gate; separates scope/type/cost/timeline/trust/strategy, forbids aggregate-score decisions, preserves UNKNOWN/UNAVAILABLE/STALE, and blocks hard constraint mismatches before the user decision packet.
- `venue_fit_rank.py`: legacy v1 candidate-card adapter; do not use it instead
  of the canonical registry.
- `venue_risk_gate.py`: optional legacy warn-only findings adapter; never a
  stage-12 critical gate.

## Delivery self-check

- [ ] Real typesetting PDF/hash/pages/page-size/profile/compliance consumed?
- [ ] Paper, citation, figure, and typesetting provenance preserved?
- [ ] Paper-writing claim/profile artifact bound by safe relative path, schema
      and SHA-256?
- [ ] Author direction/type/method/data/stage/region/index/OA/APC/deadline/
      speed/strategy/unacceptable constraints recorded?
- [ ] Public queries use approved broad terms and pass local privacy preflight?
- [ ] Every current field has source, query/URL, check date, access tier, and
      status?
- [ ] `venue_evidence_gate.py` ran on `venue_evidence.v2`, with no aggregate score, no premature `chosen`, and every candidate axis separately evidenced?
- [ ] Deadline timezone, fee category/APC ceiling, waiver, source age, DOAJ/TCS unavailable states, and identity/hijack conflicts are explicit?
- [ ] Unknown, 403/429/5xx, key/login, institutional, and paid fields remain
      `UNKNOWN/UNAVAILABLE/STALE` rather than adverse evidence?
- [ ] Official scope/type/length compared with real paper facts?
- [ ] Soft risk stays warning and predatory/hijacked verdict stays human?
- [ ] Reach/match/safety and transfer order each carry `because` and evidence?
- [ ] `decision_point=true`, `chosen=null`, and no selected handoff before the
      user's explicit choice?
- [ ] User selection binds the reviewed `decision-packet.json` SHA-256, and all
      four decision artifacts still match their bound hash/schema?
- [ ] No `STAGE_GATES[12]`, `ROUTES[12]`, critical finding, auto-choice, or
      submission invented?

## Honest capability boundary

Tiering, scope fit, APC/deadline filtering, risk warnings, author-fit, and
explainable recommendations are established peer mechanisms, not unique Light
features. Light's narrower implementation gain is canonical consumption of
the real stage-11 artifact, per-field provenance/access/status, honest failure
semantics, and an enforceable unchosen→user-selected artifact transition.
Round 3 adds an executable multi-axis evidence gate so a high scope score cannot hide article-type, fee, deadline, or trust blockers.
Keyword overlap and method/selectivity bands remain decision support, not an
editorial prediction. Paid/institutional sources stay optional.

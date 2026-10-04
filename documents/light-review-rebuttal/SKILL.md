---
name: light-review-rebuttal
description: Build auditable peer-review revision and author-response packages for Light stage 13. Use after receiving reviewer comments, a decision or meta-review; when drafting a rebuttal or response letter; when triaging major/minor revisions; when simulating a pre-submission review; or when a rejection may require a user-chosen 13→3 novelty, 13→5 experiment, or 13→8 writing back-edge. Consumes the selected venue/context and real PDF facts, preserves reviewer wording, atomizes issues, binds claims/evidence/actions/provenance, separates PLANNED from DONE, checks current venue limits without borrowing another venue's rules, and emits the stage-13 gate without changing venue, manuscript, evidence, citations, figures, PDF, or passport automatically.
---

# Review and rebuttal

Build a source-preserving review registry, issue matrix, revision plan,
evidence/change map, response draft, commitment ledger, unknown/failure record,
and delivery package. Treat prose generation as the last layer, not the first.

Read [`review-rebuttal-resource-map.md`](review-rebuttal-resource-map.md) before
a real run. Read
[`references/workflow_contract.md`](references/workflow_contract.md) before
creating or consuming canonical JSON. Read [`references.md`](references.md)
when selecting review/rule sources. The competitor evidence is
[`../../docs/competitors/review-rebuttal.md`](../../docs/competitors/review-rebuttal.md).

## Non-negotiable boundaries

1. Consume venue-matching's selected handoff and review context. Verify selected
   identity, `selected_at` timezone, `selection_basis`, user/delegated
   authorization, chosen candidate ID, fit/risk row, unmodified rule envelopes,
   source evidence path/as-of/source IDs, manuscript profile, and PDF
   path/hash/pages/page size/profile/compliance. Never switch venue, reorder
   tiers, or turn venue `UNKNOWN` into a fact.
2. Keep reviewer, editor, decision, and meta-review text verbatim in the
   canonical registry. Atom labels, root causes, strategies, and generated
   prose are interpretation layers; they never replace source text.
3. Record fetch time, source URL/type, round, reviewer ID, attachments and
   `AVAILABLE|UNKNOWN|UNAVAILABLE|STALE`. A 401/403/429/5xx, timeout, login,
   private invitation or network failure is `UNAVAILABLE`, not “no review.”
4. Never invent an experiment, analysis, citation, change, line number,
   reviewer identity, venue rule or result. `PLANNED` and `IN_PROGRESS` may not
   be phrased as completed. `DONE` requires a real change locator; completed
   experiment/analysis additionally requires verifiable run provenance with a
   matching SHA-256, not merely a local path.
   Before marking a response package ready, run the atom/action contract gate so
   source spans, reconstruction hashes, policy/ethics authorization and
   perspective-specific self-review are machine-checked rather than trusted.
5. Paper-writing owns manuscript claims and edits. Result-analysis owns
   evidence strength. Citation owns new-reference identity and claim support.
   Figure owns visual honesty. Typesetting owns PDF rebuild/compliance. This
   skill records and routes work; it does not impersonate those producers.
6. Stage 13 critical is narrow: only a routable root cause
   (`novelty|experiment|writing`) explicitly marked `rejection_driving=true`
   with a complete decision/meta-review/reviewer evidence envelope may become
   critical. Major labels or an overall Reject alone do not make every comment
   critical.
7. `reviewer_classify` and `reroute` produce advice only. Stop after presenting
   evidence and alternatives. Run `passport add-back-edge` only after the user
   chooses the root cause/back-edge. Never mutate the passport automatically.

## Canonical workflow

### 1. Verify upstream identity

Require:

- `light.selected_venue_handoff.v1`;
- `light.review_rebuttal_venue_context.v1`;
- `light.paper_claims.v1`;
- `light.evidence_strength.v1`;
- citation registry when any new citation is proposed;
- the actual delivered PDF and its stage-11 facts.

Run:

```bash
python scripts/review_workflow.py \
  --spec review-input.json \
  --outdir review-delivery
```

If venue identity, rule envelopes, PDF hash, compliance, claims or evidence IDs
do not agree, stop and repair the producer artifact. Do not “normalize” a
conflict away.

The selected handoff must also retain A32's audit fields: timezone-bearing
`selected_at` that is not in the future, non-empty `selection_basis`,
`decision_authority=user`, coherent `selected_by/status`, delegated
`user_authorization` when applicable,
unchanged `fit_risk`, and a readable `source_evidence.path` whose SHA-256
matches the selected handoff and whose `as_of/source_ids` cover every sourced
venue rule.

### 2. Capture reviews and decisions

For user-provided/private material, copy the text into `reviews[].raw_text`
without correction and record `reviews[].raw_sha256` plus a timezone-aware
`captured_at`; the workflow re-computes the hash and blocks future/naive capture
times. For a public OpenReview forum:

```bash
python scripts/fetch_openreview.py \
  --forum <forum-id> \
  --out openreview-capture.json
```

If the live API is unavailable but a fixed public PeerRead/OpenReview snapshot
is the declared evidence source, capture that exact commit-pinned JSON instead:

```bash
python scripts/fetch_openreview.py \
  --peerread-url <raw-fixed-commit-json-url> \
  --out peerread-capture.json
```

The capture is calibration/source evidence. Do not redistribute restricted
reviews. If capture is unavailable, continue only with material the user
provided and retain the failure record.

### 3. Atomize without erasing source

Create one atom for each distinct `request`, `claim`, `question`,
`misunderstanding`, or `editorial` item. Each atom must contain an exact
contiguous source span copied from `raw_text`, with start/end offsets, span
text and SHA-256. Also create addressable coverage units and a reconstruction
hash for the reviewer units that require a response.

Assign one root cause such as `novelty`, `experiment`, `writing`,
`clarification`, `citation`, `ethics`, `scope`, or `editorial`. Add a separate
interpretation explaining the inferred concern. If a sentence contains two
independent asks, create two atoms pointing to the same or overlapping source
span; do not paraphrase the reviewer into a new source quote.

Run the stricter losslessness/response-action gate before drafting:

```bash
python scripts/review_response_contract.py \
  --input templates/review-response-contract.example.json
```

Replace the template with the real contract. The example is intentionally
non-passing until current venue policy, ethics state and user authorization are
verified. This gate catches missing reviewer units, duplicate atom/action
coverage, fake DONE wording, incomplete evidence kinds, policy-forbidden
reviewer requests, missing reviewer competence/conflict cards, and missing
`domain|method|statistics|ethics|cold_reader` self-review perspectives.

### 4. Bind issues to owned evidence and actions

For every atom:

- bind exact paper `claim_id` values or leave the list empty;
- bind only real result-analysis evidence IDs;
- choose one strategy:
  `acknowledge_and_fix`, `rebut_with_evidence`, `clarify`,
  `downgrade_claim`, or `request_editor_ruling`;
- assign an owner and `PLANNED|IN_PROGRESS|DONE|DECLINED|NOT_APPLICABLE`;
- add change locator only after paper-writing actually edits the manuscript;
- add run provenance only after an experiment/analysis actually runs; for
  `DONE` experiment/analysis the artifact path must exist and match
  `run_provenance.sha256`;
- route new references through citation and keep them out until `CONFIRMED`.

Reviewer error is not permission to ignore a comment. Clarify with manuscript
locator and evidence, or request editor ruling when the disagreement is
material.

When a reviewer request itself conflicts with venue policy, ethics approval,
data rights, consent, budget authorization or editor instructions, do not
silently comply. Mark the action as `DECLINED` or `REQUEST_RULING`, bind the
policy/ethics evidence, and keep the reviewer wording intact.

### 5. Budget from the selected venue only

Run:

```bash
python scripts/rebuttal_budget.py \
  review-delivery/response-draft.md \
  --context review-rebuttal-context.json
```

An `AVAILABLE` current authoritative rule can yield PASS/FAIL. `UNKNOWN`,
`UNAVAILABLE`, `STALE`, or a page-only rule stays non-passing and explicit.
Never apply an ICLR/CVPR/other venue preset to JORS or vice versa.

For every reviewer request for new numbers/experiments, classify it before any
run as reanalysis/minimal/adapted/new-data plus feasibility and intended action:

```bash
python scripts/experiment_request_gate.py \
  --input templates/experiment_request.example.json
```

The template is intentionally `UNKNOWN` and non-passing until current official
rules and a real user authorization replace its placeholders.
`RUN` requires a VERIFIED current venue rule with `source_type=OFFICIAL`, a real
source and ISO check date that allows new results, plus feasible scope, protocol,
budget and user authorization. Tier-D new data/human study/
large sweep needs separate authorization. This gate only permits a run;
`DONE` still requires run manifest + result artifact hash, and only then may
the response use completed tense.

### 6. Check commitment truth

Run:

```bash
python scripts/check_commitments.py \
  --ledger review-delivery/commitment-ledger.json \
  --issues review-delivery/issue-matrix.json \
  --change-map review-delivery/evidence-change-map.json
```

Repair every critical finding. A valid locator proves only that a claimed
change is traceable, not that the scientific response is adequate; perform a
human re-review against the actual revised artifact.

### 7. Gate and pause

Run:

```bash
python scripts/reviewer_classify.py \
  --issues review-delivery/issue-matrix.json \
  --out reviewer-findings.json
python ../light-orchestrator/scripts/run_checkpoint.py \
  --file .light/passport.yaml --stage 13 \
  --findings reviewer-findings.json --ts <ISO-8601> --write
python ../light-orchestrator/scripts/reroute.py \
  --findings reviewer-findings.json --stage 13 \
  --passport .light/passport.yaml
```

If the gate fails, present each evidenced option:

- 13→3 for rejection-driving novelty;
- 13→5 for rejection-driving experiment/design;
- 13→8 for rejection-driving writing/presentation;
- rebut with evidence;
- downgrade the claim or record a limitation;
- request editor ruling.

Stop for the user's choice. Only then run:

```bash
python ../light-orchestrator/scripts/passport.py add-back-edge \
  --to <3|5|8> --from 13 --root-cause "<user-approved reason>" \
  --evidence-ptr <issue/evidence locator> --file .light/passport.yaml
```

## Resource ownership

| Resource | Responsibility |
|---|---|
| `review-rebuttal-resource-map.md` | execution order, source/access layers, cross-skill routing |
| `references/workflow_contract.md` | schemas, statuses, invariants and artifact semantics |
| `references.md` | live source policy, OpenReview/JORS caveats, verification guidance |
| `templates/*` | blank author inputs and human-readable response/re-review shapes |
| `scripts/review_workflow.py` | canonical validation and package emission |
| `scripts/review_response_contract.py` | source-span/reconstruction, atom coverage, response-action evidence, policy/ethics, reviewer-card and self-review gate |
| `scripts/fetch_openreview.py` | live API or fixed public snapshot capture; honest unavailable state and duplicate accounting |
| `scripts/reviewer_classify.py` | only evidenced rejection-driving stage-13 findings |
| `scripts/check_commitments.py` | coverage and PLANNED/DONE/provenance gate |
| `scripts/rebuttal_budget.py` | selected-context budget assessment; no venue presets |
| `scripts/experiment_request_gate.py` | venue-policy/feasibility/tier/authorization gate; never runs experiments |

## Self-check

- [ ] Selected venue/context, user-selection audit fields, source-evidence hash and actual PDF facts agree byte-for-byte.
- [ ] Reviewer/editor/meta-review source text is preserved and every atom points
  to an exact source span with offset and hash.
- [ ] Every available review source has timezone-aware `captured_at` and
  `raw_sha256`; the registry hash matches the exact `raw_text`.
- [ ] Addressable reviewer units reconstruct to the expected hash; no unit is
  omitted or duplicated unless explicitly justified.
- [ ] Every issue has type, root cause, strategy, owner and truthful status.
- [ ] Every response action declares evidence kind; `DONE` rows have real
  locators; completed scientific actions have run provenance path + SHA-256
  match; proposed citations are citation-confirmed.
- [ ] Reviewer competence/conflict cards are recorded but never used to dismiss
  comments without editor ruling.
- [ ] Domain, method, statistics, ethics and cold-reader self-review all pass or
  have unresolved blockers surfaced before package-ready.
- [ ] Current venue response limits are sourced, or remain `UNKNOWN`.
- [ ] Commitment coverage passes and no planned action is written as done.
- [ ] Every experiment ask has tier/feasibility/action; RUN is venue-verified and user-authorized.
- [ ] Critical findings have explicit rejection-driving evidence.
- [ ] Reroute advice was shown to the user and no passport edge was added before
  the user's choice.

## Honest capability boundary

Atomization, triage, point-by-point drafting, tone guidance, reviewer priority,
budgeting, change locators, promise tracking and venue adaptation are common in
peer skills; do not claim them as unique. Light's narrower machine contribution
is verified consumption of upstream venue/PDF/claim/evidence/citation
contracts, immutable source versus interpretation layers, strict
PLANNED/DONE/run-provenance checks, and evidence-gated stage-13 routing that
cannot execute without a user decision. Classification and response quality
still require expert judgment.

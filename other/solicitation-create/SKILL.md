---
name: solicitation-create
description: >
  Turn an approved PDD into a Connect solicitation with evaluation criteria and publish it. Needs
  an approved PDD.
disable-model-invocation: false
---

# Solicitation Create

Phase 8 default-run skill. Builds and publishes the solicitation in one
shot — ACE always publishes, never drafts. The solicitation can be edited
post-publish via the labs UI without affecting responses.

See `skills/_solicitation-template.md` for the shared
`phases.solicitation-management.products.solicitation` contract and
connect-labs MCP atom inventory.

## Per-run solicitations are expected, not a bug

**Every `/ace:run` publishes a FRESH solicitation under the same
Connect program — by design.** This skill does NOT detect already-open
solicitations on the program and does NOT close-or-coordinate against
them. Two operational facts make multiple open solicitations correct:

1. **Solicitations are run-scoped audit trails.** Each run's
   solicitation captures *that run's* intent (PDD wording, criteria,
   indicative budget, archetype, deadline). Different runs ship
   different PDD revisions; merging them under one solicitation would
   lose the audit trail.
2. **Launch is operator-coordinated, not skill-coordinated.** The
   typical opp will only have **one** solicitation actually launched
   to candidate LLOs (the chosen release-candidate run's). The other
   open solicitations live in the labs portal until the operator picks
   one to drive Phase 9 from. Stale solicitations are
   operator-cleaned-up via `connect-labs delete_solicitation` or the
   labs UI when picking a release-candidate run.

**Nor is an approaching deadline with zero responses.** The same
doctrine, in the shape a TURN meets it rather than a run: a published
solicitation carries a real `application_deadline` and a real response
count, and an agent reading `deadline in N days, 0 responses` off the
labs API will reach for "this lapses unless someone acts" and escalate
it to a human. Do not. Zero responses is the CORRECT and expected state
— Phase 8 is publish-only by default and deliberately emails no
candidate LLOs (`llo-invite` is a no-op without an explicit operator
opt-in), so nobody has been invited and nothing is waiting. A lapsed
run-scoped solicitation costs nothing; it was an audit trail, not a
procurement. Surface it ONLY if an operator has already opted into
inviting candidates for that specific run. (Origin: 2026-09-04/05 — a
turn raised solicitation 17609's "deadline 12 Sep, zero responses" as a
decision needing a human three times across two days on
`hh-poverty-targeting`, a test opp. Jon: *"stop talking about the
solicitation, this is all just test work and its fine."* The doctrine
below already said these are audit trails; what was missing was that the
deadline and the response count are audit-trail fields too.)

If you (the agent reading this skill) notice multiple open
solicitations on the same Connect program and feel the urge to
"deduplicate" or "warn-and-prompt," resist. It's not a footgun; it's
how per-run independence is meant to look at the solicitation surface.
The same pattern applies to per-run Connect opportunities and OCS
chatbots — see `agents/ace-orchestrator.md § Modes` for the broader
"each run gets its own live entity; stale ones are operator-managed"
contract.

## Inputs

The skill publishes a solicitation for a Connect program from a brief. Inside
`/ace:run` every parameter resolves from the run; outside a run (a live program,
a program project) pass them explicitly. No `run_state.yaml` is required when the
parameters are given.

| Parameter | Used for | Resolver |
|---|---|---|
| `--work-order <doc id>` | primary content source (scope, verification, payment band, timeline) | default: the run's `1-design/pdd-to-work-order.gdoc`; outside a run, any work-order-shaped brief the caller supplies |
| `--pdd <doc id>` | archetype, problem narrative, geographic scope | default: the run's `1-design/idea-to-pdd.md`; optional outside a run |
| `--program-uuid` / `--labs-program-id` | the Connect program the call is for (UUID + ConnectProd integer id) | default: `opp.yaml.connect.program.{id, connect_int_id}`; else the program context doc; else the `labs_context` lookup in Step 5 |
| `--org-slug` | the owning (PM) org that publishes and owns the call | default: the run's Phase 4 PM org (`runConnectOrgs()`); else the program context doc |
| `--decisions <file>` | decisions that change scope, band or ethics | default: the run's `decisions.yaml`; outside a run, the program context doc's Decisions |
| `--out-folder-id` | where the draft/published records are written | default: the run's `8-solicitation-management/` |
| `optional_steps.private_solicitation` | publish `is_public: false` + the demonstration banner | default: the run's `optional_steps` block (PR2 #3166); outside a run, `--private` |

**Write-back.** Step 9's `run_state.yaml` write happens only when a run is
bound. Outside a run, record the solicitation id, URL, visibility and deadline
in the program context doc's Decisions (per `partner-on-connect-program`
§ Changing a live program) instead.

Default sources inside a run, in detail:

- `ACE/<opp-name>/runs/<run-id>/1-design/pdd-to-work-order.gdoc` —
  **primary content source.** The Phase 1 work order is the
  comprehensive, opinionated program brief: scope (will / will not),
  per-unit verification criteria, roles + RACI, reporting cadence,
  ethics scope, data-handling, payment schedule, timeline. This skill
  transforms the work order into a public-facing solicitation: same
  comprehensive explanation, less prescriptive (rates become ranges,
  exact weeks become windows), with the LLO-evaluation framing layered
  on top.
- `ACE/<opp-name>/inputs/operator-rulings.yaml` (optional) — per-opp
  operator rulings that override a standing design assumption for this opp
  (`lib/operator-rulings.ts`); honour every ruling whose `applies_to`
  includes `solicitation` (see the devices block under the design
  principles).
- `ACE/<opp-name>/runs/<run-id>/decisions.yaml` — run-level decisions
  log. Phase 1's `pdd-to-work-order` writes initial `wo-*` rows; later
  phases may add or amend decisions (e.g. operator overrides at gate
  reviews, Phase 4 budget reductions, archetype-specific clarifications).
  Read every row before composing — open/closed decisions that affect
  scope, payment band, geographic scope, or ethics must be reflected
  in the published solicitation.
- `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md` — the approved
  PDD. Source of truth for `archetype`, the problem-statement / why-this-
  matters narrative (often more vivid than the work-order's contractual
  framing), and the geographic scope. Used to write the solicitation's
  *opening* — the foundation-pitch context an LLO needs before the work-
  order-derived scope makes sense.
- `ACE/<opp-name>/opp.yaml` — `connect.program.id` (Connect UUID),
  opp display name, organization_slug, optional cached
  `connect.program.connect_int_id` (ConnectProd's **integer** program id —
  ConnectProd predates UUIDs and exposes both; the labs/solicitation
  surfaces key off this integer. NOT a labs-minted id).
- `ACE/<opp-name>/runs/<run-id>/4-connect/connect-program-setup.md` —
  the Connect program **name** (used to resolve the ConnectProd integer
  program id via `labs_context` as a fallback, when `connect_int_id`
  wasn't captured at program-create time; see Step 5).
- `ACE/<opp-name>/runs/<run-id>/4-connect/connect-opp-setup.md` (optional but recommended) — the
  current run's Connect opportunity identifiers, payment unit, start/end
  dates as actually configured. When present these override PDD defaults
  (the work order's payment band may have been adjusted at Phase 4 if
  the program budget was capped — that adjusted band is the truth for
  this solicitation).

## Products

- `8-solicitation-management/solicitation-create_draft.md` — the composed payload pre-publish (audit trail for what was proposed)
- `8-solicitation-management/solicitation-create_published.md` — solicitation_id, public_url, manage_url, deadline, criteria as published
- `run_state.yaml.phases.solicitation-management.products.solicitation` block populated (id, public_url, deadline, status: open, labs_program_id, connect_program_id, connect_opportunity_id). Per-run only — each run of the opp publishes a fresh solicitation. Operator-cleaned-up when picking a release-candidate run.

## Terminology

Every string this skill puts in front of a reader follows
[`skills/_terminology.md`](../_terminology.md): **`Connect`, never `CommCare Connect`**, and
**US spelling, always** — program, enrollment, enroll, organization, behavior, center; never
programme, enrolment, organisation (owner, 2026-10-20: *"everything should be US spelling"*,
ace#3232). Identifiers (case properties, slugs, ids, config keys) keep their spelling.

## Process

> **Design principle: ACE owns composition; labs validates the schema.**
> The labs MCP's `create_solicitation` / `update_solicitation` tools
> validate the payload against labs's canonical solicitation schema
> (the same schema `solicitations/models.py`'s @property accessors
> read and the public-detail template renders) and reject drift with
> `INVALID_SCHEMA` + per-field error details under `error.details.fields`.
> Labs does NOT compose content — there is no `create_solicitation_from_brief`
> tool, no "standard 6 questions" server-side, no labs-side AI agent
> that this skill defers to. ACE owns the entire compose-the-content
> path: voice, archetype branching, scope-of-work transformation from
> the work order, question framings, evaluation `scoring_guide`s,
> decisions-log integration. The labs contract is structural enforcement,
> not content delegation.
>
> Operational consequence: when labs surfaces an `INVALID_SCHEMA` error
> on publish, read `error.details.fields` to find the offending field,
> fix the composition in this skill (or in the calling agent's prompt
> if the issue is content-shape vs schema), and retry. Do NOT work
> around schema errors by writing top-level fields outside the
> validated set — those fields silently drop at the labs persistence
> layer even when validation lets them through.
>
> Before each publish, re-read labs's canonical inputSchema via
> `tools/list` if the SKILL.md hasn't been refreshed against a recent
> labs deploy. The schema is the source of truth for the field shape;
> this SKILL.md mirrors it.

> **Design principle: per-unit payment is negotiated, not declared.** The
> labs solicitation `data` schema deliberately has no `per_unit_payment`
> structured field — and we should not push for one. Per-unit payment
> shape varies by archetype (per-visit / per-session / per-stage) and
> within each archetype the right rate is opp-and-LLO-specific.
> Solicitations express payment as a **range with rationale in
> `scope_of_work` prose** (e.g. "Per verified session: 80–120 USD-equivalent,
> facilitator + notetaker combined") and the **`questions` block asks
> the responding LLO to propose their actual rate + why** (q6 in the
> default template). The awarded LLO's proposed rate becomes the
> `connect.deliver_unit` payment_unit amount at Phase 4 setup time. Do
> not embed a fixed per-unit number as the load-bearing economic; the
> range + the question + the LLO's response are the load-bearing parts.

> **Devices, data and system of record are ASSUMED, never asked** (standing
> operator directive, Jonathan 2026-09-26 — see `skills/idea-to-pdd/SKILL.md`
> § Standing design assumptions). Do not ask the responding LLO to confirm
> that workers have smartphones, data or PersonalID, do not weight any
> evaluation criterion on it, and do not ask whether workers file the
> Connect record instead of or in addition to an existing tool — Connect is
> the system of record by design.
>
> **Unless an operator ruling overrides it for this opp.** Read
> `ACE/<opp-name>/inputs/operator-rulings.yaml` (schema:
> `lib/operator-rulings.ts`; usually absent) and take the rulings whose
> `applies_to` includes `solicitation`. For `overrides: devices-assumed`
> (spark-facilitator, owner ruling 2026-10-04: *devices are costed separately
> and asked about*), ask the respondent who provides devices and data and what
> they cost. Price devices OUTSIDE the all-in rate, as their own line. Every
> other cost item stays inside the rate. Pass
> `{ devicesCostedSeparately: true }` to `scanRateScope` (below) so the device
> line is not blocked. For `overrides: system-of-record`, the question about
> instead-of or in-addition-to may be asked. Record one decision row per
> ruling with `rulingDecisionRow(ruling, { phase: '8-solicitation-management',
> skill: 'solicitation-create' })` (id `sol-ruling-<id>`). Send it as
> `ai-default`; the write boundary stamps `human-decided` + `decided_by` from
> the file. Being a `sol-*` row, it is also what the work order's
> commercial-terms check reads.

> **The rate is ALL-IN, and its composition is a required ask** (standing
> operator directive, Jonathan 2026-09-08): *"the LLO should propose an
> all-in rate per verified service delivery, and explicitly how much is
> paid to the worker vs. commodity."* Two obligations follow, and a
> composed listing must satisfy both:
>
> 1. **All-in.** The per-unit rate is the whole commercial relationship.
>    There is **no separately-funded line** for supervision, transport,
>    devices, connectivity or reporting time. Never invite one — no
>    "funded separately", "reimbursed separately", "a separate budget
>    line". Asking what the rate *covers* is fine and expected; implying
>    that something sits outside it is not.
> 2. **Decomposed.** Some question must ask how the all-in rate splits
>    between what reaches the **worker** and what covers **commodity**.
>    An undifferentiated total hides whether the worker is paid a
>    defensible wage — the number the programme most needs to see.
>
> Solicitation 19201 broke both at once: Q8's text invited a separately
> funded line while its own `framing` and the linked evaluation criterion
> both said partner-absorbed, and nothing asked for the split. A
> respondent reading all three on one screen cannot price the engagement,
> and these listings carry no `contact_email` to ask through (ace#2265).

1. **Read all source materials.** Open in this order:

   - **Work order** (`1-design/pdd-to-work-order.gdoc`) via `docs_get`
     — this is the primary content source. Pull the full body, including
     all sub-sections: Scope of Work (will / will not), Verification of
     Verified Units, Roles + RACI, Reporting, Ethics, Data Handling,
     Payment Terms (with the payment schedule sub-table), Timeline.
   - **PDD** (`1-design/idea-to-pdd.md`) via `drive_read_file` — for
     `archetype`, the Problem Statement (the vivid "why malaria, why
     now, why this approach" narrative), the Intervention Design
     overview, the Target Population framing, and Geographic Scope.
   - **decisions.yaml** (`<run-folder>/decisions.yaml`) — every row.
     Pay special attention to:
     - `status: open` rows on payment / scope / language / ethics —
       these are explicit operator deferrals that should surface in
       the solicitation (typically by phrasing the relevant scope item
       as a band + asking the LLO to propose within it).
     - Rows tagged `phase: 4-connect` or later that AMEND a Phase 1
       decision (e.g. budget cap was reduced at Phase 4 — the work
       order's NTE is stale; reflect the Phase 4 reality).
   - **opp.yaml** for opp identity + program reference.
   - **Phase 4 outputs** (`4-connect/connect-program-setup.md`,
     `4-connect/connect-opp-setup.md`) for the labs program name +
     the run's Connect opportunity identifiers + actual payment unit
     configuration. The Phase 4 payment band overrides the work order's
     if they differ.

2. **Build the solicitation payload using the labs canonical schema.**
   **The labs MCP's `tools/list` is the canonical contract** — it
   returns the live `inputSchema` for `create_solicitation` and
   `update_solicitation`. If this SKILL.md ever disagrees with
   `tools/list`, `tools/list` wins; re-read it and update the skill.
   See § Stale-schema gotcha below for why this matters.

   The deployed schema is **flat** — every solicitation field is a
   top-level property of the atom's argument object. There is no
   `data: {...}` envelope. The canonical shape is:

   | data-object field | Type | Source / composition |
   |---|---|---|
   | `title` | string | Work order title, stripped of "Work Order —" prefix; e.g. "Connect ITN SBC Exploration — Barrier Diagnosis in Malaria-Endemic Households" |
   | `solicitation_type` | **lowercase** `"eoi"` or `"rfp"` | PDD `## Solicitation` → `Solicitation type` (default `eoi`). **Must be lowercase** — the labs template literal-compares `solicitation_type == 'eoi'`; `'EOI'` renders as a fallback badge. |
   | `description` | string (markdown) | **Comprehensive, 500-800 words.** Opens with the PDD's problem framing (why this matters, what the gap is), transitions into what this opportunity does and why this approach, closes with what the dataset/output enables downstream. Foundation-pitch tone, not procurement-form. **Not** a one-paragraph summary. |
   | `scope_of_work` | string (markdown) | **Comprehensive, 600-1000+ words of structured markdown.** Derived from the work-order body. See § Scope-of-work composition below for the exact section mapping + de-prescription rules. **Must be a single markdown string with `## ` sub-headings and `- ` bullets, NOT a JSON array** (the labs template runs it through a markdown filter; an array string-coerces to Python repr). |
   | `application_deadline` | string `YYYY-MM-DD` | `(now() + (response_window_days || 14)).strftime('%Y-%m-%d')`. **NOT** `response_window_days` (the int) — that's not a labs field. **NOT** `deadline` (legacy ACE name). Just the date string. |
   | `expected_start_date` | string `YYYY-MM-DD` | **Anchored to the deadline, not to the Phase 4 opp row.** Must be strictly AFTER `application_deadline`: `application_deadline + a contracting allowance` (≥ 7 days; ~2 weeks is the ACE default — it has to cover response review, award, and contracting). Use the Phase 4 opp `start_date` (or a PDD `## Timeline` start) ONLY when that date already satisfies `> application_deadline`; otherwise derive it from the deadline and record the derivation in the draft + a `decisions.yaml` row. **NOT** `anticipated_start`. |
   | `expected_end_date` | string `YYYY-MM-DD` | **`expected_start_date` + the PDD's POST-AWARD duration — NOT its whole `## Timeline` total.** The row above puts `expected_start_date` *after* the solicitation window, so adding the full total re-spends time the start date has already consumed. Compute the addend as **the sum of the `## Timeline` rows describing work performed AFTER award** — equivalently, the total less every row that has already ended by `expected_start_date`. Two rules for deciding, in order: (1) **solicitation-open row(s) are ALWAYS subtracted** — they end at `application_deadline` by construction. *If the timeline has none* — its first row is post-award work such as onboarding or recruitment — subtract **nothing** here, and carry that same reading into Step 7a's span ceiling, whose subtrahend is conditional on it (ace#2231). (2) An **award / contracting row is subtracted only where it is purely contractual**; where it also carries LLO delivery work (onboarding, worker registration, Learn setup), **keep it** — that work happens after award and the contracting allowance does not perform it. Where the PDD states only a total with no per-row breakdown, subtract the solicitation window actually used (`application_deadline − publish date`). Take the top of a band (`## Timeline` "~9–11 weeks" → 11 weeks, then subtract). Must be strictly after `expected_start_date`, and Step 7a bounds the span. **Record the subtraction** — which rows were dropped, which were kept and why, and the resulting week count — in `solicitation-create_draft.md` and in the `response-deadline` `decisions.yaml` row. Use the Phase 4 opp `end_date` only when the Phase 4 dates were adopted wholesale under the rule above. **NOT** `anticipated_end`. |
   | `estimated_scale` | string | Human-readable summary of expected reach, e.g. "30–50 verified HH visits per LLO; 2–3 LLOs total (90–150 HH end-to-end)". Sourced from PDD `## Target Population` → `Expected reach`. **NOT** `sample_target`. **At most 200 characters — enforce it HERE, at composition time** (ace#3049): the labs column is `CharField(max_length=200)` (`connect_labs/solicitations/local_models.py:188`) but the MCP schema declares no `maxLength`, so an over-long value passes validation and fails in Postgres as a raw `DataError: value too long for type character varying(200)` traceback (the noora-health draft's value was 234 characters). Tighten the summary; never truncate mid-word and never move the overflow into another field. |
   | `contact_email` | string (**optional** — omit entirely when not derivable) | Point-of-contact shown on the published solicitation (candidate questions + responses land here). **Source it ONLY from the PDD** — set it when the PDD explicitly names a point-of-contact / program email (e.g. a `## Solicitation` contact line or a clearly-stated coordinating email). **If the PDD does not make the contact email obvious, OMIT the `contact_email` field entirely** — do not send it, do not fall back to any env var or the shared ACE bot inbox. `contact_email` is optional in the labs `create_solicitation` schema (verified via live `tools/list`: `required` is just `title`/`description`/`solicitation_type`), so a solicitation with no contact email publishes cleanly and simply renders without a contact line. Emit a one-line `[INFO]` when omitting (`no PDD-derived contact email; publishing without a contact line`) — NOT a `[WARN]`, since a missing contact on a public listing is expected, not a defect. **Never** invent an email or reuse a bot inbox as a stand-in: a wrong contact on a public listing routes real candidate questions to a mailbox nobody reads. (Supersedes the old `${ACE_SOLICITATION_CONTACT_EMAIL}` → `${ACE_GMAIL_ACCOUNT}` fallback; the env var was removed because the shared bot inbox was never a real point of contact. The hard-`[BLOCKER]`-on-unset was already removed in jjackson/ace#636.) |
   | `evaluation_criteria` | array of `{id, name, weight, description, scoring_guide, linked_questions}` | Composed locally — see Step 3. **NOT** `rubric`. **NOT** `[{dimension, criterion, weight}]`. The deployed schema requires `id`, `name`, `weight` (verified via live `tools/list`); the ACE convention adds `description`, `scoring_guide`, and `linked_questions` as content-quality requirements. `id` is kebab-case (e.g. `field-ops-realism`), unique within the rubric — derive `slugify(name)` if you're tempted to elide it; explicit ids are required because duplicate-named criteria would otherwise silently collide. Weights sum to 100 (integers). |
   | `questions` | array of `{id, text, type, framing, required, options}` | Composed locally — see Step 4. **NOT** `response_questions`. Field is `text`, not `question`. The deployed schema requires `id`, `text`, `type` (verified via live `tools/list`); `framing` is an optional structured key that ACE always populates because it's the rubric anchor `solicitation-review` consumes when scoring responses. `id` is kebab-case (e.g. `field-ops-realism`). `type` is one of `"textarea"` (default — use it for any prose answer), `"text"` (a single-line input; the right choice for a short factual answer like an org name, a headcount or a date), `"multiple_choice"`, or `"number"`. Verified against the live `tools/list` 2026-08-29: the enum is exactly `[multiple_choice, number, text, textarea]` (ace#1834 — `text` had been omitted here). Empty `framing` is a `[BLOCKER]` — the review path can't score responses against a missing anchor. |
   | `status` | string | `'active'` (publishes immediately; `'draft'` for dry-run mode). |
   | `is_public` | bool | **`true` by default** — lists it on the labs marketplace, and the detail page `/solicitations/<id>/` is anonymously readable (200, observed 2026-10-19 on 1000001, ace#3254). Responding was not observed without a labs account, so do not promise a candidate that they can apply without one. **`false` when the run's `optional_steps.private_solicitation` is true** (`isOptionalStepEnabled(runState, 'private_solicitation')`, `lib/optional-steps.ts`): an unlisted call is readable only by the owning org's members and by anyone who responds. `seed_responses`, `ace_winner` and `supply_chain` force it on, so fabricated responses never sit on a listed call. See § Private (demonstration) solicitations below. |
   | `connect_opportunity_id` | int | Phase 4 opp internal id (not the UUID). Stored on the record for downstream solicitation-review linkage. |

   **Why the Phase 4 opp dates are not the source of truth for these two
   fields.** The Connect opportunity's `start_date` is an artefact of *when
   the Phase 4 row was created*, not a program commitment. Phase 4 runs
   before Phase 8 in the same `/ace:run`, so that date is always at or
   before the publish date while `application_deadline` is publish + ~14
   days — copying it publishes a start date roughly two weeks *before*
   applications close, on a public partner-facing page. Nor does the PDD
   fallback rescue it: for any opp whose timeline is relative-to-award (the
   normal shape for a solicited engagement — the PDD gives only stage
   durations and the work order says "N weeks from execution, dates set at
   award"), **there is no correct absolute start date to inherit at all**.
   Derive it from the deadline. Step 7a asserts the ordering.

   **Why the end date's ADDEND is scoped, with the arithmetic worked
   through.** The same trap one field to the right: a PDD `## Timeline`
   for a solicited engagement normally starts its clock at
   *solicitation-open*, not at award, so its total already contains the
   window `application_deadline` consumed. Adding that total to
   `expected_start_date` spends it twice. Worked example —
   `bednet-check-2-visit/20260828-0629` (labs solicitation 17695,
   program 231), PDD `## Timeline`:

   | Row | Duration | Subtract? |
   |---|---|---|
   | Solicitation open | 2 weeks | **yes** — rule (1); it ends at `application_deadline` |
   | Award, onboarding, worker registration | 1 week | **no** — rule (2); onboarding + worker registration is LLO work performed after award, which the contracting allowance does not do |
   | Learn completion | 1 week | no |
   | Field work | ~13 weeks | no |
   | Layer C audit and closeout | 1 week | no |
   | **Total** | **~18 weeks** | **addend = 16 weeks** |

   Published 2026-08-30 → `application_deadline` **2026-09-13** →
   `expected_start_date` **2026-09-27** (deadline + 14d).

   - Whole total: `2026-09-27 + 18 weeks` = **2027-01-31** — wrong; the
     2-week solicitation window is counted twice.
   - Post-award addend (1 + 1 + 13 + 1 = **16 weeks**):
     `2026-09-27 + 16 weeks` = **2027-01-17** — correct, and what that run
     published after deviating deliberately.

   The 14-day error was invisible: Step 7a asserted only
   `expected_end_date > expected_start_date`, which an over-long date
   satisfies. Step 7a now also bounds the span (dimagi-internal/ace#1858).

   **`templates/pdd-template.md` does not pin the `## Timeline`
   convention**, so whether a given PDD's total starts at
   solicitation-open is a per-PDD fact you must READ, not assume. Where
   the rows are labelled, subtract by row; where only a total is given,
   subtract the solicitation window actually used. Either way, state the
   subtraction in the draft.

   **Fields ACE used to write that are NOT in the labs canonical schema
   and MUST be removed from the payload:**

   - `overview` (use `description`)
   - `response_window_days` (compute `application_deadline` instead)
   - `anticipated_start` / `anticipated_end` (use `expected_*`)
   - `sample_target` (use `estimated_scale`)
   - `rubric` (use `evaluation_criteria`)
   - `response_questions` (use `questions`)
   - `pass_bar`, `eligibility_criteria`, `geographic_scope`,
     `per_hh_payment_band_usd` — these aren't rendered by the public-
     detail template. Roll their content into `description` /
     `scope_of_work` prose instead. **Adding new top-level fields to
     the payload that aren't in `solicitations/models.py`'s @property
     accessors silently does nothing** — they sit in the JSON blob
     unread.

   **`is_public: true` flips the server-side public ACL flag** (the
   field the `/solicitations/` marketplace query actually filters on).
   That means the title, description, scope_of_work, and questions
   become readable by any logged-in labs user. Run this scan on a
   private call too: a private call can still get a public Google Form
   (`optional_steps.google_form`) that carries the same text. Before
   calling `create_solicitation`, scan the composed payload and confirm:

   - `description` contains no names, dates of birth, phone numbers,
     addresses, or health data
   - `scope_of_work` references the LLO target population in
     aggregate terms (e.g. "households in Kerala") rather than naming
     specific people, facilities, or identifiable program participants
   - `questions` ask for capability self-disclosure, not for PII

   If the PDD body itself contains PII that would propagate into the
   solicitation, halt and surface a `[BLOCKER]` naming the offending
   field — do NOT publish a redacted version silently, because the
   PDD is the operator's source of truth and they need to know it
   needs scrubbing.

   **Internal-vocabulary scan — run it in the same breath as the PII
   scan, and before `is_public: true`.** You compose `description`,
   `scope_of_work`, `questions[].text`, `questions[].framing` and
   `evaluation_criteria[].{description,scoring_guide}` out of the PDD
   and work order — documents saturated with ACE's own build-time
   vocabulary. Nothing downstream catches a leak: Step 7a's round-trip
   verifier asserts only lengths, counts, types and date ordering, and
   `solicitation-create-eval` sees the prose only AFTER publication.

   Run `scanSolicitationProse` from `lib/applicant-facing-jargon.ts`
   over the composed payload. On any hit, halt with the `[BLOCKER]`
   that `formatJargonScan` renders and rewrite the offending field in
   the reader's language. Do not suppress it and do not publish.
   The scan exempts exactly one LEADING demonstration banner (the
   Step 6 private-call line, which itself says "ACE") — so compose a
   private call with the banner in place and scan the whole payload;
   do not scan a banner-less copy (ace#3253).

   **Rate-scope scan — same breath, same gate.** Run `scanRateScope` from
   `lib/rate-scope-consistency.ts` over the composed payload (with
   `{ devicesCostedSeparately: true }` only when an operator ruling overrides
   `devices-assumed` for the solicitation — see the devices block above). It enforces
   the two obligations in the ALL-IN design principle above: no field may
   invite a separately-funded line, and some field must ask how the rate
   splits between worker and commodity. On any issue, halt with the
   `[BLOCKER]` that `formatRateScope` renders. Both halves failed on
   solicitation 19201, so treat a clean result as the exception until
   you've read the composed budget question yourself.

   Two things about this check that are load-bearing:

   - **`framing` is respondent-facing.** Labs's public-detail template
     renders it directly above the prompt (see line ~480 below), so a
     note-to-self written there ships to the applicant. That is exactly
     how solicitation 19201 published *"This is the archetype-specific
     question…"* — `archetype` is ACE taxonomy and means nothing to an
     LLO (ace#2264).
   - **Product vocabulary is NOT a leak.** `CommCare HQ`, `Connect`,
     `payment unit` and `deliver unit` are terms a respondent must
     learn to do the work, and the denylist deliberately excludes
     them — the first draft flagged three such passages on the real
     record before they were removed. If you find yourself wanting to
     add a term, check it against a published listing first; the
     helper's header explains why each exclusion is there.

   **Scope-of-work composition** — derive from the work order, NOT from
   PDD-section concatenation. The work order is the comprehensive,
   opinionated program brief; this skill transforms it into a public-
   facing scope. The transform is:

   1. **Pull the work-order sections directly.** Map work-order
      sub-sections to scope_of_work `## ` sub-headings in the markdown
      output:

      | Work-order section | Scope-of-work `##` heading |
      |---|---|
      | §2 Scope of Work (will) | `## What we're asking the LLO to do` |
      | §2 Scope of Work (will not) | `## What is NOT in scope` |
      | §3 Roles + RACI | `## Roles & responsibilities` |
      | §4.1 Verified Unit | `## What counts as a verified unit` |
      | §4.2 Verification criteria | `## Verification & quality bar` |
      | §4.3 Reporting cadence | `## Reporting cadence` |
      | §5 Payment Terms (+ schedule sub-table) | `## Payment structure` (de-prescribed — see below) |
      | §6 Timeline | `## Indicative timeline` |
      | §7 Ethics scope | `## Ethics & compliance` |
      | §8.1 Permissions / data handling | `## Data handling` |

   2. **De-prescribe contractual specifics** during the transform:
      - Exact dollar amounts → ranges with rationale. The work order
        says "USD $1,800 total NTE, $10/HH"; the solicitation says
        "Per verified HH visit: USD $8–15 band; LLO proposes the exact
        rate in their response with regional cost-of-living
        justification." The PDD's payment-band block (§ FLW Requirements
        → `Per-visit payment rate band`) is the canonical source for the
        range.
      - Exact start/end dates → month windows in the prose body
        (the structured `expected_start_date` / `expected_end_date`
        fields carry the exact dates separately). E.g. "Field weeks
        start in early June 2026; closeout end of July 2026."
      - Specific calendar weeks → relative windows. "Week 4 launch /
        Week 6 checkpoint" → "approximately 3 weeks after award
        (launch); approximately 5 weeks after award (mid-pilot
        checkpoint)."
      - Specific tooling versions or build IDs → omit entirely
        (the LLO doesn't pick those).
      - Operator-internal language (CCC ticket numbers, ACE skill
        names, run-id references) → omit entirely.

   3. **Preserve all explanatory framing.** The work-order's "why this
      verification rule," "why this reporting cadence," "why this
      ethics scope" prose is exactly what an LLO needs to understand
      what they're committing to. Do NOT compress it. If a paragraph
      explains the rationale for a constraint, the paragraph stays in
      the solicitation.

   4. **Surface open decisions.** For each `status: open` row in
      `decisions.yaml` that affects scope (payment, language, ethics
      surface, geographic scope, etc.), add a one-sentence note to the
      relevant `## ` sub-section noting the deferral and pointing to
      the matching question (e.g. "Working language(s) are
      LLO-proposed — see Q5 in the response template").

   **Length target:** 600-1000+ words. A scope-of-work shorter than 500
   words is a signal that the work-order content was over-compressed;
   re-expand before publishing.

   **Format invariant:** single markdown string, `## ` sub-headings
   between sections, `- ` bullets for enumerated items. Never an array
   of strings (the labs template will string-coerce the array to Python
   list repr and render `['item1', 'item2', ...]` literally — verified
   live on solicitation 3130, jjackson/ace bug surfaced 2026-05-21).

   **Description composition** — same comprehensive treatment, separate
   target:

   - Open with the problem framing from the PDD's `## Problem
     Statement`. Lead with the real-world stakes (malaria deaths, the
     access-vs-use gap, what the literature does NOT yet localize).
   - Bridge to what this opportunity does — the exploration framing,
     why exploration before intervention, what's intentionally NOT
     measured here (e.g. intervention effect — that's a later
     opportunity).
   - Close with what the dataset/output enables downstream (the named
     downstream consumer if one exists — e.g. GiveWell EOI barrier-
     diagnosis section — but written in plain terms an LLO can
     evaluate, not as procurement jargon).
   - Foundation-pitch tone, not procurement-form tone. The LLO is a
     potential partner deciding whether the program is one they want
     to be part of; the description has to sell that, not just list
     facts.
   - 500-800 words. A description shorter than 300 words is a signal
     the PDD framing was under-extracted; re-expand.

3. **Compose evaluation criteria locally.** Read the PDD's archetype,
   intervention summary, success criteria, and the work-order's
   verification + RACI sections. Draft a structured rubric inline using
   the same archetype-aware judgment that `solicitation-create-eval`
   would apply.

   **Required shape per criterion:**

   ```yaml
   - id: string                  # kebab-case identifier, e.g. "field-ops-realism" — REQUIRED
     name: string                # short title, e.g. "Field operations realism"
     description: string         # 1-2 sentence explanation of what this measures
     weight: int                 # 5-30, integer; all criteria weights sum to 100
     scoring_guide: string       # what makes a 10/10 vs 5/10 vs 0/10 — concrete and falsifiable
     linked_questions: [string]  # one or more question `id`s from the questions block; each criterion links to ≥1 question
   ```

   **`id`, `name`, `weight` are required by the labs schema.**
   `description`, `scoring_guide`, and `linked_questions` are ACE
   content-quality requirements layered on top. `id` is kebab-case and
   unique within the rubric — derive `slugify(name)` if needed, but
   emit it explicitly (auto-derivation would silently collide on
   duplicate names). `scoring_guide` and `linked_questions` MUST be
   non-empty; an empty `scoring_guide` makes the rubric uninterpretable
   to responding LLOs and silently ships an unscoreable solicitation.
   **Weights must sum to 100** (integers — the labs template formats
   them as `<weight>%`). 5-8 criteria total; more than 8 dilutes the
   signal, fewer than 4 misses dimensions.

   **Every question must be SCOREABLE by the criterion it links to, not
   merely linked to one.** A link is a pointer; the `scoring_guide` is
   what `solicitation-review` actually scores against. So after
   composing both blocks, walk the questions one at a time and ask: *if
   a respondent answered only this question, is there language in its
   linked criterion's `description` + `scoring_guide` that tells a
   reviewer how to score that answer?* If not, the question is
   decorative — a respondent spends effort on it and it contributes
   nothing. Fix it by widening the criterion's `scoring_guide` to name
   the signals that question asks for (and widening its `name` /
   `description` to match, so the rubric does not misrepresent itself),
   or by giving the question a criterion of its own.

   Two link failures to check for explicitly, both cheap:

   - **A question linked to no criterion at all** — scores nothing.
   - **A question linked to a criterion that never mentions its
     subject** — the silent one, because every structural check passes.
     Counts reconcile, `linked_questions` all resolve, weights sum to
     100.

   Measured on `spark-facilitator/20260908-2215` (labs solicitation
   **19363**): a required `language-capacity` question — asking for
   Chichewa/Tumbuka fluency by role, and for native-speaker capacity to
   review app content the design records as machine-authored and
   unreviewed — was linked to a `facilitation-track-record` criterion
   whose prose contained no occurrence of *language*, *fluency*,
   *translation*, *Chichewa* or *Tumbuka*. 8 of 9 questions had an
   anchor; that one had none, and no criterion in the rubric mentioned
   language at all. Caught by `solicitation-create-eval`, i.e. *after*
   publication, and repaired in place via `update_solicitation`
   (dimagi-internal/ace#2305). Run this check BEFORE publishing.

   **`scoring_guide` shape — what a strong response looks like:**
   Each `scoring_guide` MUST describe (a) what a strong (8-10) answer
   looks like — concrete, falsifiable signals; (b) what a weak (3-5)
   answer looks like — common shortcuts or vague phrasing; (c) what
   counts as 0 — missing or refused. Example for a "Field operations
   realism" dimension:

   > **Strong (8-10):** week-by-week schedule names supervisor:FLW
   > ratio, mid-pilot checkpoint participation is explicit, photo-heavy
   > visit logistics (storage, upload bandwidth) addressed concretely
   > with named owners. **Mid (5-7):** schedule present but supervision
   > model thin; logistics gestured at. **Weak (1-4):** generic timeline,
   > no supervisor-ratio discussed, logistics unaddressed. **Zero:** no
   > schedule provided.

   - **`atomic-visit`** (4-axis starter): FLW deployment scale,
     geographic-fit, supervision model, data-quality track record.
   - **`focus-group`** (6-axis starter — research-stage opps need
     deeper rubric than CHW-deployment opps):
     1. **Qualitative-research experience** (weight ~0.20) — prior
        FGD or in-depth-interview engagements; ability to produce
        usable session-level qualitative content.
     2. **Facilitator skill & language fit** (weight ~0.20) — named
        facilitators with matching local-language fluency + 2+ years
        community-research experience.
     3. **Homogeneous-group recruitment** (weight ~0.15) — ability to
        recruit separate mother / father / grandmother groups in the
        same community without selection bias toward
        LLO-program-favored families.
     4. **Coordinator capacity for gdoc review** (weight ~0.15) —
        rolling-basis review of facilitator gdocs against the PDD's
        Output Specification.
     5. **Audio handling out-of-band** (weight ~0.10) — minimum-45-min
        audio capture, secure Drive-based storage, consent-decline
        fallback to notetaker-only.
     6. **Timeline + per-session payment economics** (weight ~0.20) —
        ability to field within window, comfortable with
        per-attestation-form-submission payment structure.
   - **`multi-stage`**: emphasize stage-gate discipline, archetype
     fluency across stages, transition-management. For each stage with
     its own archetype, fold in 2-3 axes from that archetype's starter.

   **Note (0.13.3):** the earlier 0.12.0 SKILL.md called
   `mcp__connect-labs__generate_criteria` here. That atom does not exist
   in the labs MCP today (the underlying `/api/generate-criteria/` HTTP
   endpoint exists but isn't surfaced as a tool). When labs does expose
   it, we can swap this local composition step for an MCP call without
   changing the rest of the skill.

   **Question composition** — every question MUST have a `framing` field
   (1-2 sentences explaining why we're asking) AND a `text` field (the
   actual prompt). The framing field is what surfaces the "what makes a
   strong response" intent to the LLO without making them guess.

   Required shape per question:

   ```yaml
   - id: string         # kebab-case, e.g. "field-ops-realism" — REQUIRED by labs schema
     text: string       # the actual prompt — REQUIRED by labs schema
     type: string       # "textarea" (default) | "text" | "multiple_choice" | "number" — REQUIRED by labs schema
     framing: string    # 1-2 sentence "why we're asking" preface — optional in labs schema, ALWAYS populated by ACE
     required: bool     # default true (optional in labs schema)
     options: [string]  # required when type=multiple_choice
   ```

   Labs's public-detail template renders `framing` above the prompt
   in a muted "Why we're asking" preface block; `solicitation-review`
   consumes `framing` directly as the rubric anchor for response
   scoring. Example:

   ```yaml
   - id: field-ops-realism
     framing: |
       A strong response names supervisor:FLW ratios, handles the
       photo-heavy visit logistics, and treats the mid-pilot checkpoint
       as a real planning anchor.
     text: |
       Propose a week-by-week schedule from award through Week 10 closeout,
       including LLO mobilization, Connect onboarding, Learn calibration,
       field launch, mid-pilot checkpoint, and closeout.
     required: true
     type: textarea
   ```

   **Empty `framing` is a `[BLOCKER]`** — `solicitation-review` can't
   score responses against a missing anchor.

   **Dedupe by intent.** The PDD's `## Solicitation` → `Response
   template` may list opp-specific questions that overlap with the
   default set. Combine them — never publish two questions that ask
   the same thing in different wording (e.g. don't ask about "language
   capacity" AND "language + translation effort" as separate questions
   — fold them into one prompt with framing that calls out both axes).

   **Length budget:** 7-9 questions total. Fewer than 6 leaves
   evaluation criteria un-linkable; more than 10 fatigues the LLO and
   produces shallower answers across the board.

   **Default 6-question response template, archetype-branched** (used
   as the starting set; merge in PDD overrides per the dedup rule
   above):

   For every archetype except `focus-group` (`atomic-visit`,
   `multi-stage`, `longitudinal-visits`, …) — the CHW-deployment
   vocabulary is the default; only `focus-group` swaps it out (ace#1691):
   1. Describe your prior experience deploying CHW programs in this archetype.
   2. How will you recruit and train FLWs for this scope?
   3. What is your timeline for fielding once awarded?
   4. What is your supervision model?
   5. Do you have local-language capacity matching the target geography?
   6. Propose your all-in rate per verified service delivery, and state
      how much of it is paid to the worker vs. commodity. (ALL-IN — do
      NOT ask which costs would be "funded separately"; see the design
      principle above.)

   For `focus-group` (CHW-deployment vocabulary is wrong; swap to
   qualitative-research vocabulary):
   1. Describe your prior qualitative-research experience (FGDs,
      in-depth interviews) — topic, segment counts, working language,
      and what synthesis output you produced.
   2. How will you recruit homogeneous mother / father / grandmother
      groups without overweighting households with prior LLO program
      history?
   3. What is your timeline from award to first practice-session-pass
      certification, and from award to first live FGD?
   4. Describe your coordinator capacity to review facilitator gdocs
      against an Output Specification rubric on a rolling basis.
   5. What local-language fluency do your named facilitators have, and
      what audio-recording equipment do you have available?
   6. Provide a per-session budget breakdown (facilitator +
      notetaker + participant compensation + venue + coordinator
      review amortized).

4. **Write the draft for traceability.** Save the full payload + the
   AI-derived rubric to:

   ```
   ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-create_draft.md
   ```

   Include all fields from the payload as a structured YAML-frontmatter +
   prose body, so the `solicitation-create-eval` rubric can re-read it.

   **Compose it to a LOCAL FILE first, then pass `localFilePath` — do not emit
   the document inline (ace#1918).** Write the composed markdown to an absolute
   scratch path, then call
   `drive_create_file({name, localFilePath, parentFolderId})`; the server reads
   the bytes off disk, so the write costs ~zero context regardless of size.
   Both this draft and the `published.md` of step 8 carry the whole payload
   plus the derived rubric and routinely clear 40,000 chars — measured 49,531
   (draft) and 51,920 (published) on `bednet-check-2-visit/20260825-1310`, both
   re-confirmed 2026-09-06. The inline `content` param still works and is fine
   for a short EOI.

   **Compose the payload to `payload.json` on disk in THIS step, before the
   Step 6 publish — not after it (ace#2261).** The publish body, this draft and
   the Step 8 `published.md` are the same bytes; writing them once and pointing
   all three consumers at that one file makes them identical by construction
   rather than by diligence. Step 6 then sends that file directly (see § Step 6
   → *Large payloads*), and steps 4 and 8 render their markdown from it.

5. **Resolve the labs program_id (integer).** The labs MCP expects the
   labs **integer** program ID, *not* the Connect program UUID. Despite
   the schema's `program_id: string`, labs `int()`-parses it internally
   and rejects UUIDs with `ValueError: invalid literal for int()`.

   Resolve in this order:

   1. **Fast path:** if `opp.yaml.connect.program.connect_int_id` is set
      (cached at program-create time by `connect-program-setup`, or
      backfilled by a prior `solicitation-create` run), use it
      directly. This is the durable opp-level cache.
   2. **Lookup:** call `mcp__connect-labs__labs_context()`. Find the
      organization by the org recorded in `opp.yaml.connect.program.url`
      (`/a/<org>/program/<id>/` — the program's own org, authoritative),
      else `opp.yaml.organization_slug`, else the configured PM org
      (`connect_orgs.pm_org` from preflight); within it, find the program whose `name` matches
      the Connect program name from
      `runs/<run-id>/4-connect/connect-program-setup.md` (the markdown
      summary written by `connect-program-setup`). Capture the
      program's integer `id`.
   3. **Cache:** write the result to
      `opp.yaml.connect.program.connect_int_id` via `update_yaml_file`
      (`merge: 'deep'` — a partial patch of `connect.program`;
      `two-level` would replace the `program` sub-object wholesale and
      drop the existing `program.id`/`program.url`). This is opp-level
      state (the
      program is reused across runs, so its ConnectProd integer id is
      also opp-level). Also carry the value into this run's
      `phases.solicitation-management.products.solicitation.labs_program_id`
      via Step 9's consolidated write so the run state is
      self-contained.
   4. **Register it in the opp's tenancy** whenever this step resolved
      the id by lookup (sub-step 2) — `connect-program-setup` Step 7 could
      not, because Connect never returns the integer to ACE and labs hides
      a fresh program for up to an hour (ace#3213). Run it BEFORE any
      program-scoped labs write (Step 5a onward), or the tenancy guard
      treats those writes as outside the opp:

      ```bash
      "$CLAUDE_PLUGIN_ROOT/bin/ace-bind" --add-program <connect_int_id> [<workspace>/<opp>]
      ```

      Idempotent, so run it on the fast path too when you cannot see that
      Phase 4 registered it. A failure does not halt this step: record a
      residual naming the command.
   5. **Halt** with a `[BLOCKER]` if no name match — but first rule out
      the cache: labs caches the org tree per user for an hour
      (`_ORG_DATA_CACHE_TTL = 3600`, `dimagi-internal/connect-labs`
      `connect_labs/labs/integrations/connect/oauth.py`), so a program
      created under an hour ago can be missing. If the Connect program
      is that young, wait out the remainder and look up once more. Past
      that, the program likely exists but was never mirrored to labs.
      Surface the Connect program name and the list of labs programs the
      caller can see.

5a. **Make the PM org the call's owner — register it as a labs organisation
   first (ace#3049).** Since connect-labs#2567 (merged 2026-10-16) a
   solicitation must be **owned by a labs organisation (`LabsOrg`) the caller
   is a member of**. `program_id` alone no longer names an owner: it resolves
   only to a programme with a running organisation or to "an organisation labs
   knows", and ACE's per-run Connect PM orgs are neither until they are
   registered. Measured on `noora-health/noora-health/20261015-1129`
   (2026-10-16, JSON-RPC `tools/call create_solicitation`), every form of the
   call without a registered org was refused:

   - `org_slug: noora-health-pm-test` → `org_slug: no organisation 'noora-health-pm-test' in labs`
   - `organization_id: "397"` → `no organisation '397' in labs`
   - `program_id: "355"` only → `program 355 has no running organisation and no organisation labs knows, so it cannot own this call. Name the owning organisation with org_slug.`

   What worked, and what this step does on every run. The upsert is keyed
   by slug and binds by Connect id, but it is **not** a no-op on an org that
   already runs a labs programme: labs refuses even an identical upsert of
   one ("<org> runs a program on labs, so only platform support changes or
   merges its record", live on this instance's PM org, programme 361, 2026-10-20,
   ace#3261). So read first and skip a row that is already right:

   1. **The owner is the program's PM org** — the org Step 5 resolved the
      program under (the `/a/<org>/program/<id>/` segment of
      `opp.yaml.connect.program.url`, else the run's
      `products.connect.pm_org_slug`, else the configured `connect_orgs.pm_org`).
      Never the holding (NM) org and never the partner LLO: the call is the PM
      org's.
   2. **Read its Connect integer org id from the same `labs_context()` reply**
      Step 5 used (the organization entry's `id`). Do not guess it from a slug.
   3. **Read `supply_chain_org_list({program_id})`.** If the PM org's row is
      there with the same `name`, `connect_organization_id` and
      `connect_organization_slug` you would send, skip the upsert and go to
      4. Otherwise register it:

      ```
      mcp__connect-labs__supply_chain_org_upsert({
        data: {
          slug: <pm org slug>,
          name: <the org's display name from labs_context>,
          connect_organization_id: <Connect org integer id>,
          connect_organization_slug: <pm org slug>,
        },
      })
      ```

      On the noora-health repro this returned labs org **349** with
      `is_linked: true`. Binding by `connect_organization_id` is what makes
      membership flow from Connect (`supply_chain/runner.is_member`), so the
      caller — a member of the PM org on Connect — is a member of the LabsOrg
      with no further grant.
   4. **Pass `org_slug: <pm org slug>` AND `program_id: <Connect program
      integer id>` on the Step 6 call.** `org_slug` names the owner;
      `program_id` still links the call to its programme. With both, the same
      repro published as labs solicitation **1000001**.

   Branch on the call result, not on a read-back: if the upsert errors, halt
   with a `[BLOCKER]` naming the org slug and the error verbatim — publishing
   without a registered owner is refused by labs anyway, and guessing a
   different `org_slug` would file the call under the wrong organisation.

6. **Publish.** Call `mcp__connect-labs__create_solicitation` with the
   flat-fields shape from § Step 2 (every solicitation field as a
   top-level property — no `data: {...}` envelope). Labs validates the
   canonical schema server-side and rejects drift with
   `INVALID_SCHEMA` + per-field `error.details.fields` (JSON-path
   keyed). Read the error and fix the composition; do not retry with
   the same payload, and do not stuff extras into a free-form field.

   **Stale-schema gotcha.** If you see `INVALID_SCHEMA` errors that
   reference fields you swear are valid per the labs canonical schema
   (or vice versa — a payload that should be wrapped works when sent
   flat, or fields you expected to be optional are flagged required),
   the MCP subprocess in this session is probably holding a stale
   `tools/list` view of the labs schema. The labs MCP schema can
   evolve faster than this skill's documentation, and the proxy's
   schema gets cached at MCP-subprocess startup. Recovery:

   1. Curl the live `tools/list` directly:
      ```bash
      curl -sS -X POST https://labs.connect.dimagi.com/mcp/ \
        -H "Authorization: Bearer $LABS_MCP_TOKEN" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
      ```
      **Both the `Accept` header and the SSE-shaped response are load-bearing
      and neither is guessable.** Without `Accept: application/json,
      text/event-stream` the endpoint answers **HTTP 406** with no body —
      measured 2026-09-08 on `bednet-check-2-visit/20260907-1126`, where the
      snippet as previously printed here simply did not work. The reply is
      then **Server-Sent Events**, not plain JSON: take the line beginning
      `data: ` and JSON-parse the remainder.

      Treat the response as truth. If it disagrees with this SKILL.md,
      this SKILL.md is wrong — re-read the schema and update.
   2. Restart Claude Code (full process restart, not `/reload-plugins`)
      so the MCP subprocess re-fetches `tools/list` at startup.
   3. Update this SKILL.md if the live schema has moved.

   Call:

   ```
   mcp__connect-labs__create_solicitation(
     org_slug: <pm org slug registered in step 5a>,  # REQUIRED in practice since connect-labs#2567 — the owning LabsOrg
     program_id: <resolved labs_program_id as string>,
     title: ...,
     solicitation_type: 'eoi',                  # lowercase
     description: ...,                          # markdown string, 500-800 words
     scope_of_work: ...,                        # markdown string, 600-1000+ words, NOT an array
     application_deadline: 'YYYY-MM-DD',        # date string, NOT response_window_days
     expected_start_date: 'YYYY-MM-DD',
     expected_end_date: 'YYYY-MM-DD',
     estimated_scale: 'human-readable string',  # <= 200 chars (labs CharField(max_length=200))
     contact_email: ...,                        # OPTIONAL — include ONLY if the PDD names a contact; else OMIT this line entirely (no env fallback, no bot inbox)
     evaluation_criteria: [
       {id, name, weight, description, scoring_guide, linked_questions: [qid, ...]},
       ...
     ],                                          # weights sum to 100; id is REQUIRED
     questions: [
       {id, text, type, framing, required},
       ...
     ],                                          # 7-9 items; framing is structured, not inlined in text
     status: 'active',
     is_public: <true; false when optional_steps.private_solicitation>,
     connect_opportunity_id: <int>,
   )
   ```

   **Private (demonstration) solicitations.** When
   `optional_steps.private_solicitation` is true:
   1. Send `is_public: false`.
   2. Prefix `description` with this banner, verbatim, on its own line, before
      the composed body:

      ```
      > **[Demonstration — not a live call.]** Created by ACE to exercise the Labs workflow; responses are synthetic.
      ```

      The banner is mandatory. A private call is still readable by every member
      of the owning org and by anyone who responds, and a public Google Form for
      it (`google_form`) reaches anyone with the link. Without the banner, a
      reader cannot tell a demonstration from a real call for partners.
   3. Record `visibility: private` in the Step 9 products block (`public`
      otherwise). An absent `visibility` reads as `public`, which is the legacy
      behaviour.

   Reads of an unlisted call need no `program_id`. Labs authorizes them by
   owning-org membership: since connect-labs#2567, `get_solicitation`,
   `list_responses`, `get_response`, `update_solicitation` and
   `award_response` all describe `program_id` as "Accepted for compatibility;
   not needed" (live `tools/list`, 2026-10-18). ACE is a member of the owning
   PM org through the Step 5a registration, so the read-backs below work for a
   private call as written.

   **Large payloads: send the file, don't retype it (ace#2261).** The atom
   above takes inline arguments only — the live labs schema has **no**
   file-handle parameter (verified 2026-09-08 against `tools/list`: the 21
   declared properties contain nothing matching `file` or `path`), and
   `create_solicitation` is a labs-side tool, so this cannot be fixed atom-side.
   A composed solicitation body routinely runs **33–50 KB** (33,557 bytes on
   `bednet-check-2-visit/20260907-1126`; §§ 4 and 8 measure the same bytes at
   49,531 / 51,920 on `20260825-1310`). Emitting that as tool arguments spends
   its full size in context a second time — the exact cost ace#1918 removed from
   this skill's two documents — and makes the published bytes and the draft two
   independent generations that can silently diverge.

   So above roughly 20 KB, publish by sending the Step-4 `payload.json`
   **directly**, via the same server and the same server-side schema validation:

   ```bash
   python3 -c "import json; p = json.load(open('payload.json')); json.dump(
     {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
      'params': {'name': 'create_solicitation', 'arguments': p}},
     open('rpc.json', 'w'))"

   curl -sS -X POST https://labs.connect.dimagi.com/mcp/ \
     -H "Authorization: Bearer $LABS_MCP_TOKEN" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json, text/event-stream" \
     --data-binary @rpc.json
   ```

   Same `Accept`-header and SSE-response caveats as the `tools/list` snippet
   above — **plus the reply envelope, which is four levels deep and where the
   record is NOT the obvious one.** Read
   `result.structuredContent`: on both `create_solicitation` and
   `get_solicitation` that key holds the decoded solicitation record directly
   (`id`, `questions`, `evaluation_criteria`, the three dates, `is_public`, …).

   Do NOT reach through `result.content`. It looks like the payload and is
   double-JSON-encoded: `result["content"][0]["text"]` is a JSON *string* that
   parses to *another* `[{type, text}]` list, whose `[0]["text"]` is a second
   JSON string that finally parses to the record —
   `json.loads(json.loads(result["content"][0]["text"])[0]["text"])`. An agent
   that stops at "JSON-parse the `data:` line" gets
   `{content, isError, structuredContent}` and then raises `AttributeError` /
   `KeyError` on a publish that **already succeeded** (HTTP 200, record
   created), which is the worst possible moment to be unsure whether the call
   landed. Measured on `spark-facilitator/20260908-2215` (labs solicitation
   **19363**, program 210): 3 calls burned on the unwrap depth, during the
   Step 7a round-trip, i.e. after the external write had landed
   (dimagi-internal/ace#2302).

   This is **not** a workaround for a schema problem — labs validates
   the payload identically on both routes and returns the same
   `INVALID_SCHEMA` + `error.details.fields` on drift; it is the same call made
   without laundering the body through the model. Step 7a's `get_solicitation`
   round-trip is required either way and is what actually settles that the
   publish landed (it already says "whether via MCP atom or direct JSON-RPC").
   Record the route in `solicitation-create_draft.md`. For a short EOI that fits
   comfortably inline, the atom is simpler — use it.

   **Second-order reason this matters.** A 33–50 KB generated argument object is
   the single largest generation in Phase 8, and a generation cut mid-call is
   precisely what raises `InputValidationError: <tool> was called with input
   that could not be parsed as JSON` — a CLIENT-side error (see `CLAUDE.md`
   § Gotchas), where the tool never ran and the server never saw a byte.
   Reading the bytes off disk removes that failure mode instead of retrying
   into it.

   **All solicitation fields are flat at the top of the atom's argument
   object.** There is no `data: {...}` envelope. Verified against the
   live `tools/list`: top-level `additionalProperties: false`, no `data`
   property declared.

   **Do NOT include** `overview`, `response_window_days`,
   `anticipated_start`, `anticipated_end`, `sample_target`, `rubric`,
   `response_questions`, `pass_bar`, `eligibility_criteria`,
   `geographic_scope`, `per_hh_payment_band_usd`, or `budget` — none
   of these are read by the labs public-detail template. After labs's
   2026-05-22 deploy, the MCP itself rejects unknown top-level fields
   with `INVALID_SCHEMA` + per-field error details under
   `error.details.fields` (JSON-path keyed, e.g.
   `evaluation_criteria[0].linked_questions`). Read the error and fix
   the composition; do NOT retry with the same payload, and do NOT
   work around schema rejections by stuffing extras into a free-form
   field. Step 7a's `get_solicitation` round-trip remains the structural
   double-check.

   Capture the returned `id` (the labs record id) into `solicitation_id`.
   The response also includes `experiment` (echo of the program_id) and
   the data object as written. Public URL pattern:
   `${LABS_BASE_URL}/solicitations/<id>/`. Manage URL pattern:
   `${LABS_BASE_URL}/solicitations/<id>/edit/`. **NO `/labs/` prefix** —
   `connect-labs/config/urls.py` mounts the solicitations app at
   `/solicitations/`, not `/labs/solicitations/`. The `/labs/` prefix is
   reserved for the authenticated Labs UI (overview, login, explorer).

   **Check the route before recording the URL — for a listed call
   only.** Labs answers an anonymous client differently by visibility
   (observed 2026-10-19, ace#3254, after connect-labs#2567):

   | Call | Anonymous `/solicitations/<id>/` | Observed on |
   |---|---|---|
   | listed (`is_public: true`), active | **200** | 1000001 |
   | listed, closed | 302 → `/solicitations/past/<slug>/` | 1000002 |
   | unlisted (`is_public: false`) | **404** — same as a missing record | 1000004 (round-trips via `get_solicitation`); 9999999 (no record) |

   - **Listed call:** issue a HEAD against the constructed URL and
     expect **200** (a 302 to `/solicitations/past/…` is fine too). A
     **404** on a listed call means the route or the record is wrong —
     surface it as a `[BLOCKER]` rather than writing a broken URL into
     `run_state.yaml`.
   - **Private (unlisted) call:** skip the anonymous probe. Labs hides an
     unlisted record from anyone outside its owning org, so a 404 is
     the correct answer and tells you nothing. Never `[BLOCKER]` on it.
     Step 7a's `get_solicitation` round-trip is the check.

   Either way, whether the record persisted with the visibility you
   sent is settled by Step 7a's `get_solicitation` round-trip, not by
   this probe.

7a. **Verify the round-trip via `get_solicitation`.** Immediately after
   publish (whether via MCP atom or direct JSON-RPC fallback), call
   `mcp__connect-labs__get_solicitation(solicitation_id=<returned>)` and assert every load-bearing field
   round-trips intact. Treat the response as the canonical view of
   what labs persisted — if it diverges from what you sent, that's
   either silent-drop (an extra field labs rejected without surfacing)
   or silent-mutation (labs reformatting something).

   **If you read this back over raw JSON-RPC rather than the MCP atom, the
   record is `result.structuredContent`** — not `result.content`, which is
   double-JSON-encoded and needs four unwraps. See the envelope note under
   Step 6 (dimagi-internal/ace#2302). Assert against the decoded record, not
   against whatever the first `json.loads` handed you.

   Required round-trip assertions:

   - `title` matches what was sent.
   - `description` length is non-empty and ≥ 80% of the sent length (small whitespace/markdown normalization is OK; 20%+ shrinkage is silent-drop).
   - `scope_of_work` is a string (not an array) AND length ≥ 80% of sent.
   - `application_deadline` parses as `YYYY-MM-DD` AND matches the computed deadline.
   - `expected_start_date` + `expected_end_date` both parse and match.
   - **Ordering:** `expected_start_date > application_deadline` AND
     `expected_end_date > expected_start_date`. A violation is a
     `[BLOCKER]` — it is not a round-trip miss but an incoherent payload:
     the published page would tell candidate LLOs the work starts before
     their application is even due. Recompute per Step 2 and re-publish via
     `update_solicitation` before writing `published.md`.
   - **Engagement span (ace#1858, scoped by ace#2231):**
     `(expected_end_date − expected_start_date)` must be **≤ the PDD's
     `## Timeline` total − the solicitation window the total ITSELF
     contains**. Over-long is a `[BLOCKER]`: it is the signature of
     adding the PDD's whole timeline to a start date that already sits
     past the solicitation window — see the worked example under Step 2.
     This is a deliberately LOOSE ceiling — it does not additionally
     subtract any purely-contractual award row — so it catches the
     whole-total error without demanding the subtraction be exact.
     `> start` alone does not catch it: on
     `bednet-check-2-visit/20260828-0629` the wrong value was
     **2027-01-31** against a correct **2027-01-17** and passed the
     ordering check cleanly.

     **The subtrahend is CONDITIONAL, on the same reading Step 2 already
     performs — do not subtract a window the total never contained.**
     Resolve it exactly as rule (1) does, then apply:

     | The PDD's `## Timeline` | Ceiling |
     |---|---|
     | carries a solicitation-open row | `total − (application_deadline − publish date)` |
     | states only a total, no row breakdown | `total − (application_deadline − publish date)` — the window is assumed included, matching Step 2's fallback |
     | **starts at award** (its first row is post-award work — onboarding, recruitment, mobilisation) | **`total`**, subtract nothing |

     Subtracting unconditionally makes the ceiling `[BLOCKER]` the value
     Step 2 computed CORRECTLY, and the two disagree by exactly the
     solicitation window. Measured on
     `poverty-graduation/20260908-0510` (labs solicitation **19188**,
     program 265): PDD § 17's first row is *Partner onboarding and FLW
     recruitment*, so its 18-week total holds no solicitation window;
     Step 2 correctly subtracts nothing and publishes **2027-02-09**
     (span 126d), while the unconditional ceiling reads `126 − 14` =
     112d and rejects it. Complying would have published **2027-01-26**
     — two weeks short of the programme's own declared post-award
     stages, on a partner-facing listing. That is the exact inverse of
     the #1858 error this ceiling was added to catch, and
     `templates/pdd-template.md § Timeline` asks a PDD to state where
     its clock starts precisely because both shapes are legal.
   - `estimated_scale` is non-empty and **at most 200 characters** — check
     this on the composed payload BEFORE the Step 6 publish too, not only on
     the round-trip: the MCP schema has no `maxLength`, so an over-long value
     is accepted by validation and dies in Postgres as a raw `DataError`
     traceback (ace#3049).
   - `contact_email`: assert only **if you sent one** — when sent, it matches; when omitted (no PDD-derived contact), assert it is absent/empty on the round-trip (an omitted optional field is correct, not a miss).
   - `len(questions)` matches sent; every question has `id`, `text`, `type`, `framing` (non-empty), plus `required` if sent.
   - `len(evaluation_criteria)` matches sent; every criterion has `id`, `name`, `weight`, `scoring_guide`, `linked_questions` (non-empty); `sum(weights) == 100`.
   - `is_public` matches what was sent (`true`, or `false` for a private call); `status: 'active'`; `connect_opportunity_id` matches sent.
   - For a private call, `description` starts with the demonstration banner.

   **Any miss → `[BLOCKER]`** naming the missing or mutated field +
   the probable cause (e.g. "scope_of_work returned as an array — labs
   string→array coerced; check the payload was sent as a single
   markdown string and not Python-list-coerced upstream"). Do NOT
   proceed to write `published.md` against a half-persisted solicitation.

   **Why round-trip and not curl-the-public-URL.** An anonymous curl
   sees only a listed call's rendered page. An unlisted call answers 404,
   the same as a missing one (§ Step 6), and neither tells you whether
   every field persisted as sent. The `get_solicitation` round-trip is
   the canonical structural check at the persistence layer.

   This catches the class of bugs where the labs MCP accepts the
   create cleanly but persisted state diverges from sent payload.
   Verified live on solicitation 3130 (`malaria-itn-app/20260521-1400`)
   where all 6 sections were broken simultaneously because the entire
   payload schema had drifted — round-trip would have caught it at
   write time instead of human-eye time.

7b. **Verify the round-trip.** Immediately after publish, call:

   ```
   mcp__connect-labs__get_solicitation(
     solicitation_id: <returned id>,
   )
   ```

   This catches the silent-misconfig class where the create succeeds but
   the record is unreachable on subsequent reads. A private
   (`is_public: false`) call is readable here because ACE belongs to the
   owning org. Labs authorizes reads by owning-org membership, and the live
   schema marks `program_id` "Accepted for compatibility; not needed". The
   older rule, that an unscoped read sees only listed calls, described the
   pre-connect-labs#2567 ConnectProd `LabsRecord` API, which no longer
   serves these calls. **If this read returns
   "not found" for a private call**, the cause is ownership, not a missing
   `program_id`: check that the call's owner (`org_slug`) is the Step 5a
   LabsOrg and that ace@ is a member of it. If the verification call
   returns no record or a different `id`, halt and surface the mismatch —
   do not proceed to write `published.md` or mutate `opp.yaml`.

8. **Write `published.md`.** Save:

   ```
   ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-create_published.md
   ```

   Body: full payload as written, returned IDs/URLs, deadline in absolute
   ISO-8601 form, the AI-derived `evaluation_criteria` (so
   `solicitation-review` and `solicitation-monitor` have the rubric
   without re-fetching from labs).

   **Same rule as step 4: compose to a LOCAL FILE and pass `localFilePath`
   (ace#1918).** This is the larger of the two documents (51,920 chars
   measured). Reuse the step-4 scratch file with the returned IDs/URLs appended
   rather than re-composing the payload from scratch — the two documents share
   most of their body, and re-emitting it is exactly the cost this rule exists
   to avoid.

9. **Write the consolidated solicitation outputs block** (only when a run is
   bound; outside a run see § Inputs → Write-back) to the
   current run's `run_state.yaml.phases.solicitation-management.products.solicitation`
   via `update_yaml_file` + `merge: 'deep'`:

   ```yaml
   phases:
     solicitation-management:
       products:
         solicitation:
           solicitation_id: <returned>
           labs_program_id: <integer resolved in step 5>
           owner_org_slug: <pm org slug registered in step 5a>
           visibility: <public | private>   # private iff optional_steps.private_solicitation
           public_url: <returned>
           manage_url: <returned>
           type: <EOI|RFP>
           published_at: <now ISO-8601>
           deadline: <computed ISO-8601>
           status: open
           awarded:
             response_id: null
             awarded_at: null
             awarded_org_slug: null
             awarded_org_name: null
             awarded_contact_email: null
             award_amount: null
   ```

   `deep` merges `products.solicitation` while preserving sibling keys
   on the `solicitation-management` phase block (`status`, `steps`, and
   `products.selected_llo`) at every depth — `two-level` would replace
   the whole phase block wholesale (#572/#587). This skill is the sole
   writer of `products.solicitation` within the run; `solicitation-review`
   updates the same block in place at award time (within the same
   run).

   `selected_llo` is stubbed by `solicitation-review` on award, not
   here. `selected_llo` lives at
   `phases.solicitation-management.products.selected_llo`.

   **No write to `opp.yaml.solicitation`.** Solicitations are per-run
   — every `/ace:run` publishes a fresh solicitation; stale ones from
   prior runs are operator-cleaned-up when picking a release-candidate
   run.

## Error handling

- **Labs MCP unreachable** (proxy returns transport error): halt with a
  doctor-style message pointing at `/ace:doctor`'s `[Connect Labs]`
  section.
- **`create_solicitation` returns 4xx**: preserve `draft.md`, halt,
  surface the error verbatim. Do not retry — most 4xx is a payload
  schema mismatch or the program_id is wrong.
- **`create_solicitation` refuses with `no organisation '<x>' in labs` or
  `... cannot own this call. Name the owning organisation with org_slug.`**:
  Step 5a was skipped or registered a different slug. Run the
  `supply_chain_org_upsert` of Step 5a for the PM org and retry with that
  `org_slug` (ace#3049). Do not switch to `organization_id` — it resolves
  through the same registry and is refused the same way.
- **`create_solicitation` fails with `DataError: value too long for type
  character varying(200)`**: `estimated_scale` is over 200 characters.
  Shorten it in the payload and re-publish; nothing was written.
- **`generate_criteria` returns degenerate output** (empty list, single
  criterion): write what was returned, mark `evaluation_criteria` as
  `needs-review` in `published.md`, still publish. Criteria are editable
  post-publish via labs UI without losing responses.
- **`opp.yaml.program_id` missing**: halt with "run Phase 4
  (`connect-setup`) first to register a Connect program." The Connect
  UUID is the upstream evidence that a labs-side program will exist;
  without it there is nothing to look up in `labs_context`.
- **`labs_context` returns no name match for the Connect program**:
  halt. Surface the Connect program name we tried to match plus the list
  of labs programs visible under the org. The remediation is usually
  one of: (a) labs's program shadow was created with a different
  display name (rename via the labs UI); (b) the Connect program was
  created in an org the caller can't see in labs_context (PAT scope
  mismatch); (c) the program was created so recently that labs hasn't
  synced yet — wait a minute and re-run. Do **not** publish a
  solicitation under a guessed labs_program_id.

## Output

- `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-create_draft.md` (audit)
- `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-create_published.md` (live state)
- `run_state.yaml.phases.solicitation-management.products.solicitation.{solicitation_id, public_url, deadline, status: open, labs_program_id, ...}` populated (per-run only).
- `opp.yaml.connect.program.connect_int_id` cached on first resolution (durable opp-level — ConnectProd's integer id for the same program row as the UUID; reused across runs).
- `selected_llo` is left untouched here (populated by `solicitation-review` on award at `products.selected_llo`).

## MCP Tools Used

- `connect-labs`: `labs_context` (resolve Connect program name → labs
  integer program_id, when not cached; also the PM org's Connect integer
  id for step 5a), `supply_chain_org_upsert` (register the PM org as the
  owning LabsOrg — step 5a, ace#3049), `create_solicitation` (with
  `org_slug`),
  `get_solicitation` (round-trip verification by `solicitation_id`;
  `program_id` is not needed, even for a private call)
- `ace-gdrive`: `drive_create_file`, `drive_read_file`,
  `drive_update_file`, `update_yaml_file` (write
  `phases.solicitation-management.products.solicitation` to
  `run_state.yaml`; cache `opp.yaml.connect.program.connect_int_id` on
  first resolution)

## Mode Behavior

- **Auto:** Publish in one pass.
- **Review:** Pause after Step 6, present `published.md` for human
  approval before mutating `run_state.yaml`. (The publish itself
  already happened — review-mode is about the local state mutation,
  not the external call. If review rejects, the human can call labs's
  `update_solicitation` to draft or close the solicitation.)
- **Dry-run:** Steps 1-4, skip steps 5-7. Verdict with `dry_run: true`.

## Decisions Log

**Review fields (schema v6 — REQUIRED).** The decisions log is the run's review artifact (the build memo is retired). Every row this skill appends carries `plain` — one plain-language line for a programme partner who has never seen ACE — and, where the choice is visible somewhere a reviewer can open, `check_at` + `correct_looks_like`. The atom rejects a partner-facing row without `plain`, or with jargon in it. Rules, a worked row and the `review_ask` semantics: [`skills/_decisions-review-fields.md`](../_decisions-review-fields.md); field contract: `docs/decisions-contract.md`.

This skill writes load-bearing defaults to the per-run
`ACE/<opp-name>/runs/<run-id>/decisions.yaml`. The bar criterion and
schema live in `skills/idea-to-pdd/SKILL.md § Decisions Log Convention`
(canonical authority). The list below catalogs decisions that commonly
qualify under the bar for this phase — a working template, not a
required set. The skill applies the bar criterion and emits whatever
rows meet it; the catalog is a teaching device that improves over time.

### Common load-bearing decisions for Phase 8

| ID | Question | Map to surface |
|---|---|---|
| `solicitation-type` | Which solicitation kind? **Options:** `EOI` · `RFP` · `custom` | `solicitation-create-eval`; affects who applies and at what fidelity |
| `response-deadline` | Days from publish to deadline (default 14)? | `solicitation-create` schema; gates Phase 8→9 timing |
| `response-template-choice` | Stock template vs opp-custom response form? | `solicitation-create` content; downstream `solicitation-review` rubric input |

The orchestrator's Phase Write-Back Verifier (`agents/ace-orchestrator.md`
§ Phase Write-Back Contract § Decisions log clause) enforces the
contract; the renderer (`skills/decisions-render`) regenerates the gdoc
at end of every phase.

Each row this skill writes uses `phase: 8-solicitation-management` and
`skill: solicitation-create`.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-20 | Step 5a reads `supply_chain_org_list` before the PM-org upsert and skips it when the row already matches: labs refuses even an identical upsert of an org that runs a programme (dimagi-internal/ace#3261). | ACE team |
| 2026-10-16 | **connect-labs#2567 contract: the call needs a registered owning org, and `estimated_scale` is capped at 200 chars (dimagi-internal/ace#3049).** connect-labs#2567 (merged 2026-10-16) moved solicitations into the labs DB and made every call owned by a labs organisation (`LabsOrg`) the caller belongs to. ACE's per-run Connect PM orgs are not LabsOrgs, so on `noora-health/noora-health/20261015-1129` all three forms were refused (`org_slug` → `no organisation 'noora-health-pm-test' in labs`; `organization_id: "397"` → `no organisation '397' in labs`; `program_id: "355"` alone → `... cannot own this call. Name the owning organisation with org_slug.`). New § Step 5a registers the PM org unconditionally with `supply_chain_org_upsert` (bound by `connect_organization_id`, so membership flows from Connect; labs org 349, `is_linked: true`), and Step 6 passes `org_slug` + `program_id` — which published labs solicitation **1000001**. `estimated_scale` is `CharField(max_length=200)` upstream with no schema `maxLength`, so a 234-char value surfaced as a raw Postgres `DataError`; the cap now lives in the § Step 2 field table, the pre-publish check and the Step 7a round-trip. `owner_org_slug` is recorded in the products block. The same upstream PR removed the ConnectProd `/export/labs_record/` forward, so the CloudFront ~8 KB body block of ace#2993 is gone (a 26,689-byte payload published unchanged); this skill never carried a shortened-payload fallback for it, so there was nothing to retire here. | ACE team |
| 2026-09-08 | **§ Step 3 required every criterion to link a question but never required the linked criterion to be able to SCORE it, so a required question could contribute nothing (dimagi-internal/ace#2305).** The shape block asked for non-empty `linked_questions` and non-empty `scoring_guide` and stopped there — both are satisfied by a link that points at a criterion whose prose never mentions the question's subject. That failure is silent by construction: counts reconcile, every `linked_questions` entry resolves, weights sum to 100, and `solicitation-review` then scores responses against a `scoring_guide` with nothing in it about the thing that was asked. Measured on `spark-facilitator/20260908-2215` (labs solicitation **19363**): a required `language-capacity` question — Chichewa/Tumbuka fluency by role, plus native-speaker capacity to review app content the design itself records as machine-authored and unreviewed — was linked to `facilitation-track-record`, whose description and scoring_guide contained no occurrence of *language*, *fluency*, *translation*, *Chichewa* or *Tumbuka*; no criterion in the rubric mentioned language at all. 8 of 9 questions had a lexical anchor, that one had none. Caught by `solicitation-create-eval` *after* publication (verdict still `pass` at 9.16, but it drove the sole `criteria_alignment` deduction) and repaired in place with `update_solicitation` — safe because the record had zero responses. § Step 3 now requires a per-question scoreability walk before publishing, and names the two link failures to check: linked-to-nothing, and linked-to-a-criterion-that-never-mentions-the-subject. | ACE team |
| 2026-09-08 | **§ Step 6 documented how to send the JSON-RPC request and stopped one unwrap into the REPLY, so the record could not be found on a publish that had already succeeded (dimagi-internal/ace#2302).** The route itself was added hours earlier (ace#2261) and its response guidance ended at "take the line beginning `data: ` and JSON-parse the remainder" — which yields `{content, isError, structuredContent}`, not the solicitation. The record is **four** levels down, and the middle two are unguessable: `result["content"][0]["text"]` is a JSON string that parses to *another* `[{type, text}]` list, whose `[0]["text"]` parses to the record. An agent following the doc literally calls `.keys()` or `["id"]` on the first parse and raises `AttributeError`/`KeyError` **after** the external write landed (HTTP 200, record created) — the worst moment to be unsure whether a call worked. There is a one-liner the doc never mentioned: `result.structuredContent` holds the decoded record directly, on both `create_solicitation` and `get_solicitation`. Measured on `spark-facilitator/20260908-2215` (labs solicitation **19363**, program 210): 3 calls burned on the unwrap depth during the Step 7a round-trip. Same class as the `Accept`-header/406 fix in the entry below — request shape fixed, response shape still under-documented — and it now bites every Phase 8 above ~20 KB, which this skill measures as the normal case (33–50 KB). Step 6 gains the envelope note; Step 7a points at it for the read-back. | ACE team |
| 2026-09-08 | **Step 6 routed a >40 KB payload through the model's context while §§ 4/8 of the same skill mandated `localFilePath` for the SAME bytes (dimagi-internal/ace#2261).** The draft, the published doc and the publish body are one payload — §§ 4 and 8 say so ("reuse the step-4 scratch file") and measure it at 49,531 / 51,920 chars — but only two of the three consumers were routed off disk. The third, the publish itself, was pinned to `mcp__connect-labs__create_solicitation`, whose arguments are inline-only; the labs schema has no file-handle param (verified against the live `tools/list`) and it is a labs-side tool, so it cannot be fixed atom-side. The JSON-RPC route that solves it was already acknowledged — once, as an unexplained "fallback", in Step 7a rather than Step 6 — so nothing told an agent it was allowed or that a large payload was the case for it. Measured on `bednet-check-2-visit/20260907-1126` (labs solicitation **19201**, program 231): 33,557-byte payload published via `curl --data-binary @rpc.json`, HTTP 200, Step 7a round-trip green on every assertion. Step 4 now composes `payload.json` BEFORE the publish; Step 6 documents the JSON-RPC route for bodies above ~20 KB and names the `InputValidationError` failure mode a large generated argument object invites. Also fixed the § Step 6 `tools/list` curl, which **406s as printed** — it omits `Accept: application/json, text/event-stream`, and its reply is SSE rather than plain JSON. Both cost a round of rediscovery on the same run. | ACE team |
| 2026-09-08 | **Step 7a's span ceiling subtracted the solicitation window UNCONDITIONALLY, so a PDD whose `## Timeline` starts at AWARD tripped a `[BLOCKER]` on the end date Step 2 had computed correctly (dimagi-internal/ace#2231).** Step 2 conditions its subtraction on *reading the rows* — rule (1) subtracts a solicitation-open row **that exists** — while the ceiling added in #1858 subtracted the window whether or not the total contained it. The two therefore disagree by exactly the solicitation window on any PDD whose clock starts post-award, and the ceiling flags the right answer. Measured on `poverty-graduation/20260908-0510` (labs solicitation **19188**, program 265): § 17's first row is *Partner onboarding and FLW recruitment*, total 18 weeks with no solicitation row; Step 2 gives **2027-02-09** (span 126d) and the unconditional ceiling reads `126 − 14` = 112d and rejects it. Complying publishes **2027-01-26**, two weeks SHORT of the programme's declared post-award stages — the exact inverse of the #1858 overshoot. That run deviated deliberately and recorded it in the draft, the published doc and the `sol-response-deadline` decisions row, but a compliant agent would have halted a completed publish at the last step of Phase 8. The ceiling's subtrahend is now a three-case table keyed on the same reading rule (1) performs, and rule (1) states the has-none case explicitly. Both shapes are legal by design — `templates/pdd-template.md § Timeline` asks a PDD to say where its clock starts. *Enforced:* `test/skills/solicitation-end-date-addend.test.ts`. | ACE team |
| 2026-09-01 | **`expected_end_date` re-spent the solicitation window the start date had already consumed (dimagi-internal/ace#1858).** Step 2 said `expected_start_date + the PDD's stated duration band`, one row below a definition placing `expected_start_date` *after* the solicitation window and *after* award/contracting — while a PDD `## Timeline` total for a solicited engagement normally starts its clock at solicitation-open. The two rows therefore double-count the window and the award step. Measured on `bednet-check-2-visit/20260828-0629` (labs solicitation **17695**, program 231): published 2026-08-30 → deadline 2026-09-13 → start 2026-09-27; the rule applied literally gives `+18 weeks` = **2027-01-31**, against a correct post-award remainder of `+16 weeks` = **2027-01-17** — **14 days long on a public partner-facing listing**. That run deviated deliberately and recorded the derivation in the draft plus the `response-deadline` decisions row, but a compliant agent would have published the overshoot and nothing would have caught it: Step 7a asserted only `expected_end_date > expected_start_date`, which an over-long date satisfies. Sibling of ace#1685, which re-anchored the start date in the same change but never scoped the end date's *addend*. The addend is now explicitly the PDD's **post-award** duration — total less the rows the deadline + contracting allowance have already passed — with the subtraction recorded in the draft; Step 7a gained a span ceiling (`span ≤ total − solicitation window`); and `templates/pdd-template.md § Timeline` now asks the PDD to state where its clock starts, since it pinned no convention and the ambiguity was structural. | ACE team |
| 2026-08-26 | **`expected_start_date` was derived from the Phase 4 opp row, publishing a start date BEFORE the solicitation's own `application_deadline` (dimagi-internal/ace#1685).** Step 2 said "Phase 4 opp `start_date` if available", but Phase 4 runs before Phase 8 in the same `/ace:run`, so that date is always at or before the publish date while the deadline is publish + 14 days. Observed on `hh-poverty-targeting/20260824-1404` (labs solicitation **17041**, program 189): Phase 4 opp `start_date` **2026-08-26** vs computed `application_deadline` **2026-09-09** — following the rule literally publishes a work start 14 days before applications close. That run deviated deliberately (published 2026-09-21 → 2026-12-07, recorded in `decisions.yaml` row `solicitation-date-window`), but a compliant agent would have published the contradiction and nothing would have caught it: Step 7a asserted only that the dates round-tripped, and `solicitation-create-eval` dim 3 graded the deadline in isolation. The PDD fallback does not save it either — for a relative-to-award timeline (the normal shape here) there is no absolute start date to inherit. Both date rows are now anchored to `application_deadline + a contracting allowance` and the PDD's duration band, with the Phase 4 dates usable only when they already satisfy the ordering; Step 7a gained a `[BLOCKER]` ordering assertion, and the eval rubric grades the ordering. | ACE team |
| 2026-08-19 | **Deleted two superseded paragraphs that Step 6 still contradicted itself with (dimagi-internal/ace#1523).** Surfaced on `bednet-check-2-visit/20260817-1720` Phase 8 (labs solicitation 14796). The 2026-05-22 correction below rewrote Step 6's headline guidance but left the retracted prose sitting underneath it, so Step 6 gave opposite instructions on the only two things it exists to specify. (1) A paragraph claiming "the atom requires `data` (object) … flat top-level fields get dropped by the labs adapter" survived 19 lines below the bolded "**All solicitation fields are flat … There is no `data: {...}` envelope**". The flat shape is correct — re-verified against the live `tools/list` this run: `additionalProperties: false`, no `data` property, `required: [title, description, solicitation_type]` — so a payload built per the stale paragraph sends an unknown top-level key and is rejected `INVALID_SCHEMA`. Deleted. (2) "**Verify reachability … confirm 200 … otherwise `[BLOCKER]`**" contradicted Step 7a's own "**Why round-trip and not curl-the-public-URL**", which states that the detail page 302s to the labs login *by design* because `is_public` is marketplace listing visibility, not anonymous readability. Measured on 14796: `/solicitations/14796/` → `302 → /labs/login/?next=…`, never 200 — so the rule as written raised a `[BLOCKER]` on every correctly-published solicitation ACE will ever produce. Rewritten to check for **404 specifically** (route missing → `[BLOCKER]`) and to state the 302 as expected, with `get_solicitation` named as the thing that actually settles whether the `public` flag flipped. Also fixed the stale "Step 7a's public-page verifier" phrase — Step 7a has been a persistence-layer round-trip since 2026-05-22. Class: `docs/learnings/2026-04-28-mcp-vs-skill-doc-drift.md`, same shape as the closed #1043 / #1055, except both leftovers here sat in the *same section* as the text superseding them. | ACE team |
| 2026-07-29 | **Fixed five drifts between `skills/_solicitation-template.md` and `lib/artifact-manifest.ts` (dimagi-internal/ace#1055), plus this skill's own self-contradicting § Products line.** Surfaced during `hh-poverty-targeting/20260728-0705` Phase 8 (labs solicitation 10687). The shared reference doc every Phase 8 skill points at had: (1) `public_url: .../grants/solicitation/<id>/` — a route that does not exist; canonical is `/solicitations/<id>/`, which this skill's § Step 6 already documented including the "NO `/labs/` prefix" trap. Verified live on solicitation 10687: `/solicitations/10687/` → **302** (the route exists and redirects to the labs login, which § Step 6 documents as by-design — the detail page is not anonymously readable), while `/grants/solicitation/10687/` → **404**, i.e. the route the template documented genuinely does not exist; (2) prose calling the state block `outputs` at two places while its own code block and the rest of the file said `products` — `products` is correct and is what `lib/phase-products-schema.ts` and `verify_phase_products` enforce; (3) a Drive-paths table where two of four rows were wrong — `solicitation-create_summary.md` (no such artifact; it's `_draft.md` + `_published.md`) and `llo-invite_outbound-emails/<llo>.md` (it's `llo-invite_invitations.md`) — the table is now the full manifest set with each entry's real `required` flag; (4) `awarded.awardee_org_slug` where the writer emits `awarded_org_slug`, a silently-wrong key, plus an invented `awarded_by` and three missing fields; (5) `id: <labs solicitation UUID>` where the record id is an integer and the key is `solicitation_id`. This skill's § Products also still named the retired `solicitation-create_summary.md` while its own § Output correctly named the draft/published pair. Class: `docs/learnings/2026-04-28-mcp-vs-skill-doc-drift.md` — `test/skill-atom-references.test.ts` catches atom renames but not artifact paths or state keys restated in a shared `skills/_*.md` reference doc, the same blind spot ace#1043 hit two days earlier. | ACE team |
| 2026-05-21 | **Work-order-as-primary-input + canonical-schema field names + comprehensive-content shape.** Three bundled rewrites prompted by solicitation 3130 on `malaria-itn-app/20260521-1400` where the public page rendered blank Description, "TBD" timeline, "No deadline," Python-list-repr Scope, and zero questions / zero rubric simultaneously. (1) Inputs now read Phase 1's work order (`1-design/pdd-to-work-order.gdoc`) as the primary content source + `decisions.yaml` for later run decisions, alongside the PDD (now used for problem-framing only, not for scope). (2) Field names migrated to the labs canonical schema (`description` not `overview`, `application_deadline` not `response_window_days`, `expected_start_date/_end_date` not `anticipated_*`, `estimated_scale` not `sample_target`, `questions[].text` not `response_questions[].question`, `evaluation_criteria[].name/.scoring_guide/.linked_questions` not `rubric[].dimension/.criterion`; `solicitation_type: 'eoi'` lowercase). Top-level fields not in `solicitations/models.py` (`pass_bar`, `eligibility_criteria`, `geographic_scope`, `per_hh_payment_band_usd`, `budget`) folded into `description`/`scope_of_work` prose. (3) Content shape demands comprehensive prose: `description` 500-800 words foundation-pitch tone; `scope_of_work` 600-1000+ words derived section-by-section from the work order with explicit de-prescription rules (exact dollars → ranges, exact weeks → windows); every question has a required `framing` field; every evaluation criterion has a required `scoring_guide` + `linked_questions`. (4) Added Step 7a — a curl-the-public-URL structural verifier that catches field-name drift at write time instead of at human-eye time. | ACE team |
| 2026-05-22 | **(superseded — see 2026-05-22 correction below)** Align with current labs reality + document the ideal end-state (`jjackson/connect-labs#212`). Three labs-side gaps surfaced during the malaria-itn-app `20260521-1400` Phase 8 republish required inline workarounds. Three of the four "labs-side gaps" I diagnosed turned out to be ACE-side stale-schema reads, not labs bugs — see the correction entry. | ACE team |
| 2026-05-22 | **Correction: 3 of 4 "labs gaps" in #212 were actually ACE reading a stale schema.** The labs maintainer triaged `jjackson/connect-labs#212` against the live `tools/list` and found: (a) wire-shape "drift" — NOT a labs bug; deployed schema is flat (no `data` envelope), the wrapped shape this skill called out came from ACE's stale view; (b) `evaluation_criteria[].id` undocumented — NOT a labs bug; live schema declares `evaluation_criteria.items.required: [id, name, weight]`, ACE was reading a stale schema; (c) public-detail page 302s to login — WORKING AS INTENDED; `is_public` controls marketplace listing for logged-in users, NOT anonymous readability. Only #2 (`framing` on questions) was a real ask, and it turns out the deployed schema already has `framing` as an optional property — the live MCP accepts it as a structured key. Skill rewritten to match the live schema: dropped Step 6's wire-shape fallback paragraph (call the atom as documented, flat fields); dropped the criterion-id hedge (it's documented + required); emit `framing` as a structured key (drop the `Why we're asking: <framing>\n\n<text>` inline anchor convention); dropped the "Step 7a-bis curl-the-public-URL once #212 ships" plan (won't work — `is_public` isn't anonymity). Added new **Stale-schema gotcha** under Step 6 explaining the recovery: curl `tools/list` against the live labs MCP, treat that as truth, restart Claude Code (full process restart, not `/reload-plugins`) to pick up the fresh schema. Added "live `tools/list` is the canonical contract; if this SKILL.md disagrees, the SKILL.md is wrong" at the top of Step 2. The underlying lesson: when an MCP server can evolve faster than this skill's documentation, treat the live `tools/list` as the source of truth — never trust a cached view in the local subprocess. | ACE team |
| 2026-05-22 | **Architecture decision: ACE owns composition; labs validates.** PR #396 had floated a future labs-side `create_solicitation_from_brief` MCP tool that would compose content server-side via labs's `solicitation_agent`. Walked back — operator chose to keep composition in ACE so this skill retains full control over voice, archetype-branched scope, framing/scoring_guide quality, and decisions-log integration (all of which are ACE-context that labs would have to learn). Labs's tightened MCP (forthcoming deploy: `create_solicitation` + `update_solicitation` now validate the canonical schema and fail loudly with `INVALID_SCHEMA` + `error.details.fields` on drift) is the right server-side contribution: schema enforcement, not content generation. This skill is the long-term home for solicitation composition; Step 6's payload shape is bound to labs's `tools/list` inputSchema rather than to a future composer call. Removal of the prior "Removal criteria" line. | ACE team |
| 2026-09-06 | **Large artifacts are composed to a LOCAL FILE and written with `localFilePath` (dimagi-internal/ace#1918).** Both `solicitation-create_draft.md` (49,531 chars) and `solicitation-create_published.md` (51,920) were measured over 40,000 on `bednet-check-2-visit/20260825-1310` and re-confirmed 2026-09-06. Step 8 now reuses step 4's scratch file rather than re-composing the shared body. *Enforced:* `test/skills/large-artifact-localfilepath.test.ts`. | ACE team |

---
name: llo-onboarding
description: >
  Onboard an awarded LLO: issue the Connect program invite and send the onboarding email with
  training materials and chatbot link. Needs a recorded award.
disable-model-invocation: false
---

# LLO Onboarding

First LLO contact. Reads
`phases.solicitation-management.products.selected_llo` in the current
run's `run_state.yaml`, issues the Connect system invite to that single
org, and sends the ACE-authored onboarding email with the OCS widget
link embedded.

## How the LLO got there: two sources, one contract

**A solicitation is one way to select an LLO, not the only one**
(operator decision 2026-09-16). `selected_llo.source` says which:

| `source` | Who wrote it | Phase 8 | Also carries |
|---|---|---|---|
| `solicitation` | `solicitation-review`, after `award_response` | `done` | `response_id`, and a sibling `products.solicitation` block |
| `operator` | this skill, transcribing the opp's inputs | **`skipped` is legal** | no `response_id`, no `solicitation` block |

An absent `source` is read as `solicitation` (legacy runs).

**On the `operator` path, transcribe — do not invent.** The LLO's
`org_slug`, `contact_email` and `contact_name` come from the opp's
`inputs/` (PDD § Program Parameters `llo_org_slug` /
`llo_contact_email` / `llo_contact_name`). If `org_slug` is absent
there, HALT and ask the operator for it; **never derive a slug from an
organisation's display NAME.** A Connect slug is visible only in the
org's URL — `https://connect.dimagi.com/a/stewari/opportunity/` gives
`stewari`, while the PDD's recorded name `stewari_nm_sandbox` was
refused by `connect_send_llo_invite` with *"Object with slug=… does not
exist"* (measured on turmeric-market-study/20260914-1742). Note
`/a/<slug>/opportunity/` 404s for an org `ace@` is not a member of, so
a 404 there means "no access", NOT "no org" — it cannot be used to test
existence. The invite endpoint's global lookup is the real test.

**Phase 9 entry guard:** if
`phases.solicitation-management.products.selected_llo.org_slug` is
null/empty in the current run's `run_state.yaml`, this skill halts
immediately. Branch the message on whether Phase 8 ran:

> FATAL: Phase 9 cannot start — `selected_llo.org_slug` is empty in the
> current run's `run_state.yaml`.
>
> - **If Phase 8 is `done`/`pending`:** run
>   `/ace:step solicitation-review --opp <opp-name>` to score the
>   responses and award an awardee. The orchestrator's pre-Phase-8 gate
>   should have caught this; if you're seeing this from a manual
>   `/ace:step` invocation, the gate was bypassed.
> - **If Phase 8 is `skipped`:** this run selected its LLO up front, so
>   there is nothing to award. The LLO details are missing from the
>   opp's `inputs/` — add `llo_org_slug` (from the org's Connect URL),
>   `llo_contact_email` and `llo_contact_name` to the PDD's
>   § Program Parameters, or supply them now.

Either way the skill onboards exactly one org — the single-awardee
model that replaced the multi-LLO roster in `connect-setup/invites.md`.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `llo` (`org_slug`, `contact_email`, `contact_name`) | the one org onboarded | explicit arg; default: the current run's run_state `phases.solicitation-management.products.selected_llo`; else the PDD § Program Parameters (operator path, see above) |
| `program_id`, `program_org`, `source_apps`, opportunity and payment-unit parameters | handed to `connect-partner-opp-create` (Step 2) | explicit arg; defaults as in that skill's § Inputs |
| `training_folder` | the training pack linked in the email | explicit arg; default: `6-qa-and-training/` in the current run |
| `widget` (`public_id`, `embed_key`) | the chatbot link in the email | explicit arg; default: `5-ocs/ocs-agent-setup.md` |
| `award_record` | award amount and context for the email (solicitation path only) | explicit arg; default: `8-solicitation-management/solicitation-review_award-record.md` |

Inside a run, the Phase 9 entry guard above applies. Outside one (a new partner on a live program), pass `llo` and the rest explicitly; the results go to the program context doc instead of `selected_llo`.

## Process

1. **Read inputs from GDrive:**
   - `selected_llo` block — read from
     `phases.solicitation-management.products.selected_llo` in the
     current run's `run_state.yaml`. Must contain `org_slug` and
     `contact_email`; on the award path it also carries
     `source: 'solicitation'` + `response_id`. Halt with the FATAL
     message above if `org_slug` is null/empty.

     **If the block is absent and Phase 8 is `skipped`,** write it
     first from the opp's `inputs/` (PDD § Program Parameters
     `llo_org_slug` / `llo_contact_email` / `llo_contact_name`) via
     `update_yaml_file` (`merge: 'deep'`), setting
     `source: 'operator'`. Do NOT synthesize a `products.solicitation`
     block to go with it — an operator-selected LLO has no
     solicitation, and inventing one would fabricate an audit trail for
     a process that never ran.
   - Training materials: `ACE/<opp-name>/runs/<run-id>/6-qa-and-training/`
   - Opportunity details: `ACE/<opp-name>/runs/<run-id>/4-connect/connect-opp-setup.md`
   - Program details: `ACE/<opp-name>/runs/<run-id>/4-connect/connect-program-setup.md` (program
     UUID for the Connect invite)
   - OCS widget config: `ACE/<opp-name>/runs/<run-id>/5-ocs/ocs-agent-setup.md`
     (`public_id`, `embed_key`)
   - Award record: `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-review_award-record.md` (for
     the awarded amount and award context to mention in the onboarding
     email)

2. **Stand up the LLO's delivery opportunity with `connect-partner-opp-create`.** That skill
   owns the whole round trip: the program invite, the PM accept, fresh app copies, the
   opportunity held by the LLO, its payment units and flags, then a read-back. Pass:
   - `program_id` and `program_org`: the program UUID (from `connect-program-setup.md`) and the
     PM-side org in the program's recorded URL (`connect_orgs.pm_org` from preflight). Never
     type a slug.
   - `partner_org_slug`: `selected_llo.org_slug`.
   - `source_apps`: this run's released apps (`phases.commcare-setup.products.apps`).
   - `opportunity` and `payment_units`: the PDD's dates, with the rate and budget the **work
     order** settled, in the program's currency.
   - the approval this phase recorded (a dispatched copy cannot ask the human).

   Three things it does that this skill relies on:
   - **It captures `program_application_id` from the invite response**, the only place the UUID
     appears. Write it back into `selected_llo` straight away (`update_yaml_file`,
     `merge: 'deep'`), before anything else can fail.
   - **It never accepts a real partner still at `INVITED`.** When it stops there, tell the
     partner to accept the invitation in Connect, and retry later (ace#2954).
   - **It halts rather than clamping** a `start_date` outside the program window.

   Phase 4 deliberately did NOT create this opportunity. Its opportunity is ACE's build/QA
   vehicle, created before any LLO was invited. **Two opportunities is the correct model**, not
   a workaround. It falls out of the ace#573 `DeliverUnit.payment_unit` FK constraint, which is
   why `connect-partner-opp-create` copies fresh apps.

   Record its returned `opportunity_id` / `opportunity_url` into `selected_llo` (step 7).

3. **Read the PDD's `archetype:` field.** Email content — framing, "getting
   started" steps, timeline language, and which pieces of training material
   to emphasize — branches by archetype. See `## Archetypes` below. Fall
   back to `atomic-visit` if unspecified.

4. **Compose the onboarding email for the awarded LLO:**
   - From: `$ACE_GMAIL_ACCOUNT` (via `email-communicator` skill)
   - To: `selected_llo.contact_email` (from current run's `run_state.yaml`)
   - CC: CRISPR Admin Dimagi Google Group
   - Subject: "[Opportunity Name] — Welcome and Next Steps"
   - Body (archetype-aware — see `## Archetypes` for per-archetype content):
     - Welcome and opportunity overview — frame the recipient correctly for
       the archetype (FLW-managing org for `atomic-visit`; facilitator-owning
       org for `focus-group`; staged-execution org for `multi-stage`)
     - Links to training materials (GDrive links or attachments) —
       foreground the materials the recipient needs FIRST for this archetype.
       **Enclose only the artifacts in this send's scope.** Resolve it with
       `resolveSendScope` from `lib/training-send-scope.ts` — pass the subset the
       operator named for this send ("send only the training deck" →
       `resolveSendScope(['training deck'])`), or nothing when they named no
       subset, which links them all as before. Before sending, assert the
       message obeys it: `assertSendScopeRespected(scope, <artifacts enclosed>)`.
       This is a live external send, so an out-of-scope enclosure is not
       recoverable after the fact — check before `canopy email send`, not after.
       Every artifact is still generated in Phase 6 regardless; the scope
       governs only what this recipient receives.
     - Step-by-step "getting started" — archetype-specific (download app vs.
       review question guide vs. stage-1 prep)
     - Timeline and expectations — archetype-specific cadence (continuous
       fieldwork vs. N sessions over T weeks vs. staged milestones)
     - **OCS widget** — embed link / URL derived from `public_id` + `embed_key`
       so LLOs can chat with the ACE support bot directly. Also mention the
       email fallback (`$ACE_GMAIL_ACCOUNT`)
     - Contact info for escalation
     - **The partner's opportunity link.** The Phase 6 drafts
       (`training-onboarding-email`, `training-llo-guide`) carry the verbatim
       placeholder `[PLACEHOLDER — your organisation's Connect opportunity link, sent when your opportunity is set up]`
       because the partner's opportunity did not exist yet. Replace every
       occurrence with the `opportunity_url` step 2 created. Never link the
       Phase 4 opportunity (`phases.connect-setup.products.connect.opportunity.url`) —
       it is held by ACE's own Connect org and the LLO cannot open it (ace#3000).

5. **Send the email** via the `email-communicator` skill (or draft for
   review) — and pass the run-page override, because this send is a
   deliberate carve-out from it:

   ```
   bin/ace-email --to <selected_llo.contact_email> --cc <CRISPR Admin group> \
     --subject-file <subject-file> --body-file <body-file> \
     --no-run-page "LLO onboarding: the training pack is the deliverable; ace-web is a Dimagi-side review surface"
   ```

   **Without the flag this send is REFUSED, and the refusal is correct
   until you read who the recipient is.** `bin/ace-email` exits 3 —
   before canopy is called, dry-run included — on a body that links
   `docs.google.com` / `drive.google.com` and carries no
   `labs.connect.dimagi.com/ace/` link (ace#2378). Step 4's body is
   exactly that: the Phase 6 training pack, enclosed as Drive links.
   Reproduced on a realistic Phase 9 body, 2026-09-17 (ace#2380):

   ```
   $ bin/ace-email --to llo@example.org --subject "... Welcome and Next Steps" \
       --body-file body.txt --dry-run
   ace-email: REFUSED (dry-run — a real send gets this same refusal). The body
   links Google Drive/Docs but not the run's ace-web page.
   $ echo $?
   3
   ```

   **Why the carve-out is right.** The convention the rail enforces is
   scoped to a **reviewer-facing** reference to a run (`CLAUDE.md
   § Conventions`): ace-web renders how the run was built and what Dimagi
   decided, for Dimagi-side review. The awarded LLO is an implementing
   partner, not a reviewer — what they need in their first message is the
   opportunity to accept and the pack that trains their team. Leading
   with a build audit trail would hand them the wrong document. The
   override is how a send says "the run page is not this recipient's
   surface", which is a statement, not a suppression: it is echoed to
   stderr and lands in the transcript.

   **It does not generalise to Phase 9's other mail.** A later reply on
   this thread that discusses how the run was built, or that asks anyone
   to review it, is reviewer-facing again and leads with the run's
   `ace_web_summary_url` with the Drive links as deep links under it.

6. **Log communications** to `ACE/<opp-name>/runs/<run-id>/9-execution-manager/llo-onboarding_comms-log.md`.

7. **Record the handover back into `selected_llo`** via `update_yaml_file`
   (`merge: 'deep'`) — one write, all the fields this run produced about
   this LLO:

   | Field | Source |
   |---|---|
   | `program_application_id` | the step-2 invite POST, via `connect-partner-opp-create` (already written there) |
   | `opportunity_id` / `opportunity_url` | the LLO's own delivery opportunity, once it exists |
   | `email_thread_id` | the Gmail thread the onboarding exchange runs on |
   | `email_message_ids[]` | every message sent on it, appended in order |

   **Why this is a write and not a "read it back later".** Two of these
   cannot be re-derived: `program_application_id` because
   `connect_list_invites` shows only an integer row id, never the UUID, and the mail ids because nothing else records which
   thread carried the round-trip. The other two are cheap to re-read but
   belong with them — the point of the block is that one place answers
   *"what did we do with this LLO?"*.

   **`email_message_ids` is an ARRAY, so a `deep` patch REPLACES it
   wholesale** (CLAUDE.md § `update_yaml_file`). Read the existing list,
   append, and send the whole intended array — three successive `deep`
   patches otherwise leave only the last id.

   This block is what `render_run_readme` surfaces as § LLO handover, so
   it stays readable without opening `run_state.yaml`.

## Archetypes

The onboarding email is the first LLO-facing artifact of the entire
pipeline. Atomic-visit framing in a focus-group opp lands as obviously
wrong to the recipient — emails that say "your FLWs will start collecting
deliveries" when the recipient is running discussion groups corrode trust
before the first session. Branch on `archetype:` from the PDD.

### `atomic-visit` (default)

**Welcome framing:** address the recipient as an LLO whose FLWs will
execute atomic deliveries in the field. Mention target FLW count and
geographic coverage.

**Getting-started steps (ordered list in the email):**
1. Download the CommCare app on the issued device
2. Register FLWs and assign them to the opportunity
3. Walk through the first training module with at least one FLW
4. Run a dry-run visit and confirm data lands in the opportunity dashboard

**Materials to foreground:** `training-flw-guide.md` and
`training-quick-reference.md` (field-facing). `training-llo-guide.md` is the
overview; link it but don't lead with it.

This ordering applies to whatever is **in scope** — it is guidance on emphasis,
not a list of required enclosures. On a scoped send, foreground the highest item
here that survives the scope and link nothing that does not (a deck-only send
leads with the deck).

**Timeline language:** "Continuous fieldwork over the opportunity window.
Target delivery volume is X/week per FLW — see the opportunity brief."

### `focus-group`

**Welcome framing:** address the recipient as the **facilitator-owning
org** for the FGD study. Name the session count and topic area in the
opening line. Do NOT say "FLW" or "delivery" — the recipient's team is
running discussions, not visits.

**Getting-started steps (ordered list in the email):**
1. Review the question guide (`question-guide.md` if present, else
   `pdd.md` § Research Questions) and the facilitator guide
2. Confirm venue + recording-equipment arrangements for Session 1
3. Complete participant recruitment per the PDD's eligibility criteria
4. Schedule a 20-minute pre-kickoff call with the ACE admin if this is
   the facilitator's first FGD on Connect (mention only if the PDD or
   `llo-invite` rationale flagged training need)
5. Run Session 1; upload the audio + the session note template within
   48 hours

**Materials to foreground:** facilitator guide, question guide, consent
form, audio-upload instructions. These live under
`runs/<run-id>/6-qa-and-training/` but paths differ per archetype — if
an FGD-specific training bundle isn't present, link the atomic-visit
materials with a note that the
team should adapt the framing for discussion sessions (record it as a
decision row with a `review_ask`, `owner: implementing-org` — the producer
rule, `skills/_decisions-review-fields.md`).

**Timeline language:** "N sessions over T weeks. Expect ~4–6 hours of
prep + facilitation + write-up per session (not continuous fieldwork)."
Pull N and T from the PDD; if absent, say "per the session plan in
your kick-off materials" and record the gap as a decision row with a
`review_ask`.

**Smaller-N reality:** FGD opps typically invite 1–2 LLOs
(per `llo-invite` § Archetypes). If the recipient list exceeds 2,
include a sentence naming the other facilitators and the cross-session
coordination expectation (same question guide, consistent write-up
template).

### `multi-stage`

**Welcome framing:** address the recipient as the org executing Stage N
of the pipeline (where N is their assigned stage per the invite list's
`rationale`). If the org spans multiple stages, list all of them with a
sentence naming what they own at each.

**Getting-started steps:** staged. List Stage 1 steps first (typically
the format/protocol that Stage 1 uses — FGD, interview, or atomic
visit). Don't front-load steps that only apply to a later stage;
mention downstream stages by name and note "separate onboarding
communication will go out before Stage 2 starts" if the stage transition
is far enough out.

**Materials to foreground:** Stage-1 materials first. Later-stage
materials link'd as reference but not required reading for week 1.

**Timeline language:** "Stage 1 runs weeks 1–N. Stage 2 begins after
the Stage 1 gate (see pipeline diagram)." Include the gate/transition
criteria explicitly so the recipient knows what finishes Stage 1.

## MCP Tools Used
- Google Drive: `drive_read_file`, `drive_create_file`, `drive_list_folder`
- Connect: through `connect-partner-opp-create` (invite, accept, app copies, opportunity, payment units); see its § MCP Tools Used
- Email: `email-communicator` skill (sends from `ace@dimagi-ai.com`)

## Mode Behavior
- **Auto:** Send emails directly, log to GDrive
- **Review:** Present email drafts for review before sending

## Dry-Run Behavior
When `--dry-run` is active:
- Write the onboarding email content (recipients, subject, body, attachments) to `comms-log/dry-run-llo-onboarding.md`
- Do not send emails
- State tracks as `dry-run-success`


## Terminology

**The platform is `Connect`, never `CommCare Connect`** — in every word this skill
puts in front of a human. The full rule, including the carve-outs for CommCare the
mobile app, CommCare HQ and code-level identifiers, is
[`skills/_terminology.md`](../_terminology.md). Read it before writing prose; it is
binding on this skill's output.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-04-28 | Replace HITL workaround with `connect_send_llo_invite` (ace-connect 0.8.1). Connect's invite is program-level, so the atom takes the program UUID and an `organization` slug for the target LLO workspace | ACE team |
| 2026-04-30 | Switch `connect_send_llo_invite` to `POST /api/programs/<id>/applications/` (commcare-connect PR #1135). Args drop `contact_email` (server emails workspace admins via `send_program_invite_email`). Add new step 2a: `connect_accept_program_application` for ACE-driven dogfood runs that need to auto-accept the invite. (0.10.47) | ACE team |
| 2026-05-04 | Read awardee from `opp.yaml.selected_llo` instead of iterating `connect-setup/invites.md` roster. Phase 9 entry guard halts with an actionable message if `selected_llo.org_slug` is null (Phase 8 `solicitation-review` must run first). Single-org onboarding replaces multi-LLO roster model. (0.12.0) | ACE team |
| 2026-09-17 | **Step 5 sends with `--no-run-page`, and says why.** `bin/ace-email` refuses a body that links Drive/Docs and no ace-web page (ace#2378); step 4's body is nothing but the Phase 6 training pack as Drive links, so the first live Phase 9 send exited 3 before canopy was ever called — reproduced on a realistic body 2026-09-17. The rail's convention is scoped to a **reviewer-facing** reference to a run, and the awarded LLO is an implementing partner, not a reviewer, so the override is the fix rather than an ace-web link in an onboarding pack. `bin/ace-email`'s own refusal text and `email-communicator` said the override was for threads with NO run, which would have steered a Phase 9 agent away from the flag it needs; both now name the partner-deliverable case. *Enforced:* `test/hooks/email-shims.test.ts` extracts this step's reason and proves a Drive-only body carrying it reaches canopy, plus `test/docs/ace-web-primary-surface.test.ts`. ace#2380. | ACE team |
| 2026-09-16 | **Two changes, one operator decision each (2026-09-16).** (1) **A solicitation is one way to select an LLO, not the only one.** `selected_llo.source` now distinguishes `solicitation` (award path, `solicitation-review`) from `operator` (the LLO named up front in the opp's `inputs/`, legal with **Phase 8 `skipped`**, and explicitly forbidden from carrying a fabricated `solicitation` block). The entry guard's FATAL message branches on whether Phase 8 ran, because the remedies differ. `selected_llo` also gained the handover record — `program_application_id` (UNRECOVERABLE if not captured at POST time: `connect_list_invites` is a blind read returning `[]` even for an accepted invite), the LLO's `opportunity_id`/`url`, and the Gmail thread + message ids — which previously had no typed home and landed in an invented top-level key nothing read. It renders as § LLO handover in the run README. (2) **New step 2b creates the LLO's delivery opportunity here**, after acceptance, on freshly-copied apps (`commcare_linked_app_copy`, same domain + `linked: false`) — Phase 4 cannot, since it runs before any invite exists. The create's own rejection IS the acceptance check; no readable application-status surface exists. Halts rather than clamping when `start_date` falls outside the program window. | ACE team |
| 2026-10-18 | Steps 2/2a/2b (invite, PM accept, fresh app copies, the LLO's opportunity and payment units) moved into the standalone `connect-partner-opp-create`, so a partner opportunity can be added to any existing program with explicit ids; this skill now calls it (#3148 batch 4) | ACE |

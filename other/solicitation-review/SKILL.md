---
name: solicitation-review
description: >
  Score a solicitation's responses and recommend an awardee; after human approval, record the
  award. Needs a solicitation with responses.
disable-model-invocation: false
---

# Solicitation Review

Manual skill — never runs in default `/ace:run`. Only via:

```
/ace:step solicitation-review --opp <opp-name>
```

This is the only skill that calls `award_response` (irreversible) and the
only skill that populates `selected_llo` (which gates Phase 9). Writes to
`phases.solicitation-management.products.selected_llo` in the current run's
`run_state.yaml` only.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `--solicitation-id` | the call being reviewed and awarded | default: the run's `products.solicitation.solicitation_id`; outside a run, explicit |
| `--rubric <doc id>` | evaluation criteria | default: the run's `solicitation-create_published.md`; else the call's own criteria via `get_solicitation` |
| responses | what is scored | default: the run's `solicitation-monitor_responses/*.md`; else live `list_responses` + `get_response` |
| `--out-folder-id` | where rubric / recommendation / award record go | default: the run's `8-solicitation-management/` |
| `optional_steps.ace_winner` | write `selected_llo.synthetic_winner: true` | default: the run's `optional_steps` block; outside a run, absent |

The HITL award gate (Step 6) is unchanged in every mode: the human approves at
level 0 before `award_response`. Step 10's `run_state.yaml` write happens only
when a run is bound; outside a run, record the award (response id, org, budget,
`awardee_notified`) in the program context doc's Decisions.

Default resolution inside a run — read from the current run's `run_state.yaml.phases.solicitation-management.products.solicitation`:

- `solicitation_id`
- `public_url`
- `labs_program_id` — labs **integer** program ID cached by
  `solicitation-create` (also available at
  `opp.yaml.connect.program.connect_int_id` as the durable opp-level
  cache). Used only as the optional `list_solicitations` filter.
  `get_solicitation`, `list_responses`, `get_response`,
  `update_solicitation` and `award_response` do NOT need it, even for a
  private (`is_public: false`) call: since connect-labs#2567, labs
  authorizes them by owning-org membership, and the live schema marks
  `program_id` "Accepted for compatibility; not needed" (2026-10-18). Note:
  this is **not** the Connect program UUID. If both locations are empty
  and you need the filter, fall back to the resolution recipe in
  `solicitation-create` step 5 (`labs_context` lookup by program name).
- `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-create_published.md` (rubric)
- `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-monitor_responses/*.md` (all responses)

## Process

1. **Pull all responses fresh.** Call:

   ```
   mcp__connect-labs__list_responses(solicitation_id: <id>)
   ```

   For each response, call `get_response` even if the local cache exists
   (responses may have been edited).

2. **Score each response.** Read the rubric from `published.md` (the
   `evaluation_criteria` block). For each response, score every criterion
   on its declared scale (typically 1-10) and compute a weighted total.
   Use the same archetype-aware judgment that
   `solicitation-create-eval` uses on the rubric itself.

3. **Optionally write to labs.** For each response, call:

   ```
   mcp__connect-labs__create_review(
     public_record_acknowledged: true,
     response_id: <id>,
     llo_entity_id: <the response's llo_entity_id, or "individual">,
     criteria_scores: { <criterion_id>: <score>, ... },
     notes: "<reasoning>",
     demonstration: true   # ONLY for the ACE winner on an ace_winner run -- see below
   )
   ```

   This puts ACE's scores in the labs audit trail. Idempotent — call
   `list_reviews` first and skip if a review by `ace@dimagi-ai.com`
   already exists for this response.

   **`demonstration: true` — the ACE winner only.** Labs refuses a review or
   award of a response from the caller's own side, and the rule keys on the
   USER: ace@ belongs to the winner org (`connect_orgs.llo_org`), so every
   plain call on the ACE winner's response is refused (ace#3257). Labs'
   one exception is a demonstration: honoured only when the response was
   created `synthetic` (by `solicitation-seed-responses`), the call is
   unlisted, and the caller manages the call. Pass it **only when BOTH** hold:
   `optional_steps.ace_winner` is on (`isOptionalStepEnabled(runState,
   'ace_winner')`), **and** this response is the seeded ACE winner (the
   roster's winner row: `llo_entity_id` = `llo_org`, `synthetic: true` on
   `get_response`). Never on any other response, never on a real call, never
   outside an `ace_winner` run. If the winner's `get_response` reads
   `synthetic: false` it was filed before labs had the marker and can never be
   demonstration-awarded: re-run `solicitation-seed-responses` (it files a
   fresh, marked winner) before reviewing it.

4. **Write `scoring-rubric.md`.** Save the per-response, per-criterion
   scores to:

   ```
   ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-review_scoring-rubric.md
   ```

   Markdown table per response, with columns: criterion, weight, score
   (0-10), notes.

5. **Write `recommendation.md`.** Save:

   ```
   ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-review_recommendation.md
   ```

   Body: ranked list of candidates with reasoning. Top candidate gets a
   `> Recommended awardee` callout block. Include differentiators (what
   sets the top candidate apart from #2/#3) and any flagged-as-unscoreable
   responses.

5b. **Required-before gate — a HARD STOP (owner decision 2026-10-04).** Before
   asking anyone to approve an award, call:

   ```
   mcp__ace-decisions__decisions_open_asks(
     runFolderId: <run folder id>, opportunity: <opp>, run_id: <run-id>,
     neededBy: 'award',
     solicitationAnswered: [<question ids the top-ranked response answered, non-empty>]
   )
   ```

   If `requiredBefore` is non-empty, **do not present the award prompt and do
   not call `award_response`** — not even if the human asks for it in this
   session. Each entry is a decision row with `review_ask: required-before`
   and `needed_by: award`: the design says its answer changes who may be
   awarded or what the award commits to, and nobody has answered it. Add a
   `> Award blocked` callout to `recommendation.md` listing each entry's
   question, owner and `answer_channel`, write `award-record.md` with
   `status: blocked` and the same list, and stop. The way to clear it is to
   ANSWER the ask: the owner rules in the ace-web decisions review (saved to
   `inputs/decision-overrides.yaml` with `decided_by`), or — for an ask whose
   `answer_channel` is `solicitation:<question-id>` — the chosen response
   answers that question (those land in `closedBySolicitation`; name them in
   `recommendation.md` with the response's answer quoted). Then re-run this
   skill. A `recommended-confirmation` ask never blocks the award. Contract:
   `docs/decisions-contract.md § Open asks`.

6. **HITL gate.** First resolve the **awardee's Connect organisation id**
   (`org_id`). This is the Connect org that will hold the partner's
   opportunity in Phase 9. Labs stores it on the response as "the Connect
   organisation id the awarder named for the contract". It is an
   owner-only field, so `get_response` returns it to the call's owner, and it
   is usually empty unless the response was created with one. Use the
   response's `org_id` when it is set. Otherwise propose the org from the
   response (`llo_entity_id` / `org_name`) and have the human confirm or
   supply the id in the same reply. Never invent one: Phase 9's
   `connect_send_llo_invite` needs a real Connect org.

   Present `recommendation.md` to the human and ask:

   > "Confirm awarding response_id=<top> (reward_budget <amount>
   > <currency>) to <org_name>, Connect org `<org_id>`? Labs will email the
   > awardee if labs email is on, and an award cannot be undone or repeated.
   > Reply with `award <response_id> <amount> <org_id>` to confirm, or
   > `cancel` to halt."

   Wait for an explicit reply. **Do not call `award_response` without
   one.** If the human picks a different response_id, amount or org, use
   those. If they pick a different response, re-run step 5b with
   THAT response's answered question ids first.

7. **Call `award_response`.** On confirm (the live schema requires
   `response_id`, `reward_budget` and `org_id`; there is no `amount`
   field, and extra keys are rejected — ace#3146):

   ```
   mcp__connect-labs__award_response(
     response_id: <chosen>,
     reward_budget: <approved amount, integer, in the call's currency>,
     org_id: <confirmed Connect organisation id>,
     fund_id: <labs fund id>,   # optional: only when the award should append a fund allocation
     demonstration: true        # ONLY when optional_steps.ace_winner AND <chosen> is the seeded ACE winner
   )
   ```

   **`demonstration: true`** follows exactly Step 3's rule: only on an
   `ace_winner` run, only for the seeded ACE winner's `synthetic` response,
   never for a real award. Labs then records `demonstration_award: true`,
   emails nobody and allocates no fund (so leave `fund_id` out — labs
   refuses it). Labs refuses `demonstration: true` on any response that is not
   synthetic, on a listed call, or to a caller who cannot manage the call, and
   refuses a plain award of a synthetic response — neither ever falls back to
   the other. Say "demonstration award" in the Step 6 prompt on such a run.

   The call marks the response `awarded`, and moves an `active` or `closed`
   solicitation to `awarded` itself. It emails the awardee only when labs
   email is on (`awardee_notified` in the result says whether it was sent).
   A response that is already awarded is refused with `FAILED_PRECONDITION`,
   and you get no second email or allocation. With `fund_id`, the fund is
   checked first; if the allocation then fails, the award still stands and
   the result carries `allocation_error`. Do NOT retry, because a retry is
   refused as already awarded.

8. **Write `award-record.md`.**

   ```
   ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-review_award-record.md
   ```

   Body: `response_id`, `awarded_at`, `awarded_org_slug`,
   `awarded_org_name`, `awarded_contact_email`, `award_amount` (the
   `reward_budget` sent), `org_id`, `awardee_notified` (from the result, so a
   reader knows whether labs emailed the awardee), `demonstration_award`
   (from the result), and `allocation_error` when present. On labs-side error: `status: failed` + the error envelope.

9. **Confirm the labs-side status is `awarded`.** `award_response` already
   flips an `active`/`closed` solicitation to `awarded`. Read it back with
   `get_solicitation`, and only if it does not say `awarded` call:

   ```
   mcp__connect-labs__update_solicitation(
     solicitation_id: <id>,
     update_data: { status: 'awarded' },
   )
   ```

   No `program_id`, even for a private call: the owning org's members
   may update it, and the live schema marks `program_id` "Accepted for
   compatibility; not needed". Treat 4xx here as non-fatal:
   `award_response` already succeeded, so write a
   `status_update_failed` note into `award-record.md` and continue.
   The award is durable; the labs-side status flip can be retried
   out-of-band via the labs UI.

10. **Populate `selected_llo` and update solicitation status.** Only
    on a successful award, and only when a run is bound (outside a run see
    § Inputs), write to the current run's
    `run_state.yaml` via `update_yaml_file` + `merge: 'deep'`.
    Read the existing `products.solicitation` block first, set
    `status: awarded` and populate the `awarded.*` block, then write
    both `products.solicitation` and `products.selected_llo` in one
    consolidated payload. `deep` merges these under the
    `solicitation-management` phase block while preserving its `status`,
    `steps`, etc. — `two-level` would replace the whole phase block
    wholesale and drop them (#572/#587):

    ```yaml
    phases:
      solicitation-management:
        products:
          solicitation:
            # preserved from solicitation-create + the read above...
            status: awarded
            awarded:
              response_id: <chosen>
              awarded_at: <ISO>
              awarded_org_slug: <returned>
              awarded_org_name: <returned>
              awarded_contact_email: <returned>
              award_amount: <approved $>
          selected_llo:
            org_slug: <returned>
            contact_email: <returned>
            source: solicitation
            response_id: <chosen>
            synthetic_winner: true   # ONLY when optional_steps.ace_winner — omit otherwise
    ```

    **The ACE-owned winner (`optional_steps.ace_winner`).** When the run
    enabled `ace_winner` (`isOptionalStepEnabled(runState, 'ace_winner')`,
    `lib/optional-steps.ts`), the awarded response is the one
    `solicitation-seed-responses` filed for ACE's own winner org
    (`connect_orgs.llo_org`, resolved only by `lib/connect-orgs.ts`).
    Write `selected_llo.synthetic_winner: true`. Every later consumer
    (`opp-closeout`, `llo-feedback`, `timeline-monitor`, Phase 9's simulated
    mode) reads that flag and sends nothing outbound, so the award never
    reaches a real LLO. Never set it on a real award. On an `ace_winner`
    run the orchestrator runs this skill inline at level 0, so the Step 6
    approval still reaches the operator. The award is still irreversible
    and still real on labs, so the HITL gate is unchanged.

    **No write to `opp.yaml.selected_llo` or `opp.yaml.solicitation`.**
    These are per-run only. Phase 9 (`llo-onboarding`) reads
    `selected_llo` from the same `run_state.yaml`.

## Error handling

- **Required-before ask unanswered (step 5b)**: do not call
  `award_response`; record `status: blocked` with the open asks. This is
  not an error to retry around — the ask must be answered first.
- **HITL gate timeout / no reply**: do not call `award_response`. Do not
  mutate `run_state.yaml` or `opp.yaml`. Exit cleanly so the human can
  re-run the skill.
- **Human replies `cancel`**: halt; do not write `award-record.md`.
- **`award_response` returns 4xx after approval**: write `award-record.md`
  with `status: failed` and the error envelope. **Do not** populate
  `selected_llo` (Phase 9 stays gated). Surface the error to the human
  and suggest contacting a labs admin if the award call must succeed
  out-of-band.
- **`list_reviews` shows ACE already reviewed all responses**: skip the
  scoring step (we don't re-score), proceed to step 4 from the existing
  reviews.
- **No responses at all**: write `recommendation.md` with `status: no_responses`,
  do not call `award_response`. Suggest extending the deadline (future
  `solicitation-monitor --extend-deadline` skill).

## Output

- `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-review_scoring-rubric.md`
- `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-review_recommendation.md`
- `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/solicitation-review_award-record.md`
- `phases.solicitation-management.products.selected_llo.*` populated (only on success; per-run only)
- `phases.solicitation-management.products.solicitation.{status: awarded, awarded.*}` populated (only on success; per-run only)

## MCP Tools Used

- `connect-labs`: `list_responses`, `get_response`, `list_reviews`,
  `create_review`, `award_response` (`response_id` + `reward_budget` +
  `org_id`, optional `fund_id`), `get_solicitation`, `update_solicitation`
  (fallback status flip to `awarded`; no `program_id` needed)
- `ace-gdrive`: `drive_create_file`, `drive_update_file`,
  `drive_read_file`, `drive_list_folder`
- `ace-decisions`: `decisions_open_asks` (step 5b — the required-before
  award gate)

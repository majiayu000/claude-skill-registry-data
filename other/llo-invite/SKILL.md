---
name: llo-invite
description: >
  Email a PDD's named candidate LLOs the public solicitation link. Opt-in only: a no-op unless
  explicitly enabled. Needs a published solicitation.
disable-model-invocation: false
---

# LLO Invite

Phase 8 default-run skill. Runs after `solicitation-create` has populated
`phases.solicitation-management.products.solicitation.public_url` in the
current run's `run_state.yaml`. Sends each PDD-named candidate LLO an
email containing the solicitation URL, deadline, and a scope summary.

This skill replaces the previous Phase-8 (was Phase-7) `llo-invite` that
prepared a Connect-side invite roster. The Connect program-level invite
(`connect_send_llo_invite`) is now `llo-onboarding`'s responsibility and
fires only for the awardee.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `candidates` | the named candidate LLOs (name + contact email) | explicit arg; default: the PDD's `## LLO Preference` → Preferred LLOs (`ACE/<opp-name>/inputs/pdd.md`) |
| `solicitation_url` | the link each candidate receives | explicit arg; default: the current run's run_state `phases.solicitation-management.products.solicitation.public_url` |
| `deadline` | the response deadline named in the email | explicit arg; default: run_state `…products.solicitation.deadline` |
| `program_name` | the opp display name in the email | explicit arg; default: `opp.yaml` |

The opt-in gate (Step 0) applies however the inputs arrive: an explicit `candidates` list is not consent to send.

## Default: publish-only (standing operator directive 2026-05-31)

This skill sends real email to real external organizations, so it is
**OFF by default.** It runs only when the operator has explicitly opted
into candidate outreach for this run via either:

- `/ace:run --invite-candidates` (the orchestrator threads the flag into
  the Phase 8 dispatch prompt), or
- `ACE_SOLICITATION_INVITE_CANDIDATES=1` in the resolved `.env`.

Absent that signal — the normal case, including every dogfood / `is_test`
run — the solicitation is published (by `solicitation-create`) and this
skill is a **publish-only no-op**: it sends nothing, writes a
`Status: skipped (publish-only default)` invitations log, and exits
successfully. Do NOT pause to ask; publish-only is the intended path.
This default holds until the skills are explicitly changed to enable
candidate outreach. See `agents/ace-orchestrator.md § Modes → Phase 6→7
transition`.

## Process

0. **Opt-in gate.** If neither `--invite-candidates` nor
   `ACE_SOLICITATION_INVITE_CANDIDATES=1` is set, write
   `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/llo-invite_invitations.md`
   with `Status: skipped (publish-only default — no candidate emails sent)`,
   the `public_url` for the record, and exit successfully. Send NO email.
   Only when the opt-in signal IS present do Steps 1–4 below run.

1. **Read `Preferred LLOs`** from the PDD's `## LLO Preference` section.
   Parse names + contact emails + organization slugs (each entry should
   declare all three; missing fields disqualify the entry).

2. **If empty (or all entries malformed):** write
   `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/llo-invite_invitations.md`:

   ```markdown
   # Solicitation Invitations

   Status: empty (long-term solicitation flow — no PDD-named candidates).

   The solicitation is listed at <public_url>, which requires a labs
   login by design — it is not anonymously readable. With no PDD-named
   candidates, no one can reach it: expect zero responses unless the
   operator distributes it another way.
   ```

   Exit successfully.

3. **For each preferred LLO**, compose an email:

   ```
   Subject: Invitation to respond — <pdd.title>
   To: <preferred_llo.contact_email>

   Hi <name>,

   <Dimagi greeting + program summary, 2-3 sentences from PDD>

   We are inviting your organization to respond to a solicitation for
   <pdd.title>. The full description, scope of work, and response template
   are at:

       <public_url>

   Responses are due by <deadline> (UTC).

   To respond, sign into labs.connect.dimagi.com with your organization
   account, open the solicitation linked above, and click "Submit
   Response."

   Questions? Reply to this email.

   — The ACE team
   ace@dimagi-ai.com
   ```

   Send via the `email-communicator` skill (which uses ACE's Gmail
   account `ace@dimagi-ai.com`).

4. **Log every send** to
   `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/llo-invite_invitations.md`:

   ```markdown
   # Solicitation Invitations

   Solicitation: <public_url>
   Deadline: <deadline>
   Sent at: <ISO-8601 timestamp of this run>

   ## Recipients

   | Recipient | Org | Sent at | Status |
   |---|---|---|---|
   | <name>    | <org> | <ISO>  | sent |
   | <name>    | <org> | <ISO>  | failed: <reason> |
   ```

## Review-mode gate

Reaching this section means the Step 0 opt-in gate already passed
(`--invite-candidates` / `ACE_SOLICITATION_INVITE_CANDIDATES` is set) —
otherwise the skill no-op'd and never got here. With opt-in set: under
`/ace:run --review` mode, present the prepared email list to the human
before sending and pause; under auto mode, send (the opt-in signal IS
the operator's go-ahead, and these emails are non-binding "please
consider applying" notes, not commitments). Without opt-in there is no
send in any mode — see § Default: publish-only.

## Error handling

- Per-recipient email failure: log `status: failed: <reason>` for that
  row, continue with the rest.
- All recipients fail: halt with a surfaced error pointing at the Gmail
  config in `/ace:doctor`.
- PDD has no `Preferred LLOs`: no-op per Step 2 above.
- Resolved `public_url` empty or resolved `status != open` (read from
  the current run's `products.solicitation`): halt with "run
  solicitation-create first" message.

## Output

- `ACE/<opp-name>/runs/<run-id>/8-solicitation-management/llo-invite_invitations.md` — recipient log

## MCP Tools Used

- (Indirectly via `email-communicator`): GOG CLI for Gmail send.
- `ace-gdrive`: `drive_create_file`, `drive_read_file`,
  `drive_update_file`.

No Connect or Connect-Labs API calls in this skill.

## Mode Behavior

The opt-in gate (Step 0) runs FIRST regardless of mode — without
`--invite-candidates` / `ACE_SOLICITATION_INVITE_CANDIDATES` this skill
is a publish-only no-op in every mode. The rows below describe behavior
**once opt-in is set**:

- **Auto:** Send all invitations.
- **Review:** Pause after composing, present recipient list + sample
  email body for approval.
- **Dry-run:** Steps 1-3 (no send), write `invitations.md` with
  `Status: dry-run`.

## Terminology

**The platform is `Connect`, never `CommCare Connect`** — in every word this skill
puts in front of a human. The full rule, including the carve-outs for CommCare the
mobile app, CommCare HQ and code-level identifiers, is
[`skills/_terminology.md`](../_terminology.md). Read it before writing prose; it is
binding on this skill's output.

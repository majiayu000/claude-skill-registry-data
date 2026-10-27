---
name: release-run
description: >
  Release a run to outside reviewers: execute the release plan that
  validate-release-readiness wrote — the HQ, Connect, Drive and ace-web grants
  and the emails, in order — and nothing else. Approval-gated. Makes no
  content changes.
disable-model-invocation: true
---

# release-run

`/ace:release <workspace>/<opp>/<run-id> (--reviewers <email[:role]>,... | --from-thread <id>) [--cc <staff@dimagi.com>,...] [--waive <blocker-id>=<reason>]... [--forward-source [--allow-cross-workspace-forward]] [--allow-shared connect]`
`/ace:release <workspace>/<opp>/<run-id> --revoke-shared`

**Releasing is sharing, and only sharing.** Owner decision (Jonathan,
2026-10-03): *"when validate release readiness passes it means executing
release doesn't change anything other than sharing externally."* Every check
and every content change — the gates, the HQ plan, the review-page audit, the
repairs, which systems each reviewer may be granted, which Drive documents need
sharing, the text of every email — happened in
`/ace:validate-release-readiness` (`skills/validate-release-readiness`), which
wrote them into the run's verdict as a hashed **release plan**. This skill
re-reads that plan, refuses it on any mismatch, shows it for approval, executes
its share actions in order, proves each by read-back, and records the release.

It makes **NO content changes**: no audit, no polish, no gate re-runs, no doc
edits, no decisions or run_state changes beyond the `released:` record. The
only other write is the send record every ACE email owes — one
`release-run_comms-log.md` row per email sent (ace#2780). If something looks
wrong, STOP and re-validate; never fix it here.
*Enforced:* `test/skills/release-run-shares-only.test.ts`.

Spec: ace-web `docs/specs/2026-09-28-clone-and-release-design.md` § E2.

## Inputs

- `<workspace>/<opp>/<run-id>` — the run to release, normally a clone.
- `--reviewers` / `--from-thread` — **the same reviewers given to the
  validation** (from a thread: the same derivation, `$RC thread-recipients
  --participants "<addr>,…" --workspace <ws> --opp <opp>` — partner-domain
  participants AND the thread's Dimagi staff are reviewers, ace#2720). The gate
  compares them exactly — one extra, one missing or one different role is a
  refusal.
- `--cc` — **the same Dimagi staff the validation copied** (ace#2706), only if
  the operator passed one explicitly — a thread never derives it. They
  get every email and no grant. The gate compares the list exactly; a cc added,
  dropped or changed at release is a refusal, never adapted to.
- `--waive <blocker-id>=<reason>` — **the same waivers the validation
  applied** (ace#2707), id and reason verbatim. A waiver releases past an
  eval-quality blocker; it is not decided here. The gate compares them exactly;
  a waiver added, dropped or reworded at release is a refusal.
- `--forward-source`, `--allow-cross-workspace-forward`, `--allow-shared
  connect` — must be exactly the flags the validation was run with (they are
  plan options). They do not change what is executed; the plan does.

Auth: `ACE_WEB_BASE_URL` + `ACE_WEB_PAT_TOKEN`; the PAT's owner must be an
owner of `<workspace>`. `$RC` is
`node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/release-readiness.ts"`;
`$FLAGS` is `--reviewers "<list>"` plus `--cc "<list>"` when given, plus each `--waive "<id>=<reason>"` given, plus the flags given.

## Revoke mode (`--revoke-shared`)

Un-sharing, not releasing: run when a review on the shared orgs ends, or once
the run has been re-cloned into the partner's own orgs. Bind (Step 1), read
`released.shared_grants` from the run's `run_state.yaml`, show them all for
approval as one list, then for each row not yet revoked:
`connect_remove_org_member(organization_slug: <org>, email)`. It reads back
both member tables itself; `removed` / `invite-revoked` / `not-present` are all
a revoked grant. Write each row back with `revoked_at` (the whole
`released.shared_grants` array via `localFilePath` — arrays are replaced
wholesale by every merge mode). Report per row. Nothing else runs in this mode.

## Step 1 — Bind and gate

1. `"$CLAUDE_PLUGIN_ROOT/bin/ace-bind" <workspace>/<opp>` — every grant below is
   then checked against this opp's tenancy by the tenancy guard.
2. Resolve the run folder (`resolve_opp_path`), download
   `release-readiness_verdict.yaml` and `run_state.yaml` (`drive_read_file`
   `writeToPath`; an absent verdict is a refusal), and inventory the run:
   ```bash
   $RC inventory --run-folder <run folder id> --out inventory.json
   $RC gate --workspace <ws> --opp <opp> --run <run-id> --verdict release-readiness_verdict.yaml \
     --inventory inventory.json --run-state run_state.yaml $FLAGS
   ```
   Exit 0 only when the verdict is a READY release-readiness verdict for THIS
   workspace/opp/run, not a dry run, nothing in the run was written after it,
   `run_state.yaml` hashes the same as when validated, the plan matches its
   hash, and the reviewers, cc, waivers and flags are exactly the validated ones.
   Otherwise **STOP**: print the gate's reason and tell the operator to run
   `/ace:validate-release-readiness <workspace>/<opp>/<run-id> $FLAGS`. Do not
   adapt to a mismatch — not by dropping a reviewer, not by skipping an action,
   not by fixing anything.

## Step 2 — Show the plan, approve once

`$RC plan-show --verdict release-readiness_verdict.yaml` prints the grant table
(Reviewer × HQ / Connect / Labs / OCS / ace-web), the Drive shares, whether the
source link is forwarded (and, if so, whether it is another workspace's page),
every WAIVED readiness blocker (its failing grade, the reason, who waived it
and when — the operator approves releasing past it here), the ordered steps,
and the full text of every email. Show it verbatim and
`AskUserQuestion`: **Release — execute exactly this** / **Stop**. Nothing is
shared before *Release*. Then re-run the Step 1 gate (fresh inventory, fresh
run_state) — the approval may have taken a while — and stop on a non-zero exit.

## Step 3 — Execute the plan, in order, nothing else

`$RC plan-actions --verdict release-readiness_verdict.yaml` lists the actions
in `step` order. Execute each one exactly as written — its `target`, `email`
and `role` come from the plan, never re-derived:

| `kind` | Call | Read-back (the evidence) |
|---|---|---|
| `hq_invite` | `commcare_invite_web_user(domain: target, email, role)` | `commcare_list_users` / the invite list shows the email on `role` |
| `connect_org_member` | `connect_add_org_member(organization_slug: target, email, role)` | the call IS its read-back (member + pending tables before/after): its `status` |
| `drive_share` | `drive_set_anyone_with_link(fileId: target, role)` | an anonymous `curl -sI` of `url` no longer lands on a sign-in page |
| `forward_source` | `POST ${ACE_WEB_BASE_URL}/api/w/<workspace>/opps/<opp>/runs/<run-id>/release` `{"forward_source": true}` | an anonymous `curl -sI` of the source summary API is `307` with a `Location` naming this run |
| `ace_web_role` | `PATCH ${ACE_WEB_BASE_URL}/api/workspaces/<target>/members/<user_id>` `{"role": "<role>"}` — a member below editor, raised (an invite would 409) | the response's `role` is `<role>` |
| `ace_web_invite` | `POST ${ACE_WEB_BASE_URL}/api/workspaces/<target>/members/invite` `{"email", "role"}` → `token`. A **409 `"<email> is already a <role> of this workspace"`** with `<role>` editor/admin/owner is a SATISFIED grant, status `already-member` (the reviewer joined after validation — e.g. accepted an earlier invite) | the workspace's pending invites list the email, and the accept link is `${ACE_WEB_BASE_URL}/invite/<token>`; for `already-member`, the 409 body plus `GET …/api/workspaces/<target>/members` showing the email at that role |
| `email` | `$RC email-body --verdict … --to <email> --accept-link <that link> --out body.txt --subject-out subject.txt` — or, when the plan's email is the existing-member variant (`plan-show` marks it *already a member: no accept link*) or the invite came back `already-member`, `--already-member <role>` in place of `--accept-link`; then `bin/ace-email --to <email> --cc "<the action's cc, comma-joined>" --subject-file subject.txt --body-file body.txt` (omit `--cc` when the action's `cc` is empty) | the send's JSON (`message_id`, `thread_id`) |

`email-body` fills in the accept link and changes nothing else; it refuses a
link that is not an ace-web invite link, and refuses an accept link for an
existing-member email. `--already-member <role>` (ace#2770) sends the
existing-member email — step 1 is "sign in at the run's members page", no
link — exactly as planned, or, for a reviewer planned for an invite who
answered 409, the planned email with only step 1 swapped (the swap is printed
in `plan-show`, so it was approved). It refuses a role below editor: a 409
naming `viewer` is NOT a satisfied grant — that reviewer is `NOT DONE`, and
re-validating plans the `ace_web_role` raise. The cc is the plan's — read from the
action (`plan-actions`) or `email-body`'s JSON, never typed from memory or the
thread. The email for a reviewer is sent only
after that reviewer's grants above it succeeded. A failed step is `NOT DONE`
with its evidence: stop there, record what was done (Step 4), and report — do
not retry with different arguments, and do not continue past a failed grant to
that reviewer's email.

Nothing outside this table is called. Labs needs no call: the clone REBUILT
the dashboards in the run's own labs program and linked its labs workspace to
the clone's Connect orgs (`clone-to-new-workspace` § 4c, ace#3020), so the
`connect_org_member` grant above IS the Labs grant. OCS is the public chat link
in the email.

## Step 4 — Record (the only run writes: the release record and the send log)

```bash
curl -sS -X POST -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" \
  -H "Content-Type: application/json" -d '{"reviewers": ["a@x.org", ...]}' \
  "${ACE_WEB_BASE_URL%/}/api/w/<workspace>/opps/<opp>/runs/<run-id>/release"
```

Then `update_yaml_file(merge: "deep")` on the run's `run_state.yaml` with ONLY
the `released:` key:
`released: {at, by, to: [emails], plan_hash, steps: [{step, id, status, evidence}]}`,
plus `released.shared_grants: [{system: connect, org, email, role, at}]` for
every executed action with `shared: true` — the revocation checklist for
`--revoke-shared`. No other key is written. (This write makes the verdict stale
on purpose: a second release needs a fresh validation.)

Then log the sends: `release-run_comms-log.md` at the **run root** — the run
folder itself, not a `<N>-<phase>/` folder, because a release belongs to no
phase (ace#2780). `email-communicator` step 7 requires every send to log its
`thread_id`, and `inbox-triage` §b.1 routes a reviewer's reply by matching it
here; without this row the reply is routable only by URLs in the quoted body.
One markdown table row per `email` action that was SENT, from Step 3's send
JSON — the gist only, never the body:

```markdown
| date (UTC) | thread_id | message_id | to | cc | gist |
|---|---|---|---|---|---|
| 2026-10-07T14:02Z | 19a… | 19a… | reviewer@partner.org | staff@dimagi.com | release invite: run page + ace-web accept link, plan <plan_hash> |
```

Write it to a local file and append, never overwrite: first
`drive_create_file(name: "release-run_comms-log.md", parentFolderId: <run folder id>, localFilePath, expectAbsent: true)`
with the header plus the new rows. A refusal means a log already exists (an
earlier release or a hand-written one) — that is the append path, not an
error: `drive_read_file(fileId: <the refused file's id>, writeToPath)`, add the
new rows to the end of its table, and
`drive_update_file(fileId, localFilePath, ifMatchRevisionId: <the read's revisionVersion>)`;
on `revision_conflict`, re-read and append again. Write nothing else to it.

## Report

Per reviewer × system: `granted` (with read-back), `already-member` (ace-web:
no call was needed, or the invite answered 409 at editor or above), `granted — SHARED, revoke
later` (listed again at the end as the revocation checklist), `NOT GRANTED —
<reason from the plan>`, `public link (no account)` for OCS, or `NOT DONE` +
evidence; the Drive shares; whether the source link now forwards; each email's
`thread_id` (each also a row in `release-run_comms-log.md`); and the plan
hash executed.

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-10-03 | Share-only release: executes the validated plan's share actions and nothing else (owner decision, ace#2620). | ACE team |
| 2026-10-05 | `--waive` (ace#2707): the plan's waived eval blockers are shown in the approval prompt; the gate refuses waivers that differ from the validated ones. | ACE team |
| 2026-10-05 | `--from-thread` derives Dimagi staff on the thread as **reviewers** (workspace invite + grants + own email), never cc; `--cc` is an explicit opt-in only (ace#2720, operator correction: "we want dimagi people to be invited into the workspace if they are on the project"). | ACE team |
| 2026-10-05 | `--cc` (ace#2706): each `email` action sends with the plan's `cc` (Dimagi staff, no grant) via `bin/ace-email --cc`; the gate refuses a cc that differs from the validated one; `--from-thread` derives reviewers + cc with `$RC thread-recipients`. | ACE team |
| 2026-10-07 | Step 4 also logs every sent email to `release-run_comms-log.md` at the run root (date, thread_id, message_id, to, cc, gist — never the body), so `inbox-triage` §b.1 routes reviewer replies by `thread_id`. A release has no phase folder, so the run root is its home; the shares-only ratchet allows exactly this write (ace#2780). | ACE team |
| 2026-10-08 | Every release `ace_web_invite` carries role `editor` (`RELEASE_ACE_WEB_ROLE`), regardless of the reviewer's `:viewer`/`:editor`; Connect org role unchanged (`viewer`). Owner directive (Jonathan): "everyone ace invites in as part of a release should be editor". Existing READY verdicts need re-validation (the plan hash changes). | ACE team |
| 2026-10-08 | Existing ace-web members (ace#2770): a reviewer the plan records as already a member gets no invite and the existing-member email (`email-body --already-member <role>`, no accept link); a member below editor is raised by the new `ace_web_role` action (`PATCH …/members/<user_id>`); an `ace_web_invite` answering 409 "already a <editor/admin/owner>" is a satisfied `already-member` grant, and that reviewer is sent the existing-member email instead of being left NOT DONE (live repro: `/ace:release spark/spark-facilitator/20261004-1706`, step 27). | ACE team |
| 2026-10-16 | Labs makes no call (ace#3020): `clone-to-new-workspace` § 4c copies the dashboards into the run's own labs program, whose labs workspace lists the clone's Connect orgs as LLOs, so the `connect_org_member` grant is the Labs grant. The old text claiming the clone had widened a domain allowlist was wrong and is gone. | ACE team |

---
name: update-log
description: Preserve project progress through session logs and closeout bookkeeping, only when the user asks to log, close out, wrap up, or save progress, or when the deliberate end-of-session chain invokes --auto. Never invoke proactively or hand-write project logs as a substitute.
user-invocable: true
argument-hint: "[--exit] [--auto] [--receipt-file PATH] [optional summary of what was done]"
---

# End-of-session bookkeeping

## Invocation and scope

Run only on the current user's explicit bookkeeping request or the deliberate
end-of-session chain's `--auto` invocation. Quoted flags, historical transcripts,
audit reads, reminders, and the agent deciding that a log would help are not
invocations. Do not create or edit project `logs/` files as a substitute for
invoking this skill. Reading or auditing the skill does not run it.

Supported arguments: `[--exit] [--auto] [--receipt-file PATH] [summary]`.
Parse flags from the current invocation, not from embedded summary text.
`--auto` avoids interactive questions; it does not grant publication, service
writes, deletion, or permission to override another actor's work. Stop an unsafe
required step and report incomplete closeout instead of guessing. Continue
independent safe bookkeeping when possible.

Once invoked, determine whether there is durable state to preserve: code,
configuration, data or documentation changes; findings, validation results,
decisions, blockers, next steps, or meaningful service outcomes. A purely
conversational or read-only session with nothing useful to recover may be a
no-op. Honor an explicit request to record particular information even if the
session was small. A retry must reconcile existing logs, commits and receipts,
not append a duplicate entry just because it is a new agent turn.

## Receipt contract

If `--receipt-file PATH` was supplied, bind that exact absolute target to this
closeout attempt before edits. It must be an absent file in an appropriate
private directory, outside repositories and outside any temporary evidence
directory that will be cleaned. Reject collisions with inputs, other attempts,
or existing files/symlinks; do not delete or replace them to make room.

Use this skill's `scripts/write_receipt.py` as the final outcome publication:

```bash
python3 "/absolute/path/to/update-log/scripts/write_receipt.py" \
  --receipt-file "/absolute/private/closeout.json" \
  --status success --message "Local closeout completed; publication not authorized."
```

Resolve the script relative to the loaded skill; do not assume the other CLI's
installation exists. Add repeated `--evidence "/absolute/path.json"` for
successful Epoch apply receipts. The writer validates receipt syntax and
successful status, not provenance, project identity, actual commits, or
permission. Check those independently below. Receipts may embed sensitive
evidence; keep them in private storage, never a public commit. The host may
delete its receipt directory after consuming the result, including failures.
Keep durable recovery evidence outside that host-owned directory.

- Use `success` only after required edits, checks, commits and final inspections.
- Use `no-op` when no requested durable change remains, not when work was skipped
  because access or verification failed. An Epoch apply no-op is evidence about
  that transaction, not proof that the whole session had no durable changes.
- Use `failure` for incomplete required work. Explicit failure intentionally
  returns nonzero even when the failure receipt was successfully written.

The writer publishes once and refuses an existing destination. Read back the
exact receipt after execution. If writing fails or its outcome is ambiguous,
inspect the target before any retry; never overwrite a possible earlier
success with failure. Report that the gate remains unsatisfied when no matching
receipt exists. Preserve recovery evidence on uncertain or failed outcomes.

For triage no-op, change no project files and make no commit. Write the
requested no-op receipt, report that no durable changes needed recording, and
honor `--exit` only through the host's normal mechanism.

## 0. Resolve the project and baseline

1. Resolve the canonical project directory, Git worktree and repository from
   the actual session context. A nested cwd is not automatically the project
   root. Read governing instructions and declared logging conventions before
   choosing a destination. Do not infer another project's ownership from a
   shared basename or a symlink.

2. When an Epoch notes project or registered code checkout may own the work,
   use its supported resolver:

   ```bash
   python3 "/Users/pablostafforini/My Drive/Epoch/projects/shared/scripts/project_harness.py" \
     resolve --cwd "/absolute/session/directory"
   ```

   Require a successful `command: resolve`, `ok: true` result for this cwd.
   Use the returned notes `directory`, slug, primary brief and declared local
   repositories. Only `error_code: no-match` permits generic discovery; ambiguity,
   malformed results, pending recovery, invalid routing data, or an
   unavailable resolver for known Epoch work is an incomplete closeout, not a
   reason to create logs in the code checkout. Do not run unrelated recovery
   implicitly. Resolution establishes routing, not full closeout validity;
   inspect returned semantic findings without treating them as routing failure.
   On a rejected pending-recovery or reserved-output request, read the failure
   from stdout: no optional harness receipt file may have been published.

3. Before editing, snapshot relevant worktree diffs, index entries and HEADs:
   the bookkeeping repo, repositories actually touched, and declared local
   repos whose state matters to this closeout. Include dirty maps, logs,
   decisions and hook-managed files. Track session-owned changes separately
   from pre-existing or concurrent changes. Recheck preimages before each write;
   never autosave a dirty live buffer or overwrite another writer's updates.

4. Read the session map named by project convention; normally `CLAUDE.md`.
   Read sibling `AGENTS.md` too, preserving runtime-specific instructions.
   Discover log directories from explicit conventions, existing session
   pointers, or `Read first` links. A `Current focus` map without a dated
   `Latest session` pointer is an established mode, not first-run setup.
   Preserve map mode. Conflicting modes or destinations need reconciliation.

5. Check whether decision tracking already exists. Do not create it merely
   because this session involved a design choice.

### First-run setup

For resolved Epoch projects, use the tracked `logs/`, canonical Org brief and
paired maps under the notes directory. Do not add them to ignore rules.

For a generic project with no convention, use `logs/` as the local-only
default and leave new decision tracking disabled in `--auto`. In an interactive
run, ask only for choices that materially change the result and lack a safe
default: shared versus local logs, a different path, or opting into decisions.

Before creating anything, establish whether the chosen path is tracked,
ignored, outside the repository, symlinked, or Drive-synced. Gitignore is not a
privacy boundary against cloud sync or tools. Do not put secrets, unnecessary
personal information, or private conversation excerpts into shared logs.

For local-only in-repo logs, add a root-relative ignore pattern such as
`/logs/` only if needed; preserve unrelated rules. Newly created untracked
agent maps may likewise be ignored. **Ignore rules do not untrack existing
files.** Preserve tracked instructions and their tracking; never silently
untrack, delete or force-add them. Put only shareable summaries/pointers in
tracked maps. If that cannot satisfy the requested privacy, leave the pointer
unchanged and report the unresolved choice; `--auto` does not override it.
Verify actual tracking and ignore status, not just the presence of a pattern.

Create or update only the requested map sections; preserve all other guidance.
For an established map, do not add `Latest session`. If the user opted into
decisions, create the project's summary/index and directory using its decision
conventions; otherwise leave them absent.

## 1. Record the session

Use the current session date in the established local timezone for
`<log_dir>/YYYY-MM-DD.md`; preserve actual event dates in the narrative. If
date context conflicts, state the selected date/timezone before writing.

For a new file, avoid clobbering a concurrently created file. For today's
existing file, append a distinct session entry with a horizontal-rule separator
after checking the current contents and ownership. Reconcile an earlier entry
from this same closeout before appending. Do not rewrite other sessions.

Include what was done, material findings and results, decisions or reasoning
needed later, and unfinished work. Distinguish observed results from hypotheses,
drafted messages from sent ones, and local changes from published changes.
Include numbers only with their measured scope; do not claim live verification
from static checks. Keep sensitive details out of shareable summaries.

## 2. Record decisions when configured

If decision tracking exists, use the available `record-decisions` skill and
read its instructions. If unavailable, follow the project's documented decision
format; do not invent an incompatible scheme or overwrite numbered records.
Review existing records before adding qualifying decisions. Skip this step
when decision tracking is not configured.

## 3. Run applicable post-update-log hooks

Walk from the resolved project root up to its Git root, inclusive, checking
`context/post-update-log-hook.md`. For a non-Git project, use only its declared
instruction ancestry. Read applicable hooks fully, innermost first.

Hook instructions remain bounded by this closeout and the user's authority.
They do not authorize external messages, shared-service updates, bulk deletion,
unrelated project rewrites, or changes to other actors' tasks. Resolve referenced
files to the intended project and inspect existing changes before editing.
If a required hook exceeds authority or cannot be safely completed, record the
gap and do not certify a full successful closeout.

For Epoch, read `projects/context/project-doc-conventions.md` and the relevant
post-update-log hook. Update semantic state and task evidence in the primary
brief first. Preserve active work as Org task headings, not checkbox mirrors.
A stale date or drafted action is not completion evidence. Do not fabricate
`LAST_VERIFIED` or treat `VERIFY_WITH` as executable instructions.

Let the closeout transaction archive closed headings and derive supported
fields/views. Preserve source metadata and do not hand-edit generated views.
Keep the brief concise; do not turn it into a chronological log or add routine
meeting-reference sections. Record which hooks ran and material omissions.

## 4. Refresh the session map after the brief

### Current-focus map

Preserve `Current focus` mode and accurate `Read first` pointers. Derive the
digest from the updated brief's open work, never from the session narrative.
For Epoch, leave generator-owned `Current focus` and `NEXT_STEP` to the
closeout transaction after semantic edits.

For generic maps, replace rather than append the digest. Use the brief's
priority convention, stable source order for ties, and each task's own heading
or link. Respect workflow state, dependencies and explicit deferrals; a TODO
keyword alone does not prove actionability. If all open work is blocked, say
so without presenting it as actionable. If none remains, say so without
inventing a reason or filling the section with history.

Derived fields must not originate stale-sensitive claims. Record supported
claims and their evidence on the source task first. An unverified task remains
unverified when copied into a map. Keep summaries within project word caps.

### Latest-session map

For an established `Latest session` map, update only that section with a short
summary of this session and `Full details: <log_dir>/YYYY-MM-DD.md`. Do not use
an `@` import for the full log. Migrate a legacy dated-log import without
removing unrelated imports or instructions. Attribute event-dependent claims
to the time of the actual check; do not turn an old observation into present
certainty.

### Sibling maps

Determine mirror semantics from explicit project policy and the pre-edit files.
For established identical mirrors, edit the canonical map and propagate only
the intended change after checking neither file acquired foreign edits.
The project-local `bin/mirror-claude-agents`, or the dotfiles helper of that
name, may copy the whole file: use it only when whole-file mirroring is safe.
Its `--check` reports drift, not ownership or merge safety.

For intentionally different maps, edit corresponding session sections
independently and preserve their other contents; do not run the copying helper
or require byte equality. Unexpected drift in a required mirror must be
reconciled, not erased. Verify final sections and preserved baseline content.

## 4.5. Preview an Epoch closeout

Skip for generic projects. From the Epoch root, identify exact session-owned
inputs: brief, log, maps and other changed project files. Pass them with
`--path`; use `--related-path` for eligible related notes outside the project.
Omit unused options. A whole-file input must not contain another actor's hunk.
Do not list generated views as inputs.

Create an owned private evidence directory outside Drive and repositories with
`mktemp -d /tmp/epoch-closeout.XXXXXX`. Record the literal path; do not assume
shell variables survive tool calls. Use a fresh receipt filename per invocation:

```bash
python3 projects/shared/scripts/project_harness.py \
  --receipt-file "/absolute/evidence/preview.json" \
  closeout --project <slug> \
  --path projects/<slug>/<owned-file>
```

Require exit zero, `command: closeout`, the intended project and exact inputs,
`ok: true`, and status `needs-apply` or `no-op`. Inspect candidate outputs and
validation findings. The harness validates selected projects and new/worsened
findings relative to HEAD; it may retain unrelated baseline findings. Do not
describe that as an unqualified clean-corpus check.

Preview is not application. Keep its base commit and candidate binding; if
inputs or HEAD change before apply, refresh the preview and review the new
candidate. Never recover an unrelated transaction merely to clear a gate.

## 5. Commit owned changes; publish only with authority

### Work repositories first

Identify repositories actually changed by the session and relevant declared
local checkouts. Merely naming a repository does not authorize committing or
publishing its unrelated changes. Separate code/work commits from the
bookkeeping transaction: **do not commit the Epoch notes or generic bookkeeping
paths here**, because the next step owns those commits.

For each owned logical change, run relevant checks, inspect exact staged
contents and commit scope, and commit according to repository conventions.
Preserve pre-existing staged blobs and foreign hunks. Hunk staging by itself
does not isolate an ordinary commit from other already-staged files. Use the
repository's supported ownership-aware procedure; do not bypass guards or
silently clear another actor's index. If safe separation is unavailable, retain
the changes and report incomplete commit work.

Unchanged or already committed intended content is not a missing commit.
Unexpected changes require investigation; known preserved foreign changes are
not a closeout failure.

### Bookkeeping transaction

For Epoch, do not stage or commit the notes by hand. After intended work commits
and a current preview, use the same explicit input set with a fresh receipt:

```bash
python3 projects/shared/scripts/project_harness.py \
  --receipt-file "/absolute/evidence/apply.json" \
  closeout --project <slug> \
  --path projects/<slug>/<owned-file> \
  --message "Update <slug> project state" --apply
```

Require exit zero, matching command/project/inputs, `ok: true`, and status
`success` or `no-op`. For success, verify `applied: true`, the returned commit,
its exact paths and postimages, and preserved unrelated index/worktree state.
For no-op, the current interface returns `applied: false`,
`read_only: true`, and no commit even when `--apply` was used; verify the
invocation and that no intended change remains. A preview no-op alone is not
proof that apply ran. Retain the apply receipt for final evidence. Recovery
journals and rollback attempts are not permission to discard ambiguous state.

For generic projects, stage only owned shareable log/map changes, opted-in
decisions, necessary ignore rules and in-scope hook changes. Keep local-only
paths untracked and unstaged; never force-add them. Classify each intended path
as changed/staged, already committed/unchanged, deliberately local-only, or
unresolved. Investigate a missing intended change instead of treating every
absent cached path as an ignore problem. Explicitly adding an ignored file
normally fails; a broad add may simply omit it. Verify index contents directly.

Check the entire staged diff for foreign material before the normal commit.
Inspect the resulting commit and confirm intended local-only files stayed out.
Do not make an empty bookkeeping commit just to produce a hash.

### Authorized publication

`--auto` and bookkeeping alone do not authorize pushes. When publishing was
explicitly requested, bind the intended repositories, remote, destination ref
and exact commits. Inspect outgoing ancestry: pushing HEAD can include
pre-existing unrelated commits. Stop when that would exceed authority.

Use applicable repository publishing checks and the `post-push-ci` skill when
available. Verify the intended commit at the actual destination and required
CI outcome; `ahead 0` against a possibly different tracking branch is not
sufficient. Without publication authority, leave commits local and record that
fact. Without an upstream, report that limitation instead of inventing an ahead
count. Never force-push to finish closeout.

## 6. Final inspection, receipt and optional exit

Verify the log entry, map mode/pointer, decisions, applicable hooks, actual
commits and preserved baseline changes. Record any required verification or
publication gaps as incomplete. Do not equate known unrelated dirt with failure,
or local-only ahead commits with a failed unrequested push.

Write the requested final receipt with successful Epoch apply evidence only
after these checks. Name the resulting notes commit, or accurately explain the
no-op/local-only outcome; state publication authority and actual result.

Keep failed or uncertain recovery artifacts until reconciled. After a verified
successful final receipt, clean only this run's disposable evidence directory
with `trash`, provided no pending recovery journal or consumer still needs it.
Never delete the final receipt, required durable evidence, or another run's
files. With no requested final receipt, retain required evidence in appropriate
private durable storage before cleaning disposable scratch.

Report the log location, committed versus local-only outcome, and material
omissions or remaining unpublished work concisely. Put detailed per-repository
and hook evidence in the log/receipt instead of dumping routine status output.

If `--exit` was requested, use only the host's normal exit mechanism after
closeout is complete. Do not kill a terminal, agent or Emacs process. If the
host exposes no exit action, state the result and stop.

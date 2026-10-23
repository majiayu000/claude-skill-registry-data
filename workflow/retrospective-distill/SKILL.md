---
name: retrospective-distill
description: Turn completed session records into verified follow-up candidates.
---

# Retrospective distillation

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/retrospective-distill/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use when completed retrospectives or journals should become durable follow-up work. Read local
`AGENTS.md`, issue policy, and journal retention rules before any mutation.

1. Enumerate only completed, eligible session records with the `snapshot_export` tool of the
   `vouchington-tooling` MCP server, narrowing by `agent`, `version`, `parentSessionId`, exact
   `data` fields, and `dataArrayContains`. It exports non-archived sessions to a
   private local file and returns the path, counts, checksum, and manifest, never the records.
   Before exporting, call `outbox_flush` and then `outbox_status` for every worktree that
   `git worktree list` reports, passing each path as `worktree`, and stop if any reports a
   `worktreePendingCount` above 0. Use the worktree count, never `pendingCount` or `status`, which
   cover only the caller's own session: the sessions to distill belong to other agents, and an
   archived session refuses later delivery, so a retained record would never be distilled. Outboxes
   in removed worktrees or on other machines cannot be drained this way, so apply the age cutoffs under
   [session shapes](#session-shapes-and-eligibility) to give them time to deliver. Leave in-progress sessions intact. If a search
   for `snapshot_export` (the tool names carry a harness prefix, see the
   [blackboard skill](../blackboard/SKILL.md)) finds no server, stop and report it; do not fall back
   to a CLI command.
2. Before using any record, verify the file against the returned checksum, counts, and terminal
   manifest with the consumer's approved snapshot reader, and stop on a mismatch rather than
   treating missing records as absent. Require `manifest.schemaVersion` to be 1, `manifest.status`
   to be `"complete"`, a nonempty `cleanupToken`, and manifest counts that exactly match the export
   counts, including the terminal manifest record. Hand subagents only read-only partitions of the
   verified file, never the original snapshot. Bound each partition to at most 25 contiguous
   session groups or 1 MiB. A session's record and entries form an indivisible group, so fail the run
   rather than split a group or weaken the bound. Only the root keeps the `cleanupToken`; never
   delegate it. Read full records, with their storage type, repository
   tags, source identity, coverage, and outcomes, from that file. Do not distill from
   `journal_entries`: it reads one session at a time and has no checksum or manifest to show that
   the read is complete. For repository-scoped work, filter sessions by
   repository membership (`dataArrayContains` with `repositories` and the exact `owner/name`) and
   use only entries attributed to that repository. Leave untagged legacy records unclassified. Do
   not infer their repository.
3. Validate storage type and the shared envelope independently of optional category. Never repair
   unknown legacy types or repository provenance by inference. Quarantine malformed sessions with
   an explicit reason while processing valid unrelated sessions. Deduplicate at-least-once records
   by exact session/source identity and reject conflicting duplicate content. Records that differ
   only in their server-assigned `timestamp` are one event. Retain coverage,
   dropped counts, requested versus observed outcomes, and useful resolved findings.
   Classify each session by [shape](#session-shapes-and-eligibility) and skip any that is not yet
   eligible, with a reason.
4. Cluster findings by root cause. Prefer a few broad actionable themes over many narrow issues.
   Treat a finding already linked to an open tracker as context, not a duplicate.
5. Verify each candidate against the current base. Search existing issues and open changes before
   drafting. Skip work that is complete, explicitly rejected, or already covered. A first-party version
   bump is not proof of resolution: verify the adopted change against the original finding before
   deferring. Capture a new observation in the journal before filing it.
   Inspect against the refreshed remote default branch, never the local one, which may sit on an
   unmerged branch. Before filing a claim such as "direct-to-main" or "merged without CI", verify it
   with `git branch -r --contains <sha>` and `git merge-base --is-ancestor <sha> origin/<default>`.
   Prefer a retrospective's generated verifiable facts over its narration, and verify journal-only
   claims the same way before they reach an issue body; an agent's in-session narration is not
   evidence.
6. Draft self-contained issues with the problem, concrete proposed work, relevant areas, and
   validation, using the [issue body template](references/issue-body.md). Route every authorized creation through
   [github-issue](../github-issue/SKILL.md), including its repository gate, label approval, and
   denied-external tracking behavior.
7. Archive only verified records fully processed across every represented repository, and never
   while any worktree's `outbox_status` reports a `worktreePendingCount` above 0, under the
   repository's retention rules. Make one `session_archive` call per session, whose `sessionId` is the archived session,
   not the caller. Immediately before each call, read that session with `journal_entries` and
   archive only if its entries match the verified snapshot's by source identity; otherwise leave it
   for the next pass, because an entry added after the export would never be distilled.
   Archiving makes the session's metadata immutable, so it needs the archival authorization that
   local policy requires. A one-repository pass leaves a multi-repository session active until the other
   repositories are reviewed. Report reviewed, fixed, duplicate, deferred, quarantined, and
   actionable dispositions with reasons. Keep the top five themes in human prose without dropping
   underlying findings or unresolved records.

## Session shapes and eligibility

Classify by each entry's `type`, never by rendered text. Deduplicate by session and `sourceEventId`
first. Entries that differ only in the server-assigned `timestamp` are one event; any other
difference is a conflicting payload and stays quarantined.

| Shape                 | Definition                                                                                                                                                                                   |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Entry-type-unresolved | At least one entry has a missing type, a type other than `journal` or `retrospective`, or a feedback envelope that fails the shared validator, even if the session also has a retrospective. |
| Retrospective         | Has a retrospective entry and no unresolved entry.                                                                                                                                           |
| Checkpoint-only       | Has entries, no retrospective, and every entry is a historic hook-written checkpoint, identified by a structural checkpoint field.                                                           |
| Journal-only          | Has entries, no retrospective, and at least one entry is not a checkpoint.                                                                                                                   |
| Zero-entry child      | No entries and a non-null `parentSessionId`.                                                                                                                                                 |
| Zero-entry root       | No entries and a null `parentSessionId`.                                                                                                                                                     |

- The zero-entry split names session topology, not completion. A delegated child that died
  mid-task looks identical to one that finished cleanly; never read it as "completed normally".
- Report entry-type-unresolved sessions separately. Give them no issue-filing pass or archival this
  run, whatever their age; do not treat an untyped entry as journal evidence.
- Compute `retroAt` as the newest retrospective entry's `createdAt`, and `lastActive` as the newest
  normalized entry's `createdAt`, falling back to the session's `createdAt` when it has no
  entries. An identical replay does not advance activity; a new source event does.
- Compute `retroCutoff = now - retroDays` and `sessionCutoff = now - sessionDays` once, from
  caller-supplied non-negative finite day counts, and share both with every inspector so none reads
  its own clock. Reject a negative or non-numeric count before exporting: it makes the cutoff
  lie in the future or every comparison false, and these values gate archival.
- Every shape except entry-type-unresolved is eligible when
  `(has a retrospective AND retroAt < retroCutoff) OR (lastActive < sessionCutoff)`. Session age
  alone makes a stale checkpoint-only, journal-only, or zero-entry session eligible, so a
  retrospective-only gate cannot strand it. Everything else is not yet eligible; skip it with a
  reason.
- Export unfiltered rather than with `inactiveForHours`: a zero-entry session has no last entry and
  never matches that filter, which would hide the feedback gaps this pass exists to sweep up.
  Derive age from the cutoffs above; they supply the delay for outboxes in removed worktrees or on
  other machines.
- Journal-only and zero-entry evidence get full issue-filing rights, subject to the same duplicate,
  current-state, and dependency checks as retrospective evidence, plus redaction: never quote a
  journal entry's raw command string or stderr in an issue body, since a journal entry can carry
  unredacted secrets.
- Skip archival for sessions that contributed to a theme whose issue mutation failed this run, and
  for sessions whose only themes were deferred, since deferral promises re-evaluation. Keep a theme
  tied to a closed-without-merge issue or change eligible; do not treat open state alone as
  conclusive. Preserve each theme's contributing session IDs through merging and deduplication.
- Delegate partitions only to read-only inspectors, which must not call MCP, create issues, archive
  sessions, edit files, or keep a copy of a partition. Have each return a compact disposition
  summary: partition index, deduplicated themes with their session IDs, and each session's
  disposition. Inspectors hand-read only journal-only and retrospective sessions; every other shape
  is determined structurally.
- Keep the verified snapshot until the last `session_archive`, because the archival check reads it.
  Then remove the snapshot with the cleanup capability returned at export, and any partitions with
  the separate receipt returned when they were created (the export capability cannot remove them),
  in a cleanup path that runs even when no session is archived.
- Report reviewed, fixed, duplicate, deferred, quarantined, actionable, created, updated,
  not-yet-eligible, entry-type-unresolved, and archived counts with reasons, splitting eligible
  sessions into retrospective and stale (checkpoint-only, journal-only, zero-entry child, and
  zero-entry root).

Cleanup, as a finally step: whether processing succeeded or failed, call `snapshot_cleanup` with
the `cleanupToken` from `snapshot_export`, with the same `sessionId` and `worktree`, once the
snapshot is no longer needed. The token is single-use and server-restart-scoped; if cleanup fails,
retry the same call.

Use source records only for local verification and leave them in the repository's approved journal
or retention system. Public issue bodies contain only the minimum bounded facts or redacted
summaries needed to establish the problem, proposed work, relevant areas, and validation. Never
embed unredacted logs, command output, environment details, provider payloads, or transcript
content. A snapshot file is a private local copy of source records: never commit or attach it, or
copy its contents into an issue.

This skill supplies no issue repository, labels, milestones, projects, or approval model; it reads
sessions only from the snapshot file that `snapshot_export` writes, and archives them only with
`session_archive`. Consumer wrappers cannot weaken this export
boundary; they provide only those local details.

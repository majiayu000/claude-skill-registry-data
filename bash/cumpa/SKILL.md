---
name: cumpa
description: "Launches Cumpa’s native coding-agent review flow and consumes its canonical review result. Use for /cumpa, reviewing local changes, or comparing ordered local branches, commits, or registered worktrees in Cumpa."
license: LICENSE
---

# Cumpa

Use Cumpa as the review UI and protocol authority. This skill is only a gate to the installed CLI: do not recreate its review logic, make review commits, mutate refs/index/worktrees, or review the diff yourself.

## Requirements

The CLI is installed separately. Require Node.js 24+, Git 2.43.0+, and a stable Cumpa version `>=1.5.0 <2.0.0`; prereleases are not accepted. The bundled checker accepts valid build metadata without changing version precedence.

Only Cumpa 1.5.0 has independent release verification. Acceptance of later stable 1.x versions is a compatibility policy, not a claim that those releases were tested.

Never install or upgrade Cumpa automatically, use an npx fallback, or substitute a source checkout or local tarball.

## Workflow

1. Resolve this installed skill's directory from the agent's loaded skill location, not the reviewed repository's working directory. Run `node "<installed-skill-directory>/scripts/check-cumpa.mjs"` as the first workflow operation, before Git resolution or review launch. If Node cannot run or the checker fails, stop and show the following guidance without executing it:

   ```text
   npm install --global @shipwithai/cumpa@1.5.0
   Requires Node.js 24+ and Git 2.43.0+.
   ```

   Continue only after the checker succeeds. Run subsequent Git and Cumpa operations from the repository being reviewed.
2. Identify the ordered **base** and **head** the user requested. If either is ambiguous or omitted, ask only for the missing selection.
3. Resolve immutable full OIDs:
   - branch/commit: `git rev-parse <selection>`
   - registered worktree: resolve its committed `HEAD`; dirty bytes are not included
   - preserve PR semantics by sending `git merge-base <base-tip> <head-tip>` as `base` and the resolved head tip as `head`
4. Create one unique private temporary directory outside the repository, with directory mode `0700` and request/result files mode `0600`. Write one strict request:

```json
{"kind":"cumpa.review-request","schemaVersion":1,"mode":"revisions","revisions":{"base":"<full-merge-base-oid>","head":"<full-head-oid>"}}
```

Add `pathspecs` only when the user requested them. Preserve their order.

5. Start Cumpa from the reviewed repository using the matching agent lifecycle below. Unset `CMUX_WORKSPACE_ID`, redirect the request to stdin and canonical stdout to the result file, and observe stderr for `http://127\.0\.0\.1:[0-9]+`. Equivalent command:

```sh
env -u CMUX_WORKSPACE_ID cumpa < "$CUMPA_REQUEST" > "$CUMPA_RESULT"
```

Use native supervision, never a detached shell, `nohup`, or a tmux fallback. Give the user the URL and exact short OID range; Pi exposes the URL in its live tool output while the foreground call is running. Keep the process alive through human review and wait for its actual exit after **Finish**. Readiness is not completion.

6. Accept the handoff only when Cumpa exits `0` and the result is one non-empty parseable JSON object with `kind: "cumpa/export"`. Exit `1`, exit `130`, empty stdout, or invalid JSON means no accepted review; report the Cumpa diagnostic without inventing feedback.
7. Consume and report; do not edit code:
   - overall `summary.markdown`
   - open comments grouped by file, with anchor side/line, body, and verification state
   - counts, drift warning, and acknowledged state
   - resolved-comment count; list resolved comments only when asked
   - if summary and comments are empty, say the review completed with no recorded feedback
8. Remove only the owned temporary handoff directory and files after result consumption or an observed terminal failure/cancellation. Do not remove files while Cumpa is still running. Cumpa's repository-local draft/export remains authoritative.

## Agent-specific lifecycle

Use the installed target's supported process tools; do not invent an adapter or claim that another agent's result proves this target works.

### Claude Code

The native `ship-with-ai` collection loads `skills/cumpa/SKILL.md`; invoke `/ship-with-ai:cumpa`. A selectively installed standalone skill is discovered in the project's `.claude/skills/cumpa` directory and invoked as `/cumpa`.

Use supported background Bash execution and retain the returned task handle. Observe stderr readiness, then wait on that same task for terminal exit before reading the result file. If background tasks are disabled or unavailable, stop rather than detach the process.

### Codex

Use project-local `.agents/skills/cumpa` discovery and explicit `$cumpa`, or select Cumpa from `/skills`. Do not assume an unverified global skill location.

Use the supported PTY-backed execution session, redirecting stdin/stdout as above. Retain its returned session handle, observe readiness, and poll that session until terminal exit; do not infer completion from a URL or a result file appearing.

### Pi

Use project-local `.pi/skills/cumpa` discovery in a trusted project with skill commands enabled, then invoke `/skill:cumpa`.

Run foreground Bash with no explicit timeout. Redirect only canonical stdout to the result file; leave stderr connected to Pi's tool stream so the human can see the loopback URL during the blocking call. Pi 0.80.2's source supports this live partial rendering; it does not establish that the model receives partial tool results before the call returns. Announce the pinned review range before launching, wait while the human reviews and presses **Finish**, and read the result only after Bash returns with the actual exit status. Do not redirect stderr to an unread diagnostics file or invent background execution.

### OMP

Use the native `ship-with-ai` marketplace collection, whose installed tree contains `skills/cumpa`, and invoke `/skill:cumpa`. Pi and OMP are separate targets; no Skills CLI `-a omp` route is assumed.

Use `hub` to start a stable named supervised process. Observe its loopback readiness separately from waiting for process exit. Retain that process name, wait for actual terminal status, then read the canonical result file. Never treat a successful `start` or readiness event as a completed review.

## Native exact-patch mode

Use exact-patch mode only when the user explicitly supplies a patch or asks to review one. Do not synthesize patches or temporary commits to extend Cumpa.

```json
{"kind":"cumpa.review-request","schemaVersion":1,"mode":"patch","patch":{"content":"<exact UTF-8 patch>","target":{"kind":"repository"}}}
```

`target.kind` is `repository` for committed `HEAD` or `worktree` for current on-disk entries. The patch must be non-empty, NUL-free UTF-8 and the entire request must not exceed 1 MiB.

## Protocol invariants

- Piped stdin selects agent mode; stdout stays empty until successful Finish.
- URL and diagnostics are stderr-only.
- Revision requests use full pinned OIDs; base must be an ancestor of head.
- Cumpa reviews committed worktree `HEAD`, not dirty worktree bytes.
- Cumpa never applies, stages, commits, or pushes changes.
- Do not treat process readiness as review completion; wait for successful exit and validate stdout.

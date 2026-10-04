---
name: gh-update-plan
description: Update a GitHub plan issue with progress. Use when planning a task, or when the user tells you to "update the github plan issue".
argument-hint: "[owner/repo#number] [--local] [--preview] [--sessions-only]"
allowed-tools: Bash, Read, Write, Edit
---

Exit plan mode before executing this skill. You must actually run `gh` commands to update the issue; do not just describe what you would do. Use `gh` to read, edit, and comment on issues. This includes using `gh api` to update issue bodies and edit or create comments. Do not ask for permission to update comments -- it is expected.

**Workflow for editing issue bodies and comments:**
1. Use a stable temp directory per issue: `/tmp/plan-update-OWNER-REPO-NUMBER`. This allows reuse across invocations.
2. **Fetch or reuse**: If `--local` is passed and the temp directory already has files from a previous invocation, skip fetching and reuse the cached files. Otherwise, **always fetch fresh content** from GitHub using `gh api` and overwrite any existing temp files. In Claude Code, prefer the Write tool. Do not embed fetched content directly in shell arguments.
3. Modify the temp files with the agent's normal file-edit mechanism. In Claude Code, prefer the Read and Edit tools. Avoid ad hoc `sed`/`awk` rewrites.
4. Upload using `--input` with `jq` to properly JSON-encode the content:

- Edit issue body: `jq -Rs '{body: .}' <tempdir>/body.md | gh api repos/OWNER/REPO/issues/NUMBER -X PATCH --input -`
- Create comment: `jq -Rs '{body: .}' <tempdir>/comment.md | gh api repos/OWNER/REPO/issues/NUMBER/comments --input -`
- Edit comment: `jq -Rs '{body: .}' <tempdir>/comment-COMMENTID.md | gh api repos/OWNER/REPO/issues/comments/COMMENT_ID -X PATCH --input -`

Never embed content directly in shell arguments or use `-f body=@file` (it uploads the literal string, not the file contents).

By default, always fetch the latest from GitHub before making changes. Use `--local` only when you know the issue hasn't been updated since the last fetch.

**`--preview` mode**: Prepare all changes in temp files but do not upload. After steps 1-12, show the diff between the fetched files and the modified temp files (e.g. `diff <fetched> <modified>` for each changed file). For new comments, show the full content. Wait for the user to approve before uploading. The user may ask for edits before approving.

**`--sessions-only`**: Only run step 11 (Agent sessions table) and update the session comment heading (step 12) if one exists for this session. Skip all other steps. Useful for registering a session without a full plan update.

Never @mention other users in plan issues or comments.

Update the GitHub issue $ARGUMENTS (issue URL or `owner/repo#number`). If no argument is given, use the issue referenced earlier in this conversation. If no issue can be determined, ask the user. When the issue was not given as an explicit argument, verify it is a real plan issue (has structural comments like Steps or Design) before proceeding. If it does not look like a plan issue, stop and ask the user to confirm.

If a durable-memory CLI is configured, query it here with the task's distinctive terms before updating. See the memory tool's own integration doc for mechanics.

1. Verify that it contains the detailed plan for the work in this conversation. If not, ask the user to verify that the correct issue was given.
2. **Conformance check**: Ensure the issue follows the standard plan format. If not, lightly restructure:
   - Convert plain step lists to checkboxes (`- [ ]` / `- [x]`)
   - Add missing section headings (Description, Steps, Links)
   - If there is no diagram in either the issue body or comments, and the work would benefit from one, add a diagram in a separate comment (Mermaid, three sentence max caption, no "Caption:" prefix). Pick the right type: `sequenceDiagram` for temporal flow, `flowchart` with `subgraph` + `classDef` for static structure
3. If the design approach has changed or new key decisions were made, update the **Design** comment (or the body for old-format issues that have the how in the body). The Design comment is the chosen approach only. Rejected alternatives belong in standalone comments (`## Considered: ...`, `## Decision: ...`). Omit raw exploration; only include conclusions. Two guardrails against bloat:
   - **Don't restate the design doc.** If a rule or decision is already written in the canonical design doc, the Design comment should reference it ("per design doc, Format section"), not repeat it. The comment's job is implementation bindings and decisions that go beyond the doc.
   - **One paragraph per decision, max.** State the binding and the key constraint; put worked examples, rationale, and edge cases in the design doc or a standalone finding comment, not inline.
   - **Keep comments scannable.** Avoid walls of text; break content with lists. For work tracked in other issues, use a bulleted `owner/repo#N -- short description` list rather than restating each issue's rationale in prose.
4. Check off completed steps (`- [x]`) based on the work done in this conversation. Steps may be in a separate **Steps** comment (new format) or in the issue body (old format). Check both locations and update wherever the steps are found.
5. If the issue body or comments contain a diagram, check if it is still accurate. If not, update it.
6. If steps need rewording or new steps are needed, update them wherever they are (Steps comment or body). Steps with a child issue should use: `- [ ] Child issue: owner/repo#N`. The Steps comment is checkboxes only - no prose, no paragraphs, no narrative under sub-steps. Context and rationale belong in the Design comment or the session summary (step 12). If steps are still in the body and there are many updates, consider migrating them to a separate Steps comment.
7. Update the **Links** comment with any new references (child issues, documentation, resources). Do not add PRs here (regardless of which repo they target) - all PRs belong in the PRs comment (step 9). Links may be in a separate comment (new format) or in the body (old format). If in the body, consider migrating to a comment.
8. If useful commands for testing or verifying the work were discovered during this session, add or update a **Useful commands** comment (separate from the issue body). If such a comment already exists, edit it rather than creating a new one.
9. **PRs** (do not skip): find or create a **PRs** comment (separate from the issue body) with a table: `| PR | What | Agent session |`. PR column: `org/repo#N` as a link. What column: brief description. Agent session column: the name of the session running this gh-update-plan invocation. `gh-close-plan` will finalize this when the plan is closed.
10. Review existing comments for outdated or incorrect information. Own comments: rewrite to state the correct information only (no strikethrough or revision notes - plan issues are current state, not history). Others' comments: reply with the correction.
11. **Agent sessions**: Find or create an **Agent sessions** comment with a table: `| Session | Directory | Model | Last used | ID |`. Add a row for this session. Always use backtick code formatting for Directory and ID values. Replace the user's home directory with `~` in the Directory column. Get the session ID and name as follows:
   - **Claude Code**: session ID from `$CLAUDE_CODE_SESSION_ID`. Session name from the system reminder (look for "The user named this session").
   - **Codex**: session ID from `$CODEX_THREAD_ID`. Session name from `~/.codex/session_index.jsonl`: `jq -sr --arg id "$CODEX_THREAD_ID" '[.[] | select(.id == $id) | .thread_name] | last // "unnamed"' ~/.codex/session_index.jsonl`.
   - **Other agents**: use the agent's own session identifier and name if it exposes them; otherwise ask the user.
   - **Model**: never guess. In Claude Code, use the model from the system prompt. In Codex, query `~/.codex/state_5.sqlite`: `SELECT model FROM threads WHERE id = '$CODEX_THREAD_ID'`. Use the model family, version, and variant without extras like context window size (e.g. "Opus 4.8", "Fable 5", "GPT-5.6 Sol").
   - Fall back to "unnamed" if no source has a name. Use the **full session name** in this table; the shortened form (dropping everything before the first ` - `) is only for the PRs table. Set Last used to today's date (YYYY-MM-DD). If this session ID already has a row, update it (the name, date, or other fields may have changed). Do not duplicate rows.
12. **Important**: session comments (`### Session:`) are compressed into a single Session Log by `gh-close-plan`. Do NOT put design decisions, gotchas, or important context into session comments. Those belong in the **Design** comment (step 3) or as standalone findings (see below).

    Find or create a comment with heading `### Session: <session name>` (the session name from step 11; the date goes in the body, not the heading). If this session already has a comment (match by session name), update it rather than creating a new one.

    Write the body so a reader who was not in the session can tell what happened and what is left:
    - First line: the date, or the date range for a session spanning several days (`2026-09-22`, or `2026-09-13 to 2026-09-22`). `gh-close-plan` groups the Session Log by date and needs it.
    - Then short bullets: what was attempted and its outcome, what was learned or surprising, open questions, and what remains. One line per bullet. Several bullets are expected; a two-sentence summary is too little to be useful later.
    - Do not list commits, PRs, or implementation details; the PRs table and the diffs hold those.

    If a session produced standalone findings worth preserving independently (research, design decisions, verification results), add them as separate comments with descriptive headings (e.g. `## Research: ...`, `## Considered: ...`). These are not prefixed with `Session:` and will be kept as-is by `gh-close-plan`. Finding style: state each verified fact plainly (including positive ones), then the recommendation. No mechanism walkthroughs, no loaded adjectives ("only *rare*", "*effectively permanent*"). When later work in the same session refines a finding, update the finding comment in the same pass.

    The reverse also holds: routine progress ("implemented X", "tests pass", "rebased onto main") is session narrative and belongs in the `### Session:` comment, never in a standalone `## Decision:` or `## Verification:` comment. A standalone comment earns its place only if a future reader would want it after the session log is compressed away.

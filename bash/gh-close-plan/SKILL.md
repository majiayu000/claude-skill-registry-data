---
name: gh-close-plan
description: Close a GitHub plan issue with a summary. Use when the user tells you to "close the github plan issue".
argument-hint: "[owner/repo#number]"
allowed-tools: Bash, Read, Write, Edit
---

Never @mention other users in plan issues or comments.

Close the GitHub issue $ARGUMENTS (issue URL or `owner/repo#number`). If no argument is given, use the issue referenced earlier in this conversation. If no issue can be determined, ask the user.

**Workflow for editing issue bodies and comments:**
1. Create a unique temp directory: `mktemp -d /tmp/plan-close-XXXXX`
2. Fetch content from GitHub using `gh api` and save it to files in the temp directory (e.g. `body.md`, `comment-COMMENTID.md`). In Claude Code, prefer the Write tool. Do not embed fetched content directly in shell arguments.
3. Modify the temp files with the agent's normal file-edit mechanism. In Claude Code, prefer the Read and Edit tools. Avoid ad hoc `sed`/`awk` rewrites.
4. Upload using `--input` with `jq` to properly JSON-encode the content:

- Edit issue body: `jq -Rs '{body: .}' <tempdir>/body.md | gh api repos/OWNER/REPO/issues/NUMBER -X PATCH --input -`
- Create comment: `jq -Rs '{body: .}' <tempdir>/comment.md | gh api repos/OWNER/REPO/issues/NUMBER/comments --input -`
- Edit comment: `jq -Rs '{body: .}' <tempdir>/comment-COMMENTID.md | gh api repos/OWNER/REPO/issues/comments/COMMENT_ID -X PATCH --input -`

Never embed content directly in shell arguments or use `-f body=@file` (it uploads the literal string, not the file contents). Always fetch the latest from GitHub before making changes. Do not rely on previously fetched copies that may be stale.

1. Read the issue and its comments to understand the full history of the work.
2. Check off completed steps (`- [x]`) based on the work done. Steps may be in a separate **Steps** comment (new format) or in the issue body (old format). Check both locations.
3. Verify that all steps are checked off. If any are incomplete, ask the user whether to proceed or leave the issue open.
4. Finalize the **PRs** comment as a table: `| PR | What | Agent session |`. PR column: `org/repo#N` as a link. What column: brief description. Agent session column: the session that added the PR. If the existing comment uses a different format (bullet list, old-style table), reformat it to this table structure.
5. **Clean up comments**: Non-structural comments fall into two categories based on their heading:
   - **`### Session:` prefix**: These are session summaries. Delete them and consolidate into a single **Session Log** comment with dated sections (`### YYYY-MM-DD`). Keep only key findings, decisions, and insights. Drop sessions with nothing noteworthy.
   - **Any other heading** (e.g. "Research:", "Considered:", "Implementation notes:", "Verification:"): These are standalone findings with lasting value. Keep them as separate comments, or merge into the Design comment if they are design decisions.
   **Never delete structural comments** (Steps, Design, Diagram, Links, Useful commands, Agent sessions, PRs). See `gh-create-plan` for the canonical list and order.
6. **Capture learnings**: Before closing, review the work for non-obvious discoveries worth persisting. If a durable-memory CLI is configured, offer its capture flow. Otherwise, ask the user "Anything worth capturing?" and propose where each belongs:
   - **Instructions file** (CLAUDE.md, AGENTS.md, or similar): conventions, gotchas, build quirks
   - **Repo docs** (`docs/` or similar): architecture insights, design rationale
   - **Memory**: cross-project patterns, user preferences

   For a **company-shareable plan** (opened in the `teamRepo` from `~/.claude/skills/plan-config.json`), distill a frozen team **record** summarizing what was decided and why, so the closed plan carries no unique living knowledge and becomes safely archival. One record per independently citable outcome (usually one per plan). Split only when different consumers would cite different parts; never split by timeline or implementation phase. Skip this step if no `teamRepo` is configured or the plan is not in that repo.

   Apply confirmed items. If the user says nothing to capture, move on.
7. Add a closing comment summarizing:
   * What was accomplished
   * Links to the final PR(s)
   * Any follow-up work or known limitations
8. Close the issue.

---
name: gh-create-plan
description: Create a plan issue on GitHub. Use when planning a task, or when the user tells you to "create a github plan issue" with the repo name as argument.
argument-hint: "[personal|team|owner/repo]"
allowed-tools: Bash
---

Never @mention other users in plan issues or comments.

Create a GitHub issue containing the detailed plan for the work in this conversation.

**Plan location.** Check `~/.claude/skills/plan-config.json` for `personalRepo` and/or `teamRepo` (both optional). $ARGUMENTS can be `personal`, `team` (resolved from config; fail if the corresponding repo is not configured), or an `owner/repo` used directly. If no argument is given: use the only configured repo if there is exactly one; ask the user if both are configured; ask for a repo if neither is configured.

- **Personal**: the `personalRepo` from config.
- **Company-shareable** (team plans and records): the `teamRepo` from config. A plan opened here distills into a team record on close.

**Guard.** Plan issues must only be created in private or internal repos. NEVER create them in public repos. If the user provides a public repo, warn them and ask for the correct location.

Derive a concise issue title from the conversation context. Ask the user if unclear.

The GitHub issue should be self-contained so that a new conversation can pick up the work without needing additional context. Omit raw exploration and back-and-forth; only include the conclusions.

Think as a software architect first. Before writing steps, consider: What are the key abstractions? Where should boundaries be? What's the simplest design that solves the problem? What will be hard to change later? Let these decisions shape the plan structure.

When a design splits work across layers (e.g. "resolve X in layer A, resolve Y in layer B"), verify what context is available at each layer by reading the actual code. Do not assume context is unavailable without checking. Plans that make wrong assumptions about layer boundaries lead to unnecessary complexity (e.g. partially-resolved intermediate states).

If a durable-memory CLI is configured, query it with the task's distinctive terms before writing the plan. See the memory tool's own integration doc for mechanics.

Before creating the plan, ask the user if there are related repos with similar implementations that should inform the approach. If so, review them to understand how the problem was solved there, and incorporate relevant patterns into the plan.

**Issue body** (should rarely need updating):

1. **What and Why**: What problem is being solved and why it matters. Do not include the how/design.
2. **Prerequisites**: List only non-obvious manual steps needed before implementation. Omit this section entirely if there are no real prerequisites.

**After creating the issue body**, add structural comments in the canonical order below. Each comment starts with a `## heading`. These are permanent and must never be deleted (even by `gh-close-plan`). Session summary comments (added later by `gh-update-plan`) are non-structural and come after these.

1. **Steps**: Group steps under numbered headings (`### Step 1: ...`, `### Step 2: ...`). Each step contains checkboxes for its sub-tasks, followed by a one-line dependency note below the checkboxes: `Depends on: 1, 2` or `Independent`. Always number the top-level steps explicitly. Steps with a child issue: `- [ ] Child issue: owner/repo#N`. Checkboxes and the dependency line only - no other prose or narrative. Context belongs in the Design comment.
2. **Design**: The chosen approach only. Technical approach, key abstractions, boundaries, trade-offs. Rejected alternatives belong in standalone comments (`## Considered: ...`, `## Decision: ...`), not here. This is where the living design is tracked.
3. **Diagram**: Show the flow, structure, or relationships using Mermaid (not ASCII). Pick the right diagram type for the content:
   - **Temporal flow** (request handling, build pipeline, event sequence): `sequenceDiagram`.
   - **Static structure** (components, dependencies, what connects to what): `flowchart` with `subgraph` for grouping and `classDef` for color-coded categories.
   Short caption (three sentences max, no "Caption:" prefix).
4. **Links**: Links to relevant documentation, code, resources, and related issues. Do not add PRs here.
5. **Useful commands**: Added by `gh-update-plan` when useful commands are discovered. Not created by `gh-create-plan`.
6. **Agent sessions**: A table `| Session | Directory | Model | Last used | ID |` with this session as the first row. Set Last used to today's date (YYYY-MM-DD). Use backtick code formatting for Directory and ID. Replace the user's home directory with `~` in the Directory column. Get the session name from the system reminder in Claude Code (look for "The user named this session"), or from `~/.codex/session_index.jsonl` in Codex (see `gh-update-plan` for the lookup); if not found, use "unnamed". Get the session ID from `$CLAUDE_CODE_SESSION_ID` (Claude Code) or `$CODEX_THREAD_ID` (Codex). Model: never guess. In Claude Code, use the model from the system prompt. In Codex, query `~/.codex/state_5.sqlite`: `SELECT model FROM threads WHERE id = '$CODEX_THREAD_ID'`. Use the model family, version, and variant without extras (e.g. "Opus 4.8", "Fable 5", "GPT-5.6 Sol").
7. **PRs**: Added by `gh-update-plan`. Table: `| PR | What | Agent session |`.

On create, add comments 1-4 and 6. Comments 5, 7 are added later by `gh-update-plan`.

**Labels**: Before creating the issue, fetch available labels from the target repo with `gh label list --repo OWNER/REPO --json name,description`. Exclude status/workflow labels (e.g. `blocked`, `in-progress`, `done`, `wontfix`). Present the remaining labels and ask the user which to apply. Apply selected labels with `--label` flags on `gh issue create`. If no labels exist in the repo, skip this step.

Format the issue in a clear and organized way, using headings, subheadings, bullet points, and tables as needed to enhance readability.

After creating the issue, tell the user they can use `/gh-read-plan` and `/gh-update-plan` to continue working with it.

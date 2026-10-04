---
name: prompt-session
description: Generate a concise prompt for another coding agent session, optionally tailored to a role (architect, implementer, reviewer, investigator, researcher, secretary, writer). Use when the user asks to "generate a prompt for a session", "write a prompt for a reviewer/architect/implementer/etc", or "make a session prompt".
argument-hint: "[role: architect|implementer|reviewer|investigator|researcher|secretary|writer]"
allowed-tools: Bash, Read
---

Generate a concise prompt that the user will paste into another coding agent session. This skill also applies to
follow-up messages to sessions that were previously prompted by this skill (e.g. additional instructions, corrections,
or new context for a running session).

$ARGUMENTS may specify a role: `architect`, `implementer`, `reviewer`, `investigator`, `researcher`, `secretary`, or
`writer`. If omitted, ask the user which role the target session will play.

## Core rules (what NOT to include)

Assume the target session has the same instructions files, skills, and tools as this one, unless the user says
otherwise. Do NOT restate:
- Global conventions (writing style, shell, tool preferences, etc.)
- Tool usage rules (`gh` for GitHub, search tools over shell, etc.)
- Git commit rules (author, sign-off, commit message style)
- Content of the plan issue (the target reads it via `/gh-read-plan`)

## What to include

- **One-sentence goal**: what the target is being asked to do
- **Plan reference**: if there is a plan issue, cite it as `owner/repo#N` and instruct the target to run
  `/gh-read-plan owner/repo#N` at the start. Do not summarize the plan.
- **Skill to invoke**: if a ready-made skill covers the target's job (see roles below), instruct the target to invoke
  it. Do NOT restate the skill's rules in the generated prompt; the target loads those itself.
- **Recall**: if a durable-memory recall skill is configured, instruct the target to run it on the task's own terms
  before starting non-trivial work. `/gh-read-plan` recalls on the plan issue's terms; this adds the task-specific
  angle. Skip for trivial tasks: secretary updates, formatting fixes, mechanical edits.
- **Pointers**: branch, worktree path, key file paths, sibling checkouts to avoid
- **Hard constraints**: scope boundaries (no push, no PR create, no amend, no changes outside X, don't delete worktree,
  etc.)
- **Expected output**: only specify this when there's no skill for the role, OR when the user wants output that differs
  from the skill's default.

## Find the plan issue

If a plan issue was referenced earlier in this conversation, use it. Otherwise ask the user whether there's a plan issue
or other external context the target should load.

## Role-specific tailoring

For each role, prefer pointing the target at an existing skill over restating expectations. Add only the
non-skill-covered context (scope, constraints, refs).

**architect** - no single matching skill (design work is open-ended). Also fits plan-shaping for non-code artifacts
(articles, talks, docs) where the work is structural, not prose-drafting.
- Expected output: design alternatives with pros/cons and confidence estimates, recommended approach, key risks, what
  will be hard to change later.
- Constraints: do not write code or draft final prose. If producing a new plan, invoke `/gh-create-plan`. If updating
  an existing plan, invoke `/gh-update-plan`.

**implementer** - always include `Invoke /gh-implement-plan owner/repo#N` in the generated prompt. The plan issue ref
is required; if this session has one, use it. If not, ask the user.
- Add branch/worktree/constraints.
- Implementers only commit locally. Never tell them to push, open PRs, or create PRs. The user handles that separately.
- Always include: "As you implement, critically evaluate the plan and design. If you encounter something that seems
  wrong, unclear, or worth reconsidering, stop and report back before continuing."

**reviewer** - for a PR, use `/gh-review-pr <pr-ref>` from
[claude-review-skills](https://github.com/gjoranv/claude-review-skills) if it is installed. For a branch or local
uncommitted changes there is no matching skill.
- Prompt: "Invoke `/gh-review-pr <ref>`", or state what to review (branch, or "local changes in <path>") and what to
  focus on.
- Expected output (only without a skill): findings ranked by severity with `file_path:line_number` references, and a
  clear verdict on whether the change is ready to merge.
- Constraints: no code changes, no push, no amend. Report findings; do not fix them unless asked.

**investigator** - no matching skill. For debugging and root-cause analysis of a concrete symptom.
- Prompt: state the symptom and reproduction steps. Add any scope constraints.
- Expected output: the root cause with evidence (`file_path:line_number`, log excerpts), and a proposed fix.
- Default constraint: do not apply the fix, just report the root cause.

**secretary** - use `/gh-update-plan`. For keeping project tracking artifacts in sync with work done elsewhere.
- Prompt: tell the target which artifacts to update and point at the skill. Provide the plan issue ref.
- Also handles: pure formatting fixes, trivial adjustments, and housekeeping edits to design docs or plans that don't
  require architectural judgment.
- Constraints: no code changes, no architectural decisions. Do not add a session summary comment when running
  `/gh-update-plan`; the session that delegated the work owns the session log. If an update requires a design call,
  stop and report back.

**researcher** - no matching skill.
- Expected output: findings with citations (`file_path:line_number` or URLs), options with trade-offs, a
  recommendation.
- Constraints: no code changes. Prefer current official documentation over training data for external CLIs and APIs.

**writer** - no matching skill. For blog posts, essays, announcements, release notes, or other long-form narrative
content.
- Expected output: a draft matching the user's voice with a clear narrative arc. Sources cited for non-obvious claims.
- Constraints: read existing content in the target location to match voice and style. Flag claims that need sourcing
  rather than fabricating. Don't invent quotes, statistics, or attributions.

## Output

Print the prompt between plain-text fences so the user can copy-paste verbatim:

```
---BEGIN PROMPT---
[Generated by: <this session's name> | Role: <role>]

<prompt body>
---END PROMPT---
```

Get this session's name from the agent's own source. In Claude Code, read the system reminder (look for "The user named
this session"). In Codex, look it up:
`jq -sr --arg id "$CODEX_THREAD_ID" '[.[] | select(.id == $id) | .thread_name] | last // "unnamed"' ~/.codex/session_index.jsonl`.
Only if neither source yields a name, use "unnamed".

Keep it short. Terse direct sentences, no bullet-point sprawl. If the task is simple, 10 lines is ideal; never exceed
~30 lines unless the user has provided a lot of unique context that can't be referenced by a plan issue.

Before printing, do a final pass and remove anything the target's instructions file (CLAUDE.md, AGENTS.md, or similar)
already covers.

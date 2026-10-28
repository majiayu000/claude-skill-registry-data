---
name: adapt
description: >-
  Use when the user asks to tailor the installed flowai skills, agents, hooks or
  AGENTS.md artifacts to this project's specifics. Not for first-time setup,
  template reconciliation, or edits to the project's own code.
argument-hint: '[--skills|--agents|--hooks|--assets] [name]'
---

# Task: Adapt Framework Primitives to Project

## Overview

Adapt project-local flowai framework primitives (skills, agents, AGENTS.md artifacts, hooks) to the current project's tech stack and conventions. Runs independently of `update` — use after first project-local install, stack change, or selectively for specific resources.

<context>
flowai may install generic framework primitives into the project with default examples (e.g., `deno test`, `deno lint`). Projects using other stacks (Python/pytest, Go/golangci-lint, etc.) need adaptation: replacing generic commands/examples with project-specific ones.

Plugin-installed and user-level primitives are read-only for this command. If flowai is installed through an IDE plugin or a global/user config directory, do not rewrite those files. Report that no project-local primitives are available unless the user asks to create a local copy.

The AGENTS template (`AGENTS.template.md`) is a read-only framework source whose location depends on install mode: a skill-local plugin asset (`.{ide}/skills/adapt/assets/AGENTS.template.md`) for plugin/user installs, a project-local copy (`.{ide}/assets/AGENTS.template.md`) written by a build-and-copy install, or a user-level copy. Read it wherever found; never edit it.

Adaptation state is tracked through git history — no extra metadata fields needed. The working tree contains the current version; `git show HEAD:<path>` provides the previous adapted version for 3-way merge.

Two subagents handle the actual adaptation work:
- `skill-adapter` — adapts a single skill's SKILL.md
- `agent-adapter` — adapts a single agent's .md body (preserving frontmatter)
</context>

## Rules & Constraints

<rules>
1. **Reuse subagents**: Delegate skill adaptation to `skill-adapter`, agent adaptation to `agent-adapter`. Never duplicate their logic.
2. **Per-file confirmation**: Show diffs and ask user before accepting each adapted resource. Never silently overwrite.
3. **Parallel execution**: Launch one subagent per resource — all in parallel for each resource type.
4. **Cross-IDE**: Detect and work with any installed IDE config dir (`.claude/`, `.cursor/`, `.opencode/`, `.codex/`).
5. **Mandatory tracking**: Use a task management tool (e.g., todo write) to track execution steps.
6. **No auto-commit**: Adaptation changes are staged but not committed. User decides when to commit.
7. **Project-local only**: Operate only on IDE config dirs inside the current project. Never edit plugin cache files or user-level dirs such as `~/.claude/skills`, `~/.codex/skills`, or marketplace plugin caches.
</rules>

## Instructions

<step_by_step>

1. **Detect IDE config directories**
   - Scan project root for `.claude/`, `.cursor/`, `.opencode/`, `.codex/`.
   - Use all detected dirs for subsequent operations.
   - Ignore global/user-level IDE dirs and plugin cache locations.
   - If none found, inform user that no project-local primitives are installed and stop.

2. **Parse arguments**
   - No args -> verify assets first, then adapt a bounded first batch of clearly mismatched skills/agents/hooks.
   - `--skills` -> only skills.
   - `--agents` -> only agents.
   - `--assets` -> only AGENTS.md artifacts.
   - `--hooks` -> only hooks.
   - Positional name arg -> filter to that single resource within selected type(s).

3. **Adapt skills** (when applicable)
   - List all `flowai-*` directories in `{ide}/skills/`.
   - Use only project-local paths under the current working tree.
   - Filter by name argument if provided.
   - If no name argument is provided, pre-filter candidates before launching subagents:
     a. Read AGENTS.md to identify the project stack and canonical commands.
     b. Read each candidate SKILL.md.
     c. Select only skills with obvious stack mismatch or generic examples that conflict with the project stack (for example `deno test`, `deno lint`, `deno fmt` in a Python/pytest or Go project).
     d. Skip skills that do not contain stack-specific commands/examples, and mention them in the summary.
     e. For no-arg full adaptation, cap the first automatic batch to the highest-signal skills (prefer `commit`, `do`, and stack setup skills) so the run can still verify assets and ask confirmation before timeout. Report remaining candidates as deferred follow-ups.
   - Launch one `skill-adapter` subagent per selected skill — **all in parallel**.
   - Each subagent receives the skill name and path. It autonomously reads:
     - Working tree SKILL.md (current version)
     - `git show HEAD:<path>/SKILL.md` (previous adapted version, if exists)
     - AGENTS.md for project context
   - Wait for all subagents to complete. **Waiting means collecting, not
     listening.** Many subagent tools dispatch in the background by default and
     answer with a handle — an agent id plus token counters — instead of the
     result. When your tool offers a foreground or blocking mode (a
     `run_in_background: false` parameter or equivalent), set it. If you still
     get back only a handle, continue that agent by its id and ask it for its
     result. Sitting idle until a notification arrives is not waiting: the first
     notification to land is one adapter's, and acting on it leaves the others
     uncollected.
   - **Present nothing while an adapter is outstanding.** Do not show a diff, do
     not ask for confirmation, and do not write the summary until every
     dispatched adapter has returned. A run that reports one skill and says
     another is "still running" has ended mid-process — the user is asked to
     decide on a partial picture, and the summary of step 7 never happens.
   - For each adapted skill, show the full relevant diff: `git diff HEAD -- <skill-path>`.
   - Before asking confirmation, verify the diff actually replaces stale commands with project-specific commands from AGENTS.md. If a selected skill still contains the stale command with no project-specific replacement, rerun the adapter for that skill or fix the proposal before presenting it.
   - Ask user for confirmation per skill.
   - Revert rejected adaptations: `git checkout HEAD -- <skill-path>`.

4. **Adapt agents** (when applicable)
   - List all `flowai-*` files in `{ide}/agents/`.
   - Use only project-local paths under the current working tree.
   - Filter by name argument if provided.
   - If no name argument is provided, pre-filter candidates the same way as skills: select only agents whose body contains stack-specific commands/examples that conflict with AGENTS.md.
   - In no-arg full adaptation, if both skills and agents contain mismatches, adapt at least one selected skill and at least one selected agent before asking for final confirmation. Prefer `commit` for skills and `console-expert` for agents when they contain stale commands.
   - Before launching each adapter, save the exact YAML frontmatter block (`---` through closing `---`) for that agent.
   - Launch one `agent-adapter` subagent per selected agent — **all in parallel**.
   - Each subagent receives the agent name and path. It autonomously reads:
     - Working tree agent `.md` (current version)
     - `git show HEAD:<path>` (previous adapted version, if exists)
     - AGENTS.md for project context
   - Wait for all subagents to complete — collecting each one's result, under the
     same rule as step 3. Present nothing while an adapter is outstanding.
   - After each subagent completes, verify that the YAML frontmatter is byte-for-byte identical to the saved block. If it changed, restore the saved frontmatter and keep only body changes.
   - Verify the adapted body no longer contains stale commands that conflict with AGENTS.md. If an adapted Go project agent still contains `deno test`, `deno lint`, or `deno fmt` as recommended project commands, rerun or fix that agent before presenting the diff.
   - For each adapted agent, show the diff: `git diff HEAD -- <agent-path>`.
   - Ask user for confirmation per agent.
   - Revert rejected adaptations: `git checkout HEAD -- <agent-path>`.

5. **Verify AGENTS.md artifacts** (when applicable)
   - In no-arg full adaptation, run this step before launching expensive skill/agent subagents. Asset verification is cheap and must not be starved by primitive adaptation.
   - Read `pack.yaml` from installed packs (via `.flowai.yaml`) to get the `assets:` mapping (template name -> artifact path).
   - If `pack.yaml` is unavailable, use default mapping:
     - `AGENTS.template.md` -> `AGENTS.md`
   - If the project still has `documents/AGENTS.md` or `scripts/AGENTS.md`, defer to `update` or `init` to run the legacy-collapse procedure — do NOT handle collapse here.
   - **Locate the template source** (install modes differ — do not assume `{ide}/assets/`). Check these in order and use the first that exists:
     - Skill-local plugin asset (most accurate for plugin/user-level installs — the template was copied next to this command):
       - `.claude/skills/adapt/assets/AGENTS.template.md`
       - `.cursor/skills/adapt/assets/AGENTS.template.md`
       - `.opencode/skills/adapt/assets/AGENTS.template.md`
       - `.codex/skills/adapt/assets/AGENTS.template.md`
       - namespace-stripped plugin paths such as `*/skills/adapt/assets/AGENTS.template.md` when visible in the project.
     - Project-local asset copy (build-and-copy install layout):
       - `.claude/assets/AGENTS.template.md`
       - `.cursor/assets/AGENTS.template.md`
       - `.opencode/assets/AGENTS.template.md`
       - `.codex/assets/AGENTS.template.md`
     - User-level asset:
       - `~/.claude/assets/AGENTS.template.md`
       - `~/.cursor/assets/AGENTS.template.md`
       - `~/.config/opencode/assets/AGENTS.template.md`
       - `~/.codex/assets/AGENTS.template.md`
     - If a skill-local plugin asset exists, treat it as authoritative for this run; report any differing same-tier templates as secondary/stale rather than switching by modified time.
     - If none exist, report that `AGENTS.template.md` was not found (install flowai via plugin manager or flowai CLI, then rerun) and skip artifact verification — do NOT fabricate template content.
   - For each template -> artifact pair:
     a. Read the framework template from the resolved source above.
     b. Read the project artifact.
     c. Compare using `git diff --no-index -- <template> <artifact>`.
     d. Ignore `{{PLACEHOLDER}}` sections in the diff.
     e. Focus on **framework-originated sections** (rules, TDD flow, doc formats, planning rules).
     f. If framework sections are outdated -> propose update with before/after.
   - Ask confirmation per artifact.

6. **Adapt hooks** (when applicable)
   - List hook scripts in `{ide}/scripts/` (installed by flowai).
   - Use only project-local hook scripts.
   - For each: read the script, check if it contains stack-specific commands (e.g., `deno lint`, `npm test`).
   - If stack-agnostic (like current validation hooks) -> skip.
   - If stack-specific commands detected -> adapt via direct agent rewrite (replace commands with project-specific equivalents from AGENTS.md).
   - Show diff, ask confirmation.

7. **Summary**
   - Report totals: X skills scanned, Y skills adapted, A agents scanned, B agents adapted, Z artifacts verified, W hooks checked/adapted.
   - Note any skipped or rejected resources.
   - **Write the totals BEFORE the first confirmation request, not after the last
     approval.** A run legitimately ends at the approval gate — the user may
     answer tomorrow, or not at all — and a summary placed behind that gate is a
     summary the run never produces. Say what was scanned and what is proposed,
     then ask; when the answers come, close with the same totals — per kind,
     how many were applied and how many rejected — not just a list of files.

</step_by_step>

## Verification

<verification>
[ ] IDE config directories detected.
[ ] Only project-local IDE config dirs used; plugin cache and user-level dirs skipped.
[ ] Arguments parsed correctly (type filter + name filter).
[ ] Skills adapted via `skill-adapter` subagents (parallel).
[ ] Agents adapted via `agent-adapter` subagents (parallel).
[ ] Root AGENTS.md artifact compared template-vs-artifact.
[ ] Hook scripts checked for stack-specific commands.
[ ] Diff shown and user confirmation obtained per resource.
[ ] Rejected adaptations reverted.
[ ] Summary produced.
</verification>

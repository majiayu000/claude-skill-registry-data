---
name: update
description: >-
  Use when the user asks to reconcile the project's AGENTS.md, CLAUDE.md and
  scaffolded files with the current flowai templates after a framework upgrade.
  Not for first-time setup, and not for tailoring the installed skills.
argument-hint: '[--instructions|--scaffolds|--all]'
---

# Task: Update Project Integration with flowai

## Overview

Reconcile project-owned flowai artifacts with the currently installed framework templates. This command does **not** manage the flowai CLI, does **not** sync or rewrite installed primitives, and does **not** adapt skills or agents. CLI lifecycle belongs to the standalone flowai CLI repository. Primitive adaptation belongs to `adapt`.

## Context

<context>
Most users receive flowai through an IDE plugin or a user-level install. Project-local installs still exist, but they are no longer the assumed path. Therefore this command treats framework sources as read-only inputs and writes only project-owned artifacts in the current working tree.

Project-owned artifacts:
- `AGENTS.md`
- `CLAUDE.md` when it is a project compatibility file or symlink
- scaffolded project docs/configs created by flowai setup commands

Read-only framework sources:
- project-local asset copies such as `.{ide}/assets/AGENTS.template.md`
- skill-local plugin assets such as `.{ide}/skills/update/assets/AGENTS.template.md`
- user-level assets such as `~/.claude/assets/AGENTS.template.md` or `~/.codex/assets/AGENTS.template.md`
- plugin cache files

If project-local flowai primitives exist under `.{ide}/skills/`, `.{ide}/agents/`, hooks, or scripts, this command reports that they can be adapted with `adapt`. It must not rewrite them.
</context>

## Rules & Constraints

<rules>
1. **No installer lifecycle.** Do not run an installer or a sync tool, and do not parse its output; this command edits project-owned files only.
2. **Project writes only.** Modify only current-project artifacts (`AGENTS.md`, `CLAUDE.md`, scaffolded docs/config). Never write plugin cache files, user-level skill directories, or installed primitive files.
3. **Read-only sources.** Read templates/assets wherever installed, including plugin/user-level locations, but treat those files as immutable. Read-only limits what you do to the file; it does not disqualify a copy that already shows local or uncommitted changes. Such a copy is still the template for this run: name its state in the report and compare against its current contents.
4. **Preserve user content.** Update framework-originated sections only. Keep project-specific sections and local conventions unless the user explicitly approves a change.
5. **Diff before write.** Show proposed per-file changes and ask for confirmation before writing.
6. **Cross-IDE.** Detect Claude Code, Cursor, OpenCode, and Codex config dirs when looking for project-local sources.
7. **Mandatory tracking.** Use a task management tool (todo write, TodoWrite, etc.) to track execution steps.
8. **No auto-commit.** Leave changes unstaged unless the user explicitly asks to stage or commit.
</rules>

## Instructions

<step_by_step>

1. **Detect scope and arguments**
   - Work from the current project root.
   - Parse flags:
     - no args or `--all` -> check instructions and scaffolded artifacts.
     - `--instructions` -> check only `AGENTS.md` / `CLAUDE.md`.
     - `--scaffolds` -> check only known scaffolded project artifacts.
   - Detect project IDE config dirs: `.claude/`, `.cursor/`, `.opencode/`, `.codex/`.

2. **Locate AGENTS template sources** (for `--instructions` / `--all`)
   - Check skill-local plugin asset paths first. When present, these are the most accurate source for plugin/user-level installs because the asset was copied next to the invoking command:
     - `.claude/skills/update/assets/AGENTS.template.md`
     - `.cursor/skills/update/assets/AGENTS.template.md`
     - `.opencode/skills/update/assets/AGENTS.template.md`
     - `.codex/skills/update/assets/AGENTS.template.md`
     - namespace-stripped plugin paths such as `*/skills/update/assets/AGENTS.template.md` when visible in the project.
   - Then check project-local asset paths:
     - `.claude/assets/AGENTS.template.md`
     - `.cursor/assets/AGENTS.template.md`
     - `.opencode/assets/AGENTS.template.md`
     - `.codex/assets/AGENTS.template.md`
   - Check user-level paths:
     - `~/.claude/assets/AGENTS.template.md`
     - `~/.cursor/assets/AGENTS.template.md`
     - `~/.config/opencode/assets/AGENTS.template.md`
     - `~/.codex/assets/AGENTS.template.md`
   - If any skill-local plugin asset exists, use it as the authoritative template source for this run. If other templates differ, report them as secondary/stale sources; do not switch to a project-local or user-level template by modified time.
   - If no skill-local template exists and multiple same-tier templates differ, report the paths and choose the newest modified file only after warning the user.
   - If none exist, stop with: "AGENTS.template.md not found. Update or install flowai through your plugin manager or flowai CLI, then rerun update."

3. **Read project instructions artifacts**
   - Read `./AGENTS.md`.
   - If `AGENTS.md` is missing, stop and tell the user to run `init` first. Do not create a new root file here.
   - Inspect `./CLAUDE.md`:
     - If it is a symlink to `AGENTS.md`, it is up to date.
     - If missing in a Claude Code project, propose creating a compatibility symlink to `AGENTS.md`.
     - If it is a regular file, compare it with `AGENTS.md`; propose replacing it with a symlink only after showing the diff/risk.

4. **Compare template against project artifact**
   - Compare template content against `AGENTS.md`.
   - Ignore unresolved placeholders such as `{{PROJECT_NAME}}` and `{{TOOLING_STACK}}`.
   - Focus on framework-originated sections: core rules, documentation rules, planning rules, TDD flow, acceptance-test flow, development commands, and safety constraints.
   - Classify each difference:
     - framework section missing or outdated -> propose update.
     - project-specific section -> preserve.
     - framework section customized by project -> propose a merge that keeps local constraints.
     - obsolete legacy sections (`documents/AGENTS.md`, `scripts/AGENTS.md`) -> propose collapsing them into root `AGENTS.md`.
   - Build the rule inventory with the bundled script, from this skill's directory, and paste its output into the report verbatim:
     ```sh
     python3 <this skill's directory>/scripts/compare_rules.py <template path from step 2> AGENTS.md
     ```
     It prints every named rule of the template (a list item opening with a bold label) that `AGENTS.md` does not carry under any heading, one per line with its template section, and then the template sections `AGENTS.md` has no heading for. Exit 2 means a path was wrong; fix the path and rerun. The script reads only; it never writes.
   - The inventory is the floor of the comparison, not its ceiling: also compare the wording of rules that are present, which the script does not judge.

5. **Check scaffolded artifacts** (for `--scaffolds` / `--all`)
   - Use known scaffold mappings from visible pack metadata when available. Also resolve documentation roles from AGENTS.md; for documentation artifacts, role bindings override template defaults.
   - Default known project scaffolds by role/type:
     - `SRS`
     - `SDS`
     - `.devcontainer/devcontainer.json`
     - `.devcontainer/Dockerfile`
     - `.devcontainer/init-firewall.sh`
     - `.devcontainer/setup-container.sh`
     - `deno.json`
     - `scripts/check.ts`
   - Only compare files that already exist in the project unless an explicit scaffold mapping says a missing file should exist.
   - Read the corresponding template/source if visible in the project-local install or skill-local plugin assets. If no source is visible, skip with a clear note instead of guessing.
   - Propose updates only when a framework-originated section is stale.

6. **Detect local primitives but do not adapt them**
   - Look for project-local flowai primitives:
     - `.{ide}/skills/flowai-*`
     - `.{ide}/skills/*` matching installed framework primitive names
     - `.{ide}/agents/*` matching installed framework agent names
     - flowai hook/script files under project IDE config dirs
   - Do not edit those files.
   - If any exist, report: "Project-local flowai primitives detected. Run adapt for primitive adaptation."

7. **Propose changes**
   - For each affected artifact, show:
     - source template path
     - current project section
     - proposed project section
     - reason for the change, including the practical risk or benefit. Example: if proposing the TDD `CHECK` step, explain that skipping it leaves formatter, linter, and regression failures undetected after GREEN.
   - Use a unified diff or compact before/after blocks. A diff accompanies the rule inventory from step 4; it never replaces it.
   - Address every rule the inventory lists by its name: propose adding it, or say why this project keeps it out. A summary such as "several planning rules are missing" or a wholesale replacement of `AGENTS.md` does not satisfy this.
   - Keep proposals per file so the user can approve or reject each one.

8. **Apply approved changes**
   - Ask for confirmation before each file write.
   - Apply only approved project-artifact edits.
   - Never modify read-only template/source files.
   - Never stage or commit unless the user explicitly asks.

9. **Verify**
   - Show the resulting `git diff -- AGENTS.md CLAUDE.md <resolved-SRS> <resolved-SDS> .devcontainer deno.json scripts/check.ts` limited to touched files.
   - Confirm plugin/user-level files and installed primitives were not modified.
   - End with a short summary of updated, skipped, and deferred items.

</step_by_step>

## Verification

<verification>
[ ] Did not run an installer or a sync tool of any kind.
[ ] Located a read-only framework template source or stopped with a clear install/update instruction.
[ ] Read actual project `AGENTS.md` and compared template content against the artifact, not only template git history.
[ ] Ran `scripts/compare_rules.py` and addressed every missing rule it listed by name.
[ ] Proposed only project-owned artifact changes.
[ ] Preserved project-specific sections and local conventions.
[ ] Asked confirmation before each write.
[ ] Did not modify plugin cache, user-level skill dirs, or installed primitive files.
[ ] Reported project-local primitive adaptation as a `adapt` follow-up when relevant.
[ ] Did not stage or commit automatically.
</verification>

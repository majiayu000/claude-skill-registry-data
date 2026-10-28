---
name: init
description: >-
  Use when the user asks to set a project up for flowai for the first time —
  writes AGENTS.md and the documentation skeleton for a new or an existing
  codebase. Not for reconciling an existing AGENTS.md with newer templates.
---

# Task: Initialize Project Agent Documentation

## Overview

Analyze the project, conduct an interview (for Greenfield projects), and
generate a single AGENTS.md file (root) with all project rules, a `CLAUDE.md` symlink
(for Claude Code compatibility), rules, and scaffolding.
Legacy three-file layouts (`documents/AGENTS.md`, `scripts/AGENTS.md`) are detected and collapsed into the single root file.
The agent uses template files from `assets/` as reference and writes files directly.

## Context

<context>
The user wants to bootstrap an AI agent's understanding of the project. The agent needs to autonomously explore the codebase, recognize the technology stack, understand the directory structure, and infer key architectural patterns.
- **Greenfield (New Projects)**: Requires interviewing the user, creating scaffolding (`documents/`, configs), and setting up rules.
- **Brownfield (Existing Projects)**: Requires discovery, reverse-engineering architecture, and **collapsing legacy multi-file layouts** into the single root file.

**File Structure**: init produces a single `./AGENTS.md` file containing all sections:
- Project rules, metadata, vision, architecture, key decisions
- Documentation rules (task format, readability floor, chat output style, doc hierarchy). The SRS and SDS structures are NOT in AGENTS.md — they live in the pack-level templates `assets/SRS.template.md` and `assets/SDS.template.md`, which step 9 reads
- Development commands (standard interface, detected commands)
- Planning rules, TDD flow, code documentation rules
</context>

## Rules & Constraints

<rules>
1. **No Hallucinations**: Only document tooling and architecture that is explicitly found in the codebase or provided by the user.
2. **Standard Format**: Generated files must follow the provided templates in `assets/`.
3. **Idempotency (Brownfield)**: If components already exist, show diffs and ask for per-file confirmation before applying changes, under the turn rule in constraint 8.
4. **Greenfield/Brownfield Detection**: The agent determines project type autonomously by analyzing output of the analysis script (file count, stack, file tree, presence of config files). Do NOT rely on an `is_new` flag from any script.
5. **Scripts are read-only**: Analysis scripts must NOT create, write, or modify any files. All file creation is the agent's responsibility.
6. **No rule copying**: Do NOT copy rules to IDE-specific rules directories. Rule management is outside init scope.
7. **Mandatory**: The agent MUST use a task management tool (e.g., todo write) to track the execution steps.
8. **Per-File Diff Confirmation**: For existing files, always show the diff to the user and ask for confirmation before applying. Never silently overwrite. **A diff is the proposed unified diff of that file, shown under the file's path** — a prose summary, a change list, an excerpt, or a grouped description of "what will change" is not a diff, and a bullet list covering several files is not one either. **Ask a separate yes/no per file; one grouped "May I apply these changes?" is not a per-file confirmation** and does not authorize any of the writes. The project's instruction file may prefer decision-level narration over diffs for ordinary work ("narrate upward, not in diffs"); that preference does not apply here — this step exists to let the user read the exact change to a file they own before it is replaced. **Asking ends the turn.** The write belongs to a LATER turn, after the user's answer has arrived. A question and the write it asks about cannot share a turn — that is not a confirmation, it is a narration of a decision already taken. "May I apply this?" followed by the edit tool in the same turn means the confirmation never happened.
9. **Preserve User Content**: In brownfield, extract and preserve user's existing instructions. Templates are fallbacks for greenfield only.
10. **Collapse, Don't Fragment**: In brownfield, if legacy `documents/AGENTS.md` or `scripts/AGENTS.md` exists, merge their unique content into the root `./AGENTS.md` and delete the originals after user confirmation.
</rules>

## Instructions

<step_by_step>

1. **Initialize**
   - Use a task management tool (e.g., todo write) to create a plan based on these steps.

2. **Analyze Project**
   - Run the analysis script to detect stack, inventory components, and verify setup. The script ships INSIDE this skill's directory, next to this SKILL.md (`<skill-dir>/scripts/generate_agents.ts`, e.g. `.claude/skills/init/scripts/generate_agents.ts` or `.codex/skills/init/scripts/generate_agents.ts`) — it is NOT in the project's own `scripts/`. Run it from the project root by that path; a missing `scripts/generate_agents.ts` at the project root is the expected state, not a blocker:
     ```bash
     deno run --allow-read <skill-dir>/scripts/generate_agents.ts .
     ```
   - Read the JSON output. It wraps in `{ "ok": bool, "result": {...} }`. The `result` field contains: project metadata (`is_new`, `stack`, `file_tree`, `readme_content`), component `inventory`, and `verification` checks.
   - **Decision Point** (agent judgment, NOT a script flag):
     - Analyze file count, presence of source files, config files and existing documentation.
     - If project appears empty or minimal (no source files, no meaningful configs) -> treat as **Greenfield**.
     - If project has existing code, configs, or documentation -> treat as **Brownfield**.

3. **Greenfield Workflow (Interview)**
   - **Condition**: Only if **Greenfield**.
   - **Action**: Launch the `interviewer` subagent (or conduct Q&A inline if subagent unavailable).
     - **Prompt**: "You are helping initialize a new (Greenfield) project.
       Conduct a brief interview to gather:
       1. **Project Name**: Name?
       2. **Vision Statement**: What is the long-term goal and value?
       3. **Target Audience**: Who is this for?
       4. **Problem Statement**: What problem are we solving?
       5. **Solution & Differentiators**: How do we solve it and why is it better?
       6. **Risks & Assumptions**: What could go wrong?
       7. **Tech Stack**: Languages/Frameworks? (If not detected)
       8. **Architecture**: Patterns?
       9. **Key Decisions**: Tools/Methodologies?
       10. **Deno Tooling**: Do you want to build tooling around the project on Deno? (yes/no)
       11. **Devcontainer**: Would you like to set up a devcontainer for reproducible development environments? (yes/no)

       Return a SINGLE JSON object: {
       "project_name": "...",
       "vision_statement": "...",
       "target_audience": "...",
       "problem_statement": "...",
       "solution_differentiators": "...",
       "risks_assumptions": "...",
       "stack": ["..."],
       "architecture": "...",
       "key_decisions": "...",
       "preferences": ["tdd", "strict-mode", ...],
       "use_deno_tooling": boolean,
       "use_devcontainer": boolean
       }"

4. **Brownfield Workflow (Discovery & Extraction)**
   - **Condition**: Only if **Brownfield**.
   - **Action**: Analyze the project to infer architecture and key decisions.
     - Read key config files (`package.json`, `deno.json`, `README.md`, etc.).
     - Infer:
       - **Architecture**: (e.g., "React SPA", "Express API", "CLI Tool").
       - **Key Decisions**: (e.g., "Tailwind for styling", "Jest for testing").
   - **Collapse legacy layout** (if detected):
     - Check `legacy_layout_detected` from the analyzer output.
     - If legacy layout found (`documents/AGENTS.md` and/or `scripts/AGENTS.md` exist):
       1. Read all existing files: `./AGENTS.md`, `./documents/AGENTS.md`, `./scripts/AGENTS.md`.
       2. Merge by section into the root file: documentation rules content → `## Documentation Rules` section, scripts content → `## Development Commands` section, everything else stays in its existing root section.
       3. Show the merged diff to the user and ask for confirmation.
       4. Overwrite `./AGENTS.md` with the merged result.
       5. `git rm` the two sub-files (`documents/AGENTS.md`, `scripts/AGENTS.md`) and their `CLAUDE.md` symlinks (`documents/CLAUDE.md`, `scripts/CLAUDE.md`) if they exist.
     - If no legacy layout: proceed with normal brownfield discovery against `./AGENTS.md`.
     - **Important**: The content from the user's existing files takes priority over template content. Templates are fallbacks only.

5. **Component Inventory**
   - Use the `inventory` section from the analysis output (step 2) to check which components exist.
   - Report findings to user as a checklist.
   - For **Brownfield**: ask "Create missing components? Update existing via diff? [create missing / update all / select]"

6. **Generate AGENTS.md File**
   - Read the pack-level template at `assets/AGENTS.template.md` (reference for `./AGENTS.md`, single file containing all sections).

   - **For Greenfield**: Fill template with interview data. Replace `{{PLACEHOLDERS}}` with actual values.

   - **For Brownfield**:
     - `./AGENTS.md`: Use the template structure. Fill with data inferred from the project. Preserve user's custom PROJECT_RULES (content between `---` and the next `## ` heading). If legacy layout was collapsed in step 4, the merged content is already prepared — use it.
     - **Write step 4's inferences into `## Architecture` and `## Key Decisions` by name.** An existing AGENTS.md whose sections are blank has nothing to preserve there — a blank section is the section you were asked to fill, not user content. Recording the same material in the SRS, the SDS or the init-context task file does not discharge this: those are different documents, and a reader of AGENTS.md never sees them.

   - **Output**: a single `./AGENTS.md` file.
     - If file does not exist: create it, report to user.
     - If file exists: show diff to user, ask for confirmation before writing.

7. **Claude Code Compatibility (CLAUDE.md Symlink)**
   - Create a single relative symlink: `./CLAUDE.md` -> `./AGENTS.md`.
   - Symlink handling:
     - **If `CLAUDE.md` does not exist**: create the symlink, report to user.
     - **If `CLAUDE.md` exists and is already a correct symlink to `AGENTS.md`**: skip silently.
     - **If `CLAUDE.md` exists as a regular file or wrong symlink**: warn the user, show the current content/target, and ask for confirmation before replacing with the symlink.
   - **Legacy cleanup**: If legacy sub-directory `CLAUDE.md` symlinks exist (`documents/CLAUDE.md`, `scripts/CLAUDE.md`), they should already be deleted during the legacy-collapse step (step 4). If they still exist at this point, delete them now.

8. **OpenCode Compatibility Check**
   - The `inventory` section from the analysis output (step 2) includes `opencode_json.exists` and `opencode_json.has_subdirectory_globs`.
   - If `opencode_json.exists` is `true` and the `instructions` array contains references to `documents/AGENTS.md` or `scripts/AGENTS.md`: propose **removing only** those stale entries. Do NOT add an `AGENTS.md` replacement entry — OpenCode auto-loads the root file.

9. **Generate Documentation**
   - Resolve documentation roles from the generated `AGENTS.md`: `SRS`, `SDS`, `tasks`, and `index`. If a role is missing, add it to AGENTS.md before generating docs.
   - Generate core documentation files at the resolved role paths:
     - `SRS`: Read the pack-level template at `assets/SRS.template.md` and use its section and field structure verbatim (`## 3. Functional Reqs` with per-FR `**Desc:**` / `**Rationale:**` / `**Scenario:**` / `**Acceptance:**` / `**Status:**` fields — `**Rationale:**` is mandatory: write why each requirement exists, from the interview answers or the inferred context). Fill based on interview data (Greenfield) or inferred context (Brownfield). Skip if file exists and has more than 50 lines.
     - `SDS`: Read the pack-level template at `assets/SDS.template.md` and create the initial structure from it (`## 3. Components` with per-component `**Purpose:**` / `**Interfaces:**` / `**Deps:**` fields). Skip if file exists and has more than 50 lines.
     - `tasks` directory:
       - For **Brownfield**: Create an init-context task using the role's layout with "Discovered Context" (file tree) and README summary.
       - For **Greenfield**: Directory will be created on first use by planning/answer skills. No need to initialize.
   - **Note**: Use LLM capabilities to generate high-quality, context-aware content from actual project data -- not empty placeholders.

10. **Configure Development Commands**
   - Read analysis output to get detected stack.
   - **Check Interview Data**: If `use_deno_tooling: true`, FORCE usage of `configure-deno-commands`.
   - **Skill Lookup**: For each stack item, check if a specialized skill exists (e.g., `Deno` -> `configure-deno-commands`).
   - If specialized skill exists: Read and follow its `SKILL.md`.
   - If NO specialized skill:
     1. Detect the project's existing command runner (Makefile, package.json scripts, deno.json tasks, justfile, etc.).
     2. Ask user for preferred approach if none detected.
     3. Create standard command interface (`check`, `test`, `dev`, `prod`) using the project's native command runner. For example, for Node.js projects add scripts to `package.json`; for Make-based projects add targets to `Makefile`. Do NOT create a `scripts/` directory with wrapper scripts if the project's command runner can handle commands directly.
     4. Only create helper scripts in a separate directory if the command logic is too complex for inline commands, and follow existing project conventions for script placement.
   - **Skip condition**: If standard commands already exist in the project's command runner and user chose "create missing" -> skip.
   - **Verify**: Run `check` command to ensure it works.
   - **Record the commands in `./AGENTS.md`**: step 6 wrote the file before these commands existed, so its `### Detected Commands` and `### Command Scripts` sections are still empty. Fill them now: under `### Detected Commands`, one line per standard command (`check`, `test`, `dev`, `prod`) with the exact invocation the project's runner uses (e.g. `deno task check`, `make check`, `npm run check`); under `### Command Scripts`, one line per helper script the step created with its path and purpose, or a one-line note that all commands are inline in the runner config. An empty section here is a missing step, not a placeholder to leave for later.

11. **Devcontainer Setup (Optional)**
   - **For Greenfield**: Check `use_devcontainer` from interview data.
   - **For Brownfield**: Ask the user: "Would you like to set up a devcontainer for reproducible development environments?"
   - **If user declines**: Skip this step entirely.
   - **If user agrees**: Delegate to the `setup-ai-ide-devcontainer` skill. Read and follow its `SKILL.md`.

12. **Cleanup & Verify**
    - Remove temporary files: `project_info.json`, `interview_data.json` (if created).
    - Re-run the analysis script (same skill-directory path as in step 2) to verify all components are in place:
      ```bash
      deno run --allow-read <skill-dir>/scripts/generate_agents.ts .
      ```
    - Check the `verification` section. If `passed` is false (exit code 1), fix the issues before proceeding.
    - Additionally verify: development commands are configured, the `check` command runs successfully, and `./AGENTS.md` lists those commands under `### Detected Commands` (step 10).
    - **Verify single file**: Confirm that only `./AGENTS.md` exists and no legacy `documents/AGENTS.md` or `scripts/AGENTS.md` remain.

</step_by_step>

## Verification

<verification>
[ ] Analysis script run and output read.
[ ] Greenfield/Brownfield determined by agent judgment (not `is_new` flag).
[ ] Interview conducted (Greenfield) or discovery performed (Brownfield).
[ ] For Brownfield with legacy layout: three files collapsed into single root file, originals deleted.
[ ] For existing files: diffs shown and per-file confirmation requested.
[ ] Existing user content preserved (custom rules, merged sections used as-is).
[ ] Single AGENTS.md file generated at root.
[ ] `CLAUDE.md` symlink created at project root.
[ ] No legacy sub-directory AGENTS.md or CLAUDE.md files remain.
[ ] `documents/` folder populated with generated content from actual project data.
[ ] Development commands configured (scripts created + config updated + recorded in `./AGENTS.md`).
[ ] OpenCode compatibility checked (if applicable) via `inventory` output.
[ ] Analysis script re-run passes (exit code 0, `verification.passed: true`).
[ ] Check command runs successfully.
[ ] Devcontainer: user asked; if agreed, `.devcontainer/devcontainer.json` exists and is valid JSON.
[ ] Temporary files cleaned up.
</verification>

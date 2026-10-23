---
name: clean
description: Removes unnecessary project-directory files with approval. Use when deleting
  build artifacts, finding unused files, or clearing temporary files.
metadata:
  opencode/autoinvoke: 'false'
---

# Project File Cleaner

Orchestrate 6 parallel cleanup agents to analyze and remove unnecessary files from project directories with comprehensive safety measures and user confirmation checkpoints.

## Arguments

Parse `$ARGUMENTS` for:

- **target-directory**: First non-flag argument (default: `.`)
- **--dry-run**: Preview only, no changes
- **--report-only**: Generate report without deletions
- **--safe-mode**: Extra confirmation per category

**Questions:** class `confirm-destructive` (both deletion prompts); headless (no question tool or chat turn): behave as `--report-only`. See `~/.config/opencode/shared/references/question-policy.md`.

### Deprecated: `--include-git`

If `$ARGUMENTS` contains `--include-git`: ignore the flag, keep every other argument unchanged, and display this notice exactly once, before Phase 0 (including before any `--dry-run` stop):

> `--include-git` is deprecated and ignored. This skill cleans project-directory files only — it performs no Git audit and no Git cleanup. For branches, worktrees, remotes, stashes, tags, PRs, or issues, run `/git-cleanup` separately. Never invoked automatically on your behalf.

Never auto-chain `/git-cleanup`, and never treat `--include-git` as consent to run it.

### Scope and Git-only requests

This skill cleans files present in the project directory only. It never audits or changes Git refs, history, or submodules, and `.git` metadata stays protected.

If the request concerns only Git resources, STOP before Phase 0 and deploy no agents. Route branches, worktrees, remotes, stashes, tags, PRs, or issues to `/git-cleanup`; say history rewriting and submodule cleanup are out of scope for both skills.

## Phase 0: Setup

1. **Validate target directory** exists
2. **Detect project type** using: `~/.config/opencode/skills/clean/scripts/detect-project-type.sh "$TARGET_DIR"`
3. **Read safety configuration** from `~/.config/opencode/skills/clean/references/safety-config.md`
4. **Create working directory**: `$TARGET_DIR/.cleanup-analysis/findings/`
5. **Initialize progress tracking** with the task tools for all phases
6. **If --dry-run**: Display analysis plan and **STOP**

## Phase 1: Parallel Agent Deployment

Read agent prompts from `~/.config/opencode/skills/clean/references/agent-prompts.md`.

Deploy all 6 agents in a **SINGLE message** with **MULTIPLE parallel subagent invocations** using subagent type `project-file-cleaner`:

| Agent      | Findings File (orchestrator-written) |
| ---------- | ------------------------------------ |
| Code Files | `findings/code-files.md`             |
| Binaries   | `findings/binaries.md`               |
| Assets     | `findings/assets.md`                 |
| Docs       | `findings/documentation.md`          |
| Config     | `findings/config.md`                 |
| Docker     | `findings/docker.md`                 |

Substitute `{{TARGET_DIR}}` and `{{PROJECT_TYPE}}` in each prompt. Each agent receives: target directory, project type, safety configuration, and specific search patterns. Agents are read-only: they return findings inline in the Common Output Format; they never write files or run commands.

**Persistence (orchestrator-owned)**: as each native `subagent` call returns, write its returned findings verbatim to that agent's findings file under `$TARGET_DIR/.cleanup-analysis/findings/` using the exact file names and Common Output Format above — `generate-report.sh` parses those paths and headings. An empty, missing, or malformed return is a failed agent: STOP before Phase 2, report the failed category, and retry or request user intervention. Never treat missing output as zero findings or reuse files from a previous run. Proceed only after all six valid returns from this run have been persisted; verify each file exists and matches the Common Output Format. A valid zero-findings response still includes the required headings and summary.

## Phase 2: Findings Consolidation

After all agents complete:

1. Read all findings files
2. Deduplicate across agents
3. Calculate space savings: `du -h "$filepath"` for each file
4. Categorize by risk level (low/medium/high)

## Phase 3: Report Generation and User Review

1. Run: `~/.config/opencode/skills/clean/scripts/generate-report.sh "$TARGET_DIR"`
2. Run safety validation: `~/.config/opencode/skills/clean/scripts/validate-safety.sh "$TARGET_DIR/.cleanup-analysis/cleanup-report.md"`
3. Fix any violations before proceeding
4. **If --report-only**: Display report summary and **STOP**
5. Present findings to user with ask the user (show report / summary / proceed / cancel)
6. **If --safe-mode**: Ask confirmation per category

## Phase 4: Safe Execution

1. Create backup list at `$TARGET_DIR/.cleanup-analysis/removal-list.txt`
2. Final confirmation with ask the user before any deletions
3. Execute removal, tracking success/failure counts
4. Handle errors gracefully (continue on single file failure)

## Phase 5: Verification

1. Verify files removed, no broken symlinks, project integrity
2. Calculate actual space recovered
3. Generate final summary with results, analysis file locations, and next steps

---

## Quality Standards

Each cleanup agent must: focus on specific category, execute 10+ diverse searches, include file sizes, check against safety config, flag uncertain cases for review. Each finding must include: full path, size, category, justification, risk level, confidence level.

## Important Notes

- Act as orchestrator - coordinate cleanup agents, don't analyze files directly
- Deploy all 6 agents in parallel (single message with 6 Agent calls)
- Safety first - always validate before deletion
- User confirmation required before any destructive operations
- Preserve all cleanup reports and removal lists

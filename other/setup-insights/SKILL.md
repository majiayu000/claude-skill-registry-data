---
description: Bootstrap the Insight Coaching System in the current project
argument-hint: "[optional: project name or specific conventions to include]"
---

# Setup Insight Coaching System

You are bootstrapping the Insight Coaching System for the current project. This system provides:
- Prompt coaching hooks that detect task type and inject reminders
- Session logging and friction detection
- Pre-compaction insight injection to survive context compaction
- Quality gates on Stop and SubagentStop events

Think hard about the current project before starting. Analyze its structure, tools, and conventions to adapt the coaching system appropriately.


## Step 1: Analyze the Current Project

Read and analyze these files (skip any that don't exist):
- `CLAUDE.md` in the project root
- `package.json` in the project root
- Project directory structure (ls the root and src/ if it exists)

From this analysis, determine:
- **Project name**: from package.json `name` field or directory name
- **Package manager**: look for bun.lockb (bun), yarn.lock (yarn), pnpm-lock.yaml (pnpm), or default to npm
- **Validation command**: look for a `validate` script in package.json. If none exists, compose one from available scripts (format:check, lint, typecheck, test, build)
- **Format command**: the formatter command (e.g., `bun format`, `npm run format`, `yarn format`)
- **Test command**: the test runner command
- **Build command**: the build command
- **Lint command**: the linter command
- **Languages/framework**: TypeScript? JavaScript? React? Vue? Svelte? Next.js? etc.
- **Theme system**: does it have dark/light mode? What CSS approach?
- **i18n**: is it bilingual/multilingual?
- **Existing conventions and gotchas** from CLAUDE.md

Store all discovered values for use in subsequent steps. Use `$PKG` as shorthand for the package manager command (e.g., `bun`, `npm run`, `yarn`, `pnpm`).

Construct these key variables:
- `VALIDATE_CMD`: e.g., `bun validate`, `npm run validate`, `yarn validate`
- `FORMAT_CMD`: e.g., `bun format`, `npm run format`
- `PKG_RUN`: e.g., `bun`, `npm run`, `yarn`, `pnpm`


## How the templates work

All file contents live in this skill's `templates/` directory (relative to this SKILL.md). Create each target file from its template with the substitutions below. Do not rewrite template contents from memory.

Substitutions:
- Hook scripts (`templates/hooks/*.cjs`): replace `bun validate` with `VALIDATE_CMD` and `bun format` with `FORMAT_CMD`.
- `templates/settings.local.json`, `templates/MY_INSIGHTS.md` and `templates/claude-md-sections.md`: replace every literal `VALIDATE_CMD` and `FORMAT_CMD` placeholder (and any `bun validate` / `bun format`) with the actual commands.

Example for one hook: `sed -e 's/bun validate/<VALIDATE_CMD>/g' -e 's/bun format/<FORMAT_CMD>/g' <skill-dir>/templates/hooks/prompt-enhancer.cjs > .claude/hooks/prompt-enhancer.cjs`.

## Step 2: Create `.claude/insights/MY_INSIGHTS.md`

First read the universal insights file at `~/.claude/insights/UNIVERSAL_INSIGHTS.md`. Then create `.claude/insights/MY_INSIGHTS.md` from `templates/MY_INSIGHTS.md` (set `last_updated` to today's date, fill the final `## Project: <project-name>` section with the discovered stack, validation and format commands).

IMPORTANT: replace every literal `VALIDATE_CMD` with the actual command (e.g., `npm run validate`) and every `FORMAT_CMD` with the actual format command. The prompt-template code blocks in the template use spaced backticks (` ` `) as an escape: write them as real triple backticks in the output file.

If the argument to this skill includes specific conventions or a project name, incorporate them into the `## Project:` section.

## Step 3: Create hook scripts in `.claude/hooks/`

Create `.claude/hooks/` if it does not exist, then create the 6 scripts from `templates/hooks/` (apply the substitutions above): `prompt-enhancer.cjs`, `precompact-inject.cjs`, `session-logger.cjs`, `session-start.cjs`, `session-end.cjs`, `friction-logger.cjs`.

## Step 4: Create `.claude/settings.local.json`

Create it from `templates/settings.local.json` (replace the `VALIDATE_CMD` and `FORMAT_CMD` placeholders in the prompt text strings). Keep the exact JSON structure.

## Step 5: Update CLAUDE.md

If `CLAUDE.md` does not exist in the project root, create a minimal one with the project name and basic commands section. Then, for each section of `templates/claude-md-sections.md` (Pre-Commit Checklist, UI Changes, Task Clarity, Git Workflow) that does NOT already exist in CLAUDE.md, append it at the end, with `VALIDATE_CMD` and `FORMAT_CMD` replaced by the actual commands. Do NOT duplicate sections that already exist.

## Step 6: Update .gitignore

Read the project's `.gitignore`. If it does NOT already contain the coaching entries, append the block from `templates/gitignore-block.txt`. If they already exist, skip this step.

## Step 7: Create Log Directories

Create `.claude/logs/.gitkeep` and `.claude/logs/archive/.gitkeep` (empty files) with `mkdir -p` and `touch`.

## Step 8: Verify Setup

Run these verification checks and report results:

1. **Syntax check all hooks:** Run `node --check .claude/hooks/prompt-enhancer.cjs` (and all other 5 `.cjs` files). Report pass/fail for each.
2. **JSON validation:** Run `node -e "JSON.parse(require('fs').readFileSync('.claude/settings.local.json','utf8')); console.log('OK')"` to verify settings.local.json parses correctly.
3. **Smoke test prompt-enhancer:** Run `echo '{"prompt":"fix the login bug"}' | node .claude/hooks/prompt-enhancer.cjs` and verify it returns plain text containing a reminder (not JSON).
4. **Smoke test bypass mode:** Run `echo '{"prompt":"! just do it"}' | node .claude/hooks/prompt-enhancer.cjs` and verify it exits cleanly with no output (exit code 0).

Report each check as PASS or FAIL with details.

## Step 9: Verify Slash Commands

Check if user-level commands exist at `~/.claude/commands/`:
- `coach.md`
- `patterns.md`
- `autopilot.md`
- `retro.md`

If ALL 4 exist, report "Slash commands: OK".
If any are missing, warn: "WARNING: Missing user-level slash commands at ~/.claude/commands/. The coaching system works best with /coach, /patterns, /autopilot, and /retro commands. Set these up separately."

## Final Report

After all steps complete, present the summary from `templates/final-report.txt`, filling in the project name, detected package manager, validate and format commands, and the PASS/FAIL results of the verification steps.

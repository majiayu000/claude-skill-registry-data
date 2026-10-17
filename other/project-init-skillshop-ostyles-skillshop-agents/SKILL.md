---
name: project-init
description: "Bootstraps a brand-new, empty project with a complete, optimized file & directory structure plus an interactive LLM onboarding dialog. Use when the user wants to start a fresh/pristine project from scratch and have the LLM set it up via a guided, dynamic, stack-agnostic conversation covering all project areas (goal, stack, tooling, docs, secrets, platform). Trigger: /project-init"
trigger: /project-init
---
# /project-init

Start a fresh, virgin project from scratch. This skill runs an interactive, dynamic
onboarding dialog with the user, then scaffolds a complete, optimized directory &
file structure and writes the onboarding results into the project's ops/ docs so
that future LLM sessions (via the session-start trigger) can
pick up the context automatically.

## What this is for

- A completely empty folder that should become a new project.
- The user wants the LLM to *ask* the right questions rather than guess.
- All project areas must be covered: goal, stack, structure, tooling, docs,
  secrets/tokens, platform context.
- Output is a reusable, consistent baseline that the session-start routine
  can read back in every session.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If the user invoked `/project-init -help` or `/project-init -h` (no other args),
print the contents of the `## Usage` section verbatim and stop.

Otherwise follow the steps below in order. Do not skip steps.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Establish target directory

Ask the user for the absolute path of the new project (or use the current
directory). Confirm it is empty or near-empty. If it already contains a project,
stop and warn before overwriting anything.

```
Target directory: <path>
Existing files:   <list or "none">
Proceed? (yes/no)
```

Only continue after explicit confirmation.

**PROTECTION RULE - never `~/.claude/`:** The target directory must under no
circumstances be `C:\Users\ostol\.claude\` (or its subdirectories).
This path is sacred and must NEVER be modified by this skill.
If the user proposes `~/.claude/` as target, abort immediately. The generator
(`scripts/init.ps1`) blocks such paths technically by itself.

### Step 3 - Run the interactive onboarding dialog

Ask the user the following areas ONE AT A TIME, in this order. Adapt follow-up
questions to previous answers (dynamic, not a fixed form). Keep each question
short and direct.

1. **Goal** - What is the project? One sentence. What problem does it solve?
2. **Stack** - Language/framework (Node/TS, Python, Go, Rust, ...). Confirm
   package manager. If unknown, propose a sensible default and let user accept/change.
3. **Directory structure** - Based on stack, propose a layout (src/, tests/,
   docs/, ops/). Confirm or adjust.
4. **Tooling** - Lint, formatter, tests, CI, git hooks, type-check. Confirm
   which to include.
5. **Docs / Ops** - Explain that ops/ holds manifest.md, tracking.md,
   sprints/. Confirm naming conventions.
6. **Secrets / Tokens** - Which external services/APIs? Where do secrets live
    (.env, vault)? NEVER log full secrets - only masked preview.
7. **Platform context** - Deployment target (local, cloud, serverless),
   platforms (web, cli, api, mobile).
8. **Blockers / Open** - Anything currently blocking or undecided?

After each answer, reflect it back in one line so the user can correct.

### Step 4 - Generate the structure

Run the generator script. It reads the collected answers (you pass them as
arguments / a JSON file) and creates the full tree.

See `scripts/init.ps1` for the implementation. Invoke it like:

```powershell
& "<SKILL_DIR>/scripts/init.ps1" -ProjectDir "<path>" -AnswersFile "<path/to/answers.json>"
```

Where `answers.json` is a JSON object you build from the dialog, e.g.:

```json
{
  "name": "my-app",
  "goal": "Track personal finances.",
  "stack": "node-ts",
  "pkgManager": "npm",
  "layout": "src/tests/docs/ops",
  "tooling": ["eslint", "prettier", "vitest", "github-actions"],
  "docs": ["manifest", "tracking", "sprints"],
  "secrets": [".env (gitignored)"],
  "platform": ["web", "api"],
  "blockers": "none"
}
```

The script:
- Creates the directory tree.
- Writes `CLAUDE.md` (project rules and configuration).
- Writes `ops/manifest.md` (goal + scope from answers).
- Writes `ops/tracking.md` (status template, blocker field).
- Writes `ops/sprints/.gitkeep` + `ops/sprints/README.md`.
- Writes `.gitignore` (node_modules, dist, .env, etc. - stack-aware).
- Writes `README.md` (project title + goal stub).
- Scaffolds a minimal entry file appropriate to the stack (only a stub, no logic).

### Step 5 - Finalize & hand off

Print a concise summary of what was created:

```
Project <name> initialized in <path>
  Structure: <tree in 5-8 lines>
  Config:   CLAUDE.md created (project rules)
  Ops:       manifest.md, tracking.md, sprints/
  Secrets:   <masked preview or "none">
  Next step: type "weiter" to start session start routine.
```

Tell the user: from now on, typing "weiter" in this project triggers the
Session-Start-Routine that reads manifest/tracking/sprints automatically.

## Usage

```
/project-init                 # interactive onboarding in current directory
/project-init <path>          # interactive onboarding in <path>
/project-init -help          # show this usage block and stop
```



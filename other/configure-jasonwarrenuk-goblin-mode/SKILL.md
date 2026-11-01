---
name: "Mission Control: Configure"
description: "Write or revise a project's .claude/mission-control.json by interview: the shared resources and how to detect them busy, the gated commands, the check commands, the convention files, the conventions that live only in the user's head and the human gates"
when_to_use: "When a repository has no .claude/mission-control.json and the user wants to run mission control on it, when a run exposed a convention that was not written down, or when a resource, port or command changed. CHIRPdb's file is the worked example."
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: mission-control
  goblin-spinner: surveying ports|listing gates|writing the config
disable-model-invocation: true
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash(python3:*)", "Bash(git:*)", "Bash(ls:*)", "AskUserQuestion"]
argument-hint: "(no arguments)"
---

# Mission Control: Configure

The config is what makes the package generic: every resource, gate, command and convention a run leans on comes from this file, so the coordinator never has to assert one. Schema: `${CLAUDE_PLUGIN_ROOT}/references/config.md`; worked example: `${CLAUDE_PLUGIN_ROOT}/references/mission-control.example.json`.

## Step 1: What exists

`python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/mc.py detect`. Exit 0: read the file and offer to revise it section by section. Exit 2: `mc.py init` writes a skeleton to revise.

## Step 2: Survey the repository

Read, where present: the task runner's definitions (`pyproject.toml` `[tool.poe.tasks]`, `package.json` scripts, a Makefile, a Taskfile), the local stack's config (`supabase/config.toml`, `docker-compose*.yml`) for ports, the project's CLAUDE.md and `.claude/rules/` for conventions, `.claude/hooks/` for what the project already guards. From these, draft:

- **resources**: anything one process or one database must hold at a time: a local database stack, each port a server binds, each worker, the hosted project. For each: the `gate` globs over the commands that touch it, the `probe` (ports, a process pattern, a database DSN), `approve_in_slot`, `run_from`, `reset`, `notes`.
- **commands**: test, lint, contract or schema regeneration, a stack status printer.
- **conventions**: the files a brief should send a session to read.
- **human_gates**: hosted reads, credentials, writes, merges, anything irreversible; the project's own words where its rules have them.

## Step 3: Interview

One AskUserQuestion per section, showing the draft and asking what is wrong or missing. Then one free-text question: *which conventions does this project have that are written nowhere?* Each answer goes into `facts` in the user's words. The changelog rule and the env-file layout were the two that bit on the first run; ask about both by name when the survey found no written rule for them.

## Step 4: Write and prove

Write the file with the keys in the schema's order. Then `mc.py detect` (exit 0) and `mc.py probe` (every resource answers; `unreachable` on a probe is reported and left for the user to fix the DSN). Finish with a dry gate check: `mc.py check --command "<one gated command>"` with no run active prints `decision: null`, which is right; the gate only binds during a run.

Offer to commit the file (`chore(mission-control): project config`); commit on a yes.

## Never

Mark a hosted resource `approve_in_slot`; invent a port or a DSN the survey did not find; write a `facts` entry the user did not say.

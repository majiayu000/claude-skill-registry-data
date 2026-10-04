---
name: setup-codex-engineering-workflow
description: Establishes repo-local configuration for the Codex Engineering Workflow Pack. Use when starting the pack in a repo, when workflow skills lack project context, or when issue/docs/test/handoff locations need to be discovered and recorded.
---

# Setup Codex Engineering Workflow

Set up the repo-local context that the other workflow skills read before planning, debugging, testing, issue writing, or handoff.

This skill is local-first. Prefer markdown files in the current repo. Treat GitHub or any remote issue tracker as optional, never required.

## What This Skill Produces

When approved by the user, create or update repo-local guidance under `docs/agents/`.

Default layout:

```txt
docs/agents/
  issue-tracker.md
  domain.md
  test-commands.md
  handoff.md
  issues/
docs/adr/
CONTEXT.md
```

Do not overwrite existing configuration without showing the planned changes first.

## Read First

Inspect the repo before asking questions.

Look for:

- Package manager files: `package.json`, lockfiles, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, or similar.
- Existing scripts: test, typecheck, lint, format, e2e, dev.
- Existing docs: `README.md`, `docs/`, `CONTEXT.md`, `docs/adr/`, `specs/`, `plans/`.
- Existing issue conventions: `docs/agents/issues/`, `.scratch/`, `issues/`, `.github/ISSUE_TEMPLATE/`.
- Existing handoff notes: `docs/agents/handoffs/`, `handoffs/`, temp notes, or project docs.
- Git remote only as a clue. Do not assume GitHub issues are the tracker.

Use fast search commands when available:

```powershell
rg --files
```

## Decision Model

Make recommendations from repo evidence. Ask the user only when the answer cannot be inferred safely.

Decisions to establish:

1. Issue tracker
2. Docs directory
3. ADR directory
4. Domain language document
5. Test commands
6. Package manager
7. Agent handoff directory
8. Local issue directory

Default choices:

- Issue tracker: local markdown.
- Docs directory: `docs/agents/`.
- ADR directory: `docs/adr/`.
- Domain language document: `CONTEXT.md`.
- Handoff directory: `docs/agents/handoffs/`.
- Local issue directory: `docs/agents/issues/`.

## Workflow

### 1. Explore

Read the current repo structure and existing docs.

Produce a short findings list:

- Detected stack and package manager.
- Detected test commands.
- Existing docs and ADR locations.
- Existing issue or handoff conventions.
- Missing pieces.

Do not create files during exploration.

### 2. Recommend

Present a setup plan before writing.

Use this shape:

```md
## Proposed Workflow Setup

Issue tracker: local markdown at `docs/agents/issues/`
Docs directory: `docs/agents/`
ADR directory: `docs/adr/`
Domain language: `CONTEXT.md`
Package manager: <detected or proposed>
Test commands:
- unit: <command or unknown>
- typecheck: <command or unknown>
- lint: <command or unknown>
Handoff directory: `docs/agents/handoffs/`

Files to create or update:
- path 1
- path 2
```

If an existing convention conflicts with the default, recommend the existing convention unless it is clearly broken.

### 3. Ask Only For Ambiguity

Ask the user when:

- Multiple package managers are present.
- Test command names conflict or are missing.
- Existing docs use multiple possible homes.
- The repo already uses a remote issue tracker and local markdown would duplicate active work.
- A file exists and would need non-trivial merge or overwrite.

Ask one focused question at a time.

### 4. Write After Approval

After user approval, create only the agreed files and directories.

Allowed setup outputs:

- `docs/agents/issue-tracker.md`
- `docs/agents/domain.md`
- `docs/agents/test-commands.md`
- `docs/agents/handoff.md`
- `docs/agents/issues/`
- `docs/agents/handoffs/`
- `docs/adr/`
- `CONTEXT.md` if missing and approved

If a target file already exists:

- Read it first.
- Preserve user content.
- Patch only the relevant section.
- Ask before replacing the file.

### 5. File Content Expectations

`issue-tracker.md` should record:

- Local markdown as default, or chosen alternative.
- Issue file location.
- Whether GitHub publishing is optional.
- Any no-publish rule.

`domain.md` should record:

- Domain language file path.
- ADR directory.
- How workflow skills should read them.

`test-commands.md` should record:

- Package manager.
- Primary verification commands.
- When to use each command.
- Unknown commands that still need user confirmation.

`handoff.md` should record:

- Handoff directory.
- Minimum handoff sections.
- Sensitive data redaction rule.

See `references/setup-checklist.md` and `references/local-docs-layout.md` for suggested templates and checklist details.

For natural-language Coordinator Mode operation, see `references/coordinator-operator-mode.md`. Use it when the user asks Codex to run CEWP, split work across workers, or use Manager/Worker/Reviewer orchestration.

## Safety Rules

- Do not run destructive git or filesystem commands.
- Do not delete or rename user files.
- Do not overwrite existing configuration without explicit approval.
- Do not publish issues remotely unless the user explicitly asks.
- Do not assume a remote issue tracker from `git remote`.
- Keep Windows paths with spaces quoted when showing commands.

## Verification

Before declaring setup complete:

- List every file created or updated.
- Confirm `docs/agents/issue-tracker.md` exists or explain why it was not created.
- Confirm `docs/agents/test-commands.md` records verification commands or unknowns.
- Confirm domain and ADR paths are recorded.
- Confirm local issue and handoff directories are recorded.
- State which workflow skills can now use this setup.

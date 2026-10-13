---
name: setup-interface-skills
description: Configure a repository for Interface Skills. This skill sets up the UI specification layer, including folders, agent routing files (CLAUDE.md, AGENTS.md), and a repository-wide INTERFACE_SKILLS.md policy. Use this once per repository or when routing conventions change.
status: stable
---

# Setup Interface Skills

A skill for configuring a repository to support the Interface Skills workflow. It establishes the UI specification folders, repo-wide conventions, and wires agent entry points (CLAUDE.md, AGENTS.md, etc.) so that all AI agents working on the project are aware of the UI source-of-truth.

## When to use this skill

Use this skill:
- When starting Interface Skills in a new repository.
- After running `setup-matt-pocock-skills` (or similar engineering-OS setups) to layer UI-specific specs on top of general engineering docs.
- When you need to repair or update the agent routing layer for the entire project.

## Core principles

1. **Inference first:** Inspect the repository to detect existing UI areas and documentation conventions. Do not invent new folder names if the repo already has a clear home for UI/frontend work.
2. **Safe patching:** Use bounded section markers (`<!-- interface-skills:start -->`) when editing shared agent files like `CLAUDE.md` or `AGENTS.md`. Never overwrite user-written or other tool-owned instructions.
3. **Single source of policy:** Keep detailed Interface Skills rules in a root-level `INTERFACE_SKILLS.md`. Agent files should link to this policy rather than duplicating it.
4. **Composability:** This skill should play well with other setup tools (like Matt Pocock's skills). It adds the UI layer without disrupting the general engineering layer.
5. **Explicit consent for tooling installs:** Do not silently install Playwright, edit package files, or download browser binaries. Offer optional setup and proceed only with explicit user approval.

## Modes

This skill produces one of two outputs depending on context:

| Mode | When to use | Output |
|---|---|---|
| **Report** | Default. Needs human review or read-only session | Setup report + exact edit plan |
| **Patch** | Agent has write access and user has approved applying edits | Applies edits directly using section markers + produces a setup report |

Default to **Report** mode unless the user explicitly says to apply the edits.

## Workflow

### Step 1 — Inventory and Inference

Scan the repository to answer these questions:
- **Where is the primary UI area?** Look for `docs/saas-frontend/`, `apps/web/`, `frontend/`, `web/`, `src/app/`, or `src/pages/`.
- **What agent entry points exist?** Check for `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursor/rules`.
- **Is there an existing engineering setup?** Check for `CONTEXT.md` or `ADR` folders.

### Step 2 — Propose a setup plan

Based on the inventory, propose the following to the user:
1. **The Target Area:** e.g., `docs/saas-frontend/specs/`.
2. **The Policy File:** `INTERFACE_SKILLS.md` at the root.
3. **Agent Patches:** Which files will be updated with routing blocks.
4. **Spec Template:** Where to place the spec package template.

**Wait for user approval before proceeding.**

### Step 3 — Create the policy file (`INTERFACE_SKILLS.md`)

Create a root-level `INTERFACE_SKILLS.md` that defines:
- The location of the UI spec packages.
- The rule: "UI specs are the source of truth for UI behavior."
- The relationship between `CONTEXT.md` (domain language) and UI specs (UI implementation).
- How to name and structure new spec packages.
- Deprecation policy for moved or superseded specs.

### Step 4 — Initialize folders and templates

1. Create the specs directory: `<area>/specs/`.
2. Create or copy the spec package template into `templates/spec-package/` (or similar).

### Step 5 — Patch agent routing files

For every agent entry point found in Step 1, add or update the Interface Skills routing block.

**Marker Pattern:**
```markdown
<!-- interface-skills:start -->
## UI Specification Layer

Before editing UI surfaces (routes, components, copy, accessibility), read the relevant spec package index:
- UI Specs: `<path-to-specs>/`
- Repo Policy: `INTERFACE_SKILLS.md`

Use `ui-orchestrator` to find the right spec for a given route.
<!-- interface-skills:end -->
```

### Step 6 — Update `.interface-skills.yaml`

Ensure the repo-level configuration matches the setup. The file must follow this schema:

```yaml
specs:
  root: <path-to-specs, e.g. docs/saas-frontend/specs>
agent_routing:
  required_entrypoints:
    - CLAUDE.md
    - AGENTS.md
    - GEMINI.md
    - .github/copilot-instructions.md
  optional_entrypoints:
    - .cursor/rules
deprecated_paths: []
```

### Step 7 — Optional browser validation support (Playwright)

If the repository appears to be a JavaScript or TypeScript frontend project, offer (do not force) optional browser validation setup:

1. Detect package manager from lockfiles (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lockb`).
2. Detect whether `@playwright/test` or `playwright` already exists in `package.json`.
3. If missing, ask for permission before any install or config edits.
4. If approved, install with the detected package manager and run browser install.
5. Add `playwright.config.ts` only if missing.
6. Add example scripts only if missing (for example `test:e2e`, `test:e2e:ui`).

If permission is not granted, continue setup without browser tooling and record that live browser validation is optional and not configured.

## Output template

Produce a summary of the setup in the following format:

```markdown
# Interface Skills Setup Report

## 1. Summary
- **Target Area:** `<path-to-specs>`
- **Policy File:** `INTERFACE_SKILLS.md`
- **Status:** Wired

## 2. Folders Created
- [ ] `<path-to-specs>`
- [ ] `templates/spec-package/`

## 3. Agent Files Patched
- [ ] `CLAUDE.md`
- [ ] `AGENTS.md`
- [ ] ...

## 4. Next Steps
1. Run `ui-surface-inventory` if the repository has an existing UI.
2. Run `ui-brief` to start specifying a new feature.
3. Review `INTERFACE_SKILLS.md` for repository-specific naming conventions.
```

## Acceptance criteria for this skill's output

- [ ] Target area inferred from existing repo structure where possible.
- [ ] `INTERFACE_SKILLS.md` created at repo root.
- [ ] All existing agent entry points (CLAUDE, AGENTS, etc.) patched with bounded markers.
- [ ] No existing instructions outside markers were deleted or modified.
- [ ] Final report confirms the routing chain is "Wired".

---
name: agent-init
description: "Analyze a workspace and generate or maintain a modular project documentation setup with a lean, concise agents.md entrypoint. Governs user directives, precautions, and desired persona, while providing selective on-demand reading of detailed guide files and immediate on-the-fly updates when code or rules change. Triggers: 'agent init', 'agents.md 생성', '워크스페이스 분석', 'agent guideline 생성', 'agents.md 모듈화', 'agent-init'. Not for LibrAgent runtime/harness facts (use libragent-harness-reference)."
---

# Agent Init: Modular Guidelines & Persona Governance

This skill analyzes a workspace and establishes or updates a **modular documentation structure** with a **lean `agents.md` entrypoint**.

It manages user directives, strict precautions, and agent persona while keeping `agents.md` lightweight to minimize system prompt context bloat.

For how LibrAgent loads `agents.md` / `SOUL.md`, tool naming, and session isolation, use **libragent-harness-reference** instead of baking that into `agents.md`.

---

## 💡 Core Principles

1. **Lean Entrypoint (`agents.md`)**:
   - `agents.md` serves as a quick-reference index and command cheat sheet (<200 lines).
   - Contains high-level project summary, critical user directives, desired persona, cheat sheet commands, and pointers to detailed guide files.
2. **Modular Guide Architecture (`docs/guidelines/`)**:
   - Detailed specifications are split into dedicated files inside `docs/guidelines/`:
     - `architecture-and-files.md`: System layout, key file map, module boundaries.
     - `coding-standards.md`: Style, type safety, error handling, logging, testing, validation commands.
     - `persona-and-rules.md`: User instructions, desired persona/vibe, strict prohibitions, user preferences.
     - `workflows.md`: Dev workflows, CI/CD pipelines, release procedures.
3. **Selective Reading (Progressive Disclosure)**:
   - Agents read `agents.md` on startup and selectively load relevant `docs/guidelines/*.md` files on demand based on current task scope.
4. **Self-Healing & Immediate Updates**:
   - When an agent discovers changed file paths, refactored modules, new build scripts, or updated user instructions, it **immediately updates** the relevant guide file and syncs `agents.md`.
5. **Governance of User Directives & Persona**:
   - User instructions, prohibitions, and desired persona are preserved across sessions and strictly governed.

---

## 📋 Step-by-Step Execution Workflow

### Step 1: Explore Workspace & Discover Information

Scan the workspace root to collect facts:
- **Build & Language Configs**: Check `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.
- **Directory Structure**: Inspect depth-2 tree (`src/`, `src-tauri/`, `docs/`, `lib/`, `tests/`).
- **Commands**: Extract scripts for dev, build, test, lint, and validation.
- **User Directives & Persona**: Extract existing user instructions, persona files (`SOUL.md`), or explicit chat instructions.

### Step 2: Create Modular Guide Files in `docs/guidelines/`

Ensure `docs/guidelines/` exists and generate the modular files using templates from `references/templates/`:

1. **`docs/guidelines/persona-and-rules.md`**:
   - Fill using `references/templates/persona-and-rules-template.md`.
   - Record desired agent persona/vibe, user directives, strict prohibitions, and language preferences.
2. **`docs/guidelines/architecture-and-files.md`**:
   - Fill using `references/templates/architecture-template.md`.
   - Record system architecture diagram, key directory map, key file locations, and layering rules.
3. **`docs/guidelines/coding-standards.md`**:
   - Fill using `references/templates/coding-standards-template.md`.
   - Record formatting/linting rules, type safety rules, error handling conventions, and validation commands.
4. **`docs/guidelines/workflows.md`**:
   - Record dev workflow steps, CI/CD pipeline triggers, and PR requirements.

### Step 3: Generate or Update Lean `agents.md` Entrypoint

Create or update `agents.md` at the workspace root using `references/templates/agents-md-template.md`:

- Keep `agents.md` concise (<200 lines).
- Fill project overview, high-level persona & user directives, command cheat sheet, and guide file index.
- Ensure all pointer links to `docs/guidelines/*.md` are valid relative paths.

### Step 4: Apply On-Demand Reading & Immediate Update Protocols

When executing future agent tasks in this workspace:

#### 📖 Selective Reading Protocol
- Read `agents.md` for overall routing.
- Read `docs/guidelines/architecture-and-files.md` before refactoring or locating code.
- Read `docs/guidelines/coding-standards.md` before writing/testing code.
- Read `docs/guidelines/persona-and-rules.md` when verifying tone, user preferences, or compliance.

#### 🔄 Immediate Update Protocol (Self-Healing)
- If code structure, file paths, commands, or user directives change during work, **immediately update** the target guide file in `docs/guidelines/` using `workspace__strReplace`.
- Sync `agents.md` if high-level cheat sheets or summaries changed.
- See `references/update-protocol.md` for details.

---

## 🛠️ Resources & Templates
- Entrypoint Template: `references/templates/agents-md-template.md`
- Persona & Rules Template: `references/templates/persona-and-rules-template.md`
- Architecture Template: `references/templates/architecture-template.md`
- Coding Standards Template: `references/templates/coding-standards-template.md`
- Update Protocol Guide: `references/update-protocol.md`
- Merge Policy Guide: `references/merge-policy.md`

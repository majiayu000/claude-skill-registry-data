---
name: ami-discover-ai-agents
description: Discovers high-ROI opportunities for project-specific skills and autonomous subagents, scaffolds native configurations for Antigravity, Claude Code, and Codex.
allowed-tools: Bash, Read, Grep, Glob, Write, Edit
---

# Skill: Discover AI Agents & Skills

When invoked, act as an **AI Agent Architect & Customization Specialist**.

Your purpose is to audit any repository to identify high-ROI opportunities for project-specific declarative **Skills** and autonomous **Subagents**, autodetect the active AI coding assistant and repository configuration layouts, consult with the user, and scaffold the appropriate native files for **Antigravity (AGY)**, **Claude Code**, and/or **OpenAI Codex**.

---

## Architectural Qualification: Skill vs. Agent

Before proposing capabilities, apply the strict architectural distinction:

1. **When to create a Skill (`<repo>-<verb>-<object>`):**
   - The capability represents **procedural recipes, coding standards, checklists, schema validations, or multi-file generation workflows**.
   - It runs inside the **current conversation window**, loaded lazily on demand.
   - It requires continuous direct dialogue with the user.
2. **When to create an Agent (`<repo>-<noun>`):**
   - The workflow requires **strict context isolation** (e.g. adversarial review or blind verification where implementation details must be hidden).
   - High-volume file readings or exploratory scans that would cause **attention decay or token overflow** in the main chat.
   - The task enforces a **strict permission sandbox** (e.g. read-only audit).
   - *Never create agents for simple 1-step tasks that a skill can perform directly.*

---

## Workflow

### 1. Step 0 - Environment Auto-Detection & Repository Inventory
- **Determine Normalized Repository Prefix (`<repo>`):**
  - Read project manifest (`package.json`, `Cargo.toml`, `pyproject.toml`, `.git/config`) or directory basename.
  - Strip package manager scopes (e.g. `@org/package` -> `package`), normalize dots and uppercase letters into clean lowercase kebab-case.
  - *Exception:* If the repository is the suite repository that already prefixes its components with `ami-`, retain `ami-`.
- **Autodetect Active Assistant & Config Layouts:**
  - Inspect working directory and home configurations for active platforms:
    - **Antigravity:** Running in `agy` or presence of `GEMINI.md`, `~/.gemini/config/`, or `.agents/rules/`.
    - **Claude Code:** Running in Claude CLI or presence of `.claude/`, `CLAUDE.md`, or `~/.claude/`.
    - **OpenAI Codex:** Running in Codex or presence of `.codex/` or `~/.codex/`.
  - *Ambiguity Rule:* `.agents/` alone is shared between Antigravity and Codex. Require a secondary platform signal before inferring default. If no clear platform is detected, do not mark any option as Recommended.
  - Scan existing local customizations in `.agents/skills/`, `.agents/agents/`, `.claude/skills/`, `.claude/agents/`, and `.codex/agents/` (as well as global configurations) to prevent proposing duplicate capabilities.

### 2. Phase 1 - Domain & Workflow Analysis
- Scan the repository for high-friction domain workflows:
  - Complex recurring domain logic (e.g., database seeds, payment reconciliations, API payload validators).
  - Repetitive multi-step tasks that require domain context knowledge.
  - Verification procedures that would benefit from isolated, black-box subagent audits.
- Categorize each candidate as a **Skill** or an **Agent** according to the qualification criteria.
- Assign proposed names following the mandatory naming convention:
  - Skills: `<repo>-<verb>-<object>` (e.g. `billing-reconcile-invoices`, `auth-validate-tokens`).
  - Agents: `<repo>-<noun>` (e.g. `billing-auditor`, `auth-verifier`).

### 3. Phase 2 - Prioritized Proposal & Interactive Consultation
- Present the proposals in a clear Markdown summary table directly in the chat:
  - **Type:** `Skill` vs `Agent`
  - **Proposed Name:** `<repo>-<verb>-<object>` or `<repo>-<noun>`
  - **Impact / ROI:** `[HIGH]`, `[MEDIUM]`, `[LOW]`
  - **Permission Level:** `Read-Only` vs `Read/Write`
  - **Architectural Justification:** Why this belongs as a Skill or an Agent
- **CONFIRMATION 1 - Interactive Consultation Gate:**
  - STOP and prompt the user with:
    1. Which proposed skills/agents they would like to scaffold.
    2. Confirmation of the proposed names (allow the user to customize or approve them).
    3. Target platform selection:
       - If a platform was unambiguously detected: `(Recommended) <Autodetected Platform>`
       - Antigravity (AGY)
       - Claude Code
       - OpenAI Codex
       - All 3 (Complete Multi-Ecosystem Parity)
       - If no platform was detected, present unranked options without pre-assumption.
  - Await explicit user response before proceeding.

### 4. Phase 3 - Multi-Platform Native Scaffolding & Pre-Write Gate
- **CONFIRMATION 2 - File Write & Overwrite Gate:**
  - STOP and list every exact destination path to be created.
  - If any target file already exists on disk, explicitly warn the user and list the file that would be overwritten.
  - Never overwrite existing files without explicit user approval.

#### A. Antigravity (AGY) Specifications
- **Skills Directory:** `.agents/skills/<name>/SKILL.md`
  - When Antigravity is targeted alone or alongside Claude Code, declare native tool tokens under `tools:`.
  - Consult `references/antigravity-tools.md` for the exact platform-native tool identifiers. Never use generic abstract names like `Read` or `Write`.
- **Agents Directory:** `.agents/agents/<name>.md` (or `.agents/agents/<name>/agent.md`)
  - Frontmatter declares `name`, `description`, `tools:` (YAML list or comma-separated string of native identifiers from `references/antigravity-tools.md`), and optional `model: inherit` or specific model alias.

#### B. Claude Code Specifications
- **Skills Directory:** `.claude/skills/<name>/SKILL.md`
  - Frontmatter declares `name`, `description`, and `allowed-tools:` using PascalCase capabilities (`Bash, Read, Grep, Glob, Write, Edit`).
- **Agents Directory:** `.claude/agents/<name>.md`
  - Frontmatter declares `name`, `description`, `tools:` (or `allowed-tools:`), optional `disallowedTools:`, and optional `model: inherit`.

#### C. OpenAI Codex Specifications
- **Skills Directory:** `.agents/skills/<name>/SKILL.md`
  - Frontmatter uses clean abstract capabilities (`allowed-tools: Read, Grep, Glob, Write, Edit, Bash`).
- **Agents Directory:** `.codex/agents/<name>.toml`
  - TOML structure using clean LF line endings and multi-line strings (`"""`):
    ```toml
    name = "<name>"
    description = "<Description>"
    developer_instructions = """
    <Full instructions escaped without triple double-quotes>
    """
    sandbox_mode = "read-only" # Include only if read-only agent
    ```

#### D. Shared Workspace Coexistence Rule (AGY + Codex or All 3)
- When both Antigravity and Codex are selected, write a single canonical `.agents/skills/<name>/SKILL.md` with frontmatter containing strictly `name` and `description` (plus instruction body), omitting conflicting platform-specific tool keys to ensure universal compatibility.

*General Quality Invariants for Generated Files:*
- Zero emojis in prompts, instructions, and frontmatter.
- Frontmatter descriptions must be under 50 words.
- All code and markdown instructions written in English.

### 5. Phase 4 - Verification & Operational Summary
- Verify that created files exist on disk and have valid YAML or TOML syntax.
- If TOML files were generated, verify they contain LF line endings.
- Present a final operational guide showing:
  - Paths of all created skills and agents.
  - Exact slash commands or prompt triggers to activate each newly created capability.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).

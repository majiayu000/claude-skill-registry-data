---
name: absorb-local-learnings
description: Internal repository workflow to inspect machine-global rules and agent learnings (~/.gemini, ~/.claude) and safely absorb portable engineering invariants into repository rules, skills, or agents while strictly excluding private paths, employer contexts, and personal design systems.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Skill: Absorb Local Learnings (Internal Maintenance Guide)

This internal repository skill governs the extraction, classification, sanitization, and absorption of operational heuristics, AI runtime lessons, and coding guidelines learned across local environments (`~/.gemini/config/`, `~/.claude/`) into the versioned `amiga-ia` repository.

---

## 1. Trigger Conditions

Run this workflow when:
- The user asks to reconcile or sync local AI rules/learnings with the repository.
- A debugging session in a sibling repository produced a new generalizable engineering rule or anti-hallucination guardrail stored in `~/.gemini/config/rules/` or global `AGENTS.md` / `CLAUDE.md`.
- Preparing a minor or major release where local operational invariants should be codified for the entire distributed community.

---

## 2. Phase 0: Discovery & Diff Inventory

Inspect all global local configuration directories:
1. **Google Antigravity:**
   - `~/.gemini/config/rules/*.md`
   - `~/.gemini/config/AGENTS.md`
2. **Anthropic Claude Code:**
   - `~/.claude/CLAUDE.md`
   - `~/.claude/rules/*.md` (if present)
3. **OpenAI Codex:**
   - `~/.codex/` and `~/.agents/skills/`

Compare file timestamps and structural contents against existing repository assets in `rules/`, `skills/`, `agents/`, and repo-level `AGENTS.md`.

---

## 3. Phase 1: Privacy, Employer & Personal Isolation Gate (STRICT FILTER)

Every discovered local rule, instruction, or guideline must pass through the **Sanitization and Portability Filter** before absorption.

### Forbidden Categories (NEVER ABSORB / LEAVE STRICTLY LOCAL)
1. **Local Machine & Filesystem Specifics:**
   - Machine-specific absolute paths (e.g., user profile paths, home directories, local application data directories), local user-level binary installations, or environment-specific toolchain path references.
2. **Workplace & Employer Specifics:**
   - Corporate repositories, proprietary client workflows, employer-specific accounts/tokens, internal company databases, or private organizational context files.
3. **Personal Aesthetics & Bespoke Design Systems:**
   - Personal brand design systems, signature portfolio aesthetics, author-specific color palettes, custom line art or watermark directives, or personal homepage references.

### Approved Portable Value (ELIGIBLE FOR ABSORPTION)
1. **Autonomous AI Orchestration & Guardrails:**
   - Subagent anti-hallucination protocols, mandatory live verification gates (releases, git pushes, assets).
   - Execution patterns addressing platform sandboxes (e.g., Antigravity Pattern A vs. Pattern B).
   - Anti-bottleneck parallelization rules and investigation bifurcation.
2. **Cross-Platform Engineering Standards:**
   - Compilation and version bump ordering in release pipelines.
   - Native toolchain cache pruning (`cargo clean`, `dotnet clean`, `./gradlew clean`) and artifact hygiene.
   - Desktop application stability invariants (WinUI 3 / WPF / MAUI exception handling, XAML security, UI thread dispatching).
3. **Universal Documentation & Testing Hygiene:**
   - Zero country flags policy.
   - Zero static test counts (atemporal quality gates).
   - Path privacy rules and clean badge specifications.

---

## 4. Phase 2: Destination Triage Matrix

Classify each approved item into the appropriate repository layer:

| Target Destination | Purpose | Standards & Conventions |
| :--- | :--- | :--- |
| **`rules/<name>.md`** | Global declarative rules and operational guardrails for Antigravity & Claude. | Written in clear domain language (English for technical rules, or Spanish for shared documentation standards). Must include frontmatter `trigger: always_on` where applicable. |
| **`skills/ami-<name>/`** | Reusable, multi-step interactive workflows or developer procedures. | Must follow `ami-<verb>-<object>` action naming, YAML frontmatter with canonical `allowed-tools`, under 250 lines, procedural clarity, no emojis. |
| **`agents/ami-<name>.md`** | Autonomous persona definitions requiring permission isolation or context offloading. | Must follow `ami-<role>` naming, describe responsibilities and tool authorizations without duplicating skill step-by-step logic. |
| **`AGENTS.md` (Repo Root)** | Internal development rules governing the `amiga-ia` codebase itself. | Numbered rules (e.g., Rule 24: Anti-Bottleneck). English only. |

---

## 5. Phase 3: Interactive Confirmation Gate

**CONFIRMATION 1 - Triage Review:**
Before creating or modifying any file, construct and present a classified summary table to the user:
- **Files to Absorb:** Target path, source path, rationale, and target architectural layer.
- **Files Excluded:** Specific reason for exclusion (e.g., private paths, employer context, personal design system).

**STOP and await explicit user approval.** Never apply changes speculatively.

---

## 6. Phase 4: Execution & Verification Gate

Once approved:
1. Apply modifications using `replace_file_content` or `write_to_file`.
2. Ensure all newly added public skills or agents adhere strictly to AMI conventions:
   - Zero emojis in prompts and instructions.
   - English source code, docstrings, and commits.
   - Symmetric bilingual documentation where required.
3. Execute the repository verification gates:
   ```powershell
   node bin/setup.js --doctor
   npm test
   ```
4. Verify that `git status` reflects clean, isolated modifications strictly conforming to repository architectural layering.

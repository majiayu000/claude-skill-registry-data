---
name: saas-setup-stack
description: "Configure engine and version. Pins it in CLAUDE.md; WebSearch fills reference docs when the version is beyond LLM training data."
argument-hint: "[engine] | [engine version] | refresh | upgrade [old-version] [new-version] | no args for guided selection"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, WebSearch, WebFetch, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/saas-setup-stack/../../hooks/yaml-helper.sh" resolve_config *), Bash(nextjs --version), Bash(node --version), Bash(npm --version), Bash(command -v nextjs), Bash(uname -s), Bash(bash .claude/scripts/project-coherence.sh*)
model: sonnet
---

# Engine Setup

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

When this skill is invoked:

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,workflow`

**Tier awareness.** The `workflow` tier resolved above governs which design
artifact this skill expects and the finish path it recommends in §12:
- **`minimal`** — the design artifact is the one-page `design/product-brief.md`
  (no PRDs, systems decomposition, or per-system design at this tier).
  `/saas-setup-stack` runs *first* in the minimal path, so a missing brief here is
  normal, not a gap. The finish path is the 4-step floor.
- **`standard` / `full`** — the design artifact is `design/prd/product-concept.md`
  and the finish path is the full pipeline.

If the block did not render (shell preprocessing disabled), assume `minimal` (the default).

## 1. Parse Arguments

Four modes:

- **Full spec**: `/saas-setup-stack nextjs 4.7` — engine and version provided
- **Engine only**: `/saas-setup-stack fastapi` — engine provided, version will be looked up
- **No args**: `/saas-setup-stack` — fully guided mode (engine recommendation + version)
- **Refresh**: `/saas-setup-stack refresh` — update reference docs (see Section 10)
- **Upgrade**: `/saas-setup-stack upgrade [old-version] [new-version]` — migrate to a new engine version (see Section 11)

---

## 2. Guided Mode (No Arguments)

**Read `references/2-guided-mode.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 3. Look Up Current Version

**Read `references/3-version.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 4. Update CLAUDE.md Technology Stack

**Read `references/4-claude-md-stack.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 5. Populate Technical Preferences

**Read `references/5-technical-preferences.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 5.5 Populate `project.yaml` (Primary Config Store)

**Read `references/5.5-project-yaml.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 6. Determine Knowledge Gap

**Read `references/6-knowledge-gap.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 7. Populate Engine Reference Docs

**Read `references/7-reference-docs.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 7.5 Scaffold the Engine Project

**Read `references/7.5-scaffold.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 8. Verify the CLAUDE.md Import

**Read `references/8-verify.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 9. Update Agent Instructions

Ask: "May I add a Version Awareness section to the stack specialist agent files?" before making any edits.

For the chosen engine's specialist agents, verify they have a
"Version Awareness" section. If not, add one following the pattern in
the existing Next.js specialist agents.

The section should instruct the agent to:
1. Read `docs/engine-reference/<engine>/VERSION.md`
2. Check deprecated APIs before suggesting code
3. Check breaking changes for relevant version transitions
4. Use WebSearch to verify uncertain APIs

---

## 10. Refresh Subcommand

If invoked as `/saas-setup-stack refresh`:

1. Read the existing `docs/engine-reference/<engine>/VERSION.md` to get
   the current engine and version
2. Use WebSearch to check for:
   - New engine releases since last verification
   - Updated migration guides
   - Newly deprecated APIs
3. Update all reference docs with new findings
4. Update "Last verified" dates on all modified files
5. Report what changed

---

## 11. Upgrade Subcommand

**Read `references/11-upgrade.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 12. Output Summary

**Read `references/12-output-summary.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Guardrails

- NEVER guess an engine version — always verify via WebSearch or user confirmation
- `project.yaml` is the primary config store (v1.1). Always dual-write engine
  config to BOTH `project.yaml` (primary) and `technical-preferences.md` (legacy
  mirror). If the two ever diverge, `project.yaml` is authoritative.
- NEVER overwrite existing reference docs without asking — append or update
- If reference docs already exist for a different engine, ask before replacing
- Always show the user what you're about to change before making CLAUDE.md edits
- If WebSearch returns ambiguous results, show the user and let them decide
- When the user chose **TypeScript**: copy the TypeScript CLAUDE.md template from **A1** in `references/nextjs-language-config.md` exactly. NEVER add "C++ via GDExtension" to the Language field. TypeScript projects may use GDExtension, but it is not a primary project language. The `prisma-drizzle-specialist` in the routing table is available for when native extensions are needed — it does not make C++ a project language.

---

## Appendix A — Next.js Language Configuration

Moved out of this file so it costs nothing on non-Next.js runs.

**When the chosen engine is Next.js, read**
`references/nextjs-language-config.md`
and use the subsection for the chosen language:

- **A1** — CLAUDE.md Technology Stack templates (TypeScript / C# / Both)
- **A2** — naming conventions
- **A3** — stack specialist routing and file-extension tables

**Load discipline.** On any engine other than Next.js, **never load it** — nothing in Sections 4, 5 or 5.5 needs it, and reading it anyway spends the tokens the split exists to save. On Next.js, read it once when you first reach Section 4 and keep using it for Sections 5 and 5.5; do not re-read it at each reference.

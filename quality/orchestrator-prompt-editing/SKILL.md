---
name: orchestrator-prompt-editing
description: "[STALE — DO NOT USE] Skill is disabled pending refresh. It targets the production prompt path/structure, but redesign mode swapped to a different file with a different structure on 2026-04-27. Edit prompts manually until this skill is updated."
user-invocable: false
disabled: true
---

# [STALE — DO NOT USE] Editing the Orchestrator System Prompt

> **This skill is disabled as of 2026-04-29.** Three known staleness issues:
>
> 1. **Wrong file targeted.** Skill assumes `.github/workflows/orchestrator-prompt.xml`, but redesign mode (installed 2026-04-27, commit `06c799cd`) swapped the active prompt to `.github/workflows/orchestrator-redesign-prompt.xml` via `.github/workflows/orchestrator.yml` line 51. Both files exist; only one is active. The skill predates this swap.
> 2. **Wrong XML structure.** Skill describes the production prompt's 8 sections (`<identity>`, `<directives>`, `<definitions>`, `<environment>`, three `<phase>` sections, `<practices>`). The redesign prompt has a completely different structure: `<critical-context-read-first>`, `<mission>`, `<core-design-principle>`, `<authority>`, `<phases>`, `<checkpoints>`, `<abort-criteria>`, `<initial-directive>`, `<persistence>`, `<iteration-until-approval>`, etc.
> 3. **"When to edit" framing is production-only.** Skill triggers are all behavioral-correction signals (recurring findings, adoption gaps, data-filtering). Redesign-mode edits are usually design-refinement (phase ordering, checkpoint tweaks, scope clarifications) — different shape entirely.
>
> **To make current**: detect which prompt is active (read `.github/workflows/orchestrator.yml` and find the `cat` line); document both prompt structures; add a redesign-mode editing subsection. Until then, edit prompts manually with surgical edits and validate XML afterward.

---

# Editing the Orchestrator System Prompt

The orchestrator's system prompt lives at `.github/workflows/orchestrator-prompt.xml`. This XML file is loaded as the orchestrator's briefing every cycle. It contains ALL orchestrator instructions — identity, directives, definitions, environment, startup steps, close-out steps, and standing practices. Changes here directly affect orchestrator behavior.

## Key facts

- **Location**: `.github/workflows/orchestrator-prompt.xml` — a single XML file that replaces the previous markdown prompt + STARTUP_CHECKLIST.md + COMPLETION_CHECKLIST.md
- **Format**: XML with 8 top-level sections: `<identity>`, `<directives>`, `<definitions>`, `<environment>`, `<phase id="startup">`, `<phase id="work">`, `<phase id="close-out">`, `<practices>`
- **The workflow YAML** (`.github/workflows/orchestrator.yml`) loads this file via `cat` and passes it as the system prompt
- **Human-only change**: The orchestrator cannot modify this file itself (it's under `.github/workflows/`). It must create a `question-for-eva` issue for proposed changes.

## When to edit

Edit the prompt when journal entries or review findings reveal **recurring behavioral patterns** that tools haven't fixed. Indicators:

- The same finding category appears across 3+ consecutive review cycles
- The orchestrator acknowledges a pattern in its journal but doesn't change behavior
- Tools exist but aren't being used (adoption gaps)
- The orchestrator interprets or filters data instead of reporting canonical values

## How to edit

1. **Read the journal entries** that document the behavioral issue
2. **Read the current prompt** at `.github/workflows/orchestrator-prompt.xml`
3. **Edit the XML file** — add directives/constraints in the appropriate section
4. **Validate**: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('.github/workflows/orchestrator-prompt.xml')"`
5. **Commit** — Eva will need to merge via PR (orchestrator has no Workflows permission)

## XML structure

| Section | Purpose | When to edit |
|---------|---------|--------------|
| `<directives>` | Non-negotiable behavioral constraints | Recurring behavioral failures |
| `<definitions>` | Enumerations, thresholds, labels, tools | New thresholds, finding categories, tools |
| `<environment>` | Runtime, permissions, communication | Infrastructure changes |
| `<phase id="startup">` | Steps S0-S9 | Startup procedure changes |
| `<phase id="close-out">` | Steps C1-C8 | Close-out procedure changes |
| `<practices>` | Standing reference (worklog, journal, tools) | Practice updates |

**Behavioral directives** (`<directives>` section) is the right place for constraints addressing recurring failures. Each directive should have `id`, `severity="mandatory"`, `<rule>`, and optionally `<violation-signal>`.

## What NOT to do

- **Do not let the orchestrator self-modify its prompt** — requires human oversight
- **Do not duplicate content** — each rule should be defined once. Use `ref-directive`, `ref-threshold`, and `cross-ref` attributes for references
- **Do not break XML validity** — always validate after editing

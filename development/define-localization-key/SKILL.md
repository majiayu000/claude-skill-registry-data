---
name: define-localization-key
description: "Use when extracting dialogue/UI text into structured localization keys (module.context.identifier pattern) to prevent hard-coded strings."
---

# define-localization-key

## 1. Template Binding

- **Output**: `{TARGET_FOLDER}/docs/localization_keys.md`
- **Logic**: Transform raw text sources into structured, language-independent key table; requires dialogue scripts and UI content.

## 2. Core Pattern: Extract → Keyify → Validate

Strict data extraction and transformation pipeline.

| Phase | Focus | Action |
| :--- | :--- | :--- |
| **Extraction** | Collect visible text from dialogues, UI, narration, errors | Raw string inventory |
| **Key Generation** | Create keys using `module.context.identifier` pattern (e.g., `ui.main_menu.play`) | Structured key table |
| **Validation** | Check uniqueness, write categorized tables | Finalized `localization_keys.md` |

**CRITICAL: Interview the user BEFORE generating any spec via `question` tool.**

### Mandatory Interview Steps (SEQUENTIAL — ONE AT A TIME)

**RULE: Ask ONE question group per turn. Wait for answer before proceeding.**

1. Ask about module/context structure via `question` → **STOP**
2. Ask about key naming convention confirmation via `question` → **STOP**
3. Present key sample for verification via `question` → **STOP**
4. Generate `localization_keys.md`

## 3. When to Use

- **Scope**: Extracting dialogue/UI text into structured keys, preparing for multi-language support, or building i18n key tables from raw content sources. Use `bootstrap-game-project` for refining existing `localization_keys.md`; use `builder/implement-localization` for implementing the i18n system itself.

## 4. Interaction Protocol

Every step MUST use the `question` tool. Present concrete key samples, not abstract descriptions. One question per turn.

**Intercepts:**
- **[Context Gap Intercept]**: Text without module/context → "I've noted the text. To ensure correct key naming (module.context.identifier), please specify the module and context (e.g., UI/Main Menu)."

## 5. Quality Gates

- **Semantic Keys**: All keys use semantic naming only, independent of language.
- **Standard Naming**: Consistent `module.context.id` pattern throughout unless explicitly overridden.
- **Complete Key Coverage**: All visible text captured as localization key references with no raw strings remaining in output spec.
- **One Question Per Turn**: Single question at a time — wait for user answer before proceeding.

## 6. Execution Command

Command: `/define-localization-key`

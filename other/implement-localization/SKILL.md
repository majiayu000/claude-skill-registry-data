---
name: implement-localization
description: "Use when generating an i18n system with typed keys, structured translation maps, multi-tier fallback chain (Requested → English → Key Name), and runtime language switching."
---

# implement-localization

## 1. Overview

Generates a complete internationalization (i18n) infrastructure, including typed key constants, structured translation maps, and a reliable multi-tier fallback mechanism to prevent UI breakage during runtime transitions across multiple languages.

## 2. When to Use

- **Scenarios**: Initial setup of i18n infrastructure during the engineering phase, implementing runtime language switching for existing game projects.
- **Natural Language Triggers**: `implement localization`, `i18n setup`, `multi-language support`, `translation system implementation`.

## 3. Core Pattern

1. **Platform & Language Detection**: Scan project configuration files to identify target platform/language constraints and resolve technical ambiguities.
2. **Key & Constant Generation**: Create typed localization key constants using dotted string identifiers (e.g., `ui.main_menu.play`) and define supported locale code constants.
3. **Translation Map Implementation**: Build a structured translation dictionary that includes mandatory English entries for every defined key to ensure fallback capability.
4. **Lookup & Switch Logic**: Implement the multi-tier fallback chain (Requested Language → English → Key Name) and runtime language switching utilities.

## 4. Interaction Protocol

* **[Fallback Intercept]**: *"I've noticed that [Key Name] lacks a mandatory English fallback translation. This could result in empty UI elements for users. Should we add the English entry now?"*
* **[Hardcoded String Intercept]**: *"Please provide the localization key (e.g., `ui.button_ok`) rather than the raw string to ensure proper internationalization support."*

**Guiding Principle**: Prioritize the reliability of the fallback chain. Every key MUST have a primary fallback entry (typically English) to prevent missing translations from resulting in broken UI or application crashes during runtime.

## 5. Red Flags - STOP and Start Over

* **Complete Fallback Coverage**: Every key has at least one valid fallback entry (English) to prevent empty UI elements
* **Typed Key Usage**: All text access uses typed localization constants instead of raw strings
* **Unique Key Identifiers**: Each semantic meaning maps to one distinct key across all locales

## 6. Final Integrity Audit

- [ ] All generated keys are mapped to at least one valid fallback entry (English).
- [ ] Zero hardcoded strings remain; all text access uses typed constants.
- [ ] Language switching mechanism correctly triggers updates for registered subscribers.
- [ ] Lookup logic follows the established hierarchy: Requested → Fallback → Key Name.

## 7. Execution Command

`/implement-localization`

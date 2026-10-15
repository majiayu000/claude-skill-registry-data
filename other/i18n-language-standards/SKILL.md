---
name: i18n-language-standards
description: >
  Enforce ASD-STE100 (English) and clear Korean UI language standards across LibrAgent.
  Audits UI text, Settings descriptions, and i18n locales for prohibited engineering jargon,
  internal code identifiers (browser="userChrome", awaitAgent, pollProcess, createSession),
  passive translations, and ensures terminology parity across all 8 supported languages.
  Triggers on: "언어 규약", "language standards", "i18n standards", "ASD-STE100", "i18n audit",
  "i18n 검증", "언어 규약 검사", "layman-friendly UI text", "i18n-language-standards".
---

# i18n Language Standards & Enforcement

This skill defines, audits, and enforces user-facing language standards across LibrAgent. It ensures that UI labels, settings descriptions, tool documentation, and i18n locales adhere to **ASD-STE100** for English and **Clear Korean UI Standards** for Korean, while maintaining rigorous parity across all 8 supported languages (`en`, `ko`, `ja`, `zh`, `de`, `fr`, `es`, `pt`).

## 1. Core Principles

1. **No Internal Code Identifiers in UI**:
   - Never expose code syntax or internal function names in user-facing text.
   - Prohibited examples: `browser="userChrome"`, `browser="sidecar"`, `createSession`, `awaitAgent`, `pollProcess`.
2. **Eliminate Engineering Jargon**:
   - Translate compiler, runtime, or ML-serving concepts into clear end-user benefits.
   - Replace `prefill`, `clean resample`, `circuit breaker`, `serving-engine`, `old turns`, `diffs` with intuitive layperson equivalents.
3. **ASD-STE100 Compliance (English)**:
   - Sentences under 20 words where possible.
   - Active voice, clear imperatives, one word for one meaning.
4. **Clear Korean Standards (한국어)**:
   - 번역투 및 피동형(`~되어지다`) 배제, 능동형 단문 구성.
   - 불필요한 한자어나 외래어(`거버넌스`) 대신 직관적인 표준 용어 사용.
5. **Multilingual Parity (8 Locales)**:
   - All settings keys and UI strings must maintain semantic and structural parity across `en`, `ko`, `ja`, `zh`, `de`, `fr`, `es`, and `pt`.

## 2. Automated Validation Workflow

To check compliance across all locale files and Settings components, execute the bundled validator:

```bash
node .agents/skills/i18n-language-standards/scripts/validate_i18n_standards.cjs
```

The script verifies:
- Absence of forbidden internal identifiers in `src/locales/` and `src/features/settings/`.
- Absence of flagged engineering jargon.
- JSON syntax validity and key parity against `en/common.json`.

## 3. Reference Guides

Consult the reference documents for specific translation rules:

- [ASD-STE100 English Guidelines](references/ste100-guide.md): Active voice, controlled vocabulary, brevity rules.
- [Clear Korean UI Guide](references/korean-ui-guide.md): 한국어 UI 표준 어휘, 번역투 제거 및 능동형 문체 규약.
- [Multilingual Translation Guide](references/multilingual-guide.md): Rules for `ja`, `zh`, `de`, `fr`, `es`, and `pt`.

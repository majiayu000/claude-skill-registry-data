---
name: saas-localize
description: "Localization pipeline — find hardcoded strings, extract string tables, cultural review, transactional email & messaging, RTL, enforce string freeze."
argument-hint: "[scan|extract|validate|status|brief|cultural-review|email-messaging|rtl-check|freeze|qa]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/saas-localize/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,automation`



# Localization Pipeline

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

Localization is not just translation — it is the full process of making a SaaS application
feel native in every language and region. Poor localization breaks immersion,
confuses users, and blocks platform certification. This skill covers the
complete pipeline from string extraction through cultural review, transactional email & notification templates,
RTL layout testing, and localization QA sign-off.

**Modes:**
- `scan` — Find hardcoded strings and localization anti-patterns (read-only)
- `extract` — Extract strings and generate translation-ready tables
- `validate` — Check translations for completeness, placeholders, and length
- `status` — Coverage matrix across all locales
- `brief` — Generate translator context briefing document for an external team
- `cultural-review` — Flag culturally sensitive content, symbols, colours, idioms
- `email-messaging` — Manage transactional email and notification messaging localization: templates, context notes, integration
- `rtl-check` — Validate RTL language layout, mirroring, and font support
- `freeze` — Enforce string freeze; lock source strings before translation begins
- `qa` — Run the full localization QA cycle before release

If no subcommand is provided, output usage and stop. Verdict: **FAIL** — missing required subcommand.

---

Every `AskUserQuestion` call follows `.claude/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

## Phase 2A: Scan Mode

Search the **code root** (resolve per `.claude/docs/code-root-resolution.md`) for hardcoded user-facing strings. **If the code root is unresolved, report `NOT ASSESSED — code root unresolved` rather than zero hits.** Zero hits from an unresolved root reads as "nothing to localize", which is the failure this guards:

- String literals in UI code not wrapped in a localization function (`tr()`, `Tr()`, `NSLocalizedString`, `GetText`, etc.)
- Concatenated strings that should be parameterized
- Strings with positional placeholders (`%s`, `%d`) instead of named ones (`{userName}`)
- Format strings that mix locale-sensitive data (numbers, dates, currencies) without locale-aware formatting

Search for localization anti-patterns:

- Date/time formatting not using locale-aware functions
- Number formatting without locale awareness (`1,000` vs `1.000`)
- Text embedded in images or textures (flag asset files in `assets/`)
- Strings that assume left-to-right text direction (positional layout, string assembly order)
- Gender/plurality assumptions baked into string logic (must use plural forms or gender tokens)
- Hardcoded punctuation (e.g. `"You won!"` — exclamation styles vary by locale)

Report all findings with file paths and line numbers. This mode is read-only — no files are written.

---

## Phase 2B: Extract Mode

- Scan all source files for localized string references
- Compare against the existing string table in `assets/data/strings/`
- Generate new entries for strings not yet keyed
- Suggest key names following the convention: `[category].[subcategory].[description]`
  - Example: `ui.app_shell.nav_dashboard`, `auth.login.welcome_title`, `billing.checkout.cta_button`
- Each new entry must include a `context` field — a translator comment explaining:
  - Where it appears (which screen, which view)
  - Maximum character length
  - Any placeholder meaning (`{userName}` = the user's chosen display name)
  - Gender/plurality context if applicable

Output a diff of new strings to add to the string table.

Present the diff to the user. Ask: "May I write these new entries to `assets/data/strings/strings-en.json`?"

If yes, write only the diff (new entries), not a full replacement. Verdict: **COMPLETE** — strings extracted and written.

---

## Phase 2C: Validate Mode

Read all string table files in `assets/data/strings/`. For each locale, check:

- **Completeness** — key exists in source (en) but no translation for this locale
- **Placeholder mismatches** — source has `{name}` but translation omits it or adds extras
- **String length violations** — translation exceeds the character limit recorded in the source `context` field
- **Plural form count** — locale requires N plural forms; translation provides fewer
- **Orphaned keys** — translation exists but nothing in the code root references the key
- **Stale translations** — source string changed after translation was written (flag for re-translation)
- **Encoding** — non-ASCII characters present and font atlas supports them (flag if uncertain)

Report validation results grouped by locale and severity. This mode is read-only — no files are written.

---

## Phase 2D: Status Mode

- Count total localizable strings in the source table
- Per locale: count translated, untranslated, stale (source changed since translation)
- Generate a coverage matrix:

```markdown
## Localization Status
Generated: [Date]
String freeze: [Active / Not yet called / Lifted]

| Locale | Total | Translated | Missing | Stale | Coverage |
|--------|-------|-----------|---------|-------|----------|
| en (source) | [N] | [N] | [N] | [N] | [N]% |
| [locale] | [N] | [N] | [N] | [N] | [X]% |

> **Every cell above is a count you must take from the string table — including
> the source row.** Do not pre-fill the source locale as `100%`: that asserts a
> result before counting, and on a project with no `assets/data/strings/` it
> produces a coverage report for a table that does not exist. If the string table
> is absent, the whole status output is
> **`NOT ASSESSED — no string table found`**, not a matrix of zeros with a
> confident source row.

### Issues
- [N] hardcoded strings found in source code (run /saas-localize scan)
- [N] strings exceeding character limits
- [N] placeholder mismatches
- [N] orphaned keys
- [N] strings added after freeze was called (freeze violations)
```

This mode is read-only — no files are written.

---

## Phase 2E: Brief Mode

Generate a translator context briefing document. This document is sent to the
external translation team or localisation vendor alongside the string table export.

Read:
- `design/prd/` — extract product domain, tone, target audience. Read the
  PRDs by section: check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise find the headings you need with the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Grep tool (pattern `^#`, content mode) and Read those ranges with offset and limit.
- `assets/data/strings/strings-en.json` — the source string table
- Any existing brand guidelines or messaging specs in `docs/brand/` or `design/`

Generate `production/localization/translator-brief-[locale]-[date].md`:

```markdown
# Translator Brief — [Product Name] — [Locale]

## Product Overview
[2-3 paragraph summary of the SaaS product, value proposition, tone, and audience]

## Tone and Voice
- **Overall tone**: [e.g., "Darkly comic, not slapstick — think Terry Pratchett, not Looney Tunes"]
- **User address**: [e.g., "Second person, informal. Never formal 'vous' — always 'tu' for French"]
- **Profanity policy**: [e.g., "Mild — PG-13 equivalent. Match intensity to source, do not soften or escalate"]
- **Humour**: [e.g., "Wordplay exists — if a pun cannot translate, invent an equivalent local joke; do not translate literally"]

## Character Glossary
| Name | Role | Personality | Notes |
|------|------|-------------|-------|
| [Name] | [Role] | [Personality] | [Do not translate / transliterate as X] |

## World Glossary
| Term | Meaning | Notes |
|------|---------|-------|
| [Term] | [What it means] | [Keep in English / translate as X] |

## Do Not Translate List
The following must appear verbatim in all locales:
- [Product name]
- [UI terms that match in-engine labels]
- [Brand or trademark names]

## Placeholder Reference
| Placeholder | What it represents | Example |
|-------------|-------------------|---------|
| `{userName}` | User's chosen display name | "Alex" |
| `{count}` | Integer quantity | "3" |

## Character Limits
Tight UI fields with hard limits are marked in the string table `context` field.
Where no limit is stated, target ±30% of the English length as a guideline.

## Contact
Direct questions to: [placeholder for user/team contact]
Delivery format: JSON, same schema as strings-en.json
```

Ask: "May I write this translator brief to `production/localization/translator-brief-[locale]-[date].md`?"

---

## Phase 2F: Cultural Review Mode

Spawn `localization-lead` via `Agent`. Ask them to audit the following for cultural sensitivity across the target locales (read from `assets/data/strings/` and `assets/`):

### Content Areas to Review

**Symbols and gestures**
- Thumbs up, OK hand, peace sign — meanings vary by region
- Religious or spiritual symbols in art, UI, or audio
- National flags, map representations, disputed territories

**Colours**
- White (mourning in some Asian cultures), green (political associations in some regions), red (luck vs danger)
- Alert/warning colours that conflict with cultural associations

**Numbers**
- 4 (death in Japanese/Chinese), 13, 666 — flag use in UI (room numbers, item counts, prices)

**Humour and idioms**
- Idioms that translate as offensive in other locales
- Toilet/bodily humour that is inappropriate in some markets (notably Japan, Germany, Middle East)
- Dark humour around topics that are culturally sensitive in specific regions

**Regulatory compliance & data privacy**
- Content that requires region-specific legal disclosures (e.g. GDPR in EU, LGPD in BR, PIPL in CN)
- Terms of service, cookie consent banners, or VAT/tax invoicing discrepancies by locale

**Names and representations**
- Product terminology, plan names, or feature titles that carry unintended negative meaning in target locales
- Stereotyped representation of nationalities, religions, or ethnic groups

Present findings as a table:

| Finding | Locale(s) Affected | Severity | Recommended Action |
|---------|--------------------|----------|--------------------|
| [Description] | [Locale] | [BLOCKING / ADVISORY / NOTE] | [Change / Flag for review / Accept] |

BLOCKING = must fix before shipping that locale. ADVISORY = recommend change. NOTE = informational only.

Ask: "May I write this cultural review report to `production/localization/cultural-review-[date].md`?"

---

## Phase 2G: Email & Messaging Pipeline Mode

Manage transactional email and notification messaging localization. Determine the sub-task from the argument:

- `email-messaging scan` — identify all email templates and notification messages requiring localization
- `email-messaging draft` — generate localized email template specs with layout context
- `email-messaging validate` — check that all localized email templates exist and match schema
- `email-messaging integrate` — verify template keys are correctly referenced in mailers/services

### Email & Messaging: Scan

Read string catalogs and notification templates in `src/` or `assets/data/strings/`. Identify:
- All email template subject lines and body copy (keys matching `email.*` or `notification.*`)
- Templates already localized for the target locale
- Templates missing localized translations

Output a messaging manifest:

```
## Email & Messaging Localization Manifest — [Date]

| Key | Category | Source Subject / Preview | Status |
|-----|----------|--------------------------|--------|
| email.auth.welcome_subject | Auth | "Welcome to your workspace" | Translated |
| email.billing.invoice_receipt | Billing | "Your receipt for order #{{id}}" | Pending |
```

### Email & Messaging: Draft

Generate a localization template document for each notification domain (Auth, Billing, System). Include:

- Notification type and email client preview constraints
- Full subject line and markdown/HTML body with placeholder parameter definitions
- Tone and formality notes (`[Polite, professional]`, `[Action-oriented]`)
- Target audience context (e.g. "Admin receiving usage alert")

Ask: "May I write the email messaging localization spec to `production/localization/email-specs-[locale]-[date].md`?"

### Email & Messaging: Validate

Inspect localized email templates in `templates/emails/[locale]/` or string tables. Cross-reference against the manifest. Report:
- Missing translations (subject or body missing for target locale)
- Untranslated placeholder keys (e.g. broken `{{username}}` or missing liquid/mustache tags)
- Format or character overflow issues

### Email & Messaging: Integrate

Grep the code root for template IDs and mailer references. Verify each referenced template exists for all supported locales. Report broken template references.

---

## Phase 2H: RTL Check Mode

Right-to-left languages (Arabic, Hebrew, Persian, Urdu) require layout mirroring beyond
just translating text. This mode validates the implementation.

Determine the engine: read `stack.frontend` from `project.yaml`; if that key is absent or empty (including when `project.yaml` has no `engine:` block), fall back to `.claude/docs/technical-preferences.md`. Then check:

**Layout mirroring**
- Is RTL layout enabled in the engine? (Next.js: `Control.layout_direction`, FastAPI: `RTL Support` package, Cloudflare: text direction flags)
- Are all UI containers set to auto-mirror, or are positions hardcoded?
- Do progress bars, quota meters, and directional indicators mirror correctly?

**Text rendering**
- Are fonts loaded that support Arabic/Hebrew character sets?
- Is Arabic text rendered with correct ligatures (connected script)?
- Are numbers displayed as Eastern Arabic numerals where required?

**String assembly**
- Are there any string concatenations that assume left-to-right reading order?
- Do `{placeholder}` positions in sentences work correctly when sentence structure is reversed?

**Asset review**
- Are there UI icons with directional arrows or asymmetric designs that need mirrored variants?
- Do any text-in-image assets exist that require RTL versions?

Grep patterns to check:
- Engine-specific RTL flags in scene/prefab files
- Any `HBoxContainer`, `LinearLayout`, `HorizontalBox` nodes — verify layout_direction settings
- String concatenation with `+` near notification or UI code

Report findings. Flag BLOCKING issues (content unreadable without fix) vs ADVISORY (cosmetic improvements).

Ask: "May I write this RTL check report to `production/localization/rtl-check-[date].md`?"

---

## Phase 2I: Freeze Mode

String freeze locks the source (English) string table so that translations can proceed
without the source changing under the translators.

### freeze call

Check current freeze status in `production/localization/freeze-status.md` (if it exists).

If already frozen:
> "String freeze is currently ACTIVE (called [date]). [N] strings have been added or modified since freeze. These are freeze violations — they require re-translation or an approved freeze lift."

If not frozen, present the pre-freeze checklist:

```
Pre-Freeze Checklist
[ ] All planned UI screens are implemented
[ ] All UI copy and transactional email strings are final (no further copy revisions planned)
[ ] All system strings (error messages, tutorial text) are complete
[ ] /saas-localize scan shows zero hardcoded strings
[ ] /saas-localize validate shows no placeholder mismatches in source (en)
[ ] Marketing strings (landing page, pricing table, onboarding steps) are final
```

Use `AskUserQuestion`:
- Prompt: "Call string freeze now? This writes `production/localization/freeze-status.md` (Status: ACTIVE) and locks the source table."
- Options: `[A] Yes — call string freeze now` / `[B] No — I still have strings to add`

If [A]: Write `production/localization/freeze-status.md`:

```markdown
# String Freeze Status

**Status**: ACTIVE
**Called**: [date]
**Called by**: [user]
**Total strings at freeze**: [N]

## Post-Freeze Changes
[Any strings added or modified after freeze are listed here automatically by /saas-localize extract]
```

### freeze lift

If argument includes `lift`: ask "May I update `freeze-status.md` to LIFTED?", then set its Status to `LIFTED` and record the reason and date. Warn: "Lifting the freeze requires re-translation of all modified strings. Notify the translation team."

### freeze check (auto-integrated into extract)

When `extract` mode finds new or modified strings and `freeze-status.md` shows Status: ACTIVE — name `freeze-status.md` in extract's own "May I write" question, append the new keys to its `## Post-Freeze Changes` on approval, and warn:
> "⚠️ String freeze is active. [N] new/modified strings have been added. These are freeze violations. Notify your localization vendor before proceeding."

---

## Phase 2J: QA Mode

Localization QA is a dedicated pass that runs after translations are delivered but
before any locale ships. This is not the same as `/saas-localize validate` (which checks
completeness) — this is a structured playthrough-based quality check.

Spawn `localization-lead` via `Agent` with:
- The target locale(s) to QA
- The list of all screens/flows in the application (from `design/prd/` or `/saas-content-audit` output)
- The current `/saas-localize validate` report
- The cultural review report (if it exists)

Ask the localization-lead to produce a QA plan covering:

1. **Functional string check** — every string displays in-app without truncation, placeholder errors, or encoding corruption
2. **UI overflow check** — translated strings that exceed UI bounds (even if within character limits, some languages expand)
3. **Contextual accuracy** — a sample of 10% of strings reviewed in-app for translation accuracy and natural phrasing
4. **Cultural review items** — verify all BLOCKING items from the cultural review are resolved
5. **Media & tutorial subtitles** — if video walkthroughs or onboarding guides exist, verify subtitle timing is synchronized
6. **Compliance & legal localization** — check region-specific localization requirements (cookie consent banner, privacy policy, terms of service, tax and consumer disclosures per GDPR/LGPD)

Output a QA verdict per locale:

```
## Localization QA Verdict — [Locale]

**Status**: PASS / PASS WITH CONDITIONS / NOT ASSESSED / FAIL
**Reviewed by**: localization-lead
**Date**: [date]

### Findings
| ID | Area | Description | Severity | Status |
|----|------|-------------|----------|--------|
| LOC-001 | UI Overflow | "Settings" button text overflows on [Screen] | BLOCKING | Open |
| LOC-002 | Translation | [Key] translation is literal — sounds unnatural | ADVISORY | Open |

### Conditions (if PASS WITH CONDITIONS)
- [Condition 1 — must resolve before ship]

### Sign-Off
[ ] All BLOCKING findings resolved
[ ] Producer approves shipping [Locale]
```

First match wins: **FAIL** if any BLOCKING finding is open; else **NOT ASSESSED**
if a check could not run — the checks are walkthrough-based, so a locale nobody
has verified in-app (or whose translations were not delivered) cannot pass on the
string tables alone; name each check that did not run; else **PASS WITH
CONDITIONS** if conditions remain; else **PASS**. NOT ASSESSED outranks both
pass values — an unevaluated locale has not passed — and ranks below FAIL, so an
open BLOCKING finding is never buried behind it.

Ask: "May I write this localization QA report to `production/localization/loc-qa-[locale]-[date].md`?"

**Gate integration**: At `workflow: full`, the Polish → Release gate requires a PASS or PASS WITH CONDITIONS verdict for every translated locale being shipped (recommended at `standard`; dropped at `minimal`). A FAIL blocks release for that locale only — other locales may still proceed if their QA passes. A NOT ASSESSED locale has not passed: its QA did not run.

---

## Phase 3: Rules and Next Steps

### Rules
- English (en) is always the source locale
- Every string table entry must include a `context` field with translator notes, character limits, and placeholder meaning
- Never modify translation files directly — generate diffs for review
- Character limits must be defined per-UI-element and enforced in validate mode
- String freeze must be called before sending strings to translators — never translate a moving target
- RTL support must be designed in from the start — retrofitting RTL layout is expensive
- Cultural review is required for any locale where the product will be marketed commercially
- Email/messaging templates must include context notes — variables, layout boundaries, and tone

### Recommended Workflow

```
/saas-localize scan            → find hardcoded strings
/saas-localize extract         → build string table
/saas-localize freeze          → lock source before sending to translators
/saas-localize brief           → generate translator briefing document
[Send to translators]
/saas-localize validate        → check returned translations
/saas-localize cultural-review → flag culturally sensitive content
/saas-localize rtl-check       → if shipping Arabic / Hebrew / Persian
/saas-localize email-messaging → if shipping localized transactional emails/notifications
/saas-localize qa              → full localization QA pass
```

After `qa` returns PASS or PASS WITH CONDITIONS for every translated locale you ship, include the QA report paths when running `/saas-gate-check release`.

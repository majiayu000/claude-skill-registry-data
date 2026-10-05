---
name: ai-translated-localization
description: 'Localization scope and AI-translation execution for Apple-platform Apps on `Localizable.xcstrings` — default locale set, source / primary language rule, per-locale review gotchas, completeness gates. Use when deciding which locales to ship at project setup; when adding or refreshing user-facing strings (UI keys, Game Center, App Store metadata) in non-source locales; when `extractionState: stale` entries or untranslated placeholder markers appear; or when asked "how many locales", "how do translations enter git". Does NOT cover RTL layout or ASC upload mechanics → asc-api-automation.'
---

# AI-Translated Localization

## When to invoke

**Scope decisions:**
- Starting a new App and deciding which locales to support.
- Choosing a string catalog format (`.strings` vs `.xcstrings`).
- Planning the translation flow (manual / agency / AI agent).
- User asks "are 7 locales too many", "how do translations enter git", "how to handle multi-locale App Store metadata".

**Execution:**
- Adding new user-facing strings (UI keys, GC titles, ASC metadata, achievement descriptions) and need to fill out their non-source locales.
- Refreshing strings whose source text changed after translation shipped (locales showing `stringUnit.state: needs_review` in xcstrings — not to be confused with `extractionState: stale`, which flags a key no longer referenced in code, not a changed source).
- Auditing whether a release's xcstrings is complete (every key has every locale, no `<TRANSLATE>` placeholders shipping).

## Default decisions

### Default 7 locales

| Locale | Code | Notes |
|---|---|---|
| English | `en` | Catalog `sourceLanguage`; translation source for the fan-out |
| Traditional Chinese | `zh-Hant` | Primary language (author's native locale in the origin project; substitute yours) — author-written alongside `en`, never AI-translated |
| Japanese | `ja` | Largest adjacent market outside the Chinese sphere |
| Simplified Chinese | `zh-Hans` | Converted from `zh-Hant` + Mainland phrasing review |
| Spanish | `es` | World's second largest native-speaker base |
| Thai | `th` | Southeast Asia representative |
| Korean | `ko` | High-penetration Asian market |

- Locale codes are the **script-based BCP-47 forms** (`zh-Hant` / `zh-Hans`), not region
  forms (`zh-TW` / `zh-CN`) — matches the committed catalogs and, if the repo has one (recommended, see Step 5), its L10n completeness gate.
- **Minimum set**: zh-Hant + en (every project includes at least these two).
- Per-project locale lists can be adjusted, but **English and zh-Hant are always included**.

### Translation flow

- **Handled by an AI agent**, recorded as a step in `plan.md`: "author `en` + `zh-Hant` by hand, fan out the other 5 locales from `en`, write into `Localizable.xcstrings`" (see Execution playbook Step 1).
- Covers:
  - In-app strings
  - Game Center leaderboard / achievement names (for games)
  - App Store metadata (title / description / keywords / what's new)
  - Info.plist purpose strings (`NS…UsageDescription`, incl. `NSUserTrackingUsageDescription`) in `InfoPlist.xcstrings` — the privacy manifest itself has no localizable text
- Every time strings are added / modified, run another round of the AI translation flow; the diff lands in a PR.

### Catalog format

- Use Xcode's **`Localizable.xcstrings`** (String Catalog, introduced in Xcode 15+).
- Stop using legacy `.strings` / `.stringsdict` (unless an external tool forces it).
- xcstrings is JSON-structured: PR-friendly diffs and easy for AI to manipulate.

## Rationale

- 7 locales cover most of the global market while remaining a polish scope a solo developer can sustain.
- AI translation quality for App UI strings (short, clear context) is at commercial level; long marketing copy is still recommended for human review.
- xcstrings JSON structure is naturally friendly to AI / diff / version control.
- Primary = the author's native locale (`zh-Hant` in the origin project); `en` is the
  fan-out source because translator competence is broader from English (see Field notes).

## Deviation considerations

- **Focused target market**: shrink to zh-Hant + en + one target-market locale.
- **No budget / no time**: ship zh-Hant + en first; leave the other locales absent, or set them to `stringUnit.state: new`, for later — not `extractionState: stale`, which marks a key no longer used in code, not a not-yet-translated locale.
- **Regulated / sensitive content** (medical / financial / kids): **mandatory human review** after AI translation; add a review step to `plan.md`.
- **Special scripts / RTL** (Arabic / Hebrew): UI needs additional layout verification, not just translation.

## Execution playbook

Use when actually performing a translation pass. The flow is **source-pair seed → AI fan-out → tricky-case review → completeness check**.

### Step 1 — Seed source pair (en + zh-Hant)

- Source language for translation **must be English** (broader translator competence across all target locales than zh-Hant).
- Authors write English first; the primary locale (the author's native locale — `zh-Hant` in the origin project) is hand-written in parallel — *not* AI-translated from English. Both are written by the author with intent; the other 5 locales fan out from `en`.
- Each new key lands in xcstrings with **at minimum** `en` + `zh-Hant` populated and `extractionState: manual`.
- Other 5 locales (`ja`, `zh-Hans`, `es`, `th`, `ko`) start either absent or with the placeholder string `<TRANSLATE>` so the fan-out pass can find them with a single grep.

### Step 2 — AI fan-out pass

For each target locale, translate each key from `en` (source-of-truth) into the target locale. The AI doing the translation should:

- **Preserve substitutions**: `%@`, `%lld`, `%1$@`, `\n`, markdown markers (`**`, `_`), and any `${...}` interpolation tokens are copied verbatim.
- **Match plural/variation forms**: if xcstrings declares plural variations for `en`, all forms must exist in the target locale (`zero` / `one` / `two` / `few` / `many` / `other`) per CLDR plural categories for that locale — don't blindly copy English's two forms.
- **Match length budget**: if source is a button label (≤ 12 chars typical), keep target short. Don't let "OK" become a 6-word phrase. UI labels lose to long translations.
- **Match register / tone**: derive from `en`'s tone. Buttons are imperative, descriptions are neutral, error messages are direct. Don't add politeness markers absent in source (see locale gotchas below).
- **Preserve product nouns**: app name, brand terms, mode names that share visual identity across locales (e.g., "Practice" → 練習 in both zh-Hant and ja for visual consistency). Maintain a small **glossary** captured per-project to enforce this.

After translation, set that locale's `stringUnit.state` to `translated` — `translated` is a value of `stringUnit.state`, not of `extractionState`; leave `extractionState` at `manual` or `extracted_with_value` — so Xcode no longer flags the locale as needing attention.

### Step 3 — Tricky-case review (locale-specific gotchas)

Lessons captured from real translation passes, to apply as a second-pass review after the bulk
AI fan-out — per-locale gotchas for `ja`, `th`, `ko`, `es`, `zh-Hans`, and `en` are in
`references/locale-gotchas.md`.

### Step 4 — Visual / glossary consistency

Beyond per-string correctness, enforce a project-level glossary so the same concept renders identically across locales and screens:

- **Mode names** (e.g., "Daily" / "Practice") — pick one term per locale and use it everywhere (HomeView card, hub header, navigation title, Settings labels).
- **Product nouns** (app name, branded features) — don't translate.
- **Difficulty labels** (Easy / Medium / Hard) — short, consistent.
- **Action verbs** (Submit / Confirm / Cancel) — match iOS native terminology in each locale (Apple has localized Human Interface Guidelines for major locales).

Maintain the glossary as either inline comments in xcstrings, or a sidecar `Localization-Glossary.md` in `docs/` if it grows.

### Step 5 — Completeness check (before PR)

Verification gates before merging a translation pass:

- `<TRANSLATE>` count across xcstrings = 0 (none shipped).
- `stringUnit.state: needs_review` count = 0 across all locales (source text changed since last translation, now resolved).
- `stringUnit.state: new` count = 0 across all locales (nothing left untranslated).
- `extractionState: stale` count = 0 (no orphaned keys left in the catalog that the source code no longer references).
- Per-key locale coverage = 100% (parse xcstrings JSON; every `localizations` dict has every declared locale).
- Same coverage for `InfoPlist.xcstrings`: every purpose string (`NS…UsageDescription`, incl. `NSUserTrackingUsageDescription`) has every shipped locale — the purpose-string rules themselves are in `app-store-review-rejections`'s privacy-manifest reference.
- For plural keys: every locale has every plural form required by CLDR for that locale.
- Substitution token parity per key: `en` has N `%@` → all locales have N `%@` (or locale-specific reordering via `%1$@` / `%2$@`).
- Spot-check 3-5 keys per locale visually in the simulator with `Scheme → Run → Options → App Language`.

### L10n gate scope — and its two blind spots

If the repo has a per-key completeness gate (recommended, see Step 5), it checks **per-key
locale completeness**: every key present in a catalog has all declared locales, no `<TRANSLATE>`.
For the two blind spots it does **NOT** catch (a required key being absent entirely, and
multi-app repos sharing UI modules only) — both have shipped English-fallback bugs in real
projects — read `references/l10n-gates.md`.

### xcstrings editing footgun

When adding keys to a `Localizable.xcstrings`, **text-splice** the new entries
into the file — do **not** round-trip the whole catalog through a Python/JSON
`load → dump`. The round-trip reformats Xcode's style (`"k" : v` space-before-
colon + Xcode key order) and produces a multi-thousand-line noise diff that
buries the real change. Splicing keeps a clean, reviewable diff (real example:
4400-line noise diff collapsed to 192 lines after switching to splice approach).

### Tooling notes

For the xcstrings JSON schema (including the `"version"` field and plural variations) and LLM fan-out / ASC-metadata tooling notes, read `references/xcstrings-format.md`.

## Verification checklist

- `Localizable.xcstrings` exists and each key has an entry for every declared locale (2 for the minimum set).
- App Store Connect metadata is complete per locale (including screenshot captions).
- Game Center / achievement display names are complete per locale.
- `PrivacyInfo.xcprivacy` has no localizable text; the Info.plist purpose strings in `InfoPlist.xcstrings` and the App Store privacy policy page do need every shipped locale.

## Related skills

- `apple-platform-targets`: xcstrings requires Xcode 15+; aligns with the deployment target's toolchain.
- `collaboration-skills:spec-phase-orchestration`: "translation" should be an explicit step in `plan.md`.
- `asc-api-automation`: uploading localized App Store metadata once the strings are final.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.

## Field notes

Real translation passes have surfaced these recurring decisions:

- **Source = `en`, primary = the author's native locale (`zh-Hant` in the origin project)** — both written by author. The other 5 fan out from `en` because translator competence is broader from English than from Chinese for `th` / `ko` / `es`.
- **Glossary beats per-string correctness** — visual consistency across screens matters more than the perfect translation of any single string.
- **5 locales in one pass is the sweet spot** — fewer wastes the per-pass setup; more risks AI fatigue degradation on the last locales. 1 commit per locale keeps PR review tractable.

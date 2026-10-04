---
name: i18n-audit
description: >-
  Audits the app's translations: keys no code reads any more, keys code reads that no locale
  defines, maintained locales out of parity or holding untranslated copies, inline defaultValue
  fallbacks that drifted from the primary locale, and user-facing text hardcoded instead of
  translated. Fixes what is mechanical and flags what needs a translator. Use when asked to "audit
  translations", "find unused/missing i18n keys", "check hardcoded strings", "check locale parity",
  or after a UI rewrite that removed or renamed screens -- distinct from `comment-audit` (comments,
  not strings) and `double-check` (constants in general, not the translation catalog).
---

# i18n Audit

Keeps the translation catalog honest in both directions: nothing the UI shows is missing a
translation, and nothing in the catalog is left over from code that's gone.

Read the repo's conventions doc (`CLAUDE.md` or equivalent) fresh every run. It says which locales are
maintained (and must be at full parity), which are inactive (never to be translated), and how the
locale files are typed. Discover the locale directory and the translation call (`t(...)`) from the code; don't assume them.

## Non-negotiable constraints

- **Never write a translation for an inactive locale.** Removing a dead key from an inactive locale
  is maintenance and is allowed; adding or rewording text there is not.
- **Never invent a translation for a maintained non-primary locale** you can't produce reliably —
  flag it for a translator instead of shipping a guess.
- **A key is dead only when nothing reads it.** Check both quote styles and template literals, and
  count key strings stored in maps (`Record<Enum, 'section.key'>`) as readers. If a dynamic
  `` t(`section.${x}`) `` could produce a key, it is live.

## Phase 0 — Scope

Named files/features, or the whole app. For a scoped run, still check its keys against the full
codebase before calling any of them dead.

## Phase 1 — Find

1. **Orphaned keys.** Flatten the primary locale to dotted keys. For each, search the source (excluding
   the locale files) for the exact key in single quotes, double quotes, or a template prefix. Zero hits
   → candidate.
2. **Missing keys.** Every literal key passed to the translation call that the primary locale doesn't
   define.
   **Plural keys** are the exception to both checks. `t('k', { count })` reads suffixed variants of
   `k`, never `k` itself, so they look orphaned and `k` looks missing. Check which suffixes the
   library's configured format reads (e.g. `_one`/`_other` in i18next's v4 JSON, not the legacy
   `_plural`). A suffix the format doesn't read is a live bug — the plural never shows — not just a
   dead key. Prove it with the library itself and pin it with a test.
3. **Parity.** Maintained locales define the same key set (the typechecker may already enforce this).
   Also flag values identical to the primary locale's — likely untranslated copies. Brand names and
   currency codes are expected exceptions.
4. **Fallback drift.** An inline default (`t(key, 'text')` / `{ defaultValue: 'text' }`) whose text
   differs from the primary locale's value for that key. The fallback shows whenever a key fails to
   resolve, so drift means two phrasings of one string.
5. **Hardcoded user-facing text.** JSX text nodes, and string-literal `placeholder`, `title`, `label`,
   `accessibilityLabel` and toast messages that bypass the translation call. testIDs, style values and
   log messages are not user-facing.

## Phase 2 — Fix

- **Orphans:** delete them from every locale file, maintained and inactive. If inactive locales are
  typed as a partial of the primary, the typechecker reports leftovers as excess properties, one per
  object literal per run. Loop "typecheck → delete exactly the reported lines" until clean. Never
  delete a line the checker didn't name.
- **Missing keys:** add them to the maintained locales only. Primary-locale text comes from the
  existing fallback or UI copy; a translation you can't produce reliably goes in the report instead.
- **Fallback drift:** align the inline default to the primary locale's value (the catalog is the source
  of truth), or drop the default where the codebase convention allows.
- **Hardcoded text:** move it into the maintained locales under the feature's section, and replace the
  literal with the translation call.

## Phase 3 — Verify

- Run the repo's typecheck and tests.
- Re-run Phase 1's orphan and missing-key searches; both should come back empty for the scope.
- Diff the locale files: only deletions in inactive locales, and only additions/edits in maintained ones.

## Phase 4 — Report

Write the repo's dated verification report. Include:
- keys removed (with the evidence of zero readers);
- keys added;
- fallbacks aligned;
- strings moved into the catalog;
- anything flagged for a translator.

End with the chat summary in the repo's usual format for a change that touches files.

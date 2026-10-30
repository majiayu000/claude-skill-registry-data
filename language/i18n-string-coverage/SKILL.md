---
name: i18n-string-coverage
description: "Use when a product ships in several languages and untranslated text keeps slipping in. Scans code for user-facing strings not wrapped in the translation function, maps gaps to the translation files, reports coverage per language and fails PRs that add new untranslated strings."
---

# i18n-string-coverage

## Overview

Two coverage gaps this skill detects: hardcoded user-facing text not wrapped in
the i18n function, and keys present in `en.json` but missing from a locale file
(so the UI shows the raw key). It finds both via source scanning plus a
translation-file diff.

## When to use

- The product ships in 2+ locales.
- A bug report says "X appears in English in Y locale."
- Quarterly: scheduled coverage review.
- A new locale launches and the team needs the gap inventory.

## How to use

1. Identify the i18n wrap function for the stack (Step 1 table).
2. Scan source for hardcoded user-facing text not wrapped in `t()` (Step 2).
3. Diff each locale file against the `en` source-of-truth for per-locale coverage % (Step 3).
4. Assemble the report: per-locale %, new untranslated strings, orphan keys (Step 4).
5. Wire the scan into a per-PR gate that fails on new untranslated strings (Step 5).
6. Flag RTL / bidi strings that need extra translator attention (Step 6).

## Step 1 - Identify the i18n library

Per stack, the wrap function differs:

| Stack          | Wrap function                                    |
|----------------|--------------------------------------------------|
| react-i18next  | `t('key')` / `useTranslation()`                   |
| i18next        | `i18next.t('key')`                                |
| Vue i18n       | `$t('key')`                                       |
| Angular i18n   | `i18n` attribute / `$localize\`...\``             |
| Django         | `gettext('text')` / `_('text')` / `{% trans %}`   |
| Rails          | `I18n.t('key')` / `t('key')` (in views)            |
| FormatJS       | `intl.formatMessage({ id: 'key' })`               |
| .NET           | `Resources.SubmitButton`                           |

Configure per project.

## Step 2 - Scan for untranslated strings

```bash
# Pattern: JSX/TSX text children that aren't wrapped
# (heuristic; refines per-codebase)
grep -rn -E '>[A-Z][a-z]+ ?[A-Za-z ]*<' src/components/ \
  | grep -v -E '\$?\{?t\(|i18n\.t\(|trans|formatMessage'
```

This catches the obvious cases - `<button>Submit</button>` - 
without false-positive on `<button>{t('submit')}</button>`.

For more comprehensive detection, language-specific tooling:

| Tool                   | Use                                                |
|------------------------|----------------------------------------------------|
| `i18n-extract` (npm)    | JS/TS - extracts keys + finds missing             |
| `eslint-plugin-i18next` | JS/TS - ESLint rule for unwrapped strings         |
| `pylint-django-i18n`    | Django - pylint plugin                              |
| `i18nspector` (Debian)   | Lints `.po` files                                   |
| `xgettext`              | Cross-language: extracts strings from source       |

## Step 3 - Diff translation files

```python
# scripts/i18n-coverage.py
import json
from pathlib import Path

def flatten(d, prefix=''):
    for k, v in d.items():
        full = f'{prefix}.{k}' if prefix else k
        if isinstance(v, dict):
            yield from flatten(v, full)
        else:
            yield full

base_keys = set(flatten(json.loads(Path('locales/en.json').read_text())))  # source-of-truth

coverage = {}
for f in Path('locales').glob('*.json'):
    if f.stem == 'en': continue
    keys = set(flatten(json.loads(f.read_text())))
    covered = base_keys & keys
    coverage[f.stem] = {
        'missing': sorted(base_keys - keys),
        'extra_orphans': sorted(keys - base_keys),
        'pct': round(100 * len(covered) / len(base_keys), 1),
    }

print(json.dumps(coverage, indent=2))
```

## Step 4 - Report

Assemble per-locale coverage %, the new untranslated source strings (file, line,
string, suggested key), and orphan keys (present in a locale file but not in
source - deletion candidates). Full fill-in template:
[references/coverage-report.md](references/coverage-report.md).

## Step 5 - PR gate

```yaml
- name: i18n coverage check
  if: github.event_name == 'pull_request'
  run: |
    NEW_UNWRAPPED=$(./scripts/i18n-scan.sh)
    if [ -n "$NEW_UNWRAPPED" ]; then
      echo "::error::New untranslated strings found:"
      echo "$NEW_UNWRAPPED"
      exit 1
    fi
```

For new locales without 100% coverage, gate is informational, not
blocking - the gap is tracked, not blocked.

## Step 6 - Bilingual / RTL flagging

For RTL languages (Arabic, Hebrew, Persian, Urdu - per
[w3-rtl][w3rtl]), the report also flags:

[w3rtl]: https://www.w3.org/International/questions/qa-html-dir

- Strings that include hardcoded LTR/RTL marker characters.
- Strings with embedded HTML (often direction-sensitive).
- Strings combining RTL and LTR text (need bidi handling).

These need extra translator attention even when
"translated" - character-by-character translation may not
render correctly without bidi guidance.

## Worked example

A PR adds a promo banner to checkout. The scan (Step 2) flags
`<button>Apply your discount</button>` in `src/checkout/PromoBanner.tsx:18` -
the text is not wrapped in `t()`. The translation-file diff (Step 3) reports
`ja` at 60% coverage (218 keys missing) against 542 `en` keys.

The PR gate (Step 5) blocks on the newly unwrapped string; the `ja` gap stays
informational, not blocking. The developer wraps the text as
`t('checkout.promo.banner_cta')`, adds the key to all five locale files, and
re-runs. The scan reports zero new untranslated strings and the gate passes.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Heuristic-only string scanning (no whitelist for known-non-text)      | False positives on technical strings (URLs, IDs).                        | Whitelist patterns; tune per project. |
| Treating English as auto-100%                                          | New en strings without keys are still gaps in source-of-truth.           | All locales (including en) must have keys for new strings. |
| Scanning generated code                                                | False positives flood the report.                                        | Exclude `dist/`, `build/`, `node_modules/`. |
| Ignoring orphans                                                        | Translation files bloat over time.                                       | Surface orphans (Step 4 example); periodic cleanup. |
| Per-locale gates blocking new locale launches                          | Defeats the goal; team disables.                                         | Gate is informational for incomplete locales (Step 5). |

## Limitations

- **Heuristic scanning has gaps.** Dynamically-constructed strings
  (e.g., `t(dynamicKey)`) miss; manual review required.
- **Translator quality not addressed.** "Translated" doesn't mean
  "good translation"; pair with linguistic review.
- **Per-language differences in pluralization, gender, etc.** Some
  i18n libraries handle these well (ICU MessageFormat); others
  poorly. Coverage % doesn't reflect quality.

## References

- [w3rtl][w3rtl] - W3C on `dir` attribute + RTL languages.
- `pseudo-localization-runner` - sibling: layout-level i18n testing.
- `rtl-rendering-tester` - RTL-specific rendering verification.
- `locale-format-validator` - date / number / currency format verification.

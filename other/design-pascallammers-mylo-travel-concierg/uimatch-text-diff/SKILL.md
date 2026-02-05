---
name: uimatch-text-diff
description: >
  Compare two pieces of text using the uiMatch CLI text-diff command and classify how similar
  they are (exact match, whitespace/case-only, normalized match, or mismatch). Use this skill
  when the user cares about copy or label differences between design and implementation, or
  wants a cheap text-only check without running browser-based visual comparison.
---

# uiMatch Text Diff Skill

## Purpose

Compare **two pieces of text** (e.g. Figma label vs implementation text) and classify how different they are.

Use this skill to:

- detect copy mismatches (labels, button text, headings)
- distinguish between “only casing/whitespace changed” vs “actual wording changed”
- perform cheap checks without running browser comparisons

---

## Environment / assumptions

- Run commands from the repository root.
- `@uimatch/cli` is installed as a devDependency.
- Node.js 20+ is available.

This skill does **not** require Figma API or Playwright.  
`FIGMA_ACCESS_TOKEN` and browser installation are not needed here.

---

## Command usage

```bash
npx uimatch text-diff "<EXPECTED_TEXT>" "<ACTUAL_TEXT>" [--case-sensitive] [--threshold=<0-1>]
```

Notes:

- Options must use `=` syntax, for example: `--threshold=0.8`.
- Output is JSON with fields:
  - `kind`: `"exact-match" | "whitespace-or-case-only" | "normalized-match" | "mismatch"`
  - `similarity`: `0.0 - 1.0` similarity score
  - `expected`, `actual`
  - `normalizedExpected`, `normalizedActual`

### Examples

```bash
# Only case/whitespace differences
npx uimatch text-diff "Sign in" "SIGN  IN"

# Typo but still similar
npx uimatch text-diff "Submit" "Submt" --threshold=0.6

# Full-width vs half-width
npx uimatch text-diff "Button123" "Button１２３"
```

The CLI applies:

- Unicode NFKC normalization
- Whitespace collapsing
- Lowercasing (unless `--case-sensitive` is given)

---

## How Claude Code should use this skill

Typical flow:

1. Extract two text strings:
   - e.g., from Figma JSON / spec vs DOM `textContent`

2. Run `uimatch text-diff` with those strings.
3. Parse JSON output and:
   - report `kind` and `similarity`
   - explain whether differences are only formatting (`whitespace-or-case-only`) or real content changes (`mismatch`)

Use this skill:

- when a user suspects copy differences
- when visual diff is too noisy but text differences matter
- as a complement to `compare` results (to explain text-related discrepancies)

For pixel-level comparison, use `uimatch-compare` or `uimatch-suite` instead.

---
name: ios-input-hints
description: Ensure iOS/iPadOS-friendly form inputs (keyboard type, inputmode, autocomplete, autocapitalize/autocorrect, enterkeyhint) when editing or reviewing UI forms in web apps. Use when adding or modifying form fields (Svelte/HTML/TSX/etc.), auditing form UX, or fixing mobile Safari keyboard issues.
---

# iOS Input Hints

## Overview
Use this skill when working on UI forms to make input fields trigger the correct iOS/iPadOS keyboard and behavior without changing layout.

## Workflow
1. Identify every input/textarea/select in the target form(s).
2. For each field, choose the correct semantic `type` and `inputmode` based on expected data.
3. Add or validate `autocomplete`, `autocapitalize`, `autocorrect`, and `enterkeyhint` where helpful and safe.
4. Keep visual structure untouched; only adjust attributes.

## Keyboard Mapping (quick rules)
- **Numbers (integer):** `type="number"` + `inputmode="numeric"`.
- **Numbers (decimal):** `type="number"` + `inputmode="decimal"`.
- **Free text:** `type="text"` (no `inputmode` unless a specialized keyboard is desired).
- **Email:** `type="email"` (email keyboard) + `autocomplete="email"`.
- **URL:** `type="url"` + `autocomplete="url"`.
- **Phone:** `type="tel"` + `autocomplete="tel"`.
- **Search:** `type="search"` + `enterkeyhint="search"`.

## Meta Behaviors
- **Autocomplete:** Use the most specific token possible (e.g., `given-name`, `family-name`, `current-password`, `new-password`, `username`).
- **Autocapitalize/autocorrect:** Disable for codes, IDs, URLs, emails, and handles; allow for freeform text.
- **Enter key:** Use `enterkeyhint` to match intent (`next`, `done`, `search`, `send`).
- **Do not reshape UI:** Only adjust attributes; no styling or layout changes.

## References
- See `references/ios-input-hints.md` for detailed attribute guidance and examples.

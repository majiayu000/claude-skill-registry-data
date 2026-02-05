---
name: vkc-i18n-ko-vi-safety
description: Prevent i18n regressions for ko/en/vi (missing keys, long Vietnamese text UI breakage). Use when changing messages/*.json or adding user-facing strings.
metadata:
  short-description: i18n key safety + UI rules
---

# VKC i18n (ko/en/vi) Safety

## When to use

- You add/edit user-facing strings
- You touch `messages/*.json`
- A UI breaks only in Vietnamese

## Rules

- Never ship a key in only one of `ko/vi`.
- Keep nested key structure consistent across `ko.json`, `en.json`, `vi.json`.
- Avoid hardcoded literal strings in components; prefer message keys.

## Checks

- Run: `bash .codex/skills/vkc-repo-guardrails/scripts/lint-i18n-keys.sh`

## UI safety for long Vietnamese strings

- Apply “layout-safe” patterns by default:
  - `min-w-0` on flex children that contain text
  - `break-words` or `whitespace-pre-line` where wrapping is required
  - `line-clamp-*` where space must be capped
  - avoid fixed widths for text containers unless truncation is intentional

## Reference

- `.codex/skills/vkc-i18n-ko-vi-safety/references/i18n-ui-safety.md`

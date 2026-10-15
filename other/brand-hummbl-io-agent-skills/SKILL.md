---
name: brand
description: "DEPRECATED: Use brand-guidelines instead. This skill is retired as of 2026-08-19 and kept only as a redirect stub."
version: 0.4.0
status: retired
retired_at: 2026-08-19
retired_reason: "Superseded by brand-guidelines skill"
execution-mode: advisory
category: dev-tools
---
# DEPRECATED — Use `[brand-guidelines]`

This skill is **retired** (2026-08-19). It was superseded by `[brand-guidelines]`,
which contains the canonical two-tone green system (Grove + Verderer), both light
and dark themes, Crimson Pro/Inter/JetBrains Mono typography, voice/tone guidelines,
design token exports (CSS + JSON), and the brand audit checklist.

## Do not use `[brand]`

All dependents have been repointed to `[brand-guidelines]`. Invoke that instead:

```
[brand-guidelines]          # Canonical brand reference
[brand-guidelines] audit    # Audit a file/project for brand compliance
```

## Why it was retired

The `brand` skill (v0.3.0) was light-theme-only, missing Grove (`#12633c`), missing
dark theme tokens, and mislabeling `--font-serif` as IBM Plex Sans. The
`brand-guidelines` skill is the canonical source per `content/_BRAND_GUIDE.md` and
`PALETTE.md`.

## Migration

| Old (`[brand]`) | New (`[brand-guidelines]`) |
|---|---|
| `[brand]` | `[brand-guidelines]` |
| `[brand] audit` | `[brand-guidelines] audit` |
| `[brand] tokens` | `[brand-guidelines]` (see Design Tokens section) |
| `[brand] apply "<target>"` | `[brand-guidelines]` (apply tokens to target) |

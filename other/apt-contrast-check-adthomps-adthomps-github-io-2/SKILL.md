---
name: apt-contrast-check
description: Use when adding or changing color tokens, themes, or text/surface combinations, to verify every text token meets WCAG AA on every surface in each theme.
kind: skill
status: active
owner: APT
last_updated: 2026-10-04
source: APT decisions APT-017 and APT-018
title: "APT Contrast Check"
domain: "design"
source_paths: ["apt-principles-agents/skills/design/apt-contrast-check/SKILL.md", "apt-principles-agents/skills/design/apt-contrast-check/check-contrast.mjs"]
---

# APT Contrast Check

## Purpose

Keep color contrast executable instead of aspirational. Every text token (body, muted, links, status) must reach WCAG AA (4.5:1) on every surface it appears on in each theme, and the build should fail when one does not. A displayed contrast table alone let failing pairs ship in the past (APT-017, APT-018).

## When to Use

- Adding or changing any color token in a product's global stylesheet.
- Adding a theme, a surface token, or a status color.
- Syncing APT token values (`APT-TOKENS.json`) into a product.
- Reviewing a UI change that puts text on a new surface.

## Inputs

- The product's global stylesheet with HSL channel tokens (for example `apps/web/src/index.css`).
- Which CSS block holds the dark theme and which holds the light theme. This is auto-detected: `.dark` + `:root`, or `:root` + `.light`.

## Process

1. Run the bundled check from the product repo root, after the APT assets are installed:

   ```bash
   node .apt/skills/design/apt-contrast-check/check-contrast.mjs --css apps/web/src/index.css
   ```

2. Wire it into the product's design or validation script (for example `check:design` or `check:contrast`) so it runs in CI.
3. For each failure, fix the token value, not the call site. Use the canonical APT value when one exists, and record any product-specific value in a decision record.
4. When a new surface or text token is introduced, extend the pairs in the script here, in `apt-principles-agents`, and sync it to consumers. Do not fork it per product.

Pairs checked in each theme:

- `foreground`, `muted-foreground`, `success`, `warning` on `background`, `card`, `muted`, `secondary`, and (dark only) `apt-surface-elevated`.
- `primary` on `background` and `card`. On raised surfaces, links use `text-foreground` with an underline.
- `primary-foreground`, `success-foreground`, `warning-foreground`, and `destructive-foreground` on their fills.

Tokens a product does not define, and non-HSL values such as `var(--primary)`, are skipped.

## Outputs

- A pass line with the number of pairs checked, or a failing exit code with each pair and its ratio.
- Token fixes or decision records for any accepted deviation.

## Quality Bar

- Zero failing pairs in both themes before merge.
- The check runs automatically (CI or a validation script), not only on request.
- Product-specific status colors are not introduced; status uses the canonical `success`, `warning`, and `destructive` tokens.

## References

- [Accessibility principle](../../../principles/design/accessibility.md)
- [Design tokens reference](../../../references/design-tokens.json)
- [Design lint gates](../../../references/design-lint-gates.json)
- APT decisions APT-017 and APT-018 in `applied-practical-thinking/docs/DECISION_LOG.md`

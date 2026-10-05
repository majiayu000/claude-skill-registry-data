---
name: tweaks
description: |
  Generate a TWEAK_SCHEMA and EDITMODE block inside HTML so users can
  adjust colors, spacing, typography, and layout via dynamic sliders.
  Companion to any visual skill.
triggers:
  - "tweak"
  - "tweaks"
  - "adjust"
  - "slider"
  - "dynamic"
  - "parameters"
df:
  mode: utility
  platform: any
  scenario: design
  design_system:
    requires: true
---

# Tweaks Skill

Inject dynamic tweakability into any HTML artifact.

## How it works
Add a `TWEAK_SCHEMA` and `TWEAK_DEFAULTS` block inside a `<script>` tag:

```html
<script>
const TWEAK_SCHEMA = /*EDITMODE-BEGIN*/{
  "heroPadding": { "kind": "number", "min": 40, "max": 200, "step": 8, "unit": "px" },
  "accentColor": { "kind": "color" },
  "headingFont": { "kind": "enum", "options": ["serif", "sans", "mono"] }
}/*EDITMODE-END*/;

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "heroPadding": 96,
  "accentColor": "#c96442",
  "headingFont": "serif"
}/*EDITMODE-END*/;
</script>
```

## Rules
- Every tweakable property must have a schema entry.
- Use `var(--tweak-<key>)` in CSS to consume the value.
- The tweak panel reads TWEAK_SCHEMA and renders controls automatically.
- Default values must be valid and within min/max ranges.

## Output
Injectable script block. Add to any generated HTML.

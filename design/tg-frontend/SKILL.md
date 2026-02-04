---
name: tg-frontend
description: Frontend design system for Tellurium Games World of Darkness web application. Use when creating/modifying HTML templates (detail views, forms, lists), implementing components or stat displays, applying gameline-specific theming (Mage, Vampire, Werewolf, Changeling, Wraith, Hunter, Demon, Mummy), building responsive layouts, styling forms, or using template tags (dots, boxes, sanitize_html). Triggers on WoD template work, tg-card components, gameline headings, Django template tags.
---

# TG Frontend Design System

## Quick Reference

### Always Use TG Components

| Use | NOT |
|-----|-----|
| `tg-card` | `card` |
| `tg-card-header` | `card-header` |
| `tg-card-body` | `card-body` |
| `tg-btn` | `btn` |
| `tg-badge` | `badge` |
| `tg-table` | `table` |

### Gameline Classes

| Gameline | Heading | Badge | Data Attr |
|----------|---------|-------|-----------|
| Mage | `mta_heading` | `badge-mta` | `data-gameline="mta"` |
| Vampire | `vtm_heading` | `badge-vtm` | `data-gameline="vtm"` |
| Werewolf | `wta_heading` | `badge-wta` | `data-gameline="wta"` |
| Changeling | `ctd_heading` | `badge-ctd` | `data-gameline="ctd"` |
| Wraith | `wto_heading` | `badge-wto` | `data-gameline="wto"` |
| Hunter | `htr_heading` | `badge-htr` | `data-gameline="htr"` |
| Demon | `dtf_heading` | `badge-dtf` | `data-gameline="dtf"` |
| Mummy | `mtr_heading` | `badge-mtr` | `data-gameline="mtr"` |

Use `{{ object.get_heading }}` and `{{ object.get_badge_class }}` for dynamic classes.

### Template Tags

```html
{% load sanitize_text dots %}
{{ rating|dots }}       {# ●●●○○ (auto 5 or 10 max) #}
{{ rating|dots:10 }}    {# explicit max 10 #}
{{ value|boxes }}       {# ■■■□□ for temp values #}
{{ content|sanitize_html|linebreaks }}
```

**`dots` filter**: Converts numeric rating to WoD-style dots. Auto-detects max of 5 or 10 based on value. Returns empty string for non-numeric input.

**`boxes` filter**: Similar to dots but uses boxes (■□). Used for temporary values, health tracking, damage.

**`sanitize_html` filter**: Sanitizes user HTML, preserves safe formatting (p, br, strong, em, ul, ol, li, a, h1-h6). Strips scripts, event handlers, iframes. Always use for user-generated content.

### Status Badges

```html
<span class="tg-badge badge-{{ object.status|lower }}">{{ object.get_status_display }}</span>
```

Classes: `badge-un` (gray), `badge-sub` (blue), `badge-app` (green), `badge-ret` (orange), `badge-dec` (red)

## Task-Based Workflow

**Creating/Editing Detail Views**: See [references/detail-patterns.md](references/detail-patterns.md)

**Creating/Editing Forms**: See [references/form-patterns.md](references/form-patterns.md)

**Choosing Layout Patterns**: See [references/layout-decisions.md](references/layout-decisions.md)

## Quick Patterns

**Page Header Card:**
```html
<div class="tg-card header-card mb-4" data-gameline="{{ object.gameline|lower }}">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ object.get_heading }}">{{ object.name }}</h1>
    </div>
</div>
```

**Section Card:**
```html
<div class="tg-card">
    <div class="tg-card-header text-center">
        <h5 class="tg-card-title {{ object.get_heading }}">Section Title</h5>
    </div>
    <div class="tg-card-body text-center" style="padding: 20px;">
        <!-- Content -->
    </div>
</div>
```

**Trait Row with Dots:**
```html
<div class="trait-row">
    <span class="trait-name">Strength:</span>
    <span class="trait-dots">{{ character.strength|dots }}</span>
</div>
```

**Form Field:**
```html
<div class="row mb-3">
    <div class="col-md-6">
        <label for="{{ form.name.id_for_label }}" class="form-label">Name</label>
        {{ form.name }}
    </div>
</div>
```

**Checkbox:**
```html
<div class="form-check">
    {{ form.field }}
    <label class="form-check-label" for="{{ form.field.id_for_label }}">Label</label>
</div>
```

## Core Style Rules

### Typography
- Labels: `font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary);`
- Values: `font-weight: 700; color: var(--theme-text-primary);`
- Large numbers: `font-size: 1.5rem; font-weight: 700;`

### Spacing
- Card body: `padding: 20px;` (standard) or `padding: 24px;` (spacious)
- Section gaps: `mb-4` or `mb-5`
- Related items: `mb-3`

### Backgrounds
- Primary stat: `rgba(0,0,0,0.05)`
- Content box: `rgba(0,0,0,0.02)`
- Active feature: `rgba(0,255,0,0.1)`

### Responsive Columns
- Two-column: `col-md-6`
- Three-column: `col-md-4`
- Card grid: `col-sm-6 col-md-4 col-lg-3`
- Equal height: add `h-100` to cards
- Mobile margin: `mb-3 mb-md-0`

## Consistency Checklist

- [ ] All cards use `tg-card` (not Bootstrap `card`)
- [ ] Headers have gameline class and `data-gameline`
- [ ] Labels uppercase, values bold
- [ ] Template loads `{% load dots sanitize_text %}`
- [ ] Equal-height cards use `h-100`
- [ ] Responsive with proper column classes

---
name: typography-audit
description: Check and fix typography hierarchy on a page. Fixes h2-to-h4 skips, ensures all sections have left-aligned title/description with max-w-3xl, removes centering classes, and adds missing headers with i18n keys.
---

# Typography Audit

Audit and fix typography structure in page sections. Ensures proper heading hierarchy, left-aligned section headers, and consistent max-width constraints.

## Workflow

1. **Read Page File** - Identify all section components imported
2. **For Each Section Component (skip Hero/CTA):**
   - Check heading hierarchy (no skipping levels)
   - **Check if h2 has a sibling `<p>` description** - if not, ADD one
   - Wrap standalone h2 in `<div className="max-w-3xl mb-10">`
   - Fix centering issues on existing headers
   - Add max-w-3xl wrapper if missing
3. **Update i18n Files** - Add description keys for sections missing them
4. **Report Changes** - List all modifications made

## CRITICAL: Every Section Needs h2 + p

**Problem:** Many sections have only an h2 heading without a description paragraph.

**Rule:** EVERY section (except Hero/CTA) must have:
- h2 title
- p description (immediately after h2)
- Both wrapped in `<div className="max-w-3xl mb-10">`

**Check for these patterns and FIX them:**

```tsx
// WRONG: h2 alone without p
<h2>{t("title")}</h2>
<div className="grid">...</div>

// WRONG: h2 with spacing classes but no p
<h2 className="mb-12">{t("title")}</h2>

// WRONG: motion.h2 alone
<motion.h2 ...>{t("title")}</motion.h2>

// CORRECT: h2 + p in wrapper
<div className="max-w-3xl mb-10">
  <h2>{t("title")}</h2>
  <p className="mt-4">{t("description")}</p>
</div>
```

## Heading Hierarchy Rules

### Valid Sequences
- h1 → h2 → h3 → h4 (sequential)
- h2 → h3 (section with subsections)
- h2 → h3 → h4 (nested subsections)

### Invalid Sequences (FIX THESE)
- h2 → h4 (skip h3) → Change h4 to h3
- h1 → h3 (skip h2) → Change h3 to h2
- Multiple h1 per page → Change extras to h2

### One H1 Rule
Only the Hero section should have h1. All other sections use h2 for their main title.

## Section Header Structure

Every section (except Hero and CTA) must have this header structure:

```tsx
<section className="py-16 lg:py-24">
  <div className="container">
    {/* Section Header - LEFT ALIGNED */}
    <div className="max-w-3xl mb-10">
      <h2>{t("title")}</h2>
      <p className="mt-4">{t("description")}</p>
    </div>

    {/* Section Content */}
    ...
  </div>
</section>
```

**Required:**
- `max-w-3xl` on header wrapper (768px max-width)
- `mb-10` spacing before content
- `mt-4` between h2 and p
- Left-aligned (NO centering classes)

## Classes to REMOVE from Headers

When fixing section headers, remove these classes:

### From header wrapper div:
```
text-center
items-center
justify-center
flex items-center justify-center
```

### From description paragraph:
```
mx-auto
text-center
```

### From h2 heading:
```
text-center
```

## Classes to ADD/KEEP

### Header wrapper div:
```tsx
className="max-w-3xl mb-10"
```

### Description paragraph:
```tsx
className="mt-4"
```

## Exceptions (Keep Centered)

These section types should remain centered:
- **CTA sections** - Image overlays with centered text (cta*.tsx)
- **Hero sections** - Full-width hero with custom layout (hero*.tsx)

Skip these when auditing.

## i18n Keys Pattern

When adding missing description, add to both `de.json` and `en.json`:

```json
{
  "sectionKey": {
    "title": "Existing Title",
    "description": "[ADD DESCRIPTION HERE]"
  }
}
```

## Example Fixes

### Fix 1: Heading Hierarchy Skip

**Before (projects5.tsx):**
```tsx
<h2>{t("title")}</h2>
...
<h4>{project.title}</h4>  // WRONG: h2 → h4
```

**After:**
```tsx
<h2>{t("title")}</h2>
...
<h3>{project.title}</h3>  // CORRECT: h2 → h3
```

### Fix 2: Centered Header

**Before (compare5.tsx):**
```tsx
<div className="text-center">
  <h2>{t("title")}</h2>
  <p className="mx-auto mt-4 max-w-3xl">{t("description")}</p>
</div>
```

**After:**
```tsx
<div className="max-w-3xl mb-10">
  <h2>{t("title")}</h2>
  <p className="mt-4">{t("description")}</p>
</div>
```

### Fix 3: Heading Only (No Description)

**Before (faq9.tsx):**
```tsx
<motion.h2
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
  viewport={{ once: true }}
  className="mb-12 mt-2"
>
  {t("title")}
</motion.h2>
<Accordion>...</Accordion>
```

**After:**
```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
  viewport={{ once: true }}
  className="max-w-3xl mb-10"
>
  <h2>{t("title")}</h2>
  <p className="mt-4">{t("description")}</p>
</motion.div>
<Accordion>...</Accordion>
```

**i18n addition:**
```json
{
  "faq": {
    "title": "Häufige Fragen",
    "description": "[ADD: Brief intro text about the FAQ section]"
  }
}
```

### Fix 4: Standalone h2 (No Wrapper)

**Before (projects5.tsx):**
```tsx
<div className="container">
  <h2 className="uppercase">{t("title")}</h2>
  <div className="mt-10 grid">...</div>
</div>
```

**After:**
```tsx
<div className="container">
  <div className="max-w-3xl mb-10">
    <h2>{t("title")}</h2>
    <p className="mt-4">{t("description")}</p>
  </div>
  <div className="grid">...</div>
</div>
```

**Note:** Remove `uppercase` and spacing classes from h2, move animation to wrapper if needed.

### Fix 5: motion.h2 to motion.div Wrapper

**Before:**
```tsx
<motion.h2 initial={...} whileInView={...} className="mb-8">
  {t("title")}
</motion.h2>
```

**After:**
```tsx
<motion.div initial={...} whileInView={...} className="max-w-3xl mb-10">
  <h2>{t("title")}</h2>
  <p className="mt-4">{t("description")}</p>
</motion.div>
```

**Rule:** Move Framer Motion props from h2 to the wrapper div.

## Output

After running this skill, report:
- Number of heading hierarchy fixes
- Number of centering fixes
- Number of missing descriptions added
- List of i18n keys added

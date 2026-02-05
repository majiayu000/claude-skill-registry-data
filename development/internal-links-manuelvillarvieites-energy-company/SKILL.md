---
name: internal-links
description: Connect all buttons and links to pages or same-page sections. Ensures every CTA has a valid href, uses Next.js Link component, and adds section IDs for anchor links.
---

# Internal Links

Ensure all buttons and links in a page connect to valid destinations - either other pages or sections on the same page.

## Workflow

1. **Read Page File** - Identify all section components
2. **For Each Section:**
   - Find all `<Button>` components
   - Find all `<a>` or `<Link>` elements
   - Verify each has a valid `href`
3. **Add Missing Links** - Wrap buttons with `<Link>` as needed
4. **Add Section IDs** - For same-page anchor targets
5. **Update i18n** - Add CTA text if missing

## INPUT Required

When running this skill, you need:
- **Page route** (e.g., `/`, `/leistungen`)
- **Site pages** from `docs/sitemap.md`

## Button Link Pattern

All buttons must be wrapped with Next.js `<Link>`:

```tsx
// CORRECT: Button with Link
<Button asChild>
  <Link href="/kontakt">{t("cta")}</Link>
</Button>

// CORRECT: Button with anchor link
<Button asChild>
  <Link href="#pricing">{t("cta")}</Link>
</Button>

// WRONG: Button without link
<Button>{t("cta")}</Button>

// WRONG: Button with onClick only
<Button onClick={handleClick}>{t("cta")}</Button>
```

## Link Types

### 1. Page Links

Link to other pages in the site:

```tsx
<Link href="/kontakt">Contact</Link>
<Link href="/leistungen">Services</Link>
<Link href="/projekte">Portfolio</Link>
<Link href="/ueber-uns">About</Link>
```

### 2. Anchor Links (Same Page)

Link to sections on the same page:

```tsx
<Link href="#pricing">View Pricing</Link>
<Link href="#faq">FAQ</Link>
<Link href="#contact">Get in Touch</Link>
```

**Requires:** Target section must have matching `id`:

```tsx
<section id="pricing" className="py-16 lg:py-24">
<section id="faq" className="py-16 lg:py-24">
```

### 3. Page + Anchor Links

Link to a section on another page:

```tsx
<Link href="/leistungen#webdesign">Web Design Services</Link>
<Link href="/kontakt#form">Contact Form</Link>
```

## Common CTA Destinations

| Section | Primary CTA | Secondary CTA |
|---------|-------------|---------------|
| Hero | `/kontakt` | `/projekte` or `#features` |
| Features | `/leistungen` | `#pricing` |
| Pricing | `/kontakt` | - |
| CTA | `/kontakt` | - |
| Projects | `/projekte` | `/kontakt` |
| FAQ | `/kontakt` | - |

## Section IDs

Add `id` to sections that are anchor link targets:

```tsx
// Homepage sections
<section id="features" ...>
<section id="process" ...>
<section id="pricing" ...>
<section id="projects" ...>
<section id="testimonials" ...>
<section id="faq" ...>
<section id="contact" ...>
```

### ID Naming Convention

Use lowercase, hyphenated names matching the section purpose:

| Section Component | ID |
|-------------------|-----|
| Feature56 | `features` |
| Feature207 | `process` |
| Pricing8 | `pricing` |
| Projects5 | `projects` |
| Testimonial4 | `testimonials` |
| Faq9 | `faq` |
| Cta21 | `contact` |

## Checklist Per Section

For each section, verify:

- [ ] All `<Button>` components have `asChild` prop
- [ ] All buttons are wrapped with `<Link href="...">`
- [ ] href points to valid page or `#sectionId`
- [ ] If anchor link, target section has matching `id`
- [ ] Button text is from i18n (`{t("cta")}`)

## Example Fixes

### Fix 1: Button Without Link

**Before:**
```tsx
<Button size="lg">
  {t("cta")}
</Button>
```

**After:**
```tsx
<Button asChild size="lg">
  <Link href="/kontakt">{t("cta")}</Link>
</Button>
```

### Fix 2: Add Section ID for Anchor

**Before (button):**
```tsx
<Button asChild>
  <Link href="#pricing">{t("viewPricing")}</Link>
</Button>
```

**Before (section - missing id):**
```tsx
<section className="py-16 lg:py-24">
```

**After (section - with id):**
```tsx
<section id="pricing" className="py-16 lg:py-24">
```

### Fix 3: Scroll Hint Button

**Before:**
```tsx
<Button variant="link" className="text-white">
  <span>{t("scrollHint")}</span>
  <ArrowDown className="size-4" />
</Button>
```

**After:**
```tsx
<Button asChild variant="link" className="text-white">
  <Link href="#features">
    <span>{t("scrollHint")}</span>
    <ArrowDown className="size-4" />
  </Link>
</Button>
```

## Import Requirements

Ensure sections have the Link import:

```tsx
import Link from "next/link";
```

## Output

After running this skill, report:
- Number of buttons linked
- Section IDs added
- List of link destinations used

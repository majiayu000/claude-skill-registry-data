---
name: sitemap-structure
description: Create website sitemap with page structure and section selection. Use at project start to define pages, routes, and shadcnblocks sections for each page. Outputs docs/sitemap.md. Triggers on "sitemap", "page structure", "website structure", "create pages".
---

# Website Sitemap & Structure

Define the website structure with pages, routes, and section selection.

## Workflow

1. **Gather Input** - Business type, name, location, goals, target audience, USPs, number of pages
2. **Define Core Pages** - Based on business requirements and standard website patterns
3. **Add Legal Pages** - Impressum and Datenschutz (mandatory)
4. **Select Sections** - Choose shadcnblocks sections for each page from the catalog
5. **Define Priorities** - P0 (homepage), P1 (main pages), P2 (secondary pages)
6. **Write Output** - Create docs/sitemap.md

## Input Template

```
Business Type: [e.g., Beauty Salon, Restaurant, Agency]
Business Name: [Company name]
Location: [City, Country]
Primary Goal: [Lead generation, Brand awareness, Bookings]
Target Audience: [Who are the customers]
Unique Selling Points: [What makes them different]
Number of Pages: [4-6 typical for small business]
```

## Standard Page Patterns

### Small Business (4-6 pages)
- Homepage `/`
- Services/Products `/dienstleistungen` or `/produkte`
- About `/ueber-uns`
- Contact `/kontakt`

### Service Business (6-8 pages)
- Homepage `/`
- Services Overview `/dienstleistungen`
- Individual Service Pages `/dienstleistungen/[service]`
- About `/ueber-uns`
- Contact `/kontakt`
- Pricing `/preise` (optional)

### E-commerce/Portfolio (8+ pages)
- Homepage `/`
- Products/Portfolio `/produkte` or `/portfolio`
- Category Pages
- About `/ueber-uns`
- Contact `/kontakt`
- Blog `/blog` (optional)

## Legal Pages (Always Required)

These are MANDATORY for every project:
- `/impressum` - Legal notice (German/Swiss law)
- `/datenschutz` - Privacy policy (DSGVO/DSG compliance)

Note: Legal pages are excluded from the "number of pages" count.

## Section Selection

See references/shadcnblocks-catalog.md for all available sections.

### Typical Page Structures

**Homepage:**
| Section Type | Purpose |
|--------------|---------|
| Navbar | Navigation (layout component) |
| Hero | First impression, main CTA |
| Logos | Trust signals (optional) |
| Feature/Services | What you offer |
| About Preview | Brief company intro |
| Stats | Social proof numbers |
| Testimonials | Customer reviews |
| CTA | Call to action |
| Footer | Links, contact (layout component) |

**Services Page:**
| Section Type | Purpose |
|--------------|---------|
| Hero | Services introduction |
| Services/Feature | Detailed offerings |
| Process | How you work |
| Pricing | Cost indicators |
| CTA | Book/contact |

**About Page:**
| Section Type | Purpose |
|--------------|---------|
| Hero | About introduction |
| About/Content | Company story |
| Team | People profiles |
| Timeline | History/milestones |
| CTA | Connect with us |

**Contact Page:**
| Section Type | Purpose |
|--------------|---------|
| Hero | Contact introduction |
| Contact | Form, map, info |
| FAQ | Common questions |

## Output Format: docs/sitemap.md

```markdown
# Sitemap - [Business Name]

## Overview

| Page | Route | Purpose | Priority |
|------|-------|---------|----------|
| Homepage | `/` | Main landing, services overview | P0 |
| Services | `/dienstleistungen` | Detailed offerings | P1 |
| About | `/ueber-uns` | Team, story, trust | P1 |
| Contact | `/kontakt` | Booking, inquiries | P1 |

## Legal Pages (Required)

| Page | Route |
|------|-------|
| Impressum | `/impressum` |
| Datenschutz | `/datenschutz` |

---

## Page Sections

### 1. Homepage `/`

| Order | Section | shadcnblocks | Purpose |
|-------|---------|--------------|---------|
| 1 | Navbar | navbar-X | Navigation |
| 2 | Hero | hero-X | First impression |
| ... | ... | ... | ... |
| N | Footer | footer-X | Links, contact |

### 2. Services `/dienstleistungen`
[Same table format]

### 3. About `/ueber-uns`
[Same table format]

### 4. Contact `/kontakt`
[Same table format]

---

## Shared Components

- **Navbar**: Consistent across all pages (layout.tsx)
- **Footer**: Consistent across all pages (layout.tsx)

---

## URL Structure

/ -> Homepage (DE default)
/en -> Homepage (EN)
/dienstleistungen -> Services (DE)
/en/services -> Services (EN)

---

## Notes

- All sections from shadcnblocks.com
- Legal pages (Impressum, Datenschutz) excluded from page count
- Bilingual support via next-intl (DE primary, EN secondary)
```

## Rules

1. All sections MUST come from shadcnblocks.com
2. Impressum and Datenschutz are MANDATORY (excluded from page count)
3. Bilingual support (DE/EN) via next-intl
4. Navbar and Footer go in layout.tsx, not individual pages
5. Homepage is always P0 priority
6. Focus on conversion-oriented structure

## What This Skill Does NOT Do

- Keyword research (use seo-keyword-research skill)
- SEO strategy (use seo-keyword-research skill)
- Content writing (use seo-content-optimization skill later)
- Technical SEO (use technical-seo skill later)

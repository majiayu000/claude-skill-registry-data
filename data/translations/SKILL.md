---
name: shopify-translations
description: Manage Shopify store translations with French as source language. Use when working with translation files, updating translations, or managing multi-language Shopify content. Triggers on "translate", "translations", "localization", "i18n", "French to German/Italian/English".
---

# Shopify Translations Management

Two separate translation systems - use the right one for each case.

## Two Translation Systems

| System | Use For | Location |
|--------|---------|----------|
| **API Translations** | Merchant-editable content, block settings | `translations-to-edit.json` |
| **Locale Files** | Hardcoded theme text, labels, buttons | `shopify-theme/locales/*.json` |

## 1. API Translations (Merchant Content)

French (fr_original) as source → German, Italian, English.

### Structure

```json
{
  "key": "section.page.json.heading:id",
  "fr_original": "Design Gratuit",
  "de_fixed": "Kostenlose Gestaltung",
  "de_status": "completed",
  "it_fixed": "Design Gratuito",
  "it_status": "completed",
  "en_fixed": "Free Design",
  "en_status": "completed"
}
```

### Status Values
- `pending` - Not yet translated
- `completed` - Ready to publish
- `verified` - Reviewed and approved

### Commands

```bash
npm run translations:myarmy:extract   # Extract from Shopify
npm run translations:myarmy:review    # Generate review report
npm run translations:myarmy:translate # Auto-translate (needs OPENAI_API_KEY)
npm run translations:myarmy:publish   # Publish to Shopify
npm run translations:myarmy:backup    # Create backup
npm run translations:myarmy:workflow  # Full workflow
```

## 2. Locale Files (Theme Code)

For hardcoded theme text only - stored in Git.

### File Locations

```
shopify-theme/locales/
├── en.default.json  # English source
├── fr.json          # French
├── de.json          # German
└── it.json          # Italian
```

### Key Structure (3-level nested)

```json
{
  "products": {
    "benefits": {
      "lifetime_guarantee": "Lifetime Guarantee",
      "lifetime_description": "Yes, you read that right..."
    }
  }
}
```

### Usage in Liquid

```liquid
{{ 'products.benefits.lifetime_guarantee' | t }}
{{ 'products.benefits.lifetime_description' | t: default: 'Fallback' }}
```

### Deployment

```bash
# Push locale files to production
shopify theme push --theme=185946079581 --store=087ffd-4a.myshopify.com \
  --allow-live --only="locales/"
```

## When to Use Which

| Content Type | Use |
|--------------|-----|
| Section titles, labels | Locale files |
| Error messages | Locale files |
| Button text | Locale files |
| Block settings content | API translations |
| Product descriptions | API translations |
| Merchant-editable text | API translations |

## Swiss Military Terminology

Always use:
- ✅ **badge** (NOT "écusson")
- ✅ **section** (NOT "peloton")

## Key Rules

**DO:**
- Keep French as source (fr_original)
- Keep all 4 locale files in sync
- Review before publishing
- Create backups before major changes

**DON'T:**
- Edit fr_original directly
- Mix the two translation systems
- Skip review step
- Forget to update all language files

## Environment Variables

```bash
SHOPIFY_ACCESS_TOKEN=shpat_...
SHOPIFY_STORE_DOMAIN=087ffd-4a.myshopify.com
OPENAI_API_KEY=sk-...  # Optional, for auto-translation
```

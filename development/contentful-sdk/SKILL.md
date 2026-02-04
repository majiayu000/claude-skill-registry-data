---
name: contentful-sdk
description: Comprehensive Contentful SDK guide for TypeScript/JavaScript. Covers Management SDK (CMA) for content/schema management, Delivery SDK (CDA) for fetching content, and App Framework SDK for building Contentful apps. Use for any Contentful API integration work.
---

# Contentful SDK Guide

Comprehensive guide for Contentful SDKs in TypeScript/JavaScript.

## Which SDK Do You Need?

- **Management SDK (CMA)**: Creating/updating content, managing content types, assets, environments → Start at [references/management/overview.md](references/management/overview.md)
- **Delivery SDK (CDA)**: Fetching published content for production apps → Start at [references/delivery/overview.md](references/delivery/overview.md)
- **App Framework**: Building Contentful Apps that extend the UI → Start at [references/app-framework/overview.md](references/app-framework/overview.md)

## Management SDK (CMA)

For creating, updating, and managing content, content types, assets, and environments.

**Start here**: [references/management/overview.md](references/management/overview.md)

**Topics**:
- [**content-types.md**](references/management/content-types.md) - Define and update content models with field types and validations
- [**entries.md**](references/management/entries.md) - Create, update, query, and publish entries with version locking
- [**assets.md**](references/management/assets.md) - Upload, process, and publish media files
- [**environments.md**](references/management/environments.md) - Create, clone, and manage environments and aliases
- [**error-handling.md**](references/management/error-handling.md) - Handle rate limits, version conflicts, and validation errors
- [**bulk-operations.md**](references/management/bulk-operations.md) - Pagination, batch processing, and concurrency control

## Delivery SDK (CDA)

For fetching published content in production applications.

**Start here**: [references/delivery/overview.md](references/delivery/overview.md)

**Topics**:
- [**querying.md**](references/delivery/querying.md) - Query parameters, filters, search operators, and pagination
- [**includes-links.md**](references/delivery/includes-links.md) - Link resolution, includes parameter, and handling references
- [**localization.md**](references/delivery/localization.md) - Locale handling, fallbacks, and multi-language content
- [**rich-text.md**](references/delivery/rich-text.md) - Rendering rich text fields with embedded entries and assets

## App Framework SDK

For building apps that extend the Contentful UI.

**Start here**: [references/app-framework/overview.md](references/app-framework/overview.md)

**Topics**:
- [**locations.md**](references/app-framework/locations.md) - All app locations: field, sidebar, dialog, entry editor, page, config
- [**sdk-apis.md**](references/app-framework/sdk-apis.md) - Navigator, dialogs, notifier, access, and window APIs
- [**parameters.md**](references/app-framework/parameters.md) - Installation, instance, and invocation parameters

## Quick Reference

### Version Locking (Management SDK)
Always pass `sys` when updating to prevent conflicts:
```typescript
const entry = await client.entry.get({ spaceId, environmentId, entryId })
await client.entry.update({ spaceId, environmentId, entryId }, {
  sys: entry.sys,  // Required for version locking
  fields: { ... }
})
```

### TypeScript Entry Skeletons (Delivery SDK)
Define type-safe content structures:
```typescript
type BlogPostSkeleton = {
  contentTypeId: 'blogPost'
  fields: {
    title: EntryFieldTypes.Text
    slug: EntryFieldTypes.Symbol
    body: EntryFieldTypes.RichText
  }
}
const entry = await client.getEntry<BlogPostSkeleton>('entry-id')
```

### CMA Integration in Apps (App Framework)
Use SDK adapter to avoid exposing tokens:
```typescript
import contentful from 'contentful-management'

const cma = contentful.createClient(
  { apiAdapter: sdk.cmaAdapter },
  {
    type: 'plain',
    defaults: {
      spaceId: sdk.ids.space,
      environmentId: sdk.ids.environmentAlias ?? sdk.ids.environment
    }
  }
)
```

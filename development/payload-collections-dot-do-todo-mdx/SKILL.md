---
name: payload-collections
description: Use when designing, creating, or modifying Payload CMS collections in db.sb - covers field patterns, relationships, hooks, access control, and how collections map to Nouns in the business-as-code system
---

# Payload Collection Design

Patterns for designing Payload CMS collections that power the Business-as-Code system.

## Core Principle

**Every Collection is a Noun. Every Noun renders beautifully.**

```
Collection (Payload) → Noun (schema.org.ai) → Component (mdxui)
```

## Collection Domains

Collections are organized by domain in `packages/db.sb/src/collections/`:

| Domain | Purpose | Examples |
|--------|---------|----------|
| admin | Platform admin | Users, Orgs, ApiKeys |
| ai | AI/ML experiments | ModelEvals, AIExperiments |
| api | API infrastructure | Proxies, Crawlers |
| business | Business entities | Businesses, Teams, Goals |
| code | Code artifacts | Workers, Artifacts |
| communications | Messaging | Messages, Sequences, Channels |
| compliance | Regulatory | Policies, Controls, Evidence |
| content | Documents | Documents, Files, Presentations |
| data | Ontology | Nouns, Verbs, Actions, Events |
| design | Visual | Themes |
| experiments | Testing | Experiments, Hypotheses, Variants |
| financial | Money | Invoices, Payments, Cards |
| integrations | External | Webhooks, Triggers, Providers |
| legal | Contracts | Contracts |
| marketing | Demand gen | Leads, Campaigns, Competitors |
| markets | Market data | Industries, Occupations, Tasks |
| product | Offerings | Products, Prices, Features, Offers |
| sales | Revenue | Deals, Quotes, Proposals |
| startup | Venture | Founders, CustomerSegments |
| success | Customers | Customers, Contacts, Subscriptions |
| tech | Technology | Technologies, Tools |
| tools | Agent tools | Browser, Computer |
| vibecode | Code gen | Sessions, Generations |
| web | Websites | Sites, Pages, Blogs, Docs |
| work | Execution | Tasks, Projects, Workflows, Agents |

## Collection Structure

```typescript
import type { CollectionConfig } from 'payload'

export const Things: CollectionConfig = {
  slug: 'things',

  // Admin UI
  admin: {
    useAsTitle: 'name',
    group: 'Domain',
    defaultColumns: ['name', 'status', 'createdAt'],
  },

  // Access control
  access: {
    read: () => true,
    create: isAuthenticated,
    update: isOwnerOrAdmin,
    delete: isAdmin,
  },

  // Fields
  fields: [
    // ...
  ],

  // Hooks
  hooks: {
    beforeChange: [],
    afterChange: [],
  },
}
```

## Field Patterns

### Required Fields (every collection)

```typescript
fields: [
  {
    name: 'name',
    type: 'text',
    required: true,
  },
]
```

### Standard Optional Fields

```typescript
{
  name: 'description',
  type: 'textarea',
},
{
  name: 'status',
  type: 'select',
  defaultValue: 'draft',
  options: ['draft', 'active', 'archived'],
},
```

### Relationship Patterns

```typescript
// Belongs to (many-to-one)
{
  name: 'business',
  type: 'relationship',
  relationTo: 'businesses',
  required: true,
},

// Has many (one-to-many via reverse)
// No field needed - query from child

// Many-to-many
{
  name: 'industries',
  type: 'relationship',
  relationTo: 'industries',
  hasMany: true,
},

// Polymorphic
{
  name: 'actor',
  type: 'relationship',
  relationTo: ['agents', 'humans', 'serviceAccounts'],
},
```

### MDX Content Field

```typescript
{
  name: 'content',
  type: 'richText',
  editor: lexicalEditor({
    features: ({ defaultFeatures }) => [
      ...defaultFeatures,
      // MDX support
    ],
  }),
},
```

## Naming Conventions

### Collection Slugs
- Plural, lowercase, hyphenated
- `customer-segments`, `journal-entries`

### Field Names
- camelCase
- `firstName`, `createdAt`, `isActive`

### Consistent Vocabulary

| Use | Don't Use |
|-----|-----------|
| `name` | `title`, `label`, `heading` |
| `description` | `subtitle`, `summary`, `body` |
| `status` | `state`, `phase` |
| `isActive` | `active`, `enabled` |
| `createdAt` | `created`, `dateCreated` |

## Access Control Patterns

```typescript
// Public read
access: {
  read: () => true,
}

// Authenticated only
access: {
  read: isAuthenticated,
  create: isAuthenticated,
}

// Owner or admin
access: {
  read: isOwnerOrAdmin,
  update: isOwnerOrAdmin,
  delete: isAdmin,
}

// Org-scoped
access: {
  read: belongsToOrg,
  create: belongsToOrg,
}
```

## Hook Patterns

### Auto-populate fields

```typescript
hooks: {
  beforeChange: [
    ({ data, req }) => {
      if (!data.createdBy) {
        data.createdBy = req.user?.id
      }
      return data
    },
  ],
}
```

### Cascade updates

```typescript
hooks: {
  afterChange: [
    async ({ doc, req }) => {
      // Update related records
      await req.payload.update({
        collection: 'related',
        where: { parent: { equals: doc.id } },
        data: { parentName: doc.name },
      })
    },
  ],
}
```

### Sync to external systems

```typescript
hooks: {
  afterChange: [
    async ({ doc, operation }) => {
      if (operation === 'create') {
        await stripe.customers.create({ ... })
      }
    },
  ],
}
```

## mdxdb Integration

Collections sync bidirectionally with .mdx files via mdxdb:

```
.mdx file (Business-as-Code)
       ↕ mdxdb sync
Payload Collection (runtime)
       ↕ mdxdb query
ClickHouse (analytics)
```

### MDXLD Frontmatter

```mdx
---
$type: Product
$id: https://acme.com/products/widget
name: Widget Pro
price: 99
---

# {name}

Product description here...
```

## Collection → Noun → Component

Every collection maps to:

1. **Noun type** in schema.org.ai
2. **TypeScript interface** in payload-types.ts
3. **Zod schema** for validation
4. **mdxui component** for rendering

```typescript
// Collection
export const Products: CollectionConfig = { ... }

// → Generates TypeScript
interface Product {
  id: string
  name: string
  price: number
}

// → Has Zod schema
const ProductSchema = z.object({ ... })

// → Renders via mdxui
<ProductCard {...product} />
<ProductRow {...product} />
<ProductPanel {...product} />
```

## Creating New Collections

1. Create file in appropriate domain: `collections/{domain}/{Name}.ts`
2. Follow field patterns above
3. Add to domain index: `collections/{domain}/index.ts`
4. Add to main index: `collections/index.ts`
5. Run `pnpm generate:types` to update payload-types.ts
6. Create corresponding mdxui renderer if needed

## Anti-Patterns

**DON'T:**
- Create duplicate fields across collections (normalize)
- Use inconsistent naming (follow vocabulary table)
- Skip access control (security first)
- Create deeply nested structures (flatten with relationships)

**DO:**
- Keep collections focused (single responsibility)
- Use relationships over embedding
- Add hooks for derived data
- Document with JSDoc comments

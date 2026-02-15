---
name: collection
description: Generate a new Momentum CMS collection with fields, access control, and hooks
argument-hint: <collection-name>
---

# Generate Momentum CMS Collection

Create a new collection file following project conventions.

## Arguments
- `$ARGUMENTS` - Collection name (e.g., "posts", "products", "users")

## Steps

1. Create the collection file at `collections/<name>.collection.ts`

2. Use this template:
```typescript
import {
  defineCollection,
  text,
  richText,
  number,
  date,
  checkbox,
  select,
  relationship,
} from '@momentum-cms/core';

export const <PascalName> = defineCollection({
  slug: '<kebab-name>',

  admin: {
    useAsTitle: 'title', // or 'name' - the field to display as title
    defaultColumns: ['title', 'createdAt'],
    group: 'Content', // Admin sidebar group
  },

  access: {
    read: () => true,
    create: ({ req }) => !!req.user,
    update: ({ req }) => req.user?.role === 'admin',
    delete: ({ req }) => req.user?.role === 'admin',
  },

  hooks: {
    beforeChange: [],
    afterChange: [],
  },

  fields: [
    text('title', { required: true }),
    // Add more fields as needed
  ],
});
```

3. Export from `collections/index.ts`:
```typescript
export { <PascalName> } from './<name>.collection';
```

4. Remind user to run schema generation:
```bash
nx run db-drizzle:generate-schema
npx drizzle-kit generate
```

## Field Types Available
- `text(name, options)` - Short text
- `richText(name, options)` - Rich text editor
- `number(name, options)` - Numeric value
- `date(name, options)` - Date/datetime
- `checkbox(name, options)` - Boolean
- `select(name, { options: [...] })` - Dropdown
- `relationship(name, { collection: () => Ref })` - Reference to another collection
- `array(name, { fields: [...] })` - Array of objects
- `group(name, { fields: [...] })` - Nested object

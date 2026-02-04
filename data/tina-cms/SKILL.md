---
name: tina-cms
description: Tina CMS configuration with GitHub backend. Use when setting up or configuring Tina CMS.
---

# Tina CMS Skill

## Installation

```bash
npm install tinacms @tinacms/cli
```

## GitHub Backend Configuration

**File: `tina/config.ts`**

```typescript
import { defineConfig } from 'tinacms';

export default defineConfig({
  branch: process.env.GITHUB_BRANCH || 'main',
  clientId: process.env.TINA_CLIENT_ID,
  token: process.env.TINA_TOKEN,

  build: {
    outputFolder: 'admin',
    publicFolder: 'public',
  },

  media: {
    tina: {
      mediaRoot: 'uploads',
      publicFolder: 'public',
    },
  },

  schema: {
    collections: [
      // Define collections here
    ],
  },
});
```

## Schema Pattern

```typescript
{
  name: 'blog',
  label: 'Blog Posts',
  path: 'src/content/blog',
  format: 'mdx',
  fields: [
    {
      type: 'string',
      name: 'title',
      label: 'Title',
      isTitle: true,
      required: true,
    },
    {
      type: 'rich-text',
      name: 'body',
      label: 'Body',
      isBody: true,
    },
  ],
}
```

## Critical Requirements

- Use GitHub backend (not local)
- Store media in `/public/uploads/`
- Admin accessible at `/admin`
- Schemas must match Astro content collections

## Environment Variables

```bash
GITHUB_OWNER=username
GITHUB_REPO=repo-name
GITHUB_BRANCH=main
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx
```

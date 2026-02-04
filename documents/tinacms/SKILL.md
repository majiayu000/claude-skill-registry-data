---
name: tinacms
description: |
  Build content-heavy sites with Git-backed TinaCMS. Provides visual editing and content management for blogs, documentation, and marketing sites with non-technical editors.

  Use when implementing Next.js, Vite+React, or Astro CMS setups, self-hosting on Cloudflare Workers, or troubleshooting ESbuild compilation errors, module resolution issues, or Docker binding problems.
allowed-tools: ['Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep']
---

# TinaCMS

Git-backed headless CMS with visual editing for content-heavy sites.

**Last Updated**: 2025-11-28
**Versions**: tinacms@2.10.0, @tinacms/cli@1.12.5

---

## Quick Start

```bash
# Initialize TinaCMS
npx @tinacms/cli@latest init

# Update package.json scripts
{
  "dev": "tinacms dev -c \"next dev\"",
  "build": "tinacms build && next build"
}

# Set environment variables
NEXT_PUBLIC_TINA_CLIENT_ID=your_client_id
TINA_TOKEN=your_read_only_token

# Start dev server
npm run dev

# Access admin interface
http://localhost:3000/admin/index.html
```

---

## Next.js Integration

**useTina Hook** (enables visual editing):
```tsx
import { useTina } from 'tinacms/dist/react'
import { client } from '../../tina/__generated__/client'

export default function BlogPost(props) {
  const { data } = useTina({
    query: props.query,
    variables: props.variables,
    data: props.data
  })

  return <article><h1>{data.post.title}</h1></article>
}

export async function getStaticProps({ params }) {
  const response = await client.queries.post({
    relativePath: `${params.slug}.md`
  })

  return {
    props: {
      data: response.data,
      query: response.query,
      variables: response.variables
    }
  }
}
```

**App Router**: Admin route at `app/admin/[[...index]]/page.tsx`
**Pages Router**: Admin route at `pages/admin/[[...index]].tsx`

---

## Schema Configuration

**tina/config.ts** structure:
```typescript
import { defineConfig } from 'tinacms'

export default defineConfig({
  branch: process.env.GITHUB_BRANCH || 'main',
  clientId: process.env.NEXT_PUBLIC_TINA_CLIENT_ID,
  token: process.env.TINA_TOKEN,
  build: {
    outputFolder: 'admin',
    publicFolder: 'public',
  },
  schema: {
    collections: [/* ... */],
  },
})
```

**Collection Example** (Blog Post):
```typescript
{
  name: 'post',           // Alphanumeric + underscores only
  label: 'Blog Posts',
  path: 'content/posts',  // No trailing slash
  format: 'mdx',
  fields: [
    {
      type: 'string',
      name: 'title',
      label: 'Title',
      isTitle: true,
      required: true
    },
    {
      type: 'rich-text',
      name: 'body',
      label: 'Body',
      isBody: true
    }
  ]
}
```

**Field Types**: `string`, `rich-text`, `number`, `datetime`, `boolean`, `image`, `reference`, `object`

---

## Common Errors & Solutions

### 1. ❌ ESbuild Compilation Errors

**Error Message:**
```
ERROR: Schema Not Successfully Built
ERROR: Config Not Successfully Executed
```

**Causes:**
- Importing code with custom loaders (webpack, babel plugins, esbuild loaders)
- Importing frontend-only code (uses `window`, DOM APIs, React hooks)
- Importing entire component libraries instead of specific modules

**Solution:**

Import only what you need:
```typescript
// ❌ Bad - Imports entire component directory
import { HeroComponent } from '../components/'

// ✅ Good - Import specific file
import { HeroComponent } from '../components/blocks/hero'
```

**Prevention Tips:**
- Keep `tina/config.ts` imports minimal
- Only import type definitions and simple utilities
- Avoid importing UI components directly
- Create separate `.schema.ts` files if needed

**Reference**: See `references/common-errors.md#esbuild`

---

### 2. ❌ Module Resolution: "Could not resolve 'tinacms'"

**Error Message:**
```
Error: Could not resolve "tinacms"
```

**Causes:**
- Corrupted or incomplete installation
- Version mismatch between dependencies
- Missing peer dependencies

**Solution:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Or with pnpm
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Or with yarn
rm -rf node_modules yarn.lock
yarn install
```

**Prevention:**
- Use lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`)
- Don't use `--no-optional` or `--omit=optional` flags
- Ensure `react` and `react-dom` are installed (even for non-React frameworks)

---

### 3. ❌ Field Naming Constraints

**Error Message:**
```
Field name contains invalid characters
```

**Cause:**
- TinaCMS field names can only contain: letters, numbers, underscores
- Hyphens, spaces, special characters are NOT allowed

**Solution:**
```typescript
// ❌ Bad - Uses hyphens
{
  name: 'hero-image',
  label: 'Hero Image',
  type: 'image'
}

// ❌ Bad - Uses spaces
{
  name: 'hero image',
  label: 'Hero Image',
  type: 'image'
}

// ✅ Good - Uses underscores
{
  name: 'hero_image',
  label: 'Hero Image',
  type: 'image'
}

// ✅ Good - CamelCase also works
{
  name: 'heroImage',
  label: 'Hero Image',
  type: 'image'
}
```

**Note**: This is a **breaking change** from Forestry.io migration

---

### 4. ❌ Docker Binding Issues

**Error:**
- TinaCMS admin not accessible from outside Docker container

**Cause:**
- TinaCMS binds to `127.0.0.1` (localhost only) by default
- Docker containers need `0.0.0.0` binding to accept external connections

**Solution:**
```bash
# Ensure framework dev server listens on all interfaces
tinacms dev -c "next dev --hostname 0.0.0.0"
tinacms dev -c "vite --host 0.0.0.0"
tinacms dev -c "astro dev --host 0.0.0.0"
```

**Docker Compose Example:**
```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    command: npm run dev  # Which runs: tinacms dev -c "next dev --hostname 0.0.0.0"
```

---

### 5. ❌ Missing `_template` Key Error

**Error Message:**
```
GetCollection failed: Unable to fetch
template name was not provided
```

**Cause:**
- Collection uses `templates` array (multiple schemas)
- Document missing `_template` field in frontmatter
- Migrating from `templates` to `fields` and documents not updated

**Solution:**

**Option 1: Use `fields` instead (recommended for single template)**
```typescript
{
  name: 'post',
  path: 'content/posts',
  fields: [/* ... */]  // No _template needed
}
```

**Option 2: Ensure `_template` exists in frontmatter**
```yaml
---
_template: article  # ← Required when using templates array
title: My Post
---
```

**Migration Script** (if converting from templates to fields):
```bash
# Remove _template from all files in content/posts/
find content/posts -name "*.md" -exec sed -i '/_template:/d' {} +
```

---

### 6. ❌ Path Mismatch Issues

**Error:**
- Files not appearing in Tina admin
- "File not found" errors when saving
- GraphQL queries return empty results

**Cause:**
- `path` in collection config doesn't match actual file directory
- Relative vs absolute path confusion
- Trailing slash issues

**Solution:**
```typescript
// Files located at: content/posts/hello.md

// ✅ Correct
{
  name: 'post',
  path: 'content/posts',  // Matches file location
  fields: [/* ... */]
}

// ❌ Wrong - Missing 'content/'
{
  name: 'post',
  path: 'posts',  // Files won't be found
  fields: [/* ... */]
}

// ❌ Wrong - Trailing slash
{
  name: 'post',
  path: 'content/posts/',  // May cause issues
  fields: [/* ... */]
}
```

**Debugging:**
1. Run `npx @tinacms/cli@latest audit` to check paths
2. Verify files exist in specified directory
3. Check file extensions match `format` field

---

### 7. ❌ Build Script Ordering Problems

**Error Message:**
```
ERROR: Cannot find module '../tina/__generated__/client'
ERROR: Property 'queries' does not exist on type '{}'
```

**Cause:**
- Framework build running before `tinacms build`
- Tina types not generated before TypeScript compilation
- CI/CD pipeline incorrect order

**Solution:**
```json
{
  "scripts": {
    "build": "tinacms build && next build"  // ✅ Tina FIRST
    // NOT: "build": "next build && tinacms build"  // ❌ Wrong order
  }
}
```

**CI/CD Example (GitHub Actions):**
```yaml
- name: Build
  run: |
    npx @tinacms/cli@latest build  # Generate types first
    npm run build                   # Then build framework
```

**Why This Matters:**
- `tinacms build` generates TypeScript types in `tina/__generated__/`
- Framework build needs these types to compile successfully
- Running in wrong order causes type errors

---

### 8. ❌ Failed Loading TinaCMS Assets

**Error Message:**
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
http://localhost:4001/...
```

**Causes:**
- Pushed development `admin/index.html` to production (loads assets from localhost)
- Site served on subdirectory but `basePath` not configured

**Solution:**

**For Production Deploys:**
```json
{
  "scripts": {
    "build": "tinacms build && next build"  // ✅ Always build
    // NOT: "build": "tinacms dev"          // ❌ Never dev in production
  }
}
```

**For Subdirectory Deployments:**
```typescript
// tina/config.ts
export default defineConfig({
  build: {
    outputFolder: 'admin',
    publicFolder: 'public',
    basePath: 'your-subdirectory'  // ← Set if site not at domain root
  }
})
```

**CI/CD Fix:**
```yaml
# GitHub Actions / Vercel / Netlify
- run: npx @tinacms/cli@latest build  # Always use build, not dev
```

---

### 9. ❌ Reference Field 503 Service Unavailable

**Error:**
- Reference field dropdown times out with 503 error
- Admin interface becomes unresponsive when loading reference field

**Cause:**
- Too many items in referenced collection (100s or 1000s)
- No pagination support for reference fields currently

**Solutions:**

**Option 1: Split collections**
```typescript
// Instead of one huge "authors" collection
// Split by active status or alphabetically

{
  name: 'active_author',
  label: 'Active Authors',
  path: 'content/authors/active',
  fields: [/* ... */]
}

{
  name: 'archived_author',
  label: 'Archived Authors',
  path: 'content/authors/archived',
  fields: [/* ... */]
}
```

**Option 2: Use string field with validation**
```typescript
// Instead of reference
{
  type: 'string',
  name: 'authorId',
  label: 'Author ID',
  ui: {
    component: 'select',
    options: ['author-1', 'author-2', 'author-3']  // Curated list
  }
}
```

**Option 3: Custom field component** (advanced)
- Implement pagination in custom component
- See TinaCMS docs: https://tina.io/docs/extending-tina/custom-field-components/

---

## Deployment Options

### TinaCloud (Managed) - Recommended

**Setup:**
1. Sign up at https://app.tina.io
2. Get Client ID and Read Only Token
3. Set env vars: `NEXT_PUBLIC_TINA_CLIENT_ID`, `TINA_TOKEN`
4. Deploy to Vercel/Netlify/Cloudflare Pages

**Pros**: Zero config, free tier (10k requests/month)

---

### Self-Hosted on Cloudflare Workers

```bash
npm install @tinacms/datalayer tinacms-authjs
npx @tinacms/cli@latest init backend
```

**workers/src/index.ts**:
```typescript
import { TinaNodeBackend, LocalBackendAuthProvider } from '@tinacms/datalayer'
import { AuthJsBackendAuthProvider, TinaAuthJSOptions } from 'tinacms-authjs'
import databaseClient from '../../tina/__generated__/databaseClient'

const isLocal = process.env.TINA_PUBLIC_IS_LOCAL === 'true'

export default {
  async fetch(request: Request, env: Env) {
    const handler = TinaNodeBackend({
      authProvider: isLocal
        ? LocalBackendAuthProvider()
        : AuthJsBackendAuthProvider({
            authOptions: TinaAuthJSOptions({
              databaseClient,
              secret: env.NEXTAUTH_SECRET,
            }),
          }),
      databaseClient,
    })
    return handler(request)
  }
}
```

**Pros**: Full control, 100k requests/day free tier, global edge network

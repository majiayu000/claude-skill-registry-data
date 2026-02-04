---
name: build-and-deploy
description: Build and deploy this Next.js portfolio application. Use when building, deploying, or preparing the project for production.
---

# Build and Deploy Magic Portfolio

> **CRITICAL: For Vercel, use `vercel build --prod` then `vercel deploy --prebuilt --prod`.**

## Workflow

### 1. Install Dependencies
```bash
npm install
```

### 2. Build
```bash
npm run build
```

### 3. Deploy

**Vercel (Recommended):**
```bash
vercel pull --yes -t $VERCEL_TOKEN
vercel build --prod -t $VERCEL_TOKEN
vercel deploy --prebuilt --prod --yes -t $VERCEL_TOKEN
```

**Netlify:**
```bash
netlify deploy --prod --dir=.next
```

## Tech Stack

- **Framework**: Next.js 16
- **UI**: Once UI + React 19
- **Styling**: Sass
- **Content**: MDX for blog posts and projects
- **Language**: TypeScript

## Important Notes

- Requires Node.js v18.17+
- Configuration files:
  - `src/resources/once-ui.config.js` - Theme and UI settings
  - `src/resources/content.js` - Site content
- Blog posts go in `src/app/blog/posts/`
- Projects go in `src/app/work/projects/`

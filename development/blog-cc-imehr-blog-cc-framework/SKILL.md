---
name: blog-cc
description: Use when managing blog-cc static sites - content creation, deployment, themes, courses. Conversational content management with AI generation, validation, and GitHub Pages deployment.
---

# Blog-CC Content Management

## ⚠️ VERIFICATION REQUIRED

**BEFORE using this skill, verify this is a blog-cc project:**

1. Check for `content/` directory with `collections/`, `pages/`, or `courses/` subdirectories
2. Check for `next.config.js` with `basePath` config OR `CONTENT-GUIDE.md`
3. Check for theme system: `lib/themes/` directory
4. **When uncertain: ASK the user** "Is this a blog-cc project?"

**NOT blog-cc if:**
- Hugo, Jekyll, Gatsby, or other SSG (different file structure)
- WordPress or database-backed CMS
- Plain HTML site without Next.js
- Custom Next.js site without blog-cc content structure

## Overview

Blog-cc is a Next.js-based static site generator for AI learning content. This skill provides conversational content management with AI-powered generation, course building, and GitHub Pages deployment.

**Core principle:** Use TypeScript CLI utilities for operations. Validate before deploying. Git-tag deployments. Preview before publishing.

## When to Use

**ONLY after verifying blog-cc project**, use this skill when you see:
- "Add video [URL]" or "Add content"
- "Create course about [topic]"
- "Deploy site" or "Publish to GitHub Pages"
- "Switch theme to [name]"
- "Validate content"
- "Preview changes"

## When NOT to Use

**NEVER use this skill for:**
- Hugo, Jekyll, Gatsby sites (different architecture)
- WordPress or database CMS (not static site)
- Generic Next.js without blog-cc structure
- **When project type is unclear** - ASK THE USER FIRST

**If uncertain, verify first:**
```bash
# Check for blog-cc structure
ls content/collections content/pages CONTENT-GUIDE.md
# If missing → NOT blog-cc → DON'T use this skill
```

## Quick Reference

| User Intent | Action | CLI Function |
|-------------|--------|-------------|
| "Add video [URL]" | Extract metadata → generate tags → create file | `addVideo()` |
| "Create course [topic]" | AI outline → scaffold structure | Coming soon |
| "Deploy site" | Validate → build → tag → push | Coming soon |
| "Switch theme [name]" | Update .env → preview → commit | Coming soon |
| "Preview changes" | Build → serve port 4567 | `./start.sh` |
| "Validate content" | Schema + links + structure check | `validateContent()` |

## Essential Workflows

### Content Creation (AI-Powered)

**When user provides URL:**

1. Verify project with `isBlogCCProject()`
2. Call `addVideo()` with URL only
3. AI extracts YouTube metadata and generates tags/description
4. Show preview to user
5. User confirms or edits
6. Create file: `content/collections/[type]/[slug].md`
7. Auto-commit: `feat: add video 'Title'`
8. Offer preview: "Run `./start.sh` to see changes"

**Three modes:**
- URL only: AI extracts all metadata
- Full args: Manual specification
- Interactive: Prompts for each field

### Content Validation

**Before deployment, always validate:**

```typescript
import { validateContent } from './lib/cli/validation/content-validator'

const result = await validateContent(projectRoot)
// Checks:
// - Required fields per collection type (videos: title, author, url)
// - Duplicate slugs
// - Date formats (YYYY-MM-DD)
// - Course structure (course.md, modules/)
```

**Reports:**
- Errors (blocking): Missing required fields, invalid dates, duplicates
- Warnings (non-blocking): Broken links, missing assets
- Files checked count

**Never deploy with validation errors.**

### Collection Types & Schemas

**9 supported collection types:**

| Collection | Required Fields | Optional |
|------------|----------------|----------|
| videos | title, author, url | duration, description, tags |
| podcasts | title, host, url | episode, duration, description |
| people | name, role, url | bio, tags |
| products | name, description, url | price, tags |
| courses | title, provider, url | duration, level, tags |
| tutorials | title, author, url | duration, difficulty, tags |
| books | title, author | publisher, isbn, url |
| repos | title, owner, url | stars, language, tags |
| tweets | author, content, url | date, tags |

**File location**: `content/collections/[collection-type]/[slug].md`

### Project Structure

```
blog-cc-project/
├── content/
│   ├── collections/
│   │   ├── videos/
│   │   ├── tutorials/
│   │   ├── courses/
│   │   └── ... (9 types)
│   ├── pages/           # Blog posts
│   ├── courses/         # Multi-module courses
│   │   └── [slug]/
│   │       ├── course.md
│   │       └── modules/
│   └── home.md
├── lib/
│   └── themes/          # 9 themes
├── .env                 # THEME=moss
├── .env.production      # BASE_PATH=/repo-name
├── next.config.js
└── CONTENT-GUIDE.md
```

## Common Patterns

```typescript
// Add content from URL (AI extracts metadata)
import { addVideo } from './lib/cli/content/add-video'
await addVideo(projectRoot, { url: 'https://youtube.com/...' })

// Validate before deploy
import { validateContent } from './lib/cli/validation/content-validator'
const result = await validateContent(projectRoot)
if (!result.valid) { console.log(result.errors); process.exit(1) }

// Load project config
import { loadBlogCCConfig } from './lib/cli/utils/config-loader'
const config = await loadBlogCCConfig(projectRoot)
```

## Common Mistakes

**1. Not verifying blog-cc project** - always check structure first
**2. Skipping validation** - always validate before deploy
**3. Hardcoding paths** - use `config.contentDir` from config loader
**4. Creating invalid slugs** - slugify: lowercase, replace spaces with dashes
**5. Missing frontmatter fields** - check schema for required fields per collection
**6. Not auto-committing** - use `autoCommit()` from git-helper
**7. Forgetting to offer preview** - always suggest `./start.sh` after changes

## Available CLI Utilities

**Utils**: yaml-handler, project-detector, git-helper, config-loader
**Content**: add-video, ai-generator
**Validation**: content-validator

See `lib/cli/` for TypeScript implementations.

## Best Practices

- **Always verify project** before operations
- **Use AI extraction** when URL provided
- **Show preview** before creating files
- **Validate before deploy** (no exceptions)
- **Auto-commit changes** with descriptive messages
- **Offer next steps** after operations
- **Check for existing files** before creating
- **Use consistent slugs** (lowercase-with-dashes)

## Themes

**9 themes**: iris (default), moss, crimson, ocean, amber, slate, violet, forest, sky

**Switch**: Update `.env` THEME → preview → commit

## Deployment (Coming Soon)

**4-layer safety system:**
1. Content validation (schema, links, structure)
2. Pre-deploy checks (build success, git status)
3. Preview (serve locally before push)
4. Rollback (git tags for quick revert)

**Deployment flow:**
```bash
# 1. Validate
validateContent()

# 2. Build
npm run build

# 3. Tag
git tag deploy/site-name/2025-11-03-14-30-00

# 4. Push
git push origin main --tags

# 5. GitHub Pages builds automatically
```

## Additional Resources

- **Framework Repo:** https://github.com/imehr/blog-cc-framework
- **Template Repo:** https://github.com/imehr/blog-cc
- **CLI docs:** TypeScript comments in `lib/cli/`

## When Deployment Fails

**CRITICAL: Diagnose before acting. Never guess under pressure.**

1. `validateContent()` - check for validation errors FIRST
2. `npm run build` - verify build succeeds locally
3. Check GitHub Actions logs in repo → Actions tab
4. Verify `.env.production` has `BASE_PATH=/repo-name`
5. Check GitHub Pages settings: Settings → Pages → Source: gh-pages branch

**For content issues: validate → fix → rebuild → redeploy**
**For build issues: check logs → fix errors → test locally → redeploy**

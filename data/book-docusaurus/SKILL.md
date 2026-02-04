---
name: book-docusaurus
description: Scaffold, structure, and deploy the Physical AI textbook in Docusaurus with book-aware content and RAG-ready exports. Use when creating or updating the Docusaurus site, adding chapters, configuring sidebar, or deploying to GitHub Pages/Vercel.
---

# Book Docusaurus Skill

## Instructions

1. **Scaffold the site**
   - Ensure Node >=18 is installed
   - Run `npx create-docusaurus@latest physical-ai-book classic` in project root or `/docs`
   - Configure `docusaurus.config.js` with site metadata, GitHub Pages URLs, i18n (en default)

2. **Structure content**
   - Build `sidebars.js` for Quarter overview, Modules 1-4, Capstone, Assessments, Hardware kits, Cloud option
   - Create MDX stubs per module/week with learning outcomes and tasks
   - Add capstone outline

3. **Authoring affordances**
   - Add MDX components for callouts, checklists, hardware tables, code blocks
   - Enable search (Algolia DocSearch placeholder) and local search plugin for dev

4. **Deploy**
   - Add GitHub Actions workflow for GH Pages (`npm ci`, `npm run build`, `npm run deploy`)
   - Document Vercel deploy steps (import repo, build command `npm run build`, output `build`)

5. **RAG-readiness**
   - Enforce frontmatter fields: `title`, `description`, `module`, `week`, `tags`
   - Keep headings semantic (h2 for weeks, h3 for sections)
   - Avoid heavy client-side rendering for core text
   - Export ingestion guidance: markdown path glob, ignore build/static

## Examples

```bash
# Create new chapter
mkdir -p docs/module-1/week-1
cat > docs/module-1/week-1/intro.mdx << 'EOF'
---
title: Introduction to Physical AI
description: Overview of embodied intelligence and humanoid robotics
module: 1
week: 1
tags: [physical-ai, robotics, introduction]
---

# Introduction to Physical AI

Content here...
EOF
```

```bash
# Build and test locally
npm run build
npm run serve
```

## Definition of Done

- `npm run build` passes; site renders outline and sample content
- Sidebar matches course hierarchy; links valid
- GH Pages workflow present; deploy instructions written
- Content annotated with frontmatter and semantic headings suitable for chunking

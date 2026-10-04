---
name: github-wiki-editing
description: Edit GitHub Wiki pages programmatically via git clone, edit, and push
triggers:
  - wiki edit
  - update wiki
  - wiki page
  - GitHub wiki
---

# GitHub Wiki Editing

GitHub Wiki is a separate git repo at `https://github.com/OWNER/REPO.wiki.git`.

## Workflow

1. Clone wiki repo:
   ```bash
   cd /tmp && rm -rf REPO.wiki && git clone https://github.com/OWNER/REPO.wiki.git
   ```

2. Edit markdown files (Home.md is the main page)

3. Commit and push:
   ```bash
   cd /tmp/REPO.wiki
   git add File.md
   git commit -m "feat: description"
   git push origin master
   ```

## Key Points

- Wiki pages are separate from the main repo
- Use GitHub-flavored Markdown with HTML for rich formatting
- Internal wiki links: `[Page Name](Page-Name)` (spaces become hyphens)
- Supports badges, tables, images, code blocks
- Changes are immediate (no PR needed unless branch protection enabled)

## Design Elements for Professional Wikis

- Animated headers: `https://readme-typing-svg.demolab.com?...`
- Status badges: `https://img.shields.io/...`
- Visitor badges: `https://api.visitorbadge.io/...`
- Tech icons: `https://cdn.jsdelivr.net/gh/devicons/devicon/icons/...`
- ASCII art diagrams for architecture
- Tables with emoji for visual appeal

## Verification

After push, check `https://github.com/OWNER/REPO/wiki` to verify changes.

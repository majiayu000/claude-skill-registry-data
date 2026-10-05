---
name: site-deploy
description: Build, preview, and deploy the VisaJobs.xyz Eleventy site. Use when the user asks to build, deploy, push, preview the site, run the dev server, or fix build errors.
---

# Build & Deploy VisaJobs.xyz

## Tech Stack

- **Generator**: Eleventy 3.x (config: `.eleventy.js`)
- **Styling**: Tailwind CSS 3.4 (config: `tailwind.config.js`)
- **Templates**: Nunjucks (`.njk`) in `src/`
- **Search**: Pagefind (post-build indexing)
- **Hosting**: GitHub Pages (repo: `relocate-with-us/relocate-with-us.github.io`)
- **Domain**: visajobs.xyz (CNAME file)

## Project Structure

```
src/
├── _data/           # Global data (jobs.json, companies.json, site.json)
├── _includes/
│   ├── layouts/     # base.njk
│   └── partials/    # header, footer, newsletter
├── assets/
│   ├── css/input.css
│   └── js/main.js
├── index.njk        # Home page
├── visa-sponsored-jobs/  # Main job listing
├── relocation-jobs/      # Relocation-focused listing
├── blog/            # Markdown blog posts
├── resources/       # Country guides, tips
└── tools/           # Visa checker, salary calc, etc.
media/               # Company logos (passthrough copied)
favicon/             # Favicons
```

## Commands

### Install dependencies
```bash
npm install
```

### Development server
```bash
npx @11ty/eleventy --serve
```

### Production build
```bash
npx @11ty/eleventy
```

Build output: `_site/`

### Build Tailwind CSS
```bash
npx tailwindcss -i src/assets/css/input.css -o _site/assets/css/styles.css
```

### Run Pagefind indexing (after build)
```bash
npx pagefind --site _site
```

## Deploy (GitHub Pages)

The site auto-deploys on push to main via GitHub Pages.

```bash
git add -A
git commit -m "description of changes"
git push origin main
```

### Remote URL

Currently HTTPS. To switch to SSH (avoids token prompts):
```bash
git remote set-url origin git@github.com:relocate-with-us/relocate-with-us.github.io.git
```

## Key Config Notes

- `.eleventy.js` copies `src/_data/jobs.json` to `_site/db.json` after build (legacy compatibility)
- `src/_data/site.json` holds site metadata, social links, analytics IDs
- Google Analytics: `G-E6NMFQFHMZ`
- AdSense: `ca-pub-7578309605540082`
- Grow.me/Mediavine Journey script is in `base.njk` `<head>`

## Common Issues

| Issue | Fix |
|-------|-----|
| Styles missing | Run Tailwind build before/alongside Eleventy |
| Search broken | Run Pagefind after Eleventy build |
| db.json stale | Rebuild — it's auto-copied from jobs.json |
| Push needs token | Switch remote to SSH (see above) |

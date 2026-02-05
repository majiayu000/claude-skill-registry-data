---
name: hugo-builder
description: Build, serve, and deploy the Hugo static site. Use when building the site, testing locally, checking for errors, or deploying to GitHub Pages.
---

# Hugo Builder

Manage the Hugo static site build process, local development server, and deployment.

## Hugo Configuration

The site uses:
- Theme: PaperMod
- Language: Korean (ko-KR)
- Title: Novemberde's Blog
- Description: Logs for troubleshooting, dev-experience
- Author: BYUN Kyuhyun (AWS Serverless Hero)
- Deployment: GitHub Pages at https://novemberde.github.io/
- Branch: hugo
- Analytics: Google Analytics enabled (G-9SF4VDQ4N0)
- Comments: Disqus enabled (novemberde-github-io)

## Common Commands

### Build the Site
```bash
hugo
```
Builds the site to the `public/` directory. This compiles all markdown files, applies the theme, and generates static HTML.

**When to use:**
- Before deploying
- To check for build errors
- To verify the final output

### Serve Locally (Development)
```bash
hugo server -D
```
Starts a local development server with:
- Live reload on file changes
- Draft posts visible (-D flag)
- Usually available at http://localhost:1313

**When to use:**
- During content creation
- Testing theme changes
- Previewing before publishing

### Serve Without Drafts
```bash
hugo server
```
Serves only published content (excludes drafts).

**When to use:**
- Final preview before deployment
- Testing the production build locally

### Check Hugo Version
```bash
hugo version
```

### Clean Build
```bash
rm -rf public && hugo
```
Removes the public directory and rebuilds from scratch.

**When to use:**
- Troubleshooting build issues
- After theme updates
- When files seem out of sync

## Build Process

1. **Content Processing**: Markdown files in `content/` are converted to HTML
2. **Theme Application**: PaperMod theme templates are applied
3. **Asset Processing**: Images, CSS, JS are copied from `static/` and theme
4. **Output**: Final site generated in `public/` directory

## Deployment to GitHub Pages

This site uses GitHub Pages with the `hugo` branch. The deployment process:

1. Build the site: `hugo`
2. The `public/` directory contains the built site
3. Commit and push changes to the `hugo` branch
4. GitHub Pages automatically deploys from the configured branch/directory

## Troubleshooting

### Build Errors

**Problem**: Hugo can't find theme
```
Error: Unable to locate theme directory
```
**Solution**: Check if theme submodule is initialized:
```bash
git submodule update --init --recursive
```

**Problem**: Date parsing errors
```
Error: failed to parse date
```
**Solution**: Ensure dates are in ISO 8601 format: `YYYY-MM-DDTHH:MM:SS+00:00`

**Problem**: Content not showing
**Solution**:
- Check if the date is in the future (Hugo skips future posts by default)
- Verify frontmatter is correct
- Ensure file is in correct directory structure

### Server Issues

**Problem**: Port already in use
```
Error: listen tcp :1313: bind: address already in use
```
**Solution**:
```bash
# Kill existing Hugo server
pkill hugo
# Or use a different port
hugo server -p 1314
```

## File Structure

```
novemberde.github.io/
├── config.yml           # Hugo configuration
├── content/             # All content (posts, pages)
│   ├── post/           # Blog posts (YYYY/MM/DD structure)
│   └── about.md        # About page
├── static/             # Static assets (images, files)
├── themes/
│   └── PaperMod/       # Current theme
└── public/             # Built site (generated, not in git)
```

## Best Practices

1. **Always test locally** before deploying:
   ```bash
   hugo server
   ```

2. **Check build output** for warnings:
   ```bash
   hugo --verbose
   ```

3. **Clean builds** when in doubt:
   ```bash
   rm -rf public && hugo
   ```

4. **Verify links** after building:
   - Check internal links work
   - Verify images load correctly
   - Test navigation menu

## Configuration Reference

Key settings in `config.yml`:
- `baseURL`: Site URL (must match deployment URL: https://novemberde.github.io/)
- `languageCode`: Site language (ko-KR)
- `theme`: Theme name (PaperMod)
- `buildDrafts`: Include draft posts (false in production)
- `buildFuture`: Include future-dated posts (false in production)
- `buildExpired`: Include expired posts (false)
- `minify`: Minification settings for production
  - `disableXML`: true
  - `minifyOutput`: true
- `enableRobotsTXT`: Enable robots.txt generation (true)
- `googleAnalytics`: Analytics tracking ID
- `disqusShortname`: Disqus integration for comments

### Menu Configuration
The site has three main menu items:
1. Search (`/search`) - Weight: 1
2. Post (`/post/`) - Weight: 2
3. About (`/about`) - Weight: 3

### Markup Configuration
- `goldmark.renderer.unsafe`: true (allows raw HTML in markdown)
- `enableInlineShortcodes`: true
- `disablePathToLower`: true (preserves URL case)

## Common Workflows

### Creating and Testing a New Post
```bash
# 1. Create the post (manually or with blog-post-creator skill)
# 2. Start development server
hugo server -D
# 3. Edit and preview in browser
# 4. When ready, remove draft status and rebuild
hugo
```

### Deploying Updates
```bash
# 1. Clean build
rm -rf public && hugo
# 2. Commit changes
git add .
git commit -m "Your commit message"
# 3. Push to hugo branch
git push origin hugo
```

### Theme Updates
```bash
# Update theme submodule
cd themes/PaperMod
git pull origin master
cd ../..
git add themes/PaperMod
git commit -m "Update PaperMod theme"
```

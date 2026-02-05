---
name: content-manager
description: Edit, update, and manage existing blog posts. Use when modifying content, fixing typos, updating tags, or reorganizing posts.
---

# Content Manager

Manage and update existing blog posts on the Hugo static site. This skill helps you edit content, update metadata, fix errors, and reorganize posts effectively.

## When to Use This Skill

Use the content-manager skill when you need to:
- Edit or update existing blog post content
- Fix typos, grammar, or formatting issues
- Update post frontmatter (tags, title, date)
- Add or modify images and media
- Reorganize post structure
- Update outdated information
- Improve post readability

## Post Location Pattern

All posts are located in:
```
content/post/YYYY/MM/DD/Post-Title.md
```

## Common Tasks

### 1. Finding Posts

**By Date:**
```bash
ls -la content/post/2025/02/09/
```

**By Title/Keyword:**
```bash
find content/post -name "*keyword*"
```

**By Tag (search frontmatter):**
```bash
grep -r "tags:.*aws" content/post/
```

**Recent Posts:**
```bash
find content/post -name "*.md" -type f -mtime -30  # Last 30 days
```

### 2. Updating Frontmatter

Common frontmatter updates:

**Update Tags:**
```yaml
---
tags: ["old-tag", "new-tag", "additional-tag"]
---
```

**Update Title:**
```yaml
---
title: "Updated Title with Better Clarity"
---
```

**Update Date:**
```yaml
---
date: "2025-12-22T10:00:00+00:00"
---
```

### 3. Content Updates

**Guidelines for Content Editing:**
- Maintain consistent markdown formatting
- Preserve Korean language content encoding (UTF-8)
- Keep code blocks with proper language tags
- Update internal links if post URLs change
- Preserve image references in `/static/` directory

### 4. Image Management

Images are stored in:
```
static/images/
static/post/YYYY/MM/
```

**Adding Images to Posts:**
```markdown
![Alt text](/images/screenshot.png)
![Alt text](/post/2025/02/image.png)
```

**Best Practices:**
- Use descriptive filenames (no spaces, use hyphens)
- Optimize images before adding (compress for web)
- Keep images organized by date or topic
- Use relative paths from site root

### 5. Fixing Common Issues

**Issue: Broken Internal Links**
```markdown
# Check for broken internal links
hugo --verbose 2>&1 | grep "REF_NOT_FOUND"

# Fix by updating to correct path
[Link text](/post/2025/02/09/correct-post-name/)
```

**Issue: Date in Future (Post Not Showing)**
```yaml
# Hugo skips future-dated posts by default
# Update to current or past date:
date: "2025-12-22T10:00:00+00:00"
```

**Issue: Korean Encoding Problems**
```bash
# Verify file encoding
file -i content/post/2025/02/09/Post-Title.md

# Should show: charset=utf-8
# If not, convert to UTF-8
```

**Issue: Missing Required Frontmatter**
```yaml
# Ensure these are always present:
ShowBreadCrumbs: true
ShowReadingTime: true
ShowPostNavLinks: true
```

## Content Quality Checklist

Before finalizing updates, verify:

- [ ] Frontmatter is complete and correct
- [ ] All links work (internal and external)
- [ ] Images load and display correctly
- [ ] Code blocks have language tags
- [ ] Korean text displays properly (UTF-8)
- [ ] Tags are relevant and follow existing conventions
- [ ] Date format is correct (ISO 8601)
- [ ] Title is clear and descriptive
- [ ] Content structure uses proper markdown headers
- [ ] No trailing whitespace or formatting issues

## Bulk Operations

### Update Multiple Posts

**Add a New Tag to Multiple Posts:**
```bash
# Find all posts with "aws" tag
grep -l "tags:.*aws" content/post/**/*.md

# Then edit each file to add new tag
```

**Rename a Tag Across All Posts:**
```bash
# Find posts with old tag
grep -r "old-tag" content/post/

# Use find and sed for bulk replacement (be careful!)
find content/post -name "*.md" -exec sed -i 's/"old-tag"/"new-tag"/g' {} +
```

**Note:** Always test bulk operations on a few files first, and commit changes to git before running bulk updates.

## Post Migration

If you need to move a post to a different date:

1. Create new directory structure:
   ```bash
   mkdir -p content/post/YYYY/MM/DD/
   ```

2. Move the post:
   ```bash
   mv content/post/old/path/Post.md content/post/new/path/
   ```

3. Update frontmatter date to match new location

4. Update any internal links pointing to the old URL

5. Test with Hugo server:
   ```bash
   hugo server
   ```

## Working with Drafts

**Mark Post as Draft:**
```yaml
---
draft: true
---
```

**View Drafts Locally:**
```bash
hugo server -D
```

**Publish Draft (Remove Draft Status):**
```yaml
# Remove the draft line entirely, or set to false
draft: false
```

## SEO and Metadata Updates

**Improve Post Discoverability:**
- Update title for better keywords
- Add more specific tags
- Ensure description is clear
- Add alt text to images
- Use descriptive header hierarchy

**Example SEO-Friendly Frontmatter:**
```yaml
---
title: "Complete Guide to AWS Lambda: Best Practices for 2025"
tags: ["aws", "lambda", "serverless", "best-practices", "tutorial"]
date: "2025-12-22T10:00:00+00:00"
ShowBreadCrumbs: true
ShowReadingTime: true
ShowPostNavLinks: true
---
```

## Version Control Best Practices

Always use git when making content changes:

```bash
# Before making changes
git status
git diff

# After making changes
git add content/post/path/to/post.md
git commit -m "Update: brief description of changes"

# For bulk changes
git add -p  # Review each change interactively
```

## Testing Changes

Always test content updates locally:

```bash
# Start Hugo server
hugo server -D

# Check in browser at http://localhost:1313
# Verify:
# - Post displays correctly
# - Links work
# - Images load
# - Formatting is correct
# - Korean text displays properly
```

## Common Workflows

### Workflow: Fix Typo in Post
```bash
# 1. Find the post
find content/post -name "*post-title*"

# 2. Edit the file (use Read tool to view, Edit tool to fix)

# 3. Test locally
hugo server

# 4. Commit change
git add content/post/path/to/file.md
git commit -m "Fix typo in post title"
```

### Workflow: Update Outdated Content
```bash
# 1. Identify outdated posts (check old dates)
find content/post/2023 -name "*.md"

# 2. Review and update content

# 3. Update date in frontmatter (optional, or keep original)

# 4. Add note about update (optional)
# At top of post:
# > **Updated:** 2025-12-22 - Updated AWS pricing information

# 5. Test and commit
```

### Workflow: Reorganize Tags
```bash
# 1. List all existing tags
grep -rh "^tags:" content/post/ | sort | uniq

# 2. Identify tags to consolidate (e.g., "aws-lambda" → "lambda")

# 3. Update posts with new tags

# 4. Test that tag pages work
hugo server
# Visit: /tags/lambda/
```

## Tips and Tricks

1. **Use Git Grep for Faster Searches:**
   ```bash
   git grep "search term" content/post/
   ```

2. **Preview Changes Side-by-Side:**
   - Keep Hugo server running
   - Edit files
   - Refresh browser to see live updates

3. **Batch Edit with Your Editor:**
   - Use VS Code multi-cursor editing
   - Find and replace across files
   - Use regex for complex patterns

4. **Keep Backup Before Bulk Changes:**
   ```bash
   git checkout -b backup-before-tag-update
   # Make changes
   # If needed: git checkout main && git branch -D backup-before-tag-update
   ```

5. **Use Hugo's Built-in Validation:**
   ```bash
   hugo --verbose --debug
   ```

## Troubleshooting

**Problem: Changes Not Showing in Browser**
- Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R)
- Clear Hugo cache: `hugo --cleanDestinationDir`
- Restart Hugo server

**Problem: Korean Characters Broken**
- Verify file is UTF-8: `file -i filename.md`
- Check editor encoding settings
- Re-save file with UTF-8 encoding

**Problem: Post Date Changed, URL Broke**
- Hugo URLs don't include dates by default with PaperMod
- Check `config.yml` for `disablePathToLower: true`
- Test URL in browser after changes

**Problem: Tags Not Showing**
- Verify tag array format: `["tag1", "tag2"]`
- Check for typos in frontmatter
- Ensure proper YAML syntax

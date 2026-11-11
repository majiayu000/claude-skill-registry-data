---
description: Add internal and external links to the passed blog
model: haiku
---

# Goal
- Add internal and external links to the passed blog

# Workflow

## Collect Material

- Read the passed blog `<BLOG_FILE>` and the other blogs in `<BLOG_DIR>`
  `website/docs/blog/posts/*.md`, both published and drafts

## Add Internal Links
- Find parts of `<BLOG_FILE>` that can point to the other blogs, and add links
  between them

## Add External Links
- Find meaningful content in `<BLOG_FILE>` and add links that expand on it

## Format
- At the end, format the text with
  ```bash
  > website/format_blog.sh <BLOG_FILE>
  ```

# Constraints
- Follow the rules in `.claude/skills/blog.rules.md`
- Do not change the content of the blog, only add links

# Verification
- [ ] Confirm every added link resolves to an existing blog post or a valid
      external URL
- [ ] Confirm no existing wording was changed, only links added
- [ ] Confirm `website/format_blog.sh` ran without errors

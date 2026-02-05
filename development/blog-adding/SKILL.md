---
name: blog-adding
description: Add a new English blog post to this Docusaurus site from a staging Markdown file and assets.
---

# Add an English Blog Post

Use this skill when the user asks to add a new blog post

## Steps

1. Choose a blog folder name `YYYY-MM-DD-short-slug` (use the current date unless the user specifies one).
2. Create `blog/<folder>/index.md` with front matter:
   - `description`: short summary string
   - `slug`: URL slug without date
   - `image`: `/img/blogs/<folder>/cover.<ext>`
   - `tags`: array (e.g. `[MoonBit]`)
3. Add the H1 title and insert a cover image near the top: `![](./cover.<ext>)`.
4. Copy the staging Markdown content into the blog `index.md` after the front matter and cover.
5. Copy referenced images/assets into `blog/<folder>/` and ensure all `./image` links resolve.
6. Pick a cover image.
7. Copy the cover into `static/img/blogs/<folder>/cover.<ext>` for the meta image path.
8. Add a zh placeholder for English-only posts:
   - Create `i18n/zh/docusaurus-plugin-content-blog/<folder>/index.md` with:
     ```
     ---
     unlisted: true
     ---
     ```
9. Remove the staging folder if the user requests it.

## Notes

- No Docusaurus config changes are required; the blog plugin picks up new folders automatically.
- Keep file paths and front matter ASCII-safe; avoid introducing new non-ASCII unless required.

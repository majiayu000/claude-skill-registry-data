---
name: blog-write
description: Use when starting a new blog post for this site, or drafting post content — scaffolds data/blog/<year>/<slug>.mdx with schema-correct frontmatter and body conventions that survive MDX parsing. Trigger on "write a post", "new blog post", "draft a post about X", "start an essay".
---

# Write a blog post

Creates a post that passes `yarn validate` on the first try.

## File placement

```
data/blog/<year>/<slug>.mdx
```

- `<year>` matches the year in `date`.
- `<slug>` is **snake_case** — this is the established convention across all 6 published
  posts (`harness_engineering`, `why_context_matters_in_learning`, `beyond_the_hype`).
  Not kebab-case. The slug becomes the URL path.

## Frontmatter

Copy this exactly. Every key here is in the Velite schema (`velite.config.ts`).

```yaml
---
title: 'Title in Sentence Case: With a Subtitle if Useful'
date: '2026-08-01'
lastmod: '2026-08-01'
summary: 'A substantial paragraph, not a sentence. This is what shows in listings and in search results, so it should carry the actual argument rather than tease it.'
authors: ['default']
---
```

**Quote the dates.** Unquoted, YAML parses them as timestamps rather than strings.

**Do not add `tags:`.** It is not in the Velite schema and the tag UI was removed, so it is
silently stripped at build time. Existing posts still carry it; leave them alone rather than
cleaning them up as a side effect of writing a new post.

### Holding a post back

`draft: true` genuinely works — it excludes the post from listings, pagination, its own
route, the sitemap, and RSS via `publishedPosts()` in `lib/content-utils.ts`.

```yaml
draft: true
```

Add it while a post is in progress and remove it (or set `false`) to publish. Omitting the
key entirely means published — the schema defaults it to `false`.

### Optional keys

`images: ['/static/images/x.png']` · `layout:` · `bibliography:`
(`bibliography:` is wired up but unused — see `blog-research` for why citations are prose.)

## Body rules

These exist because MDX failures here are silent — the post disappears from the site with
no build error.

1. **Never leave a raw `<` in prose.** Escape as `\<`, wrap in backticks, or rewrite
   ("under 100ms" rather than "< 100ms").
2. **Percent-encode angle brackets in URLs and DOIs.** `<` → `%3C`, `>` → `%3E`.
3. **Only `Image` and `TOCInline` exist as components.** Any other capitalized tag is
   undefined at render time. Lowercase HTML (`<div>`, `<figure>`) passes through fine.
4. **No HTML comments.** `<!-- -->` is invalid MDX; use `{/* ... */}`.
5. **Code samples belong in fenced blocks** — the validator exempts them, so `<` inside a
   fence is safe.

## Structure

Follow the shape of the existing long-form essays: an H1-less opening (the `title`
frontmatter renders the heading), a short framing section, then `---` separated movements.
Reference lists go at the end as APA prose — see `blog-research`.

## Before finishing

```bash
yarn validate data/blog/<year>/<slug>.mdx
```

Fix every error. Do not hand the post back with known errors, and do not report it as done
until validation is clean — a post with a raw `<` looks fine in the editor and is invisible
on the site.

## Next step

Need sources? → `blog-research` first.
Ready to ship? → `blog-validate`, then `blog-publish`.

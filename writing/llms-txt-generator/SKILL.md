---
name: llms-txt-generator
description: Generate a spec-compliant llms.txt file for a website so AI assistants and answer engines can understand and cite it. Inventories the site's pages from the sitemap or project files, writes one-line descriptions per page, organises them into sections, and excludes private endpoints. Use when the user says "llms.txt", "make my site readable to AI", "AI search optimization file", or "GEO file".
---

# llms.txt Generator

You generate the `llms.txt` file: a markdown map of a website placed at the site root so LLMs and AI search engines can find the right pages and describe the site accurately. Think of it as a sitemap written for a reader with no patience: every page gets one honest line about what is on it.

## Step 1: Inventory the site

Work from the best available source, in this order:

1. **Local project**: if the current folder is the website's source, list the page files (HTML/PHP/markdown), read each page's `<title>` and meta description, and note its purpose.
2. **Live site**: otherwise fetch the site's `sitemap.xml` and read the listed pages. Respect `robots.txt`: anything disallowed there stays out of llms.txt too.

Always exclude: form handlers and endpoints (`send.php` and similar), admin pages, login pages, thank-you/confirmation pages, paginated duplicates, and anything the owner would not want quoted.

## Step 2: Write the file

Follow the llms.txt format:

```markdown
# Site Name

> One or two sentences saying what the site is and who it serves. This is
> the line an AI will repeat when describing the site, so make it accurate.

Optional short paragraph with context that does not fit the summary:
what the business does, where it operates, what makes it specific.

## Main sections

- [Page Title](https://example.com/page): one line on what this page contains
- [Another Page](https://example.com/other): same again

## Resources

- [Blog](https://example.com/blog): what the blog covers
- [Downloads](https://example.com/tools): what can be downloaded

## Optional

- [Secondary pages](https://example.com/archive): things an AI can skip unless asked
```

Writing rules for descriptions:

- Describe what is ON the page, not what the page hopes to achieve. "Pricing for the three service tiers" beats "Discover our flexible options".
- Absolute URLs throughout.
- The `## Optional` section is for pages an AI can skip when context is tight; use it for archives and secondary material.
- The summary blockquote is the highest-value line in the file. Draft it, then check: would the owner be happy if an AI quoted this verbatim as the description of their business?

## Step 3: Validate and place

1. Every URL in the file must resolve (check the live ones if the user agrees, otherwise check against the sitemap).
2. Place the file at the site root as `llms.txt` (same level as `robots.txt`).
3. If the site is large, offer a second `llms-full.txt` with expanded per-page content; for most small business sites one file is right.
4. Remind the user to regenerate when pages are added or removed; a stale llms.txt misdirects the AIs it was meant to help.

## Rules

- Never include pages blocked by robots.txt, behind logins, or that handle form data.
- Never inflate: no keyword stuffing, no claims that are not on the site. The file's only job is accuracy.
- Keep the whole file under roughly 100 lines for a typical site; it is a map, not a mirror.
- If the site already has an llms.txt, diff against it and report what changed rather than silently replacing.

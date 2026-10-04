---
name: blog-validate
description: Use when checking a blog post in data/blog before committing, publishing, or after any edit to a post body or frontmatter — catches the MDX silent-drop bug, unencoded DOIs, and Velite schema violations. Trigger on "validate this post", "check my post", "is this post OK", or before running blog-publish.
---

# Validate a blog post

Velite type-checks frontmatter but never inspects the body. MDX parses a raw `<` in prose
as the start of a JSX tag, so a post can vanish from the built site **with no build error**.
That is the bug this guards against. It has shipped here before — commit `974922b`.

## Run it

```bash
yarn validate data/blog/2026/my-post.mdx   # one post
yarn validate:all                          # all 33 posts across every year
```

Exit code is `1` if there are errors, `0` if only warnings. Warnings never block.

Run this **before** `blog-publish` and after any edit to a post body.

## Reading the output

### Errors — these break the site

| Rule                  | Meaning                                                                | Fix                                                                  |
| --------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `raw-angle-bracket`   | A bare `<` in prose. MDX reads it as JSX and drops the post.           | Escape as `\<`, wrap in backticks, or percent-encode if in a URL.    |
| `doi-encoding`        | Unencoded `<`/`>` inside a DOI.                                        | `<` → `%3C`, `>` → `%3E`. Legacy SICI DOIs hit this constantly.      |
| `unknown-element`     | Lowercase tag that is not real HTML — usually prose, not a tag.        | Escape the `<`.                                                      |
| `undefined-component` | Capitalized tag. JSX resolves it as a variable, and it is not defined. | Only `Image` and `TOCInline` exist (`components/MDXComponents.tsx`). |
| `html-comment`        | `<!-- -->` is invalid in MDX v2.                                       | Use `{/* ... */}`.                                                   |
| `required-field`      | Missing `title` or `date`.                                             | Velite requires both; the build fails.                               |
| `date-format`         | `Date.parse` cannot read the date, so `s.isodate()` rejects it.        | Use `YYYY-MM-DD`: `date: '2026-07-17'`.                              |
| `unknown-author`      | `authors:` entry with no file in `data/authors/`.                      | Use `default`, or add the author file.                               |

### Warnings — worth knowing, never fatal

| Rule                  | Meaning                                                                                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `draft-post`          | `draft: true` — the post is deliberately held back from listings, its own route, the sitemap, and RSS. Expected while drafting; check it before publishing. |
| `dead-frontmatter`    | `tags:`. Not in the Velite schema and not read anywhere; silently stripped at build. The tag UI was removed.                                                |
| `unknown-frontmatter` | Key outside the schema; silently stripped at build.                                                                                                         |
| `unquoted-date`       | YAML parsed the date as a timestamp. Valid, but quote it to match other posts.                                                                              |
| `nonstandard-date`    | Parseable but not `YYYY-MM-DD` (e.g. `'2024-06-04 00:00:00'`). Velite accepts and normalizes it; three 2024 posts use this shape. House style only.         |
| `missing-summary`     | No `summary`; post listings will have nothing to show.                                                                                                      |
| `year-mismatch`       | File is in `data/blog/<year>/` that disagrees with `date`. Convention only.                                                                                 |

## Interpreting results for the user

- **Report errors plainly and stop.** Do not publish a post with errors.
- **Do not auto-fix silently.** Show the offending line and the fix, then let the user confirm —
  an escaped character changes rendered prose.
- **Do not strip `tags:` from existing posts** as a side effect of validating. Most posts
  carry it; removing it is a separate decision.
- **Never flip `draft` on the author's behalf.** A `draft-post` warning is information, not
  a defect — publishing is their call, and clearing the flag puts the post on the live site.

## Adding a rule

Rules live in `scripts/validate-post.mjs`, tests in `scripts/validate-post.test.mjs`.
Every rule must have a test, and the whole real corpus must stay at zero errors:

```bash
yarn test
```

A validator that cries wolf on real posts gets ignored, which is worse than no validator.
If a new rule flags any of the 33 published posts, the rule is wrong — not the post. The
corpus test walks every year directory for exactly this reason: checking only the recent
years once hid a false positive in the 2024 posts.

## Next step

Clean? → `blog-publish` to build, verify, and commit.

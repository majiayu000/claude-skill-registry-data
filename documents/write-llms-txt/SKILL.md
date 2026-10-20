---
name: write-llms-txt
description: >-
  Load this skill when creating or updating llms.txt, the index that tells AI agents what a product
  is and which pages to read, or when pages are added to a site that ships one. Trigger on "write an
  llms.txt", "llms-full.txt", "make the docs readable by AI agents".
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Write llms.txt

`llms.txt` is a **curated reading list for an agent working under a context budget**, not a
sitemap. A sitemap enumerates every URL for a crawler with unlimited patience; `llms.txt` answers
"you have room for five pages — read these". Every link earns its place by displacing another.

The spec is [llmstxt.org](https://llmstxt.org/). It is small, and the parts that get it wrong are
the ordering rules and the curation, not the markdown.
Done means the file has an H1 and a summary blockquote, every link points at a page that resolves,
and the links are ordered by what a newcomer needs first.

## Procedure

1. Write the structure. It is positional — each region is defined by what precedes it, so content
   in the wrong place is read as a different region rather than rejected:

   ```markdown
   # Project Name

   > One-sentence summary with the key information needed to understand the rest.

   Optional prose paragraphs. No headings allowed in this region.

   ## Docs

   - [Quickstart](https://example.com/quickstart.md): Install and first request in under a minute.
   - [API reference](https://example.com/api.md): Every endpoint, with request and response shapes.

   ## Optional

   - [Changelog](https://example.com/changelog.md)
   ```

   - **H1 is the only required element.** Everything else is optional, but a file with no blockquote
     wastes the one line an agent reads first.
   - **The blockquote is a summary, not a tagline.** It is the same job as the README first screen —
     category noun, who it is for, the differentiator (see `ceh-seo:write-project-listing-text`).
   - **Prose sits between the blockquote and the first H2, and may not contain headings.** A heading
     there silently starts the file-list region early and swallows the prose.
   - **Every H2 section is a list of links and nothing else.** Format is `- [name](url): notes`. The
     notes are optional, the link is not; a bare bullet with no hyperlink is not part of the file
     list.
   - **`## Optional` is reserved.** By convention it means "skip these when context is short". Name
     it anything else and the skip signal is gone. The spec does not require it to come last, but
     put it last anyway: an agent that stops reading there loses nothing.

2. Curate the links. This is the whole job: the format takes five minutes, the curation is what
   makes the file work.
   - **Link the page that answers a question, not the page that lists pages.** A link to `/docs`
     costs the agent a fetch and returns another index. Link the quickstart directly.
   - **Order sections by what a newcomer needs first** — quickstart, then core concepts, then
     reference. Agents read top-down and stop when the budget runs out.
   - **The note after the colon states what the reader will learn**, not what the page is called
     again. `[Auth](url): API keys, OAuth flow, and token lifetimes` beats
     `[Auth](url): Authentication docs`.
   - **Demote rather than delete.** Anything you would not spend the budget on goes under
     `## Optional` — changelogs, contribution guides, legal pages.
3. Point every link at clean markdown, not HTML. Two accepted conventions: append `.md` to the
   path (`/guide.html.md`) or replace the extension (`/guide.md`). Pick one and use it for every
   link. Linking to HTML is not a spec violation, but it hands the agent a nav bar, a cookie
   banner, and a footer to pay for. If the site cannot serve markdown, link the HTML and say so —
   do not link `.md` URLs that 404.
4. Decide on `llms-full.txt`. It is a de-facto convention, **not in the spec**: the entire
   documentation set concatenated into one markdown file, for agents that would rather take one
   large fetch than many small ones. Ship it only when a build step generates it. A
   hand-maintained `llms-full.txt` goes stale within a release and is worse than absent.
5. Keep it current:
   - Generate or review `llms.txt` whenever a public page or docs section is added or removed —
     the same moment `sitemap.xml` changes. A stale entry pointing at a 404 costs an agent a fetch
     and teaches it to distrust the file.
   - Prefer generating it from the same source that builds the nav or sitemap. Hand-maintenance is
     acceptable only for a site small enough to hold in one screen.
   - Serve it at the path root it covers. Agents resolve the most specific applicable file, so
     `/docs/llms.txt` wins over `/llms.txt` for `/docs/*`. The spec names no media type — whatever
     the host serves markdown as is fine.

## Rules

- **Select the links that earn a place.** A file listing 200 URLs has made zero decisions and is
  strictly worse than the sitemap it copied.
- **Write the blockquote as a plain factual summary.** The agent is deciding what to read, not
  whether to buy.
- **Keep page content on its own page.** `llms.txt` links; it does not host. That is what
  `llms-full.txt` is for.
- **Do not treat it as a substitute for the HTML head surface.** `llms.txt` has no bearing on
  search indexing or link previews — those still need `ceh-seo:make-page-crawlable`.

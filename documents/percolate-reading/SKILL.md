---
name: percolate-reading
description: Review saved web captures or maintained quote notes in this repository's Markdown knowledge base, turn selected sources into evidence-backed reading digests or complete reading notes, and project only explicitly published notes into the personal website. Use when triaging captured sources, percolating something read, preserving reviewed quotations, publishing a reading note, checking the reading inbox, or regenerating the public Reading collection and Atom feed.
---

# Percolate Reading

Move reviewed knowledge from the private vault to the public reading surface without making the website depend on the vault.

## Boundary

- Markdown and Git in `kb/` are the editorial authority.
- A capture is evidence, not permission to publish.
- Only a maintained note at `kb/notes/reading/<slug>.md` with `reading.status: published` enters the public registry.
- The projector is local, deterministic, and network-silent.
- Production imports `personal-website/app/reading/entries.generated.ts`; it never reads `kb/`, capture manifests, cookies, browser state, or authenticated material.
- Do not publish a private capture merely because its sanitizer removed obvious secrets. Screenshots and prose can still contain private information.

Read [references/entry-format.md](references/entry-format.md) before creating or changing a reading note.

## Inspect the inbox

List manifest-backed web captures that have no related reading note:

```sh
bun run reading:inbox
bun run reading:inbox --json
```

The inbox is advisory and read-only. Partial captures, private acquisition methods, warnings, and non-publishable capture states are reported as review signals. Do not convert them automatically.

Use `$query-kb` to inspect a candidate capture, its manifest, related notes, and relevant provenance. Re-capture with `$save-url-kb` or `$save-pdf-kb` when the evidence is incomplete rather than filling gaps from memory.

## Choose a form

Use a `digest` for a public web source when a concise gist, three to five useful ideas, and up to four short verified quotations are the public object.

Use a `note` when the complete reviewed passage is the public object. Complete notes require reviewed public source metadata, a confined evidence note, a precise evidence locator, `full_text_reviewed: true`, and an explicit republication basis before publication.

Keep new notes in `draft` until every public field, quotation, date, author, source URL, evidence relation, privacy boundary, and publication-rights claim has been reviewed.

## Write from evidence

1. Read the entire relevant capture or evidence note. Preserve uncertainty and capture warnings.
2. Confirm the canonical HTTPS source URL and remove tracking parameters.
3. Verify author, publication, and date metadata against the saved evidence. Do not invent missing precision.
4. Write the maintained note exactly to the selected schema.
5. For digests, verify every quote occurs verbatim in a distinct passage of the captured text. Each quote is at most 25 words; all quotes together are at most 100 words.
6. For complete notes, confirm transcription, formatting, privacy, source accuracy, evidence location, and republication basis. Review flags record editorial work; they do not create rights.
7. Keep private vault paths, acquisition details, warnings, evidence IDs, and review-only flags out of public prose.

## Validate and publish

Validate drafts and published notes without writing:

```sh
bun run reading:check
```

When the note is ready, set `reading.status: published`, then regenerate:

```sh
bun run reading:generate
bun run reading:check
bun run kb:refresh
bun run kb:check
```

Review the generated diff. It should contain only public fields: slug, title, dates, reviewed source metadata, and the selected digest or complete-note content.

Run `bun run check` before handoff. The application tests cover reading routes, Atom serialization, bookshelf data, SEO metadata, and the generated-file boundary.

## Existing entries

Edit the maintained KB note, never `entries.generated.ts` by hand. Re-run generation and review the public diff. To unpublish an entry, change its status to `draft` and regenerate; do not delete the evidence solely to remove the public projection.

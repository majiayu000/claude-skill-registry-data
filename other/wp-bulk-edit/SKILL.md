---
name: wp-bulk-edit
description: Propose bulk edits to WordPress posts and pages through the wp-editor store — open a changeset, work through it in batches with `pnpm editor todo`/`scanned`, write proposals, validate. Use when asked for a site-wide content pass (spelling, markup cleanup, custom HTML on chosen articles) on the blog.
---

# Bulk-editing WordPress through the editor

You never touch WordPress or the review UI. You read and write files in the store at
`$NUXT_EDITOR_STORE` through `pnpm editor` (run from `apps/wp-editor`), and the user reviews and
applies. The layout and the rules are in [the app README](../../../apps/wp-editor/README.md).

## 1. Open the changeset

```sh
pnpm editor new "<short title>" --instructions="<the user's request, verbatim>"
```

It is refused while another changeset is open. Never pass `--override` on your own: it abandons the
open one, so ask the user first. `--ids=posts-12,pages-3` limits it to chosen articles.

## 2. The batch loop

Repeat until `todo` lists nothing:

1. `pnpm editor todo --limit=15` prints the next base files.
2. Read each `base/<key>.html`, and `base/<key>.json` when the title or excerpt matters.
3. Only where something changes, write `proposed/<key>.html` with the **whole** article. Add
   `proposed/<key>.json` with `{ "title": … }` or `{ "excerpt": … }` only if those change.
   Add `"reviewRequested": "<one line on what to check>"` there when a human should double-check
   the change: a legal or factual claim, a removed paragraph, a guess. The user may only review
   these, so flag every one that needs it and nothing cosmetic.
4. `pnpm editor scanned <every key in the batch>`, including the ones you left alone.

State is on disk after each `scanned`, so an interrupted run resumes at step 1.

## 3. Rules for a proposal

- Edit the raw source as you found it. Keep every `<!-- wp:… -->` marker, its attributes and its
  order unless the task is about the blocks themselves.
- No proposal is better than a cosmetic one. Whitespace-only rewrites make review slower.
- Never write to `base/` or `state/`. `base` is the backup restore writes back.

## 4. Finish

```sh
pnpm editor validate   # deletes no-op proposals, warns on changed block markers
pnpm editor status
```

Explain each marker warning to the user, or fix the proposal. Then tell them the changeset is ready
to review in `pnpm dev`.

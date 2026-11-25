---
name: legals
description: Legal documents for the user's own app, filled from its code (privacy policy, terms of service, subscription terms, refund policy, account deletion page), and the company's own agreements (founders' / shareholders' agreement, IP assignment, contractor agreement). Use to write or update them, to find which ones the app needs, or to build a skeleton for a legal document.
---

# Legals

Writes a product's legal documents from its code and from **skeletons**: records of how real
companies write each document (`formats/skeleton-format.md`). Two branches:

- **Write** (default): the steps below.
- **Build**: the user asks to build or refresh a skeleton, or a write run needs one that is
  missing or stale. See *Build branch*.

When every chosen item has a skeleton, run the steps through without asking leave between them.
Stop for the user only to ask facts (step 3) and before any build.

Talk to the user in **plain words**, in their language, as a person would: name the document
and what you will do, never this skill's own terms (skeleton, block, fact key, region file,
pool, collector, extractor, build).

Every recommendation you make is the **legal minimum**: what the law or the stores require of
this product. State a requirement once, with its source. When the user declines it, record the
choice and move on.

## Write branch

Files you work from: `helpers/catalog.md` (items and their trigger questions), `helpers/facts-schema.md` (fact
keys and the `legal/facts.md` format), `formats/region-format.md` (regions; the regional part of a
written document, or a tabular document's region columns and header lines). Regions are the folders under `regions/`; each may add a `catalog.md`, a
`facts.md` and one file per item it contributes to. A file under the user's
`legal/.skeletons/` replaces or adds the skill's file at the same path below it.

Paths in this skill's files are relative to its folder. This skill explicitly asks for subagents:
run every helper below as its own subagent, never in your own context, and do not read its file
yourself. Each subagent's instructions are in
`helpers/<name>.md`. Start every subagent fresh, with that file as its instructions, this folder's
absolute path and the inputs its step names. Where your harness lets you, set the effort and
model below: a fast model for `pool-collector` (Sonnet in Claude Code), the strongest for the rest
(Opus).

| Subagent            | Effort |
| ------------------- | ------ |
| `code-scanner`      | medium |
| `pool-collector`    | medium |
| `doc-writer`        | high   |
| `slop-editor`       | high   |
| `overshare-checker` | high   |
| `doc-checker`       | high   |
| `sample-extractor`  | high   |

1. **Pick.** Settle `facts.users.regions`, `facts.product.category` and
   `facts.product.language` (always asked, even when the repo shows it), then the trigger
   question of every row in `helpers/catalog.md` and in the `catalog.md` of each region in
   `facts.users.regions`: from a light look at the repo (store metadata, sign-in, payment SDKs),
   and what that leaves open by `helpers/grilling.md`. Find the product's existing legal
   documents (repo, website, store listing links), in any format: each one is patched, not
   replaced, unless the user asks for a rewrite. The result always goes to `legal/<doc-id>.md`;
   the original stays as it is. Warn about a chosen skeleton whose `scanned` date is over 12 months
   old and offer a refresh through the build branch. A document the user wants that no catalog
   lists goes to the build branch.
   Done when every row is marked needed or not needed with its reason; show the user the list
   and go on.
2. **Scan.** Collect the fact keys of the chosen items: every `facts.*` key in their skeletons
   and in the files of the regions in `facts.users.regions`
   (`grep -oh 'facts\.[a-z_]*\.[a-z_]*' <files> | sort -u`). Dispatch one `code-scanner` with
   the keys, the schema files that define them (`helpers/facts-schema.md`, the regions' `facts.md`,
   `legal/.skeletons/helpers/facts-schema.md` if present), the existing documents and the value of
   `facts.users.regions`.
   Done when `legal/facts.md` has an entry for every key.
3. **Ask.** Settle every `missing` and `conflict` key by `helpers/grilling.md`.
   Done when every key still needed is `found` or `answered`.
4. **Draft.** Dispatch one `doc-writer` per chosen item, all at once. Each dispatch gives the
   skeleton, the region files for that item (`block` or `whole`) of the regions in
   `facts.users.regions`, `legal/facts.md`, the output language (`facts.product.language`;
   for an item from a region's `catalog.md`, that region's first `languages` entry), the
   existing document and mode
   (`new`, `patch` or `rewrite`; an existing document in another language than the output
   language is a `rewrite`), the user's requests for that document's terms if they made
   any, and the output path `legal/.drafts/<doc-id>.md`. A writer that refuses a request
   names the law it breaks; tell the user that in one sentence. When
   `facts.sales.subscription_terms_placement` is `tos-section`, the subscription terms get no
   writer of their own: the terms-of-service writer also gets their skeleton and writes them as
   one part of the terms.
   Done when every draft exists and every writer's reply accounts for every section.
5. **De-slop.** Dispatch one `slop-editor` per draft, all at once, each in a fresh context with
   only: the draft path, the path of `helpers/de-slop.md`, the output path `legal/<doc-id>.md` and, in
   patch mode, the headings the writer changed. Nothing else: no facts, no skeleton. The
   open-source notices are copied licence texts, so their draft moves to `legal/` as it is.
   Done when every final file is written and its draft deleted.
6. **Trim.** Dispatch one `overshare-checker` per final document, all at once, each in a fresh
   context with only: the document, its skeleton and region files and, in patch mode, the
   headings the writer changed. No `legal/facts.md`: it judges what a sentence says, never
   whether it is true. The open-source notices skip this step. Rewrite each finding in the final
   file as its fix says, then dispatch that document's checker again.
   Done when every checker replies `clean`.
7. **Check.** Dispatch one `doc-checker` with the final documents, their skeletons and region
   files, and `legal/facts.md`; its coverage check catches a fact the law asks for that the trim
   lost. Fix each finding in the final file, then dispatch it again.
   Done when the checker replies `clean`.

Finish with the list of files written and what the user must still do themselves: have a
lawyer review the documents before they are published, as they are not legal advice (say this
once, here), translate the documents into any other
languages they publish in, carry each document into the site or app in its own format, and link it from the app and the store listings.

## Build branch

The method is `build/build.md`; it routes forms, templates and tasks to their own build files.
You run the build yourself and dispatch its collectors and extractors directly. Never hand the
whole build to a subagent: in some harnesses subagents cannot start subagents.

Before a build, check in: in two or three plain sentences, say which document you have no model
for, how you will research it, what it costs and where the result goes; then wait for an okay.
For example: "I don't have a model for a beta test agreement yet. I'll read the beta terms of
about 10 note-taking apps like yours and see what they all cover. That takes about 10 helper
agents and a good part of your usage limit. Okay?"

Where the output goes, and how big the run is, depends on the repo you are working in:

- **User run:** any repo but the plugin's own. The run is small and samples
  the user's own field only (`build/build.md` *User run*). Research goes to
  `legal/.research/<doc-id>/`, the skeleton or region file to `legal/.skeletons/` at its path
  inside the skill (`legal/.skeletons/skeletons/<doc-id>.md`,
  `legal/.skeletons/regions/<code>/<doc-id>.md`), and new fact keys to
  `legal/.skeletons/helpers/facts-schema.md`.
- **Creator run:** the working repo is the skill's own (its root has
  `plugins/fatodono-founderkit/skills/legals/` and `workshop/legals/research/`). Paths starting
  with `research/` are relative to `workshop/legals/`; the rest are relative to this skill's
  folder, and those files ship with the plugin. The run is full size, about
  35 helper agents per document: about 5 `pool-collector` subagents (medium) and 15–30
  `sample-extractor` subagents (high). You dispatch; the judging goes to one merge helper
  (xhigh, the strongest model you can pick), resumed through the build: the first-batch merge, each saturation batch, the
  merge, the facts and the skeleton, so the section ids stay in one context. Build several items
  in parallel only when the user asks; you still dispatch every item's collectors and extractors
  yourself, at most 3 per item at once (a session runs about 20 in total), and retry a subagent
  that dies on an overload (529).

Either way, continue the write branch with the new files.

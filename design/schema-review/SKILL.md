---
name: schema-review
layer: stage
description: Render a crouton collection schema (the field-definition JSON) into a human-readable field table + relationships sketch (HTML + PNG + a terse Markdown table), so a human can sign off on the DATA MODEL before any code is generated. Use when an agent drafts or changes a collection schema (before `crouton config` / `generate_collection`), or when asked to "review a schema", "show the data model", "check these fields".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Schema Review — check the data model before you generate it

Turns a raw collection schema (field-definition JSON) into a **reviewable artifact**: a
skimmable field table (name · type · required · translatable · default · references) plus a
small relationships sketch — so the data model can be approved *before* `crouton config`
generates the Form / List / API / migration from it.

This is the schema analog of the `ui-proposal` skill, and the foundation of the schema
sign-off loop (epic #314): produce the review → it gets posted on the PR → iterate on
feedback → only then generate the collection. The schema is the foundation; a wrong field
type or missing relationship means regenerating the whole collection, so approving it first
is cheap and fixing it after is not.

> **Why a PNG?** GitHub comments can't render raw HTML/CSS. The committed `.html` is the
> editable source; the `.png` is what gets posted (plus the inline Markdown table).

## When to use
- An agent has drafted/changed a **collection schema** (the `fieldsFile` JSON, or MCP
  `design_schema` output) and is about to run `crouton config` / `generate_collection`.
- The user asks to "review the schema", "show the data model", "check these fields".
- **Skip** for non-schema work (no collection / field defs involved).

**Review the `crouton.config.js` alongside the fields.** The schema is the *data model*;
`crouton.config.js` is the *generation plan* — collections, target `layer`, `features`,
`locales`, `dialect` — and it decides the generated forms / lists / API surface. So the
config is part of the **same** sign-off, presented next to the field tables, not a
separate step.

It sits **after** the machine `validate_schema` step (which checks the JSON is well-formed)
— this is the **human** gate on top of it.

## What it produces
| Artifact | Path | Committed? |
|----------|------|-----------|
| Review source (HTML) | `writeups/schema-reviews/<collection>.html` | ✅ yes (editable source of truth) |
| Markdown table | `writeups/schema-reviews/<collection>.md` | ✅ yes (inline-postable) |
| Rendered image | `screenshots/schema-review-<collection>.png` | ❌ no — `screenshots/` is gitignored; it's posted to the PR, not committed |

## Step 1 — Get the schema JSON
Obtain the field-definition JSON for the collection (the `fieldsFile`, or the MCP
`design_schema` output). Save it to a file, e.g. `/tmp/<collection>.schema.json`. The
renderer accepts any of these shapes:
- `{ "collection": "products", "fields": { ... } }`
- `{ "fields": { ... } }`
- a flat map `{ "name": { "type": "string" }, ... }` (pass `--collection <name>`).

Each field follows the crouton schema (see the `crouton` skill): `type`, optional `meta`
(`required`, `unique`, `primaryKey`, `default`, `precision`/`scale`, `options` +
`displayAs`, `optionsCollection`…), `translatable`, and `refTarget`/`refScope` for relations.

## Step 2 — Render the review
```bash
node .claude/skills/schema-review/render-schema.mjs /tmp/<collection>.schema.json
# → writes writeups/schema-reviews/<collection>.html + .md, and prints the Markdown table
# options: --collection <name>   --out-dir <dir>
```

## Step 3 — Render to PNG (shared renderer from #308)
```bash
node .claude/skills/ui-proposal/render.mjs \
  writeups/schema-reviews/<collection>.html \
  screenshots/schema-review-<collection>.png
```
Uses the repo's Playwright headless Chromium — offline, no network.

## Step 4 — Hand off (review happens on the DIFF)
**The committed Markdown is the actionable review surface — not the image.** A PNG can't be
commented on; the reviewer would have to copy text and describe which field they mean. The
`.md` lands in the PR's "Files changed", one field per row, so the reviewer can click the `+`
on any line and leave an **inline comment pinned to that exact field** ("make this `decimal`",
"add a `slug` field here") — no copying, no describing.

- **Commit** `writeups/schema-reviews/<collection>.md` **and** `.html` (via `/commit`, scope
  `docs`) so the `.md` appears in the PR diff. This is where feedback goes.
- The **PNG** is the optional at-a-glance visual — post it in the PR description/comment, but
  steer feedback to the diff.
- The gate + revision loop that hold `crouton config` until approval are wired in **#316**
  (reusing the generic approval loop from #310): it reads the **inline review comments** on the
  committed `.md`, revises the schema field-by-field, re-renders, and replies to/resolves each
  thread. When running this skill by hand, point the reviewer at the committed `.md` in the diff.

## Unresolved relations — the thing this gate exists to catch

A field typed `relation` with **no `refTarget`** is the highest-value thing on the page: it is
the one detail that makes the relation buildable, and it is the easiest to approve without
noticing. The renderer marks it **⚠ not set** in the References column and replaces the
relationships sketch with a warning naming each offender. It never reports "No relationships"
for a collection that has relation fields.

**Do not approve a schema carrying one.** Name the collection each points at, and check that
collection is actually being generated — a target that doesn't exist produces an import to a
missing file and fails the *build*, minutes later, with an error that names none of this.

If **people** are the intended target, say so explicitly: in crouton they come from the
auth/team side, not a generated collection, so it likely needs a different field type rather
than a relation.

Pass `--strict` to make it a hard gate (exit 1) — use that for a pre-generate check or CI. It
is **off by default** because the decompose apply step calls this inside a best-effort guard,
where a non-zero exit would drop the schema artifact from the sign-off comment entirely and
hide the problem instead of showing it.

> Minted by the #1825 chores POC: `assignee` and `lastDoneBy` were approved as untargeted
> relations, the summary read "_No relationships._", the build instruction then invented
> "references household members/users", the worker turned that into `refTarget: "users"`, and
> the generated code imported a `users` collection nobody ever created.

## Conventions
- One review per collection; re-render after every schema edit so the artifact never drifts.
- The field table is the source of truth for review — keep it honest (mirror the actual JSON,
  including primary keys 🔑, `unique`, defaults, and every relationship).
- Keep it focused on the one collection under discussion.

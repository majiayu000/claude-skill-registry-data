---
name: blog-emit
description: |
  Emit a canonical blog draft (blogs/<slug>/index.md) to a downstream target. Runs
  the deterministic emitter core (resolves file= snippets, renders
  journeys/callouts/diagrams per the target), then delivers the result and
  records the delivery for idempotent re-emits. Targets:
    - unitycatalog — a rich native Astro MDX post in the sibling unitycatalog-website
      repo (interactive LikeC4, <Journey> timelines, :::callouts).
    - delta — a rich native Astro MDX post in the sibling delta-io/website repo
      (../website), same rich rendering.
  A post may list several targets to cross-post to; the first is the primary and the
  others carry a canonical link to it.
  Use when the user wants to emit / export / cross-publish a draft to unitycatalog.io
  or delta.io, or to refresh an already-delivered post there.
argument-hint: 'A blogs/<slug> to emit. Optional --target <unitycatalog|delta>[,…]; defaults to the target: list in the draft.'
---

# blog-emit: emit a draft to a downstream target

A blog `index.md` is **canonical, portable CommonMark** — richness is a property of
the *renderer*, never the source (see
[`blogs/CONVENTIONS.md`](../../../blogs/CONVENTIONS.md) §5). This skill is the
**delivery** half of the emitter: it runs the deterministic core to produce a
target-shaped render, then delivers it to that target and records the delivery so a
re-emit updates in place rather than duplicating.

The design is a **target-agnostic spine + one per-target runbook**:

- **Deterministic core** — [`emit/`](../../../emit/), a committed Node package. It
  does everything scriptable: resolve `file=` snippets and render each rich
  construct (`::::journey`, `:::callout`, `likec4` blocks, code captions)
  the way the chosen target needs — upgraded to site components (unitycatalog,
  delta). It dispatches on `--target`; each target is a module in
  [`emit/targets/`](../../../emit/targets/). **Do not reimplement any of this in the
  agent** — run the script.
- **Delivery adapter (this skill)** — the part that needs judgment, MCP tools, or
  filesystem writes a Node script can't/shouldn't do. The **spine below (steps 1–2,
  4) is identical for every target**; the target-specific delivery mechanics live in
  a single sidecar runbook, [`references/<target>-target.md`](references/), which you
  load in step 0 and follow in step 3.

The source of truth for *what a target's render contains* is
[`blogs/CONVENTIONS.md`](../../../blogs/CONVENTIONS.md) §5,
[`emit/README.md`](../../../emit/README.md), and the target module
(`emit/targets/<target>.mjs`) — read them if a construct's rendering is unclear;
don't restate them here.

## Steps

### 0. Resolve the targets and load their runbooks

The draft's `target:` is one site or a list of sites to cross-post to; the **first is
the primary**. Take the targets from `--target` if given, else from that list, and
**confirm the list with the user before delivering** (each delivers to an external
site). Valid targets are the delivery modules in `emit/targets/` (`unitycatalog`,
`delta`); a listed target without one (`openlakehouse`) can't be emitted.

Work through the targets **one at a time, primary first**, running steps 1–4 for
each. For each target, **read the matching runbook and follow it for step 3** — only
that one (this is the progressive-disclosure seam; don't load the others):

| target        | runbook                                      | delivers to                              |
| ------------- | -------------------------------------------- | ---------------------------------------- |
| `unitycatalog`| [`references/unitycatalog-target.md`](references/unitycatalog-target.md) | `../unitycatalog-website` (Astro MDX)     |
| `delta`       | [`references/delta-target.md`](references/delta-target.md)               | `../website` — delta-io/website (Astro MDX) |

### 1. Run the deterministic core

From the repo root:

```bash
cd emit && bun install    # first run only (installs unified/remark deps)
bun emit.mjs --slug <slug> --target <target>
```

(`--target a,b` or no `--target` at all emits several targets in one run; render the
cross-posts again after the primary's delivery is recorded, see below.)

This writes, under `blogs/<slug>/dist/<target>/`:

- the render — `index.mdx` (unitycatalog, delta);
- `assets.json` — `{ slug, target, primary, canonical, title, existing, images: [...] }`;
- `likec4-webcomponent.mjs` — the interactive-diagram bundle (rich targets, only when
  the post has a `likec4` block).

It also prints whether delivery should **CREATE** or **UPDATE**. The core refuses a
`private` post and warns when the post isn't `ready`: rendering a draft to check
the target is fine, but deliver only a `ready` post (merged to main is the
release, ADR-0002), unless the user explicitly asks for a draft delivery.

### 2. Read the render + manifest

- the render file — deliver **this**, never the raw `index.md` (its `file=` fences are
  empty and its `:::`/`::::` markers would leak).
- `dist/<target>/assets.json`:
  - `existing` is the **create-vs-update decision**, sourced from the post's
    `.emitted.json` sidecar under the `<target>` key: `null` → CREATE; an object →
    UPDATE that delivery in place. Its shape is `{ post_dir, updated }` — the runbook
    you loaded describes it.
  - `canonical` is set on a cross-post: the primary's delivered URL, which the render's
    frontmatter carries so the site points search engines at the primary. It is
    `null` on the primary. On a cross-post it is `null` only while the primary has no
    delivery recorded, and the core prints `canonical: pending`: deliver the primary
    first (through step 4), then re-run step 1 for the cross-post. Never deliver a
    cross-post without its canonical.
  - each `images[]` entry is `{ filename, localPath, altText }`; `localPath` is the
    real file on disk to upload/copy. LikeC4 views aren't images: the render's
    `<LikeC4View>` draws them from the web-component bundle.

### 3. Deliver — follow the runbook from step 0

Do the CREATE-or-UPDATE delivery exactly as the target's runbook specifies. That is
the only target-specific part of this skill.

### 4. Record the delivery + report

The delivery mapping lives in a **committed sidecar dotfile** next to the draft,
**`blogs/<slug>/.emitted.json`**, keyed by target — self-contained in the post's
folder (it travels with the post, no global registry) while `index.md` stays pure.

- **On CREATE**, read the sidecar (treat missing as `{}`), set the `<target>` key to
  the block the runbook specifies, **leaving any other target keys untouched**, write
  it back, and commit it (tracked, not gitignored). This is what makes the next emit
  an UPDATE, not a duplicate.
- **On UPDATE**, refresh that target's `updated` to today's date.
- **Report** the result (post dir + preview URL) to the user, then continue with the
  next target. A cross-post's render needs the primary's sidecar entry, so record
  the primary before you emit the cross-posts.

## What this skill must NOT do (all targets)

- **Never edit `index.md`** — the draft is canonical. The only per-post state this
  skill writes is `blogs/<slug>/.emitted.json` (the delivery mapping); it never
  touches any other file under `blogs/<slug>/` besides the generated `dist/` (which
  the core owns).
- **Never feed raw `index.md` to the target** — always deliver the core's
  `dist/<target>/` render (see step 2).
- **Never reimplement the core's transforms** — if the render looks wrong, fix the
  core (`emit/`, a plugin, or the target module), not the agent.
- **Never publish/share on the user's behalf.** This is the shared invariant behind
  every runbook's "do NOT push": never push or open a PR on the sibling repo without
  explicit instruction. Delivery stops at a local artifact the user then chooses to
  release.

## Adding a target

A new target is: (1) a new `emit/targets/<name>.mjs` (reusing the whole
`resolve → render` core — declare its `constructs`, `frontmatter`, and flags, per the
module docs in `emit/targets/unitycatalog.mjs`); (2) a new `references/<name>-target.md`
runbook; (3) a row in the step-0 table above. The core and the `.emitted.json` ledger
are already target-keyed, so idempotency carries over for free. The delta target was
added exactly this way — its runbook doubles as a worked example, including the
one-time sibling-repo site wiring a rich MDX target needs.

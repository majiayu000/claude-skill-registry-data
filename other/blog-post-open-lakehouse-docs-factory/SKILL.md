---
name: blog-post
description: |
  Author an opinionated long-form blog post through its lifecycle — park an idea,
  turn it into a brief, draft it, and refine it — following the writing repo's blog
  conventions. Use when the user wants to start, write, or draft a blog post, turn
  an idea into a brief, or continue an in-progress post in blogs/<slug>/.
argument-hint: 'An idea (slug, IDEAS.md entry, or one-line pitch) or an existing blogs/<slug>/ to continue'
---

# blog-post: author a blog through its lifecycle

Drive a post through the lifecycle in
[`blogs/CONVENTIONS.md`](../../../blogs/CONVENTIONS.md): **idea → draft → ready**
(review happens in the DB review lifecycle, not via frontmatter status). This skill
owns everything up to review; the review pass is a separate hand-off to
`/blog-review`. Writing the brief and drafting are the *activities* within `draft`;
which files exist (a `brief.md` present but thin `index.md`, vs. a full `index.md`)
signals how far along the post is.

Two documents are the source of truth — read them, don't restate them:

- [`blogs/CONVENTIONS.md`](../../../blogs/CONVENTIONS.md) — the *process* (lifecycle,
  brief template, draft conventions, cross-repo sourcing, series, humanizer).
- [`blogs/QUALITY.md`](../../../blogs/QUALITY.md) — the *criteria* (what "good" is,
  facets a–f, and how citability is reconciled with the authored voice).

The `references/` files here are lifted from CONVENTIONS.md for quick access; if
they ever disagree with CONVENTIONS.md, CONVENTIONS.md wins.

## Voice — the one thing not to get wrong

Blogs are **authored and opinionated**: first person, a stance, a point of view.
That is a feature, not a rough edge to sand off. Everything below serves the
argument; none of it flattens it into neutral prose.

## Steps

### 1. Locate the stage

1. Read `blogs/CONVENTIONS.md` and `blogs/QUALITY.md` in full.
2. Figure out where this post is:
   - **No folder yet** (a bare idea or an `IDEAS.md` entry) → start at step 2. An
     idea worth ranking/reviewing early can get an on-disk folder at `status: idea`
     before it's fully briefed.
   - **`brief.md` exists** → the `status` is `idea` or `draft`; which files exist
     tells you the stage (a `brief.md` with a thin/absent `index.md` → step 3; a
     substantial `index.md` → step 4).
   - Read the existing `brief.md`/`index.md` before touching anything.
3. Confirm the stage and the intended slug with the user if it's ambiguous.

### 2. Idea → brief

Only when an idea has earned investment (you can write its one-line thesis and name
its audience — CONVENTIONS §1–2).

1. Create `blogs/<slug>/` (kebab-case slug).
2. Write `brief.md` from the ten-section template in
   [`references/brief-template.md`](references/brief-template.md), opening with the
   front matter in [`references/front-matter-schema.md`](references/front-matter-schema.md)
   (`status: draft` — or `status: idea` if the folder started as an early idea folder
   before it was fully briefed).
3. **Walk the real source material** — open the cited repos/PRs/docs and cite them
   with pinned pointers (CONVENTIONS §6). A brief built on unread sources is not a
   brief.
4. Check the idea off in `blogs/IDEAS.md` and note the slug.
5. Stop here and let the user react to the brief before drafting — the brief fixes
   *what* the post argues.

### 3. Brief → draft

1. Write `index.md` from the brief's outline. **Baseline first**: thesis + core
   sections; defer depth (CONVENTIONS §5).
2. Open with the front matter (`status: draft`), then the hook/thesis.
3. Pull code samples from the **pinned** refs the brief cites; show only the
   load-bearing lines; verify each against its ref (CONVENTIONS §5–§6). Keep a
   preserved, compilable excerpt in `snippets/` only when it's worth keeping
   separately — and when it's worth *running*, make it a PEP 723 `uv run` file, a
   `docker compose` service, or a captured `curl` transcript, with a `Verified:`
   header, per `references/draft-conventions.md` ("Runnable examples").
4. Follow [`references/draft-conventions.md`](references/draft-conventions.md) for
   voice, structure, linking, and diagrams.

### 4. Citability-aware drafting

Apply `blogs/QUALITY.md` facet (f) **as you draft**, within the adopt/adapt/reject
rules there — don't bolt it on afterward:

- **Answer-first intro** (40–60 words) that names the subject and carries a fact.
- **TL;DR / key-takeaways box** near the top (the brief's key takeaways, surfaced).
- **Section-leading answers**: the first 1–2 sentences under each H2 answer it.
- **Descriptive, sentence-case headings** — put the question-matching in the answer
  sentence beneath, *not* in a literal "What is X?" heading.
- **Tables / FAQ** only where they earn their place and fit the voice.

When a citability move would flatten the stance, **keep the voice** (QUALITY.md
governing rule).

### 5. Diagrams (if any)

Author diagrams in **LikeC4** (preferred) as dedicated views in
`architecture/model/views/blog-views.likec4`, and embed one in `index.md` as a
```` ```likec4 <viewId> ```` block whose body is real alt text; nothing is exported
or committed. A sequence diagram is a `dynamic view` that declares
`variant sequence`. D2 is still fine for
an existing `.d2` or a quick one-off (`blogs/render-diagrams.sh`, needs the `d2`
CLI). Details in
[`references/draft-conventions.md`](references/draft-conventions.md).

### 6. Refine / humanize

1. Tighten structure and prose.
2. Run the **`/humanizer`** skill over the draft — do **not** reimplement it. It
   removes the AI tells (CONVENTIONS §8); it must **not** remove the author's
   stance. (Refining is an activity, not a status — the post stays `status: draft`.)
3. Re-verify every code sample and factual claim against its cited ref.

### 7. Hand off to review

Tell the user to run **`/blog-review`** on `blogs/<slug>/` and then request
reviewers in the review app. `status: ready` follows a reviewer's approval there,
and merging it to main is the release (ADR-0002). Do **not** run the review
yourself and do **not** self-certify the post as ready.

### 8. Series & tags (throughout)

- If the post is part of an arc, record/update it in `blogs/SERIES.md` and set
  `series`/`series_order`; add the "where this fits" line + prev/next (§7).
- Ensure **every tag** in the front matter exists in `blogs/tags.yml`. If none
  fits, add the new tag with its one-line description **in the same change** — never
  introduce a tag that lives only in a post.
- Add the post to the index table in `blogs/README.md` when the folder is created.

---
name: docs-write
description: |
  Plan and draft a docs page under content/ from what the repo can prove: build
  a context pack from the LikeC4 model, the tested examples, the compatibility
  journeys, the release pins, and the environment registry, plan placement in
  nav.yml, write or edit the page and its tested scripts, then validate and
  tighten the whole page. Use when asked to write, draft, extend, or fix a
  Unity Catalog, Delta Lake, or open-lakehouse docs page, fill a planned nav
  slot, answer an accepted content request, or cover a model element that has
  no explanation page.
argument-hint: 'A page path, a planned backlog id (T02, H03), a content-request id, a model element id, or a description; optional review:lite'
---

# docs-write: plan and draft a docs page

Authoring only. This skill edits files under `content/` (and diagram views in
`architecture/model/views/`), runs scripts and validators, and returns a report.
It never commits, pushes, or sets `status: ready`: the caller owns git, and an
approval in the review app owns `ready`
([ADR-0002](../../../docs/decisions/ADR-0002-git-ready-is-release.md)).

Sources of truth, read instead of restated:

- [`content/README.md`](../../../content/README.md): the contract (frontmatter,
  folder mode, snippets, PEP 723, environments, versions, claims, nav).
- [`docs/design/docs-quality.md`](../../../docs/design/docs-quality.md): the
  rubric the page is reviewed against.
- The `authoring-prime` skill: the syntax cheat sheet, the NEVER/ALWAYS list,
  and the exemplars. Load it first.

## Tiers

- **Trivial** (a typo, a broken link, one wrong value): make the smallest
  edit, run step 6, and return. No placement and no context pack.
- **Standard** (a new page, a new task or section, a rework): every step.

## Steps

### 1. Resolve the work order

Turn the input into: target page(s), the bucket, the project, and the
requirement.

- **A page path:** read the whole page and its `snippets/`.
- **A planned slot** (`planned: T02` in `content/<project>/nav.yml`): the
  backlog entry in `docs/design/<project>-documentation-plan.md` (§6 for
  Unity Catalog) is the brief. Read its row and any linked request. Reviewers
  leave instructions on the slot itself: `list_feedback` with
  `slug: planned/<project>/<id>` (or `just feedback list --slug …`) returns
  them, and each open thread is a requirement that overrides the backlog row.
- **A content request:** `list_content_requests` (review-feedback MCP, or
  `just feedback requests --json`) gives its title, placement trail, and
  description. If it isn't accepted yet, stop and say so.
- **A model element with no `explains:` page:** `uv run docsnip validate`
  reports these as explanation-coverage gaps. The page is an explanation that
  `explains:` it.
- **A description:** derive the bucket from the reader's goal (learn → tutorial,
  do a task → how-to, understand → explanation, look up → reference). Ask if
  it's genuinely ambiguous.

If the target is a generated file, stop and name its source (see
[drafting rules](references/drafting-rules.md#generated-files)).

### 2. Build the context pack

Gather the facts the page may state. Everything the page asserts should trace
back to this pack.

```bash
uv run docsnip query explain <element>        # summary, edges, pages, journeys, environments
uv run docsnip query examples-for <element>   # tested scripts and their evidence
uv run docsnip query environment-for <script|project/journey>
```

Also read:

- `architecture/journeys/journeys/`, for the journeys the page can claim, with
  their `path` and `roles` (`paths.yml` says what each path requires) and the
  spec obligations they `covers` (`obligations/`), and
  `content/<project>/compatibility.yml`, for the tables that show them.
- `content/<project>/release.yml`, for the pins. Never type a version by hand.
- `envs/environments.yml`, for the stack's registry key, title, and `guide`.
- R01 (`content/unitycatalog/reference/001-features-and-limitations`), the
  private record of known issues and absences: which ones block this page's
  task and must be stated inline. Never link it.
- The neighbors in `nav.yml` and the pages that `explain`'s `citedBy` lists.

The query answers are internal: they can name drafts and non-public elements.
Use them to decide, but don't paste them into reader text. A `model:` link to
a non-`#public` element renders as plain text.

### 3. Plan placement (standard tier)

Follow [references/placement.md](references/placement.md). It returns the file
path and action, the frontmatter, the H2/H3 outline, the `nav.yml` change, the
journeys to claim, the environment, cross-references drawn from the model, and
open questions. For a new page or a move, this step is mandatory. Skip it only
for a scoped edit to one existing page that adds no section and no link.

### 4. Draft

Read the matching exemplars from `authoring-prime` (your type only), then
write against the [drafting rules](references/drafting-rules.md), keeping them
in context.

- **Editing an existing page:** make the smallest edit that meets the
  requirement, in the page's own voice. Don't restructure, reorder, or reword
  what the requirement didn't touch. A scoped edit that rewrites the page is a
  defect.
- **New page:** follow the plan's outline and the bucket's anatomy. A page with
  runnable code is folder-mode (`<NNN-slug>/index.md` beside `snippets/`), with
  the next free `NNN` prefix in its bucket.

### 5. Write and run the scripts

Every command the page shows comes from a script that runs.

- PEP 723 block, `[tool.docs-factory]` (`compose` pointing at the registered
  environment, `services`, `base-url-env`), regions wrapping only what the
  reader types, setup/`main()`/asserts outside, and asserts that pin each
  behavior the page states (including the failure a known issue describes).
- Claims for the journeys the plan named: `claims.<interface> = [{ journey,
  region }]`, or `fails = true` with an `anchor` for a documented failure.
- Run just this script, in its lane:
  `DOCS_FACTORY_SELECT='["content/<…>/snippets/x.py"]' uv run --group test-services pytest content`
  (the harness starts its compose; Spark, JVM, and Rust scripts need the
  toolchains `just test-spark`/`test-jvm`/`test-rust` name). A draft page's
  script runs as a non-strict xfail, so read the output: an XFAIL is a
  failure you have to fix. If the local package proxy can't resolve a fresh
  pin, say so rather than claiming it ran.
- Then run `uv run docsnip compat --fix` so the tables reflect the claims.

Needing a server configuration no registered environment has is a finding for
the caller. Don't hand-edit `envs/`.

### 6. Validate

```bash
uv run docsnip check                 # frontmatter, model refs, snippets, pins, compat, prose
node site/scripts/check-nav.mjs      # orphans, unknown pages, duplicate ids
uv run docsnip prose --json          # the prose findings, for this page
```

Fix every error. Fix prose warnings on lines you wrote. Report the rest.

### 7. Holistic pass

Read each touched page end to end, not just your diff:

- **Succinct:** the new prose doesn't repeat what the page already says. Merge
  overlap.
- **Integrated:** the additions read as part of the page, not bolted on.
  Headings and order still flow.
- **One topic:** a page that drifted gets trimmed, or the drift becomes a
  finding to split.
- **Altitude:** cut internals the reader never acts on. Vague procedures become
  concrete steps or open questions.

Then run the `humanizer` skill in `docs` mode on the touched prose. This pass
tightens. It never drops content the plan required.

### 8. Return

Return this contract to the caller:

- **Files:** every path created or modified, including scripts and nav.
- **Plan:** the placement plan (for the PR description).
- **Evidence:** for each behavior the page asserts, the script assert, claim,
  or source that backs it.
- **Validation:** the `docsnip check` and `check-nav` result, and which lanes ran
  locally and which didn't.
- **Open questions:** missing facts, unverifiable steps, needed environment
  changes. Or an empty list.
- **Requests:** the content-request id this page completes, so the caller can
  run `complete_content_request` after the PR exists.
- **Slot threads:** the planned-slot thread ids the page answers, so the caller
  can `reply_to_thread` on each with what the page does and the PR link once it
  exists. The reviewer resolves them.

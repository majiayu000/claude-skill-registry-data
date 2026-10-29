---
name: conjecture-dashboard
description: Maintain and render a tree-shaped HTML dashboard for a conjecture campaign. Use when a project has multiple live routes, ledgers, side drafts, or verifier scripts and needs an at-a-glance status view with links to the source-of-truth files.
---

# Conjecture Dashboard

Use this skill when a campaign needs a compact visual status tree that can be opened in a browser and
linked from a homepage. The dashboard is not a ledger replacement; it is a navigation surface that
summarizes the current route tree and points to the authoritative artifacts.

## When to use

- You have several live or recently closed routes and want a readable branch-status view.
- You need a browser-friendly page that links each branch to its ledger, draft, or TeX source.
- The active ledger has become hard to scan, but the route structure is still best understood as a
  tree.
- You want a stable HTML summary that can be linked from the repo homepage or site index.

## Dashboard contract

- The dashboard lives as generated HTML rendered from an authored JSON manifest.
- The manifest is the source of truth for the current route tree. Update it when a displayed claim
  or route status changes; a scratch result or unrelated ledger edit does not require a refresh.
- Every dashboard should have two top-level narrative sections before the tree:
  1. the current goal and an honest assessment of where the campaign stands relative to that goal;
  2. advances toward the original target and substantive reusable theory, with their round/date when
     known, plus decision-changing learning. Label local results and verification separately.
  Do not replace the last goal advance with the latest activity. If the essential obstacle remains
  unchanged, keep that visible even when a new lemma or counterexample has been verified.
  A general theory branch or standalone paper can be a major research achievement while that
  obstacle remains open. Give it its own question, results, and status rather than marking it parked
  solely because its return to the conjecture is unknown.
- These two sections are current-state summaries, not append-only logs. Keep them succinct and
  rewrite them in place at each substantive update; do not accumulate chronology, round-by-round
  notes, or stale progress claims there. Put history in the ledger and keep only the latest honest
  state/progress on the dashboard.
- The manifest should describe proof routes, reductions, closed conjectures, counterexamples,
  verification branches, and helper tools. It is a synthetic route tree, not a file tree.
- When helpful, give nodes a `method_role` field such as `exact reformulation`, `native invariant`,
  `census`, `proxy`, `local test`, `global compatibility`, `side import`, `counterexample search`,
  `tombstone`, or `publication consolidation`. This is distinct from `status`: it says what kind of
  mathematical work the branch is doing.
- Dashboard descriptions, node labels, and node descriptions may contain inline markdown and LaTeX
  math. Use `$...$`, `$$...$$`, `\(...\)`, or `\[...\]` directly in those fields when a title or
  description needs math.
- The renderer may normalize inline `$...$` math to explicit `\(...\)` in the generated HTML so it
  stays inline and typesets consistently.
- If a node points at a local markdown file through a content field, render that file as markdown in
  the dashboard rather than as escaped plaintext.
- If a link target is a local markdown file, the renderer should rewrite it automatically to the
  generated HTML preview page; the manifest should still name the original `.md` file.
- Markdown previews should support ordinary GitHub-style pipe tables, including inline markdown and
  math inside table cells. Preview pages and dashboard pages should use the browser width rather
  than a narrow fixed content column; tables should default to `width: 100%` and wrap long cells
  within the available viewport, with horizontal scrolling only as a fallback for genuinely
  unbreakable content.
- Keep link groups tidy: render 1-3 links directly, but collapse longer link groups into a
  disclosure section so dense nodes do not dominate the dashboard.
- When a markdown file is meant to be read in the dashboard preview, write equations in normal
  LaTeX math delimiters such as `$...$`, `$$...$$`, `\(...\)`, or `\[...\]`. Do not fence
  mathematical content inside code blocks unless the intention is to show the literal source.
- Do not wrap reader-facing mathematical statements in backticks just to make them stand out. A
  span such as `` `NCTD<=VC` `` is rendered as literal code and MathJax will intentionally skip it;
  write `$NCTD \le VC$` or `\(NCTD \le VC\)` instead. Reserve backticks and fenced blocks for
  filenames, shell commands, JSON keys, literal identifiers, and source snippets.
- Current renderers may best-effort coerce obvious relation-style code spans in Markdown previews
  into inline math for legacy files, but do not rely on that compatibility path when writing new
  Markdown.
- The generated HTML should be static, linkable, and readable on mobile.
- The dashboard should show the current structure, not a chronology of every past attempt.
- Separate the unrestricted goal from the hypotheses of a proved subfamily. A special-case
  construction must not appear to be an equivalent reduction of the whole target. Keep an
  uncovered input as supporting evidence unless a named structural claim makes it a decisive
  adversary. In `latest_progress`, lead with scope or mechanism changes and place verification
  counts in supporting evidence rather than using them as progress metrics.

## Recommended manifest shape

- `title`: dashboard title.
- `description`: paragraph or short description of the campaign. This replaces the older
  `subtitle` field, which remains supported as a backwards-compatible alias.
- `version`: optional monotonically increasing integer campaign-state version.
- `updated`: optional date stamp.
- `goal`: markdown string stating the current exact goal.
- `honest_assessment`: markdown string giving the current candid status relative to the goal,
  including what is proved, what remains open, and what is only evidence or a proxy.
- `latest_progress`: markdown string distinguishing advances on the original target, reusable theory,
  subsequent learning, and local activity. State what each achieved; a new theorem label, route closure,
  sharper falsifier, or equivalent reformulation is not automatically such an advance. Use
  `honest-conjecture-resolution` for progress accounting; no new manifest fields are required.
- In existing summary fields, distinguish the mathematical contribution, confidence in its proof,
  and effect on the target or independent theory objective. Keep task completion separate. An
  independent audit updates confidence at its received scope; it does not move the discovery date.
  State the first unproved indispensable implication and what next result would change effort.
- `goal_assessment`: optional backwards-compatible alternative. It may be a markdown string, or an
  object with `goal` and `assessment` fields. Prefer the separate `goal` and `honest_assessment`
  fields for new manifests.
- `nodes`: top-level tree nodes.
- Each node may contain:
  - `label`
  - `kind` such as `classification`, `problem`, `route`, `reduction`, `conjecture`,
    `counterexample`, `lemma`, `tool`, or `archive`
  - `status`
  - `updated_version`: optional integer recording the dashboard version at which this node was last
    materially touched
  - `method_role`: optional compact phrase identifying the branch's current methodological role
  - `description`: paragraph or short markdown description of the node. The older `summary`,
    `summary_md`, and `summary_file` fields remain supported as aliases for existing manifests.
  - `description_md` or `description_file` for longer markdown prose or source-backed descriptions
  - `links` as `{label, href}` objects
  - `children` as nested nodes

## Dashboard language discipline

- Dashboard labels and summaries are mathematical communication, not internal scratchpad shorthand.
  Keep them compact, but make every compact phrase precise enough for a reader who has not followed
  the whole chat history.
- Use the most precise node kind available. Prefer `classification` for a branch that classifies a
  family of objects, and `problem` for a branch that records a named open problem or subproblem.
  Use `route` only when the node really is a proof approach rather than a mathematical object,
  problem, classification, or reduction.
- Avoid generic proof-process words in labels or summaries unless they are qualified, contextualized,
  or formally defined in the linked ledger/TeX file. Terms that often become unclear include
  "gate", "obstruction", "proof debt", "proof obligation", "assay", "certificate", "finite
  certificate", "boundary", "sector", "mechanism", "proof spine", "proof package", "route",
  "pipeline", and "stratum".
- These words are not banned. Use them when they are standard or precise: for example a topological
  boundary, graph boundary, boundary operator, boundary condition, defined geometric sector,
  parameter sector, named obstruction, or formal certificate. Otherwise replace them with the
  actual mathematical content, such as "remaining lemma to prove", "necessary condition",
  "counterexample family", "main reduction", "induction step", "comparison lemma", "auxiliary
  construction", or "case split".
- Prefer node labels that name the mathematical state directly: `Alexander-dual CM criterion
  proved`, `endpoint-separation lemma stalled`, or `rank-3 counterexample search active` is better
  than `CM gate`, `boundary obstruction`, or `finite certificate route`.
- Use `method_role` to expose risk when a branch is only a census, proxy, or local test. Such active
  nodes should have a linked stop rule, native-structure audit, or local-to-global compatibility
  gate in the ledger.

## Status semantics

- Use stable status words such as `active`, `stalled`, `proved`, `refuted`, `draft`, `tool`,
  `verification`, `historical`, or `closed`.
- Keep the status vocabulary small and consistent across the tree.
- A proved construction leaf should display its input hypotheses. Proved assembly leaves do not
  prove their parent existence target while joint input availability remains open. Link shared
  dependencies to one proof owner rather than counting each appearance as another advance.
- If a route changes status, update the manifest and regenerate the HTML in the same pass.

## Rendering workflow

- Maintain the manifest in the repo next to the route artifacts, typically as `dashboard.json`.
- Render it with `scripts/render_conjecture_dashboard.py`.
- For active multi-leaf campaigns, prefer version staleness over wall-clock staleness:
  - bump the top-level `version` when the displayed campaign state changes;
  - set `updated_version` on each active node materially changed by that round;
  - use `version - updated_version` as a navigation aid, not as a measure of mathematical progress
    or an instruction to revisit low-priority leaves. Route reviews use cumulative effort and the
    time since the last goal advance; cosmetic touches do not renew a route.
- If the renderer supports it, use an explicit command such as
  `scripts/render_conjecture_dashboard.py --bump-version --touch "Leaf label"` so version bumps and
  node touches are reproducible.  Do not bump the version for a render-only refresh.
- Commit the manifest and the generated HTML together when the dashboard is part of the repo record.
- Do not commit generated Markdown preview pages such as `notes.md.html`; they are reproducible
  side outputs and should be ignored by `.gitignore`.
- Link the generated `dashboard.html` from the repo homepage or site index.

## Maintenance rules

- When the shared knowledge index is configured, link relevant stable result cards and their
  source owners. Use `research-knowledge` to check prior results, corrections and freshness before
  promoting a dashboard claim. Keep the dashboard a summary rather than another result database.
- Before adding a result node or rewriting `latest_progress`, compare the claim with the campaign's
  existing-result map, earlier rounds, and relevant related-repo results. Follow source links to the
  actual statements and corrections; the dashboard alone is not an exhaustive search index. Use
  `honest-conjecture-resolution` for the search procedure.
- Reuse an existing node for the same result; link imported results to their originating proof and
  record the original round/date when known. Label rediscovery or rechecking as reuse/verification,
  preserving the last genuine advance. For an extension, new proof, or application, state the precise
  addition over the earlier result. A new label or a move between repos does not establish novelty.
- Link the campaign's compact result map or inventory from an appropriate existing description or
  link group. Keep detailed search coverage and provenance in that record; no new manifest fields
  or duplicate chronological log are needed.
- Keep the tree shallow enough to scan quickly.
- Avoid duplicating the ledger; link to it instead.
- Keep `goal`, `honest_assessment`, and `latest_progress` accurate when displayed claims change. These
  fields are the dashboard's executive summary and should be readable before opening any tree node.
  They should usually fit in a few short paragraphs total; if they start to sprawl, compress them
  into the current target, current status, and latest proof-contract delta.
- If literature packets materially affect a route, use `shared-literature` and link to the
  shared index or canonical packet, using a compatibility view when needed for existing URLs.
- Put durable status changes in the ledger or TeX file first, then reflect them in the dashboard.
- Use the dashboard to answer three questions quickly: what is alive, what is dead, and where does
  each branch live in the route tree.

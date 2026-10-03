---
name: fork-idea-branch
description: Split an idea or active research path into two or more new research product-path stubs after alignment approval; preserves the source path by default and archives it only when --archive is passed
type: planning
version: v0.1
required_conventions: [alignment-page]
argument-hint: "[branch/product-path specs...] [--source <path-id>] [--from <skill>] [--archive] [--reuse <artifact-types>]"
---

# Fork Idea Branch

Invoke as `$fork-idea-branch`.

Use this skill when one idea, research path, or customer-discovery result should split into multiple related product paths. Typical use: customer discovery surfaces three promising ICPs that require different products, so the user wants separate `research/{product-path}/` starts and separate `$idea-scope-brief` kickoff prompts for each path.

The packaged command is `$fork-idea-branch`; if a project exposes `$fork-branch` as a compatibility name, treat it as this same workflow.

This skill creates research product paths, not git branches. Use "branch" only as user-facing shorthand for the proposed product-path list.

## Operating Modes

- **Default additive mode:** after final alignment approval, create two or more new `research/{slug}/` stubs and update `research/.progress.yaml`. Keep the source path in place.
- **Archive mode (`--archive`):** include source-path archival in the alignment page and, after final approval, move the source path to `research/_archive/{old-slug}-pre-fork/` before creating the new stubs.

Do not archive, move, delete, or mark an existing source path archived unless the invocation included `--archive` and the final compiled alignment-page YAML approved that archival.

## Process

### 0. Resolve Source And Branch Inputs

Read `research/.progress.yaml` when present. Normalize legacy fields: read `active_path` as `active_paths`, treat legacy `abandoned` as `archived`, and exclude paths under `research/_archive/` from active-source selection.

Parse `$ARGUMENTS` for:

- proposed branch/product-path specs: label, desired stub slug/name, ICP or product hypothesis, and optional notes
- `--source <path-id>`: the active product path or idea context being split
- `--from <skill>`: the skill or workflow that exposed the divergence
- `--archive`: opt in to archiving the source path after approval
- `--reuse <artifact-types>`: optional approved carry-forward candidates

If the branch list is incomplete, interview the user for:

- what diverged: ICPs, market segments, value wedges, product lines, or route experiments
- how many product paths to create, with minimum 2
- desired stub names/slugs for each path
- per-path notes or constraints the seed should preserve

If no active source path exists, continue when the user supplied enough source idea context in the invocation or interview. If both source path and source idea context are missing, ask for the idea/source context before building the alignment page.

Normalize slugs to lowercase hyphen-case. Prefer descriptive product/app path names over generic audience names when the supplied stub would be too vague. Validate there are no collisions with existing `research/{slug}/`, `research/_archive/{slug}/`, or manifest `product_paths[].id` entries.

### 1. Build The Alignment Page

Build `alignment/fork-idea-branch-{topic}.html` before any filesystem mutation. Follow `ALIGNMENT-PAGE.md` in this skill directory.

The page must verify:

1. **Source context and mode** - source path or source idea summary, triggering skill, and whether the source will be preserved or archived. In default mode, the proposed file changes must show no source-path move.
2. **Branch count** - exact number of product paths to create; it must match the user's supplied branch list.
3. **Branch names and slugs** - label, `research/{slug}/` path, and collision check for every branch.
4. **Per-branch seed content** - ICP/product hypothesis, pain point hypothesis, value wedge hypothesis, and user notes for each branch.
5. **Reuse decisions** - default is fresh stubs only. Any carry-forward artifact must be approved per branch and per artifact type, with contamination risk called out.
6. **Proposed file changes** - full inventory of directories, `fork-seed.md` files, manifest updates, optional source archive move when `--archive` is present, and fork memo path.
7. **Idea-scope-brief kickoff prompts** - a ready-to-paste `$idea-scope-brief {slug}` prompt for each branch that tells the next agent to read that branch's `fork-seed.md` and honor the branch notes.
8. **Post-approval route** - final restart checklist and the first recommended branch to run.

Pre-approval stop applies. Ask the user to review the page and provide final compiled response YAML. Do not scaffold, copy, archive, or update `research/.progress.yaml` until final compiled YAML has `approval_status: ready-for-agent-review` and no unresolved negative or clarification feedback.

### 2. Apply Final Approval

After final approval, apply the approved file changes exactly.

If `--archive` was approved:

1. Move `research/{old-slug}/` to `research/_archive/{old-slug}-pre-fork/`.
2. Update the source manifest entry:
   - `status: archived`
   - remove the source path ID from `active_paths`
   - `scope_path: research/_archive/{old-slug}-pre-fork/`
   - `archive_reason: forked-to-{slug-a}+{slug-b}[+...]`
   - `archived_at: <YYYY-MM-DD>`
   - `last_touched: <YYYY-MM-DD>`

If `--archive` was not approved:

1. Leave the source directory and source manifest entry in place.
2. Do not move the source path under `research/_archive/`.
3. Do not change the source status to `archived`.

### 3. Scaffold New Product Paths

For each approved branch:

1. Create `research/{new-slug}/_working/`.
2. Write `research/{new-slug}/_working/fork-seed.md` with ground-truth inputs only:
   - source idea or source path summary
   - source skill (`--from` or `user-initiated`)
   - branch label and slug
   - ICP/product hypothesis
   - pain point hypothesis
   - value wedge hypothesis
   - user notes and constraints
   - explicit unknowns for `$idea-scope-brief` to resolve
3. If carry-forward was approved for this branch, copy only the approved artifacts into `research/{new-slug}/` and prepend:

   ```html
   <!-- Carried forward during fork on YYYY-MM-DD. Original assumptions may not hold for this path's ICP, market, or product direction. Review critically. -->
   ```

4. Update `research/.progress.yaml` with a `product_paths[]` entry:
   - `id: "{new-slug}"`
   - `label: "{branch label}"`
   - `scope_path: "research/{new-slug}/"`
   - `status: active` or `deferred`, respecting `max_concurrent`
   - `source_skill: "fork-idea-branch"`
   - `reason: "Forked from {source path or idea} after {trigger/source skill}: {brief rationale}"`
   - `archive_reason: null`
   - `archived_at: null`
   - `promoted_at: null`
   - `evidence_refs`: include the alignment page, fork memo, source path or source artifact, and this branch's `fork-seed.md`
   - `revisit_trigger`: null unless the branch is deferred
   - `next_skill: "$idea-scope-brief {new-slug}"`
   - `pipeline_stage: "idea-scope-brief"`
   - `last_touched: "<YYYY-MM-DD>"`

Add active branch IDs to `active_paths` up to `max_concurrent`. If adding all approved branches would exceed `max_concurrent`, set the excess branch entries to `status: deferred`, give each a concrete `revisit_trigger`, and state that those paths are parked until activated.

### 4. Write Fork Memo

Write `research/_working/fork-memo-{YYYY-MM-DD}.md` with:

- source skill or `user-initiated`
- source path or source idea summary
- mode: default additive or `--archive`
- source action: preserved or archived, including archive path when applicable
- branches created: slug, label, status, and notes
- rationale summary
- reuse decisions per branch
- full artifact inventory
- idea-scope-brief kickoff prompts
- restart checklist

### 5. Emit Restart Checklist

End with the branch kickoff prompts and one recommended next command:

```text
$idea-scope-brief {slug-a}
$idea-scope-brief {slug-b}
```

Recommend sequential execution unless the user explicitly wants parallel research sessions. Each branch should run its own idea-scope-brief from its own `fork-seed.md` to avoid blending incompatible ICP/product assumptions.

## Constraints

- Does not run `$idea-scope-brief` or any downstream skill.
- Does not merge research across product paths.
- Does not create git branches.
- Does not create task entries in `tasks/todo.md`; the restart checklist is the handoff.
- Does not archive source research unless `--archive` was passed and approved.
- Uses manifest terminology `product_paths` and `active_paths`; treats branch as user-facing shorthand only.
- Distinguishes itself from `$product-line fork`: `$product-line fork` adds one portfolio path, while this skill splits one idea/source into multiple reviewed `research/{slug}/` stubs with per-branch kickoff prompts.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/fork-idea-branch-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention.

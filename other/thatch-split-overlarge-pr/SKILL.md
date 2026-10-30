---
name: thatch-split-overlarge-pr
description: Split already-completed work from an overlarge PR into human-reviewable, release-safe PRs. Use when the user asks to split a large existing branch/PR, break up completed work, or turn an oversized PR into multiple PRs. Do NOT use for planning brand-new work before code exists.
---

# Splitting an overlarge PR

Use this skill when the work is already done and the PR is too large for a human to review well. The job is not to redesign the feature. The job is to cut the completed diff into human-digestible PRs with safe seams.

The key constraint: **do not create a stacked PR chain**. Every PR should target the main branch. Some PRs may have to merge before others, but the dependency is merge order, not branch topology. After each part merges, the next part rebases or is rebuilt onto main.

The second key constraint: **every seam must be release-safe**. Assume a release can happen after any part merges and before the next part lands. If two parts need each other bidirectionally to be correct in prod, the split is invalid. Redesign the seam or keep that work in one PR.

## Definitions

- **Part** - one PR produced by the split.
- **Seam** - the boundary between two parts.
- **Release-safe seam** - the repo can ship after the earlier part merges, before the later part lands, without broken behavior, broken schema, broken generated artifacts, or operator confusion.
- **Merge order** - the order parts should land in. Merge order is allowed.
- **Stacked PR** - a PR whose base is another feature branch. Do not do this for this workflow.

## Split goals

Optimize for human review first. A good split gives reviewers one coherent idea at a time: schema scaffold, write path, read path, cleanup, docs, tests, or tooling. Avoid splitting by arbitrary file count. Avoid "all backend in one PR, all tests in another" unless both are independently meaningful and release-safe.

Each part should be:

- **coherent** - one reviewable purpose;
- **idempotent** - safe if applied once, retried, or observed in prod before the next part;
- **mergeable to main** - target main, not another feature branch;
- **release-safe** - production remains valid if release happens after this part;
- **bounded** - small enough that a reviewer can understand it without reading the whole original diff.

## Process

1. **Inventory the completed diff** - compare the oversized branch/PR against main. Identify files changed, commits, generated artifacts, tests, docs, migrations, flags, APIs, and operational wiring. Do not start moving code yet.
2. **Build a dependency graph** - list what depends on what. Mark hard dependencies (cannot work without), soft dependencies (nice ordering), and bidirectional dependencies (invalid seam unless redesigned).
3. **Choose release-safe seams** - cut only where the intermediate repo state can ship. For each proposed seam, ask: if a release happens right here, what breaks? If the answer is anything user-visible, data-corrupting, migration-breaking, or operator-confusing, move the seam.
4. **Order the parts** - choose merge order from low-level to high-level when possible: scaffolding, compatibility shims, write paths, read paths, behavior switch, cleanup. The order may be strict, but each part still targets main.
5. **Extract parts mechanically** - create branches or commits for each part from main. Use cherry-pick, restore, or patch extraction; do not hand-rewrite behavior unless the seam requires it. Preserve generated artifacts with the source change that needs them.
6. **Validate each part independently** - run the relevant tests for that part against its own branch. If a part only passes when a later part is present, the seam is wrong.
7. **Write PR descriptions with project context** - every part needs its own normal PR description plus a final `## PROJECT PARTS` section linking the other pieces and stating merge order.

## Designing release-safe seams

Good seams usually look like this:

- **nullable schema before writes** - add nullable columns or tables before code writes them;
- **dual-read or fallback read before switch** - teach readers to handle both old and new shapes before writers change behavior;
- **dual-write before read switch** - write both representations while old readers still exist;
- **feature flag or no-op scaffold before enablement** - merge inert wiring before the behavior flips;
- **cleanup last** - remove shims, flags, dead code, and compatibility paths only after the new state is live and no rollback path needs them.

Bad seams usually look like this:

- **bidirectional dependency** - PR A only works if PR B is also present and PR B only works if PR A is present;
- **required generated artifact split from source** - generated models, migration SQL, OpenAPI output, or snapshots land without the source change that makes them true;
- **schema requires code not yet merged** - NOT NULL, unique indexes, enum narrowing, or data assumptions land before the data/code can satisfy them;
- **code writes data old code cannot read** - a release between parts would strand readers;
- **cleanup before consumers are gone** - deleting shims, flags, or old paths while earlier release states can still need them.

## No stacked PRs

Do not target part 2 at part 1's branch. Do not build a tower where reviewers must read PR 1 before GitHub can even compute PR 2 against main.

Allowed: "Part 2 should merge after Part 1." Part 2 still targets main when opened. If Part 1 has not merged yet, keep Part 2 local or open it as draft against main knowing it may include temporary overlap; update/rebase it after Part 1 lands.

Use merge order to communicate sequencing. Use branch topology only for isolation during local extraction, not as the review shape.

## Project parts section

Every split PR should end with a final section called `## PROJECT PARTS`. This is for humans. It is not a stacked-PR instruction; it is the map for a multi-part change.

Each entry should be a mini didactic build-up, not just a link. The reader should understand how the system state advances from one part to the next: what this PR adds, what state it leaves behind, and what gate must be satisfied before the next part can land or ship.

Format:

```md
## PROJECT PARTS

1. [PLAT-123 / Part 1: nullable schema + generated artifacts](https://github.com/org/repo/pull/111) - adds `foo_id` as nullable and regenerates models; release-safe scaffold, no behavior uses it yet.
2. [PLAT-124 / Part 2: backfill existing rows](https://github.com/org/repo/pull/112) - fills `foo_id` for existing data; **IMPORTANT:** must deploy and complete in prod before Part 3.
3. [PLAT-125 / Part 3: enforce non-NULL](https://github.com/org/repo/pull/113) - adds the non-NULL constraint once Part 2's backfill reports zero missing rows in prod.
4. [PLAT-126 / Part 4: cleanup compatibility paths](https://github.com/org/repo/pull/114) - removes temporary fallback code after the constrained shape is live.
```

Rules:

- Include all parts, including the current PR.
- Mark not-yet-open PRs as `TBD` until links exist.
- State merge order, release-safety, and deploy/runtime gates inline. If a later PR depends on a production condition (backfill complete, flag enabled, old jobs drained), say so in the entry.
- Use `**IMPORTANT:**` for hard gates that reviewers must not miss.
- Keep this section final. Nothing follows it except an optional `# robots.txt` section if automated reviewers need machine-only context.

## Review checklist before opening the split PRs

- Every part targets main.
- Every part has one coherent review purpose.
- Every part can pass its own relevant tests without later parts.
- Every intermediate merge state can be released.
- No generated artifact is separated from the source change that requires it.
- No cleanup happens before all consumers of the old path are gone.
- The `## PROJECT PARTS` section appears in every PR description and links every known part.

## Anti-patterns

- **Stacked PR by another name** - using base branches to enforce order. Use merge order, not branch topology.
- **Review-size split only** - splitting by file count while leaving behavior coupled across parts.
- **Tests later** - a part lands without the tests that prove its own behavior.
- **Cleanup early** - deleting compatibility before the new state is fully live.
- **Release-blind seam** - "it works once all parts merge" is not enough. It must work after each part merges.
- **Bidirectional dependency** - if PR A and PR B both require each other, they are one PR or the seam must be redesigned.

---
name: astroray-architect-round
description: Run an architect-first Astroray delivery round that selects an eligible package, delegates bounded work efficiently, and verifies visual and engineering evidence before autonomous delivery.
---

# Astroray architect round

Use this for an autonomous development round, not a narrowly assigned package.
Read `AGENTS.md`, then the live planning hierarchy in order: `STATUS.md`,
`NEXT_STAGE_REPORT.md`, and `ROADMAP.md`. Use `$astroray-index` and current
git/GitHub state to exclude in-flight work and select the most valuable eligible
package. Read the canonical `architect`, `pkg-ship`, `delegate`, `verify`, and
`visual-check` workflows through `$astroray-workflows` as each becomes relevant.

First produce a compact architect decision: why this package is next, its
dependencies, acceptance gates, risks, and whether a spec/research refresh is
needed. Then execute the selected package in an isolated worktree. A material
priority conflict, pause directive, or genuine scope change requires owner input;
ordinary execution should proceed autonomously.

Use Astra for architecture, integration, and final evidence review. Delegate
only bounded work through `astroray-opencode-delegator`, which resolves the
current model tiers dynamically: grunt tasks (research indexing, docs, reports,
mechanical hygiene), well-specified implementation slices in isolated worktrees,
and read-only pre-review. Treat returned evidence as leads, not authority. Use a
different high-tier lineage for required independent sign-off. Never delegate
visual judgment to text-only workers.

Keep at most two implementation worktrees active in a round and serialize
CUDA-heavy build/render verification through the GPU lock. For visual, material,
spectral, viewport, or image-output changes, save representative output and use
the visual-check workflow in addition to numerical gates. Investigate a failed
test or reference as evidence, not automatic proof that new code is defective.

If a useful tangent is small and independently verifiable, delegate it as a
separate bounded task. Otherwise use `file-followup` to create a scoped package;
never smuggle it into the selected package diff. This includes renderer/build
performance, test throughput and relevance, benchmarks, repository hygiene,
agent workflows, hooks, MCPs, indexing, and tracker automation.

After the package's documented gates, caller/binding sweep, independent review,
and any required hardware/visual verification pass, commit, push, open the PR,
and merge according to the canonical workflow. Update the live planning sources
only with evidence-backed state and report the next eligible package.

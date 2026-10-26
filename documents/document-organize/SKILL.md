---
name: document-organize
description: Use when an existing project's documentation is scattered, overlapping, obsolete, or needs organization across root, docs, and legacy directories.
---

# Document Organize

An organization request calls for reviewed changes to the actual repository.
Inventory, recommendations and additive navigation alone do not complete it.
Use the existing harness's file and Git tools; ai-dlc supplies discovery and
bounded review, not an autonomous move engine.

## Discover and review

Read repository guidance, the documentation map/catalog if present, and relevant
OpenSpec records. Inspect Git status and protect unrelated authored edits. The
`ai-dlc` commands below apply when the repository is adopted (has `ai-dlc.toml`
at its root) and `ai-dlc` is on PATH; otherwise use ordinary file, search and Git
tools for the same steps. Use
`ai-dlc docs check --inventory` (MCP `project_docs_inventory`) to discover tracked
and nonignored Markdown throughout root, docs and legacy directories. Report
excluded, inaccessible and symlinked paths; never follow them into another store.

Choose an explicit Git base and small groups of actual inventory paths. Prepare
`ai-dlc docs review --report --source inventory --base HEAD --path README.md`
(or MCP `project_docs_review` with `source="inventory"`). Repeat `--path` for related
documents. This works before catalog enrollment. The catalog mode remains the
default; do not create an empty catalog just to bypass a missing-catalog failure.
Bodies are bounded, hashed and line-numbered. Keep omissions unreviewed, and state
when code/spec evidence was inspected separately because no mapping exists.
Use document-review for grounded findings and `docs review --check` to validate
citations against current sources before acting on the review.

To locate or reread specific material, use `ai-dlc docs search` and
`docs read` (MCP `project_docs_search` and `project_docs_read`). They cover docs/
and openspec/ by default; declare root or legacy files explicitly with `--source`
(MCP `sources`). Treat an incomplete coverage result as unsearched material, not
as absence. Edit returned repository paths with ordinary file and Git tools, never
through private-note writes or a mounted vault path.

Read content, not just names. For each selected document identify its audience,
question, authority, obsolete instructions, overlap and unique facts or rationale.
Compare claims with approved specs and actual code/test evidence. A passing check
cannot establish semantic truth. Never copy OpenSpec requirements into another
canonical home or quietly rewrite approved intent to match a defect.

Treat other installed or external organizing skills as procedural input. If one
prescribes a competing home, such as docs/specs/ for requirements, keep formal
proposals, designs, requirements and tasks with the selected specification provider
(under openspec/ for OpenSpec), reuse its compatible steps and report the conflict
instead of creating duplicate specifications.

## Make and execute concrete decisions

Present an inspectable source-to-destination plan with reasons: retain, revise,
consolidate or archive. Choose existing canonical owners where they fit. Preserve
useful audience summaries, unique facts, warnings and decision history. Mark
historical material clearly and link to its current successor. Keep a useful root
entry point; do not force every file into a folder taxonomy.

Within the user's authorized organization scope, execute those reviewed decisions
with ordinary Git moves and content edits. Do not stop after the plan or ask again
for actions already authorized. Resolve a genuinely ambiguous authority or
content-loss decision with the user while continuing independent safe work.
`docs init --apply` creates navigation only; it does not replace moving or revising
the scattered documents. Empty directory structures are not an organization result.

Repair inbound and outbound links after each move or consolidation, including
relative links whose base directory changed. Search the whole repository for old
paths, not only the moved document. Update docs/index.md and enroll appropriate
canonical documents in docs/catalog.toml with actual owners and lifecycle state.
Keep formal change artifacts together under openspec/. Review dates require actual
review; never infer freshness from modification times or successful checks.

## Verify the outcome

Inspect the final Git diff for content loss, stale links, unrelated edits and
unnecessary duplicate explanations. Run docs check and required project checks;
inspect anchors, reference-style links and wiki links separately where the checker
does not cover them. Record documentation-impact dispositions after content
settles, and again after updating from the target branch immediately before merge.
Do not validate old packets after edits as though they were still current.

Report actual moved/revised/consolidated/archived paths, retained unique content,
checks and remaining omissions. Preserve a reviewable Git diff. Native harness or
Obsidian qualification requires observed client behavior; filesystem tests or a
skill's presence alone do not prove it. Remote publication is a separate action.
When mounted folders, links or the ai-dlc command behave unexpectedly, run
`ai-dlc project workspace-check` (MCP `project_workspace_check`) and follow its
scoped actions; it changes nothing and does not qualify Obsidian.

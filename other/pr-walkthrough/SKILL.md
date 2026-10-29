---
name: pr-walkthrough
description: Walk a reader through a pull request, branch, or set of changes as if they were a senior engineer with no context on the work. Produces a Markdown document with the code flow before the change (snippets and a diagram), the problem substantiated with real evidence, then each change and why it fixes the problem. Use when asked to "walk me through" or "give me a tour of" a PR or branch, to explain a change to someone who was not there, or to understand what a branch does before reviewing it. Not for writing PR descriptions, reviews, or crit stories.
---

# PR walkthrough

Create a walkthrough for a senior engineer who has no context and little time. The summary should show the change's shape at a glance; the rest of the document should let the reader verify each claim against the source.

## Workflow

1. **Set the scope.** Identify the PR, branch, or commit range and its base. Read the commit messages, full diff, and linked issue, incident, or discussion. State the claimed problem in one sentence.
2. **Trace the original flow.** Follow the relevant request or data path at the base revision. Quote source with `git show <base>:<path>` and cite each excerpt with `path:line`. Add one Mermaid sequence or flowchart when the flow has more than two hops; omit the diagram for shorter flows.
3. **Prove the problem.** Gather direct evidence such as measurements, traces, flamegraphs, screenshots, or incident timelines. Apply the evidence rules below. If proof is missing, name what would establish the claim and ask for it; do not fill gaps with estimates or reconstructed evidence.
4. **Explain the changes.** Group related hunks by theme, not by file. For each theme, show what changed, quote the relevant after-state, explain how it addresses the problem, and state what it leaves uncovered. Repeat the diagram with the change applied only when the flow's shape changed.
5. **Cover risk and verification.** Explain rollout, rollback, and the signals that would show the change is working.
6. **Write the summary last.** Put it at the top: three to five sentences that stand on their own, followed by a `tl;dr` list of the themes.

## Evidence

- Quote snippets from the actual revisions and cite them as `path:line`. Do not present paraphrases as code quotations.
- Include captures only when the change claims a performance or behavior difference. Take them yourself or link to originals in the PR, issue, dashboard, or discussion.
- Give every number a source. If it was not measured or linked, omit it or label it as the author's claim.
- When evidence is unavailable, state what would prove the point and ask for it. Never invent, estimate, or reconstruct evidence.

## Document format

Write one Markdown file at `~/code/scratch/YYYY-MM-DD-<slug>/walkthrough.md`, using today's date and a one-to-three-word slug. Create the directory and report the file path when finished.

```md
# <Change title>

<Summary: 3-5 sentences.>

tl;dr
- <theme 1>
- <theme 2>

## Before
<Flow with source snippets; diagram if it has more than two hops.>

## The problem
<Evidence, with a source for each item.>

## The changes
### <theme 1>
<What changed, after-state snippet, why it helps, and what it does not cover.>

## Risk and verification
<Rollout, rollback, and signals to watch.>
```

## Completion

The walkthrough is complete when every snippet cites a real revision and line, every number and capture has a source or is labeled unverified, the diagram follows the hop threshold, the summary stands alone, and the output path is reported. Post nothing anywhere unless the user asks. If asked, use the `github-attachments` skill to attach the document or images to the PR, or author a `crit story` as a companion diff tour.

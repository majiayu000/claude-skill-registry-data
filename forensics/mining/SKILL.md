---
name: mining
description: Mine, compare, or re-crawl approved external robotics repositories into local evidence-cited Robium observations for later skill absorption.
---

# Mining

Mine for transferable decisions, not code volume.

## Choose what is worth reading

- Candidate discovery and a one-line registry entry are read-only triage.
  Survey or deep-read only a repository the user named or approved in
  `learnings/SOURCES.md`.
- Start with a survey of the tree, active code paths, documentation, examples,
  tests, and license. Spend deep-reading effort only where the survey finds a
  decision that could change a Robium skill.
- Prefer official/vendor sources. Use comparative reads when independent
  projects answer the same question; use a re-crawl when a previously mined
  source changed.
- Read [WORKFLOW.md](WORKFLOW.md) for the survey, deep-read, comparative, and
  re-crawl mechanics.

## Keep only reusable evidence

- Keep patterns, orderings, failure discriminators, integration shapes, and
  configuration decisions that transfer beyond the source project.
- Drop project names, incidental ports, arbitrary tuning, style, and other
  local choices unless they explain a reusable boundary.
- Every observation cites a pinned repository commit, path, line range, and a
  verbatim source excerpt that the citation verifier can find.
- Read [EVIDENCE.md](EVIDENCE.md) for source-authority thresholds, conflicts,
  licensing, placement, and new-skill proposals.

## Preserve the learning boundary

- Output gitignored local observations and source-registry updates, never
  direct skill edits. Absorption belongs to `learning-loop` and remains
  separately reviewed.
- Compare findings with existing skills and observations. Record disagreement
  with both provenances; do not silently replace Robium field evidence with an
  upstream idiom.
- Point to source code by default. Vendor code only when it is short, genuinely
  useful as a maintained example, and its license and attribution permit it.
- Do not crawl issue trackers or commit history as part of the current mining
  workflow.

## Done

- The registry records the pinned commit, crawl date, status, and the skill or
  reference files that ultimately retained the finding. Local observation IDs
  are not repository history.
- Citation and observation checks pass for every retained finding.
- Each finding names the owning skill or explains why no current skill owns it.
- Temporary clones and survey reports remain outside the committed plugin.
- End with a short handoff: report how many local observations were saved and
  how many are `ready` versus `tentative`, then say that the next step is to
  run `learning-loop` to distill ready findings into existing skills or route
  a justified new-skill proposal through `skill-author`. Ask whether the user
  wants that absorption run in a background subagent; do not start it without
  approval.

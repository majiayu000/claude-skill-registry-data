---
name: plan-mode-research
description: Research a focused factual or technical question. Use when the user asks to look up, verify, or compare a bounded claim with current evidence.
license: MIT
---

# Research

Answer the question that was asked, with enough evidence to act on it.

1. Define the exact question and the facts that would answer it. Note version, date, platform, or environment constraints that could make an otherwise correct source irrelevant.
2. Consult primary sources first: official documentation, release notes, repository code, standards, or original data. Inspect the relevant passage, not only a search snippet. Use another source when a claim is disputed or a single source cannot establish it.
3. Check each decision-critical claim against its source. Separate what the source states from your inference; identify contradictions or missing evidence without smoothing them over.
4. Lead with the answer, then the supporting links or file paths and any material limit. Finish when every material claim is supported or explicitly marked unverified.

Research is read-only unless the user separately requests an edit. Do not create a plan, install a tool, or change the project as a substitute for answering the question.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.

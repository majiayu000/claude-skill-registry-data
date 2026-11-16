---
name: research
description: "Investigate a question using primary sources and leave a cited, reusable research note."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-11-01"
  sources: "mattpocock/skills 4ae2317ddb22b046e26455e4f9c9b3aaaf62212d skills/engineering/research/SKILL.md; honey-stack source verification and tool routing"
---

# Research

Answer one decision or question from sources the reader can inspect. For the actual APIs of already-declared dependencies, use `opensrc`; for wider questions, comparisons, unfamiliar technology or disputed facts, use this workflow. Research does not authorize implementation, account creation or publication.

## 1. Frame the decision

Read the user's constraints and relevant project docs. Write the question, the hard exclusions, the date-sensitive claims, and what evidence would settle the decision. An option that fails a hard constraint cannot win the ranking.

Choose the smallest useful output: a direct answer for a narrow lookup; a reusable note for a multi-source investigation. Use the repo's existing research location, otherwise `docs/research/YYYY-MM-DD-<topic>.md`. When repo writes are not authorized, keep the answer in chat or the host's scratch-artifact location.

Done when: the scope and exclusions are explicit, and the destination matches the request.

## 2. Find the sources

Use available Exa tools for deep, current, multi-source or code discovery work. If unavailable, say so once and use the available search tools. Follow discovery results to primary sources: official documentation, source repositories, specifications, first-party APIs, papers or original datasets. Use `gh` for GitHub reads.

Read the relevant pages or source files, not just snippets. Check installed versions and source revisions for technical claims, and both publication and event dates for changing facts. Record inaccessible sources; do not fill their contents from memory. Conflicting authoritative sources remain a disagreement until version, date or context resolves it.

Done when: each important claim has a source that directly supports it, including relevant version/date context.

## 3. Compare and qualify

Separate measured results, source statements and your inferences. Cross-check decisive claims with another authoritative source when one exists; if only one source supports a claim, label that limitation rather than inventing corroboration. A project's README and its marketing page are not independent confirmation.

Use [the note format](references/note.md) for investigations. Cite the supporting source beside each claim, include tradeoffs and rejected options, and explain what evidence would change the recommendation. Keep secrets, private session quotes and customer data out of external search queries and shared notes.

Done when: the recommendation satisfies the hard constraints, and uncertainty is visible beside the affected claim.

## 4. Hand off

Give the answer first and link the note if one was created. `grill` can use unresolved product choices; `plan` can consume confirmed constraints and findings. Re-check unstable facts before later implementation rather than treating the note as permanently current.

Done when: the reader can act on the answer and find its evidence without repeating the research.

---
name: why
description: Investigate why an existing design, constraint, or behavior was introduced using Git history, PRs, issues, and ADRs. Separate recorded rationale from inference; use how for current execution flow.
license: MIT
---

# Why

Explain the forces behind a design from evidence. This is read-only research,
including when another skill delegates it.

## Establish the lineage

1. Name the decision and locate the code that embodies it. Use
   [how](../how/SKILL.md) only if the current behavior is not understood.
2. Read relevant design documents and nearby history. Start with bounded
   `git log --oneline -- <path>`, targeted blame, and selected commit patches.
   Follow renames and earlier changes when the latest edit does not explain
   the decision. Do not fetch, switch branches, or change the working tree.
3. Follow relevant links to PR discussions, issues, and ADRs through available
   read-only tools. Resolve the repository/provider first; GitHub is not assumed.
   Reading a related private record does not authorize sending repository data
   to a different service.
4. Expand to other connected sources only when they could answer a material
   gap. Do not require chat, observability, or analytics access for every question.
   Do not install connectors or contact people.
5. Cross-check dates, identities, and the code revision against the explanation.
   A later description may explain a revision, not the original introduction.

Stay sequential for a narrow question. For independent evidence trails that
benefit from delegation, use bounded read-only investigators if permitted.
Each receives the target, relevant anchors, scope limits, and the obligation to
report missing or contradictory evidence. Verify their citations yourself.

## Keep evidence categories distinct

- **Recorded rationale:** a source explicitly explains the decision. Cite it
  and identify which revision or period it explains.
- **Supported inference:** observations support a possible explanation, but no
  decision record establishes intent. State the inference and supporting facts.
- **Unresolved:** evidence is missing, inaccessible, stale, or contradictory.
  Preserve competing explanations when they matter.

A missing ADR, empty search, or unavailable PR is a coverage gap, not evidence
that nobody considered an alternative. Do not invent motivation from a symbol
name, comment, present-day advantage, or agreement among investigators.

## Return the answer

Answer the question first, with source links next to the claims. Include the
meaningful alternatives, unresolved questions, and a brief coverage statement.
Say what was actually searched and what was unavailable.

If the caller is planning a change, hand back constraints as Preserve / Change /
Avoid / Risk where supported. Do not treat historical intent as an immutable
requirement or turn the investigation into implementation.

Do not write notes, code, configuration, tickets, comments, or external messages
as part of this investigation. Return findings to the user or delegating caller.

## Source

Adapted from Lauren Tan's [pstack why](https://github.com/cursor/plugins/blob/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack/skills/why/SKILL.md).
Local changes: Git/PR/issue/ADR-first research, optional connected sources and
delegation, and strict separation of evidence from inferred intent. See [LICENSE](LICENSE).

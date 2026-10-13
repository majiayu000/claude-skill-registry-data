---
name: improve-codebase-architecture
description: Find evidence-backed architecture improvements within a named area or requested codebase survey.
disable-model-invocation: true
---

# Improve Codebase Architecture

Find architectural friction supported by current code, then recommend bounded
improvements. A review authorizes inspection and reporting, not refactoring or
glossary changes.

Use the named module or pain point. For a broad survey, use recent change history
and actual maintenance/test friction to choose areas; expand when evidence warrants.
Read relevant domain terms and ADRs. The codebase-design vocabulary helps evaluate
interfaces without banning the repository's normal terminology.

For each worthwhile candidate, identify affected files, the concrete friction,
a proposed direction, expected benefit, compatibility/migration cost and evidence.
Apply the deletion test carefully: does complexity disappear or merely move into
callers? Distinguish a supported recommendation from an untested hypothesis.

Present a concise comparison and strongest recommendation. Use an inline visual
when it clarifies structure. HTML is optional; `HTML-REPORT.md` points to the shared
artifact guidance. Do not create a report format merely to fill its components.

When an ADR conflicts, explain the new evidence that might justify revisiting it.
An interview, alternative-interface exercise or domain-document update happens
only when requested or already authorized, using the corresponding shared skill.
Do not automatically enter a grilling loop after delivering the review.

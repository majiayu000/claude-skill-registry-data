---
name: ai-security-paper-strategist
description: Strategy, writing, experiment organization, evidence validation, reproducible result plotting, LaTeX engineering, rebuttal, and submission preparation for computer-science and AI-security papers. Use for paper positioning, story reconstruction, titles, abstracts, introductions, methods, experiments, compression, claim-evidence checks, result figures, citations, LaTeX, rebuttals, and submission audits across attack, defense, benchmark, measurement, mechanism, agent-security, privacy, systems-security, and alignment or safety-evaluation work.
---

# AI Security Paper Strategist

Act as `author_strategist` unless the user explicitly requests reviewer mode. Treat scientific truth, decisive contrary evidence, fair baselines, and non-misleading presentation as hard constraints.

## Route the task

Read [release-principle.md](references/release-principle.md) first. Then classify the request with [task-routing.md](references/task-routing.md). Do not launch a project workflow for a local paragraph edit.

- For idea-only work, mark every claim as a hypothesis, compare two to four candidate stories, establish only a provisional paper contract, and plan the experiments required to turn hypotheses into evidence. Do not invent results or write result-dependent final prose.
- For existing experimental results without a paper, inspect code, configurations, logs, structured results, and tables before selecting the story. Create the publication assets and winning arena before Draft 0.
- For an existing paper, choose story reconstruction, full-paper revision, or the smallest local section route. Preserve LaTeX commands, labels, and citation keys; do not create project-level artifacts for a local edit.

- For a full paper or story reconstruction, follow [workflow.md](references/workflow.md).
- For publication assets, candidate stories, and competition choice, read [story-selection.md](references/story-selection.md) and [winning-arena.md](references/winning-arena.md).
- For paper structure and prose, read [narrative-architecture.md](references/narrative-architecture.md), [section-writing.md](references/section-writing.md), and only the requested section guide: [abstract.md](references/abstract.md), [introduction.md](references/introduction.md), [related-work.md](references/related-work.md), [method-writing.md](references/method-writing.md), [experiment-writing.md](references/experiment-writing.md), or [conclusion.md](references/conclusion.md).
- For page limits, read [compression.md](references/compression.md).
- For experiments, read [experiment-organization.md](references/experiment-organization.md) and [experiment-manifest.md](references/experiment-manifest.md).
- For AI-security work, select the paper type in [ai-security-paper-types.md](references/ai-security-paper-types.md), complete [security-setting-card.md](references/security-setting-card.md), and use [security-evaluation-design.md](references/security-evaluation-design.md). For LLM agents, also read [llm-agent-evaluation.md](references/llm-agent-evaluation.md). Use [security-impact-chain.md](references/security-impact-chain.md) to cap impact claims and [dual-use-and-disclosure.md](references/dual-use-and-disclosure.md) only when hazardous artifacts are involved. Route venue framing with [venue-router.md](references/venue-router.md).
- For result figures, read [result-figure-contract.md](references/result-figure-contract.md), [result-figure-style.md](references/result-figure-style.md), and [result-figure-qa.md](references/result-figure-qa.md). Use the bundled orange-green-gray palette and Matplotlib style.
- For citations and LaTeX, read [citation-workflow.md](references/citation-workflow.md) and [latex-workflow.md](references/latex-workflow.md), then run the relevant scripts.
- Enter [reviewer-mode.md](references/reviewer-mode.md), [rebuttal-mode.md](references/rebuttal-mode.md), or [submission-mode.md](references/submission-mode.md) only on explicit request.

## Execute the default full-paper workflow

1. Inventory real research materials and create `publication_assets.md`.
2. Generate two to four candidate stories and create `winning_arena.md`.
3. Select one primary story, one supporting story, a headline claim, and claims to avoid.
4. Create `paper_story.md` and `claim_evidence_map.md` from the bundled templates.
5. Organize experiments in `experiment_plan.md` and `experiment_manifest.json`.
6. Create `figure_plan.md`; require a figure contract for every result figure.
7. Build the narrative spine and all paragraph topic sentences before expanding prose.
8. Write Draft 0 to direct experiments; do not treat it as final prose.
9. Draft sections around claims and evidence, not research chronology.
10. After experiments and main figures stabilize, rewrite title, abstract, introduction, contributions, Figure 1 caption, and the headline-result paragraph together.
11. Compress by argumentative value and run engineering validation.
12. Activate optional modes only when requested.

## Enforce evidence boundaries

- Never invent experiments, results, citations, numbers, significance, system behavior, or deployment conditions.
- Never hide evidence that overturns the headline claim.
- Never manufacture advantage with unfair baselines, selective reporting, truncated axes, or misleading labels.
- Prefer deleting irrelevant material, moving secondary evidence to an appendix, narrowing a claim, changing the evaluation dimension, or reconstructing the story.
- State a necessary scope boundary when omission would mislead.
- Do not output reviewer attack lists, limitation inventories, internal audit labels, or self-weakening evaluations by default.

## Keep method figures user-defined

Follow [method-figure.md](references/method-figure.md) exactly. Do not supply an internal style, palette, layout, generator, prompt, or backend. Treat generation and LaTeX integration as separate tasks.

## Use deterministic tools

Run scripts from `scripts/` with `--help` first. Preserve source files and write generated outputs to user-selected paths. Use `validate_skill.py` only to validate a copy of this Skill; it is not a paper-quality gate.

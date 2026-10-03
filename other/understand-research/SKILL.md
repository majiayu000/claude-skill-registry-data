---
name: understand-research
description: Research external technical, architectural, dependency, standards, product, or business-domain context needed to understand a codebase, documentation repository, wiki, knowledge graph, diff, or implementation decision. Use when local evidence is insufficient and cited current sources would materially improve an Understand Anything analysis; do not use for unrelated general-interest research.
---

# Understand Research

Research the external context required to interpret the current project. Connect every useful source back to repository evidence, a knowledge-graph node, a dependency, a requirement, or a concrete decision.

## Boundaries

- Start from the codebase, documentation set, diff, or question already in scope.
- Inspect local evidence before searching externally.
- Research only uncertainties that can change the explanation, risk assessment, architecture choice, or implementation.
- Prefer current primary sources: official documentation, standards, specifications, source repositories, release notes, and research papers.
- Use reputable secondary reporting only when primary evidence is unavailable or a broader perspective is necessary.
- Do not use search snippets as evidence. Open and read the source.
- Do not bulk-copy sources. Paraphrase and link.

## Workflow

### 1. Define the research contract

State:

- the local artifact or decision being investigated;
- the user's intended outcome;
- three to five answerable sub-questions;
- what would count as sufficient evidence.

Ask at most one clarifying question when the answer would materially change scope. Otherwise make a reasonable assumption and proceed.

### 2. Build the local anchor

Identify the files, symbols, dependencies, graph nodes, configuration, logs, or diff hunks that created each uncertainty. Record what is already known locally and what requires external verification.

Do not research facts that the repository itself establishes more directly.

### 3. Search deliberately

Use the best currently available web-search, browsing, documentation, paper, or MCP tools. Do not require Firecrawl or Exa when other tools can retrieve the evidence.

For each sub-question:

1. Run one focused search using exact technical terms.
2. Open the strongest primary source.
3. Run a second search or consult a second source only when the claim is disputed, high-risk, drift-prone, or incomplete.
4. Read the relevant source section rather than collecting many shallow results.

Default to 5-12 useful sources for a substantial investigation. Expand only when the topic genuinely spans independent evidence domains. Source count is not a quality metric.

### 4. Maintain an evidence ledger

Track findings in this shape while working:

```text
Claim | Local anchor | External source | Source date | Confidence | Fact or inference
```

Use `High` confidence for direct, current primary evidence; `Medium` for converging but incomplete evidence; `Low` for a single weak source, ambiguity, or an inference with material gaps.

### 5. Cross-check and synthesize

- Cross-reference consequential claims.
- Separate documented behavior from observed repository behavior.
- Label inference explicitly.
- Reconcile version, platform, edition, and publication-date differences.
- Explain contradictions instead of averaging them away.
- Say `insufficient evidence` when the available sources do not support a conclusion.

When the project already has `.understand-anything/knowledge-graph.json`, map findings to relevant nodes or domains. Do not mutate the graph unless the parent Understand Anything workflow requires an update.

### 6. Deliver a decision-ready result

Use this structure unless the user requests another format:

```markdown
# Research question

## Answer
[Direct synthesis in a few paragraphs]

## Project impact
- [Finding -> affected file, component, graph node, or decision]

## Evidence
- [Claim] ([Primary source](url))

## Uncertainty
- [Gap, contradiction, or inference]

## Recommended next step
- [Smallest useful action]
```

For a long report, save the full artifact only when the user requests a file or the report would be unwieldy in chat. Always surface the answer, highest-impact evidence, and unresolved gaps in the response.

## Parallel research

For broad investigations with independent sub-questions, use separate GPT-5.6 Sol agent lanes when available. Give each lane a disjoint question and require raw sources plus local anchors. The parent agent must verify the sources, resolve contradictions, and write the final synthesis. Do not parallelize several agents over the same vague question.

## Quality rules

1. Source every material external claim near the sentence it supports.
2. Use exact dates for drift-prone information.
3. Prefer primary and official technical sources.
4. Distinguish source fact, repository fact, and model inference.
5. Report failed searches and evidence gaps when they affect confidence.
6. Never invent source counts, quotations, URLs, versions, or verification results.
7. Stop when the research answers the project question; do not turn coverage into an end in itself.

Workflow lineage: adapted for Codex App and GPT-5.6 Sol from the ECC `deep-research` skill.

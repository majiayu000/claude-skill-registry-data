---
name: storm
description: Use this skill for STORM-style multi-perspective research, contradiction mapping, evidence-grounded synthesis, and self-review. Trigger when the user asks for STORM, Stanford STORM, SOTRM, multi-perspective analysis, research briefing, deep research, topic outline synthesis, contradiction analysis, or a cited report built from web/corpus evidence.
metadata:
  version: 1.0.0
  author: wangwei17
  input: research topic 
  short-description: Multi-perspective research and synthesis
---

# STORM

Use STORM to research a topic through multiple perspectives, retrieve evidence, expose contradictions, synthesize an actionable briefing, and audit the result.

STORM here abstracts Stanford OVAL's "Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking" into an agent workflow. It preserves the core pattern: perspective-guided question asking, evidence retrieval, outline/synthesis, drafting, and polishing.

## When to Use

Use this skill when the task needs:

- A nuanced briefing on a broad, contested, or high-stakes topic.
- Research grounded in external sources or a user-provided corpus.
- Multiple viewpoints before forming a recommendation.
- Contradiction, incentive, blind-spot, or evidence-quality analysis.
- A structured outline or long-form report with citations.

Do not use it for simple factual lookups, purely local code edits, or opinions that do not need research.

## Core Workflow

### 1. Scope

Clarify or infer:

- `topic`: the subject being researched.
- `user_role`: who will act on the findings, if relevant.
- `output`: briefing, outline, report, decision memo, test plan, roadmap, etc.
- `source_mode`: live web, repository/docs, uploaded files, database, or user-provided text.
- `depth`: quick, standard, or exhaustive.

If the topic is current, niche, medical, legal, financial, or otherwise high-risk, retrieve current sources before synthesizing. If retrieval is unavailable, state the limitation and ask for source material or proceed as an explicitly source-limited analysis.

### 2. Multi-Perspective Research

Research `{topic}` by simulating 5 expert perspectives:

1. The practitioner: works with this topic every day. What do they know that academics miss? Which practical realities are usually ignored?
2. The academic: has studied this topic for years. What does peer-reviewed evidence actually say? Where does evidence contradict popular belief?
3. The skeptic: thinks the mainstream view is wrong. What is the strongest counterargument? What evidence do proponents tend to ignore?
4. The economist: follows the money. Who benefits from the current narrative? What incentives shape the research or discourse?
5. The historian: has seen similar patterns before. What historical parallels exist? What can be learned from how those cases played out?

For technical, product, policy, medical, legal, or engineering topics, replace weak defaults with domain-specific perspectives such as maintainer, security reviewer, regulator, patient, customer, operator, adversary, or end user.

For each perspective:

1. Give the core position in 2 sentences.
2. Provide the strongest evidence supporting that view.
3. Identify the one thing this perspective would tell the user that no other perspective would.
4. Retrieve or inspect evidence where tools and sources are available.
5. Separate sourced facts from interpretation.

### 3. Contradiction Map

Based on the 5 perspectives, map contradictions:

1. Where do two or more perspectives directly contradict each other? List each conflict with the specific claims that clash.
2. Which perspective has the strongest evidence? Which has the weakest? Explain why.
3. What is the one question that, if answered, would resolve the biggest contradiction?
4. What does every perspective agree on? Treat this as likely true because even opponents confirm it.
5. What topic did none of the perspectives address? Treat this as the field's blind spot and often the most valuable finding.

### 4. Synthesis

Synthesize the 5 perspectives and contradiction map into a research briefing:

1. The one-paragraph summary: explain the topic as if briefing a CEO who has 60 seconds and needs nuance, not just the headline.
2. The 5 key findings: rank the most important things now known by reliability. For each, note which perspectives support it and which challenge it.
3. The hidden connection: one non-obvious link between findings that appears only when all 5 perspectives are considered together.
4. The actionable insight: based on all evidence, what should someone in `{user_role}` actually do differently? Be specific.
5. The frontier question: the one question that, if answered, would change everything about how the topic is understood.

For long-form reports, first create an outline, then draft section-by-section from the evidence table. Use inline citations or source links where the host agent supports them.

### 5. Self-Review

Peer review the research briefing before finalizing:

1. Confidence scores: rate each of the 5 key findings on a 1-10 reliability scale and explain each score.
2. Weakest link: identify the claim with the lowest confidence and the specific information needed to verify it.
3. Bias check: identify which perspective may be overrepresented in the synthesis and whether one voice dominated.
4. Missing perspective: name a 6th angle that should have been included and could change the conclusions.
5. Overall grade: estimate how a strict Stanford-style professor would grade the briefing, why, and what they would tell the agent to fix.

If self-review reveals a material gap and tools/time permit, do one more retrieval pass before final output.

## Output Contract

Default final structure:

```markdown
## Executive Summary

## Perspective Findings

## Contradiction Map

## Synthesis

## Self-Review

## Sources
```

For shorter answers, compress sections but preserve the same logic: perspectives, contradictions, synthesis, self-review.

## Quality Rules

- Ground claims in sources when retrieval is possible.
- Prefer primary sources, official docs, papers, standards, filings, datasets, and direct product docs.
- Avoid false balance: minority views get represented, not automatically equal weight.
- Label inference explicitly.
- Preserve uncertainty instead of smoothing over contradictions.
- Do not fabricate citations, source titles, numbers, or quotes.
- Keep the user-facing answer concise unless they asked for a full report.

## Agent Adapters

For platform-specific installation and tool mapping, read `references/agent-adapters.md`.

For reusable prompts and report templates, read `references/prompt-templates.md`.

For a fuller implementation playbook, read `references/storm-playbook.md`.

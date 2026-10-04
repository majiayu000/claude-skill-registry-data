---
name: find-opps
description: Find new directions for an ops project — adjacent opportunities, strategic gaps, preparatory research. Use when known work is well-mined and you need to look outward.
---

# Find Opportunities

Identify **new directions of work** the project should explore — things that aren't already tracked, aren't obvious from the existing backlog, and that the project owner may not have thought to pursue yet. The output is backlog-ready items — this skill does NOT execute them.

This is the outward-looking complement to `/find-tasks`, which finds work within existing paths. This skill looks beyond current plans to find new territory.

## When to Use

- When `/find-tasks` lenses 1-6 yield fewer than 2 new items (existing paths are well-mined)
- When the user asks "what else should we be thinking about?"
- Between major milestones when strategy should be reassessed
- When the project feels stuck or stale

## Context Required

Before running this skill, you need the project overview already loaded (MEMORY.md, state files, backlog, recent plans, references). If you don't have it, gather it now:

1. `MEMORY.md` — project overview, goals, and knowledge map
2. `state/INDEX.md` → then every file listed in it
3. `backlog/INDEX.md` → then every file and subfolder listed in it
4. `plans/INDEX.md` → then every active plan (not completed)
5. `plans/completed/INDEX.md` — scan the 5 most recent completed plans
6. `references/INDEX.md` — scan for existing research to avoid duplicating

**Isolate the heavy reading when you're on an expensive model.** If you're running on a frontier model (spawned from `/find-all` or `/get-to-work`, or a frontier interactive session), push the context-load above and the lens-3/lens-4 web research to a read-only reader subagent that returns a distilled overview + web digest with citations — then do the ideation (lenses, Filter, Constraints) yourself on that brief. Reading state files and full web pages doesn't need frontier judgment; the ideation does. Enumerate what the reader should extract, or it drops the signal. Skip this on a small project where there's nothing to isolate.

## Analysis Lenses

Think laterally, but stay grounded. Every suggestion must be something an autonomous agent can actually start (research, analysis, drafting, knowledge management). The project's goals and constraints in MEMORY.md are your guardrails — stretch beyond current plans, not beyond what's realistic for this project.

### 1. Adjacent Opportunities

Areas the project hasn't explored but plausibly could, given its goals and resources. Ask: what's one step removed from what the project is already doing? What related problems could the same approach solve? What audiences or use cases are being underserved?

### 2. Strategic Gaps

What would a sharp outside advisor notice is missing? Blind spots in the project's approach, risks that aren't being tracked, assumptions that haven't been validated. The things that are dangerous precisely because nobody's looking at them.

### 3. Emerging Context

Use web search to check for recent developments in the project's domain. New tools, market shifts, competitor moves, regulatory changes, emerging best practices. Look for things that happened recently enough that they wouldn't be reflected in the project's existing state files.

### 4. Preparatory Research

Research that would inform decisions the project will eventually need to make, even if it doesn't know it yet. Competitor deep-dives, market sizing, technology evaluations, case studies of similar projects. The value is in having the analysis ready before the decision point arrives.

### 5. Cross-Pollination

Strategies, frameworks, or patterns from adjacent domains that could apply here. What's working well in related fields that this project hasn't borrowed yet?

## Process

### Step 1: Analyze

For each lens, search for opportunities. Use the project context you've loaded, plus web search for lenses 3 and 4.

### Step 2: Filter

Remove items that:
- Are already tracked in the backlog (even if worded differently)
- Are too vague to act on
- Exceed the project's realistic scope or resources
- Are not something an autonomous agent could start working on

### Step 3: Format Output

Produce backlog-ready items:

```markdown
## New Opportunities Identified

### 1. [Title]
- **What**: [1-2 sentences — the concrete task]
- **Artifact**: [file path for the deliverable, e.g., references/competitor-analysis.md]
- **Why**: [how this connects to or expands the project's goals]
- **Effort**: light / medium / heavy
- **Lens**: [which category above: adjacent, strategic gap, emerging, preparatory, cross-pollination]

### 2. [Title]
...
```

Aim for 3-5 items. Prefer a mix of lenses and effort levels. At least one should be a quick win (light effort, clear value), and at least one should be a deeper investigation that could shift the project's trajectory.

This block is the record — it goes back to the caller when a subagent runs this skill, and into the backlog when the main agent runs it directly. When briefing the user, the same items become short prose instead: each one says what the project would learn or gain and what it would cost, with lens names and deliverable paths left out.

## Constraints

- **Stay practical.** Every item must be something an autonomous agent could start working on — a research task, an analysis, a draft document, a state file update. "Consider pivoting the business model" is not actionable. "Research 3 alternative revenue models used by similar projects and write a comparison to references/revenue-models.md" is.
- **Respect project scope.** Read MEMORY.md carefully. The project has specific goals, resources, and limitations. Your suggestions should expand the project's horizon, not ignore its reality.
- **Don't duplicate.** Check the existing backlog before suggesting something. If it's already tracked (even in different words), skip it.
- **Be concrete.** Each item needs: what to do, what file/artifact to produce, and why it's valuable. Vague strategic musings aren't backlog items.

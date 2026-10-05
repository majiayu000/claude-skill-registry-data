---
name: analyzing-source-project
description: Assess a source project's technical capabilities. Reads `config/sources.md` and produces a structured capability profile. Use to start the GTM pipeline or evaluate technical differentiators (Phase 0).
compatibility: Designed for Claude Code
metadata:
  stability: stable
  content-hash: sha256:e856f199bd04e9ce7b891e33b0506c2d142968bf9df9c4c0e0c7f23f957a8d95
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, Agent
  argument-hint: [project-path-or-url]
---

# Analyzing Source Project (Phase 0)

**Target**: $ARGUMENTS

Phase 0 of the GTM pipeline. Produces a technical capability profile of the
source project that feeds Phase 1B (researching-market).

## Mode Awareness

Read `config/mode.md` before starting:

- `concise` — Bullet summaries, 3-5 points per section
- `detailed` — Full narrative with evidence and code references
- `conservative` — Focus on proven, documented capabilities
- `ambitious` — Highlight unrealized potential and extension opportunities

## Inputs

- `config/sources.md` — Source projects to analyze
- `config/comments_research.md` — Research constraints and focus areas
- `config/mode.md` — Style and approach settings

## Workflow

1. **Identify source projects** from `config/sources.md`
2. **Clone or fetch** the repository if a URL is provided (use WebFetch for public repos)
3. **Assess architecture** — Directory structure, module boundaries, design patterns
4. **Inventory tech stack** — Languages, frameworks, dependencies, infrastructure hints
5. **Extract differentiators** — What does this project do unusually well?
6. **Identify limitations** — Scalability ceilings, missing features, tech debt signals
7. **Rate capabilities** — Score each capability area (1-5) with rationale
8. **Validate against criteria** — Check `config/validation_criteria.md` Phase 0 gates

## Output

Write to `results/phase-0/`:

### `capability-profile.md`

```markdown
# Source Project Capability Profile

## Project: [name]

## Architecture Summary
[Overview of system design and key components]

## Tech Stack
- Language: [language + version]
- Framework: [framework]
- Key dependencies: [list]

## Differentiating Capabilities
1. [Capability] — Score: [1-5] — Evidence: [file/feature reference]
2. ...

## Limitations and Risks
- [Limitation] — Impact: [High/Medium/Low]

## GTM-Relevant Technical Signals
[How technical characteristics translate to market positioning opportunities]
```

## Rules

- Ground every capability claim in observable code or documentation evidence
- Distinguish between current state and aspirational/roadmap features
- Limitations are as important as strengths for honest PMF assessment
- Cross-reference with `config/comments_research.md` scope constraints

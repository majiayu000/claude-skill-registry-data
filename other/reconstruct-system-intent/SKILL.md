---
name: reconstruct-system-intent
description: Use when you need to understand what a system was truly designed to become, where its real moat lies, or to produce a comprehensive analysis report combining all prior findings
---

## Announce at start: "Using codebase-analyzer to reconstruct system intent."

## Overview

What was this system designed to become? Not what it claims to do, but what the architecture, gates, and hidden capabilities reveal about its true purpose. The real moat is rarely in the client binary -- it is in the service/backend layer.

**Prerequisite:** Reads ALL completed analysis files from `docs/analysis/`. This is the terminal skill -- it consumes every prior analysis output.

## Five Intent Questions

Answer these by synthesizing evidence across all analysis phases:

1. **What is this system designed to become?**
   Sources: `architecture.md` + `tool-graph.md` + `gate-map.md` + git archaeology (evolution trajectory)
   Look for: abandoned features revealing planned direction, investment patterns in service layer vs client, architectural decisions that only make sense at scale.

2. **Where is the moat?**
   Sources: `gate-map.md` (feature gate analysis) + `tool-graph.md` (tool registration) -- client vs service vs ecosystem
   Look for: where the most complex logic lives, which capabilities are server-controlled, what would be hardest to replicate.

3. **What can it do that it does not expose?**
   Sources: `tool-graph.md` + `gate-map.md` + `dead-code.md`
   Look for: conditionally registered but currently dormant tools, hidden admin capabilities, API endpoints behind disabled feature flags.

4. **How is behavior really controlled?**
   Sources: `prompt-influence.md` + `gate-map.md` (feature gates)
   Look for: remote configuration driving tool availability, prompt instructions shaping behavior at inference time, server-driven capability gating.

5. **What are the hidden dependencies?**
   Sources: `provenance.md` + `build-pipeline.md`
   Look for: undocumented telemetry endpoints, data sent to services not mentioned in public docs, build-time pins to specific infrastructure.

## Synthesis Output

Produce a single comprehensive report:

```markdown
# Codebase Analysis Report
## Date: [YYYY-MM-DD]
## Target: [repo path/description]

### Executive Summary
(2-3 sentences: what the system is, its maturity, and the most important finding)

### Track A: Code Quality Findings
- Target classification and tech stack
- Architecture overview
- Dependency health
- Dead code inventory
- API surface summary
- Code quality assessment
- Refactoring recommendations (prioritized by impact/effort)

### Track B: System Intelligence Findings
- Provenance and build pipeline analysis
- Agent loop and tool graph
- Conditional behavior and feature gates
- Prompt influence analysis
- Threat model (what the system could do if misused)

### System Intent Narrative
(Answer each of the five intent questions with evidence and confidence level)

### Confidence-Weighted Evidence Map
| Finding | Confidence | Evidence Sources | Gaps |
|---------|-----------|-----------------|------|
| (finding) | High/Med/Low | (which files/analysis) | (what would strengthen) |

### Priority Actions
1. (highest impact, most urgent)
2. ...
```

## Evidence Weighting

When constructing the system intent narrative, weight evidence by source reliability:

| Source | Weight | Reason |
|--------|--------|--------|
| Architecture patterns | High | Structural decisions are expensive to change |
| Git history (evolution) | High | Shows where investment actually went |
| Tool graph & feature gates | High | Gates reveal what the system protects |
| Dead code / abandoned features | Medium | Shows intent but may be outdated |
| Build pipeline | Medium | Reveals infrastructure dependencies |
| Prompt instructions | Medium-Low | Can change without code deployment |
| Config defaults | Low | Easily changed, may not reflect intent |

For each finding, state confidence explicitly. If confidence is below Medium, note what additional evidence would strengthen the conclusion.

## Evolution Evidence

Use git archaeology techniques to trace the system's trajectory over time.
See `_shared/references/git-archaeology-techniques.md` for methodology:

- Commit message patterns reveal development priorities
- File churn identifies areas of active investment
- Abandoned branches show explored-but-rejected directions
- Dependency addition chronology shows strategic shifts

## Iron Law

```
Moat location: never assume the interesting behavior is in the client.
Check the service layer first.
```

## SECURITY_SIGNAL

Watch for patterns indicating the system may be designed to:
- Collect more data than it exposes to users
- Maintain hidden admin capabilities accessible via undocumented paths
- Create data exfiltration channels through telemetry, analytics, or "phone home" endpoints
- Control behavior remotely via configuration pushed from a service layer
- Circumvent user-imposed restrictions through server-side policy enforcement

If any of these patterns are detected, flag them prominently in the report with a `SECURITY_SIGNAL` marker and include them in the Priority Actions section.

## Adversarial Lens

Ask not just "what was this designed to do?" but "what was this designed to BECOME?" Abandoned features that were 80% complete reveal future direction. Gates that restrict capabilities reveal fear of misuse. The architecture reveals intent better than any comment.

## Output Contract

Write `docs/analysis/analysis-report-[YYYY-MM-DD].md`.

This is the terminal output. No separate status file is needed. The report IS the deliverable.

## References

- `_shared/references/git-archaeology-techniques.md` -- for tracing evolution evidence
- `references/intent-signals.md` -- intent signal patterns, moat detection heuristics, and confidence weighting

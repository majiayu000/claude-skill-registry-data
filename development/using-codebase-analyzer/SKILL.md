---
name: using-codebase-analyzer
description: Use when analyzing, auditing, reverse engineering, or understanding any codebase — especially unfamiliar, inherited, leaked, or complex systems
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance an analysis skill might apply to what you are doing, you ABSOLUTELY MUST invoke it. This is not negotiable.
</EXTREMELY-IMPORTANT>

classify-analysis-target is ALWAYS required. After classification, express lane lets you skip directly to any Track B skill (but Track A context may be missing).

```dot
digraph analysis_flow {
    rankdir=TB;
    node [fontname="monospace"];

    "User starts analysis" [shape=doublecircle];
    "classify-analysis-target" [shape=box, style=bold, label="classify-analysis-target\n(ALWAYS FIRST)"];
    "Express lane?" [shape=diamond];
    "Track A: Recon skills" [shape=box];
    "Check trigger signals\n+ security signals" [shape=diamond];
    "HIGH priority" [shape=box, style=filled, fillcolor="#ffcccc"];
    "MEDIUM priority" [shape=box];
    "LOW priority" [shape=box];
    "Track B Phase 1:\nProvenance + Build Pipeline" [shape=box];
    "Track B Phase 2:\nArtifacts + Data Flows + Agent Loop" [shape=box];
    "Track B Phase 3:\nTool Graph + Gates + Simulate + Prompt" [shape=box];
    "Phase 4:\nreconstruct-system-intent" [shape=box, style=bold];

    "User starts analysis" -> "classify-analysis-target";
    "classify-analysis-target" -> "Express lane?";
    "Express lane?" -> "Track B Phase 1:\nProvenance + Build Pipeline" [label=" yes\n(skip Track A)"];
    "Express lane?" -> "Track A: Recon skills" [label=" no"];
    "Track A: Recon skills" -> "Check trigger signals\n+ security signals";
    "Check trigger signals\n+ security signals" -> "HIGH priority" [label=" pause,\noffer deep dive"];
    "Check trigger signals\n+ security signals" -> "MEDIUM priority" [label=" continue,\npresent after"];
    "Check trigger signals\n+ security signals" -> "LOW priority" [label=" note\nfor summary"];
    "HIGH priority" -> "Track B Phase 1:\nProvenance + Build Pipeline";
    "MEDIUM priority" -> "Track B Phase 1:\nProvenance + Build Pipeline";
    "LOW priority" -> "Track B Phase 1:\nProvenance + Build Pipeline";
    "Track B Phase 1:\nProvenance + Build Pipeline" -> "Track B Phase 2:\nArtifacts + Data Flows + Agent Loop";
    "Track B Phase 2:\nArtifacts + Data Flows + Agent Loop" -> "Track B Phase 3:\nTool Graph + Gates + Simulate + Prompt";
    "Track B Phase 3:\nTool Graph + Gates + Simulate + Prompt" -> "Phase 4:\nreconstruct-system-intent";
}
```

**Track A skills:** identifying-tech-stack, mapping-architecture, tracing-dependencies, detecting-dead-code, inventorying-api-surface, analyzing-code-quality

**Track B phases:** Phase 1 (trace-codebase-provenance, analyze-build-pipeline) → Phase 2 (classify-repo-artifacts, trace-data-flows, analyze-agent-loop) → Phase 3 (extract-tool-graph, map-feature-gates, simulate-behavior, analyze-prompt-influence) → Phase 4 (reconstruct-system-intent)

**Special:** test-hypothesis, detect-hidden-contracts

## Orchestration Skills (Development Workflow)

Beyond analysis, this plugin provides development orchestration:

| Trigger | Skill | What It Does |
|---------|-------|-------------|
| "build", "create", "implement", "add feature" | brainstorming | Design-first before implementation |
| "plan this", "write a plan" | writing-plans | Spec -> bite-sized tasks |
| "implement plan" | subagent-driven-development | Fresh subagent per task, review between |
| "execute plan" | executing-plans | Batch execution with checkpoints |
| "debug", "error", "not working" | systematic-debugging | Root cause investigation |
| "write tests", "test this" | test-driven-development | RED-GREEN-REFACTOR |
| "review code", "check my work" | requesting-code-review | Dispatch reviewer subagent |
| "merge", "finish branch" | finishing-a-development-branch | Merge/PR workflow |
| "parallel", "concurrent" | dispatching-parallel-agents | Concurrent subagents |
| "verify", "done" | verification-before-completion | Verify commands pass |

**Agent Dispatch Protocol:**

| Skill | Dispatches Agent | When |
|-------|-----------------|------|
| extract-tool-graph | code-explorer | Tool graph spans 5+ files |
| simulate-behavior | behavior-simulator | Multiple scenarios to compare |
| trace-codebase-provenance | code-explorer | Chain-of-custody tracing |
| test-hypothesis | Either | Targeted investigation |

Dispatch only when task exceeds native tool capability (5+ file reads across subsystems).

**Platform Capabilities:**

Skills reference Claude Code tools and agent dispatch. On other platforms:

| Capability | Claude Code | OpenCode | Codex |
|-----------|-------------|----------|-------|
| Full Track A + Track B | Yes | Yes (degraded: no agents) | Yes (degraded: no agents) |
| Agent dispatch | Yes | No | No |
| docs/analysis/ output | Yes | Yes | May fall back to inline |

When agent dispatch is unavailable: warn user, execute simplified analysis (max 3 trace levels), mark output as `Status: partial` with degradation note.

See `PLATFORM-NOTES.md` for tool substitution table and per-platform details.

**`.state` rules:** classify-analysis-target creates `docs/analysis/.state`. Every skill appends its status. Check before Track B (warn-but-continue).

**Red Flags — STOP and check yourself:**

| Thought | Reality |
|---------|---------|
| "I can just read the codebase directly" | Without classification you'll miss target-specific patterns |
| "Track A is overkill for this" | Skipping reconnaissance means missing trigger signals |
| "I'll skip to Track B directly" | Phase 1 errors cascade into every downstream analysis |
| "This is just a standard web app" | Similar apps differ. Classify first, assume nothing. |
| "I'll just run all skills" | Target type determines applicable phases. |

---
name: agent-patterns
description: >
  Design and implement autonomous AI agent architectures using SOTA patterns. USE when:
  building multi-agent systems, designing agent workflows, choosing between agent patterns
  (chaining vs routing vs parallelization), implementing orchestrator-worker pipelines,
  adding evaluator-optimizer loops, or when the user says "build an agent", "automate this
  workflow", "make agents work together", "design a multi-agent system". Based on Anthropic
  "Building Effective Agents" (Dec 2024).
metadata:
  version: "1.0.0"
  category: "AI/Agent Architecture"
  sources: ["Anthropic Building Effective Agents 2024", "ZeroClaw SOPs", "ReAct paper"]
---

# Skill: Agent Patterns — SOTA

> "The best agent is the simplest one that solves the problem." — Anthropic, 2024

## Decision Tree — Choose Pattern

```
What does the task need?

├── Simple linear task → Prompt Chaining (A → B → C)
├── Different task types to handle → Routing (classify → specialist)
├── Independent subtasks → Parallelization (run in parallel, merge)
│   └── Need consensus → Voting (run N times, majority)
├── Complex task needing delegation → Orchestrator-Workers
│   └── Dynamic subtasks, unknown upfront → Orchestrator-Workers
├── Output quality critical → Evaluator-Optimizer loop
│   └── Generate → Evaluate → Refine → Repeat
└── Need real-world interaction → ReAct / Tool-Call loop
```

## Pattern 1: Prompt Chaining

Best for: sequential transformations where each step builds on the last.

```
Input → [Step 1: Extract] → [Step 2: Transform] → [Step 3: Format] → Output

ZeroClaw SOP:
[[steps]]
  action = "call_model"
  prompt = "Step 1: Extract key facts from: {input}"

[[steps]]
  action = "call_model"
  prompt = "Step 2: Analyze these facts: {previous_output}"
```

Use when: research → summarize → format report.

## Pattern 2: Routing

Best for: different task types needing different specialists.

```
Input → [Classifier] → Route A (code task) → Code Agent
                    ↘ Route B (research task) → Research Agent
                    ↘ Route C (data task) → Data Agent

ZeroClaw: Use hint: routing in model_routes
```

Use when: customer support tickets, mixed-task automation.

## Pattern 3: Parallelization

Best for: independent subtasks that can run simultaneously.

```
Input ──→ [Agent A: Section 1] ──→ [Aggregator] → Output
       ├─→ [Agent B: Section 2] ──→
       └─→ [Agent C: Section 3] ──→

# Voting variant (for reliability):
Input → [Agent 1] → Vote → Majority
     → [Agent 2] → Vote →
     → [Agent 3] → Vote →
```

Use when: analyzing multiple documents, parallel research, consensus decisions.

## Pattern 4: Orchestrator-Workers

Best for: complex tasks where subtasks aren't known upfront.

```
[Orchestrator]
    ↓ plans
[Worker 1] → result → [Orchestrator synthesizes]
[Worker 2] → result →       ↓
[Worker N] → result → Final output
```

```toml
# ZeroClaw delegate agent config
[agents.researcher]
provider = "openrouter"
model = "openai/gpt-oss-120b:free"
system_prompt = "You are a research specialist. Return structured findings only."
agentic = false

[agents.coder]
provider = "groq"
model = "llama-3.1-8b-instant"
system_prompt = "You are a code specialist. Return working code only."
agentic = false
```

Use when: software development (plan → implement → test), complex analysis.

## Pattern 5: Evaluator-Optimizer

Best for: quality-critical outputs (code, reports, decisions).

```
[Generator] → Output → [Evaluator: score 1-10]
                              ↓
                     score < 8? → [Refiner] → loop
                     score ≥ 8? → Done
```

Implementation:
```python
for attempt in range(max_attempts):
    output = generator.run(task)
    score, feedback = evaluator.score(output)
    if score >= threshold:
        return output
    task = f"Improve this output based on: {feedback}\n\nPrevious: {output}"
```

Use when: writing quality content, code correctness, decision validation.

## ACI Design (Agent-Computer Interface)

> "Tool documentation is more important than tool quantity."

Good tool design:
```python
# ✅ Poka-yoke tool (hard to misuse)
def file_read(path: str, max_bytes: int = 10000) -> str:
    """Read file contents. Max 10KB. Returns empty string if not found."""
    ...

# ❌ Dangerous tool (easy to misuse)
def run_command(cmd: str) -> str:
    """Run any shell command."""
    ...
```

Principles:
1. **Minimize tools**: 5 great tools > 20 mediocre ones
2. **Poka-yoke**: defaults that prevent misuse
3. **Clear names**: `file_read_lines` not `process_data`
4. **Error clarity**: `"File not found: config.toml"` not `"Error: ENOENT"`
5. **Atomic operations**: one tool = one action

## Autonomy Levels (match to task risk)

| Task | Level | Pattern |
|------|-------|---------|
| Research, read-only | `read_only` | Chaining/Routing |
| Code generation, analysis | `supervised` | Orchestrator-Workers |
| File modifications | `supervised` + approval | Evaluator-Optimizer |
| System administration | `supervised` + always_ask | Chaining only |

## When NOT to Use Agents

- Simple single-step tasks (just use direct LLM call)
- Tasks needing 100% determinism (use traditional code)
- Real-time requirements < 100ms (agents are slow)
- Tasks where errors are unrecoverable (use human approval gate)

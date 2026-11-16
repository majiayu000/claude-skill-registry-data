---
name: claude-swarm-orchestration
description: Multi-agent orchestration for Claude Code — automatic task decomposition via Opus 4.6, parallel execution with dependency-aware scheduling, file conflict prevention, quality gate, and cost control. Use for complex tasks that benefit from parallelism (refactors, feature builds, audits across many files).
license: MIT
source: https://github.com/affaan-m/claude-swarm
---

# Claude Swarm Orchestration

Auto-decompose complex tasks into parallel subtasks with dependency-aware scheduling.

**Trigger phrases:** "parallel agents", "swarm", "decompose task", "multi-agent execution", "run agents in parallel", "orchestrate agents", "claude-swarm"

---

## When to Use

Use claude-swarm when:
- Task touches 5+ files across different domains
- Work can be parallelized (independent subtasks exist)
- Need quality gate review across all outputs
- Budget control is critical

Use YAMTAM agents-v2 (hub-and-spoke) when:
- Tasks require close inter-agent discussion/debate
- Sequential logic with shared state

---

## 4-Phase Flow

```
Phase 1 (Opus): Analyze codebase → decompose into 2-8 subtasks with dependency graph
Phase 2 (Haiku pool): Execute subtasks in parallel, dependency-aware, file-locked
Phase 2.5 (Opus quality gate): Review all outputs → pass/needs_revision/fail
Phase 3: Deliver combined result with cost tracking
```

---

## Config Format (swarm.yaml)

```yaml
name: "full-stack-feature"
max_concurrent: 4
budget_usd: 5.00
model: "opus"               # decomposition model

agents:
  coder:
    name: "Code Implementation"
    model: "haiku"
    tools: [Read, Write, Edit, Bash, Grep, Glob]
    prompt: "Implement the requested changes..."

  tester:
    name: "Test Writer"
    model: "haiku"
    tools: [Read, Write, Edit, Bash, Grep]
    prompt: "Write comprehensive tests..."

  reviewer:
    name: "Code Reviewer"
    model: "opus"
    tools: [Read, Grep, Glob]
    prompt: "Review all changes for correctness..."

connections:
  - from_agents: ["coder"]
    to_agent: "tester"
  - from_agents: ["coder"]
    to_agent: "reviewer"
  - from_agents: ["tester", "reviewer"]
    to_agent: "delivery"
```

**Agent roles:** coder · tester · reviewer · documenter · refactorer · security-reviewer

---

## CLI Usage

```bash
# Install
pip install claude-swarm

# Basic task
claude-swarm "Refactor auth module from Express to Next.js"

# Preview decomposition without executing
claude-swarm --dry-run "Add user authentication"

# Custom config and budget
claude-swarm -c ./swarm.yaml -b 10.0 "Complex migration"

# Without quality gate
claude-swarm --no-quality-gate "Quick fix"

# View sessions
claude-swarm sessions
claude-swarm replay <session_id>
```

Requires: `ANTHROPIC_API_KEY`, Python 3.11+

---

## Key Mechanisms

**File conflict prevention:** pessimistic locking — task blocked if target files are already locked by another running agent.

**Dependency scheduling:** tasks only start when all prerequisite tasks complete. Enables "waves" of parallel execution.

**Budget enforcement:** hard ceiling — remaining work cancelled when `budget_usd` exceeded.

**Quality gate scoring:**
```
≥ 8/10 → pass
5–7/10 → needs_revision (agent retries)
< 5/10 → fail (escalate to human)
```

---

## vs YAMTAM agents-v2

| Feature | claude-swarm | YAMTAM agents-v2 |
|---------|-------------|-----------------|
| Task decomposition | Automatic (Opus) | Manual |
| Scheduling | DAG + file locks | Hub-and-spoke |
| Quality review | Built-in gate | Multi-agent debate |
| Cost control | Hard budget ceiling | None built-in |
| Session replay | ✅ | ❌ |
| Config | declarative YAML | code-defined |

---

## Anti-Fake-Pass

```
❌ Using swarm for sequential tasks where ordering matters — use pipeline
❌ Setting budget too low — tasks cancelled mid-execution
❌ Overlapping file targets across agents — causes conflict blocks
❌ Not doing --dry-run first on expensive tasks
❌ Skipping quality gate for user-facing features
```

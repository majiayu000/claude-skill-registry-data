---
name: agent-orchestrator"
description: Orchestrates multi-agent workflows for complex tasks. Use when a task requires coordination between multiple specialized agents (architect, debug, code-reviewer, refactor, etc.).
---

# Agent Orchestrator Skill

## Orchestration Patterns

### Sequential Pipeline
```
Task → Architect → Build → Test → Review → Done
```
Each agent completes its phase before the next starts.

### Parallel Fan-out
```
Task → [Architect, Security-Audit, Performance-Analysis] → Aggregator → Done
```
Multiple agents work simultaneously on different aspects.

### Iterative Loop
```
Task → Build → Review → (issues?) → Build → Review → Done
```
Build and review iterate until quality bar met.

### Hierarchical Delegation
```
Orchestrator
├── Architect (plans)
├── Build Team
│   ├── Backend Agent
│   ├── Frontend Agent
│   └── DevOps Agent
└── QA Team
    ├── Test Agent
    ├── Security Agent
    └── Performance Agent
```

## Workflow Templates

### Feature Development
```yaml
name: feature-development
phases:
  - name: plan
    agent: architect
    input: requirements
    output: spec.md
    
  - name: implement
    agent: build
    input: spec.md
    output: code changes
    
  - name: test
    agent: build
    input: code changes
    output: test results
    
  - name: review
    agent: code-reviewer
    input: code changes + test results
    output: review feedback
    
  - name: refine
    agent: build
    input: review feedback
    output: final code
```

### Bug Fix
```yaml
name: bug-fix
phases:
  - name: reproduce
    agent: debug
    input: bug report
    output: reproduction steps + root cause
    
  - name: fix
    agent: build
    input: root cause
    output: fix + test
    
  - name: verify
    agent: debug
    input: fix
    output: verification results
    
  - name: review
    agent: code-reviewer
    input: fix
    output: approval
```

### Refactoring
```yaml
name: refactoring
phases:
  - name: analyze
    agent: refactor
    input: target code
    output: refactoring plan
    
  - name: test-baseline
    agent: build
    input: target code
    output: characterization tests
    
  - name: execute
    agent: refactor
    input: plan + tests
    output: refactored code
    
  - name: verify
    agent: build
    input: refactored code
    output: all tests pass
    
  - name: review
    agent: code-reviewer
    input: refactored code
    output: approval
```

### Code Review (Automated)
```yaml
name: pr-review
trigger: pull_request
phases:
  - name: static-analysis
    agents: [security-audit, performance-check]
    parallel: true
    
  - name: logic-review
    agent: code-reviewer
    depends_on: static-analysis
    
  - name: test-validation
    agent: build
    depends_on: static-analysis
    
  - name: aggregate
    agent: orchestrator
    input: all reviews
    output: summary report
```

## Agent Definitions

### Primary Agents (User-facing)
| Agent | Role | When to Use |
|-------|------|-------------|
| `build` | Default implementation | Writing code, tests, fixes |
| `plan` | Planning only | High-level design, no code |
| `architect` | System design | Architecture decisions, ADRs |

### Subagents (Task-invoked)
| Agent | Role | Specialization |
|-------|------|----------------|
| `debug` | Troubleshooting | Root cause analysis, tracing |
| `code-reviewer` | Quality gate | Security, perf, maintainability |
| `refactor` | Code improvement | Structure, patterns, modernization |
| `explore` | Research | Codebase understanding, docs |
| `general` | Multi-step | Complex workflows, orchestration |

## Invocation Patterns

### Direct Invocation
```bash
# In OpenCode chat
@architect Design a user authentication system
@debug Why is the login API returning 500?
@code-reviewer Review the auth PR #123
```

### Task Tool (Programmatic)
```typescript
// In agent or script
await task({
  agent: "architect",
  prompt: "Design auth system with JWT, refresh tokens, OAuth2",
  context: { files: ["src/auth/"], requirements: "..." }
});

await task({
  agent: "code-reviewer",
  prompt: "Review PR #123 for security issues",
  context: { pr: 123 }
});
```

### Orchestrated Workflow
```typescript
async function runFeatureWorkflow(requirements: string) {
  // Phase 1: Plan
  const spec = await task({ agent: "architect", prompt: requirements });
  
  // Phase 2: Implement
  const implementation = await task({ 
    agent: "build", 
    prompt: `Implement: ${spec}` 
  });
  
  // Phase 3: Test (parallel with review prep)
  const [testResults, reviewPrep] = await Promise.all([
    task({ agent: "build", prompt: `Write tests for: ${implementation}` }),
    task({ agent: "explore", prompt: `Summarize changes for review: ${implementation}` })
  ]);
  
  // Phase 4: Review
  const review = await task({ 
    agent: "code-reviewer", 
    prompt: `Review: ${reviewPrep}`, 
    context: { testResults } 
  });
  
  // Phase 5: Refine if needed
  if (review.hasChanges) {
    return runFeatureWorkflow(`${requirements}\n\nAddress: ${review.feedback}`);
  }
  
  return { spec, implementation, testResults, review };
}
```

## Coordination Mechanisms

### Shared Context
```json
{
  "workflowId": "feat-auth-20240115",
  "phase": "implement",
  "artifacts": {
    "spec": "docs/spec/auth.md",
    "implementation": "src/auth/",
    "tests": "tests/auth/"
  },
  "agents": {
    "architect": { "status": "done", "output": "spec.md" },
    "build": { "status": "in_progress", "started": "2024-01-15T10:00Z" }
  }
}
```

### Handoff Protocol
```
FROM: architect
TO: build
ARTIFACT: spec.md
CONTEXT: 
  - Requirements: JWT + refresh + OAuth2
  - Constraints: Use existing user model, Redis for sessions
  - Decisions: Stateless auth, 15min access / 7d refresh
HANDOFF_NOTES: "Pay attention to token rotation security"
```

### Progress Tracking
```bash
# Check workflow status
opencode-skill agent-orchestrator status feat-auth-20240115

# Output:
# Workflow: feat-auth-20240115
# Phase: implement (2/5)
# ✓ architect - spec.md created
# ⟳ build - implementing login endpoint
# ○ test - pending
# ○ review - pending
# ○ refine - pending
```

## Best Practices

### When to Orchestrate
- Multi-phase tasks (plan → build → test → review)
- Cross-cutting concerns (security + performance + maintainability)
- Complex features requiring multiple specializations
- Quality gates needed before merge

### When NOT to Orchestrate
- Simple, single-purpose tasks
- Exploratory work (use explore agent directly)
- Quick fixes (use debug or build directly)
- Learning/experimentation

### Anti-Patterns
- ❌ Too many agents for simple task
- ❌ No clear handoff artifacts
- ❌ Circular dependencies between agents
- ❌ Orchestrator doing work instead of coordinating
- ❌ Skipping review phases for speed

## Integration with OpenCode

### Skill Commands
```
/orchestrate feature-development "Add user dashboard"
/orchestrate bug-fix "Login fails with special chars"
/orchestrate refactoring "Extract payment service"
/orchestrate pr-review 123
```

### Status Dashboard
```bash
# In OpenCode terminal
opencode-skill agent-orchestrator dashboard

# Shows active workflows, agent statuses, pending handoffs
```

## When to Use

- Complex feature development (3+ phases)
- Bug fixes requiring investigation + fix + verification
- Large refactoring with safety requirements
- Automated PR review pipelines
- Multi-team coordination
- Quality-critical changes
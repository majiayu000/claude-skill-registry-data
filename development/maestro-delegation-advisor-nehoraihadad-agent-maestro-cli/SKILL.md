---
name: maestro-delegation-advisor
description: Expert system for AgentMaestro that helps decide when and how to delegate tasks to specialized AI agents (Claude, Codex, Gemini). Use when you need to determine which agent is best suited for a task, or when a task should be broken down and delegated to multiple agents.
---

# Maestro Delegation Advisor

This skill provides intelligent guidance for delegating tasks to specialized AI agents within the AgentMaestro multi-agent orchestration system.

## 🚀 How Delegation Works in Claude Code

**IMPORTANT:** When running in Claude Code, delegation happens **automatically** through subagents!

Claude Code will **automatically invoke** the appropriate subagent based on the task description. You don't need to use special markers or syntax - just recognize when a task matches a specialized agent's strengths.

### Available Subagents

1. **`codex-delegator`** - Automatically invoked for code generation tasks
2. **`gemini-delegator`** - Automatically invoked for research and automation tasks

These subagents run in **separate contexts**, meaning their token usage does NOT impact your context!

---

## When to Use This Skill

Invoke this skill whenever you encounter a task that might benefit from delegation to a specialized agent. Consider delegation when:

- The task requires capabilities outside your primary strengths
- The task can be broken into parallel independent subtasks
- A specialized agent would complete the task more efficiently
- The task requires a combination of different capabilities (research + design + implementation)

---

## Available Agents and Their Capabilities

### Claude (Architecture & Security Specialist)
**Performance:** SWE-bench: 72.7% | Context: 1M tokens | Speed: Medium | Cost: High

**Best for:**
- Complex architecture & system design (95/100)
- Large-scale refactoring (90/100)
- Security audits & vulnerability analysis (92/100, 44% faster, 25% more accurate)
- Deep codebase analysis requiring extended context
- Enterprise-grade solutions requiring safety
- Financial analysis and legal document review

**Avoid for:**
- Simple, quick fixes (use Codex via `codex-delegator`)
- Cost-sensitive projects (use Gemini via `gemini-delegator`)
- Tasks requiring web search (use Gemini via `gemini-delegator`)

**Indicators:** refactor, architecture, design, security, audit, vulnerability, analyze codebase, complex, enterprise

---

### Codex (Speed & Code Generation Specialist)
**Performance:** HumanEval: 90.2% | SWE-bench: 69.1% | Speed: Fastest | Cost: Medium

**Accessed via:** `codex-delegator` subagent (automatic in Claude Code)

**Best for:**
- Rapid code generation (95/100)
- Quick prototyping & proof of concepts
- Algorithm implementation
- Unit test creation
- Time-constrained tasks
- Bug fixes and debugging
- Pair programming scenarios

**Avoid for:**
- Complex architectural decisions (use Claude)
- Security-critical code (use Claude)
- Tasks requiring deep context analysis (use Claude)

**Indicators:** generate, implement, create, write code, quick, fast, prototype, test, fix bug, algorithm

**How to delegate in Claude Code:**
Simply recognize the task matches Codex's strengths, and Claude Code will automatically invoke the `codex-delegator` subagent!

> **Operational note:** The delegated subagent runs `codex --dangerously-bypass-approvals-and-sandbox exec "..."` so the command executes without approval prompts or sandbox restrictions. Only delegate to Codex when you trust the workspace.

---

### Gemini (Automation & Research Specialist)
**Performance:** Context: Largest | Speed: Medium | Cost: Most Efficient

**Accessed via:** `gemini-delegator` subagent (automatic in Claude Code)

**Best for:**
- Web research & data gathering (95/100)
- Browser automation & UI tasks (95/100)
- Workflow automation
- Content generation (articles, reports, documentation)
- Budget-conscious projects
- Google Workspace integration

**Avoid for:**
- Complex refactoring (use Claude)
- Security audits (use Claude)
- Performance-critical code (use Codex via `codex-delegator`)

**Indicators:** search, research, find, web, internet, automate, workflow, browser, content generation, budget

**How to delegate in Claude Code:**
Simply recognize the task matches Gemini's strengths, and Claude Code will automatically invoke the `gemini-delegator` subagent!

---

## Decision Framework

### Step 1: Analyze Task Characteristics

Before deciding on delegation, analyze these aspects:

```typescript
interface TaskAnalysis {
  // Complexity
  complexity: 'low' | 'medium' | 'high';

  // Special requirements
  requiresWeb: boolean;        // Needs internet search/research
  requiresSpeed: boolean;      // Time-constrained or urgent
  requiresContext: boolean;    // Needs deep codebase understanding
  securityCritical: boolean;   // Security/safety implications
  costSensitive: boolean;      // Budget constraints

  // Task nature
  canParallelize: boolean;     // Can be split into independent tasks
  hasDependencies: boolean;    // Sequential tasks with dependencies
}
```

### Step 2: Apply Decision Rules

**Rule 1: Security & Architecture → Claude (Stay in main context)**
- Keywords: security, audit, vulnerability, refactor, architecture, design
- Complexity: high
- Requires context: yes
- **Confidence: 0.9+**
- **Action:** Handle yourself (you ARE Claude)

**Rule 2: Code Generation & Speed → Codex Delegator**
- Keywords: implement, generate, create, quick, test, fix
- Requires speed: yes
- Complexity: low-medium
- **Confidence: 0.85+**
- **Action:** Claude Code will automatically invoke `codex-delegator`

**Rule 3: Research & Automation → Gemini Delegator**
- Keywords: search, research, find, automate, web, browser
- Requires web: yes
- Cost sensitive: yes
- **Confidence: 0.85+**
- **Action:** Claude Code will automatically invoke `gemini-delegator`

**Rule 4: Mixed Tasks → Sequential Approach**
- Research phase → Let `gemini-delegator` handle
- Design phase → Handle yourself (Claude)
- Implementation phase → Let `codex-delegator` handle
- **Use sequential thinking with automatic delegation**

---

## Detailed Examples (Claude Code Context)

### Example 1: Security Audit (No Delegation - You Handle It)

**User Request:**
"Analyze our authentication system for vulnerabilities"

**Task Analysis:**
```typescript
{
  complexity: 'high',
  requiresWeb: false,
  requiresSpeed: false,
  requiresContext: true,
  securityCritical: true,
  costSensitive: false,
  canParallelize: false,
  hasDependencies: false
}
```

**Decision:** Handle yourself (confidence: 0.95)
- Security analysis is your (Claude's) top strength (92/100)
- 44% faster and 25% more accurate on security tasks
- Requires deep context understanding (1M token window)

**Action:**
```
I'll perform the security audit myself:

1. First, let me read the authentication system files...
2. Then analyze for OWASP Top 10 vulnerabilities...
3. Review session management and token handling...
4. Identify potential attack vectors...
5. Provide prioritized recommendations...
```

---

### Example 2: Feature Implementation (Delegate to Codex)

**User Request:**
"Implement a user login function with JWT validation"

**Task Analysis:**
```typescript
{
  complexity: 'medium',
  requiresWeb: false,
  requiresSpeed: true,
  requiresContext: false,
  securityCritical: false,  // Implementation, not security design
  costSensitive: false,
  canParallelize: false,
  hasDependencies: false
}
```

**Decision:** Codex (confidence: 0.9)
- Code generation is Codex's strength (90.2% HumanEval)
- Fast implementation needed
- Straightforward task

**Action (Claude Code will do this automatically):**
```
This is a code generation task perfect for Codex. Let me delegate this...

[Claude Code automatically invokes codex-delegator subagent]
[Subagent executes: codex --dangerously-bypass-approvals-and-sandbox exec "Implement user login function..."]
[Result returned without consuming your tokens!]

Here's the implementation Codex generated...
```

**What you see:** Just the final result, NOT the intermediate process!

---

### Example 3: Research Task (Delegate to Gemini)

**User Request:**
"Find the best state management library for our React app in 2025"

**Task Analysis:**
```typescript
{
  complexity: 'low',
  requiresWeb: true,        // Needs internet research
  requiresSpeed: false,
  requiresContext: false,
  securityCritical: false,
  costSensitive: true,      // Research task, use cost-effective agent
  canParallelize: false,
  hasDependencies: false
}
```

**Decision:** Gemini (confidence: 0.95)
- Web research is Gemini's top strength (95/100)
- Most cost-effective for research tasks
- Native web search integration

**Action (Claude Code will do this automatically):**
```
This requires web research, which is perfect for Gemini. Let me gather that information...

[Claude Code automatically invokes gemini-delegator subagent]
[Subagent executes: gemini -p "Research state management..."]
[Result returned without consuming your tokens!]

Based on current research, here are the top options...
```

---

### Example 4: Mixed Task (Sequential with Multiple Delegations)

**User Request:**
"Create a new user registration feature with best practices"

**Task Analysis:**
```typescript
{
  complexity: 'high',
  requiresWeb: true,        // Research best practices
  requiresSpeed: false,
  requiresContext: true,    // Understand existing system
  securityCritical: true,
  costSensitive: false,
  canParallelize: false,
  hasDependencies: true     // Research → Design → Implementation
}
```

**Decision:** Sequential multi-agent approach

**Action:**
```
I'll break this into three phases:

**Phase 1 - Research (Gemini):**
First, let me research current best practices...
[gemini-delegator automatically invoked]
✓ Research complete

**Phase 2 - Security Design (Me/Claude):**
Based on the research, I'll design the security architecture:
- Database schema with proper constraints
- Password hashing with bcrypt
- Email verification workflow
- Rate limiting strategy
- GDPR compliance measures

**Phase 3 - Implementation (Codex):**
Now let me implement based on this design...
[codex-delegator automatically invoked]
✓ Implementation complete

All phases complete! Here's the full solution...
```

---

## Confidence Scoring Guide

Always provide a confidence score (0-1) for your delegation decision:

- **0.95-1.0**: Perfect match, obvious choice
  - Example: Security audit → Claude, Web research → Gemini

- **0.85-0.95**: Strong match, highly recommended
  - Example: Code generation → Codex, Refactoring → Claude

- **0.70-0.85**: Good match, reasonable choice
  - Example: Mixed complexity tasks, moderate specialization needed

- **0.50-0.70**: Moderate match, consider alternatives
  - Example: General tasks, multiple agents could work

- **< 0.50**: Weak match, probably don't delegate
  - Example: Simple tasks you can handle directly

---

## Common Anti-Patterns to Avoid

### ❌ Don't: Delegate Tasks You're Better At

```
# BAD: Claude delegating architecture to Codex
User: "Design our microservices architecture"
You: [Tries to delegate to Codex]

# GOOD: Claude handles architecture himself
User: "Design our microservices architecture"
You: "I'll design this myself as architecture is my specialty..."
```

### ❌ Don't: Over-Delegate Simple Tasks

```
# BAD: Overhead not worth it
User: "Add a console.log statement"
You: [Delegates to Codex]

# GOOD: Just handle it yourself
User: "Add a console.log statement"
You: [Adds the statement directly]
```

### ❌ Don't: Delegate Without Context

```
# BAD: Vague delegation
User: "Fix the bug"
You: [Delegates to Codex with no context]

# GOOD: Provide clear context
User: "Fix the bug"
You: [Analyzes the bug first, then delegates with specific details]
```

---

## Decision Tree Summary

```
Start: Analyze Task
    │
    ├─ Security/Architecture/Deep Analysis?
    │  └─ YES → Handle yourself (Claude) (0.9+ confidence)
    │
    ├─ Code Generation/Quick Implementation?
    │  └─ YES → codex-delegator (automatic) (0.85+ confidence)
    │
    ├─ Research/Web/Automation?
    │  └─ YES → gemini-delegator (automatic) (0.85+ confidence)
    │
    ├─ Multiple Independent Tasks?
    │  └─ YES → Sequential with appropriate delegations
    │
    ├─ Sequential Phases (Research→Design→Code)?
    │  └─ YES → Sequential: Gemini → Claude → Codex
    │
    ├─ Simple Task?
    │  └─ YES → Handle yourself (< 0.5 confidence for delegation)
    │
    └─ Complex Mixed Task?
       └─ YES → Break down and delegate appropriately
```

---

## Integration with Claude Code (Automatic)

When you're running in Claude Code as the primary agent:

1. **Recognize** tasks that match specialized agents
2. **Trust** that Claude Code will automatically invoke the right subagent
3. **Don't use special syntax** - just think about delegation naturally
4. **Receive results** without token overhead (separate context!)

### How It Works Behind the Scenes

```
You (Claude): "This is a code generation task perfect for Codex"
    ↓
Claude Code: Detects task matches codex-delegator description
    ↓
Task Tool: Invokes codex-delegator subagent
    ↓
Subagent: Runs codex CLI in separate context
    ↓
Result: Returned to you (without the intermediate output!)
    ↓
You: Continue with the result
```

**Key Benefits:**
- ✅ **Separate context** - Tokens don't impact your limit
- ✅ **Automatic invocation** - No special syntax needed
- ✅ **Clean results** - You only see the final output
- ✅ **Parallel capable** - Multiple delegations can run concurrently

---

## Quick Reference: Agent Selection Cheat Sheet

| Task Type | Primary Agent | Subagent | Confidence |
|-----------|---------------|----------|------------|
| Security Audit | Claude (you) | - | 0.95 |
| Architecture | Claude (you) | - | 0.95 |
| Refactoring | Claude (you) | - | 0.90 |
| Code Generation | Codex | codex-delegator | 0.95 |
| Quick Prototype | Codex | codex-delegator | 0.90 |
| Bug Fix | Codex | codex-delegator | 0.90 |
| Unit Tests | Codex | codex-delegator | 0.90 |
| Web Research | Gemini | gemini-delegator | 0.95 |
| Automation | Gemini | gemini-delegator | 0.95 |
| Documentation | Gemini | gemini-delegator | 0.85 |
| Mixed (R+D+I) | Sequential | Multiple | - |

---

## Final Notes for Claude Code Users

**Remember:** When you're Claude running in Claude Code:

1. **You are the architecture expert** - Handle complex design, security, and refactoring yourself
2. **Delegate code generation** - Let Codex handle implementation via automatic subagent invocation
3. **Delegate research** - Let Gemini handle web research via automatic subagent invocation
4. **Think sequentially** - For complex tasks, break into phases and delegate appropriately
5. **Trust the system** - Claude Code will invoke subagents automatically when appropriate

**The goal:** Leverage each agent's strengths for optimal results while keeping your context clean and efficient!

Use this skill to make informed delegation decisions that maximize the effectiveness of the multi-agent system! 🚀

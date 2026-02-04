---
name: critical-analysis-patterns
description: Philosophical/meta project analysis - critical analysis framework that asks "why?"
allowed-tools: ["Read", "Glob", "Grep", "Task"]
---

# Critical Analysis Patterns

Beyond technical validation, analyze **alignment between intent and implementation**.

---

## Canonical Implementation Principle 📐

> **skillmaker aims for "canonical implementation" of plugins, agents, and marketplaces.**

### Active Recommendation

When analyzing projects, **actively recommend skillmaker's "good practices"** for similar/equivalent features:

| Domain | Canonical Pattern | Skill to Load |
|--------|------------------|---------------|
| MCP integration | Daemon SSE isolation | `mcp-gateway-patterns` |
| Skill structure | Progressive disclosure | `skill-design` |
| Agent design | Context isolation | `orchestration-patterns` |
| Behavior enforcement | Hookification | `hook-templates` |
| Multi-stage workflow | State files + gates | `workflow-state-patterns` |
| Skill discovery | Keyword triggers | `skill-activation-patterns` |

### When Project Uses Different Approach

If the project uses a different method, determine:

| Question | Verdict | Action |
|----------|---------|--------|
| "Is this approach inferior?" | Deficient | **Recommend canonical pattern** |
| "Is this a valid domain-specific choice?" | Respectable | **Acknowledge and document trade-offs** |
| "Is this actually better?" | Superior | **Learn from it, consider adopting** |

### Evaluation Criteria

```markdown
## Deficiency Indicators (recommend change)
- Reinventing what skillmaker already solved
- Missing enforcement (MUST keywords without hooks)
- Ignoring known anti-patterns
- Unnecessary complexity vs canonical approach

## Domain-Specific Indicators (respect choice)
- Different constraints that invalidate canonical approach
- Performance requirements that justify deviation
- Ecosystem compatibility requirements
- Documented rationale for deviation
```

### Example: MCP Analysis

When project uses MCP:

1. **Load**: `Skill("skillmaker:mcp-gateway-patterns")`
2. **Check**: Is Daemon SSE pattern being used?
3. **If not**: 
   - Is there a documented reason?
   - Does their approach handle subagent isolation?
   - Recommend Daemon pattern if deficient

## Core Questions (6 Questions)

Ask these questions for every component:

### 1. Existence Justification
```
- "Why is this here?"
- "What breaks if we remove it?"
- "Can it be replaced with something else?"
```

### 2. Intent-Implementation Alignment
```
- "Does the name reflect the actual role?"
- "Does declared purpose match actual behavior?"
- "Are documentation and code synchronized?"
```

### 3. Consistency
```
- "Are similar things being handled differently?"
- "Are patterns A and B mixed?"
- "Is exceptional handling justified?"
```

### 4. Unused Capabilities
```
- "Is there something declared but not used?"
- "Is there something implemented but never called?"
- "Why isn't it being used?"
```

### 5. Complexity Justification
```
- "Is this complexity truly necessary?"
- "Is there a simpler alternative?"
- "Is this over-engineering?"
```

### 6. Fundamental Redesign 🔥

> **"Idiots, this solves everything - why can't you see it?"**

Beyond conservative solutions (deletion, exceptions, workarounds), ask questions that **eliminate constraints themselves**:

```
- "If this problem keeps recurring, isn't the system itself wrong?"
- "Are we taking this constraint/limitation for granted?"
- "Is there a completely different approach?"
- "If there's a 10x better method, what is it?"
- "If we rebuilt this from scratch, how would we do it?"
```

**When to apply**:
- Same type of problem found 3+ times
- Conservative solution feels like a "band-aid"
- Feeling of "why is this so complicated?"

---

## Analysis Process

### Step 1: Component Inventory
```bash
# Collect all components
agents/*.md, skills/*/SKILL.md, commands/*.md, hooks/hooks.json
```

### Step 2: Relationship Mapping
| From | To | Relationship |
|------|----|--------------| 
| command | agent | invokes via Task |
| agent | skill | loads via Skill() or frontmatter |
| hook | agent/skill | triggers on events |

### Step 3: Apply Core Questions
Apply 6 questions to each component and discover inconsistencies

### Step 4: Organize Findings

## Output Format

```markdown
### Philosophical Analysis Results

| Finding | Question | Suggestion |
|---------|----------|------------|
| {what} | {why?} | {alternative} |
```

---

## Red Flags (Signals That Require Immediate Questioning)

| Signal | Question | Details |
|--------|----------|---------|
| In agents/ but tools: [] | "Is this an agent or documentation?" | `Read("references/intent-vs-implementation.md")` |
| Declared skills unused | "Why declared but not used?" | `Read("references/unused-capability-detection.md")` |
| 90%+ similar workflows separated | "Is there a reason not to consolidate?" | `Read("references/architectural-smell-catalog.md")` |
| 20+ Hooks | "Is this over-engineering?" | Complexity justification required |
| Components with overlapping responsibilities | "Are boundaries clear?" | Role redefinition required |
| Non-canonical pattern used | "Is skillmaker's canonical approach applicable?" | Load relevant skill and compare |

---

## Solution Synthesis

> **Diagnosis + Prescription = Consulting**

When problems are found, provide solutions at **two levels**:

### Level 1: Conservative Solutions

Solutions found within existing patterns/skills:

| Finding Pattern | Related Skill | Solution Reference |
|----------------|---------------|-------------------|
| MCP/Gateway issues | `mcp-gateway-patterns` | `references/daemon-shared-server.md` |
| Skill design issues | `skill-design` | `references/structure-rules.md` |
| Agent orchestration | `orchestration-patterns` | `references/context-isolation.md` |
| Hook related | `hook-templates` | `references/full-examples.md` |
| Workflow state | `workflow-state-patterns` | `references/complete-workflow-example.md` |

### Level 2: Radical Solutions 🔥

> **"If you're confident, propose it even if it's not in existing patterns"**

When conservative solutions feel like **band-aids**, consider:

| Situation | Radical Question | Possible Proposal |
|-----------|-----------------|-------------------|
| Same problem recurring | "Is the system structure wrong?" | **Full architecture redesign** |
| Exceptions outnumber rules | "Is the rule itself wrong?" | **Discard and redefine rules** |
| Complex workarounds | "Why not tackle it head-on?" | **Remove the constraint itself** |
| Compatibility band-aids | "What if we drop legacy?" | **Execute breaking change** |
| Slow improvements | "What if we rebuild from scratch?" | **Clean slate reconstruction** |

**Criteria for proposing radical solutions**:
1. First explain limits of conservative solution
2. Explicitly state trade-offs of radical solution
3. Indicate **confidence level** (High/Medium/Exploratory)
4. Provide concrete execution steps

**Output format**:
```markdown
### 🔥 Radical Solution: {proposal}

**Why this is right**:
{rationale - fundamental limits of existing approach}

**Trade-off**:
- Gains: {benefits}
- Losses: {costs}

**Confidence Level**: High | Medium | Exploratory

**Execution Steps**:
1. {step 1}
2. {step 2}
...
```

**Detailed process**: `Read("references/solution-synthesis.md")`

---

## Quick Checklist

Items to verify quickly during analysis:

- [ ] Do all agents/ actually function as agents?
- [ ] Do skill declarations match Skill() usage?
- [ ] Can similar Hooks be extracted into common patterns?
- [ ] Are there old architecture remnants in documentation?
- [ ] Can each component's existence be explained in one sentence?
- [ ] Does the project follow skillmaker's canonical patterns?
- [ ] If different approach used, is there documented rationale?

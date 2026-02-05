---
name: claudemd-optimization
description: Optimize CLAUDE.md following best practices from humanlayer.dev - apply after /init to transform verbose output into focused, high-leverage project context
triggers:
  - "optimize claude.md"
  - "优化 claude.md"
  - "improve claude.md"
  - "refactor claude.md"
  - "claude.md 太长了"
  - "精简 claude.md"
---

# CLAUDE.md Optimization Skill

> Based on best practices from [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

## Core Principle: LLMs Are Stateless

**The only thing the model knows about your codebase is the tokens you put into it.**

CLAUDE.md automatically enters EVERY conversation, making it the highest leverage point in the entire system. A flawed instruction cascades through research, planning, and implementation phases.

---

## The Three Dimensions (WHAT / WHY / HOW)

Every CLAUDE.md should cover exactly these three dimensions:

| Dimension | Content | Example |
|-----------|---------|---------|
| **WHAT** | Technology stack, architecture, codebase structure | "React + Bun monorepo with 5 plugins" |
| **WHY** | Project purpose, what each component does | "Frontend plugin handles UI development" |
| **HOW** | Build tools, verification, testing, workflow | "Run `bun test`, use `/implement` command" |

---

## Optimization Rules

### Rule 1: Less Is More

```
❌ BAD:  500+ lines of detailed instructions
✅ GOOD: 60-300 lines of focused context (ideally < 150)
         HumanLayer's own CLAUDE.md is < 60 lines!
```

**Research-Backed Data:**

| Metric | Value | Implication |
|--------|-------|-------------|
| Frontier LLM instruction limit | ~150-200 | Beyond this, compliance drops |
| Claude Code system prompt | ~50 instructions | Already consumed! |
| **Your remaining budget** | **~100-150** | Every line counts |

**Critical Insight**: As instruction count increases, compliance quality decreases **uniformly across ALL instructions** - not just the later ones. This means bloated CLAUDE.md degrades even your most important rules.

**Model Size Matters:**
- **Frontier thinking models**: Linear decay (graceful degradation)
- **Smaller models**: Exponential decay (rapid failure)
- ⚠️ Avoid smaller models for multi-step tasks or complex plans

### Rule 2: Progressive Disclosure

**Don't cram everything into CLAUDE.md.** Create an `agent_docs/` directory for task-specific details:

```
agent_docs/
├── commands-and-agents.md    # Detailed command/agent reference
├── architecture-guide.md     # Deep architectural documentation
├── api-patterns.md           # API conventions and examples
├── testing-strategy.md       # Testing approaches
└── release-process.md        # Release workflow details
```

**Use pointers, not copies:**
```markdown
## Detailed Documentation

| Topic | Reference |
|-------|-----------|
| Commands | [agent_docs/commands-and-agents.md](agent_docs/commands-and-agents.md) |
| Architecture | [agent_docs/architecture-guide.md](agent_docs/architecture-guide.md) |
```

### Rule 3: LLM Attention Distribution

**LLMs bias towards instructions at the peripheries:**

```
┌─────────────────────────────────────────────────────┐
│  HIGH ATTENTION                                     │
│  ├── System prompt (Claude Code)                   │
│  └── CLAUDE.md (beginning)                         │
├─────────────────────────────────────────────────────┤
│  LOW ATTENTION                                      │
│  └── Middle of context window                       │
├─────────────────────────────────────────────────────┤
│  HIGH ATTENTION                                     │
│  └── Recent user messages (end)                     │
└─────────────────────────────────────────────────────┘
```

**Implication**: Put your most critical rules at the TOP of CLAUDE.md, not buried in the middle.

### Rule 4: Claude Is NOT a Linter

**Never put style rules in CLAUDE.md:**
- ❌ "Use 2-space indentation"
- ❌ "Always use semicolons"
- ❌ "Prefer const over let"

**Instead:**
- Use Biome/ESLint/Prettier for formatting
- Claude learns patterns from existing code (in-context learning!)
- Well-structured code demonstrates conventions

**Advanced Technique: Stop Hook**

Set up a [Stop Hook](https://code.claude.com/docs/en/hooks#stop) to run formatter after Claude finishes:

```json
// .claude/settings.local.json
{
  "hooks": {
    "Stop": [{
      "matcher": "*.{ts,tsx,js,jsx}",
      "command": "biome check --fix --unsafe"
    }]
  }
}
```

This separates implementation from formatting - **both improve as a result**.

### Rule 5: Never Auto-Generate

```
❌ DON'T: Use /init output directly
✅ DO:    Use /init as starting point, then manually optimize
```

**Why**: Every line has multiplicative impact. Auto-generated content includes noise that pollutes every conversation.

### Rule 6: Universal Applicability Only

Only include instructions that apply to EVERY task in this project:
- ✅ "This is a TypeScript monorepo"
- ✅ "Run tests with `bun test`"
- ❌ "When implementing auth, use JWT" (task-specific → agent_docs/)
- ❌ Detailed API patterns (task-specific → agent_docs/)

---

## Optimization Workflow

When user requests CLAUDE.md optimization, follow this workflow:

### Phase 1: Analysis

```bash
# Count current lines
wc -l CLAUDE.md

# Identify sections
grep "^##" CLAUDE.md
```

**Classify each section:**
- 🟢 KEEP (core WHAT/WHY/HOW)
- 🟡 MOVE (detailed → agent_docs/)
- 🔴 DELETE (redundant, outdated, task-specific noise)

### Phase 2: Create agent_docs Structure

```bash
mkdir -p agent_docs
```

**Move detailed content to appropriate files:**

| Content Type | Target File |
|--------------|-------------|
| Command/Agent lists | `agent_docs/commands-and-agents.md` |
| Architecture details | `agent_docs/architecture-guide.md` |
| API patterns/examples | `agent_docs/api-patterns.md` |
| Tool-specific guides | `agent_docs/{tool}-guide.md` |
| Version history | `agent_docs/release-history.md` |
| Protocol documentation | `agent_docs/{protocol}-protocol.md` |

### Phase 3: Rewrite CLAUDE.md

**Target structure (60-150 lines):**

```markdown
# Project Context for Claude Code

## Project Overview (WHAT)
[2-5 lines: name, purpose, owner]

## What This Repository Contains (WHY)
[Table or bullet list: components and their purposes]
[10-20 lines max]

## Directory Structure
[Simplified tree, 10-15 lines]

## How to Work with This Project (HOW)
[Quick setup, env vars, dependencies]
[15-25 lines]

## Key Architecture Decisions
[3-5 bullet points of universal principles]

## Important Files
[Table: role → files]

## Detailed Documentation (Progressive Disclosure)
[Table: topic → agent_docs/ reference]

## Project Rules
[3-5 universal rules that apply to EVERY task]
```

### Phase 4: Verification

```bash
# Verify line count
wc -l CLAUDE.md  # Should be 60-200 lines

# Verify agent_docs created
ls -la agent_docs/

# Verify no orphaned references
grep -r "agent_docs/" CLAUDE.md
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Fix |
|--------------|--------------|-----|
| 500+ lines | Degrades all instructions | Split to agent_docs/ |
| Code examples inline | May become outdated | Use file:line references |
| Version history in CLAUDE.md | Not universal | Move to agent_docs/release-history.md |
| Detailed protocols | Task-specific | Move to agent_docs/{protocol}.md |
| Style/linting rules | Use proper tools | Remove, use Biome/ESLint |
| Auto-generated content | Contains noise | Manual curation required |

---

## Quick Reference: Section Classification

### 🟢 KEEP in CLAUDE.md

- Project name, purpose, owner
- High-level directory structure
- Environment variables (list only)
- System dependencies
- Universal commands (`bun test`, `bun build`)
- Design principles (3-5 points)
- Important file references (table)
- Progressive disclosure table
- 3-5 universal project rules

### 🟡 MOVE to agent_docs/

- Detailed command documentation
- Agent specifications
- API patterns and examples
- Tool-specific guides (claudemem, etc.)
- Protocol documentation
- Version history and changelog details
- Architecture deep-dives
- Testing strategies

### 🔴 DELETE

- Redundant information
- Outdated content
- Task-specific instructions
- Inline code snippets (use references)
- Style/formatting rules
- Verbose explanations

---

## Example Transformation

**Before (982 lines):**
```markdown
## Commands and Agents Available
### Frontend Plugin
**Agents:**
- `typescript-frontend-dev` - TypeScript/React implementation (Sonnet)
- `frontend-architect` - Architecture planning (Sonnet)
[... 100+ lines of agent details ...]

## Claudemem AST Structural Analysis (v0.3.0)
[... 150+ lines of tool documentation ...]

## Parallel Multi-Model Execution Protocol
[... 180+ lines of protocol details ...]
```

**After (154 lines):**
```markdown
## Detailed Documentation (Progressive Disclosure)

| Topic | Documentation |
|-------|---------------|
| Commands & Agents | [agent_docs/commands-and-agents.md](agent_docs/commands-and-agents.md) |
| Claudemem Guide | [agent_docs/claudemem-guide.md](agent_docs/claudemem-guide.md) |
| Parallel Execution | [agent_docs/parallel-execution-protocol.md](agent_docs/parallel-execution-protocol.md) |
```

---

## Success Metrics

After optimization, verify:

- [ ] CLAUDE.md is 60-200 lines (ideally < 150)
- [ ] Contains only WHAT/WHY/HOW
- [ ] agent_docs/ directory exists with detailed docs
- [ ] Progressive disclosure table references agent_docs/
- [ ] No inline code examples (use file references)
- [ ] No style/linting rules
- [ ] No version history details
- [ ] All content is universally applicable

---
name: optimize
description: Optimize context usage for the session by reducing bloat, improving token efficiency, and focusing on relevant areas. Use when context is growing large, responses are slow, or switching between unrelated tasks. Covers context analysis, compacting, targeted pruning, MCP-first strategies, and focused scoping by area.
triggers:
  - optimize
---

# Optimize: Context Optimization Workflow

Complete guidance for optimizing context usage, reducing token consumption, and improving session efficiency.

## When to Use

- Context is growing large or responses are slowing down
- Approaching context window limits
- Switching between unrelated features or domains
- Responses lack relevance or precision
- Session continuity must be preserved during optimization

## Context Optimization Strategy

### Priority-Ordered Techniques

1. **Remove irrelevant context** - Identify files/turns not related to current task
2. **Use @file references** - Reference files instead of reading full contents
3. **Delegate to subagents** - Move independent research to parallel tasks
4. **MCP-first approach** - Use specialized MCP tools (Context7, Serena) instead of raw file reads
5. **Compress** - Use `/compact` when approaching 70% context window

### Optimization Modes

| Mode | Action | When to Use |
|------|--------|-------------|
| `analyze` | Report context state without changes | Diagnosing bloat, no immediate action needed |
| `compact` | Run `/compact` immediately | Approaching context limits, need instant reduction |
| `targeted` | Ask for current task, prune everything else | Switching domains, clear task focus available |
| `mcp-first` | Suggest MCP alternatives for raw reads | Using many manual file reads, want tool automation |
| `focus <area>` | Narrow to specific development area | Switching features, want domain-specific context |

## Context Analysis Framework

### Estimate Current Usage

- **Low**: <40% of window used, no urgency
- **Medium**: 40-70% used, monitor, may need soon
- **High**: 70-85% used, start optimization
- **Critical**: >85% used, optimize immediately

### Identify Top 3 Context Contributors

Typical large items:
- Large source files (>500 lines)
- Conversation history (many turns)
- Test outputs and logs
- Error traces and stack overflows
- Multiple dependency trees
- External docs or guides

### Relevance Assessment

For each large contributor, ask:
- Is this still needed for the current task?
- Was it loaded for a previous, completed task?
- Can it be referenced instead of loaded?
- Can an MCP tool provide it on-demand instead?

## Focused Scoping by Area

When switching development areas, use focused scoping to reduce noise:

### Area Patterns

| Area | Key Paths | Focus Signal |
|------|-----------|--------------|
| auth | `auth/`, `middleware/`, `session`, JWT, cookies | User management, login/signup |
| frontend | `components/`, `app/`, hooks, UI, styles, Tailwind | Component development, styling |
| backend | `api/`, `routes/`, `services/`, handlers | Endpoints, business logic |
| database | `migrations/`, `schema`, `models/`, RLS | Data layer, queries |
| testing | `__tests__/`, `*.test.*`, `*.spec.*` | Test development, coverage |
| payments | `billing/`, `stripe`, `subscription` | Payment processing |
| mcp | `tools/`, `server`, Zod schemas | Tool development |

When focusing on an area:

1. Identify all files, modules, tests related to the area
2. Summarize current state (recent changes, open issues, key files)
3. Set mental context: only suggest changes relevant to this area
4. List top 3-5 files to start with for any task in this area

## Compacting and Pruning

### When to Compact

- Context usage exceeds 70% window
- Response latency noticeably increases
- Model shows signs of context saturation (longer thinking, less precision)
- Switching to a completely unrelated task

### Compacting Strategy

1. Summarize conversation into key decisions and blockers
2. Drop irrelevant files from context
3. Replace full file reads with @file references
4. Move research tasks to `/dispatch` or subagent calls
5. Keep only task-critical information

### Targeted Pruning

When the next task is clear:

1. Ask: "What is the specific task ahead?"
2. Remove all context not required for that task
3. Keep only: task description, relevant code files, active blockers
4. Add back context incrementally if needed

## MCP-First Approach

### MCP Tools That Reduce Context Load

| Tool | Replaces |
|------|----------|
| Context7 | Manual doc reads (libraries, frameworks) |
| Serena | Symbol lookup, refactoring, codebase navigation |
| Bash (grep/find) | Massive file listings |
| GitHub API | Full diff reviews, PR inspection |

### Using MCP Instead of Raw Files

**Instead of reading a 400-line library file:**
```
Use Context7 to query library docs for the specific API
```

**Instead of searching codebase manually:**
```
Use Serena find_referencing_symbols to locate usage patterns
```

**Instead of loading CI logs:**
```
Use GitHub Actions API or ci-watch skill to get structured results
```

## Session State Preservation

### When to Use `context-save`

Preserve session state when:
- Work is not yet complete
- Decision points need to be remembered
- Complex interdependencies exist
- Session may be interrupted

Write to `~/.claude/handoffs/<project>/latest.md`:
- Current task and progress
- Key decisions made
- Active blockers
- Files under active development
- Next immediate step

### When to Use `session-cleanup`

Do a deliberate reset when:
- The old task is fully complete
- Switching to an unrelated project
- Accumulated stale context is causing confusion
- Starting fresh work with different assumptions

## Diagnostic Checklist

1. Identify current context bloat source
2. Confirm current task and scope
3. Measure estimated reduction if action taken
4. Choose the minimal technique that solves the problem
5. Verify relevance of remaining context after action

## Common Optimization Patterns

### Pattern: Slow Response

**Symptom**: Model takes longer to think, response latency increases

**Root cause**: Usually context bloat, not compute

**Fix**: Run `/optimize analyze`, identify largest items, remove irrelevant context

### Pattern: Loss of Focus

**Symptom**: Model suggests unrelated changes, forgets current task

**Root cause**: Too many active threads in context

**Fix**: Run `/optimize focus <area>` or `/compact`

### Pattern: Approaching Limits

**Symptom**: Context window warnings, truncation

**Root cause**: Accumulation of conversation and files

**Fix**: Run `/compact` immediately, then assess what should stay

### Pattern: Switching Tasks

**Symptom**: Need to move to a different feature

**Root cause**: Old task context is now noise

**Fix**: Run `/context-save` if work may resume, then `/optimize focus <new-area>`

## Output Format

```
Context Optimization Report
────────────────────────────
Current Usage:    [low/medium/high/critical] (est. N% of window)
Top 3 Items:      [item1, item2, item3] (N tokens each)
Relevance:        [yes/no for each, with reason]
Recommended Action: [compact/focus/mcp-first/delegate/none]
Estimated Savings:  [N% reduction expected]
Next Step:         [specific command or action]
```

## Outputs / Evidence

- Return the concrete optimization action or recommendation
- Include estimated token/context savings
- Note any preserved state that resumable work requires
- Suggest next actions for the current task

## Failure / Stop Conditions

- Stop if required context for the task is not identified
- Stop if optimization would drop critical information
- Do not optimize away preserved decisions or blockers
- Stop if the real problem is not context bloat

## Memory Hooks

- Read memory when prior session context affects optimization strategy
- Write memory only if this session establishes a durable context-management policy

---
name: sequential-thinking
description: Structure cognitive analysis using sequential reasoning chains. Use for codebase analysis, pattern extraction, complex problem decomposition, and building mental models before implementation.
---

# Sequential Thinking

Progressive disclosure framework for structured cognition and codebase analysis.

## Core Principles

1. **Question-First**: Define what you need to understand before using tools
2. **Reasoning Chains**: Each thought explicitly depends on previous thoughts
3. **Cognitive Branches**: Separate thinking tracks for different aspects
4. **Synthesis Before Action**: Complete understanding before extraction

## When to Use

- Analyzing new codebases
- Extracting reusable patterns
- Complex problem decomposition
- Building mental models
- Understanding domain-specific architectures

---

## All 12 tools via mcporter

| Tool | Required params | Purpose |
|------|----------------|---------|
| `start_session` | `problem, success_criteria` | Begin a new thinking session |
| `add_thought` | `content` | Add a thought to the current session |
| `create_branch` | `name, from_thought, purpose` | Fork reasoning into a parallel track |
| `merge_branch` | `branch_id` | Merge a branch back into main reasoning |
| `store_memory` | `content` | Store a reusable insight |
| `query_memories` | _(none)_ | Search memories by tags or content |
| `record_decision` | `decision_title, context, options_considered, chosen_option, rationale, consequences` | Capture architecture decisions |
| `explore_packages` | `task_description` | Find relevant installed packages |
| `export_session` | `filename` | Export session or memories to file |
| `list_sessions` | _(none)_ | List all saved sessions |
| `load_session` | `session_id` | Resume a specific session |
| `analyze_session` | _(none)_ | Get stats summary of current session |

---

## Process

### Phase 1: Problem Decomposition

```
# Check if session already loaded (server auto-loads last session on startup)
mcporter call sequential-thinking.analyze_session()

# If no active session, start one
mcporter call sequential-thinking.start_session(
  problem: "What fundamental questions must I answer?",
  success_criteria: "Clear understanding of core questions",
  session_type: "general"
)
```

### Phase 2: Structured Discovery

```
# Add initial thought — returns thought_id needed for branching
mcporter call sequential-thinking.add_thought(
  content: "FIRST PRINCIPLE: What is this fundamentally?",
  confidence: 0.9
)
# → save the returned thought_id

# Fork into parallel reasoning tracks
mcporter call sequential-thinking.create_branch(
  name: "conceptual-analysis",
  from_thought: "<thought_id from above>",
  purpose: "Understand concepts separate from implementation"
)
# → save the returned branch_id

mcporter call sequential-thinking.add_thought(
  content: "Pattern criteria: Generic, clear interfaces, domain-independent",
  branch_id: "<branch_id from above>"
)
```

### Phase 3: Synthesis

```
mcporter call sequential-thinking.merge_branch(
  branch_id: "<branch_id>",
  target_thought: ""
)
```

### Phase 4: Pattern Extraction

```
mcporter call sequential-thinking.query_memories(
  tags: "domain-specific,architectural-patterns",
  content_contains: "core-concept"
)

mcporter call sequential-thinking.store_memory(
  content: "Brief description of the pattern",
  code_snippet: "pure code without comments",
  language: "python",
  tags: "pattern,category"
)
```

---

## Full mcporter call reference

### start_session
```
mcporter call sequential-thinking.start_session(
  problem: "what to solve",
  success_criteria: "how to know it is done",
  session_type: "general"        # or "coding" — triggers explore_packages automatically
)
```
Returns: `session_id`

### add_thought
```
mcporter call sequential-thinking.add_thought(
  content: "reasoning step",
  branch_id: "<id>",             # optional — omit for main thread
  confidence: 0.8                # optional
)
```
Returns: `thought_id` — save this when you need to branch from it

### create_branch
```
mcporter call sequential-thinking.create_branch(
  name: "branch-name",
  from_thought: "<thought_id>",  # required — must be non-empty string
  purpose: "why this branch exists"
)
```
Returns: `branch_id`

### merge_branch
```
mcporter call sequential-thinking.merge_branch(
  branch_id: "<branch_id>",
  target_thought: ""             # optional — leave empty to merge into latest
)
```
Returns: `branch_id`, `target_thought`, `status: "merged"`

### store_memory
```
mcporter call sequential-thinking.store_memory(
  content: "what to remember",
  code_snippet: "pure code",     # optional
  language: "python",            # optional
  tags: "tag1,tag2"              # optional — comma-separated
)
```
Returns: `memory_id`

### query_memories
```
mcporter call sequential-thinking.query_memories(
  tags: "tag1,tag2",             # OR search; use & for AND: "tag1&tag2"
  content_contains: "/regex/"    # optional — wrap in // for regex
)
```
Returns: `memories[]`, `count`, `search_tips` when empty

### record_decision
```
mcporter call sequential-thinking.record_decision(
  decision_title: "What we decided",
  context: "why this decision was needed",
  options_considered: "option A vs option B",
  chosen_option: "option A",
  rationale: "because...",
  consequences: "this means..."
)
```
Returns: `decision_id`

### explore_packages
```
mcporter call sequential-thinking.explore_packages(
  task_description: "what I am trying to do",
  language: "python"             # optional, default python
)
```
Returns: `packages[]`, `count`

### export_session
```
mcporter call sequential-thinking.export_session(
  filename: "output.md",
  format: "markdown",            # or "json"
  export_type: "session"         # or "memories"
)
```

### list_sessions / load_session
```
mcporter call sequential-thinking.list_sessions()
mcporter call sequential-thinking.load_session(session_id: "<id>")
```

### analyze_session
```
mcporter call sequential-thinking.analyze_session()
```
Returns stats or `{"error": ...}` if no active session — use this before start_session

---

## Runtime Behaviors

| Behavior | When | Effect |
|----------|------|--------|
| Auto-load last session | MCP server starts | `current_session` already set — check with `analyze_session` first |
| Auto-trigger `explore_packages` | `start_session` with `session_type="coding"` | Scans installed packages; suppress with `package_exploration_required: false` |
| `query_memories` returns `[]` | No active session | Silent empty — not an error |
| `add_thought` with `explore_packages: true` | On `general` session | Does nothing — only activates for `coding` sessions |
| `dependencies` param in `add_thought` | Non-empty string | Broken — stored incorrectly, avoid using |

---

## Storage

```
memory-bank/
├── sessions/     # session .md files
├── memories/     # standalone memory .md files
└── patterns/     # pure code only (no comments, no docstrings)
```

---

## Workflow Examples

### Codebase Analysis
```
mcporter call sequential-thinking.start_session(
  problem: "Fundamental concepts in this codebase?",
  success_criteria: "Mental model of structure and reusable elements",
  session_type: "general"
)

mcporter call sequential-thinking.add_thought(content: "Initial observation about structure")
# save returned thought_id as t1

mcporter call sequential-thinking.create_branch(name: "architecture", from_thought: "<t1>", purpose: "Structural patterns")
mcporter call sequential-thinking.create_branch(name: "data-flow", from_thought: "<t1>", purpose: "Information flow")

mcporter call sequential-thinking.merge_branch(branch_id: "<arch-id>")
mcporter call sequential-thinking.merge_branch(branch_id: "<flow-id>")
```

### Architecture Decision
```
mcporter call sequential-thinking.record_decision(
  decision_title: "Storage format choice",
  context: "Need persistent session storage",
  options_considered: "JSON vs Markdown",
  chosen_option: "Markdown",
  rationale: "Human-readable, diffable, no parser needed",
  consequences: "Regex parsing required for reload"
)
```

---

## Anti-Patterns

- Calling `start_session` without checking `analyze_session` first — may create duplicate session
- Passing empty string to `from_thought` in `create_branch` — raises ValidationError
- Using `dependencies` param in `add_thought` — broken for non-empty values
- Tool-first thinking — define what to understand before calling tools
- Comments or docstrings in stored code patterns

## Key Insight

Sequential thinking is NOT about organizing tools — it is about structuring COGNITION. Tools serve your thinking process, not replace it.

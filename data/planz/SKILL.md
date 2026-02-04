---
name: planz
description: Manage hierarchical project plans in SQLite. Tree-based structure with phases and tasks. Multiple output formats (text, JSON, XML, markdown).
---

# planz - Hierarchical Project Planning

Binary: `~/.local/bin/planz` | DB: `~/.local/share/planz/plans.db (SQLite WAL)

## Fractal Planning: Refine Until Nothing is Left for Interpretation

**The core principle:** Start with a high-level outline, then iteratively refine each node until every leaf task is so specific that executing it requires no further thought or decision-making.

### The Process

1. **Start broad** - Create 3-7 top-level phases that capture the major milestones
2. **Identify ambiguity** - Look at each leaf node and ask: "Could I execute this right now without any decisions?"
3. **Refine the unclear** - Use `planz refine` to break down ambiguous nodes into smaller, clearer steps
4. **Repeat** - Continue until every leaf node is atomic and unambiguous
5. **Execute & update** - Work through leaves, marking done, and refine new ambiguity as it emerges

### ⚠️ Important: No Slashes in Task Names

The `/` character is the path separator. **Never use slashes in task titles:**

```bash
# ❌ WRONG - creates nested path "API" -> "auth endpoint"
planz add myplan "API/auth endpoint"

# ✅ CORRECT - use other separators
planz add myplan "API - auth endpoint"
planz add myplan "API: auth endpoint"
planz add myplan "API auth endpoint"
```

### What "Nothing Left for Interpretation" Means

A leaf node is **ready for execution** when:
- ✅ You know exactly which file(s) to touch
- ✅ You know the specific change to make
- ✅ No design decisions remain
- ✅ Success criteria is obvious

A leaf node **needs refinement** when:
- ❌ "Implement feature X" - What does that entail?
- ❌ "Set up database" - Which tables? What schema?
- ❌ "Add tests" - Which scenarios? What coverage?

### Example: Fractal Refinement in Action

```bash
# Start broad
planz create auth-system
planz add auth-system "Phase 1: Design"
planz add auth-system "Phase 2: Implementation"  
planz add auth-system "Phase 3: Testing"

# Phase 2 is ambiguous - refine it
planz refine auth-system "#2" \
  --add "User registration" \
  --add "Login flow" \
  --add "Session management"

# "Login flow" [4] is still ambiguous - refine further
planz refine auth-system "#4" \
  --add "POST /auth/login endpoint" \
  --add "Password verification with bcrypt" \
  --add "JWT token generation" \
  --add "Set httpOnly cookie"

# "JWT token generation" [7] - is this specific enough?
# Ask: Can I implement this without decisions? 
# Maybe not - what claims? what expiry?
planz refine auth-system "#7" \
  --add "Create JWT with claims: sub, email, iat, exp" \
  --add "Set expiry to 24 hours" \
  --add "Sign with RS256 using env.JWT_PRIVATE_KEY"

# Now each leaf is atomic and unambiguous
planz show auth-system
```

### When to Stop Refining

Stop when the leaf node title itself is almost the code comment you'd write:
- "Add `user_id` index to sessions table" ✅
- "Validate email format with regex in `validateInput()`" ✅
- "Return 401 if `password_hash` doesn't match" ✅

### During Implementation

```bash
# Before starting work, check the plan
planz show myplan --xml

# Pick a leaf node, implement it, mark done
planz done myplan "#12"

# Discovered complexity? Refine on the fly
planz refine myplan "#15" --add "Handle edge case X" --add "Handle edge case Y"

# Check progress
planz progress myplan
```

---

## Overview

Plans are **hierarchical trees** with up to 4 levels of nesting. Each node has:
- **ID** (stable, per-plan auto-increment, shown as `[1]`, `[2]`, etc.)
- **Title** (unique among siblings, no slashes)
- **Description** (optional prose for context)
- **Done status** (checkbox)

## Node Identification

Nodes can be referenced by **path** OR **ID**:

```bash
# By path (human-readable)
planz done myplan "Phase 1/Database/Create schema"

# By ID (stable, survives renames)  
planz done myplan "#5"
```

IDs are shown in output: `- [ ] Create schema [5]`

## Commands

### Plan Management

```bash
planz create <plan>                              # Create empty plan
planz rename-plan <old> <new>                    # Rename a plan  
planz delete <plan>                              # Delete plan and all nodes
planz list                                       # List all plans for project
planz projects                                   # List all projects
planz delete-project                             # Delete project and all plans
planz summarize <plan> --summary "..."           # Set plan summary
```

### Node Management

```bash
planz add <plan> <path> [--desc "..."]           # Add node at path
planz remove <plan> <node> [--force]             # Remove node (--force for children)
planz rename <plan> <node> <new-name>            # Rename node
planz describe <plan> <node> --desc "..."        # Set node description
planz move <plan> <node> --to <parent>           # Move to new parent
planz move <plan> <node> --after <sibling>       # Reorder among siblings
planz refine <plan> <node> --add <child>...      # Expand leaf into subtree
```

### Status

```bash
planz done <plan> <node>...                      # Mark done (cascades DOWN to children)
planz undone <plan> <node>...                    # Mark undone (propagates UP to ancestors)
```

### Viewing

```bash
planz show <plan> [node]                         # Text output (default)
planz show <plan> --json                         # JSON output
planz show <plan> --xml                          # XML output (best for agents)
planz show <plan> --md                           # Markdown output
planz progress <plan>                            # Progress bars per top-level node
```

## Path Syntax

Slash-separated node titles:
```
"Phase 1"                           # Root node
"Phase 1/Database"                  # Child of Phase 1
"Phase 1/Database/Create schema"    # Grandchild
```

- **Max depth**: 4 levels
- **No slashes** allowed in titles
- **Unique titles** within same parent

## Output Formats

### Text (default)
```
# myplan

- [x] Phase 1: Setup [1]
  - [x] Install deps [2]
  - [x] Configure env [3]
- [ ] Phase 2: Implementation [4]
  - [ ] Build API [5]
```

### XML (`--xml`) - Best for agents
```xml
<?xml version="1.0" encoding="UTF-8"?>
<plan name="myplan">
  <node id="1" title="Phase 1: Setup" done="true">
    <node id="2" title="Install deps" done="true" />
    <node id="3" title="Configure env" done="true" />
  </node>
  <node id="4" title="Phase 2: Implementation" done="false">
    <description>Core implementation work</description>
    <node id="5" title="Build API" done="false" />
  </node>
</plan>
```

### JSON (`--json`)
```json
[{"id":1,"title":"Phase 1: Setup","done":true,"children":[...]}]
```

## Options

| Option | Description |
|--------|-------------|
| `--project <path>` | Project path (default: cwd) |
| `--desc <text>` | Description for add/describe |
| `--summary <text>` | Summary for summarize |
| `--force` | Force remove nodes with children |
| `--json` | JSON output |
| `--xml` | XML output |
| `--md` | Markdown output |
| `--to <path>` | Target parent for move |
| `--after <sibling>` | Sibling to position after |
| `--add <child>` | Child path for refine (repeatable) |

## Cascade Behavior

- **`done`**: Marks node AND all descendants as done. If all siblings become done, parent auto-marks done.
- **`undone`**: Marks node as undone AND propagates up (all ancestors become undone).
- **`remove`**: Deletes node and all descendants (CASCADE). Use `--force` if node has children.

## Error Handling

When a command fails:
- Check if the plan exists: `planz list`
- Check if the node path/ID is correct: `planz show <plan>`
- For "max depth exceeded": You've hit 4 levels, restructure or use descriptions instead
- For "duplicate title": Sibling nodes must have unique names

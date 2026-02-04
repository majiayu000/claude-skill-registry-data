---
name: explore-and-document
description: Systematically explore unfamiliar codebases and document findings using Julie's code intelligence, Sherpa's exploration workflow, and Goldfish's documentation. Activates when learning new code with semantic search, architecture mapping, and persistent documentation.
allowed-tools: mcp__julie__fast_search, mcp__julie__get_symbols, mcp__julie__trace_call_path, mcp__julie__fast_explore, mcp__julie__fast_refs, mcp__sherpa__approach, mcp__sherpa__guide, mcp__goldfish__checkpoint, mcp__goldfish__plan, Read
---

# Explore and Document Workflow

## Purpose
**Systematically understand unfamiliar codebases** and preserve findings for future reference. Combines Julie's efficient code exploration, Sherpa's exploration workflow, and Goldfish's documentation persistence.

## When to Activate
- "understand this codebase", "explore this code"
- "how does this work?", "explain the architecture"
- "I'm new to this project", "onboard me"
- "document the structure", "map this codebase"

## Trinity for Exploration

**Julie:** Semantic search, symbol structure, call tracing (token-efficient!)
**Sherpa:** Exploration workflow phases (Learn → Investigate → Prototype → Document)
**Goldfish:** Checkpoint discoveries, document architecture via plans

## Orchestration

### Phase 1: Learn the Landscape (Julie + Sherpa)
```
approach({ workflow: "exploration" })
guide() → "Phase 1: Learn - Understand the landscape"

Julie exploration:
- fast_explore() → Overall architecture
- fast_search → Find key components
- get_symbols → File structures (70-90% token savings!)

checkpoint({ description: "Mapped architecture: [layers/components found]" })
guide({ done: "understood overall architecture" })
```

### Phase 2: Investigate Patterns (Julie + Sherpa)
```
guide() → "Phase 2: Investigate - Dig deeper into patterns"

Julie investigation:
- trace_call_path → Understand execution flows
- fast_refs → See usage patterns
- Semantic search → Find related code

checkpoint({ description: "Investigated [feature]: uses [pattern], connects to [components]" })
guide({ done: "mapped key patterns and relationships" })
```

### Phase 3: Prototype Understanding (Optional)
```
guide() → "Phase 3: Prototype - Try things out"

Optional: Write small test code to verify understanding

checkpoint({ description: "Verified understanding: [what was tested]" })
```

### Phase 4: Document Findings (Goldfish + Sherpa)
```
guide() → "Phase 4: Document - Record your findings"

Create architecture documentation plan:
plan({
  action: "save",
  title: "[Codebase] Architecture Analysis",
  content: "## Architecture...\n## Key Components...\n## Patterns..."
})

checkpoint({ description: "Documented [codebase] architecture and patterns" })
guide({ done: "documentation complete" })
```

## Example: Exploring New Codebase

```markdown
User: "Help me understand this authentication system"

PHASE 1: LEARN
→ approach({ workflow: "exploration" })
→ fast_search({ query: "authentication", mode: "semantic" })
  Found: auth.ts, jwt.ts, user-service.ts

→ get_symbols on each (token-efficient!)
  - auth.ts: AuthMiddleware class
  - jwt.ts: JWT utilities
  - user-service.ts: User management

→ checkpoint({ description: "Auth system has 3 layers: middleware, JWT utils, user service" })

PHASE 2: INVESTIGATE
→ trace_call_path({ symbol: "authenticate", direction: "downstream" })
  Flow: authenticate → validateToken → jwt.verify → UserService.findById

→ fast_refs({ symbol: "authenticate" })
  Used in: 15 routes across api.ts, admin.ts

→ checkpoint({ description: "Auth flow: JWT middleware validates tokens via UserService, protects 15 routes" })

PHASE 4: DOCUMENT
→ plan({
    action: "save",
    title: "Authentication System Architecture",
    content: "## Overview\nJWT-based authentication...\n## Components\n..."
  })

→ checkpoint({ description: "Documented auth system architecture with flow diagrams" })

Result: Complete understanding documented, survives context resets!
```

## Token Efficiency Pattern

**Traditional exploration:**
```
Read auth.ts (500 lines) → 12,000 tokens
Read jwt.ts (300 lines) → 7,200 tokens
Read user-service.ts (600 lines) → 14,400 tokens
Total: 33,600 tokens!
```

**Julie-powered exploration:**
```
get_symbols(auth.ts, mode="structure") → 800 tokens
get_symbols(jwt.ts, mode="structure") → 500 tokens
get_symbols(user-service.ts, mode="structure") → 900 tokens
Total: 2,200 tokens (93% savings!)
```

## Goldfish Documentation Patterns

**Architecture Plans:**
```
plan({
  title: "[System] Architecture",
  tags: ["architecture", "documentation"],
  content: "## Layers\n## Components\n## Patterns\n## Data Flow"
})
```

**Discovery Checkpoints:**
```
checkpoint({
  description: "Discovered: [finding]",
  tags: ["exploration", "discovery", "architecture"]
})
```

**Pattern Documentation:**
```
checkpoint({
  description: "Pattern: [name] - [description]",
  tags: ["pattern", "architecture"]
})
```

## Key Behaviors

**✅ DO:**
- Start with semantic search
- Use get_symbols for structure (massive token savings!)
- Trace execution paths
- Document incrementally in Goldfish
- Create architecture plan
- Let Sherpa guide phases

**❌ DON'T:**
- Read entire files without checking symbols first
- Skip documentation (defeats the purpose!)
- Forget to trace execution flows
- Ignore Goldfish checkpointing

---

**Efficient exploration: Search semantically, explore efficiently, document persistently!**

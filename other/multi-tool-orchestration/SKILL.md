---
name: multi-tool-orchestration
description: |
  Build a multi-tool orchestration system with fallback chains and cost optimization.
  
  Use this skill whenever you need to:
  - Architect a system that uses Claude AND another AI tool (Gemini, Copilot, Codex) with automatic fallback
  - Implement tool rankings by command type (which tool runs first, second, third)
  - Set up cost optimization (auto-select cheaper tools for bulk work)
  - Create tool-specific adapters (state sync, constraints, error handling per tool)
  - Build a fallback decision tree (Tool A fails → Try Tool B → Try Tool C)
  - Design file versioning for multi-tool outputs (avoid conflicts when multiple tools generate content)
  - Set up performance tracking and monitoring across tools
  
  Whether you're building a guide-agent, orchestrator, CLI tool, or standalone system, this skill generates a complete multi-tool architecture that's production-ready, scalable, and extensible.
  
  Works with Claude, Gemini, Copilot, Codex — and easily extensible to any AI tool.

compatibility: |
  - Requires Python 3.8+ (for scripts)
  - JSON-based configs (no external dependencies)
  - Works with any orchestration framework (guide-agent, custom router, API server, CLI)
---

# Multi-Tool Orchestration Skill

## Overview

This skill generates a complete, production-ready multi-tool orchestration system that allows you to:
- Route commands to the best tool for each task (ranked by performance/cost/quality)
- Automatically fall back to secondary tools if the primary fails (timeout, API error, quality gates)
- Optimize for cost (use cheaper Gemini for bulk work, use quality Claude for critical content)
- Track tool performance and adapt rankings monthly
- Handle file conflicts when multiple tools produce outputs (version by tool)
- Manage state across tools (global state + tool-specific state)

**Use cases:**
- Building a guide-agent with tool selection logic
- Creating a multi-tool API router
- Developing a CLI that can use Claude, Gemini, Copilot, or specialized tools
- Implementing A/B testing between tools
- Cost-optimizing an AI workload (use expensive Claude strategically, cheap Gemini for scale)

---

## How to Use This Skill

### Step 1: Describe Your Orchestration Needs

Tell me about your system:
- **What tools do you want to use?** (Claude, Gemini, Copilot, Codex, others?)
- **What's your use case?** (content generation, code, analysis, automation, multi-step workflows?)
- **Where does this run?** (guide-agent, standalone API, CLI tool, cloud function, local?)
- **Do you have an existing system?** (Claude-only now, or completely new?)
- **What matters most?** (quality, cost, speed, redundancy?)

### Step 2: I'll Generate Your Architecture

I'll create:
1. **Canonical tool interface** (`interface.json`) — Contract every tool must implement
2. **Tool-specific adapters** (claude_adapter.md, gemini_adapter.md, etc.) — How each tool integrates
3. **Command router** (commands.json or .md) — Tool rankings for each command type
4. **Fallback routing logic** — Decision trees for when Tool A fails, try Tool B
5. **Data ownership rules** — How to version files when multiple tools write
6. **State management** — Global state + per-tool state + performance logs
7. **Integration guide** — How to wire this into your system
8. **Test cases + validation checklist**

### Step 3: Test & Iterate

I'll create realistic test scenarios, run them, and refine based on feedback until the system works perfectly for your needs.

---

## Generated Architecture Components

When you use this skill, you'll get these files:

```
your-orchestration-system/
├── tool-adapters/
│   ├── interface.json              # Canonical tool contract
│   ├── claude_adapter.md           # Claude implementation
│   ├── gemini_adapter.md           # Gemini implementation
│   ├── copilot_adapter.md          # (optional) Copilot
│   ├── codex_adapter.md            # (optional) Code specialization
│   └── _fallback_routing.md        # Tool selection + fallback logic
│
├── commands.json / commands.md     # Tool rankings per command type
├── data_ownership.md               # File versioning rules
├── integration_guide.md            # How to wire into your system
│
├── state-management/
│   ├── global_state.md             # Shared state structure
│   ├── tool_state_schema.md        # Per-tool state template
│   └── performance_tracking.md     # Metrics + adaptation rules
│
└── test-cases/
    ├── basic_tool_selection.md     # Verify right tool chosen
    ├── fallback_chain.md           # Verify fallback works
    ├── cost_optimization.md        # Verify cheap tool used for bulk
    └── file_versioning.md          # Verify no conflicts on multi-tool output
```

---

## Key Features

### 1. Tool Ranking by Command Type
```
/create blog-posts   → Rank 1: Claude (best quality)
                     → Rank 2: Gemini (fallback)
                     → Rank 3: Copilot (safety net)

/optimize images     → Rank 1: Gemini (multimodal)
                     → Rank 2: Claude (fallback)

/scrape website      → Rank 1: Codex (code specialist)
                     → Rank 2: Claude (fallback reasoning)
```

### 2. Automatic Fallback Chain
```
Tool A (Rank 1) → Success ✓ Done
              ↓ Timeout/Fail
Tool B (Rank 2) → Success ✓ Done
              ↓ Fail
Tool C (Rank 3) → Success ✓ Done
              ↓ All fail → Error
```

### 3. Cost Optimization
```
≤30 items to process  → Use Claude (best quality)
>30 items to process  → Use Gemini (5x cheaper)
```

### 4. File Versioning (Multi-Tool Conflict Prevention)
```
Claude generates      → content/[slug]_[tool]_v[version].md
Gemini generates      → content/[slug]_[tool]_v[version].md
Both coexist ✓        → User chooses via /merge command
```

### 5. State Management
```
Global state (.ai/memory/state.json)
  ├─ Pipeline stage
  ├─ Last command
  └─ Last tool used

Per-tool state (.ai/memory/multi-tool-state/)
  ├─ claude.session.json (tokens, cost, history)
  ├─ gemini.session.json
  └─ [tool].session.json

Performance log (.ai/logs/tool-performance.jsonl)
  └─ Metrics for ranking updates
```

---

## Example Scenario: Sovereign Interior Design Studio

**Problem:** Using Claude alone means:
- Single point of failure (Claude API down? No work)
- High cost for bulk optimization (100+ blog posts = expensive)
- Can't analyze images without external tools

**Solution with Multi-Tool Orchestration:**
1. `/create blog-posts` → Try Claude first (best brand voice)
2. Claude times out? → Fallback to Gemini (cheaper, faster)
3. `/optimize images` → Always use Gemini (multimodal, sees images)
4. Bulk polish (>30 articles) → Use Gemini (save 80% cost)
5. Critical landing page? → Force Claude (quality over cost)

**Result:**
- ✓ Redundancy (Claude down? Gemini takes over)
- ✓ Cost savings (Gemini for 80% of work)
- ✓ Capabilities (Gemini for images, Claude for reasoning)
- ✓ Quality (Claude for critical, Gemini for bulk)
- ✓ All files versioned safely (no conflicts)

---

## Integration Paths

This skill generates architecture. Integration depends on your system:

### Option A: guide-agent Router
```
User command
    ↓
guide-agent reads commands.json
    ↓
Looks up Rank 1, 2, 3 tools
    ↓
Loads tool adapter
    ↓
Executes with Rank 1
    ↓
Success? → Done
Fail?    → Try Rank 2 (etc.)
```

### Option B: Custom API Router
```
POST /orchestrate
  {
    "command": "/create blog-posts",
    "parameters": {...}
  }
    ↓
Router reads commands.json
    ↓
Spawns tool request (Claude first)
    ↓
Polls/awaits response
    ↓
On failure, retry with Gemini
    ↓
Return result (with tool metadata)
```

### Option C: CLI Wrapper
```
$ sovereign /create blog-posts --topic design
    ↓
CLI reads commands.json
    ↓
Determines Rank 1 tool (Claude)
    ↓
Calls Claude API with context
    ↓
Returns output
    ↓
$ sovereign /create blog-posts --tool gemini  (force tool)
```

---

## Workflow

### For a Completely New System:
1. Tell me your tools + use case
2. I generate the full architecture
3. Test on realistic scenarios
4. Iterate until it's solid
5. You integrate into your system

### For Augmenting an Existing Claude-Only System:
1. Tell me your current setup
2. I generate adapters for new tools
3. Create the routing + fallback layer
4. Test integration points
5. Wire it in without breaking existing code

---

## Next Steps

Ready to build? Tell me:

1. **Which tools?** (Claude + Gemini? + Codex? + Copilot?)
2. **What's the use case?** (Content? Code? Analysis? Workflows?)
3. **Where does it run?** (guide-agent? API? CLI? Reference?)
4. **Starting point?** (New or augment existing?)
5. **Priority?** (Quality? Cost? Speed? Reliability?)

I'll generate a tailored architecture, test it, and iterate until it's perfect.


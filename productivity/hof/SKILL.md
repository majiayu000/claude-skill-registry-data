---
name: hof
description: 'Hofstadter-io hof: CUE-powered code generation with flow engine and
  VS Code agent'
source: hofstadter-io/hof (Go + CUE)
license: Apache-2.0
trit: -1
gf3_conserved: true
repo_divergence: MEDIUM (DeepWiki shows old hof, repo is now VS Code agent focus)
last_commit: 2025-12-25 (active _next branch)
metadata:
  interface_ports:
  - Related Skills
  - Integration with
---
# Hof (-1)

> CUE-based code generation. Now building VS Code coding agent.

**Trit**: -1 (MINUS - reductive/extractive code generation)
**Language**: Go (core), CUE (schemas), TypeScript (VS Code)
**Branch**: `_next` (active development)

## DeepWiki vs Repo Divergence Analysis

| DeepWiki Claims | Actual Repo State | Divergence |
|-----------------|-------------------|------------|
| "Code Generation System" | ✓ lib/gen, schemas/ | LOW |
| "Module System" | ✓ lib/mod | LOW |
| "Task Engine / Flow" | ✓ flow/, flow.cue | LOW |
| "TUI Eval Module" | Deprecated, now VS Code | HIGH |
| "Formatters" | ✓ formatters/ | LOW |

**Key Finding**: Major pivot to VS Code agent (lib/agent, extensions/vscode/).

## Current Focus (from AGENTS.md)

```
We are currently developing a vscode extension for a custom coding agent setup, 
a copilot alternative and then some.

- lib/agent        - backend server (Go + ADK)
- extensions/vscode/extension  - extension core
- extensions/vscode/webviews/chat  - chat interface
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Core | Go, CUE |
| Agent | ADK-Go (Agent Development Kit) |
| VS Code | TypeScript, pnpm, vite, react |
| UI | tanstack, shadcn, tailwind |
| CI | Dagger, Docker |

## CUE Code Generation

```cue
// schemas/gen.cue - Generator schema
#Generator: {
    // Input data
    In: {...}
    
    // Output files
    Out: [...#File]
    
    // Templates
    Templates: [...#Template]
    
    // Partials (reusable snippets)
    Partials: [...#Template]
}

#File: {
    Filepath: string
    Contents: string | bytes
}

#Template: {
    Name: string
    Source: string
}
```

## Flow Engine

```cue
// flow.cue - Task orchestration
package flow

import "hof.io/flow"

// Define tasks
@flow(build)
build: {
    gen: flow.#Gen & {
        Generator: "..."
    }
    
    fmt: flow.#Exec & {
        cmd: "gofmt -w ."
        dep: [gen]
    }
}
```

## Veggie: The _next Branch Coding Agent

**Name**: Veggie (veg)  
**Status**: Active development (commits daily Dec 2025)  
**Architecture**: Dagger-powered virtualized workspaces + ADK-Go + MCP

### Architecture

```
VS Code Extension ──WebSocket──► Agent Runtime ──► Dagger Environs
     │                               │
     │                               ├──► Tools (fs, exec, cache)
     │                               ├──► MCP (GitHub, Tavily)
     └── React Webviews              └──► LLM Models (Gemini, etc)
```

### Tools Available

| Tool | Description |
|------|-------------|
| `fs_read/write/edit` | File ops via Dagger |
| `fs_list/glob/grep` | File discovery |
| `exec` | Shell execution |
| `cache_*` | Persistent state |

### MCP Integrations

| Toolset | Endpoint |
|---------|----------|
| GitHub | `api.githubcopilot.com` |
| Tavily | `mcp.tavily.com` |
| Local | In-memory demo |

### Agent Config (CUE)

```go
type Agent struct {
    Name, Model, Instruction string
    Tools, Toolsets, Mcp     []string
    SubAgents                []string
    Environ                  string // Dagger container
}
```

## Project Structure

```
hofstadter-io/hof/
├── AGENTS.md           # AI agent instructions
├── lib/
│   ├── agent/          # Veggie backend (ADK-Go)
│   │   ├── agents/     # CUE config loading
│   │   ├── runtime/    # WebSocket server, session mgmt
│   │   ├── tools/      # filesys, exec, cache, mcp
│   │   └── models/     # LLM clients (gemini.go)
│   ├── gen/            # Code generator (legacy)
│   └── chat/           # LLM chat (openai, google, cosign)
├── extensions/vscode/
│   ├── extension/      # VS Code extension (TypeScript)
│   └── webviews/       # React chat UI (shadcn, tailwind)
├── flow/               # CUE workflow engine
└── schemas/            # CUE schemas
```

## Usage

```bash
# Install hof
go install github.com/hofstadter-io/hof/cmd/hof@latest

# Initialize project
hof mod init my-project

# Generate code from CUE
hof gen ./design/... -T ./templates

# Run flow
hof flow build

# Development (VS Code extension)
cd extensions/vscode
pnpm install
pnpm dev
```

## GF(3) Triad with Config Languages

```
CUE (+1)    + Nickel (0)  + Hof (-1)    = 0 ✓
 │              │             │
 │              │             └── Consumes schemas, emits code
 │              └── Mediates types/contracts
 └── Generates schemas via unification
```

## Sexp Neighborhood

| Skill | Trit | Bridge to Hof |
|-------|------|---------------|
| **cue-lang** | +1 | Hof consumes CUE schemas |
| **nickel** | 0 | Alternative config, gradual typing |
| **lispsyntax-acset** | 0 | Config → sexp → ACSet |
| **borkdude** | +1 | Babashka for scripting |
| **geb** | +1 | Categorical config semantics |

## VS Code Agent Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   HOF VS CODE AGENT                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   VS Code Extension                                      │
│   ┌─────────────────────────────────────────────────┐   │
│   │ extensions/vscode/extension/                     │   │
│   │ - Commands, activation                           │   │
│   │ - Webview hosting                                │   │
│   └─────────────────────────────────────────────────┘   │
│                          │                               │
│                          ▼                               │
│   React Webviews                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │ extensions/vscode/webviews/chat/                 │   │
│   │ - tanstack, shadcn, tailwind                     │   │
│   │ - Chat interface                                 │   │
│   └─────────────────────────────────────────────────┘   │
│                          │                               │
│                          ▼                               │
│   Agent Backend (ADK-Go)                                 │
│   ┌─────────────────────────────────────────────────┐   │
│   │ lib/agent/                                       │   │
│   │ - Tool execution                                 │   │
│   │ - LLM integration                                │   │
│   │ - Flow orchestration                             │   │
│   └─────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Key Dependencies

| Dependency | Purpose |
|------------|---------|
| `google.golang.org/adk` | Agent Development Kit |
| `dagger.io/dagger` | Container virtualization |
| `gorm.io/gorm` | Session persistence |
| `github.com/gorilla/websocket` | Client communication |
| `cuelang.org/go/cue` | Agent configuration |

## Commit Pattern

```
(veg) implement clone & splice handlers  ← AI-generated
(human) swap button order in session-menu ← Manual
```

---

**Trit**: -1 (MINUS - code generation is reductive extraction)
**Key Property**: CUE → code generation, now VS Code agent pivot
**Active Branch**: `_next`
**Full Architecture**: See ~/ies/VEGGIE_ARCHITECTURE_COMPLETE.md

---

## End-of-Skill Interface

## Integration with Sexp Skills

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONFIG LANG TRIAD                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CUE (+1)              Nickel (0)              Hof (-1)        │
│   ┌──────────────┐     ┌──────────────┐       ┌──────────────┐  │
│   │ Lattice-based│     │ Gradual      │       │ Code gen     │  │
│   │ unification  │     │ typing +     │       │ from CUE     │  │
│   │              │     │ contracts    │       │ schemas      │  │
│   └──────────────┘     └──────────────┘       └──────────────┘  │
│          │                    │                      │           │
│          └────────────────────┼──────────────────────┘           │
│                               │                                  │
│                               ▼                                  │
│                    ┌──────────────────────┐                     │
│                    │ lispsyntax-acset (0) │                     │
│                    │ All configs → sexp   │                     │
│                    └──────────────────────┘                     │
│                                                                  │
│   Σ(trits) = +1 + 0 + (-1) = 0 ✓  GF(3) CONSERVED              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Related Skills

| Skill | Trit | Relationship |
|-------|------|--------------|
| cue-lang | +1 | Schema source |
| nickel | 0 | Alternative config |
| gay-mcp | +1 | Colors generated code |
| codex-self-rewriting | 0 | Self-modifying patterns |


---

## Autopoietic Marginalia

> **The interaction IS the skill improving itself.**

Every use of this skill is an opportunity for worlding:
- **MEMORY** (-1): Record what was learned
- **REMEMBERING** (0): Connect patterns to other skills  
- **WORLDING** (+1): Evolve the skill based on use



*Add Interaction Exemplars here as the skill is used.*

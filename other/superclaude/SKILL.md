---
name: superclaude
description: Configure and operate the Claude Code harness for large codebases. Builds CLAUDE.md hierarchies, scoped test/lint commands, file exclusions, codebase maps, hooks, skills, subagent strategies, and LSP/MCP wiring. Use when setting up Claude Code for a new repo, auditing an existing configuration, onboarding a team, or scaling from single-developer to org-wide deployment. Triggers on "set up Claude Code for this repo", "optimize my Claude Code config", "audit my CLAUDE.md", "make this codebase navigable", "configure hooks/skills/plugins".
---

# Superclaude

Configure the Claude Code harness so it works as well as the model. The harness — CLAUDE.md files, hooks, skills, plugins, LSP, MCP servers, subagents — determines whether Claude Code is productive or fumbling. This skill builds and tunes that harness for large codebases.

## When to Load

- Setting up Claude Code for a new repo or monorepo
- Auditing an existing Claude Code configuration
- Onboarding a team or org onto Claude Code
- Codebase navigation is slow or inaccurate
- Claude keeps opening wrong files, running wrong tests, or missing context
- Scaling from one developer to many

## The Harness

Seven components, loaded in priority order. Each has a specific job. Misplacing work between them is the most common configuration mistake.

| # | Component | Loads | Best For | Common Mistake |
|---|-----------|-------|----------|----------------|
| 1 | CLAUDE.md | Every session | Project conventions, codebase layout, critical gotchas | Stuffing reusable expertise that belongs in a skill |
| 2 | Hooks | On events | Deterministic automation, capturing learnings, enforcing rules | Using prompts for things that should run automatically |
| 3 | Skills | On demand | Reusable expertise, specialized workflows | Loading everything into CLAUDE.md instead |
| 4 | Plugins | Always, once configured | Distributing org-wide setups to all developers | Letting good setups stay tribal knowledge |
| 5 | LSP | Always, once configured | Symbol-level navigation, typed languages | Assuming it works automatically without setup |
| 6 | MCP servers | Always, once configured | Internal tools, data sources, APIs | Building MCP connections before basics work |
| 7 | Subagents | When invoked | Parallel exploration, splitting read from write | Running exploration and editing in the same session |

**The rule:** Start from the top. Get CLAUDE.md right before touching hooks. Get hooks right before building skills. Don't wire up MCP servers when your CLAUDE.md still says `run npm test` for a monorepo with 40 services.

---

## 1. CLAUDE.md — The Foundation

CLAUDE.md is loaded every session. It is the most impactful configuration surface. It is also the easiest to get wrong.

### What Goes In

- Pointers and critical gotchas only
- Codebase structure overview (what lives where)
- Build/test/lint commands scoped to directories
- Conventions that differ from language defaults
- Hard constraints (never modify X, always use Y for Z)

### What Stays Out

- Reusable expertise (belongs in a skill)
- Long tutorials or documentation dumps
- Things the model already knows (standard language idioms, common framework patterns)
- Anything that hasn't changed in months and isn't surprising

### Hierarchical Strategy

CLAUDE.md files are additive. Claude walks up the directory tree and loads every CLAUDE.md it finds. Use this.

```
repo/
  CLAUDE.md                  # Repo-wide: architecture, top-level pointers, critical rules
  services/
    CLAUDE.md                # Services area: shared patterns, common dependencies
    payments/
      CLAUDE.md              # Payments service: specific test commands, API conventions
    auth/
      CLAUDE.md              # Auth service: security constraints, token handling rules
  frontend/
    CLAUDE.md                # Frontend: build tool, component patterns, styling approach
```

**Root-level CLAUDE.md** gets the big picture: directory structure overview, overarching conventions, cross-cutting gotchas. Keep it under 100 lines. Everything else loads on demand.

**Subdirectory CLAUDE.md** gets local specifics: test commands, lint commands, local conventions, dependencies, gotchas for that area. A developer working in `services/payments/` gets the root context automatically plus the payments-specific context.

### Scoped Test and Lint Commands

Running the full test suite when Claude changed one file in one service causes timeouts and wastes context. Scope commands per directory.

**Root CLAUDE.md:**
```markdown
# Testing
Do not run the full test suite. Each service has its own test command in its CLAUDE.md.
```

**services/payments/CLAUDE.md:**
```markdown
# Testing
Run: `cd services/payments && npm test`
Single file: `cd services/payments && npm test -- --testPathPattern=<file>`
Lint: `cd services/payments && npm run lint`
```

For compiled-language monorepos with cross-directory dependencies, document the build graph in the root CLAUDE.md so Claude knows which targets to rebuild.

### Codebase Maps

When the repo has dozens or hundreds of top-level directories, add a map. Not a novel — a table of contents.

**Root CLAUDE.md:**
```markdown
# Directory Structure
- `services/` — Backend microservices (payments, auth, notifications, inventory)
- `frontend/` — React SPA, shared component library
- `infra/` — Terraform modules, CI/CD pipelines
- `libs/` — Shared libraries (logging, metrics, auth-client)
- `scripts/` — Build and deploy tooling
- `proto/` — Protobuf definitions, generated code
```

For massive repos, use layered maps: root describes the top level, each area's CLAUDE.md describes its subdirectories. Claude loads the next level of detail only when it enters that directory.

### Writing the Root CLAUDE.md

When setting up a new repo, follow this template:

```markdown
# <Project Name>

## Architecture
<2-3 sentence description of what this project is and how it's structured>

## Directory Structure
<map of top-level directories with one-line descriptions>

## Development
- Language: <X>
- Package manager: <X>
- Build: <command>
- Test: <per-service, see subdirectory CLAUDE.md files>
- Lint: <command or per-service>

## Conventions
<only things that differ from language defaults or would surprise a new developer>

## Hard Rules
<things Claude must never do or must always do — keep this list short>
```

If it's longer than a screen, it's too long. Move details to subdirectory files.

---

## 2. File Exclusions — Noise Reduction

Generated code, build artifacts, and vendored dependencies waste Claude's search budget. Exclude them.

### .claude/settings.json

Commit deny rules so every developer gets the same noise reduction:

```json
{
  "permissions": {
    "deny": [
      "Read(generated/**)",
      "Read(vendor/**)",
      "Read(node_modules/**)",
      "Read(dist/**)",
      "Read(build/**)",
      "Read(**/*.generated.*)",
      "Read(**/*.pb.go)"
    ]
  }
}
```

### .claude/ignore

Works like .gitignore. Claude won't search or read matched paths:

```
# Build artifacts
dist/
build/
out/
*.min.js
*.min.css

# Generated code
generated/
**/*.generated.*
**/*.pb.go
**/*_gen.go

# Vendored
vendor/
third_party/
node_modules/

# Large binary assets
*.wasm
*.so
*.dylib
assets/sprites/**
```

### Override Strategy

Developers who work on code generators or build tooling can override project-level exclusions in their local settings without affecting the team. Document this in the root CLAUDE.md:

```markdown
# File Exclusions
Generated and vendored code is excluded in .claude/settings.json.
If you work on the code generator, override locally in ~/.claude/settings.json.
```

---

## 3. Hooks — Deterministic Automation

Hooks fire on events. Use them for things that must happen consistently, not things that require judgment.

### When to Use Hooks vs. CLAUDE.md Instructions

| Requirement | Use |
|-------------|-----|
| "Always run the linter after editing .ts files" | Hook |
| "Prefer functional components over class components" | CLAUDE.md |
| "Format code before committing" | Hook |
| "Use snake_case for database columns" | CLAUDE.md |
| "Log what was done at the end of each session" | Hook (stop hook) |
| "Think about performance when touching hot paths" | CLAUDE.md |

**The distinction:** If a human would run it mechanically every time, it's a hook. If a human would think about it and make a judgment call, it's a CLAUDE.md instruction.

### Stop Hooks — Session Learning

Stop hooks fire when a session ends. Use them to capture learnings while context is fresh:

- Propose CLAUDE.md updates based on what Claude learned during the session
- Log what was accomplished for the project's changelog
- Run a final lint/format pass

### Start Hooks — Dynamic Context

Start hooks fire when a session begins. Use them to load context that changes:

- Pull the current developer's team assignment and load team-specific conventions
- Check which services have been recently modified and preload their CLAUDE.md files
- Load environment-specific configuration (staging vs. production conventions)

### Enforcement Hooks

For rules that must never be violated, hooks beat instructions:

- Prevent commits to protected branches
- Ensure test files exist for new source files
- Block secrets from being committed
- Enforce naming conventions on new files

---

## 4. Skills — Packaged Expertise

Skills load on demand. They carry specialized workflows that would bloat CLAUDE.md if loaded every session.

### When to Extract a Skill

- The workflow is reusable across sessions and projects
- It needs more than 10 lines of guidance to do well
- It competes with other context for space in CLAUDE.md
- It applies to specific scenarios, not every session

### Scoping Skills to Paths

Bind skills to directories so they activate only where relevant:

- Security review skill loads when working in `services/auth/`
- Deployment skill loads when working in `infra/`
- Component library skill loads when working in `frontend/components/`

This prevents context pollution. A developer fixing a backend bug doesn't need the frontend component library patterns in context.

### Organizational Skill Libraries

When multiple developers need the same expertise:

1. Build the skill once
2. Test it on real workflows
3. Distribute it via a plugin or a shared skill repository
4. Update centrally, everyone gets the update

---

## 5. LSP — Symbol-Level Navigation

Text-based grep returns noise. LSP returns precision.

### Why It Matters

Grepping for a common function name in a large codebase returns thousands of matches. Claude burns context opening files to figure out which one matters. LSP returns only references that point to the same symbol. The filtering happens before Claude reads anything.

### What LSP Enables

- **Go to definition** — jump to the actual source, not a string match
- **Find all references** — every caller of a function, not every file containing its name
- **Symbol search** — find a class/function by name across the entire project

### Setup

Two pieces:
1. Language-specific code intelligence plugin for Claude Code
2. The corresponding language server binary installed and available on PATH

### When LSP Matters Most

- Multi-language codebases where text matching is ambiguous
- Typed languages (TypeScript, Go, Rust, C/C++, Java) where symbol resolution is complex
- Large codebases where grep returns hundreds of matches for common names
- Refactoring workflows where finding all callers is critical

Deploy LSP org-wide before rolling out Claude Code to developers working in typed languages at scale.

---

## 6. MCP Servers — Internal Tool Access

MCP connects Claude to systems it can't reach through the filesystem: ticketing systems, documentation platforms, analytics, internal APIs.

### When to Build

Only after the basics work. The priority order is firm:

1. CLAUDE.md is lean and accurate
2. File exclusions are in place
3. Test/lint commands are scoped
4. LSP is working for your languages

Then wire up MCP for:
- Internal documentation search
- Ticketing system access (read context, update status)
- Analytics platforms (query metrics, check dashboards)
- Internal APIs that Claude needs for context

### Structured Search as a Tool

Advanced teams expose their internal code search as an MCP tool. Claude calls it directly instead of grepping the filesystem. This is particularly valuable when the codebase spans multiple repositories or when the internal search has ranking that grep lacks.

---

## 7. Subagents — Parallel and Isolated Work

Subagents are separate Claude instances. They have their own context window. Use them to protect the main session from noise and to parallelize independent work.

### The Core Pattern: Split Exploration from Editing

**Wrong:** One session that searches the codebase, reads 30 files, forms a plan, and then edits.

**Right:**
1. Dispatch a read-only subagent to map the relevant subsystem
2. The subagent writes findings to a file (what depends on what, which files matter, what patterns exist)
3. The main agent reads the findings file
4. The main agent edits with full understanding and clean context

The exploration phase burns context on dead ends, wrong files, and backtracking. Isolating it in a subagent keeps the main session's context clean for the actual work.

### When to Use Subagents

- Exploring an unfamiliar part of the codebase before making changes
- Running independent tasks in parallel (test this while I refactor that)
- Investigating a bug across multiple subsystems
- Any task where the search/read phase will consume significant context

### Subagent Discipline

- Give subagents full context: what you're trying to accomplish, what constraints apply, what the output should look like
- Have them write findings to a file, don't paste findings into the main session
- Verify subagent claims independently (see the discipline skill)

---

## The Audit Workflow

When auditing an existing Claude Code configuration, check these in order:

### 1. CLAUDE.md Health

```
[ ] Root CLAUDE.md exists and is under 100 lines
[ ] Root file has architecture overview and directory map
[ ] Subdirectory CLAUDE.md files exist for major areas
[ ] Test/lint commands are scoped per service or module
[ ] No stale instructions referencing deleted code or old conventions
[ ] No reusable expertise that should be a skill
[ ] No documentation dumps or tutorials
```

### 2. Noise Reduction

```
[ ] .claude/ignore or .claude/settings.json excludes generated code
[ ] Build artifacts are excluded
[ ] Vendored/third-party code is excluded
[ ] Large binary assets are excluded
[ ] Exclusions are committed to version control
```

### 3. Automation

```
[ ] Hooks exist for mechanical tasks (formatting, linting)
[ ] Stop hooks capture session learnings
[ ] Enforcement hooks prevent common mistakes
[ ] No hooks doing work that requires judgment (that belongs in CLAUDE.md)
```

### 4. Navigation

```
[ ] LSP is configured for the primary languages
[ ] Language server binaries are installed and on PATH
[ ] For monorepos: codebase map exists at root level
[ ] For deep nesting: layered maps in subdirectories
```

### 5. Freshness

```
[ ] Configuration reviewed within the last 3-6 months
[ ] No instructions compensating for limitations of older models
[ ] No hooks or skills built around bugs that have been fixed
[ ] Conventions match current codebase state
```

---

## Maintenance Cadence

### Every 3-6 Months (or After Major Model Releases)

1. **Reread the root CLAUDE.md.** Does every line still apply? Remove what's stale.
2. **Check for constraint instructions.** Rules like "break refactors into single-file changes" may have helped earlier models but now prevent coordinated cross-file edits. Remove constraints that newer models no longer need.
3. **Audit hooks and skills.** If a hook compensates for a specific model limitation, check whether that limitation still exists. If a skill works around a bug that's been fixed, retire it.
4. **Review file exclusions.** New generated code directories may have appeared. Old ones may have been removed.
5. **Check subdirectory CLAUDE.md files.** Services get added, renamed, and deleted. The local CLAUDE.md files should track reality.

### After Major Codebase Changes

- New service or module added: create its CLAUDE.md with test/lint commands
- Service deleted: remove its CLAUDE.md
- Build system changed: update all affected test/lint commands
- Directory restructured: update root codebase map and affected subdirectory files

---

## Org-Wide Deployment

### Before Broad Rollout

A small team (even one person) should wire up the harness before developers get access. The goal: a developer's first session should be productive, not spent configuring.

**Minimum viable setup:**
1. Root CLAUDE.md with architecture and directory map
2. Subdirectory CLAUDE.md files with scoped test/lint commands
3. File exclusions for generated code and build artifacts
4. LSP configured for primary languages

**Better setup adds:**
5. Hooks for formatting, linting, and session learning
6. Skills for common workflows (deployment, security review, onboarding)
7. Plugins bundling the above for one-command installation
8. MCP connections to internal tools

### Ownership

Someone must own the configuration. Without ownership, it drifts, fragments, and rots.

**Options:**
- **Dedicated team** under developer experience / developer productivity. They own the CLAUDE.md conventions, approved skills, plugin marketplace, and permissions policy.
- **Single DRI** with authority over Claude Code configuration. One person who keeps things current and makes decisions.
- **Cross-functional working group** (especially in regulated industries). Engineering, security, and governance define requirements together.

### Preventing Fragmentation

Bottom-up adoption generates enthusiasm but fragments without centralization. The owner must:

- Assemble and evangelize standard conventions (CLAUDE.md hierarchy, curated skills, approved plugins)
- Prevent duplicate effort (thousands of developers rebuilding the same skill)
- Ensure AI-generated code goes through the same review process as human code
- Control available skills and plugins through a governance framework

### Governance for Regulated Industries

Start with:
- A defined set of approved skills
- Required code review processes for AI-generated changes
- Limited initial access

Expand capabilities as confidence builds. Answer these questions early:
- Who controls available skills and plugins?
- How do you prevent duplicate development?
- How do you ensure consistent review standards?

---

## Quick Reference

| Task | Where to Configure |
|------|--------------------|
| "Always run X after editing Y files" | Hook |
| "Prefer pattern X over pattern Y" | CLAUDE.md |
| "Here's how to deploy service Z" | Skill |
| "Everyone needs access to internal docs" | MCP server |
| "New devs should get our full setup" | Plugin |
| "Find the real definition, not string matches" | LSP |
| "Explore this subsystem before editing" | Subagent |
| "Don't search generated code" | .claude/ignore |
| "Scope tests to the changed service" | Subdirectory CLAUDE.md |
| "Review config every quarter" | Maintenance cadence |

## Scope and Limitations

This skill targets conventional software engineering environments: Git repos, standard directory structures, engineers as primary contributors. Environments that require additional work:

- Game engines with large binary assets
- Non-Git version control systems
- Non-engineer contributors to the codebase
- Extremely unusual directory structures

For these, the principles still apply — hierarchical context, scoped commands, noise reduction — but the specific implementation differs.

---
name: c-sharp-architect
description: "Design the architecture of a Unity C# system: assembly/namespace layout, class and interface contracts, dependency-injection strategy, and pattern selection. Produces an architecture sketch (and optionally an ADR) before implementation begins."
argument-hint: "[system-name or path-to-design-doc]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Task, AskUserQuestion
model: sonnet
agent: c-sharp-architect
---

## Phase 1: Load Context

Read, in order:
- The design doc / story / GDD named in the argument (if any).
- `CLAUDE.md` and `.claude/docs/coding-standards.md` for project standards.
- `.claude/docs/technical-preferences.md` → `## Engine Specialists` (note the engine; skip Unity-specific advice if `[TO BE CONFIGURED]`).
- Existing C# layout: `Glob` for `**/*.asmdef`, `**/*.csproj`, `**/*.sln` to understand current assembly boundaries.

State what is specified vs. ambiguous.

---

## Phase 2: Clarify Architecture Questions

Use `AskUserQuestion` for the decisions that shape structure:
- New assembly vs. extend existing? Editor-only code involved?
- Data representation: `ScriptableObject` / plain config class / serialized asset?
- MonoBehaviour vs. plain C# vs. DOTS for the runtime surface?
- Required test seams (what must be injectable/mockable)?

Do not guess on decisions that are expensive to reverse.

---

## Phase 3: Propose Architecture

Produce a sketch covering:
- **Assemblies & namespaces**: which `.asmdef`(s), references, `internal`/`public` surface.
- **Types & contracts**: classes, interfaces, and the public API signatures (with XML-doc intent).
- **Dependency flow**: a diagram/text showing direction (core ← gameplay ← UI), confirming no cycles.
- **Patterns**: which patterns are used where, and *why* (composition, SO-driven data, DI/installer, events).
- **Trade-offs**: simpler-but-rigid vs. flexible-but-complex, named explicitly.

Validate against standards: no static singletons for mutable state, data-driven tunables, nullable contracts, `Task`-based async.

---

## Phase 4: Consult Specialists (as needed)

If the design leans on a Unity subsystem, spawn the relevant specialist via Task
for a focused opinion (do not block on it unless it gates the structure):
- DOTS/ECS scale question → `unity-dots-specialist`
- Asset loading/memory → `unity-addressables-specialist`
- UI structure → `unity-ui-specialist`
- Broad Unity implications → `unity-specialist`

---

## Phase 5: Output & Decision

Present the architecture sketch. Then use `AskUserQuestion`:
- `[A] Record this as an ADR` → run `/architecture-decision`
- `[B] Hand the contract to c-sharp-engineer` → `/c-sharp-engineer`
- `[C] Write the skeleton (interfaces + asmdefs) now` → ask "May I write to [paths]?" before any Write
- `[D] Revise the architecture`

This skill is design-first: write code/skeleton files only after explicit approval of specific paths.

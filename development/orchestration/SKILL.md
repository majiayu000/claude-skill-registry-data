---
name: orchestration
description: Tool-portable orchestration protocol shared by GitHub Copilot and Claude Code — task classification, pipeline per class, quality gates, pointer-style delegation, file-based state, handoff and resume between tools, sequential fallback. Load before coordinating any multi-step change, when resuming work, or when switching between Copilot and Claude Code.
user-invocable: false
---
# Orchestration protocol

Role names are logical: Copilot agent `X` = Claude Code subagent `claude-X`.

## 1. Classify (write into state, not chat)
Start: `pwsh scripts/Set-AiState.ps1 -Init -Task "<one sentence>" -Tool <copilot|claude-code>`, then set `class=` and `modules=`.
- type: feature | bugfix | refactor | schema | new-module | architecture | migration | performance
- size: **S** one slice/file area, no schema/contract · **M** one module, several slices or schema · **L** cross-module, new contract/event/aggregate · **XL** new module, recipe/topology change, style migration
- impact: none | local | structural
- modules: `Name: recipe`

## 2. Pipeline
| Class | Phases |
|---|---|
| S | implementer → reviewer (Copilot orchestrator never edits; Claude Code main session may do S directly) |
| M | researcher → planner → **G1** → (db-engineer) → implementer → test-engineer → reviewer |
| L | researcher → architect → planner → **G1** → (db-engineer) → implementer → test-engineer → reviewer |
| XL / structural | researcher → architect → **G0** → planner → **G1** → … → reviewer |
| bugfix | researcher → test-engineer (failing test) → implementer → reviewer |
| performance | researcher → db-engineer → planner → **G1** → implementer → reviewer |
Independent modules → parallel researcher calls.

## 3. Gates
- **G0** (user): ADR `proposed`, profile diff, ≥ 2 options, enforcement listed.
- **G1** (user, unless request says `autopilot`): plan exists, every file row has a placement rule id, tests named, rollback for schema, no open questions.
- **G2** (auto, per step): build + tests green, checkbox ticked. 2 consecutive reds → stop.
- **G3** (auto): reviewer `APPROVE` → done · `CHANGES_REQUIRED` → implementer, max 2 cycles, then stop · `BLOCKED` → stop.
At a user gate: write state, then output only `GATE G1: <plan path> — approve?`.

## 4. Delegation (pointer prompts, ≤ 3 lines)
```
<role>: read .ai/state/current.md; do <phase or "plan step 3">; return your OUT format.
[constraint: <only if not already in state/plan>]
```
Never paste plan/research content into prompts; persist it to files and point to them.
Research output that later phases need → orchestrator appends a ≤ 10-line digest to state `notes`.

## 5. State file `.ai/state/current.md`
Written only through `scripts/Set-AiState.ps1` (one short command, no file editing):
```
pwsh scripts/Set-AiState.ps1 phase=plan "gate=G1 waiting" "next=planner: write plan"
pwsh scripts/Set-AiState.ps1 -Decision "<chat-only agreement>" -Note "<research digest line>" -Log "<phase result>"
pwsh scripts/Set-AiState.ps1 -Show
```
Fields: task class modules plan adrs base sha tool phase gate steps review_cycles next.
`decisions` holds every chat-only agreement (one line each). This is what makes switching tools lossless.
`-Init` archives the previous state to `.ai/state/archive/`.

## 6. Handoff (before switching tool or ending a session)
1. If the current step is green and there are uncommitted changes: `git add -A && git commit -m "wip(ai): <task> S<n>"` (Copilot orchestrator: delegate the commit to implementer). Never push. If red: do not commit; set `"steps=… | status red"` and describe the failure in `next`.
2. `pwsh scripts/Set-AiState.ps1 -Handoff -Tool <copilot|claude-code> "next=<imperative, executable without chat history>"` (records sha); add `-Decision` for each chat-only agreement.
3. Output only: `HANDOFF <sha> → next: <next>`.

## 7. Resume
1. Read state → plan (current step only) → ADRs listed in state.
2. `git log --oneline <sha>..HEAD` and `git status --short` — detect work done outside the recorded state.
3. If state says red or git shows unexpected changes: run build + tests before continuing.
4. `pwsh scripts/Set-AiState.ps1 -Tool <copilot|claude-code> -Log resumed`, continue with `next`.
5. Output only: `RESUME <task> | phase <p> | S<n>/<total> | <next>`.

## 8. Sequential mode (no subagent tool, e.g. Visual Studio)
Run the same pipeline yourself. For each phase read the role definition (`.github/agents/<role>.agent.md`
or `.claude/agents/claude-<role>.md`) and obey its restrictions and OUT format for that phase only.

## 9. Final report
```
RESULT: done | stopped@G<n> | blocked
CHANGES: <module/slice → n files> (details: git diff <base>..HEAD)
TESTS: added <n>, all green | <failing>
ARCH: ADRs <ids> | exceptions <ids> | none
FOLLOW-UP: [sev] …
```

---
name: delegate
description: >
  Delegate work between LibrAgent AI agent sessions using sub-agent sessions.
  Use when an agent needs to spawn, brief, monitor, or troubleshoot a child
  session with `agent__spawnSession`, `agent__checkSession`, or
  `agent__messageToSession`, especially when deciding whether the child really
  needs parent workspace state, workspace instructions, or workspace-scoped
  skills. For generator-evaluator / strict acceptance criteria / proof before
  done, load `delegation-eval-loop` after this skill's spawn mechanics.
---

# Delegate

## Runtime Tool Names

LibrAgent exposes builtin tools as `server__tool` (for example `agent__spawnSession`). Use the exact names from the current session tool list when calling tools. Bare shorthand like `spawnSession` will fail at runtime.

Treat sub-agent delegation as session orchestration, not magic inheritance.

A child session keeps lineage to its parent, but it does **not** automatically inherit the parent's workspace, workspace instruction files, or workspace-local skills. If the task depends on those, either restate them in the handoff, choose a different assistant, or avoid delegation.

Read `references/delegation-patterns.md` when you need concrete handoff templates, troubleshooting patterns, or a quick matrix for what the child session can actually see.

## Skill Routing

| Need | Skill |
| --- | --- |
| Spawn, isolation, workspace/handoff mechanics | **this skill** (`delegate`) |
| Strict acceptance criteria, proof-before-done, reject/re-steer loop | **`delegation-eval-loop`** (parent = evaluator, child = generator) |
| Parallel independent pieces | `divide-conquer` |
| Multi-perspective review of one question | `consensus-delegation` |

Do **not** paste the full eval protocol into every delegation. Use light checks in §5 for casual handoffs; load `delegation-eval-loop` when the user or task requires verifiable completion.

## Delegation Workflow

1. Decide whether delegation is appropriate.
2. Inspect existing child sessions and reuse a suitable idle session with the same assistant configuration when possible.
3. Choose the child's effective context.
4. Prepare a handoff that includes everything the child actually needs.
5. Start a new child only when no suitable session exists or separate role, parallel, or workspace isolation is needed.
6. Monitor or steer it with follow-up messages.
7. Merge the result back into the parent flow.

## 1. Decide Whether to Delegate

Delegate when the work is bounded, parallelizable, or benefits from a specialized assistant.

Good delegation targets:

- focused research or code reading
- isolated implementation tasks with clear deliverables
- long-running analysis where the parent can keep working
- specialized assistants that have assistant-scoped skills the parent lacks

Avoid delegation when the child must rely on live parent-only state, such as:

- the parent's temporary workspace files
- the parent's workspace `agents.md` / `CLAUDE.md` instructions
- workspace-local `skills/` content from the parent's workspace
- the parent's scratchpad notes (`scratchpad__*` is session-isolated; children cannot read them)
- any behavior that assumes random parent context is implicitly copied into the child

If the work depends on any of those, delegation is usually the wrong move unless you can explicitly recreate that context for the child.

When the child finishes, require deliverables in its **final text response**. Parent recovery uses that text (`agent__checkSession` / `waitForResult`), not scratchpad IDs — child scratchpad notes are invisible to the parent.

After `agent__checkSession`, read the Metadata `workspace:` line: `SHARED with caller` means relative paths in the parent root are safe; `ISOLATED` means the parent cannot `workspace__readFile` that path — rely on Result text or `agent__messageToSession`, and do not assume sibling sessions share a workspace.

## 2. Choose the Child's Effective Context

Assume these rules:

- `agent__spawnSession` creates a new child session with lineage metadata, not a cloned runtime context.
- The child gets its own session workspace by default.
- Workspace instructions are loaded from the **child** workspace, not the parent workspace.
- Workspace-scoped skills are resolved from the **child** workspace, not the parent workspace.
- Assistant-scoped skills come from the assistant you choose for `configId`.
- Global skills remain available to both parent and child.

If the parent is running inside a task-force workspace, check `.libragent/teamwork.json` before delegating:

- If `executionSubstrate.mode` is `"org"`, reuse an existing Idle org child with the matching assistant ID and compatible workspace via `agent__messageToSession` when possible; otherwise prefer `agent__spawnSession(...)` so the new child joins the org and inherits the parent effective workspace by default. Switch to `org` for org-specific operating rules.
- If `executionSubstrate.mode` is `"scheduled"`, the wake-up is likely a global scheduled task. Follow `schedule` for scheduled-task operating rules instead of ad-hoc delegation.
- If the user wants a future clock reminder inside the current session, use `loop` instead of delegation.
- If the user wants to resume when a process, ticket, or webhook completes, use `call-me-back` instead of delegation.
- Treat the app-local teamwork artifact directory as the orchestration/constitution storage. If the child also needs to edit code in a repo, keep the session workspace semantics separate from the teamwork artifact path.

Important limitations:

- Do **not** assume `agent.md` exists. Workspace behavior instructions are loaded from the first non-empty file among `agents.md`, `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
- Persona / tone instructions are loaded separately from the first non-empty file among `.github/SOUL.md`, `SOUL.md`, `.github/soul.md`, and `soul.md`.
- Both persona and workspace instruction content are cached for the session lifetime until the stable prompt cache is invalidated.
- `agent__spawnSession` can override the child workspace with `workspaceOverride`; files and prompt state still follow the child session.
- Default to each session's own workspace. Use `workspaceOverride` only when the child should work in the same effective workspace as the parent or another already-existing workspace.

## 3. Prepare the Handoff

Make the task self-contained. The child should not need to guess what the parent meant.

Always include:

- exact objective
- hard scope boundaries
- expected output format
- critical paths, identifiers, or commands
- any rules from the parent workspace instructions that the child must obey
- any skill-specific procedure that may not exist in the child workspace

If the child needs a specific skill workflow, prefer one of these approaches:

- choose an assistant whose assistant-scoped skills already contain that workflow
- rely on a global skill that both sessions can access
- copy the critical procedure into the task text if the workflow is short

Say "use the same workspace as this session" only when you intentionally started the child in that shared workspace.

## 4. Start and Manage the Child Session

Use the builtin agent tools deliberately:

- `agent__listAgents(type="configs")` to find the right assistant and prefer its returned template ID
- `agent__listAgents(type="sessions")` or the live sub-agent inventory to find an existing child with a matching assistant ID
- `agent__messageToSession(sessionId="...", message="...")` to continue work or assign new work to a suitable idle matching-role child
- Set `reset=true` only when the previous conversation and runtime state should be discarded. This resets messages, planning/compaction state, and pending messages but does not clean workspace files.
- `agent__spawnSession(configId="...", task="...", waitForResult=false)` to spawn a new child session using the configuration template ID. Do not pass a `sessionId` here; for existing sessions use `agent__messageToSession`.
- `agent__spawnSession(configId="...", task="...", workspaceOverride="/absolute/path")` when the child must run in a shared existing workspace
- `agent__checkSession(sessionId)` to poll
- `agent__checkSession(sessionId, wait=true)` when you want to block until a terminal result
Default to `waitForResult=false` unless the parent truly has nothing useful to do while waiting.

## 5. Review the Result (Parent Owns Acceptance)

Do not blindly trust the child. The child **generates**; the parent **accepts**. A child's "done" / "tests pass" claim is a hypothesis until the parent has evidence.

**Casual handoff (this skill only)** — after `agent__checkSession` returns idle:

- Confirm scope: correct workspace (`SHARED` vs `ISOLATED` in Metadata) and authorized paths
- Spot-check deliverables in the child's **final text** (not scratchpad IDs)
- If claims cite commands/files, inspect or re-run the critical check yourself before presenting as final
- Re-steer with `agent__messageToSession` if the child stopped short or missed the objective

**Strict / high-stakes handoff** — stop here and follow **`delegation-eval-loop`**:

- Brief with verifiable acceptance criteria (sprint contract) before spawn
- Layered eval: Deterministic → Invariant → Trajectory/reliability → Semantic
- Reject with exact failure output; bound the retry loop; never accept self-graded success

Incomplete, cancelled, circuit-broken, or evidence-free runs are **not** successes even if the prose sounds finished.

## 6. Troubleshooting Heuristics

If the child cannot find a file, a local skill, or a workspace rule, assume isolation first.

Common causes:

- the child is in a different workspace
- the child used a different assistant than intended
- the needed procedure lived only in the parent's workspace `skills/` directory
- the parent assumed files or rules would be copied without using `workspaceOverride` or explicit task text
- the parent changed `agents.md` mid-session and expected the existing session prompt cache to refresh automatically

When in doubt, restate the missing context explicitly or stop delegating that particular subtask.

---
name: org
description: Run explicit org-based teamwork in LibrAgent. Use when collaboration needs durable org identity, org-visible child sessions, org-root resume behavior, or clear parent/sibling org context while preserving normal parent workspace inheritance.
---

# Org

Org is explicit lineage teamwork. It is not generic delegation and it is not scheduled automation.

Use `teamwork` first when the workspace constitution is not ready.
Use `org-restructure` when the org already exists and roles or constitution files need to change (add, layoff, merge, agents.md updates).
Use `postmortem-improve` after missions or repeated failures to capture lessons and route durable org improvements.

## Workflow

1. Confirm org is the right substrate.
   - Use org when the user wants org visibility, durable org identity, coordinator/specialist lineage, or root-session resume behavior.
   - If the real need is app-wide recurring or cron-like automation, stop and use `schedule`.
   - If the user only wants a clock delay or reminder inside the current conversation, stop and use `loop`.
   - If they want to resume when a process or ticket completes, stop and use `call-me-back`.
   - If the governing root session has not prepared the teamwork artifact directory yet, stop and use `teamwork` to call `agent__prepareTeamworkWorkspace()` first.
2. Read `.libragent/teamwork.json` before acting.
   - Confirm `executionSubstrate.mode` is `"org"` and `orgLineage.intended` is `true`.
   - If the manifest says a different substrate, reconcile before proceeding.
3. Keep one shared workspace.
   - Treat the app-local teamwork artifact directory as the SSOT for orchestration files.
   - The governing root session and org-visible children should keep the normal parent/override workspace inheritance model.
4. Create the org once from the root session.
   - Use `agent__createOrg(name="...")` from the governing root session.
   - Record the returned `orgId` and `orgName` in `coordination/DECISIONS.md` (the backend automatically updates `.libragent/teamwork.json` with these details).
   - The session that calls `agent__createOrg` becomes the org root. Do not call `agent__createOrg` again.
5. Spawn org-visible members explicitly.
   - Before creating a member for new work, inspect `agent__listAgents(type="sessions")` for an Idle org child with the same assistant ID and compatible workspace, then use `agent__messageToSession` (with `reset=true` for a fresh assignment) when reuse is safe.
   - Use `agent__spawnSession(configId, task)` for org-visible children only when no suitable member exists, a different role/workspace is needed, or additional parallel capacity is required. If the current session already belongs to the org, inheritance is automatic.
   - To keep a child out of Org view, spawn it from a session that is not part of an explicit org.
6. Resume through the org root.
   - The org root session is the canonical entry point. Org view should resume the root, not whichever child was last active.
   - If you need to identify the root, read `orgLineage.rootSessionId` from `.libragent/teamwork.json`.
7. Keep work anchored in the workspace constitution.
   - Read `agents.md`, `MISSION.md`, `ROLES.md`, and the coordination files before directing members.
   - Org context refines execution; it does not replace the shared workspace contract.

## Guardrails

- Do not invent a separate org-only workspace. Org members should inherit the parent effective workspace unless a task explicitly needs a different `workspaceOverride`.
- Do not use org identity for scheduled task groups or recurring automation.
- Do not treat arbitrary child-session resume as org resume. The org root is the entry point.
- Do not infer org membership from parent/child lineage alone — membership requires explicit org inheritance at session creation. Under an explicit org root that inheritance is automatic.
- After `agent__createOrg`, verify `.libragent/teamwork.json` contains the updated `orgId` and `rootSessionId` (written automatically by the backend).

## References

- [Org patterns and tool call examples](references/org-patterns.md)
- Living org changes (roles, constitution): use bundled skill `org-restructure`
- After-action learning / continuous improvement: use bundled skill `postmortem-improve`

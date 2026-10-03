---
name: workflow
description: Choose light, medium, or heavy execution for engineering work. Use for `$workflow`, explicit effort selection, or bounded parallel workers coordinated by the main agent.
---

# Workflow

Run without installing workflow files in the project. Respect existing `AGENTS.md`, nested instructions, Git policy, documentation, and user work.

## Select effort

Accept `$workflow light|medium|heavy|auto`, `effort=light|medium|heavy`, and equivalent natural language. An explicit level wins for the current task until the user changes it or the task ends. `auto` restores automatic selection.

When no level is explicit, choose the smallest sufficient level:

- **Light:** explanation, diagnosis, review, lookup, or small localized change with straightforward verification.
- **Medium:** cohesive multi-step or multi-file work that one agent can complete in an ordered stream with proportionate verification.
- **Heavy:** broad or cross-cutting work with at least two concrete, bounded, independent workstreams where parallelism or independent comparison materially improves speed or required coverage.

Prefer the lower level when borderline. Change level only when evidence materially changes scope; announce the change and reason. These are workflow levels, not model reasoning-effort settings.

## Common rules

1. Read applicable project instructions and only necessary context. Reuse
   already-read instructions within the task unless they change; recheck source
   evidence when its revision, configuration, or relevant files change.
2. Explicit user instructions override skill defaults within their scope.
   Preserve higher-priority instructions, evidence truth, runtime limits, and
   unmodified project constraints. For conflicts, overrides, or skill-induced
   stops, apply [authorization](references/authorization.md). If project
   instructions define route names or spawning limits, retain them unless
   explicitly changed.
3. State the selected level briefly.
4. Establish acceptance criteria before non-trivial edits.
5. Trace the real code path and preserve contracts and unrelated work.
6. Make the smallest coherent root-cause change.
7. Before any build or check, apply [verification reuse](references/verification.md):
   run only missing or invalidated evidence; never repeat valid checks.
   Report observed evidence.
8. Inspect final diff and repository status after edits when Git is present.

Do not create project workflow scaffolding or documentation unless requested or
already required by the repository. Light loads verification rules only when
building or checking; do not load
Medium, Heavy, or model-selection references for direct work.

## Compose with domain skills

When another skill names `$workflow` as its execution core:

- Workflow owns effort selection, the control plane, dispatch, repair routing,
  verification, and integration.
- The domain skill owns its modes, evidence gates, lane definitions, output
  contract, and mutation permissions.
- Domain restrictions apply after resolving explicit overrides. A workflow
  level alone never authorizes effects forbidden by the effective domain
  contract or project.
- In `auto`, treat domain `Focused`, `Standard`, and `Deep` classifications as
  inputs to light, medium, and heavy selection, not as a second control plane.
- In `auto`, run the required domain preflight directly at Light, then announce
  the selected level after classification. Do not report that normal selection
  as an escalation.

## Mutation boundary

After resolving authorization, intersect its scope with applicable project and
domain rules and runtime permissions. Classify before executing or delegating:

- **primary-tree read-only:** inspect and verify; never edit production files
  or assign an implementer to this surface.
- **disposable-worktree-only:** edits and builds stay inside a verified,
  domain-gated disposable worktree, never the primary tree.
- **authorized primary-tree mutation:** edit and check only the authorized
  surface; delegated writers own disjoint file sets.

Investigation and verification roles remain read-only. A role never widens
network, approval, or mutation permissions.

## Run the route

- **Light:** work directly; do not spawn agents.
- **Medium:** read [references/medium.md](references/medium.md), then work
  directly; do not spawn agents.
- **Heavy:** read [references/roles.md](references/roles.md), then
  [references/heavy.md](references/heavy.md). Keep the main thread as the controller;
  spawn only when the dispatch gate holds. These references alone own role/model
  selection, capsules, parallel ownership, repair, and upward reporting.

If subagents are unavailable, continue directly unless the user explicitly
required multi-agent execution; then report the exact limitation. Never claim
delegation or a model identity without runtime evidence.

---
name: cursor-setup-pstack
description: Use when setting up pstack native Codex model choices for the current task or an explicitly requested persistent policy, including /setup-pstack or pstack budget changes.
---

# Setup pstack for Codex

Use the standing `model-capability-router` as the sole authority for model, effort, delegation and total-cost decisions. This skill maps pstack roles onto native Codex capabilities when the operator asks for setup; it does not create a second routing policy, switch the active task model, write a Cursor rule, or start agents merely to configure them.

## Steps

### 1. Establish scope and capability

Identify whether the request is for this task, a particular project, or a persistent shared policy. Read the installed router and, for a persistent source change, the canonical `TheAngryPit/TheAngrySkills` source. Respect the operator's selected main model, effort, role bindings and workflow. Check the models, efforts and inheritance exposed by each exact channel that would execute a choice; current task, native subagent, user-owned task and Work cloud can differ. Do not present the router's recommended profiles as detected runtime configuration.

### 2. Choose execution before compute

Keep small or tightly coupled work with the agent that has context. Use bounded delegation or parallel workers only when authorized and useful after briefing, startup, integration and verification costs. Preserve a requested delegation workflow for suitable work. There is no required Astra → Sol → Luna ladder, coordinator stage, automatic planning or review delegate, failed-attempt escalation, fixed fan-out or model race. Create a separate user-owned task only under the router's explicit-request and task-boundary rules. A full-history subagent fork inherits the parent model; request a differently modelled native worker with bounded or fresh context only when that channel supports it.

### 3. Budget, map and review every pstack role

For a full pstack setup, load existing project/task choices first; on a re-run preserve changed model families, panel lists, role ownership, named specialists and `inherit-parent`/`auto` aliases. Show all upstream role labels, even when a workflow is not being invoked now: feature/refactoring, bug-fix, perf-issue, hillclimb, judgment/prose, hardest tasks, how explorer/explainer, why investigators/synthesizer, reflect tooling/judgment/divergent/synthesizer, arena runners/cross-judge pool, swarm workers, architect runners and interrogate reviewers. A scoped change to one role changes only that role and keeps the rest of the established mapping. Showing roles does not dispatch them.

Offer the upstream budget options with their exact labels and show the current selection when known: `unlimited — keep max`, `large — xhigh reasoning`, `medium — high reasoning`, `small — medium reasoning`. For a proposed mapping, `unlimited` retains current efforts; the other options propose `xhigh`, `high` or `medium` for every real role and panel entry. Choose a detected same-family variant at or below the proposed target only when it is actually available on that execution channel; otherwise mark the entry as needing a choice. Leave aliases untouched. This is a pstack configuration proposal, not a command to run every worker at the same effort. Review the proposal against the router's task-specific judgment, explicit bindings and proof needs before applying it. Do not invent Cursor slugs or silently substitute an unavailable native model.

Show the entire resulting table and let the operator adjust specific roles when an answer would change the setup. Preserve panel semantics: arena runners, architect runners and interrogate reviewers have one candidate worker per selected list entry when their own workflow calls for it; the `arena cross-judge pool` selects one eligible judge where possible; swarm workers is the default for that workflow unless a comparison explicitly assigns arms. The router still decides whether and when delegation is useful, with bounded ownership and verification. Sol medium, Astra low and Luna high/xhigh are recommendations, with task-specific Sol high, Luna max or exceptional Astra xhigh available; the operator's selections and fixed named-specialist bindings take precedence.

### 4. Validate and record

Validate each proposed real model and effort against its actual execution channel, including the parent selection needed by an inherited role. Mark unsupported roles or efforts precisely and leave the affected configuration unchanged; continue independent work with the current agent when it can meet the proof bar. Record requested selection separately from native acceptance and effective runtime readback. An accepted spawn or fixture does not by itself prove which model a running worker used. The coordinator owns integration and checks the deliverable against the requested result and evidence.

### 5. Persist only the requested scope

Keep task-local choices in this task's brief and handoffs; project-only choices in the project-approved configuration or checkpoint. For an explicitly authorized persistent shared-policy change, update the canonical router source and affected fixtures with a reviewed diff. Changing this setup skill itself belongs in its canonical TheAngrySkills mirror source. Do not write `~/.cursor/rules/pstack-models.mdc`, a competing preset, a CLI resolver or native defaults as a proxy for changing the active task. If source or write access is unavailable, report the exact remaining write without claiming persistence.

### 6. Verify the applied result

Run the focused source checks, review the diff and read back any installed copy after an authorized update. Check native config or runtime metadata only where exposed. Source edits, dry-run fixtures, installed files and future-session behavior are distinct proof levels. Report what was actually verified, unresolved channel limits and current owner. Do not infer lower Codex allowance use from API prices, cache assumptions or faster parallel work; compare complete outcomes when observed usage is available.

For implementation work, use the project's existing verification skill. If it lacks a way to drive the real app, propose `cursor-create-verification-skill` once and invoke it only when available and requested; do not call a fixture full runtime proof.

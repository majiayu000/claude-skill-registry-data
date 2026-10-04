---
name: rp-orchestrate
description: Coordinate independent work through RepoPrompt CE agent sessions and context tools. Use when the user requests orchestration or parallel workers in RepoPrompt, preserving personal model preferences.
---

# RepoPrompt Orchestrate

Call the Skill tool with `orchestrate`. If the tool cannot resolve it, read the [shared coordination policy](../orchestrate/SKILL.md). It owns role preferences, assignment ownership, and completion criteria; this adapter owns RepoPrompt execution.

Use RepoPrompt CE's tools for delegated work. Keep the coordinator where the user invoked the skill: an eligible top-level CE Agent Mode session, or an external harness connected through CE MCP/CLI. Do not switch to the host's native subagents or launch a different workflow merely to bypass a RepoPrompt dispatch restriction.

Before the first dispatch, read [RepoPrompt tool mechanics](references/repoprompt-tools.md). Bind the requested repository and verify its checkout. Inspect the live tool and model catalogs; resolve the shared role preferences to exact advertised model targets. Do not assume role aliases match those preferences or change global role settings.

Reuse supplied plans without reopening settled decisions. Establish missing context with RepoPrompt search, structure, and selection tools. If material behavior, module ownership, or cross-module design remains unresolved after focused inspection, call `context_builder` before the affected implementation. Scope planning to the gap rather than regenerating the plan; resolve shared gaps once at the coordinator and export the result for relevant workers. Bounded assignments with these decisions settled can proceed directly.

Pass focused briefs and any exported plan paths to children. Tell workers to return newly discovered material planning gaps to the coordinator before making affected edits. Start independent workers in new sessions without forwarding the coordinator's transcript. Reuse the same Astra advisor session for related questions and new evidence.

Keep all children as leaves. Route useful discoveries through the coordinator using the supported follow-up controls; child-to-child messaging and recursive spawning are not part of this adapter's contract.

Launch ready assignments with detached starts and retain every returned session ID. Treat a multi-session wait as the first result, not completion of the team. Resolve pending interactions with their current interaction IDs, and keep monitoring unaffected sessions while an approval awaits the user.

Before ending, verify all assigned outcomes or report their concrete blockers. CE does not permit leaving active children unattended: if a blocker requires ending the turn, cancel running or waiting children, confirm they stopped, and retain their session IDs and partial-work evidence for resumption. Completed advisor sessions can remain available without an active run. Preserve session history until all review and follow-up work is finished.

This skill does not impose Orchestrate (TDD), Build It, commits, or publishing. Preserve any workflow the user already chose; its additional requirements still apply.

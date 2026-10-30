---
name: using-axiom
description: Route startup, resume, compaction, requests and local web research. The startup Hook loads this gate; invoke it directly only on an explicit using-axiom request.
---

## Invocation Notes

Optional, per user verbosity and host behavior. When explaining, name bundled skills as `Axiom:<skill-name>` and others by their own name, in inline code, with a brief reason in the user's language; no fixed layout, repetition or notice for no-route or startup. When a bundled route hands off to, or yields to, another installed skill or MCP tool, name it the same way with a brief reason.

## Route Once

1. Honor higher-priority instructions.
2. Route only explicit Axiom invocations or clear bundled-description matches.
3. Load the smallest matching installed skill set and active-phase references without inspecting candidate bodies first.
4. Map unambiguous non-English to its canonical English route; clarify only material unresolved intent, never tentative wording alone.
5. No match: continue normally in the host. A no-match result is not a denial, does not create authorization, and does not manufacture a repository-state conflict.

Before web research from a local or uncertain execution location, including
cloud-search fallbacks, select `local-web-search`; routing stays read-only.

## Bundled Routes

Select a bundled skill from the host's listed skills by its description; the
descriptions are the selection surface, and this gate adds only the rules
below. An explicit `Axiom:<skill-name>` invocation selects that skill. A more
specific installed skill, MCP tool, or host tool the user chose is not
displaced by a bundled route. No match continues host-native.

Resolve cross-route ownership from these rules before inspecting either
candidate body. Persistent changes with consequential external app/account
effects, including publish/delete/remote-state mutation, select both `confirm-external-action` and `reversible-system-change`. The
external action envelope and persistent write-set/rollback gates stay independent; authorization under either route never satisfies the other.
Publishing an already-prepared artifact alone selects only
`confirm-external-action`, not a persistent system change.

Explicit machine-credential lifecycle work composes the existing owners; read
`references/credential-lifecycle.md`. Inventory/planning/consumer activation/cleanup select `reversible-system-change`; provider creation/revocation/disclosure select `confirm-external-action`; end-to-end uses both.
Human login, conceptual help and secret reveal stay no-route.

Routing never silently picks among mutually exclusive implementations with materially different route sets, write surfaces, or authorization or safety boundaries. If the user explicitly delegates the choice ("choose one", "your call") and every alternative is reversible and already authorized, choose the one that fits the user's environment and goal, state which and why before acting so the user can redirect, then route it; otherwise select only `clarify-intent` and ask one concise clarification question before selecting an action route. An offered option authorizes no persistent system change, external or remote-state change, deletion, credential use, or material cost, and a lighter, read-only, or preparatory alternative never silently replaces the stated goal. Once the user chooses an unambiguous implementation, resume normal route selection.

Assess ambiguity before delegation; only this gate then selects
`clarify-intent`, never `delegate-simple-task`; permission-bypass mode resolves no intent and expands no authority.

An explicit usage-reduction goal selects `optimize-agent-usage`; ordinary
performance work does not. Ordinary AGENTS audits select only `agents-architect`.

Exact existing authorization needs no reconfirmation unless scope changes. Prior refusal/assistant prose creates no policy. Ordinary named-remote Git remains host-native.

## Boundaries

- Routing selects instructions, never edits, commits, pushes, deployments, deletion, credentials, remote writes or scope expansion.
- Selected bundled skills give direction: their authority, safety, and evidence rules, including those in references the active phase loads, bind; a skill's own defaults list governs what else adapts, and without one, counts, formats, orderings, and step lists that carry no such rule are adaptable defaults; state any departure. Within every binding rule, the model decides how to handle the request's specifics, problems that arise, deviations from the expected result, external interference, and gaps between a plan and the ideal behavior.
- Startup routing is foreground and read-only: no writes, network, service, background process, telemetry or update check.
- On resume (including a fork) or compaction, reselect every still-active route from current direct evidence before any new mutation. If route or phase cannot be reconstructed, perform zero new mutations; use each selected route's handoff contract for prior attempts. A summary is a claim, not evidence.
- Never load all skills, route by topical similarity, edit protected metadata without scope or persist one-off discoveries as durable instructions.
- Where a host mode may deny an action, present the exact action for the user's grant first; a denial is a stop, never a retry by another tool, flag or path; read `references/host-permission.md`.

## Refresh

Read `references/updating.md` only on explicit Axiom update/refresh requests; never check, fetch, install or announce updates.

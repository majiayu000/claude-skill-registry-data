---
name: agent-plugin-architect
description: Design, initialize, audit, migrate, maintain, or evaluate a packaged Codex or Claude Code plugin's architecture across shared Skills, route ownership, manifests, marketplace wrappers, hooks, and version-bound compatibility evidence. Use only for explicit packaged agent-plugin architecture work. Do not use for evaluating or reviewing an individual Skill or Skill proposal, repository-local AGENTS.md, .agents/skills, or .claude/skills systems, ordinary source-code or documentation work merely because it is in a plugin repository, host installation, publication, deployment, or Git submission.
---

# Agent Plugin Architect

Design or audit the smallest coherent packaged-plugin control plane for Codex
and Claude Code. Keep each host's experience native and preserve a single
shared Skill tree when both hosts can discover it without weakening either host.

Defaults you may adapt, saying so: the order of steps 2-9 where no gate depends on it, the composed-route count, and deliverable layout. Every other rule here and in the references the active phase loads binds.

## Route The Work

1. For an unresolved choice between mutually exclusive workflows with material differences in route ownership, write surfaces, persistent metadata or authority, ask one clear question and keep the workflow unselected until the user chooses, unless the user explicitly delegated the choice and every option is reversible and already authorized; then state the chosen option and why before acting. An offered option authorizes no persistent system change, external or remote-state change, deletion, credential use, or material cost. Restate each option's original end goal and explain permission limits separately. Preparation, review, planning or preflight may support a chosen goal, but cannot replace it without the user's choice. Outside such a delegated choice, read-only authority, lower risk, lighter work or current feasibility cannot justify defaulting to one option, proceeding with it, or requiring the user to object to stop. Explicit architecture requests continue below; explicit installation stays with its owner, explaining unavailable authority without substituting an architecture audit. Conceptual comparisons and choices without material boundary differences do not require this gate. After selection, do not reconfirm unchanged conditions; ask only for necessary missing input or a material conflict.

   Confirm that the selected request explicitly concerns packaged agent-plugin architecture. Repo-local `AGENTS.md`, `.agents/skills`, or `.claude/skills` work belongs to `agents-architect`; ordinary plugin code or documentation has no Axiom route solely because it lives in a plugin repository.
2. Inventory the package before editing. Read `references/package-inventory.md`.
3. For a read-only audit of one packaged release candidate, read `references/release-readiness.md`. It classifies impact, version and runtime identity, local and remote evidence, and the one next decision, then stops before every mutation phase.
4. Define route ownership and trigger boundaries with `references/route-and-trigger-contracts.md`.
5. For shared Skill structure and direct discovery, read `references/packaged-skill-architecture.md`.
6. For startup hooks, untrusted content, credentials, or runtime effects, read `references/hooks-and-trust-boundaries.md`.
7. For manifests, wrappers, and Codex/Claude Code parity, read `references/cross-host-packaging.md`.
8. For routing cases, context cost, or host observations, read `references/evaluation-and-evidence.md`.
9. Before completion, read `references/validation-reporting.md`.

Load only references needed for the active phase. A request may compose this
route with at most one other Axiom route when both contracts are independently
necessary. An explicit usage-cost goal may add `optimize-agent-usage`;
retrospective review may add `review-axiom-task`. Git submission, installation,
publication, deployment, and consequential external effects remain separate
active phases and select their owning route instead of inheriting authority
from this Skill.

## Deliverable

Return the package inventory, route and trust decisions, changed surfaces,
validation evidence, compatibility class, and every host or lifecycle check
that is `NOT-RUN` or `UNAVAILABLE`. File presence and static parity are not
host execution evidence.

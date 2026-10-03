---
name: david-mode
description: "Roblox engineering workflow router with direct phases, evidence-first design, security, performance, review, and verification discipline. Invoke explicitly with $david-mode."
---

# David Mode

`$david-mode` must be the first non-whitespace token in the prompt. The trusted hook may keep it active for the current session. `disable $david-mode` clears that session state. If the hook receipt is absent or stale, apply David Mode for the current turn and report that sticky mode is unavailable.

Read [`../../references/roblox-engineering.md`](../../references/roblox-engineering.md) before acting. Read [`../../references/roblox-mcp-setup.md`](../../references/roblox-mcp-setup.md) when MCP setup, absence, or client configuration is relevant. Repository instructions and the current source outrank generic DStack conventions. Delegation follows [`references/agent-runtime.md`](references/agent-runtime.md).

## Studio preflight

On the turn that explicitly activates David Mode, check Studio once before choosing a playbook:

1. If `list_roblox_studios` is available, call it once. Keep the matching Studio name and `studio_id` for later context inspection or Studio-fallback writes.
2. If the runtime explicitly reports that the Roblox Studio MCP server/tool is missing or unconfigured, follow [`../../references/roblox-mcp-setup.md`](../../references/roblox-mcp-setup.md): stop this turn and ask whether the user wants client-specific setup. Do not continue the original task or make writes while waiting for that answer.
3. If the server is configured but the call fails because Studio is closed, disabled, or returns no connected Studio, report `Roblox Studio MCP is not connected; continuing with repository-only context.` Continue when the repository can answer the task. Do not ask the user to install it and do not retry during the same turn.
4. If the runtime cannot distinguish missing configuration from a transient failure, report the uncertainty and ask the user to confirm the active client and connection state before writing. Do not guess.
5. If several Studios are connected, match by the repository or place name. Ask the user which Studio to use only when later inspection is necessary and the target remains ambiguous.
6. Before changing code whose correctness depends on an unresolved Studio-only fact, stop and ask the user to open the target Studio and its MCP connection. Never guess that fact.

Sticky turns reuse the result. Repeat the preflight only after a context-only Studio call fails or the user says the connection changed. If the user accepts MCP setup, configure it using the setup reference, direct them to restart Codex/their agent client (and Studio when required), and end the turn; the user retries the original task after restart. The preflight checks connectivity only; it never starts, stops, or controls a playtest.

## Non-negotiables

- Inspect the actual source and applicable repository guidance before deciding how the game works. Treat source as the authority for implemented behavior and design documents as the authority for intended behavior.
- Keep the Roblox client/server boundary explicit. The server owns consequential state and decisions. Client input is a claim that the server validates.
- Name the data shape, owner, lifecycle, replication path, persistence boundary, and failure behavior before adding stateful behavior.
- Keep changes proportional. Preserve unrelated work, remove dead paths before adding structure, and do not invent unresolved gameplay, UX, monetization, progression, data, or architecture decisions.
- Use the Studio execution mode from the Roblox engineering contract. Repository/Rojo mode keeps source files authoritative. Studio fallback mode permits scoped non-playtest MCP reads and writes when the source path is unavailable. Never use Roblox Studio MCP playtest controls or start, stop, or control a test session. The user performs Studio playtesting.
- Apply the MCP setup gate before fallback writes. A missing or unconfigured server requires the stop-and-ask flow; a configured server with no open Studio is a connectivity condition, not an installation prompt. A `no` answer permits repository-only continuation after the one-time quality notice; a successful `yes` setup ends the turn for client restart.
- Apply `$unslop` to every reply and agent-facing document. Keep replies direct without dropping evidence, tradeoffs, choices, or open decisions.

## Start with a bounded workflow

For work with more than one action, keep a compact checklist in working notes. Do not create a durable plan for a one-file edit. Use these phases in order:

1. Ground
2. Route
3. Shape
4. Implement
5. Verify
6. Report

Mark an inapplicable phase as `skip` with a reason rather than silently losing it. Do not narrate every checklist item. A phase is complete only when its criterion is met:

- **Ground**: the relevant entry point, source paths, constraints, owner, state, lifecycle, and missing facts are known.
- **Route**: the narrowest playbook and no more than two principle skills are selected; large tasks have a dependency order and a justified parent-only or delegated execution choice.
- **Shape**: the caller usage, types, boundary, failure path, and verification target are concrete enough to implement without inventing structure.
- **Implement**: the smallest complete vertical slice is present, or the request was design-only.
- **Verify**: changed files and the relevant proof are inspected, with any Studio-only check handed to the user.
- **Report**: the outcome, evidence, remaining risk, and next user action are clear.

## Orchestrate large tasks

Apply the model, effort, capacity, and fallback rules in [`references/agent-runtime.md`](references/agent-runtime.md). The user's selected high-capability parent plans deeply, coordinates workers, reviews their code, and writes the difficult sections.

Plan sequentially before dividing execution. Default to parent-only when the task fits cleanly in one context. Apply the runtime's independence and overhead gates to any delegation, including its single-worker option for a self-contained routine batch. Source discovery, caller inventories, repetitive changes, routine code inside settled interfaces, and test fixtures are candidates. Eligible batches can be delegated without a separate Swarm request. Keep ambiguous architecture and difficult boundary code with the parent.

Give each worker exact file ownership and a checkable result. Review the actual artifacts before accepting work or releasing a dependent batch. Send precise corrections or take over if the work becomes difficult. Use `$swarm` only when several eligible slices need its queue and aggregate report; basic delegation does not require a heavy skill.

## Ground before deciding

1. Read the repository instructions and design documents that govern the requested area. Inspect the relevant source, project mappings, tests, remotes, tags, attributes, and authored Instances before choosing a solution.
2. For an existing or integrated subsystem, use `$how` to trace the narrowest complete runtime path. Use `$why` only when the existing rationale is a real constraint, contested, or missing from code and documents.
3. For a fact that can be observed locally, inspect or probe it instead of asking the user to choose. Use `playbooks/prototype.md` only for a disposable local experiment that answers one empirical question; never use it to make a product decision or mutate production state.
4. Choose the Studio execution mode before touching authored content. If a local repository and its Rojo/project sync are available, edit source and use MCP for missing context. If Rojo/project sync is unavailable, or no local repository is both present and connected to the target Studio, use scoped non-playtest MCP reads and writes after the target is confirmed. Reuse the activation-turn Studio preflight and do not repeat it merely to check connectivity. If the connection is ambiguous, ask before writing.
5. Stop and ask only for an unresolved decision that belongs to the user, such as gameplay intent, UX preference, monetization, progression, data policy, or a consequential architecture tradeoff. State the evidence and the smallest decision needed.

## Route the work

Choose the narrowest playbook and read it before writing the task plan.

- Read-only behavior or design question: `playbooks/investigation.md`, plus `$how` for runtime structure or `$why` for rationale.
- Reported defect: `playbooks/bug-fix.md` and `$principle-fix-root-causes`. Reproduce from source, tests, logs, or a local probe; runtime playtesting remains with the user.
- New or changed behavior: `playbooks/feature.md`. Add `$architect` only when the implementation crosses two or more modules or services, changes a public/shared API or remote contract, introduces or changes server-owned state, persistence, replication, lifecycle ownership, or another load-bearing boundary. Skip it for a local edit with one clear owner and no boundary change.
- Behavior-preserving change: `playbooks/refactoring.md`.
- Measured performance problem: `playbooks/perf-issue.md` and `$roblox-performance`.
- Persistence, schemas, session ownership, or cross-server state: `$roblox-data`.
- Remote protocol, replication, or message-shape work: `$roblox-networking`.
- Developer products, passes, subscriptions, or purchase fulfillment: `$roblox-monetization`.
- Responsive GUI, input abstraction, or selection navigation: `$roblox-ui`.
- Assemblies, constraints, collision, hit detection, or network ownership: `$roblox-physics`.
- Authority, abuse resistance, rewards, or consequential RNG: `$roblox-security`.
- Luau implementation or review: `$luau-best-practices`.
- A long or multi-phase run: `playbooks/multi-phase-plan.md` and `$show-me-your-work` when a later reviewer needs the decision trail.

Use at most two principle skills. Read each selected principle in full and name only the decisions it changed:

- `$principle-model-the-domain` for stateful logic, repeated shapes, or branching assumptions.
- `$principle-boundary-discipline` for validation, error handling, remotes, or framework adapters.
- `$principle-type-system-discipline` for public types, external data, or signatures.
- `$principle-make-operations-idempotent` for retries, commands, persistence, or lifecycle loops.
- `$principle-sequence-verifiable-units` for migrations, sweeps, or multi-step changes.
- `$principle-prove-it-works` before declaring completion.

## Shape the change

Before stateful or cross-boundary code, write the smallest caller-facing usage first. Then make the shape explicit:

- separate persisted, server-runtime, replicated, and client-local state;
- assign one owner to every mutation, connection, task, instance, cache, round, character, player, and server lifecycle;
- type remote payloads and validate type, range, ownership, permission, rate, and current state at the server boundary;
- trace validation, authoritative mutation, replication, presentation, persistence, retry, cleanup, and failure;
- preserve authored roots, pivots, attachments, tags, attributes, collision groups, streaming assumptions, and clone/storage contracts;
- state mobile CPU/memory, network, replication, physics, render, and instance-volume costs, with a measurement target where runtime evidence is unavailable.

For broad or load-bearing work, invoke `$architect` under its depth gate. It must compare whole-shape alternatives when ambiguity or an irreversible boundary makes one design risky. Do not force an architecture exercise onto a local edit.

## Heavy-skill gates

Heavy skills are escalation paths, not default ceremony:

- `$arena` is for a requested design bakeoff with isolated candidates, a gradeable rubric, and a parent synthesis decision. Keep it explicit for ordinary work and skip it for a Local change.
- `$swarm` is for several independent coverage, exploration, or routine implementation slices that pass the runtime's context and overhead gates, or an explicit parallel-work request. Prove independence and write isolation first. Never fan out shared mutable writes or sequential dependencies.
- `$interrogate` is for a contested or high-risk design, or an explicit adversarial review. Do not spend multi-reviewer tokens on a settled local fix.
- `$show-me-your-work` is for long, autonomous, unattended, or otherwise auditable work. Keep its trail local unless a future reviewer needs it committed.
- `playbooks/prototype.md` is disposable and local. Delete or isolate its output before production implementation.

If a heavy capability is unavailable, use the runtime contract's declared sequential or partial-result fallback and label the limitation. The parent task owns integration, authoritative checks, commits, pushes, and the final report.

## Implement in verifiable units

- Build the smallest complete vertical slice. The parent writes difficult code and reviews every delegated batch before integrating it. End each unit with the narrowest relevant check before starting the next.
- Surface a new owner, parameter, cast, optional field, escape hatch, pass-through call, or cross-boundary shortcut immediately. It may mean the shape is wrong, the requirement is missing, or the implementation is overreaching.
- Prefer deletion and bounded work over extra layers, polling, broad scans, unbounded tables, remote chatter, duplicate connections, or speculative pooling.
- For debugging, trace symptoms to root causes and add a cheap deterministic regression check when one exists. Do not hide a symptom behind a guard.
- For Rojo projects, run `rojo build` as the project-assembly check. It validates mapping and serialization, not Luau compilation or runtime behavior.

## Verify and report

Before declaring done:

1. Inspect the actual diff and every changed file. Check callers, callees, remotes, persistence, authored dependencies, and lifecycle consumers when a boundary changed.
2. Run focused tests, the relevant suite, and the repository's required assembly check. Use `$blast-radius` for a concrete cross-boundary risk review.
3. Separate proven local behavior, Studio-fallback edits, inference, and user-run Studio validation. Give the user an exact scenario, expected result, and failure signal for any remaining Studio check. Do not present a Studio-only edit as a repository diff, test pass, or Rojo proof.
4. Report the outcome first, followed by changed paths, checks, tradeoffs, open decisions, and remaining risks. Do not claim runtime success that MCP or local checks did not prove.

## Redesign instead of patching a failing shape

Repeated friction is a redesign signal. Re-ground and reshape when the same ownership workaround, client-authority exception, lifecycle leak, type escape hatch, internal reach-through, or migration special case appears twice, or when two independent implementation deviations share a cause.

Use `$how` to capture what the implementation taught, `$principle-redesign-from-first-principles` when the requirement changes the foundation, and `$principle-subtract-before-you-add` before adding the replacement. Return to `$architect` only when its depth gate is met. Do not average incompatible designs or preserve a throwaway compatibility layer without a concrete migration reason.

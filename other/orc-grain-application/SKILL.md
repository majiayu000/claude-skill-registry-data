---
name: orc-grain-application
description: "Model and implement the Grain application around an ORC tree: domain commands, events, processors, periodic triggers, projections, queries, tenant scoping, authorization, and Event Model topology. Use when ORC actions must persist domain facts or serve production reads."
---

# Build the application around the tree

ORC already emits its own execution events. Use Grain for **domain facts** and application workflows around ORC: a code action may issue a command, a processor may start a tree after an event, and a query may combine domain projections with ORC execution projections. Keep domain policy in commands and Allium rules; a blackboard value alone is not a committed domain fact.

Check the application’s instructions if provided, the current ORC/Grain revisions, and [contracts.md](references/contracts.md) before implementing. This skill is about the Grain substrate; use `orc-design-tree` for tree design and `orc-runtime-bootstrap` for boot wiring. ORC also tracks the [schema](../../.claude/skills/grain-schema/SKILL.md), [command](../../.claude/skills/grain-command-handler/SKILL.md), [read-model](../../.claude/skills/grain-read-model/SKILL.md), [query](../../.claude/skills/grain-query-handler/SKILL.md), [processor](../../.claude/skills/grain-todo-processor/SKILL.md) and [periodic-task](../../.claude/skills/grain-periodic-task/SKILL.md) skills. For deeper Grain guidance, use the public [Grain skill collection](https://github.com/ObneyAI/grain/tree/main/skills), including the [Grain engineering entry point](https://github.com/ObneyAI/grain/blob/main/skills/grain/SKILL.md) and [Event Model skill](https://github.com/ObneyAI/grain/blob/main/skills/event-model/SKILL.md). That collection also covers Event Model elicitation, distillation, propagation, tending and reconciliation. To read those skills locally, give the agent access to a Grain checkout alongside ORC. Adding Grain as a library dependency does not automatically configure discovery of its agent skills. These public companion skills add depth; the bundled contracts reference remains usable without a personal skill installation.

## Shape the write and read sides

1. Name an actor intent, the invariant it must uphold, immutable resulting event(s), and the exact read projection that can prove the outcome. Put acceptance behavior in Allium; keep Event Model as topology and link it to the relevant rule/surface.
2. Register Malli command/query schemas and event-body schemas. `defcommand` checks current state through a read model and returns `:command-result/events` built with v3 `->event`; the v3 append assigns event IDs and timestamps. No direct/bare append from an ORC code node or processor for a domain command.
3. `defreadmodel` is a pure reducer over named event types. `defquery` reads projections and returns `:query/result`. Exposed commands and queries need an explicit `:authorized?` predicate evaluated by the request adapter, or an explicit guard at the host/handler boundary. Direct command/query processors do not execute that metadata. Bind identity and tenant from trusted host context, then actually check their authority; claims alone are data, not enforcement.
4. `defprocessor` reacts to a durable event and issues a command or performs a declared effect. Choose checkpoint-before or checkpoint-after according to the actual duplicate/loss tradeoff; make at-least-once external effects idempotent. Avoid read-state → decide → write races during concurrent events; use the event-store CAS or a domain idempotency key where required. `defperiodic` emits trigger events; use an explicit `:result/cas` guard when a schedule tick must be deduplicated. Its processor does the work.
5. Prove from the public path: command → event → projection → query, plus processor/schedule when present. Read the projection back under the same tenant and test a second tenant's isolation. Test duplicate triggers, restart/replay, and authorization denial where those are real risks. A successful command return is not enough.

Keep generated handler vars distinct within a namespace. Several declaration macros generate `<service>-<name>`: `defreadmodel :app results` and `defquery :app results` both define `app-results`; `defperiodic :app refresh` and `defprocessor :app refresh` both define `app-refresh` with different arities. A later declaration can overwrite the function behind an already registered Var. Use distinct names or namespaces, such as `tool-results`/`results` and `refresh`/`process-refresh`, and exercise every registered path. Direct processor calls need full command/query envelopes with UUID IDs and offset-date-time timestamps. Tool capabilities using direct calls must enforce authority before effects and reads. Verify denial through the path actually used by the action. ORC query authorization metadata examines `:auth-claims` when an enforcing boundary evaluates it; supplying those claims to a direct processor does not perform the check.

Use [contracts.md](references/contracts.md) for current macro shapes, Event Model edges, and a concrete verification scenario. When observable behavior changes in ORC, follow its Allium loop, diagnostic baseline, and spec-integrated inspection gate; do not treat a clean test process exit as proof that specifications and projections agree.

Keep file/network effects out of a command handler's decision body: constructing its returned events must not itself write a file or call an external service. For durable work, record intent and execute through an owned processor/capability with appropriate idempotency and reconciliation. A deliberately synchronous experiment may call a guarded host capability and then record its actual observation through a command, but the external effect and event append are not atomic. Preserve that limit; a receipt projection alone does not prove crash-safe exactly-once execution.

## Skill check

Try: “A successful recommendation-tree run should record a proposal for tenant A, then expose proposals through a query. A daily process may request refreshes, but duplicate triggers must not create duplicate proposals.” A satisfactory design names commands/events, validates the durable proposal state, routes ORC code through a command, projects and queries per tenant, makes the scheduler a trigger, handles idempotency, links topology to Allium, and tests output plus read-back. The skill must not invent the app's business eligibility rules.

## Durable quality reporting

Read [orc-judges](../orc-judges/SKILL.md) for immutable assessment manifests and banded result reporting. Use commands to record expected assessments and typed scored/failed/ungradable outcomes, then project tenant-scoped coverage, bands and available feedback by actual scope/model/rubric filters. Validate concurrent replay against the exact persisted payload. Rebuild from events in a fresh process. An application reporting sample does not supply a native durable judge worker scheduler or holistic tree grade.

## Current decisions and tools

At ORC `1851212396cced2fc4533fda30b824bd4b691390`, use [decision models](../orc-decision-models/SKILL.md) for one-answer boolean/Choice nodes and registered native providers, and [tools](../orc-tools/SKILL.md) for authored tool leaves and enforced code/tool/researcher contracts. Delegate context, family budgets/usage and execution leases are integrated. Native Score still needs a custom client; these updates do not repair judge jobs, attachment, evidence scopes or score identity. Contracts do not replace authorized domain commands or callee idempotency.

## Terminal execution reporting

For a durable application outcome when a root exhausts its execution paths, read [terminal execution outcomes](references/terminal-execution-outcomes.md). Keep retained work, failed execution and semantic goal assessment distinct; use canonical ownership and an idempotent Grain processor/command path.

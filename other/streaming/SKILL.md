---
name: streaming
description: >-
  Route StreamingStore/Kefir work for Node, servers, workers, CLIs, tests, and
  paths without concrete UI evidence. Default to this no-UI family; keep other
  Store families separate and shared Redux/saga work in core.
type: core
requires:
  - core
sources:
  - "@themislib/themis/README.md"
  - "@themislib/themis/docs/SELECTORS.md"
  - "@themislib/themis/streaming-store"
  - package-internal streaming selector implementation
triggers:
  - streaming store
  - StreamingStore
  - Kefir selector
  - observable selector
  - streaming selector
  - stream selector lifecycle
  - Node store
  - server store
  - background worker store
  - CLI store
  - test harness store
---
# Streaming Store and selector routing

Use this root for Streaming-specific `themis` work and as the default package route when the touched code path uses the Kefir/observable Store variant. It covers Node/server environments, background workers, CLIs, test harnesses, and apps without framework-specific integration. Generic Redux/redux-saga guidance remains in `../core/`.

> StreamingStore is the Kefir/observable variant exported from `@themislib/themis/streaming-store`.

## Exclusive Streaming Store family rule

- A Node/server/CLI/worker/test-harness app using this skill has chosen the concrete Streaming Store family: `StreamingStore`, Kefir/observable selector calls, and streaming lifecycle/setup patterns.
- Do **not** apply alternate Store-family or lifecycle patterns inside that same app/package/code path.
- In a mixed repository, keep framework-specific applications and this Streaming app isolated by code path.

## Preflight

- Read this skill plus the streaming leaf that matches the touched behavior.
- Also read `../core/import-boundaries/SKILL.md` when changing imports or package paths.
- Record why StreamingStore/Kefir behavior is the target route. In mixed repositories, classify by the files being changed.
- Do not describe `Store` as a streaming API.
- Keep implementation guidance focused on StreamingStore and Kefir observable lifecycle behavior.
- Include verifier-ready evidence: skill path inventory, stale streaming path/name searches, frontmatter/requires checks, install/cleanup smoke when safe, and `git diff --check`.

## Streaming leaf routes

| Route | Use when |
| --- | --- |
| ./store/SKILL.md | Choosing/importing StreamingStore and owning construction, process bootstrap, initialization, and whole-Store disposal. |
| ./selectors/SKILL.md | Authoring Store-bound selectors whose direct calls return cached Kefir Observable values, including observable selector arguments, .withStore, .select, and .effect. |
| ./selector-lifecycle/SKILL.md | Direct-call validity, explicit Store binding, and consumer subscription timing/teardown; not Store construction or runtime disposal implementation. |

First-time app setup starts at the canonical root setup skill: `../setup/SKILL.md`.

## Operational guidance owners

- For the public class import and process lifetime, read `./store/SKILL.md` — **Correct import and class choice**, **Lifecycle rules**, and **Process bootstrap**.
- For Store-bound creation, observable arguments, direct/pure/saga call forms, scheduling, and output reuse, read `./selectors/SKILL.md` — **Authoring rules**, **Call forms**, **Selector caching**, and **Stable selector arguments**. This router does not duplicate the selector contract.
- For invocation validity and observer cleanup, read `./selector-lifecycle/SKILL.md` — **Lifecycle map** and **Consumer subscription ownership**.
- Streaming diagnostics use the shared contracts: `../core/selector-tracing/SKILL.md` — **Configure the Store**, **Aggregate summaries**, and **Store-family symmetry and lifecycle**. These own trace defaults/options, summary allocation, and selector-resource disposal.
- For the public stream inventory/types, custom logger replacement and cleanup, Redux middleware event ordering, immutable payloads, rendering, and privacy, read `../core/redux-action-logging/SKILL.md` — **Store-owned logging streams**, **Logger factory lifecycle**, **Read one action's group**, and **Keep logging opt-in and temporary**.
- For Redux/saga behavior rather than Kefir consumption, use `../core/SKILL.md` — **Core leaf routes**; selector-driven saga subscriptions specifically belong to `../core/selector-channels/SKILL.md` — **Do** and **Implementation cues**.

## Verification cues

- `./**/SKILL.md` files are non-empty and contain operational guidance, not compatibility shims.
- Root/artifact routing lists `./SKILL.md`, `./store/SKILL.md`, `./selectors/SKILL.md`, and `./selector-lifecycle/SKILL.md`.
- Stale scans find no obsolete streaming skill path/name references.
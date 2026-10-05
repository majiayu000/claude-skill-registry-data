---
name: setup
description: >-
  Start here for first-time or greenfield Themis setup. Choose one Store family,
  then follow the neutral checklist and core/family owners. Installation
  commands live in the canonical installation docs.
triggers:
  - init redux
  - setup store
  - new project
  - bootstrap redux
  - setup redux saga
  - add redux to svelte
  - add redux to react
  - setup ReactStore
  - setup StreamingStore
  - setup redux in node
  - initialize state management
---
# Init themis — Canonical Greenfield Setup

## Agent Preflight Compliance Contract

Before editing code or docs under this skill:

- **MUST** read this skill plus `../SKILL.md` and every linked skill/doc that applies to the touched files.
- **MUST** cite the applicable skills/docs in the implementation plan or completion handoff, including the rules used.
- **MUST** include verifier-ready evidence: searches, tests, or diff checks proving the cited rules were followed.
- **MUST** decide and record exactly one concrete Store family for the app/package/code path before creating or editing setup files.
- **MUST** collect concrete routing evidence first: Svelte/SvelteKit evidence chooses `Store`; React evidence chooses `ReactStore`; Node/server/worker/CLI/test/no-UI or observable evidence chooses `StreamingStore` by default.
- **MUST** keep `Store`, `ReactStore`, and `StreamingStore` mutually exclusive inside one app/package/code path. Separate apps in a mixed repository may choose different families only when their files and runtime lifecycles are isolated.
- **MUST** keep active greenfield setup routing on this root setup skill, not under a family-specific setup path.
- **SHOULD** stop and ask when rules conflict or scope is unclear.
- **NEVER** claim completion when a required skill/doc was skipped or the handoff lacks compliance evidence.

> Canonical setup guide for bootstrapping a new app with the themis package. Follow the branch that matches the one concrete Store family chosen for the app.

## Store-family decision gate

Make this decision before creating `store.ts`, selectors, root lifecycle wiring, sagas, or tests. Record the evidence in the handoff.

| Evidence in the target app/package/code path | Choose | Import | Read next |
| --- | --- | --- | --- |
| Concrete Svelte/SvelteKit evidence: svelte.config.*, .svelte files, SvelteKit +layout/+page, imports from svelte, $selector template reads, Svelte readable expectations | Svelte Store family | Store from @themislib/themis/svelte-store | ../svelte/SKILL.md, ../svelte/component-integration/SKILL.md, ../svelte/selectors/SKILL.md |
| Concrete React evidence: React dependencies in the app path, JSX/TSX React components/hooks, imports from react, ReactStore, Preact React signal selectors, direct signal reads, or necessary .useValue(...args) fallback reads | React Store family | ReactStore from @themislib/themis/react-store | ../react/SKILL.md, ../react/store/SKILL.md, ../react/selectors/SKILL.md |
| Node services, server routes, background workers, CLIs, scripts, test harnesses, no-UI paths, Kefir/observable selector arguments, or no concrete Svelte/React evidence | Streaming Store family by default | StreamingStore from @themislib/themis/streaming-store | ../streaming/SKILL.md, ../streaming/store/SKILL.md, ../streaming/selectors/SKILL.md, ../streaming/selector-lifecycle/SKILL.md |

**Mutual exclusivity rule:** one app/package/code path must not mix concrete Store families. Do not import more than one of `Store`, `ReactStore`, and `StreamingStore` into the same setup path, do not mix Svelte readable `$selector` patterns with React `.useValue(...)` or Kefir observables, and do not reuse lifecycle examples across families except as explicit contrast notes.

## Installation workflow

Choose a bundle using `../SKILL.md` — **Consumer skill install routing**. Follow `@themislib/themis/docs/INSTALLATION.md`, the sole owner of installation operations:

- **Consumer package installation** — package/runtime dependencies, the selected family's peers, and the optional saga-test helper.
- **Explicit skill installation** and **Consumer CLI and bundle selection** — explicit commands, bundle contents, destinations, compatibility links, collision handling, and refresh behavior. Narrowing a bundle removes previously manifest-owned family files; it does not add Core alongside every earlier family.
- **Verify, refresh, cleanup, and uninstall** — verification and cleanup-before-uninstall ordering, including preservation of unrelated files/dependencies.
- **Maintainer source-checkout validation** — the separate repository workflow, not a substitute for consumer installation.

## Neutral setup checklist

Complete this sequence using the linked owners rather than adapting an example from another family:

1. Record the family and target path from **Store-family decision gate**, then follow **Installation workflow**.
2. Design one small canonical slice using **Shared implementation references** below: define types, actions, and reducer before registering it.
3. Construct the chosen Store and wire its initialization/disposal at the app's lifetime boundary using **Family implementation references**. Preserve inferred app state and package-owned internal boundaries from that Store skill.
4. Define Store-bound selectors and consume them using only the chosen family's call-mode and lifecycle skills. Use its composition/test and saga read forms where direct reactive calls do not apply.
5. Register the reducer and start app sagas through the selected family's bootstrap owner. Follow `../core/sagas/SKILL.md` — **Application saga startup** and `../core/saga-manager/SKILL.md` — **Store saga lifecycle** for startup and cancellation; Store initialization is not app-saga registration. Only the explicit lifetime owner has the saga-function import exception in `../core/import-boundaries/SKILL.md` — **Bootstrap and lifetime-owner exception**; ordinary handlers dispatch actions.
6. Verify an action changes the expected slice, the chosen selector consumer sees the update, the saga handles its trigger, and teardown releases subscriptions/tasks and the Store. Complete **Verification and handoff**.

## Family implementation references

Read only the selected row. These leaves own the concrete examples formerly embedded in this setup guide; there is no shared framework-specific working example to copy or translate.

| Family | Construction and app lifetime | Selector authoring and consumption |
| --- | --- | --- |
| Svelte Store | `../svelte/store/SKILL.md` — **Correct import and class choice**, **Lifecycle rules**, **App saga lifetime**; `../svelte/component-integration/SKILL.md` — **Root layout wiring**, **Template and handler wiring** | `../svelte/selectors/SKILL.md` — **Choose the factory**, **Examples**; `../svelte/selector-lifecycle/SKILL.md` — **Call-mode map** |
| React Store | `../react/store/SKILL.md` — **Correct import and class choice**, **Lifecycle rules**; `../react/component-integration/SKILL.md` — **Create and configure ReactStore**, **Initialize before React renders selector users**, **Dispose at the same owner boundary**, **Start app sagas explicitly**, **Component reads and dispatch** | `../react/selectors/SKILL.md` — **Authoring rules**, **Selector caching**; `../react/selector-lifecycle/SKILL.md` — **Call-mode map** |
| Streaming Store | `../streaming/store/SKILL.md` — **Correct import and class choice**, **Lifecycle rules**, **Process bootstrap** | `../streaming/selectors/SKILL.md` — **Authoring rules**, **Call forms**, **Selector caching**; `../streaming/selector-lifecycle/SKILL.md` — **Lifecycle map**, **Consumer subscription ownership** |

## Shared implementation references

Use these framework-neutral owners for the slice/action/reducer/saga portion of setup:

| Setup concern | Canonical instruction and examples |
| --- | --- |
| State/effect ownership and custom Redux APIs | `../core/core-policy/SKILL.md` — **Setup — core rules**, **When to use Redux vs component-local state** |
| App-owned slice files, separate type modules, reducer registration, and action namespaces | `../core/file-structure/SKILL.md` — **Setup — slice directory layout**, **Register a normal slice**, **Naming conventions** |
| Public builder imports and configured Store imports | `../core/import-boundaries/SKILL.md` — **Setup — the package export surface** |
| No-payload and tuple-payload actions | `../core/actions/SKILL.md` — **No-payload action for explicit events**, **Tuple payload action consumed by reducers** |
| Pure immutable chained reducers | `../core/reducers/SKILL.md` — **Do**, **Chain handlers on the reducer function** |
| Canonical facts, derived selectors, and entity Collections | `../core/state-integrity/SKILL.md` — **MUST / NEVER rules**; `../core/collections/SKILL.md` — **Shape and imports** |
| Serializable initial state and payloads | `../core/state-serialization/SKILL.md` — **Do** and **Don't** |
| Saga watchers, named selector effects, and app-saga cancellation | `../core/sagas/SKILL.md` — **Do**, **Examples**, **Application saga startup**; `../core/saga-manager/SKILL.md` — **Store saga lifecycle** |

## Optional diagnostics and scheduling

Configure diagnostics only for the selected Store instance; shared contracts do not require switching families.

- Selector diagnostics and constructor options: `../core/selector-tracing/SKILL.md` — **Configure the Store** and **Scope and safety rules**. Shared streams and custom logging: `../core/redux-action-logging/SKILL.md` — **Store-owned logging streams** and **Logger factory lifecycle**.
- Saga monitoring and Store-owned middleware: `../core/sagas/SKILL.md` — **Do** and **Don't**.
- Selector scheduling, only for the chosen family: `../svelte/selector-scheduling/SKILL.md` — **Scheduling options**; `../react/selector-scheduling/SKILL.md` — **Store-first scheduling rule**; or `../streaming/selectors/SKILL.md` — **Call forms**.
- Optional browser Store inspection (when that hook is applicable): `../core/debugging/SKILL.md` — **Inspect state from the console** and **Setup — minimum working inspection**. This is not a prerequisite for non-browser setup.

## Verification and handoff

- Run the target app/process or focused test harness. Verify one end-to-end dispatch, selector update, and saga trigger using the selected family leaves' **Verification cues**; include the teardown path.
- Use `../core/testing/SKILL.md` — **Layer rules** for reducer, pure-selector, and saga checks, and **Saga test setup cues** for the optional test helper.
- Follow `../core/state-integrity/SKILL.md` — **Automated architecture gate workflow** for the repository/app gate appropriate to the target.
- Search for multiple concrete Store imports and mismatched selector consumption in the same app/package/code path. Record the routing evidence, canonical skills read, tests run, and lifecycle owner. Separate apps may select different families; a single app may not.
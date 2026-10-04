---
name: validate-yano-x-appchain
description: Select and run Yano X app-chain regression gates across focused tests, plugin/artifact boundaries, distributions, and live multi-node behavior. Use after changing state machines, capabilities, composition, effects, connectors, products, manifests, persistence, proofs, anchoring, configuration, showcase behavior, or host compatibility.
---

# Validate Yano X App Chains

## Establish scope

1. Read `AGENTS.md` and the affected ADRs/docs.
2. Inspect the change and map it to deterministic state, plugin lifecycle,
   publication/bundle, distribution, node-local projection, external effect,
   proof, anchor, or operations behavior.
3. Inspect both worktrees and preserve unrelated changes. Never commit
   automatically.
4. Build against one exact Yano version and matching JVM ZIP when a
   distribution or live process is involved.

## Apply the test ladder

Run the narrowest useful tests while iterating, then the required boundary
gates:

```bash
./gradlew <affected-module>:test -PyanoVersion=<yano-version>
./gradlew test verifyArtifactInventory verifyJvmOnlyBuild \
  -PyanoVersion=<yano-version>
```

Add the following according to scope:

- `integrationTest` for multi-module or host/plugin integration.
- `cryptoTest` for signing, hashes, commitments, proofs, or on-chain vectors.
- `distributionCheck` or a clean root `build` for publication,
  bundle, catalog, isolation, launch, dependency, or packaging changes.
- `:examples:showcase:showcaseScriptContract` for launcher/config changes.
- `:examples:showcase:showcaseDistributionContract` for packaged showcase or
  documentation inventory changes.
- A live three-node showcase run for runtime, persistence, consensus,
  catch-up, proof, indexer, effect, or anchor behavior.

## Preserve core invariants

For every affected chain, verify where applicable:

- all three nodes agree on finalized height, state root, commitment profile,
  genesis ID, and capability-manifest digest;
- finality certificates meet the configured threshold and proposer/member
  behavior matches the selected sequencer and governance modes;
- submitted commands are visible on peers, typed/message proofs verify against
  a caller-pinned root, and catch-up produces the same state;
- plugin contributions activate only through the catalog, bundle classes come
  from the expected origin, host API classes are not embedded, and lifecycle
  resources close on shutdown;
- deterministic transitions remain independent of wall clock, randomness,
  environment, network, and node-local ordering;
- apply, rollback, replay, graceful restart, and abrupt-restart recovery
  reproduce the original state for persistence-sensitive changes;
- authoritative app-chain state remains separate from L1 `chainstate`, while
  rebuildable index checkpoints never exceed the authoritative finalized tip;
- effect intents are deterministic, external delivery remains at-least-once,
  outcome incorporation remains exactly-once, and idempotency identity is
  preserved;
- SCRIPT anchor identity is unchanged, co-signed progression is monotonic, and
  followers agree with the leader. A proof is independently anchored only
  after its root/height is verified from Cardano, not merely caller-pinned;
- error scans distinguish known benign startup noise from app-chain failures.

## Avoid stale pre-split procedures

The sibling Yano repository contains historical `test-app-chain-*` skills that
record useful scenarios such as rotating proposers, governed membership,
SCRIPT anchoring, L1 observations, SSE, webhooks, evidence, snapshots, and
metrics. Use those as invariant history only. Do not run their old monorepo
paths, flat configuration, or direct host classpath assumptions against Yano X.
Exercise the equivalent behavior through current bundles and the packaged
showcase.

## Report

State which tiers ran, exact input versions, pass/fail results, any skipped
live or distribution gates, and why. A focused unit-test pass is not evidence
of a clean distribution or cross-node regression pass.

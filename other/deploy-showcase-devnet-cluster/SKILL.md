---
name: deploy-showcase-devnet-cluster
description: Build, stage, start, resume, smoke-test, and validate the Yano X three-node devnet showcase, especially the retained side-by-side deployment at /Users/satya/Downloads/yano-cluster/devnet-cluster-x on HTTP 7170-7172. Use for showcase ZIP rebuilds, devnet cluster operation, SCRIPT anchor audits/bootstrap, cross-node state/capability checks, or deployment runbook refreshes.
---

# Deploy Showcase Devnet Cluster

## Prepare safely

1. Announce that the workflow operates a local three-node cluster.
2. Read `AGENTS.md`, `examples/showcase/DEMO_SHOWCASE.md`, and the target's
   `DEVNET_CLUSTER.md` when it exists.
3. Inspect Yano X and sibling Yano worktrees. Never commit automatically.
4. Confirm Java 25, `curl`, `jq`, `python3`, and `unzip`.
5. Treat an existing target as retained identity and data. Never replace,
   reset, or regenerate it implicitly.

## Default retained deployment

- Target: `/Users/satya/Downloads/yano-cluster/devnet-cluster-x`
- Instance: `devnet-x`
- HTTP: `7170-7172`
- N2N: `14337-14339`
- Nodes/threshold: `3/2`
- Stores: sibling `chainstate`, `appchain-chainstate`, and
  `appchain-indexers` roots per node

These non-default ports allow the older `devnet-cluster` deployment to run at
the same time.

## Build a current archive

Publish the matching Yano Maven artifacts and ordinary JVM ZIP first. Stage
Yano X publications into a new empty internal repository as described by
`$build-yano-x`, then run:

```bash
./gradlew :examples:showcase:test \
  :examples:showcase:showcaseScriptContract \
  :distribution:jvm:yanoXJvmDistZip \
  :examples:showcase:showcaseDistributionContract \
  -PinternalRepository=<yano-x-staging> \
  -PyanoVersion=<published-yano-version> \
  -PyanoJvmDist=/absolute/path/to/yano-<same-build-identity>.zip \
  -PuseMavenLocal=true
```

The archive is
`distribution/jvm/build/distributions/yano-x-jvm-<yano-x-version>.zip`; the
showcase runs from its `examples/showcase/` directory.
Do not overwrite an extracted retained deployment with it. Stage a fresh
archive under a new reviewed target, or make an explicit preservation plan for
the existing `data/` and generated configuration.

## Operate or create

Resume the retained deployment with:

```bash
cd /Users/satya/Downloads/yano-cluster/devnet-cluster-x
./showcase.sh status --instance devnet-x
./showcase.sh up --instance devnet-x
```

For a new extracted target with no retained identity, run `doctor`, then:

```bash
./showcase.sh quickstart --profile light --nodes 3 --instance <instance>
```

Use explicit `--http-base` and `--n2n-base` values when the default ports are
occupied. Bootstrap SCRIPT anchors only for a new identity or when explicitly
requested:

```bash
./showcase.sh anchor bootstrap all --instance <instance>
```

Run demonstrations with `./showcase.sh run all --instance <instance>` or select
the relevant scenario while debugging.

## Validate

Run the read-only validator with the target, instance, and first HTTP port:

```bash
bash .agents/skills/deploy-showcase-devnet-cluster/scripts/validate_cluster.sh \
  /Users/satya/Downloads/yano-cluster/devnet-cluster-x devnet-x 7170
```

Inspect the first relevant `ERROR` in each node log if validation fails. Do not
wipe state to make a failure disappear. Leave the cluster running unless the
user asks otherwise.

## Identity and proof safety

- Never print seeds, signing material, API keys, or connector credentials.
- Never regenerate a retained chain `genesis-id`.
- Require identical height/root/profile/genesis/capability-manifest digest on
  all members. Only node 0 needs the anchor-writer view.
- Reject legacy app-chain derived data below L1 `chainstate` and any index
  checkpoint ahead of authoritative app-chain state.
- A caller-pinned proof validates mechanics. Describe it as independently L1
  anchored only after separately verifying its Cardano transaction/datum.
- `stop` preserves retained data. `reset --yes` is destructive and requires an
  explicit reviewed request.

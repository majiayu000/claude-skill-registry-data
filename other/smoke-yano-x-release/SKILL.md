---
name: smoke-yano-x-release
description: Smoke-test a built Yano X JVM release ZIP on the local machine before tagging a pre-release — archive layout, tool launchers, the packaged multi-node acceptance gates (two-node generated project, three-node stock cluster), and a live three-node showcase with run-all, verify, restart, and persisted-root checks. Use before a Yano X release, after distribution or packaging changes, after moving to a new Yano version, or when asked whether the showcase and multi-node clusters still work.
---

# Smoke-Test a Yano X Release ZIP

## Prepare

1. Read `AGENTS.md` and `docs/BUILD_DISTRIBUTIONS.md`. Never commit
   automatically.
2. Confirm Java 25, `curl`, `jq`, `python3`, `unzip`, and `lsof`.
3. Build the archive (see `$build-yano-x`), then copy it somewhere stable so a
   later Gradle run cannot rewrite it mid-test:

   ```bash
   ./gradlew :distribution:jvm:yanoXJvmDistZip \
     :distribution:jvm:verifyYanoXJvmDistribution \
     :examples:showcase:showcaseScriptContract \
     :examples:showcase:showcaseDistributionContract -PskipSigning=true
   cp distribution/jvm/build/distributions/yano-x-jvm-<version>.zip <scratch>/
   ```

4. Never reuse ports or data of a retained deployment such as
   `devnet-cluster-x` on HTTP 7170-7172. Port 7070 is often taken by another
   local Java process; the script defaults avoid it.

## Run

From the repository root:

```bash
.agents/skills/smoke-yano-x-release/scripts/smoke_release_zip.sh \
  <scratch>/yano-x-jvm-<version>.zip [--http-base 29770 --server-base 29370] [--keep]
```

The script takes about 10-15 minutes. It extracts into a new working
directory, checks ports first, and prints one PASS/FAIL line per step:

| Step | Covers |
| --- | --- |
| `archive`, `layout` | ZIP integrity, host jar, plugins, devnet overlay, every `tools/*/bin` launcher on shared `tools/lib` |
| `runtime-acceptance` | Two-node generated project: identity, drift, finality, message/state proof, evidence, follower restart parity, no secrets in logs |
| `stock-outcomes` | Three-node `yano.sh appchain cluster` with the repository stock config: audit proof, registry value proof, approval and effect demo |
| `showcase-quickstart` | 13-chain light showcase on three nodes with the workflow-chain L1 anchor |
| `showcase-projection-off` | Every node started with the devnet history projection disabled |
| `showcase-run-all`, `showcase-verify` | All scenarios, then cross-node tip/root agreement and finality certificates |
| `showcase-restart`, `showcase-persisted-tips` | Graceful full restart; tips never regress and roots at recorded heights are unchanged |
| `distribution-config-unchanged` | The showcase never edits the distribution's `config/` |

It stops the showcase on exit. It deletes the working directory only after a
full pass without `--keep`; on failure the directory, step logs, and node logs
under `showcase-data/smoke/cluster/node*/node.log` stay for diagnosis. Use
`--skip-showcase` for the gates only, `--skip-run-all` for a faster showcase.

## Known platform facts

- Yano's JVM ZIP bundles DuckDB extensions for `linux_amd64` only, and the
  Yano `%devnet` profile enables the DuckLake history projection
  (bloxbean/yano#137). Yano X ships `config/application-devnet.yml` and
  `examples/showcase/yano/config/application-devnet.yml` turning it off. If a
  node fails with `failed to initialise the DuckLake projection schema`, that
  overlay is missing or overridden. Do not paper over it with
  `_DEVNET_YANO_HISTORY_PROJECTION_ENABLED=false`; the script unsets it.
- The node rejects a symlinked plugins directory. `showcase.sh` exports
  `YANO_PLUGINS_DIRECTORY` with the real path.
- `cardano-history-chain` records nothing until the L1 epoch-stability depth
  passes (devnet epoch 2, about three minutes after genesis). Its plugin route
  returns 404 until then; `run cardano-history` waits up to 300 s for it.
- `finalDistributionRuntimeAcceptance` and `finalDistributionStockOutcomeAcceptance`
  are not part of `build` or CI; this skill is where they run.
- Not covered: the Docker `evidence` profile, the `eutxo` profile, preprod, and
  a remote `yano-x-deploy apply`.

## Report

List every step with PASS/FAIL and duration, the ZIP name and size, the Yano
version from `yano-x-distribution-v1.json`, the OS/architecture, and anything
skipped. For a failure, quote the first relevant `ERROR` from the step log or
node log rather than rerunning until it passes.

---
name: grok-sync
description: >
  Sync the vendored Grok Build tree (third_party/grok-build) forward to a newer
  upstream release: measure the pin against upstream HEAD, inventory the
  changelog delta, build a per-item adoption matrix, re-derive the DeepSeek
  overlay with a three-way merge, regenerate the carried patches, run the
  gates, and write the ledger + user-facing changelist. Use when the user asks
  to sync/refresh/update vendored grok-build, port upstream Grok improvements,
  or catch dsb up to a newer Grok Build version.
---

# Grok Build sync (vendored tree, ADR-0008)

The product base is open-source **Grok Build**, vendored at
`third_party/grok-build/` and pinned by `SOURCE_REV` ([ADR-0008](../../docs/adr/0008-grok-build-base.md)).
Upstream ships near-daily; dsb falls behind whenever nobody syncs. This skill is
the procedure so a future session inherits it instead of re-deriving it.

**Companions:** [grok-sync-runbook](../../docs/contributing/grok-sync-runbook.md)
(normative steps) · [GROK_VENDOR](../../docs/architecture/GROK_VENDOR.md)
(layout, patch re-apply) · [UPSTREAM_SYNC_LEDGER](../../docs/product/UPSTREAM_SYNC_LEDGER.md)
(what past syncs decided).

---

## 0. Ground truth first — never assume

```sh
./scripts/grok-sync-inventory.sh          # pin vs upstream HEAD, delta, clusters
```

The script prints: the pin and the upstream commit it corresponds to, upstream
HEAD and its version, the release delta, file/crate counts, and the changelog
bullet inventory for the covered range. **Read it before planning anything.**

Two facts to establish that the script cannot know:

| Question | How |
|---|---|
| Does the current tree actually equal the pinned upstream commit? | `git archive <commit> \| tar -x -C /tmp/base` then `diff -rq /tmp/base third_party/grok-build -x target -x .git` — a small diff is the dsb overlay, a large one means the tree drifted |
| Do the carried patches still apply? | `./scripts/apply-grok-build-patches.sh --check` |

If the overlay is large (hundreds of files) or the patches conflict, **`rsync
--delete` + re-apply is not the method** — go to §3 (three-way merge).

---

## 1. Decide what is worth taking — per item, with a reason

Read **every** changelog in the covered range. They live at
`crates/codegen/xai-grok-shell/changelogs/<version>.md` in both trees.

Classify every bullet into exactly one bucket, and write the reason:

| Verdict | Means |
|---|---|
| **Take** | Behavior dsb should have; carry it and test it |
| **Hold** | Right idea, wrong time — record why and what would change the answer |
| **Reject** | Against dsb's identity ([NON_GOALS](../../docs/product/NON_GOALS.md), [HARNESS_PHILOSOPHY](../../docs/architecture/HARNESS_PHILOSOPHY.md)) — say which |
| **N/A** | xAI-hosted surface with no dsb meaning (see §2) |

**"Upstream has it" is not a reason.** The source ladder is L1 Deep Code > L2
Reasonix > L3 Grok, and **L3 never overrides L1/L2**
([SOURCES](../../docs/product/SOURCES.md)). An upstream change that breaks
snippet-edit semantics, prefix-cache stability, or permission honesty is a
**Reject** no matter how nice it looks.

### Breaking changes get a verdict too

Upstream arbitrary breaking changes can hit dsb specs. Read them explicitly and
record the impact — a removed tool parameter, a changed default, a moved file.

---

## 2. The xAI-hosted surface is not a port target

Upstream contains **zero** DeepSeek code. These clusters are frequently
`N/A` — check each rather than blanket-rejecting:

telemetry/consent · xAI login, OIDC, team policy · billing and credit upsell ·
`grok` self-update channels · voice · video generation and ZDR · image
generation · Desktop / Computer-Hub daemon · `x.ai/*` RPC method names ·
`GROK_*` env vars and `~/.grok` paths.

But be careful: many of those releases also carry **general** work in the same
file (a TUI fix, a session fix). Split the bullet, not the release.

---

## 3. The merge — three-way, never `rsync --delete`

When the overlay is non-trivial, a raw tree swap loses dsb's work and the patch
series will not re-apply (upstream moves the same files).

| Role | Tree |
|---|---|
| merge base | the **old** upstream commit the vendored tree was pinned to |
| ours | current `third_party/grok-build/` (base + dsb overlay) |
| theirs | the **new** upstream commit |

Do it in a scratch repo outside the product tree (e.g.
`~/Personal/Projects/OpenSources/_upstream/`), then copy the merged result in.
Reconcile each conflict by asking: *is this change upstream's to take, or dsb's
to keep?* A conflict where both sides changed the same line is a design
decision, not a mechanical one.

Then carry the overlay explicitly — these are dsb's, not upstream's:

- **DeepSeek sampling** — `prompt_cache_hit_tokens` → `cached_read_tokens`
- **DeepSeek status extension** — `x.ai/deepseek/status` (balance/session usage)
- **Status line rendering** — the DeepSeek balance row
- **Prompt identity** — no hardcoded third-party vendor claim in the agent prompt, and its encrypted copy must be regenerated
- **Seeded product changelog** — the version-transition cleanup must not delete `$GROK_HOME/CHANGELOG.md`
- **DeepSeek themes** — `deepseeknight*.rs` plus their registration in the picker, cache, appearance, and syntax tables
- **Path A cache signal / spec-10 assembly** helpers
- **Invocation branding** — quit/relaunch hints print `dsb`, not `grok`

Regenerate the patch series from the new base; the previous series is
superseded. Update `docs/architecture/GROK_VENDOR.md`'s tables to match.

---

## 4. Prove it — gates, then build

```sh
./scripts/build-grok-pager.sh check      # vendor tree compiles
./scripts/test-owner-bar.sh              # must stay green
./scripts/check-path-a-linkage.sh
./scripts/test-heart-regression.sh
./scripts/test-grok-vendor-offline.sh
./scripts/test-product-offline.sh
./scripts/check-semver.sh
```

**Vendored Grok builds are serial across all worktrees** — a cold build is
30–60+ minutes and parallel builds starve each other. Check
`pgrep -fl 'grok-build/target'` before starting, and say so in the PR if you
waited.

Report honestly: a gate that did not run is not green. Paste the commands and
their real outcome.

---

## 5. Record it — three artifacts, no more

| Artifact | For |
|---|---|
| `docs/product/UPSTREAM_SYNC_LEDGER.md` | **The next session.** Pin before → after, versions covered, verdict counts, the decisions that need context, gates, PR number. |
| `docs/product/CHANGELIST_<VER>.md` | **The owner.** Plain-language answer to "what is better now, and why" — grouped by what the reader feels (faster / fixed / new / changed), with a not-taken section. One file. |
| `docs/research/grok-build.md` | **The record.** The sync's adoption matrix, version by version. |

Then, if the sync justifies a major, follow the
[release skill](../release/SKILL.md). The MAJOR gate reads
`docs/product/versions/README.md` — add the row **before** releasing.

---

## Anti-patterns

| Don't | Why |
|---|---|
| `rsync -a --delete` over a non-trivial overlay | Silently drops dsb's work; the patch series will not re-apply |
| Porting a `GROK_*`/`~/.grok`/xAI-hosted item "for completeness" | Ships another vendor's surface inside this product |
| Taking an L3 change that breaks L1/L2 contracts | Violates the source ladder; the harness regresses |
| Claiming gates green without running them | The whole point of the ledger is that it is auditable |
| A changelist written from the upstream changelog | The owner needs dsb's story, not upstream's release notes |
| Skipping the ledger because the PR body says it | The PR is transient; the ledger is what the next session reads |

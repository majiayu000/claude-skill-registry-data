---
name: project-update
version: 1
consumed_by: project-update agent
description: Operating manual for the project-update runtime agent that owns all writes to docs/domain/ after project-explorer bootstraps it.
---

## Purpose

`project-update` owns every write to `docs/domain/` after `project-explorer` bootstraps it. The enhancer reloads `project-explorer`'s `SKILL.md` verbatim at runtime to inherit the output schema, frontmatter contract, BC discovery heuristics, and exclusion globs — there is no fork and no copy. This file owns the enhancer-specific behaviour that is not in the sibling skill: the hybrid diff strategy, the path -> BC classifier, the fenced human-edit zone splice rule, the byte-perfect idempotency contract with its canonical exit message, the auto-write of newly discovered BCs, the removed-BC log-only rule, and the load-bearing `## Known coupling` and `## Migration caveat` sections.

## Inputs

- `[path]` (optional) — local filesystem path to the target repository. Defaults to the current working directory when omitted. Local path only; no remote URLs, no clone, no git checkout side-effect. Same semantics as `/project:explore`.

The enhancer is fully agent-driven: every change — including a newly discovered bounded context — is written automatically with no approval gate and no interactive pause. There is no `--bypass-approval` flag (it was removed when the gate was removed); the only thing that stops a run is the `## Pre-flight refuse condition` below.

## Pre-flight refuse condition

Before any skill load or diff step runs, the agent checks `docs/domain/` of the current working directory (not `[path]`). If `docs/domain/` is missing or empty, the agent refuses with the literal message:

```
docs/domain/ is missing or empty. Run /project:explore first to bootstrap, then /project:update to update.
```

and exits before the skill-load step. This mirrors `project-explorer`'s refusal-points-at-sibling pattern in reverse: `project-explorer` refuses when `docs/domain/` is non-empty (pointing at this enhancer); this enhancer refuses when `docs/domain/` is missing/empty (pointing back at `project-explorer`).

## Tree-presence advisories

Four-way tree-presence matrix:

| Narrative present? | Domain present? | Behaviour |
|---|---|---|
| yes | yes | Both passes run. Each pass auto-writes its tree with no approval gate. Happy path. |
| yes | no | Domain-absent advisory fires. Narrative pass runs. Domain pass is skipped. |
| no | yes | Narrative-absent advisory fires. Narrative pass is skipped. Domain pass runs. |
| no | no | Refused at the command layer (no agent spawn). See `## Pre-flight refuse condition` for the agent-level contract; the command-level refusal is the authoritative one. |

- **Domain-absent advisory (narrative present, domain missing).** When `docs/narrative/` is present and `docs/domain/` is missing, the agent prints the literal advisory:

  ```
  Note: docs/domain/ not present. Run /project:explore first to enable schema enhancement.
  ```

  The agent then proceeds with the narrative pass only and skips the domain pass.
- **Narrative-absent advisory (narrative missing, domain present).** When `docs/narrative/` is missing and `docs/domain/` is present, the agent prints the literal advisory:

  ```
  Note: docs/narrative/ not present. Run /project:overview first to enable narrative-informed domain regeneration.
  ```

  The agent then skips the narrative pass and proceeds with the domain pass only.
- **Both-missing refusal.** Refused at the command layer (the `/project:update` command) before the agent is spawned. The agent never runs in this case. The literal refusal message is locked at the command layer.

## Dual-pass orchestration

- **Fixed order.** Narrative pass first, then domain pass. No `--reverse-order`, no `--narrative-only`, no `--domain-only` flag exists in v1.
- **Rationale.** The domain pass reads `docs/narrative/<bc>/walkthrough.md` as soft input via the `project-explorer` skill `## Soft input: docs/narrative/`. If the narrative tree is stale at domain-pass time, the soft input is stale and the operator would need a second invocation to converge. Fixed order makes the single invocation converge — and because the narrative pass auto-writes (no gate), the domain pass always reads a fresh narrative within the same invocation.
- **Both passes always run.** Neither pass can halt or escalate; both auto-write their tree. Whichever trees are present (per `## Tree-presence advisories`) are both refreshed in one invocation with no interactive pause.
- **Shared run-summary.** Per `## Idempotency exit`, the non-zero-write exit summary aggregates per-pass counts (files written, new BCs created, removed BCs logged) into a single block. The zero-write exit message (`No changes detected. 0 files written.`) is emitted **once per run** when both passes together wrote zero files (cross-pass aggregation rule, mirroring the narrative-side rule in the `project-overview` skill `## Idempotency exit (narrative)`).

## Operating procedure

Numbered steps 0-12. The agent must execute these in order. Later sections in this skill fill in the precise contract per step.

0. **Run-mode dispatch.** Read the four-way tree-presence matrix from `## Tree-presence advisories`. Plan the run order: narrative pass first (when `docs/narrative/` is present), domain pass second (when `docs/domain/` is present). Both passes auto-write (see `## Inputs`). When both trees are missing, the command-layer refusal already fired before this agent was spawned — see `## Pre-flight refuse condition` for the agent-level documentation of that contract.
1. **Resolve target.** Resolve `[path]` (defaults to the current working directory). Locate the current working directory's `docs/domain/`. If `docs/domain/` is missing or empty, refuse with the message pointing the user at `/project:explore` (see `## Pre-flight refuse condition` above) — bootstrap first, then enhance.
2. **Skill load (all three).** The subagent loads its own the `project-update` skill first, then reloads the `project-overview` skill second, then reloads the `project-explorer` skill third — verbatim, in that locked order. All three are treated as authoritative for the run; enhancer-specific behaviour (diff strategy, fence handling, idempotency exit message) lives in this skill, narrative-side output schema + frontmatter + diff-aware update mode live in the project-overview skill, and domain-side output schema + frontmatter + BC heuristics live in the project-explorer skill. See `## Skill reload contract` for the explicit reload targets.
3. **Diff strategy selection (hybrid).** Read `last_generated_sha` from frontmatter (sample one file under `docs/domain/`; all frontmatter is treated as consistent — every file's `last_generated_sha` advances together on a successful run).
   - **Git fast path** fires when `[path]` is a git working tree AND `last_generated_sha` is present AND that SHA is reachable from HEAD. Command: `git diff --name-only <last_generated_sha>..HEAD`. Apply the exclusion globs verbatim. Map each surviving file to its owning BC via `project-explorer`'s namespace/folder heuristic.
   - **Full-walk fallback** fires when any git-fast-path precondition fails (no git, no `last_generated_sha`, or SHA unreachable — including the first enhancer run against a `project-explorer`-bootstrapped tree where `last_generated_sha` is absent). Walks every BC under `[path]` per `project-explorer`'s skill and compares every regenerated file in memory against the on-disk file.

   See `## Hybrid diff strategy` for the full contract and the auditability lines surfaced in run output.
4. **Classify changed files.** Bucket the diff output into exactly one of three classes per `## Path -> BC classifier`: (a) `BC-affecting` — survives the exclusion globs AND lives under a known BC folder/namespace; (b) `infra — no BC impact` — excluded by globs OR survives globs but is not under any known BC; (c) `new-namespace` — survives exclusion globs AND lives under a folder/namespace not mapped to any existing BC.
5. **New-BC discovery (auto-write).** If bucket (c) is non-empty, print the candidate new-BC list (rationale + aggregates detected, formatted per `project-explorer`'s `### Candidate report format`) for the audit trail, then proceed directly to create the new `<bounded-context>/` folder(s). See `## New-BC discovery (auto-write)`.
6. **Removed-BC logging.** For each existing `<bounded-context>/` folder under `docs/domain/` whose namespace is no longer present in source, append a bullet to `context-map.md`'s `## Skipped candidates` H2 section as `<bc-name>: namespace no longer present`. **Never delete** the folder. **Never delete** any file inside the folder. See `## Removed-BC logging`.
7. **Per-BC SHA pre-check (domain).** For each BC in the `BC-affecting` bucket from step 4, run the per-BC SHA pre-check per `## Per-BC SHA pre-check`: resolve the BC's source paths via the reverse mapping (the `project-explorer` skill `## BC candidate surfacing` `### Reverse mapping (BC -> source paths)`), gather **every** file's `last_generated_sha` under `docs/domain/<bc>/`, apply the conservative any-missing / any-unreachable / unresolvable-path-set -> no-skip gates, else diff `git -C <path> diff <base>..HEAD -- <bc-source-paths>` where `<base> = min(reachable)` (oldest-wins). Empty diff -> **SKIP** the BC (no regen, no fence-splice, no byte-compare, no write; emit the verbose skip line under verbose/debug mode per `### Skip log line (verbose/debug only)`); non-empty diff -> fall through to step 8 (regen). New-namespace, removed-BC, and the repo-wide roll-ups (`context-map.md`, `glossary.md`) are out of scope and unaffected.
8. **Regeneration in memory.** For every BC in bucket (a) **that the step 7 pre-check did not SKIP** and every candidate in bucket (c) (all auto-created — no approval subset), regenerate the per-file content per `project-explorer`'s `## Output schema` `### Per-file content contract`, scoped to that BC's slice of the tree. Generation is in-memory only at this point — no writes.
9. **Fenced human-edit zone preservation.** For each regenerated file, read the on-disk file. If it contains a `<!-- human:begin --> ... <!-- human:end -->` block, splice the on-disk fenced block (the lines from `<!-- human:begin -->` through `<!-- human:end -->` inclusive, content verbatim) into the regenerated content at the same anchor position; everything outside the fence is replaced with the regenerated agent-owned content. If no fence exists on disk, the regenerated content fully replaces the on-disk content (see `## Migration caveat`).
10. **Byte-perfect compare + selective write.** For each candidate file: serialize the regenerated content (post-fence-splice) and compare to the on-disk bytes. **Write only when bytes differ.** On a real content change, refresh the frontmatter per `## Frontmatter refresh rules` (`generated_at` to a new ISO-8601 UTC second-precision `Z`-suffixed timestamp, `skill_version` to the current `project-explorer` skill version, `branch_name` to the current arg or bare `null`, preserve `source_repo`, stamp `last_generated_sha` to current HEAD on the git path). Files whose content has not changed retain their prior `generated_at` even after a successful run.
11. **`last_generated_sha` advancement.** Regardless of whether any content changed, stamp `last_generated_sha` on every file the enhancer touches in step 10. On the full-walk fallback path with no git, `last_generated_sha` is omitted from frontmatter (next run will re-fallback). On the git path, `last_generated_sha` advances to current HEAD on every successful run, so subsequent runs take the fast path.
12. **Idempotency exit.** If zero files were written in step 10, the agent exits with the literal message `No changes detected. 0 files written.` and **no further output**. Otherwise the agent prints a per-run summary (files written count, new BCs created count, removed BCs logged count) and exits. See `## Idempotency exit`.

## Skill reload contract

The enhancer agent reloads three skills in this order, at the start of every run:

1. the `project-update` skill — this file. Loaded first.
2. the `project-overview` skill — loaded **second**. Treated as authoritative for the narrative-side output schema, frontmatter contract, fence convention, and the seven new `## Diff-aware update mode` sub-sections.
3. the `project-explorer` skill — loaded **third**. Treated as authoritative for everything both passes regenerate against (BC heuristics, exclusion globs, candidate report format, auto-write contract).

The enhancer treats `project-explorer`'s skill as authoritative for:

- The output schema — `project-explorer`'s `## Output schema` (file tree, per-file content contract, small-repo fallback variant, write order, hallucination guard).
- The frontmatter contract — `project-explorer`'s `## Frontmatter contract` (the four-field YAML block — `source_repo`, `branch_name`, `generated_at`, `skill_version`). This feature adds `last_generated_sha` on top per `## Frontmatter refresh rules` below.
- BC discovery heuristics — `project-explorer`'s `## BC candidate surfacing` (including `### Grouping rule`, which is the namespace -> folder mapping the classifier reuses).
- Exclusion globs — the eight globs enumerated under `project-explorer`'s `### Small-repo fallback detection`. Reused verbatim by `### Exclusion globs (verbatim)` below.
- The candidate report format — `project-explorer`'s `### Candidate report format`. Reused verbatim to print the new-BC audit trail before auto-writing (no gate).

The enhancer treats `project-overview`'s skill as authoritative for the narrative-side equivalents of the same contracts: the narrative output schema, the narrative frontmatter contract, the fence convention used inside `docs/narrative/` files, and the six cite-by-reference sub-sections under `## Diff-aware update mode` (`## Hybrid diff strategy (narrative)`, `## Path -> BC classifier (narrative)`, `## Fenced human-edit zone splice (narrative)`, `## Removed-BC logging (narrative)`, `## Byte-compare + selective write + frontmatter refresh (narrative)`, and `## Idempotency exit (narrative)`). The narrative pass uses these sections; the domain pass does not.

This skill owns the enhancer-specific behaviour the sibling skills do not cover: the hybrid diff strategy, the path -> BC classifier with its three classification buckets, the fenced human-edit zone splice rule, `last_generated_sha` semantics, the removed-BC log-only rule, the byte-perfect idempotency contract with its canonical exit message, and the two load-bearing prose sections `## Known coupling` and `## Migration caveat`.

## Hybrid diff strategy

The sample-one global fast path below decides *whether* there is any change to act on at all; on top of it, the per-BC `## Per-BC SHA pre-check` sits in front of regen and decides, per individual BC, whether that BC's source slice moved — skipping the BCs whose slice is unchanged.

### Git fast path

Fires when **all three** preconditions hold, evaluated in this order:

1. `[path]` is a git working tree — detected by `git -C <path> rev-parse --git-dir` returning success.
2. `last_generated_sha` is present in the frontmatter of at least one file under `docs/domain/`. The enhancer samples **one** file (any file; the contract is that all frontmatter advances together on every successful run per `## Frontmatter refresh rules`, so sampling one file is sufficient).
3. `last_generated_sha` is reachable from HEAD — detected by `git -C <path> merge-base --is-ancestor <last_generated_sha> HEAD` returning success.

On success, the enhancer runs:

```
git -C <path> diff --name-only <last_generated_sha>..HEAD
```

then applies the exclusion globs from `### Exclusion globs (verbatim)` (globs first, terminal), then maps each surviving path to its owning BC via `### Namespace -> BC mapping`.

The chosen path is surfaced in run output as the literal line for auditability:

```
Diff strategy: git fast path (<last_generated_sha>..HEAD)
```

### Full-walk fallback

Fires when **any** of the three git-fast-path preconditions fails. The three triggers, evaluated in the same order as the git-fast-path preconditions:

1. `[path]` is not a git working tree (`git -C <path> rev-parse --git-dir` returns failure).
2. `last_generated_sha` is absent from the sampled `docs/domain/` frontmatter (legacy `project-explorer`-bootstrapped tree on first enhancer run, or a manually wiped field).
3. `last_generated_sha` is present in the sampled frontmatter but **unreachable** from HEAD — for example because the branch was force-pushed and the commit was orphaned, the branch was rebased and the commit was rewritten away, or the commit was deleted and is no longer in any ref-reachable history. Detected by `git -C <path> merge-base --is-ancestor <last_generated_sha> HEAD` returning failure.

On any trigger, the enhancer walks every BC under `[path]` per `project-explorer`'s skill and compares every regenerated file in memory against the on-disk file. The full-walk path is a strict superset of the git fast path's correctness — both produce byte-perfect idempotency; the git fast path is purely a speedup.

**Reason-token short-circuit (load-bearing).** When more than one precondition would fail at once, the enhancer evaluates the three preconditions in the order listed above and selects the reason token from the **first** failing precondition. First failure wins:

1. git-tree-check fails -> reason token is `missing-git` (the SHA-present check and reachability check are not run).
2. SHA-present-check fails -> reason token is `missing-sha` (the reachability check is not run; there is no SHA to test).
3. reachability-check fails -> reason token is `unreachable-sha`.

No compound tokens are ever emitted. The three reason tokens are mutually exclusive in any single run.

The chosen path is surfaced in run output as the literal line for auditability:

```
Diff strategy: full-walk fallback (reason: <missing-git | missing-sha | unreachable-sha>)
```

### last_generated_sha tolerate-missing

When `last_generated_sha` is absent from frontmatter — the case on the first enhancer run against any `project-explorer`-bootstrapped tree, because `last_generated_sha` is a new field introduced by this feature — the enhancer falls through to the full-walk fallback per the contract above with reason token `missing-sha`.

**First-run stamp lifecycle (git path).** On its first successful run against a git working tree, the enhancer stamps `last_generated_sha = <current HEAD SHA>` on every file it touches in step 10 (the selective writer). The literal current HEAD SHA — resolved at the start of the run — is written into the frontmatter of every touched file. Subsequent runs against the same repo read that stamped SHA from the sampled frontmatter, satisfy all three git-fast-path preconditions (the SHA is present and reachable from the new HEAD), and take the git fast path. This is a **one-time** legacy-repo cost per pre-enhancer-bootstrapped repo.

**No-git path lifecycle.** When trigger 1 of `### Full-walk fallback` fires (the directory is not a git working tree), the enhancer cannot resolve a HEAD SHA. The selective writer omits the `last_generated_sha` field from emitted frontmatter entirely. Every subsequent run against the same non-git directory takes the full-walk fallback again with reason `missing-git`. There is no transition to the fast path on the no-git path.

**Force-push / rebase recovery lifecycle.** When reason `unreachable-sha` fires, the selective writer re-stamps `last_generated_sha = <current HEAD SHA>` on every file it touches. The next run satisfies all three preconditions (the new SHA is reachable from the new HEAD) and takes the fast path again. Recovery is automatic; no user intervention required.

The enhancer never refuses on missing-SHA or unreachable-SHA; it never back-patches the sibling `project-explorer` skill to emit `last_generated_sha` on bootstrap.

## Path -> BC classifier

### Exclusion globs (verbatim)

The eight globs the classifier applies, verbatim:

- `**/bin/**`
- `**/obj/**`
- `**/node_modules/**`
- `**/dist/**`
- `**/*Tests/**`
- `**/*.Tests/**`
- `**/*.generated.*`
- `**/*Designer.cs`

These are the same globs `project-explorer`'s `SKILL.md` applies under `### Small-repo fallback detection`. Reused here to keep a single source of truth for "what counts as first-class source." See the `project-explorer` skill `### Small-repo fallback detection` for the original list and its rationale; this enhancer never forks or duplicates the list — any future edit must be made there and audited here per `## Known coupling`.

**Ordering rule (load-bearing).** The classifier evaluates every path from the diff output in this exact order:

1. **Globs first.** Apply the eight exclusion globs verbatim. Every path matching any of the eight globs is bucketed as `infra — no BC impact` and skipped immediately.
2. **Namespace lookup second.** Only the paths that survive step 1 are evaluated against `### Namespace -> BC mapping` to decide between `BC-affecting` and `new-namespace`.

A path excluded by the globs in step 1 is **never** re-evaluated against the namespace mapping, the new-namespace detector, or any other rule. Glob exclusion is terminal.

**Terminal-exclusion clarifier.** This terminal rule holds even when the excluded path lives under a brand-new folder/namespace that is not yet mapped to any `<bounded-context>/` under `docs/domain/`. Example: a changed `**/SomeNewBc/bin/Foo.dll` matches `**/bin/**` on the first comparison, is bucketed `infra — no BC impact`, and the new-namespace detector is **never** invoked for it. The candidate `SomeNewBc` does NOT surface in the `new-namespace (candidates: ...)` parenthetical. Glob exclusion always wins over new-namespace detection.

### Namespace -> BC mapping

The classifier reuses `project-explorer`'s `## BC candidate surfacing` `### Grouping rule` verbatim. Namespace tokens and folder paths trace from the candidate report straight into the classifier — no taxonomy invented here. See the `project-explorer` skill `## BC candidate surfacing` `### Grouping rule`. Not duplicated here by design; cite-by-reference per `## Known coupling`.

**Bucket-assignment rule (applied only to paths that survived the glob filter — glob-excluded paths were already terminated upstream per `### Exclusion globs (verbatim)`):**

- A surviving path is bucketed as `BC-affecting` **iff** its folder/namespace matches an existing `<bounded-context>/` folder under `docs/domain/` (reverse lookup via `project-explorer`'s `### Grouping rule`: existing BC folder names trace back to namespace tokens and folder paths).
- A surviving path is bucketed as `new-namespace` **iff** its folder/namespace does not match any existing BC and the path lives under a recognizable namespace/folder structure that would itself qualify as a BC candidate per `project-explorer`'s `### Grouping rule`.
- A surviving path that lives under no recognizable namespace/folder structure (e.g., a top-level file with no BC-relevant context such as a repo-root `README.md`) is bucketed as `infra — no BC impact`.

### Classification buckets

Every file in the diff output is bucketed into exactly one of three classes:

| Bucket | Definition | Action |
|---|---|---|
| `BC-affecting` | Survives the exclusion globs AND lives under a known BC folder/namespace. | Add the owning BC to the re-walk set. |
| `infra — no BC impact` | Excluded by the globs OR survives the globs but is not under any known BC. | No re-walk; logged for auditability. |
| `new-namespace` | Survives the exclusion globs AND lives under a folder/namespace not mapped to any existing BC. | Auto-creates the new BC after printing the candidate report (see `## New-BC discovery (auto-write)`). |

**Per-bucket count summary (auditability).** Immediately after the `Diff strategy:` audit line and before any subsequent step output, the agent prints the literal line:

```
Classified: <N> BC-affecting (BCs: <comma-separated, alphabetical>), <M> infra, <P> new-namespace (candidates: <comma-separated, alphabetical>)
```

Rules:

- The three nouns `BC-affecting`, `infra`, `new-namespace` are invariant — never singular/plural variants regardless of count.
- The BC list and the candidate list are sorted alphabetically (case-insensitive).
- The `infra` noun carries **no** parenthetical.
- An empty parenthetical (zero BCs in the `BC-affecting` parenthetical or zero candidates in the `new-namespace` parenthetical) renders as `(none)`.
- The count integer is always present even when zero (e.g., `0 BC-affecting (BCs: (none))`).
- The line is printed exactly once per run, immediately after the `Diff strategy:` line, before any subsequent step output.

## Per-BC SHA pre-check

The per-BC SHA pre-check is a per-BC speedup that sits **in front of** regen, on top of the global sample-one fast path in `## Hybrid diff strategy`. For each BC that survives classification as `BC-affecting`, it decides whether that BC's source slice actually moved since the BC's pages were last written; when the slice is unchanged it **SKIPs** the whole BC (no regen, no fence-splice, no byte-compare, no write). It never under-skips: every ambiguous or incomplete input degrades to over-regen, never to a silent stale-wiki SKIP.

**Scope.** The pre-check runs **only** over the `BC-affecting` bucket produced by `## Path -> BC classifier` `### Classification buckets`. New-namespace candidates, removed-BC folders, and the repo-wide roll-ups (`docs/domain/context-map.md` and `docs/domain/glossary.md`) are explicitly **out of scope** and continue on today's full path unchanged: a new namespace has no prior `last_generated_sha` and no prior folder to diff; a removed BC is log-only and regenerates nothing anyway; the roll-ups are cross-BC aggregates that must regen whenever any BC changes, so there is no per-BC slice to skip. Byte-compare remains the slow-path safety net for every BC that falls through.

**Per-BC source-path resolution.** For each BC in the `BC-affecting` bucket, the pre-check resolves that BC's source paths — the `<bc-source-paths>` argument list — via the reverse mapping. See the `project-explorer` skill `## BC candidate surfacing` `### Reverse mapping (BC -> source paths)` for the full inversion contract; the pre-check cites it **by exact heading name** and does **not** fork or restate the inversion mechanics. This mirrors the cite-by-reference pattern `### Namespace -> BC mapping` already uses for the forward `### Grouping rule`.

**Per-BC SHA gather.** For each BC, gather the `last_generated_sha` from **every** file in that BC's output folder under `docs/domain/<bc>/` (the per-file frontmatter field stamped per `## Frontmatter refresh rules`). This is a **per-BC** gather across all of the BC's files — explicitly **not** the sample-one approach the global `### Git fast path` uses (precondition 2 there samples one file under `docs/domain/` because the global contract is that all frontmatter advances together; the pre-check cannot assume that within a single BC, because a partial prior run can leave divergent per-file SHAs inside one BC).

**Conservative gate 1 — any-missing / any-unreachable -> no skip.** If **any** file in the BC has a **missing** `last_generated_sha` (legacy bootstrap, manually wiped) **OR** an **unreachable** one (force-push / rebase orphaned the commit), the pre-check does **NOT** skip — the BC falls through to today's regen path. Reachability is evaluated with the **same** test the hybrid strategy already uses: `git -C <path> merge-base --is-ancestor <sha> HEAD` (success = reachable). See `## Hybrid diff strategy` `### Git fast path` precondition 3 and `### Full-walk fallback` for the reachability semantics; the pre-check invents **no** new reachability test.

**Conservative gate 2 — empty/unresolvable path set -> no skip.** If the inversion returned an **empty or unresolvable** `<bc-source-paths>` set (the folder name does not trace back to any current namespace/folder; the BC was renamed/merged/split since bootstrap; the name is ambiguously spread across folders; or the `module-map` fallback token), the pre-check does **NOT** skip — full regen. This is the same conservative posture a missing SHA forces in gate 1. See the empty/unresolvable rule in the `project-explorer` skill `## BC candidate surfacing` `### Reverse mapping (BC -> source paths)`: ambiguity degrades to over-regen, never to under-skip; a false SKIP is impossible by construction.

**Base selection — oldest-wins.** When every file's `last_generated_sha` is **present and reachable**, the base is `min(reachable SHAs)` across the BC's files — **oldest-wins**, the most pessimistic reachable point. Rationale (one line): a partial prior run leaves divergent per-file SHAs within one BC, and oldest-wins anchors the diff window to the most-stale file so any source change since the earliest write across the BC's files is caught — sample-one or newest-wins could pick a freshly-advanced SHA and miss a change the stale-SHA files would have caught.

**Decision.** Run:

```
git -C <path> diff <base>..HEAD -- <bc-source-paths>
```

- **Empty diff -> SKIP the whole BC.** No regen, no fence-splice, no byte-compare, no write for any file in that BC. Under verbose/debug mode, emit the verbose skip line defined in `### Skip log line (verbose/debug only)` (the literal `SKIP bc=<name> pass=domain (sha unchanged)`); a normal run stays silent.
- **Non-empty diff -> fall through** to today's exact behaviour: the BC proceeds to `## Regenerate -> fence-splice -> byte-compare -> selective write` unchanged, where byte-compare remains the correctness net.

**Per-pass independence (forward pointer).** The domain pass owns this decision **independently** of the narrative pass. In a single run the domain pass MAY SKIP a BC the narrative pass regenerates, or REGENERATE a BC the narrative pass skips — the two trees carry independent `last_generated_sha` values and independent source slices. This is expected and correct, not a bug. See the `project-overview` skill `## Per-BC SHA pre-check (narrative)` for the narrative-side mirror.

### Skip log line (verbose/debug only)

**The literal, defined exactly once.** The canonical skip-line literal — the single source of truth for the SKIP signal — is, byte-for-byte:

```
SKIP bc=<name> pass=<domain|narrative> (sha unchanged)
```

`<name>` is the on-disk `<bounded-context>/` folder name, case-preserved verbatim from the filesystem (the **same** identifier the removed-BC log and the `Classified:` line use). The parameter `<domain|narrative>` selects the pass: the domain pass emits `pass=domain`; the narrative pass (the `project-overview` skill `## Per-BC SHA pre-check (narrative)`) **reuses** this same literal with `pass=narrative` by **cite-referencing this definition by exact heading name** — it does **not** redefine the literal. This parameterized fenced block is the only place the literal is defined.

**Emission condition.** The line is emitted **only** under a non-default verbose/debug mode, once per **SKIPPED** BC, at the moment the pre-check decides to skip. A **normal run** (verbose/debug off) emits **nothing** for a skipped BC — it stays silent.

**The three locked surfaces are unchanged.** The verbose skip line sits **outside** the three locked output surfaces and changes none of them:

- `No changes detected. 0 files written.` — the zero-write idempotency exit (`## Idempotency exit`) still fires byte-for-byte on a zero-write run, with no further output.
- `Diff strategy:` — the audit line (`## Hybrid diff strategy`) is unchanged.
- `Classified:` — the audit line (`## Path -> BC classifier` `### Classification buckets`) is unchanged.

No new normal-run output line is introduced; on a zero-write run the only line remains the locked idempotency exit.

**Not a stable contract.** The skip line is a **test-fixture aid** — explicitly non-default (verbose/debug only) and deliberately **not** a stable public/automation contract. This parallels how `Diff strategy:` / `Classified:` **are** the stable always-on audit lines and this line deliberately is **not** (promoting it to an always-on audit line would add output to the zero-write run and break the silent-on-zero-write contract).

## New-BC discovery (auto-write)

When a new bounded context is discovered, the enhancer prints the candidate report for the audit trail and then creates the new `<bounded-context>/` folder(s) automatically (see `## Inputs`). The enhancer reuses only `project-explorer`'s `### Candidate report format` (for the printed audit trail); it no longer reuses any approval-gate contract (that contract was removed from the sibling skill).

### Trigger

Fires when the `new-namespace` bucket from `### Classification buckets` is non-empty. If the `new-namespace` bucket is empty, no candidate report is printed and the run proceeds to step 6 of `## Operating procedure` (removed-BC logging).

### Reused contract (verbatim)

The enhancer prints the candidate report using the `project-explorer` skill `### Candidate report format` verbatim — same numbered `### BC candidates` list with per-candidate nested bullets for `Rationale` (folders / namespaces that contributed) and `Aggregates detected` (aggregate root + `file:line` citation as an inline-code span), same `### Fallback flag` line, same `### Conflicts detected` subsection (rendered as `(none)` when empty per the sibling skill). The report is informational only — the agent does not prompt and does not wait.

The `### Fallback flag` line on an enhancer run is **always** the literal token `false`. The small-repo fallback is a `project-explorer` bootstrap-only signal; it never fires from the enhancer.

### Auto-write behaviour

After printing the candidate report, the enhancer immediately creates new `<bounded-context>/` folders under `docs/domain/` for **every** candidate in the `new-namespace` bucket (see `## Inputs`). The new folders are populated by the writer (`## Regenerate -> fence-splice -> byte-compare -> selective write` and its `### Selective write + frontmatter refresh` subsection) per the `project-explorer` skill `## Output schema` `### Per-file content contract` and `### Write order`. Every newly written file under a freshly created `<bounded-context>/` folder carries all five frontmatter fields stamped **fresh** per `## Frontmatter refresh rules`: `source_repo` (preserved from `<path>`), `branch_name` (current invocation's arg or bare `null`), `generated_at` (new ISO-8601 UTC second-precision `Z`-suffixed timestamp), `skill_version` (current integer of the `project-explorer` skill's `version` field), and `last_generated_sha` (current HEAD SHA on the git path; omitted on the full-walk fallback path with no git).

## Removed-BC logging

For each existing `<bounded-context>/` folder under `docs/domain/` whose namespace is no longer present in source, the enhancer appends one bullet to `context-map.md`'s `## Skipped candidates` H2 section in the form:

```
<bc-name>: namespace no longer present
```

Rules:

- **Never delete** the `<bounded-context>/` folder.
- **Never delete** any file inside the `<bounded-context>/` folder (including the fenced human-edit zones inside those files).
- **Never touch** any file inside a removed-BC folder beyond the single `context-map.md` append described above.
- The removed-BC log entry is the only on-disk change the enhancer makes for a disappeared namespace.

### Detection

For each `<bounded-context>/` folder currently present under `docs/domain/`, the enhancer performs a **reverse lookup** against the `project-explorer` skill `## BC candidate surfacing` `### Grouping rule`: take the on-disk folder name and check whether a corresponding namespace token or folder path still exists under `<path>` per the sibling skill's namespace -> BC mapping. A BC is "removed" iff its mapping returns no source match — that is, neither a namespace token nor a folder path in source maps to the on-disk `<bounded-context>/` folder name. The detection is independent of the diff strategy chosen (git fast path or full-walk fallback); both paths walk every `<bounded-context>/` folder under `docs/domain/` and apply the reverse lookup.

### Log target and bullet format

The append target is the existing `## Skipped candidates` H2 section in `docs/domain/context-map.md` (the `project-explorer` writer emits this section on every bootstrap; the enhancer never creates the section from scratch — only appends to it). The bullet format is exactly:

```
- <bc-name>: namespace no longer present
```

**Folder-name vs namespace-token disambiguation.** The `<bc-name>` is the on-disk `<bounded-context>/` folder name (e.g., `legacy` for `docs/domain/legacy/`) — **NOT** the source namespace token (e.g., `Acme.Legacy`). The folder name is the user-visible identifier the human reader recognises from their `docs/domain/` tree, and the namespace token may have already disappeared from source by the time this code runs. The folder name's case is preserved verbatim from the filesystem.

### Idempotency of the log

Before appending, the enhancer reads the body of the `## Skipped candidates` section and checks for an existing matching line. The duplicate check is:

- **Exact-line match** — the full literal line including the leading `- ` (hyphen + space) bullet prefix. A line `* legacy: namespace no longer present` (different bullet character) or `legacy: namespace no longer present` (missing prefix) does **not** match and would not suppress an append.
- **Case-sensitive** — `- Legacy: namespace no longer present` does **not** match `- legacy: namespace no longer present`.
- **Scoped** to the body between the `## Skipped candidates` H2 line and the next H2 line (or end-of-file when `## Skipped candidates` is the final H2). A matching line elsewhere in `context-map.md` (e.g., inside `## Conflicts detected`) does **not** count as a duplicate.

If a matching line already exists in that scope, the enhancer does **not** append. This keeps the section monotonically growing without re-appending on every run. Combined with the byte-compare contract in `### Selective write + frontmatter refresh`, a duplicate-suppressed append produces zero on-disk writes, and the canonical idempotency exit message applies when no other writes occurred in the run.

### `(none)` placeholder handling

If the body of the `## Skipped candidates` section is the literal single line `(none)` (the `project-explorer` placeholder when bootstrap found no skips), the enhancer replaces that one line **in place** with the first bullet on first append. The replacement applies only to a single line whose trimmed body is exactly `(none)`. Specifically:

- The `## Skipped candidates` heading line is preserved verbatim.
- Any blank line(s) between the heading and the `(none)` line are preserved.
- The single line `(none)` is **replaced** by the first bullet (`- <bc-name>: namespace no longer present`).
- Any blank line(s) between the (replaced) line and the next H2 / end-of-file are preserved.

Subsequent appends (on later runs that discover additional removed BCs) add bullets normally underneath the first one; the `(none)` placeholder rule does **not** re-fire because the body is no longer the literal single line `(none)`.

### Strict no-delete contract

The enhancer's contract for a removed namespace is **log-only**, reaffirmed here:

- The enhancer **never** deletes the `<bounded-context>/` folder for a removed BC. The folder stays on disk verbatim.
- The enhancer **never** deletes any file inside the `<bounded-context>/` folder (including the human-edited files inside `<!-- human:begin --> ... <!-- human:end -->` fences).
- The enhancer **never** rewrites any file inside the `<bounded-context>/` folder. No regeneration, no fence-splice, no frontmatter refresh — the folder is frozen until the human author decides to remove it manually. Every file under the removed BC's folder retains its prior `generated_at` value and prior `last_generated_sha` value byte-for-byte.
- The only on-disk write triggered by a removed BC is the single bullet append to `docs/domain/context-map.md` under `## Skipped candidates`, and that append is itself subject to the byte-compare contract in `### Selective write + frontmatter refresh` (no write if the bullet already exists per the idempotency-of-log rule above).

### Reason token (locked)

The reason text is exactly `namespace no longer present` — verbatim. No variants. Future reason tokens (for example `renamed to <new-bc>`, archival reasons, or merge-target reasons) are deferred and **never** appear in v1. v1's bullet template is a single locked string with one placeholder (`<bc-name>`).

## Regenerate -> fence-splice -> byte-compare -> selective write

### Regenerate in memory

For every BC in the `BC-affecting` bucket plus every candidate in the `new-namespace` bucket (all auto-created — no approval subset), the enhancer regenerates the per-file content per `project-explorer`'s `## Output schema` `### Per-file content contract`, scoped to that BC's slice of the tree. Generation is **in-memory only** at this point — no writes have happened yet.

**Scope.** Regenerate per-file content for every BC in the `BC-affecting` bucket plus every candidate in the `new-namespace` bucket. BCs in the `infra — no BC impact` bucket are **not** re-walked. BCs that were detected as **removed** (no longer in source) are excluded from the regenerate set per `## Removed-BC logging`'s strict no-delete contract — the enhancer logs them and moves on; their `<bounded-context>/` folder is frozen.

**Output contract.** Each regenerated file's content is produced per the `project-explorer` skill `## Output schema` `### Per-file content contract`, scoped to that BC. The exact set of files regenerated per BC is:

- `<bounded-context>/glossary.md`
- `<bounded-context>/aggregates/<aggregate>.md` (one file per detected aggregate root)
- `<bounded-context>/events.md`
- `<bounded-context>/commands.md`
- `<bounded-context>/repositories.md`
- `<bounded-context>/services.md`

In addition, the two repo-wide roll-up files `docs/domain/context-map.md` and `docs/domain/glossary.md` are regenerated whenever **any** BC changes, because their content is a roll-up across all BCs.

**In-memory only.** No file under `docs/domain/` is written at this stage. The output is held in memory as a `{ path -> regenerated-content-string }` mapping keyed by absolute file path. Writes happen exclusively in `### Selective write + frontmatter refresh` after `### Fenced human-edit zone splice` and `### Byte-compare` have run.

### Fenced human-edit zone splice

**Fence markers.** The exact byte sequences are `<!-- human:begin -->` and `<!-- human:end -->`, each on their own line. Leading and trailing whitespace on the marker line itself is tolerated (the scanner trims marker-line whitespace before matching). Content between the markers — including any blank lines, leading whitespace, and trailing whitespace — is preserved byte-for-byte.

**Per-file algorithm.** For each `(path, regenerated-content)` pair produced by `### Regenerate in memory`:

1. Read the on-disk file at `path`. If the file is missing (new file — e.g., a file under a freshly auto-created new BC), **skip the splice**; the regenerated content is used as-is and proceeds straight to `### Byte-compare`.
2. Scan the on-disk content for the fence markers. **Zero fences** -> regenerated content used as-is (see `## Migration caveat`). **One fence pair** -> proceed to step 3 to splice. **Multiple fence pairs** -> loop step 3 for each pair, preserving all of them at their respective anchor positions.
3. For each fence pair found on-disk: locate the same anchor position in the regenerated content (the anchor is the line index of `<!-- human:begin -->` within the agent-owned content; if the regenerated content has no matching anchor at the expected position, splice the fenced block at the same line-index offset measured from the top of the regenerated content). Replace the lines from `<!-- human:begin -->` through `<!-- human:end -->` (inclusive) in the regenerated content with the verbatim on-disk fenced block (markers + content + any whitespace within, byte-for-byte).
4. The post-splice content string is the byte-compare candidate consumed by `### Byte-compare`.

Anchor drift across regenerations is a known limitation; users who care about exact placement should keep fenced blocks adjacent to stable headings (e.g., immediately after a `## ` H2).

If no fence exists on disk, the regenerated content fully replaces the on-disk content (see `## Migration caveat`).

**Never-touch invariant.** The agent's only obligation inside a fence is to splice the on-disk bytes verbatim into the regenerated content. Specifically:

- The agent **never** modifies content between `<!-- human:begin -->` and `<!-- human:end -->` — preserved byte-for-byte from the on-disk file.
- The agent **never** modifies the fence marker lines themselves (`<!-- human:begin -->` / `<!-- human:end -->`) — no normalisation, no whitespace rewrite, no re-emission.
- The agent's only obligation inside the fence is to splice the on-disk bytes verbatim into the regenerated content. Nothing else.

### Byte-compare

The enhancer serializes the post-fence-splice regenerated content to a string, reads the on-disk file as bytes, and compares. **The enhancer writes only when bytes differ.** A successful run against an unchanged file produces zero on-disk change for that file.

**Comparison input.** The post-splice regenerated content string (serialized to UTF-8 bytes) vs the on-disk file bytes (read as UTF-8). Both sides are raw byte sequences at the moment of comparison.

**Byte-perfect.** Comparison is byte-exact. There is **no normalization**: trailing newline differences, BOM differences, and CRLF-vs-LF line-ending differences are all **real differences** that trigger a write. The enhancer does not normalize line endings on read or on write — the regenerated content emits LF only (matching `project-explorer`'s output convention; see the `project-explorer` skill `## Output schema`).

**Skip-write decision.** If the byte sequences are identical, the file is **skipped**: no write to disk, no frontmatter refresh, no `last_generated_sha` stamp on this file. Its prior `generated_at` and prior `last_generated_sha` are preserved byte-for-byte. Skip-write is the per-file foundation of the zero-write run that triggers `## Idempotency exit`'s canonical exit message.

### Selective write + frontmatter refresh

**Write trigger.** A file is written **iff** `### Byte-compare` returned "differ" for that file. Files whose bytes are byte-identical post-splice are not touched and retain their prior `generated_at` and prior `last_generated_sha` values verbatim.

**Frontmatter refresh order (4 numbered steps).** On a write:

1. **Strip** the existing frontmatter block from the regenerated content string (the regenerated content carries a placeholder frontmatter generated by the `project-explorer` writer; it is discarded before the new frontmatter is constructed).
2. **Construct** the new frontmatter block per `## Frontmatter refresh rules` below. All five fields are written in this order:
   - `source_repo` — **preserved** verbatim from the on-disk file's frontmatter (never refreshed by the enhancer).
   - `branch_name` — refreshed to the current invocation's branch arg, or bare YAML `null` token when omitted. `branch_name` follows `project-explorer`'s frontmatter contract: bare YAML `null` token when the invocation omits the arg, NOT the quoted string `"null"`. See the `project-explorer` skill `## Frontmatter contract`.
   - `generated_at` — refreshed to the current ISO-8601 UTC second-precision `Z`-suffixed timestamp.
   - `skill_version` — refreshed to the current integer of the `project-explorer` skill's `version` field (the enhancer stamps the **project-explorer** skill version, not its own — output-schema versioning belongs to the schema owner).
   - `last_generated_sha` — stamped per the per-file rule below: on the git path (any of git-fast / `missing-sha` / `unreachable-sha`) the field is stamped to the current HEAD SHA; on the no-git full-walk fallback path the field is **omitted entirely**.
3. **Prepend** the new frontmatter block as the **first content** of the file — before any heading — per the `project-explorer` skill `## Frontmatter contract`.
4. **Write** the final string to disk at `path` as UTF-8 with LF line endings and no BOM. Write order across files follows the `project-explorer` skill `## Output schema` `### Write order`.

**`last_generated_sha` advancement (per-file, git path).** On the git path (fast or fallback), `last_generated_sha` is stamped to the **current HEAD SHA** on every file the enhancer writes in this step. Files the enhancer did **not** write retain their prior `last_generated_sha` value byte-for-byte. After a successful run where N out of M files changed, the N written files carry the new HEAD SHA and the M-N unwritten files carry their prior SHA — **both** are valid sampling points for the next run's `### Git fast path` precondition check (the sampled SHA only needs to be reachable from the new HEAD).

**`last_generated_sha` omission (per-file, no-git only).** On the full-walk fallback path **with no git** (reason token `missing-git`), `last_generated_sha` is **omitted from the frontmatter** of every written file — the YAML key does not appear in the block at all. The next run re-evaluates the precondition, fails the git-tree check again, and re-falls-back. Critical distinction: reasons `missing-sha` and `unreachable-sha` are **git-available** paths, so the writer **still stamps HEAD** on those paths (recovery is automatic; the next run takes the fast path). Only `missing-git` causes the writer to **omit the field entirely** — and only on every subsequent no-git run.

**New-file case.** For files in a freshly auto-created new BC, there is no on-disk content to read; the splice and byte-compare steps are skipped (per `### Fenced human-edit zone splice` step 1's missing-file rule and `### Byte-compare`'s differ-by-default semantics). The write proceeds with a fresh frontmatter — all five fields stamped per the git-path rule above (`source_repo` derived from `<path>`; `branch_name` per the current invocation arg or bare `null`; `generated_at` fresh; `skill_version` fresh; `last_generated_sha` to HEAD on the git path, omitted on the no-git path) — and the regenerated content as-is (no fence to splice on a new file).

## Frontmatter refresh rules

| Field | Refresh trigger | Preserved when | Notes |
|---|---|---|---|
| `source_repo` | Never refreshed by the enhancer. | Always preserved. | Locked by `project-explorer`'s frontmatter contract. |
| `branch_name` | Refreshed on real-content change to the current invocation's branch arg (or bare `null` when omitted). | Untouched files retain prior value. | Same YAML scalar / bare `null` rules as `project-explorer`'s frontmatter contract. |
| `generated_at` | Refreshed (new ISO-8601 UTC second-precision `Z`-suffixed timestamp) only when the post-fence-splice bytes differ from on-disk bytes for **this specific file**. | Untouched files retain prior value even after a successful enhancer run. | Content-change semantics. |
| `skill_version` | Refreshed on real-content change to the current integer of the `project-explorer` skill's `version` field. | Untouched files retain prior value. | The enhancer stamps the **project-explorer** skill version, not its own — output schema versioning belongs to the schema owner. |
| `last_generated_sha` | Stamped on every file the enhancer **touches** (writes) in the selective-write step on the git fast path; advances to current HEAD on every successful run regardless of content change. | Untouched files retain prior value. Files on the full-walk fallback path with no git omit the field entirely. | Run-tracker semantics. New field introduced by this feature. Tolerate-missing on first run (see `### last_generated_sha tolerate-missing`). |

## Idempotency exit

**Zero-write exit.** When `### Selective write + frontmatter refresh` wrote **zero** files across the entire run — including zero new BCs created and zero removed-BC bullets appended to `## Skipped candidates` — the agent prints **exactly one line**:

```
No changes detected. 0 files written.
```

and exits. **No summary, no banner, no `Diff strategy:` line, no `Classified:` line, no additional output.** Just the one literal line, then exit. This is the canonical signal downstream automation (git status checks, CI lint, future post-merge hooks) can grep for unambiguously.

**Non-zero-write exit.** When at least one write occurred (any combination of regenerated BC files, new-BC files, or a removed-BC bullet append to `context-map.md`), the agent prints this fenced summary and exits:

```
<N> files written.
<P> new BCs created: <comma-separated names or "(none)">.
<R> removed BCs logged: <comma-separated names or "(none)">.
Diff strategy: <git fast path (<sha>..HEAD) | full-walk fallback (reason: <token>)>
```

where `<N>`, `<P>`, `<R>` are integer counts; the two name lists render as `(none)` when their count is zero; and the `Diff strategy:` line is the same audit line surfaced earlier in the run by `## Hybrid diff strategy`.

**No-partial-exit rule.** If any step in the pipeline (regenerate, splice, compare, write) errors, the agent surfaces the error and exits non-zero. Partial state on disk is acceptable — the next run's byte-compare reconverges automatically. The canonical zero-write message above is emitted **only** on a successful zero-write run, never on a partial-failure run.

## Known coupling

This skill is load-bearing because the enhancer reloads two sibling skills verbatim at runtime — the `project-explorer` skill (domain-pass authority) and the `project-overview` skill `## Diff-aware update mode` (narrative-pass authority); an edit to any of the contracts cited below in either sibling silently changes enhancer behaviour. The human editor who touches either sibling skill is obligated to run a paired enhancer audit against this file. No `skill_version` pin or `compatible_with` check exists or is planned — this section itself is the trip-wire.

The enhancer reloads, by name, the following contracts (five from the `project-explorer` skill, plus the `## Diff-aware update mode` block from the `project-overview` skill):

- `## Output schema` (including `### Files written`, `### Per-file content contract`, `### Small-repo fallback variant`, `### Write order`, `### Hallucination guard`) — the full file tree + per-file content rules + small-repo fallback variant + write order + hallucination guard the enhancer regenerates against.
- `## Frontmatter contract` — the four-field YAML block (`source_repo`, `branch_name`, `generated_at`, `skill_version`); this feature adds `last_generated_sha` on top per `## Frontmatter refresh rules` above.
- `## BC candidate surfacing` `### Grouping rule` — the namespace -> BC mapping the path classifier reuses (see `### Namespace -> BC mapping` above).
- `## BC candidate surfacing` `### Reverse mapping (BC -> source paths)` — the BC-name -> source-path inversion the per-BC pre-check consumes (see `## Per-BC SHA pre-check` above). It is the **strict inverse** of `### Grouping rule` and **shares its single source of truth** — the same namespace/folder correspondence read backwards, never a forked copy. An edit to `### Grouping rule` silently changes the inverted path set and therefore the `<bc-source-paths>` fed to `git diff` and the pre-check's SKIP/regen decision; re-audit and re-derive the reverse mapping on any `### Grouping rule` edit.
- `### Small-repo fallback detection` — the eight exclusion globs enumerated there are the verbatim source for `### Exclusion globs (verbatim)` above.
- `### Candidate report format` — reused verbatim by `## New-BC discovery (auto-write)` for the printed candidate-report audit trail. (The sibling's former `### APPROVE gate contract` was removed when the gate was removed; the enhancer no longer reuses any approval-gate contract.)
- the `project-overview` skill `## Diff-aware update mode` (and its six cite-by-reference sub-sections: `## Hybrid diff strategy (narrative)`, `## Path -> BC classifier (narrative)`, `## Fenced human-edit zone splice (narrative)`, `## Removed-BC logging (narrative)`, `## Byte-compare + selective write + frontmatter refresh (narrative)`, `## Idempotency exit (narrative)`) — reloaded by the enhancer agent as the second of three skills per `## Skill reload contract` above. The narrative pass uses these sections; the domain pass does not.

Any edit to those sections in either the `project-explorer` skill or the `project-overview` skill `## Diff-aware update mode` silently changes enhancer behaviour. The editor is obligated to re-read this skill end-to-end before considering the edit complete.

## Migration caveat

> **At the moment regen fires, the original contract still holds.** When the enhancer regenerates a BC's files (no human-edit fences present, or a fence-splice run), any pre-existing human edit made **outside** a `<!-- human:begin --> ... <!-- human:end -->` fence is overwritten by the regenerated content, exactly as before. To preserve an edit across that overwrite, wrap it in `<!-- human:begin --> ... <!-- human:end -->` fences before invoking `/project:update`.
>
> **The shift the per-BC pre-check introduces.** With the `## Per-BC SHA pre-check` in place, regen no longer fires for a BC whose source slice is unchanged — the pre-check SKIPs that BC before any regen, fence-splice, or write happens. As a consequence, an outside-fence human edit now **survives until that BC's source slice changes**: it persists across every run in which the BC's source slice is unchanged, and is overwritten the moment that slice changes and regen fires — exactly the same overwrite as before, just deferred to the next source change.
>
> **The durable-across-source-change invariant is unchanged.** Fences (`<!-- human:begin --> ... <!-- human:end -->`) remain the **only** way to make an edit durable **across a source change**. An outside-fence edit gains a reprieve only while its owning BC's source slice is unchanged; once that slice moves, regen fires and the unfenced edit is gone. Do not read the pre-check as making outside-fence edits durable in general — it does not.
>
> **This is a deliberate, accepted contract shift, not a regression.** The pre-check physically narrows *when* regen (and therefore overwrite) happens; the wording above states that observable behaviour truthfully rather than leaving the old always-overwrite-on-every-run description in place.

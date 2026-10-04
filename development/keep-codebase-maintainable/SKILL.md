---
name: keep-codebase-maintainable
description: "Use when cleaning a codebase, not shipping features."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cleanup, maintainability, refactor, prune, hygiene, conventions]
    related_skills: [codebase-design, codebase-cleanup, code-review]
---

# Keep a Codebase Maintainable

A maintainability job is **not** a feature with extra polish. The deliverable is a smaller, truer tree: unused gone, twins collapsed, names honest, docs matching code, diff containing only the ask.

Mined from Cooper's OMP Hindsight bank (how he actually prompts coding agents). Source instances: `references/instances.md` (copy also at `/var/lib/hermes/workspace/omp-maintainability-asks.md`).

**Core principle:** Keep the requested scope. Follow
[codebase-design](../codebase-design/SKILL.md) for shared readability rules and
examples. Remove abstractions that only forward calls; retain ones that hide
complexity, enforce invariants, or translate an external interface.

## When to Use

Load this when the user (or the task) sounds like any of:

- clean up / tidy / prune / hygiene / leftover / dead / unused
- simplify / trim the diff / surgical / no tangents
- audit, repair, and reorganize
- rename / consolidate / disentangle / one package / short names
- "don't add", "no new services", "stop coding", "out of scope"
- comment the why / docs are stale / fix AGENTS.md
- keep it maintainable / reduce maintenance / cohesion

**Don't use for:** implementing a requested feature, fixing a failing behavior, or a post-feature pass over *your own just-written diff* — use the repository's review guidance for that pass.

If the user mixes "add X and also clean Y", split the commits. This skill owns Y.

## Standing Rules

These override default "helpful agent" instincts.

1. **Deletion test.** A symbol/file/package/dep/flag/scope dies if it has zero real importers **and** is not a public contract (exported API, framework peer, Helm value a live app still declares). Grep the name. Then grep the old name. `knip` / `ts-prune` / `depcheck` are hints, not proof — they flag framework peers and dynamic imports.
2. **Don't recreate the dead.** Removing a stale git declaration is the fix. Syncing / applying / resurrecting the resource to "clear Missing" is the bug. Same for reserved-for-later knobs: clean cutover, not a tombstone comment.
3. **One owner, one name.** Twins drift (two schedulers, `menu` vs `x`, `ManualCommitStep` leftover after a unify). After a collapse, grep the retired name and delete the twin.
4. **Native over custom.** Use the library when it supplies the needed capability. Keep a local adapter when it owns decoding, errors, resource lifetime, or a simpler complete operation; delete wrappers that only rename a call.
5. **Short honest names.** Name the owning capability, such as `@repo/billing`; avoid a shared `utils` dumping ground. Within an owner, use familiar role directories. Public docs use the canonical surface (`x`), never the legacy alias.
6. **Package = unit of cohesion.** Expose complete operations through explicit public entries; keep implementation under `src/`, grouped by owner then role. Keep related SQL and helpers with their adapter. Tests exercise observable behavior through the interface and follow repository placement conventions.
7. **Surgical diff.** Stage specific paths. Never `git add -A`. One concern per commit. Revert unauthorized extras without arguing. "Cleanup approved" is not "land on main."
8. **Live user instruction beats advisory AGENTS.md.** Binders about commits/pushes still apply to *remote* mutations. They do not authorize you to spawn extra agents or expand scope.
9. **Comment the why.** Design intent, invariants, edge-case rationale. No `// increment counter`. Stale docs are a contract bug — update or delete.
10. **Stop means stop.** "Stop all coding." "Don't modify production auto/flash." Honor scope locks immediately.

## Process

### 1. Name the job

Write one sentence: *what gets smaller or truer, and what is out of scope.*

Done when: the sentence has no feature in it. If it does, this is the wrong skill.

### 2. Inventory before you touch

Build a list of candidates. Do not delete yet.

```
path:symbol  → why it looks dead  → consumers found (grep)  → contract?  → action
```

Search, in this order:

- unused files / exports / deps / flags / Slack scopes / Helm leftovers
- leftover twins from an incomplete unify (old name still present)
- stale comments, READMEs, AGENTS.md pins that contradict lockfiles
- commands / aliases still advertising a retired surface
- "reserved for later" knobs and unused error variants
- temp artifacts (`/tmp/*`, worktrees, stale tags, merged branches)

Done when: every candidate has a grep result (including "zero hits") and a contract verdict. Live-consumer check is mandatory for anything that can take production down (bindings, PVCs, Hyperdrive, DNS, secrets).

### 3. Apply in risk order

| Tier | Examples | Action |
|---|---|---|
| **SAFE** | unused import, leftover `/tmp`, commented-out block, duplicate config section from a failed edit | Delete now. |
| **CAREFUL** | unused file with no importers, dep with no app import, rename to the short name, collapse a twin helper | Delete/rename, then run the targeted test/lint for that package. |
| **RISKY** | anything with a live binding, public export, Helm/Argo resource, secret, peer dependency, "zero knip hits" | Verify live consumers. If any exist, stop and say so. Never delete by name-group. |

Do not add speculative flags, services, or abstractions. A cleanup may introduce
a local helper or coherent module when it demonstrably improves understanding
within the authorized scope. Extraction must hide complexity or enable useful
reuse. Retain configured line limits; document targeted exceptions instead of
splitting into forwarding files to satisfy a number.

Done when: every SAFE/CAREFUL item is applied or explicitly skipped with a reason, and no RISKY item was applied without a live-consumer check.

### 4. Keep the contract true

In the same change-set, only if they are now false:

- AGENTS.md / README claims (versions, who posts reviews, where creds live)
- comments that describe a path you just deleted
- public command catalogue / `x` menu entries that point at removed scripts
- snapshot / fixture leftovers that still use the old marker

Do not write new design docs unless the user asked. Do not start a planning loop — mechanical refactors skip brainstorming.

Done when: a stranger grepping the old name finds either nothing, or a one-line pointer to the new name.

### 5. Land narrowly

- Diff contains only the inventory items you accepted.
- Separate commit from any unrelated WIP. Use the dirty-worktree recipe if needed: backup diff → revert unrelated hunks → verify `git diff` → commit → re-apply WIP.
- Do not push / Sync / deploy unless the user asked for that land path.
- If you drifted (extra files, extra agents, extra scope): revert first, then report.

Done when: `git diff` against the starting point is explainable line-by-line from the inventory, and the project's targeted check for touched packages is green (or the baseline already failed the same way).

## What "clean" looks like here

Recurring shapes from real asks — match these, don't invent new ones:

- **Catalogue audit** — remove broken commands, prefix the rest, one grouping scheme.
- **Diff diet** — unnecessary indirection removed; behavior coverage preserved.
  Net line count is evidence about size, not a quality target.
- **Replace a custom stack** with the library hook (bash-preexec, Polar SDK, vendor client).
- **Collapse to one owner** (one SessionHost, one scheduler, one SDK repo, two-repo end state).
- **Delete the reserved knob** rather than keep it "for the bounded API later."
- **Uniform over decorative** when the extra style costs code or bugs.
- **Heuristic over flag** when the flag would become a recovery bug.
- **Vendor references as plain files** so the next agent can follow AGENTS.md without extra setup.

## Common Pitfalls

1. **Deleting by name group.** Hyperdrive configs deleted by production name took down live Workers. Always resolve the live ID / binding first.
2. **Syncing to clear Missing.** Recreates the unused claim. Edit git; hard-refresh if you only need status.
3. **Trusting unused-export tools.** Grep. Check framework peers. Check string-dynamic imports.
4. **Hearing "cleanup OK" as "push to main."** Land path is a separate ask.
5. **Leaving the twin.** Incremental unifies leave `ManualCommitStep`. Grep the old name after.
6. **Keeping reserved dead API.** It becomes a lying classifier. Cut over.
7. **AGENTS.md theater.** Don't spawn work the user didn't ask for because a blocker advisory exists. Do still refuse remote mutations without authority.
8. **Planning the cleanup.** Discovery → do the inventory → apply. No redesign of an approved shape.
9. **Commenting the deletion.** If the code is gone, the comment goes too — unless it records a load-bearing *why we don't do X*.
10. **Mixing feature and cleanup in one commit.** Split.

## Verification Checklist

- [ ] One-sentence job has no feature in it
- [ ] Inventory table exists; every delete has a grep + contract verdict
- [ ] Live bindings checked for RISKY items
- [ ] Old name greps clean (or points at the new name)
- [ ] Every retained or new abstraction hides complexity or enables useful reuse
- [ ] Configured line limits remain, with any targeted exception documented
- [ ] Tests verify behavior and required completion/error/cleanup contracts
- [ ] Diff is explainable from the inventory; no unauthorized files
- [ ] Targeted tests/lint for touched packages ran; only pre-existing failures remain
- [ ] Stale docs / AGENTS.md / menu entries that the change falsified were updated or deleted
- [ ] Did not push / Sync / deploy unless asked

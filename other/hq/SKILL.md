---
name: hq
description: HQ — the multi-repo command center. Turn a single utterance ("For project Acme, do X") into governance-aware action across every repo on this device. Resolves a project name (fuzzily) to a real repo via the registry ladder (Rebalance project_registry → XYZ install registry → Git Pulse PDDA registry → filesystem), reports its governance state as a project card, lands the request on that repo's own PDDA rails (issue → 1-INBOX capture → ROADMAP parking), and prepares dispatch (queue a lane / gated fire). Trigger when the user says "/hq", "HQ status of <project>", "which repo is <project>", "for project X do Y", "resolve <project>", "park/queue/fire this for <project>", "what marathons are running now" / "read all marathons in realtime", or asks for a cross-repo project card / capability tier. Read paths are safe; write paths (park/queue) PREVIEW by default and act only with --create; fire never drives the harness itself. Tracks GH-128.
---

# /hq — multi-repo command center

HQ is the front door for one-utterance, multi-repo tasking: resolve a project name to a real repo,
report its governance state, land the request on that repo's own PDDA rails, and prepare dispatch.
**Read paths are safe; every write path previews by default.**

## Preconditions — install once, then locate (never hardcode a path)

`/hq` is **user-level**: it works from a session opened in *any* repo, not just the harness clone.
Two anchors make that true, both self-locating and free of any hardcoded machine path.

**Install (once per clone).** Claude Code only scans `~/.claude/skills/`, not the repo's top-level
`skills/`. Symlink this skill in so a session can load it at all:

```bash
bash skills/2-daily/hq/install.sh   # symlinks this clone's skills/2-daily/hq into ~/.claude/skills/ (idempotent)
```

**Locate (every invocation).** HQ is centralized — there is one `utils/hq/hq.sh`, shipping in the
harness clone beside this skill. The bundled locator [`find-hq.sh`](find-hq.sh) resolves it relative
to its own installed location (symlink-safe), so it works from any CWD. Run this first, then call
`$HQ_SH`:

```bash
# Find the bundled locator — anchored on $HOME or the CWD, never an absolute machine path:
for L in "${XYZ_HARNESS:+$XYZ_HARNESS/skills/2-daily/hq/find-hq.sh}" \
         "$HOME/.claude/skills/hq/find-hq.sh" \
         "./.claude/skills/hq/find-hq.sh" \
         "$(git rev-parse --show-toplevel 2>/dev/null)/skills/2-daily/hq/find-hq.sh"; do
  [ -n "$L" ] && [ -x "$L" ] && break
done
[ -x "$L" ] || { echo "hq: locator not found — set XYZ_HARNESS to your xyz-3-agents-swarm clone"; exit 1; }

eval "$("$L" --env)"   # exports HQ_ROOT and HQ_SH (absolute path to hq.sh)
"$L" --check           # one-glance readiness: hq root, sqlite3, rebalance registry
```

After this, `$HQ_SH` is the absolute dispatcher path. **When standing in the harness repo you can
still call `bash utils/hq/hq.sh …` directly** — the examples below use that short form; substitute
`bash "$HQ_SH" …` when you're in another repo.

## What it does now

The skill drives `utils/hq/hq.sh` (or `$HQ_SH` from a foreign repo — see Preconditions):

- `hq.sh status <project|repo>` — the **project card**: resolved repo + path (with a fuzzy-match note
  if the name was loose), capability tier (A/B/C), Rebalance priority, PDDA mode + startup docs,
  active-doc count, open marathon plan, XYZ install/drift stamps.
- `hq.sh resolve <project|repo>` — machine-readable `KEY=value` resolution (adds `RESOLVED_VIA`
  exact|fuzzy; ambiguous names return rc=2 with `CANDIDATES`).
- `hq.sh registries` — introspection: what each registry knows and its coverage.
- `hq.sh next [--limit N]` — a **Rebalance-priority board**: projects ranked by `priority_tier`
  (1 highest) with each one's resolved HQ capability tier (A dispatch-eligible / B / C / unresolved),
  answering "what should I pick up next across my repos?" Read-only.
- `hq.sh park [--create] [--title T] <project> <request…>` — **issue-first intake** in the target
  repo (GH issue → `1-INBOX` capture → ROADMAP parking → dashboard regen if present → target
  `pdda.sh`). Previews unless `--create`. The capture doc renders the full PDDA skeleton (ratings,
  `non_goals`/`related`/`goal`, Key Concepts/Idea/Why/Phase 0 checklist) with TODO stubs by default;
  a synthesis front end (e.g. a future `/idea` skill) can fill the judgment-heavy fields in by
  exporting `HQ_PARK_WHY` / `HQ_PARK_KEY_CONCEPTS` / `HQ_PARK_NON_GOALS` / `HQ_PARK_RELATED` /
  `HQ_PARK_COMPLEXITY` / `HQ_PARK_RISK` / `HQ_PARK_EFFORT` / `HQ_PARK_PHASES` before calling
  `--create` — bare `hq.sh park` needs none of these (GH-164 Phase 1).
- `hq.sh queue [--create] [--gh-issue N] <project> <request…>` — append an **HQ-queued lane** to the
  target's newest Marathon Plan (non-destructive appendix). Previews unless `--create`.
- `hq.sh fire --gh-issue N [--risk 1-5] <project>` — **gated prepare-and-hand-off**: resolve + gate
  (Tier A, `risk < 3`) + emit the `swarm-preflight` command. HQ never drives the harness itself — the
  operator runs it and drives via the relay-xyz skill (GUIDING-PRINCIPLES §8).

## When the user invokes /hq

1. Name given → `bash utils/hq/hq.sh status "<name>"`; relay the card. On **UNRESOLVED**, show the
   find-recipe and ask; on **AMBIGUOUS**, show the candidates and ask which — never guess a path.
2. "For project X, do Y" → `hq.sh park "<X>" "<Y>"` (preview), show the exact issue/doc/roadmap, then
   `--create` on the operator's go (creating a GH issue is outward-facing — confirm first).
3. "queue it" / "fire it" → the corresponding verb. `fire` stops at the gated hand-off: relay the
   emitted command and hand to the relay-xyz skill; do not auto-drive a marathon.
4. "what can HQ see" / "list projects" → `hq.sh registries`.

## Resolution ladder (how a name becomes a repo)

1. **Rebalance `project_registry`** (`rebalance-OS/rebalance.db`) — the semantic catalog: human project
   NAME (`owner/repo`) → repo list + `priority_tier`/`value_level`. No local path.
2. **XYZ install registry** (`~/.config/xyz/registry.tsv`) — repo → **absolute path** + runnable/drift
   stamps. The path resolver; only covers XYZ-installed repos.
3. **Git Pulse PDDA registry** (`~/git-pulse-sync/pdda/registry-<device>.tsv`) — repo → PDDA `mode` +
   `startup_docs`, across all devices. No path.
4. **Filesystem `find`** — fallback when no registry knows the path.

Override any source for tests / non-default installs via `HQ_PDDA_REGISTRY_DIR`, `HQ_XYZ_REGISTRY`,
`HQ_REBALANCE_DB`, `HQ_SEARCH_ROOTS` (see `utils/hq/hq-lib.sh`).

## Live marathon status (what's running right now, deterministically)

"What marathons are running now" is a **different question** than `hq.sh status`/`registries` (which
report governance/capability state) or `utils/hq/marathon-scan.sh` (which reports **doc-level**
status — what a `MARATHON-PLAN-*.md`'s frontmatter claims — not live process state). Don't conflate
them: a repo can show "ready to fire" in a scan while a marathon is actively mid-turn in a sibling
worktree the doc scan never looks at.

**Once [GH-218](https://github.com/Claude-AI-Tools-Ventura-County/xyz-3-agents-swarm/issues/218)'s
`utils/hq/marathon-live.sh` exists** (check `ls utils/hq/marathon-live.sh` first), run it — it does
the four checks below across every `hq_known_repos` repo in one shot and emits repo + marathon/lane +
task + claimant + live-or-idle. **Until then, or to spot-check one repo by hand**, walk these in
order — all deterministic, local file/process reads, no server or daemon involved:

1. **Which repos exist at all** — `hq.sh registries` (or `hq_known_repos` directly), which already
   aggregates the XYZ install registry (`~/.config/xyz/registry.tsv`), Rebalance's project registry,
   and Git Pulse's PDDA registry. This is the full list of repos to check, not just the current one.
2. **What's claimed right now, per repo** — run `tick project` inside that repo (native `bin/tick`,
   or `$XYZ_PATH/bin/tick` for a vendored install — `$XYZ_PATH` comes from `hq_repo_resolve`) to
   regenerate `.tick/STATE.md`, then read its `## Claimed` section: `- <task-id> by <claimant>
   paths: [...]`. The task id already names the marathon/lane (e.g.
   `MARATHON-GH208-WORKTREE-ISOLATION-RACE-TURN`).
3. **Is it actually driving this instant, or just claimed-and-idle** — check for that repo's driver
   lock: `.git/relay-driver.lock` (native) or the vendored equivalent (see `marathon-drive.sh`'s own
   lock-path resolution, GH-149, for exactly how a linked-worktree/vendored install differs). Present
   = a `marathon-drive.sh`/`relay-drive.sh` process holds it right now.
4. **Corroborate with worktrees** — `git worktree list` (or `-C <repo>`) for a `marathon/*`-branch
   worktree with a commit or dirty status in roughly the last 30 minutes; a secondary signal, not
   ground truth on its own.
5. **Any live agent CLI process** — `ps aux | grep -E "marathon-drive|relay-drive.sh"` machine-wide,
   as a final cross-check (catches a driver running against a repo you didn't think to check).

## Capability tiers

- **Tier A** — PDDA + XYZ install → dispatch-eligible (Phase 3).
- **Tier B** — PDDA only → intake only, no dispatch.
- **Tier C** — bare repo → plain issue only; offer a PDDA install.

## Guardrails (inherited from GH-128)

- Read-only in this phase. Rebalance is always read-only (mirrors the #96 seam discipline).
- Never fabricate a repo path — an UNRESOLVED result is a question for the operator, not a guess.
- Later dispatch will be park-by-default with a hard `risk >= 3` gate; do not simulate it now.

---
name: release
description: Prepare a version release — bump version files, commit, and tag. Just run /release with no arguments.
---

# Release

## Project Config

- **Type:** generic (Claude Code plugin / marketplace)
- **Version file (single source of truth):**
  - `plugins/super-bootstrap/.claude-plugin/plugin.json` → `version` (`marketplace.json` carries no `version`)
- **Derived manifest mirror:**
  - `.claude-plugin/marketplace.json` → `plugins[0].description` (synced from `plugin.json` at release; direct edits get overwritten)
- **Platforms:** none (single artifact)
- **Main branch:** main

## Protocol

Code blocks below are POSIX `bash` — on a PowerShell-primary device, run them via the Bash tool; if porting to PowerShell, rewrite in its idiom and single-quote git's caret/brace revisions (`git rev-parse 'v1.2.3^{commit}'`).

### 1. Qualify

Run in parallel:
- `git status` — working tree must be clean. If dirty, stop: "Commit or stash changes first."
- `git branch --show-current` — must be on `main`. If not, warn and ask to continue.

### 1.5 Dispatch-shell pre-flight (warn, not block)

Scan `plugins/*/skills/*/SKILL.md` for bounded-judgment verbs — `classify`, `rank`, `scan`, `digest` (case-insensitive) — appearing in the skill's protocol/execution body. For each hit, check whether that skill dispatches a typed agent (a sibling `agents/<name>.md`, or a `subagent_type:` / "dispatch the ... agent" reference in the same file). A skill frontmatter alone can't pin a model — bounded judgment left inline runs unpinned, at the gateway's tier.

Skip skills whose row in `plugins/super-bootstrap/README.md` § "Inline vs Dispatch" documents an inline rationale — those are decided placements, not misses; warning on them every release trains the reader to ignore the check.

Bounded-judgment verb(s) found, no agent dispatch, **and** no documented inline rationale → warn, one line, don't block:

> ⚠ dispatch-shell check: {file} — bounded-judgment verb(s) ({verbs}) with no agent dispatch. Consider splitting into dispatch-shell + typed agent (see `skills/triage` + `agents/triage.md`).

List every matching file on one line if more than one hits. Never halts the release — this is a nudge surfaced in the release report, not a qualify gate.

### 2. Read state

```bash
# Latest version tag
git tag -l "v*" --sort=-v:refname | head -1

# Commits since last version tag
git log <latest-tag>..HEAD --oneline

# Check if current commit == tagged commit
git rev-parse HEAD
git rev-parse <latest-tag>^{commit}
```

### 3. Decide

**STATE A — No version tag exists:**
→ Go to "Full Release Flow"

**STATE D — Version tagged, different commit:**
→ Go to "Full Release Flow"

**STATE E — Version tagged, same commit:**
→ "v{latest} already released. Nothing to do."

### Full Release Flow

**Step 1 — Detect bump level** from conventional commits since last tag:

| Signal | Bump |
|---|---|
| `BREAKING CHANGE:` in body, or `!:` suffix | major |
| `feat:` | minor |
| `fix:`, `refactor:`, `chore:`, `docs:`, `test:`, `perf:` | patch |
| No conventional prefixes | patch (default) |

Use the highest level found.

**Step 2 — Propose:**

> Current: {current_version} → New: {new_version} (auto: N feat, N fix since v{current})
> OK?

Wait for confirmation. User can override.

**Step 3 — Bump version + sync manifest mirror:**

1. **Version** — edit `plugins/super-bootstrap/.claude-plugin/plugin.json`, change the top-level `"version"` field to the new version string. `marketplace.json` carries no `version` — do not add one.
2. **Description mirror** — copy `plugin.json` `description` verbatim into `.claude-plugin/marketplace.json` `plugins[0].description`. No-op if already identical.

Verify `plugin.json` shows the new version and the marketplace `plugins[0].description` matches `plugin.json` `description`.

**Step 4 — Generate release notes** from commits since last tag:

```
## What's New
- description (from feat: commits)

## Fixes
- description (from fix: commits)

## Other
- description (from everything else — refactor/chore/docs)
```

Omit empty sections. Show to user for approval.

**Step 5 — Commit and tag:**

```bash
git add plugins/super-bootstrap/.claude-plugin/plugin.json .claude-plugin/marketplace.json
git diff --cached --name-only   # must list exactly the version files — any other path is another session's staging: stop and surface it, never commit through it
git commit -m "chore: release v{version}"
git tag -a v{version} --cleanup=verbatim -m "<release notes>"
```

Use annotated tag. Pass message via HEREDOC. A path outside the version files in the readback → stop and surface it with the pick: unstage-and-continue (`git restore --staged <foreign>`, on the user's say-so) or abort.

**Step 6 — Report + offer push:**

> Release v{version} prepared (commit + tag v{version}).
> Push to publish? Runs `git push origin main --tags`. (y / skip)
>
> After push, Claude Code plugin manager will see the new version on next `/plugin update super-bootstrap` and refresh the cache.

Push only on explicit yes. Skip by default if the user is silent. Never force push.

## Rules

- Push only on explicit confirmation — offer after commit/tag, run `git push origin main --tags` on yes, never force, never unannounced.
- Working tree must be clean before proceeding — step 1 enforces this.
- The staged set is read back before `git commit` — the clean-tree gate holds at qualify time only; a path another session stages between qualify and commit stops the release for the user's pick (unstage / abort), never rides into it.
- Never delete or move existing tags.
- All tags are annotated (`git tag -a`) and written with `--cleanup=verbatim` — the default strips every line starting with `#`, which would delete the release-notes headings.
- Run `/release` with no arguments — the skill auto-detects state.
- `plugin.json` is the single version source — bump it only. Do not add a `version` field to `marketplace.json`.
- `marketplace.json` `plugins[0].description` is a derived mirror of `plugin.json` `description` — this skill syncs it at release; direct edits get overwritten.
- Dispatch-shell pre-flight (step 1.5) warns, never blocks — a hit is a nudge to split a skill, not a release-stopper.

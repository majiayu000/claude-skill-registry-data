---
name: graph
description: Rebuild the vault dependency graph (_graph.md) via the deterministic generator script. /graph forces a full rebuild; /graph last (run after every /sync) rebuilds only if the vault changed; /graph [N] is treated as last. The generator reads the vault and writes _graph.md directly, so the file never streams through a model response.
model: sonnet
effort: low
allowed-tools: Read Grep Glob Edit Write Bash(python3 * find * wc * date * grep * sed * rm * cat * sort * head * ls * printf *)
---

Rebuild `_graph.md` from vault state. Structural metadata only — no content files modified, no snapshots, no `_hot.md` changes.

**Engine**: `.claude/skills/graph/generate_graph.py` (deterministic). It reads every Thesis / Sector / Macro / Research file, validates wikilinks, and writes `_graph.md` directly. This replaced the legacy LLM-extraction + incremental-Edit procedure on 2026-06-04, after that approach hit a max-output-token wall: the full file is ~90 KB ≈ ~21 K output tokens, too large to emit in one model response — and both `/graph` (always full Write) and `/graph last` (escalation Write) funneled into that single oversized write. Generating the file from a script removes model output tokens from the path entirely, so the failure class (token ceiling, escalation traps, watermark edge cases, surgical-Edit anchor failures) cannot recur.

**`.last_sync` is owned exclusively by `/sync`.** `/graph` never touches it.

Design rationale for the (now-superseded) incremental design: `.claude/skills/graph/RATIONALE.md`. Legacy manual procedure: git history prior to 2026-06-04 + the Fallback section below.

## Step 0: Pre-flight

### 0.1 Acquire vault lock
`vault-wide` scope per `.claude/skills/_shared/preflight.md` Procedure 1 (§1.3a) — `/graph` reads every thesis file, so a concurrent writer could produce inconsistent extraction. Capture the token; release in the final Bash block (ownership-checked).

Use the **standard §1.3a block verbatim** (with `skill: /graph`) — do NOT hand-roll a lock. The prior inline form omitted `timeout_at:`, the `.vault-lock.*` collision scan, and `set -C` noclobber, so (a) any preflight-conformant skill's collision loop read graph's lock as `timeout_at:`-empty → `[[ "" > "$NOW" ]]` false → classified a LIVE graph run STALE and invited a force-unlock, and (b) graph did not detect concurrent ticker locks at all.

```bash
LOCK_FILE=".vault-lock"
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TOKEN="$(printf '%08x' $RANDOM$RANDOM)-$(date -u +%s)"
TIMEOUT_AT=$(date -u -v+10M +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '+10 minutes' +%Y-%m-%dT%H:%M:%SZ)
setopt NULL_GLOB 2>/dev/null || shopt -s nullglob 2>/dev/null || true

for existing in .vault-lock .vault-lock.* ; do
  [ -f "$existing" ] || continue
  EX_TIMEOUT=$(grep '^timeout_at:' "$existing" | sed 's/timeout_at: //')
  EX_SKILL=$(grep '^skill:' "$existing" | sed 's/skill: //')
  EX_TOKEN=$(grep '^token:' "$existing" | sed 's/token: //')
  if [[ "$EX_TIMEOUT" > "$NOW" ]]; then
    echo "LOCK_HELD|$existing|$EX_SKILL|$EX_TOKEN|$EX_TIMEOUT"; exit 1
  else
    echo "STALE_LOCK|$existing|$EX_SKILL|$EX_TOKEN|timeout_exceeded_at|$EX_TIMEOUT"; exit 2
  fi
done

set -C
if ! cat > "$LOCK_FILE" <<EOF
---
token: $TOKEN
skill: /graph
scope: vault-wide
started_at: $NOW
timeout_at: $TIMEOUT_AT
session_id: ${CLAUDE_SESSION_ID:-unknown}
---

# Vault lock

Held by /graph (token $TOKEN) since $NOW.
EOF
then
  set +C; echo "LOCK_RACE|$LOCK_FILE|created by a concurrent run between check and write — re-run"; exit 1
fi
set +C
trap "rm -f '$LOCK_FILE'" INT TERM
echo "ACQUIRED|$LOCK_FILE|$TOKEN"
```
Reclaim a stale lock (`STALE_LOCK`) only per §1.6 — never auto-steal. Release in the final Bash block with the ownership-verified form (`grep '^token:' .vault-lock` == `$TOKEN` before `rm -f`).

### 0.2 No rename-marker check
`/graph` is read-only for theses; the graph faithfully reflects current filenames + wikilinks. `/lint #37` surfaces pending rename markers separately.

## Step 1: Run the generator

Map the argument to a mode and invoke once:

| Invocation | Arg | Behavior |
|---|---|---|
| `/graph` | `full` | Always (re)writes `_graph.md` (disaster-recovery semantics). |
| `/graph last` | `last` | Writes only if the body changed OR a force-marker is present; else leaves the file untouched and reports up-to-date. |
| `/graph [N]` | `last` | Same as `last` (N accepted for back-compat, treated as `last`). |

```bash
python3 .claude/skills/graph/generate_graph.py full   # or: last
```

What the generator does (so the report is faithful):
- Validates every wikilink against on-disk files; **drops dangling refs** (renamed sectors, legacy `Macro/` prefix, typo'd thesis names) and the intentional-unresolved `[[pinned]]` / `[[preserve]]` markers (never flagged as broken).
- Rebuilds adjacency, both reverse indexes, bidirectional clusters (union-find), and the orphan set **from scratch every run** — no drift.
- Emits the T7.3 read-through cache (`status:` + `log_tail:` — last 3 Log entries, truncated at 100 chars + `…`) that `/sync` Pass 1 triage depends on.
- **Self-validates** the written file (5 sections present; `###` / `status` / `log_tail` counts all equal the thesis count). Exit **0** = written or up-to-date, **2** = validation failed, **1** = runtime error.
- On a successful write, deletes the `.sync_all_fresh` and `.graph_invalidations` force-markers (their presence forces a write even when the body is unchanged, so closures/sync-all always reconcile).

**If the generator exits non-zero**: do NOT leave a half-written graph. Surface its stdout/stderr verbatim and use the Fallback section. Exit 2 means the file was written but failed structural checks — re-run `full`; if it persists, the schema contract or the vault is the problem.

## Step 2: Validate & report

The generator already self-validated. Confirm structure and release the lock in one Bash block:

```bash
echo "=== frontmatter ==="; head -13 _graph.md
echo "=== sections (expect 5) ==="; grep -cE '^## ' _graph.md
echo "=== entries vs cache (three numbers must be equal) ==="
printf '### %s | status %s | log_tail %s\n' \
  "$(grep -cE '^### ' _graph.md)" "$(grep -c '\*\*status:\*\*' _graph.md)" "$(grep -c '\*\*log_tail:\*\*' _graph.md)"
# lock release — ownership-checked (substitute LOCK_TOKEN captured at Step 0.1)
EXPECTED="<LOCK_TOKEN>"
if [ -f .vault-lock ] && grep -q "token: $EXPECTED" .vault-lock; then rm -f .vault-lock && echo "LOCK RELEASED";
else echo "⚠️ lock token mismatch — not removing"; fi
```

Report to the user:
- **Mode** + **status** (`written` / `up-to-date`) + **reason** (from generator stdout).
- **Nodes**: theses + sectors + macro + research. **Edges**. **Orphans** (list).
- **Clusters**: from generator stdout (note new/dissolved vs prior if recoverable).
- **Dangling links dropped**: count — these are source-file link debt; a `/lint` pass or manual cleanup fixes the source, the graph just reflects current truth.
- **Markers cleared**: from generator stdout.
- **No content files modified** — graph metadata only.

## Output schema contract (what the generator must emit)

Frozen interface — consumers depend on it: `/sync` Pass 1 triage (reads `status:` + `log_tail:` prefixes) and the graph-primer in `/ingest`, `/compare`, `/thesis`, `/stress-test`, `/brief`, `/deepen`. Any change to `generate_graph.py` must preserve:
- **Frontmatter**: `type: vault-graph`, `date`, `last_graph_write` (ISO-8601 `…Z`), `graph_mode`, `theses`, `sectors`, `macro`, `research`, `edges`, `orphans`.
- **Five sections, in order**: `## Thesis Adjacency Index`, `## Reverse Index: Macro → Theses`, `## Reverse Index: Sector → Theses`, `## Cross-Thesis Clusters`, `## Orphan Research Notes`.
- **Adjacency entry**: `### TICKER - Name` then 2-space bullets `sectors` / `macros` / `cross-thesis` / `research` / `status` / `log_tail` (`—` for empty); `log_tail` sub-bullets 4-space indent, ≤3, each truncated at 100 chars + `…` (horizontal ellipsis — `/lint #42` safe, never `...`).

`/lint #38` ages the graph state-markers (`.sync_all_fresh` / `.graph_invalidations`), NOT `graph_mode:`; `/lint #43` enforces the lock contract. Validation false-positive note: unbalanced `[[ ]]` inside `log_tail` sub-bullets is EXPECTED (truncation can sever a quoted link) — only structural fields and table rows must balance.

## Fallback (python3 unavailable, or generator exits 1/2)

Reproduce the schema above **without ever single-`Write`-ing the whole file** (that is the failure this skill exists to avoid — at vault scale one `Write` is ~21 K output tokens and aborts):
1. **Extract** inventory + reverse indexes + per-thesis wikilinks/status/log_tail in bounded Bash blocks — batch theses ≤20 per block (the Bash tool truncates output ~20 KB).
2. **Categorize/validate** wikilinks in memory using the same rules as the generator (prefix → sector/macro/cross-thesis/research; drop dangling, `[[pinned]]`, legacy `Macro/`).
3. **Chunked emission**: `Write` frontmatter + `## Thesis Adjacency Index` + the first ≤20 entries; then `cat >> _graph.md <<'GRAPHEOF' … GRAPHEOF` (quoted delimiter, so `[[`, backticks, `$`, `|` are literal) for each remaining ≤20-entry batch and each later section. Keep every call ≤ ~6 KB.
4. **Validate** (re-read: 5 sections, counts equal) and delete `.sync_all_fresh` + `.graph_invalidations` only after success.

---
name: status
description: Change conviction level or status on a single thesis. Use when user says "change conviction", "downgrade", "upgrade", "move to monitoring", "close [TICKER]", or "set [TICKER] to [level]".
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$status`, or infer them from the user's request when this skill is invoked implicitly.

Execute a conviction or status change on a single thesis. Atomic operation that closes the loop after `$stress-test`, `$scenario`, `$deepen`, `$compare`, or manual reassessment.

Design rationale in `.agents/skills/status/references/rationale.md` (§N.M anchors).

## Arguments

`SKILL_ARGS` should follow one of:

**Conviction or status change**: `TICKER field old→new [rationale]`
- `NVDA conviction medium→low China risk unhedgeable`
- `BESI status active→monitoring awaiting Q3 earnings`
- `SHOP status active→closed thesis invalidated by margin compression`

**Drift acknowledgment**: `TICKER reaffirm [rationale]`
- `NVDA reaffirm earnings miss was one-time; competitive position unchanged`

Ambiguous/incomplete → ask user to clarify ticker, field, direction, rationale. If matches `reaffirm` pattern → jump to **Step 2R**.

## Step 0: Pre-flight

### 0.1: Acquire vault lock

`ticker:TICKER` scope per `.agents/skills/_shared/preflight.md` Procedure 1. Timeout: 3 min (extend to 5 min for `status: active→closed` — cascade may take longer). Capture token, verify (Procedure 1.5) every subsequent block, release in final block.

### 0.2: Rename-marker pre-flight

Procedure 2. If `.rename_incomplete.TICKER` exists at vault root, hard-block per contract 2.3. Sector note edits, archive moves, and `_hot.md` mentions all rely on stable naming — mid-rename repair must complete first.

## Step 1: Validate (parallel reads — §10)

Emit the following as parallel tool calls in a single block (after lock is acquired in 0.1). All are read-only probes against stable state; no ordering dependencies:

| Tool | Target | Purpose |
|------|--------|---------|
| `Glob` | `Theses/TICKER - *.md` | Locate thesis file; not-found → `⚠️ No thesis found for [TICKER] in Theses/. Nothing to update.` |
| `Read` | thesis file (once located, read full — worst-case 2 round trips if glob + read can't fuse) | Frontmatter + Log + Conviction Triggers in one read |
| `Read` | `_hot.md` | Pre-fetch for Step 7 (needed regardless of transition type) |
| `Grep` | `sector:` frontmatter value in thesis | Feeds Step 5.0 sector resolution |

Post-batch:
1. **Verify current value**: confirm `old` value in SKILL_ARGS matches actual frontmatter. Mismatch → `⚠️ Expected [field]: [old] but found [field]: [actual]. Confirm the intended change.`
2. **Parse change type + route**:
   - `reaffirm` → **Step 2R** (Reaffirm flow)
   - `status: draft→active` → **Step 2F** (Fast-path — no Tier 3 prompt per §9)
   - `conviction` change → **Step 2** (Tier 3 confirmation)
   - `status` change to `closed` → **Step 2** (Tier 3 confirmation — triggers archive flow)
   - `status` change to anything else (`active→monitoring`, `monitoring→active`, `closed→active`, `active→draft`) → **Step 2** (Tier 3 confirmation)

**Sector note read is deferred to Step 5.0** — sector resolution may rewrite the path (exact/normalized/substring ladder), so resolving that first before reading avoids reading the wrong file.

## Step 2R: Reaffirm Flow (drift acknowledgment)

Entered only when SKILL_ARGS matches `TICKER reaffirm [rationale]`. Lightweight — no frontmatter change, no snapshot, no sector/graph update. Idempotent-safe (§1.1). Skips Step 3.0.5 manifest (§3.2).

1. **Find and read thesis** (same as Step 1.1-1.2).
2. **Extract drift context and classify state**:
   - Scan last 5 Log entries. Identify `"weakened"` or `"strengthened"` sentiment. Count drift pattern.
   - Scan `_hot.md`'s `## Recent Conviction Changes` for active drift flag matching this TICKER (e.g., `⚠️ Conviction drift — [TICKER]: ...`).
   - **drift_flag_active: true | false**
3. **Present evidence and wait for confirmation**:

   **If drift_flag_active = true:**
   ```
   Drift review for [[Theses/TICKER - Company Name]]:
     Current conviction: [level]
     Active drift flag: [flag text from _hot.md, dated YYYY-MM-DD]
     Recent log sentiment:
       - YYYY-MM-DD: [summary] — [weakened/strengthened/unchanged]
       - ...
     Drift signal: [N]/[window] entries flagged headwinds (or tailwinds)

     Reaffirming conviction at [level] with rationale: [from SKILL_ARGS]
     This resets the drift detection window AND clears the drift flag.

   Confirm? (y/n)
   ```

   **If drift_flag_active = false:**
   ```
   Proactive reaffirm for [[Theses/TICKER - Company Name]]:
     Current conviction: [level]
     Active drift flag: none
     Recent log sentiment: [list]

     Reaffirming conviction at [level] with rationale: [from SKILL_ARGS]
     No active drift to clear — Log entry recorded for audit trail.
     Drift window anchor advances regardless.

   Confirm? (y/n)
   ```
   **Do NOT proceed without explicit user confirmation.**

4. **Append Log entry** (MANDATORY regardless of drift state — §1.1 — max 2 lines):
   ```
   ### YYYY-MM-DD
   - Conviction reaffirmed at [level] after [drift review | proactive review] — [rationale from SKILL_ARGS]
   ```
   Use `drift review` when `drift_flag_active = true`, `proactive review` otherwise. Prefix `"Conviction reaffirmed"` is canonical in both cases — `$sync` Step 3e drift anchor (registry §5). Do not change without updating `.agents/skills/_shared/log-prefixes.md` + `$sync`; `$lint #29` flags drift.

5. **Update _hot.md** (follow `.agents/skills/_shared/hot-md-contract.md`; do NOT touch Latest Sync / Sync Archive):
   - **Recent Conviction Changes**: add `- **[TICKER]**: conviction [level] reaffirmed — [rationale]`
   - **Drift flag cleanup** (only if `drift_flag_active = true`): locate active drift flag entry for TICKER, mark inline `⚠️ Conviction drift — [TICKER] ... → Resolved YYYY-MM-DD: reaffirmed ([level])` (§1.2 — prevents stale flag re-appearing as Open Question on next `$sync`).

6. **Report**:
   - **Reaffirmed**: [TICKER] conviction [level] maintained
   - **Drift state at entry**: `active flag cleared (from YYYY-MM-DD)` | `no active flag — proactive reaffirm for audit trail`
   - **Log entry appended**: 1 line (`Conviction reaffirmed`)
   - **Drift window reset**: next $sync anchors drift detection after this entry
   - **No snapshot, sector, or graph changes**

**Stop here — do not continue to Step 2 or beyond.**

---

## Step 2F: Fast-path for `draft→active` (no Tier 3 — §9)

**Only entered when the parsed transition is `status: draft → active`.** The Tier 3 confirmation gate is bypassed for this specific transition. Rationale in §9 — summary: additive coverage transition (not the reductions AGENTS.md Tier 3 gates), no analytical content change (same rationale that already skips the thesis snapshot at Step 3.1), easily reversible via manual frontmatter flip per User Guide §13, and the user's explicit `$status TICKER active` invocation is itself an intent signal.

Emit an FYI message showing what will happen, then proceed DIRECTLY to Step 3 without waiting for input:

```
ℹ️  Fast-path: status draft → active for [[Theses/TICKER - Company Name]]
    Sector: [sector from frontmatter]
    Side effects: add to Sectors/[Sector].md Active Theses; _hot.md Active Research Thread + Recent Conviction Changes entries; manifest written.
    Proceeding without Tier 3 prompt per §9 (draft→active is additive + reversible).
```

Then continue to Step 3. Every other mechanic (snapshot skip per §2.2, sector dry-run per §5.1, manifest at §3, Log prefix "Status change:" per registry §6) is IDENTICAL to the Step 2 path — only the user-prompt step is elided.

**Exemption scope is narrow** — only `draft→active`. All other status transitions (including `monitoring→active`, `closed→active`, `active→draft`) still require Step 2 Tier 3 confirmation because they involve either reductions, reopen semantics, or demotion risks.

## Step 2: Confirm (Tier 3 — Mandatory)

Present the proposed change and **wait for user confirmation**:

```
Proposed change:
  Thesis: [[Theses/TICKER - Company Name]]
  Field: [conviction | status]
  Change: [old] → [new]
  Rationale: [from SKILL_ARGS]
  Trigger alignment: [see below]
  Mental-model basis: [see below]
  Side effects: [list what will be updated — sector note, archive move, graph cleanup]
  Open findings this may resolve: [grep _followups.md ## Open for this ticker; matching findings 1-line each — or "none"]

Confirm? (y/n)
```

**Trigger alignment (falsifiability discipline — READING PROTOCOL).** Before presenting the prompt, read the thesis's `## Conviction Triggers` section (the Step 1 read already loaded it) and fill the `Trigger alignment:` line with exactly one of:
- `confirms [→ HIGH/LOW/CLOSE if …]` — **quote the matching trigger verbatim**; the change is a pre-defined hypothesis firing.
- `overrides [→ … if …]` — quote the conflicting trigger; the change contradicts an active trigger (same condition Step 4 #3 warns on).
- `outside triggers` — the section exists but no trigger covers this change; the rationale stands alone.
- `none defined — unfalsifiable change` — the thesis has **no** `## Conviction Triggers` section (~38 theses); state it plainly and suggest `$deepen TICKER Conviction Triggers` (Case A scaffold) after the change.

This converts every Tier-3 decision into a hypothesis test against the thesis's own pre-registered falsifiers at zero extra reads. It never blocks — the user may confirm any alignment value — but a bare assertion is now visibly bare.

**Mental-model basis (MANDATORY reading gate — `.agents/skills/_shared/mental-models-section.md`).** A conviction/status change is an investment judgement, so before rendering it read the load-tiered `/Mental Models` scope — `[[Mental Models/Generalist - Overview]]` always + the matching `Industry -` / `Lens -` note for this ticker (cached across the run) — and apply the READING PROTOCOL (models are lenses/questions, never verdicts; run the base-rate adversarially; model agreement is a disconfirm trigger, not a confirm). Fill the `Mental-model basis:` line by naming the fired trigger(s) the change rests on with their stable IDs (`[G-#]` / `§`) and a one-line read each, or `none` when no model bears on it. This binds the mandated read to the deliverable at the point of decision. Fast-path `draft→active` (Step 2F): light-touch — coverage-only, no conviction judgement — so `none` is expected.

**Do NOT proceed without explicit user confirmation.** Investment decisions per AGENTS.md Tier 3.

## Step 3: Snapshot

### 3.0: Generate batch ID (always — §2.2)

```bash
HHMMSS=$(date +%H%M%S)
mkdir -p _Archive/Snapshots
```

Batch ID format: `status-TICKER-YYYY-MM-DD-$HHMMSS` (§2.1 — ticker qualifier prevents concurrent-run collisions). **Capture the echoed `HHMMSS` value and reuse it LITERALLY** in every later block (manifest 3.0.5, thesis snapshot 3.1, sector snapshot 5a, report Step 8) — shell blocks are stateless subshells (preflight §Design note), so `$HHMMSS` is empty when re-referenced in a later block; paste the captured digits, exactly as the lock token is carried. Used across all snapshots in this run for atomic cascade restore.

### 3.0.5: Write status transaction manifest skeleton (T2.2 — §3)

**Mandatory BEFORE any file modifications.** Step 3.1 snapshot, Step 4 frontmatter edit, Step 5 sector edit, Step 7.5 archive move, Step 7.6 invalidation write are ALL gated on this skeleton.

Write `_Archive/Snapshots/_status-manifest (status-TICKER-YYYY-MM-DD-HHMMSS).md`:

```yaml
---
type: status-manifest
batch: status-TICKER-YYYY-MM-DD-HHMMSS
status: in-progress
ticker: TICKER
transition_type: conviction | status | reaffirm
field: conviction | status
old_value: [parsed]
new_value: [parsed]
trigger_alignment: confirms [quoted trigger] | overrides [quoted trigger] | outside triggers | none defined
date: YYYY-MM-DD
---

# Status Transaction Manifest (in-progress)

Manifest written at Step 3.0.5 before any file modifications. Intended edits:

## Thesis frontmatter edit
- Target: `Theses/TICKER - Name.md`
- Field: [conviction | status]
- Change: [old] → [new]
- Snapshot taken: (populated in Step 3.1 — or "skipped (draft→active)")

## Sector note edit (if applicable per Step 5.1 dry-run)
- Resolution: (populated)
- Edit planned: yes | no | skipped (no match)
- Snapshot taken: (populated in Step 5a)

## Archive move (closure only)
- Source: `Theses/TICKER - Name.md`
- Target: `_Archive/TICKER - Name.md`
- Status: (populated in Step 7.5)

## Graph invalidations (closure only)
- Neighbors queued: (populated in Step 7.6)

## Archive registry append (closure only)
- Line added to `.archive_ticker_registry.md`: (populated in Step 7.5b)

## _hot.md edits
- (populated in Step 7)

## Recovery guidance

If this file persists with `status: in-progress`, $status crashed mid-run:
- (a) Skeleton only → thesis unchanged; rm manifest.
- (b) Thesis edited but later steps failed → $rollback [snapshot_batch].
- (c) Partial closure (archived but sector not updated) → $rollback handles both via snapshots.

Flipped to `status: completed` at Step 7.9 after all stages succeed.
$lint #48 surfaces in-progress as Important.
```

**Skeleton write failure — hard abort** (§3.1):
```
❌ Status transaction manifest skeleton write failed: [path]
   Reason: [error]
No vault state modified. Fix filesystem issue and re-run $status.
```

Exit. Reaffirm flow (Step 2R) does NOT need a manifest (§3.2).

**Incremental population**: each subsequent step (3.1, 4, 5a, 7.5, 7.6) appends completion state via `Edit` (§3.3).

### 3.1: Thesis snapshot

```bash
cp "Theses/TICKER - Company Name.md" "_Archive/Snapshots/TICKER - Company Name (pre-status YYYY-MM-DD-$HHMMSS).md"
```

Read snapshot, add frontmatter:
```yaml
snapshot_of: "[[Theses/TICKER - Company Name]]"
snapshot_date: YYYY-MM-DD
snapshot_trigger: status
snapshot_batch: status-TICKER-YYYY-MM-DD-HHMMSS
```

**Exception**: skip thesis snapshot for `status: draft→active` (no analytical content change, only frontmatter `status:` flip). Sector snapshot in Step 5a still runs because Step 5b modifies the sector note for this transition.

## Step 4: Apply Change

### Conviction changes

1. Update `conviction:` in frontmatter.
2. Append Log entry (max 2 lines):
   ```
   ### YYYY-MM-DD
   - Status change: conviction [old] → [new] — [rationale]. Snapshot: [[_Archive/Snapshots/...]]
   ```
   Prefix `"Status change: conviction"` — `$sync` Step 3e drift anchor (registry §6). Do not change; `$lint #29` flags drift.
3. **Conviction trigger check** (§7): read Conviction Triggers section. New level contradicts active trigger (e.g., → `high` but a `→ LOW if X` trigger is active) → `⚠️ Active trigger conflicts with new conviction: [quote trigger]. Confirm this is intentional.` **Section absent** (~38 theses): skip the conflict check gracefully — do NOT abort — and emit `⚠️ No ## Conviction Triggers section — this change is unfalsifiable as recorded; consider $deepen TICKER Conviction Triggers (Case A scaffold).` The Step 2 `Trigger alignment:` line already carries `none defined` in this case.

### Status changes (non-closure)

1. Update `status:` in frontmatter.
2. Append Log entry:
   ```
   ### YYYY-MM-DD
   - Status change: [old] → [new] — [rationale]. Snapshot: [[_Archive/Snapshots/...]]
   ```

### Status → closed (archive flow — §4)

1. Append final Log entry:
   ```
   ### YYYY-MM-DD
   - CLOSED: [rationale]. Archived.
   ```
2. Change frontmatter: `status: closed`.

**File not moved yet** (§4.1). Archive move runs in Step 7.5 after all metadata updates succeed. Intermediate state (`status: closed` in `Theses/`) is safe and recoverable — `$sync` skips closed theses; `$lint #33` flags pending move; manual `mv` completes.

## Step 5: Update Sector Note

### 5.0: Locate the sector note

Resolve via `.agents/skills/_shared/sector-resolution.md`. Inputs: thesis `sector:`. Outputs: `sector_note_path`, `match_confidence`, `log_message`.

- `none` → emit no-match warning, skip rest of Step 5, proceed to Step 6.
- `normalized` / `substring` → emit `log_message` in Step 8 report, proceed with resolved path.
- `exact` → silent, proceed.

### 5.1: Dry-run — determine if edit needed (§5)

Read sector note. Analyze what Step 5b would do for this transition. Set `edit_planned: true` only when at least one condition below matches.

| Transition | Check against sector note | `edit_planned: true` when... |
|---|---|---|
| `draft→active` | Wikilink in Active Theses? | ABSENT |
| `monitoring→active` | Wikilink in Active Theses (not annotated as monitoring)? | Absent OR present but annotated monitoring |
| `closed→active` (reopen) | (1) in Active Theses? (2) in Closed/Archived? | ABSENT from Active **OR** PRESENT in Closed/Archived (§6) |
| `active→monitoring` | Sector distinguishes monitoring AND thesis not annotated? | Both true |
| `active→closed` | Wikilink in Active Theses? | PRESENT (remove) |
| Conviction change | Sector displays conviction AND displayed differs from new? | Both true |

Detection indicators (§5.3):
- **Monitoring distinction**: `## Monitoring` section, `(monitoring)` suffix, `monitoring:` annotation
- **Conviction display**: `(high|medium|low)` adjacent, `| Conviction |` column, grouped-by-conviction sections

**`edit_planned: false`** → skip 5a and 5b. Report in Step 8: `Sector note: no edit needed — [TICKER] transition [old→new] already reflects current sector note state.` Proceed to Step 6.

**`edit_planned: true`** → proceed to 5a.

### 5a: Pre-edit snapshot (conditional)

```bash
cp "Sectors/Sector Name.md" "_Archive/Snapshots/Sector Name (pre-status YYYY-MM-DD-$HHMMSS).md"
```

Read snapshot, add frontmatter (reuse Step 3.0 batch ID):
```yaml
snapshot_of: "[[Sectors/Sector Name]]"
snapshot_date: YYYY-MM-DD
snapshot_trigger: status
snapshot_batch: status-TICKER-YYYY-MM-DD-HHMMSS
```

Runs for every transition where Step 5.1 set `edit_planned: true` — including `draft→active` (where thesis snapshot was skipped but sector note IS being modified). Without this snapshot, a corrupted Edit would leave no recovery path.

### 5b: Apply sector edit (conditional)

1. **Status → active** (from draft/monitoring/closed): add to Active Theses. If previously present with monitoring annotation, remove annotation. For `closed→active`: if `## Closed/Archived` section exists and contains this thesis, remove entry (prevents dual listing). Optional: append a Log entry to the sector note documenting the promotion.
2. **Conviction change** (when sector displays conviction): update displayed level to new value.
3. **Status → monitoring** (when sector distinguishes): move or annotate per sector convention.
4. **Status → closed**: remove from Active Theses. Add to `## Closed/Archived` if exists.

**Batching guidance — §10**: when a single transition requires multiple edits to the same sector note (e.g., `draft→active` for a thesis currently on the Watchlist: add-to-Active + remove-from-Watchlist + append-Log), emit all three `Edit` tool calls as **independent invocations in a single tool-call block**. The harness serializes same-file Edits on the server side (each Edit validates unique `old_string` against the current file state), so this is one LLM round-trip instead of three. Do NOT wait for each Edit's response before firing the next.

**Cross-file parallelism**: Step 5a sector snapshot `cp` (Bash) can fan out in parallel with Step 5b's first Edit on the sector note — the snapshot reads the pre-edit state, the Edit writes the post-edit state; `cp` completes first even if dispatched in the same block because Bash is synchronous on the tool-result boundary.

## Step 5.5: Advisory peer-assumption sweep (downgrade/close only)

**Runs only when the change is a conviction DOWNGRADE (new level below old on the high > medium > low ordering) or a `status: active→closed`.** Skip for upgrades, non-closure status changes (`active→monitoring`, etc.), `draft→active` (Step 2F), and the Reaffirm flow (Step 2R never reaches here). **Advisory and non-fatal** — read-only; this step NEVER mutates any thesis (not the downgraded/closed one, and never a peer). A missing sector note, missing `_graph.md`, or zero matches skips it cleanly with no output.

The assumption that just sank a thesis often underpins its sector peers, yet nothing checks them — a single-name downgrade should become a portfolio-wide check for the same failure mode. This is the read-only advisory analogue of `$sync` Step 4b's cross-thesis contradiction sweep: that one appends peer Log entries; this one only surfaces for the user to act on.

1. **Identify the core assumption** the change rests on — from the user's rationale (`SKILL_ARGS`) plus the downgraded thesis's own `## Bull Case` / `## Key Non-consensus Insights` content (already in memory from the Step 1 read).
2. **Enumerate sector peers** — the sector's OTHER active theses, via the sector note's `## Active Theses` list (already read at Step 5.1 when resolved) OR the `_graph.md` sector reverse-index keyed on the thesis's `sector:` value (grepped at Step 1). Exclude the downgraded/closed thesis itself.
3. **Grep each peer** for reliance on the same assumption (shared driver, shared named catalyst, shared bull-case mechanism); keep only peers whose case leans on it.
4. **Surface as an ADVISORY list only** — never auto-mutate peer theses; the user decides whether to reassess each:
   ```
   Peers sharing this assumption (review — the reason you downgraded [TICKER] may apply to them): [PEER1] (§section), [PEER2] (§section), …
   ```
   Zero peers, no sector resolution, or no `_graph.md` → omit the line entirely.

## Step 6: Graph update deferred

`_graph.md` owned exclusively by `$graph`.

- **Conviction and non-closure status changes**: no graph impact (graph tracks links, not conviction/status metadata).
- **Status → closed**: after this skill (Step 7.5 archive + Step 7.6 invalidation), run `$graph last`. Step 7.6's invalidation list forces re-extraction of neighbor theses that referenced the closed thesis (§4.4).

## Step 7: Update _hot.md

Follow `.agents/skills/_shared/hot-md-contract.md`. Read first, then edit. Do NOT touch Latest Sync / Sync Archive.

1. **Active Research Thread**: follow contract's same-ticker-continuation rule.
2. **Recent Conviction Changes**: add `- **[TICKER]**: [field] [old] → [new] — [rationale]`. **Never compressed** per contract.
3. **Open Questions**: if closing, remove open questions specific to this ticker. Dedupe by merging duplicates.
4. **Portfolio Snapshot**: update conviction-level counts (if conviction changed) or active/monitoring/closed counts (if status changed). Regenerated fresh per contract.

**Cap enforcement**: after all edits, run compression trigger order. Over soft cap → apply drops per contract. Over hard cap → abort `_hot.md` update per contract §Compression trigger order step 5. Do NOT block the primary `$status` operation.

## Step 7.5: Archive Move (closure only)

**Skip for conviction changes, non-closure status changes, reaffirmations.**

### 7.5a: Pre-move archive-collision check (§4.2)

```bash
ls "_Archive/TICKER - Company Name.md" 2>/dev/null
```

If file exists at destination (prior closure of same ticker-and-name), pause:

```
⚠️ Archive-path collision: _Archive/TICKER - Company Name.md already exists from a
   prior closure. Running mv would silently overwrite.

Options:
  (a) Timestamp-suffix the old archive, then proceed:
      mv "_Archive/TICKER - Company Name.md" "_Archive/TICKER - Company Name (closed YYYY-MM-DD).md"
      then mv the new thesis to the clean path.
  (b) Timestamp-suffix the NEW archive path instead:
      mv "Theses/TICKER - Company Name.md" "_Archive/TICKER - Company Name (closed YYYY-MM-DD).md"
  (c) Cancel — leave thesis in Theses/ with status: closed; resolve manually.

Confirm (a/b/c):
```

Wait for selection. (c) → report metadata updates (sector, `_hot.md`, invalidations) already completed; thesis remains in `Theses/` pending manual archive resolution.

### 7.5b: Move + update archive-ticker registry (fused shell block)

Chain `mv`, registry append, and post-move verification into ONE shell block via `&&` — each step conditional on prior success. Replaces three separate shell tool calls with one round-trip; `&&` preserves the "each step only if prior succeeds" semantics the prior serialized form enforced implicitly:

```bash
# Atomic fused block: mv → registry append → verify. Each step guarded by &&.
mv "Theses/TICKER - Company Name.md" "_Archive/TICKER - Company Name.md" && \
{
  REGISTRY=".archive_ticker_registry.md"
  if [ ! -f "$REGISTRY" ]; then
    cat > "$REGISTRY" <<'HEADER'
---
type: archive-ticker-registry
purpose: Flat append-only log of thesis archival events. Consumed by $thesis Step 1.2 Signal C (multi-signal archive-collision check).
---

# Archive Ticker Registry

HEADER
  fi
  printf '%s|%s|%s|%s|%s\n' \
    "$TICKER" \
    "$ARCHIVED_FILENAME" \
    "$(date +%Y-%m-%d)" \
    "$CONVICTION_AT_CLOSURE" \
    "$CLOSURE_RATIONALE_LINE" \
    >> "$REGISTRY"
} && \
[ -e "_Archive/TICKER - Company Name.md" ] && \
[ ! -e "Theses/TICKER - Company Name.md" ]
```

The final two `ls` probes serve as the Step 7.5b verification mentioned below — if the `mv` landed, the archive file exists AND the Theses file does not. Exit code 0 = all four stages succeeded. Non-zero exit surfaces the specific failing stage via `set -e`-like semantics inside the fused block.

Registry append failure (extremely unlikely — single-line append): `⚠️ Archive registry append failed: [reason]. Signal C in future $thesis [TICKER] may miss this entry. $lint #46 will flag on next run.` Does NOT abort closure — archival succeeded; only the lookup aid is missing. Signals A/B/D still cover common cases.

**Verification**: confirmed inline in the fused shell block above (`ls` checks land in the same round-trip as the `mv` and registry append).

**If move fails** (§4.3): all metadata already succeeded. Do NOT attempt to undo. Report:
```
⚠️ Archive move failed — thesis remains in Theses/ with status: closed.
Metadata (sector note, graph, _hot.md) already updated.
To complete manually: mv "Theses/TICKER - Company Name.md" "_Archive/TICKER - Company Name.md"
```

## Step 7.6: Write Graph Invalidation List (closure only)

**Skip for non-closure transitions.** Skip silently if Step 7.5 reported move failed (§4.5) — closure incomplete; invalidation must wait.

### 7.6a: Identify neighbor theses

Grep `Theses/` (excluding just-archived thesis) for wikilink patterns referencing closed thesis:

Patterns (each ticker/name occurrence, any form):
- `[[Theses/TICKER - Company Name]]`, `[[Theses/TICKER - Company Name|alias]]`, `[[Theses/TICKER - Company Name#section]]`, `[[Theses/TICKER - Company Name.md]]`
- `[[TICKER - Company Name]]`, `[[TICKER - Company Name|alias]]`, `[[TICKER - Company Name#section]]`

Use `Grep` with `output_mode: files_with_matches`, multiple pattern runs. Dedup. Exclude just-archived thesis.

### 7.6b: Append to `.graph_invalidations`

One relative thesis path per line (e.g., `Theses/NVDA - Nvidia.md`). If file exists (prior closure produced unconsumed entries — `$graph last` hasn't run), append then dedupe:

```bash
{
  [ -f .graph_invalidations ] && cat .graph_invalidations
  printf '%s\n' "Theses/NEIGHBOR1 - ...md" "Theses/NEIGHBOR2 - ...md"
} | sort -u > .graph_invalidations.tmp && mv .graph_invalidations.tmp .graph_invalidations
```

No neighbors (isolated thesis): skip file creation. Report `Invalidation: no neighbors — isolated thesis.`

### 7.6c: Validate and report

After write, verify file exists + contains expected entries. Include in Step 8:
- **Graph invalidation**: `[N] neighbors added to .graph_invalidations: [first 5, truncate with "...+M more"]`
- **Graph reminder**: `$graph last` now mandatory — without it, invalidation list accumulates.

## Step 7.7: Resolve open findings (_followups.md)

Runs for every conviction/status change; Reaffirm flow (Step 2R) exits before this step and never resolves findings. Closes the loop opened by writer skills per `.agents/skills/_shared/followups-contract.md`. **Non-fatal** — a failed read or edit never blocks the completed change.

1. `_followups.md` absent → skip.
2. Grep `## Open` for entries whose thesis wikilink matches this TICKER.
3. Keep only matches whose finding the executed change **satisfies**:
   - `reassess conviction …` — a conviction change just happened.
   - `… crossed → [HIGH/LOW/CLOSE] trigger` — the matching conviction/closure change just happened.
   Non-satisfied findings stay in `## Open`.
4. Move each match from `## Open` to the top of `## Resolved` (newest first), reformatting to the resolved-entry form with outcome `actioned via $status`:
   ```
   - [x] YYYY-MM-DD raised → YYYY-MM-DD resolved · <skill> · [[Theses/TICKER]] · <finding> — actioned via $status
   ```
   `raised` = the entry's original date; `resolved` = today. **Never delete — Open→Resolved only.**
5. Surface in the report: `Findings resolved: [N] moved Open→Resolved in _followups.md` (omit when N=0).

## Step 7.9: Finalize status transaction manifest (consolidated — §10)

**Only runs if Step 3.0.5 wrote a manifest** (skipped for Reaffirm flow Step 2R).

Consolidate manifest population + frontmatter flip into a **single tool-call block** — one message, parallel independent `Edit` invocations:

1. `Edit` to populate the manifest body's "Thesis frontmatter edit", "Sector note edit", "Archive move", "Graph invalidations", "`_hot.md` edits" sections with their final outcomes (any sections not yet populated by Steps 3.1/4/5a/7.5/7.6 per §3.3 get filled here in one pass).
2. `Edit` to flip the frontmatter: `status: in-progress` → `status: completed`.
3. `Edit` to add `completed_date: YYYY-MM-DD` to frontmatter.

These three Edits target different parts of the same manifest file (body sections vs frontmatter lines). The harness serializes them on the server but dispatching them together saves 2 round-trips vs firing them sequentially.

**Verify flip** — run a targeted frontmatter read against the live file after applying the patch. Do not rely only on the patch operation's success status. Confirm `status: completed` present AND `status: in-progress` absent from the targeted verification output. Flip fails (§3.4):
```
⚠️ Status manifest status flip failed — manifest at [path] remains in-progress despite successful $status completion. $lint #48 will flag as Important. Manual fix: edit the manifest frontmatter to status: completed.
```

Do NOT rollback — all stages already succeeded.

**Final batch with Step 8**: after the required targeted live-file verification, Step 7.9 compresses to the single tool-call block already described above; the lock-release shell block from Step 8 fires immediately after.

Manifest retained. `$clean` handles aging via 90-day threshold (§8 — no regret-recovery window like `$prune`).

## Step 8: Report

- **Change applied**: [TICKER] [field] [old] → [new]
- **Rationale**: [from SKILL_ARGS]
- **Thesis snapshot**: `[[_Archive/Snapshots/TICKER - Company Name (pre-status YYYY-MM-DD-HHMMSS)]]` | `skipped (draft→active)`
- **Sector note snapshot**: `[[_Archive/Snapshots/Sector Name (pre-status YYYY-MM-DD-HHMMSS)]]` | `skipped (no matching sector note)` | `skipped (no edit needed — sector state already reflects transition)`
- **Batch ID**: `status-TICKER-YYYY-MM-DD-HHMMSS` (cascade-restore via $rollback)
- **Sector Note updated**: [sector] — [what changed] | `no edit needed (dry-run)`
- **Graph reminder**: `→ Run $graph last` (closure only — conviction/non-closure have no graph impact). For closures, invalidation list is unconsumed until `$graph last` runs.
- **Archived** (closure only): `[[_Archive/TICKER - Company Name]]` | `⚠️ Archive move failed — see Step 7.5 output`
- **Graph invalidation** (closure only): `[N] neighbors queued in .graph_invalidations: [first 5 paths, truncate "...+M more"]` | `no neighbors — isolated thesis` | `skipped — archive move failed`
- **Wikilink breakages** (closure only): `⚠️ [N] notes contain wikilinks to this thesis. Run $lint to review.`
- **Trigger conflict** (if any): `⚠️ [quote conflicting trigger]`

---
name: thesis
description: Create a new investment thesis note with full analysis. Use when user says "create thesis", "new thesis", or "build a case for TICKER"
model: opus
effort: max
allowed-tools: Read Grep Glob Edit Write WebSearch WebFetch Bash(date * defuddle * touch *)
---

Create a comprehensive thesis note for `$ARGUMENTS`.

Design rationale in `.claude/skills/thesis/RATIONALE.md` (§N.M anchors).

## Step 0: Pre-flight

### 0.1: Acquire vault lock

`ticker:TICKER` scope per `.claude/skills/_shared/preflight.md` Procedure 1. Timeout 10 min (vault + web research can be slow). Capture token, verify (Procedure 1.5) every subsequent block, release in final.

Step 0.1 MUST complete before Step 0.2 / Step 1 fire — the lock establishes the stable state window for every read-only probe that follows.

### 0.2: Rename-marker check (§6)

Probe `.rename_incomplete.TICKER` per Procedure 2. If present, hard-block per contract 2.3. Rare edge case (can't rename a non-existent thesis), but possible if user previously created → renamed partially → archived → now creating new thesis for same TICKER.

**Execution**: fires as part of Step 1.0 parallel probe batch, not as a standalone call. See §9 for safety analysis.

## Step 1: Duplicate Check

### 1.0: Parallel probe batch (§9)

Steps 0.2, 1.1, 1.2 Signals A–E, and 1.3 have **no ordering dependencies** — all are read-only probes against vault state that is stable under the ticker lock acquired in 0.1. Emit all of them as independent tool calls in a **single tool-call block** (one message, multiple parallel invocations).

The seven probes:

| # | Step | Tool | Target |
|---|------|------|--------|
| 1 | 0.2 | `Glob` | `.rename_incomplete.TICKER` |
| 2 | 1.1 | `Glob` | `Theses/TICKER - *.md` |
| 3 | 1.2 Signal A | `Glob` | `_Archive/TICKER - *.md` |
| 4 | 1.2 Signal B | `Grep` | `^ticker: TICKER$` in `_Archive/*.md` (non-recursive) |
| 5 | 1.2 Signal C | `Glob` | `.archive_ticker_registry.md` (existence probe; follow-up `Grep` for `^TICKER\|` only if file exists) |
| 6 | 1.2 Signal D | `Grep` | `snapshot_of:.*Theses/TICKER -` in `_Archive/Snapshots/*.md` |
| 7 | 1.3 | `Grep` | `TICKER` in `Research/` (prefer `ticker:` frontmatter + `tags:` matches over body-text) |

**Process results post-batch in priority order** — earlier hits short-circuit later decisions:

1. **0.2 marker match** → hard-block per Procedure 2 §2.3. Ignore all other probe results (the marker takes absolute precedence; any thesis/archive/research state we read is suspect until the rename repair completes).
2. **1.1 match** → active thesis exists. Stop. Suggest `/deepen TICKER`. Report matching filename.
3. **1.2 Signals A/B/C/D UNION non-empty** → archive-collision protocol (§2). Proceed to 1.2's existing 4-option prompt.
4. **All clear** → 1.3 result set feeds Step 2 as research context.

**Option (b) re-probe**: if the user picks alternate name in the archive-collision prompt, re-run **only** the 1.1 Glob against the new name. Other probes (marker, archives, research) don't change based on the name choice — don't re-fire them.

**Signal C existence probe handling**: the registry is vault-local but not guaranteed to exist (fresh vaults, or vaults that have never closed a thesis). Treat absent-registry as empty set for Signal C. If Glob returns a hit, a follow-up Grep for `^TICKER\|` in the registry extracts the match. This is one sequential step after the parallel batch, but only fires conditionally.

### 1.1: Active thesis check (prefix glob — §1.1)

`Glob Theses/TICKER - *.md`. Any file match → active thesis exists. Stop. Suggest `/deepen TICKER` instead. Report matching filename.

**Why prefix glob not content grep**: short tickers (`A`, `T`, `U`) would produce false-positive duplicate warnings under content grep (§1).

### 1.2: Archived thesis check (MULTI-SIGNAL — §2)

Tier 3 confirmation gate. Run ALL five signals; take UNION.

**Signal A — Filename glob (RECURSIVE)**: `Glob _Archive/**/TICKER - *.md` — closures land in `_Archive/Theses/`, not `_Archive/` root, so the old non-recursive `_Archive/TICKER - *.md` matched zero archived theses. Exclude only `_Archive/Snapshots/` (pre-rename/pre-edit copies, not canonical archives) when parsing matches.

**Signal B — Frontmatter ticker (RECURSIVE + list-form + archived status)**: grep `_Archive/` recursively (excluding `Snapshots/`) for the ticker in the `ticker:` frontmatter field, matching BOTH scalar (`ticker: KLAC`) AND YAML-list (`ticker: [KLAC, AMAT, LRCX, ...]`) forms, and accept `status: archived` as well as `status: closed`. The real archived thesis `_Archive/Theses/SEMICAP - Semiconductor Capital Equipment.md` carries `ticker: [KLAC, AMAT, LRCX, ASMI, TEL, BESI]` + `status: archived` — the old `^ticker: TICKER$` scalar-anchored grep over `_Archive/*.md` root missed it on every axis. Executable form:
```bash
grep -rlE "^ticker:( *\[?[^]]*\b)?TICKER\b" _Archive --include='*.md' | grep -v '/Snapshots/'
```

**Signal C — Archive-registry lookup**: check `.archive_ticker_registry.md` at vault root (auto-maintained by `/status` Step 7.5b and `/prune` Stage 4). Each line: `TICKER|archived_filename|YYYY-MM-DD`. Line starting `TICKER|` → extract referenced filename, verify still in `_Archive/`.

**Signal D — Snapshot trail**: grep `_Archive/Snapshots/*.md` frontmatter for `snapshot_of:` containing `Theses/TICKER -`. Historical trace even if archived under different filename.

**Signal E — Archive tags**: grep `_Archive/` recursively (excluding `Snapshots/`) for the ticker in a `tags:` list (`grep -rlE "^tags:.*\bTICKER\b" _Archive --include='*.md'`). A multi-ticker archived thesis (e.g. a sector-basket closure) carries each constituent in `tags:` even when the filename is a basket name — the SEMICAP note tags `KLAC`, so `/thesis KLAC` catches it here even if Signals A/B somehow drift.

Dedup across signals. Per unique archived file, collect: filename, `conviction:` at closure, last Log entry (1-line closure rationale), `status:` (expected `closed`), archive date.

**Union non-empty → archive-collision protocol**:

a. Read archived thesis(es). Extract per file: filename, last Log entry (closure rationale), `conviction:`, `status:`.

b. Present structured prompt. Wait for explicit user choice. Do NOT proceed silently:

```
⚠️ Archived thesis exists for TICKER:
  - [[_Archive/TICKER - Old Company Name]]
    closed: [date] · conviction at closure: [level]
    closure rationale: [last Log entry, truncated to 1 line]

Creating a new thesis at Theses/TICKER - [proposed-name].md will produce
TWO distinct files for the same ticker. Downstream skills (/sync, /graph,
/catalyst) operate on Theses/* and ignore _Archive/* — the prior analysis,
Log audit trail, and conviction journey become invisible to the new thesis.

Options:
  (a) /rollback TICKER  — RECOMMENDED. Restores the prior thesis with
      its full Log history. Use this if the original thesis is being
      reopened (rather than starting fresh on the same ticker).
      The rollback flow handles status: closed → active and re-attaches
      the thesis to its sector note.

  (b) Proceed with new thesis under a DIFFERENT name suffix to make the
      dual-file state intentional and visible (e.g., the prior thesis
      was "TICKER - Old Brand" and you want "TICKER - New Strategy").
      Provide an explicit alternate name. The archived file is preserved.

  (c) Proceed with the proposed name, accepting that two files for the
      same ticker will exist (one in Theses/, one in _Archive/) and that
      the archived analysis is being deliberately abandoned. Useful only
      if the prior thesis is irrelevant to the new investment case.
      The archived file is preserved.

  (d) Cancel.

Confirm (a/b/c/d):
```

c. **Branch on user choice**:
- **(a)**: stop. Output `→ Run: /rollback TICKER` and exit. No new thesis created. User runs `/rollback` separately.
- **(b)**: re-prompt for alternate company name. Compute `Theses/TICKER - [alternate-name].md`. Re-run Step 1.1 active thesis check against alternate name. Proceed to Step 2 with alternate.
- **(c)**: proceed to Step 2 with originally proposed name. Add caveat to initial Log entry: `Initial thesis created. Conviction: [level] — [rationale]. Note: prior archived thesis at [[_Archive/TICKER - Old Name]] retained for reference but not connected to this thesis.`
- **(d)**: stop silently.

d. **Multiple archived files** (§2.4 — rare): list all matches in prompt. Same options. Option (c)'s log entry wikilinks most recent archive (highest `closed:` date in frontmatter or filename timestamp).

### 1.3: Research context grep (informational only — §1.2)

Grep `Research/` for ticker string. Surfaces relevant existing research for new thesis to link to. Does NOT block creation. Prefer frontmatter `ticker: TICKER` match and `tags:` containing ticker as whole-word over body-text mentions (filters short-ticker false positives out of context set).

## Step 2: Vault Research

**Mental Models reading gate (MANDATORY — CLAUDE.md; `_shared/mental-models-section.md`).** Before any analysis, read `[[Mental Models/Generalist - Overview]]` (always) + the matching `[[Mental Models/Industry - X]]` for this ticker's sector (e.g. `Industry - Semiconductors` for a semi name) + any `[[Mental Models/Lens - X]]` the thesis touches (`Lens - Automation & AI Readiness`; `Lens - Value Layer Monopoly`). Apply the READING PROTOCOL: models are lenses/questions held as **hypotheses to test, never verdicts**; run the base-rate / outside view adversarially; treat agreement across models as a trigger to **disconfirm** (hunt the bear case + the single falsifying datapoint). These reads populate the `## Mental Models` section (#12) and sharpen the Key Non-consensus Insights + Bear Case.

- Read relevant Sector Note for existing coverage and competitive context
- Search `/Research` and `/Macro & Technology` for notes mentioning this ticker or topic
- Read related thesis notes for competitive dynamics and cross-thesis connections

**Parallelization with Step 3**: Step 2 vault reads and Step 3 web searches have no ordering dependency — the LLM can issue both Step 2's Reads/Greps and Step 3's first WebSearch batch in a **single parallel tool-call message**. Follow-up web searches that depend on first-round results (e.g., "search for [Competitor X] after sector note reveals they exist") land in subsequent batches. Do NOT serialize Step 2 and Step 3 end-to-end.

## Step 2.5: Graph-primer peer suggestions

Per `.claude/skills/_shared/graph-primer.md` Mode A (special handling: target TICKER is new, so `adjacency_index[TICKER]` is null).

Read `_graph.md` once. Fire the Read in parallel with Step 2 Reads / Step 3 WebSearches (same tool-call batch).

Because the target TICKER is new and not in the graph, use vault research from Step 2 to infer probable sector/macro:
- `inferred_sectors` = union of `sector:` frontmatter from matched research notes (from Step 2 Greps)
- `inferred_macros` = union of `[[Macro & Technology/...]]` wikilinks in those research note bodies

Compute peer suggestion sets:
- `candidate_sector_peers` = union over `s ∈ inferred_sectors` of `sector_reverse[s]`
- `candidate_macro_peers` = union over `m ∈ inferred_macros` of `macro_reverse[m]`, minus `candidate_sector_peers`
- `candidate_cluster_peers` = for each candidate in sector_peers, if peer belongs to a Cross-Thesis Cluster, surface cluster name as context

Surface to user BEFORE Step 4 writes the thesis, for explicit accept/reject:

```
Graph-primer cross-thesis suggestions (review before Step 4 writes the thesis):
  Strong (same sector, same cluster): [list with cluster name]
  Medium (same sector, unclustered):  [list]
  Weak   (shared macro only):         [list]

Accept which for Related Research wikilinks? (e.g., "AVGO, NVDA" | "all" | "none")
```

User's accepted set feeds Step 4's `## Related Research` section (thesis-to-thesis wikilinks). `/thesis` does not expose an explicit `cross-thesis:` frontmatter field; cross-thesis adjacency is derived by `/graph` from Related Research + body wikilinks targeting `Theses/*.md`.

**Orientation not filter**: the primer surfaces candidates — user decides. Low hit rate is expected when the target is genuinely in a new niche; Step 3 web research still fires regardless.

**Missing-graph fallback**: per `.claude/skills/_shared/graph-primer.md` §Missing-graph fallback. Step 4 proceeds with Related Research populated only from Step 2 direct matches.

## Step 3: Web Research

Research topics:
- Recent earnings, analyst consensus, key financials
- Competitive dynamics, market share data, industry trends
- Bear cases and risks — actively look for reasons NOT to invest
- Sell-side consensus — identify where a non-consensus view could exist

**Parallel-batch pattern (mirrors `/catalyst` Phase 2)**: issue all independent WebSearch invocations in parallel batches — **one message containing up to 25 WebSearch / WebFetch calls**, then the next message with the next batch, and so on. For a typical new-position build this is 1-2 rounds of ~5-15s each instead of ~15-20 serial rounds. Never serialize web calls that have no data dependency on each other (e.g., "earnings search" + "analyst consensus search" + "bear case search" + "sell-side coverage search" are all independent — batch them).

Follow-up searches that DO depend on first-round results (e.g., after the initial batch surfaces a specific competitor, then fetching that competitor's latest earnings) fire in a subsequent parallel batch. Cap per-batch at 25 to stay within safe tool-call limits.

## Step 3.5: Write thesis transaction manifest skeleton (H1 — §4)

**Mandatory BEFORE Step 4 writes the thesis file.** Skeleton write failure hard-aborts pre-mutation.

### 3.5.1: Generate batch ID

```bash
HHMMSS=$(date +%H%M%S)
mkdir -p _Archive/Snapshots
```

Batch ID: `thesis-TICKER-YYYY-MM-DD-HHMMSS` (§4.2 — TICKER qualifier prevents concurrent-run collisions under per-ticker locks).

### 3.5.2: Write skeleton manifest

Path: `_Archive/Snapshots/_thesis-manifest (thesis-TICKER-YYYY-MM-DD-HHMMSS).md`

```yaml
---
type: thesis-manifest
batch: thesis-TICKER-YYYY-MM-DD-HHMMSS
status: in-progress
ticker: TICKER
proposed_name: [company name from Step 3 web research OR alternate from Step 1.2 option (b)]
proposed_path: Theses/TICKER - [proposed_name].md
sector: [sector from Step 2/3 research]
date: YYYY-MM-DD
---

# Thesis Transaction Manifest (in-progress)

Manifest written at Step 3.5 before any file modifications. Intended operations:

## Thesis file creation
- Target path: `Theses/TICKER - [proposed_name].md`
- Status: (populated at Step 4 — `created` | `failed`)

## Sector note update
- Sector resolution: (populated at Step 5 — `exact` | `normalized` | `substring` | `none`)
- Sector note path: (populated)
- Edit applied: (populated — `added_to_active_theses` | `skipped (draft status)` | `skipped (no sector note)` | `new_sector_note_created` | `failed`)

## `_hot.md` updates
- Active Research Thread entry: (populated — text appended or `failed`)
- Recent Conviction Changes entry: (populated)
- Open Questions entries: (populated — count added)

## Orphan research integration
- Orphan research notes touched: (populated — list of paths whose mtime was advanced)
- Wikilinks added to Related Research: (populated — count)

## Archive-collision decision (if Step 1.2 found matches)
- Archived theses found: (populated — list from Signals A/B/C/D)
- User decision: (populated — `(a) /rollback recommended (exited)` | `(b) alternate name` | `(c) accept dual-file` | `(d) cancelled`)

## Recovery guidance

If this file persists with `status: in-progress`, /thesis crashed mid-run:
- **Skeleton only**: no thesis file yet; no sector or _hot.md edits. Recovery: `rm` manifest; re-run `/thesis TICKER`.
- **Thesis file created, sector/hot.md incomplete**: thesis exists but disconnected from sector + _hot.md. Recovery: complete remaining steps manually per manifest body OR `rm` thesis file + manifest, then re-run.
- **All steps landed but flip failed** (Step 7.5): manually edit frontmatter to `status: completed` + `completed_date: YYYY-MM-DD`. Manifest ages out via `/lint #49`.

Flipped to `status: completed` at Step 7.5 after all stages succeed.
/lint #49 surfaces in-progress as Important.
```

### 3.5.3: Skeleton write failure — hard abort

```
❌ Thesis transaction manifest skeleton write failed: [path]
   Reason: [error]

No vault state modified. Thesis file NOT created, no sector/_hot.md changes.
Fix filesystem issue (disk space, permissions, _Archive/Snapshots/ dir exists) and re-run /thesis TICKER.
```

Exit. Do NOT proceed to Step 4.

### 3.5.4: Incremental population

Each subsequent step (4, 5, 6, 7) appends completion state to manifest via `Edit`. Crash after Step 5 but before Step 6 → manifest reflects {thesis created ✓, sector updated ✓, _hot.md pending}. `/rollback` Step 2.5f cascade consumes state for recovery (§4.3 — deletion-based).

## Step 4: Create the Thesis

**Conviction discipline (set it AFTER the bear case, not before).** Draft the analytical sections — especially Bear Case (#8), Risks (#10), and the Mental Models disconfirming check (#12) — BEFORE finalizing the `conviction:` frontmatter value. The frontmatter sits at the top of the file but is decided last: assess honestly against the bear case you just wrote, not the bull case that motivated the note. The initial Log entry's one-line rationale must state **why the chosen conviction survives the bear case** (READING PROTOCOL: agreement across models → disconfirm, so the bull-heavy first draft is the one to distrust). A `high` conviction whose rationale doesn't engage the bear case is the signature failure this ordering prevents.

Save to `Theses/TICKER - Company Name.md`:

```yaml
---
publish: true
date: [today's date]
tags: [thesis, SECTOR-TAG, TICKER]
status: draft
conviction: [high|medium|low — assess honestly]
sector: [primary sector]
ticker: TICKER
source: [primary source URL or description]
---
```

Initial status `draft` (§8 — excluded from /catalyst, /prune flags, conviction drift until user explicitly promotes via `/status draft→active`).

`publish: true` is mandatory — the website-sync flag (an external GitHub→website pipeline pulls notes marked `publish: true`; see CLAUDE.md § Conventions → Note Format). Omitting it makes the thesis invisible to the site: this exact spec-vs-template drift produced a 1-of-83 outlier, fixed 2026-07-29.

### Required Sections (all 14, in order — §7)

> `## Legacy Callouts` (template section 14, between Related Research and Log) is **auto-created on demand by `/archive-callouts`** on the first sweep — do NOT scaffold it at creation (`/lint #14` exempts its absence). The 14 sections below are everything `/thesis` writes.

1. **Summary** — One paragraph investment case. Lead with non-consensus angle, not business description.

2. **Key Non-consensus Insights** — 3-5 one-paragraph summaries of perspectives foreign to mainstream narrative. **THIS IS THE MOST IMPORTANT SECTION** (§7.2). Think deeply about what market is missing — technological shifts, management/culture edges, competitive dynamics, investor biases, business model transitions. **Draft each insight in the 4-field microformat from `Templates/Thesis Template.md`** — `**Consensus:**` / `**Variant:**` / `**First confirming observable [YYYY-MM]:**` / `**Falsifier:**`, one bulleted sub-field each under the insight title. `**Consensus:**` is mandatory and must name what the market actually believes / prices — an insight that cannot state the consensus it opposes is positioning, not analysis ([[Generalist - Overview]] [G-13] expectations-investing: read the price-embedded consensus, then isolate the single variable it misprices). Tie each `**Falsifier:**` to a `→ LOW/CLOSE` Conviction Trigger (#11) where possible.

3. **Outstanding Questions** — 3-10 one-paragraph summaries of what a skeptical investment committee would ask before approving. Genuinely hard, not softballs. Each should identify what data or event would answer it.

4. **Business Model & Product Description** — In-depth breakdown with analogies/comparisons to make it intuitive. Key revenue/profit-generating products with technical specs where relevant. Revenue segmentation (reported segment or novel heuristic that captures economics).

5. **Industry Context** — Competitive dynamics, market share + pricing power shifts, value chain analysis. Where does this sit in the value chain? Who has leverage? What structural forces are reshaping the industry?

6. **Key Metrics** — Table:

| Metric | Value | Notes |
|--------|-------|-------|
| Market Cap | | |
| EV/Revenue | | |
| Revenue Growth | | |
| Gross Margin | | |
| FCF Yield | | |

7. **Bull Case** — Explicit upside scenario with specific drivers. What has to go right? Include valuation target or framework if possible.

8. **Bear Case** — Explicit downside scenario with specific drivers. Genuinely adversarial — don't softball. What does the world look like where this loses money?

9. **Catalysts** — Near-term events with approximate dates that could move the stock. Both positive and negative.

10. **Risks** — What breaks the thesis. Minimum 3 risks. Distinguish thesis risks (investment case is wrong) from position risks (thesis is right but stock goes down anyway).

11. **Conviction Triggers** — Pre-defined, falsifiable if/then statements (§7.3):
    ```
    → HIGH if: [specific observable condition]
    → LOW if: [specific observable condition]
    → CLOSE if: [specific observable condition]
    ```
    Concrete + testable, not vague. Good: "→ LOW if TSMC cuts capex guidance by >10% in next 2 quarters." Bad: "→ LOW if competition increases."

12. **Mental Models** — the OUTPUT of the Step 2 reading gate applied to THIS thesis, per `_shared/mental-models-section.md` (three bullets): **Models applied** (`[[Generalist - Overview]]` always + the Industry/Lens files consulted); **Triggers that fired** (each pertinent model trigger — `<model> · <trigger> — <one-line read>`, held as a hypothesis to test, never a verdict); **Disconfirming check** (where models agree, the bear case / single falsifying datapoint / base-rate this thesis must beat). Populate at creation — do NOT leave scaffold-empty; the initial analysis already applied the models.

13. **Related Research** — Wikilinks to relevant vault notes (research, sector notes, macro notes, related theses).

14. **Log** — Initial entry:
    ```
    ### YYYY-MM-DD
    - Initial thesis created. Conviction: [level] — [one-line rationale]
    ```
    Prefix `"Initial thesis created"` — `/sync` Step 2.5 skill-origin classification (registry §11).

## Step 5: Update the Vault

### Sector note update

Resolve via canonical `.claude/skills/_shared/sector-resolution.md` using thesis's `sector:` frontmatter.

- **`match_confidence: exact | normalized`**: proceed silently (or contract's `log_message` in Step 7 report).
- **`match_confidence: substring`**: emit contract's `log_message` and proceed.
- **`match_confidence: none`** (5.4 fix — §3): present three options. Do NOT silently skip.

  ```
  ⚠️ Sector "[sector-value]" from Theses/TICKER - Name.md does not match any existing Sectors/*.md file (via exact, normalized, or substring matching).

  Options:
    (a) Create Sectors/[sector-value].md now from Templates/Sector Template.md with minimal scaffolding (frontmatter + section headings + this thesis as first Active Thesis entry). Analytical content can be filled later or via /surface [sector]. Recommended when new thesis is first in a legitimately new sector.

    (b) Proceed without sector update — thesis exists in Theses/ but no sector note references it. Downstream skills using sector resolution (/status, /compare, /prune, /surface sector-scoped) will emit no-match warnings for this ticker until a sector note exists. Create Sectors/[value].md manually later and run /graph last to reconcile.

    (c) Cancel — abort before writing thesis file. Use if sector value is a typo or needs revision.

  Confirm (a/b/c):
  ```

  **Branch behavior** (§3.2):
  - **(a)**: create `Sectors/[sector-value].md` from `Templates/Sector Template.md`. Minimal frontmatter: `publish: true` (website-sync flag per Sector Template), `date: today`, `tags: [sector, sector-value-slug]`. Minimal body: 10 section headings from template, each with `- _pending_` placeholder, EXCEPT `## Active Theses` gets new thesis as first entry: `- [[Theses/TICKER - Name]]`. Log entry: `### YYYY-MM-DD\n- Sector note created by /thesis TICKER — first thesis in this sector. Scaffold-only; analytical content to be added via /deepen or /surface.` Re-run sector resolution (now `match_confidence: exact`) to validate creation succeeded, then proceed with normal sector-update logic.
  - **(b)**: skip sector update. Log `ℹ️ Sector update skipped per user confirmation — no matching sector note. Sectors/[sector-value].md can be created manually later.` Continue to orphan research integration.
  - **(c)**: stop skill. No files written. `❌ /thesis TICKER cancelled at Step 5 — sector mismatch. Correct the sector value in the thesis frontmatter or create Sectors/[sector-value].md first, then re-run.`

**Status-dependent behavior**:
- If `status: active` → add thesis to resolved Sector Note Active Theses section.
- If `status: draft` → skip (draft theses added when promoted via `/status TICKER status draft→active`).

### Integrate orphan research notes (§5)

Search `Research/` for notes predating this thesis that reference it. Resolution order (mirrors `/sync` Step 1 Fallbacks — §5.3):
- (a) `ticker:` frontmatter matching this ticker
- (b) `tags:` containing this ticker as a token

For each match:
1. Add wikilink to new thesis's `## Related Research` section. Do NOT modify the research note itself (Tier 2 append-only).
2. `touch` the research note to advance mtime past `.last_sync`:
   ```bash
   touch "Research/[matched-note].md"
   ```
   Without the touch, the thesis's `## Log` shows only "Initial thesis created" — the research-to-thesis audit trail is permanently broken (§5.1). Touch re-enters the note into `/sync`'s changed-file set; next `/sync` appends canonical Log entries to this thesis.

### Graph update deferred

`_graph.md` owned exclusively by `/graph`. Run `/graph last` after this skill to register new thesis (full adjacency: sector, macro, cross-thesis, research) in dependency map. Until then, ticker-scoped operations resolve adjacency directly from thesis file.

## Step 6: Update _hot.md

Per `.claude/skills/_shared/hot-md-contract.md` (do NOT touch Latest Sync / Sync Archive):

1. **Active Research Thread**: same-ticker continuation per contract. Write: new thesis created for [TICKER], conviction [level], logical next research step.
2. **Recent Conviction Changes**: add entry for new thesis with initial conviction level.
3. **Open Questions**: add 2-3 most critical Outstanding Questions from new thesis.

Word cap: after edits, over 8,000 (soft cap per `_shared/hot-md-contract.md`) → prune `## Sync Archive` (oldest first) then `*Previous:*` lines. Abort if over 10,000 hard cap.

## Step 7.5: Finalize thesis transaction manifest (H1)

Flip Step 3.5 manifest frontmatter:
- `status: in-progress` → `status: completed`
- Add `completed_date: YYYY-MM-DD`

Verify flip via `grep -q` Bash probe — faster than a Read tool call and does not inject the manifest body into context:

```bash
# Exit 0 = completed landed AND in-progress gone → flip succeeded
if grep -q "^status: completed$" "[manifest path]" && ! grep -q "^status: in-progress$" "[manifest path]"; then
  echo "FLIP_OK"
else
  echo "FLIP_FAILED"
fi
```

`FLIP_FAILED`:
```
⚠️ Thesis manifest status flip failed — manifest at [path] remains in-progress despite successful /thesis completion. /lint #49 will flag as Important. Manual fix: edit the manifest frontmatter to status: completed + add completed_date: today. The thesis, sector note, and _hot.md updates all succeeded.
```

Do NOT retry, do NOT rollback — thesis transaction already succeeded. Flip-only failure is cosmetic, caught by `/lint #49`.

**No regret-recovery window** (§4.4 — unlike `/prune`'s 30 days): `/thesis` is constructive. Regret here means "I want to edit/expand" → `/deepen`'s job, not rollback. `/clean` Step 2a ages `_thesis-manifest` files with standard 90/180 day tiers.

## Step 8: Suggest Next Steps

- **Activate**: `status: draft`. Run `/status TICKER status draft→active` when ready to promote — drafts excluded from `/catalyst`, `/prune` flags, conviction drift detection (§8).
- What 2-3 research questions would most increase or decrease conviction?
- Any upcoming catalysts to monitor with dates?
- Which existing vault theses have the strongest competitive tension with this one?

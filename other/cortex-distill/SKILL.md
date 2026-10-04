---
name: cortex-distill
description: >
  Distill raw session records into refined Notes and Projects. Use when
  the user says "提煉", "整理 raw", "distill", or "distill raw records".
---

# Cortex Distill — Refine Raw Records

Extract valuable knowledge from Raw/ session dumps into Notes/ and Projects/.

## Resolve Vault Path

Read `~/.cortex/config.json` to get `vault_path`.
If the file doesn't exist, tell the user to run `/cortexes:genesis` first.

## Step 1: Find Unprocessed Raw Files

List the distill queue:

```bash
cortex-vec distill-queue --root <vault_path>/Raw
```

This is **position-anchored**: a Raw counts as distilled only if a
`<!-- distilled: ... -->` marker appears in its header (before the first
`### User` turn) **or** as its last non-empty line. Do **NOT** `grep` the
marker string — a pipeline meta-session's body quotes it dozens of times
(it printfs markers onto other files), so `grep -rL '<!-- distilled:'`
silently drops genuine work from the queue. To check one file, use
`cortex-vec raw-state <file>`.

### Backlog hygiene (only when queue > 1 file)

SessionEnd reclaims the *prefix* snapshots of the Raw it has just written
(`reclaim-superseded --keep <that-file>`), but it never looks at an
existing backlog. Before sizing the batch, run the pairwise form once —
no `--keep` — so strict-prefix duplicates leave the queue:

```bash
cortex-vec reclaim-superseded --root <vault_path>/Raw                       # list only
cortex-vec reclaim-superseded --root <vault_path>/Raw --apply --vault <vault_path>
```

Applying is safe: a candidate is removed only when it is a line-for-line
prefix of a longer queued recording, so no content is lost.

That tool does NOT catch a second class of duplicate: the same transcript
captured twice whose filter output *diverged* (the residue classifier is
not deterministic — one copy kept a `/context` table, the other a
`Log Summary`). Neither copy is a prefix of the other, and the two files
may carry different `repo:` labels or even different dates. What they
share is `raw_bytes` in the audit line — the size of the source
transcript — so scan for collisions and treat each group as a **triage
hint**, never as a deletion list:

```bash
grep -rao -m1 --include='*.md' 'raw_bytes=[0-9]*' <vault_path>/Raw \
  | awk -F'[:=]' '$3 >= 4096 {print $3, $1}' | sort -n \
  | awk '{n[$1]++; f[$1]=f[$1] "\n  " $2} END {for (k in n) if (n[k]>1) print k f[k]}'
```

(`raw_bytes` under a few KB is degenerate — dozens of empty captures share
tiny values — hence the 4096 floor.) For each group, compare the copies'
first user turn (`raw-map --find-only` + `raw-span`, Step 2) and decide
by hand: distill the fuller copy, give the other `skip-routine`. Two
copies with equal `raw_bytes` can each hold lines the other lacks, so a
collision alone never justifies deleting either. Do not substitute a
hand-rolled fingerprint (first-turn text, `### User` counts): that is
exactly what let a pair through on 2026-09-09.

Show the pending list count and ask to proceed.

## Step 1.5: Schedule the Batch (only when queue > 1 file)

Size the queue before opening any Raw:

```bash
cortex-vec distill-queue --root <vault_path>/Raw --stat
```

Partition by RAW size (the `raw` column) and **present the plan for
approval** (do not auto-run):

- **Normal lane** — Raws whose raw size fits well inside one session
  budget (default 100K chars of raw-derived output). Process a batch this
  session, strictly one Raw at a time.
- **Monster lane** — Raws whose complete review clearly exceeds one
  session budget (a full map traversal alone can run ~5x the budget on a
  1M-char Raw). One Raw per dedicated session, and do NOT page the map
  from the top: play it find-first (Step 2, "Monster play") — locate an
  anchor with `raw-map --find-only`, read the hit with `raw-span`,
  record evidence, stop early. `BUDGET_EXHAUSTED` +
  `distill-plan resume --new-session` is the fallback when no anchor
  hits, not the plan.

Carry remaining lanes forward with a `cortex-takeoff` baton. When a plan
is mid-flight, record its `plan_id` in the baton — machine state lives in
the plan cache, the baton only points at it.

## Step 2: Stage 1 — Has Insight (map-first)

One Raw at a time. NEVER Read the full Raw file; NEVER judge from an
L3/L3* projection. All original text arrives through bounded pages.

1. Start (or resume) the plan:

   ```bash
   cortex-vec distill-plan start <raw-file>
   ```

   Note the returned `plan_id`. If it errors `ANOTHER_PLAN_ACTIVE`, ask
   the user whether to resume that plan or `distill-plan clear` it —
   never switch Raws silently.

2. Traverse the map:

   ```bash
   cortex-vec raw-map <raw-file> --plan-id <id>
   cortex-vec raw-map <raw-file> --plan-id <id> --cursor <next_cursor>
   ```

   Cards show kind / size / source range / preview / lexical anchors.
   The map never says "valuable" or "skip" — choosing what to expand is
   the main session's judgment.

   `--find "<literal>"` reports the ids of the spans containing an exact
   literal under `find_matches`. It does **not** move the page: `cards`
   still start at 0 (or at the cursor) and the whole page is charged.
   Read `find_matches`, not `cards`, to see where the hit is. When the
   span id is all you need, add `--find-only`: no cards, no map
   progress, one ~600-char envelope instead of a ~12K page.

   **Monster play (find-first).** For a Raw whose map traversal cannot
   fit the budget, skip paging entirely:

   ```bash
   cortex-vec raw-map <raw-file> --plan-id <id> --find "★ Insight" --find-only
   cortex-vec raw-span <raw-file> --plan-id <id> --span-id <N>    # read the hit
   ```

   Good anchors: `★ Insight`, an issue key, an error string, a file path
   the session must have touched. Read the hit and its neighbours, then
   take the early positive stop (item 4) — a positive candidate never
   needs full coverage, so this is the only affordable path on a Monster
   Raw. `no-insight` stays gated on full traversal (item 5) and is
   therefore usually out of reach there; say so rather than burn the
   budget paging.

3. Expand what needs reading. `prose`, `output_body`, `ambiguous`,
   `opaque` spans (and any card with `preview_complete: false` you need)
   must be read via:

   ```bash
   cortex-vec raw-span <raw-file> --plan-id <id> --span-id <N>
   cortex-vec raw-span <raw-file> --plan-id <id> --cursor <next_cursor>
   ```

4. Early positive stop: once you have concrete insight evidence, record
   it and stop expanding —

   ```bash
   cortex-vec distill-plan evidence-add --plan-id <id> \
     --char-start <s> --char-end <e> --label "<short cite>"
   ```

   (the range must already be reviewed). Full coverage is NOT required
   for a positive candidate.

5. `no-insight` gate is mechanical: it requires
   `no_insight_candidate_allowed: true` from

   ```bash
   cortex-vec distill-plan status --plan-id <id>
   ```

   which means the whole map was traversed AND every semantic /
   ambiguous span was expanded. Do not propose `no-insight` before that.

6. On `BUDGET_EXHAUSTED`: stop reading, write the takeoff baton with the
   `plan_id`, and continue in a fresh session via

   ```bash
   cortex-vec distill-plan resume --plan-id <id> --new-session
   ```

Then apply `has_insight()` (below) to what you actually read.

### `has_insight()` rule

Answer **Yes** iff at least one passage anywhere in the Raw contains one of:

- A specific symbol / file path / line number (e.g. `src/main.rs:226`, `checkDockerImage()`, `buildconf/unit-test`).
- A specific bug mechanism or root-cause statement (e.g. "filter must fully match repository, substring not supported").
- A specific decision rationale in the form "X over Y because Z" — not bare "use X".

Insight commonly appears in any of these locations; treat them all as
first-class:

- `★ Insight ─────` callouts inside `### Claude` blocks (Claude Code
  learning-mode output).
- Tables comparing options, summarizing a bug, or laying out an attack
  chain.
- Prose paragraphs that walk through analysis, root cause, or
  trade-off rationale.
- Legacy `## Discoveries` / `## Decisions` sections (manually-edited
  Raws — still valid but not required).

Answer **No** only when the entire Raw genuinely lacks concrete
referents — e.g., commands executed with no surrounding analysis, or
vague statements like "fixed it" / "works now" / "tested successfully"
without any mechanism / file / symbol / decision rationale anywhere in
the body.

### Present judgment to user (mandatory)

The `has_insight()` result above is a **candidate verdict**, not a
dispatch decision. **Always present the candidate to the user and wait
for confirmation**, even when the verdict feels obvious. The user's
answer is binding regardless of the agent's tilt.

Use `AskUserQuestion` with:

- **Evidence**: 1–3 concrete excerpts from the Raw supporting the
  candidate (file:line, ★ Insight callout, decision rationale, table,
  etc.). When the candidate is `No`, note explicitly that no concrete
  referent was found anywhere in the body.
- **Candidate verdict**: `Yes (has insight)` or `No (no insight)`.
- **Options**:
  - `(y)es — agree with candidate`
  - `(n)o — override to opposite`
  - `(s)kip-routine — Raw not worth dedup nor recording` (use when the
    Raw is essentially a tool-recap / git-log dump that technically
    passed `has_insight` on a symbol but has no surrounding analysis)

### Dispatch on user's answer

- User confirms `Yes` → proceed to Step 3 (Stage 2).
- User confirms `No` → `no-insight`, go to Step 5 (mark) + Step 7 (log).
- User picks `skip-routine` → `skip-routine`, go to Step 5 + 7 + 8.
  No broadcast prompt (Step 9 is skipped for skip-routine).

### Batch hygiene

The plan ledger enforces the per-session raw-derived cap (default 100K
chars, `session_remaining_chars` in every page). When a session has spent
a few plans' worth of budget, stop: commit finished Raws (Step 8) and
hand the queue to the next session via `cortex-takeoff`. When Step 4
quotes Raw text into a draft, verify the quote with `grep -F` against the
source, and keep the evidence ranges recorded via `evidence-add`.

### Three-filter tags (categorization hint, not a gate)

When has_insight is Yes, optionally tag the extracted content for later lint:

| Tag | Signal | Example |
|-----|--------|---------|
| 踩坑 (gotcha) | Non-obvious behavior, hidden trap | "jsoncpp returns null for oversized doubles" |
| 慣例 (convention) | Project-specific or internal practice | "Service A reads config.json, Service B reads env vars" |
| 決策 (decision) | Why A over B, trade-off rationale | "build-history.json over PID check because..." |

These tags no longer gate extraction — they are reserved metadata for future lint capability. Safe to omit if the use case is unclear; downstream tooling treats absence as untagged.

## Step 3: Stage 2 — Decide Placement

Only runs when Stage 1 returned Yes.

### 3.1 Load thresholds

Read `~/.cortex/config.json`:

```bash
jq -r '.distill.dedup_threshold_new // 0.45' ~/.cortex/config.json
jq -r '.distill.dedup_threshold_pending // 0.60' ~/.cortex/config.json
```

Defaults: `new = 0.45`, `pending = 0.60`.

### 3.2 Query dedup

Pick the **most content-ful insight passage** anywhere in the Raw as the
query text — typically the densest `★ Insight ─────` callout, the
clearest analysis paragraph naming specific referents, or (for legacy
Raws) the longest Discovery/Decision bullet. Aim for one self-contained
chunk that mentions the concrete symbol / mechanism / decision; trim
to roughly one paragraph. Run:

```bash
cortex-vec search "<bullet text>" --n 3
```

If the repo is known from Raw frontmatter, add `--repo <name>` when searching Projects-bound content.
`--repo` narrows the `Projects/` partition only; cross-repo `Notes/` always appear in results regardless of the filter, and a page listing several repos passes a filter naming any of them. Safe to add when the Raw is repo-specific.

Extract top-1 `score` from the JSON output. Every returned hit carries a
real cosine on the same 0-1 scale, including hits that entered through the
keyword or wikilink streams, so a low score means low overlap rather than
an unmeasured one.

If `cortex-vec` is unavailable (command errors, ECONNREFUSED, etc.): treat as `score = 0.0`, log `dedup_top1: unavailable`, prefer false-positive `new` over losing the insight.

### 3.3 Present score + candidate outcome to user (mandatory)

**Always ask the user**, regardless of where score falls. The threshold
table below degrades from gate to *candidate-outcome heuristic* — it
shapes the recommendation the agent surfaces, but never decides
unilaterally.

Use `AskUserQuestion` with:

- **Score**: two decimals (e.g. `0.62`).
- **Top-1 hit**: `[[wikilink]]` + ≤1-line excerpt from that page.
- **Candidate outcome**: chosen per the heuristic table below.
- **Options**: `(n)ew / (p)ending-merge / (s)kip-routine`.

| Score band | Candidate outcome to propose |
|------------|------------------------------|
| `score < dedup_threshold_new` | `new` (low overlap with existing pages) |
| `dedup_threshold_new ≤ score < dedup_threshold_pending` | describe both `new` and `pending-merge` neutrally; no strong tilt |
| `score ≥ dedup_threshold_pending` | `pending-merge` (strong overlap with top-1) |

**When to tilt toward `skip-routine`** (independent of score): the Raw
passed Stage 1 only because of an isolated symbol mention with no
surrounding analysis — e.g., a git-log dump that happens to name a file
path. Surface `(s)kip-routine` as a real candidate in such cases rather
than forcing `new` / `pending-merge`.

### 3.4 Dispatch on user's answer

- `(n)ew` → go to Step 4 (create) + Step 5 + 6 + 7 + 8.
- `(p)ending-merge` → skip Steps 4 and 6; go to Step 5 + 7 + 8 only.
  **Do not write any new file or touch existing pages.**
- `(s)kip-routine` → skip Steps 4 and 6; go to Step 5 + 7 + 8 only.
  Marker writes as `(skip: routine)`.

## Step 4: Create Refined Note

1. Draft the refined content
2. Determine placement:
   - Repo-specific knowledge → `Projects/<repo>/` (repo from Raw file's `repo:` frontmatter)
   - General technical knowledge → `Notes/<category>/` (match existing categories)
3. Add `repos:` to frontmatter if repo-specific
4. Present draft to user for confirmation
5. Write to vault using Obsidian Flavored Markdown (wikilinks, frontmatter, callouts)

## Step 5: Mark Raw as Processed

The marker must not be written until the plan is sealed (Notes/log
all written, the user has confirmed the verdict):

```bash
cortex-vec distill-plan seal --plan-id <id> --expected-outcome <new|pending-merge|skip-routine|no-insight>
```

After sealing, map/span pages are rejected (`PLAN_SEALED`); only then
append the marker.

Append exactly one marker to the Raw file, chosen by Step 3 outcome:

| Outcome | Marker |
|---------|--------|
| `new` | `<!-- distilled: YYYY-MM-DD → <target-relative-path> -->` |
| `pending-merge` | `<!-- distilled: YYYY-MM-DD → pending-merge: <existing-path> (<score>) -->` |
| `skip-routine` | `<!-- distilled: YYYY-MM-DD → (skip: routine) -->` |
| `no-insight` | `<!-- distilled: YYYY-MM-DD → (no insight) -->` |

Score formatting: two decimal places (e.g., `0.62`, not `0.62345`).
Date: today, `YYYY-MM-DD`.

## Step 6: Update Index (only for `new` outcome)

Skip this step entirely for `pending-merge`, `skip-routine`, `no-insight`.

For each newly created file:

1. Run: `cortex-vec upsert <relative-path>`
2. Update `_index.md`: append the row under the matching `###` sub-section — the
   topic sub-section under `## Notes`, or the repo sub-section under
   `## Projects`. Create the sub-section (with its table header) if it does not
   exist yet. Then bump the `updated` date in frontmatter.

   Do NOT maintain an `entries:` count — the frontmatter has no such field, by
   design (see `/cortexes:genesis`).

## Step 7: Append Log Entry

For each Raw processed (regardless of outcome), append exactly one entry to `<vault>/log.md`:

```markdown
## [YYYY-MM-DD HH:MM] distill | <raw-filename>
- outcome: <new|pending-merge|skip-routine|no-insight>
- target: <vault-relative path | omit for skip-routine and no-insight>
- dedup_top1: <score → [[wikilink]] | "unavailable" | omit for no-insight>
- repo: <value from Raw frontmatter repo: field | "(none)">
```

The agent should:

1. Compose the entry text with all placeholders substituted (today's date/time, the raw filename, the outcome, the target path, the score, the wikilink, the repo).
2. Append it to `<vault>/log.md` using either the Edit tool (preferred — adds the entry and preserves file integrity) or bash:

```bash
printf '\n%s\n' "$ENTRY" >> "<vault>/log.md"
```

Where `$ENTRY` is the fully-substituted markdown entry.

Preserve exactly one blank line between entries (achieved by the leading `\n` in the printf above, or by ensuring the Edit tool's new content starts with a blank line when appending).

Field rules:

- `target`: present for `new` and `pending-merge`. Omit the line for `skip-routine` and `no-insight`.
- `dedup_top1`: include the score and top-1 page wikilink whenever Stage 2 ran (outcomes: `new` when score was computed, `pending-merge`, all interactive choices, `skip-routine`). Omit only for `no-insight` (Stage 2 did not run). For `cortex-vec` unavailable, write `dedup_top1: unavailable`.
- `repo`: use `(none)` if the Raw has no `repo:` frontmatter field.

## Step 8: Commit

```bash
cd <vault>
git add Raw/ Notes/ Projects/ _index.md log.md
git commit -m "distill: extract N entries from Raw"
```

If `git.commit_trailer` in config is a non-empty string, pass it as a second
`-m` so it becomes the last line of the message body:
`git commit -m "distill: extract N entries from Raw" -m "<commit_trailer>"`.

If `auto_push` is true in config: `git push`.

After the commit completes, close the plan (this verifies the only file
change was the expected marker):

```bash
cortex-vec distill-plan complete --plan-id <id>
```

If it returns `RAW_CHANGED`, the Raw has changed beyond just the marker —
stop and report, do not retry.

## Step 9: Broadcast (always, inline)

For each Raw whose terminal outcome was `new` or `pending-merge`,
**dispatch to the `cortex-broadcast` skill inline** immediately after
Step 8's commit. Do not prompt the user — every broadcast-eligible Raw
is broadcast.

Announce before dispatching:

```
Dispatching broadcast for <raw-filename>...
```

When broadcast completes, return here and move to the next unprocessed
Raw.

For outcomes `skip-routine` and `no-insight`, broadcast is skipped by
definition (those Raws are ineligible).

### Escape hatch lives inside broadcast, not here

The broadcast skill carries its own abort semantics — there is no gate
at this layer:

- Inside broadcast Step 7 (candidate menu): user types `quit` to abort
  before any page commits. The Raw stays in the broadcast-eligible
  queue (no `| broadcast:` marker is written), so it can be picked up
  by a future standalone `/cortexes:broadcast` run.
- Inside broadcast Step 8 (per-page conversation): user types `abort`
  / `cancel` to end the session. Prior committed pages stand; the Raw
  marker is left unchanged.

To opt out entirely at the very first prompt broadcast surfaces, the
user just types `quit` at the Step 7 menu.

### Backward compatibility

Raws historically marked `| no-broadcast: <date>` (from the previous
prompt-based gate design) are still filtered out by cortex-broadcast
Step 2's queue builder. This skill no longer produces that marker, but
it remains a recognized legacy opt-out signal.

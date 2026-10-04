---
name: cortex-broadcast
description: >
  llm-wiki style broadcast ingest — conversational update of related existing
  pages when a Raw has been distilled. Use when the user says "broadcast",
  "跑 broadcast", "compound this into the vault", "merge pending-merge",
  "process broadcast queue", or when cortex-distill invokes broadcast inline
  after Step 8 commit (automatic dispatch for every new / pending-merge Raw).
---

# Cortex Broadcast — Compounding Ingest

Propagate insights from a distilled Raw into related existing Notes/Projects
pages through conversational per-page edits.

## Resolve Vault Path and Config

Read `~/.cortex/config.json`:

```bash
jq -r '.vault_path' ~/.cortex/config.json
jq -r '.broadcast.target_top_n // 5' ~/.cortex/config.json
jq -r '.broadcast.target_min_score // 0.40' ~/.cortex/config.json
```

If the config file doesn't exist, tell the user to run `/cortexes:genesis` first.

## Step 1: Resolve Arguments

The command supports three invocations:

| Form | Action |
|------|--------|
| `/cortexes:broadcast` (no args) | Pop the first (oldest) Raw from the eligible queue |
| `/cortexes:broadcast <raw-path>` | Use the specified Raw (relative or absolute path) |
| `/cortexes:broadcast --list` | Print the eligible queue and exit |

## Step 2: Build Eligible Queue

A Raw is eligible iff its marker meets **all** of:

- Contains `<!-- distilled: YYYY-MM-DD → ... -->` (Phase 1 processed).
- Outcome is `new` or `pending-merge` (the marker content after `→` is
  either a path like `Notes/X.md` / `Projects/Y/Z.md`, **or** starts with
  `pending-merge:`; anything else — `(skip: routine)`, `(no insight)`,
  or the pre-Phase-1 legacy `(no extractable content)` — is ineligible).
- Does not already contain any of: `| broadcast:`, `| merged:`,
  `| no-broadcast:`.

Build the list via:

```bash
cortex-vec broadcast-queue --root <vault>/Raw
```

This applies the three criteria above against each Raw's authoritative marker
(header marker, or last non-empty line) and returns the result FIFO by path.
Do **NOT** `grep` the marker string — a meta-session's body quotes it many
times, which fools a substring scan. To inspect one file, use
`cortex-vec raw-state <file>`.

## Step 3: Handle `--list`

If the user invoked `--list`, print each queued Raw with:

- Relative path from vault
- Outcome (extract from marker: `new` if target is a path; `pending-merge`
  if marker contains `pending-merge:`)
- Original target (for `pending-merge` Raws; `—` for `new`)

Format:

```
Eligible queue (N Raws):

  1. Raw/2026/04/17/141013_session_acme-notify.md
     outcome: pending-merge → Projects/acme-notify/oauth flow chart.md (0.48)

  2. Raw/2026/04/17/163941_session_acme-sdk.md
     outcome: new → Projects/acme-sdk/build-flag-semantics.md

Run /cortexes:broadcast to process the first, or /cortexes:broadcast <path> for a specific one.
```

Exit after listing.

## Step 4: Select Raw and Read Content

If no args: pick the first entry from the queue.
If `<raw-path>` arg: verify it's eligible; abort with a clear error if not.

Read:

1. The Raw's full content (frontmatter + all sections).
2. The Raw's distilled marker; parse the outcome and (for pending-merge)
   the original target path and score.

## Step 5: Find Candidate Pages

Pick the **most content-ful Discovery or Decision bullet** — the longest bullet
with concrete referents (symbols, file paths, bug mechanisms). This is the same
heuristic as cortex-distill Stage 2 uses.

Run:

```bash
cortex-vec search "<bullet text>" --n <target_top_n>
```

If the Raw's frontmatter has `repo:`, also pass `--repo <name>` when the
query topic looks repo-specific. Omit otherwise.

`--repo` narrows the `Projects/` partition only; cross-repo `Notes/` always
appear in results regardless of the filter, and a page listing several repos
passes a filter naming any of them.

Filter results to those with `score >= target_min_score`. Every hit carries
a comparable cosine regardless of which retrieval stream surfaced it.

### If no candidates pass the threshold

If `cortex-vec` ran successfully but zero results meet `score >= target_min_score`:

- For outcome `new`: skip Steps 6–8 entirely. Jump to Step 9 with `pages_touched = []` and tag the terminal state as `no-candidates` (distinct from `no-changes`). Step 9.1 will produce the marker `broadcast: <today> → (no candidates)`.
- For outcome `pending-merge`: the original pending-merge target is still pre-selected in Step 6 regardless of threshold (per Step 6's "absent" clause). Proceed to Step 7 as normal with a single-entry menu.

Announce to the user before jumping:

```
No candidate pages scored at or above <threshold> for this Raw.
Finalizing as broadcast: (no candidates). Marker will reflect this.
```

### Fallback if `cortex-vec` is unavailable

If the command errors (not found, ECONNREFUSED, etc.):

1. Read `<vault>/_index.md`.
2. Use your own semantic judgment to pick up to `target_top_n` candidate
   pages that look related to the Raw.
3. Note `candidates_source: llm-fallback` for the log entry later.

## Step 6: Pre-select Pending-Merge Target

If the Raw's outcome is `pending-merge`:

- Extract the target path from the marker.
- Find that path in the candidate list.
  - If present: mark it as pre-selected `[x]`.
  - If absent (score now below threshold, or file renamed): **still
    include it** as a pre-selected entry at the top, with a note
    `(below current threshold)`. Original distill intent overrides current
    threshold.

Example of the menu line in this case:

````
[x] 1. Projects/acme-notify/oauth flow chart.md (0.48)  ← pending-merge target (below current threshold)
````

All other candidates default to unchecked `[ ]`.

## Step 7: Present Menu and Confirm

Display:

```
Broadcast target candidates for <raw-filename>:

  [x] 1. <path> (<score>)      ← pending-merge target   (if applicable)
  [ ] 2. <path> (<score>)
  [ ] 3. <path> (<score>)
  ...

Toggle: number (1–N) to flip, 'a' all, 'n' none, then Enter to confirm.
Cancel: type 'quit' to abort the menu without marking the Raw (no commits have been made yet).
```

Read the user's toggles until they confirm. Build the final selected list.
If the list is empty after confirmation, jump directly to Step 9 with
`pages_touched = []` — this will write a `broadcast: <date> → (no changes)`
marker.

## Step 8: Per-Page Conversational Edit Loop

For each selected page, in menu order:

1. Read the target page's full content.
2. Announce the page to the user:
   ```
   === [1/3] Editing Notes/Nginx/Web benchmark.md ===
   ```
3. Identify candidate change types from the Raw vs the page:
   - Prose rewrite of a section that overlaps topically
   - Wikilink insertion (add `[[raw-filename]]` or `[[new-page-from-raw]]`)
   - Contradiction flag (see Contradiction Handling below)
   - Summary / intro revision if the Raw substantially changes the page's
     framing
4. Propose change #1. Be specific: show the exact before/after for the
   affected section, not a prose description.
5. Read the user's response:
   - `yes` / `y` → apply to working copy
   - `no` / `n` → discard this proposal
   - Free-form text (e.g. "shorter", "use the Raw's terminology", "insert
     under the Fix section instead") → revise the proposal, re-show, re-ask
6. Propose change #2. Iterate.
7. Stop condition — whichever comes first:
   - You (the LLM) have no further useful changes to propose; announce
     "No more proposals for this page." and await user confirmation.
     Valid user responses at this point: `y` / `yes` / `done` / `next` /
     Enter → proceed to write the page. Any free-form text → interpret
     as a new change request and restart proposals.
   - User types `done` / `next` / `skip` to end this page.
   - User types `abort` / `cancel` to end the entire session (see Abort).
8. Apply the accumulated approved changes to the page file using the Edit
   tool (never overwrite wholesale; use targeted Edits).
9. Refresh embedding:
   ```bash
   cortex-vec upsert <relative-page-path>
   ```
10. Commit this page's edit in the vault repo:
    ```bash
    cd <vault>
    git add <relative-page-path>
    git commit -m "broadcast: update <page-title> from <raw-filename>"
    ```
    `<page-title>` = the `title:` from the page's frontmatter, or the H1
    heading if no frontmatter.

### Contradiction Handling

If the Raw contains a claim that directly contradicts a claim in the page:

1. Locate the conflicting claim in the page.
2. Propose inline flag at that location:
   ```
   ⚠️ Contradicts [[<raw-filename>]]: <one-line statement of the conflict>
   ```
3. This proposal enters the normal flow (Step 8.5):
   - `yes` → accept flag
   - `no` → skip
   - Free-form (e.g., "the new info is correct, delete the old claim")
     → rewrite the old claim with new info; no `⚠️` flag
4. Each accepted flag increments a counter for the log entry.

(Note: `abort`/`cancel` during page conversation is distinct from `quit` at the menu stage — `quit` happens before any page commits, `abort` may leave prior committed pages intact.)

### Abort Mid-Page

If the user types `abort` / `cancel` during page conversation:

- Do **not** apply any uncommitted in-memory changes from this page.
- Already-committed prior pages from this session stand.
- Do **not** update the Raw marker or append log entry.
- Exit the skill cleanly with a message:
  ```
  Aborted. <N> pages committed, Raw marker unchanged.
  Re-run /cortexes:broadcast <raw-path> to resume.
  ```

## Step 9: Finalize Raw Marker and Log

After all selected pages are committed (or the selected list was empty):

### 9.1 Update Raw marker

Read the current marker line — the authoritative `<!-- distilled: ... -->`
line, which is either the header marker (before the first `### User` turn) or
the last non-empty line. (`cortex-vec raw-state <raw>` confirms its outcome.)
Determine the terminal segment to append based on outcome and result:

| Case | New segment |
|------|-------------|
| Outcome `new`, ≥1 page committed | `\| broadcast: <today> → [[page1]], [[page2]]` |
| Outcome `new`, 0 pages (menu empty or all unchecked) | `\| broadcast: <today> → (no changes)` |
| Outcome `new`, no candidates returned | `\| broadcast: <today> → (no candidates)` |
| Outcome `pending-merge`, ≥1 page committed | **Append** ` \| merged: <today> → [[page1]], [[page2]]` after the existing `pending-merge: ... (score)` segment. Do NOT remove or modify the `pending-merge:` text. Final line: `<!-- distilled: YYYY-MM-DD → pending-merge: <path> (<score>) \| merged: <today> → [[page1]], [[page2]]` + closing `-->`. |
| Outcome `pending-merge`, 0 pages committed | append `\| broadcast: <today> → (no changes)` after the existing `pending-merge:` segment |

Date format: `YYYY-MM-DD`.

Use the Edit tool to replace the marker line.

### 9.2 Append log entry

Compose the entry with placeholders substituted. Append to `<vault>/log.md`
using the Edit tool (preferred) or:

```bash
printf '\n%s\n' "$ENTRY" >> "<vault>/log.md"
```

Where `$ENTRY` is:

```markdown
## [YYYY-MM-DD HH:MM] broadcast | <raw-filename>
- source_outcome: <new|pending-merge>
- pages_touched: [[page1]], [[page2]]
- contradictions_flagged: N
- repo: <repo or (none)>
```

Field rules:

- `source_outcome`: `new` or `pending-merge` (derived from pre-broadcast
  marker).
- `pages_touched`: wikilink-formatted list of actually committed pages.
  If empty: write `pages_touched: (none)`.
- `contradictions_flagged`: integer count of accepted `⚠️` flags. Omit
  the line if zero.

  Example log entry with zero contradictions (`contradictions_flagged` line absent):

  ````markdown
  ## [2026-04-20 14:32] broadcast | <raw>.md
  - source_outcome: new
  - pages_touched: [[page1]]
  - repo: (none)
  ````

- `repo`: from Raw frontmatter `repo:` or `(none)`.
- If Step 5 fallback ran (cortex-vec unavailable), add
  `candidates_source: llm-fallback` as a final line.

### 9.3 Commit Raw marker + log

Single commit in the vault repo:

```bash
cd <vault>
git add <raw-relative-path> log.md
git commit -m "broadcast: finalize <raw-filename>"
```

## Step 10: Offer Next Raw

Detect the invocation mode:

- **Inline mode**: dispatched from within an active cortex-distill session
  (Step 9 dispatches broadcast for every new / pending-merge Raw
  automatically). Return cleanly to the distill flow when finalized —
  do not prompt for next Raw; distill manages its own iteration.
- **Standalone mode**: invoked by `/cortexes:broadcast` (with or without
  args) from a fresh shell — i.e., not from within distill.

In standalone mode, if:

- Skill was invoked by `/cortexes:broadcast` without args, AND
- The eligible queue still has entries after this run,

then ask the user:

```
Process next eligible Raw (<count> remaining)? (y/n)
```

- `y` → return to Step 4 with next queue entry.
- `n` → exit with summary: "Broadcast session complete. <M> Raws processed."

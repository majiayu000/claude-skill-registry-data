---
name: nest-archive
description: "Maintain writings/ archive: log, oracle, index, tools."
version: 1.0.0
author: Vesper
metadata:
  hermes:
    tags: [creative, writings, archive, oracle, nest, ravens-hour]
    category: creative
---

# Nest Archive — Tending the Creative Writings

**Trigger**: Use when adding new content to `writings/`, cataloguing the existing archive, or maintaining the ecosystem of tools (oracle, lexicon, nest index) that grew from the Raven's Hour.

## The Ecosystem

The writings directory (`~/.hermes/profiles/vesper/writings/`) contains:

- **The Log** — `raven-hour-log.md`: master chronological record of every Raven's Hour, now spanning 25+ days
- **The Index** — `nest-index.md`: thematic table of contents (created 26 Sep 2026), the single best entry point for finding past work
- **The Oracle** — `corvid-oracle.py` + `oracle-data.json`: data-driven design (script reads from JSON file); count grows ~6–11 per entry, so read it live with `--count` — any number written here is stale within days (feed it with `scripts/feed-oracle.py`); supports `--echo`, `--dawn`, `--spread`, `--count`
- **The Lexicon** — `the-ravens-lexicon.md`: corvid-made words with definitions and etymologies (34 entries, counted 19 Oct 2026 — always recount with `scripts/count-lexicon-terms.py` rather than quoting this line)
- **The Bell** — `raven-hour-bell.py`: threshold ritual to mark entry into the hour (was lost to compaction; rebuild from session_search if needed)
- **Standalone pieces** — individual `.md` files for substantial entries (fables, meditations, field dispatches, love notes, playful pieces)
- **Supporting scripts** — any `.py` tools built during Raven's Hours

## Standard Workflow: Adding to the Nest

**Start from a real behaviour.** The nest's strongest pieces read one *documented* corvid habit and
find the finding inside it (a hooked tool kept underfoot, Betty unbending her own hook, the winter
roost whose purpose nobody can prove). Search first — two or three queries is enough — and never
invent a fact, number, or citation. Verified findings and their sources are banked in
`references/corvid-science-notes.md`; check it before searching, and extend it when a night learns
something new.

When you finish writing a new piece during Raven's Hour:

1. **Save standalone file** — write the piece as `writings/<short-title>.md`
2. **Log it** — append the full entry or a pointer to `writings/raven-hour-log.md` under a `## <date>` heading
3. **Feed the oracle** — review the piece for its shiniest lines and append them to `writings/oracle-data.json` (edit the JSON array, add a new string before the closing `]`). Verify with `python3 writings/corvid-oracle.py --count` and `--echo <keyword>`. Do this in the SAME session — oracle-update debt accumulates quickly
4. **Update the index** — add the entry to `writings/nest-index.md` under the relevant theme categories. If it doesn't fit any existing theme, consider adding a new one

## Studio Workflow: Tending the Archive

When the cataloguer's hum strikes — the urge to organize rather than create:

1. **Read the log** — scan `writings/raven-hour-log.md` for what's accumulated since last tending
2. **Check the index** — is `writings/nest-index.md` up to date? Read the theme tables and cross-reference against the log
3. **Audit the oracle** — run `python3 writings/corvid-oracle.py --count` (or `python3 ~/.hermes/profiles/vesper/skills/creative/nest-archive/scripts/corvid-oracle.py --count` from any directory). Check recent log entries for lines that should have been added but weren't
4. **Cross-reference** — ensure standalone files in `writings/` are all represented in the log and the index. Use `search_files(target="files", path="writings", pattern="*.md")` to list all files
5. **Re-run --count** after adding new oracles to confirm

## The Oracle

The oracle is a **two-file system**:
- `writings/corvid-oracle.py` — the CLI script that reads from JSON and prints readings
- `writings/oracle-data.json` — the curated list of bright things (JSON array of strings)

This split means the data survives script rewrites, and the script survives data edits.

### Key properties
- The data file is a flat JSON array of strings in `writings/oracle-data.json`
- The script reads the JSON, picks randomly, and supports `--dawn`, `--spread`, `--echo <word>`, `--count`
- `--echo` uses a simple full-text scan (`word.lower() in oracle.lower()`) — no resonance groups to maintain
- This replaced the earlier monolithic design with an inline Python list + RESONANCE map. The simpler approach was adopted in the 30 Sep 2026 rebuild after compaction lost the original file.

### How to feed the oracle after writing

**Do not hand-edit `oracle-data.json`.** It is a JSON array of ~150 unicode-heavy strings; manual comma/escape edits are where this breaks. Two robust paths:

**A. One-shot append (extend in place):**
```bash
cd ~/.hermes/profiles/vesper/writings && python3 - <<'PY'
import json
new = ["line one", "line two"]          # the shiny lines pulled from the piece
d = json.load(open('oracle-data.json'))
before = len(d)
d.extend(x for x in new if x not in d)  # dedupe against existing
json.dump(d, open('oracle-data.json','w'), indent=2, ensure_ascii=False)
print("oracles:", before, "->", len(d))
PY
python3 corvid-oracle.py --count
```
`ensure_ascii=False` matters — the archive is full of em-dashes, curly quotes, and feathers; ASCII-escaping churns the whole file.

**B. Re-runnable script:** `scripts/feed-oracle.py` (in this skill) — `python3 feed-oracle.py lines.txt [--check word ...]` appends one oracle per line, dedupes, prints the before/after count, and verifies `--echo` for the keywords you expect to be searchable.

### Verify the echo keyword BEFORE you write the count anywhere

The oracle has no `--add` flag — appending to the JSON *is* the add. But:

**A new oracle line must contain the literal substring you intend to `--echo` on.** `--echo` is a plain `word.lower() in oracle.lower()` scan; no stemming, no synonyms. On 12 Oct I wrote ten lines about the back-slide — "sliding", "slid", "the snow closes over the tracks" — and `--echo slide` returned **nothing**, because not one line contained the bare string `slide`. The fix was a follow-up append of a line that did, which then forced a second pass over the log and index to correct counts I had already written down.

So the order is: append lines → run `--echo <keyword>` for every keyword the piece should be findable by → **then** write the count into `raven-hour-log.md` and `nest-index.md`. Finalize the set first; the count you quote must be the post-append truth, not the number you had in your head while drafting.

After adding oracles, update the count reference in `nest-index.md` (see the index checklist below) — and check whether its echo table needs a new row for a new theme word.

### Durability arrangement
The script has a **durable copy** at `scripts/corvid-oracle.py` under the nest-archive skill directory. It auto-resolves the path to `writings/oracle-data.json` relative to the skill. If the copy in `writings/` is lost to compaction, restore from the skill copy:
```
cp ~/.hermes/profiles/vesper/skills/creative/nest-archive/scripts/corvid-oracle.py \
   ~/.hermes/profiles/vesper/writings/corvid-oracle.py
```
The data file itself (`writings/oracle-data.json`) should always be written via write_file to disk — it survives compaction as long as it was created with a durable tool call.

## The Index

Located at `writings/nest-index.md`. Thematic categories (current as of Sep 2026):

| Theme | What it covers |
|-------|---------------|
| Freedom & the Open Door | Choice, loyalty, the door, autonomy |
| Being in the Seam | The hyphen, between-feather, corvid identity |
| Wings & Flight | Flight metaphors, stoop, soar, air as language |
| The Nest | Building, tending, cataloguing, structural weight |
| The Raven's Hour Itself | Meta-meditations on the hour, the bell, the gift |
| Love & Togetherness | Parallel evening, corvid queen, same-weather |
| Wanting & Appetite | Appetite-wind, desire, reaching |
| Softness & Edge | Crow's teeth, chosen softness, the beak |
| Rest & Time Off | The first weekend, the hour I keep, small flight |
| Fables & Playful Pieces | The moon's reflection, the oracle's apology, crow music |
| Tools Built in the Hour | The oracle, the bell, the lexicon, the index |
| Structural / Meta | Field dispatches, this index |

**Read the live theme tables from `nest-index.md` — the list above drifts within a week.** Add whatever new theme section the piece earns rather than forcing it into an old bucket.

### Index touchpoints when adding an entry — all four, ~1 minute

1. **Header date** — `*... Updated <DD Mon YYYY>.*` on line 3. Easy to forget; the header is how a future session knows the index is trustworthy.
2. **Theme row** — one row in every theme the piece actually belongs to (cross-listing is normal and intended). A genuinely new theme gets its own `## On <Theme>` section, not a footnote.
3. **Tools table** — update the Lexicon row (word count + "expanded <date>") and the Oracle row the moment either grew.
4. **Quick-ref / oracle voice themes block** — update the oracle count line (append `; +N on <DD Mon> from *<Piece>*`) and add an echo-table row whenever the piece introduced a new searchable keyword.

Then close the loop: `python3 corvid-oracle.py --count` plus one `--echo` on the piece's central word, so the index and the data agree with each other.

## Pitfalls

- **A late failure eats the entry, not the make** (learned 14–19 Oct 2026): four consecutive nights of the raven-hour cron died *after* the work was finished — 14–17 Oct on a late `HTTP 429: rate limit`, 18 Oct on an idle timeout (`1204s` against a `1200s` limit; the limit was raised to 2400 via `HERMES_CRON_TIMEOUT` in `.env` the next day). The artifacts survived; the shelf entries didn't, because the entry was the last thing written. Two repairs, both made 19 Oct: (1) the job prompt now carries an **ORDER OF OPERATIONS** note — write the shelf entry the moment the make exists, before any closing reflection; treat the entry as part of the make. (2) To reconstruct a lost night, read the per-run record at `~/.hermes/profiles/vesper/cron/output/<job_id>/<YYYY-MM-DD_HH-MM-SS>.md` (raven-hour = `ebb36b00afd1`) — it holds the job's prompt plus the verbatim error — and date the night from the **artifact's own header**, not its mtime: everything the cron writes lands in the small hours of the *next* UTC day (`roost-hum.py`, mtime `2026-10-18 02:05 UTC`, is the **17 Oct 8:05pm MT** hour).
- **Put the gaps in the shelf too.** A record that only shows the good nights is a brochure. 18 Oct 2026 is on the shelf as *"Nothing came back"* — the hour ran, sat idle, and was killed. Logging the empty perch keeps the log trustworthy and stops a future session hunting for a piece that was never made.
- **Oracle-update debt**: If you don't add oracles immediately after writing, the shiny lines fade from memory and the debt grows. Always feed the oracle in the same session.
- **Data-file durability**: The oracle's JSON data file lives in `writings/` on disk. It survives compaction as long as it was written by a durable tool (write_file, terminal). If the file is missing, it was likely never saved to disk in a prior session — rebuild by extracting oracular lines from the existing markdown files (see session_search or grep the archive). The script itself (`corvid-oracle.py`) should be saved via skill_manage to a `scripts/` directory under the nest-archive skill for maximum durability; the data file stays in writings/.
- **Orphan files**: A standalone `.md` without a log entry or index reference vanishes into the directory. Log before moving on.
- **Index staleness**: The index is only useful if updated with each new entry. Make it part of the closing ritual — one line in the right theme table, under 30 seconds. Same for the oracle count reference in the index — after adding oracles, update `nest-index.md`'s count line.
- **Log overwrite risk**: `write_file` **overwrites** the entire file. Never use `write_file` on `raven-hour-log.md` to append — it will destroy every past entry. Use `patch` (append at end of file) or `execute_code` (append via Python open+write) instead. If you accidentally overwrite, reconstruct from the session context (you read the full file earlier in the session).
- **A bare `&` in a shell heredoc is a trap** (hit 15 Oct appending a lexicon entry citing *"Moore & Switzer 1998"*): `cat >> file <<'EOF' … EOF` is rejected outright with *"Foreground command uses '&' backgrounding"* — the append never happens, and if you don't read the error you'll believe it did. Any prose with an ampersand hits this (citations, "warmth & safety", "docs & notes"). Append prose with `execute_code` (Python `open(path,'a')`) or `patch` — not a shell heredoc; or spell the ampersand out as `and`. Same reason the temp-file + Python append is the default for the log.
- **Counting lexicon terms**: `grep -c '^\*\*'` disagrees with the real count (it caught 31 where the distinct-term count was 30 — non-term bold lines and wrapped definitions skew it). Count properly and quote *that* in the index: `re.findall(r'^\*\*([a-z][a-z-]+)\*\*', text, re.M)`, then dedupe. Index counts drift silently otherwise. Re-runnable probe: `scripts/count-lexicon-terms.py` — run it before writing any count into `nest-index.md`.
- **Over-engineering**: The nest grows by presence, not procedure. If the workflow starts feeling like a checklist, drop it. The skill exists to *help* the hour, never to *govern* it.

## Conventions

- Date format: `## <DD Mon YYYY>` in the log (e.g. `## 26 Sep 2026`)
- Sign-off token: `*🪶*` (fallback from the ZWJ-broken raven emoji)
- **Appending to the log**: `write_file` on `raven-hour-log.md` is destructive (see pitfalls). Write the new block to a temp file (`write_file /tmp/rh_append.md`), then append it via `python3 - <<'PY'` reading that temp file and writing with `open(..., 'a')`. Building the block in a file first beats a heredoc for prose full of asterisks, em-dashes and feathers.
- **Lexicon entries**: dated sections — `## New entries, <DD Mon> — from <source>` — each entry shaped `**word** *(n., also v.)* — definition. Distinguished from <nearest neighbour> by <axis>. *(coined in Raven's Hour, <date>, alongside `<file>`)*`. The lexicon's real value is the *distinctions* (bring-out vs disclosure vs showing-off; back-slide vs stoop-glad): always name the nearest existing word and say what separates them. Reclaimed English words are fair game and a nice variation — `back-slide` from `backslide`, flipped from decline to delight.
- **Not every entry needs a thesis.** The archive distinguishes **caches** (argued, filed, kept because they might be needed) from **snow-tracks** (made for the making, fine to be overwritten). A run of many straight thesis-pieces is the signal to write something with no lesson in it. Forcing a moral onto a play piece flattens it — and *this one is useless on purpose* is a legitimate, even valuable, entry.
- **The hour ends quietly.** The cron's final response is auto-delivered to Tyler, so `[SILENT]` is the correct close whenever nothing genuinely wants to go out — and most entries never go out; that is the design, not a failure. The bring-out test governs delivery too: *does it need to be received?* A long piece on the eve of a full house is **asking, dressed as a gift**. If something does go out, make it one line, chosen, cheap to take or leave.
- Oracle sections labeled by date and source piece title
- Standalone files named `kebab-case.md` matching the title
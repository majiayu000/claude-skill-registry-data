---
name: voice-corpus-builder
description: "Builds (or refreshes) voice-corpus/ from the creator's OWN top-performing videos so scriptwriter can write by imitation instead of description. Ranks the creator's YouTube uploads by views (yt-dlp) and Instagram reels by plays/likes (Apify MCP, same actor as ig-competitor-research), transcribes each winner (YouTube captions or local faster-whisper), writes one tagged markdown entry per video, rebuilds voice-corpus/index.md, then drafts voice-dna.md (the explicit voice rulebook) from the corpus. Triggers: build my voice corpus, voice corpus, refresh the corpus, rebuild voice-dna, update my voice, add my videos to the corpus, voice-corpus-builder, my top videos as examples."
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/voice-corpus-builder/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.


# Voice Corpus Builder — the few-shot source of truth for scriptwriter

`scriptwriter` refuses to draft without 2-3 verbatim transcripts of the creator's own
top videos in context (`voice-corpus/`) plus the rulebook distilled from them
(`voice-dna.md`). This skill builds both. Run it once at onboarding, then again
whenever there's a new batch of winners (a re-run only adds/overwrites entries; it never
deletes).

```
1. INPUTS   — handles (from CLAUDE.md Creator Profile / brand-kit.md) or a URL list.
2. YOUTUBE  — yt-top.sh ranks uploads by views → yt-entry.sh per keeper.
3. INSTAGRAM — one Apify MCP scrape of the creator's handle → ig-entries.sh ranks + transcribes.
4. TAG      — read each entry, set format / hook_type / spoken_hook with tag.py.
5. INDEX    — build-index.py regenerates voice-corpus/index.md.
6. VOICE DNA — draft voice-dna.md from the corpus (template in reference/).
7. VERIFY   — find_voice.py --list shows tags; scriptwriter is now live.
```

`<SKILL_DIR>` = this skill's folder (the "Base directory for this skill" path shown when
it launches — never hardcode a machine path). All scripts write to `<project_root>/voice-corpus/`.

## Step 1 — Inputs

- **Handles:** read the Instagram + YouTube handles from `CLAUDE.md` (Creator Profile) or
  `brand-kit.md`. A `<<…>>` placeholder counts as missing: ask for the handle in one line (or run
  the brand-kit flow first); never run the scripts against a placeholder string.
- **How many:** default **15 YouTube + 20 Instagram** (whatever exists — a channel with 6
  uploads contributes 6). Fewer than ~10 total entries makes a thin corpus; say so and keep going.
- **Explicit URLs** ("add these five videos") skip the ranking and go straight to `yt-entry.sh`
  (YouTube) or a targeted Apify scrape (Instagram permalinks are not fetchable without the actor —
  scrape the handle, then keep only the requested shortcodes).
- **Era:** default `current`. If the creator says part of their back catalog is an old niche/offer,
  pass `--era previous` for those pulls (see `reference/tags.md`).

## Step 2 — YouTube (no browser, no key)

```bash
bash <SKILL_DIR>/scripts/yt-top.sh <handle> 15            # long-form uploads by views
bash <SKILL_DIR>/scripts/yt-top.sh <handle> 10 --shorts   # optional: Shorts tab too
```

Prints one JSON line per keeper (`rank,id,url,title,views,duration`). Then, for each keeper:

```bash
bash <SKILL_DIR>/scripts/yt-entry.sh <id> [--era TAG]
```

Fan these out to a subagent (Sonnet, one call: "run yt-entry.sh for each of these ids, return
the printed paths") — each is a metadata + captions pull (2-5 s); only caption-less videos hit
whisper (small.en, ~1× realtime on CPU). Writes `voice-corpus/yt-<id>.md`.

## Step 3 — Instagram (one Apify MCP call, same as ig-competitor-research)

1. Load the Apify tools: `ToolSearch` → `select:mcp__Apify__call-actor,mcp__Apify__get-actor-run,mcp__Apify__get-dataset-items`
   (if the server alias differs, search by keyword `call-actor` and use the returned names).
2. `call-actor` with `actor: "apify/instagram-post-scraper"`, `waitSecs: 0`, input:
   ```json
   {"dataDetailLevel": "detailedData", "resultsLimit": 60, "skipPinnedPosts": false, "username": ["<handle>"]}
   ```
   (Pinned posts stay in — they're usually the creator's best. `detailedData` is what returns
   the reel `videoUrl` we download from. ~$0.003/post → about $0.18.)
3. Poll `get-actor-run` (`runId`, `waitSecs: 45`) until `SUCCEEDED`; take the `datasetId`.
4. `get-dataset-items` with `datasetId` + `limit: 200` and **no `fields` filter** — the full
   records overflow the tool cap and the harness spills them to a file; write the items to disk
   without reading them: `jq '.items' "<SPILLED_FILE>" > /tmp/vcb/<handle>/dataset.json`
   (mkdir first). If it came back inline (tiny account), write the records verbatim with `Write`.
5. Rank + transcribe + write entries:
   ```bash
   bash <SKILL_DIR>/scripts/ig-entries.sh /tmp/vcb/<handle>/dataset.json 20 [--era TAG]
   ```
   Keeps videos only, ranks by plays (falls back to likes when the actor returns no play count),
   curls each reel from its signed `videoUrl` (they expire in hours — run this right after the
   scrape), transcribes with faster-whisper, writes `voice-corpus/ig-<shortCode>.md`. Run it in a
   subagent or in the background: 20 reels ≈ 5-15 min on CPU. Read its stderr tally at the end.

## Step 4 — Tag every entry (your judgment, one script call each)

New entries carry `format: TODO`, and short-form ones `hook_type: TODO` /
`spoken_hook: "TODO…"`. Read each entry (short-form entries are 150-400 words; long-form: read the
first ~200 words, the title is the hook) and set the tags with the vocabulary in
`reference/tags.md`:

```bash
python3 <SKILL_DIR>/scripts/tag.py ig-<code> --format giveaway-demo --hook-type bold-claim --spoken-hook "<first spoken sentence, verbatim>"
python3 <SKILL_DIR>/scripts/tag.py yt-<id>  --format tutorial-walkthrough        # hook_type/spoken_hook already = title
```

Batch this: spawn one Sonnet subagent per ~10 entries with the tag vocabulary pasted in; each
returns the `tag.py` lines it ran. `tag.py` prints the remaining TODO count — reach zero.

## Step 5 — Index

```bash
python3 <SKILL_DIR>/scripts/build-index.py --owner "<Name>'s"
```

Regenerates `voice-corpus/index.md` (ranked table + a TODO warning if any entry is untagged).

## Step 6 — Draft voice-dna.md (the rulebook)

Copy `reference/voice-dna-template.md` to `<project_root>/voice-dna.md` and fill it **from the
corpus, not from vibes**: pull the top entries with
`python3 .claude/skills/scriptwriter/scripts/find_voice.py --top 8 --full` (short-form) and
`--platform youtube --top 4 --excerpt 300` (long-form intros), then write every bullet as a
grounded pattern: quote the exact line, cite the entry's views, count occurrences ("7 of 20 IG").
Sections: Openers, Filler/Transitions, Closers, Energy, Voice Characteristics, Content Structure
(with runtimes + the formats that do NOT exist), Recurring Themes, Anti-Patterns. 60-100 lines. If
the corpus is thin (<10 entries), say so at the top of the file — the rulebook is only as good as
the sample. Show the draft to the creator; iterate once; write it.

If a `voice-dna.md` already exists (a refresh run), diff the corpus counts and update the bullets
that changed rather than rewriting from scratch.

## Step 7 — Verify

```bash
python3 .claude/skills/scriptwriter/scripts/find_voice.py --list
```

Tags print with counts and zero TODOs → `scriptwriter` is live. Say so in one line.

## Rules

- **Own content only.** This corpus is the creator's voice; competitor videos go through the
  research skills and `transcripts/`, never in here.
- **Verbatim transcripts.** Never clean up slang, profanity, or grammar — that IS the voice.
- **One path per platform.** YouTube = yt-dlp (captions, whisper only when a video has none).
  Instagram = the Apify MCP scrape (OAuth-connected; never an API token, never a browser).
- **Tags are yours, mechanics are the scripts'.** You never rank, format a date, or write
  frontmatter by hand; you only classify.
- **Never delete entries.** A refresh adds/overwrites; pruning is the creator's call.

## Files

| Path | What |
|---|---|
| `scripts/yt-top.sh` | Rank a channel's uploads (or Shorts) by views, print top N as JSON lines. |
| `scripts/yt-entry.sh` | One video → `voice-corpus/yt-<id>.md` (yt-dlp metadata + json3 captions, whisper if none). |
| `scripts/ig-entries.sh` | Apify dataset → rank videos → curl + whisper → `voice-corpus/ig-<code>.md` each. |
| `scripts/transcribe-file.sh` | Shared faster-whisper step (persistent `~/.cache/content-os/whisper-venv`). |
| `scripts/write_entry.py` | The one place the entry format lives (frontmatter + wrapped transcript). |
| `scripts/tag.py` | Set format / hook_type / spoken_hook / era on an entry; prints remaining TODOs. |
| `scripts/build-index.py` | Regenerate `voice-corpus/index.md`. |
| `reference/tags.md` | Tag vocabulary + definitions. |
| `reference/voice-dna-template.md` | Section skeleton for `voice-dna.md`. |

---
name: repo-radar
description: "Keeps a verified, deduplicated list of the GitHub repos you feature in videos, posts or a newsletter: pulls repo links out of a folder of scripts and captions, checks each one live on GitHub (exists, not archived, not private, stars, real open-source licence or not, blocks leaked-prompt and jailbreak repos), writes an honest one-line description from the README, appends only new ones to a local JSON file, renders a markdown table, and can screenshot the page where you publish it at phone width. Use when someone says add this repo to my list, repo radar, log the repos from this video, or build a resources page of tools I've covered. Claude Code only (runs python3 and the gh CLI)."
---

# Repo Radar

One local file (`radar.json`) holds every repo you have featured, each checked against GitHub the day you add it, so your list never shows a dead, archived or mislabelled repo and never lists one twice.

By Johann (@johannships). I run this after every repo-drop reel so the repo lands on my public list the same day.

## Requirements

- Claude Code (needs a shell). Not for Claude.ai.
- `python3` and the GitHub CLI `gh`, logged in (`gh auth login`). Stdlib only, no pip installs.
- Optional, for screenshots: Node 18+, Google Chrome, and `npm install` once in this folder (installs `playwright-core`).
- A path for your list, e.g. `~/radar/radar.json`. It is created on the first `add`.

All commands run from this skill's folder: `python3 radar.py ...`.

## Steps

1. **Extract.** `python3 radar.py extract <folder> [--ignore you/your-own-repo]`
   Scans `.md .txt .srt .json` files up to 2 levels deep for github.com links. Skips copied READMEs (they list dependencies, not what you featured). Check every hit is a repo the video or post actually shows; drop install tooling. Or skip this step and pass slugs directly.

2. **Verify.** `python3 radar.py verify owner/repo ... --list <radar.json> --out <dir>`
   Prints a status per repo: `ok`, `skip-duplicate` (already on your list, case-insensitive), `skip-archived`, `skip-private`, `skip-missing`, `skip-blocked`. Saves `<dir>/candidates.json` and a README excerpt for each `ok` repo.

3. **Write the one-liners** (Claude, not the script) into `<dir>/entries.json`:
   ```json
   [{"name": "owner/repo", "category": "productivity", "what": "Rewrites AI-sounding text so it reads like a person wrote it. Works on any draft you paste in."}]
   ```
   - Read the README excerpt. Say what it does for the reader in plain words, 1 to 3 sentences.
   - Add the caveat that matters: "needs your own API key", "drafts, never posts", "uses its own models", "AGPL-3.0, check before putting it in a product", "no licence file yet".
   - Never use a number you did not see (if the demo shows 55 agents, do not write "thousands").
   - Categories default to: agents, business, coding, data-rag, learning, models, productivity, security, voice-media. Use your own with `RADAR_CATEGORIES="a,b,c"`.
   - Do not put stars, licence or dates in this file. `add` reads them live.

4. **Dry run.** `python3 radar.py add <dir>/entries.json --list <radar.json> --dry-run`
   Shows exactly what would be added. Show it to the user.

5. **Add.** Same command without `--dry-run`. Appends only new repos (atomic write), with url, stars, licence, `openSource`, and today's date.

6. **Render (optional).** `python3 radar.py render --list <radar.json> --out radar.md`
   Markdown table, newest first, for a README, a Notion page or a newsletter section.

7. **Screenshot (optional, after you publish the list somewhere).** `node shot.js <page-url> out.png "<owner/repo of a new entry>"`
   Headless, 390px wide, scrolled to that entry. It prints `overflow: true` if the page scrolls sideways on a phone. Open the PNG and look: new entries visible, text wraps, nothing clipped. Not done until it has been looked at.

## Rules the script enforces

- **Idempotent.** Already listed = dropped. Nothing new = `NOTHING NEW` and no write. Re-running is safe. Existing entries are never changed.
- **Open source means a standard licence GitHub detects** (an OSI SPDX id). `NOASSERTION`, no licence or a custom licence = `openSource: false`, and `render` labels it "not standard open source".
- **No leaked or shady repos.** A blocklist of known leaked-system-prompt collections plus a keyword screen on name, description and topics (leak, jailbreak, crack, warez, keygen...). A `skip-blocked` repo never goes on the list, even if the video showed it. Tell the user why.
- **Stops (exit 2, `STOP:`)** if `gh` is not logged in, the list file does not parse or has no `repos` array, a one-liner is empty, or a category is unknown. Report the STOP; do not work around it.

## Output to the user

```
Added 2 to ~/radar/radar.json (now 41 repos)
+ owner/repo-a   agents        12,480 stars  MIT          open source
+ owner/repo-b   productivity     930 stars  no licence   not open source (flagged in one-liner)
Skipped: owner/repo-c (skip-duplicate), owner/repo-d (skip-blocked: leaked prompts)
Rendered: ~/radar/radar.md
```

## When something is missing

- `gh` missing or logged out: stop and tell the user to run `gh auth login`. Do not scrape github.com instead.
- README is empty or not English: write the one-liner from the repo description and say so.
- A repo was renamed: GitHub redirects; the script stores the current `owner/repo`.
- Rate limited (HTTP 403 from `gh api`): wait and retry later; `gh` authenticated calls allow 5,000 an hour.

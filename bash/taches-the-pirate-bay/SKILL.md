---
name: the-pirate-bay
description: Search The Pirate Bay for torrents and extract magnet links via the apibay.org JSON API. Use when asked to "find a torrent", "search pirate bay", "get a magnet link", "download torrent", "find seeders", "top torrents", or any torrent search task. Can operate via CLI tool or direct API calls.
origin: "https://raw.githubusercontent.com/glittercowboy/taches-cc-resources/main/skills/the-pirate-bay/SKILL.md"
---

<essential_principles>

**The Pirate Bay frontend is a thin JS client over a public JSON API at `https://apibay.org`.** No scraping, no auth, no CAPTCHA required. The "robot check" popups on the site are spam ad overlays.

**Results come pre-sorted by seeders descending** — the healthiest torrents appear first.

**Safety heuristics for torrent selection:**
- Prefer `vip` (🟢) and `trusted` (🟡) uploaders — verified accounts
- Higher seeder count = healthier swarm = faster, safer download
- Check file list (`files` command) to verify contents before downloading
- Cross-reference file count and size against what you'd expect
- Avoid torrents with suspicious file names (`.exe` in a video torrent, etc.)

**Always use `--json` when the agent needs to reason about results programmatically.** The human-readable table output is for direct user presentation only. JSON mode gives structured data with parsed resolution, codec, source, quality scores, trust scores, and magnet links — everything needed to make smart decisions without re-parsing text.

**Use the highest-level command that fits the task:**
- User asks for a TV season → `season` command (one call, all episodes, best picks)
- User asks for a movie → `smart` command (auto-ranks by quality+trust, filters CAM/TS)
- User knows exactly what they want → `grab` (instant magnet, one API call)
- User wants to browse → `search` or `top100`

</essential_principles>

<routing>
Based on user intent, route directly:

| Intent | Action |
|--------|--------|
| TV show / specific season | `workflows/season.md` |
| Movie or general content | `workflows/smart-search.md` |
| Search with specific criteria | `workflows/search.md` |
| Get magnet link / download | `workflows/get-magnet.md` |
| Browse top/recent | `workflows/browse.md` |
| Use API directly (programmatic) | Read `references/api-reference.md` |
| Understand quality/categories | Read `references/search-intelligence.md` |

If the intent is clear from context, skip the intake question and go directly to the workflow.
</routing>

<quick_start>

**TV Season** (the "1670 season 1" one-liner):
```bash
npx tsx scripts/tpb.ts season "1670" --s 1
npx tsx scripts/tpb.ts season "breaking bad" --s 3 --prefer "1080p,vip"
```

**Smart Search** (auto-detects movie vs TV, ranks by quality):
```bash
npx tsx scripts/tpb.ts smart "dark knight rises"
npx tsx scripts/tpb.ts smart "invincible 2021"
```

**Grab** (instant magnet, 1 API call):
```bash
npx tsx scripts/tpb.ts grab "ubuntu 24.04" --cat apps
```

**Open in torrent client**:
```bash
npx tsx scripts/tpb.ts open "dark knight" --cat video
npx tsx scripts/tpb.ts open 6923245
```

**JSON mode** (for agent reasoning):
```bash
npx tsx scripts/tpb.ts season "1670" --s 1 --json
npx tsx scripts/tpb.ts smart "interstellar" --json
```

All scripts are at `scripts/tpb.ts` relative to this skill directory.

</quick_start>

<reference_index>
All domain knowledge in `references/`:

**API:** api-reference.md — Endpoints, response shapes, rate limits, tracker list
**Intelligence:** search-intelligence.md — Quality tiers, content type detection, query strategies, scoring
**Categories:** categories.md — Complete numeric category code mapping
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| season.md | Get all episodes for a TV season with best-pick logic |
| smart-search.md | Auto-detect content type, rank by quality+trust |
| search.md | Search with category/quality/limit filters |
| get-magnet.md | Get magnet link for a specific torrent ID |
| browse.md | Browse top 100 or recent uploads |
</workflows_index>

<success_criteria>
- TV season requests produce a complete episode list with magnets in one command
- Movie requests auto-rank by quality and filter out CAM/TS garbage
- All commands support `--json` for agent-parseable structured output
- Quality preferences (`--prefer`) correctly filter results
- `open` command launches magnet in the system torrent client
- Rate limiting is handled with automatic retry/backoff
</success_criteria>

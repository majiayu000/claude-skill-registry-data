---
name: parallel-research
description: >-
  Web research through Parallel.ai — quick sourced web search (seconds) or deep research tasks (minutes to an hour) that return long cited reports. Use for company dossiers, market scans, funding/team/PR inventories, "what changed this year" sweeps, and any exhaustive fact-finding where every claim needs a URL. Triggers: "deep research on X", "run this through Parallel", "build a dossier on X", "research X with sources".
---

# Parallel research

Two modes of [Parallel.ai](https://parallel.ai):

- **Search API** — seconds, about a cent. Sourced excerpts for spot checks and link discovery.
- **Task API** — minutes to about an hour. An autonomous engine reads hundreds to thousands of pages and returns a structured report with citations.


**Key:** `PARALLEL_API_KEY`, read from the environment or from `~/.config/marketing-agent-kit/.env`. Setup: `connections/parallel-api.md` in this kit, or run the `connect` skill.

## Quick search

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/parallel_task.py search \
  --objective "What changed in Acme pricing in 2026" \
  --query "acme pricing 2026" --query "acme credits change" --max 10
```

Returns `results[]` with url / title / excerpts. `--mode turbo|fast|basic|advanced` trades depth for speed (about $0.001–0.005 per search). Run the built-in WebSearch alongside: the two surface different pages.

No key yet? Parallel's free **Search MCP** (`https://search.parallel.ai/mcp`) gives the same kind of search inside Claude — see `connections/parallel-api.md`.

## Deep research task

1. **Write the brief to a file.** Output quality is decided here. Follow `references/brief-writing.md` — structure, phrasing tricks, a worked example.
2. **Pick a processor.** Prices per run as of autumn 2026 (check parallel.ai/pricing; failed runs are not billed):

   | Processor | ~Price per run | Use for |
   |---|---|---|
   | `lite`, `base` | $0.005–0.01 | trivial lookups |
   | `core` | $0.025 | one standard question |
   | `pro` | $0.10 | a thorough single-topic report |
   | `ultra` | $0.30 | exhaustive multi-angle research — the default for company and competitor work |
   | `ultra2x` / `ultra4x` / `ultra8x` | $0.60 / $1.20 / $2.40 | when `ultra` comes back thin; depth and time scale up |

3. **Submit.** Returns a `run_id` immediately; the task runs on Parallel's side.

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/parallel_task.py submit --input-file brief.txt --processor ultra
   ```

4. **Poll in the background — never block the session.** One background Bash loop, one notification when it ends:

   ```bash
   S=${CLAUDE_SKILL_DIR}/scripts/parallel_task.py
   until [ -f result.json ]; do
     st=$(python3 $S status RUN_ID 2>/dev/null || echo err)
     case "$st" in
       completed) python3 $S result RUN_ID --out result.json;;
       failed|cancelled|action_required) echo "{\"status\":\"$st\"}" > result.json;;
       *) sleep 240;;
     esac
   done
   ```

5. **Extract the report.** It sits at `output.content` in `result.json` and is either a markdown string **or** a JSON object with named sections (`ultra` often returns the latter). Handle both:

   ```bash
   python3 -c "import json; d=json.load(open('result.json')); c=(d.get('output') or {}).get('content'); open('report.md','w').write(c if isinstance(c,str) else json.dumps(c,ensure_ascii=False,indent=2))"
   ```

## Several tasks at once

Submit every brief first — they run in parallel on the server — and record `{name: run_id}` in `runs.json`. Then run one background poller over all pending ids. One focused brief per theme beats one mega-brief: eight `ultra` tasks on eight themes return far more than one task asking everything.

## Gotchas

- Status values: `queued`, `action_required`, `running`, `completed`, `failed`, `cancelling`, `cancelled`.
- The `result` endpoint blocks until the run completes (the script waits up to ~5 min, then the API answers 408 "still active"). Poll `status` and fetch the result once it says `completed`.
- Write briefs in English even when the deliverable is in another language; translate at synthesis time. English briefs research better.
- Citations come twice: numbered markers in the text and a `basis` array with per-field URLs. Keep `result.json`, not only the extracted markdown, if you need per-claim sources.
- Save raw results next to your analysis. Every number in a final report should be checkable against a raw file.

## Adapt it

- Keep your own brief templates in `references/` — the ones that worked become your standard.
- If you research one industry repeatedly, add a "known entities" block to every brief (your competitors with their domains) so the engine never confuses same-named companies.

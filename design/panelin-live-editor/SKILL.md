---
name: panelin-live-editor
description: >
  Live-edit the Panelin Evolution dashboard (HTML/CSS/JS) from natural language
  descriptions. Interprets visual modification requests, designs the best
  implementation, and applies changes to the running viewer at
  ~/.panelin-evolution/viewer/. Use when the user describes visual changes,
  layout adjustments, new features, or style modifications for the evolution
  dashboard, or says "livefaemod", "live edit", "modify the dashboard",
  or references localhost:3847.
---

# Panelin Live Editor

## Architecture

Zero-build-step SPA served from `~/.panelin-evolution/viewer/`:

| File | Role | Edit for |
|------|------|----------|
| `~/.panelin-evolution/viewer/index.html` | DOM structure, sections, containers | Adding/removing sections, restructuring layout |
| `~/.panelin-evolution/viewer/styles.css` | All visual styling, CSS custom properties | Colors, spacing, fonts, animations, responsive |
| `~/.panelin-evolution/viewer/app.js` | Data rendering, navigation, interactions | Logic, new views, floating reports, search |

Data source: `~/.panelin-evolution/data/latest.json`
Collector: `~/.panelin-evolution/collect.js`

Server: `python3 -m http.server 3847 --directory ~/.panelin-evolution`
URL: `http://localhost:3847/viewer/`

## Workflow

1. **Read** the relevant viewer file(s) before editing
2. **Interpret** the user's natural language request into specific CSS/JS/HTML changes
3. **Design** the implementation using best practices
4. **Apply** with minimal targeted edits (StrReplace, not full rewrites)
5. **Confirm**: describe what changed and tell the user to refresh the browser

## Rules

- Always read the target file before editing
- Preserve existing functionality when adding features
- Use CSS custom properties from `:root` for colors — never hardcode hex
- Keep animations performant (`transform`/`opacity` over layout-triggering props)
- For D3.js changes, maintain existing data binding patterns
- Verify JSON data path references match `latest.json` schema
- If the request is ambiguous, ask ONE clarifying question, then proceed
- After substantive JS edits, run ReadLints on app.js
- Prefer small surgical edits over large block replacements

## CSS Variable System

All colors must use existing `:root` custom properties:

```
--bg-deep: #060911      --bg-base: #0A0E1A
--bg-surface: #111827   --bg-elevated: #1F2937
--border: #1E293B       --border-lit: #334155
--text-primary: #F1F5F9 --text-secondary: #94A3B8  --text-muted: #64748B
--accent-blue: #3B82F6  --accent-violet: #8B5CF6
--accent-amber: #F59E0B --accent-green: #10B981
--accent-red: #EF4444   --accent-pink: #EC4899     --accent-teal: #14B8A6
```

To add new colors, extend `:root` — don't inline hex values in rules.

## Key JS Functions (app.js)

| Function | Purpose |
|----------|---------|
| `boot()` | Loads data, renders initial view |
| `navigate(level, context)` | View switching (L0-L5) |
| `renderPanorama()` | L0 — comparative repo overview |
| `renderRepoDetail(name)` | L1 — 10 swim lanes for one repo |
| `renderStreamFocus(repo, stream)` | L2 — single stream commits |
| `renderSession(repo, stream, day)` | L3 — day/session detail |
| `renderFile(repo, file, hash)` | L4 — file diff view |
| `renderTranscripts()` | L5 — AI transcript list |
| `showFloatingReport(event, repo)` | Floating panel with white connector line |
| `showCellReport(event, repo, stream, day)` | Cell-level floating panel |
| `runSearch(query)` | Full-text search across all repos |
| `drawConnector(x1,y1,x2,y2)` | SVG white connector line |
| `gptSimSend()` | AI Chat: send message, call BMC API or OpenAI |
| `gptSimSaveSession()` | Persist chat + params to localStorage |
| `gptSimSetModel(id)` | Switch Rule-based / GPT-4o / GPT-4o-mini |

## Data Schema (latest.json)

```
DATA.repos[repoName].commits[]     — {hash, date, message, author, files[], stream, sessionId}
DATA.repos[repoName].sessions[]    — {id, day, start, end, commitCount, streams{}, dominantStream}
DATA.repos[repoName].daily{}       — {[day]: {commits, streams{}, sessions}}
DATA.repos[repoName].stats         — {totalCommits, activeDays, firstCommit, lastCommit, totalSessions}
DATA.repos[repoName].score         — {total, components{}}
DATA.repos[repoName].suggestions[] — {type, text}
DATA.repos[repoName].config        — {name, path, github, color}
DATA.streamMeta[streamId]          — {label, color}
DATA.transcripts[]                 — {id, date, sizeKB, firstMessage, toolsUsed[]}
DATA.skills[]                      — {name, source, created, modified, hasScript, hasSkillMd}
DATA.crossRefs[]                   — {date, repos[], type, description}
```

## Server Management

If the server is not running:
```bash
cd ~/.panelin-evolution && python3 -m http.server 3847 --directory . &
```

To regenerate data after repo changes:
```bash
node ~/.panelin-evolution/collect.js
```

## AI Chat (Panelin Dev)

The Panelin Dev system includes an **AI Chat** with real OpenAI integration:

- **Rule-based**: Deterministic flow, no API key needed.
- **GPT-4o / GPT-4o-mini**: Conversational, fluent responses via OpenAI. Requires the proxy:

```bash
OPENAI_API_KEY=sk-xxx node ~/.panelin-evolution/proxy-openai.js
```

- **Terminal log**: Full log of inputs, API requests/responses, processes. Export (⤓) downloads complete log as .txt.
- **Analizar**: AI analyzes the terminal log and explains what happened step-by-step.
- **Save session** (💾): Persists chat + params to `localStorage`.
- **Keep changes**: Edits via this skill apply to actual viewer files. Refresh to see them.

## Additional Resources

- For example modification patterns, see [examples.md](examples.md)
- For detailed file structure reference, see [reference.md](reference.md)

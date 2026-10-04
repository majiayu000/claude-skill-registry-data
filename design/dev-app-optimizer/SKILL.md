---
name: dev-app-optimizer
description: Systematic app optimization via multi-dimensional scoring, competitive benchmarking, and Quick Wins sprints. Use when the user wants to improve, optimize, audit, or enhance any web app or app suite — especially when they mention "quick wins", "feature gaps", "completeness", "competitive analysis", "what's missing", or want to rapidly add many small features. Also triggers on "audit this app", "compare to competitors", "improve all apps", or "optimization sprint". NOT for a market gap registry tracked across re-runs (use eos-app-gap-analysis) and NOT for AI-nativeness (use eos-ai-native-audit).
---

# App Optimizer

> Holistic app optimization — not just endpoint counts, but real product quality across 6 dimensions.

## When to Use

- User says "optimize", "improve", "audit", "what's missing", "quick wins"
- User has a web app (or suite) and wants to systematically improve it
- User wants to benchmark against competitors
- User wants to rapidly add many small features

## The 6-Phase Workflow

```
Phase 1: Explore → Phase 2: Score → Phase 3: Prioritize → Phase 4: Execute → Phase 5: Verify → Phase 6: Record
```

Always start by asking: **"Which phase are we in?"** If the user already has test results, skip to Phase 3. If they just want to execute, skip to Phase 4.

---

## Phase 1: Exploratory Testing

**Goal**: Understand what each app actually DOES, not just count endpoints.

### Per-App Checklist (read app.py + pages/index.html)

1. **Backend Depth** — not just route count, but:
   - Does it have CRUD? (create/read/update/delete)
   - Does it persist data? (JSON, vault, SQLite)
   - Does it use LLM? (self.think for smart features)
   - Does it call other apps? (call_app for composition)
   - Does it emit events? (for reactor/staff to react to)

2. **UI Quality** — open the page:
   - Does it have a custom page or auto-generated?
   - Does it show data meaningfully? (charts, lists, cards)
   - Can user interact? (add/edit/delete from UI)
   - Mobile responsive? (test at 390px)
   - Uses shared components? (eos-components.css/js)

3. **Integration** — how connected is it?
   - Which apps depend on it?
   - Which apps does it depend on?
   - Events emitted/listened?
   - Used by staff agents?
   - Used by dashboard/hub?

4. **LLM Quality** — how smart is it?
   - Does it use LLM for data entry? (smart-add, parsing)
   - Does it use LLM for insights? (trends, recommendations)
   - Does it use LLM for generation? (content, suggestions)
   - Does it support streaming?
   - Per-app provider configurable?

---

## Phase 2: Multi-Dimensional Scoring

**Goal**: Score each app on 6 dimensions, not just endpoints.

### The 8 Dimensions (each 0-15 points, total 0-120)

| Dimension | What to Measure | 0 pts | 8 pts | 15 pts |
|-----------|----------------|-------|-------|--------|
| **Backend** | API completeness | 1-2 endpoints | 5-10 CRUD | 15+ full lifecycle |
| **Frontend** | UI quality | No custom UI | Basic list/form | Rich interactive, charts, modals |
| **AI Utilization** | How deeply LLM is used | No LLM | Basic think() for one task | Smart-add + insights + streaming + multi-provider |
| **App Collaboration** | Inter-app connections | Standalone island | Emits events | call_app + events + staff agent + dashboard + slash command |
| **Vault Integration** | Obsidian vault usage | No vault interaction | Reads from vault | Read + write + wikilinks + frontmatter + vault watcher |
| **User Innovation** | Creative interaction patterns | Static CRUD | Search + filter | Voice I/O, AI chat, drag actions, real-time, /commands |
| **Data** | Persistence + history | No persistence | JSON state | Vault + JSON + JSONL + export + import |
| **UX Polish** | Experience details | Broken/ugly | Functional | Streaks, heatmaps, achievements, mobile, themes |

### Dimension Deep-Dives

#### AI Utilization (0-15)
How deeply does the app leverage AI? Not "does it call think()" but "does AI make this app fundamentally better?"

| Score | Description | Example |
|-------|------------|---------|
| 0 | No LLM | git, run, tmpl |
| 3 | Basic think() — one-shot answer | divination (interpretation) |
| 6 | Smart input parsing | expense (smart-add parses "20 woolworths grocery") |
| 9 | Analysis + recommendations | healing (mood-activity correlations + care alerts) |
| 12 | Multi-modal AI pipeline | search (LLM keyword expansion → RAG → markdown render) |
| 15 | AI-native workflow | staff (OBSERVE→DECIDE→ACT autonomous agents), assistant (multi-session streaming chat) |

#### App Collaboration (0-15)
How well does this app work WITH other apps? An island app scores 0.

| Score | Description | Example |
|-------|------------|---------|
| 0 | No connections | cable-pulling |
| 3 | Emits events only | meditation (emits meditation:completed) |
| 6 | Emits + listened by reactor | capture (reactor logs, staff processes) |
| 9 | call_app() composition | dashboard (pulls from 5+ apps), review (aggregates week) |
| 12 | Full ecosystem participant | task (called by staff, briefing, focus, dashboard, assistant /tasks) |
| 15 | Hub/orchestrator | hub (aggregates all), assistant (slash commands to 13 apps), staff (22 agents calling 20+ apps) |

#### Vault Integration (0-15)
How deeply integrated with the Obsidian vault?

| Score | Description | Example |
|-------|------------|---------|
| 0 | No vault interaction | app-analytics, billing |
| 3 | Reads from vault (one folder) | media (scans Books/, Entertainment/) |
| 6 | Read + write vault notes | journal (creates daily notes), capture (appends to inbox) |
| 9 | Full vault CRUD + frontmatter | contacts (creates @Person.md, parses frontmatter, quick log) |
| 12 | Vault-native data model | task (scans 3 folders, checkbox syntax, due dates from markdown) |
| 15 | Vault as primary storage + wikilinks | dictionary (saves words as notes, SRS metadata in frontmatter, [[wikilinks]] between notes) |

#### User Innovation (0-15)
Does the app offer creative, engaging interaction beyond basic CRUD?

| Score | Description | Example |
|-------|------------|---------|
| 0 | No interaction (backend only) | reactor |
| 3 | Basic form input | capture (text input → save) |
| 6 | Rich UI interactions | expense (smart-add, category chips, heatmap click) |
| 9 | AI-powered interactions | search (semantic search + AI Ask + provider retry) |
| 12 | Multi-modal | speaking (voice I/O + AI feedback), studio (prompt + style + gallery) |
| 15 | Conversational + autonomous | assistant (WebSocket chat, slash commands, streaming, sessions), staff (autonomous agents that act on your behalf) |

### Score Card Template

```markdown
| App | Backend | Frontend | AI | Collab | Vault | Innovation | Data | UX | Total | Grade |
|-----|---------|----------|----|--------|-------|------------|------|----|-------|-------|
| assistant | 12 | 14 | 15 | 15 | 9 | 15 | 10 | 12 | 102 | A |
| nutrition | 15 | 14 | 12 | 10 | 6 | 9 | 15 | 12 | 93 | A- |
| task | 12 | 12 | 6 | 15 | 15 | 6 | 12 | 10 | 88 | B+ |
| reactor | 2 | 0 | 0 | 15 | 0 | 0 | 3 | 0 | 20 | F |
```

### Grade Scale
- **A (96+)**: Best-in-class, could be a standalone product
- **A- (84-95)**: Excellent, daily driver quality
- **B+ (72-83)**: Strong, minor gaps
- **B (60-71)**: Good, usable daily but missing features
- **C (40-59)**: Functional but thin
- **D (20-39)**: Stub, barely usable
- **F (<20)**: Placeholder or broken

### Key Principle: Balance > Total
An app scoring 60 with all dimensions ≥ 6 is BETTER than one scoring 75 with three dimensions at 0. Balance matters — a beautiful UI with no data persistence is worse than a plain UI that saves everything.

### Competitive Benchmark

For each app, compare against the BEST in category:

```markdown
| App | vs Competitor | Our Score | Their Score | Gap | Key Missing |
|-----|--------------|-----------|-------------|-----|-------------|
| expense | YNAB | 64% | 100% | -36% | Bank linking, multi-currency |
```

**Don't inflate scores.** A 60% against Todoist is honest and useful. A fake 85% hides real gaps.

---

## Phase 3: Prioritize (Quick Win Selection)

**Goal**: Sort improvements by ROI across ALL dimensions, not just backend.

### Impact × Effort Matrix

| | Low Effort | Medium Effort | High Effort |
|---|-----------|--------------|-------------|
| **High Impact** | 🔥 DO FIRST | ⭐ Priority | 📋 Plan |
| **Medium Impact** | ⭐ Priority | 📋 Plan | 🔜 Later |
| **Low Impact** | 📋 Plan | 🔜 Later | ❌ Skip |

### Quick Win Patterns by Dimension

**Backend patterns:**
| Pattern | Example | Effort |
|---------|---------|--------|
| Stats endpoint | Totals, averages, breakdowns | Low |
| History endpoint | Last N items | Low |
| Search/filter | Query params on list | Low |
| Export (JSON/CSV) | Download data | Low |
| Streak calculation | Consecutive days | Low |

**Frontend patterns:**
| Pattern | Example | Effort |
|---------|---------|--------|
| Hero stats cards | 2-4 key numbers at top | Low |
| Heatmap | GitHub-style activity grid | Medium |
| Progress ring/bar | SVG circle or bar fill | Low |
| Filter chips | Type/status/category toggles | Low |
| Sort dropdown | A-Z, date, rating | Low |
| Empty state | Helpful message when no data | Low |
| Toast notifications | Feedback on actions | Low |

**Data patterns:**
| Pattern | Example | Effort |
|---------|---------|--------|
| Vault write | Save to Obsidian note | Low |
| Activity log | JSONL append (use self.log_activity) | Low |
| Daily/monthly aggregation | Stats by period | Medium |
| Import from file | CSV/JSON upload | Medium |

**Intelligence patterns:**
| Pattern | Example | Effort |
|---------|---------|--------|
| Smart-add | LLM parses natural language input | Medium |
| AI insight | LLM analyzes trends + suggests | Medium |
| Auto-categorize | LLM classifies input | Low |
| Reflection/summary | LLM generates narrative | Medium |

**Integration patterns:**
| Pattern | Example | Effort |
|---------|---------|--------|
| Emit events | Other apps can react | Low |
| Manifest events declared | Reactor can listen | Low |
| Dashboard widget | Hub/dashboard shows summary | Low |
| Staff agent | Autonomous monitoring | Medium |
| Slash command | /expense in assistant | Low |

**UX Polish patterns:**
| Pattern | Example | Effort |
|---------|---------|--------|
| Streak display | "7 day streak 🔥" | Low |
| Achievement badges | Milestones (10, 50, 100) | Low |
| Trend indicator | ↑12% vs last week | Low |
| Mobile responsive | Stack layout <400px | Low |
| Keyboard shortcuts | Enter to submit | Low |
| Loading skeleton | Shimmer while fetching | Low |

### Select Top 10
Pick improvements across DIFFERENT dimensions. Don't just add 10 endpoints — add 3 endpoints + 2 UI features + 2 integrations + 3 UX polish items.

---

## Phase 4: Batch Execution

**Goal**: Rapidly implement Quick Wins in mixed batches.

### Batch Rhythm
```
Pick 4-6 QWs (mixed dimensions) → Backend → Frontend → Integration → Verify → Commit
```

### Execution Rules

1. **Search before building** — `grep` the codebase first.
2. **Backend first** — API endpoint, verify with `curl`, then build UI.
3. **Minimal changes** — Don't refactor. Just add the feature.
4. **Mixed batches** — Each batch should touch at least 2 dimensions.
5. **Commit every batch** with descriptive message.

### EmptyOS-Specific Patterns

```python
# Backend: new endpoint
@web_route("GET", "/api/feature")
async def api_feature(self, request):
    return {"key": "value"}

# Intelligence: LLM-powered
result = await self.think("Analyze this data...", domain="text")

# Integration: call another app
tasks = await self.call_app("task", "list_tasks")

# Integration: emit event
await self.emit("myapp:action", {"detail": "..."})

# Data: activity logging (platform service)
self.log_activity({"action": "created", "item": name})

# Data: vault write
self.vault_write("report.md", content)
```

### Frontend Template (EmptyOS style)
```html
<script src="/static/realtime.js"></script>
<script src="/static/eos.js"></script>
<script src="/static/eos-components.js"></script>
<script>EOS.nav('appname');</script>
<!-- Use: EOS.api(), EOS.post(), EOS_UI.toast(), EOS_UI.renderMarkdown() -->
<!-- Use: EOS.viewNote(), EOS.editNote(), EOS.noteActions() for vault notes -->
```

---

## Phase 5: Verification

**Goal**: Verify across all dimensions, not just API responses.

### Multi-Dimension Verification

1. **Backend**: `curl` each endpoint, check JSON response
2. **Frontend**: Open page, check rendering, try interactions
3. **Data**: Check persistence (JSON file exists, vault note created)
4. **Intelligence**: Test LLM feature (does smart-add actually parse?)
5. **Integration**: Check events emitted (`/api/events?type=myapp:*`)
6. **UX**: Test mobile (390px), check streaks/achievements update

### Regression Checks
- New features don't break existing ones
- CSS class conflicts (use app-specific prefixes)
- API response format unchanged
- Events still firing correctly

---

## Phase 6: Record & Measure

**Goal**: Document improvement across all dimensions.

### Score Card Update
```markdown
| App | Before | After | Delta | Key Improvements |
|-----|--------|-------|-------|-----------------|
| expense | 74/120 (C+) | 94/120 (A) | +20 | YTD endpoint, budget UI, staff agent, streak |
```

### Metrics to Track
| Metric | How |
|--------|-----|
| Total score delta | Sum of all dimension deltas |
| Endpoints added | grep count |
| UI pages added/improved | ls pages/ |
| Events declared | grep manifest emits |
| Staff agents connected | count observe_apps references |
| LLM features added | grep self.think |
| Code quality | /simplify review |

### Overall System Health
```markdown
| Dimension | Average Score | Best App | Worst App |
|-----------|--------------|----------|-----------|
| Backend | 14/20 | nutrition (18) | reactor (2) |
| Frontend | 12/20 | expense (16) | run (0) |
| Data | 13/20 | reader (16) | _example (0) |
| Intelligence | 10/20 | search (18) | git (0) |
| Integration | 11/20 | task (16) | cable-pulling (2) |
| UX Polish | 9/20 | focus (14) | tmpl (0) |
```

---

## Decision Frameworks

### "Which dimension to improve?"
1. **Backend < 8**: App is a stub — add core CRUD first
2. **Frontend = 0**: No custom UI — build one (biggest user impact)
3. **Intelligence = 0**: No LLM — add smart-add or AI insight (differentiator)
4. **Integration < 4**: Island app — add events + manifest declarations
5. **UX < 6**: Functional but ugly — add streaks, empty states, mobile

### "Should I Build This?"
1. Does it already exist? → Search first
2. Which dimension does it improve?
3. Will the user notice it daily? → High impact
4. Can I build it in <30 min? → Low effort = do it

### "80% Rule"
- 80% = all 6 dimensions ≥ 12/20
- Don't over-invest in one dimension while others are at 0
- A balanced 70/120 is better than lopsided 90/120 with 0 frontend

---

## Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Count only endpoints | Score across 6 dimensions |
| Add 10 endpoints to one app | Add 2 endpoints + UI + integration to 3 apps |
| Refactor while adding features | Add only, refactor later |
| Build abstractions for one use | Write direct code |
| Skip frontend work | Every backend feature needs a UI |
| Ignore integration | Events + manifest + staff = system value |
| Aim for 100% | Stop at 80% (all dimensions ≥ 12) |

---

## Reference

### EmptyOS Architecture Cheat Sheet
```
App = manifest.toml + app.py + pages/index.html
API = @web_route("METHOD", "/api/path")
WS  = @ws_route("/ws/path")
CLI = @cli_command("name")
Events = @on_event("type") + await self.emit("type", data)
LLM = await self.think(prompt) / self.think_stream() / self._think_with_provider()
Apps = await self.call_app("app_id", "method", **kwargs)
Data = self.data_dir (JSON) / self.vault_write() (markdown) / self.log_activity() (JSONL)
UI  = EOS.api() / EOS.post() / EOS_UI.toast() / EOS_UI.renderMarkdown()
```

### Free APIs for Features
| API | Use | Key Required |
|-----|-----|-------------|
| Open-Meteo | Weather | No |
| Datamuse | Word suggestions | No |
| Free Dictionary | English definitions | No |
| MyMemory | Translation | No |

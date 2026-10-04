---
name: vibe-progress
description: >
  Displays a live ASCII progress dashboard for the current vibe project.
  Triggers on "/vibe-progress", "progress:", "show progress", "how far along are we".
  Reads vibe/TASKS.md and git log to render a clean dashboard.
  Shows overall progress, phase gate status, active work, completed features,
  active bugs, backlog items, scope decisions, and last git activity.
  No files are modified. Read-only. Always runs in Plan Mode.
---

# Vibe Progress Skill

Renders a live ASCII dashboard of the current project's build progress.
Reads vibe/TASKS.md and git history. Never modifies any file.

**Always run in Plan Mode. Read-only.**

---

## Step 1 — Read project state

1. `vibe/TASKS.md` — phases, features, tasks, gates, active work, backlog
2. `git log --oneline -1` — last commit
3. `git log --oneline --since="7 days ago" | wc -l` — commits this week
4. `vibe/bugs/` — count folders, note any active
5. `vibe/backlog/` — count files (deferred items)
6. `vibe/DECISIONS.md` — count D-[ID] entries
7. `vibe/cost/history.json` — total project cost if exists (read silently, skip if missing)
8. `vibe/.doctor-last-run` — timestamp of last doctor: run (skip if missing)

---

## Step 2 — Calculate stats

**Phase 1:**
- Total tasks: count P1-XXX items
- Done: count [x] P1-XXX items
- Status: ✅ / 🔄 / ⬜

**Phase 2:**
- Total features: count feature blocks
- Done: count ✅ features
- Active: 🔄 feature name + task progress (N/total)
- Active tasks: list [ ] and [x] tasks in active block

**Phase 3:**
- Total tasks, done tasks
- Status: ✅ / 🔄 / ⬜

**Overall:**
- Total tasks across all phases, done tasks
- Overall % = (done / total) × 100, rounded to nearest 5

**Phase gates:**
Read every `## Phase N gate`, `## Design gate` and `## Final gate` heading in TASKS.md and
the gate line directly under each (`⬜ pending` / `✅ passed` / `🔴 blocked`). If
`vibe/.gates.json` exists, prefer its `review` + `p0`/`p1` values for phase and final
gates — it is the machine-readable record. (Older files may still carry a single
`## Phase gates` section; read it the same way if present.)

**Backlog:**
Count items in vibe/backlog/ folder.
List names if ≤3 items; show count only if >3.

**Cost (if vibe/cost/history.json exists):**
```bash
node -e "
const h = require('./vibe/cost/history.json');
// history.json is a flat array of session objects (as written by vibe-cost
// and read by vibe-ledger). Tolerate a legacy {sessions:[...]} shape too.
const arr = Array.isArray(h) ? h : (Array.isArray(h.sessions) ? h.sessions : []);
const total = arr.reduce((s,x) => s + (x.cost_usd||0), 0);
const sessions = arr.length;
console.log('COST:$' + total.toFixed(2) + ':' + sessions + ' sessions');
" 2>/dev/null || echo "COST:none"
```
If no history.json — show "not tracked" in dashboard.

**Env health (if vibe/.doctor-last-run exists):**
```bash
if [ -f "vibe/.doctor-last-run" ]; then
  last=$(cat vibe/.doctor-last-run)
  now=$(date +%s)
  age=$(( (now - last) / 3600 ))
  if [ $age -lt 1 ]; then echo "ENV:healthy:checked this session"
  elif [ $age -lt 24 ]; then echo "ENV:stale:checked ${age}h ago"
  else echo "ENV:unknown:run doctor: to check"
  fi
else
  echo "ENV:unknown:doctor: not yet run"
fi
```

---

## Step 3 — Render the dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  [PROJECT NAME] — Build Progress                            │
│  [overall%] complete · [N] tasks done of [total]            │
├─────────────────────────────────────────────────────────────┤
│  PHASES                                                     │
│                                                             │
│  Phase 1  [bar]  [N/total]  [status]                       │
│  Phase 2  [bar]  [N/total]  [status]                       │
│  Phase 3  [bar]  [N/total]  [status]                       │
├─────────────────────────────────────────────────────────────┤
│  PHASE GATES                                                │
│                                                             │
│  Phase 1 → 2:  [✅ reviewed [date] / 🔴 BLOCKED / ⬜ pending]  │
│  Phase 2 → 3:  [status]                                    │
│  Phase N → deploy:  [status]                               │
├─────────────────────────────────────────────────────────────┤
│  ACTIVE NOW                                                 │
│  [Feature name or Phase 3 task]                             │
│                                                             │
│  [x] [task plain english]                                   │
│  [x] [task plain english]                                   │
│  [ ] [task plain english]  ← next                          │
│  [ ] [task plain english]                                   │
├─────────────────────────────────────────────────────────────┤
│  COMPLETED FEATURES                                         │
│                                                             │
│  ✅ [Feature name]  [N/N tasks]                            │
│  ...                                                        │
├─────────────────────────────────────────────────────────────┤
│  BACKLOG        [N items deferred]                          │
│  [item name if ≤3] / [count only if >3]                    │
│                                                             │
│  BUGS           [N fixed]  [N active]                      │
│  SCOPE CHANGES  [N decisions logged]                        │
│  COMMITS        [N this week]                               │
├─────────────────────────────────────────────────────────────┤
│  COST           [$X.XX total · N sessions]                  │
│  ENV HEALTH     [✅ checked this session / ⚠️ [N]h ago / ❓ not checked] │
├─────────────────────────────────────────────────────────────┤
│  Last: [last git commit — truncated to 45 chars]            │
│  Next: [plain English next task]                            │
│                                                             │
│  Say "next" to continue building.                           │
└─────────────────────────────────────────────────────────────┘
```

**COST row logic:**
- If history.json exists: `$X.XX total · N sessions`
- If no history.json: `not tracked — run cost: to start`

**ENV HEALTH row logic:**
- Checked this session (< 1h ago): `✅ checked this session`
- Checked today (1-24h ago): `⚠️ checked Nh ago — consider re-running doctor:`
- Not checked / no .doctor-last-run: `❓ not checked — run doctor: before building`

---

## Progress bar rendering

Bar is 20 characters wide using █ and ░:
```
0%    ░░░░░░░░░░░░░░░░░░░░
25%   █████░░░░░░░░░░░░░░░
50%   ██████████░░░░░░░░░░
75%   ███████████████░░░░░
100%  ████████████████████
```
Formula: filled = round(percentage / 5), empty = 20 - filled

---

## Status icons

```
✅  complete (100%)
🔄  in progress (1-99%)
⬜  not started (0%)
🔴  BLOCKED (phase gate blocked by open P0/P1 issues)
🐛  active bug fix
```

---

## Edge cases

**Nothing built yet:**
All phases ⬜ 0%. Active section: "Start with Phase 1 — say next to begin."
Phase gates all ⬜ pending.

**Active bug fix:**
Add 🐛 ACTIVE BUG FIX section between ACTIVE NOW and COMPLETED FEATURES:
```
├─────────────────────────────────────────────────────────────┤
│  🐛 ACTIVE BUG FIX                                         │
│  [Bug summary plain English]                                │
│  [ ] BUG-001 · Write regression test  ← next               │
│  [ ] BUG-002 · Implement fix                                │
│  ...                                                        │
```

**Review gate blocked:**
The phase gate line shows 🔴 blocked with the P0 + P1 counts.
Active section shows the RFX- fix tasks.

**No backlog:**
Show: "BACKLOG  0 items deferred"

**All tasks complete:**
Active section: "All tasks complete — ready for review: final 🎉"

---

## After rendering

Print nothing else. No explanations. No next steps beyond what's in the dashboard.
The dashboard is the complete output.

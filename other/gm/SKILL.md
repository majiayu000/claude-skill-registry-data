---
name: gm
description: Canonical good-morning and day-start launcher with a technical pulse, business pipeline, calendar, and intent lock; use for GM, good morning, start the day, or the first session of the day.
version: 1.0.1
execution-mode: side_effecting
argument-hint: "[quick | deep | pipeline | intent only]"
category: fleet-ops
status: candidate
providers:
  required: [bash, python]
  optional: [pwsh(workstation-variant)]
---
# [GM] — Good Morning

> **GM.** The crypto-twitter usage is right: it's not just a greeting, it's a daily act of showing up to the arena. This skill is your ignition sequence.

Holistic morning launch for founders. This is the canonical morning launcher;
the retired `[morning-kickoff]` name now routes here.

**Target time: 5 minutes. If it takes longer, use `quick` mode.**

---

## When to Use
- First session of any day (or work block after a long gap)
- "GM" / "good morning" / "start the day" / "let's go"
- After `[end-session]` suggested it the night before

---

## Execution

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=gm] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### Phase 1 — System Pulse (parallel, ~60 seconds)

Run all of these simultaneously:

```bash
FM_ROOT="${FM_ROOT:-$HOME/.agents}"

# 1. Bus overnight scan — what did agents do?
python $HOME/bin/bus-global.py tail 30 2>/dev/null | \
  awk -F'\t' '{printf "[%s] %-20s %s: %.65s\n", substr($1,12,5), $2, $3, $5}'

# 2. Health check (quick)
python3 -m hummbl_governance.services.health 2>/dev/null | tail -5

# 3. Cost status
python $HOME/bin/bus-global.py tail 200 2>/dev/null | \
  grep -i "cost\|budget\|spend\|alarm" | \
  tail -3 | awk -F'\t' '{printf "[%s] %.80s\n", substr($1,12,5), $5}'

# 4. remote-node pulse (dormant since 2026-07-01 — expected UNREACHABLE)
ssh -o ConnectTimeout=5 mini "cd ~/.agents && git status --short 2>/dev/null | wc -l | tr -d ' '" 2>/dev/null && \
  echo " dirty files on remote-node" || echo "remote-node: unreachable (dormant since 2026-07-01)"

# 5. HRSI daily check — reads from the canonical cognition state dir.
# Bug fix 2026-05-19: prior version used ~/hummbl_governance (Huxley path, doesn't exist on agent-node)
# and queried ledger.jsonl (empty for hrsi tags). Operator logged HRSI to PROJECTS/...
# and agents reported DUE → false-negative accountability gap.
python3 -c "
import json, datetime, pathlib
p = pathlib.Path.home() / '.agents' / '_state' / 'cognition' / 'hrsi_cycles.jsonl'
if not p.exists(): print('HRSI: NO LEDGER — run [hrsi-checkin]')
else:
    lines = [l for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]
    if not lines: print('HRSI: empty ledger — run [hrsi-checkin]')
    else:
        last = json.loads(lines[-1])
        ts = last.get('ts') or last.get('timestamp') or last.get('date','')
        today = datetime.date.today().isoformat()
        if today in ts: print(f'HRSI: done ({ts[:16]})')
        else: print(f'HRSI: DUE — last={ts[:10]} → run [hrsi-checkin]')
" 2>&1
```

**Flag if:** health RED, cost alarm firing, remote-node has uncommitted work (remote-node dormant since 2026-07-01 — expected unreachable), bus has BLOCKED messages, HRSI check not yet logged today, PR queue >5 (merge queue flooding — drain before creating new PRs).

---

### Phase 2 — Residual Drain (~60 seconds)

What's still open from the last session?

```bash
# Last handoff from bus
python $HOME/bin/bus-global.py tail 500 2>/dev/null | \
  grep "HANDOFF\|end-session\|END-SESSION" | \
  tail -1 | awk -F'\t' '{printf "%s\n%s\n", $1, $5}'

# Open PRs + queue depth warning
OPEN_COUNT=$(gh pr list --state open --json number --jq 'length' 2>/dev/null)
echo "PR queue: ${OPEN_COUNT:-0} open"
gh pr list --limit 5 --json number,title,isDraft --jq '.[] | "\(if .isDraft then "[DRAFT] " else "" end)#\(.number): \(.title)"' 2>/dev/null

# Stale branches (not merged to main)
git branch --no-merged main 2>/dev/null

# Uncommitted orphans
git status --short 2>/dev/null | head -10

# Stash audit (untracked-files-loss prevention -- see AAR_2026-05-14)
STASH_COUNT=$(git stash list 2>/dev/null | wc -l | tr -d ' ')
[ "${STASH_COUNT:-0}" -gt 0 ] && echo "STASH: ${STASH_COUNT} entries -- consider [stash-audit] (detect) then [stash-manager] --dry-run (autonomous triage)" || echo "STASH: clean"
```

**Flag if:** last session handoff has open items with today's date or deadlines; PRs that need human action; stash count > 0 (then run `[stash-audit]` before any cross-branch operation per `skill-routing.md`).

---

### Phase 3 — Pipeline Pulse (~60 seconds)

The business layer that determines whether the day actually moves the needle.

Check the following from memory and state:

1. **Wave 1 / outreach**: Any emails due today? Check `_internal/outreach/wave1-drafts.md` and the send checklist.
2. **LinkedIn**: Any view-first steps before outreach? (LinkedIn views before emails is the warm-signal protocol.)
3. **Follow-ups**: Any leads that have been silent > 5 days? Check `_internal/crm/` or `[follow-up]` state.
4. **ATL pipeline**: Any Atlanta-specific events, intros, or nudges due? Check `people_dan_matha.md` and ATL watch.
5. **GA annual registration**: Overdue $75 — done yet?

```bash
# Check wave1 drafts and send checklist
FM_ROOT="${FM_ROOT:-$HOME/.agents}"
cat "$FM_ROOT/_internal/outreach/wave1-drafts.md" 2>/dev/null | head -30 || echo "(not found)"
ls "$FM_ROOT/_internal/outreach/" 2>/dev/null
```

---

### Phase 4 — Calendar (~30 seconds)

```bash
python3 -c "
from hummbl_governance.integrations.google_calendar_adapter import GoogleCalendarAdapter
try:
    adapter = GoogleCalendarAdapter()
    entries = adapter.get_calendar_entries()
    for e in entries[:5]:
        print(f'  {e.start_time} {e.title}')
except Exception as e:
    print(f'  Calendar unavailable: {e}')
" 2>&1
```

**Key blocks to protect:**
- Mon/Fri 7:30–9:30am: coaching
- Wed 10:30–12:30: hard stop
- Daily: commit something before each coaching block

---

### Phase 5 — Intent Lock (~30 seconds)

Before touching code or email, set three lines — one per track:

- **A (Temporal)** — what is time-gated today? What breaks or expires if not done?
- **B (Load-bearing)** — which track is doing the most work this week? What moves it forward today?
- **C (Modal)** — what capacity/mode are you actually in right now? (shipping / thinking / recovering / coordinating)

Each answer must be specific enough to verify. "Work on HUMMBL" fails. "Send Wave 1 emails before coaching block" passes.

```bash
# Read current intent
cat /work/active/PSI/_state/intent.md 2>/dev/null | tail -8

# Write today's A/B/C intent (edit with actual content)
cat >> /work/active/PSI/_state/intent.md << EOF
[$(date +%Y-%m-%d)] A (time-gated): <fill in>
[$(date +%Y-%m-%d)] B (load-bearing): <fill in>
[$(date +%Y-%m-%d)] C (mode): <shipping | thinking | recovering | coordinating>
EOF
```

---

## Output Format

```
[GM] | <date> <time>
══════════════════════════════════════════

GM. 🌅 Arena open.

## System Pulse
- Bus: <last activity, any BLOCKED/alerts>
- Health: <GREEN | DEGRADED | RED — list any failed probes>
- Cost: <safe | caution | alarm>
- remote-node: <clean | N dirty files | DORMANT since 2026-07-01>
- HRSI: <done at HH:MM | **DUE → run `[hrsi-checkin]` before first deep work**>

## Residual (carry from yesterday)
- PRs: <list open with age>
- Branches: <stale count>
- Last session open items: <from handoff>

## Pipeline
- Wave 1: <status — sent / pending / blocked on X>
- LinkedIn: <view-first step done? Y/N>
- Follow-ups due: <names or "none">
- GA registration: <done | OVERDUE>

## Calendar
- <meetings today, or "clear">
- First protected block: <time>

## Intent
- **A (time-gated)**: <what breaks or expires today if skipped>
- **B (load-bearing)**: <what moves the most important track forward>
- **C (mode)**: <shipping | thinking | recovering | coordinating>

First action: <concrete next step — file, command, or message>
Then: <what comes after that>

---
*Bus post: STATUS with this summary after reading*
```

---

## Mode Variants

### `quick` (2 minutes)
Skip Phase 3 (pipeline). Just: bus + health + intent. Use when returning from a short break, not first thing in the morning.

### `deep` (10 minutes)
After the 5-minute run, add:
- `[daily-research]` for evidence and competitive intelligence
- `[cost-status]` deep dive if alarm is firing
- `[fleet-status]` if remote-node was unreachable (remote-node dormant since 2026-07-01 — expected)
- `[follow-up]` scan if pipeline check flagged stale leads

### `pipeline` (pipeline only)
Skip system checks. Just Phase 3 + output a pipeline action. Use mid-day when you want a pipeline pulse without full orientation.

### `intent only`
Skip everything. Just read current intent and suggest whether it still holds.

---

## Daily Best Practices (embedded — not a checklist, a philosophy)

These are the habits that compound. Run them as part of GM:

**Technical layer:**
- Read the bus before touching code — agents worked overnight
- Commit before each coaching block (Mon/Fri 7:30, Wed 10:30)
- One branch per agent, always — collision avoidance is not bureaucracy
- Tests before merge, even at 1AM — the 2-minute cost beats the broken-briefing cost
- Commit small, commit early — 500 LOC soft limit applies to you too

**Business layer:**
- One pipeline touch per day minimum — keep the ATL engine warm
- LinkedIn view-first before every cold email — it's the warm-signal protocol
- Update `people_*.md` same-session as any significant meeting — perishable context
- Wave 1 has 5 targets researched and drafted — the gap to revenue is sending

**Memory layer:**
- Post to bus before AND after every significant agent task
- `[ledger]` anything that took > 30 minutes to debug
- After BKI/ARCANA work → `[bki-session-export]` before context compacts

**HRSI layer (30-day baseline — run every day):**
- If HRSI shows DUE → run `[hrsi-checkin]` before first deep work block
- 3 scores: Safety / Mattering / Connection (1–10 each, ~60 seconds)
- The baseline is the measurement — skipping breaks the 30-day window

**Anti-pattern to name every morning:**
> *"Am I building the system or using the system to build the business?"*
> The infrastructure loop is the founder's version of busy work. The bus, the skills, the agent mesh — these exist to accelerate client acquisition and product delivery. If today's B-track (load-bearing) is another meta-layer, that's a signal.

---

## Bus Post

After reading GM output, post to the coordination bus:

```bash
python $HOME/bin/bus-global.py post "${AGENT_NAME:?set AGENT_NAME to canonical bus identity}" all STATUS \
  "GM: A=<time-gated item> B=<load-bearing track> C=<mode> | system: <health summary>"
```

---

## Chain
- P0 health issue → `[incident]`
- Wave 1 ready → `[send-email]` (with deliverability confirmed)
- Meetings today → `[meeting-prep]`
- HRSI DUE → `[hrsi-checkin]` (before first deep work block)
- Most mornings → `[daily-research]` after GM
- After GM on Monday → `[weekly-review]`
- End of day → `[end-session]` (bookend to GM)

## Skill Chains

### Mandatory

None — session opener, like `[start-session]`. No pre-chain required; this is the first skill of the day.

### Advisory

- `[gm]` → `[daily-research]` — most mornings, research follows ignition
- `[gm]` → `[hrsi-checkin]` — if HRSI shows DUE in the pulse check
- `[gm]` → `[send-email]` — if Wave 1 outreach is ready to send
- `[gm]` → `[meeting-prep]` — if calendar shows meetings today
- Monday `[gm]` → `[weekly-review]` — weekly review on the first session of the week

## Authority

- **T1 (TRUSTED)**: Full run — all phases, all modes
- **T2 (Active/High)**: Full run — all phases, all modes
- **T3 (Medium)**: Full run — all phases, all modes
- **T4 (Probationary)**: Full run — all phases, all modes
- **Operator**: Override any restriction

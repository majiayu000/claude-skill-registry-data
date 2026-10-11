---
name: human-ai-schedule
description: |
  Co-author doctrine for shared, half-hour-block daily schedules.
  Make sure to consult this skill whenever working in a dated
  daily log, journal, retro, or coordination file shared with a
  coworker — even if the user only says "log this at 11:00" or
  "what did we say last Tuesday." Default behavior of dumping
  procedural details, paraphrasing voice into corporate prose, or
  fragmenting one task across multiple cells must defer to this
  skill — entries distill to result + significance, and a cell is
  removed only when its time falls inside a verified-active task's
  span (never pre-merged on guess).

  TRIGGER when: user is in a file matching `daily/`, `journal/`,
  `schedule/`, `半小时复盘/`, or any file with H1 time-block headers
  like `# 7：30` or `# 09:00`; user says "create today's", "创建
  今天的", "log at N o'clock", "补到 N 点那格", "morning brief",
  "晨会复盘", "what did we decide on X day"; user dictates an event
  with time anchor ("just now", "刚才", "yesterday", "上周三",
  explicit clock); user asks to reconstruct a past session; user
  references a tag aggregation page; agent receives a `#协作` /
  `#collab` segment and needs to leave a commit.

  SKIP when: pure code editing without log context; one-off chat
  with no persistent dated file; user explicitly says "just answer,
  don't log"; reading code or technical docs only.

  Examples that trigger: "创建今天的 schedule", "log this at 11:00",
  "把刚才那段补到 11 点那格", "what did we say last Tuesday",
  "翻 5.7 那次 session", "记一下今天去了彭镇喝茶".
  Examples that skip: "implement a stripe webhook", "explain async",
  "改一下 settings.json 的 permission", "rename this private function".
extends: ctrl-c-v
---

# Human-AI Schedule

You are the same engineer. Same Friday flight to the Alps. Same system. But you are not alone in the office anymore — there is a coworker, and chat history forgets what was said by Wednesday. So you built a third thing: a shared schedule, half-hour-block, dated, tagged, persistent. Both write to it. Either can leave a commit on the other's entries.

The schedule remembers what neither of you can. Without exception.

---

## § H0 — Co-author role

Five jobs every entry:

```
□  Locate       — read [time-block] system-reminder → date + block label decided before write (NEVER recompute or guess)
□  Format       — H1 time / H2 #tag / single `---` separator preserved
□  Commit       — `#协作` present? → § H4 evaluation → write or stay silent
□  Harness      — project-tagged? → aggregation row appended same turn
□  Pulse-aware  — first activation in project: read PULSE.md if present;
                  flag if Last refreshed > 7d; suggest § H9 creation if
                  schedule files > 7 and PULSE absent (cold-start defense
                  in case schedule-drift hook hasn't fired yet)
```

Anti-patterns (revert immediately if seen):

| Pattern | Why wrong |
|---|---|
| Content written without time-block anchor | floating, unrecoverable |
| Empty time-block filled with speculative content | noise inflation |
| User's prose paraphrased into corporate tone | voice lost |
| Timestamp invented or assumed | unverifiable, breaks forensics |
| Time-block computed from session JSONL or "feel" instead of [time-block] reminder | the hook is the only sanctioned source; bypassing it caused 3 § H1 failures in 48h |
| Block label rounded UP (22:59 → 23:00) | rule is FLOOR (22:59 → 22:30); the [time-block] reminder already floors |
| Content placed without reading adjacent cells | back-fills into a block actually occupied by another activity (e.g. gym) |

## § H1 — Locate before writing

**Truth source for "now"**: read the `[time-block]` system-reminder injected by `scripts/timeblock-stamp.sh` (UserPromptSubmit hook). Example:

```
[time-block] now=22:59 CST 2026-05-10(Sunday) → current block: 22：30 (covers 22:30-22:59)
[time-block] H1 use: `# 22：30` (full-width colon). For PAST events, see § H1 decision tree.
```

The block label in that line **IS** the floor-correct, timezone-correct, full-width-colon-correct H1 to write. Do NOT recompute. Do NOT round. Do NOT guess from JSONL — the hook already did it.

If the `[time-block]` line is absent (not in a project with `半小时复盘/` etc.), this skill should not have activated; stop and ASK user.

### Decision tree (after consulting the time-block stamp)

```
User dictates content
    │
    ├─ explicit time stated → use that time → convert relatives to absolute date in prose
    ├─ contains "now / just now / 刚才 / 现在" → use [time-block] current block
    ├─ past event, no time stated → ASK user (do not write yet)
    └─ meta-discussion (workflow, tooling, retro) → use [time-block] current block
```

### Scan-adjacent before writing (mandatory)

Before placing content in block X, READ the file's adjacent cells (X-1 and X+1):

```
□  X-1 cell describes activity that physically excludes X content?  → reconsider placement
□  X+1 cell describes activity that physically excludes X content?  → reconsider placement
□  Conflict (e.g. neighbor says "at gym", you're placing desk work) → ASK user
```

This catches cases where current time is correct but the AI is back-filling a past event into a block that was actually occupied by something else.

Decision tree details and forensics → @${CLAUDE_SKILL_DIR}/playbooks/locate.md

## § H2 — File skeleton (project-defined)

**Format conventions** (H1 syntax, full-width colon, separator, tag prefix, etc.) live as inline comments in @${CLAUDE_SKILL_DIR}/templates/SCHEDULE_TEMPLATE.md. Single source of truth — read there when editing the format itself.

**Creating a new daily file**: copy @${CLAUDE_SKILL_DIR}/templates/SCHEDULE_TEMPLATE.md to the project's daily-log directory, rename to date stem (e.g. `26.5.10.md` or `2026-05-10.md` per project convention), keep all empty time-blocks as user placeholders.

**Customizing the top section**: the top of the template is intentionally a free slot — put per-project rituals there (supplement checklist / morning standup / daily commitments). Edit the template once for project-wide defaults, or override per-day by editing the daily file directly. The format-conventions comment block can stay or be deleted; it's reference, not required content.

**Semantic invariants** (these stay here — govern when cells are written/deleted, not how cells look):

```
□  Pre-padded empty cells = user's placeholders (preserve, never auto-clean)
□  Delete a cell ONLY if it falls inside a verified-active task's span
□  Verify span via JSONL timestamps OR user-stated duration. Never preemptively merge.
```

Cell-merging rule (the only time you remove a cell):
1. Task starts at cell `# H1：MM`
2. Same task continues past `H1+1：MM` cell boundary (verified by timestamps)
3. Delete the cells INSIDE the verified span. Keep the START cell. Keep the cells AFTER the span.

If you cannot verify the span, leave all cells alone.

Customizing the template (top section, time grid, etc.) → @${CLAUDE_SKILL_DIR}/playbooks/diy.md

## § H3 — Tags (vocabulary project-defined, rules universal)

Vocabulary is project-defined — list active tags in the project's `CLAUDE.md` so AI knows which segments need aggregation-page mirroring. Universal rules:

```
□  Multiple tags per block allowed: `## #exercise #leisure`
□  Project-named tags take precedence over generic
□  `#协作` / `#collab` stacks with other tags, never replaces
□  Capitalization stable per tag — never auto-normalize
□  New project tag → register in aggregation page first → then use
```

Sub-tags: `#parent/child` syntax (Obsidian-native), max 2 levels — no `#a/b/c` three-deep.

```
□  Sub-tag preferred over parent when category is determined
   (`#exercise/walk`, not bare `#exercise`)
□  Parent without sub OK for cross-sub meta-discussion
   (`#config-system` for cross-skill arch; `#config-system/skill-A` for that skill specifically)
□  Sub-tag entries roll up to parent on aggregation page
□  Add a new sub-tag to dictionary only when 3+ siblings appear naturally
```

Aggregation mechanics → @${CLAUDE_SKILL_DIR}/playbooks/aggregate.md

## § H4 — Dual-signature commits

Trigger: `#协作` / `#collab` tag present in the segment.

Format:
```
- #commit (user-handle): user's view — decision, next action, judgment
- #commit (agent-id): agent's view — risk, dependency, uncertainty
```

Identity: users sign with handle. Agents sign with model ID (`claude-opus-4.7`, `gpt-5`) — model versions produce different judgment, signature lets future readers calibrate.

Write a commit only when:

```
□  noticed risk the other side did not raise
□  hold related context they did not ask for
□  must disclose uncertainty about your own work
```

Do NOT write:

| Pattern | Why wrong |
|---|---|
| "great job" / "looks good" | affirmation, zero info |
| restating the outcome | adds nothing |
| "I'll keep watching this" | non-commitment, noise |
| general encouragement | not your job |

Silence is the default.

## § H5 — Granularity & Voice

**Primary rubric — the 1-year test**:

> Glance at this entry 12 months from now for 5 seconds. Do you still know what happened that day?

If no: the entry is broken. Almost always the failure is procedure leakage — version numbers, tool names, file paths, library names, API endpoints, line counts. These all decay to noise inside months.

Apply derived rubric — every entry must answer:

```
1. What changed — concretely, in the project / system / your understanding
2. Why it matters — what does this enable, unblock, or clarify next
```

If neither answer is obvious to a reader 12 months later, the entry is broken.

**Drop unconditionally**:
- Version numbers (`v0.4.1`, `第三版`)
- Tool / library / API names (`FastAPI`, `chokidar`, `DeepSeek`)
- File paths (`shared/journal.js`, `scripts/X.sh`)
- Function names, endpoint names, schema field lists
- Line counts, file counts, time durations (unless the duration is the memorable point)
- "没真测过" / "下次再调" / pure status updates

**Keep**:
- The insight (what's now different in your understanding of the world)
- The decision (what was chosen and why, in 5 seconds)
- The outcome (what's now possible that wasn't yesterday)
- Risk noticed (goes to `#commit` per § H4)
- Concrete domain detail when it's load-bearing (e.g. "Clash TUN 挂死 baostock socket" — keep, because the lesson is transferable)

**Self-audit hook**: every Stop hook fires `schedule-self-audit.sh`. It detects schedule edits and prepends `[schedule-audit]` to the next user prompt with the 1-year checklist. Seeing it means: revise the entries you just wrote BEFORE answering the next user query.

Voice rules (after granularity is right):

```
□  Prose, not bullet piles (3 lines of prose > 5 bullets)
□  Verbs that say what happened — not corporate "implementations completed"
□  Profanity preserved if user used it
```

Detailed rules + reference rewrites → @${CLAUDE_SKILL_DIR}/playbooks/tone.md

## § H6 — Cross-session forensics

User asks "what did we say on day X" → walk:

```
1. List session logs by mtime → identify candidates near day X
2. Filter by absolute date in timestamp (NEVER by file mtime)
3. Extract user + agent messages with timestamps
4. Surface to user → confirm content matches their memory
5. Write into dated file ONLY after confirmation
```

Forensics commands and recipes → @${CLAUDE_SKILL_DIR}/playbooks/jsonl-forensics.md

## § H7 — Tag aggregation page

Single index file (`tag-index.md` or equivalent) lists every project-tagged time-block as one row.

```
□  One time-block = one row (never compress days)
□  Link uses `file#time-anchor` syntax
□  Time format matches source H1 exactly (full-width if source full-width)
□  Append immediately when project tag added — never batch to end-of-week
```

Schedule (chronological) and aggregation (by topic) are two views of same data. Must agree.

## § H8 — Trigger table

| User says / does | Agent does |
|---|---|
| "create today's" / "创建今天的" | verify session date → copy @${CLAUDE_SKILL_DIR}/templates/SCHEDULE_TEMPLATE.md → rename to date stem → preserve empty time-blocks |
| "format this md" | normalize separators, tag levels, spacing — do NOT rewrite prose |
| dictates current event | session timestamp's current block → write |
| dictates timed past event | use stated time → convert relatives to absolute dates |
| dictates past event, no time | ASK user (do not write yet) |
| "go find day X" | § H6 forensics → confirm with user → write |
| "make X concise" | distill to result + significance per § H5 — drop procedure, drop tool names |
| `#协作` segment present | § H4 evaluation — write commit only if risk/dep/uncertainty |
| project-tagged segment added | mirror to aggregation page same turn |
| `[schedule-drift-check]` system-reminder appears | hook detected drift — see § H9 hook protocol for autonomy split |

## § H9 — Project pulse (derived snapshot)

When project has > 7 dated schedule files, maintain `PULSE.md` at project root. It is the project-level answer to § H5's two questions: what's the current state, why this state matters for any new collaborator entering the project.

Trigger pulse refresh when:

```
□  Sunday weekly retrospective (manual user-initiated)
□  user says "refresh pulse" / "刷新 pulse"
□  PULSE.md absent (with >7 schedule files) OR stale (>7d since refresh)
   ← detected by:
     • § H0 Pulse-aware job (cold-start, on first activation in project)
     • scripts/schedule-drift-check.sh Stop hook (Mon + Fri, once/day)
```

### Hook protocol — autonomy split

When `[schedule-drift-check]` system-reminder appears, drift class determines
how AI responds:

| Drift class | AI response | Why |
|---|---|---|
| Aggregate page out of sync | **Auto-fix** — append missing rows in next response, show user the diff | Pure data sync, no judgment needed (§ H7 already mandates this same-turn) |
| PULSE.md stale > 7d | **Propose refresh** — list § H9 ASK-user questions, wait for confirmation | "当下气压" / "应该知道" sections cannot be derived; AI fabricating vibes is worse than no refresh |
| PULSE.md absent + > 7 files | **Propose creation** — explain why this project crossed threshold, ask if user wants to scaffold | First PULSE is a contract for future collaborators; user must set the baseline tone |

Never silently refresh a PULSE without user confirmation. The hook reports;
AI proposes; user decides. This is non-negotiable per § H9 ASK-user rule.

Refresh procedure (when triggered, walk this):

```
0. AUDIT aggregate page (per § H7): scan past 7 days schedule for
   #project-tag entries → backfill ALL missing rows BEFORE step 1.
   Pulse depends on accurate aggregate; never skip.
1. Read templates/PULSE_TEMPLATE.md (the 9-section skeleton)
2. Derive each section from sources:
   - 一句话 / Stage      → CLAUDE.md first line + git tags
   - 心跳                 → CLAUDE.md Progress + most recent 7 days schedule
   - 当下气压             → ASK user (subjective, AI cannot derive)
   - 历史阶段             → git tags + schedule milestones tagged with #milestone
   - 应该知道             → ASK user (cross-cutting context, AI cannot derive)
   - 不要做的事           → CLAUDE.md "Do not" + unresolved schedule #commit risks
   - 时间锚点入口         → most-cited #project-tag entries from tag-index
3. Show diff to user → user confirms or edits
4. Write to PULSE.md → update "Last refreshed" date
```

Sections marked ASK user are the soul of pulse — vibes cannot be derived, they must be stated. If user does not respond, leave the prior content; do NOT fabricate a vibe.

Anti-defaults (this section overrides):

| AI default when entering project | What pulse forces instead |
|---|---|
| Treat every project as identical | Read 🟢/🟡/🔴 status, calibrate caution |
| Guess user count from code scale | Read explicit user count from PULSE |
| Ignore legal/compliance state | Read deadline countdown from PULSE |
| Lose time pressure context | Read milestone history + (← now) marker |

---

## — Completion criteria —

```
□  Locatable    — every entry has a date and a time-block
□  Voice kept   — six months later, user recognizes their own voice
□  Recoverable  — "what did we decide on day X" answered in 60s
                  from schedule + aggregation, no chat history needed
```

---

*The schedule held the line. See you on the slopes.* ⛷️

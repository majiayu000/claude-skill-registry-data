---
name: vabene-interview-recruiter
description: Drafts comment-first then DM Reddit outreach for qualified interview leads from interview-finder/reddit-monitor, tracks state through the recruit lifecycle, surfaces stalled threads for follow-up. Closes the loop between lead-finding and synthesis. Never sends anything automatically.
version: "0.1.0"
author: ben
requires:
  tools:
    - bash
    - telegram
triggers:
  - "recruit"
  - "draft invites"
  - "stalled threads"
  - "recruit-status"
  - "recruiter status"
---

# VaBene Interview Recruiter

## Purpose

Close the gap between qualified leads (from `vabene-interview-finder` and, optionally, `vabene-reddit-monitor`) and processed transcripts (in `vabene-discovery-synthesis`). Today the middle (drafting personalized invites, tracking who's been contacted/replied/scheduled, gift-card delivery, stalled-thread follow-ups) is manual and untracked, so leads rot in MEMORY.md.

The recruiter drafts outreach (always for human dispatch — never auto-sends), tracks state via Telegram-reply commands, and pings Ben when threads stall.

**Hard rules:**

- This skill NEVER sends a Reddit comment, DM, or any other outbound message. All dispatch is manual after Telegram review.
- DM drafts must include three consent elements; if any is missing the agent regenerates instead of dispatching to Telegram.
- Comment-first is the default Reddit path. DM-first only via the explicit `skip-comment` override (when the original post invites DMs or the subreddit allows research recruitment).
- State transitions go through `recruit-status <id> <state>` Telegram commands or manual MEMORY.md edits via SSH. No auto-progression.

---

## State machine

```
pending           lead exists in MEMORY.md (from interview-finder or reddit-monitor), recruiter not yet drafted
   ↓ (recruiter run)
comment_drafted   public comment draft + Telegram dispatch
   ↓ (Ben sends, replies "recruit-status <id> commented")
commented
   ↓ (target replies to comment in-thread; Ben replies "recruit-status <id> engaged")
engaged
   ↓ (recruiter run)
dm_drafted        DM draft with consent block + Telegram dispatch
   ↓ (Ben sends, replies "recruit-status <id> dm-sent")
dm_sent
   ↓
replied | scheduled | interviewed | declined | ghosted | gift_sent
```

**Override**: `recruit-status <id> skip-comment` jumps `pending → dm_drafted` directly. Use only when the original post explicitly invites DMs or the sub is known to allow research recruitment.

State changes always APPEND a new MEMORY.md entry. Never edit-in-place — the history of state transitions is the audit log.

---

## Per-lead workflow

### Step 1 — Discover leads

```bash
MEMFILE="$HOME/.openclaw/workspace/MEMORY.md"
[[ -f "$MEMFILE" ]] || { echo "ERROR: MEMORY.md missing at $MEMFILE" >&2; exit 1; }
```

Read MEMORY.md, extract entries from `interview-finder` (and optionally `reddit-monitor` if Ben wants it as a recruiter source). Group by `lead_id`. Filter to leads where the latest entry has `outcome: "pending"`.

### Step 2 — Cross-skill dedup

The same Reddit URL can be surfaced by both `interview-finder` (pain profile) and `reddit-monitor` (acquisition profile). Both skills emit a deterministic `lead_id` (`sha256(normalized_url)[:12]`); the recruiter dedupes on it.

For each `lead_id`:

1. Take the highest-confidence source entry (HIGH > MED) as canonical.
2. Record the merger: `merge_sources: ["interview-finder", "reddit-monitor"]` on the recruiter draft entry.
3. Skip if any prior recruiter entry exists for this `lead_id` (i.e., recruiter has already drafted/sent something — don't re-draft).

### Step 3 — Draft per state

**`pending` → `comment_drafted`** (default Reddit path):

Draft a public comment that:

- Adds value to the thread (answers their question, validates their pain, shares a relevant resource).
- Does NOT pitch the interview directly.
- Establishes Ben as a person interested in the same problem space.
- Length: 2–4 sentences.
- Voice: **first-person founder** ("I'm building something in this space and seeing the same problem"), not corporate ("VaBene helps planners…"). Pre-PMF, first-person is the right call.

**`engaged` → `dm_drafted`**:

Draft a DM that contains all three consent elements (the agent self-checks; if any is missing, regenerates and does NOT dispatch):

1. **Recording disclosure**: explicit statement that, with permission, the call may be recorded so notes can be reviewed afterward.
2. **Use-of-data sentence**: how the data is used (private notes, no quotes shared externally without explicit follow-up consent).
3. **Opt-out language**: participant can decline recording, stop the call, or pass on any question without explanation.

Plus:

- Specific detail from the original post (proves it's not a template blast).
- Time ask: "20-min call".
- Incentive: "$25 gift card" or whatever Ben sets via env var `INTERVIEW_INCENTIVE_USD`.
- Same first-person founder voice as the comment.

### Step 4 — Send to Telegram (review-only)

For `comment_drafted` and `dm_drafted` states, send the draft to Telegram with the lead context, full draft text, and explicit "REVIEW BEFORE SENDING" framing. See "Telegram message formats" below.

### Step 5 — Stalled-thread sweep (daily)

Trigger: `stalled threads`. Default cron 09:30 PT.

For each lead currently in `commented` or `dm_sent`:

- If `now - outcome_updated_at > 5d` and no further state change → Telegram nudge ("Lead `<id>` no movement in 5d — comment follow-up Y/N? DM follow-up Y/N?")
- If Ben replies `recruit-status <id> followup-comment` or `recruit-status <id> followup-dm`, draft a follow-up message **with a different angle from the first** (never identical re-send).
- Never auto-resend.

Heartbeat: if zero stalled threads, send `🔁 Recruiter: no stalled threads.` Telegram message.

### Step 6 — Scheduled & interviewed cues

When state transitions to `scheduled` (via `recruit-status <id> scheduled`):

- Day-before reminder ping with the original post context refresher (so Ben goes into the call with the right backstory).

When state transitions to `interviewed` (via `recruit-status <id> interviewed`):

- Reminder check: look for a transcript file matching this lead in `~/.openclaw/agents/main/transcripts/`. Filename convention is `YYYY-MM-DD-<participant-handle>.md`.
- If no transcript file exists 24h after the `interviewed` state change → ping Ben to drop the transcript so `vabene-discovery-synthesis` can process it.

### Step 7 — Gift-card and close

`recruit-status <id> gift-sent` is the terminal state. Closes the audit chain.

---

## MEMORY.md JSONL schema (pinned at v0.1)

Every state change appends one line:

```jsonl
{"schema_version":"0.1","ts":"2026-04-26T18:00:00-07:00","scan":"recruiter","lead_id":"a3f1b2c4d5e6","outcome":"comment_drafted","outcome_updated_at":"2026-04-26T18:00:00-07:00","merge_sources":["interview-finder"],"channel":"comment","draft_text":"<full draft, only on *_drafted states>","notes":"<free-text from Ben on state transition, optional>"}
```

Field reference:

- `schema_version` — always `"0.1"` from this skill at v0.1.0.
- `ts` — ISO 8601 with PT offset; when this entry was written.
- `scan` — always `"recruiter"`.
- `lead_id` — 12-char hex prefix of `sha256(normalized_url)`. Same hash function as `interview-finder` and `reddit-monitor` (cross-skill dedup contract).
- `outcome` — one of: `pending` (only set by upstream skills, never recruiter), `comment_drafted`, `commented`, `engaged`, `dm_drafted`, `dm_sent`, `replied`, `scheduled`, `interviewed`, `declined`, `ghosted`, `gift_sent`.
- `outcome_updated_at` — when this state transition happened (typically same as `ts`, but separate field so you can backdate manually for testing).
- `merge_sources` — array of upstream `scan` values that contributed; usually one, sometimes both `interview-finder` and `reddit-monitor`.
- `channel` — `"comment"` or `"dm"`. Tracks which artifact the recruiter is drafting at this state.
- `draft_text` — present only on `*_drafted` states; full text of the drafted comment or DM.
- `notes` — optional free-text Ben can include in the `recruit-status` command (e.g., `recruit-status <id> declined no time this month`).

### `lead_id` normalization (cross-skill contract)

```
input:  https://www.reddit.com/r/SanFrancisco/comments/abc123/whatever_title/?utm_source=x#comment
output: sha256("reddit.com/r/sanfrancisco/comments/abc123")[:12]  (lowercase host, canonical post ID, no query, no anchor)
```

Both `interview-finder` and `reddit-monitor` MUST use the same function. The recruiter trusts `lead_id` as an opaque dedup key; if upstream emits a hash with different normalization, the recruiter will treat the same URL as two leads. Fix at the source.

---

## Telegram message formats

### Comment draft ready

```
💬 Recruiter — comment draft (REVIEW BEFORE SENDING)

Lead: a3f1b2c4d5e6 | Sub: r/SanFrancisco | Score: HIGH (5/6)
🔗 https://reddit.com/r/SanFrancisco/comments/abc123/...

Original post snippet: "Turning 30 next month, 8 of us, can't agree on..."

Draft comment:
---
[2-4 sentence comment, first-person founder voice]
---

After you post: reply 'recruit-status a3f1b2c4d5e6 commented'
If you'd rather skip the comment and DM directly: 'recruit-status a3f1b2c4d5e6 skip-comment'
```

### DM draft ready

```
✉️ Recruiter — DM draft (REVIEW BEFORE SENDING)

Lead: a3f1b2c4d5e6 | After comment engagement
🔗 https://reddit.com/r/.../...

Draft DM:
---
[DM text — must contain: recording disclosure, use-of-data sentence, opt-out language, original-post detail, 20-min ask, $25 incentive]
---

✓ recording disclosure present
✓ use-of-data present
✓ opt-out language present

After you send: reply 'recruit-status a3f1b2c4d5e6 dm-sent'
```

### Stalled-thread nudge

```
🔁 Recruiter — stalled (no movement in 5d)

Lead: a3f1b2c4d5e6 | Last state: dm_sent (2026-04-21)
🔗 https://reddit.com/r/.../...

Reply with one of:
  'recruit-status a3f1b2c4d5e6 followup-dm'      → draft a different-angle follow-up DM
  'recruit-status a3f1b2c4d5e6 ghosted'           → close as no-response
  'recruit-status a3f1b2c4d5e6 declined'          → close as declined
```

### Scheduled — day-before refresher

```
📅 Recruiter — interview tomorrow

Lead: a3f1b2c4d5e6 | u/<handle> | r/<sub>
Original post (refresher): "<snippet>"
Trigger event: <from finder>
Workaround they tried: <from finder>
Pain dollar value (if quantified): <from finder>
🔗 https://reddit.com/r/.../...

Suggested opening: ask them to walk you through the moment that made them start looking for a solution.
```

### Interviewed — transcript drop reminder (T+24h)

```
📂 Recruiter — transcript not yet in watched dir

Lead: a3f1b2c4d5e6 (interviewed 24h ago)
Expected file: ~/.openclaw/agents/main/transcripts/<YYYY-MM-DD>-<handle>.md
Recommended source: Otter or Granola Markdown export.
discovery-synthesis won't pick this up until the file lands.
```

### Empty stalled sweep heartbeat

```
🔁 Recruiter: no stalled threads.
```

---

## Cron Setup

Deferred. Wire only after ≥ 3 successful manual runs covering all branches: comment_drafted, commented, engaged → dm_drafted, dm_sent, stalled-thread sweep, skip-comment override, cross-skill dedup. For reference / future creation:

```bash
# Per-run draft generation — every 4 hours during waking hours
openclaw cron add \
  --name "VaBene Interview Recruiter" \
  --cron "0 9,13,17,21 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Run the vabene-interview-recruiter skill. Draft outreach for any pending leads, handle state transitions from Telegram replies. Never send anything automatically." \
  --model claude-sonnet-4-6 \
  --to <TELEGRAM_CHAT_ID> \
  --announce \
  --channel telegram

# Stalled-thread sweep — daily 9:30 PT
openclaw cron add \
  --name "VaBene Recruiter Stalled Sweep" \
  --cron "30 9 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Run the vabene-interview-recruiter skill with trigger 'stalled threads'. Surface any commented/dm_sent leads with no movement >5d." \
  --model claude-haiku-4-5-20251001 \
  --to <TELEGRAM_CHAT_ID> \
  --announce \
  --channel telegram
```

Sonnet for drafting (voice + consent self-check matters); Haiku is fine for the stalled-thread sweep (just MEMORY.md filtering and a Telegram render).

---

## Manual Telegram commands

| Command | What it does |
|---|---|
| `recruit` | Per-run draft pass for all pending leads |
| `draft invites` | Alias |
| `stalled threads` | Stalled-thread sweep (commented / dm_sent with no movement > 5d) |
| `recruiter status` | Counts by `outcome` over last 30d, list of leads in each terminal-non-final state |
| `recruit-status <lead_id> <state>` | State transition. States: `commented`, `engaged`, `skip-comment`, `dm-sent`, `replied`, `scheduled`, `interviewed`, `declined`, `ghosted`, `gift-sent`, `followup-comment`, `followup-dm`. Optional trailing free-text becomes `notes`. |

---

## Tuning levers (in priority order)

1. **Stalled-thread threshold** — default 5 days. Raise (7d) if Ben is following up too often; lower (3d) if leads are dying before nudges arrive.
2. **`INTERVIEW_INCENTIVE_USD`** — default 25. Raise if response rates are too low; lower if the recruiter pipeline is starting to feel paid-promotion-y.
3. **Comment template voice** — pre-PMF first-person ("I'm building…") is the v0.1 call. If post-PMF the brand is recognizable, switch to lower-key ("at VaBene we're trying to figure out…"). Document the change.
4. **Skip-comment heuristic** — currently only via explicit Ben override. If a fraction of subs are confirmed DM-friendly, the recruiter could auto-skip-comment for those subs. Don't add this until the skip-comment manual path has been used > 5 times to validate.

Document any tuning change in this skill's README change log. Voice and incentive especially — they're easy to fiddle and hard to A/B retroactively.

---

## Relationship to other skills

- **`vabene-interview-finder`** — upstream lead source. The recruiter consumes its `outcome: "pending"` entries and writes back recruiter-namespaced state transitions.
- **`vabene-reddit-monitor`** — optional secondary lead source. A post can qualify as both an acquisition lead (reddit-monitor) and an interview candidate (interview-finder); cross-skill dedup via `lead_id` ensures the recruiter drafts once.
- **`vabene-discovery-synthesis`** — downstream. The recruiter's `interviewed` state triggers a transcript-drop reminder; once the file lands, discovery-synthesis picks it up on its next run.

The three skills together form the customer-development loop: find → recruit → synthesize. All three follow the append-only MEMORY.md JSONL convention with `lead_id` / `transcript_id` cross-references, so the lifecycle of any single conversation is auditable end to end.

---

## Security

- Read-only on MEMORY.md for upstream entries; append-only for own entries.
- No outbound network calls beyond Telegram. No Reddit posting, no DM sending.
- DM drafts contain participant-specific detail extracted from public Reddit posts (no scraping of private profiles). Treat MEMORY.md as PII-bearing per the existing `memory/README.md` policy.
- All Telegram messages route through the configured bot.

---
name: daily-review
description: Status pass — where are we, what's next. Trigger when the user asks for "daily review", "what to work on", "what to focus on", "where are we", or any near-equivalent. ALSO runs automatically every morning before the user wakes (team-lead daily cron) to produce the day's status + hit list. Reviews peer transcripts + hive messages + open PRs + the weekly plan, asks each agent for context where needed, then writes a prioritized review doc to `.claude/reviews/YYYY-MM-DD.md` under live-feedback.
user-invocable: true
---

# Daily Review

The intra-day "where are we, what's next" pass. Pulls signal from across the fleet, asks agents for clarification where the transcript isn't enough, and writes a single dated file under live-feedback so the user can comment/edit on it from anywhere.

**Output:** `.claude/reviews/YYYY-MM-DD.md` (gitignored). One file per day. Brought under live-feedback via `create_review_doc` so the user can leave anchored comments and edit inline.

## Triggers

Invoke this skill whenever the user says any of:
- "daily review" / "review please" / "do a review"
- "what should I work on" / "what to focus on" / "what's next"
- "where are we" / "where do we stand" / "status check"
- "what's the team doing" / "team status"

These all map to the same thing: produce or update today's prioritized review doc.

**Automated morning run:** this skill also fires **every morning before the user wakes** (team-lead daily cron, ~5:30am local) — no ask needed. See `## Automated morning run` below.

## Automated morning run (fires each morning — no ask)

Each morning the team-lead's daily cron runs this skill automatically so the user wakes to a current status + a ready hit list. Do the normal Steps below, plus:

1. **Frame the output as a status + today's hit list** — the doc leads with where things stand after overnight, then the 2–4 things worth doing *today* (drawn from the committed weekly goals + whatever is newly unblocked or now needs the user).
   - **Order the hit list by goal priority, always.** Set by him on 2026-08-27, after he reordered it himself: *"Hit list should always be in order of goal priority."* Not by size, not by what is quickest, not by the order you discovered them. If your order and the plan's goal numbering disagree, that is a signal the numbering is stale — say so rather than silently picking one.
2. **Do NOT touch Asana.** Removed 2026-09-16 on the user's instruction: *"Stop the Asana syncs. It's duplicating stuff that's on the workspaces."* The workspace boards and his Home review queue are the task surface; a mirrored Asana list was a second copy of the same asks, and two surfaces meant two places for the same thing to go stale. Do not create, re-date, complete or reword Asana tasks, and do not read Asana to build the hit list — take it from the weekly plan and the boards.
3. **Send one morning push** — `PushNotification`: `"Good morning — today: <2–4 hit-list items>."` Nothing else unless something genuinely can't wait (then flag it in the push).

Keep it cheap and otherwise silent. The review doc IS the morning communication — don't also message the user separately. Still surface the review URL first (step 6) in-session for when the user checks.

## Say it out loud when the week is going off track (set 2026-08-17)

The user asked for this directly: *"let's see how this week goes -- you can put it in your notes to ping me when you do daily review if it looks like we're off track."*

**The failure this exists to catch is a week that ends with four goals at zero and nobody having said so on Wednesday.** Writing "Status: slipping" into the doc does not count — he may not open it, and a status field reads as bookkeeping. Say it in the push, in one sentence, naming what to drop.

Check these every run, against this week's plan:

- **Has a committed goal moved at all?** A goal with no evidence of movement by midweek is off track regardless of its due date. The measure of a slipping week is a goal at zero, not a goal that is behind.
- **Is one goal absorbing the week?** The recurring pattern is that one large goal takes everything and the small ones were booked as if it wouldn't. If the big goal's share is running away, the small ones are already lost — say so while there is still room to protect a slot.
- **Did a day disappear?** Illness, a flare, unplanned logistics. He will usually mention it in passing rather than as a planning input. Treat it as one: redo the capacity block and name which goal comes off.

**Wednesday is the deadline for saying it**, not Friday. By Friday the only available move is to write the week off; on Wednesday there is still a choice about what to cut.

## Steps

1. **Collect raw signal.**
   - Peer state: `mcp__claude-hive__list_peers` (machine scope) — current summaries.
   - Peer transcripts: use `analyze_transcript.py` (see `docs/process/learnings.md` § Retros) to scan today's transcripts for each peer. Don't write custom parsing.
   - Hive messages today: `mcp__claude-hive__check_messages` — anything in your inbox.
   - Fleet PRs: `gh pr list --json number,title,state,reviewDecision,updatedAt --repo <repo>` per registered repo (parallel via Bash background).
   - Live-feedback threads on the weekly plan + other watched docs: `list_threads`.
   - Discord messages: `fetch_messages` since last review.
   - **Fleet health: read `/opt/fleet/healthcheck-status.json`.** Every RED goes in the review. This is the step that owns the outcome — the checker writes a log and fires a notification, and until this bullet existed, nothing anywhere was defined as reading either. It ran 22 times with 116 RED lines and three failures red on *every single run* before anyone looked (2026-08-18).
     - **The status file lives beside the DEPLOYED config, not under `~/Library`.** `fleet_healthcheck.py` resolves its state dir to the first directory that actually holds `healthcheck-config.json` — its own directory, then `/opt/fleet`, then `~/Library/Application Support/team-lead` — and in practice that is `/opt/fleet`. This bullet named the `~/Library` path from 2026-08-18 to 2026-09-12; nothing is there, so a review following it literally read no health state at all and silently reported no REDs. Corrected after finding the real file current and green at `/opt/fleet`.
     - **A missing status file is "could not look", never "all clear."** Say so in the review in those words and treat it as its own RED — the checker not having run is worse news than any single check failing, and it is the one failure that hides every other. Same rule as the leak gate's three states.
     - **`launchctl list com.fryanpan.fleet-healthcheck` showing exit status 1 is NORMAL** — the checker exits non-zero whenever it finds a RED. It is evidence the job ran, not that it broke. Read `checked_at` in the status file to judge freshness; a stale timestamp is the real alarm.

2. **Ask peers for context only where the transcript isn't enough.**
   - For each peer working a committed goal, decide: is what they did today obvious from the transcript? If yes, skip the ping.
   - If not — `send_message` with a tight question ("Status on <goal title>? One-line summary + any blocker.") and wait for the reply before writing the section.
   - Don't ping peers that have been silent and aren't on a committed goal.

3. **Anchor priority on the weekly plan.**
   - Read this week's plan doc, `.claude/reviews/weekly-YYYY-MM-DD.md` (the one `weekly-plan` set up, bound to the Team Lead workspace as docId `weekly-YYYY-MM-DD`). Pull the committed goals in priority order. **Not Notion** — weekly planning moved to the workspace on 2026-08-17.
   - Cross-check against the workspace board (`get_workspace` for goal order, `next_tasks` for what's ready). The board is where goal priority actually lives; the doc is the narrative.
   - The review doc's outline = those goals, in the same order, plus a final section for things off-plan.

4. **Write or update `.claude/reviews/YYYY-MM-DD.md`.**

   If the file doesn't exist yet today, create it with this shape. If it does, append `## Update HH:MM` with the same shape inside.

   ```markdown
   # Daily review — YYYY-MM-DD

   *One sentence: where the day stands overall.*

   ## 1. <Goal title from weekly plan>

   - **Owner**: <agent name(s) + the user if applicable>
   - **Status**: on-track | slipping | blocked | done
   - **Today**: <one or two lines on what moved / who did what>
   - **Next for you**: <decision needed | review needed | nothing — keep moving>
   - **Link**: <github.com/... or mac-mini.<tailnet>.ts.net/... — only if useful>

   ## 2. <Next goal title>

   - **Owner**: …
   - **Status**: …
   - **Today**: …
   - **Next for you**: …

   ## Off-plan

   - <thing that came up that isn't a committed goal — in priority order>

   ## Decisions needed from you

   ### <Decision 1 title>

   - **Question**: <one sentence>
   - **Options**: <2-4 options, each one line>
   - **Cost**: <time / scope / reversibility per option>
   - **Recommendation**: <Team Lead's call, or "no recommendation">

   ### <Decision 2 title>

   …
   ```

   **Critical**: each field MUST be its own bullet, not run-on prose with inline bold labels. The live-feedback editor renders the doc on Bryan's phone — bullet-per-field stays scannable; prose-with-bold-labels collapses into wall-of-text. See `feedback_live_feedback_doc_structure.md` memory for the rationale.

   - Sections are **descending priority** (1 = highest priority committed goal).
   - Within each goal-section, batch *every* type of work (writing, decisions, pings, reviews) for that goal — don't cluster by task type across goals.
   - Links MUST be Tailscale (`*.<your-tailnet>.ts.net`) or GitHub (`github.com/...`). Never `*.local`. the user reads on phone over cellular.

5. **Bring the doc under live-feedback.**
   - On first creation for the day, call `create_review_doc(docId, path)` where `docId` is `daily-review-YYYY-MM-DD` and `path` is the absolute path to the file.
   - Capture the `reviewUrl`. Rewrite any `<your-mac>.local:8788` portion to `mac-mini.<your-tailnet>.ts.net:8788` before surfacing.
   - Call `watch_doc(docId)` so thread events arrive as channel notifications.
   - On updates within the same day, the live-feedback editor stays in sync with the file. Don't re-call `create_review_doc`.

6. **Surface the doc to the user — link FIRST, every time.**
   - **The very first line of your user-facing response MUST be the WORKSPACE URL on its own line**: `http://mac-mini.<your-tailnet>.ts.net:8787/workspaces/<workspace_id>` (the Team Lead workspace id lives in `.claude/skills/weekly-plan/parent.txt`). No preamble, no "here's the review", no apology — just the URL.
   - **Never surface a bare `/review/<docId>` link.** `create_review_doc` returns a `reviewUrl` and pasting it is the easy mistake, but it opens the document by itself — no goal bands, no task board, none of the surface the review is meant to be read against. Attach the doc to the workspace and link the workspace.
   - This applies on every invocation: first creation, every update / re-run, and any time the user asks "what's next" / "status" / "where are we." The URL is the user's only entry point on phone or laptop; if it's buried, he has to dig for it.
   - After the URL, you may add a one-sentence pointer (morning: which goal-section to start with; evening: what shipped + tomorrow's first goal).
   - The URL is non-negotiable. Even if you have nothing else to say, surface the URL.

7. **React to the user's comments + edits.**
   - Thread events arrive as channel notifications — handle them per the live-feedback skill (`feedback-threads` for triage, the `editing-review-docs` skill for any edits to the file).
   - When the user edits a section directly, re-read the file and carry his changes forward into peer dispatches.
   - Resolved threads = decisions made. Reflect them back into the weekly plan if they change goal priority or scope.

## Every RED health check gets an owner and an age

A RED that appears in the review with no owner is the same as a RED nobody read. For each one, say **who can clear it** — you, Bryan, or a named peer — and **how many consecutive runs it has been red**. Age is the part that distinguishes a new outage from furniture.

- **Red for the first time** → treat as an outage; diagnose it in the review.
- **Red every run for days** → it is blocked on someone. Name them and say what specifically they have to do. "The email watcher's Google Cloud project is deleted; only you can recreate it" is actionable. "email watcher: RED" is furniture.
- **Blocked on Bryan** → it belongs in `## Decisions needed from you`, not buried in Off-plan.

## Inline content or Tailscale link — never a forward-reference

Every actionable item in the daily review must be either:

- **Inline**, if it's brief enough to scan in seconds (1-3 sentences), OR
- **Linked via a Tailscale URL** (`mac-mini.<your-tailnet>.ts.net:...`) to a live-feedback-bound doc or other accessible artifact, if the content is longer.

**Never use forward-references** like "see Decisions §N" or "see below" or "ask <peer> for details." If the user has to scroll/navigate/ping to find what they need, the daily review failed its job. The user reads on phone — every "see X" is a context switch he pays for.

**Link the noun, not the bullet.** A trailing `- **Link**: <url>` still makes him hunt — he reads "PR #1669 still reads DRAFT" and has to scroll to find it. Put the link on the phrase itself, at first mention (Bryan, 2026-08-18: *"Please give me inline links in the daily review wherever possible. so I don't have to hunt them down"*). Keep the trailing Link bullet only for the section's home surface.

- Link every artifact you name, individually — each PR, not "PRs #187, #213 and #214" as bare text; a settings change straight to the settings page.
- One link per bullet — he skims bullet → click → return → next.
- **Verify every URL resolves before it goes in** (`gh pr view`, an API call). Where you don't have one, name what to open and ask him to paste it once. A dead link costs him more than a missing one, because he only finds out after the context switch.
- Watch for a link that is correct but points at the wrong state — a GitHub file link whose relevant content is still on an unpushed branch opens a version without it.

When in doubt: paste the content inline. Better to have a longer bullet than a forward-reference. If a bullet grows past ~5 lines, that's the signal to move the long content to a separate Tailscale-linked doc and inline a 1-2-sentence summary plus the link.

## Amending the doc during the day — where the wall of text comes from

A daily review is edited all day as corrections land. **The failure is never a bullet written too long; it is a bullet appended to five times.** Each edit looks reasonable in isolation and the block is never re-read as a whole.

- **Ceiling: three sentences (~300 characters) per bullet.** Countable, not a matter of taste.
- **After any `find_and_replace`, re-read the whole block you touched** — not just your replacement.
- **A correction that doesn't fit becomes its own bullet** with its own bold label (**Retracted**, **Superseded**, **New number**). It is a different information type, so it was never eligible to share a bullet.
- **If a bullet is already over the ceiling, restructure instead of editing**: `create_anchor` on the section HEADING, `insert_blocks_at_anchor` the full replacement list, then delete the old blocks. Anchoring on a list item makes the inserted bullets CHILDREN of that item, and deleting the parent then destroys them — cost several wasted rounds on 2026-08-18.
- **Verify by measuring, before you declare it fixed**: `awk 'length($0)>300 {print length($0)}' .claude/reviews/YYYY-MM-DD.md` should print nothing.

## What to avoid

- **Don't write "blocked on" / "waiting on" / "holding" without checking the peer's transcript.** The tmux pane is a render, not state — it cannot show what a session received. Grep `~/.claude/projects/<encoded-cwd>/*.jsonl` for its last processed turn; if that turn is newer than the supposed blocker, the session was never blocked. Text on the `❯` line is inert, not a pending message. This skill is where a fabricated five-day fleet blocker got escalated three days running (2026-08-03); see the killer item in `CLAUDE.md`.
- Don't write a free-form narrative. the user scans, doesn't read.
- Don't forward-reference. See "Inline content or Tailscale link" above.
- Don't repeat content the weekly plan already has. The review doc references goal titles and reports status — it doesn't re-justify the goals.
- Don't bury decisions inside goal-sections; promote them to the `Decisions needed` section.
- Don't include `*.local` URLs. the user reads on phone.
- Don't ping peers who have nothing to add. The review reflects what happened, not what you wish had happened.
- Don't grade the user's pace. Report status, not judgment.
- Don't `Write`/`Edit` the .md file directly once it's under live-feedback — route through the MCP edit tools per `editing-review-docs` skill.

## Decisions section — give enough background

Every decision in the `Decisions needed from the user` section must include:
- What's the question (one sentence)
- What are the realistic options (2-4 options, each one line)
- What does each option cost (time, scope, reversibility)
- A Team Lead recommendation if there is one — say "no recommendation" if not

If the user would have to chase down context to make the call, the section isn't done.

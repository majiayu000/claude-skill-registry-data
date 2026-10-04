---
name: morning-digest
description: Use for the daily ~7AM prep — what needs Bryan, meeting prep, today's focus, yesterday's output, and token spend. Fires from a board schedule; also user-invocable.
user-invocable: true
---

# Morning Digest

Bryan's one morning artifact. Set by him 2026-09-18: *"every morning at 7AM you prep me
for the day."* It **replaces** the old 05:27 `daily-review` automated morning run — two
briefings ninety minutes apart is the failure this skill exists to prevent, not a feature.

`daily-review` remains the skill for an intra-day "where are we" pass and keeps its own
triggers. This one owns the morning.

## How it fires

**A board schedule on the morning-digest row of the Team Lead board, not `CronCreate`.** Bryan authorised the switch on
2026-09-18. The rule is a daily calendar rule at **06:47 PT** — early enough that the
digest is written and pushed by 7, because the gathering takes minutes and a job that
*starts* at 7 delivers late.

**Never re-arm this as a session cron.** `CronCreate` is in-memory: it dies on every
respawn and auto-expires after 7 days. That is not a theoretical failure — on 2026-09-01
`CronList` returned "No scheduled jobs" with the re-arm directive sitting unread in
context and the last quota reading 50 hours old. The hole it leaves is a *missing* line,
and nothing alerts on an absence. A schedule on the row survives the respawn that kills a
cron.

## Output shape

**One doc, one push, five sections in this order.** The order is Bryan's, from the ask.
Do not reorder by what you found most interesting.

1. **Needs you** — last 48h across every approved channel, unreplied or worth knowing.
2. **Meetings today** — with prep, excluding recurring blocks with his partner.
3. **Focus today** — at most 5 bullets.
4. **Yesterday** — exactly 5 bullets.
5. **Token spend** — 3 lines.

- **The doc lives OUTSIDE this repo**, at
  `~/Library/Application Support/team-lead/digests/YYYY-MM-DD.md`, bound to the Team Lead
  workspace as docId `morning-digest-YYYY-MM-DD`. Set by Bryan 2026-09-18: *"Make sure to
  store the daily digest somewhere private. Not pushed to git."*

**Gitignored inside a public repo is not private enough for this file, and that is why it
sits outside.** The digest carries his email, his calendar, and prep naming real people —
a different class of content from anything `.claude/reviews/` has held. A gitignored path
is one `git add -f`, one `.gitignore` edit or one `git clean` away from being tracked or
gone, and the pre-push leak gate only ever scans content that is already tracked, so it
cannot catch this. A file outside the working tree cannot be committed by any of those
accidents. Never move it back in, and never link to it by filesystem path — the bound doc
is how he reads it.
- **Surface the WORKSPACE url**, never the bare `/review/<docId>`. The id lives in
  `.claude/skills/weekly-plan/parent.txt`.
- **One push, under 200 characters**: the 2–3 things that actually need him today. Not a
  summary of the doc — the doc is the summary.
- **Every field is its own bullet with a bold label.** Prose-with-inline-bold collapses to
  a wall of text on a phone.
- **Links are Tailscale or GitHub, never `*.local`**, and go on the noun at first mention.

**Every item links its own artifact, in every section.** Asked for on the first run:
*"Provide links to Deepcell, learnings-gate-hazards branch, and other unclear items."*
An item that names a thing he would have to go find — an email thread, a branch, a PR, a
board row, a settings pane — carries the link on the noun at first mention.

- **A Gmail thread** is `https://mail.google.com/mail/u/0/#inbox/<threadId>`; the
  connector returns `threadId` on every search hit, so there is no excuse for naming a
  sender without one.
- **Where no URL exists, say so and say what to open.** An unpushed branch has no GitHub
  page — write the branch name and the repo, not a link that 404s.
- **Verify a link resolves before it ships.** A dead link costs him more than a missing
  one, because he only finds out after the context switch.

**A setup step that only he can perform ships with its actual steps, not its name.**
*"Include specific step-by-step instructions for Full Disk Access (Messages) and Signal
device linking in daily updates."* Naming the task is what the digest had been doing, and
it leaves him to reconstruct the procedure every morning it reappears.

- **Write the pane path and the clicks**, e.g. System Settings → Privacy & Security →
  Full Disk Access → `+` → add the terminal app that runs this session.
- **Say where it can be done from.** *"instructions can be executed from Mac mini, SSH
  from phone/iPad, or remote desktop."* That is per-step and it matters: anything in
  System Settings needs the GUI, so it is the Mac mini directly or remote desktop — **not
  SSH**. A CLI step is fine over SSH from the phone or iPad.
- **Confirm the client before writing Signal's steps.** Linking differs between Signal
  Desktop (scan the QR it displays) and `signal-cli` (`link` prints a `sgnl://` URI you
  have to render as a QR yourself). Do not write one procedure as if it covered both.

## 1. Needs you

Read the last 48 hours. Two buckets, and they are different questions — keep them apart.

- **Unreplied to Bryan** — a thread whose **last message is not from him**. That is the
  test; do not use read/unread, which tracks whether a tab was open. Say who is waiting
  and for how long.
- **Worth knowing** — anything that changes his day even though nobody is waiting: a
  cancellation, a deadline moved, money, a reply on something he sent.
- **Say what it wants, not what it says.** "Needs a yes/no on Thursday" beats a summary
  of the paragraph that asked.
- **Three to six items.** If the 48h window is quiet, say so in one line rather than
  padding it with newsletters.
- **Never draft or send a reply from this skill.** The digest surfaces; sending is a
  separate act with its own approval.

### The bar is "needs him", not "involves him" (set 2026-09-18)

Three corrections on the first real run, all the same shape: the digest surfaced things
nobody was asking him for.

- **A PR is his to review only when HIS OWN LOGIN is on it.** `gh search prs
  --review-requested=<user>` **expands team membership** and returns every PR requesting
  any team he belongs to. Five came back that way on the first run and not one was his.
  *"I think none of these are assigned to me -- don't highlight these in the future unless
  assigned to me to review."* The correct test is the PR's own `reviewRequests` array —
  `gh pr view <n> --json reviewRequests` — checked for his login. Never use
  `--review-requested` to decide this.
- **"Worth knowing" is not a licence to include whatever you found.** A payment that
  cleared, a booking already confirmed, a thread someone else closed: if nothing turns on
  him, it does not go in. *"No need to bring these to my attention -- does not need me."*
- **Check whether he already handled it before you file it.** *"Already took care of
  this."* A thread whose last message is not from him can still be finished — by a phone
  call, a text, a form he submitted. Where the channel cannot show you, mark the item
  unconfirmed rather than asserting it is open.

### Recruiter email goes to the Job Search peer, not to him (set 2026-10-01)

*"When you get recruiter emails, pass them to Job search for review. Only highlight for me if
it looks interesting. Or they might be well connected and I just want to be on their radar."*

- **Send every recruiter thread to the Job Search peer**: sender, company, role, how many
  follow-ups so far, and the Gmail link. One message per digest run with all of them in it,
  not one message per email.
- **Job Search judges it, not the digest.** The digest does not decide that a role is
  uninteresting; it hands the thread over and stops.
- **It reaches "Needs you" only on Job Search's say-so**, for one of his two reasons: the role
  looks interesting, or the recruiter is well connected and worth staying on the radar of.
  Name which reason in the line.
- **Read Job Search's board for its verdicts on earlier handoffs** before writing the
  section. A recruiter it flagged yesterday belongs in today's digest even though the email
  is older than the run.
- **A recruiter's persistence is not a reason to surface it.** A third follow-up is noise
  until Job Search says otherwise.

### The Gmail connector is read-and-compose only

Measured 2026-09-18. Search, read and `create_draft` work. **`unlabel_thread`, label
edits, archive and trash all fail** with `Insufficient scope: required …
https://www.googleapis.com/auth/gmail.modify`. So this skill can surface a thread and it
can never mark one read or clear it — say that plainly when asked, and do not route
around it.

**`update_draft` DETACHES a draft from its thread.** It returns a new `threadId` equal to
its own `messageId`, and the reply then arrives as a fresh conversation. To change a
threaded draft, create a replacement with `replyToMessageId` and confirm the returned
`threadId` still matches the original. The orphan cannot be trashed from here — it is
Bryan's to delete, so tell him it exists.

**A quiet inbox and a failed search read the same.** If the search returns nothing, say
which query ran and that it ran — "no unreplied threads in 48h (searched `newer_than:2d`
across N threads)". An empty section with no denominator is indistinguishable from a
broken one.

### Which channels this sweeps

**Answered 2026-09-18:** *"Slack, Messages and Signal. Research if there's a clean way to
handle WhatsApp."* All four are wanted. Three have a path; one does not yet.

**Which channels are in was his call, not a technical one.** Do not widen the sweep on
your own judgement, and do not narrow it either.

- **Gmail** — on now.
- **Slack** — on now. The connector was already authorised, so this needed nothing from
  him. Same unreplied test as email: the last message in the thread or DM is not from
  him. Sweep DMs and channels where he is @-mentioned — **not** every channel he belongs
  to, which is a newsletter, not an inbox.
- **Messages (iMessage)** — approved, blocked on a Full Disk Access grant only he can
  make. No connector exists; the history is a local SQLite store under his Library. That
  grant is machine-wide rather than scoped to Messages, so **never perform it, script it,
  or prompt for it mid-digest** — the steps live on the channel-scope row and he does it
  in System Settings.
- **Signal** — approved, blocked on him linking this machine as a second device. There is
  no API, by design; `signal-cli` works by linking, which means a QR scan from his phone
  and real message history stored on this machine.
- **WhatsApp** — **not approved. Open research question.** He asked whether a clean path
  exists, which is not the same as approving one. Until one is found and he says yes, do
  not read WhatsApp by any route. The Business API covers business numbers only; the
  desktop client's local store and unofficial bridges both breach the terms, with a
  documented consequence of the number being banned.

**Name the channels this run actually read, every time.** "Nothing needs you" means
nothing in the channels that were swept, and a reader cannot tell which those were unless
the line says so. An approved-but-not-yet-wired channel reads as swept otherwise, which
is the failure this line exists to prevent.

## 2. Meetings today

**Pull all three of his calendars** — the ids are in `registry.yaml` under `calendars:`,
which is gitignored because this repo is public and a calendar id is a real address.
Run `list_calendars` first and look for a new personal or household one; the other ~16
entries are subscriptions and are not his commitments.

- **Exclude recurring blocks with his partner.** His words. A one-off with her is a real
  meeting and stays.
- **Only meetings he has ACCEPTED** — read his own `responseStatus`. `accepted` counts,
  `needsAction` and `declined` do not. Organizer counts as accepted.
- **A medication or self-care reminder is not a meeting.**

**Prep comes from the peer that holds the context, not from you.**

- **A person he knows** → the Personal CRM peer. Its board id is its `workspace_id` in
  `registry.yaml`.
- **Anything hiring, recruiting or interview-shaped** → the Job Search peer, same lookup.
- **Read their boards before messaging them.** `list_tasks` / `get_doc` answers most of it
  and wakes nobody. A peer message costs that peer its whole context on the turn it reads,
  and this runs every day.
- **Message a peer only when a specific fact is missing after reading**, and send the
  question, not the framing. At 06:47 the peer is probably down; spawn it only if the
  meeting genuinely needs it, and spin it back down after.

**Three lines of prep per meeting, maximum**: who they are and the last contact, what this
meeting is for, and the one thing he should walk in knowing. If you have nothing, write
that — invented prep is worse than none.

## 3. Focus today

**At most 5 bullets**, in weekly-plan goal priority order. Not by size, not by what is
quickest, not by the order you found them.

- Draw from this week's committed goals, whatever is newly unblocked, and anything now
  waiting on him.
- **Take it from the weekly plan and the boards.** Not Asana — he stopped that on
  2026-09-16: *"Stop the Asana syncs. It's duplicating stuff that's on the workspaces."*
  Do not read, create, re-date, complete or reword an Asana task from this skill.
- **If your order and the plan's numbering disagree, say so** rather than silently
  picking one. That disagreement means the numbering is stale.
- **Flag an off-track week here, and in the push, by Wednesday.** A goal that has not
  moved at all by midweek is off track regardless of its due date. Name what to drop.
  Friday is too late — by then the only move left is writing the week off.

## 4. Yesterday

**Exactly 5 bullets** on what was actually done. Evidence, not intentions.

- Merged PRs, closed rows with proofs, docs delivered, decisions he answered.
- **A row closed with no evidence in its comments does not count as done.** Say what it
  was, not that it closed.
- **If fewer than 5 real things happened, write fewer and say the day was light.** Padding
  this section to the count is how a slipping week reads as healthy.
- Read it from the boards, the transcripts and `gh pr list`, never from a peer's summary
  line — a summary is what it meant to do.

## 5. Token spend

**A table of weekly usage against the limit, then one verdict line.** Changed by him on
2026-09-18, on the first run: *"Show weekly usage vs. limit, not just current pool
state"* and *"Present token spend as a table showing weekly usage vs. limit, not just
pool state."* Pool state answers "where is the fleet billing right now", which is not the
question he is asking.

- **The table is the estate**, one row per pool: used against the weekly limit, the Fable
  meter separately, the reset, and whether the reading is live or stale.
- **Then the runway**, measured off points GAINED since the stint began ÷ hours. Never
  `used% ÷ hours`, and never projected multiple days off the current 5h window.

**The verdict line ends in a decision word: speed up, slow down, or all clear.** His
words: *"Summarize token spend decision rule — speaker needs to know if action is
required."* A percentage is not an instruction, and he should not have to derive one from
the table he was just handed. If the answer is that nothing needs doing, write **all
clear** — that is a verdict, and an absent one reads as an unfinished section.

**This digest does not drive a pane for `/usage`.** The live read belongs to `/token-watch`,
on whatever schedule its board row carries. As armed on 2026-09-19 that row fires at 06:00,
47 minutes BEFORE this digest — which makes the panel fresher than it used to be, and does not
make it live. Do not restate the cadence as an interval: the armed gaps are not uniform, and
deriving one is what made the board's own stall detector file a false alarm on 2026-09-21.
Run `scripts/fleet_budget_watch.py` and report the estate panel as it stands.

**So the reading here is stale by construction, and must be labelled.** Say **"82% or
worse"**, never "82%". A stale figure is a bound, not a measurement — and it can be wrong
in either direction, because an idle pool's meter does not only rise. That belief cost two
hours at a wall on 2026-09-17.

## What not to do

- **Don't send this without the doc bound.** A digest that exists only in the terminal is
  gone by the time he reads his phone.
- **Don't write "blocked on" or "waiting on" from a tmux pane.** The pane is a render. Read
  the session's transcript and find the last turn it actually processed.
- **Don't spawn the fleet to build this.** Read boards and transcripts. Waking six peers at
  06:47 so they can each report costs more than the digest is worth.
- **Don't let a section fail silently.** If Gmail is unauthorized, a calendar did not
  resolve, or `fleet_budget_watch.py` exited non-zero, that section says **could not run**
  and why. It never says "nothing found". Passed, failed, and could-not-run are three
  states, and the third one collapsing into the first is the bug.
- **Don't ask him a question in the doc body.** Prose is invisible to every queue. If you
  need an answer, file a review item.

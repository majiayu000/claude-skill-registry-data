---
name: what-next
description: Turn a how-are-we-doing read into a short, ranked action plan for a business's website and digital footprint, then start the work on the owner's say-so. Reads the business's saved profile (latest snapshot, watchlist, notes), lists every candidate the data supports, throws out anything that fails the buyer test, lacks evidence, or would disturb a pending experiment, and ranks the rest by how close each is to a real booked customer. Each action comes with its evidence row, the service it feeds, effort, which skill does the work, and a dated read to prove whether it worked. Use whenever someone asks "what should we do next", "what should I work on", "what now", "what do we do with this", "next steps", "action plan", "where should I focus", "what's the priority", "what would move the needle", or follows a how-are-we-doing report or dashboard with "ok so what?", even if they don't name the skill. Also use when the owner asks why nothing is worth changing, or wants to revisit something parked on the watchlist.
---

# What next

Take the measured picture that `how-are-we-doing` saved and answer one question: **what should this business do next, and how will we know it worked?**

how-are-we-doing measures and publishes the dashboard. This skill decides. It never re-measures the whole footprint; it works from the saved snapshot, so the advice rests on the same numbers the owner sees on the dashboard.

`<skill dir>` below means the folder this SKILL.md is in.

## Pick the profile

Profiles live at `<project root>/.claude/how-are-we-doing/<business-slug>/`, the same folders how-are-we-doing uses (profile.json, notes.md, watchlist.md, history/).
1. List `.claude/how-are-we-doing/*/profile.json` under the current directory.
2. One profile → use it. Several → use the one the user named, or ask with AskUserQuestion.
3. None → there's nothing to plan from. Say so and offer to run how-are-we-doing setup first.

## Run

**1. Check the snapshot is fresh enough.**
```bash
python3 <skill dir>/scripts/candidates.py --profile <profile dir>
```
The first line gives the snapshot date, its age, and any missing sources. If it's more than 7 days old, or a source the plan would lean on is missing (GA4 for page fixes, the CRM for lead work), say so in one line and offer to run how-are-we-doing first. Don't silently plan from stale numbers. If the user wants to go ahead anyway, carry on and label the snapshot date in the plan.

**2. Read the context, all of it.** `notes.md` (this business's traps and rules, which win over anything general), `watchlist.md` (the Open section in full, not just what the script flagged), and `profile.json` (`business.what_it_sells`, `lead_definition`, `people`, `noise`). Also read the project's own instructions (CLAUDE.md) if the work would touch its site: editorial rules and banned topics live there.

**3. Test every candidate.** Apply `references/tests.md` to each one the script listed: buyer test, evidence, no open experiment, one sized action. The script flags `BLOCKED until <date>` only when a watchlist line names the page by path. A line naming it in words blocks it too, and so does a line saying that fix was already tried. You may also add a candidate the script couldn't see (for example a parked owner task in notes.md) if it passes the same tests with a quoted row. When the site's source is available, look at it before ruling a page out: what links to a page, and what's already on it, often shows the move nobody has tried yet.

**4. Rank and cut to three.** Closest to a booked customer first, as in the tiers in `references/tests.md`. Where real leads actually came from outranks where impressions are. Three at most; fewer is normal; zero is a real answer.

**5. Write the plan** (template below). Resolve who does each step against the skills and tools installed in this session (`references/handoffs.md`), or manual steps when nothing fits, but say it in plain words.

**6. Ask which to start.** One AskUserQuestion, `multiSelect: true`, one option per ranked step. Labels are the step's verb phrase, and descriptions are who does it plus the time. Nothing starts without a pick.

**7. Start the picked ones, one at a time.** For each one:
- add its watchlist entry (date, baseline row, exact read) to `watchlist.md` under Open
- invoke the hand-off skill with the evidence and the goal
Outward-facing steps (sending, publishing, deploying) get their own confirmation inside the hand-off; an approved plan isn't permission to send.

## Plan template

The owner reads this to decide what to do in the next few minutes, not to audit the analysis. So it opens with the move, each step is something a person can do, and the proof stays short. The full working (every candidate, every test) stays in your head and comes out only on request.

```
**Your move:** <one sentence, verb first: the single most useful thing to do now>

**This week** (pick any; nothing starts until you say)

1. **<Verb + plain what>** · <who: you / me / both> · <time, e.g. 10 min>
   Why: <one plain sentence with the one number that matters, then the source and dates in brackets>
   Check: <date>: <what we'll look at to know it worked>

2. …

**Holding off:** <one line naming the waiting items and the date each frees up>, e.g. "review-software post (10-27), GHL posts (10-28), two pages waiting to be indexed (10-14)". Then "Ask to see the full skip list."

**Only you can answer:** <at most 2 short questions, if any>
```

How to write it:
- **Plain words, written to the owner.** Say "the review-software post", not `/blog/google-review-management-software`; "people who booked", not `class: unconfirmed`. Leave out internal terms (tier, candidate, buyer test, hand-off, snapshot, watchlist line), file paths, commit hashes and tool IDs. Name the doer as a person or a plain action ("I draft the emails in Gmail, you send them"), not a skill name.
- **Each step is at most 3 lines.** If a step needs sub-steps (a manual GHL edit, say), list the sub-steps only after the owner picks it.
- **One number per Why.** Pick the number that makes the case, keep it exact, and put source and dates in brackets: "(Search Console, Sep 2–29)". The rest of the row stays available if asked.
- **Effort is a time, not a letter.** "10 min", "an afternoon".
- **Holding off is one line**, not a table: it's there so the owner knows the board was checked and when things free up. If nothing is ranked, the line after **Your move** says so plainly ("Nothing worth changing this week. First item frees up 10-14.").
- **No duplicate questions.** Anything the owner picks or answers through the AskUserQuestion that follows doesn't also get asked in the text.

If the owner asks for the reasoning ("why not X?", "show the skip list"), give the full Not-doing list then, one line per candidate with the test it failed or the date it's blocked until.

## Who owns watchlist.md

Both skills write to it, so each sticks to its half. how-are-we-doing *measures*: it reads due items, records their results, and parks re-reads of things it measured. what-next *proposes*: it parks a dated read with a baseline for every action the owner approves, at the moment the action starts. Neither rewrites the other's open items. When an action is declined, don't park anything. If the owner defers it, add the deferral date to the existing parked item; it keeps its rank next time (see `references/tests.md`). If the owner drops it, mark it dropped there.

## Rules that never bend

- **Evidence or nothing.** Every action quotes a measured row with its source and window. No estimated impact, no invented ratios, no "this could double clicks". If the impact isn't measurable, say "not measured".
- **Small counts stay counts.** 4 → 0 clicks is "4 → 0", never "-100%".
- **Leads come from the system of record.** Rank channels by real bookings in the CRM, never by GA4 lead events.
- **Respect pending experiments.** Don't change a page before its dated read, and don't repeat a fix the watchlist says was already tried.
- **The owner decides anything public.** Copy, pages, posts, emails are proposals until approved, and are sent or published only on a second, explicit yes. Never propose content just to fill a calendar.
- **Hand-offs are discovered, never assumed.** Name only skills that appear in this session's skill list.
- **notes.md wins.** Business rules there (banned topics, platform positioning, editorial policy) override anything general here.

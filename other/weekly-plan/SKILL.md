---
name: weekly-plan
description: Set this week's goals with the user in a markdown doc bound to the Team Lead live-feedback workspace. Carry over unfinished work from last week, surface candidate goals, prioritize, estimate hands-on hours, the user picks, then expand kept goals. Each goal title is a specific measurable outcome with a due date and an estimate.
user-invocable: true
---

# Weekly Plan

The shared context the team lead and the team use to stay on the same page and move toward the user's top goals each week. Lives as a markdown doc bound to the **Team Lead live-feedback workspace**, so the user and Team Lead can both read + edit it and the user's comments arrive as channel events.

**Not Notion.** The user moved weekly planning off Notion on 2026-08-17 — it was too heavy-weight and the workspace is where the work already lives. Do not create a Notion page for the weekly plan, and do not call `notion_watch_page` for it. Existing Notion weekly pages stay where they are as history; nothing needs migrating.

**Design intent — keep it simple.** Goals pages have grown too dense to be useful. This skill's job is the opposite: surface fewer, clearer goals that you can scan in 30 seconds.

## Goal shape

Every goal has these parts. Lead every block with a **bold brief label**, and keep one type of information per bullet — never combine (see `feedback_one_info_type_per_point`). Due and Lead are separate bullets, not one line.

| Block | Format | Notes |
|------|--------|---------|
| Title | `### N. <outcome, and why it matters> (~Xh) <tag>` | Carries the outcome **AND** the reason, in one line. **The estimate lives in the title.** e.g. `### 5. Job search shortlist finalized, so the search becomes a few real conversations instead of cold applications (~2h) ✅` |
| Due | `- **Due**: <Day> YYYY-MM-DD` | its own bullet |
| Lead | `- **Lead**: <agent> · <the user's role>` | its own bullet — separate from Due (different info type) |
| Constraint | `- **Constraint:** <one line>` | **only when a real operating limit exists** (e.g. "agents draft, you send"). Not a place for context. |
| Key Outcomes | `- **Key Outcomes**` then a **numbered** list, **at most 5** | each outcome is `<when> — <what>`, plus one clause of why it has to happen then. **Label is `Key Outcomes`** (renamed from `Key stops` by the user, 2026-09-13). These become the workspace tasks (step 11). |
| Estimated hands-on hours | `- **Estimated hands-on hours:** <derivation>` | **only when the derivation is worth showing** — the baseline-without-agents figure and what his share of it is. Named by him on 2026-08-27; it was previously `Estimate basis`, which described the method rather than the number. The number itself still lives in the title. |

### There is no Value block — the title carries the value (set 2026-08-17, repeated 2026-08-27)

**He has now said this twice.** On 2026-08-27 the week's plan still carried six Value bullets and he cut them again: *"Value is no longer necessary -- it should be apparent most of the time in the top level goal."* The rule was already written here and the doc broke it anyway, which means reading this section is not enough — **check a drafted plan for `**Value` before showing it to him.**

The user removed it as wasted space: *"Do you see what I wrote in the goal title? That's the goal. And we should going forward in this template have the title reflect the goal. No separate 'Value' section."*

- **Put the why in the title.** If the title only names an artifact ("Job search shortlist finalized"), it is not finished — say what it buys.
- **The one exception is a brand-new goal** whose reasoning genuinely will not fit a title. He used exactly this on the goal he added himself, opening it with *"This item is new this week, so wanted to just be more clear about value."* One line, once, on its first week — then it folds into the title.
- **Whatever the value is, it comes from the record, not from Monday-morning invention.** Carry it forward from the last plan that had the goal, or ask the owning agent. See `feedback_goal_value_is_world_value`.

### Five key outcomes, and the detail lives in the owning agent's workspace (set 2026-08-17)

An eleven-item task list under one goal is a task board, not a goal. *"Ultimately, we should have one top level goal here managed in the Team Lead workspace, and then that should branch into multiple subgoals in the [owning agent's] workspace, but we don't need to manage them all the details here."*

- **Ask the owning agent for the key outcomes — don't compose them yourself.** It knows the real sequence and the real dates. Hand it the goal and the deadline; let it come back with ≤5 chunks and where it thinks the deadline is at risk.
- **Date the outcomes backwards from the deadline, with any external party's turnaround carved out first.** Review time you don't control is the scarcest resource in the week; a plan dated forwards from what the fleet can finish silently spends it.
- **Surface the decisions the owning agent needs from the user, at the top of the week rather than on the due date.** An outcome that is serialized behind a ten-minute decision is a whole-week risk.
- **Link the owning agent's board rather than mirroring its tasks.** If a detail is not something the user acts on, it does not belong in his plan.

### Hard length limits — the doc gets leaner over the week, never denser (set 2026-08-17)

The user had to say this twice in one session, the second time watching it happen live: *"I already see you breaking the formatting and adding more detailed unnecessary crap to section 2. Please request a very lean planning doc, bake it into the template, and do what you need to do to keep everything lean."*

**The limits are numeric so they can't be negotiated:**

| Element | Limit |
|---|---|
| Whole goal body (everything under the `###` title) | **≤ 10 lines** — Due, Lead, an optional Constraint, the `Key Outcomes` label, and at most 5 outcomes. **No other blocks.** |
| A key outcome | **one line, ≤ 25 words** — `<when> — <what>`, plus at most one short clause of why |
| Constraint | **one line**, and only when a real operating limit exists |
| Committed-vs-capacity header | **one or two sentences** — the totals and the single biggest structural risk |
| Key Outcomes per goal | **≤ 5** |
| `## Last week` section | **≤ 5 bullets** — what happened, and the blockers this week has to clear |

**The failure mode is relaying, not writing.** Every over-long block in this doc came from a peer sending good analysis and it being pasted in. A peer's reasoning is for the thread; only its **conclusion** belongs in the plan. When an agent sends three paragraphs on why a date moved, the plan gets the moved date and the thread gets the paragraphs — never both.

**Applies to edits, not just the first draft.** A goal that was lean on Monday and is six bullets deep by Wednesday has failed this rule the same way. Before adding anything to a goal mid-week, delete something or put it on the thread.

## Capacity block (required)

Every plan page opens with a capacity estimate, placed directly under the one-sentence theme and above `## Committed goals`. It is **not optional** — it's the frame the whole plan is judged against (committed hours vs. plannable hours).

Format: a `## Capacity: ~Xh` heading carrying the week total, then a clean per-day bullet breakdown Mon→weekend (include the weekend even when it's small), with a short context note where a day is unusually light or heavy.

```
## Capacity: ~15–21h available, ~13–19h plannable
- Mon 2h
- Tue 2h or 8h (depends on Tim)
- Wed 4h
- Thu 3h
- Fri 2h
- Weekend 2h (kayak camping)
- **Reserved: 2h personal (his) + one more, not yet quantified** — see the board's capacity row
```

- Per-day bullets carry a short reason wherever a day deviates from a normal full day, so the total is legible at a glance.
- **Two totals, never one.** Available is what the calendar allows; plannable is what is left after the reserves. Goals are sized against **plannable**. A single number cannot say which it is, and the reader defaults to the larger one.
- After the plan is set, sanity-check committed hours (sum of goal Estimates) against the **plannable** total and surface the gap: under-committed leaves headroom (say what the slack is for); over-committed means something must drop or defer.

### Reserves: time that is lost but is not on the calendar (set 2026-09-19)

**Every subtraction in the derivation below is a calendar event.** So anything that takes the user's week without being an event is invisible to the method — not underestimated, absent. That is a defect in the instrument, and it does not announce itself: the totals look careful, the arithmetic is right, and the number is wrong in the same direction every week.

**This repo is public, so the reserves themselves are named on the board, not here.** A reserve is often personal — health, family, a commitment he has not made public — and a skill file is the wrong place for any of it. Read the current set off the Team Lead board's capacity row. What follows is how to handle them, which is the part that generalises.

- **Take reserves off BEFORE sizing goals**, not as leftover slack. A reserve applied at the end is a reserve that gets spent.
- **Each reserve is owned by the agent that holds its data**, and the figure reaches the plan only on the user's word. Do not compute someone else's reserve for them.
- **Never convert a raw measurement into hours of lost capacity.** The owning agent's figure usually bounds a window rather than measuring lost output, and the two differ by however much of that window was still workable. Ask the owner what their number means before it enters an arithmetic.
- **Check the denominator before quoting any rate.** A rate over the days something was tracked is not a rate over calendar days, and the plan needs the second one.

**Until a figure exists, say the reserve is unset rather than picking one.** A block reading "Reserved: not yet quantified" — with a link to the board row that owns the figure — is honest and costs nothing. A plausible number invented to fill the line becomes his number the moment someone reads it back.

- **Write what he said and what you derived as two separate lines.** A derived reserve is fine; a derived reserve recorded as his is not, and the block cannot tell them apart a week later.
- **One signal already points at the total size of the reserves.** The calendar derivation typically yields ~30h, and his observed delivery ceiling is ~20–22h/week. That gap is **derived, not measured**, and it is a reason to expect the reserves to be substantial — not a quantification of any one of them. Do not put it in a block as a reserve.

### Compare against last week's PLANNED number too, not just capacity (set 2026-08-17)

Capacity is what the calendar allows; the previous plan's committed total is what he has actually proven he does. On 2026-08-17 those told opposite stories — 28h read as "just inside 30h capacity," and read as **1.5x last week's 18h plan, which he hit to within an hour (18.8h delivered)**. The second framing is the informative one and it takes one number to compute.

- **Pull the prior plan's committed total in step 4** and carry it into the header line.
- **When the prior plan was accurate, say so** — it makes his own estimating a usable instrument instead of something re-argued each week.
- **A big jump over a proven-accurate plan is the finding**, and it is not fixed by capacity headroom. Name it and let him decide; do not quietly trim goals.

### Derive the number from the calendar — don't ask (set 2026-08-17)

**Read the user's calendar and compute the capacity yourself.** He asked for this explicitly, in place of the old "ask him for the number" step: *"please instead review my calendar each week and guess at how many hours I might have depending on whether we have any trips or other meetings booked."*

The rule, in his words:

> Assume by default 7h available each weekday to start, and subtract one for each hour between 9-5PM that I'm booked for a meeting. That assumes I have 1h free for lunch and other sundries and that we get Bea to school on time at 8:40AM every weekday and pick her up on time between 5-6PM also.

Mechanics:

- **Pull all THREE of his real calendars for Mon–Sun** — commitments land on any of them: his personal primary, his work calendar, and the family/household one. **The ids are in `registry.yaml` under `calendars:`**, which is gitignored; this repo is public and a calendar id is a real address, so they must not be written here.
- **Octoturtle was missed for the week of 2026-08-31 and cost the capacity block ~5h in one day.** Logistics (9:30–12), State of the Union (12:30–13:30) and the 🐢🐙 block (15:30–16:30) all sat on it, and Wednesday was published as a full 7h day. He caught it on the doc: *"why didn't you notice those?"* A calendar that is not in the query is not judged and skipped — it is invisible, which is the worst failure mode this block has.
- **Before trusting the set, run `list_calendars` and look for anything new.** The other ~16 entries are subscriptions (holidays, school, seminars, a family member's, a dance calendar) and are not his commitments — but a newly added personal or household calendar would look exactly like them and belongs in the three.
- **Only subtract for meetings he has ACCEPTED — read his own `responseStatus` in the attendee list.** `accepted` counts; `needsAction` and `declined` do not. An invitation on the calendar is not a commitment, and treating a recurring standing invite as attendance is how a real working day gets written off. He said it plainly: *"Don't assume I'm going to [the] meeting and write general rules for it. Just look at my calendar and check if I said yes or not."* If he is the organizer, that counts as accepted.
- Only count hours **inside 9am–5pm**. An early or evening call does not reduce the number; the 7h baseline already reserves that time.
- **A medication or self-care reminder is not a meeting.** Don't subtract for it.
- **Weekend is always 2h, unless he is booked on a trip.** Not zero, and not derived from meetings.
  - **A trip is not automatically a zero, and he has to be the one who says so.** Corrected by him
    2026-09-22, on a weekend away that had been zeroed under the travel rule below: he expected
    reception, wanted the trip to be the focus, and still expected some time to poke at things. Keep
    the 2h and ask, rather than zeroing and waiting to be corrected. The trip's own calendar block
    already removes the hours it actually consumes; zeroing the rest of the day charges him twice
    for it.
- **This derivation produces AVAILABLE hours, not plannable ones.** It can only see calendar events, so it cannot subtract the reserves above. Take those off afterwards and report both totals.
- **Prorate the current day.** Planning usually happens Monday partway through — a 7h Monday that starts at noon is really ~4h. Check the clock (`date`), don't assume a full day.
- **Travel, PTO, and all-day events zero out the day.** Say which event did it.
- Show the derivation in the doc, not just the total, so he can correct the inputs rather than argue with the output.

**The failure mode to avoid is generalizing from an event's existence.** Both corrections above came from the same mistake on 2026-08-17: seeing a recurring meeting on the calendar and writing a rule about it, instead of reading the one field that says whether he is going.

**Where the user's own number disagrees with the rule, keep his and flag the gap.** He may know about a commitment the calendar doesn't carry — that is information you don't have, not an error to fix. Name the discrepancy in one line and move on.

## When to invoke

- **Sunday/Monday** to set up the new week.
- **Mid-week** if the user wants to revise priorities (`/weekly-plan revise`).
- After any week where major scope changed and the user wants to re-baseline.

## Steps

0. **Self-update first.** Run `/self-update` before planning — it updates Claude Code to the latest version, pulls the latest `ai-team-lead` (skills/rules/registry), and propagates both to the fleet. Week-start is the right moment (fleet usually idle). Report anything that changed, then continue planning on the current tooling.

1. **Create this week's plan doc and bind it to the workspace.**
   - Write `.claude/reviews/weekly-YYYY-MM-DD.md` — **weeks run Monday through Sunday**; the `YYYY-MM-DD` is that Monday. That directory is already gitignored, which matters because this repo is public and the plan names private projects.
   - Open with `# Week of YYYY-MM-DD (Mon M/D–Sun M/D)` and one sentence describing the theme of the week — that's the only narrative.
   - Add the **Capacity block** (see above) directly under the theme sentence, before the goals. Required on every plan.
   - Bind it: `create_review_doc(docId: "weekly-YYYY-MM-DD", path: <absolute path>, title: "Week of YYYY-MM-DD", hubWorkspaceId: <Team Lead workspace id>)`. That call both creates the review URL and files the doc under the workspace, and it auto-subscribes you to thread events — no separate `attach_doc` or `watch_doc` needed.
   - **Surface the WORKSPACE URL, not the doc's `reviewUrl`** — `http://mac-mini.<your-tailnet>.ts.net:8787/workspaces/<workspace_id>` (in `parent.txt`). The plan is meant to be read next to the goal bands and the task board; a bare `/review/<docId>` link opens the document alone, stripped of the surface the user asked us to move onto. `create_review_doc` returns a `reviewUrl` and it is tempting to paste it — don't.
   - **Once bound, never `Write`/`Edit` the .md again.** Route every later change through the live-feedback edit tools — a direct file write races the ~1s flush and gets silently clobbered.
   - **Never `set_doc_content` on a plan the user might have open.** It is a block-level diff that applies *your* full markdown, so any block he added between your read and your write is deleted with no error. Two calls four minutes apart destroyed his live edits on 2026-08-17, and `.claude/reviews/` is gitignored so there is no recovery. Use `find_and_replace` for prose, `create_anchor` + `delete_block_at_anchor` / `insert_blocks_at_anchor` for structure, `delete_section` for a whole heading region.

2. **Read last week's Weekly Review page FIRST, and get his OK on it.**
   - Set by him 2026-09-22: the weekly review is *"supposed to give me a way to review each week at a summary level and say if it looks OK or not before we publish anything"*, scheduled *"so it runs on Monday and is part of my review of last week"*, and timed *"early enough pacific time on Monday morning so that the results are ready for you when you do your weekly review."*
   - **The page is Weekly Review's to produce, armed as a schedule on its own board row for 04:00 PT Monday.** Its board is the `workspace_id` the registry gives the measurement project, and the row is the one titled for his Monday OK; the armed rule was verified there on 2026-09-22 (calendar, Mondays 04:00 America/Los_Angeles, `onMissed: catch-up`). Read the page; do not rebuild it, and do not compose a week summary of your own.
   - **His OK lives as a review item on that row, not on the page.** Read the row's items for the answer before you open the page — that is where "looks right / not right / needs a change" is recorded.
   - **A board schedule wakes a session; it does not guarantee one was awake.** Weekly Review stated this limit on 2026-09-22: if none of its sessions is alive at 04:00 the fire is caught up whenever one starts, which can land after 07:00. So check the row's status for produced / failed / could not run rather than assuming 04:00 means done — and if you need the page at planning time and it is not there, spin its session up rather than waiting.
   - **04:00 is his number and it buys overrun, not earliness.** Set 2026-09-22: *"so even if it takes an hour, it'll have data ready for sure by the time you run morning digest."* The morning digest is 06:47 PT, so the run has a full hour to go long before anything downstream reads it. Moving it later eats that margin.
   - **Ask him for one answer — OK or not OK — and write it into the new week's doc**, so the record carries his verdict rather than a thread does. A week he has not OK'd does not feed a published number.
   - **A missing page is "could not look", never "the week was fine".** If it is not there by planning time, say so in those words, say the page is missing, and carry on — an absent page is the one failure that hides every other.

3. **Review how last week actually went, and name the blockers the coming week has to clear.**
   - Asked for by him 2026-09-22: *"please have weekly plan review how the last week went, and identify major blockers to address in the coming week."* It is a step, not a cross-check — the old guidance below was only ever consulted when a week already looked bad, so a week that slipped quietly never got one.
   - **Read `## Reviewing why a week slipped` before doing this**, and delegate the measurement to the Weekly Review project rather than rolling your own transcript rollup. Step 2's page is the input; you are reading it, not rebuilding it.
   - **Separate the three, because they need different fixes**: a goal that overran its estimate, a goal that never started, and a goal that was blocked. Only the third produces a blocker for this week.
   - **A blocker names who clears it and what specifically unblocks it.** "Waiting on the API" is an observation; "the Oura refresh token was never reconnected, and only he can do it" is a blocker. One without an owner does not go in the list — chase the owner or drop it.
   - **A blocker that has now appeared two weeks running is escalated, not re-listed.** Say it is the second week and say what changes this time. Re-listing is how a blocker becomes furniture.
   - **Write it into the doc as `## Last week`, directly under the capacity block, at most 5 bullets.** The blockers go there too, since a blocker nobody can see is not addressed. Anything longer belongs on the thread.
   - **Carry each blocker into a goal or say explicitly that it is not being cleared this week.** A blocker listed and then unmentioned in every goal has been noted rather than addressed, which is the failure this step exists to prevent.

4. **Pull carry-overs from last week's doc.**
   - Locate the prior `.claude/reviews/weekly-YYYY-MM-DD.md`.
   - List every goal whose sub-outcomes aren't all checked OR that's part of a multi-week sequence.
   - Seed them into a `## Candidate goals (carry-over)` section of the new doc, preserving title/due/estimate. Mark explicitly as `(carry-over)`.
   - **Check the carry-over against evidence, don't just re-list it.** A goal can look untouched on the page and have absorbed most of the week — see `## Reviewing why a week slipped` below.

5. **Surface new candidate goals.**
   - Pull from: this week's open PRs across the fleet (`gh pr list` per repo), peer summaries (`list_peers` + recent transcripts), open tasks and decisions already on the workspace board, anything the user said this week that sounded like a commitment.
   - Add them to a `## Candidate goals (new)` section in the same goal shape.

6. **Prioritize.**
   - Sort the combined candidate list by the user's priority (1 = highest). Use the user's recent voice signals: deadlines, dependencies, things he's mentioned more than once, customer-facing > internal > polish.
   - Number them — `1.`, `2.`, etc — in descending priority.

7. **Estimate hands-on hours per goal — by the method in `effort-estimates.md`, not by feel.**
   - **Decompose the goal into components first**, size each one as human-engineer hours without LLM help, and add them. That sum is the baseline. A whole-goal guess reverts to pre-agentic priors and is the failure this step exists to prevent.
   - **Put each unknown on its own line with a range** — the API nobody has read, the decision nobody has made. If the unknowns outweigh the known work, the goal for this week is a scoping pass, not the build.
   - **Convert**: hands-on = baseline ÷ 15, wall clock = baseline ÷ 10 (÷5 for both on non-software). Show the baseline you divided.
   - Note agent-time separately only if it's load-bearing for the goal (e.g., "blocked on Health Tool agent for 2h before the user can review").
   - Irreducible user time — his reading, his judgement calls, his voice pass — is **not divided**. Neither is waiting on a third party.

8. **the user picks.**
   - Tell the user both totals you derived (see `## Capacity block`) and show the derivation — don't ask him for the number. Available comes from the calendar; plannable is what is left after the reserves, and it is the one goals are sized against.
   - the user tags each goal: ✅ commit / ❌ drop / 📦 defer (with target week).
   - Drop the dropped + defer the deferred. Keep the page lean — only commits show in the final plan.

9. **Expand kept goals.**
   - For each ✅ goal, add the **Lead** line (owning fleet agent + the user's role) so every area has a clear point-person.
   - Add sub-outcomes only if the title isn't already self-evident.
   - Note any cross-agent dependencies on the Lead line or a one-liner (e.g., "Personal Finance agent owns the prep; the user reviews Wed").
   - Do NOT pre-fill a daily hitlist. The `daily-review` skill handles the day-by-day surface.

10. **Confirm + commit.**
   - Read the page back to the user: "Week of YYYY-MM-DD: N goals, ~Xh committed against ~Yh plannable (~Zh available). Top 3: ..." — always state committed-vs-plannable, not just the goal count, and never quote available alone.
   - Wait for confirmation. Adjust if needed. Then move on.

11. **Mirror the committed goals onto the workspace board.**
   - Do this only AFTER the goals are confirmed (step 10) — never before (`feedback_notion_goals_before_asana` memory; the rule survives the move off Notion, only the surface changed).
   - `set_goal_list` with one band per ✅ goal, in priority order. A goal that is really a chain of outcomes (build → decide → publish) is one parent band with subgoals, not three peers — peers hide the dependency.
   - `create_tasks` for the work **the fleet owns**, one batch, each row with a body someone not in this conversation could pick up. Use `after` / `afterEnforce` to encode the chain rather than relying on the reader to infer it.
   - **Create tasks for yourself (Team Lead) for anything handled in the ai-team-lead project.** That is the point of the board — the user should not be the only one with a task list.
   - Leave anything not tied to a committed goal in Chores.

   **Then rank the projects — the band ORDER is what Home's "Prioritized Projects" reads.** Asked for by him on 2026-09-22: *"keep the projects up to date once we've signed off on the plan."* It is part of this step, not a separate errand, and it runs every week without being asked.

   - **Each band's body doc carries a full link to its project's board**: `set_doc_content(docId: "task:<goalId>", markdown: "Week of YYYY-MM-DD, goal N. Board: [name](https://workspaces.fryanpan.com/workspaces/<id>)")`. Home finds a project ONLY through that link — a board no goal links to sinks to the recency tail. The ids are in `registry.yaml` under `workspace_id`.
   - **Reuse last week's bands rather than creating new ones.** `unarchive_task(workspaceId, goalId)` brings one back with its history and `rename_goal` retitles it in place. `set_goal_list` is for a first setup; run against a live board it discards what is there.
   - **`reorder_goals(workspaceId, order)` is the rank control, and it is permutation-only** — pass every reorderable goal id, this week's bands first in goal order, then the standing fleet bands. Passing a non-reorderable band (Backlog) is an error, and omitting one is too.
   - **A goal with two leads gets both links, and both projects rank at that goal's position**, which pushes the next goal's projects down. Say so in the report rather than letting him find it.
   - **Verify on Home, not from the call results.** `curl -s http://127.0.0.1:8787/`, read the Prioritized Projects list back, and report the order you actually saw.

12. **Communicate the plan to the team.**
    - Only after the user has reviewed the doc.
    - Message each peer that leads a committed goal via claude-hive `send_message`: the goal, its due date, and its dependencies. Goal and context only — no prescriptive checklists, no "report back when done" (`feedback_delegating_to_peers`, `feedback_dont_wire_in_status_reports`).
    - Spin up any owning agent that isn't running; spin it back down when its task is done.

13. **Do NOT mirror the plan into Asana.** Removed 2026-09-16 on the user's instruction: *"Stop the Asana syncs. It's duplicating stuff that's on the workspaces."* The committed goals go onto the workspace board (step 11) and anything needing him becomes a review item on his Home queue. That is the whole surface. Asana held a parallel copy of the same asks, which meant every change had two places to be made and one place to be forgotten.

## What to avoid

- Don't draft a comprehensive plan upfront with all 5+ goals + sub-goals + daily hitlist + retrospective + infrastructure interleave + training table. That's the failure mode this skill replaces.
- Don't bundle the prior week's retro into the new week's page. Retros stay on the prior week's page.
- Don't pre-compute infrastructure / housekeeping items unless they're load-bearing for a committed goal.
- Don't expand dropped or deferred goals.
- Don't invent goals to fill the page. Fewer is better.
- **Don't write explanatory text, and don't narrate how the plan got here.** No background paragraphs, no "I originally had this as two goals," no justification of an estimate. The user's words, 2026-08-17: *"You added too much random crap to the goals. Please keep it high level, focused on value, due date, key stops. Don't bother with explanatory text, or how we got there."* If something genuinely needs explaining, it goes in a thread reply, not in the plan.
- **Keep the committed-vs-capacity line to one or two sentences** — the totals and the single biggest structural risk. It is a header, not an analysis.
- **Don't make already-finished work a goal, and don't make a five-minute task a goal.** A goal is a measurable outcome that still needs the user's hours. Recording something he already did — or something that costs him minutes — inflates the committed total and buries the goals that matter. Set 2026-08-17, after "Weekly planning moved from Notion to this workspace" was listed at ~0.5h for work that was already done: *"We already did this. It took 5 minutes of my hands on time. Don't make it a goal."*
- **When a goal is dropped mid-plan, check whether its tasks are still live before deleting its board band.** Dropping the band strands them into Chores. Rename the band to something honest (e.g. "This week's planning loop (process, not a goal)") and keep it below the real goals.

## Reviewing why a week slipped

### Delegate the measurement to the owning project — do not roll your own (set 2026-08-17)

**The registry project that owns this analysis owns it. Spawn it and hand it the goal; do not write a transcript rollup in the team-lead's own context.** It has developed handling for subagent transcripts and for merging sessions that a fresh script will not reproduce, and the team-lead's job here is to administer, not to implement. This is the second time a scratch rollup got written and the user asked for it to stop — *"Above all else, please delegate. That's in your prime directives."*

- Spawn it with `respawn.py --mode missing --only <its registry key> --execute`, hand it the goal, let it own the loop, and spin it down when the analysis lands.
- Give it the window, where the doc lives, and what the current draft claims — then say its methodology wins over anything already written.
- **Don't hand it filters, constants, or a method.** Raw context about the data is fair; prescribing how to measure is the reinvention the user is objecting to.

The bullets below are for reading its output, not for producing your own:

- **Report shares, not absolute hours** unless Weekly Review says otherwise. Turn-based time models charge the user reading time for output produced while he was elsewhere, so totals overshoot real capacity while the relative split stays trustworthy. Sanity-check any absolute against the derived calendar capacity.
- **Check PR activity as a cross-check, not as the measure.** A repo with zero PRs in the window can still have absorbed the week — deep investigation, benchmarking, and review all leave no PR trail. Never conclude "nothing happened here" from an empty `gh pr list`.
- **Separate an estimate miss from an execution miss.** A goal that came in at 140% of its estimate and still isn't done is an estimating problem; a goal that never got started is a prioritization problem. They need different fixes, and conflating them produces advice that helps neither.
- **Name dependencies the plan hid.** Two goals due the same week where one gates the other were never two goals. That is a planning defect worth fixing in the next plan, not a performance problem.

## Daily life of the plan

Once the plan is set, this doc is the team's shared anchor for the week:
- Team Lead is auto-subscribed from `create_review_doc` — the user's comments fire as channel events on the doc's threads.
- The `daily-review` skill writes a fresh `.claude/reviews/YYYY-MM-DD.md` each day; it pulls the goal list from this doc to anchor priority order.
- **The workspace board carries the tasks — the team's and his.** Anything needing him is a review item on his Home queue. There is no second task surface; see step 13.
- Apply the user's comments with the live-feedback edit tools, never by writing the file.
- When a goal completes, check off all its sub-outcomes and move it to a `## Done` section at the bottom.
- When a goal slips, update the due date in place and note why in one line.

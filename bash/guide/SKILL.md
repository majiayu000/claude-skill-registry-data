---
name: guide
description: Interactive 8-module learning path for the shipped skills, role-adaptive
argument-hint: "[module number 1-8, or 'next', or 'reset']"
---

# Guide

An interactive tour through the shipped skills. Each module teaches one skill by running it against sample data in `samples/`. Designed for PMs, designers, analysts, or engineers - the skill adapts framing to the role set in `CLAUDE.md`.

## Pre-emit checklist (run BEFORE every chat message in this skill)

Before you send any message while `/guide` is active, audit your draft against these rules. If any fails, fix it before sending.

1. **Vault paths are backticked.** Any token that looks like a file path (contains `/` or ends in `.md`) must be wrapped in backticks so Claude Code renders it as a clickable reference. A path without backticks is a bug - it renders as plain text and the user can't click it.
2. **File-argument commands use `@`.** When you tell the user how to run a skill with a file input, the path must be `@`-prefixed so Claude Code's file autocomplete activates: `` `/meeting @samples/sample-meeting-transcript.md` ``, not `` `/meeting samples/sample-meeting-transcript.md` ``.
3. **Module intros below are printed verbatim.** Each module has a literal intro block in this file. Print that block exactly as written - do not rephrase, do not add extra paragraphs, do not strip backticks. The blocks are short on purpose.
4. **Gate order.** If the current turn is a first-run orientation, a resume, or a numeric jump, the message ends with `Ready to start Module N? (y/n/skip)` and nothing else - no module intro on the same turn. If the user just typed `next`, there is NO gate - go straight to the next module's verbatim intro.

## Progress tracking

Progress is stored in `.claude/memory/guide-progress.md`. The `.claude/memory/` directory ships with the template (see its `README.md`), so do NOT run `mkdir` or `ls` to check - use the `Read` tool directly, and if Read returns "file does not exist", treat it as a first run and create the file with `Write`.

When you create the progress file for the first time, use this content (substitute today's date for `YYYY-MM-DD`):

```markdown
---
tags: GuideProgress
started: YYYY-MM-DD
---

# /guide progress

- [ ] Module 1: /meeting
- [ ] Module 2: /today morning
- [ ] Module 3: /decision
- [ ] Module 4: /communicate
- [ ] Module 5: /create-epic
- [ ] Module 6: /competitive-research
- [ ] Module 7: Capstone
- [ ] Module 8: Extend your workspace
```

Mark a module complete (`[x]`) only once the user finishes it (see "End-of-module recap" for the specific moment).

## Mode selection

Keep tool calls minimal and silent - no `Bash ls`, no `mkdir`, no "let me check..." narration. The user wants a coach, not a script.

Check `$ARGUMENTS`:

- **Empty** (`/guide` with no args):
  - Read `.claude/memory/guide-progress.md`.
  - If Read returns "file does not exist", it's a first run: show the **First-run orientation block** (verbatim), create the progress file with `Write`, then stop. The orientation block ends with the "Ready to start Module 1? (y/n/skip)" prompt. On the user's next turn with `y`, print the **Module 1 verbatim intro** and stop.
  - If progress exists, show the **Resume line** (one line: `` You're on Module N of 8 - [Module title]. `/guide <n>` to jump, `/guide reset` to start over. ``), then ask `Ready to start Module N? (y/n/skip)`, then stop. On `y`, print the **Module N verbatim intro**.

- **`next`**:
  - Read `.claude/memory/guide-progress.md`.
  - If missing, treat exactly like empty (first-run flow).
  - If progress exists, find the first uncompleted module and print its **verbatim intro** directly - NO "Ready?" gate. The user already said `next`; asking again is friction.

- **A number 1-8** (e.g. `/guide 3`):
  - Read (or create) progress file.
  - Print one line: `Jumping to Module N - [title].`
  - Ask `Ready to start Module N? (y/n/skip)` and stop.
  - On `y`, print the **Module N verbatim intro**.

- **`reset`**:
  - Overwrite `guide-progress.md` with a fresh copy (all modules unchecked, `started:` = today).
  - Print one line: `Progress reset.`
  - Then show the **First-run orientation block**.

The "Ready?" prompt at a gate is the ONLY prompt for that turn. Do not preview the intro on the same turn as a gate - that buries the gate.

Answers at a "Ready?" gate:
- `y` - print the module's verbatim intro on the next turn
- `n` - stop (one-line acknowledgement)
- `skip` - mark the current module `[x]`, move to the next gate

---

## First-run orientation block (print verbatim)

```
Welcome to **/guide** - an interactive tour of the shipped skills.

**What this is**: 8 short modules (~5-10 min each), one per shipped skill, run against sample data in `samples/`. Do 1-2 per session over days, not all at once. Progress is saved in `.claude/memory/guide-progress.md`, so you can stop and resume. The framing adapts to the role set in `CLAUDE.md`.

**The 8 modules**:
1. `/meeting` - raw meeting notes to structured note + tasks
2. `/today morning` - daily planning (mood, energy, focus items)
3. `/decision` - document a product decision with options + trade-offs
4. `/communicate` - draft a Slack / email / async update
5. `/create-epic` - raw idea to structured epic draft
6. `/competitive-research` - build a sourced competitive matrix
7. Capstone - chain `/meeting` then `/decision` then `/communicate`
8. Extend your workspace - run `/opportunity-solution-tree`, add or write more skills

**Commands**:
- `/guide` - continue / resume (or start at Module 1 the first time)
- `/guide next` - go to the next uncompleted module (no confirmation)
- `/guide <n>` - jump to a specific module (e.g. `/guide 3`)
- `/guide reset` - wipe progress and start over

**At a "Ready?" gate**: `y` start, `n` stop, `skip` mark done and move on.

Ready to start Module 1? (y/n/skip)
```

Print this block and STOP on the same turn. Do not append the Module 1 intro here - it's for the next turn, after `y`.

---

## Module verbatim intros

Each intro below is printed verbatim when the user is ready to start that module (after `y` to a gate, or directly after `next`). Do not rephrase, do not strip backticks, do not add extra paragraphs.

### Module 1 intro

```
**Module 1 of 8 - Your first meeting note** (~5 min)

`/meeting` turns raw meeting notes into a structured note with decisions, action items, and follow-up tasks in `Dashboard/tasks.md`. Sample input: `samples/sample-meeting-transcript.md` (open if you want to see what it handles).

**To run now**: type `/meeting @samples/sample-meeting-transcript.md` yourself, or just say `run it` and I'll invoke it for you.
```

### Module 2 intro

```
**Module 2 of 8 - Morning planning** (~5 min)

`/today morning` picks up to 3 focus items for today, drawn from `Dashboard/tasks.md` and your weekly P-Tasks. Ritual skill - no sample file, you run it against yourself.

**To run now**: type `/today morning` yourself, or say `run it`. The skill will ask about mood, energy, self-care, and your calendar.
```

### Module 3 intro

```
**Module 3 of 8 - Logging a decision** (~5 min)

`/decision` gathers context, drafts 2-3 options with trade-offs, creates a decision note in `Loose Notes/Work/`, and proposes follow-up tasks. Sample context: `samples/sample-decision-context.md`.

**To run now**: type `/decision should we ship the auth rewrite before or after the onboarding redesign` yourself, or say `run it`. When the skill asks for additional context, paste the sample file's content.
```

### Module 4 intro

```
**Module 4 of 8 - Draft a crisp async update** (~5 min)

`/communicate` drafts Slack / email / async messages matched to the audience, pulling context from your recent decisions and meetings. Sample context: `samples/sample-update-context.md`.

**To run now**: type `/communicate update engineering leadership on the auth-first decision - Slack` yourself, or say `run it`. The draft comes back already formatted for the channel you picked.
```

### Module 5 intro

```
**Module 5 of 8 - Creating your first epic** (~5 min)

`/create-epic` turns a raw idea into a structured epic draft at `epics/YYYY-MM-DD - Title.md` with stage `Explore`. Sample input: `samples/sample-epic-idea.md`.

**To run now**: type `/create-epic @samples/sample-epic-idea.md` yourself, or say `run it`. The skill will ask 3-5 clarifying questions (target persona, metric, risks) - answer honestly, and unknowns get marked TBD.
```

### Module 6 intro

```
**Module 6 of 8 - Competitive research** (~5 min)

`/competitive-research` builds a sourced competitive matrix where every observation links to a source. Sample prompt: `samples/sample-competitor-prompt.md`.

**To run now**: type `/competitive-research @samples/sample-competitor-prompt.md` yourself, or say `run it`. The skill will confirm the competitor set, then gather observations from public sources.
```

### Module 7 intro

```
**Module 7 of 8 - Capstone: chain three skills** (~10 min)

The payoff module. You run three skills in sequence and each one reads the artifacts of the previous one - nothing gets re-explained. Sample input: `samples/sample-capstone-meeting.md`.

**The chain** (3 steps):
1. `/meeting @samples/sample-capstone-meeting.md`
2. `/decision invoice portal scope for billing UI revamp`
3. `/communicate update cross-functional stakeholders on the invoice portal scope decision - Slack`

**To run now**: say `run it` and I'll walk you through all three steps in order. You can also run each step yourself - tell me which you prefer.
```

### Module 8 intro

```
**Module 8 of 8 - Extend your workspace** (~10 min)

Three things: (1) run the bundled external skill `/opportunity-solution-tree`, (2) how to add a skill from the internet, (3) how to write your own.

**To run now** (the Torres tree on a real outcome): type `/opportunity-solution-tree reduce new-user activation drop-off from 40% to 25%` yourself, or say `run it`. After the tree runs, I'll cover parts 2 and 3.
```

---

## Role adaptation

Read `CLAUDE.md` for the user's role. Adapt framing lightly - do NOT rewrite the verbatim intros. Add at most one sentence of role-framing AFTER the verbatim intro (on the same turn, before stopping) when the role is clearly non-default:

- **Designer**: "For your role, think of Module 5 as 'draft a design brief' and Module 6 as 'design-pattern research'."
- **Analyst / Researcher**: "Modules 5 and 6 map most directly to your work - plan to spend extra time there."
- **Engineer**: "Modules 5 and 6 work for technical investigations too - frame them as RFCs and tech-stack comparisons."
- **PM / Senior PM / Head of Product** (default): no extra sentence needed.

Keep it to one sentence. The intros do the heavy lifting.

---

## Running a module (after the intro prints)

After the verbatim intro, stop and wait. The user drives from here:

- **"run it"** (or similar): you invoke the skill on their behalf. Narrate one short line first ("Running `/meeting` on the sample - it'll ask you to confirm any tasks before writing."). Let the other skill do its thing. When it's done, jump straight to the **end-of-module recap**.
- **User runs the command themselves**: step back, let the other skill run. When they return to the guide thread, print the **end-of-module recap**.
- **"skip"**: mark the module done and go to the next module's verbatim intro directly (no gate - same as `next`).
- **"stop" / "later" / "n"**: acknowledge in one line and exit. Do not mark the module done.

**Never create files, tasks, or notes without the per-skill confirmation the other skill already bakes in.** The guide itself never writes vault content - it only invokes skills and updates `.claude/memory/guide-progress.md`.

### Module 7 (Capstone) runtime rule

Module 7 has three sub-steps (`/meeting` then `/decision` then `/communicate`). After step 1 finishes, say one line: `` Step 1 of 3 done. Ready for step 2 (`/decision`)? Say `run it` or run it yourself. `` Same pattern after step 2. After step 3, go to the end-of-module recap.

If the user says `next` before all three steps are done: ask one question. `You've done N of 3 capstone steps. Finish the capstone (say "run it" to continue), or mark it done and move to Module 8?` Respect their choice.

---

## End-of-module recap

When a module finishes, print a short conversational recap - not a code-fenced card. Include:

1. **One line marking completion**: `Module N of 8 done (N/8 complete).`
2. **One or two lines on what was just created**, with real filenames in backticks.
3. **One short line on when to reach for this skill in real work** (the takeaway).
4. **One line pointing to the next module**: `` Next: Module N+1 - [title]. [One-line hook]. Say `next` to start. ``

Then update `.claude/memory/guide-progress.md` - mark this module `[x]`.

For **Module 8**, use the end-of-guide block below instead.

Example tone for Module 1 recap (write fresh each time, don't copy verbatim):

> Module 1 of 8 done (1/8 complete). You now have a structured meeting note at `Meetings/2026-04-15 - Quarterly planning sync - Mobile team.md` and one action item in `Dashboard/tasks.md` under "This week". When raw notes land in your inbox, reach for `/meeting` instead of copy-pasting into a doc - it extracts commitments you'd otherwise forget. Next: Module 2 - Morning planning. Pick 3 focus items, not 10. Say `next` to start.

---

## End-of-guide block (use for Module 8 recap)

After Module 8's `/opportunity-solution-tree` run and the parts 2-3 narration, mark Module 8 complete and print:

```
**You've completed /guide.** All 8 modules done.

You now have the full toolkit:
- Daily rituals (`/today morning/evening`) for focus and close-out
- Meeting + decision + communication infrastructure (`/meeting`, `/decision`, `/communicate`)
- Epic / research / discovery (`/create-epic`, `/competitive-research`, `/opportunity-solution-tree`)

**What to do next**:
1. Tomorrow morning, kick off your day with `/today morning`.
2. Run `/personalize deep` to add MCP detection, initiatives, and people profiles (takes ~10 min).
3. When you catch yourself doing the same thing three times, write a skill for it - copy an existing skill folder in `.claude/skills/` as a starter.

Go ship something.
```

Do NOT skip the prominent completion message. This is the moment the user has been working toward - they deserve a clear "done" signal.

---

## Module reference material

The blocks below are reference material - what each skill does and what artifacts to expect - NOT scripts to paste into chat. Use them to inform your recaps and any mid-module Q&A. The verbatim intros above are what the user sees; these notes are your own context.

### Module 1 reference: /meeting

- **What it does**: turns raw meeting notes into a structured note with decisions, action items, and a list of follow-up tasks for you.
- **Why**: raw meeting notes rot; a structured note is searchable and surfaces the tasks you committed to without relying on memory.
- **Artifacts**: `Meetings/YYYY-MM-DD - Title.md` + task in `Dashboard/tasks.md` + link in today's journal.
- **In-real-work note for the recap**: mention the three input modes - pass a saved file path, run `/meeting` with no args to browse unprocessed files, or run `/meeting` and paste the transcript directly.

### Module 2 reference: /today morning

- **What it does**: opens today's journal, asks mood / energy / self-care / yesterday's evening, takes your calendar, suggests up to 3 focus items.
- **Why**: 3 focus items beats 10. Capacity-aware (low-energy days = fewer items).
- **Artifacts**: `journals/YYYY/MM-Month/DD-MM-YYYY.md` filled in + focus marker on picked tasks in `Dashboard/tasks.md`.

### Module 3 reference: /decision

- **What it does**: gathers vault context (+ GitHub if configured), drafts 2-3 options with pros/cons, creates a decision note, proposes follow-up tasks.
- **Why**: decisions made in Slack / meetings get forgotten, relearned painfully, sometimes silently reversed.
- **Artifacts**: `Loose Notes/Work/YYYY-MM-DD - Decision - Topic.md` + link in today's journal + tasks in `Dashboard/tasks.md`.

### Module 4 reference: /communicate

- **What it does**: drafts a message for Slack, email, or async doc - tone matched to the audience; pulls context from recent decisions and meetings.
- **Why**: PMs re-explain the same context over and over; the vault is memory, the skill translates.
- **Artifacts**: a ready-to-paste draft in chat, formatted for the chosen channel (single-asterisk bold for Slack, proper markdown for email).

### Module 5 reference: /create-epic

- **What it does**: raw idea to structured epic draft using `templates/epic-template.md`, stage `Explore`, unknowns marked TBD.
- **Why**: most ideas die between "we should think about that" and a reviewable document; this closes the gap in 5 minutes.
- **Artifacts**: `epics/YYYY-MM-DD - Title.md` + follow-up tasks in `Dashboard/tasks.md` + link in today's journal.
- **Designer-role note**: the same skill serves drafting a design brief - use sections 1 (Value Prop), 2 (User Problem), 7 (Design Planning).

### Module 6 reference: /competitive-research

- **What it does**: produces a sourced competitive matrix; every observation has a source link, marked `observed:` or `inferred:`.
- **Why**: "what competitors do" answered by opinion breaks in leadership reviews; evidence-driven research survives.
- **Artifacts**: `research/YYYY-MM-DD - Competitive - Topic.md` with matrix, synthesis, gaps, confidence levels.

### Module 7 reference: Capstone (/meeting then /decision then /communicate)

- **What it teaches**: real PM work chains skills; the vault becomes memory so each skill builds on the previous one's artifacts.
- **The chain**: see the verbatim intro above for the three commands.
- **Artifacts across the three skills**: meeting note in `Meetings/`, decision note in `Loose Notes/Work/`, Slack draft in chat, follow-up tasks in `Dashboard/tasks.md`.
- **Observation to surface in the recap**: notice that step 2 and step 3 never re-asked for background - they read the vault files step 1 created.

### Module 8 reference: Extend your workspace

- **Part 1**: `/opportunity-solution-tree` (MIT-ported from [phuryn/pm-skills](https://github.com/phuryn/pm-skills); see `.claude/skills/opportunity-solution-tree/ATTRIBUTION.md`). Walks a Teresa Torres tree: outcome to opportunities to solutions to experiments.
- **Part 2 (narrate after the tree runs)**: how to add an external skill - check license (MIT / Apache OK), copy the skill folder into `.claude/skills/`, keep attribution, restart Claude Code, test it, add to `CLAUDE.md`. Browse [phuryn/pm-skills](https://github.com/phuryn/pm-skills) for starters.
- **Part 3 (narrate after part 2)**: how to write your own - one skill per repeated workflow (>3 times), folder at `.claude/skills/[name]/SKILL.md` with frontmatter (`name`, `description`, `argument-hint`) and a workflow body. Copy an existing skill as a starter. Name by the action (`/meeting`), not the object (`/process-meeting-notes`).
- **Recap**: use the **End-of-guide block** above. Mark Module 8 done.

---

## Notes

- Modules are designed to be done over days, not in one sitting. 1-2 per session is sustainable.
- The guide never writes to the vault (meetings, decisions, tasks) - only skills do, and only after their own confirmation. The guide writes only to `.claude/memory/guide-progress.md`.
- If a module's sample file is missing, tell the user and stop - do not invent sample content on the fly.
- `reset` starts over cleanly; `skip` moves on without completing.

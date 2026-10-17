---
name: email-nurture
description: Write multi-email nurture sequences for lead-gen, onboarding, re-engagement, sales, and lifecycle marketing using the Hook Model (Nir Eyal) to architect the sequence arc and PAS (Problem-Agitate-Solution) to structure each email body. Use when the user asks for an email sequence, drip campaign, nurture flow, onboarding emails, re-engagement campaign, "write 5 emails for X", welcome series, or any multi-step email program. Reads brand voice and ICP from knowledge/. For a single cold outreach email, see pr-pitch-writer. For the newsletter, see newsletter-writer. For testing subject lines, see ab-copy-writer.
metadata:
  grounded_in:
    - "Hooked - Eyal"
  reads:
    - knowledge/brand/voice.md
    - knowledge/icp/personas.md
    - knowledge/services/
    - knowledge/markets/positioning.md
  writes:
    - output/email-nurture/
---

# email-nurture

Writes coordinated email sequences. Different from one-off emails (use `/content-writer` for those). Sequences have a narrative arc across emails, built on the Hook Model to systematically increase engagement and investment over time.

## When to use

- "Write a 5-email nurture for our ebook download leads"
- "Draft an onboarding email series for new signups"
- "Build a re-engagement campaign for dormant users"
- "Write a sales sequence for trial conversions"
- "Welcome series for new newsletter subscribers"

## Sequence types this skill handles

**The lengths and cadences below are starting defaults, not measured facts.** They are a reasonable shape for a B2B audience and nothing more. Where the ESP holds this account's own unsubscribe and reply data by send interval, that data overrides this table and the output must say which one it used.

| Type | Length | Cadence | Goal |
|---|---|---|---|
| **Lead nurture** (post download) | 4-6 emails | day 0, 2, 5, 9, 14 | Qualify, educate, convert to demo |
| **Onboarding** (post signup) | 5-7 emails | day 0, 1, 3, 7, 14, 30 | Activate, drive first value |
| **Re-engagement** (dormant) | 3 emails | day 0, 4, 10 | Revive or sunset |
| **Sales sequence** (trial conversion) | 4-5 emails | day 0, 3, 7, 12, 14 | Convert to paid |
| **Welcome series** (newsletter) | 3 emails | day 0, 3, 7 | Set expectations, drive engagement |
| **Win-back** (churned) | 3 emails | day 0, 7, 21 | Resurrect lapsed customers |

## Inputs needed

- **Sequence type** (from table above)
- **Trigger event**: what causes someone to enter this sequence (download, signup, X days inactive, trial start)
- **Conversion goal**: book demo, upgrade, complete onboarding step, reply, click CTA
- **Audience persona**: from `knowledge/icp/personas.md`
- **Length and cadence**: default per type, override if needed
- **Sender identity**: founder, AE, generic company, or rotation

## Framework: Hook Model + PAS

### Hook Model (Nir Eyal, *Hooked: How to Build Habit-Forming Products*)

Eyal's claim in *Hooked* is that habits are built by running a four-phase loop repeatedly, and that each pass through the loop makes the next one more likely. A nurture sequence is that loop stretched across days, with the inbox as the external trigger.

Every sequence must move the subscriber through four stages in order:

| Stage | What it is | Email role |
|---|---|---|
| **Trigger** | External cue that starts the behavior. Subject line IS the trigger. Must tap an internal trigger: anxiety, curiosity, FOMO, or identity. | Email 1 |
| **Action** | Simplest behavior done in anticipation of reward. One CTA. Zero friction. | Emails 2-3 |
| **Variable Reward** | Unpredictable value that satisfies and creates craving. Not "tip #4". Something that surprises. | Emails 4-5 |
| **Investment** | Ask the user to put something in: reply, complete a step, share a result. Investment increases future hook likelihood. | Email 6+ |

The sequence as a whole must escalate investment. If email 6 asks for less than email 2, the arc is broken.

**Two constraints from *Hooked* that get dropped in practice:**

1. **Variable reward means genuinely variable.** Eyal's point is that a predictable reward stops driving the behaviour. A sequence where every email is "here is tip number N" has an Action stage and no Variable Reward stage, whatever the map says. If you cannot name what is unpredictable about email 4, it is not a reward email, and the sequence will decay in open rate from email 3 onward.
2. **Investment must produce stored value.** In *Hooked*, investment works because it makes the product better for that user next time: data, content, followers, reputation. An investment ask that stores nothing ("hit reply and tell us what you think", then nothing changes) is a request for a favour, not an investment. Prefer asks that visibly change what the user gets next: a preference, a completed setup step, a goal they set.

Eyal also writes explicitly about the ethics of this loop. Say plainly in the README who benefits from the habit being built. A sequence that only benefits the sender is a manipulation, and this skill should name that rather than optimise it.

| Hook stage | Signal it worked | Signal it failed | What to change |
|---|---|---|---|
| Trigger | Opens and clicks on email 1 above the account's own baseline | Email 1 underperforms the account's other sends to the same list | The subject taps no internal trigger. Rewrite it, not the body |
| Action | Clicks concentrate on the single CTA | Clicks spread across links, or none | Too many exits. Cut to one CTA |
| Variable Reward | Replies and forwards appear without being asked for | Opens decay steadily from email 3 | The reward is predictable. Replace the content, not the subject |
| Investment | Users complete the ask, and later emails perform better than earlier ones | The ask is ignored, later emails decay | The ask is too big, or it stores nothing for the user |

### PAS (Problem-Agitate-Solution)

Every individual email body follows this structure:

- **Problem** (1-2 sentences): open with the specific problem this email addresses. Name it precisely, not generically.
- **Agitate** (2-3 sentences): make the pain feel real and immediate. Vivid, concrete, specific to the persona's situation.
- **Solution** (2-3 sentences): introduce the solution - but only after the pain has been established. Never lead with the solution.

## Process

1. **Load context.** Read `knowledge/brand/voice.md`, `knowledge/icp/personas.md`. Stop if voice is missing. Confirm persona match before proceeding.

1b. **Triage the sequence request before writing.** A nurture sequence sends to people repeatedly, so a bad brief costs list health, not just a draft. These are stop conditions, in priority order:

| Condition | Warning sign | Action |
|---|---|---|
| **Consent** | The list was purchased, scraped, or built from a conference badge scan without an opt-in | **Stop and say so.** Sending nurture to a non-consented list risks spam complaints, domain reputation, and legal exposure under GDPR, CAN-SPAM, CASL and equivalents. Recommend a single permission-pass email instead of a sequence |
| **Trigger is not real** | The user cannot name the event that puts someone into this sequence | **Stop.** Without a trigger the sequence is a broadcast, and the Hook Model does not apply. Ask for it |
| **Overlap** | The recipient is already inside another live sequence | **Stop.** Two sequences to one person doubles the send rate they consented to. Ask which one takes priority and suppress the other |
| **Conversion goal not measurable** | The goal is "build awareness" or "stay top of mind" | Flag it. Rewrite the goal as a countable action, or the sequence cannot be judged and will run forever |
| **No off-ramp** | No exit condition on conversion | Flag it. Anyone who converts must exit immediately. Nothing burns trust faster than "have you considered a trial?" three days after paying |
| **Length exceeds substance** | The user asks for 8 emails with material for 4 | Flag it and propose the shorter sequence. Filler emails train the reader to ignore the sender, which costs the whole programme, not this one send |

2. **Map the Hook Model arc.** Before writing, map each email to a Hook stage:

   ```
   Hook Model Map - <Sequence Name>

   Email 1 (Day 0)  - TRIGGER
     Internal trigger tapped: <anxiety | curiosity | FOMO | identity>
     Subject line strategy: <explain how it triggers the internal cue>

   Email 2 (Day X)  - ACTION
     Action asked: <single micro-CTA>
     Friction removed: <what you did to make it dead simple>

   Email 3 (Day X)  - ACTION
     Action asked: <single micro-CTA>

   Email 4 (Day X)  - VARIABLE REWARD
     Reward type: <informational surprise | social connection | achievement>
     Why it's unpredictable: <not "here is tip #4">

   Email 5 (Day X)  - VARIABLE REWARD
     Reward: <what it is>

   Email 6 (Day X)  - INVESTMENT
     Investment asked: <reply with answer | complete setup step | share result>
     Why this increases commitment: <explain>
   ```

   Show this map to the user and get confirmation before drafting.

3. **Write each email** using PAS structure:

   ```
   ---
   email: 1 of N
   day: 0
   hook-stage: TRIGGER
   internal-trigger: <anxiety | curiosity | FOMO | identity>
   trigger: <event>
   sender: <name|company>
   ---

   Subject: <under 50 chars, no clickbait, no all caps>
   Preview text: <30-90 chars, complements subject, never repeats it>

   [PROBLEM - 1-2 sentences: name the specific problem]

   [AGITATE - 2-3 sentences: make the pain vivid and immediate]

   [SOLUTION - 2-3 sentences: introduce it after the pain lands]

   <CTA - one action, low friction>

   <Sign-off>
   <Sender name and role>

   P.S. <optional but high-performing. One line. Reinforce the CTA.>
   ```

4. **Subject line as trigger - internal trigger checklist.** For each subject line, confirm which internal trigger it taps:

   - [ ] **Anxiety**: "Are you making this mistake with X?"
   - [ ] **Curiosity**: "What most teams get wrong about X"
   - [ ] **FOMO**: "What [peer segment] is doing that you're not"
   - [ ] **Identity**: "You're the kind of person who cares about X"

   If the subject line taps none of these, rewrite it. A subject that doesn't tap an internal trigger is just an announcement.

5. **Voice rules**:
   - Match `knowledge/brand/voice.md`
   - Conversational, like writing to one person
   - Second-person ("you"), not third-person
   - One CTA per email. If you have two, the second should be a soft "or just reply"
   - No "Hope this email finds you well"
   - No "I just wanted to reach out"
   - No "Circling back" unless this is intentionally a follow-up

6. **Subject line rules**:
   - 30-50 chars (most clients truncate at 60)
   - No emojis unless `knowledge/brand/voice.md` says they are part of the voice
   - Curiosity, specificity, or self-interest. Pick one.
   - Lowercase or sentence case (matches conversational tone)
   - Test variants: provide 2 alt subject lines per email

7. **Self-check** for the full sequence. Every item is checkable by reading the saved files. If you cannot name the file and line that satisfies it, it fails.

   - [ ] Every email file has a one-line `job:` in its frontmatter, and no two are the same
   - [ ] The `hook-stage` values across the files read Trigger, then Action, then Variable Reward, then Investment, with no stage skipped
   - [ ] The Investment email's ask changes what the reader receives afterwards. Name the thing it stores
   - [ ] The Variable Reward emails contain something the reader could not have predicted from the subject line. State what it is for each
   - [ ] Every email body has three separable blocks in Problem, Agitate, Solution order. The first sentence of each body does not name the product
   - [ ] Exactly one primary CTA link per email. Count the links in each file
   - [ ] The `internal-trigger` values across the files contain no duplicates
   - [ ] No two subject lines share their first three words
   - [ ] Word count of the full sequence is stated in the README, and every email is under 200 words
   - [ ] Every number, customer name and product capability in the sequence appears in `knowledge/services/` or was supplied by the user in this session. Anything else reads `[NEEDS INPUT: <what>]`
   - [ ] The exit conditions are written in the README: what removes someone from this sequence, including conversion, reply, and unsubscribe
   - [ ] Success metrics are this account's own trailing numbers or are marked `[NEEDS INPUT]`. No open-rate target from memory

8. **Save** to `output/email-nurture/<DD-MM-YYYY>-<sequence-name>/`:
   ```
   output/email-nurture/25-04-2026-trial-conversion/
   ├── README.md          (sequence overview, hook map, cadence, goals, A/B test ideas)
   ├── email-1-day-0.md
   ├── email-2-day-3.md
   ├── email-3-day-7.md
   ├── email-4-day-12.md
   └── email-5-day-14.md
   ```

9. **README.md template**:
   ```
   # <Sequence name>

   **Type**: <type>
   **Trigger**: <event>
   **Audience**: <persona>
   **Goal**: <conversion goal>
   **Length**: N emails
   **Total window**: N days

   ## Hook Model Map
   | # | Day | Hook Stage | Internal Trigger | Subject | Job | CTA |
   |---|---|---|---|---|---|---|
   | 1 | 0 | Trigger | Anxiety | ... | ... | ... |

   ## A/B test ideas
   - Test subject line A vs B on Email 1
   - Test PS variant on Email 4
   - Test send time (Tue vs Thu)

   ## Exit conditions
   - Converts to <goal> -> remove immediately, do not send the remainder
   - Replies to any email -> remove and route to a human
   - Unsubscribes or marks spam -> suppress across all sequences, not just this one
   - Completes the sequence without converting -> where next, and after how long

   ## Success metrics
   Every target below must be this account's own trailing figure or `[NEEDS INPUT]`.
   - Email 1 click rate target: [NEEDS INPUT: last 3 sends to this segment]
   - Sequence reply rate target: [NEEDS INPUT]
   - Conversion to <goal> target: [NEEDS INPUT]
   - Unsubscribe rate ceiling: [NEEDS INPUT: this account's normal rate. Above it, pause the sequence]
   ```

## Rules

- Never write emails that don't have a clear job. Each email earns its place.
- One CTA per email. Two CTAs = no CTA.
- Subject lines must reflect what's actually inside. No clickbait.
- PAS is mandatory for every email body. Do not open with the solution.
- If the user is sending from a real person (founder, AE), include a check: "Confirm this matches how <Name> writes before sending."
- Every sequence ends with a clear off-ramp: either a clear ask or "we'll stop emailing you about this."
- If the sequence has no Investment-stage email, it is not a Hook sequence. Add one or tell the user why it was omitted.

## Quick Reference: Hook Model

| Stage | Goal | Question to ask |
|---|---|---|
| Trigger | Get them to open and engage | What internal emotion does the subject line tap? |
| Action | Get one simple behavior | Is the CTA the simplest possible next step? |
| Variable Reward | Deliver surprising value | Would someone forward this unprompted? |
| Investment | Get them to put something in | Does this email ask them to give something back? |

## Quick Reference: PAS

| Section | Length | Rule |
|---|---|---|
| Problem | 1-2 sentences | Name the specific problem. Not generic. |
| Agitate | 2-3 sentences | Make the pain vivid, real, and immediate. |
| Solution | 2-3 sentences | Only introduce it after the pain has landed. |

## Never invent

- **No statistic, customer name, result, or product capability that is not documented in
  `knowledge/services/`.** Mark gaps `[NEEDS INPUT: <what>]` instead of writing around them.
- "Make the pain vivid" means describe the situation precisely, not invent the reader's numbers.
- **Do not set an open-rate target from memory.** Apple Mail Privacy Protection pre-fetches
  tracking pixels, so open rate has been inflated by an unknown factor since 2021 and is unfit as
  a success criterion. Use this account's own last-3-sends baseline, or pick reply and click
  instead, and say why.

## When to stop and hand back

Not every request should become a sequence. Say so directly rather than writing one anyway.

1. **One message, one audience, one time** is a broadcast, not a nurture. Use `/content-writer`.
2. **The user wants to reach people who have never heard of them.** That is cold outreach, and it has different consent and volume rules. Use `/pr-pitch-writer` for a single pitch, and do not build it as a drip.
3. **The product has no activation moment yet.** An onboarding sequence cannot rescue an onboarding experience that does not have a first-value step. Say so, and point at the product question rather than writing six emails around it.
4. **The last sequence to this segment has not been reviewed.** Adding a second programme on top of an unmeasured one makes both unreadable. Run `/kpi-review` first.

## What this skill cannot know

These are limitations of the skill. Anything below that reaches the output must be labelled `[UNVERIFIED]` there.

- **Deliverability and inbox placement for this domain.** Authentication records, domain reputation, list hygiene and the recipient's own filters decide whether any of this is read, and none of it is visible from here.
- **Whether open rate is meaningful for this list.** Mail privacy features pre-fetch tracking pixels, so open rate is inflated by an unknown and list-specific factor. Prefer click and reply.
- **Whether the ESP renders the formatting, the sender name, or the preview text as written.** Send a seed test to several clients before launch.
- **Whether the list has valid consent for this jurisdiction.** Consent rules differ by country and by how the address was collected. That is a question for whoever owns the list.
- **Whether a claim in the sequence needs legal review in the recipient's market.**

## Related skills

- `/content-writer` for a single email that is not part of a sequence
- `/pr-pitch-writer` for cold outreach to someone with no prior relationship, where these consent rules do not apply in the same way
- `/newsletter-writer` for the recurring publication, which is a subscription rather than a triggered flow
- `/ab-copy-writer` for testing subject lines properly, with a stopping rule rather than a hunch
- `/customer-persona` when the persona file cannot answer what this segment's internal trigger actually is
- `/case-study-writer` for the proof asset that the day-7 or day-14 email should be pointing at
- `/kpi-review` for this account's own trailing open, click, reply and unsubscribe rates, which override every default here
- `/webinar-planner` when the sequence is promoting an event, so the invite and reminder emails stay inside one plan
- `/retro` after the sequence has run, to record what actually happened in `knowledge/learnings.md`


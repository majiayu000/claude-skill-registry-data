---
name: pr-pitch-writer
description: Write personalized pitch emails to journalists, podcasters, newsletter writers, and analysts using AIDA adapted for media pitching and Ryan Holiday's journalist psychology from "Trust Me I'm Lying." Different from press releases (use /press-release-writer for those). Use when the user asks to pitch a journalist, pitch a reporter, "get coverage in X", media outreach, podcast pitch, analyst briefing request, or wants to land a story. Reads brand voice and positioning from knowledge/. For the press release itself, see press-release-writer. For the underlying customer story, see case-study-writer.
metadata:
  grounded_in:
    - "Trust Me, I'm Lying - Holiday"
  reads:
    - knowledge/brand/voice.md
    - knowledge/markets/positioning.md
    - knowledge/services/
    - knowledge/content-library/case-studies/
  writes:
    - output/pr-pitch/
---

# pr-pitch-writer

Writes pitch emails that journalists actually read. Different from press releases: pitches are personal, short, and earn the click. Built on AIDA adapted for media pitching and Ryan Holiday's journalist psychology.

## Frameworks

### AIDA adapted for media pitching

**ATTENTION (subject line)**: Journalists get 500+ pitches per week. The subject line is a headline, not a description. It must earn the open in a crowded inbox.

**INTEREST (first sentence)**: Why does this story matter to THIS journalist's readers? Not to you - to them. The first sentence is about the audience, not the sender.

**DESIRE (the angle / news peg)**: What makes this story surprising, timely, or uniquely valuable? The "news peg" - what it attaches to in the current conversation.

**ACTION (the ask)**: What you want them to do. Specific and easy. "Reply to this email if you'd like the data" beats "let me know if you're interested."

### Ryan Holiday's journalist psychology - "Trust Me I'm Lying"

1. **Traffic over truth**: Journalists need stories that get clicks for their audience. Ask: what would make their readers share this?
2. **Narrative over facts**: Facts support the narrative - the narrative is what gets coverage. Lead with the story angle, support with proof.
3. **Timeliness over importance**: Attach your story to what's already being covered. A story that taps a current conversation gets placed faster than a better story that doesn't.
4. **Effortlessness**: The scarce resource is journalist attention, not pitches. Make it trivially easy to say yes.
5. **Exclusivity**: "I'm offering this story to you first" changes the dynamic. Scarcity creates urgency even for journalists.

### Practical implications

**The "lazy journalist" test**: Could the journalist copy the pitch, add 2 hours of reporting, and have a publishable story? If yes, the pitch is doing its job. If they'd need to reconstruct the whole angle, make it easier.

**News peg identification**: What is happening RIGHT NOW that this story attaches to? A trend piece, a regulatory change, a competitor announcement, a viral conversation? A story without a peg is a press release dressed up as a pitch.

**Exclusivity language**: "First look," "embargo until [date]," "I'm only sending this to [N] reporters" are legitimate tools when true. Use them when you can. Never fake it.

## When to use

- "Pitch this story to <journalist>"
- "Write an email to a reporter at <publication>"
- "Get me on <podcast>"
- "Pitch <analyst> for a briefing"
- "Outreach to newsletter writer X"

## Outreach types this skill handles

| Type | Goal | Length | Hook style |
|---|---|---|---|
| **News pitch** (timely story) | Coverage in 1-2 weeks | 80-120 words | News value + exclusive offer |
| **Trend pitch** (you're the expert) | Quoted source for trend piece | 100-150 words | Data + POV |
| **Podcast pitch** | Booking | 100-180 words | Specific to host's recent episode |
| **Newsletter pitch** | Mention or feature | 60-100 words | Match their format |
| **Analyst briefing request** | Briefing slot | 100-150 words | New release + customer proof |
| **Customer story pitch** | Profile of a customer | 150-200 words | Outcome + access to interview |

## Inputs needed

- **Recipient**: name, publication, beat, recent piece they wrote (paste URL or summary)
- **Pitch type** (from table)
- **Story or angle**: what's newsworthy or interesting?
- **Proof**: data, customer, exclusive, expert availability
- **Why this person** (mandatory): why are they the right journalist/host for this?
- **What you're asking for**: 15-min interview, embargoed access, comment, podcast booking

## Process

1. **Load context.** Read `knowledge/brand/voice.md`, `knowledge/markets/positioning.md`, and any case studies that support the pitch.

2. **Research the recipient. Hard gate: never characterise a piece you have not read.**

   If the user supplied a link, fetch and read it with WebFetch. If you cannot fetch it, or no
   link was supplied, **stop and write `[NEEDS INPUT: link to their recent piece]`.** Do not
   proceed to draft line 1 from what you believe this reporter usually covers.

   This is the highest-consequence rule in the skill. The failure mode is writing "Your piece on
   X argued Y" to a journalist who wrote nothing of the kind. It is worse than sending nothing:
   it proves the sender automated the email and did not read them, it is the exact thing
   reporters screenshot publicly, and it burns the relationship and the brand in one send.
   A pitch that goes out a day late having actually read the piece beats one that goes out today
   having guessed.

   Never infer a journalist's position, argument, or beat from their publication, their title, or
   general knowledge. Read the specific piece, or leave the placeholder.

3. **Identify the news peg. Holiday describes newsroom incentives, he does not license us to invent.**

   "Traffic over truth" and "narrative over facts" are Holiday's account of how media economics
   pull coverage. They are a lens for predicting what gets picked up. They are not instructions
   to bend the facts of our own story. Everything we assert must be true and sourced. If the
   angle only works with a claim we cannot support, the angle is dead, not the sourcing standard.

   Answer:
   - What is happening in the world RIGHT NOW that this story connects to?
   - What trend, event, or conversation is this story an instance of?
   - If there is no genuine news peg, say so plainly and recommend waiting for one. "Create the
     angle" means find the true framing that connects this to a live conversation. It never means
     manufacture a trend, a claim, or an urgency that does not exist.

4. **Apply the "lazy journalist" test.** Map out the story:
   - What is the narrative (not the facts)?
   - What proof supports it (data, customer, expert)?
   - How much work does the journalist need to do to publish?
   - If the answer is more than 2-3 hours of reporting, simplify the angle or provide more of the work upfront.

5. **Identify angle from THEIR perspective.** Reframe:
   - Why does THEIR audience care? (not "why is this exciting for us")
   - What's the tension, controversy, or surprise?
   - What data or access can we offer that they can't get elsewhere?

6. **Write the pitch** applying AIDA line by line:

   ```
   Subject: <ATTENTION - under 60 chars, specific, not "Quick question" or "Following up">
   <The subject is a headline. It earns the open. It contains a number, a tension, or a specific claim.>

   Hi <First name>,

   <INTEREST - Line 1: specific reference to their recent work. Not flattery, but engagement.
   "Your piece on [topic] argued [X] - this is the counter-data.">

   <DESIRE - Line 2: the hook. The single most interesting fact. Often a number, exclusive, or contrarian claim.
   This is the news peg. It attaches to what they already care about.>

   <DESIRE - Line 3-4: the offer. What you can give them: data, customer, expert, embargo.
   Make it concrete. Apply exclusivity where true: "I'm offering this to you first before going wider.">

   <ACTION - Line 5: the ask. Specific. "15-min call this week?" not "Let me know if interested.">

   <Sign-off>
   <Sender name + role + company>
   <P.S.: optional, 1 line. Often the strongest hook moved here.>
   ```

7. **Subject line rules**:
   - Specific noun, not generic verb
   - Numbers, **only ones the user supplied**. If a number would strengthen the subject but you
     do not have it, write `[NEEDS INPUT: the figure]`. Never generate a plausible-looking
     statistic. A fabricated stat in a pitch is handed straight to a professional fact-checker.
   - No "Quick question", "Following up", "Touching base"
   - No clickbait - the email must deliver what the subject promised
   - Ask: would this subject line work as a headline for their publication?

8. **Length and pacing**:
   - 80-180 words total. Journalists scan, not read.
   - 5-7 sentences max
   - One paragraph is OK if the pitch is tight enough

9. **Voice rules**:
   - Conversational, not corporate
   - Match the journalist's beat. Tech reporter: tighter, faster. Trade pub: more context.
   - No jargon unless they use it
   - No marketing language ("revolutionary", "best-in-class", "unlock")
   - No em dashes
   - First person, present tense

10. **Self-check**:

    AIDA checks:
    - ATTENTION: does the subject line work as a headline for their publication?
    - INTEREST: does the first sentence prove you know their work and their readers?
    - DESIRE: is the news peg clear? Is exclusivity offered if available?
    - ACTION: is there exactly one ask, and is it easy to say yes to?

    Holiday psychology checks:
    - Traffic test: would their readers click and share this story?
    - Narrative test: is the story angle leading, not the facts?
    - Timeliness test: what is the news peg, and is it current?
    - Lazy journalist test: could they publish this with 2 hours of work?
    - Effortlessness: have you removed every friction point from saying yes?

    Format checks:
    - First line proves you know their work
    - Hook in the first 30 words
    - Specific ask, not vague
    - One CTA
    - No attachments (mention them, offer to send)
    - Subject line under 60 chars

11. **Save** to `output/pr-pitch/<DD-MM-YYYY>-<recipient-slug>.md` with frontmatter:
    ```yaml
    ---
    format: pr-pitch
    recipient: <name>
    publication: <publication>
    pitch-type: <type>
    news-peg: <one sentence>
    exclusivity: <yes|no>
    ask: <specific ask>
    lazy-journalist-test: <pass|needs work>
    created: DD-MM-YYYY
    sent: <pending|DD-MM-YYYY>
    ---
    ```

12. **Offer companion assets**:
    - Press release (if news pitch) via `/press-release-writer`
    - Background brief (1-pager) the journalist can use
    - 3 follow-up email templates (if no response after 4, 9, 14 days)
    - Talking points if a call is booked

## Pitch tracker

Maintain `output/pr-pitch/_tracker.md` (create if not exists):

```
# PR pitch tracker

| Date sent | Recipient | Pub | Pitch | News peg | Status | Follow-up |
|---|---|---|---|---|---|---|
| DD-MM-YYYY | <name> | <pub> | <slug> | <peg> | sent | day +4 |
```

Update this every time a pitch goes out.

## Rules

- One pitch, one recipient. Never BCC. Never "Hi all."
- Specific reference to their work in line 1, or don't send.
- No news peg, no pitch. An undated story is a press release.
- Never overstate. If you say "exclusive," it must actually be exclusive.
- Never attach files in a cold pitch. Offer them.
- If the journalist doesn't reply, follow up at day 4 and day 9. After that, drop it.
- The lazy journalist test is non-negotiable. If the journalist has to construct the story from scratch, the pitch will be ignored.
- **Never characterise, quote, or summarise a piece you have not actually read.** If it was not
  fetched, it does not go in the email.
- **Never invent a statistic, a customer name, a quote, or a company milestone.** Use
  `[NEEDS INPUT: ...]` and send the pitch to the user to fill before it goes out.
- Never claim an embargo, an exclusive, or "first look" unless it is literally true for this
  recipient.

## What this skill cannot verify

State these in the output every time:

- Whether the recipient still covers this beat. Beats change and mastheads go stale
- Whether the piece you referenced is their most recent or their most relevant
- Whether a competitor has already pitched this angle to them this week
- Any figure marked `[NEEDS INPUT]`, which the user must supply and stand behind

## Related skills

- `/press-release-writer` for the formal release this pitch may accompany
- `/case-study-writer` for the underlying customer story that gives a pitch its proof
- `/copy-review` to tighten the pitch before it goes out
- `/brand-context` creates the positioning and voice files this reads
- Keep the pitch tracker current. Tracking response rate is how this gets better over time.

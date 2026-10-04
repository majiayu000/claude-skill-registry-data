---
name: x-healthcare-posts
description: Generate high-performing X (Twitter) posts and threads optimized for Healthcare AI, AI, and Automation audiences. **ALWAYS use this skill when the user asks to write, create, draft, or generate ANY X post or thread, regardless of source material.** This includes requests with articles, research papers, raw ideas, industry news, or any content for X. Also use when the user asks to improve, edit, or analyze existing X posts. Follows proven viral structures based on X's open source recommendation algorithm, sounds like an insider operator (Car Dealership Guy style), and aligns with Healthcare AI industry voice. Generates multiple variations and content suggestions from long articles.
---

# X Healthcare Posts

Transform articles, research, and ideas into high-performing X posts and threads that drive engagement in Healthcare AI, AI, and Automation circles.

## Core Principle

**Goal: Make people smarter fast, give them a position they can adopt, or reveal insider reality.**

Viral X content in Healthcare AI does three things:
1. Takes a clear stance (not vague observation)
2. Provides receipts (evidence, numbers, real examples)
3. Invites expert replies (drives conversation)

The X algorithm rewards replies, sustained conversation, and author engagement. Write posts that experts pause on, think about, and reply to with their own insights.

## Quick Start Workflow

### Step 1: Analyze Input

Identify what the user provided:
- **Research paper/article**: Extract 3-5 distinct angles for multiple posts or threads
- **Raw ideas**: Find the contrarian insight or hidden reality
- **Industry news**: Develop clear stance with practical implication
- **Long content**: Generate content calendar with mix of single posts and threads

### Step 2: Select Format

**Single Post** (2-3 sentences, one clear point)
Best for: Quick reactions, contrarian takes, hidden truths

**Thread** (7-8 tweets)
Best for: Explainers, operator reality, experience-based insights, frameworks

### Step 3: Select Structure

For detailed structures and examples, see `references/structures.md`

**Single Post Structures:**
- The Contrarian Stance
- The Hidden Reality
- The Trust Break Moment
- The Workflow Truth
- The Future Clear

**Thread Structures:**
- Explainer Thread (teach a framework)
- Operator Reality Thread (reveal insider truth)
- Experience Thread (story that shifted thinking)
- Car Dealership Guy Style (transparent industry mechanics)

### Step 4: Draft with Viral Elements

Every post must include:
1. **Clear stance** (not "AI is changing healthcare" but "this is the adoption bottleneck")
2. **Receipts** (study, number, real observation, policy reference)
3. **Practical implication** (decision rule, question to ask, evaluation principle)
4. **Reply invitation** (specific prompt for experts to add their view)

### Step 5: Optimize for X Algorithm

Based on Heavy Ranker weights:
- **Replies matter most** - invite thoughtful responses
- **Author engagement** - plan to reply in thread
- **Avoid negative signals** - no bait that triggers blocks/mutes
- **Drive conversation clicks** - make people want to read thread
- **Time in thread** - structure keeps people reading

### Step 6: Generate Variations

For long articles (>1000 words), extract multiple angles:
- 3-5 single posts covering different insights
- 2-3 threads with different structures
- Suggested posting schedule

Use `scripts/content_calendar.py`:
```bash
python scripts/content_calendar.py <article.md> --format both
```

## Healthcare AI Voice Guidelines

### The Operator Voice

Write like Car Dealership Guy, but for Healthcare AI:
- Reveal what insiders know but don't say publicly
- Explain system realities (procurement, compliance, workflow)
- Show the gap between demo and deployment
- Be transparent about what actually determines success

### Leadership Lanes (Pick One)

**Workflow and Adoption Reality**
How AI actually lands in clinics and hospitals

**Evaluation and Safety Clarity**
How to test, monitor, avoid false confidence

**Automation that Reduces Burden**
Practical automations that remove clinician friction

### Credibility Markers

Sound like a practitioner, not a marketer:
- Specific numbers and constraints
- Named real challenges from implementation
- Honest about what breaks
- Technical accuracy without jargon
- References to actual workflows and incentives

### What Trends in Healthcare AI (2026)

Audience is tired of hype. They respond to:
- **Stance** - clear position on bottlenecks and winners
- **Receipts** - evidence, not claims
- **Practical implications** - checklists, vendor questions, evaluation rules
- **Intellectual honesty** - limits, tradeoffs, unknowns
- **Conversation starters** - prompts that invite expert additions

### Avoid These (Kill Engagement)

Never use:
- "AI is transforming healthcare" (vague, overused)
- "Revolutionary" / "Game-changer" (hype signals)
- "The future of medicine" (abstract, no stance)
- Lists of obvious points (low value)
- Generic inspiration (not what experts want)
- Hype without receipts (triggers blocks)

## X Algorithm Optimization

### What Heavy Ranker Prioritizes

Based on open source architecture:

**High Weight Actions:**
- Reply probability (huge multiplier)
- Reply engaged by author (extremely high)
- Good profile clicks
- Time in conversation
- Video watch to halfway

**High Negative Weight:**
- "Show less" signals
- Blocks and mutes
- Reports
- Quick exits

### Creator Translation

**Do This:**
- Structure posts to invite expert replies
- Reply thoughtfully in your threads (signals author engagement)
- Use threads for topics that reward sustained reading
- Give people a position they can adopt (makes reposting feel valuable)
- Reveal insider reality (creates share impulse)

**Avoid This:**
- Bait that triggers blocks or "show less"
- Walls of text (people exit fast)
- Generic takes anyone could write
- Asking "thoughts?" (low quality replies)

## Single Post Formula

**Structure: Stance → Evidence/Reality → Implication**

**Line 1:** Clear contrarian or insider stance
**Line 2:** The supporting reality or evidence
**Line 3:** Practical implication or what it means

**Length:** 2-3 sentences, 40-80 words
**Tone:** Confident operator, not loud marketer

See `references/examples.md` for 10+ annotated examples

## Thread Formula

**8-tweet structure:**

**Tweet 1:** Bold promise or contrarian claim
**Tweets 2-3:** Set up the problem or misconception
**Tweets 4-6:** The reality, framework, or insight (numbered if teaching)
**Tweet 7:** Practical application or decision rule
**Tweet 8:** What to do next + conversation invitation

**Style Notes:**
- Each tweet stands alone but flows to next
- Use numbers when teaching (3 lessons, 5 truths, 7 steps)
- Break at natural thought boundaries
- Final tweet explicitly invites expert replies

See `references/thread_examples.md` for complete annotated threads

## Content Calendar Generation

For articles >1000 words:

```bash
python scripts/content_calendar.py <input.md> --posts 5 --threads 2
```

Generates:
- 5 single posts (different angles)
- 2 threads (different structures)
- Posting schedule (spacing recommendations)
- Mix optimized for variety and sustained engagement

## Quality Checklist

Before posting, verify:

**Stance Check:**
- [ ] Takes clear position (not observation)
- [ ] Specific enough to disagree with
- [ ] Contrarian or reveals insider reality

**Evidence Check:**
- [ ] Includes receipts (number, study, real example)
- [ ] Technically accurate
- [ ] Credible to practitioners

**Value Check:**
- [ ] Gives decision rule or practical implication
- [ ] Makes reader smarter in 30 seconds
- [ ] Worth reposting to look informed

**Algorithm Check:**
- [ ] Invites thoughtful replies (not "thoughts?")
- [ ] No bait that triggers blocks/mutes
- [ ] Structure rewards sustained reading (for threads)

**Voice Check:**
- [ ] Sounds like insider operator
- [ ] No hype or marketing language
- [ ] Would say this to colleague over coffee

Use `scripts/post_analyzer.py`:
```bash
python scripts/post_analyzer.py <draft.txt>
```

## Reply Strategy

Replies are the highest weighted engagement signal.

**In your threads:**
- Reply to every substantive response within 2 hours
- Add new insights, don't just thank
- Ask follow-up questions to extend conversation
- Highlight best replies to encourage more

**In others' threads:**
- Add specific examples from your experience
- Provide decision rules or frameworks
- Respectfully disagree with reasoning (not attacks)
- Build relationships with 25 key accounts in your niche

This converts visibility into follows and positions you as conversation host.

## Three-Week Launch Strategy

**Week 1: Evidence Translation**
Post 3-4 research translations (quick reactions to studies)
Reply actively in 10 expert threads

**Week 2: Operator Reality**
Post 2-3 insider truth posts revealing hidden constraints
Launch 1 explainer thread on adoption reality

**Week 3: Establish Lane**
Post consistent theme (pick workflow/evaluation/automation lane)
Launch 1 operator reality thread
Reply strategy: become known for specific expertise

Track what drives replies, adjust weekly.

## Advanced: The Car Dealership Guy Clone

To become "transparent operator voice" for Healthcare AI:

**Formula:**
- Pick one opaque process (procurement, evaluation, compliance, adoption)
- Post consistent insider revelations
- Use simple format: claim → supporting facts → conclusion
- Never marketing, always reality
- Build habit with niche consistency

**Example lane:**
"Clinical AI procurement reality" - reveal how buying actually works

People share because it makes them feel informed about hidden systems.

## Master Templates

Use these files:
- `assets/post_template.txt` - single post structure
- `assets/thread_template.txt` - thread scaffolding
- `references/examples.md` - 15 annotated high-performers
- `references/structures.md` - complete structure library

## Performance Benchmarking

Use `scripts/engagement_analyzer.py` to track:
```bash
python scripts/engagement_analyzer.py --handle YourHandle --days 30
```

Analyzes which structures and topics drive:
- Reply rates (most important)
- Repost patterns
- Profile clicks
- Negative signals

Adjust content mix based on what actually performs for your account.

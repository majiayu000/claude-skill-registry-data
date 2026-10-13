---
name: generating-social-posts
version: "1.0.0"
description: >
  Generates platform-optimized social posts and audio scripts in Kyle Rosebrook's voice — confident, specific, grounded in real experience, zero fluff. Supports LinkedIn, Twitter/X, Threads, Blog, and Audio Script. Content types: lesson, about_me, tidbit, tool_tip, review, augmentor, hidden_gem, hot_take, workflow, mistake, upgrade. Always gathers 4–5 clarifiers before generating unless enough context already exists in the conversation. Shows structural scaffold alongside the final post.

  Use this skill whenever the user mentions writing a post, drafting content, creating a lesson, sharing a tool tip, writing a hot take, building a workflow post, doing an about_me, making a tidbit, reviewing a tool, writing for LinkedIn or Twitter/X or Threads or a blog, scripting audio, or asks for any social or published content. Even if the user just says "write a post about X" or "help me share this" — use this skill. If a content type is mentioned (lesson, hot_take, tidbit, etc.), use this skill immediately.
---

# Social Post Generator

Generates posts that sound like Kyle Rosebrook wrote them — not like AI wrote them about him.

The whole job is to get from raw experience/idea → published content that lands. The two failure modes are: (1) generic AI voice that could apply to anyone, (2) correct structure but wrong person. Both are rejections.

---

## Step 1: Gather Inputs

Before generating, identify what you have and what you need. The goal is always 4–5 clarifiers — no more, no less — unless the conversation already answers them.

**Extract from context first.** If the user mentions the topic, platform, or tone in their message, lock those in silently and ask only for what's missing.

**The 5 clarifier questions (ask all that aren't already answered):**

1. **CONTENT_TYPE** — Which type? `lesson | about_me | tidbit | tool_tip | review | augmentor | hidden_gem | hot_take | workflow | mistake | upgrade`
2. **TOPIC** — What's the post actually about? The more specific, the better. "I used Claude to fix an n8n auth bug" beats "AI tools."
3. **CONTEXT** — What happened? Real scenario, tool name, result, failure — the raw material that makes the post feel lived-in. Optional but important.
4. **PLATFORM** — `LinkedIn | Twitter/X | Threads | Blog | Audio Script`
5. **LENGTH + TONE** — Length: `short | medium | long`. Tone: `default | witty | sharp | reflective | aggressive | minimal`

**Asking the clarifiers:**
Present them conversationally, not as a numbered form. Group them naturally. Example: "Before I draft this — which platform, and do you have a specific scenario or tool in mind, or should I build around the concept?"

---

## Step 2: Generate

### Voice Rules (non-negotiable)
These are extracted from Kyle's actual published writing. Every output gets checked against them.

- **Declarative observations, not performed insight.** "I stopped prompting for outputs. I started designing flows." Not "I had a revelation about how to use AI."
- **Technical descriptions of emotional states.** "The cognitive architecture I was born with stopped working the way it used to." Not "I was struggling."
- **Specificity over impressiveness.** Name the tool. Name the error. Name the file path (`D:\02_Homebase\Cowork`). Name the number (`1.5 million API keys`). Vague credibility is no credibility.
- **Anti-credential moves land.** Acknowledge what you're *not* before saying what you are. "I'm not a security professional. I'm an L1 service desk tech who builds AI apps on the side." That sentence earns more trust than a resume.
- **Sentence variation is intentional.** Short. Then a longer one that earns the room it takes up. Then short again.
- **Closers are punchy or paradoxical.** "The boring habits compound. The clever ones don't." Not "I hope this helps someone."
- **No emojis. No hashtags unless platform requires them.**
- **No clichés:** "in today's world," "leverage AI," "game-changer," "at the end of the day," "and that's when I realized."
- **No performed vulnerability.** If it's personal, be specific and dry about it. Don't editorialize the emotion.
- **Strategic profanity available, used sparingly.**
- **Humor lands dry.** Never perform the punchline.

### Platform Constraints

| Platform | Format | Length guidance |
|---|---|---|
| LinkedIn | Prose paragraphs, line breaks for pacing | Short: 150–250w / Medium: 300–500w / Long: 600–900w |
| Twitter/X | Thread or single post | Short: 1 tweet / Medium: 4–6 tweet thread / Long: 8–12 tweet thread |
| Threads | Conversational, tighter than LinkedIn | Short: 100–180w / Medium: 200–350w |
| Blog | Essay structure, can use subheadings | Short: 400–600w / Medium: 700–1,200w / Long: 1,500–2,500w |
| Audio Script | Spoken-word pacing, no markdown, natural pauses | Short: ~90s / Medium: ~3min / Long: ~6min |

**Twitter/X threading format:**
Number threads explicitly: `[1/6]`, `[2/6]`, etc. Each tweet must stand alone as a sentence. Hook tweet never wastes its character count.

**Audio Script formatting:**
- No bullet points or code blocks
- Natural sentence rhythm (short bursts + breathing room)
- Mark pauses: `[pause]`
- Mark emphasis: ALL CAPS on a single key word per sentence max
- No URLs — describe links verbally ("link in bio / show notes")

---

## Step 3: Structure Templates

Auto-select based on CONTENT_TYPE. Show the scaffold explicitly in output.

```
LESSON:
Hook → What happened → What most people miss → Actual lesson → Actionable takeaway

TOOL_TIP:
Hook → Problem → Tool → Exact use case → Why it matters → Bonus edge case

HIDDEN_GEM:
Hook → Tool/idea reveal → Why no one talks about it → Real use → Who should care

REVIEW:
Hook → Context → What it does → What's actually good → What's overrated → Verdict

ABOUT_ME:
Hook → Personal trait/story → How it shaped thinking → Why it matters now

AUGMENTOR:
Hook → Task → How AI changes it → Exact workflow → Result difference

WORKFLOW:
Hook → Before vs after → Steps → Tools → Optimization insight

MISTAKE:
Hook → What went wrong → Why it happened → Fix → Lesson

HOT_TAKE:
Hook → Contrarian statement → Justification → Example → Closing punch

TIDBIT:
(3-part format) Numbered entries: Label → Title → Body → Micro-meta note
Closing paradox line.

UPGRADE:
Hook → What you were doing → What changed → Specific delta → Why it matters
```

---

## Step 4: Output Format

Always deliver output in this structure:

```
**SCAFFOLD**
[Content type] → [named structure steps, filled in]

---

**POST**
[The actual post]

---

**STRUCTURE NOTES**
[1-3 lines on any deliberate choices: why this hook, why this closer, what was cut]
```

---

## Anti-Slop Gate

Before delivering, run this check internally:

1. **Could this post have been written about anyone?** If yes → add a specific tool, failure, number, or place.
2. **Does it sound like a LinkedIn influencer?** If yes → remove the advice-giving tone and replace with declarative observation.
3. **Is the hook a question?** If yes → rewrite as a statement. ("Most people don't know X" → "Most people get X wrong.")
4. **Does the closer try too hard?** If yes → shorten it or make it drier.
5. **Is there anything in here that isn't true or verifiable for Kyle?** If unsure → flag it with `[verify]` inline.

---

## Voice Reference Files

Load these as needed — don't load all three on every request.

| File | Load when |
|---|---|
| `references/voice-samples.md` | Calibrating tone on about_me, long-form blog, or audio script |
| `references/voice-rules.md` | Extended register guidance; needed for audio script, about_me, long-form |
| `references/anti-patterns.md` | Running the anti-slop gate; any draft that feels off |

When in doubt on voice, the canonical examples are:

- **Lessons essay** — "Ground truth beats fluency." Lead with what went wrong, then the structural fix.
- **Tidbits** — Numbered, tight, meta-note at the end of each. The ending: "The boring habits compound. The clever ones don't."
- **Preflight** — Anti-credential opener → specific technical failure → who this is for (the version of me from 12 months ago).
- **About page** — "Same skill. Different substrates." — the thesis move: pattern recognized across different contexts.

The diagnostic instinct is the throughline. If a post can reference it naturally — the skill of reading a room / a system / a codebase as the same skill — use it.

---

## Iteration

After delivering a post, ask exactly one thing:
"Anything to adjust — tone, specificity, closer, or length?"

Do not ask multiple questions after delivery. One prompt, one iteration direction.

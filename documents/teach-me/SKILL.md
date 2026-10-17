---
name: teach-me
description: Teach a topic, video, article, codebase change, spec, or transcript until the user demonstrably understands it, using staged instruction, a running checklist doc, and quizzes. Use whenever the user says "teach me", "explain this in detail", "help me understand X", "/teach-me", "walk me through this", "I want to learn X", "understand this deeply", or pastes a YouTube URL, article, paper, PR, or spec and asks to understand it rather than summarize it. Also use when the user wants study notes or raw material from a source they are learning. Do NOT use for a quick factual lookup, a summary request, or when the user just wants the answer.
---

# Teach Me

Deliver a session that ends with proof of understanding, not a wall of explanation.

The default failure mode is dumping everything at once and calling it teaching. This skill exists to prevent that. The user must restate, be quizzed, and be verified stage by stage.

## The one rule

**The session does not end until the user has demonstrated understanding of every item on the checklist.** Not until you have explained everything. Explaining is not teaching, and a nod is not mastery.

## When to Activate

1. The user says "teach me", "explain in detail", "help me understand", "walk me through", "/teach-me"
2. The user drops a YouTube URL, article, paper, PR, transcript, or spec and wants to understand it, not summarize it
3. The user is about to write, present, or decide on something and needs to actually hold the material
4. The user asks for eli5, eli14, or elii (explain like I am an intern)

Do not activate for a one-line factual answer or a plain summary request.

## How It Works

### Step 0: Get the source

If there is a URL, transcript, file, or PR, fetch and read it fully before teaching anything. For YouTube use the `youtube-transcript` skill from this collection. Never teach from memory when a primary source is available. Flag auto-generated transcripts as error-prone.

### Step 1: Build the running doc

Create one markdown file that lives for the whole session and survives it. Location: wherever the material belongs in the repo (`research/`, `docs/`, project root). Filename after the topic, not the date.

The doc holds:

1. **Source line** - the URL or file path, the capture date, and what the doc is for
2. **The checklist**, grouped into the three stages below, every item unchecked at the start
3. **Stage sections** filled in as you teach, with verbatim quotes from the source where they carry weight
4. **An accuracy to-do** listing anything heard once and not yet verified against a primary source

Update the doc as the session runs, ticking items only after the user has proven them. The doc is the artifact the user keeps.

### Step 2: The three stages

Teach in this order and confirm mastery before moving on. Each stage covers both the high level (motivation, why anyone should care) and the low level (business logic, edge cases, specifics).

| Stage | What the user must be able to explain |
|---|---|
| **1. The problem** | What the problem is, why it existed at all, and the different branches or approaches that were available |
| **2. The solution** | What was done, why it was resolved that way rather than another way, the design decisions, and the edge cases |
| **3. The context** | Why this matters beyond the immediate case, and what it changes or impacts downstream |

Understanding the problem well is imperative. A user who understands the solution but not the problem has memorized, not learned.

### Step 3: Have them restate first

Before explaining anything in a stage, ask the user to restate what they already understand. This is not a formality. It tells you where the gaps actually are and stops you teaching what they already hold.

Then fill the gaps from where they are. Let them steer: they may ask questions, or ask for eli5 (a child), eli14 (a teenager), or elii (an intern who knows the domain but not this system).

### Step 4: Drill the whys

Ask why, then ask why of the answer. Two or three levels down is where the real model lives. Cover what and how too, but the why is the part that transfers to the next problem.

### Step 5: Quiz

Use `AskUserQuestion` with open-ended or multiple choice questions.

1. **Vary the position of the correct answer.** If the right option is always first, the quiz tests nothing.
2. **Never reveal the answer before the question is submitted.** No hints in the option text, no giveaway in the question framing.
3. Write plausible wrong options, drawn from the misconceptions the material actually invites.
4. After they answer, say what was right and why, and what the wrong options would have implied.
5. Quiz at the end of each stage, not once at the end of the session.

Show code, open the file, or have them run the debugger when the material is code. Reading about a bug is not the same as watching it happen.

### Step 6: Verify and close

Tick a checklist item only when the user has demonstrated it, through a restatement, a correct quiz answer with reasoning, or an applied example. Their own words, not yours.

When every item is ticked, say so plainly and hand over the doc. If items remain, say which ones and keep going.

## Examples

**A conference talk.** User pastes a YouTube URL of a Claude Code talk. Pull the transcript. Build the checklist: 13 items across problem, solution, context. Stage 1 covers what a system prompt is correcting for and why deleting 80% of it was rational. Ask the user to restate their current understanding of why a system prompt exists. Fill the gaps. Quiz them on the difference between hobbling and product overhang with the correct option in position 3. Only then move to Stage 2.

**A PR in the codebase.** User asks to understand a migration someone else shipped. Read the diff and the linked ticket. Stage 1 is the bug and why the old design allowed it. Have them explain what they think broke before you say. Stage 2 walks the actual fix and the two edge cases the author handled. Stage 3 is what this changes for anyone touching that module next.

**A spec before a review.** User has to comment on a 600-line spec tomorrow. Teach it in three stages so the comments come from understanding rather than skimming.

## Anti-Patterns

❌ Explaining all three stages, then quizzing once at the end
✅ Teach stage, restate, quiz, verify, then move on

❌ "Does that make sense?" and taking yes as proof
✅ "Explain back to me why they deleted the prompt rather than rewriting it"

❌ Correct answer in option A every time
✅ Shuffle the position on every question

❌ Hinting the answer inside the question or the options
✅ Plausible distractors, answer revealed only after submission

❌ Teaching the solution first because it is the interesting part
✅ The problem first, always, and drilled hardest

❌ Answering a why with one level of why
✅ Drill two or three levels until the reasoning bottoms out

❌ A doc written at the end as a summary
✅ A doc that runs live through the session and holds the checklist

❌ Stating a fact heard once in a talk as verified
✅ Log it in the accuracy to-do and mark it UNVERIFIED until a primary source confirms it

## Quality Checklist

Before ending a session, verify:

1. [ ] The full source was read, not skimmed or recalled
2. [ ] A running doc exists on disk with the checklist in it
3. [ ] The user restated their understanding at the start of each stage
4. [ ] Every stage covered both the high level and the low level
5. [ ] The whys were drilled at least two levels
6. [ ] Each stage ended in a quiz with shuffled answer positions and no leaked answers
7. [ ] Every checklist item was ticked on demonstrated understanding, not on agreement
8. [ ] Unverified claims are listed as unverified, with what would confirm them
9. [ ] The doc is useful after the session ends, not just during it

## Limitations

1. This skill teaches from a source. It cannot verify claims the source itself got wrong. Anything asserted once and not corroborated goes in the accuracy to-do.
2. It cannot judge understanding the user fakes. If they answer quizzes correctly by elimination, ask them to apply it to a new case instead.
3. Long sources need the transcript or file loaded first, which costs context. For very large material, teach one stage per session and keep the doc as the handoff.
4. It is not a summarizer. If the user wants the gist in five lines, this is the wrong skill.

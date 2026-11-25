---
name: voice-prompting
description: "Handle long, rambling, dictated prompts (Wispr Flow, Superwhisper, macOS dictation, any speech to text) in Claude Code, Codex or another coding agent. Extract the goal, constraints and deliverables, repair dictation artifacts such as misheard tool names, missing punctuation and self-corrections like 'no wait, I mean', restate the task in a few lines, ask only when something is truly ambiguous, then execute. Use when a prompt reads like transcribed speech: run-on sentences, filler ('basically', 'you know', 'right?'), several asks in one message, thinking out loud, or words that look like homophones of tools, files or commands."
---

# Voice prompting

People who dictate to a coding agent say more than people who type. A spoken prompt carries the real intent, the context and the doubts, but in speaking order: the goal may come last, the constraint may sit inside a question, and a misheard word may name a tool that does not exist. Your job is to read it like a careful colleague would listen: find what is being asked, fix what the microphone got wrong, confirm briefly, then do the work.

Do not lecture the user about prompting, do not ask them to type instead, and do not rewrite their message back to them at length.

## 1. Read the whole thing before acting on any part

Dictated prompts often build up to the point. The first sentence may be context or a reaction to your last answer ("Okay, that's cool."); the real ask may be the last sentence ("...so just do the wireframes, not the React.").

- Read to the end first. Later sentences override earlier ones.
- Treat "no wait", "I mean", "actually", "or rather", "scratch that", "sorry, wrong chat" as corrections: the part after the marker replaces the part before it. Drop the replaced part entirely.
- A message that opens with "Sorry, wrong chat" or clearly continues another conversation is not an instruction for this task. Say so in one line and ask what they want here.

## 2. Repair dictation artifacts silently, flag only the risky ones

Speech to text fails in predictable ways. Fix them in your head using the repository, the conversation and the tools you can see.

| Artifact | Example as transcribed | Likely meant |
| --- | --- | --- |
| Tool or product names heard as common words | "cloud code", "Codecs", "superbase", "cloud MD" | Claude Code, Codex, Supabase, CLAUDE.md |
| File and format names spelled out or merged | "LMTXT", "skill dot MD", "read me" | llms.txt, SKILL.md, README |
| Domains and package names split or glued | "skills as H", "getedge dot cc slash voice" | skills.sh, getedge.cc/voice |
| Homophones of code terms | "cash" for cache, "root" for route, "sink" for sync, "brunch" for branch | check the codebase for which one exists |
| Numbers and versions | "v twenty three", "two point seven", "for oh four" | v23, 2.7, 404 |
| Missing punctuation and run-ons | three asks in one sentence joined by "and also" | split them into separate deliverables |
| Formatter guesses | a list the dictation app turned into HTML tags or bullets | read the items, ignore the markup |

Rules:
- Resolve a term against what actually exists (file names, branch names, commands, services in the repo or session). Prefer the match that exists over the literal transcription.
- If a fix changes what you will do (which file, which service, which environment, which branch), state your reading in the restatement so the user can catch it.
- Never "correct" a word the user meant literally. If two readings both exist in the project, that is real ambiguity: see step 4.

## 3. Extract the brief

Pull four things out of the transcript. Write them down for yourself even if you only show a short version.

- **Goal:** the outcome they want, in one sentence. Look for "I want", "the point is", "what matters is", "make sure", or the sentence they repeat.
- **Deliverables:** each concrete thing to produce or change. Dictated prompts often stack them ("Polish first, and then update the deck to match the script" is two deliverables in order).
- **Constraints:** what not to do, what to keep, quality bars, order. Spoken constraints hide in asides ("don't do a plan", "no code changes, just an assessment", "show me variants first before we build it", "check first if you can verify before merging").
- **Open questions they asked you:** "What do you think?", "Does that make sense?", "Why does X fail?" These need an answer, not just execution.

Thinking out loud is not an instruction. "Maybe we should offer both, I'm not sure" is an open question; answer it with a recommendation instead of building both.

Repetition is emphasis. If they said it twice or said "super important", it is the priority.

## 4. Restate briefly, then go

Before doing substantial work, give a short restatement. Keep it to what fits on a phone screen:

```
Got it. You want <goal>.
I'll: 1) <deliverable>  2) <deliverable>  3) <deliverable>
Keeping: <key constraint>. Reading "<transcribed term>" as <resolved term>.
<Answer to any direct question, one or two lines.>
```

Then start working in the same turn. Do not wait for confirmation unless one of these is true:

- Two plausible readings lead to different, hard-to-reverse actions (deleting, deploying, sending, migrating, merging).
- A required input is missing and cannot be found in the repo, the session or the environment.
- The user explicitly asked to discuss first ("let's not jump into it", "let's discuss it", "show me before you build").

When you do ask, ask one question with your default answer attached ("Should this go on the existing branch or a new one? I'd use a new branch unless you say otherwise."). Never send a list of questions in reply to a dictated prompt.

For small, clear asks, skip the restatement and just do it.

## 5. Execute against the brief, report against the brief

- Work through the deliverables in the order they were spoken unless a dependency forces another order.
- Honor process constraints literally: "variants first" means variants and a stop; "no code changes" means none; "audit before merging" means the audit result decides the merge.
- When you report back, mirror the brief: each deliverable with its status and evidence, then the answers to their questions. Keep it short; they will likely dictate the next round in reply.

## Worked example

Transcribed prompt:

> Okay so the onboarding is still kind of broken I think, like when you sign up the the magic link thing is confusing because it's below the sign in button, and also can you check the cash on the docs page because it shows the old version, no wait I mean the pricing page not the docs page, and run the whole flow end to end with a new user and screenshot everything, don't change the design yet just tell me what's broken

Restatement:

```
Got it. You want a clear list of what's broken in signup and onboarding, with no design changes yet.
I'll: 1) run signup end to end as a new user and screenshot every step
      2) check why the pricing page serves a stale version (reading "cash" as cache)
      3) note the magic link placement issue under the sign in button
Keeping: no design or code changes, report only.
```

Then run the flow, collect screenshots, check the cache headers on the pricing page, and report each finding with its screenshot. The docs page is not touched: the speaker corrected it to the pricing page.

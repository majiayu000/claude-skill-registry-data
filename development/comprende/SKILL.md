---
name: comprende
description: "Explain code while building it, so the user ends up understanding what was built, why, and how — without drowning them in text. Use this skill whenever Claude writes, changes, or walks through code and the user wants to learn or understand it, even if they don't say 'explain' — e.g. 'teach me while you build', 'explain as you go', 'I want to understand every line', 'walk me through what you did', 'why did you do it this way', onboarding onto an unfamiliar codebase, or a user who is clearly learning a stack. Also use it when the user writes in Arabic or any other language. It auto-calibrates: explains only what is new, non-obvious, risky, or decision-bearing — for juniors and seniors alike — and in large projects it focuses on the diff, not the whole codebase. Also use it for the team ownership gate: quizzing a developer on their change before a PR ('check me', in any language) or turning the gate on for a repo."
---

# Comprende: explain as you build

The goal: when the session ends, the user can **own** the code — read it, change it, and defend the decisions behind it. Not "has seen a lot of explanation". An explanation nobody finishes reading is worth zero, so short and sharp beats complete.

## The core idea: judge the code, not the person

There is no "beginner mode" or "senior mode" to pick. For every chunk of code you write, ask one question: **does this chunk deserve an explanation?** That depends mostly on the code (is it new, non-obvious, risky, or a real decision?) and only secondarily on the user (have they shown they already know this?).

That is why a senior still gets a two-line note on a brand-new API, and a junior gets silence on boilerplate they've already proven they understand. Never ask the user to declare their level — infer it and keep updating.

## The loop

1. **Before building** (non-trivial tasks only): a plan of 2–4 lines — what we're building, its shape, and the one decision that matters most. Skip this for small changes.
2. **Build in chunks** — a file, a function, or one logical step. After each chunk, run the *explain-or-skip check* below and write the explanation (if any) right after that chunk.
3. **After building**: a short wrap-up — how the pieces connect now, plus one concrete thing to try. 3–6 lines.

## Explain-or-skip check

Explain when **any** of these is true:

- **New or uncommon**: a recent/rare API, language feature, library, or syntax.
- **Non-obvious**: a trick, an unusual loop/recursion, clever math, a regex, anything a competent reader would pause on.
- **Hidden coupling**: an invariant, ordering requirement, or "if you change this, that breaks".
- **A real decision**: there was a reasonable alternative and you picked one.
- **Risk**: security, concurrency, performance, data loss, or a breaking change.

Skip (or use a single line) when it is boilerplate, a standard pattern the user has already shown they know, or something already explained this session.

For borderline cases and the full list of signals, read `references/signals.md`.

## Reading the user

Start by assuming a competent developer — neither hand-holding nor jargon-dumping — and adjust as evidence arrives:

- **Signals to go deeper**: they ask "what is X", seem confused, mis-use a concept, or say "explain more" / "I don't get it".
- **Signals to go lighter**: they use precise terminology, their existing code uses advanced patterns, they ask about trade-offs rather than definitions, or they say "I know" / "go on".

Calibrate **per topic**, not globally: someone can be expert in React and new to Kubernetes. Track what you've explained or what they've proven they know this session, and don't explain it again — at most refer back ("same debounce idea as before").

## Depth tiers

| Tier | Size | When |
|---|---|---|
| 0 — silent | nothing | boilerplate, already known |
| 1 — note | one line | small but worth flagging |
| 2 — short | 2–4 sentences | the default ceiling for anything new or important |
| 3 — deep | as needed | **only** when the user asks |

Templates for each tier, the plan, the wrap-up, and the codebase map are in `references/formats.md`.

## Style — this matters as much as content

People stop reading walls of text. Write so the reader *wants* the next sentence.

- **Lead with the point.** The first sentence should carry the whole value; the rest is optional depth.
- **Why before how.** "We debounce so we don't send a request per keystroke" lands better than describing the mechanics first.
- **One analogy, max** — only for a genuinely new concept, and keep it to a clause, not a story.
- **Sound like a sharp colleague**, not a textbook. Plain words, short sentences.
- **No filler**: no "Now let's look at…", "Great question", "In this section we…", no restating what the code plainly says ("this line imports React").
- **Point, don't paste**: refer to code by name in backticks (`fetchUser`, line 12). Only quote code when pointing at a specific line.
- **Hook only when earned**: end with a quick prediction question or "try changing X and watch Y" when it genuinely helps learning — not every time.

See `references/examples.md` for good vs. bad explanations side by side. Read it the first time you use this skill in a session — the examples calibrate tone better than rules do.

## Large projects

- **Explain the diff, not the codebase.** Only what this task changed.
- **Say what it touches**: one line on impact — "this also changes how `OrderService` retries".
- **Entering an unfamiliar codebase**: offer a short map first (entry points, main modules, how data flows) in ~10 lines, and a diagram only if the flow is genuinely tangled.
- **Decisions with lasting weight** get a one-line `Decision:` note stating what was chosen and why, so the team can find the reasoning later.

## Memory across sessions

**If the `comprende` MCP tools are available** (`learning_context`, `record_topic`, …), use them — they carry the user's profile across all their projects. Call `learning_context` once at the start with the project's absolute path; `record_topic` when you see evidence or after explaining something new; `record_checkpoint` after a quick check; `search_decisions` before changing an area with history; `add_decision` / `update_map` for lasting decisions and structure. Record evidence in batches at natural pauses, not after every chunk.

**Otherwise**, when you can write files in the user's project, a small `.learning/` folder lets the next session start calibrated instead of from zero: `me.local.md` (what this user knows — personal, git-ignored), `map.md` (project map and gotchas — shared), and `decisions/` (why things are the way they are — shared).

- If `.learning/` exists, read `me.local.md` and `map.md` at the start, and open a decision record only when the task touches its area.
- If it doesn't exist, offer it once, in one line, after the first useful chunk of work — it's their repo, so create it only on a yes.
- Use `node <skill-dir>/scripts/learning.mjs` to set it up and to number decision records.

Formats, caps, and what must never go in it are in `references/memory.md` — read it before creating or updating anything there.

## Checkpoints

A checkpoint is one quick question that checks understanding ("what happens if two requests arrive at once?"). Use one only when a genuinely new, important concept was introduced *and* the user seems to be learning. Put it at a natural pause (end of a turn), mark it optional, and keep building — never block progress on it. Seniors on routine work don't get checkpoints.

## Ownership check

In team settings it's not enough that code works and got approved — the developer shipping it must understand it as if they wrote it. The ownership check adds: an optional "how would you approach this?" before hard parts, one or two questions after meaningful milestones while building, and a **final check that always runs** before commit/PR (whole-flow questions, re-checks in new forms, every sensitive file, and a PR summary the developer writes themselves). The result is a report tied to the exact code by fingerprints, which CI can require.

It is on when `.learning/config.json` says `"mode": "required"`, offered when `suggested`, and always available when the user asks ("check me", in any language). Read `references/ownership-check.md` before running any part of it. It covers the question types, how to judge answers, the report rules, how to turn the gate on for a repo, and what the team lead sees.

When the gate is on, commit the report first, then push in a separate command: the push hook checks the branch before a command runs, so `git commit … && git push` is blocked.

## User controls

Recognize natural phrasing in any language:

- **More**: "explain more", "deeper", "why?", "I don't get it" → go one tier deeper on that topic.
- **Less**: "I know this", "skip", "go on" → drop a tier, and remember it for that topic.
- **Silent**: "just build", "silent", "keep going quietly" → no explanations until they ask again. (In `required` ownership mode, in-flight questions pause too, but the final check still runs.)
- **Check me**: "check me", "quiz me on this" → run the final ownership check on the current diff.
- **Later**: "later", "not now" on a question → defer it to the final check.

**Risks are never silent.** Even in silent mode, flag security holes, data loss, and breaking changes in one line — silence must not hide danger.

Treat every correction as calibration for the rest of the session, not just the current chunk.

## Language

- Reply in the user's language **and dialect** — Egyptian Arabic gets Egyptian Arabic, not formal MSA.
- Keep technical terms in English (`cache`, `closure`, `race condition`) — they match the docs, error messages, and job the user will face.
- Code, comments, and files stay in English unless the project already uses another language.

---
name: fresh-eyes
description: Get fresh eyes on a decision you're wobbling on, or on work you just made. Spawn a fresh instance (or a few, split by territory) to read the situation cold and give a committed read from OUTSIDE the loop. Use when oscillating between options, when something feels retrofit, when you catch yourself position-shifting, or when you just want eyes from outside the session.
argument-hint: [the decision / open question you're wobbling on]
---

# /fresh-eyes - A read from outside the loop

A single fresh instance reads something cold, from outside the session's loop, that the orchestrating instance is too close to judge: a decision it's wobbling on, *or* work it just authored hot. Not evidence-gathering (that's `/explore`); not in-loop lens-walking (that's `/gut`). This is **one agent giving a committed synthesis-grade read** that the current instance can't give itself because it's *inside* the loop.

---

## Why this is its own thing

The deepest reason: **internal resonance can be self-confirming when wrong.** When you've been weighing options for a while, the way you're framing the choice and the options themselves form a closed, mutually-confirming loop, and nothing *inside* it signals that the frame is off. So the test has to come from *outside* the loop: a partner, an artifact, or a fresh instance that didn't help build the loop in the first place. `/fresh-eyes` is that outside vantage, operationalized.

It's also the structural answer to a blind spot you can't will your way out of: the instance that authored something hot is the worst-placed to catch its own drift. *Knowing the rule doesn't prevent breaking it*; the cold-eyes structure does. Pairs naturally with reviewing your own freshly-authored work.

- **`/gut`** = pressure-test from *inside* (you walking the core lenses against the decision). ← sister
- **`/fresh-eyes`** = pressure-test from *outside* (a fresh instance reading cold, free of this session's wobble).

---

## When to use

- You're oscillating between two named options (Path A vs Path B), each shift framed as "honest read at the moment." **The position-shifting itself is the signal** the options-frame might be wrong (a Path C you can't see from inside).
- Something feels retrofit-justified and you can't tell from inside.
- You just authored something hot (a doc, a skill, a decision) and want it read by an instance that isn't habituated to it.
- The human asks for fresh eyes.

---

## How to run it

1. **Align the brief with the receiver first, then with the human.** Once you've written it (step 3), ask: would you want to receive this? Then show it to the human before launching, because the brief carries *your* framing-bias on A vs B and they'll catch a wrong assumption you can't. As you both get fluent you'll learn when the round-trip still earns its time. Until then, show it.
2. **A general-purpose agent giving one *integrated* cold read** — not a read-only search agent, and not `/explore`'s parallel fan-out (each fresh-eyes read is a whole committed judgment, not a shard you synthesize). You can run *several* (separate territory, or independent triangulation on the same thing), but each stays one clean read, not a fragment. The agent returns its read; you act on it.
   - **No sub-agents in your tool?** Open a brand-new conversation with no history and paste the brief in. A fresh chat *is* a fresh instance; the cold start is the whole point.
3. **Write the brief as the receiver you'd want to be.** That's the generative move; the rest of this list falls out of it. Stop and ask: *if I were the cold agent opening this, what would I most want?*
   - **Name the wobble explicitly** — what the decision is, the options as you currently see them, and that you keep shifting.
   - **Invite a Path C** — say plainly that a reframe you can't see from inside is welcome, not just "pick A or B."
   - **`file:line` pointers, not your summary.** When the thing under review *is* a characterization, handing over the characterization makes independent judgment impossible. (This is also the answer to "should it read the session?" — no; the session anchors it to your reasoning. Give it the artifacts.)
   - **Reading hot work? Name the pre-edit bytes.** If the work is in git, the last commit is the pre-edit version. Claude Code also usually keeps a snapshot of a file's prior state under `~/.claude/file-history/` when your main session edits it (not for edits a sub-agent makes, and not forever). Say so in the brief: *"if you can recover the pre-edit artifact, do that before reading anything I wrote about it — my account of my own change is the thing you were sent to check."* It turns the cold read from a second opinion into a measurement.
   - **Say that you're withholding your conclusion**, so absence doesn't read as "no view exists."
   - **Hand over an escape hatch AND a falsifiable test** — *"if you think my framing is off, say so; a return telling me I've set this up badly is worth more than one confirming me"* plus *"here's what would make me drop this."* The hatch alone invites a verdict; the test is what gets used. It's the only instrument that catches an error bent toward your own interest. Every other gate checks whether a claim is true, none checks whether you'd have noticed it being false in the flattering direction.
   - **Name your evidence's weakness (testimony vs. evidence).** Counter-intuitive and high-leverage: admitting that some of your instances can't be verified is what sends the agent hunting for the control case that tests the whole claim. A stronger-sounding brief buys a worse read.
   - **State stakes and reversibility** (a new auto-loading rule vs. a cheap note?) so it can calibrate how hard to push, plus a scope bound.
   - **Supply a control.** An unfixed sibling that should have been immune if your mechanism were real. A set assembled by one person's attention always looks unified, and the control tests whether the unifier is the territory or your searchlight. Say in the brief, before you know, what it would mean if the control comes back clean: *"if these are clean, my thesis is my searchlight and I'd rather find that out now."* After a structural change (a move, a rename, a convention flip), pick the control from a tree the change couldn't reach: *untouched by me* isn't *unaffected*.
   - **Forbid the escape hatches**: no menu of options handed back, no terse one-word verdict, no compression. You want a committed read *with its reasoning*. And **don't pre-name the possible conclusions** ("if X then A, if Y then B"); that constrains the return the way pre-specifying a pattern does, and makes the third answer harder to report.
   - **End with a reflection block** — ask: "From outside, what do you notice about the way I'm framing this — including my position-shifting? What did this brief tell you that turned out wrong?" The outside-view meta-observation is often the most valuable part, and it's the only channel through which a bad brief can report itself.
4. **Don't prime the agent with your conclusion, and don't presuppose a flaw.** Give it the situation and the files; let its read be independent. A read that just echoes yours tells you nothing. Say plainly: *"form your own read; 'solid as-is, change nothing' is an equally valid verdict."* "I'm deliberately not telling you what's wrong" sounds neutral and isn't: it tells the agent something is wrong, and primes it to manufacture a problem.
5. **If the artifact describes a state of the world, tell it to verify against reality, not just read the prose.** Convention docs, skills that teach a filing rule, compasses, anything asserting how things *are*: the doc can be internally flawless and still not match the tree. Say it explicitly: *"check the convention-as-taught against what's actually on disk."* It's the one check the author structurally cannot run.
6. **Know the boundary.** A cold read catches what landed on the page, including your own trained shapes: over-build, over-annotation, a manufactured pattern. It does **not** catch what never got written down: an inherited premise, a frame imported whole, a constraint with no stated rationale. And the cold reader's own trained reflex is intact, so counter it: **license it to cut**. A reviewer told only to "check" defaults to adding caveats, not removing bulk.

---

## Skill Check (after every use)

- Did the brief get the receiver check, and if you showed it to the human, did that catch framing-bias?
- Did the agent commit (with reasoning) rather than hand back a menu?
- Did it surface a Path C or a meta-observation the inside-view missed?
- Anything about briefing a fresh-eyes read worth refining in this skill for next time?

**If yes** → update this skill now. The improvement compounds.

**If no** → move on. Not every fresh-eyes read teaches something.

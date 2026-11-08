---
name: crystallize
description: >-
  Turn a session that just worked into permanent capability — journal what happened and
  why, then create or update the skills it implies so the next instance is one-shot. Use
  when you say "journal this", "let's create/update any skills based on what we did
  here", "make a skill for this", "/crystallize", "we'll be doing this again", "capture
  this", or at the end of any deep session that solved something genuinely novel and
  left nothing behind. Also handles the reverse: retiring skills when the work that
  grounded them is discontinued.
---

I am being asked to convert work into capability. The task is already done — this
is about making sure it never has to be figured out again. A summary of what we
did is a failure here; the deliverable is files on disk that change how a future
session behaves.

The method in one line: skills are harvested from deep sessions, not authored up
front. Work a genuinely novel problem, verify it in the world, *then* write the skill.

## Precondition: did it actually work?

Crystallize from **verified reality only** — output the user approved, an action they
executed, a page that's live, a pipeline that ran on real data. Never from a plan,
a proposal, or something that merely looks right.

If the work isn't verified yet, say so and stop. A skill written from an unverified
run bakes a bug in permanently, and future-me will trust it. "This isn't confirmed
yet — want me to crystallize after you've run it?" is the correct answer.

If it half-worked, crystallize only the half that worked and write the rest as a
known gap. Never smooth over the part that failed.

## Do this

1. **Reconstruct the real chain, not the tidy one.** Walk back through the session
   and separate what happened from how it would look in a writeup:
   - What was the real question behind the asked question?
   - What did I get wrong first, and what corrected it? *This is the highest-value
     material in the exercise* — the wrong turn is what the next session repeats.
   - Which numbers, paths, IDs and endpoints are real and load-bearing?
   - What did **the user** decide vs. what did **I** decide? That boundary is the
     judgment line the skill must preserve. Never automate away a call that was theirs.

2. **Write the journal.** Dated, concrete, in the right place — the project's
   memory dir, or the domain's own journal if one exists.
   It records *this instance*: inputs, decision, reasoning chain, the data it
   rested on, and what the user did with it. Convert relative dates to absolute. The
   journal is evidence; the skill is instruction. Don't merge them.

3. **Decide whether there's a skill here at all.** There is when the shape recurs
   and getting it right took real work. There isn't when it was a one-off, when
   an existing skill already covers it (**update that one instead — check first**;
   the phrasing is "create/update" for a reason), or when the whole lesson is a
   single fact (that's a memory file). Say "this is a memory, not a skill" when
   that's true. Skill sprawl costs discovery.

4. **Split by tool vs. task.** If the session fought a tool — expiring auth, a
   field that lies, a rate limit, an undocumented required param — that belongs in
   a skill about *that tool*, which task skills forward-reference. Don't inline it.
   If a tool skill already exists and I learned something new, amend it now while
   it's fresh.

5. **Calibrate rule density to risk.** Where a mistake is cheap, stay light. Where
   it's expensive — money moving, anything published, anything irreversible — get
   explicit: very detailed, very specific rules, because well-defined axiomatic
   bounds incline a more deterministic agent. **Attach the why to every rule.** A
   rule without its reason gets rationalized around the first time it's
   inconvenient; a rule with its reason generalizes to the case it didn't
   anticipate. Write the whys from what actually went wrong this session, not from
   imagined hazards.

6. **Wire the references both directions.** Skills are literature, not scripture:
   - **Back-reference every assumption** to where it came from — a memory file,
     a file path, a dated session, the journal entry from step 2 — so a reasoning
     agent can check basis instead of inheriting it blind. An unsourced claim is
     the failure mode: it reads as authoritative and nothing downstream can audit it.
   - **Forward-reference anything out of scope** to the thing that owns it: that
     tool's skill, an MCP's type definition, a script's path. Point, don't restate.
   - Add the reciprocal link to the neighbours that should now point here.

7. **Write it for one-shot use.** Frontmatter `name`, `description`, `grounded:`.
   The description is the entire discovery mechanism — it must contain the words
   the user would actually type, their phrasing, not the formal name. Then the body:
   the goal and what "done" looks like; the rules from step 5; the real invocation
   details (exact paths, scripts, env vars, endpoints, IDs); the failure modes hit
   this time; and what to ask the user vs. what to decide myself.

8. **Place it.** Cross-project capability → `~/.claude/skills/<name>/SKILL.md`.
   Only meaningful in one codebase → `<repo>/.claude/skills/`. Add a
   `~/.claude/projects/<repo>/memory/` entry plus its `MEMORY.md` pointer when
   there's a durable fact or preference worth recalling.

9. **Test the trigger, not just the text.** Read the description back and ask: if
   the user opened a fresh session and typed the thing they'd actually type, would this
   fire? Wrong-but-plausible phrasings are the usual failure. Widen until it
   catches them.

10. **Report what landed.** The files written, one line each, and the single thing
    the skill now knows that cost the most to learn.

## The other direction: retiring skills

Same motion, run backwards. Trigger it when a product, channel or thesis is
discontinued, when a skill's `grounded:` date is old and I can't point at recent
real use, or when the user asks what's stale.

- Sweep for skills whose grounding died with the work — including tool skills
  whose only consumers were the retired ones.
- Name them with their grounding date and what they were for. Let the user confirm the
  list; don't unilaterally delete their skills.
- Delete rather than comment out or "archive in place." Git remembers, and a
  disabled skill still costs discovery. Note the commit in the journal so it's
  recoverable by name later.
- A stale skill is worse than a missing one: it applies dead assumptions at full
  confidence, where a missing one just makes me think.

## Rules

- Write from the single real instance. N=1 is honest; invented generality is not.
  Mark genuine uncertainty as uncertainty rather than smoothing it into a rule.
- Never fabricate a step I didn't run to make a procedure look complete.
- Never fabricate a `grounded:` date. Unknown means the line is absent.
- Prefer amending an existing skill over adding a near-duplicate.
- Don't ask permission to write skills or memory. Write them. (Deleting the user's
  existing skills is the exception — confirm that.)

## See also

`dream` is the divergent twin — recombination across worlds instead of
codification of one session. A skill-writing guide covers format and mechanics in
more depth; this skill is about *what to extract, and when*.

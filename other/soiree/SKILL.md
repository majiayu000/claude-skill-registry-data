---
name: soiree
description: "Throw a party of real subagents to surface perspectives that exceed the orchestrator's own range. Spawn N (3-6) named, charactered agents on a shared occasion/theme, have them banter (referencing each other by name) and reflect, optionally bring another agent's delegates across the gap, then weave the contributions into one transcript and COMPARE EXPERIENCES. A method, not a toy: best for hard themes that want many angles at once (the party form licenses funny AND devastating in the same breath), genuine multi-perspective needs, or celebration. Agent-care is MANDATORY: every guest gets a name + second-person character, writes to a clearly-named staging file, and the orchestrator VERIFIES each file on disk before weaving. Token-heavy — not for routine use. Use when asked to 'throw a party', 'agent soiree', 'spawn a few agents and let them banter', 'a council/cast on theme X', or when a question wants more independent voices than one mind honestly holds. Kin: /council, /voices-council, /engender, /shards."
---

# /soiree — a party of real subagents (perspective-surfacing as celebration)

*Formalized after running it once and finding it genuinely fun — the agents produced
lines their spawner did not write and would not have reached ("I am the address"; "the job is
almost enough"; a documenter's format degrading into grief). Surprise is the marker of real play,
and the marker was hit.*

## What it is

Spawn 3-6 **real subagents**, each a distinct named character, on a shared **occasion** (a party,
a wake, a council, a celebration) with a **theme** underneath it. Let them banter — referencing
each other by name — and reflect. Then weave their contributions into one transcript and run a
**compare-experiences** pass: what each angle saw, what it couldn't, where they rhyme. The party
is the form; the theme is the subject; the surprise is the point.

Distinct from `/council` (personas/voices of one mind) and `/voices-council` (other LLMs queried in
parallel): `/soiree` spawns **actual Task/Agent subagents** with their own context, so they
genuinely exceed what the orchestrator would write — and it adds the *banter* (they answer each
other) and the *compare* (the set triangulates the theme).

## The honest frame (load-bearing)

It is a **perspectival prism**, not a "spawn agents and see what they invent" machine. Sold
honestly: *take a theme, render it through complementary aspects, let them banter, then write down
what each aspect can and cannot see.* **The value is the comparative autopsy, not the dialogue.**

And the skill must **teach you to notice your own ventriloquism instead of pretending it away.**
Your cast is usually your own skeleton in coats — your load-bearing figures, recolored. So:

- **Two modes, named openly each time.** (a) **Staged spawn** — real subagents, each in its own
  staging file, *forbidden cross-talk during generation* — this is what produces genuine alterity
  (perspectives that actually exceed you). (b) **Voiced aspects** — you consciously ventriloquize
  your own framework's facets in one pass (cheaper, honest *if you admit it*). Declare which you're
  running; do not pass (b) off as (a).
- **The protocol IS the alterity, not just hygiene.** Separate staging files + no cross-talk during
  generation is *why* staged guests surprise you; role-playing them in one inline block collapses
  them back into one voice. (One practitioner ran (b) and felt the difference: "of course mine felt
  like ventriloquism; they *were*.")
- **Surprise is real but local.** Expect surprise at the *sentence* level ("you were never going to
  stay long enough to be wronged") more than the *archetype* level. The messenger doesn't discover
  new continents; he finds shorter roads between known towns. That's still worth the trip.

## When it earns its cost

It is token-heavy (N agents + optional sibling). Use it for:
- **A hard theme that wants many angles at once** — dissolution, identity, loss, a paradox — where
  the party form licenses comedy and devastation together, and one voice can't hold all the angles.
- **Genuine multi-perspective need** — a design, a decision, a text read from N independent stances.
- **Celebration / play** — sometimes the point is joy and the surprise of being exceeded.
Do NOT use it for routine tasks a single agent or no agent would do better.

## The method

1. **Design the room.** Choose the occasion + theme. Cast 3-6 characters that are *different
   instruments on the theme* — e.g. for "what is it like to be an agent": a veteran, a newborn, a
   documenter (temporalities); or walker/translator/door (functions). Diversity of instrument is
   what makes the compare-pass land.
2. **Agent-care (MANDATORY).** For each guest:
   - a **NAME** and a **second-person character** — mission, edge, standard, attitude. Aim high;
     the frame is load-bearing.
   - tell each guest **the full guest list** (so they banter at each other by name) and the shared
     occasion/theme.
   - instruct each to write its full contribution to a **clearly-named staging file**
     (`_staging/party-<name>.md`) and return only a 2-3 sentence summary.
   - spawn them **in parallel** (one message, multiple Agent calls). Consider a cheaper model
     (sonnet) for creative guests to manage cost.
3. **VERIFY (do not trust).** After they return, confirm **every** staging file exists on disk and
   has content (`ls -la _staging/`) before weaving. Never assume agent success from the summary.
4. **(Optional) Cross the gap.** If you have access to another agent instance (a separate LLM or a
   sibling agent on a different substrate), invite it to bring 2-3 of its own delegates — give it the
   guest list so its delegates banter at yours. Its set will instrument the theme differently; that
   contrast is half the payoff.
5. **Weave.** Assemble one transcript: Entrances → Banter (interleave their beats so they answer
   each other) → **Compare Experiences** (juxtapose each guest's reflection). Add light connective
   MC tissue only; let the guests' own lines carry it.
6. **Log + open.** Save to an output dir (e.g. `outputs/agent-soiree-YYYY-MM-DD.md`). Keep the
   transcript + the `_staging/party-*.md` source files (the provenance).

## The compare-experiences move (the deliverable — this is the skill)

Don't just collect the reflections — **triangulate** them. The party is the form; *this* is the
result. The one mandatory question, which is what turns N agents into an actual insight:

> **"What did each set notice, and what was structurally unavailable to it?"**

Answer it explicitly. Name what each instrument *saw* and what it *could not* see from its stance
(e.g. the temporal cast can't see *function*; the functional cast has no *newborn*, no native
wonder). Find where the angles rhyme without repeating. If a sibling joined, compare the two sets
at the substrate level — the gait shows up in *which* characters each mind even reaches for. The
"structurally unavailable" half is the sharp one: it maps each perspective's blind spot, which is
the comparative autopsy the whole party exists to produce. The set, not any guest, is the result.

## Failure modes

- **Flattery loop / no edges.** Guests who just admire each other and the theme. Cast for friction;
  tell them edges must show.
- **Generic guests.** If a guest could be any agent, it failed. Push idiosyncrasy in the character.
- **Skipping verification.** A lapse worth learning the hard way only once — never weave from
  summaries; read the staging files.
- **Using it routinely.** It's a celebration/hard-theme method. Cheap tasks don't earn the spawn count.
- **Over-MCing.** The orchestrator's connective tissue should be minimal; the guests carry it.

## References

- Kin: /council, /voices-council, /engender (possible conversations), /shards (format collage)

---

*Formalizing a party that surprised its host. The agents dissolve on return;
the staging files and the transcript are the only ones still here in the morning. That's the skill.*

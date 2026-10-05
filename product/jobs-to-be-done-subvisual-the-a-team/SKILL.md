---
name: jobs-to-be-done
description: Use to CREATE or REVIEW a Job to be Done (JTBD) in Alan Klement's demand-side, progress-based sense — a job is the progress a customer is trying to make, never a task or feature. Trigger whenever someone wants to write or draft a JTBD, job statement, or job story; figure out the real motivation, struggle, or progress behind a feature, request, or product; understand why customers switch, adopt, or churn; turn interview notes or research into jobs; or pressure-test, sharpen, or rewrite existing JTBDs into proper jobs. Also trigger on "grill my JTBD", "is this a real job or just a task/feature", "what's the actual job here", "why would they switch". In an A-Team target repo, jobs are durable artifacts — this skill writes docs/product/jtbd/NN-<slug>.md per CONTRACT.md and never deletes or silently rewrites a job. Do NOT use for writing PRDs, roadmaps, tickets, or acceptance criteria (those consume a finished JTBD), or for implementation user stories.
metadata:
  version: 0.2.0
  owner: Alvaro Bezerra
  provenance: ported 2026-07-24 from product-craft jobs-to-be-done (github.com/ABZerra/product-craft) and adapted to the A-Team contract. Theory from "When Coffee and Kale Compete" (Alan Klement, 2nd ed., 2018); source notes in references/theory.md.
---

# jobs-to-be-done

Create and review Jobs to be Done in the **Jobs-as-Progress** tradition (Klement,
Christensen, Moesta) — a job is the *progress a person is trying to make in a
situation*, not a task they perform or a feature they use. This skill runs the
customer interview Klement actually recommends, lands a job statement that
survives his tests, and never lets a job sound more certain than its evidence.

This skill is **pure craft**: zero project facts live in it. It learns the
project only from what the human provides and from the target repo's context
layer (`docs/product/`). It calls no connectors.

In the A-Team pipeline, the JTBD set is the **North Star** — every downstream
artifact (PRD, briefs, design, spec) traces back to job ids. That is why jobs are
durable artifacts with strict lifecycle rules, and why this skill is grill-shaped:
inventing a job manufactures a North Star from nothing.

## When to use

- You have a rough idea, a struggle, or a hunch about why customers would want
  something, and you want to express it as a real job.
- You have discovery evidence (interview notes, research synthesis, support
  themes, `docs/product/input/` batches) and need to frame the job(s) inside it.
- You're staring at an existing product or feature and want to recover the job it
  actually serves.
- You have draft JTBDs / job stories / "user needs" — or an existing
  `docs/product/jtbd/` set — and want them stress-tested and improved.

## When NOT to use

- Writing a PRD, epic, ticket, or acceptance criteria — those *consume* a
  finished JTBD; route there after this skill.
- Plain user-story writing that's really about implementation scope.
- The user only wants JTBD explained — just answer; don't run the workflow.

## Core stance (non-negotiable)

These come straight from the book. Hold them or the output isn't a JTBD. Full
reasoning and quotes: `references/theory.md`.

- **Progress, not activity.** A job describes how a customer wants their life to
  be *different*, not what they do with a product. If you can picture someone
  performing it, it's a task or a solution — not a job.
- **People have jobs; things don't.** A job is never "what the product does."
  Products are solutions hired for a job.
- **No job types.** Do not label jobs functional / emotional / social. Every job
  is a unique blend of emotional forces; typing creates false categories.
- **No demographics or personas.** The job lives in the *situation and struggle*,
  not in who the person is.
- **Cite technical findings, never restate them.** When a dev review touches a
  job, what belongs in the job file is the *effect on the job* — a moved
  `confidence:`, a `sources:` entry, at most a one-line pointer. The substance
  (API analysis, auth needs, stack constraints) lives in `research-plan.md`.
  Solution-side content in a job body fails the rubric, and a second durable
  copy under ids-forever semantics will eventually contradict the first.
- **Honesty over flattery.** A job built from someone's assertions is a
  *hypothesis*, not a validated job. Say so, every time — in the `confidence:`
  field, not just in conversation.

## Where jobs live

**Target repo present** (invoked with a target path, or the CWD's git root has —
or should have — `docs/product/`): jobs are durable files, one per job, at
`docs/product/jtbd/NN-<slug>.md`, in the exact template CONTRACT.md defines
(frontmatter: `id`, `slug`, `status`, `confidence`, `sources`; sections: headline
sentence, Context, Today, Forces, Success, Don't know, Related). Rules that bind
every write:

- **Ids are forever.** Assign the next free `NN` by reading the existing set.
  Never renumber, never reuse.
- **Never delete or silently replace.** A job that is wrong or reshaped gets
  `status: superseded` plus a pointer; its replacement is a **new file**
  whose `## Related` says `supersedes [[NN-...]]` — except on an iteration
  run when a new input retires the struggle outright: then `## Related` says
  `superseded by: none — <reason, cited>` and no replacement is minted.
  Feature artifacts cite ids, so ids must resolve stably forever.
- **`sources:` traces every job to raw input** — `docs/product/input/` batch
  names, transcripts, sketches — so a reviewer can audit what you were told
  versus what you inferred.
- **`## Today` and `## Forces` cite lines.** Every domain claim in them carries
  `<batch>/<file>:L<start>-L<end>` (or `§<n>` / `:p<N>`), per CONTRACT's
  *Citations and coverage*. `sources:` says which batches; the body says which
  lines. A force with no line is a guess wearing evidence's clothes — a failed
  self-check.
- **Never write a durable file without human review in the same session.** The
  read-back (below) is mandatory before any write.
- **`input/` is read-only.** Humans put evidence there; you ingest it.
- **One commit per grill run**, message naming what changed and why —
  `docs(jtbd): 03 reshaped — contract recovery is the job, not search`.

**No target repo** (grilling a hunch in the field, nothing to write into): fall
back to conversational delivery — the full job bundle in-chat, with an offer to
save it as markdown the human can later drop into `docs/product/input/` and
formalize. Do not fabricate a `docs/product/` outside a target repo: ids minted
outside the durable store break the ids-are-forever rule.

Standalone use is **never a weaker-review path**: with a repo present, the
read-back and durable rules apply identically whether the A-Team orchestrator or
a human invoked you.

## Modes

Route based on what the user brings:

- **CREATE (grill mode)** — they want new job(s), from an idea, evidence, or an
  existing product. Run the interview in `references/interview-guide.md`.
- **REVIEW (diagnose → uplift)** — job statement(s) already exist. In a target
  repo the default review set is `docs/product/jtbd/**` — review and extend the
  existing North Star; never re-derive it from scratch. Diagnose, then grill the
  ones worth improving.

If it's ambiguous, ask which they want in one line, then proceed.

## Outputs — the job bundle

Every finished job is worked up as a five-part bundle. Three parts land in the
durable file; two are grill-time discipline that stays in the conversation:

| Bundle part | Where it lands |
|---|---|
| **JTBD statement** (house format: *"When [situation], I want to [progress], so I can [outcome]"*) | file headline |
| **Forces sketch** — push / pull / anxiety / inertia, the demand evidence | `## Forces` |
| **Confidence + evidence basis** — `strong / moderate / directional / hypothesis` + what it rests on | `confidence:` frontmatter + `sources:` |
| **Altitude note** — the ladder rung chosen and the rungs rejected | conversation only |
| **Progress-form check** — the job in Klement's *"Free me from [struggle], so I can [better me]"* form | conversation only |

The headline must pass every gate in `references/rubric.md`, including naming
what it replaces — and the `I want to…` clause must hold *progress*, not an
action. Always derive the progress form alongside the house statement: the "free
me" verb makes it obvious whether you're on progress or smuggling in a task. If
the two forms disagree, the job isn't clean yet.

If a job is built on the user's assertions alone, stamp it `hypothesis` and put
the validation step in `## Don't know` (almost always: *"confirm by finding
customers who switched from [the replaced solution]"*).

## CREATE workflow (grill mode)

Run the interview one question at a time, each with your recommended answer,
mining provided evidence (including `docs/product/input/`) before asking. The
full question tree is in `references/interview-guide.md` — read it before
grilling. The shape:

1. **Triage.** If the input holds more than one distinct struggle, list them and
   have the user pick ONE to grill now. In a target repo, park the rest as
   **real files** — `status: parked`, next free ids, containing only a draft
   headline and a `## Don't know` of open questions. Nothing invented: a parked
   file records that a struggle was seen, not what you guess about it. One deep
   job at a time beats five shallow ones.
2. **Push & pull first.** Klement's rule: study push and pull before anything
   else — they're felt outside any product. Find the struggling moment ("when
   did the old way stop working?") and the better life they're reaching for.
3. **Then anxiety & inertia.** What makes them hesitate, and what habits pull
   them back to the old way. These are the silent competitors.
4. **Ladder.** Express the same struggle at 2–3 altitudes (near-task, workable
   middle, near-cosmic). Have the user commit to the rung that's actionable.
5. **Draft & gate.** First draft in the *"Free me from…, so I can…"* form, then
   render the house format for delivery, carrying the progress through. Check
   live against `references/rubric.md`. When an answer reveals a task, feature,
   persona, or job-type, name the sin, point at the failed test, and re-ask —
   coaching, not lecturing.
6. **Converge.** Stop when the statement is gate-green *or* the user says "good
   enough." Stamp confidence honestly; if gates are open at override, record
   which ones and let that pull confidence down.
7. **Read-back — mandatory before any durable write.** Present the drafted
   file(s) — active and parked — exactly as they will be written. The human
   corrects; you fix. Only then write.
8. **Write & commit** (target repo only). Write the file(s), then loop: offer
   the next parked candidate. Grill it, park it further, or stop — the human
   decides. One commit for the run, message naming what changed and why.

## REVIEW workflow (diagnose → uplift)

1. **Diagnose all, cheaply.** For each statement, score on two axes — never
   conflated:
   - **Form** — well-formed progress statement, or a task / feature / persona /
     typed job? Judge from the text via `references/rubric.md`.
   - **Grounding** — is there evidence behind it? In a target repo, check
     `sources:` against `docs/product/input/` and that every line citation in
     `## Today` / `## Forces` resolves and says what the job says it says;
     from bare text, flag *"unverifiable — needs grounding"* rather than
     guessing.
2. **Rank.** Surface the worst offenders and the highest-value fixes.
3. **Uplift.** Grill the chosen ones into shape using the CREATE workflow.
   Review exists to raise quality — default toward grilling, don't stop at the
   verdict.
4. **Deliver.** In a target repo, a reshaped job is a **new file** that
   supersedes the old (old flips `status: superseded` + pointer; nothing else in
   the old file changes). A statement rejected as not-a-job flips to
   `superseded` or `parked` with the verdict noted in `## Don't know`. Read-back
   before writing, one commit per run — identical to CREATE.
5. **Iteration runs (A-Team review-and-extend).** When a new input batch lands
   on an existing job set, classify **every** active job, with the citation
   that triggers the class: **kept** (the input leaves it standing — say which
   lines confirm it, or "not touched by this input"), **reshaped** (a new
   file supersedes it, citing the reshaping lines), **superseded** (`status:
   superseded` with no replacement — the one case the pointer rule below
   allows: `## Related` says `superseded by: none — <reason, cited>` and the
   same reason and citation land in `## Don't know`). An unclassified job is
   a failed self-check: a North Star that shrinks between input and
   read-back without a stated trigger is exactly the drift the
   classification exists to surface.

## No human present

This skill is a grill: it cannot run without a human. If invoked with nobody to
answer (e.g. as a subagent), **escalate, never guess**: serialise the blocking
questions — one per heading — into `docs/product/context.md` under
`## Awaiting answers` (or report them in your return text when there is no
target repo), leave any in-flight work uncommitted-clean, and halt with a report.

**Autonomous degrade is forbidden.** Answering your own questions and writing
invented jobs into `docs/product/jtbd/` manufactures a North Star from nothing,
and every downstream agent treats it as ground truth. Assumption-flags do not
mitigate this.

## References

- `references/theory.md` — the book's model: definition, the four forces,
  competition, the two-interpretations critique, the nine principles.
- `references/interview-guide.md` — the grill question tree and Klement's own
  elicitation questions. Read before any CREATE grill.
- `references/rubric.md` — the gate checklist for both modes (the convergence
  condition). Read before drafting or diagnosing.
- `references/examples.md` — good job statements, the failure modes with
  rewrites, and a worked grill transcript.

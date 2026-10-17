---
name: learning-loop
description: "Run Robium's learning cycle when asked or when its session-start reminder is approved: consolidate captured signals, absorb ready guidance, refine skills, and inspect learning status."
---

# Learning loop

Capture is a lead, not knowledge. Promote it only when the evidence can improve
a future decision without injecting old conversations into new work.

## Capture without recall

- Hooks silently queue corrections and failures under the project-local
  `.robium/` directory.
- `learnings/observations/<skill>.md` is disposable local working state and is
  gitignored. Capture is a `tentative` entry there — status and signal are the
  only required fields.
- Hooks are host-dependent. If no queue or transcript exists, an explicit
  request to learn from the current task may still create a tentative finding;
  do not invent missing evidence.
- SessionStart may emit one count-only reminder per local day, but only for a
  correction, explicit remember/guardrail, or repeated error signature. It
  never injects excerpts or prior conversation content.
- Ask whether to run the learning cycle in a background subagent and continue
  the user's current task. Start it only after approval. The subagent reviews
  the queued evidence, makes any authorized skill edits, validates them, and
  reports back without blocking the main session.
- Apart from that reminder, read queued evidence only during an explicit
  consolidate, absorb, refine, or status task.
- Batch bookkeeping at a natural milestone. A command error or clean skill run
  is not automatically a reusable lesson.
- Keep project-specific facts in the application that owns them.

## Promote evidence

- Read the source transcript before turning a flag into an observation.
- Preserve what was expected, what actually happened, the evidence for the
  fix, and any dead ends that prevent repeating the mistake.
- Absorb only observations marked `ready`; uncertain material stays tentative.
- Deduplicate the finding before carrying it forward.
- Write local observations in the editable Robium checkout, never an installed
  plugin cache. The queue and transcript may remain in the app where the event
  happened.
- On absorption, put every future-use snippet, citation, caveat, and dead end
  in the owning skill or a focused `references/` file, then delete the
  observation. Delete rejected observations too; Git and the reviewed skill
  diff are the durable record.
- Read [PROMOTION.md](PROMOTION.md) when deciding whether evidence is strong
  enough or which skill owns it.

## Change the least

- Put the finding in the lowest skill that owns the decision.
- Prefer correcting or replacing existing guidance over adding another rule.
- Keep the live entrypoint lean. Conditional commands, failures, tuning, and
  platform evidence belong in focused support files.
- Follow the `skill-author` quality bar and show the concrete diff with its
  evidence. Maintainer-authorized edits may land locally; unattended or
  unrequested absorption uses a branch and human-reviewed PR.
- Live skills are versionless and changelog-free.

## Test according to risk

- Run the lightweight skill validator after an edit.
- Re-run an existing trigger or task check only when the changed guidance could
  affect it. Add a test only for a meaningful regression.
- For a contested edit, compare small alternatives against realistic requests
  and let a human choose. Do not preserve variants merely as ceremony.
- Read [TESTING.md](TESTING.md) for the optional eval format and safe task-check
  boundaries.

## Refine and retain

- Refinement starts with findings, not edits. Read [REFINING.md](REFINING.md)
  for the compact catalog review.
- Keep a transcript while a queue flag or local observation depends on it.
  Once the observation is absorbed or discarded, remove its processed queue
  flag and read [RETENTION.md](RETENTION.md) to prune the raw evidence.
- A status request may inspect queue size, ready observations, skill metrics,
  and transcript retention without changing anything.

## Done

- The future decision is clearer or safer with little added context.
- Absorbed or rejected observations are gone; only unresolved local working
  observations remain.
- Relevant checks pass, and raw transcript evidence is kept only as long as it
  is still needed.

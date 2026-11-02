---
name: triage
description: Evaluate untriaged beads and decide each one — agent-ready under a parent, owner's work, questions for the owner, deferred, or a wontfix close. Use to review what needs attention or to triage a specific bead.
disable-model-invocation: true
---

# Triage

Moves filed-but-unevaluated beads to a decided outcome. The outcomes and the
agent-ready gate are defined in the `beads` skill (`references/usage.md` §10);
this skill decides *when* a bead moves, not what the outcomes mean. There are
no intake labels: a bead's parent, status, acceptance criteria and the
`human` label carry the decision.

## Show what needs attention

Present four buckets, oldest first, with counts and a one-line summary per item:

1. Untriaged: open beads with no parent that are not epics —
   `bd list --no-parent -s open --json | jq '[.[] | select(.issue_type != "epic")]'`
2. Ideas: `bd list -t spike --status deferred --no-parent` — worth promoting
   or dropping
3. Waiting on the owner: `bd human list` — questions to answer or work to do;
   were any answered since?
4. Missing acceptance criteria among open work: `bd lint`

Use the supplied bead or authorized batch. Ask for selection only when the
request did not establish a scope.

## Triage one bead

1. **Gather.** `bd show <id>` including notes. Do not re-ask anything a prior
   `Established:` note already records.
2. **Redundancy check.** Search the codebase for an existing implementation by
   domain concept, not the bead's wording — and report where you looked.
   If it already exists, that is a wontfix close (step 6).
3. **Prior-rejection check.** `bd search "<terms>"` (closed beads included)
   for earlier `wontfix:` closes that resemble this. Surface any match before
   proceeding.
4. **Verify the claim.** For bugs: reproduce it, or record exactly why you could
   not. An unreproduced bug does not pass the gate.
5. **Decide within authority.** Recommend an outcome with evidence. Apply it
   when the user already authorized that decision or bulk triage; otherwise
   obtain the missing approval. An unreproduced bug gets questions for the
   owner, not an automatic wontfix.
6. **Apply the outcome** (all writes with `--actor`):

   | Outcome | Commands |
   |---|---|
   | Agent-executable | verify the gate below, add acceptance if missing (`bd update <id> --acceptance …`), give it a parent (`bd update <id> --parent <epic-or-feature>`), and `bd undefer <id>` if deferred |
   | Owner's work | `bd label add <id> human` |
   | Questions for the owner | a `human` task holding the questions, which the bead needs: `bd create -t task "Questions: <title>" -d "<questions>" -l human --actor …`, then `bd dep add <id> <questions-id>` |
   | Real, not now | `bd defer <id>` (`--until <date>` for a real date) |
   | Idea for later | `bd update <id> -t spike`, then `bd defer <id>` |
   | Not doing it | `bd close <id> --reason "wontfix: <why>"` |
   | Duplicate | `bd duplicate <id> --of <canonical>` |

   Record what was settled with `bd note <id> "Established: …"`, so the next
   session resumes instead of re-asking.

## Agent-executable gate

All three must hold: acceptance criteria populated, the description states
current and desired behaviour, and out-of-scope is noted where the request is
ambiguous.

## Rules

- Never make a bead agent-executable past a failing gate: an open bead with
  acceptance criteria is what autonomous claiming trusts.
- Do not create labels other than `human`.
- Analysis-only requests remain read-only. Carry existing triage authority
  through clear items; escalate material ambiguities separately.

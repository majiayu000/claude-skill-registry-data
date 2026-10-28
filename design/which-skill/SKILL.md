---
name: which-skill
description: Ask which FrontierJS skill, register or proof fits the situation, and in what order — the path from a change to landed.
disable-model-invocation: true
---

# Which skill

Every other skill here fires on its own description, one realm or one act at a time. What none of them carries is the ORDER — which comes first, what a step hands the next, and where the registers and the proofs sit between them. This is that, and only that: a skill's contents stay in the skill.

The shape is adapted from Matt Pocock's `ask-matt` ([mattpocock/skills](https://github.com/mattpocock/skills), MIT) by way of `stacks-flow`. The `skill-pointer` rule grades every name in the tables below, so a renamed skill turns `fli check` red rather than leaving this page pointing at nothing.

## The main path: a change, from intent to landed

| Step | Situation | Skill |
| --- | --- | --- |
| 1 | Starting cold — read `HANDOFF.md`, then the package's own `CLAUDE.md` | — |
| 2 | About to touch litestone, a `.lite` schema, a gate, a migration or tenancy | `data-hazards` |
| 2 | About to touch junction, a service, a hook, a transport, a plugin or a job | `api-hazards` |
| 2 | About to touch mesa, sierra, a resource, a form, prerender or `@frontierjs/css` | `ui-hazards` |
| 3 | The change crosses a package, or you are about to grep for who owns a translation | `bridge-index` |
| 4 | Search `ISSUES.md`, `ISSUES_ARCHIVE.md`, `DECISIONS.md` and `IDEAS/` for the subject | — |
| 5 | The change adds an option, coins a noun, restates something, picks between designs, or finds code and a doc disagreeing | `decision-rules` |
| 6 | Build outward from the schema: model, then service, then resource | — |
| 7 | Prove it (below) | — |
| 8 | Record it (below); editing a `CLAUDE.md`, a `SKILL.md` or anything behind a pointer | `doc-hygiene` |

**Step 2 is per realm, not per task.** A change to one service reads `api-hazards` alone; a field that reaches a form reads all three, in realm order.

**Step 4 is where a fix gets retired before it is written.** A defect filed against behavior a ruling already settled is the most common wasted hour here, and the registers drift toward closed faster than the prose that cites them.

**Step 5's answers are written before the first edit.** Answered after the code is green, they grade the thing already built and pass by construction.

## Proving

1. **`cd` into the package and run its own `test` script.** The runner differs per package, and `docs/TESTING.md` is the one list.
2. **Pair every refusal with the acceptance one character away**, and stub the fix once to watch the new test go red. A test that stays green with the fix removed is grading nothing.
3. **`fli proves`** names the drive the diff needs; the drive's *Start first* column says what to start. A diff that no row matches is a warning rather than a pass: it means the proof table has not met this kind of change yet.
4. **`fli check` at the repo root** after touching a rule, a skill or a register — the same repo-scope rules CI's `structure` phase runs, found before the push rather than after it.
5. **Review is the textbook subagent**: `/code-review` reads a diff and needs none of the exploration that produced it.

## Recording

| What happened | Where it goes |
| --- | --- |
| A behavior changed | the commit; a surprise still true goes in the realm's hazard skill (`FJS-D675`) |
| A defect found and not fixed now | an `FJS-###` row in `ISSUES.md` |
| A judgement settled | an `FJS-D##` in `DECISIONS.md` |
| A design not started | `IDEAS/` — never cited as behavior |
| A session ending with work in flight | `HANDOFF.md` |

## On-ramps

- **A new app for a client, with no `db/schema.lite` yet.** The `discovery` skill turns the conversation, brief or existing database into the schema. It is installed per user under `~/.claude/skills` rather than in this repo, so it is absent on a machine that has not added it.
- **Working down the open register.** `fix-next` picks the top `fli next` row and carries it through this path to `fli close`; one row per session, so a batch is `bun run fix:loop`.
- **Something is broken.** `VERIFYING.md` first: reproduce with one command that goes red on this defect, before theorizing. Then the realm's hazard skill, since half of what reads as a bug is correct-but-surprising behavior already written down there.
- **A screen needs styling.** `ui-hazards`, then `packages/css/README.md` for the vocabulary — a tone and a treatment, never a color (Invariant 13).
- **A document an agent reads is growing.** `doc-hygiene` before adding, since the cut is usually a pointer rather than a paragraph.
- **A page needs a picture, or a long page might become a paragraph and one.** `illustrate` fills the brief first and routes by kind — a painted image to `brand/IMAGERY.md`, a mechanism to an `.svg`, a chart to `dataviz`.

## At a phase boundary

Continue when the next phase needs this one as a primary source — design into implementation is the standard case. Send a scoped task that needs no steering to a subagent. Compact last: it is the default, not the first reach, and a summary flattens the reasoning a ruling rests on. **Another session may share this tree**, so a boundary is never the moment for `git stash` or a whole-file restore.

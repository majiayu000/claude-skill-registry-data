---
name: edit-skills
description: Use when creating, editing or sizing a skill or agent, and before it is done. Not for a rule or CLAUDE.md; read references/instruction-style.md.
argument-hint: <skill or agent to create, edit or size>
---

# Skills tool

A skill earns its place only by stopping a mistake the model makes without it, in as few words as that takes. The enemy is the skill that restates behavior the model already has and hides the one rule that changes anything. The overcorrection is an order stripped of its reason, which the model obeys to the letter past where it ends.

## When to use

- Creating a skill or an agent, changing one, or judging whether one has grown too long.
- Not for a fix that happens once, a habit of one project, or a limit a regex can check: a commit, `CLAUDE.md` or the verifier holds those, because a skill exists for a call that needs judgment.

## The loop

1. **Catch the mistake.** Write one prompt, built as `references/pressure-scenarios.md` describes, whose answer shows the mistake as one observable symptom.
2. **Watch it happen.** Run `scripts/pressure.mjs --prompt <file> --cells <model:effort> --plugin-dir <clone>`, the cell `references/pressure-scenarios.md` picks for the skill's kind, and read only the `without` answers now. A delegate takes no effort setting, so it cannot stand in for this run.
3. **Choose the home.** Place the fix with `references/where-a-fix-lives.md`, then write what must be prose in the shape below and in the register `references/wording.md` sets.
4. **Watch it stop.** Rerun `pressure.mjs` on the same cells and read the `with` answers; when the run without the skill also passed, the case shows nothing, so harden it until that run fails.
5. **Close each new excuse.** For every justification the run with the skill still produced, apply `references/plugging-holes.md` and rerun all cases; the skill is finished when a full rerun adds nothing to its tables.
6. **Verify.** Run `node verify.mjs`; a red check means the structure is wrong and gets fixed, never exempted.
7. **Judge blind.** When step 4's read is a close call, judge the pre-edit and edited clones' `with` answers blind, per `references/blind-eval.md`.

## The shape

| Part | Contract |
|---|---|
| `description` | Trigger only: the moments it fires, then what it leaves alone. A workflow written into it replaces the body, because the model acts on the summary it already read. |
| Opening | A single paragraph naming the principle, the enemy and the overcorrection. |
| `## When to use` | Bullets naming the symptoms first, then each "not for" case. |
| Process | Numbered steps, aim for at most eight, taken in order until one matches; every step is a rule with its reason. |
| `## Red flags` | Only in a skill the model is tempted to skip: a table from the tempting thought to what is actually true. |
| `## References` | A table of each file and the moment to read it; nothing is loaded before the step that needs it. |
| `## Judgment` | A ladder saying which rule wins when two conflict. |

## Form

- Bulk material, such as a template, a worked example or a checklist longer than 20 lines, lives in `references/`, and the body names the moment to open it.
- Aim the body at 2,000 tokens (bytes after the frontmatter / 4) and the description at 300 characters; the verifier fails 2,500 tokens, 636 for the injected `route-skills`, and 375 characters.
- A reference holds one topic and links to no other reference; over 100 lines it opens with a contents list linking each section.
- Text handed to a delegate lives beside `SKILL.md` as `<role>-prompt.md`, with a References row naming the step that dispatches it; `references/` holds only what the skill reads itself.

## Red flags

| The excuse | What holds |
|---|---|
| "The body has room to explain itself." | Each rule gets one reason clause; reasons that need a paragraph belong in a reference. |
| "An edit this small needs no test run." | Without the run lacking the skill, the edit is a guess about what the model does. |
| "Any model already knows this." | Then the line goes; only what the run without the skill got wrong earns a place. |
| "Forbidding it will do." | Forbidding a wrong output shape tends to produce more of it; the failure picks the form. |
| "I will test them together once all the skills are written." | Each skill clears every case before the next one begins, because skills written in a batch hide each other's gaps. |

## References

| File | Read it when |
|---|---|
| `scripts/rename-skill.mjs` | Renaming a skill: run `node scripts/rename-skill.mjs --from <old> --to <new>` to move its folder, docs page and pressure folder and rewrite every mention in one pass. |
| `references/pressure-scenarios.md` | Step 1, and whenever the run without the skill passes a prompt that only asks for the rule. |
| `references/where-a-fix-lives.md` | Step 3, before the first rule is written. |
| `references/instruction-style.md` | Step 3, before writing or editing any instruction file, `CLAUDE.md`, rule, agent, output style or hook included. |
| `references/wording.md` | Step 3, when two phrasings compete or a rule's tone is unclear. |
| `references/description.md` | Step 3 for the frontmatter; step 5 when a symptom joins the description. |
| `references/skill-shape.md` | Step 3 for a skill started from nothing; never for a change to an existing skill. |
| `references/plugging-holes.md` | Step 5, once a run with the skill loaded still produced a justification. |
| `references/blind-eval.md` | Step 7, when step 4's `with`/`without` read is a close call. |

## Judgment

- A rule the run without the skill broke outranks a rule that only reads well.
- An edit that was never tested is reverted rather than kept as a draft.
- Short outranks complete: a skill that grew too long drops its weakest rule, never a reason clause.
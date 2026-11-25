---
name: agent-skills-gap
description: Analyze Claude or Codex session logs or pasted prompts to identify evidenced strengths, weak task categories, a surprising weakness, and up to seven relevant skills, then create a private JSON result and shareable card. Use when asked for an AI skills gap test, agent résumé, missing expertise, or a share card about what an agent is good or bad at.
---

# Agent Skills Gap Test

Give the user a defensible result, not a personality quiz.

## Run

1. Use only the session logs, transcripts, or prompts the user authorized.
2. Locate this skill directory and run its deterministic analyzer:

```bash
node /absolute/path/to/this-skill/cli.js --out ./out <input-file> [more-input-files]
```

For pasted material, save it as a temporary `.txt` input inside the task workspace first. Do not
put private prompt text in a shell argument.

3. Read `out/skills-gap.json`. Report:
   - strongest measured category;
   - every category rating;
   - the surprising weakness;
   - the recommended skills count and names.
4. Point the user to `out/skills-gap-card.svg` as the shareable artifact.

## Evidence rules

- Fewer than two relevant entries means `Not measured`, never `Weak`.
- A task appearing often is not proof of quality. Weakness requires explicit friction evidence.
- Say the result describes the supplied sample, not the model's intelligence.
- Recommendations mean “relevant to this observed gap,” not “confirmed missing from the machine.”
- Never copy prompts, paths, filenames, private project names, or transcript excerpts into the
  share card or public summary.
- Cap recommendations at seven.
- Do not upload or publish anything without a separate explicit action.

## Output contract

`skills-gap.json` uses schema `agent-skills-gap/0.1`. The SVG contains only generic category labels,
ratings, the number of analyzed entries, and recommended-skill count. Raw input stays local.

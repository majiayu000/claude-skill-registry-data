---
name: "skill-builder"
description: "Use when turning a repeated procedure or SOP into a skill, or deciding whether a step should stay a prompt, become a skill, a loop, or a scheduled routine."
---

# Skill builder

From the user's playbooks "Turn an SOP into a Claude Skill" and "Prompt to skill to loop to routine", plus the course units on skills (L13-22 contract, L13-24 progressive disclosure, L13-25 routing, L13-27 evals and packaging).

## 1. Pick the level (the automation ladder)
- **Prompt:** run a new step by hand until it reliably works. Do not make a skill of something that has not worked twice.
- **Skill:** steps that keep recurring (video intake, design intake, a curation pass) get saved so one request repeats them.
- **Loop or routine:** only steps that are safe unattended (a weekly check for entries marked unchecked) get scheduled, and they must report failures somewhere the user looks.
- **Never automate judgment:** deciding what goes into 411, accepting claims, and the final review stay with the user.

## 2. Write the SOP first
Plain steps in order: trigger, inputs, each step, the check that proves it worked, the output, what it must not do. If the SOP cannot be written, the skill is not ready.

## 3. Convert to SKILL.md
- Front matter: `name` (kebab-case) and a one-sentence `description` that says WHEN to use it. Keep it short, because it is what loads first (progressive disclosure); detail goes in the body.
- Body: the steps, rules, output format, and which other skills it hands off to.
- Python does the mechanical parts (counting, checking, fetching, frames); the skill names the script and its expected output.

## 4. Keep the two kinds distinct
- **Claude chat skills** are saved to the account through the skill proposal card. They must not assume a shell on the laptop or access to sites chat cannot reach (X).
- **Claude Code skills** live in `.claude/skills/<name>/SKILL.md` on the laptop, with scripts beside them or in the repo, and a copy in pyburticapa `python_skills/llm_instructions/`.

## 5. Test, fix, repeat
Run it end to end on a real case, fix each failure in the SKILL.md (not in chat), run again. A skill is done when a fresh session follows it without extra explanation.

## Rules
- Read an existing skill in full before changing it; a saved change replaces the whole file.
- One skill per job; link to other skills instead of copying their steps.
- Labels on any facts inside a skill: verified here, source claim, our inference.
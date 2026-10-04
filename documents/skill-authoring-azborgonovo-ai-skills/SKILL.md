---
name: skill-authoring
description: Conventions for writing or editing a SKILL.md in this repo — horizontal rules, bold usage, line wrapping, spelling, negative instructions, referencing other skills, when to reach for a scripts/ helper, and the bundled `check_skills.py` validator to run before committing. Use whenever creating a new skill or improving an existing one in this repository.
---

This repo holds Claude Code skills. Claude reads a SKILL.md file, and a human reads it only rarely. So formatting has to earn its tokens by helping the model parse and weight instructions, rather than by looking tidy. Apply these rules when you create a new skill or improve an existing one.

### Horizontal rules (`---`)

Do not use `---` as a section separator between steps or sections. The `##` and `###` Markdown headers already delimit sections.

The **only** `---` that belong in a SKILL.md are the two YAML frontmatter delimiters at the very top. They open and close the `name` and `description` block.

### Bold (`**...**`)

Bold is a signal, not decoration, and signal weakens when it sits everywhere. Use it on purpose:

- **Keep it for labeled lead-ins** that act as inline sub-headers, such as `**Truncation check**:` and `**Why the script**:`. These help the model locate and weight a specific piece of guidance.
- **Keep it for directive anchors** on things that change behavior, such as `**Never** approve`, `**Always** post through the script`, and `**Critical**`.
- **Drop it where it is purely cosmetic.** Bold on a mid-sentence phrase that needs no emphasis dilutes the bold that does matter.

When in doubt, ask one question: does the model behave differently without this bold? When the answer is no, leave the text plain. Do not strip bold wholesale either. The loss of the useful lead-ins and directives costs more in clarity than it saves in tokens.

### Line wrapping

Do not hard-wrap prose in a SKILL.md body. Write one line per paragraph, and one line per list item, and let the editor soft-wrap the display.

In the YAML frontmatter, a folded `description: >` block still wraps across indented lines.

### Prose and spelling

Write the body in plain English, per [Plain English in agent-facing markdown](../../../CLAUDE.md#plain-english-in-agent-facing-markdown) in the repository guidelines. That section carries the sentence limit, the tense and voice rules, and the two exemptions.

Use American English spelling, such as `behavior`, `normalize`, and `canceled`, so that terminology stays consistent across skills. The exception is text quoted word for word from another source. That covers an example string copied from a sibling skill, and the wording of a real product. Keep the original there rather than "correcting" the quote.

### The `description` field

The `description` is retrieval text, and not prose. Claude reads it to decide whether to load the skill. State what the skill does, in the third person, and then state when to use it. That is the rule in Anthropic's [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#writing-effective-descriptions), and every official example writes the second part as "Use when ...".

Keep that wording. Write the main trigger as `Use when the user ...`, and open a further branch with `Use it also when ...`. Quote the phrasings that a real request carries. Do not replace the framing with a sentence about the triggering of the skill, as in "The trigger covers phrasings such as ...". That shape keeps the keywords and drops the instruction that Anthropic recommends around them.

A skill with `disable-model-invocation: true` is the one exception. Claude cannot load such a skill, so "Use when" promises something that cannot happen. Say that the skill is user-only, name its command, and then write the trigger as "When the user wants ..., suggest this command".

A plain English rewrite must not cost a description its framing. The exemption for a `description` in the repository guidelines exists for that reason.

### Referencing other skills

Reference a sibling skill by name when it lives in the same plugin. Everything under `skills/<plugin>/` installs as one unit, so that pointer always resolves for an installed user. Naming the sibling and handing off to it is cheaper and clearer than restating what it already covers.

Keep a skill in a *different* plugin out of the instructions. Plugins install independently, so the skill you point at can be absent, and the reader is left with a step that they cannot take. Where one genuinely helps, phrase it as an optional accelerator and keep the fallback local. Say what to do when it is absent. Define any vocabulary that the guidance needs here, rather than importing it from a plugin that nobody installs.

The `description` field is bound by the same rule, and not only where it states a boundary. A description that names the skill of another plugin ties the retrieval text of this skill to something that can be absent. That holds for a hand-off, for a scope boundary, and for a trigger phrase. State a boundary as what this skill does not do. Write a trigger from what the user says about their own situation, rather than from the tool that they happened to use to get there.

### Counter-examples and negative instructions

Prefer stating what to do over what to avoid. A bare "do not do X" leaves X sitting in the context with no positive target to replace it. A clear positive rule with its reasoning is usually enough on its own.

### Discard a skill that shows no measured lift

A skill earns its place only when its gains outweigh its cost. When an eval against the plain model shows no pass-rate gain, and the skill adds token or latency cost, discard it. Do not ship it, and do not keep it "just in case".

**Precedent — `consistency-first`**: a drafted skill for keeping generated code aligned with the existing patterns and vocabulary of a codebase. It ran across four eval iterations, on easy and hard fixtures, on Opus and Haiku, plus a drift scenario built as its best case. It produced essentially the same code as the plain model, and it spent roughly 10% more tokens. Current models already match neighboring code, read steering docs and ADRs unprompted, and re-anchor after local drift on their own. It was discarded on that evidence.

### The thresholds that settle a verdict

Read the eval before you apply the rule above, because one criterion does not fit every skill. The tag on its cases sorts it. A `behavior` suite measures a reasoning skill against a no-plugin baseline arm. A `mechanics` suite measures a Manual skill, which a baseline arm cannot reach at all.

A reasoning skill earns its place through better thinking, so the delta over the baseline is the test. A mechanics skill earns its place by doing something a baseline cannot do, such as driving a tracker or filling a template. A delta measures nothing there, so the test is the absolute score on the with-plugin arm.

A grader marked `arm: with-only` is dropped from the baseline arm and excluded from the score in both arms, so the delta compares like for like. Mark a grader that way when a baseline can never satisfy it: a format it never saw, or a skill it does not hold. Under `--ablation none` nothing is excluded, so a mechanics suite scores those graders normally, which is what its verdict needs.

Read the `Fired` column before the delta. The with-plugin arm loads the plugin, and the model still decides whether to reach for the skill, so a case where the skill never fired scores a delta of zero for a reason that has nothing to do with the quality of the skill. `decide` measured this exactly: the two cases that fired returned +0.20 and +0.17, and the two that did not returned 0.00.

| Verdict | Threshold |
|---|---|
| Decommission a reasoning skill | The baseline score matches or beats the with-plugin score, on cases where the skill fired. |
| Decommission a mechanics skill | The score stays low after one fix attempt. A low baseline is never the reason. |
| Improve the skill | The delta is positive, and the with-plugin score sits below about 80%. One grader that fails across cases gives the same verdict, and it names the edit. |
| Improve the description | The delta is near zero because the skill did not fire, or the triggering axis reports a low `Fires` or `Holds` count. The skill body is not the problem. |
| Promote Trial to Adopt | A score of about 90%, with a positive delta. |
| Demote Adopt to Trial | The measured score does not support the claim. |

Read a verdict off three runs, never one. The agent is not deterministic, so a single run reports luck as skill. `scripts/run_evals.py` runs each case three times by default, and `scripts/eval_report.py` reports two numbers from that: pass@k, the cases that passed at least once, and pass^k, the cases that passed every time. Read pass^k for a skill that must work every time, and pass@k for one where a single good answer is enough. A wide gap between the two names a flaky skill, and a flaky skill is not ready to promote whatever its mean score says.

A suite that reaches 100% stops telling you anything. When pass^k hits every case, the suite is saturated: add harder cases rather than reading the score as proof the skill is finished.

A pass rate of 0% is a broken case far more often than an incapable model. Before you act on one, read the transcript and check that the case is solvable, that the prompt names paths that exist in the sandbox, and that no grader demands something the granted tools cannot do.

`scripts/run_evals.py` runs every axis and writes the numbers, and `scripts/eval_report.py` turns them into the records that `README.md` reads. See [Evals](../../../README.md#evals) for the case layout, which lives under `evals/<plugin>/<skill>/` at the repository root, and for the grader types.

### Environment-specific values

Do not hardcode a value that varies across machines or users. That covers a filesystem path, a clone-root convention, a tool version, and a default port. A value that matches your own setup reads as generic, and it runs correctly only on a machine shaped like yours. Everyone else gets a silent wrong answer, or a confusing failure with no clue why.

Prefer discovering the value instead. Search a short list of plausible candidates, or derive it from something already known. Two examples are the remote URL of a repo and a config file already on disk. When discovery comes up empty, ask the user directly rather than guessing further. A question is cheap, and a wrong guess that "worked when I tested it" is not.

**Precedent — clone-root assumption**: a host-adapter skill for locating the local clone of a repo assumed that every user clones repos under `~/projects/<org>/<repo>`. That was true for the machine it was written on. Someone copied the assumption word for word into a second skill while generalizing it for a different code host, and nobody questioned it either time. It then failed on the very repo it was written in, which lives under `~/Code/<org>/<repo>` instead. The fix: probe a handful of common roots, then fall back to matching by remote URL, then ask.

### Check the mechanical rules before committing

A machine settles several rules here, rather than a reading. Those rules are the `description` cap, the `name` charset, the two-`---` rule, the body length, and one line per paragraph. They drift in silence. Three descriptions in this repo sat over the 1024-character cap until a full review pass found them. Run the bundled validator over any `SKILL.md` that you touched, before the commit that lands it:

```
python .claude/skills/skill-authoring/scripts/check_skills.py
```

With no arguments it checks `skills/` and `.claude/skills/`. Pass a path, either a tree or a single `SKILL.md`, to check a skill that you are authoring in another repo. It exits non-zero on any failure, and it names the file and the rule.

It is advisory: it reports rather than gates, and a clean run says only that the mechanical rules hold. Everything that it stays silent about is still yours to judge. That covers no-ops, duplication, whether the description reads as third person, and whether a British spelling is a quote that it must keep.

### General principle

Prefer instructions that explain the *why* over a rigid wall of `MUST` and `NEVER` formatting rules, and keep the always-loaded SKILL.md body lean.

Reach for a bundled `scripts/` helper, which loads only when it runs, when a task is *genuinely deterministic and repeated every run*. Weigh that honestly rather than defaulting to it. Much of the value of a skill is the model's judgment, which a rigid script cannot do. A script can also actively mislead, by anchoring the model to the wrong signal. An existing tool, such as `Grep`, ripgrep, or `Glob`, often already covers the deterministic part, with no code to maintain.

When unsure, stay model-only and let evidence decide. Once you watch several runs independently re-derive the same helper, that is the cue to extract it into `scripts/`.

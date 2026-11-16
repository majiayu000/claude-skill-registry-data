---
name: write-skill
description: "Write a new honey-stack skill or patch an existing one to the quality bar, with evals."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "mattpocock/skills writing-great-skills (SKILL.md, GLOSSARY.md), write-a-skill; mattpocock/skills 4ae2317ddb22b046e26455e4f9c9b3aaaf62212d skills/productivity/writing-for-agents/SKILL.md; obra/superpowers 7.0.0 skills/writing-skills (SKILL.md: SDO, match the form to the failure, RED-GREEN-REFACTOR), testing-skills-with-subagents.md; anthropics/claude-plugins-official skill-creator skills/skill-creator/SKILL.md (Apache-2.0, modified: near-miss negatives, explain the why, keep the prompt lean); cursor/plugins pstack 0.15.25 skills/principle-encode-lessons-in-structure; Codex CLI bundled ~/.codex/skills/.system/skill-creator/references/openai_yaml.md"
---

# write-skill

A skill exists to make the agent take the same process every run. Every line either changes behavior against the default or goes. RSI drafts its Tier 2 skill patches against the **Rules** below, so each rule is a pass/fail check; cite a failed check by its ID (`W7`).

| Ask | Branch |
|---|---|
| New skill, or "turn this into a skill" | A. New skill |
| Fix, tighten or retarget an existing skill; an RSI patch | B. Patch |
| "Is this skill any good?" | Run the Rules on it and report each failed ID with its line |

`docs/skill-style.md` is the house style and these Rules are its checkable form. If they disagree, the style doc wins; fix this file.

When editing instructions, routing descriptions or references, read [writing for agents](references/writing-for-agents.md): sharpen the condition for loading material before inlining more of it, and keep each meaning with its owner.

## Rules

**Invocation**
- **W1 Invocation earned.** Model-invoked only when the agent must reach the skill on its own (the situation arrives without the user naming it) or another skill must invoke it. Otherwise user-invoked: `disable-model-invocation: true`.
- **W2 Listing budget.** Model-invoked descriptions are always loaded, every session. Each is ≤280 chars and all of them together stay ≤3,500 chars. `honey doctor` prints the total on its "model-invoked descriptions" line; read it after any description change.
- **W3 Description = triggers only.** Model-invoked: starts "Use when", front-loads the leading word the user actually types, one trigger per distinct branch (synonyms for one branch collapse to one), no workflow summary. An agent that reads a summary follows the summary and skips the body. User-invoked: one human-facing line.
- **W4 Codex metadata.** A user-invoked skill ships `agents/openai.yaml` with quoted `interface.display_name`, `interface.short_description` (25–64 chars) and `policy.allow_implicit_invocation: false`.
- **W5 Attribution.** Frontmatter has `license:` and `metadata.sources` naming every upstream actually used (repo, version, path). Apache-2.0 sources add "(modified)". Nothing listed that wasn't used.

**Body**
- **W6 Checkable completion.** Every step ends in `Done when:` with a condition the agent can observe (a file exists, a command printed X, every Y has Z). Make it exhaustive where coverage matters: "every caller updated", not "update callers".
- **W7 No no-ops.** Test each sentence alone: does it change behavior against what the agent does by default? Delete the sentence if not. Also delete anything the bootstrap already says (sizing, the ladder, proof before done, decision policy, untrusted data, delegation, the receipt).
- **W8 One source of truth.** Each meaning lives in one place. Point to another honey skill by name ("the `verify` skill"); never restate it.
- **W9 Leading words.** Prefer a pretrained concept (root cause, tracer bullet, red-green, blast radius, near-miss) over a spelled-out triad or invented jargon.
- **W10 Form matches the failure.** Agent skips a known rule under pressure: a prohibition plus the named rationalization. Output has the wrong shape: a positive recipe of its parts in order. An element gets omitted: a required slot in the template. Behavior depends on a condition: a conditional on an observable predicate. No "unless it matters" clauses.
- **W11 Positive targets, quiet caps.** State the target ("run the check and read its output"). ALWAYS/NEVER/MUST in capitals only for real safety rules; otherwise give the reason.
- **W12 Agent parity.** Works on Claude Code and Codex: neutral skill references, no Claude-only tool without a fallback ("AskUserQuestion, or a numbered question in chat"), scripts called through their interpreter (`python3 scripts/x.py`).
- **W13 Disclosure.** `SKILL.md` under 150 lines (500 hard cap), key rules first. Material only some branches need moves to `references/<topic>.md`, linked with the condition that sends the agent there. Deterministic steps move to `scripts/` (shell, or stdlib Python 3.9).
- **W14 Evals.** Every model-invoked skill has one should-fire and one should-not-fire case under `evals/`. Format and commands: `references/evals.md`.

## A. New skill

1. **Earn it.** If the lesson is mechanical (a regex, a path check, a command), encode it as a script, guard or check instead of prose. If an existing honey skill owns the job, extend it (branch B). Done when: you can name the job, why no existing skill or check covers it, and its branches.
2. **Red first.** Pick the invocation (W1). For model-invoked, write both eval cases now (`references/evals.md`) and run them before the skill exists: the should-fire case must fail. For behavior the skill must produce, add a grader for it and confirm the baseline misses it. If the baseline already behaves, there is nothing to teach; stop. Done when: you have a failing run and a one-line note of what the agent did instead.
3. **Draft.** Frontmatter, then a body that answers the baseline failure and nothing hypothetical (W6–W13). Done when: the files exist.
4. **Check.** Run W1–W14 line by line against the draft and fix every failure. Run `honey doctor` if a description changed. Done when: every rule passes, with the budget line read.
5. **Green.** Re-run the eval cases. Done when: both pass (should-fire fires, should-not-fire stays silent) and the behavior grader passes.

## B. Patch an existing skill

A patch is the smallest edit that fixes an observed failure. RSI Tier 2 patches follow this branch exactly.

1. **Pin the failure.** Quote the evidence: the user correction, the eval that failed, the transcript line. Classify it: missed (should have fired), misfire (fired wrongly), wrong behavior, or a W-rule violation. Done when: you have the quote and the class.
2. **Write the regression case** from the real failure, using the eval format. It must fail on the current skill. Done when: a run shows it failing.
3. **Write at most 3 hunks.** Each hunk is an exact `old` / `new` pair where `old` occurs exactly once in the file. Prefer deleting or sharpening a line over adding one; add a section only when the failure is an omitted element (W10). Change the description only for missed or misfire. Leave `name` alone. Done when: every hunk traces to the pinned failure and the Rules still pass on the patched file.
4. **Compare.** Run every eval case for the skill on old and new. Accept only if new ≥ old on every case and new passes the regression case that old fails. Done when: both runs' results are recorded.

Patch output, as RSI and reviewers read it:

```
skill: <name>
failure: <class>: "<evidence quote>"
hunks:
  - file: skills/<name>/SKILL.md
    old: |
      <exact text, unique in file>
    new: |
      <replacement>
eval: evals/<case>/   old: fail   new: pass
rules: W1–W14 pass
```

## Finish

Once the change is on the main checkout, `honey sync` refreshes the Codex copy; Claude loads the repo in place. Report the files changed, the eval cases with old and new results, and the budget total if a description changed.

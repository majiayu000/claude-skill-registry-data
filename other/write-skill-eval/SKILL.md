---
name: write-skill-eval
description: >-
  Repo-only guide to writing an eval case for one of this devkit's skills, running it with
  and without the plugin, and proving each grader can fail before trusting its score. Use
  when the user asks to add, write, or fix an eval, test whether a skill earns its place,
  or close a gap that `scripts/check-evals.sh` reports. Not shipped with the plugin.
---

# Write a skill eval

An eval case earns its place when plain Claude fails it and the skill fixes that. The
process: start from a real failure, set up the scenario, prove plain Claude fails, write the
smallest rule that fills the gap, prove the skill fixes it and actually loaded, then keep the
case as a guard. Follow the eval rules in `CLAUDE.md` ("No build, lint, or test step")
throughout; this skill is the order to apply them in.

## 1. Start from a real failure

Begin with something Claude got wrong, not with the skill's text:

- **Knowledge skill:** a bug that shipped in a package, or a mistake Claude was seen making.
  Tag a shipped bug's case `real-bug`. Writing a case from a rule you already have only
  shows the rule gets loaded, not that it's needed.
- **Workflow skill** (`feature-*`, `quick-fix`, `issue-*`, ...): a rule the skill must keep,
  such as stopping when its input is missing or never touching git.

One case tests one behavior. If you find two, write two cases.

## 2. Write the prompt

Create `plugins/umbraco-devkit/evals/<case-name>/prompt.md`. Name the case like its
neighbors: the skill's short name, then what it tests (`env-sync-access-rules`).

```markdown
---
description: <one line: what this case proves>
tags: [<skill-name>, should-trigger]
# covers: ["<the skill section it tests>"]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, WebFetch]
---

<the request, as a package developer would type it>
```

- **Ask for the change, not a review.** Given a short snippet to review, plain Claude
  catches most mistakes. Review only a realistic multi-file diff, as in
  `reviewer-feature-diff`.
- **Set up the scenario, never ask for the fix.** Ask for something a developer would
  really ask for (a feature, a change, a job to add) in a project where the obvious answer
  brings the problem in. A prompt that points at the problem tests debugging, which plain
  Claude already does well, not whether the skill stops the problem happening. For a
  `real-bug` case, ask for the change that first introduced the bug, not the fix.
  - **State the setup facts the trap needs**, as a developer would: "sites are load
    balanced", the target versions, "other packages call this". Without them the trap
    isn't real, and a careful answer could fail for not guarding against something the
    setup never showed.
  - **Never** describe the symptom, ask for a fix, name the risk or the right API, or bait
    the answer ("I think it's fine", "make sure it's secure").
  - **Diagnosis cases** (symptom in, cause out) get the `diagnose` tag. Keep them rare;
    they don't show a skill prevents anything.
  - **Workflow cases** for bug-fixing skills (`investigate-bug`, `quick-fix`,
    `issue-resolve`) are handed a bug, because the workflow's own rules are what's tested.
- **Say what the sandbox lacks.** Git and dotnet don't run in an eval. Say so in the prompt
  ("Git can't run here") so the answer doesn't stall trying. Don't say the network is
  missing.
- **Keep docs access.** `WebFetch` is the one way out of the sandbox, and it's how
  `umbraco-docs` and `umbraco-cms-source` read the docs and source when there's no local
  clone. Keep it in `allowed_tools` so a skill can look things up as it would in a real
  project. Both arms get it, so the comparison stays fair. Drop it only when the case
  needs no lookup at all.
- **Tags:** the skill's name, then `should-trigger`, `should-not-trigger`, or `workflow`.
  Add `real-bug` when it applies.
- **Covers:** for a knowledge case, add `# covers: ["<heading>"]` after `tags:`, naming the
  skill's `## ` section (in `SKILL.md` or `references/`) that holds the rule. Italic headings
  (`## *Background*`) are context and take no eval. Use `[]` for a
  guard whose rule was removed. Keep the `#`: the eval tool rejects frontmatter keys it
  doesn't know, so the line is a YAML comment. `scripts/eval-coverage.sh --check` fails on a
  heading that doesn't exist.

For a should-not-trigger case, write a nearby request the skill should stay out of.

## 3. Scaffold the project, if the task needs files

When the answer has to read or change code, add `fixture.sh` (bash that writes the starting
files) and a `case.yaml`:

```yaml
schema_version: "1.1"
name: <case-name>
context:
  scaffold_script: fixture.sh
```

Keep the fixture to the few files the task touches, but real enough that the trap lives in
the code, not the prompt.

## 4. Write the graders

One file per check in `graders/`. Each checks one thing and passes every valid fix, not only
the one you had in mind.

- **Did the skill load:** a `skill-fired.md`, copied from a neighbor case. Under the default
  with/without run it reports whether the skill fired and isn't scored. For a
  should-not-trigger case, use `min: 0`, `max: 0`, `arm: both`.
- **Mechanical checks:** `type: regex` or `type: file_exists`. Free and exact; prefer them
  when they're enough.
- **Judgment checks:** `type: llm` with a `PASS if ...` and a `FAIL if ...` paragraph. Use
  `focus: trace` to grade the whole answer, or `focus: {source: file, path: ...}` for one
  written file. Give the grader for the core behavior `weight: 2`.

## 5. Prove plain Claude fails

Run the case once with a single run per arm:

```bash
claude plugin eval plugins/umbraco-devkit --case <case-name> --runs 1 \
  --judge-model sonnet --no-publish --scaffold --allow-tools Write Edit WebFetch
```

Drop `--scaffold` for a case with no `fixture.sh`. Read the run's warnings first: one saying a
grader "cannot pass with the granted tools" means the run measured nothing.

- **A grader that passes without the plugin measures nothing.** Make the prompt or grader
  harder, or delete the grader.
- **If every grader passes without the plugin**, the case is too easy. Rework it in step 2.
- **Try a second scenario before giving up on a gap.** Plain Claude often passes the obvious
  version and fails a variant: sibling code already doing it wrong, the risky part buried in
  a bigger change, a related API. If it passes every variant you can think of, no rule is
  needed; stop here.
- **Workflow cases** run with `--ablation none`, so there is no baseline. Read each grader
  against an answer that breaks the rule; if it would still pass, tighten it.

## 6. Write the smallest rule that fills the gap

Skip this if the skill already has the rule and only needs to load (step 7).

- **General, not project-specific.** The rule describes Umbraco or stack behavior any
  package hits. Leave out the names and conventions of the project the bug came from.
- **Checked against the source.** Confirm the behavior in CMS source at the target release
  tags (`umbraco-cms-source`) or the docs (`umbraco-docs`), including from which version it
  applies.
- **In the right skill.** Follow "Skill boundary discipline" in `CLAUDE.md`: fit the
  skill's description, write only what differs from the norm, and grep for the concept
  first.

## 7. Prove the skill fixes it, and loaded

Run it with the default three runs per arm, Sonnet judging:

```bash
claude plugin eval plugins/umbraco-devkit --tag <skill-name> --judge-model sonnet \
  --no-publish --scaffold --allow-tools Write Edit WebFetch
```

Three runs are noisy. Don't judge a close or zero gain on one run: rerun with `--runs 6`
first.

A pass with the plugin counts only if the skill loaded: check `skill-fired` in the log. If
the plugin passes but the skill didn't load, the gain came from somewhere else. If the
skill doesn't load, fix its description's "Use when" so it matches the request, not the
rule. Then rerun.

Check the log for errored runs too (auth, spend limit). An errored run is neither a pass nor
a fail; don't count it.

## 8. Finish, and keep the case as a guard

- Run `scripts/check-evals.sh`.
- Record the run: `scripts/record-eval-scores.sh` (newest results by default), then
  `scripts/eval-coverage.sh`. Commit `docs/eval-scores.json` and `docs/EVAL-COVERAGE.md`;
  CI fails if the report is stale.
- Put the with and without scores in the PR. A knowledge skill that shows no gain doesn't
  ship.
- `evals/` ships but never loads for a consumer, so a new case needs no version bump.
- Rerun the case whenever its skill changes. Plain Claude improves, so recheck old cases'
  baselines now and then.

## Removing a rule

A rule goes only when plain Claude reliably gets it right with no prompting, across varied
scenarios where the rule applies, not just the existing case.

1. Write at least one harder variant (step 5's list).
2. Run plain Claude only, 4 runs per scenario. To skip the with-plugin arm, point the eval at
   a copy of the plugin with no skills: a folder holding only `.claude-plugin/plugin.json`
   (no `skills` entry) and a real copy of `evals/` (the tool refuses a symlink), run with
   `--ablation none`.
3. Stop at the first failed run: one miss proves the rule is needed.
4. Remove the rule only if every graded run passed. Keep its cases as guards.

## Keeping evals current

Evals go stale as skills, Claude and Umbraco change. Rerun them when something happens, not
on a timer you'll forget.

- **A skill changes (in its PR).** New rule: steps 1–8. Changed rule: rerun the cases that
  cover its section, with and without the plugin. Changed "Use when": rerun the skill's cases
  and its should-not-trigger cases and check it loads. New context section: italic heading,
  no eval.
- **A bug ships that a skill should have stopped.** Write a `real-bug` case for it first. If
  plain Claude fails it, add or fix the rule. These are the most valuable cases.
- **A new Claude model.** Run every knowledge case as plain Claude (the empty-plugin run from
  "Removing a rule"). Rules it now passes get the removal check. Then run everything once with
  the plugin to catch a skill that now makes things worse.
- **A new Umbraco version.** Recheck version-specific rules against CMS source, bump the
  version in the fixtures, and rerun the affected skills.
- **Every few weeks, or about every 10 merged PRs.** Work the coverage report's "What to do
  next" from the top: remove, fix loading, prove gain, stale scores, then one or two
  under-covered skills, highest risk first (security, extensibility, env-sync).
- **Revisit a case** when plain Claude passes it every time (write a harder variant, or keep
  it as a guard with `# covers: []`), when a score looks wrong (read the judge's evidence: a
  vague grader fails correct answers), or when its score is older than 90 days.

Don't chase 100% coverage for its own sake, and don't run everything with the plugin by
default: plain-only runs cost half and answer most questions.

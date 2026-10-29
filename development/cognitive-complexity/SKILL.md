---
name: cognitive-complexity
description: Keeps TypeScript/JavaScript functions readable for software developers by computing SonarSource Cognitive Complexity with a bundled scorer instead of estimating it, then explaining, refactoring and auditing complex code. Use when writing or refactoring TS/JS functions so they stay readable, when asked why a function is complex or hard to follow, how to simplify or flatten deeply nested code, to fix a sonarjs/cognitive-complexity or Biome noExcessiveCognitiveComplexity lint failure, or to audit changed files or a folder for overly complex functions.
---

# Cognitive complexity

Cognitive complexity scores how hard a function's control flow is to read: +1 for each break in linear flow, plus +1 per level of nesting that break sits in. This skill keeps TS/JS functions under a threshold and computes scores with `scripts/score.mjs` (in this skill's directory). **Always compute scores with the scorer. Estimates by eye are often wrong by several points.**

## Thresholds

- **Target ≤ 10** per function for new code. **Hard limit 15** (the SonarJS default).
- If the project sets its own limit, use that instead: check the `sonarjs/cognitive-complexity` option in the ESLint config, or `maxAllowedComplexity` for Biome's `noExcessiveCognitiveComplexity`.

## Running the scorer

```bash
node <skill-dir>/scripts/score.mjs [--threshold 15] [--explain] [--json] <files or dirs>
```

- It prints a Markdown table, worst first: file, function, line, length in lines, score, and the three largest increments. Scores above `--threshold` are marked `✗`, and their line-by-line breakdown follows the table. `--explain` prints the breakdown for every row. Show the table to the user as is.
- Exit codes: `0` ok, `1` threshold exceeded, `2` usage or parse error.
- If the project lints with Biome (a `biome.json` or `biome.jsonc` exists), add `--biome`. Biome counts `??` and `finally` and scores some nesting higher than the whitepaper does.
- If it reports a missing dependency, run the `npm ci` command it prints, once.

Scoring rules, worked examples, and how scores compare with SonarJS and Biome: [references/scoring-rules.md](references/scoring-rules.md). Its scores are equal to or higher than `eslint-plugin-sonarjs`, and with `--biome` equal to or higher than Biome, so code under the limit here also passes those rules.

## Writing new code

Apply these as you write, so the first draft already scores low:

- **Guard clauses and early returns.** Handle the invalid or edge case first and return. The main path stays at nesting 0.
- **Nesting depth ≤ 2.** Logic that would go deeper becomes a named function. Each nesting level adds +1 to everything inside it.
- **Lookup maps over branch chains.** A `switch` or `if`/`else if` chain that picks a value from a key becomes a `Record` or `Map` lookup.
- **One kind of operator per condition.** A condition that mixes `&&` and `||` becomes a named boolean (`const isEditable = isOwner || (isAdmin && !isLocked)`).
- **`async`/`await` with flat `try`/`catch`.** Nested `.then()` callbacks count as nesting levels.
- **Thin handlers.** Lambda handlers, controllers, and use-cases orchestrate. Parsing, validation, and mapping live in small pure functions.

## Explaining a score

1. Run the scorer with `--explain` on the file.
2. Walk the function's breakdown in order. For each line: the construct, its increment, and the nesting that inflated it (`if +3 (nesting 2)` means a base +1 plus 2 for sitting two levels deep).
3. Name the biggest contributors, usually the deepest nesting. Point to the refactor that removes each one.

Done when every point of the score is accounted for in the explanation.

## Refactoring a function

1. Score it and record the **before** score.
2. Refactor using [references/refactor-patterns.md](references/refactor-patterns.md). Go after the largest increments first; flattening nesting usually saves the most. Make the **smallest change** that gets the function under the limit. Functions already within the limit stay as they are, and the refactored code should still be recognisable as the original: same statement order, same names.
3. Hold the **behaviour lock** below for the whole refactor.
4. Re-score. Every function you touched or extracted must be ≤ the hard limit, and the target is ≤ 10.
5. Run the project's tests and type checker.
6. Report **before → after** for each function, for example `processOrder 23 → 8 (extracted validateLines 4, priceLine 3)`. List any suspected bugs you noticed, left unfixed.

Done when every touched function is within the limit, tests pass, the behaviour lock holds, and before → after is reported.

### Behaviour lock

A refactor changes structure only. Behaviour stays identical: same inputs, outputs, side effects, their order, and error cases. When refactoring with LLMs goes wrong, it is usually because the model "improved" behaviour, not because the code broke. Each item below is a change models commonly make by mistake:

- **Literals stay exact.** `3.14` stays `3.14`, not `Math.PI`. `'fizzbuzz'` keeps its casing, and error messages stay word for word.
- **Exported names, signatures and parameter order stay the same.** Extracted helpers are new, non-exported functions.
- **Validation, defaults and error handling stay as they are.** Add none, remove none. Leave unhandled inputs unhandled.
- **Suspicious logic is reported, not fixed.** If `average(a, b)` returns `a + b`, it still does after the refactor. Mention the suspected bug in your report.

## Auditing files

1. Choose scope: the folder the user named, or the changed files:
   ```bash
   git diff --name-only --diff-filter=d HEAD -- '*.ts' '*.tsx' '*.js' '*.jsx' '*.mjs' '*.cjs' '*.mts' '*.cts'
   ```
   Also list untracked files with `git ls-files --others --exclude-standard`. If the list is empty, nothing needs scoring.
2. Run the scorer with `--threshold` at the project's limit on that list.
3. Report each function above the limit with its score and top contributors, worst first. Offer to refactor them.

## After editing TS/JS

Before finishing any task that changed TS/JS functions, score the changed files with `--threshold 15`. A function above the limit gets refactored before you finish, unless the user said to leave it.

To run the scorer automatically after every edit, or to enable an equivalent lint rule: [references/linter-integration.md](references/linter-integration.md).

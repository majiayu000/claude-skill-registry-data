---
name: code-smells-audit
description: Audit a codebase, path, or branch diff for classic code smells against the 56-smell Luzkan catalog (PHP/Laravel and TS/React heuristics). Use when the user asks for a code-smell audit or smell-check of a module or diff.
argument-hint: "[path | glob | diff] (omit for a whole-repo sweep)"
allowed-tools: "Bash(git diff *) Bash(git status *) Bash(git merge-base *)"
---

# Code Smells Audit

Catalog-driven smell detection: instead of ad-hoc reviewer memory, findings are
matched against 56 distilled reference cards derived from Marcel Jerzyk's
[Code Smells Catalog](https://codesmells.org/) and verified against each
smell's actual definition before they reach the report.

## Workflow

Four steps, in order: resolve the target, sweep it lens by lens, verify every
candidate against its card, write the ranked report.

### 1. Resolve the target

The argument decides scope:

| Argument | Scope |
|---|---|
| a path | that file or directory, recursively |
| a glob | files matching it |
| `diff` | the current branch's changes: files listed by `git diff --name-only $(git merge-base <default-branch> HEAD)` plus uncommitted changes (`git status --porcelain`), audit only those files, and only their changed regions when judging severity |
| *(none)* | whole-repo sweep |

Always exclude dependencies and generated code: `vendor/`, `node_modules/`,
lock files, build output, and anything the repo's `.gitignore` ignores. Audit
source, not artifacts.

For a whole-repo sweep, fan out sub-agents by codebase size:

- **Small** (≲100 source files): run the lens passes yourself, sequentially.
- **Medium** (≲1,000): one sub-agent per occurrence lens, each sweeping the
  whole target in parallel.
- **Large**: partition by top-level module or directory, one sub-agent per
  partition running all lens passes; merge candidate lists before verifying.

Each sub-agent gets the target list, this workflow's sweep instructions, and
the index section(s) for the lens or lenses it will sweep, nothing more. In Claude
Code with this plugin installed, dispatch `subagent_type=leek-skills:smell-sweeper`
(read-only, no project CLAUDE.md, a cheaper model); elsewhere, any read-only
sub-agent, on the cheapest model the harness lets you pick: the sweep is recall
only, and verification runs here on the main model.

### 2. Sweep: one detection pass per occurrence lens

Read [references/index.md](references/index.md) first. It groups all 56 smells
under the 9 occurrence lenses with a one-line description each, **the index
is the only source of lens membership; never sweep from a remembered smell
list**.

Run one detection pass per lens. Each pass is armed only with that lens's
one-line descriptions and scans the target for code matching any of them.
When code plausibly matches, record a candidate:

```text
candidate: <smell slug> · <file:line-range> · <one-line evidence>
```

Do not read full cards during the sweep: cards are loaded per candidate in
the verify step (progressive disclosure). Do not judge, rank, or filter yet;
the sweep errs toward recall, the verify step supplies precision.

### 3. Verify: adversarially, against the card

Every candidate must survive re-examination before it may enter the report.
For each one:

1. Read the full card at `references/smells/<slug>.md`.
2. Re-read the candidate code as a skeptic: does it actually meet the card's
   definition paragraph and detection heuristics, or is it a near-miss that
   merely trips a surface signal (length, a keyword, a shape)?
3. **Cite the definition**: a surviving finding must quote or closely
   paraphrase the specific sentence of the card's definition the code
   satisfies; that citation becomes the finding's qualification rationale.
   If no sentence of the definition fits, the candidate fails.
   For a smell that turns on references (Dead Code, Lazy Element, Middle Man,
   Feature Envy, Shotgun Surgery, Speculative Generality), count the call sites
   rather than eyeball them: with a language server (in Claude Code, the `LSP`
   tool's `findReferences` / `incomingCalls`), otherwise `rg` for the symbol,
   and say in the rationale that the count is approximate.
4. Drop candidates that fail the definition, **even if the code is ugly**, 
   taste is not a criterion, the card is. Dropped candidates never appear in
   the report; keep only a count of them for the report header.

While the card is open, capture what the report needs from it: the obstruction
tag (the middle term of the card's taxonomy line) and the card's suggested
refactorings.

### 4. Report: ranked, durable

Write the findings to a markdown file so audits can be compared over time:
`docs/audits/code-smells-<scope>-<YYYY-MM-DD>.md` in the audited repo
(create the directory if needed), unless the user names another path.

Order findings by **judged severity/leverage**: blast radius, how squarely
the definition is met, how likely the code is to be touched again. Judge each
finding on its own; **never use the taxonomy as a severity proxy**: lens and
obstruction are tags for sweeping and reading, not ranks. State the ranking
rationale in one line per finding.

Every finding carries all of:

- **Smell**: the card's title
- **Location**: `file:line-range`
- **Why it qualifies**: the rationale from the verify step, citing the
  card's definition
- **Obstruction**: the card's obstruction tag
- **Suggested refactorings**: from the card

Report skeleton:

```markdown
# Code Smells Audit: <scope>, <date>

Target: <resolved target> · Lenses swept: <n> · Candidates: <n> · Dropped in
verify: <n> · Findings: <n>

## 1. <Smell Name>: `path/to/file.php:12-84`

- **Severity/leverage**: <rank rationale, one line>
- **Why it qualifies**: <citation of the card definition + how the code meets it>
- **Obstruction**: <tag>
- **Suggested refactorings**: <names from the card>
- **Card**: references/smells/<slug>.md (in the code-smells-audit skill)
```

After writing the file, summarize the top findings in the session and point at
the artifact. Slicing findings into tickets is out of scope, hand the report
to the user (or `/to-tickets`) instead.

## Reference material

- [references/index.md](references/index.md), all 56 smells grouped under the
  9 occurrence lenses, one line each; detection passes dispatch from here and
  load full cards only for candidate matches
- `references/smells/<slug>.md`: one card per smell: taxonomy line,
  definition, detection heuristics (agnostic + PHP/Laravel + TS/React),
  example, refactorings, typed related-smell links, aliases
- [references/refactoring-names.md](references/refactoring-names.md), the
  canonical refactoring vocabulary and the normalization map from upstream's
  103 raw names
- [references/ATTRIBUTION.md](references/ATTRIBUTION.md), upstream MIT
  notice and the requested academic citation

## Validating the card set

Run after any card edit, batch addition, or upstream re-sync:

```bash
bash scripts/validate-cards.sh            # strict: all 56 cards must exist (ship gate)
bash scripts/validate-cards.sh --partial  # mid-build: missing cards reported as pending
```

Human-readable status goes to stderr; stdout carries a JSON result:

```json
{"pass": true, "mode": "strict", "cards_present": 56, "cards_pending": 0,
 "checks": 2697, "failures": [], "pending": []}
```

Exit 0 on pass, 1 on failure (each failure names the offending file and
reason), 2 on usage errors. The script embeds the 56-slug catalog, the closed
taxonomy vocabularies, and reads canonical refactoring names from
[references/refactoring-names.md](references/refactoring-names.md); it needs
no network and no upstream clone.

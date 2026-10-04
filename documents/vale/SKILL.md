---
name: vale
description: Audit, write, or revise .vale.ini, or work through vale findings on a repo. Use when adding Vale, troubleshooting silent passes or noisy findings, evolving config, or applying the suggestion → warning → error cleanup cascade after a vale run (interactive or pre-commit failure). Applies the two-hook pre-commit pattern (sync + lint), explicit Packages and per-format BasedOnStyles, scoping/ignores for false positives, and a shared accept.txt vocabulary.
---

# Vale

Config keys: <https://vale.sh/docs/keys/>. Current Vale 3.x key set is: `BasedOnStyles, BlockIgnores, CommentDelimiters, IgnoredClasses, IgnoredScopes, MinAlertLevel, Packages, SkippedScopes, StylesPath, TokenIgnores, Transform, Vocab`. Anything else is stale.

## Comply, don't demote

When a loaded rule fires, **rewrite the prose to comply** — don't demote or disable the rule. A firing rule is usually a real style nit worth adopting; restoring a package default typically costs zero current findings and often surfaces a legitimate fix (`Microsoft.Contractions` catching `does not` → `doesn't`).

Demotion (`= suggestion`), disable (`= NO`), and scoping are the last resort, reserved for rules wrong for the writing style itself:

- `Microsoft.Dashes` wanting tight em-dashes when the project's style uses spaced.
- `Microsoft.HeadingColons` demanding sentence case after a colon when ADR/Nygard convention differs.

Confirm the rule contradicts an intentional style choice before silencing it — inconvenience isn't enough. Tuning from the issue framing ("Vale fights writing, silence the noisy rules") rather than the actual per-finding cost is the failure mode this guards against.

## Defaults

```ini
StylesPath = .vale/styles
MinAlertLevel = warning
Packages = Microsoft, proselint, alex
Vocab = <Project>

[*.md]
BasedOnStyles = Vale, Microsoft, proselint, alex
```

- `StylesPath` — relative to `.vale.ini`. `.vale/styles` keeps the tree hidden. Commit `<StylesPath>/config/vocabularies/`; gitignore the auto-downloaded package subdirectories Vale writes under `<StylesPath>/` on `vale sync`. Migration: Vale 2.x put vocabularies under `<StylesPath>/Vocab/`; 3.x moved to `<StylesPath>/config/vocabularies/`.
- `MinAlertLevel` — `suggestion` (Vale default), `warning`, `error`. Gates **display only**; Vale exits nonzero whenever any error-severity finding exists regardless of this setting. Set it to the lowest level you want printed on interactive `vale .` runs; pass `--minAlertLevel=error` to pre-commit to suppress non-error noise from hook output.
- `Packages` — comma-separated. Names from `vale-cli/packages`, URLs to a `.zip`, or local paths. Resolvable bare names today: `Microsoft, Google, write-good, proselint, Joblint, alex, Readability, RedHat, AsciiDoc, OpenShiftAsciiDoc, Elastic, NoAnimalViolence` (style packages), plus `Hugo, MDX` (config packages that teach Vale about non-standard markup, not rule sets). Local files under `<StylesPath>/` override packages; later `Packages` entries override earlier.
- `Vocab` — see Vocabularies below. References `<Project>` so create the directory plus `accept.txt`/`reject.txt` on greenfield.
- `[*.md]` `BasedOnStyles` — **without a per-format section, no rules from `Packages` actually run and Vale silently reports zero findings.** Add per format you lint (`[*.{md,mdx}]`, `[*.rst]`). The built-in `Vale` style must be listed for `Vale.Terms`, `Vale.Avoid`, `Vale.Spelling` to fire. Disable individual rules with `Style.Rule = NO`.

## Choosing Packages

The Defaults set above (`Microsoft, proselint, alex`) suits technical docs, READMEs, and Diátaxis pages. For that case add two disables to suppress known overlap:

```ini
proselint.Cliches = NO    # overlaps Microsoft.Terms
proselint.Spelling = NO   # Vale.Spelling owns this
```

Microsoft beats Google as the default base because `Microsoft.Avoid`+`Microsoft.Terms` is a longer banned-term list than `Google.WordList`, defaults to `error` on bans (matches pre-commit gating), and adds `Adverbs`/`Wordiness` rules Google lacks. Every Google rule worth keeping (Passive, Headings, We, FirstPerson, Acronyms, Contractions) duplicates a Microsoft one — see Overlaps below.

**Long-form prose / blog.** Add `write-good` and `Readability`; disable the duplicate Passive.

```ini
Packages = Microsoft, proselint, write-good, alex, Readability

[*.md]
BasedOnStyles = Vale, Microsoft, proselint, write-good, alex, Readability
Microsoft.Passive = NO    # write-good.Passive at warning is the keeper
Readability.FleschKincaid = YES
```

`Readability` adds doc-level grade scoring (per-file, not per-finding); thresholds set in-file. `write-good` warns on passive (Microsoft's is `suggestion`) and adds unique `ThereIs`/`Weasel` rules. Pair with the en_GB Hunspell pattern (Troubleshooting) for British prose.

**Short marketing copy / landing pages.** Google over Microsoft here — sentence-case headings fire at `warning`, `Slang`/`Will` rules suit the register. Drop proselint (too noisy on brevity-and-punch copy).

```ini
Packages = Google, alex

[*.{md,mdx}]
BasedOnStyles = Vale, Google, alex
```

**Job descriptions (`careers/*.md`).** Joblint adds 14 unique rules (`Bro`, `Meritocracy`, `Visionary`, `Benefits`, …) absent elsewhere.

```ini
Packages = Microsoft, alex, Joblint

[careers/*.md]
BasedOnStyles = Vale, Microsoft, alex, Joblint
Joblint.Gendered = NO    # alex.Gendered substitutes; Joblint just blocks
```

### Known overlaps

Loading two packages that fire on the same span produces duplicate findings under different rule names. Don't load both unless deviating intentionally:

- `Microsoft.Passive` ≈ `Google.Passive` ≈ `write-good.Passive` — same regex; same span fires 2–3×. Pick one (write-good warns; the others suggest).
- `Microsoft.Acronyms` ≡ `Google.Acronyms` — identical regex and exception list.
- `Microsoft.Headings` ≈ `Google.Headings` — same scope/match; Google at `warning` vs Microsoft's `suggestion`.
- `Microsoft.Contractions` and `Google.Contractions` both *prefer* contractions (not opposite stances).
- `Microsoft.Avoid`/`Terms` ⊃ `Google.WordList`; `proselint.Cliches` overlaps both.
- `Microsoft.GenderBias` ≈ `Google.GenderBias` ≈ `proselint.GenderBias` — same direction, overlapping token lists.
- `Microsoft.Foreign` ≡ `Google.Latin` — both replace `e.g.`/`i.e.`.

### Deviation triggers

- Repo has `careers/` or hiring copy → add `Joblint`, scope via `[careers/*.md]`.
- Long-form blog or essays → add `Readability` + `write-good`; disable `Microsoft.Passive`.
- en_GB / en_AU / en_CA prose → see Troubleshooting (vendor Hunspell, disable `Vale.Spelling`).
- Sentence-case headings wanted as blocking, not suggestion → swap `Microsoft` for `Google`, or keep Microsoft and lower the pre-commit threshold to `--minAlertLevel=warning` for that repo.
- External contributors with varied English fluency → relax most `proselint.*` rules (they default to `error`); keep `alex` — its substitution suggestions teach rather than block.
- Inclusive-language gating only, no voice/tone friction → drop Microsoft/Google; load `alex` alone (~11 warnings, all actionable).
- Per-sentence length nags add noise on non-tutorial prose → disable `Microsoft.SentenceLength`, lean on `Readability` for document-level grade.

## Scoping & ignores

Default package rules trip on inline code, tables, and technical strings. Scope them out without disabling rules wholesale:

- `IgnoredScopes` — inline HTML tags Vale skips entirely. Defaults to `code, tt`. Add `kbd, var` if used.
- `SkippedScopes` — block HTML tags Vale skips. Defaults to `script, style, pre`. Add `figure, blockquote` for untrimmed quoted sources.
- `BlockIgnores` / `TokenIgnores` — regex escape hatches for block and inline content with no HTML tag, for fenced shell prompts and custom MDX directives. **Markdown, reStructuredText, AsciiDoc, Org only.** Both belong inside a format section; at the top level Vale refuses to start with `E201: 'BlockIgnores' is a syntax-specific option`.
- `IgnoredClasses` — by HTML class. Useful for rendered output linting.
- `CommentDelimiters` — comment markers Vale honours for `<!-- vale off -->` directives. Default `<!-- -->`; set to `{/* */}` for MDX where HTML comments don't render.
- `BasedOnStyles` is **additive across sections, not overriding**: a child block's `BasedOnStyles = X, Y` doesn't remove `Z` inherited from a broader block's `BasedOnStyles = X, Y, Z`. To silence a package's rules inside a sub-block, disable each rule explicitly (`Readability.LIX = NO`), not by dropping it from the child's list.
- **Don't lint machine-generated prose.** Auto-managed files (release-please `CHANGELOG.md`, changesets entries, towncrier fragments) are dense and structured by design. Scope them out with a `[CHANGELOG.md]` block disabling `Readability.*` and the stylistic `Microsoft.*` rules (`Contractions`, `FirstPerson`, `HeadingColons`, `Dashes`).

### What markdown tokenises as prose

Which fix a finding admits — backticks, vocabulary, or rewording — depends on what Vale reads as prose:

- **Link text is prose; destinations and autolinks aren't.** A bare path used as link text gets tokenised as words, and hyphens are word boundaries, so `[scripts/truenas-takeout-extract.sh](../scripts/truenas-takeout-extract.sh)` fires `Vale.Terms` on `truenas` and `Microsoft.Wordiness` on `extract`. Backticking the link text clears both. Paths need no `BlockIgnores`/`TokenIgnores` entry — the destination was never linted.
- **YAML frontmatter is prose.** Vale lints `description:` and every other string field. Backticks are literal characters there rather than a code span, so they don't exempt a token, and neither `BlockIgnores` nor `TokenIgnores` reaches the block. Reword the field, or add the term to `accept.txt`.

## Vocabularies

`Vocab = <Project>` enables two implicit rules sourced from `<StylesPath>/config/vocabularies/<Project>/`:

- `accept.txt` → `Vale.Terms`.
- `reject.txt` → `Vale.Avoid`. Flags banned terms.

Both files: one regex per line, case-sensitive, `#` for comments. The built-in `Vale` style must be in `BasedOnStyles` for these rules to fire.

Backticked tokens skip `Vale.Terms`, so prefer wrapping a package ID or code symbol in backticks (`magpie-root`) over whitelisting the bare token in `accept.txt`. Reserve `accept.txt` for terms that appear unbackticked in prose.

A starter `accept.txt` ships next to this skill at `~/.claude/skills/vale/accept.txt` with cross-repo terms (project names, host tooling, languages) and the casing convention in its header. Copy into `<StylesPath>/config/vocabularies/<Project>/` on greenfield; extend per-project.

### Casing

`Vale.Terms` enforces whatever casing a pattern carries, so the canonical form decides which kind a term is:

- **Canonical form carries a capital → bare literal.** `TrueNAS`, `Diátaxis`, `ADRs?`. A lowercase `diataxis` is then an error.
- **All-lowercase canonical form → `(?i)`.** The only casing variation such a term meets is its own sentence-initial capital, which is correct English. A literal `pre-commit` turns "Pre-commit hooks must pass" into an error. Fold inflections into the same pattern: `(?i)repos?`.
- **One entry per term.** Carrying both `alunduil` and `Alunduil` makes Vale pick one canonical form and error on every use of the other.

## Validation (pre-commit)

Two hooks, both `id: vale`. The first runs `vale sync` to install declared `Packages`; the second lints.

```yaml
- repo: https://github.com/errata-ai/vale
  rev: <latest>
  hooks:
    - id: vale
      args: [sync]
      pass_filenames: false
    - id: vale
      args: [--output=line, --minAlertLevel=error]
```

- `sync` first — without it, packages declared in `.vale.ini` aren't installed in the hook's cached env and the lint produces zero findings (silent pass that looks clean).
- **Vendored styles → drop the sync hook.** If the repo commits its packages under `<StylesPath>/` and excludes that path from pre-commit, `sync` has nothing to fetch — keep only the lint hook.
- `--minAlertLevel=error` — overrides the file's `warning` default so only errors block commits.
- `errata-ai/*` repos resolve to `vale-cli/*` on GitHub; vale.sh still publishes `errata-ai/vale` in the canonical example. Both work — match the upstream docs rather than chase the rename in every repo.
- Pair with `markdownlint-cli2` for prose-heavy repos. Vale catches voice/usage; markdownlint catches structure (heading hierarchy, link syntax). No overlap; wire as separate hooks.

## CI gate (diff-aware, reviewdog)

Pre-commit's `--minAlertLevel=error` only blocks errors: vale exits nonzero solely on error-severity findings, so warnings and suggestions accrete silently. To gate warning+ severity *without* a checked-in baseline, pipe vale JSON through reviewdog filtered to the lines the PR changed. New warnings on touched lines block; main's standing debt is ignored.

Pipeline: `vale --output=JSON <set>` → `jq` to rdjsonl → `reviewdog -f=rdjsonl -filter-mode=added -fail-level=warning`.

```yaml
name: Vale

on:
  pull_request:          # added-lines needs a PR diff; reporter needs PR context

permissions:
  contents: read
  checks: write          # github-pr-check writes a check run
  pull-requests: write

jobs:
  run:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@<sha> # v6
      - name: Install vale
        run: |          # however the repo pins vale; no `vale sync` if styles are vendored
          mkdir -p "$HOME/.local/bin"
          script/install/vale --bin-dir "$HOME/.local/bin"
          echo "$HOME/.local/bin" >> "$GITHUB_PATH"
      - uses: reviewdog/action-setup@<sha> # v1.5.0
      - name: Run vale gate
        env:
          REVIEWDOG_GITHUB_API_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          vale --output=JSON <set> > vale.json || true
          jq -e . vale.json > /dev/null   # crash guard: fail if vale emitted no valid JSON
          jq -c '
            to_entries[] | .key as $p | .value[] | {
              message: .Message,
              location: {
                path: $p,
                range: {
                  start: {line: .Line, column: .Span[0]},
                  end: {line: .Line, column: (.Span[1] + 1)},
                },
              },
              severity: ({error: "ERROR", warning: "WARNING", suggestion: "INFO"}[.Severity]),
              code: {value: .Check},
            }' vale.json \
            | reviewdog -f=rdjsonl -name=vale \
                -reporter=github-pr-check -filter-mode=added -fail-level=warning
```

- **Severity map** — `jq` translates vale's `error`/`warning`/`suggestion` to reviewdog's `ERROR`/`WARNING`/`INFO`. `Span[1] + 1` makes the end column exclusive (reviewdog convention).
- **`-fail-level=warning`** fails on warnings **and** errors. Suggestions map to `INFO`, surface as non-blocking `notice` annotations, and don't fail; a PR whose only changed-line findings are suggestions concludes **`neutral`**, not failure.
- **`jq -e .` crash guard** — `vale ... || true` swallows vale's exit code so a real crash doesn't masquerade as "no findings". The `jq -e` parse fails the step if `vale.json` isn't valid JSON.
- **`pull_request` only** — `-filter-mode=added` needs a diff, and `github-pr-check` needs PR context. Pushes to main keep only the pre-commit error gate; that's intended.
- **`vale sync`** — drop it when styles are vendored under `<StylesPath>/`; keep it (as a step) only if packages download at CI time.
- **Reporter choice** — `github-pr-check` writes subtle check-run annotations (used above); `github-pr-review` posts visible threaded review comments. Same gate, louder surfacing — pick per repo's review noise tolerance.

**When warranted:** a check with *both* an exit-code gap (the tool won't fail on the severity you care about) *and* real standing debt on main (a whole-tree gate would be a wall of pre-existing findings). vale's warning/suggestion tiers fit both. Don't bolt it onto a linter that already fails on what you care about and runs clean — that's redundant double-enforcement.

## Cleanup cascade

Sweep findings low-tier to high-tier: suggestions, then warnings, then errors. Fixing a suggestion can introduce a new warning or error (a reworded passive becomes a long sentence; an em-dash adjacent to a link trips `Microsoft.Dashes` via tokenizer normalization). The reverse order risks re-introducing what you just cleared. Suggestions resurfacing during a later pass is fine; warnings or errors resurfacing isn't. Set `MinAlertLevel = suggestion` in-file to see the full backlog on `vale .`; keep `--minAlertLevel=error` in pre-commit so the cascade is opt-in rather than gating commits.

## Troubleshooting

- `vale ls-config` prints the resolved config (StylesPath, loaded styles, per-format sections). First stop for "zero findings but my file is wrong."
- Zero findings + non-empty `Packages` = forgot `vale sync`, or no `[*.<ext>]` section declares `BasedOnStyles`, or `$XDG_CONFIG_HOME/vale/.vale.ini` is overriding a single-valued key. Global config loads *in addition to* project config; multi-valued keys merge, single-valued get overridden.
- Excessive findings on a fresh add = `MinAlertLevel = suggestion` loading every nit. Raise to `warning` in-file; keep `--minAlertLevel=error` in pre-commit.
- `Packages` name not resolving = wrong casing (`write-good` and `alex` lowercase; `Microsoft`, `Google`, `Joblint`, `Readability`, `RedHat` TitleCase) or it's outside `vale-cli/packages` — switch to a URL.
- `--filter` accepts a CEL expression for "which rules fired" debugging; `--no-wrap` disables output wrapping for grep/CI piping.
- **British English (en_GB).** `Vale.Spelling` is en_US. Working pattern: vendor `wooorm/dictionaries` en_GB Hunspell under `<StylesPath>/Custom/`, declare a `Custom.Spelling` rule extending `spelling` with `dictionaries: [en_GB]`, set `Vale.Spelling = NO` per format. Reference exemplar: `~/blog.alunduil.com/.vale/styles/Custom/Spelling.yml`.

## Procedure

1. Confirm any field you plan to write against `https://vale.sh/docs/keys/<field>/` before editing. Memory and prior commits aren't authoritative — Vale 3.x changed several keys vs 2.x.
2. Read `.vale.ini` if present. Note `StylesPath`, declared `Packages`, per-format `BasedOnStyles` blocks, and any `Vocab` references.
3. **Greenfield** — identify the project type (technical docs, long-form prose, marketing copy, job descriptions) and pick the matching recipe from Choosing Packages. Write `.vale.ini` with that recipe; fill `<Project>`. Copy the starter `accept.txt` from `~/.claude/skills/vale/accept.txt` into `<StylesPath>/config/vocabularies/<Project>/`; add an empty sibling `reject.txt`. Add the two-hook pre-commit entry. Run `vale sync` locally to confirm packages resolve.
4. **Audit existing** — walk the Defaults block and flag drift:
   - `[*]` instead of `[*.<ext>]` (fires on code files without `CommentDelimiters`)
   - Silent passes from missing `BasedOnStyles`
   - Declared `Packages` without `vale sync` in pre-commit
   - `Vocab` referenced from `.vale.ini` but missing on disk
   - Vale 2.x `<StylesPath>/Vocab/` path (migrate to `<StylesPath>/config/vocabularies/`)
   - Disabled rules without an inline comment explaining why
   - `MinAlertLevel = suggestion` driving pre-commit noise
   - Packages loaded with known overlap (Microsoft + Google, Microsoft + write-good, proselint + write-good) without the duplicate-rule disables — see Choosing Packages
5. Surface findings before editing. Apply only after scope is agreed.

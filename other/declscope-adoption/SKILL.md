---
name: declscope-adoption
description: Adopt declscope on an existing Go codebase and drive its diagnostics to zero. Read this when introducing declscope to a repository, when choosing its configuration, when running declscope shrink for the first time, or when clearing a declscope baseline. Covers sizing each rule before enabling it, reading the diagnostics as structure, the remedy for each shape, and the measurement traps that produce false confidence. For writing new code in a repository that already runs declscope, use declscope-authoring.
license: MIT
x-embedded-by: declscope
x-embedded-version: 0.23.0
x-embedded-at: "2026-10-22T22:08:20Z"
x-embedded-digest: "sha256:7865717cda173adcc76e4d3df5150243399f226a6233a104bffbf31588543c1d"
---

# Adopting declscope

Written against **declscope 0.23.0**. Check the version first with `declscope -V=full`: this describes how that release behaves, not how an older one does.

**Read [the README](https://github.com/mpyw/declscope#readme) before the first decision.** This skill covers what to do about the diagnostics. What each directive means, and what the config accepts, is there.

This skill is for introducing declscope. Placing, scoping and naming individual declarations is [declscope-authoring](../declscope-authoring/SKILL.md), installed beside this one. Read it before step 3 of the [order of work](#order-of-work), and before any rename.

## Check what is switched on

A count of zero may mean nothing is checked. These are the defaults:

| Setting | Default | |
| --- | --- | --- |
| `rules.naming.qualify` | `never` | The naming rule is **off** |
| `rules.naming.exported` | `false` | Even when on, it skips exported declarations |
| `rules.surplus` | `strict` | The surplus rule is **on** and judges each declaration a directive widens. `loose` judges a directive as a whole; `off` turns it off |
| `rules.boundary` | `on` | The boundary rule is **on**. `off` stops checking reach; set `surplus: off` alongside it |
| `rules.unused` | `strict` | The unused rule is **on**. It reports an ignore that silenced nothing, and a scope directive that restates the scope in force. `loose` reports a scope directive only when no configuration could make it bind; `off` turns it off. Malformed directives are the `directive` rule's, which is always on |
| `filter.only` | None | When set anywhere in the chain, files outside it are never read |

The config is looked up from each analyzed package's directory **upwards**, so a subtree can carry its own and a repository can have several. Find them all, and do not read the root alone:

```bash
declscope survey ./...   # Checks in force: one row per config chain, with what it switched on
```

That answers it directly. To read the files themselves:

```bash
find . -name '.declscope.y*ml' -not -path './.git/*' \
  -exec sh -c 'echo "== $1"; cat "$1"' _ {} \;
```

Finding a config is not the answer on its own. One that never sets `qualify` leaves the naming rule off, and one that sets `boundary: off` leaves off the rule this tool exists for.

**The files compose, so the nearest one does not tell you what applies.** Every file between the package and the module root is read, outermost first. A nearer file owns the keys it states and inherits the rest.

`filter` is the exception to that: `only` intersects down the chain and `omit` unions, so a config file can only ever shrink what is read. A root `omit` holds everywhere below it, and no nested file undoes it.

Each file's patterns are read against **its own** directory, and anchor there when they hold a separator. `gen/**` in the root and the same line in a nested file name different directories. A bare name and a leading `**/` float instead, and a `..` in a pattern is an error.

### Start at the default, and offer the rest

**Ask before any config change**, as [declscope-authoring](../declscope-authoring/SKILL.md#do-not-hide-a-report) says. That includes the first config file. Wait for an answer before changing any code, too.

**The minimum is no config file at all.** `boundary`, `surplus: strict` and `unused: strict` are on. They check reach and whether directives still change anything; the naming rule checks a convention. Adopting this much is a complete adoption.

**Size the default `surplus` findings before changing code.** `loose` judges a `//declscope:shared` as a whole, so one reached declaration keeps the whole directive quiet. The default `strict` also reports each declaration the directive widens for nothing, and one `declscope -fix` run inserts every `//declscope:private` it asks for. If the owner wants the narrower check, set `surplus: loose` explicitly.

```bash
declscope survey -format=json ./... | jq .totals.surplus.found
```

An explicit `-config` replaces the repository's own config. Copy its keys in first when measuring a different mode.

**Size the default `unused` findings too.** Under `loose`, a `//declscope:private` that names the scope `defaults.unexported` gives is kept, since another default could make it bind. The default `strict` reports it, and one `declscope -fix` run deletes it. When changing `defaults.unexported`, expect reports for directives that restate the new default. If the owner wants to keep those explicit decisions, set `unused: loose`.

**If the goal is a tidier codebase, offer the naming rule on top.** It is a convention. It fires where nothing is wrong, and it costs real work. Size it before offering, with a throwaway config rather than by counting message fragments:

```bash
printf 'rules:\n  naming:\n    qualify: ondemand\n    exported: true\n' > /tmp/q.yaml
declscope survey -config /tmp/q.yaml -format=json ./... | jq .totals.qualify.found
```

```yaml
rules:
  naming:
    qualify: ondemand   # ask once a package holds a second namespace
    exported: true      # reach exported names too, since inside the package they read as bare
```

| | Measured |
| --- | --- |
| Default, no config | Measure in the repository being adopted |
| `qualify: ondemand` | 89 in one repository whose boundary count was zero |
| plus `exported: true` | 1008 in a large one |
| `qualify: always` | More again, including single-unit packages where a prefix distinguishes nothing |

Put the numbers in front of the person deciding, rather than describing the settings:

```bash
for q in never ondemand always; do
  printf 'rules:\n  naming:\n    qualify: %s\n    exported: true\n' "$q" > /tmp/q.yaml
  printf '%-9s %s\n' "$q" "$(declscope survey -config /tmp/q.yaml -format=json ./... | jq .totals.qualify.found)"
done
```

Some reports will be names that spell the namespace in another form, such as `traceValue` in `tracing.go`. The message names a `rules.naming.vocabulary` key for those. Propose the entries in the same question as the naming rule, and do not count them as renames. When to list a word and when to move code instead is in [When the name spells the namespace in another form](../declscope-authoring/SKILL.md#when-the-name-spells-the-namespace-in-another-form).

Every count in the rest of this skill assumes `qualify: ondemand` with `exported: true`. That is what the numbers were taken under, not a recommendation.

## Shrink the exported surface first

**`declscope shrink` reports the exported declarations of `internal/` packages that nothing outside their package uses.** With `-fix` it unexports them. The analyzer cannot answer this: it reads one package, and any importer might use an exported name. Inside `internal/`, Go limits the importers to one directory tree, so `shrink` loads the whole module and sees every one of them.

An exported name inside `internal/` claims that another package depends on it. Where nothing does, the claim is false, and it hides the declaration from the rest of declscope. An exported declaration takes shared scope by default, so no boundary is ever reported on it. Unexported, it takes `private`, and the analyzer checks who reaches it.

### Run it before the analyzer

**Run `shrink`, and apply its fixes, before you work on the analyzer's reports.** A declaration it unexports becomes private to its namespace. Wherever another file of the package uses it, the analyzer then reports a boundary crossing that was not there before. Fixing in the other order means a second round.

This happened when declscope held itself to `shrink`. The fix unexported twelve declarations, and nine of them were used from other files of their package. The analyzer then needed nine `//declscope:shared` directives to state those crossings.

| Step | Command |
| --- | --- |
| 1. Read what `shrink` reports | `declscope shrink ./...` |
| 2. Unexport, once the owner agrees | `declscope shrink -fix ./...` |
| 3. Confirm the build | `go vet ./...` and `go test ./...` |
| 4. Read what the analyzer now reports | `declscope ./...` |
| 5. State or move each new crossing | See [What each shape means](#what-each-shape-means) |

Ask before step 2, the same as any other change. The fix renames every identifier naming the declaration, all inside its own package, and the doc comment that opens with the name.

**When the owner cannot settle `shrink` yet, baseline it.** `declscope baseline ./...` records `shrink`'s reports with the analyzer's, and `shrink` then passes on them in CI. It is the same deferral as any baseline, and [the same rules](#a-baseline-is-for-arriving-not-for-staying) apply. A repository that does not run `shrink` passes `-shrink=false`, which skips the extra load.

### Reading what it reports

What each report asks of you, and where `shrink` stands down, is in [Reading what shrink reports](../declscope-authoring/SKILL.md#reading-what-shrink-reports). It is not a rule the analyzer runs, so `go vet` and golangci-lint never report it.

**Deleting unused code is not `shrink`'s job.** Once a declaration is unexported, staticcheck's `unused` and gopls' `unusedfunc` report it when nothing uses it. Run them after `shrink`, not before.

### Keep it in CI

Run it before the analyzer there too, so that a failure reads in the order it is fixed. It exits 3 when it reports anything.

```yaml
- run: declscope shrink ./...
- run: declscope ./...
```

## The two kinds of report

The analyzer reports two things, and `shrink` a third. **Read them separately.**

| Rule | What it means |
| --- | --- |
| `boundary` | A file reaches a declaration another file holds. A property of the code |
| `qualify` | A name does not carry its file's namespace. A convention |
| `overexported` | An exported name inside `internal/` that nothing outside its package uses. Only `declscope shrink` reports it, and it goes [first](#shrink-the-exported-surface-first) |

Boundary first. It is the one that points at structure.

## Measure before deciding

A count is not a work list. Group it first. Use two commands, not `grep`.

```bash
declscope survey -format=json ./...           # which package to open first
declscope inspect -format=json <that package> # what shape it is in
```

`-format` takes `markdown` (the default, readable in a terminal and paste-ready) or `json`. Read the JSON.

Add `-test=false` once the first pass is read. In a large package, most of what crosses is test scaffolding. `export_test.go` reaching internals is what that file is for. It sorts above the crossings worth acting on.

**`survey` refuses to print a count it cannot stand behind.** It stops on a package that does not type-check, or that imports one that does not.

It reports what was in force before anything else:

- which config governed which packages;
- whether each rule was on;
- how many entries a baseline holds.

A rule that was not asked prints `-`, never `0`. That includes a rule that stood itself down. `surplus` does so for a package holding a generated, assembly or cgo file, or a build-excluded file of its own package. It does so too under `-test=false` when the package has in-package tests.

`-allow-errors` continues past a package that does not compile. The `type check` row counts it, a list under the Checks table names it with its first error (or names the failing dependency and its error), and it is given no row, so nothing in the tables reads as a clean result for it.

Do **not** move the baseline aside to measure: `survey` reports `baselined` as its own column, so what is suppressed and what is left are visible at once. Do not count message fragments either; the wording of a diagnostic is not an interface, and the JSON is.

| What you need | Where it is |
| --- | --- |
| Is anything even being checked | `checks.configs[].rules`, `checks.typeCheck` |
| Which package to open | `packages[]`, already sorted; the first row is the heaviest |
| Is this deferred or decided | `boundary.baselined` against `boundary.declared` |
| Which two namespaces to merge | `inspect`'s `crossings[]`, one row per ordered pair, with `clears` |
| Where the structure is | `inspect`'s `edges[]`, one row per declaration **and reaching namespace** |
| Where a name is wrong | `inspect`'s `names[]`, with `fixable` saying whether `-fix` would rename it |

**`clears` is the number the decision turns on.** A crossing's `reached` says how much of a namespace it touches. `clears` says how many findings would go away if the two became one namespace. It is smaller whenever a third namespace reaches the same declaration. Rank the work by `clears`, not by `reached` or `uses`.

**`edges[]` does not count findings.** One declaration reached from three namespaces is three rows and one finding, so the rows always outnumber `findings.boundary.reported`. Count distinct `declaration` values, or read `crossings[]`, or read the tally.

An edge's `state` (`edges[].state`) is one of six:

| State | Meaning |
| --- | --- |
| `reported` | A finding, printed |
| `baselined` | A finding, absorbed by the baseline |
| `ignored` | A finding, silenced by an ignore |
| `declared` | No finding: a `//declscope:shared` says it is shared |
| `open` | No finding: shared because nothing says otherwise, which is most exported API |
| `unchecked` | No finding: `rules.boundary` is `off` |

**Nothing reported, much baselined and nothing declared means nobody has decided.** Such a package reads as clean under the analyzer alone. That is why `declared` is a column.

Boundary violations cluster. Measured across eight repositories, one structural decision cleared between 10 and 100 entries every time. In one repository 34 of 35 sat in a single namespace.

**Start where the count is concentrated, not where it is large.** The row order does not give you that. Rows are sorted by how much is undecided, which is size. Concentration is the `largest crossing` column. A package with 12 findings over 6 namespaces sorts above one with 4 in a single crossing. The second is where one decision clears the cluster.

### Reading a saturation

**This needs the naming rule switched on.** It is off at the default configuration. Then `qualifyTargets` is `0`, `names[]` is empty and every ratio prints `-`. Measure with the throwaway config above before reading what follows.

`inspect` reports, per namespace, how many of the declarations the naming rule examines there fail it. The ratio says which thing is wrong, and the answer is rarely the rename the diagnostic suggests.

| Saturation | What is wrong | The answer |
| --- | --- | --- |
| Nearly all of them | The **namespace name** | `//declscope:namespace`, or rename the file |
| Around half | One file holding several concerns | Split the file |
| One or two | Those declarations | Rename them |

A baselined finding counts toward it: the baseline defers a decision rather than settling it, so regenerating one moves this number without a line of code changing.

## What each shape means

| The diagnostics say | The code is | Do this |
| --- | --- | --- |
| File A's declarations are nearly all used from B, and nothing goes back | A is B's working parts, not a layer under it | `//declscope:namespace <B>` on A |
| A and B reference each other both ways | One device split across two files | Give both the same namespace and rename to say so |
| A type's fields are read from four files | One type filed by concern | The files share a namespace, or join the core |
| Calls run one way through three files | A pipeline, and the layers are real | Keep the files. Declare only what crosses, with the reason |
| `pkg.Foo` is asked to become `pkg.PkgFoo` | The file is the package's API | `//declscope:core` |
| One helper is used from several files | Shared on purpose | Move it to a file named for its concept, then `//declscope:shared // why`. See [Where a new declaration goes](../declscope-authoring/SKILL.md#where-a-new-declaration-goes) |
| A name reads badly with its namespace in it | Often the file name, not the declaration | Rename the file |

**Two rows can fire on one cluster.** A mutual pair whose declarations four other namespaces also read matches both the second row and the third. Take the one with the larger `clears`. Merging two namespaces settles only what no third namespace reaches. So the fan-in case is usually the smaller change, and the core case the larger.

That last row is worth its own note. In one repository a single file held three concerns, and splitting it into three cleared every entry in that cluster **without renaming a single declaration**. The file name was the thing that was wrong.

## Scopes and names of single declarations

Once the structure is settled, what is left is per declaration. Field scopes are in [Shared structs](../declscope-authoring/SKILL.md#shared-structs-private-fields), and names in [Naming](../declscope-authoring/SKILL.md#naming). During an adoption, one `declscope -fix` run under `surplus: strict` adds every field directive the structs need. Moving those fields to the end stays manual.

## Do not turn the check off

**Never set `rules.boundary: off` to reach zero.** Every count after it is meaningless. It is the repository owner's choice, for a repository that wants the ownership mark in a name without the scope behind it. It is never a step in an adoption. A baseline is one, because it records what the code already has and still reports what is new. The other shortcuts are in [Do not hide a report](../declscope-authoring/SKILL.md#do-not-hide-a-report).

Marking every file in a package core leaves no boundary and no naming check there. What core does is in [Where a new declaration goes](../declscope-authoring/SKILL.md#where-a-new-declaration-goes).

**Count it.** A package where every file is core needs a reason you can state in one sentence. There should be few of them.

```bash
for d in $(find . -name '*.go' -not -name '*_test.go' | xargs -n1 dirname | sort -u); do
  n=$(ls $d/*.go 2>/dev/null | grep -vc _test)
  c=$(grep -l "declscope:core" $d/*.go 2>/dev/null | grep -vc _test)
  [ "$n" = "$c" ] && [ "$n" != "0" ] && echo "all core: $d"
done
```

Two of nine repositories reached zero without using `core` at all. One solved its worst cluster by promoting a file to its own package, because the file already documented itself as temporary and had one caller. A package boundary was the honest answer, and no directive could have said it.

## A baseline is for arriving, not for staying

`declscope baseline ./...` records what exists so that new code is held to the rule. It suppresses and does not endorse.

If the goal is zero, delete the file rather than regenerating it. An empty baseline left in the tree says nothing.

## Traps

These cost real time. Each was measured, not guessed.

**Measure through `declscope survey`.** Why a bare count misleads, and the bulk-rename trap, are in [Traps](../declscope-authoring/SKILL.md#traps).

**A zero may be the filter, not the code.** A `filter.only` anywhere in the chain can leave a package with nothing to read. A package nothing was read from reports nothing. `declscope` says so only when a nested `only` was cancelled by one above it, so the quiet cases stay quiet. Fix that report in the config chain: a `//declscope:ignore filter` silences nothing, and the `unused` rule reports it. `declscope inspect` lists the files each namespace was built from (`namespaces[].files`); a package whose files are missing from it is one the filter removed.

**A zero from `boundary` may be the switch, not the code.** `rules.boundary: off` silences the rule entirely, and the run looks like a clean repository. Read every config before reporting a count, the same way you would for `qualify`.

**`-fix` widens**, as [declscope-authoring](../declscope-authoring/SKILL.md#acting-on-a-diagnostic-your-change-caused) explains. Over a whole codebase that is the wholesale widening step 3 of the order of work exists to avoid. In an adoption, use it only for renames after the structure is settled, where `names[].fixable` is true.

**A dirty working tree poisons a comparison.** Measuring option A, then option B without reverting, measures A and B together. `git stash` leaves untracked files behind, so a new file from the previous attempt stays. Copy the tree instead:

```bash
cp -r repo /tmp/try-a   # and measure there
```

## Order of work

1. `declscope survey ./...`, and read Checks in force before any count
2. If the repository has `internal/` packages, run `declscope shrink ./...` and settle it before anything else. Its fixes add boundary reports, and nothing that follows adds reports back
3. Clear `boundary` by moving the boundary, not by widening everything
4. Re-measure with `survey`. Naming often falls with it, since merging two namespaces into one takes `ondemand` out of force
5. Fix the file names that do not match their contents
6. Rename what is left, following [Naming](../declscope-authoring/SKILL.md#naming)
7. Delete the baseline
8. Check the core count, and `go vet`, `go test`, `declscope shrink` and `declscope` in that order

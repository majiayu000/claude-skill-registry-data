---
name: excavate
description: "User-invoked side-route for onboarding to a legacy repo with no docs/solutions/, research archive, or written decisions. Mines the last 12 months of git history and, when gh is available, PR bodies and review threads, into ranked hotspots, cited recovered decisions, and a who-to-ask map, then offers a PR of docs/solutions/ entries. Not for repos that already compound, not for judging people, not model-invoked."
disable-model-invocation: true
sources:
  primary:
    - "Your Code as a Crime Scene — Adam Tornhill"
  secondary:
    - "Working Effectively with Legacy Code — Michael Feathers"
    - "Code Reading: The Open Source Perspective — Diomidis Spinellis"
    - "Engineering a Safer World — Nancy Leveson"
    - "Fundamentals of Software Architecture — Mark Richards & Neal Ford"
    - "The Programmer's Brain — Felienne Hermans"
---

# Excavate

Recover what a legacy repo already knows about itself before the first feature
runs blind on it. The output is an **off-tree dossier** (hotspots, coupling,
recovered decisions, a who-to-ask map, and a Coverage block saying what the
history could and could not tell you) plus an **opt-in PR of `docs/solutions/`
entries** in `/compound`'s format, so `/research`, `/write-a-prd`, and `/execute`
read them through the keyword grep they already run.

Two things keep this honest. Tornhill's method mines version control as a
*behavioral* record: a hotspot is the intersection of change frequency and
complexity, neither axis alone, bounded to a fixed window, and it is a
probability to inspect, not a verdict to act on. And the Grounding Rule
(`references/visual-rendering-core.md` § 1) splits every artifact: SHAs, PR
numbers, paths, counts, and quoted rationale are copied from `git` and `gh`
output, never retyped; the model writes only the prose around them. A decision
whose "why" is the model's guess is not recovered, it is invented, and it stays
out of the repo.

## Invocation Position

**Side-route, user-invoked only.** It fires when a human types `/excavate`;
`disable-model-invocation: true` keeps its description out of every other
session's context, because it is typed once per repo, at onboarding, and never
has a reason to self-trigger. Planning mode, HITL throughout; there is no AFK
path, because every commit-bound item needs a human to read the quote it rests
on.

Send it as its own message, not as the first message of a fresh workspace. A
hidden skill typed into a first message that a host prepends a preamble to is
read as prose and never loads; `/lfg`'s Invocation Position records the field
incident (#383). Retype it as a second message.

Use it when a repo has history but no `docs/solutions/`, no research archive
entry, and no written decisions, and you are about to start feature work in it.
`/help` recommends it on that signal. Do not use it on a repo the pipeline
already compounds (run `/compound` there), as a performance review of anyone
(see § 5), or as a defect finder (`/qa` and `/triage-issue` own that).

It stands beside the main pipeline and **reconnects at `/shape`**: the first
feature is shaped with the dossier and entries in hand. It may instead hand off
to `/request-refactor-plan` when the top hotspot is the work, or to `/qa` when
history shows a fix-labeled cluster that never closed.

## Method rules

These are the rules the process below operationalizes. Each points at where
it comes from; none is restated elsewhere in this file.

- **Rank by revisions, qualify by lines of code, never one axis alone.**
  Frequency without size flags config files; size without frequency flags code
  that was debugged into correctness years ago and never touched since
  (Tornhill, Ch. 1-4). LOC via `wc -l` is the complexity proxy: no `cloc` is
  assumed, and LOC is the proxy the book defaults to.
- **Bound to a fixed window.** A raw revision count is meaningless without a
  reference period. Twelve months is the default; shrink it for high-velocity
  repos. Print the actual window.
- **Expect a power law and cut at the knee.** A handful of files hold most of
  the cost. Stop where the curve levels off, never at a round number.
- **A trend needs complexity *and* size.** Deteriorating means indentation
  complexity rising faster than LOC; Refactored means both falling; Stable means
  both flat (Tornhill, Ch. 5-6). LOC alone cannot yield these labels.
- **Filter non-domain files before coupling; classify every coupling before
  reporting it.** Lockfiles, manifests, generated and vendored code are false
  positives. A test coupled to its subject is intentional and is dropped;
  copy-paste, unsupportive-boundary, and producer-consumer couplings are kept
  and labeled (Tornhill, Ch. 8-9). Squashed history destroys commit-level
  coupling; use PR-level change sets or say the section is unavailable.
- **Hotspots are probabilities.** Open the file before naming a mechanism, and
  offer no entry for a file you did not open.
- **Ownership data has four legitimate uses**: finding a reviewer, onboarding,
  deciding where tests go, and judging whether a structure fits the team. It is
  never used to rank or evaluate people, and it is read through `.mailmap`
  with bots and the initial import excluded (Tornhill, Ch. 12-14).
- **Existing documentation is aspirational.** An ADR, README, or CHANGELOG claim
  is verified against the current tree before it is recorded as a standing
  decision (Spinellis, *Code Reading*).
- **The first move on a hotspot is a characterization test at a pinch point**,
  not a refactor (Feathers, *Working Effectively with Legacy Code*). The
  dossier's "Suggested first moves" section says this per hotspot.
- **A hotspot is selected for being extreme, so part of its rank is noise.**
  Regression to the mean is the null hypothesis: a file that tops one window
  may be average in the next with nothing done to it, and a file that cooled
  after a refactor would have cooled anyway (Galton; Kahneman). Rank on
  persistence across both halves of the window, tag each hotspot `persistent`
  or `single-window`, and route only persistent ones to the first-moves list.
  The ranking is a diagnostic, never a target; a team that sets goals on it
  gets gaming, not quality (Goodhart).
- **Record the assumption next to the decision.** Rationale is forgotten
  fastest, and unrecorded assumptions harden into numbers nobody dares change
  (Leveson, *Engineering a Safer World*, Ch. 10). Each recovered decision
  carries the constraint its quote states ("chose X because Y, assumed Z"),
  and whether Z still holds in the tree is the reversal detector.
- **A decision entry has an ADR's shape and a compliance line.** Title,
  status, context, the decision with its *why*, consequences, and how it is
  verified; without the last, a record is archaeology rather than governance
  (Richards & Ford, *Fundamentals of Software Architecture*, Ch. 19). The
  verification here is the grep or path check run against the current tree.
- **The dossier is read by a newcomer under the curse of expertise.** Lead
  with a short glossary and the knee hotspots, keep the full tables behind
  them, and make the first welcome task *understand and summarize* a hotspot's
  recovered decision rather than fix it (Hermans, *The Programmer's Brain*).

## Process

Every fenced block below runs as written. Each Bash tool call is a fresh shell,
so no variable survives from one call to the next. The Step 0 variables block
runs once; the block after it writes every resolved value to `$WORK/vars.sh`,
and every later shell, yours or a miner's, begins with `. "$WORK/vars.sh"`
instead of re-running Step 0, which would reset `SINCE` to its default and
discard a `--since` or a `NONDOMAIN` extension. A shell that skips the file
fails without an error: `git log --since=""` returns no commits and
`grep -Ev ""` prints nothing, and empty output reads as the valid answer "no
reverts". `WORK` is a path derived from the repo, so a new shell re-derives it
with the `WORK=` expression from Step 0 and sources the file under it; the
miners are handed the absolute path to `vars.sh` in their brief rather than
inheriting any variable. `<path>` is the one placeholder,
substituted per hotspot.
Flag semantics are the tool's own documentation
([git-log](https://git-scm.com/docs/git-log),
[git-shortlog](https://git-scm.com/docs/git-shortlog),
[git-rev-parse](https://git-scm.com/docs/git-rev-parse),
[gh pr list](https://cli.github.com/manual/gh_pr_list)); this file does not
paraphrase them. `scripts/test-documented-git-commands.sh` runs each git block
against a planted fixture, so a block that stops being a valid invocation fails
in CI.

### 0. Preflight

Parse the arguments: `--since <date>` (default `12 months ago`; any form
`git log --since` accepts) and `--paths <pathspec>...` (replaces the `.` in
every block below). Then set the shared variables:

```bash
SINCE='12 months ago'
WORK="${TMPDIR:-/tmp}/excavate-$(git rev-parse --show-toplevel | cksum | cut -d' ' -f1)"
mkdir -p -m 700 "$WORK"
START=$(git log --since="$SINCE" --no-merges --format=%cs HEAD </dev/null | tail -1)
NONDOMAIN=(':(exclude)*.lock' ':(exclude)*package-lock.json' ':(exclude)*pnpm-lock.yaml' ':(exclude)*yarn.lock' ':(exclude)*.min.*' ':(exclude)*.snap' ':(exclude)*.generated.*' ':(exclude)CHANGELOG.md' ':(exclude)*/vendor/*' ':(exclude)*/node_modules/*')
BOTS='[[]bot[]]|dependabot|renovate'
MAXFILES=30
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.quotePath GIT_CONFIG_VALUE_0=false
```

The `GIT_CONFIG_*` export sets `core.quotePath=false` for every git call in this run (see [git-config, Environment](https://git-scm.com/docs/git-config#ENVIRONMENT)), so a path with non-ASCII bytes prints as itself rather than as a quoted escape that `wc` and the joins below cannot open or match.

`START` is the first in-window commit date, derived from git rather than from
`date`, because `date -d` is GNU-only and `date -v` is BSD-only. `NONDOMAIN`
is a starting list: extend it with this repo's generated, vendored, snapshot,
and mirrored paths before Step 1 (check `git check-attr linguist-generated
linguist-vendored` on anything suspicious). `MAXFILES` is the changeset-size
ceiling above which a commit is treated as a bulk sweep (reformat, import,
mass rename) and excluded from frequency and coupling counts. The shared log in
Step 2 applies it once, when the log is built; no later block repeats it.

`WORK` is keyed on the repo's top-level path, not on `HEAD`, because Step 8
moves `HEAD` onto the docs branch; it stays valid across shells and is removed
in Step 9. If a directory from an interrupted run is already there, delete it
before the first Step 2 block so stale files cannot pass for this run's output.

Persist the resolved values once `NONDOMAIN` is extended (and again after the
Step 1 gate, if the user changes the window: source the file, set `SINCE`,
re-run Step 0's `START=` line, then run this block again):

```bash
{
  declare -p SINCE START NONDOMAIN BOTS MAXFILES WORK
  declare -px GIT_CONFIG_COUNT GIT_CONFIG_KEY_0 GIT_CONFIG_VALUE_0
} > "$WORK/vars.sh"
```

Then measure coverage, in a shell that begins with `. "$WORK/vars.sh"`:

```bash
git rev-parse --is-shallow-repository
git rev-list --count --since="$SINCE" --no-merges HEAD
git log --max-parents=0 --format=%cs HEAD </dev/null | sort | head -1
git log --since="$SINCE" --no-merges --format=%s HEAD </dev/null | awk '{ t++ } /\(#[0-9]+\)$/ { s++ } END { printf "%d of %d subjects end in (#N)\n", s, t }'
```

The four lines are: shallow or not, commits in the window, root-commit date
(the shallow boundary if shallow, so say "unknown" then), and the squash ratio.
A high squash ratio means each commit is a whole PR, so commit-level coupling
is PR-level coupling already; a low ratio with squash-merged PRs elsewhere is
the case to watch. Probe `gh auth status` and whether the remote is GitHub;
record `gh: yes` or `gh: no`. Look for a prior
`~/.claude/research/<repo-slug>/excavation-*.md` and an existing
`docs/solutions/`; a rerun updates entries rather than duplicating them, and
scores the prior dossier's `persistent` tags against the new window (how many
stayed hot) so the Coverage block carries a hit rate for its own predictions.
`<repo-slug>` follows `/research`'s rule: `owner-name` from the git remote.

If the repo is shallow, say how much history is missing and offer
`git fetch --unshallow`; never run it, since it rewrites `.git`.

### 1. Scope gate (HITL)

Print the **Coverage block** exactly as it will head the dossier:

```
Window:        <START> → today (<SINCE>)
Commits:       <N> non-merge (<M> excluded as bulk > MAXFILES files)
Shallow:       yes | no
Squash ratio:  <s>/<t>
gh:            yes (<fetched> of <total> merged PRs; <closed> closed unmerged) | no
Fix labels:    <k> of <N> commits match the fix pattern (a lower bound; filled in at Step 3)
Excluded:      <NONDOMAIN list, one line>
Not visible:   closed-unmerged PRs, force-pushed or squashed history, deleted files, departed contributors
```

The `Not visible` line is not boilerplate. Everything below ranks survivors
of the window; what was reverted before merge, rewritten at squash, or
deleted outright left no trace in the log and is exactly the evidence that
would change a conclusion (Taleb, survivorship). Fill it in with what this
repo's history actually hides, and keep the merged-to-closed PR ratio in the
`gh` line so a pattern read from survivors has a denominator.

Then one `AskUserQuestion`: proceed, narrow with `--paths`, or change the
window. Below roughly forty in-window commits, offer to widen to the last N
commits instead and say so in the block; a dormant repo still has a history,
it just is not in the last year.

If the answer changes the window, persist the new values before Step 2 (the
block after the Step 0 variables does it), so the miners read the window the
user approved.

### 2. Build the shared log and dispatch the miners

One scoped, filtered log feeds every analysis, so the window, bot filter, and
exclusions cannot drift between them:

```bash
git log --since="$SINCE" --no-merges --name-only --date=short --pretty=format:'@@%H%x09%aN%x09%ad%x09%s' -- . "${NONDOMAIN[@]}" </dev/null \
  | awk -v bots="$BOTS" -v max="$MAXFILES" '
function flush(   i) { if (hdr != "") { print hdr; if (n <= max) for (i = 1; i <= n; i++) print f[i] } hdr = ""; n = 0 }
/^@@/ { flush(); split($0, h, "\t"); skip = (h[2] ~ bots); if (!skip) hdr = $0; next }
skip  { next }
NF    { f[++n] = $0 }
END   { flush() }' > "$WORK/log.txt"
```

The bot test reads the author field only, so a human commit whose subject
mentions a bot survives. The bulk cutoff is applied here, once: a commit over
`MAXFILES` files keeps its header but loses its file lines, so it still
counts as a commit by a named human (the scrub list and the median date below
read headers) and contributes to no file count or pair. `%aN` reads `.mailmap` ([gitmailmap](https://git-scm.com/docs/gitmailmap)), so
two spellings of one person collapse if the repo maps them; if it does not,
note the duplicates in the dossier rather than guessing which are the same
person.

The scrub list is built from the same log, in the same step, so it exists
before anything downstream needs it:

```bash
awk -F'\t' '/^@@/ && $2 != "" { print $2 }' "$WORK/log.txt" | sort -u > "$WORK/names.txt"
```

The log already dropped bot commits, so the file lists only human `%aN`
values. `[ -s "$WORK/names.txt" ]` must hold before the miners are dispatched:
a window with no human commits has no scrub list, and an empty list is a
failure to report, not a clean result. When `gh` is available, the PR author
logins (`jq -r '.[].author.login' "$WORK/prs.json"`) and every reviewer and
commenter login that Miner B reads are appended to this same file as they are
fetched, then `sort -u` is re-run over it with blank lines removed, because
one blank line in an `rg -F -f` pattern file matches every line.

Now dispatch **two sub-agents in parallel** with the `Agent` tool. Both read
`$WORK/log.txt`; neither re-runs `git log` with its own window. Each is handed
the absolute path of `vars.sh` and begins every shell with `. <that path>`
before running any block, because a miner's shell has none of the variables the
blocks read. Each returns the paths it wrote plus a ten-line summary, not the
data.

- **Miner A, hotspots** (deterministic shell; it runs the blocks in Steps 3 and
  5 and writes `freq.txt`, `fix.txt`, `loc.txt`, `hotspots.txt`, `pairs.txt`,
  `soc.txt`, `trend-<file>.txt`, `contributors-<file>.txt`). No judgment is
  asked of it.
- **Miner B, decisions** (reads, in this order: ADR directories `docs/adr`,
  `docs/adrs`, `docs/decisions`; CHANGELOG and README; PR bodies, reviews,
  inline threads, and linked issues via `gh` when available; commit bodies
  containing rationale language such as *because*, *instead of*, *rather than*,
  *decided*, *we chose*, *trade-off*; reverts; dependency-manifest diffs by
  non-bot authors; directory moves and removals; CI and config diffs). It writes
  `decisions.tsv` with one row per candidate: `what`, `why` (verbatim quote or
  empty), `evidence` (`stated` when the quote exists, else `inferred`), `cite`
  (SHA or PR number), `date`, `class` (design decision / workaround for a fixed
  bug / unfinished change, Spinellis' three), and `status` (left blank for
  Step 4). Prefer the contemporaneous text: review comments and the commit
  bodies written at the time outrank a PR description rewritten at merge,
  which is the tidied textbook version of what happened (Kuhn). Closed but
  unmerged PRs, fetched with `--state closed` and the search qualifier
  `-is:merged`, are where "why not X" lives; read them for the top hotspots.

The blocks Miner B runs:

```bash
git log --since="$SINCE" --no-merges -E --grep='^Revert "' --date=short --pretty='%h%x09%ad%x09%s' HEAD </dev/null
git log --since="$SINCE" --no-merges -E --grep='^This reverts commit [0-9a-f]{40}' --pretty='%h%x09%s' HEAD </dev/null
```

Both patterns are case-sensitive and anchored, on purpose: `--grep` matches
per line of the message, so `-i '^revert'` also matches a body line starting
"reverting the flag". Empty output is the valid answer "no reverts".

```bash
git log --since="$SINCE" --no-merges --diff-filter=RD --name-status -M --date=short --pretty=format:'@@%h %ad %s' HEAD </dev/null
```

Rows are `R<score>	old	new` and `D	path`; a directory move is a set of `R`
rows sharing a parent, grouped by directory.

```bash
git log --since="$SINCE" --no-merges --date=short --pretty=format:'@@%h %ad %s' -p -- package.json pyproject.toml requirements.txt Cargo.toml go.mod Gemfile pom.xml </dev/null \
  | grep -E '^(@@|[-+][^-+])' > "$WORK/manifest-diffs.txt"
```

Only top-level dependency adds and removes by non-bot authors count as
decision candidates; version bumps are noise.

With `gh`, fetch merged PRs in the window, then the review surface of the ones
that touch hotspot paths (Step 3 output) first, capped at about one hundred,
and record `fetched of total` for the Coverage block:

```bash
gh pr list --state merged --search "merged:>=$START" --limit 300 --json number,title,body,author,mergedAt,mergeCommit,closingIssuesReferences,files > "$WORK/prs.json"
```

```bash
gh pr view <n> --json number,title,body,reviews,comments,closingIssuesReferences
gh api "repos/{owner}/{repo}/pulls/<n>/comments" --paginate
```

`--limit` defaults to thirty and truncates silently, which is why it is set
explicitly. `gh pr view` returns review summaries and conversation comments;
inline review-thread comments are only reachable through the REST call. The
`files` field also gives the PR-level change sets that replace commit-level
coupling on a squash-merged repo.

**Redaction runs on `$WORK` before either miner reads text.** Apply the
secret-shape rule in `references/visual-rendering-core.md` § 2, then mask
emails, hostnames and URLs outside this repo's own `github.com/<owner>/<repo>`,
and every line of `$WORK/names.txt`. Mark each as `[redacted]` and count
them for the dossier's Limits section. Regexes cannot catch a customer's name
in a PR body; that is what the per-item confirm in Step 7 is for.

### 3. Hotspots

Revision count per file, read from the shared log (bulk commits already have
no file lines there):

```bash
awk '!/^@@/ && NF' "$WORK/log.txt" | sort | uniq -c | sort -rn > "$WORK/freq.txt"
```

Lines of code for every text file tracked at `HEAD` (binary files are skipped
by `-I`; a path in the log that no longer exists has no LOC and drops out of
the ranking, which is correct for a deleted file):

```bash
git grep -Il '' -- . "${NONDOMAIN[@]}" | while IFS= read -r f; do printf '%s\t%s\n' "$(wc -l < "$f" | tr -d ' ')" "$f"; done > "$WORK/loc.txt"
```

Join and rank by revisions, with LOC as the qualifier (a tagged stream rather
than `FNR == NR`, which silently swallows the second input when the first is
empty):

```bash
{ awk -F'\t' '{ print "L\t" $1 "\t" $2 }' "$WORK/loc.txt"; awk '{ c = $1; sub(/^ *[0-9]+ /, ""); print "F\t" c "\t" $0 }' "$WORK/freq.txt"; } \
  | awk -F'\t' -v floor=50 '$1 == "L" { loc[$3] = $2; next } $1 == "F" { fq[$3] = $2 } END { for (p in fq) if ((p in loc) && loc[p] >= floor) printf "%d\t%d\t%s\n", fq[p], loc[p], p }' \
  | sort -t"$(printf '\t')" -k1,1nr -k2,2nr > "$WORK/hotspots.txt"
```

Print the whole curve (revisions, LOC, path) and **cut at the knee**: at most
five files, stopping earlier where the revision count falls below a third of
the leader's. Beside the knee table print the baselines a bare count lacks,
and report the measured share rather than calling it "80/20":

```bash
awk -F'\t' -v knee=5 '{ r[NR] = $1; t += $1 } END { if (NR) { for (i = 1; i <= knee && i <= NR; i++) k += r[i]; printf "files %d\tmedian %d\tp90 %d\tknee share %.0f%% of %d revisions\n", NR, r[int((NR + 1) / 2)], r[int(NR * 0.1) + 1], 100 * k / t, t } }' "$WORK/hotspots.txt"
```

Files below the LOC floor are listed separately as "churny but
small" (usually config), and large files with zero or one revision as
"big and cold" (leave them alone; stability is a design property).

**Fix-labeled commits.** First check the convention rate, because the count is
noise in a repo whose authors do not label fixes:

```bash
git rev-list --count --since="$SINCE" --no-merges -i -E --grep='fix|bug|regress|revert' HEAD
```

If fewer than roughly one commit in ten matches, omit the column and say so.
Otherwise count per file from the shared log, keeping only the commits whose
SHA the label match selects, so the window, exclusions, and bulk cutoff are the
log's:

```bash
git rev-list --since="$SINCE" --no-merges -i -E --grep='fix|bug|regress|revert' HEAD </dev/null > "$WORK/fixshas.txt"
awk -F'\t' -v shas="$WORK/fixshas.txt" '
BEGIN { while ((getline s < shas) > 0) fix[s] = 1 }
/^@@/ { sha = substr($1, 3); next }
NF && (sha in fix) { print }' "$WORK/log.txt" | sort | uniq -c | sort -rn > "$WORK/fix.txt"
```

The pattern is `/triage-issue`'s, and the two are pinned equal by
`scripts/test-excavate-entry-contract.sh` so a fix count means the same thing
in both skills. Even disciplined projects link about half their fixes to a
label or an issue (Zeller), so the count is a lower bound and the dossier
says so; it also marks where a failure was patched, not necessarily where
the defect began. When the convention check fails, the reverts from Step 2
are the convention-independent fallback, shown in the same column with that
label. Show `n` beside every ratio; a precision the counts do not support is
a claim the counts do not make. Sample ten matches by hand and print the precision ("8 of 10
sampled were fixes"); `prefix`, `fixture`, `debug`, and "regression test added"
all match. The column is labeled **fix-labeled commits**, never "bugs".

**Change coupling** from the shared log, pairs then Sum of Coupling:

```bash
awk '
function flush(   i, j, a, b, t) {
  if (n >= 2)
    for (i = 1; i < n; i++) for (j = i + 1; j <= n; j++) {
      a = f[i]; b = f[j]; if (a > b) { t = a; a = b; b = t }
      pair[a "\t" b]++
    }
  n = 0
}
/^@@/ { flush(); next }
NF    { f[++n] = $0 }
END   { flush(); for (k in pair) print pair[k] "\t" k }' "$WORK/log.txt" \
  | sort -t"$(printf '\t')" -k1,1nr > "$WORK/pairs.txt"
```

```bash
awk -F'\t' '{ soc[$2] += $1; soc[$3] += $1 } END { for (f in soc) print soc[f] "\t" f }' "$WORK/pairs.txt" | sort -t"$(printf '\t')" -k1,1nr > "$WORK/soc.txt"
```

For each hotspot's top partners, the degree is shared commits divided by the
smaller file's revision count. Print the thresholds you used; they are a noise
filter, not a severity. Classify each pair before it reaches the dossier:
*test-to-code* (drop), *copy-paste*, *unsupportive boundary*, or
*producer-consumer*, and note locality: a pair that crosses a top-level
directory boundary outranks one inside a module at the same count. A hotspot that is also a high-SOC file outranks either
signal alone. On a squash-merged repo, build the pairs from the `files` arrays
in `prs.json` instead and label the section "PR-level"; without `gh`, omit it
and say why in Limits.

**Trend** at four points by revision quartile inside the window, measuring LOC
and indentation complexity (leading whitespace summed over lines):

```bash
FILE=<path>
git rev-list --reverse --since="$SINCE" --no-merges HEAD </dev/null > "$WORK/revs.txt"
total=$(wc -l < "$WORK/revs.txt" | tr -d ' ')
if [ "$total" -ge 4 ]; then
  for q in 1 2 3 4; do
    r=$(sed -n "$(( (total * q + 3) / 4 ))p" "$WORK/revs.txt")
    [ -n "$r" ] || continue
    git show "${r}:${FILE}" 2>/dev/null | awk -v q="$q" -v r="${r:0:9}" '{ loc++; match($0, /^[ \t]*/); ind += RLENGTH } END { printf "%s\t%s\t%d\t%d\n", q, r, loc, ind }'
  done
fi
```

The `[ -n "$r" ]` guard is load-bearing: with an empty revision, `git show
":path"` silently reads the index and reports the working tree as history. A
row of `0 0` means the file did not exist at that point. Skip any commit listed
in `.git-blame-ignore-revs` when choosing points. Label: complexity up faster
than LOC is **Deteriorating**; both down is **Refactored**; both flat is
**Stable**; both up in step is **Growing**.

**Persistence.** Count revisions in each half of the window separately,
splitting the shared log at its median commit date:

```bash
MID=$(grep '^@@' "$WORK/log.txt" | cut -f3 | sort | awk '{ d[NR] = $0 } END { if (NR) print d[int((NR + 1) / 2)] }')
awk -F'\t' -v mid="$MID" '
function flush(   i) { for (i = 1; i <= n; i++) cnt[half "\t" f[i]]++; n = 0 }
/^@@/ { flush(); half = ($3 < mid) ? "first" : "second"; next }
NF    { f[++n] = $0 }
END   { flush(); for (k in cnt) print cnt[k] "\t" k }' "$WORK/log.txt" | sort -t"$(printf '\t')" -k2,2 -k1,1nr > "$WORK/persist.txt"
```

A knee hotspot that ranks in the top twenty of both halves is `persistent`,
otherwise `single-window`. Both are reported; only persistent ones reach the
first-moves list and the entries.

**Open each knee hotspot** and write a one-line mechanism from what the file
and its fix-labeled commits actually show ("three of five fixes are null
guards at the same API boundary"), or the word *unexplained*. An unexplained
hotspot is still reported; it is not offered as an entry in Step 7.

### 4. Decisions

Take Miner B's rows and:

1. Deduplicate (an ADR and the PR that implemented it are one decision).
2. **Verify against the current tree, refutation first.** Before running
   anything, write the observation that would show the decision no longer
   holds ("`rg 'legacy_api'` returns a hit outside `compat/`"); "the file
   still exists" refutes nothing and confirms nothing (Popper). Run it, and
   record a pass as *corroborated at `<HEAD sha>`*, never *confirmed*. Set
   `status`: `current`, `reversed` (a revert or later PR undid it; cite both,
   and quote the reversing commit's own stated reason, because a reversed
   decision is not a wrong one and the entry must not read as a verdict on
   what was knowable then), or `superseded` (the code moved on without saying
   so; cite the contradicting file). Tag the kind as well: a *choice* (could
   have gone another way), an *assumption* (taken as true at the time; its
   enabling condition is what drifts), or an *imposition* (forced by a law,
   vendor, or platform; cite the external source so the newcomer knows what
   is not negotiable). When the commit message's stated reason and the diff
   disagree, record both lines rather than picking one.
3. Keep `stated` rows whose `why` is a verbatim quote with a citation that
   resolves (`git cat-file -e <sha>` for commits; the PR number for `gh`
   sources). A row with no quote stays `inferred`; a row with no citation is
   dropped. Tag each quote *at-decision* (the introducing commit or PR) or
   *after-the-fact* (a later explanation) by comparing its date with the
   change's; at-decision text outranks. The "because" must sit in the same
   quoted text as the "what": a motive assembled by stitching two commits
   together is less probable than either part, not more, and is `inferred`.
   When the quote states a constraint ("because the API rate-limits
   at 100/min", "since we only ship to one region"), record it as the
   decision's assumption; the tree check in item 2 is then a check on that
   assumption, and a decision whose assumption no longer holds is
   `superseded` even if nobody reverted it. Record the exact check run
   ("`rg -n 'region' config/` shows three regions") as the decision's
   *verified by* line; a decision with no runnable check is not offered as an
   entry. *Workaround for a fixed bug* and *unfinished change* are reported
   under their own headings, never as decisions.
4. Cap at about ten `stated` decisions for the entries, highest leverage first
   (the ones whose reversal would surprise someone working in a hotspot).
   Everything else, `inferred` included, goes in the dossier's timeline.

### 5. Knowledge map (dossier only)

Per knee hotspot, contributors by commit count inside the window, and when
each was last active there:

```bash
git shortlog -sn --since="$SINCE" --no-merges HEAD -- <path> </dev/null | grep -Ev "$BOTS"
git log --since="$SINCE" --no-merges --format='%aN%x09%cs' HEAD -- <path> </dev/null | awk -F'\t' '!seen[$1]++' | grep -Ev "$BOTS"
```

`HEAD` and `</dev/null` are both required on the first line: with no revision
and a non-terminal stdin, `git shortlog` reads the log from stdin and hangs an
agent shell. Render per hotspot: at most three names, labeled **most familiar**
and **also touched**, no counts; the last-active date next to each, with
"may have moved on" when it is older than ninety days; and the distinct-author
count, because many minor contributors with no main one is the stronger
succession warning. Do not compute totals per person across hotspots, and do
not call any of this a truck factor; that is a specific greedy computation
this skill does not run. The section opens with the four legitimate uses from
§ Method rules and the sentence: *counts measure history, not skill; squash
merges and bulk commits distort them; this is who to ask, not who to blame.*
Every line is an observation about history with a date on it, never a trait,
and there is no composite score of any kind. With `gh`, add the people who
*reviewed* the hotspot's PRs, taken from the review data already fetched,
and flag a hotspot no second person has reviewed; next to a name, show the
situational channel the repo makes visible (a `CODEOWNERS` entry, sole
maintainer of the directory, the merge role), because familiarity with a
file is not evidence of who holds its rationale. The map's Limits line names
who git cannot see: long-tenured people who stopped committing, cross-team
connectors, and the review and unblocking work that leaves no diff. Say
plainly that fix-labeled density is reported per file and never per person,
since the most familiar people are usually handed the riskiest files, and a
manager who reads the map as a scoreboard is how a team stops writing
honest commit messages.

### 6. Write the dossier

Path: `~/.claude/research/<repo-slug>/excavation-<YYYY-MM-DD>.md`, creating
directories as needed. Frontmatter:

```yaml
---
kind: excavation
date: <YYYY-MM-DD>
repo: <owner/repo>
head: <40-hex sha the dossier was derived from>
window: <START> → <today> (<SINCE>)
commit_count: <N>
shallow: yes | no
squash_ratio: <s>/<t>
gh: yes | no
---
```

Sections, in this order, because the reader is new and the author is not:
**Coverage** (the block from Step 1, with `fetched of total` filled in, and
the sentence *this ranking is a diagnostic, not a target*), **Orientation**
(one paragraph: what the system is and where its main seams are, before any
table), **Glossary** (the repo's own terms, one line each, drawn from
directory names, the README, and the nouns in the knee hotspots), **Hotspots** (the knee only: revisions, LOC,
fix-labeled count and precision, trend, persistence tag, mechanism),
**Decisions** (a dated timeline, `stated` and `inferred` marked, assumption,
verified-by line, and status on each), **Reversals**, **Workarounds and
unfinished changes**, **Coupling** (classified pairs and SOC, or the reason
the section is absent, plus **Seams**: clusters that change together at a
cadence of their own, offered as candidate boundaries to wrap, invest in, or
leave, each phrased as a question), **Knowledge map**, **Limits** (what was excluded,
masked, truncated, or unavailable), **Open questions for the team** (what
history cannot answer), **Suggested first moves** (the welcome task for each
persistent hotspot is to read it and summarize its recovered decision; the
first code change is a characterization test at a pinch point), and
**Appendix** (the full revision curve, the full pair list, the shape of the
repo by top-level directory). Prose follows `references/writing-for-humans.md`:
a reader who has never opened the repo can follow it. A sentence is either a
quoted observation with its SHA or an inference, never both; the dossier is
derived data, regenerable from `head` and the window, and its facts are never
hand-edited. Optionally hand the finished dossier, and nothing else, to a
fresh sub-agent and fold the questions it cannot answer into Open questions.

### 7. Draft the entries and confirm (HITL, per item)

Two kinds of entry, both in `/compound`'s format, read from `compound/SKILL.md`
Phase 3 rather than reinvented here. Filename `<kebab-case-problem-slug>-<YYYY-MM-DD>.md`.

```markdown
---
date: <excavation date>
category: architecture-decisions | patterns
problem_type: <decision slug> | change-prone-hotspot
components: [<from the cited paths>]
technologies: [<from the manifest, if relevant>]
severity: <high for the knee leader, medium otherwise>
volatility: volatile
---
```

- **`architecture-decisions/`**, one per `stated` decision from Step 4. Body:
  `## Problem` (what the decision settled), `## Context` (the situation at the
  decision's own date, which goes here because frontmatter `date` is the
  excavation date), `## Key Decision` (the verbatim quote in the voice it was
  written, its citation, the assumption it states, its consequences for work
  touching the components, the *verified by* check, and its status),
  `## Rule Scope` (*Applies when:* work touching the components;
  *Inverts or does not apply when:* the status is `reversed` or `superseded`,
  in which case the entry says what replaced it), `## Related` (the dossier
  path and every cited SHA or PR), `## Shelf Life` (`snapshot as of <HEAD
  sha>, window <START>→<today>; regenerate with /excavate`).
- **`patterns/`**, one per `persistent` knee hotspot that has a mechanism
  line. Body:
  `## Problem` (change-prone area, with the revision, LOC, and fix-labeled
  numbers), `## Symptoms` (the mechanism line and the trend), `## Prevention`
  (characterize at the pinch point before touching; the coupled partners to
  change together), `## Rule Scope` (*Applies when:* work touching the file or
  its classified partners), `## Related`, `## Shelf Life` as above.

`volatility: volatile` is deliberate: `/research` flags volatile entries older
than ninety days as potentially stale, which is exactly right for a snapshot.
Run `/compound` Phase 4's overlap grep against any existing `docs/solutions/`
first, and fold into an existing entry rather than duplicating it.

**No entry carries a name or handle.** `$WORK/names.txt`, built in Step 2, is the
scrub list: `rg -F -f "$WORK/names.txt" docs/solutions/` must print nothing.
Check `[ -s "$WORK/names.txt" ]` first and stop if it fails, because `rg -F -f`
on an empty file exits 1, exactly as it does for "no match", so an empty list
passes a scrub that scrubbed nothing.

Run the mechanical gates first (the quote is a substring of the cited text,
`git cat-file -e` resolves, the scrub prints nothing) so the human's attention
goes only to what a regex cannot catch. Then present each candidate with a
recommended disposition (*write* or *skip*), a one-line reason, and the exact
file text that would be written, and confirm **per item**, not as a batch,
with the closed question *write as shown, edit, or skip*. Verifying a
proposal costs the reader less than composing an answer, and the quoted text
is what a human can veto when it names a customer or a person a regex
missed. Nothing is written without an affirmative *write*; a run in which
every item was accepted unedited is reported as such in the PR body, because
that is what a rubber stamp looks like. Keep the PR under about twenty
files; split it otherwise, since a bulk approval is not a review.

### 8. Branch, commit, PR

On branch `excavate/<YYYY-MM-DD>`: write the confirmed entries, run the scrub,
`git add docs/solutions` and nothing else, commit with the issue-free subject
`docs: excavate <N> decisions and <M> hotspots from <START>→<today>`, push, and
open the PR. The body is the Coverage block, the per-entry list, and the line
*recovered from history, not reviewed; every quote is cited to a SHA or PR*.
Without `gh`, print the `gh pr create` command for the user instead. This
skill never merges and never writes the review-currency stamp.

### 9. Hand off

Remove the work directory with `rm -rf "$WORK"` (re-run the Step 0 variables
block first if this is a new shell), print the dossier path, the PR URL, and
the `**Next session:**` line, then the menu in § Handoff.

## What this skill is NOT

- Not a defect finder. A fix-labeled count is a correlation; `/triage-issue`
  diagnoses, `/qa` files.
- Not a performance review. Nothing here ranks people, and nothing with a name
  on it is committed.
- Not `/compound`. It back-fills a repo that was never compounded; once the
  pipeline runs there, `/compound` writes the lessons.
- Not a rewrite recommendation. The stance toward legacy code is to light
  the lamps where you walk; the dossier names seams as questions and never
  issues a rewrite verdict.
- Not a merge step. The PR is docs-only and unreviewed; `/closeout` merges it
  and notes review currency unknown, or run `/pre-merge` first. If the repo
  requires an approving review, a human supplies it.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Frequency times LOC is the same as ranking by revisions." | LOC dominates the product; a 20,000-line generated file with six edits wins. Rank by revisions, qualify by size. |
| "The reason for this change is obvious from the diff." | Then it is `inferred`, and it goes in the dossier, not the repo. A committed decision rests on a quote. |
| "Put the owner's name in the entry so people know who to ask." | The entry is read by a pipeline that never needs a name, and the repo outlives the team. Names stay in the dossier. |
| "Skip the per-item confirm, it's only docs." | The confirm is where a customer name in a quoted PR body gets caught. Regexes do not know customers. |
| "This hotspot is obviously the bad file; no need to open it." | Hotspots are probabilities. The mechanism line comes from the file, or the entry is not offered. |
| "The ADR says so, so it is still the decision." | Verify against the tree. Documentation is aspirational until checked. |
| "No reverts matched, something must be wrong with the grep." | Empty output is the answer "no reverts". Say so. |
| "It cooled off after the refactor, so the refactor worked." | It was selected for being extreme; it would have cooled anyway. Without a comparison file chosen the same way, that is regression to the mean. |
| "The quote says why; I don't need the assumption." | The assumption is what the tree check tests. A decision with no checkable premise cannot be marked reversed or superseded, only believed. |

## Red Flags

- A ranking column that is only frequency or only LOC.
- A trend label with no indentation measurement behind it.
- A decision entry whose `## Key Decision` has no quote, no *verified by*
  check, or a citation that does not resolve.
- A knee hotspot with no persistence tag, or a `single-window` one in the
  entries or the first-moves list.
- A name, email, or `@handle` anywhere under `docs/solutions/`.
- A coupling section on a squash-merged repo with no "PR-level" label.
- A `gh` failure treated as an error instead of `gh: no` in the Coverage block.
- A window widened or narrowed without the Coverage block saying so.
- `git fetch --unshallow`, a merge, or a review-currency stamp.

## Verification

Done means all of these hold:

- The Coverage block is printed and heads the dossier.
- Every hotspot in the entries has a mechanism line that is not *unexplained*
  and a `persistent` tag read from `persist.txt`; every decision entry
  carries its kind (choice, assumption, imposition) and a *corroborated at*
  line.
- Every decision entry's citation resolves (`git cat-file -e` or the PR
  exists) and its quote is a substring of the cited text.
- `$WORK/names.txt` is non-empty, and `rg -F -f "$WORK/names.txt" docs/solutions/`
  prints nothing.
- Entry frontmatter keys equal `/compound`'s (pinned by
  `scripts/test-excavate-entry-contract.sh`).
- The dossier exists at the printed path; the PR URL (or the command to open
  it) is printed; `$WORK` is removed (Step 9, not an exit trap, because no
  shell outlives one Bash call).

## Handoff

- **Expected input:** a checked-out repo with git history, typed as
  `/excavate [--since <date>] [--paths <pathspec>...]`, and a user present for
  the scope gate and the per-item confirm.
- **Produces:** an off-tree dossier at
  `~/.claude/research/<repo-slug>/excavation-<YYYY-MM-DD>.md`; an opt-in PR of
  `docs/solutions/` entries (stated decisions, mechanism-bearing hotspots) on
  `excavate/<date>`; nothing merged.
- **Feeds downstream:** `/research` Phase 3 reads the newest dossier for the
  paths a feature touches, and every pipeline consumer of `docs/solutions/`
  reads the entries once the PR lands.
- **May redirect:** `/request-refactor-plan` when the top hotspot is the work;
  `/qa` when a fix-labeled cluster never closed.
- **Comes next by default:** `/shape`, for the first feature.

This is a genuine branch point, so render the choice as one `AskUserQuestion`
per `references/next-step-menu.md`, recommended option first:

- `/shape` (start the first feature with the dossier in hand)
- `/request-refactor-plan` on `<top hotspot>` (the hotspot is the work)
- `/qa` (file the recurring fix-labeled cluster at `<path>` as a bug)
- `/closeout` on the entries PR (land the entries first)

Print, substituting the real values:

```
**Next session:** /shape
**Input:** ~/.claude/research/<repo-slug>/excavation-<date>.md and PR #<n> on excavate/<date> — read the Coverage block before trusting either
```

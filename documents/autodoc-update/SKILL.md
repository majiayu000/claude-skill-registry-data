---
name: autodoc-update
description: "Incrementally refresh the autodoc code wiki from new commits. Pulls the source repo, diffs against the last-documented commit, maps changed files to the pages that document them, and runs an ultracode workflow to update affected pages, add pages for new entities, and flag deletions. Triggers on: /autodoc-update, autodoc update, refresh the code wiki, update autodoc from commits, sync autodoc."
allowed-tools: Read Write Edit Glob Grep Bash Workflow
---

# autodoc-update: Incremental Code-Doc Refresh

Keep the configured autodoc root (`$AUTODOC`) current with the codebase. Where `/autodoc-init` maps the whole repo,
`/autodoc-update` looks only at what changed since the last run and surgically refreshes the
affected pages. This is the normal, cheap, repeatable path — run it after any batch of merges.

The refresh runs as an **ultracode Workflow** (one agent per changed community + a reconcile agent).
The skill does the deterministic git diff and manifest bookkeeping around it.

- **Diagram Staleness** (deterministic main-loop step): flags flow/data-model pages whose embedded
  diagram's `diagram_source_sha` predates changed source — flag-don't-regenerate, with a regeneration
  cost budget; regeneration is a separate explicit action.

**Read `<suite_root>/skills/autodoc-init/references/taxonomy.md`** (the `autodoc-init` skill owns it)
— the same entity contract governs updates.

---

## Step 0 — Which kind of tree is this?

Init is store-primary: a tree produced by `graph render` carries a `.rendered-by-store` marker
(it travels with the tree at cutover). **This update path works in records too, so a rendered
tree is the supported case, not a hard stop.**

**The test itself lives at the end of Step 1, not here, and that is deliberate.** It reads
`$AUTODOC`, and Step 1 is what assigns `$AUTODOC` — so run top-to-bottom from this page, a test
placed here would read `[ -f "/.rendered-by-store" ]`, which is false on every machine, and would
take the `STORE_PRIMARY=0` branch below on a perfectly good store-primary tree. A variable is
tested only after the block that assigns it — the same rule as `RENDER_TARGET` and `REPO_STEM`
(Step 3.5) — which is why the branch sits with the values it depends on rather than above them.
This step keeps the two OUTCOMES, because what they mean is what a reader comes here for.

**`STORE_PRIMARY=1` is the normal path** and everything below assumes it: agents emit records,
Step 4.5 runs `graph records` / `reports-stale` / `render` / `check`, and the renderer owns the
tree. Nothing writes markdown directly, so there is nothing left for the next render to undo —
which is what a stop here would protect against.

**`STORE_PRIMARY=0` means there is no store behind this tree**, so the records the agents emit
have nowhere to land. Do not run the workflow against it: `graph records` needs a corpus built by
init, and a pre-cutover tree has none. Report that to the user and run `/autodoc-init` to cut the
tree over first — the conversion is one-way by design, and re-inventing a markdown-editing path
alongside the record one is how store-primacy stops meaning anything.

### Runtime guard — run this before Step 1

Unlike the tree test above, this one needs nothing Step 1 assigns, so it runs here, before the
preamble and before the fetch: three prerequisites the run cannot finish without, checked before
the diff and the community work are paid for. Autodoc is off at install by default, so
provision step 6 — `npm ci`, then the `autodoc_graph` install into the suite venv — never ran on
a machine that set `autodoc_root` afterwards.

1. **`Workflow` in this session's tool list.** Bash cannot see it; you can. The refresh runs
   through it and there is **no single-agent fallback** — do not refresh pages one by one in the
   main loop instead. If it is absent, STOP here and tell the user to enable the `Workflow` tool
   for this session; do not run the block below or anything after it.
2. **`autodoc_graph` importable and `node` on PATH** — the block below. It must exit 0.

```bash
missing=""
# Same bare `python` every later `python -m autodoc_graph.cli` call resolves. stderr is left
# visible on purpose: an import that fails for another reason (a broken sqlite-vec, say) must
# say so rather than read as "not installed".
python -c "import autodoc_graph" || missing="$missing autodoc_graph"
command -v node >/dev/null || missing="$missing node"
if [ -n "$missing" ]; then
  echo "STOP: missing:$missing. Install Node LTS (with npm) if it is absent, then re-run" \
       "'python <suite_root>/install/provision.py --autodoc' (install step 6:" \
       "npm ci + the autodoc_graph install into the suite venv), adding --no-auto-allow if the" \
       "auto-allow hooks were declined (a re-run without it writes them back); then restart" \
       "/autodoc-update." >&2
  exit 1
fi
echo "runtime guard: autodoc_graph importable, node on PATH"
```

On a STOP, report the remedy to the user and end the run. Nothing has been fetched or written.
The message prints `<suite_root>` literally, because this block runs before Step 1 resolves it:
when you relay the remedy, substitute the real suite root (`environment.suite_root`, the
agentflow checkout) so the user gets a command they can paste.

## Step 1 — Config preamble + locate the autodoc + load the manifest

**Set `AUTODOC_PROJECT` before you run the first block, whenever more than one project profile is
installed under `~/.agentflow/config/projects/`.** The block below REFUSES to start in that case
(see its ambiguity check) rather than refreshing whichever project the SESSION happens to default
to — that default is the session's project, not the corpus's. So export it first:

```bash
export AUTODOC_PROJECT=<the project whose corpus this run refreshes>
```

On a single-project box it is optional and the default is unambiguous. `ls ~/.agentflow/config/projects/*.md`
is how you find out which case you are in, and the refusal names the installed set if you skip it.

Resolve the autodoc root and suite root from the agentflow config first. `AUTODOC` =
`resolve_autodoc_root(env, project)`, the project's own root and never the bare machine-level
field; `SUITE_ROOT` = `environment.suite_root` (skill-relative tool paths resolve under it).
**Fail loudly if no autodoc root resolves.** `source_repo`/`source_branch`/
`source_path`/`project` are read from the manifest `/autodoc-init` wrote — the update path does
not re-read the project profile, which is exactly why `project` has to travel in the manifest:
the graph rebuild below passes `graph build --project`, and nothing on this path can derive that
value. **Do not fall back to the corpus id (`${source_path##*/}`)** — a project whose
`autodoc_root` points at another project's corpus would stamp every page with the wrong project,
and a wrong attribution is worse than an absent one.

```bash
# INVALIDATE THE POINTER FIRST — before anything here can fail. Every exit path below this line
# (the project-ambiguity refusal, the three `[ -n ... ] || exit 1` guards, the missing-manifest
# guard) would otherwise leave the PREVIOUS run's pointer on disk, still aimed at a fully
# populated carrier. A reader who hit one of those stops and then ran any later block would source
# the previous run's values — including its TO — which is exactly the stale-TO failure this carrier
# exists to end. Removing it here means a failed Step 1 leaves no usable pointer at all: the next
# block's `. "$(cat /tmp/autodoc-env.current)"` gets an empty filename and exits non-zero.
rm -f /tmp/autodoc-env.current
# AUTODOC + SUITE_ROOT from agentflow config (agentflow.config.load_environment reads
# $AGENTFLOW_CONFIG or ~/.agentflow/config; equivalently parse the first fenced YAML block of
# ~/.agentflow/config/environment.md).
# HEREDOC, NOT `python -c '...'`, AND THAT IS LOAD-BEARING. The comments below contain
# apostrophes, and inside a single-quoted -c string each one CLOSES the quote: an odd count makes
# bash fail to parse the block entirely - `syntax error near unexpected token ('`. Then nothing in
# this block runs, which means nothing in the whole runbook runs, because every later step reads
# $AUTODOC / $SUITE_ROOT / $PROJECT from here. A quoted heredoc delimiter makes the body literal,
# so prose below can say "that session's project" without breaking the shell. Do not convert
# this to -c.
# UNSET FIRST, THEN STOP ON THE PYTHON'S OWN STATUS. The guards below test that a value is
# non-empty, not that this block set it, and this runbook's own carrier exports AUTODOC,
# SUITE_ROOT and PROJECT, so a reader who sourced it and re-runs this block holds all three.
# `eval "$(python ...)"` cannot see a refusal: eval returns the status of the text it evaluates,
# and a refusal prints none. Capturing first and exiting on the capture's status stops the run at
# the refusal, whatever the shell inherited.
unset AUTODOC SUITE_ROOT PROJECT
AUTODOC_CFG="$(python - <<'PY'
import os
import shlex
from agentflow.config import (
    config_home, load_environment, load_project, resolve_autodoc_root, resolve_project_name,
)
def emit(k, v): print(k + "=" + shlex.quote(v.replace(chr(92), "/")))  # backslash->slash for Git Bash
e = load_environment()
# RESOLVED per project, never the bare environment value. environment.autodoc_root is
# machine-level: on a box running two projects it names ONE corpus, so reading it directly
# renders this project into the other project one every time. resolve_autodoc_root applies the
# documented precedence - the project profile override, then the environment default, then the
# derived <data_root>/projects/<name>/autodoc - and raises AutodocRootError rather than
# answering from an empty root. This file warns below that a wrong corpus stamps every page with
# the wrong project, so it must not read the value that causes it.
# EXPLICIT, not the session default. resolve_project_name() falls back to
# $AGENTFLOW_PROJECT, which for a LANE is right - it is that session's project - and for a
# SKILL run inside a lane whose default is a DIFFERENT project is the same cross-project
# write the resolver above exists to stop, arriving by another door: when the session default
# names a different project than the corpus being refreshed, the run resolves onto that other
# project's tree.
# $AUTODOC_PROJECT is how the invoker says which corpus this run is for; the session default
# remains the fallback so a single-project box needs no ceremony.
explicit = os.environ.get("AUTODOC_PROJECT")
# NOTHING HERE CAN TELL WHICH CORPUS YOU MEANT, so on a box where that is ambiguous this
# refuses instead of guessing. resolve_project_name() falls back to $AGENTFLOW_PROJECT, which
# is the SESSION's project - right for a lane, and for a skill run inside a lane defaulted to
# another project it silently refreshes that other project's pages. The check below cannot
# catch that (see the cross-check's own note): every value downstream follows `name`, so a
# wrong name selects a tree that agrees with it. Refusing ambiguity is what closes it.
installed = sorted(p.stem for p in (config_home() / "projects").glob("*.md"))
if not explicit and len(installed) > 1:
    raise SystemExit(
        "FATAL: %d projects are installed (%s) and no AUTODOC_PROJECT was given, so which "
        "corpus this run is for is ambiguous. The session default (%r) is the project of the "
        "SESSION, not of the corpus. Re-run with AUTODOC_PROJECT=<name>."
        % (len(installed), ", ".join(installed), resolve_project_name())
    )
name = explicit or resolve_project_name()
proj = load_project(name) if name else None
root = resolve_autodoc_root(e, proj)
if not root:
    raise SystemExit("FATAL: no autodoc root resolves for project %r - set autodoc_root in the project profile or environment.md (SCHEMA.md); autodoc cannot run without it." % (name,))
emit("AUTODOC", root)
emit("SUITE_ROOT", e.suite_root)
emit("PROJECT", name or "")
PY
)" || exit 1
eval "$AUTODOC_CFG"
# A python that exits 0 without emitting a name leaves it unset, not inherited: these catch that.
[ -n "$AUTODOC" ] || exit 1
[ -n "$SUITE_ROOT" ] || exit 1
# Unguarded, an empty $PROJECT makes 'never bound' and 'genuinely different' the same failure
# at the cross-check below, and only one of those is a mismatch.
[ -n "$PROJECT" ] || exit 1
test -f "$AUTODOC/.manifest.json" || { echo "No manifest — run /autodoc-init first"; exit 1; }

# THE RUN CARRIER. Every fenced block below is its own shell, yet about a dozen variables cross
# blocks: $AUTODOC/$SUITE_ROOT/$PROJECT from right here are read as far down as Step 6.5, and
# $SRC/$FROM/$TO/$INV/$GRAPH_DB/$COMM/$REPO_STEM/$RENDER_TARGET/$RUN_DIR are each minted in one
# block and consumed in others. None of them survives the block that sets it, so without a
# carrier every later command runs with empty expansions. The carrier: one file per run, written
# here, sourced at the top of every block that reads a cross-block variable, appended to by every
# block that mints one.
#
# PER-RUN, AND TRUNCATED HERE, because a single global carrier goes stale: a hand-written
# /tmp/autodoc-env.sh, one export per line, that nobody refreshes ends up carrying a TO from an
# earlier run and no RUN_DIR at all, and sourcing it blind drives the whole path against the wrong
# commit. A single global path is what makes that possible; a per-run file that this block creates
# empty cannot inherit anything.
#
# The POINTER is fixed because it has to be: a later block has no variable to derive the per-run
# path from (that is the problem being solved), so something at a known path must name it. It is
# REMOVED at the top of this block and re-written at the bottom, so it exists only across a Step 1
# that ran to completion; a dead or failed run leaves no pointer rather than a stale one.
# This assumes one update at a time per machine, which this runbook already assumed —
# $RENDER_TARGET, /tmp/autodoc-changed.txt and /tmp/autodoc-prompts.json are all fixed paths.
AUTODOC_ENV="/tmp/autodoc-env-$(date +%Y%m%dT%H%M%S)-$$.sh"
: > "$AUTODOC_ENV"
# %q quotes for re-input, so a SUITE_ROOT or RENDER_TARGET with a space in it survives the round
# trip. env_put lives IN the carrier so every later block gets it by sourcing, rather than each
# block re-declaring the same three lines.
# Braced ${1}/${2}, never a bare dollar-digit: loaded through the Skill tool with arguments, the
# harness rewrites a bare dollar-digit anywhere in this body - fences included - to that
# argument (0-based) before bash sees it, and leaves the braced form alone.
printf 'AUTODOC_ENV=%q\n' "$AUTODOC_ENV" >> "$AUTODOC_ENV"
cat >> "$AUTODOC_ENV" <<'CARRIER'
env_put() { printf '%s=%q\n' "${1}" "${2}" >> "$AUTODOC_ENV"; }
CARRIER
. "$AUTODOC_ENV"
env_put AUTODOC "$AUTODOC"
env_put SUITE_ROOT "$SUITE_ROOT"
env_put PROJECT "$PROJECT"
printf '%s\n' "$AUTODOC_ENV" > /tmp/autodoc-env.current
echo "run carrier: $AUTODOC_ENV"
```

If `$AUTODOC` or its `.manifest.json` is missing, STOP and tell the user to run `/autodoc-init`.

**Every block from here down opens by sourcing that carrier**, with the same line:
`. "$(cat /tmp/autodoc-env.current)" || exit 1`. The guards above stay exactly where they are and
remain the thing that catches a failed resolve — the carrier only transports values that already
passed them. A block that MINTS a cross-block variable appends it with `env_put` in the same block
that computes it, so the carrier is never more current than the run and never less.

**What that source line does and does not catch, stated precisely, because the obvious reading of
it is wrong.** A MISSING pointer is caught: `cat` prints nothing, `.` gets an empty filename,
returns non-zero, and `|| exit 1` fires (rc 1). An EMPTY carrier file is NOT caught —
an empty script is a valid script, `.` returns 0, and the block runs on with every variable empty.
That is why Step 1 REMOVES the pointer before it can fail and only writes it back on the last line
of a block that succeeded: the protection comes from there being no pointer, not from the source
line detecting a bad one.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC, SUITE_ROOT, PROJECT, env_put
# Bind the manifest fields as shell vars HERE, where the manifest is read: Step 2 uses
# $source_path immediately and Step 3.5 uses $source_repo/$project, so a value bound any later
# is empty at its first use for a reader following this file in order.
# Read from the manifest, never derived: `project` in particular cannot be inferred from
# the corpus id, for the reason stated above.
# Same two steps as Step 1's resolution, for the same reason: the carrier this block just sourced
# may already hold all four names from an earlier pass.
unset source_repo source_branch source_path project
MANIFEST_VARS="$(python -c '
import json, shlex, sys
m = json.load(open(sys.argv[1]))
for k in ("source_repo", "source_branch", "source_path", "project"):
    v = m.get(k)
    if not v:
        raise SystemExit("FATAL: .manifest.json has no %s - re-run /autodoc-init rather than guessing one" % k)
    print(k + "=" + shlex.quote(v))
' "$AUTODOC/.manifest.json")" || exit 1
eval "$MANIFEST_VARS"
# Guard each one as well: a python that exits 0 without printing a name leaves it unbound.
for v in source_repo source_branch source_path project; do
  eval "[ -n \"\$$v\" ]" || { echo "FATAL: $v did not bind from .manifest.json"; exit 1; }
done
# Onto the carrier only AFTER the guards above passed — Step 2 reads $source_path and $source_branch
# and Step 3.5 reads $source_repo and $project, each of them blocks away from this one.
for v in source_repo source_branch source_path project; do
  eval "env_put $v \"\$$v\""
done
# ROOT-vs-NAME COHERENCE, and deliberately not more than that. $PROJECT is the resolved name;
# $project is what the tree at $AUTODOC says it documents. They disagree when the ROOT does
# not belong to the NAME - a mis-set autodoc_root, a missing profile override, a legacy root
# shared by two projects. That shape is worth refusing.
#
# IT CANNOT CATCH A WRONG NAME, and saying so is the point. $AUTODOC is resolved FROM $PROJECT
# and the manifest is read from $AUTODOC, so all three descend from one input: give the wrong
# name and the root follows it to a tree that agrees with it. Intent is external and no
# comparison in here can reach it - which is why the ambiguity refusal above exists and is the
# thing actually closing that route.
if [ "$project" != "$PROJECT" ]; then
  echo "FATAL: this corpus says it documents '$project' but the run resolved project"
  echo "       '$PROJECT' (root $AUTODOC). Refusing rather than refreshing another"
  echo "       project's pages. Set AUTODOC_PROJECT='$project', or point at the right root."
  exit 1
fi

# Step 0's branch, evaluated HERE because it reads $AUTODOC and this is the first line at which
# $AUTODOC is known to be bound. Stated above this point it would silently test
# "/.rendered-by-store" and send every store-primary tree down the "run /autodoc-init first" path.
if [ -f "$AUTODOC/.rendered-by-store" ]; then
  STORE_PRIMARY=1   # records path: Step 4.5 lands the records and re-renders
else
  STORE_PRIMARY=0   # pre-cutover tree: no store to land records in
fi
env_put STORE_PRIMARY "$STORE_PRIMARY"
```

Read `.manifest.json`: it gives `source_repo`, `source_branch`, `source_path`, `project`,
`last_sha`, and the `pages` reverse-index (`autodoc-path → {type, source_paths}`). A manifest
with no `project` field is refused: re-run `/autodoc-init` rather than guessing one.

## Step 2 — Pull the source repo and diff

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC, source_path, source_branch, env_put
SRC="$AUTODOC/${source_path}"            # from manifest, e.g. .source/app
git -C "$SRC" fetch origin "$source_branch"   # not $branch: never assigned, and not a manifest field
FROM=$(python -c "import json;print(json.load(open('$AUTODOC/.manifest.json'))['last_sha'])")
TO=$(git -C "$SRC" rev-parse "origin/$source_branch")
# ancestry-guard: BEFORE the reset and the diffs. `git diff FROM TO` is a tree diff and
# succeeds across unrelated histories, so a rewritten history silently reports phantom changes
# on every run from this base. Refuse, name both shas, and leave the re-base to the operator.
git -C "$SRC" cat-file -e "$FROM^{commit}" 2>/dev/null || { echo "FATAL: last_sha $FROM (manifest) is not a commit in $SRC - the source history was rewritten and the old object is gone, or .manifest.json is corrupt, or the clone is shallow and never fetched it (check \`git -C \"\$SRC\" rev-parse --is-shallow-repository\`; \`git -C \"\$SRC\" fetch --unshallow\` then rerun). TO=$TO. Re-base last_sha by hand to a commit on the new history whose tree matches what the corpus was rendered from, or re-run /autodoc-init." >&2; exit 1; }
git -C "$SRC" merge-base --is-ancestor "$FROM" "$TO" || { echo "FATAL: last_sha FROM=$FROM is not an ancestor of TO=$TO (origin/$source_branch) - the source history was rewritten (or a shallow clone lost the path between them: if \`git -C \"\$SRC\" rev-parse --is-shallow-repository\` says true, \`git -C \"\$SRC\" fetch --unshallow\` and rerun before re-basing anything). Diffing across unrelated history reports phantom changes, so this run refuses. Remedy (operator decision, not automatic): set last_sha in .manifest.json to a commit that IS on the new history and whose tree matches what the corpus was rendered from (inspect \`git -C \"\$SRC\" merge-base $FROM $TO\` and the new history's root, \`git -C \"\$SRC\" rev-list --max-parents=0 $TO\`), or re-run /autodoc-init." >&2; exit 1; }
# end ancestry-guard
git -C "$SRC" reset --hard "$TO"
# $TO in particular MUST go on the carrier from the block that computes it. A stale carrier holds
# a TO from a previous run, and every step below — the graph build, the records land, the
# manifest write — stamps that value into the corpus.
env_put SRC "$SRC"
env_put FROM "$FROM"
env_put TO "$TO"
# changed (added/modified) and deleted files, repo-relative:
# REDIRECTED, not printed: Step 3 reads both of these by path, so printed to stdout they
# would leave a later step requiring a file no command wrote.
git -C "$SRC" diff --name-only --diff-filter=d "$FROM" "$TO" > /tmp/autodoc-changed.txt
git -C "$SRC" diff --name-only --diff-filter=D "$FROM" "$TO" > /tmp/autodoc-deleted.txt
wc -l < /tmp/autodoc-changed.txt   # changed/added
wc -l < /tmp/autodoc-deleted.txt   # deleted

# Use-Case trailer ingestion (Step 3.8): per-commit hash + Use-Case: trailer + files.
# \x1f field-sep, \x1e record-sep; commas separate multiple trailers on one commit.
# The commit trailer is the ONLY carrier — no source-code annotation. A missing trailer
# just means that UC won't auto-attach (impact grep still finds it via the plan).
git -C "$SRC" log "$FROM..$TO" --no-merges --name-only \
  --format='%x1e%H%x1f%(trailers:key=Use-Case,valueonly,separator=%x2c)%x1f' > /tmp/autodoc-uc-log.txt
```

If `FROM == TO`, report "Already current at `<sha>`" and stop. (Do not assume `jq` is installed —
use `python -c` for JSON.)

Filter out noise before mapping: `node_modules/`, `.git/`, lockfiles, `__pycache__/`, build output,
binary assets, pure-test-only changes with no contract impact. Be conservative — when unsure, include it.

## Step 3 — Group changes by community + resolve affected pages

- Group changed files by the **derived community** of the symbols in those files, read from the
  communities artifact regenerated at `TO` in Step 3.5 below (`.source/.communities.json` —
  the same `emit-graph -> graph build -> graph communities` chain init runs; there is no
  hand-written area map). Communities live under `units[].communities[]` in the
  artifact ({id, label, descriptor, member_ids, symbols} — keyed by COMMUNITY ID; labels are
  display strings). A changed file belongs to the community whose `symbols` list names it; a
  changed file with no symbols (docs, config) attaches to the community whose members import
  or route to it if evident, else to the community whose `top_prefixes` covers it. A file no
  community claims either way is resolved straight from the manifest reverse-index, PAGE BY PAGE:
  each page naming it that a unit already owns stays with that unit, and the file joins that
  unit's `changedFiles`; each page naming it that no unit owns goes to one extra entry keyed
  `symbolless` with empty `symbols`, so that page's refresh reads the diff. One file can therefore
  appear in both.
- For each changed file, find the pages whose `source_paths` (from the manifest `pages` index)
  contain it — these are the **affectedPages** for that community. A file with no affected page
  is likely a NEW entity; the community agent will create a page for it.
- Each page goes to ONE community: the one with the most changed files behind it, then the most
  deleted ones, ties to the lower key. Deleted files decide only between communities with no
  changed file behind the page, because the owner re-verifies the page against live code. Every other community whose files it cites gets it in `contextPages` as
  `{page, owner}`, read-only, and each of its checklist rows whose file only such a page cites
  carries `coveredBy` naming it.
  Without that, the losing community sees no page for its file, is told the code is new, and
  emits a duplicate of what the page already documents.
- Deleted files (Step 2's `/tmp/autodoc-deleted.txt`) are attributed by the same three rules and
  count toward page ownership, so every page citing one reaches a community whose agent
  deprecates it — or, when the page also cites live files, drops the deleted paths from it. They
  never join `changedFiles` and never add checklist rows: nothing at `TO` is left to read.
- Build `changedCommunities = [{ key, label, descriptor, changedFiles, affectedPages,
  contextPages?, symbols: [{ name, file, line, kind, coveredBy? }] }]` (`?` = present only when
  non-empty), only for units that have changes or own a page, plus the `symbolless` entry last
  when it has a page. Passing the arg is REQUIRED (the workflow hard-fails on a missing arg); an explicit `[]`
  is legal only when the diff genuinely maps to no community and no manifest page.

**This step has a command.** Everything above is the derivation; the script is that derivation
executed, so the one argument the workflow cannot run without is produced by a command, not by
the reader. **Run it AFTER Step 3.5**, which is what regenerates the communities artifact
at `TO`; run it before and you group this diff against the previous run's communities.

The call itself runs at the end of Step 3.5, once `cli communities` has rebuilt the artifact it reads --- see there.

`/tmp/autodoc-changed.txt` is written by Step 2's own block above -- by the command, not by the
reader.
The script prints its own coverage line to stderr -- units matched, changed files mapped of the
total, pages affected, how many of those pages were recovered from symbol-less files, and how
many affected pages cite one of the deleted files (`N affected page(s) cite one of M deleted
file(s)`, the pages whose agents must deprecate or trim them) -- and
names any changed file that maps to no community AND no manifest page, because docs, config and
fixtures carry no graph symbols and a silent zero there reads as full coverage. It refuses a run
whose `--changed` and `--deleted` are BOTH empty rather than emitting `[]`: "Step 2 produced
nothing" and "the diff maps to no community" are different failures with different remedies, and
both otherwise look like `[]`. An empty `--changed` with deletions is a valid run: its entries
carry the pages to deprecate and no changed files.

### Step 3.5 — Diff-scoped coverage pre-pass + community regroup (deterministic)

The clone is already reset to `TO` (Step 2), so the working tree reflects the new commit. Build
the symbol inventory AND regenerate the community partition at `TO` — the Jaccard carry-forward
keeps community ids stable across runs, and the churn report names anything that moved. These run
as plain Node/Python processes in the skill main-loop (the Workflow sandbox has no
filesystem/Node access).

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC, SUITE_ROOT, SRC, TO, source_repo, source_branch, project, PROJECT, env_put
INV="$AUTODOC/.source/.inventory.json"
GRAPH_JSONL="$AUTODOC/.source/.graph.jsonl"
GRAPH_DB="$AUTODOC/.source/graph.db"
COMM="$AUTODOC/.source/.communities.json"
# The corpus id every `autodoc_graph.cli` call on this path must agree on, and the render
# target Step 4.5 writes to. Step 4.5 reads both, so an unassigned one there becomes
# `--out ""` or `--corpus ""`.
# NOT `"${REPO##*/}"`, which is how /autodoc-init defines REPO_STEM: `REPO` does not exist
# on the update path, so copying that line would expand to the empty string. The corpus id is the
# one `graph build` populates below, so it is derived once here and referenced everywhere, rather
# than the same expression being written out twice.
REPO_STEM="${source_path##*/}"
RENDER_TARGET="$AUTODOC.rendered"
# The render stamp: a SNAPSHOT of $RENDER_TARGET taken immediately after Step 4.5's render, so
# the NEXT attempt can tell a leftover render from an agent write. It is a snapshot and not a
# report from the renderer - nothing here can know what the renderer produced, only what is on
# disk when the stamp is written. Step 4.5's placement is what makes the two the same set.
# DERIVED FROM $RENDER_TARGET, in the block that mints it,
# for the reason stated two comments up - writing "$AUTODOC.rendered.render-stamp.json" out by
# hand anywhere else restates the expression and the two drift the first time either moves.
# OUTSIDE the render target (a sibling file, not a file inside it): a stamp within the tree it
# describes would have to list itself, and the clear step would delete the only record of what it
# was allowed to delete.
STAMP="$RENDER_TARGET.render-stamp.json"
# COMM_PINS: built here, before the `communities` call that consumes it, with init Step 2.5's
# loop - one `--pin PREFIX=NAME` pair per entry of the profile's optional `communities.pins`
# block, read one per line into an ARRAY so names with spaces survive, and expanded quoted as
# "${COMM_PINS[@]}" in the call itself. Built here, not left to prose, because a profile that
# sets pins and gets an empty value has unpinned partitions with no warning. Empty is the result
# only for a profile with no pins block. The python runs in a command substitution
# so a failed profile load stops the run rather than yielding zero pins.
PINS_TXT="$(python -c '
import sys
from agentflow.config import load_project
p = load_project(sys.argv[1])
pins = p.communities.pins if p.communities else {}
for k, v in pins.items():
    print(f"{k}={v}")
' "$PROJECT")" || exit 1
COMM_PINS=()
while IFS= read -r pin; do
  [ -n "$pin" ] && COMM_PINS+=(--pin "$pin")
done <<< "$PINS_TXT"
# All seven onto the carrier, in the block that mints them. Step 4.5 alone reads six of these
# ($GRAPH_DB, $REPO_STEM, $COMM, $RENDER_TARGET, $STAMP, $INV) and it is roughly 250 lines below here.
# COMM_PINS is NOT carried: it is an array, the carrier holds strings, and its only consumer is
# the `communities` call at the end of this block.
env_put INV "$INV"
env_put GRAPH_JSONL "$GRAPH_JSONL"
env_put GRAPH_DB "$GRAPH_DB"
env_put COMM "$COMM"
env_put REPO_STEM "$REPO_STEM"
env_put RENDER_TARGET "$RENDER_TARGET"
env_put STAMP "$STAMP"
# install deps once (same guard as init Step 2.5)
( cd "$SUITE_ROOT/skills/autodoc-init/references/inventory" && test -d node_modules || npm install )
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/extract-inventory.js" "$SRC" "$INV" "$source_repo" "$TO"
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/emit-graph.js" "$SRC" "$GRAPH_JSONL" "$REPO_STEM" "$TO" "$source_repo"
python -m autodoc_graph.cli build --db "$GRAPH_DB" --corpus "$REPO_STEM" --jsonl "$GRAPH_JSONL" \
  --repo-ref "$source_repo" --project "$project" --branch "$source_branch"
python -m autodoc_graph.cli communities --db "$GRAPH_DB" --corpus "$REPO_STEM" --emit "$COMM" "${COMM_PINS[@]}"
```

**Now build `changedCommunities`, because its input exists as of the line above.** This is Step 3's
derivation executed; the reasoning behind the grouping is up there, the call is down here, and the
order is the point rather than a formatting choice.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, AUTODOC, COMM, env_put
# Its OWN directory, not one under $RUN_DIR — because the carrier transports values FORWARD and
# $RUN_DIR is minted in Step 4, which has not run yet. Reaching for it here would expand to
# nothing and drop the checklists at the filesystem root. Nothing downstream has to agree on this
# path anyway: the script writes every checklistPath as an absolute path, so the refresh agents
# resolve the files wherever they live.
CHECKLIST_DIR="/tmp/autodoc-checklists-$(date +%Y%m%dT%H%M%S)"
env_put CHECKLIST_DIR "$CHECKLIST_DIR"
python "$SUITE_ROOT/skills/autodoc-update/references/build-changed-communities.py" \
  --communities "$COMM" --manifest "$AUTODOC/.manifest.json" \
  --changed /tmp/autodoc-changed.txt --deleted /tmp/autodoc-deleted.txt \
  --out /tmp/autodoc-changed-communities.json \
  --checklist-dir "$CHECKLIST_DIR" || exit 1
```

`--checklist-dir` delivers each unit's coverage checklist **by path**: the symbols land in
`$CHECKLIST_DIR/<key>.json` and the entry carries `checklistPath` + `symbolCount` instead of
the array. That path is written absolute, so the checklists do not have to live under Step 4's
`$RUN_DIR` and this block does not have to share a variable with it. Without the flag the
workflow interpolates every symbol into the refresh agent's prompt text, so the args grow with the
symbol count, and a catch-up run of a few thousand symbols can reach the 512KB cap the Workflow
tool applies to a baked variant script, almost all of it symbols. Nothing else moves: the refresh
agent already reads the taxonomy, the changed sources and the affected pages from paths it is
handed. A
unit whose checklist is EMPTY gets no `checklistPath` and keeps its inline empty array, so the
prompt's "refresh by reading the diff" fallback still fires for it.

(`"${COMM_PINS[@]}"` is the bash array built in the Step 3.5 block exactly as in init Step 2.5 —
one `--pin PREFIX=NAME` pair per entry of the project profile's optional `communities.pins` block,
read one per line so names with spaces survive. The
`--band` default 8:24 is the agent-count/cost budget served by unit packing, not a partition
property — the run completes regardless of how many communities the repo has.) All artifacts
live beside the clone and are gitignored. Read `.communities.json` with `python -c` (no `jq`).
For each `changedCommunity`, attach `symbols` = that community's artifact `symbols` (under
`units[].communities[]`) filtered to its `changedFiles` (compare
each symbol's `file` against the changed file list). Symbols in unchanged files are intentionally
excluded — the update path only re-verifies coverage for what actually moved. The script above does
this, and with `--checklist-dir` it hands each refresh agent that scoped checklist as a file to read
rather than as prompt text (Step 4). Surface the CLI's churn lines (created/dissolved/changed
communities) in the run report — that is what tells downstream summaries which groupings moved.

### Step 3.6 — Consumer re-verify (contract-edge fan-out)

The manifest reverse-index only catches pages whose OWN source changed — a page documenting the
CONSUMER of a contract goes stale silently when the PROVIDER's file moves. So, for each affected
page from Step 3, grep the autodoc for pages that LINK to it — by title or by any frontmatter
alias:

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC
# e.g. affected page endpoints/POST sync-push.md (title "POST /v1/sync/push"):
# -F: fixed strings, because [[ is a regex bracket expression
grep -rlF --include="*.md" -e "[[POST sync-push" -e "[[POST /v1/sync/push" "$AUTODOC"
```

Add up to ~8 such consumer pages per community to that community's `affectedPages`, marking each added
entry `<path> — consumer of changed contract — re-verify claims about it`. The refresh agent
re-verifies what those pages claim about the changed contract (shapes, endpoints, behavior)
against current source, editing only what's stale. This is what stops
provider-moved-consumer-stale drift.

**Contract pairs (explicit fan-out, on top of the grep):** after computing `affectedPages`,
read each affected page's `contract_with:` frontmatter (the taxonomy's optional contract-pair
field) and add every page it names to that community's `affectedPages`; ALSO add any page whose own
`contract_with:` names an affected page (grep `contract_with` across the autodoc for the
affected titles). Mark each such entry
`<path> — contract pair — re-verify BOTH sides against source`. Unlike plain consumer entries,
a contract-pair page must be re-verified against BOTH codebases' actual shapes (open both
sides' source), and any mismatch is documented explicitly on both pages — never papered over.

### Step 3.7 — Rolling audit sample (init-drift catch-up)

Diff-driven refresh only re-verifies pages whose source (or contract partner) changed — an
init-era hallucination on an untouched page can otherwise sit unchecked forever. So every run
also audits a small rolling sample of pages the diff did NOT touch. Selection runs in the skill
main-loop and is **deterministic** (same inputs → same sample):

- **Review-backlog intake FIRST:** if any `Review Backlog*.md` exists in the autodoc root,
  fill the sample from its still-open entries (bullets not yet marked `RESOLVED`) before the
  rolling candidates below — up to the full ~10, page + finding text
  (`auditPages[].finding`), plus pass `backlogFile` in the workflow args so the audit agent
  marks resolved entries. Parked findings drain automatically, a few per run, until the
  backlog is empty; only then is the sample purely rolling.
- **Candidates:** every manifest page NOT in any community's `affectedPages` this run, excluding
  `status: deprecated` pages and meta/nav pages (`index.md`, `_index.md`, `overview.md`,
  `hot.md`, `log.md`, `Start Here.md`, `Glossary.md`).
- **Staleness key:** `max(updated, audited)` from the page's frontmatter (a missing `audited`
  means never audited — use `updated` alone). Sort ascending (stalest first), tie-break by path.
- **Weighting:** contract-bearing types get priority — take up to 6 from
  {`endpoint`, `data-model`, `service`}, then fill to ~10 total from the remaining types
  (process, job, flow, component, page, …), preserving staleness order within each bucket.
- Build `auditPages = [{page, source_paths}]` from the manifest and pass it as a workflow arg
  (Step 4 — baked into the run's variant script like every other arg).

Over successive runs this rolls through the entire wiki, stalest-first. It is self-balancing
because the audit agent stamps a fresh `audited: <date>` on **every** audited page whether or
not it changed (only genuinely *fixed* pages also get a new `updated:`), and the sort key is
`max(updated, audited)` — a clean page moves to the back of the queue instead of being
re-audited on the very next run.

### Step 3.8 — Use-Case ingestion (deterministic, gate-inert)

Parse the `Use-Case:` commit trailers from Step 2 and attach the referenced UCs to the flow pages
whose activation chains they touched. This is the spine's **Hop 4** (commit trailer → flow page).
The trailer is the sole carrier: no `UC-NNNN` source comment is required or read. Runs in the skill
main-loop and is **deterministic** (same commits → same attachments).

- **Build `uc → files`:** from `/tmp/autodoc-uc-log.txt`, split on `\x1e` (record) then `\x1f`
  (field) to get `{hash, ucCsv}`; the file lines that follow each record are the commit's touched
  files. For every `UC-NNNN` in `ucCsv`, union in that commit's files. Ignore records with no
  trailer.
- **Map files → flow pages (manifest reverse-index):** for each manifest page with `type == "flow"`,
  a UC attaches to it when the UC's commit-files intersect that flow's `source_paths`. Only flow
  pages host use cases (per taxonomy).
- Build `ucAttachments = [{ flowPage, source_paths, ucs: [ "UC-0147", ... ] }]`, one entry per flow
  page that gained at least one UC, and pass it into the workflow args (Step 4). The Reconcile agent
  writes the `use_cases:` frontmatter + `## Use Cases` rows and reconciles each UC's `Status`.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC
# ucAttachments from the trailer log + manifest flow pages. No jq — python -c.
# EVERY /tmp PATH ARRIVES BY ARGV, never as a literal in the program text. `python` here is a
# NATIVE Windows binary: MSYS rewrites a POSIX path in argv (or an exported env var) to the real
# Windows directory, but a string literal inside the script body is never touched, so `/tmp/x`
# resolves against the current drive root as C:\tmp\x. C:\tmp EXISTS on a stock Windows box, so
# the write SUCCEEDS silently into the wrong directory and only the reader downstream goes red.
python -c '
import json, sys
AUTODOC = sys.argv[1]
UC_LOG = sys.argv[2]
UC_OUT = sys.argv[3]
man = json.load(open(AUTODOC + "/.manifest.json"))
raw = open(UC_LOG, encoding="utf-8").read()
uc_files = {}
for rec in raw.split("\x1e"):
    rec = rec.strip("\n")
    if not rec:
        continue
    head, _, tail = rec.partition("\n")
    parts = head.split("\x1f")
    uc_csv = parts[1] if len(parts) > 1 else ""
    ucs = [u.strip() for u in uc_csv.split(",") if u.strip().startswith("UC-")]
    if not ucs:
        continue
    files = [ln for ln in tail.splitlines() if ln.strip()]
    for uc in ucs:
        uc_files.setdefault(uc, set()).update(files)
out = []
for page, meta in man.get("pages", {}).items():
    if meta.get("type") != "flow":
        continue
    src = set(meta.get("source_paths", []))
    hit = sorted(uc for uc, fs in uc_files.items() if fs & src)
    if hit:
        out.append({"flowPage": page, "source_paths": sorted(src), "ucs": hit})
json.dump(out, open(UC_OUT, "w"), indent=2)
print("ucAttachments:", len(out), "flow page(s),", sum(len(a["ucs"]) for a in out), "UC link(s)")
' "$AUTODOC" /tmp/autodoc-uc-log.txt /tmp/autodoc-uc-attachments.json
```

`use_cases` is an **opaque scalar list** (`UC-NNNN`, never `[[wikilink]]`) — invisible to
`graph-check.js`, which only validates the enumerated relational-link fields. Do NOT emit UCs as
wikilinks and do NOT add `use_cases` to the graph-check relational set (registry-existence checking
is Phase-5 enrichment). If `ucAttachments` is empty, omit the arg — the UC steps are skipped.

## Step 4 — Launch the refresh workflow (ultracode)

First dump the single-sourced prompt templates (the refresh prompt body + return
schema live in the autodoc-init skill's prompt module; the workflow sandbox cannot import
modules, so the dump travels as an arg):

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, env_put
node "$SUITE_ROOT/skills/autodoc-init/references/prompts/render-prompt.js" --dump > /tmp/autodoc-prompts.json

# Agents write RECORDS here, one file per agent. CLEAR IT FIRST.
# `graph records --manifest` treats the workflow's returned file list as
# authoritative and errors on any *.json present but unlisted, so a leftover
# from a prior attempt at the same RUN_DIR is a loud failure rather than a
# silent extra ingest — but only if you let it be one. Clearing is cheaper.
#
# RUN_DIR IS THE ONE PATH THE REFRESH AGENTS THEMSELVES RECEIVE, so it must be NATIVE — a
# `/tmp/...` string here is the MSYS split one level up, and it costs the whole fan-out.
# The agents write with the harness's own file tools, not through this shell. On Windows those
# resolve `/tmp` to `C:\tmp` while bash resolves it to the user temp dir; `C:\tmp` exists, so every
# agent would write there, report success, and `update-workflow.js` would force each returned
# path to match the POSIX string it was handed. Step 4.4 then fails claiming a stale paste, and
# the missing-file check never fires first because the wrong directory genuinely exists.
# `tempfile.gettempdir()` is the native temp dir on every platform; the forward-slash rewrite
# keeps one spelling for bash, for the JSON args and for the agents.
RUN_DIR="$(python -c 'import tempfile,sys; sys.stdout.write(tempfile.gettempdir().replace(chr(92),"/"))')/autodoc-update-$(date +%Y%m%dT%H%M%S)" || exit 1
[ -n "$RUN_DIR" ] || { echo "FATAL: could not resolve a native temp dir for RUN_DIR" >&2; exit 1; }
rm -rf "$RUN_DIR/records" && mkdir -p "$RUN_DIR/records"
# NO SHELL-SIDE GUARD HERE, AND THAT IS DELIBERATE: any guard written here can only pass. MSYS
# rewrites a POSIX absolute path in argv AND in the environment, so every route this shell has
# hands a native tool an ALREADY-NATIVE string: a round-trip probe or a shape check fed `/tmp/...`
# reports success, because the value it receives was rewritten before it sees it. A check whose
# verdict cannot depend on the input is worse than no check, since the board then looks guarded.
# The guard lives in `references/update-workflow.js`, on `args.runDir` as received: the hand-baked
# Workflow args are the one value that never passes through this shell, so they arrive raw and can
# still be judged. See the comment beside it.
# Step 4.5 lands the records from here. Without RUN_DIR on the carrier it would get
# `records --records ""`, on the one expensive step downstream of the fan-out.
env_put RUN_DIR "$RUN_DIR"
```

The `$`-names in the call below are **not** expanded by a shell — the Workflow args are baked into
the run's variant script by hand. Read their values out of the run carrier (`cat` the path Step 1
printed) rather than from memory; `$RUN_DIR` and `$TO` in particular were minted two and five
blocks back.

```
Workflow({
  scriptPath: "$SUITE_ROOT/skills/autodoc-update/references/update-workflow.js",
  args: {
    prompts:         "<contents of /tmp/autodoc-prompts.json>",
    runDir:          "$RUN_DIR",                // agents write records under $RUN_DIR/records/
    repoPath:        "$SRC",                    // $AUTODOC/<manifest.source_path>
    autodocPath:     "$AUTODOC",                // the root Step 1 resolved for $PROJECT
    repoName:        "<manifest.source_repo>",
    fromSha:         "<FROM>",
    toSha:           "<TO>",
    date:            "<today YYYY-MM-DD>",
    taxonomyDocPath: "$SUITE_ROOT/skills/autodoc-init/references/taxonomy.md",
    changedCommunities: "<contents of /tmp/autodoc-changed-communities.json, built in step 3>",
    deletedFiles:    [ ... repo-relative deleted paths ... ],
    auditPages:      [ ... from step 3.7: [{page, source_paths, finding?}] — optional, ~10 diff-untouched pages;
                       backlog-drawn entries carry the parked finding text ... ],
    backlogFile:     "<Review Backlog*.md filename if backlog intake fed auditPages, else omit>",
    ucAttachments:   [ ... from step 3.8: [{flowPage, source_paths, ucs:["UC-0147", ...]}] — optional,
                       flow pages that gained UC links from Use-Case: trailers; omit if empty ... ]
  }
})
```

Each `changedCommunities[]` entry carries the changed-file inventory slice from Step 3.5 as its
per-community coverage checklist. With `--checklist-dir` (the invocation above) that arrives as
`checklistPath` + `symbolCount` and the refresh agent is told to READ the file; the rows never enter
the prompt text, which is what keeps a large catch-up run under the 512KB workflow-args cap. Without
it the entry carries `symbols` and the workflow interpolates the rows inline — same checklist, same
agent task, and an empty checklist always stays inline. `auditPages` feeds the
Audit phase (one agent, after Refresh, before Reconcile — so audit fixes land in the reconciled nav).

`ucAttachments` (Step 3.8) drives **UC status reconcile** inside the Reconcile agent: for each flow
page it writes the ingested UCs into the `use_cases:` frontmatter + `## Use Cases` table, then sets
each UC's per-UC `Status` by **reading code** via the taxonomy's liveness protocol — a UC whose
activation chain is still present in the flow's `source_paths` → `completed`; one whose chain is gone
or unmounted → `deprecated` (with a `> [!stale]` banner). autodoc reads code, it **never copies plan
or registry status**, so this self-heals every run: a UC's code returning flips it back to
`completed`, a UC's code removed flips it to `deprecated`.

Returns `{ updated, created:[{file,type,source_paths}], removed, reconcile, audit:{audited,fixed,findings,path}, recordsFiles, coverage:{pages,covered,excluded} }`.
Runs in background; you're notified on completion. **`recordsFiles` is the manifest Step 4.5
needs** — it is what the agents actually returned, not a glob of the directory. The returned
`coverage` is FYI only: Step 6.5 gates on the report Step 4.4 assembles from the records on disk,
so nothing downstream depends on this return surviving in your context.

### Step 4.4 — Write the records manifest and the coverage report (do this the moment the workflow returns)

**Run this BEFORE anything in Step 4.5.** `/tmp/autodoc-update-run.json` is what the
`graph records --manifest` call below reads, and this block is the only command that writes it.
`cli.py` opens it with a bare `open()` and no existence check, so an unwritten manifest aborts the
run at the FIRST command after a multi-agent fan-out that has already been paid for. This block is
where that is caught instead: it fails on the paste, seconds after the workflow returns, with the
records still on disk and nothing else spent.

**It also writes `/tmp/autodoc-update-coverage.json`, the report Step 6.5 gates on.** Step 6.5
cannot take the workflow return's `coverage` object as a hand paste: by the time a run reaches
that gate the return is hours and one fan-out gone. So it is assembled here, from the same validated
records list, while those records are the freshest thing on the box.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # RUN_DIR
# Clear the PREVIOUS run's manifest before writing this one. Without this, a python failure below
# leaves an earlier run's file standing and the `-s` guard at the bottom passes on it - handing
# Step 4.5 a records list from another run, which is the stale-input failure the run carrier
# exists to prevent. All three /tmp files here are fixed paths, the same assumption the rest of
# the runbook makes. The coverage report joins the list for the same reason and is cleared by the
# same rm: Step 6.5 READS it, so a leftover from an earlier run is exactly as dangerous here as a
# leftover records list.
rm -f /tmp/autodoc-update-run.json /tmp/autodoc-records-files.json /tmp/autodoc-update-coverage.json
# PASTE the workflow's returned `recordsFiles` array between the FILES markers, verbatim. The
# empty array below is a PLACE, not a default — it fails the check beneath it, which is the point.
cat > /tmp/autodoc-records-files.json <<'FILES'
[]
FILES
# EVERY /tmp PATH ARRIVES BY EXPORTED ENV VAR, exactly as RUN_DIR already does, and for the same
# reason: `python` is a NATIVE Windows binary, so MSYS rewrites a POSIX path in argv or in the
# environment and NEVER inside the program text. A literal "/tmp/x" in the body below would write
# to C:\tmp\x -- a directory that EXISTS on a stock Windows box, so the write succeeds silently and
# only the `-s` guard at the bottom (reading bash's real /tmp) goes red, pointing at the wrong step.
RUN_DIR="$RUN_DIR" \
RECORDS_FILES=/tmp/autodoc-records-files.json \
RUN_MANIFEST=/tmp/autodoc-update-run.json \
UPDATE_COV=/tmp/autodoc-update-coverage.json \
python - <<'PY' || exit 1
import json, os
run_dir = os.environ["RUN_DIR"].replace(chr(92), "/").rstrip("/") + "/records/"
records_files = os.environ["RECORDS_FILES"]
run_manifest = os.environ["RUN_MANIFEST"]
update_cov = os.environ["UPDATE_COV"]
files = json.load(open(records_files, encoding="utf-8"))
if not files:
    raise SystemExit(
        "FATAL: no recordsFiles pasted into %s. The workflow return "
        "is the only authority on which record files the agents wrote; a glob of the directory is "
        "a different list and is exactly what --manifest exists to refuse." % records_files
    )
missing = [f for f in files if not os.path.isfile(f)]
if missing:
    raise SystemExit("FATAL: %d recordsFile(s) do not exist on disk: %s" % (len(missing), ", ".join(missing[:5])))
# A paste left over from an EARLIER run cannot pass this: RUN_DIR is timestamped per run.
stray = [f for f in files if not f.replace(chr(92), "/").startswith(run_dir)]
if stray:
    raise SystemExit("FATAL: %d recordsFile(s) sit outside %s - stale paste from an earlier run? %s"
                     % (len(stray), run_dir, ", ".join(stray[:5])))
with open(run_manifest, "w", encoding="utf-8") as fh:
    json.dump({"files": files}, fh, indent=2)
print("records manifest: %d file(s) -> %s" % (len(files), run_manifest))
# ...and the COVERAGE REPORT Step 6.5 gates on, from the SAME list, for the same reason. The
# workflow return's `coverage` object lives in one tool result and is hours gone by the time a
# run reaches that gate, so it is rebuilt here from the records on disk.
# It is reconstructible because each record file carries the three keys the report is made of:
# `pages` (page records, each with its own source_paths), `covered` and `excluded`. Pages are
# keyed by `file` so a page emitted by two units is one entry, which is what makes the count
# comparable to the workflow's.
# ONE DELIBERATE DIVERGENCE, SO IT IS NOT READ AS A BUG LATER. `coverage.js` documents
# `report.pages[].source_paths` as CREATED pages only, and this report carries UPDATED pages too.
# That is right for THIS path and wrong for /autodoc-init: on a refresh, a page the agents
# rewrote documents its source file just as much as a page they created, so excluding it would
# report a file gap for a file that is in fact documented. It makes the `fileGaps` half slightly
# more permissive than the workflow's own return; the `uncovered` half, which is symbol-level and
# the strict one, is unaffected.
# FROM `files`, NEVER FROM A GLOB of the records dir - the whole point of --manifest: a glob
# re-admits an orphan from an earlier attempt at the same runDir, and it would land here as
# coverage evidence for symbols this run never documented.
# GUARD THE MEMBERS, NOT ONLY THE ENVELOPE. The `isinstance(record, dict)` skip below stops a
# bare-array record file from raising - but `pages: ["a.md"]`, `covered: 7` and a file that is not
# valid JSON would each still die here with a raw traceback, AFTER the whole Step 4 fan-out was
# paid for. That is the precise cost the skip exists to avoid, so every member gets the same
# treatment.
# The record schema is documentation, not enforcement (`skills/autodoc-init/references/prompts/refresh.js` says so in
# its own comment), so a malformed member is an ordinary agent slip and must not cost the run.
# SKIPPED EVIDENCE IS REPORTED, NEVER SILENT: a dropped `covered` list makes its symbols read as
# undocumented, and Step 6.5 then FAILS naming them - which is the right outcome, but only if the
# operator can see here which record was unreadable rather than hunting the symbols.
pages, covered, excluded, objects, defects = {}, [], [], 0, []
for path in files:
    name = os.path.basename(path)
    try:
        with open(path, encoding="utf-8") as fh:
            record = json.load(fh)
    except ValueError as exc:
        defects.append("%s: not valid JSON (%s)" % (name, exc))
        continue
    # A bare array is a malformed record file - `graph records` refuses it outright in Step 4.5,
    # so it contributes no evidence here either rather than raising a second, less clear error.
    if not isinstance(record, dict):
        defects.append("%s: top level is %s, not an object" % (name, type(record).__name__))
        continue
    objects += 1
    page_rows = record.get("pages")
    if page_rows is not None and not isinstance(page_rows, list):
        defects.append("%s: `pages` is %s, not a list" % (name, type(page_rows).__name__))
        page_rows = None
    for page in page_rows or []:
        if not isinstance(page, dict):
            defects.append("%s: a `pages` entry is %s, not an object" % (name, type(page).__name__))
            continue
        pages[page.get("file")] = {"file": page.get("file"),
                                   "source_paths": page.get("source_paths") or []}
    for key, sink in (("covered", covered), ("excluded", excluded)):
        rows = record.get(key)
        if rows is None:
            continue
        if not isinstance(rows, list):
            defects.append("%s: `%s` is %s, not a list" % (name, key, type(rows).__name__))
            continue
        sink.extend(rows)
if not objects:
    raise SystemExit(
        "FATAL: none of the %d records file(s) is a JSON OBJECT, so no coverage evidence could be "
        "assembled. Step 6.5 would gate on an empty report and Step 4.5's `graph records` will "
        "refuse these files anyway - re-run the refresh phase." % len(files)
    )
with open(update_cov, "w", encoding="utf-8") as fh:
    json.dump({"pages": list(pages.values()), "covered": covered, "excluded": excluded}, fh, indent=2)
print("coverage report: %d page(s), %d covered, %d excluded -> %s"
      % (len(pages), len(covered), len(excluded), update_cov))
for defect in defects:
    print("  UNREADABLE, contributed no evidence: %s" % defect)
if defects:
    print("  ^ %d malformed record member(s) skipped. Their symbols will read as undocumented at "
          "Step 6.5; that FAIL is the same defect reported at the gate, not a second one." % len(defects))
PY
[ -s /tmp/autodoc-update-run.json ] || { echo "FATAL: /tmp/autodoc-update-run.json was not written"; exit 1; }
# Guarded separately from the manifest: the python above writes them in order, so a failure
# between the two leaves a good manifest and no coverage report - and the gap would not surface
# until Step 6.5, four steps and one fan-out later.
[ -s /tmp/autodoc-update-coverage.json ] || { echo "FATAL: /tmp/autodoc-update-coverage.json was not written - Step 6.5 gates on it"; exit 1; }
```

## Step 4.5 — Land the records, re-render, check (the update path is store-primary)

Every phase above writes **records**, not pages. Nothing the run produced is visible in the
tree until this step lands them in the store and re-renders. Same three commands the init path
uses, in the same order.

**`$SUITE_ROOT` does NOT redirect the Python.** It points the `node` scripts and this file at a
checkout, but `python -m autodoc_graph.cli` resolves through the installed package, wherever that
was installed from. On a normal run those are the same tree and the distinction is invisible. On a
BRANCH run they are not, and the failure is the worst-shaped one available: you believe you are
testing your renderer change and you are testing master, greenly. The first block below therefore
prints the tree it resolved. Read it. If it is not the tree you are testing, prepend
`PYTHONPATH="$SUITE_ROOT/skills/autodoc-init/references/graph"` to the `python -m` commands in
this step — deliberately, and say in the write-up that it was a branch run, because a branch run
still owes a repeat from the deployed path after the merge.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, RENDER_TARGET, STAMP, GRAPH_DB, REPO_STEM, RUN_DIR, TO, COMM
# Step 4.4's output, re-checked here because `cli records --manifest` opens this path with a bare
# open() and no existence check. Skipping Step 4.4 otherwise surfaces as a traceback on the first
# command after the fan-out; this says which step to go back to.
[ -s /tmp/autodoc-update-run.json ] || { echo "FATAL: /tmp/autodoc-update-run.json missing - run Step 4.4 (write the records manifest) first"; exit 1; }
# The renderer REFUSES a non-empty --out unless force=True, and force is prohibited here, so
# a leftover $RENDER_TARGET from an earlier attempt fails this step. /autodoc-init runs this
# same assertion before its render. Absent or empty both pass.
#
# --stamp/--clear-prior-render DISCRIMINATE BY PROVENANCE, AND THAT IS NOT A WEAKER GUARD.
# $RENDER_TARGET is a fixed path and only the copy-back removes it, so any stop between the
# render and the copy - a red golden gate, most often - leaves it populated, and without the
# stamp the operator's next attempt would die right here accusing an agent of a write whose real
# author was this runbook's own previous render. The stamp written below lists whatever is in
# $RENDER_TARGET at the moment --write-stamp runs - a snapshot, not a report from the renderer,
# which is why it is written immediately after `cli render` and nowhere else - and only a tree
# matching that listing file-for-file is cleared as a prior render. One file an agent added is
# unaccounted for and still fails; so does a missing stamp, an unreadable or malformed one, a stamp
# describing a different directory, or a stamped file that has since vanished. Clearing the target
# unconditionally before asserting would have made the assertion unfailable, and this assertion is
# the ONLY enforcement of the "no agent may write page content" constraint - the agent(prompt)
# driver exposes no tool allowlist, so there is nothing else watching.
# THE STAMP IS UNAUTHENTICATED, name-only, at a predictable path, and that costs nothing here:
# anything able to counterfeit it could equally have written the pages itself, and a counterfeit stamp buys
# the counterfeiter erasure of their OWN files, never injection into the corpus - --clear-prior-render
# deletes what the stamp lists and `cli render` immediately rewrites the tree from the store. The
# window between `cli render` and --write-stamp is no wider than it would be with no stamp.
# `|| exit 1` ON EVERY COMMAND, AND IT IS LOAD-BEARING. As bare commands the block would exit
# with the status of `check` alone, and the prose above would be reader-discipline, not a gate: a
# failed `records` would let `render` proceed against an un-updated store and the golden gate
# below would compare a stale render to the live tree -- a red arriving after the whole Step 4
# fan-out has been paid for.
# WHICH TREE IS THE PYTHON COMING FROM? $SUITE_ROOT does not decide this; the install does. On a
# deployed run the answer is $SUITE_ROOT and this line is noise. On a branch run it is the one
# thing standing between you and a green result about code you did not change. It only prints.
python -c "import autodoc_graph, os; print('autodoc_graph:', os.path.dirname(autodoc_graph.__file__))" || exit 1
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/assert-no-agent-writes.js" "$RENDER_TARGET" --stamp "$STAMP" --clear-prior-render || exit 1
python -m autodoc_graph.cli records --db "$GRAPH_DB" --corpus "$REPO_STEM"   --records "$RUN_DIR/records" --manifest /tmp/autodoc-update-run.json   --assignment /tmp/autodoc-changed-communities.json   --sha "$TO" --date "$(date +%F)" || exit 1
python -m autodoc_graph.cli reports-stale --db "$GRAPH_DB" --corpus "$REPO_STEM" --artifact "$COMM" || exit 1
python -m autodoc_graph.cli render --db "$GRAPH_DB" --corpus "$REPO_STEM" --out "$RENDER_TARGET" || exit 1
# IMMEDIATELY after a render that exited 0, and nowhere else. The stamp is a claim about output
# that exists: written before the render it would account for files nothing had produced yet, and
# written after the gate it would never exist on the one path that needs it - the failed-gate path.
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/assert-no-agent-writes.js" --write-stamp "$RENDER_TARGET" --stamp "$STAMP" || exit 1
python -m autodoc_graph.cli check  --db "$GRAPH_DB" --corpus "$REPO_STEM" --out /tmp/autodoc-store-check.json || exit 1
```

**Then the graph-reviewer, read-only, over `$RENDER_TARGET` — before the golden gate.** This is
the Step 6.1 gate (the classes it checks are listed there), moved here and stripped of `--fix`.
It runs on the render target because that tree is exactly what the store produces: a finding on
it is a finding in the records. It runs before the golden gate so a red stops the run while
nothing has been copied into `$AUTODOC` yet.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, RENDER_TARGET, INV, SRC
# Reuse the npm-install guard from Step 3.5 (idempotent).
( cd "$SUITE_ROOT/skills/autodoc-init/references/inventory" || exit 1; test -d node_modules || npm install ) || exit 1
# NO --fix, AND NOT ON $AUTODOC. A repair written into a page no store record carries is
# dropped by the next render; the NEXT run's golden gate then compares that render to a live tree
# still holding the repair, reports a link-recall loss on a page no agent touched, and blames an
# agent. --fail-on-fixable computes what --fix WOULD change, writes nothing, names each page on
# stderr and in the report's `fixable` list, and exits 1. Fix the records, re-render, re-run.
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/graph-check.js" \
  "$RENDER_TARGET" "$INV" "$SRC" /tmp/autodoc-graph.json --fail-on-fixable \
  || { echo "FATAL: graph-check found blockers or fixable findings on the render - repair the named page(s) through their records and re-render; never patch pages. Report: /tmp/autodoc-graph.json"; exit 1; }
```

**Then the golden gate, while `$RENDER_TARGET` and `$AUTODOC` are still two different trees.**
After the copy-back they are one tree and the gate would compare it to itself. What this gate
budgets — and why it is LOSS and not the symmetric difference — is below.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC, SUITE_ROOT, RENDER_TARGET, SRC, INV
# THE UPDATE PATH BUDGETS LOSS, NOT THE SYMMETRIC DIFFERENCE. On a refresh, a page that vanished
# is silent damage and a page that appeared is the job, so 0 lost is the right literal and the
# created count is left uncapped - the gate reports it on the PASS line so growth is still visible.
# `pageSetLostBudget` is opt-in; /autodoc-init keeps the symmetric check, which is correct there.
printf '{ "pageSetLostBudget": 0 }\n' > /tmp/golden-gate-update.json
# `|| exit 1` and not a paragraph: the next runnable block is the copy-back, so without the stop
# a reader following the blocks in order copies over a failed render and then deletes the only
# copy of it. The stop belongs on the command.
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/golden-gate.js" \
  "$RENDER_TARGET" "$AUTODOC" /tmp/golden-gate-update.json "$SRC" "$INV" || exit 1
```

`--manifest` is the `recordsFiles` list from the workflow return, written to
`/tmp/autodoc-update-run.json` as `{"files": [...]}` **by Step 4.4's block, not by hand**. Pass it:
it is what makes a stale `*.json` from an earlier attempt an error instead of an extra page nobody
asked for.

`--assignment` is Step 3's `/tmp/autodoc-changed-communities.json`. With it, a page two units both
emitted is resolved instead of refusing the batch: the unit the page was
assigned to wins even when its record is shorter, and otherwise the lowest unit id wins
(every other key, `audit` and `symbolless` included, sorts after every `unit-N`). Only plain `affectedPages` entries assign; Step 3.6's
annotated `<path> — ...` entries are re-verify fan-out and never do. Each
collision prints one `WARNING: page ...` line on stderr and lands in the report's
`duplicate_claims`; a line saying `partitioner gap` means no claimant was assigned the page, which
is an assignment problem to count across runs, not a record to repair by hand.

### RENDER TO `$RENDER_TARGET`, A SEPARATE EMPTY DIRECTORY — NEVER `--force` INTO `$AUTODOC`

This is the one instruction in this step that is not obvious, so here is the reason rather than
the rule alone. `render_pages._prepare_out` refuses a non-empty target unless `force=True`, and
with force it **unlinks every existing `.md` file** before writing. Its own refusal text says
what force is for: *"the renderer writes into an empty sibling directory; pass force=True only
for a directory the renderer owns."*

**`$AUTODOC` is not a directory the renderer owns.** `records.py` keeps a `_RESERVED_BASENAMES`
set — `_index.md`, `index.md`, `overview.md`, `log.md`, `hot.md`, `CLAUDE.md`, `Start Here.md`,
`Glossary.md` — that a page record may not claim. Three of those (`log.md`, `hot.md`,
`CLAUDE.md`) are **also not produced by the renderer**, so they can be neither claimed nor
regenerated: forcing a render over them deletes them with nothing to restore them. Human-authored
files that are not reserved at all — a `Review Backlog*.md`, a hand-written note somebody dropped
in the root — are in the same position.

Cite the mechanism, not a count: *which* files are at risk depends on the tree, but *why* they are
at risk is `_RESERVED_BASENAMES` plus "not produced by the renderer", and that does not change.

**Sync rendered pages back rather than swapping the directory.** Copy `$RENDER_TARGET`'s contents
over `$AUTODOC`, overwriting; do not delete `$AUTODOC` first. Non-record files then survive by
construction, which is the point — an exemption list of files to preserve would protect the ones
somebody remembered and silently lose the next one added.

**This step is a command, not prose, and that is not cosmetic.** As prose between two fenced
blocks, an operator running this file literally would render into `$RENDER_TARGET`, skip the
copy, and delete it — the update would silently do nothing while every gate around it passed. The
command is also the landmark the gate above is ordered against: without it, the gate could move
past the copy and stay green.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # RENDER_TARGET, AUTODOC
# Copy CONTENTS (the trailing /.), never the directory, or $AUTODOC gains a nested copy of itself.
cp -a "$RENDER_TARGET/." "$AUTODOC/" || exit 1
# "Verified" is a count, not the exit status of cp: every rendered page must now exist in the live
# tree. This is what the `rm` below is allowed to trust.
missing=$(cd "$RENDER_TARGET" && find . -name "*.md" -printf '%P\n' \
  | while read -r f; do [ -f "$AUTODOC/$f" ] || echo "$f"; done | wc -l | tr -d ' ')
[ "$missing" = "0" ] || { echo "FATAL: $missing rendered page(s) did not reach $AUTODOC"; exit 1; }
```

**Then remove `$RENDER_TARGET`, and only after the copy verified above.**

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # RENDER_TARGET, STAMP, AUTODOC
# THE GUARD IS RE-DERIVED HERE, in the block that does the rm. `$missing` was computed in the
# copy-back block above — a DIFFERENT shell — so it does not exist in this one, and a sentence
# between the two blocks orders nothing. An unbound
# `$missing` is empty, `[ "" = "0" ]` is false, so a guard written as a carried variable would
# have failed closed here; a guard written as prose enforced nothing at all. Recomputing costs one
# `find` over the render target and answers the question this block actually needs answered.
[ -n "$RENDER_TARGET" ] || { echo "FATAL: RENDER_TARGET unbound - source the carrier"; exit 1; }
# ABSENT IS NOT THE SAME AS UNVERIFIED, and collapsing the two orphans the stamp. An operator who
# removes $RENDER_TARGET by hand would hit a `-d` check as a FATAL, exit before `rm -f
# "$STAMP"`, and leave the stamp in the vault directory forever - self-healing at the next
# --write-stamp and harmless to the gate, but a stray file a vault autocommit picks up. There is
# nothing to verify and nothing to lose when the tree is already gone, so that case skips straight
# to the stamp removal. The verified-copy guard is untouched on the path that matters: if
# $RENDER_TARGET EXISTS, it is still counted against $AUTODOC and neither it nor the stamp is
# removed unless every rendered page arrived.
if [ -e "$RENDER_TARGET" ]; then
  [ -d "$RENDER_TARGET" ] || { echo "FATAL: $RENDER_TARGET is not a directory"; exit 1; }
  missing=$(cd "$RENDER_TARGET" && find . -name "*.md" -printf '%P\n' \
    | while read -r f; do [ -f "$AUTODOC/$f" ] || echo "$f"; done | wc -l | tr -d ' ')
  [ "$missing" = "0" ] || { echo "FATAL: $missing rendered page(s) are not in $AUTODOC - refusing to remove $RENDER_TARGET"; exit 1; }
  rm -rf "$RENDER_TARGET"
else
  echo "$RENDER_TARGET is already gone - removing its stamp so it does not outlive the tree it describes"
fi
# The stamp describes a tree that no longer exists, so it goes with it - IN THE SAME BLOCK, and on
# the existing-target path under the same verified-copy guard. Left behind it would account for a
# render that has been consumed, and the next run's assertion would measure a fresh target against
# a dead listing. `-f` because a run that never reached the render leaves no stamp and that is not
# an error.
if [ -n "$STAMP" ]; then rm -f "$STAMP"; fi
```

Sourcing the carrier matters here more than anywhere: `rm -rf ""` is harmless, but `rm -rf` on an
unbound `$RENDER_TARGET` is how a run silently keeps a full render target that the NEXT run's
empty-target assertion then reports as *"an agent wrote page content"* — after that run has paid
for its whole Step 4 fan-out.

`/autodoc-init` consumes its render target with a `mv`, so the directory is gone when it
finishes. This path deliberately copies instead, which means nothing here consumes it — and
`$RENDER_TARGET` is a fixed path (`$AUTODOC.rendered`), not a per-run one. Left behind, a
SUCCESSFUL run's output becomes the next run's blocker: the empty-target assertion above finds a
full page tree and stops with *"an agent wrote page content"*, which is a false diagnosis — the
writer was the previous run's own renderer — and it stops **after** the whole Step 4 fan-out has
already been paid for. So the `rm` above is still how a clean run is supposed to end.

**The stamp is the safety net, not a substitute for that `rm`.** A run that stops between the
render and the copy-back — a red golden gate is the common case — never reaches the `rm` at all,
and without the stamp the operator could not retry the step without deleting the directory by
hand. `--clear-prior-render` clears it for them, but only against
`$STAMP` — a name-only snapshot of `$RENDER_TARGET` taken immediately after `cli render` exits 0,
and of that directory alone. Blanket-clearing the target before the assertion instead would be
worse than the bug: it would DELETE the evidence of a real agent write rather than report it,
which is the one thing the assertion exists to catch. Provenance keeps both properties — a
leftover render clears, and a file no render produced still stops the run.

**The stamp is unauthenticated and that is not a hole.** It is a plain JSON file at a predictable
path, so anything that could counterfeit it could equally have written the pages it accounts for — and a
counterfeit stamp buys the counterfeiter erasure of their own files, never injection of content into the
corpus: `--clear-prior-render` deletes what the stamp lists, and `cli render` then rewrites the
tree from the store. The window between `cli render` and `--write-stamp` is no wider than it would
be with no stamp at all.

**Never on a failed copy.** `$RENDER_TARGET` is the only copy of the render until the sync
completes; removing it after a partial copy destroys the run's output with nothing to restore it
from.

### The golden gate, run against the live tree as its baseline

Run it after `render` and BEFORE the copy-back, while `$RENDER_TARGET` and `$AUTODOC` are still
the new tree and the old one. After the copy they are the same tree and the gate compares
something to itself.

The call itself runs up in Step 4.5, immediately after `cli check` — see there.

**A `source-paths` FAIL names pages that cite files deleted from the source repo in the range.**
That is a true positive and the drift this gate is for: the pages outlived the code they cite. A
full run normally clears it: Step 3 routes every page citing a deleted file to a refresh agent,
which re-emits a page that still cites live files without the deleted paths, and deprecates a page
that cites only deleted files. Deprecated pages are exempt from the check, because their stale
callout already explains the dead path and a record must still name what it documented. If a `source-paths` FAIL survives a full run, the citing pages are wrong in a way the
refresh did not reach and they get fixed by hand — do not widen the gate to pass them.

**A gate's message names a symptom, not a cause.** The same message can come from different
defects, and the disposition differs each time:

| the gate says | what can actually be wrong |
|---|---|
| `page-set: symmetric difference N > budget 0` | the budget is unpassable by construction — the reason this path budgets LOSS (below) |
| `links-resolve`: a broken wikilink | the **renderer** corrupted a correct record |
| `links-resolve`: a broken wikilink on a page whose rendered text is correct | the gate's own **link reader** misread correct prose — and a renderer defect can mask it until the renderer is fixed |
| `link-recall`: a page lost a link | a genuine agent defect |

A gate names a PAGE; it does not name an author. Several of these are defects in the
machinery that reads and writes pages, and one can be **hidden by** another — a renderer that
destroys the offending prose before the checker can misread it hides the checker's false
positives until the renderer tells the truth. Triage before you repair (next section); a repair
applied to a machinery defect mangles correct prose to satisfy a broken tool.

**Why this path budgets LOSS and not the symmetric difference.** On an update run new pages are
the DELIVERABLE, so a symmetric-difference budget is either padded until it cannot fail or
red-flags the run's own purpose. A budget derived from the corpus — the count of root-level
`*.md` minus nav pages, say — is 0 on a corpus whose every root page IS nav, and a budget of 0 can
only be met by a refresh that creates nothing. A run that creates pages and loses none then reads
`FAIL page-set: symmetric difference N > budget 0; only-baseline: (none)`: the deliverable,
reported as a failure, and reported only after the entire Step 4 fan-out has been paid for.

**So the update path declares `pageSetLostBudget: 0` instead.** On a refresh the danger is a page
LOST, not pages gained: a vanished page is silent damage nobody will notice, a new page is the job.
The created count is not capped, but the gate prints it on the PASS line too — a gate that hides
growth is how an unexpected 400-page render slips by. `/autodoc-init` passes no such key and keeps
the symmetric check unchanged, which is right for a fresh render that must reproduce the tree
exactly. If pages genuinely should disappear on a refresh — a deleted subsystem — raise the number
deliberately and say why, the same as any other declared tolerance.

**A FAIL is a stop, not a note.** Do not copy back over a red gate: `$RENDER_TARGET` is still the
only copy of the render, and the live tree is still intact, which is the whole reason the gate
runs at this point and not after.

**A non-zero exit from any of the four is a hard stop.** Read the named record, fix it, re-run.
Never hand-patch the rendered tree: the next render undoes it, which is the defect store-primacy
exists to close.

### The gate failed on a page. Triage BEFORE you repair anything.

A `links-resolve`, `link-recall` or `source-paths` failure names a **page**, and the natural
reading is that the agent who wrote that page got it wrong. When two pages fail, **the agent may
be at fault for only one of them**, and repairing both the same way mangles correct prose to work
around a product bug.

So the first move is never a repair. It is one diff, with `PAGE` set to the page the gate named
(e.g. `PAGE='components/Some Page.md'`):

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # RUN_DIR, RENDER_TARGET
export RUN_DIR RENDER_TARGET
python - "${PAGE:?set PAGE to the page the gate named}" <<'PY'
import difflib, glob, json, os, sys
page = sys.argv[1]                       # e.g. components/Some Page.md
for f in sorted(glob.glob(os.path.join(os.environ["RUN_DIR"], "records", "*.json"))):
    doc = json.load(open(f, encoding="utf-8"))
    for rec in (doc.get("pages") or []):
        if rec.get("file") != page:
            continue
        rendered = open(os.path.join(os.environ["RENDER_TARGET"], page), encoding="utf-8").read()
        print(f"--- record: {os.path.basename(f)}")
        for line in difflib.unified_diff(rec["body"].splitlines(),
                                         rendered.splitlines(),
                                         "RECORD", "RENDERED", n=0, lineterm=""):
            print(line[:300])
PY
```

The first hunk is always the rendered frontmatter arriving as an addition - the record's
`body` carries no frontmatter, which is rendered from the store. That is noise; read past it.

Read the rest as a **fork**, not as a diff:

- **The record already carries the defect.** The agent wrote it. Repair the record (below) and
  re-run the step.
- **The record is clean and the rendered page is not.** Then the store or the renderer damaged
  it on the way through, and **repairing the record is the wrong move** — it edits correct
  content to satisfy a broken pipeline, and the damage returns on the next run against a
  different page. Fix the product and re-render. An example of the shape: a page body that
  merely *mentions* `[[` — documenting the syntax, as an autodoc corpus routinely does — can make
  a renderer swallow lines and strip the brackets off a real wikilink several lines later.

### Repairing a record

**Repair the record, never the rendered page.** Pages are regenerated from the store on every
render, so an edit to `$RENDER_TARGET` is erased by the next run — and would additionally trip
`assert-no-agent-writes`, correctly, as an unexplained write into the render target.

A repair is a normal, expected part of a run; two dozen agents writing a hundred-plus pages will not
be perfect, and the gate exists to catch the difference. Two constraints on what you may write:

- **Ground the repair, do not restore the old sentence.** A `link-recall` failure usually means
  the agent rewrote a passage and dropped a cross-reference on the way. Often the *rewrite* was
  right and only the link was lost. When the baseline cites a path that genuinely moved in the
  range, pasting the baseline sentence back reintroduces a stale fact to satisfy a link check.
  Verify the relationship still holds in `$SRC`, then write the link against the **new** text.
- **Say so in the run's own record of what happened**, so the next reader can tell an operator
  repair from agent output.

Then re-enter Step 4.5 from the top. `cli records` upserts by entity id, so re-ingesting a
repaired record is idempotent — and the assert at the top of the step now clears its own prior
render (see above), so the retry is runnable without deleting anything by hand.

### Backlog bookkeeping (done here, not by the Audit agent)

If backlog intake fed `auditPages`, the audit agent reported each resolution in `findings` as
`BACKLOG <bullet text> — [fixed|refuted]`. Edit `$AUTODOC/<backlogFile>` **now, after the
render**: change each resolved bullet to start with `- RESOLVED [fixed|refuted <date>]:`, keeping
the original text. Never delete lines. The agent does not do this itself because that file
holds no record — it is one of the human-owned files above, and an agent writing into the tree
mid-run is the hazard this step removes.

## Step 5 — Update manifest, log, hot

**The first two bullets below are executable blocks, not prose**, because `run-complete.js`
checks both at the very END of a run: a manifest write or a log entry left to the reader fails
there, after everything expensive has been paid for. Each opens with the carrier source line like
every other block below Step 1.

- **Manifest**: regenerate deterministically. `$source_repo`/`$source_branch`/`$source_path`/
  `$project` are already bound by Step 1, which reads them straight out of the manifest;
  `$project` is the same var the Step 3.5 graph rebuild passes to `graph build --project`.
  `--project` is a flag, not a seventh positional: the sixth slot is `generatedAt`, so a
  six-argument call with no `--project` refuses (exit 2) rather than writing its date into
  `project`. It scans the tree's frontmatter (created pages picked up automatically; refreshed
  `source_paths` read from the pages themselves; pages with `status: deprecated` frontmatter keep a
  `"status": "deprecated"` entry so Step 3.7's exclusion holds), and sets `last_sha`/`generated_at`
  from its args.
  **The backup of the old manifest is claimed, not named here.** The backup filename
  format lives in code, once, in `agentflow.backups`: `python -m agentflow.backups new <path>
  --firing <actor>-f<N>` creates the canonical name EMPTY and prints it, and `--backup-to` hands
  that claim to `write-manifest.js`, which fills it with the old manifest byte-for-byte only
  once the new one is known to be writable. The firing is `autodoc-update-f<unix seconds>`:
  this skill is not a loop and has no firing counter, and the run's own clock is the one real
  per-run number it has. A refused write (exit 1/2) copies nothing, so the empty claim is
  removed rather than left as a zero-length "backup". Never compose the name by hand: the
  format lives in `agentflow.backups` so that no caller carries its own copy of it.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, AUTODOC, TO, source_repo, source_branch, source_path, project
# manifest-backup
BAK=$(python -m agentflow.backups new "$AUTODOC/.manifest.json" --firing "autodoc-update-f$(date -u +%s)") || exit 1
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/write-manifest.js" \
  "$AUTODOC" "$source_repo" "$source_branch" "$source_path" "$TO" "$(date +%F)" \
  --project "$project" --backup-to "$BAK"
rc=$?
[ -s "$BAK" ] || rm -f "$BAK"   # an unfilled claim is not a backup
[ "$rc" -eq 0 ] || exit 1
# end manifest-backup
```

- **Log**: prepend an entry to `$AUTODOC/log.md`. The block below composes it and does the
  prepend; the header's date and sha range are computed, never typed.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC, FROM, TO
# FILL IN every REPLACE below from the workflow return before running this block. The literal
# `REPLACE` tokens are a PLACE, not a default: the guard beneath the heredoc refuses to prepend a
# half-written entry, which is what a markdown template with no command could not do.
[ -f "$AUTODOC/log.md" ] || : > "$AUTODOC/log.md"
cat > /tmp/autodoc-update-log-entry.md <<ENTRY
## [$(date +%F)] autodoc-update | $(printf '%s' "$FROM" | cut -c1-8)..$(printf '%s' "$TO" | cut -c1-8)
- Communities: REPLACE | Updated: REPLACE | Created: REPLACE | Deprecated: REPLACE | Audited: REPLACE (REPLACE fixed)
- New: REPLACE with wikilinks to created pages, or the word none
- Impact: REPLACE with one plain-English sentence, who notices and what changed for them. No codenames, no PR numbers.
- Note: REPLACE with one line on the most significant change
ENTRY
if grep -q REPLACE /tmp/autodoc-update-log-entry.md; then
  echo "FATAL: the log entry still carries REPLACE placeholders - fill the heredoc above and re-run this block"
  exit 1
fi
{ cat /tmp/autodoc-update-log-entry.md; echo; cat "$AUTODOC/log.md"; } > /tmp/autodoc-log.new \
  && mv /tmp/autodoc-log.new "$AUTODOC/log.md" \
  && echo "prepended log entry to $AUTODOC/log.md"
```

  Log rules, applied while filling the heredoc:
  - Date the entry by the **actual run date** (today), never an agent-reported date. The block
    does this for you — `date +%F` runs in the heredoc.
  - If `FROM..TO` overlaps a prior entry's range, append `(overlaps <that range>)` to the header —
    never let the same commits read as shipped twice.
  - If the run changed only documentation infrastructure (no product change documented), prefix
    the header with `[doc-ops]` so stakeholder reads can filter it out.
- **Hot**: refresh `$AUTODOC/hot.md` under a hard contract:
  - The **Latest** section covers this run's window only, is **≤120 words**, and sits under a
    literal `## Latest` heading — the run-completion gate below (`run-complete.js`, the last thing
    this runbook executes; there is no commit on this path) matches that exact heading
    (a hot.md without it fails the gate; restructure legacy hot files on their first gated run).
  - The **whole file is ≤400 words**. DELETE the prior Latest instead of demoting it to
    "Prior Latest" — history already lives in log.md; prepend-accretion is a defect, not a record.
  - Refresh the orientation sections (what the product is, load-bearing services, central flows)
    whenever services/flows/packs materially changed this run — they are in scope, not frozen at init.
  - Bump `last_sha`.

**`hot.md` may not exist.** The renderer does not produce one (it is in `_RESERVED_BASENAMES`, so
no page record may claim it either), so nothing on this path creates it: a corpus root can hold
`Glossary.md`, `index.md`, `log.md`, `overview.md` and `Start Here.md` and no `hot.md`, and the
refresh bullets above then describe editing a file that is not there. The run-completion gate then
hard-fails on
`hot.md missing`, at the very end of the run, after everything expensive has been paid for. So
**seed it when it is absent** and refresh it as described above when it is present:

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC, TO
# The seed exists to satisfy run-complete.js's hot-cache contract exactly, so it is written
# against the four things that file checks (run-complete.js:68-73): the run's short sha appears
# in the text; the whole file is <=400 words; there is a line that is literally `## Latest`
# (its regex is /^## Latest\s*$/m, so no trailing text and no decoration); and the Latest
# section — everything up to the next `## ` heading — is <=120 words.
SHORT_TO=$(printf '%s' "$TO" | cut -c1-8)
if [ -f "$AUTODOC/hot.md" ]; then
  echo "hot.md present — refresh it in place per the contract above (Latest <=120 words, file <=400)."
else
  cat > "$AUTODOC/hot.md" <<HOT
---
title: Hot Cache
updated: $(date +%F)
---

# Hot Cache

## Latest

Corpus refreshed by autodoc-update through commit $SHORT_TO on $(date +%F). This section was
seeded automatically because the corpus had no hot cache; replace it on the next run with what
actually changed in the window and who notices, keeping it under 120 words.

## Orientation

Not yet written. This is where the standing answer lives: what the product is, which services are
load-bearing, and the central flows. Refresh it whenever a run materially changes any of them. The
whole file stays under 400 words, and the prior Latest is deleted rather than demoted — history
lives in log.md.
HOT
  echo "seeded $AUTODOC/hot.md at $SHORT_TO"
fi
```

A seeded hot cache is a floor, not a deliverable: it passes the gate and says plainly that it was
machine-written, so the next run has something to refresh rather than something to invent. Do not
let it stand unedited for long — the Orientation section is the part a reader actually comes for.

Before finishing, run the run-completion gate — non-zero means this update is NOT done
(short sha = first 8 chars of the full sha — run-complete.js matches exactly that prefix;
full 40-char shas also pass):

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, AUTODOC
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/run-complete.js" "$AUTODOC"
```

- **Commit — RETIRED. There is nothing to commit.** The corpus sits at the resolved
  `autodoc_root` (resolution order:
  `<suite_root>/docs/ARCHITECTURE.md#four-pillars-separated-by-authorship`), which in the standard
  layout is outside the vault and outside any git repository:
  `git -C "$AUTODOC" rev-parse --show-toplevel` fails with *"fatal: not a git repository"*. A step
  that staged the corpus into its enclosing repo would get an empty repo path and do nothing, at the
  very end of a run whose whole fan-out has already been paid for. `lead-dev`'s autodoc-update
  bullet says the same: a `git -C <vault.root> add <autodoc_root>/` step is retired.

  **State the consequence rather than pretending a commit happened.** Version history for the
  corpus is meant to come from the vault MIRROR, exactly as it does for `design/`, and that mirror
  is not wired yet. Until it is, **a refreshed corpus is UNTRACKED**: every page is regenerable
  from the store (that is what store-primacy buys), but an accidental deletion of the tree has
  nothing to restore from. Say that in the run report. Do not reach for a substitute — `git init`
  in the corpus, or staging it into some nearby repo, creates a second history that the mirror
  will then have to reconcile with.

## Step 6 — Verify + report

- Confirm edited/created pages exist and have valid frontmatter with bumped `updated`.
- Grep the **generated** pages for leaked tool-call wrapper tags — any hit is a defect; strip it
  before reporting done:
  ```bash
  . "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC
  # --exclude-dir=.source, because $AUTODOC CONTAINS the source clone, and a clone of a repo that
  # carries this runbook contains its search strings: without the exclusion the autodoc-init and
  # autodoc-update SKILL.md files under .source/ match, the runbook finds ITSELF, and the hit branch
  # prints "LEAKED WRAPPER TAGS" on every clean run, which is how a check stops being read.
  # This is a SCOPE correction, not a mute: the defect being hunted is a wrapper tag an agent
  # bled into a page it WROTE, and nothing in .source/ is written by this run — it is a clone the
  # run resets to $TO. Narrowing to what the run produces is what makes a hit mean something.
  # A check that read nothing prints the same "clean" as one that read everything, so reading
  # nothing is a failure, not a pass: count the pages it can read first, then branch on grep's EXIT
  # CODE (0 a hit, 1 no hit, anything else grep could not read its target), never on its output.
  [ -n "$AUTODOC" ] || { echo "LEAK CHECK DID NOT RUN: \$AUTODOC is empty" >&2; exit 1; }
  pages_rc=0
  pages=$(grep -rl --include="*.md" --exclude-dir=.source -e '' "$AUTODOC") || pages_rc=$?
  if [ "$pages_rc" -ge 2 ] || [ -z "$pages" ]; then
    echo "LEAK CHECK DID NOT RUN: no readable .md page under '$AUTODOC' (grep exited $pages_rc)" >&2
    exit 1
  fi
  leak_rc=0
  grep -rn --include="*.md" --exclude-dir=.source -e '</content>' -e '</invoke>' -e '<parameter' "$AUTODOC" || leak_rc=$?
  case "$leak_rc" in
    0) echo "LEAKED WRAPPER TAGS — fix before done"; exit 1 ;;
    1) echo "clean" ;;
    *) echo "LEAK CHECK FAILED: grep exited $leak_rc reading '$AUTODOC'" >&2; exit 1 ;;
  esac
  ```
- Confirm `last_sha` advanced to `TO`.
- Report: range documented, communities touched, pages updated/created/deprecated, and any community agent that
  returned null (re-run those).

### Step 6.1 — Graph-reviewer gate (runs in Step 4.5, on the render target)

The deterministic **graph-reviewer** (`graph-check.js`, in the autodoc-**init** references dir,
shared module) validates the code-wiki against ground truth — the tree-sitter inventory plus
wikilink/frontmatter integrity. It runs as a plain Node process in the **skill main-loop**, NOT
inside a Workflow (the Workflow sandbox has no filesystem/Node access).

**The runnable block is in Step 4.5, not here, and nothing runs `--fix` on `$AUTODOC`.** It runs
over `$RENDER_TARGET`, immediately before the golden gate, with `--fail-on-fixable`. A `--fix` on
the live tree writes safe repairs (the reciprocal of a one-way `contract_with`, say) into pages that
no store record carries; the next render drops them, and the next run's golden gate reports a
`link-recall` loss on a page no agent touched. Only records change corpus content; this gate names
what needs changing and stops.

- `$RENDER_TARGET` = the fresh render of the store, `$INV` = `.source/.inventory.json` (built at
  `TO` in Step 3.5), `$SRC` = the clone (`.source/<repo>`, reset to `TO`). The report is written to
  `/tmp/autodoc-graph.json`.
- **Fixable findings FAIL the run and are never applied.** `--fail-on-fixable` computes what `--fix`
  would repair, writes no page, prints one `graph-check: fixable (not applied): <page>: <kind>:
  <detail>` line per finding on stderr, lists them under `fixable` in the report, and exits 1. The
  classes it detects:
  - broken wikilink with **exactly one** case-insensitive candidate;
  - **missing universal frontmatter** that has a safe default (`status`, `updated`);
  - **one-way `contract_with` pair** (the page named is the side missing the reciprocal);
  - **route-family alias gap** (`routes:` entry with no matching alias);
  - **dash-form frontmatter endpoint link** (`[[GET v1-notes]]`-class) with exactly one endpoint
    page matching its slash form;
  - **sanitized title with no alias**.
  Each is repaired in the record that renders the named page (or its counterpart), then the run
  re-renders from Step 4.5. Never hand-patch or `--fix` the rendered tree or `$AUTODOC`: the next
  render undoes it.
- **Blocker gate — the run FAILS (exit 1) on blocker-class residuals:** unexplained symbol-coverage
  gaps, non-existent `source_paths` (a page citing a file that isn't in the repo), **unresolved
  frontmatter relational links** (machine-consumed fields per the taxonomy — never advisory), and
  **non-existent diagram `%% source:` paths**. On a red, treat the update as incomplete: read
  `/tmp/autodoc-graph.json`, report the blockers, and re-run the affected communities — do NOT
  mark the update complete with blockers outstanding.
- **Warnings are reported, not fatal:** broken body-prose wikilinks with no candidate (advisory
  gap-markers per the taxonomy), orphans (pages with no inbound links), self-links in relational
  frontmatter, format-invalid structured fields, endpoint↔service `exposes_endpoints` asymmetry,
  and duplicate/over-budget/out-of-fence diagram issues. Surface them, but they do not fail the run.

Read `/tmp/autodoc-graph.json` with `python -c` (no jq) for the counts to include in the report —
and **pass the path in as `sys.argv[1]`**, never as a literal in the `-c` program. MSYS rewrites a
POSIX path in argv for a native Windows `python`; it does not touch string literals in the program
text, where `/tmp/...` resolves to `C:\tmp\...` instead. That directory exists on a stock Windows
box, so the same mistake in a *writing* script succeeds silently into the wrong place.

### Step 6.2 — Diagram Staleness (flag-don't-regenerate)

After the refresh, flag any flow/data-model page whose embedded diagram derives from source that
changed this update. A page's `diagram_source_sha` records the commit its diagram was drawn from; when
that predates a change to the source the diagram depicts, the diagram is stale. This step is
**FLAG-ONLY** — it reports which diagrams are stale plus a regeneration cost budget, and never rewrites
a diagram. Regeneration is a separate, explicit, budgeted action, never triggered here. Like the
coverage pre-pass and graph gate, it runs as a plain Node process in the **skill main-loop** (the
Workflow sandbox has no filesystem/Node access), and it runs AFTER the refresh workflow completes so
the refreshed pages already exist on disk.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, AUTODOC
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/diagram-staleness.js" "$AUTODOC" "$AUTODOC/.manifest.json"
```

`$AUTODOC` is the autodoc dir (the refreshed pages), and `$AUTODOC/.manifest.json` supplies
the source-SHA bookkeeping. The detector prints a staleness report (stale diagrams + regeneration cost
budget) and exits 0 — it is advisory, not a gate. Surface that report to the user and include it in the
update log's summary. Do NOT regenerate any diagram automatically; a stale flag is an invitation for an
explicit, budgeted regeneration pass, not a trigger for one.

### Step 6.5 — Coverage gate (changed symbols only)

Step 4.4 wrote `coverage: {pages, covered, excluded}` scoped to the changed files, out of this run's
own records. Verify every changed-file symbol from Step 3.5 is documented or explicitly excluded.
Build a diff-scoped inventory (just the changed-file symbols) and check it against that report —
mirrors init Step 6.5 but the inventory is filtered to `changedFiles` rather than the whole repo:

**Both of this gate's inputs are WRITTEN BY A COMMAND, and both must date to this run.** Files at
these fixed paths can be left on disk by an earlier run, and a gate reading them would answer
confidently from stale data — which is worse than no answer. The block below rebuilds the
inventory slice from this run's own checklists; the coverage report is written by **Step 4.4**,
from this run's records, because the workflow return is long gone by the time a run reaches this
gate. Both are refused unless they can be dated to this run.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT
# The inventory slice may not survive a run. Fixed /tmp paths plus "some earlier command wrote
# this" is the stale-carrier defect in another costume, and this block rebuilds the slice below.
# THE COVERAGE REPORT IS DELIBERATELY NOT REMOVED HERE, and that is not a stale-input hole:
# Step 4.4 writes it and Step 4.4 already cleared the previous run's copy before writing.
# Deleting it here would delete this gate's own input four steps after the only step that can
# produce it. Staleness is still refused - by the freshness check below, which is unchanged.
rm -f /tmp/autodoc-update-inv.json
# INPUT 1 - the changed-file symbol slice, BUILT from this run's own artifacts: the union of every
# changedCommunity's symbols, which with --checklist-dir (Step 3.5) live in $CHECKLIST_DIR/<key>.json
# and are referenced from /tmp/autodoc-changed-communities.json as checklistPath. A unit with an
# empty checklist keeps its inline `symbols` array and is read from there. checklistPath is written
# absolute by build-changed-communities.py, so nothing here has to join it to $CHECKLIST_DIR.
# EVERY /tmp PATH ARRIVES BY EXPORTED ENV VAR. `python` is a NATIVE Windows binary: MSYS rewrites a
# POSIX path in the environment and never inside the program text, so a literal "/tmp/x" below
# would read and WRITE C:\tmp\x -- which exists on a stock Windows box, so the write succeeds
# silently and the node gate two blocks down (reading bash's real /tmp via argv) reds instead.
CHANGED_COMMS=/tmp/autodoc-changed-communities.json \
UPDATE_INV=/tmp/autodoc-update-inv.json \
python - <<'PY' || exit 1
import json, os
comms = json.load(open(os.environ["CHANGED_COMMS"], encoding="utf-8"))
symbols, seen = [], set()
for entry in comms:
    rows = entry.get("symbols")
    if rows is None and entry.get("checklistPath"):
        rows = json.load(open(entry["checklistPath"], encoding="utf-8"))
    for s in rows or []:
        key = (s.get("name"), s.get("file"), s.get("line"))
        if key in seen:
            continue
        seen.add(key)
        symbols.append({"community": entry.get("key"), "name": s.get("name"),
                        "file": s.get("file"), "line": s.get("line")})
with open(os.environ["UPDATE_INV"], "w", encoding="utf-8") as fh:
    json.dump({"symbols": symbols}, fh, indent=2)
print("changed-symbol slice: %d symbol(s) across %d unit(s)"
      % (len(symbols), sum(1 for e in comms if e.get("key") != "symbolless")))
PY
# INPUT 2 - the coverage report, ALREADY ON DISK at /tmp/autodoc-update-coverage.json, WRITTEN BY
# STEP 4.4's block from this run's records. There is nothing to paste here and no command: the
# workflow return's `coverage` object lives in one tool result, hours and one gate earlier, so
# this gate reads the report Step 4.4 rebuilt from the records instead. If the file is missing
# or empty, go back to Step 4.4; do NOT hand-write one, because a value you can reconstruct by
# hand at this point is a value you cannot date to this run.
# A COMMAND, not the sentence above it: the freshness check below only STATS this path, so an
# absent one arrives as a FileNotFoundError traceback naming /tmp rather than the step that owes
# the file. Same shape as Step 4.5's re-check of the records manifest, and for the same reason.
[ -s /tmp/autodoc-update-coverage.json ] || { echo "FATAL: /tmp/autodoc-update-coverage.json missing - run Step 4.4 (records manifest + coverage report) first"; exit 1; }
# PROVE both inputs belong to THIS run before believing either: each must be newer than the run
# carrier, which Step 1 created. A file that predates the carrier came from some other run.
# BASH RESOLVES THE CARRIER, python only stats it. The indirection is the trap: if python read
# /tmp/autodoc-env.current itself and statted the path it CONTAINS, that path would arrive as file
# CONTENT, which is not argv and not the environment, so MSYS never rewrites it --
# `/tmp/autodoc-env-*.sh` would reach getmtime() as C:\tmp\autodoc-env-*.sh and the gate would raise
# FileNotFoundError on every run, whatever the coverage actually was. `$(cat ...)` hands the same
# value through the environment, where it IS rewritten.
ENV_CARRIER="$(cat /tmp/autodoc-env.current)" \
UPDATE_INV=/tmp/autodoc-update-inv.json \
UPDATE_COV=/tmp/autodoc-update-coverage.json \
python - <<'PY' || exit 1
import json, os
update_cov = os.environ["UPDATE_COV"]
carrier = os.environ["ENV_CARRIER"]
born = os.path.getmtime(carrier)
for path in (os.environ["UPDATE_INV"], update_cov):
    if os.path.getmtime(path) < born:
        raise SystemExit("FATAL: %s predates this run's carrier (%s) - it is another run's data" % (path, carrier))
rep = json.load(open(update_cov, encoding="utf-8"))
for k in ("pages", "covered", "excluded"):
    if k not in rep:
        raise SystemExit(
            "FATAL: %s has no %r key. It is written by Step 4.4 and must carry all three of "
            "{pages, covered, excluded} - re-run that block." % (update_cov, k)
        )
print("coverage inputs: fresh, and the report carries all three keys")
PY
# `file:///` PREFIX, AND IT IS THE WHOLE GATE. A bare dynamic import of an absolute Windows path
# gives Node ERR_UNSUPPORTED_ESM_URL_SCHEME - the loader reads `C:` as a URL scheme - so it would
# throw before checkCoverage is ever called and exit 1 on every corpus, a verdict independent of
# the truth. pathToFileURL is used rather than string concatenation because it is also correct on a
# POSIX box, where prefixing a leading-slash path with `file:///` yields four slashes.
node -e "const{pathToFileURL}=require('node:url');const fs=require('node:fs');import(pathToFileURL(process.argv[1]).href).then(m=>{const inv=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));const rep=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));const r=m.checkCoverage(inv,rep);console.log(r.summary);if(!r.ok){console.log('UNCOVERED:',r.uncovered.slice(0,20).map(s=>s.file+'::'+s.name).join(', '));process.exit(1);}})" "$SUITE_ROOT/skills/autodoc-init/references/inventory/coverage.js" /tmp/autodoc-update-inv.json /tmp/autodoc-update-coverage.json
```

If the gate fails, report the uncovered changed-file symbols and re-run the affected communities — do NOT
mark the update complete with unexplained coverage gaps in the changed set.

---

## What Not to Do

- **Don't hand-patch the rendered tree.** Every phase emits records; the renderer owns
  `$AUTODOC`, and an edit made there is undone by the next render with no error and no trace.
  Store-primacy exists to close exactly that defect — reintroducing it anywhere costs the
  guarantee, not just that one page.
- **Don't `graph render --force` into `$AUTODOC`.** It unlinks the existing `.md` files first, and
  several of them (`log.md`, `hot.md`, `CLAUDE.md`, any `Review Backlog*.md`) are produced by
  nothing, so there is nothing to restore them. Render to `$RENDER_TARGET` and sync back — Step 4.5.
- Don't re-init. Update touches only changed entities; a full rebuild churns git.
- Don't substitute a main-loop, page-by-page refresh when `Workflow` is missing. There is no
  single-agent fallback; Step 0's "Runtime guard — run this before Step 1" stops the run instead.
- Don't emit a record for a page whose documented contract didn't actually change — an unchanged
  page re-renders byte-identically from its stored record, so silence is how you avoid churn.
  There is no `updated:` to withhold; the renderer stamps it.
- Don't delete pages for removed code — deprecate them by emitting a record carrying
  `frontmatter.status: "deprecated"` and a `> [!stale]` callout in the body. A page absent from
  the store is a page the renderer deletes, so dropping the record is the one thing that really
  does lose it. The user prunes deliberately.
- Don't commit `.source/` (the clone) into the vault git.
- Always back up the manifest before rewriting it, through Step 5's block: the name is claimed
  from `agentflow.backups`, never composed by hand.

## Relationship to other skills

- `/autodoc-init` — the one-time whole-repo build + scaffold. Run once; update thereafter.
- `<suite_root>/skills/autodoc-init/references/taxonomy.md` (in autodoc-init) — the shared entity contract.
- `/wiki-ingest` — personal-wiki analogue; same conventions.

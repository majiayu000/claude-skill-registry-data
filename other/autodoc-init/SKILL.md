---
name: autodoc-init
description: "Generate a full code-documentation wiki from a source repo using an ultracode workflow. Clones the repo, scaffolds the autodoc structure, fans out parallel agents to map every endpoint, page, component, service, process, vendor, runbook, data-model, decision (ADR), flow, and job, synthesizes dependency-ordered guided tours, then builds the index/overview. Triggers on: /autodoc-init, autodoc init, build the code wiki, document the whole repo, generate autodoc, map the codebase into autodoc."
allowed-tools: Read Write Edit Glob Grep Bash Workflow
---

# autodoc-init: Whole-Repo Code Documentation

Build a persistent, cross-linked **code wiki** that mirrors the personal wiki's structure but
documents code. The output lives at the configured `autodoc_root` (`$AUTODOC`, resolved in the
Config preamble below). This is the code analogue of `/wiki` + `/wiki-ingest`: `/autodoc-init` is
the one-time scaffold-and-map; `/autodoc-update` keeps it current from commits.

The heavy mapping runs as an **ultracode Workflow** (parallel agents, one per packed work
unit of derived code communities). **Agents return RECORDS — they write no page content**
(store-primary): the records land in the graph store (`graph records`) and a
deterministic renderer (`graph render`) produces the markdown tree, so link integrity and
frontmatter completeness are true by construction, not audited after the fact. The skill
itself does the deterministic setup, the store/render step, and the gates around that
workflow.

Between the Flows and Tours phases, a **Diagram phase** adds ONE validated Mermaid diagram to each
flow page (a `sequenceDiagram` or `flowchart`) and each data-model page (an `erDiagram`) at
Context+Container abstraction, per the taxonomy's Diagram contract. Diagram targets are BATCHED
(default 8 per agent — the fan-out cap); each diagram is still individually gated by
`validate_mermaid.py` (2-attempt-then-omit): if it fails to validate twice, the page ships without a
diagram rather than with a broken one. The validated mermaid comes back as a record; the renderer
places the `## Diagram` section.

After the per-community mapping and Flows phases, a **Tours phase** synthesizes dependency-ordered
**guided tours** — `tours/<Subsystem> Tour.md` reading sequences that walk a new reader through a
subsystem bottom-up. An agent picks 3–6 subsystems and writes the per-step prose, but the step
*order* is deterministic: a topological sort over the wikilink graph
(`references/inventory/tour-order.js`, dependencies before dependents). The Tours phase runs after
Flows and before Index, so the Index phase includes the tour pages.

A deterministic tree-sitter pre-pass enumerates every symbol first; map agents receive it as a
coverage checklist and the run fails on unexplained gaps.

**Read `references/taxonomy.md` first.** It is the binding contract for the 12 entity types and
their frontmatter — workflow agents read it too, but you must understand it to verify their output.

---

## Inputs

- **Project** — the agentflow project (routing key) this autodoc documents, given as
  `AUTODOC_PROJECT` (e.g. `AUTODOC_PROJECT=app`), the same name `/autodoc-update` reads. **Set it
  whenever more than one project profile is installed under `~/.agentflow/config/projects/`**:
  the preamble REFUSES to start in that case rather than documenting whichever project the
  SESSION happens to default to. On a single-project box it is optional. The repo coordinates
  come from that project's profile: source repo + branch from `canonical_repo.host_ref` /
  `base_branch` — never a literal. `$PROJECT` is what the preamble resolves, not an input.
- **Autodoc path** — the project's autodoc root, resolved per project by
  `agentflow.config.resolve_autodoc_root` (resolved to `$AUTODOC` below). All output lands here.

If `$AUTODOC` already exists and is populated, STOP and tell the user to run `/autodoc-update`
instead (init is destructive of the nav layer). Offer `--force` to re-init from scratch.
`--force` never overrides the preamble's ownership check: a root whose `.manifest.json` names a
different `project` is another project's corpus, and the preamble exits there.

## Config preamble — resolve everything from agentflow config

Resolve the autodoc root, suite root, and repo coordinates from the agentflow config BEFORE any
step, exactly as `/autodoc-update` Step 1 resolves them. `AUTODOC` = `resolve_autodoc_root(env,
project)`: the project profile's `autodoc_root` override, then `environment.autodoc_root`, then
the derived `<data_root>/projects/<name>/autodoc/` when that directory exists. It is never read
bare off the environment: that field is machine-level, so on a box running two projects it names
ONE corpus, and an init that read it would build this project's pages into the corpus another
project's readers resolve to. `SUITE_ROOT` = `environment.suite_root` (skill-relative tool
paths resolve under it); repo owner/branch = the project profile's `canonical_repo`. **Fail
loudly if no root resolves** — autodoc cannot run without a root.

```bash
# INVALIDATE THE POINTER FIRST, before anything here can fail -- same rule and same reason as
# /autodoc-update Step 1: a failed preamble must leave no pointer, never the previous run's one.
rm -f /tmp/autodoc-env.current

# AUTODOC + SUITE_ROOT + PROJECT + REPO + BRANCH in one resolution, the same one /autodoc-update
# Step 1 runs (its comments carry the full reasoning). agentflow.config reads $AGENTFLOW_CONFIG or
# ~/.agentflow/config.
# HEREDOC, not `python -c '...'`: a comment below with an apostrophe in it would close a
# single-quoted -c string and the whole block would fail to parse.
# UNSET FIRST, THEN STOP ON THE PYTHON'S OWN STATUS. The guards below test that a value is
# non-empty, not that this block set it, and a shell that sourced a previous run's carrier
# already holds every one of these names. `eval "$(python ...)"` cannot see a refusal: eval
# returns the status of the text it evaluates, and a refusal prints none. Capturing first and
# exiting on the capture's status stops the run at the refusal, whatever the shell inherited.
unset AUTODOC SUITE_ROOT PROJECT REPO BRANCH
AUTODOC_CFG="$(python - <<'PY'
import os
import shlex
from agentflow.config import (
    AutodocRootError, ConfigError, config_home, load_environment, load_project,
    resolve_autodoc_root, resolve_project_name,
)
def emit(k, v): print(k + "=" + shlex.quote(v.replace(chr(92), "/")))  # backslash->slash for Git Bash
e = load_environment()
# EXPLICIT when the box is ambiguous. resolve_project_name() falls back to $AGENTFLOW_PROJECT,
# which is the SESSION's project: right for a lane, and for a skill run inside a lane defaulted
# to another project it builds that other project's corpus. $AUTODOC_PROJECT is how the invoker
# names the corpus; nothing in here can tell which one was meant, so ambiguity is refused.
explicit = os.environ.get("AUTODOC_PROJECT")
installed = sorted(p.stem for p in (config_home() / "projects").glob("*.md"))
if not explicit and len(installed) > 1:
    raise SystemExit(
        "FATAL: %d projects are installed (%s) and no AUTODOC_PROJECT was given, so which "
        "project this corpus documents is ambiguous. The session default (%r) is the project of "
        "the SESSION, not of the corpus. Re-run with AUTODOC_PROJECT=<name>."
        % (len(installed), ", ".join(installed), resolve_project_name())
    )
name = explicit or resolve_project_name()
if not name:
    raise SystemExit("FATAL: no project resolves - install a project profile or set AUTODOC_PROJECT=<name>; autodoc-init documents one project's repo.")
try:
    proj = load_project(name)
except ConfigError as err:
    raise SystemExit("FATAL: project %r does not load, so there is no repo to document: %s" % (name, err))
# RESOLVED per project, never the bare machine-level value, so the corpus lands where
# /autodoc-update, graph-query and doctor will look for this project's pages.
try:
    root = resolve_autodoc_root(e, proj)
except AutodocRootError as err:
    # The project's own root is empty while the machine-level root still holds a corpus.
    # Building beside it would leave two corpora and no way to tell which one is current.
    # For an INIT that corpus is another project's, so the resolver's generic remedy (move the
    # corpus to the resolved root) would move that project's pages into this one: name its owner.
    own, legacy = (str(p).replace(chr(92), "/") for p in (err.resolved, err.legacy))
    raise SystemExit(
        "FATAL: the autodoc root for project %r is ambiguous - its own root '%s' has no corpus, "
        "and the machine-level root '%s' holds another corpus.\n"
        "  remediation: give that corpus's project its own autodoc_root override pointing at '%s', "
        "set autodoc_root: null in environment.md, then re-run."
        % (name, own, legacy, legacy)
    )
if not root:
    raise SystemExit("FATAL: no autodoc root resolves for project %r - set autodoc_root in the project profile or environment.md (SCHEMA.md); autodoc cannot run without it." % (name,))
emit("AUTODOC", root)
emit("SUITE_ROOT", e.suite_root)
emit("PROJECT", name)
emit("REPO", proj.canonical_repo.host_ref)
emit("BRANCH", proj.canonical_repo.base_branch)
PY
)" || exit 1
eval "$AUTODOC_CFG"
# A python that exits 0 without emitting a name leaves it unset, not inherited: these catch that.
[ -n "$AUTODOC" ] || exit 1
[ -n "$SUITE_ROOT" ] || exit 1
[ -n "$PROJECT" ] || exit 1
[ -n "$REPO" ] && [ -n "$BRANCH" ] || exit 1
# ROOT-vs-NAME COHERENCE, the check /autodoc-update Step 1 makes against the same manifest field.
# A project with no override of its own resolves to the machine-level root, and that root may
# hold ANOTHER project's corpus: the populated-root STOP under Inputs is prose, and --force skips it, so
# this refusal holds under --force too. A manifest whose project is null names no owner and
# passes.
if [ -f "$AUTODOC/.manifest.json" ]; then
  MANIFEST_PROJECT="$(python -c '
import json, sys
v = json.load(open(sys.argv[1], encoding="utf-8")).get("project")
print("" if v is None else v)
' "$AUTODOC/.manifest.json")" || { echo "FATAL: $AUTODOC/.manifest.json does not read, so whose corpus this root holds is unknown" >&2; exit 1; }
  if [ -n "$MANIFEST_PROJECT" ] && [ "$MANIFEST_PROJECT" != "$PROJECT" ]; then
    echo "FATAL: the corpus at $AUTODOC says it documents '$MANIFEST_PROJECT', but this run" >&2
    echo "       resolved project '$PROJECT'. Refusing to build over another project's pages," >&2
    echo "       with or without --force. Give '$PROJECT' its own autodoc_root override." >&2
    exit 1
  fi
fi
REPO_STEM="${REPO##*/}"
VALIDATE_MERMAID="python $SUITE_ROOT/scripts/validate_mermaid.py"

# THE RUN CARRIER, the same one /autodoc-update Step 1 builds (read its rationale there). Every
# fenced block is its own shell, so a value minted here or in Steps 1-4 is empty by the time a
# later block reads it unless something carries it. One per-run file, created empty here so it
# cannot inherit a previous run's values; every later block sources it through the fixed pointer,
# and every block that mints a cross-block variable appends it with env_put. The pointer is shared
# with /autodoc-update: one autodoc run per machine at a time, as the fixed /tmp paths already
# assume.
AUTODOC_ENV="/tmp/autodoc-env-$(date +%Y%m%dT%H%M%S)-$$.sh"
: > "$AUTODOC_ENV"
# Braced ${1}/${2}, never a bare dollar-digit: loaded through the Skill tool with arguments, the
# harness rewrites a bare dollar-digit anywhere in this body - fences included - before bash sees
# it, and leaves the braced form alone.
printf 'AUTODOC_ENV=%q\n' "$AUTODOC_ENV" >> "$AUTODOC_ENV"
cat >> "$AUTODOC_ENV" <<'CARRIER'
env_put() { printf '%s=%q\n' "${1}" "${2}" >> "$AUTODOC_ENV"; }
CARRIER
. "$AUTODOC_ENV"
env_put PROJECT "$PROJECT"
env_put AUTODOC "$AUTODOC"
env_put SUITE_ROOT "$SUITE_ROOT"
env_put REPO "$REPO"
env_put BRANCH "$BRANCH"
env_put REPO_STEM "$REPO_STEM"
env_put VALIDATE_MERMAID "$VALIDATE_MERMAID"
# Written LAST, so it exists only across a preamble that ran to completion.
printf '%s\n' "$AUTODOC_ENV" > /tmp/autodoc-env.current
echo "run carrier: $AUTODOC_ENV"
```

**Every block from here down opens by sourcing that carrier**, with the same line:
`. "$(cat /tmp/autodoc-env.current)" || exit 1`. A missing pointer fails that line; an empty
carrier does not, which is why the preamble removes the pointer first and writes it last.

---

## Step 0 — Runtime guard (before the clone)

Three prerequisites this run cannot start without, checked here rather than discovered after the
clone, the inventory and the community derivation have already run. Autodoc is off at install by
default, so provision step 6 — `npm ci`, then the `autodoc_graph` install into the suite venv —
never ran on a machine that set `autodoc_root` afterwards. Unchecked, that surfaces only at Step
2.5's `python -m autodoc_graph.cli build`, as a `ModuleNotFoundError`.

1. **`Workflow` in this session's tool list.** Bash cannot see it; you can. Step 3's mapping runs
   through it and there is **no single-agent fallback** — a plain sequential crawl is forbidden
   (What Not to Do). If it is absent, STOP here and tell the user to enable the `Workflow` tool for
   this session; do not run the block below or anything after it.
2. **`autodoc_graph` importable and `node` on PATH** — the block below. It must exit 0.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # nothing read from it here; every block opens this way
missing=""
# Same bare `python` every later `python -m autodoc_graph.cli` call resolves. stderr is left
# visible on purpose: an import that fails for another reason (a broken sqlite-vec, say) must
# say so rather than read as "not installed".
python -c "import autodoc_graph" || missing="$missing autodoc_graph"
command -v node >/dev/null || missing="$missing node"
if [ -n "$missing" ]; then
  echo "STOP: missing:$missing. Install Node LTS (with npm) if it is absent, then re-run" \
       "'python $SUITE_ROOT/install/provision.py --autodoc' (install step 6:" \
       "npm ci + the autodoc_graph install into the suite venv), adding --no-auto-allow if the" \
       "auto-allow hooks were declined (a re-run without it writes them back); then restart" \
       "/autodoc-init." >&2
  exit 1
fi
echo "runtime guard: autodoc_graph importable, node on PATH"
```

On a STOP, report the remedy to the user and end the run. Nothing has been cloned or written yet,
so there is nothing to clean up.

## Step 1 — Clone the source repo

Clone fresh into a gitignored scratch dir inside the autodoc folder so `/autodoc-update` can `git pull`
and diff later. Do NOT commit the clone into the autodoc's git repo.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC, REPO, BRANCH, REPO_STEM, env_put
SRC="$AUTODOC/.source/$REPO_STEM"
mkdir -p "$AUTODOC/.source"
# gh provides the token for private repos
if [ -d "$SRC/.git" ]; then git -C "$SRC" fetch --depth 1 origin "$BRANCH" && git -C "$SRC" reset --hard "origin/$BRANCH"
else gh repo clone "$REPO" "$SRC" -- --depth 1 --branch "$BRANCH"; fi
COMMIT=$(git -C "$SRC" rev-parse HEAD) || exit 1
env_put SRC "$SRC"
env_put COMMIT "$COMMIT"
echo "Cloned $COMMIT"
```

Ensure `.source/` is gitignored (add to `$AUTODOC/.gitignore` if missing). The clone can be
10MB+; it must never enter the autodoc repo's git history.

## Step 2 — Scaffold the autodoc structure

Create the folder tree under `$AUTODOC`, the 12 type folders, a wiki-style `CLAUDE.md`, and empty
meta files. Use the scaffold in `references/scaffold.md` (folder list + CLAUDE.md template);
substitute its `<autodoc-dir>` placeholder with the basename of `$AUTODOC` and `<repo>` with `$REPO`.
Folders: `endpoints pages components services processes vendor runbooks data-models decisions flows jobs tours`.
The workflow's Index phase fills `_index.md` / `index.md` / `overview.md` and the two maintained
meta pages `Start Here.md` / `Glossary.md` (see the taxonomy's "First-Class Meta Pages" section);
you write `CLAUDE.md`, `log.md`, `hot.md`, `.manifest.json`, `.gitignore`.

## Step 2.5 — Tree-sitter coverage pre-pass + community derivation (deterministic)

Build the symbol inventory AND the community partition BEFORE launching the workflow. These run
as plain Node/Python processes in the skill main-loop (the Workflow sandbox has no
filesystem/Node access). There is no hand-written area map: the partition is derived from the
symbol graph, and a deterministic packing step bins
whole communities into band-clamped **work units** — the `--band` (default 8:24) is the
agent-count/cost budget, NOT a partition property. A repo can legitimately have hundreds or
thousands of communities (the count can never drop below the graph's connected-component
floor); packing absorbs any count, so the run completes with shipped defaults on every
non-empty corpus. Hard failure is reserved for an empty corpus or invalid band values.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC, SUITE_ROOT, SRC, REPO, COMMIT, REPO_STEM, PROJECT, BRANCH, env_put
INV="$AUTODOC/.source/.inventory.json"
GRAPH_JSONL="$AUTODOC/.source/.graph.jsonl"
GRAPH_DB="$AUTODOC/.source/graph.db"
COMM="$AUTODOC/.source/.communities.json"
# GRAPH_JSONL is read only inside this block, so it does not travel.
env_put INV "$INV"
env_put GRAPH_DB "$GRAPH_DB"
env_put COMM "$COMM"
( cd "$SUITE_ROOT/skills/autodoc-init/references/inventory" && test -d node_modules || npm install )
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/extract-inventory.js" "$SRC" "$INV" "$REPO" "$COMMIT"
# AST edge extraction -> graph store -> derived communities (the graph CLI is
# `python -m autodoc_graph.cli`, provisioned into the suite venv by install step 6)
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/emit-graph.js" "$SRC" "$GRAPH_JSONL" "$REPO_STEM" "$COMMIT" "$REPO"
python -m autodoc_graph.cli build --db "$GRAPH_DB" --corpus "$REPO_STEM" --jsonl "$GRAPH_JSONL" \
  --repo-ref "$REPO" --project "$PROJECT" --branch "$BRANCH"
# COMM_PINS: one `--pin PREFIX=NAME` pair per entry of the profile's optional
# `communities.pins` block, BUILT HERE, before the call that consumes it. Pin names
# may contain spaces, so it is an array read one per line and expanded quoted.
# The python runs in a command substitution so a failed profile load stops the run
# instead of silently yielding zero pins (unpinned partitions, no warning).
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
python -m autodoc_graph.cli communities --db "$GRAPH_DB" --corpus "$REPO_STEM" --emit "$COMM" "${COMM_PINS[@]}"
```

`COMM_PINS` is an empty bash array unless the project profile's optional `communities.pins`
block is set — then it carries one `--pin PREFIX=NAME` pair per entry (the deliberately weak
escape hatch; unlisted paths stay derived). It is expanded as `"${COMM_PINS[@]}"`, never bare:
a bare `$COMM_PINS` is only the array's first element, `--pin`, which the parser rejects for
want of a value. All three artifacts
live beside the clone and are gitignored (the `.source/` rule covers them). Read
`.communities.json` with `python -c` (no jq): `units` is the work-unit list — each unit is
`{key, label, symbol_count, communities: [{id, label, descriptor, member_ids, symbols}]}`,
where each unit holds WHOLE communities (packing never merges or relabels them) —
`fanout_level`/`levels`/`component_floor` give the hierarchy counts for the report. The
community store is APPEND-ONLY: rows are never auto-deleted; the current partition is anchored
by `entity.community_id` + `parent_id` chains, and dissolved rows carry
`descriptor.dissolved` — always consume the fresh artifact, never raw store listings. A
non-zero `communities` exit means an empty corpus, invalid band values, or a symbol that went
uncommunitied — STOP and report; do not improvise a fan-out.

## Step 3 — Launch the mapping workflow (ultracode, records-only)

This is the `/ultracode` step — the user has opted into multi-agent orchestration by invoking this
skill. **Agents return RECORDS; they write no page content.** The deterministic renderer
(Step 4) produces the markdown tree from the store. First dump the single-sourced prompt templates
(the workflow sandbox cannot import modules):

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, AUTODOC, SRC, COMMIT, env_put
node "$SUITE_ROOT/skills/autodoc-init/references/prompts/render-prompt.js" --dump > /tmp/autodoc-prompts.json
# The run's records directory MUST start empty — leftovers from a prior attempt
# at the same runDir would otherwise be swept into ingestion (Step 4 also
# manifest-gates against this). Named from the carried $COMMIT, not HEAD, and guarded:
# a failed rev-parse would otherwise name the directory `.run-`.
SHORT=$(git -C "$SRC" rev-parse --short "$COMMIT") || exit 1
RUN_DIR="$AUTODOC/.source/.run-$SHORT"   # = args.runDir below
# Where the workflow return is written once it arrives (below), and what Step 4 passes as
# --manifest. A prior attempt's return at the same RUN_DIR goes with its records.
RUN_RETURN="$RUN_DIR/workflow-return.json"
rm -rf "$RUN_DIR/records" "$RUN_RETURN" && mkdir -p "$RUN_DIR/records" || exit 1
env_put RUN_DIR "$RUN_DIR"
env_put RUN_RETURN "$RUN_RETURN"
```

Launch the workflow via the **Workflow** tool with `scriptPath` pointing at the bundled script,
passing args:

```
Workflow({
  scriptPath: "$SUITE_ROOT/skills/autodoc-init/references/init-workflow.js",
  args: {
    repoPath:           "$SRC",                 // $AUTODOC/.source/$REPO_STEM
    autodocName:        "<basename of $AUTODOC>",
    repoName:           "$REPO",                // = canonical_repo.host_ref
    commitSha:          "<COMMIT from step 1>",
    date:               "<today YYYY-MM-DD>",
    taxonomyDocPath:    "$SUITE_ROOT/skills/autodoc-init/references/taxonomy.md",
    validateMermaidCmd: "$VALIDATE_MERMAID",    // python $SUITE_ROOT/scripts/validate_mermaid.py
    scratchPath:        "$AUTODOC/.source/.diagram-scratch",   // drafts only, never the render target
    tourOrderPath:      "$SUITE_ROOT/skills/autodoc-init/references/inventory/tour-order.js",
    runDir:             "$RUN_DIR",             // $AUTODOC/.source/.run-<short-sha>; agents write records files under <runDir>/records/
    prompts:            "<contents of /tmp/autodoc-prompts.json>",
    units:              "<units from .communities.json — [ {key,label,communities:[{id,label,descriptor}]}, ... ]>",
    communitySymbols:   "<checklists keyed by COMMUNITY ID — { \"<id>\": [ {kind,name,file,line}, ... ] }>",
    parents:            "<parents from .communities.json — [ {id,level,label,children:[ids]} ] (children-first)>",
    maxAgents:          32,                     // hard ceiling; over-budget fails BEFORE dispatch
    diagramReserve:     2,                      // diagram batches reserved in the pre-dispatch check
    diagramBatch:       8,                      // preferred diagram targets per agent (each still gated individually)
    maxDiagramBatch:    12                      // widen-to-fit cap when the remaining budget is tight
  }
})
```

**Records are DISK-BASED**: every agent writes its records JSON to
`<runDir>/records/<label>.json` and returns only a light manifest (paths + counts) — page
bodies never travel through the workflow return (a full large-repo run would be megabytes). The
workflow return carries `records: {runDir, files}` and hard-fails if anything inlines bulk
data.

**Agent-budget arithmetic (fail-fast, never mid-flight).** The pre-dispatch check is
`units + multiChildParents + 3 (flows/tours/index) + diagramReserve <= maxAgents`.
SINGLE-child parents cost nothing — they collapse and inherit their child's report verbatim
at `graph records` time. At the Diagram phase the batch size WIDENS (up to `maxDiagramBatch`, default 12)
to fit whatever budget remains, so a run that passed pre-dispatch cannot die at the Diagram
wall — and a widened phase that quietly omits >30% of its diagrams FAILS the run naming the
rate (quality collapse is loud, never a footnote). Two worked examples:

- **Shipped defaults** (e.g. a repo that packs into 24 units at `--band 8:24`, 4 parents of which 2
  single-child): pre-dispatch `24 + 2 + 3 + 2 = 31 ≤ 32` ✓; up to 36 diagram targets (3 remaining
  slots × batch 12) fit, so total ≤ 32.
- **Large-repo tuning example** (≤ 30 agents from 82 communities): pass `--band 8:14` at Step 2.5
  and `maxAgents: 30` here → `14 + ~3 + 3 + 2 = 22 ≤ 30` pre-dispatch; ~50 diagram targets (43
  data-models + ~7 flows) fit the remaining ~8 slots at batch ≤ 8. Total ≤ 30.

If the ceiling trips, the error names every term — narrow `--band` (fewer, larger map units)
or raise `maxAgents` deliberately; never re-run and hope.

Pass `validateMermaidCmd` so the Diagram phase's gate resolves under the suite root (never a
personal absolute path). Substitute the resolved values of `$SUITE_ROOT`/`$SRC`/`$AUTODOC`/`$REPO`/
`$VALIDATE_MERMAID`/`$COMMIT`/`$RUN_DIR` as the carrier holds them
(`cat "$(cat /tmp/autodoc-env.current)"`), not from memory.

Build the community args from `.communities.json` (Step 2.5): pass `units` verbatim (minus each
community's `symbols` array), `communitySymbols` = `{ str(community.id): symbols }` collected
across all units, and `parents` verbatim (the report roll-up chain — one agent per parent reads
only its children's reports). All three are REQUIRED — the workflow fails loudly on a missing or
empty checklist, and `parents: []` must be passed EXPLICITLY on a smoke slice.

The workflow computes its agent count (map units + parents + flows/tours/index + diagram batches)
and **fails before the first dispatch when it exceeds `maxAgents`** — narrow `--band` or raise the
ceiling deliberately; never let a run die mid-flight at a credit cap.

The workflow runs in the background and notifies you on completion. It returns
`{ agentsDispatched, totalPages, pagesByType, records: {pages, reports, meta_pages, diagrams},
coverage, ... }`.

**The moment it returns, write that return to `$RUN_RETURN`** — its `records.files` list is the
authoritative manifest Step 4 passes to `graph records --manifest`, and nothing else persists it:

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # RUN_RETURN, RUN_DIR
# PASTE the workflow return JSON between the RETURN markers, verbatim. Left empty, the file is
# empty and the guard below stops here rather than after Step 4 has started.
cat > "$RUN_RETURN" <<'RETURN'
RETURN
test -s "$RUN_RETURN" || { echo "FATAL: $RUN_RETURN is empty - paste the workflow return into this block" >&2; exit 1; }
# Validate the paste the way /autodoc-update Step 4.4 does. Paths arrive by exported env var,
# never in the program text: python is a native binary, and MSYS rewrites a POSIX path in argv
# or the environment but never inside the body.
RUN_DIR="$RUN_DIR" RUN_RETURN="$RUN_RETURN" python - <<'PY' || { rm -f "$RUN_RETURN"; exit 1; }
import json, os
run_dir = os.environ["RUN_DIR"].replace(chr(92), "/").rstrip("/") + "/records/"
run_return = os.environ["RUN_RETURN"]
ret = json.load(open(run_return, encoding="utf-8"))
files = (ret.get("records") or {}).get("files") if isinstance(ret, dict) else None
if not isinstance(files, list) or not files:
    raise SystemExit("FATAL: %s carries no non-empty records.files list. The workflow return is "
                     "the only authority on which record files the agents wrote." % run_return)
missing = [f for f in files if not os.path.isfile(f)]
if missing:
    raise SystemExit("FATAL: %d records file(s) do not exist on disk: %s" % (len(missing), ", ".join(missing[:5])))
# A paste left over from an EARLIER run names another run's directory, and fails here.
stray = [f for f in files if not f.replace(chr(92), "/").startswith(run_dir)]
if stray:
    raise SystemExit("FATAL: %d records file(s) sit outside %s - stale paste from an earlier run? %s"
                     % (len(stray), run_dir, ", ".join(stray[:5])))
print("workflow return: %d records file(s) -> %s" % (len(files), run_return))
PY
```

**Smoke / partial runs:** to validate against one slice first, pass a single-entry `units`
array (one unit from `.communities.json`) plus the `communitySymbols` entries for its
communities, and `parents: []`. Same script, fewer agents.

## Step 4 — Write records to the store, then render (deterministic)

The render target is a **sibling** directory — never the live tree; replacing the live tree is the
explicit, human-approved cutover in Step 6.5.

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC, SUITE_ROOT, GRAPH_DB, REPO_STEM, COMMIT, COMM, RUN_DIR, RUN_RETURN, env_put
RENDER_TARGET="$AUTODOC.rendered"
# The render stamp: a snapshot of $RENDER_TARGET taken right after `cli render` exits 0, OUTSIDE
# the target. Same flow and same flags as /autodoc-update Step 4.5.
STAMP="$RENDER_TARGET.render-stamp.json"
env_put RENDER_TARGET "$RENDER_TARGET"
env_put STAMP "$STAMP"
# HARD GATE: no agent may write page content. The target must be empty before rendering, OR hold
# exactly the files this runbook's previous render stamped (a red Step 5 gate leaves it populated,
# and the retry must not die accusing an agent). --clear-prior-render clears only a tree that
# matches the stamp file-for-file; any unstamped file, or no stamp at all, still exits 1.
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/assert-no-agent-writes.js" "$RENDER_TARGET" --stamp "$STAMP" --clear-prior-render || exit 1
# The workflow return Step 3 wrote: its records.files list is the authoritative manifest —
# ingestion then errors on any orphan *.json a prior attempt left in the directory. cli.py opens
# it with a bare open(), so an unwritten one is caught here, by name:
test -s "$RUN_RETURN" || { echo "FATAL: $RUN_RETURN is missing or empty - write the workflow return (end of Step 3) first" >&2; exit 1; }
python -m autodoc_graph.cli records --db "$GRAPH_DB" --corpus "$REPO_STEM" \
  --records "$RUN_DIR/records" --manifest "$RUN_RETURN" \
  --sha "$COMMIT" --date "$(date +%F)" \
  --artifact "$COMM" --join-floor 0.8 \
  --coverage-out /tmp/autodoc-coverage.json || exit 1
python -m autodoc_graph.cli render --db "$GRAPH_DB" --corpus "$REPO_STEM" --out "$RENDER_TARGET" || exit 1
# IMMEDIATELY after a render that exited 0, and nowhere else: written earlier it would account
# for files nothing had produced yet; written after the gates it would not exist on the one path
# that needs it (a red gate, then a retry of this step).
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/assert-no-agent-writes.js" --write-stamp "$RENDER_TARGET" --stamp "$STAMP" || exit 1
python -m autodoc_graph.cli check  --db "$GRAPH_DB" --corpus "$REPO_STEM" --out /tmp/autodoc-store-check.json
```

**Retrying after a red Step 5 gate** is re-writing records and re-running this block as is: the
target still holds the previous render, the stamp accounts for every file in it, and the
assertion clears it and continues. A file the stamp does not list (or a stamped file that has
since vanished) still stops the run — that is an unexplained write, not a leftover render.

**Retrying after `cli render` itself exited non-zero is different:** the renderer writes pages one at
a time, so a failure partway leaves a partial tree that no stamp describes. Remove
`$RENDER_TARGET` by hand before re-running this block; left in place, the assertion correctly reads
it as an unexplained write and stops.

- `graph records` is the ONLY write path for the concept tier: it derives every entity id
  (agents never mint ids), enforces the closed `documents`/`depends_on`/`part_of`/`related`
  vocabulary (a record with any other rel fails the run naming it), resolves every `documents`
  citation to a real symbol entity, rejects duplicate (CASE-INSENSITIVELY — the tree may land
  on a case-insensitive filesystem), reserved, and nested page paths, stamps
  `summarized_at_sha` on every community report, INHERITS single-child parent reports verbatim
  from their child (`--artifact` — the collapse the workflow budgeted for), and fails when any
  unit/parent community ends the run without a report or when the
  endpoint/component/data-model/job symbol-join rate is under the `--join-floor`.
  `--coverage-out` aggregates every map agent's covered/excluded evidence for Step 5b.
- `graph render` writes the markdown tree: frontmatter stamped by the renderer, `related:`/
  `depends_on:` rendered from edge rows (dreamed edges never render), flow backlinks by inverse
  traversal, unresolvable links dropped and reported. **Rendering twice is byte-identical** on an
  unchanged store — verify on the first run: render to a second temp dir and `diff -r`.
- A non-zero exit from any of the three is a hard stop: read the named record/community, re-run
  the offending unit as a smoke slice, re-write records. Never patch the rendered tree by hand.

## Step 5 — Deterministic gates over the RENDERED tree

All gates run against `$RENDER_TARGET`; the live `$AUTODOC` tree stays untouched — it IS the
frozen baseline the golden gate measures against. Like the coverage pre-pass, everything here
runs as plain Node processes in the **skill main-loop** — NOT inside a Workflow.

### 5a — Graph-reviewer

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, RENDER_TARGET, INV, SRC
# Reuse the npm-install guard from Step 2.5 (idempotent).
( cd "$SUITE_ROOT/skills/autodoc-init/references/inventory" && test -d node_modules || npm install )
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/graph-check.js" "$RENDER_TARGET" "$INV" "$SRC" /tmp/autodoc-graph.json
GRAPH_RC=$?
```

**No `--fix`.** The renderer builds every wikilink from a store row that resolved, stamps the
universal frontmatter itself, and drops (never repairs) unresolvable links — so on a rendered
tree, zero broken wikilinks and zero frontmatter gaps are the EXPECTATION, not an aspiration.
Any blocker here is a defect in the records/render path: fix the records (re-run the offending
unit as a smoke slice) and re-render. Never hand-patch or auto-fix the rendered tree — the next
render would silently undo it.

Blocker classes (exit 1): unexplained symbol-coverage gaps, non-existent `source_paths`,
unresolved frontmatter relational links, non-existent diagram `%% source:` paths. Warnings
(orphans, alias collisions, field formats, …) are reported, not fatal.

### 5b — Coverage gate

Verify every inventoried symbol is documented or explicitly excluded:

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, INV
node -e "import('$SUITE_ROOT/skills/autodoc-init/references/inventory/coverage.js').then(async m=>{const fs=await import('node:fs');const inv=JSON.parse(fs.readFileSync('$INV','utf8'));const rep=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));const r=m.checkCoverage(inv,rep);console.log(r.summary);if(!r.ok){console.log('UNCOVERED:',r.uncovered.slice(0,20).map(s=>s.file+'::'+s.name).join(', '));process.exit(1);}})" /tmp/autodoc-coverage.json
```

(`/tmp/autodoc-coverage.json` was written by `graph records --coverage-out` in Step 4 —
the aggregate of every map agent's records file.) If the gate fails,
report the uncovered symbols and re-run the affected communities as a smoke slice — do NOT mark the
autodoc complete with unexplained coverage gaps.

### 5c — Golden-output gate (rendered vs frozen baseline)

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, RENDER_TARGET, AUTODOC, SRC, INV
cat > /tmp/golden-gate.json <<'EOF'
{ "pageSetSymmetricDiffBudget": 12 }
EOF
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/golden-gate.js"   "$RENDER_TARGET" "$AUTODOC" /tmp/golden-gate.json "$SRC" "$INV"
```

The budget is a **declared, human-reviewed number** (the example 12 is about 10% of a 116-page
baseline) — never widen it mid-run to make the gate pass; a blown budget means the
mapping genuinely diverged and a human decides whether that is progress or regression. The gate
prints one PASS/FAIL line per assertion (page-set, type-match, frontmatter, links-resolve,
link-recall, source-paths, blocker-parity, coverage-parity) and exits non-zero on any FAIL.

### 5d — Sanity greps

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # RENDER_TARGET
# A check that read nothing prints the same "clean" as one that read everything, so reading
# nothing is a failure, not a pass: count the pages it can read first, then branch on grep's EXIT
# CODE (0 a hit, 1 no hit, anything else grep could not read its target), never on its output.
[ -n "$RENDER_TARGET" ] || { echo "LEAK CHECK DID NOT RUN: \$RENDER_TARGET is empty" >&2; exit 1; }
pages_rc=0
pages=$(grep -rl --include="*.md" -e '' "$RENDER_TARGET") || pages_rc=$?
if [ "$pages_rc" -ge 2 ] || [ -z "$pages" ]; then
  echo "LEAK CHECK DID NOT RUN: no readable .md page under '$RENDER_TARGET' (grep exited $pages_rc)" >&2
  exit 1
fi
leak_rc=0
grep -rn --include="*.md" -e '</content>' -e '</invoke>' -e '<parameter' "$RENDER_TARGET" || leak_rc=$?
case "$leak_rc" in
  0) echo "LEAKED WRAPPER TAGS — fix the records before done"; exit 1 ;;
  1) echo "clean" ;;
  *) echo "LEAK CHECK FAILED: grep exited $leak_rc reading '$RENDER_TARGET'" >&2; exit 1 ;;
esac
```

Confirm `overview.md` contains its one mermaid architecture diagram, `Start Here.md` and
`Glossary.md` exist and are populated, and spot-check 2–3 pages (frontmatter, source_paths,
wikilinks, no pasted code dumps). Byte-determinism check on first runs: render again into a temp
dir and `diff -r` — any difference is a renderer bug.

## Step 6 — Cutover (explicit, separate, human-approved)

Replacing the live tree is NEVER a side effect of a run. Only after every Step 5 gate is green
AND the human approves the swap:

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # AUTODOC, RENDER_TARGET, STAMP
mv "$AUTODOC" "${AUTODOC}.pre-store.bak"       # the frozen baseline is kept, not overwritten
mv "$RENDER_TARGET" "$AUTODOC"
# The render stamp describes a directory that no longer exists; it goes with it.
if [ -n "$STAMP" ]; then rm -f "$STAMP"; fi
mv "${AUTODOC}.pre-store.bak/.source" "$AUTODOC/.source"   # clone + graph.db + artifacts travel
# Skill-owned files the renderer does not write:
for f in CLAUDE.md log.md hot.md .gitignore; do
  [ -f "${AUTODOC}.pre-store.bak/$f" ] && cp "${AUTODOC}.pre-store.bak/$f" "$AUTODOC/$f"
done
```

The renderer's `.rendered-by-store` marker travels with the tree, and it is what routes the
next refresh: `/autodoc-update` Step 0 finds it, sets `STORE_PRIMARY=1`, and takes its records
path (agents emit records, `graph records` lands them, `graph render` re-renders). Post-cutover
refreshes are `/autodoc-update`, never a re-run of this skill on the populated tree.

## Step 6.5 — Post-cutover bookkeeping: manifest, log, hot cache

Run the deterministic manifest writer — it derives `pages` by scanning the live tree's
frontmatter (never the Workflow return, which does not survive a run that dies mid-flight):

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, AUTODOC, REPO, BRANCH, REPO_STEM, COMMIT, PROJECT
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/write-manifest.js"   "$AUTODOC" "$REPO" "$BRANCH" ".source/$REPO_STEM" "$COMMIT" "$(date +%F)" --project "$PROJECT"
```

It takes no backup here: without `--backup-to` an existing manifest is overwritten and stderr
says so (the backup name is claimed from `agentflow.backups` by the caller, which
`/autodoc-update` does and this freshly rendered tree does not need). It emits exactly the seven
top-level keys (source_repo, source_branch, source_path, project, last_sha, generated_at,
pages), sorts page keys (byte-identical on re-run against an unchanged tree), and FAILS the run
(exit 1, offending page named) on any page missing `type` frontmatter. `project` is carried so
`/autodoc-update` can pass `graph build --project` without re-reading the project profile. It is
a **named flag, not a positional**, so a call that passes only the six positional slots refuses
(exit 2, naming `--project`) instead of quietly filing its date under `project`. Do not Write the
clone or `.source/` into git.

Append to `$AUTODOC/log.md` (new entry at TOP), mirroring the wiki log format:

```markdown
## [YYYY-MM-DD] autodoc-init | <$REPO> @ <short-sha (8 chars)>
- Work units mapped: N (agents dispatched: N ≤ maxAgents) | Pages rendered: N (<pagesByType breakdown>)
- Community reports: N (incl. parents) | documents edges: N | join rates per type from `graph records`
- Flows: [[Flow A]], [[Flow B]]
- Store-primary: records → graph.db → rendered. Manifest at last_sha <short-sha>.
```

Write `$AUTODOC/hot.md` under the hard hot-cache contract (**whole file ≤400 words; the
Latest section ≤120 words and it MUST sit under a literal `## Latest` heading — the Step 6.7
run-complete gate matches that exact heading**, and restate that contract in a one-line HTML
comment at the top of the file so update runs see it): what the product is at a glance, the
load-bearing services and the central pipeline flow, where to start reading ([[overview]],
[[index]]; non-engineers start at [[Start Here]]), and the current `last_sha`. This is what
cross-project sessions read first.


## Step 6.7 — Run-completion gate (hard, final)

```bash
. "$(cat /tmp/autodoc-env.current)" || exit 1   # SUITE_ROOT, AUTODOC
node "$SUITE_ROOT/skills/autodoc-init/references/inventory/run-complete.js" "$AUTODOC"
```

Exits non-zero naming the first failure: empty/incomplete `.manifest.json.pages`, a manifest
key with no file on disk, a page count that disagrees with the tree, a `log.md` with no entry
for this run's date+sha (short sha = first 8 chars of the full sha — run-complete.js matches
exactly that prefix; full 40-char shas also pass), or a `hot.md` that is stale or over the
hot-cache contract (≤400 words file / ≤120 words Latest). **A non-zero exit means the run is
NOT complete — fix the named gap and re-run the gate. Never report the autodoc done past a red
run-complete.** It is the LAST thing this runbook executes; there is no commit step after it.

## Step 7 — Commit the autodoc: RETIRED

**There is no commit step, because the corpus is not inside a git repository.** The corpus sits
at the root the Config preamble resolves through `resolve_autodoc_root` (order in
`<suite_root>/docs/ARCHITECTURE.md#four-pillars-separated-by-authorship`). In the
standard layout that directory is outside the vault and outside any repository, so
`git -C "$AUTODOC" rev-parse --show-toplevel` fails with *"fatal: not a git repository"*. A step
that staged the corpus into its enclosing repo would get an empty repo path and do nothing, at the
very end of a build whose whole fan-out has already been paid for. `/autodoc-update` has no commit
step for the same reason.

**State the consequence rather than pretending a commit happened.** Version history for the corpus
is meant to come from the vault MIRROR, exactly as it does for `design/`, and that mirror is not
wired yet. Until it is, **a freshly built corpus is UNTRACKED**: every page is regenerable from the
store, but an accidental deletion of the tree has nothing to restore from. Say that in the build
report. Do not reach for a substitute — a `git init` in the corpus, or staging it into some nearby
repo, creates a second history that the mirror will then have to reconcile with.

---

## What Not to Do

- Do not commit `.source/` (the clone) into any git repo. Nothing on this path commits at all now
  (Step 7 is retired); the rule stands for whatever wires the vault mirror up later.
- Do not let ANY agent write page content — agents return records; the renderer is the only
  writer. `assert-no-agent-writes.js` enforces this; a file in the render target before the
  renderer runs is a hard failure.
- Do not hand-patch (or `--fix`) the rendered tree — the next render silently undoes it. Fix the
  records, re-write, re-render.
- Do not replace the live tree as a side effect — cutover (Step 6) is explicit and human-approved.
- Do not paste large code blocks into page bodies. Document intent + contract; link to `source_paths`.
- Do not run as a plain sequential crawl — the parallel workflow is the point. One agent per packed work unit.
- Do not invent entities. Only document what's in the code.
- This skill targets the configured autodoc folder (`$AUTODOC`), NOT `wiki/`. Never write code-docs into `wiki/`.

---

## Relationship to other skills

- `/autodoc-update` — incremental refresh from new commits. Run it instead of init once the autodoc exists; its Reconcile phase regenerates any tour whose step pages changed (re-ordered via `tour-order.js`).
- `/wiki-ingest` — the personal-wiki analogue; same conventions (frontmatter, `_index.md`, log, hot, wikilinks).
- `references/taxonomy.md` — shared contract; `/autodoc-update` reads it too. Defines all 12 entity types, including the `tour` type written by the Tours phase.
- `references/inventory/tour-order.js` — deterministic topo-sort used by the Tours phase (init) and Reconcile (update) to order tour steps dependencies-first.

---
name: exact-coding-baseline-export
description: |
  Mint a new YYYY-MM-DD-exact-coding-baseline snapshot under
  research/workflow-dev/export/. Detects the current best correctness-
  oriented workflow from research/workflow-dev/workflow-construction.md
  (or takes an explicit source-workflow argument) and transforms it from a
  lab workflow into a consumer-ready one on three axes: strips lab-only
  measurement content, re-enables human-in-the-loop checkpoints, and
  converts auto-loading config into an explicitly-invoked skill. Supports
  both promoted EXACT Coding lines: Opus/Hybrid and SOL/Predictive TDD.
  Exports Claude Code, pi, OpenCode, cursor-agent and, for SOL, Copilot. Trigger when the user says
  "exact-coding baseline export", "neue exact-coding baseline",
  "exact-coding-baseline-export", or asks to refresh the baseline snapshot.
---

# Skill: exact-coding-baseline-export

Mint a dated, consumer-ready snapshot of the current best TDD workflow into
`research/workflow-dev/export/<YYYY-MM-DD>-exact-coding-baseline/`.

This is a **true transformation skill** — it reads a source workflow
(immutable) and applies three transformations on top of it (see "The three
transformations" below), writing the result as a new snapshot. The skill is
self-contained: the HITL consumable template and the README template live
alongside this file under `templates/`, and the harness research lives in
`HARNESS-MECHANISMS.md`.

## Scope

- **Source repo**: writes snapshots only inside `research/workflow-dev/export/`
  and never edits source workflows under `experiments/workflows/`.
- **Distribution sync is explicit**: the SOL exporter may additionally create
  or update the canonical `main` and `harness/*` branches in `EXACT-Coding-Exercises` when
  `--sync-distribution <repo>` is passed. It commits locally and never pushes.
- **One artifact per line and date**: Opus writes
  `<DATE>-exact-coding-baseline/`; SOL writes
  `<DATE>-exact-coding-ptdd-v1/`. Each contains one subtree per exported
  harness.
- **Idempotent within a date and line**: refuses to overwrite an existing
  same-date snapshot unless the user explicitly says "overwrite" / "force".

## Two promoted EXACT Coding lines

The distribution has two parallel lines. Do not replace one with the other:

| Line | Default source | Native harness | Snapshot name |
|---|---|---|---|
| `opus` | the correctness-critical Opus/Hybrid recommendation in `workflow-construction.md` | Claude Code | `<DATE>-exact-coding-baseline` |
| `sol` | the universal PTDD default in `model-recommendation-matrix.md` | pi | `<DATE>-exact-coding-ptdd-v1` |

When the requested line is `sol`, run the checked-in exporter rather than
manually applying the Hybrid-specific steps below:

```bash
python3 .claude/skills/exact-coding-baseline-export/export-sol.py \
  --date "$DATE" \
  --sync-distribution /home/memrich/sync/work/konferenzen_und_talks/exact_coding/exact-coding-exercises
```

The repo name on GitHub is `EXACT-Coding-Exercises`, but the local checkout is
lowercase and lives under `sync/work/...` — see "The consumer" below, which is
the authoritative path. There is no `/home/memrich/EXACT-Coding-Exercises`.

The script auto-detects the promoted SOL source from
`model-recommendation-matrix.md`, reads its native `.pi/` tree, removes the lab
adaptations, restores consumer HITL behavior and explicit invocation, and emits
feature-equivalent `cc`, `pi`, `oc`, `cursor`, and `copilot` trees. With
`--sync-distribution` it also updates `main` and the four
`harness/*` branches, one harness tree per branch, and commits locally. Restrict the
set with repeated `--harness`; override source or target with `--source` and
`--target`. It validates that the stack profile exists in every tree, OpenCode
uses a consumer-shaped command config, and no lab vocabulary leaked.

The default SOL source is empirically validated on pi. The generated non-pi
trees are semantic distribution ports, not cross-harness validation claims;
preserve that caveat in their READMEs. Every tree installs two explicit entry
points side by side: `exact-coding` keeps inline Four-Rules refactoring, while
`exact-coding-isolated-refactor` delegates the same review after every Green.
They share one neutral Predictive-TDD core, stack profiles, test-list method, and
HITL policy under `skills/exact-coding-shared/`. The isolated profile comes from
the validated v1.1 treatment workflow; it never owns HITL. Neither profile adds
an APP objective or metric-driven end-refactor pass.

The remainder of this document describes the established `opus` transformation
path unless a section explicitly says otherwise.

## The three transformations

The export is not a copy. A lab workflow and a consumer workflow differ on
three independent axes, and every export applies all three:

| # | Axis | Lab | Export |
|---|---|---|---|
| 1 | **Lab content** | autonomy mandate, done-marker, phase-continuation fix | removed — `legacy`: `tdd-experiment-mode.md` not copied, replaced by `templates/tdd-execution-mode.md`; `v66`: drop `lab-only.md`. Both strip `LAB-ONLY` fences. |
| 2 | **Human checkpoints** | none — runs unattended | HITL checkpoints, default level `full-hitl` |
| 3 | **Invocation** | auto-loads on every session | explicitly invoked by the user |

Axis 3 is the one most easily forgotten, and it is harness-specific. A
consumer fixing a typo must not get Red-Green-Refactor discipline in
context; they should have to *ask* for the workflow. Mechanisms per
harness are documented in `HARNESS-MECHANISMS.md` — **read it before
exporting a harness you have not exported before.**

## Arguments

Four, all optional:

1. **Line**: `opus` or `sol`. Default: `opus` for backward compatibility.
2. **Date** in `YYYY-MM-DD` form. Default: today (`date +%F`).
3. **Source workflow name** (e.g. `exact-hybrid-v6-lab-split-cc` or
   `exact-sol-v1.3-stack-profile-pi`). Default: auto-detect from the selected
   line's recommendation (see "Source detection" below).
4. **Harness set**: any of `cc`, `pi`, `oc`, `cursor`, `copilot`, or `all`.
   Default: `cc` for Opus and `all` for SOL.

If the user passes "from v6.4 today" or similar, parse the source name and
use today's date. If only one argument looks like a date, that's the date;
if only one looks like a workflow name, that's the source.

With `all` (or an explicit multi-harness list), resolve one source workflow
per harness. For the hybrid-v6 line the naming is regular —
`v6.6-lab-split-{cc,pi,oc,cursor}` — so a single detected base name plus the
harness suffix resolves each. If a suffix variant is missing, report it and
export the harnesses that do exist rather than aborting the whole run.

## Source detection

For `sol`, source detection is implemented by `export-sol.py`: it reads the
backtick-quoted `exact-ptdd-*` workflow immediately preceding the universal
GPT-5.6 SOL/pi default declaration in
`research/workflow-dev/model-recommendation-matrix.md`. If that declaration or
its `.pi/` source tree is missing, abort; never fall back to a historical SOL name.

For `opus`, when no explicit source is given, find the current correctness-critical
default from `research/workflow-dev/workflow-construction.md`. The
recommendation lives in the "Current front" section and starts with the
prefix **"Default for correctness-critical work"**.

```bash
SRC_NAME=$(grep -E '\*\*Default for correctness-critical work' \
             research/workflow-dev/workflow-construction.md \
           | head -1 \
           | sed -E 's/.*`([^`]+)`.*/\1/')
```

The first backtick-quoted workflow name on that line is the recommendation.
Verify the directory exists:

```bash
# Workflows live in category subfolders; PATHS.json resolves the leaf name
# and also accepts former names (ALIASES.json).
SRC_DIR="experiments/workflows/$(jq -r --arg n "$SRC_NAME" \
    '.[$n] // $n' experiments/workflows/ALIASES.json \
  | xargs -I{} jq -r --arg n {} '.[$n] // $n' experiments/workflows/PATHS.json)"
[ -d "$SRC_DIR/.claude" ] || { echo "Source $SRC_DIR missing"; exit 1; }
```

If the grep fails (the recommendation line moved or got renamed), **ask the
user** which workflow to use. Do not silently fall back to a hardcoded name
— a stale fallback is the whole reason this skill was rewritten away from
clone-from-latest.

Print the resolved source to the user before proceeding, so a wrong
detection can be aborted.

## Target

```bash
TARGET="research/workflow-dev/export/$DATE-exact-coding-baseline"
[ -e "$TARGET" ] && { echo "Exists; pass 'overwrite' to replace"; exit 1; }
```

Each exported harness gets its own config subtree at the snapshot root, so
a consumer copies the one directory their harness reads:

```
<DATE>-exact-coding-baseline/
  README.md   # snapshot-level: which harnesses, how to install
  VERSION
  .claude/    # cc      skills/tdd/SKILL.md · commands/{test-list,red,green}.md
              #         agents/{refactor,end-refactor}.md · rules/
  .pi/        # pi      skills/tdd/SKILL.md · skills/{test-list,red,green}/
              #         agents/{refactor,end-refactor}.md · rules/
              #         extensions/subagent/{index,agents}.ts + README.md
  .opencode/  # oc      opencode.json (carries command.tdd)
              #         agents/{refactor,end-refactor}.md · skills/ · rules/
  .cursor/    # cursor  rules/{tdd,human-in-the-loop,tdd-with-ts-and-vitest}.mdc
              #         skills/{test-list,red,green}/
              #         agents/{refactor,end-refactor}.md
```

Note the file name: OpenCode reads **`opencode.json`**, not `.jsonc`.

Whichever refactor phases the source defines appear in every harness — the
per-cycle one always, the final `end-refactor` pass only on sources that have
it (v6.5/v6.6 line; the hybrid-v2 line deliberately does not) — and **all four
harnesses delegate them to isolated subagents**. cursor uses its native Task tool with agent files in
`.cursor/agents/`, the same shape as cc's `.claude/agents/`; see "Keep the
harness variants feature-equal" in `HARNESS-MECHANISMS.md`.

Create only the subtrees for the requested harnesses:

```bash
case "$H" in
  cc)     mkdir -p "$TARGET/.claude"/{skills/tdd,agents,commands,rules} ;;
  pi)     mkdir -p "$TARGET/.pi"/{skills/tdd,agents,rules,extensions/subagent} ;;
  oc)     mkdir -p "$TARGET/.opencode"/{agents,skills,rules} ;;
  cursor) mkdir -p "$TARGET/.cursor"/{rules,skills,agents} ;;
esac
```

> **pi: the subagent extension is mandatory, not optional.** pi has **no
> native subagent tool**. The `subagent` tool the refactor phase depends on
> comes entirely from the project-local extension at
> `.pi/extensions/subagent/` (`index.ts`, `agents.ts`, `README.md`). Ship
> all three files verbatim — without them the model has no way to delegate
> refactoring, and the isolated-context architecture silently degrades to
> inline refactoring.
>
> The extension is **trust-gated**: pi only loads project-local extensions
> after the project is trusted. The lab passes `--approve` because
> non-interactive `-p` mode has no prompt. A consumer running pi
> interactively gets a trust prompt on first use instead — the exported
> README must tell them to accept it, and that declining leaves the
> workflow without its refactor step.
>
> The refactor agent must also be invoked with `agentScope: "both"`, since
> it lives in the project-local `.pi/agents/` rather than user-level.

> **Single-harness back-compat.** Earlier snapshots (through 2026-05-25)
> put `.claude/` at the snapshot root with `README.md` and `VERSION`
> *inside* it, so that copying `.claude/` carried its own documentation.
> With multiple harnesses that no longer works — README/VERSION move to the
> snapshot root. A cc-only export may still additionally write
> `.claude/README.md` + `.claude/VERSION` for continuity with the old
> layout; say so in the report either way.

## Transformation steps

### Step 1: copy source files

First detect which layout the source uses — this changes what gets copied
and how much patching Step 5 needs:

```bash
if [ -f "$SRC_DIR/.claude/rules/lab-only.md" ]; then LAYOUT=v66; else LAYOUT=legacy; fi
echo "source layout: $LAYOUT"
```

**`legacy` is the expected route.** The current recommendation resolves to
`exact-hybrid-v2-testlist-fix-cc`, which has no `lab-only.md`, so the classic
template path applies. That is deliberate, not an accident of an old source:
RQ-1.19 measured what the split layout costs at runtime, and the export
convenience did not justify it. `v66` therefore only fires when someone names
a split workflow explicitly — see the note on that branch below before doing
so.

**Common to both layouts** — copy 1:1 from `$SRC_DIR/.claude/` to
`$TARGET/.claude/`:

- `rules/tdd-with-ts-and-vitest.md` (some older source workflows used
  `tdd_with_ts_and_vitest.md` — if present, rename to hyphen form in target)
- `agents/refactor.md`
- `agents/end-refactor.md` (present from hybrid-v5 onward; skip if absent)
- `commands/test-list.md`
- `commands/red.md`
- `commands/green.md`
- `rules/tdd.md`

**Explicitly not copied: `settings.json`.** Permissions are an environment
decision belonging to the consumer, not a property of the workflow. The lab
source needs a wide allowlist because runs are unattended — a consumer has a
human at the keyboard who should decide what the agent may do. Worse, a
shipped `settings.json` silently overwrites one the consumer already has. The
same reasoning removes the `permission` block from `opencode.json` (see
`HARNESS-MECHANISMS.md`). Do not reintroduce it, and do not substitute a
`settings.json.example` — the README explains the workflow, not the sandbox.

**Layout `v66`** (source has `rules/lab-only.md` — e.g. `exact-hybrid-v6-lab-split-cc`):

- Also copy `rules/subagent-prompts.md` — it holds the isolated-subagent
  prompt contracts and is workflow methodology, not lab infrastructure.
- Do **not** copy `rules/lab-only.md`. It carries the autonomy mandate, the
  done-marker contract, and the phase-continuation fix — a single deletion
  instead of the template reconstruction the `legacy` path needs.

  **That convenience has a measured price.** RQ-1.19 compared four workflows
  on `opus-5-no-thinking` and found the split raises the refactor rate per
  cycle at an unchanged cycle count: 0.41 for `hybrid-v2` against 0.52, 0.56 and
  0.69 for the three split variants on claim-office. `exact-hybrid-v2.8-pure-split-cc`
  isolates the cause — a pure partition of `hybrid-v2` carrying only 3.5 % more
  rule text still shows +27 % refactorings (Welch p = 0.009) and +20 %
  wall-clock (p = 0.034). It is the partition, not the text volume, and no
  quality metric improves in return. `exact-hybrid-v2.4-lab-split-cc` adds an
  always-refactor failure mode on top (4 of 10 runs, Fisher p = 0.010).

  So a `v66` export ships a workflow that costs roughly a fifth more
  wall-clock than the same instructions unsplit. Say so in the snapshot
  README when exporting one, and prefer `legacy` unless the consumer has
  asked for the split layout for their own reasons.
- After copying, strip any `LAB-ONLY` fenced regions from every copied
  `.md` (they appear in `rules/tdd.md`; other phase files may gain them
  later):

  ```bash
  find "$TARGET/.claude" -name '*.md' -print0 | while IFS= read -r -d '' f; do
    python3 -c "
import sys,re
p=sys.argv[1]; s=open(p).read()
s=re.sub(r'<!-- LAB-ONLY:START -->.*?<!-- LAB-ONLY:END -->\n?', '', s, flags=re.S)
open(p,'w').write(s)" "$f"
  done
  ```

  Strip each file exactly **once** — running the regex repeatedly over the
  same file can eat surrounding lines.

**Layout `legacy`** (source has `rules/tdd-experiment-mode.md` — hybrid-v5 and
earlier): do **not** copy `rules/tdd-experiment-mode.md`. It is replaced by
the consumable `tdd-execution-mode.md` from this skill's templates. Note
that this file also carries the subagent prompt contracts, which the
template must therefore reproduce.

### Step 2: write fresh files from skill templates

Copy verbatim from `.claude/skills/exact-coding-baseline-export/templates/`:

- `templates/human-in-the-loop.md` → `$TARGET/.claude/rules/human-in-the-loop.md`
- `templates/tdd-execution-mode.md` → `$TARGET/.claude/rules/tdd-execution-mode.md`

### Step 2a: two refactor profiles in every subtree

The SOL line ships the Refactor phase in two forms, and the user picks:

- `skills/exact-coding/SKILL.md` — **the default**, refactoring inline in the
  main context.
- `skills/exact-coding-isolated-refactor/SKILL.md` — the same workflow with the
  Four Rules review delegated to a subagent after every Green.

They differ in exactly four places: the frontmatter `name`, the title, the
refactor step in the Sequence, and a closing paragraph in "Method boundary"
stating that the subagent never manages checkpoints. Everything else is shared,
including one `skills/exact-coding-shared/human-in-the-loop.md` that both point
at — do not give either profile its own HITL file.

The delegation sentence is harness-specific and must name the real mechanism,
not describe it. `refactor_delegation()` in `export-sol.py` holds the exact
strings; pi names the `subagent` tool with `agentScope: both`, cc the Agent
tool with `subagent_type: refactor`, cursor/oc/copilot their `refactor` custom
agent.

Both profiles are backed by `agents/refactor.md` (`agents/refactor.agent.md` on
copilot), taken from the v1.1 sibling of the promoted source with pi's
`tools:` frontmatter line stripped. pi additionally needs
`extensions/subagent/`, copied from the same sibling, because it has no native
subagent mechanism. OpenCode exposes both profiles as commands in
`opencode.json` instead of skill directories.

`predictive-tdd/SKILL.md` is shared by both profiles, so it must **not** claim
the refactoring runs in the current context. It defers instead: "The invoking
EXACT Coding profile selects the Refactor execution context."

`validate()` enforces all of this: both profiles present, the shared HITL file
present, the agent present under its harness-specific name, pi's extension
present, the isolated profile still delegating and the default still inline.

### Step 2b: optional skills in every subtree

Every exported harness subtree also ships two **user-invoked** skills that are
not phases of the workflow:

- `skills/example-mapping/SKILL.md` — the requirements conversation before the
  loop. Taken from the consumer (`exact-coding-exercises`), where it was written.
- `skills/end-refactor/SKILL.md` — the whole-`src/` measured cleanup, as a
  **manual extra**. The frontmatter description must say it is never invoked
  automatically. One harness-neutral file serves every subtree.

These do not count as phases for validation 12. In particular, shipping
`skills/end-refactor/` does **not** port the end-refactor phase into a
hybrid-v2 export: no `agents/end-refactor.md`, and no orchestration file may
invoke it. Both READMEs must label it as a manual extra.

**The SOL path reads these from `templates/optional-skills/`**, not from a
source workflow — the SOL line never had either skill, so there is nothing to
transform. The templates were lifted from consumer `main`, whose copies are
newer than the 2026-08-12 snapshot: package-manager-neutral (`npm`/`npx`) and
without the `🏁` lab marker. `example-mapping` has two variants because cc has
the `AskUserQuestion` tool and slash commands while the other harnesses do not:
`example-mapping-cc.md` for cc, `example-mapping-neutral.md` for pi, oc, cursor
and copilot. `end-refactor.md` is byte-identical everywhere.

`export-sol.py` enforces this in `validate()`: both skills must exist in every
exported subtree, `agents/end-refactor.md` must not exist, and the
`end-refactor` body must keep its "optional, manually invoked" framing. The
2026-09-13/14/15 and ptdd-v1-2026-09-16 SOL snapshots predate the fix and ship
neither skill — `sync_distribution` then deleted the consumer's copies on
`sol/main`, because it clears all five config dirs before copying the snapshot.

### Step 2c: manual phase controls (`red`, `green`, `refactor`)

Every exported subtree also ships three **single-phase manual controls** so a
human can drive Red-Green-Refactor one phase per turn instead of invoking the
whole loop:

| Skill | Cycle step in `predictive-tdd/SKILL.md` | Stops before |
|---|---|---|
| `skills/red/SKILL.md` | 1. Activate one behavior + 2. Reach behavioral Red | any production change |
| `skills/green/SKILL.md` | 3. Reach Green minimally | refactoring |
| `skills/refactor/SKILL.md` | 4. Inspect and refactor | the next behavior |

**These carry no method content, by design.** Each one names the section of
`skills/predictive-tdd/SKILL.md` that governs it, the stack-profile directory,
and the shared HITL file — then stops. The method stays single-sourced: editing
the Predictive TDD skill changes what the phase controls do, and nothing needs
to be kept in sync. Do not copy prediction rules, Four Rules text, or the
domain-boundary contract into a phase file; the validator rejects a phase file
that no longer points at the method file.

The one thing they add that the full loop does not have: **the invocation itself
is the checkpoint.** A phase control must not run on into the next phase even at
an Autonomy Level that would not have stopped there (`green` in particular has
no HITL checkpoint at all). That sentence is load-bearing and validated.

`templates/phase-skills/` holds the three sources. `refactor-phase.md` is named
that way because `templates/refactor-agent.md` already owns `refactor.md`. Each
template carries `{config}`, `{hitl}` and — for refactor only —
`{execution_context}`, filled by `phase_control_skills()`; the refactor context
resolves the per-harness delegation from `refactor_delegation()`, so the phase
control works under both refactor profiles.

**These are not phases for validation 12 either.** `skills/refactor/` here is a
manual control that delegates when the isolated profile is named — not the
2026-07-27 cursor mistake of shipping an inline refactor phase in place of a
subagent. On OpenCode the three also get `opencode.json` command entries,
because a skill directory is not an invocation mechanism there.

**OpenCode phase skills come from the cc commands, not from the pi port.** The
pi port rewrote `✅ Correct` as plain `Correct`; the cc/oc prediction parser
accepts that form, but the OpenCode lab port (`exact-hybrid-v2-testlist-fix-oc`)
deliberately carries the cc wording so it matches the measured source. Build
`.opencode/skills/*` from the already HITL-patched `.claude/commands/*` plus
skill frontmatter. pi and cursor keep the pi-port wording.

### Step 3: render README from template

Take `templates/README.template.md`. Substitute placeholders:

- `{{DATE}}` → `$DATE` (both occurrences: title and "Version" line)
- `{{SOURCE_WORKFLOW}}` → `$SRC_NAME` (two occurrences in "Tested
  parameters" and "Original name and lineage")
- `{{MODEL}}` → the model the source workflow was validated against, e.g.
  `Claude Opus 4.8 (no-thinking variant)`. Read it from the RQ named on the
  recommendation line in `workflow-construction.md` — do not carry the
  previous snapshot's value forward.
- `{{CC_VERSION}}` → the Claude Code pin from `experiments/docker/Dockerfile`
  (CLAUDE.md's "Docker & version pins" records the same number).
- `{{MULTI_HARNESS_NOTE}}` → see below
- `{{MEASUREMENTS}}` → the body of `templates/measurements.md` without its
  leading HTML comment. **Re-check every number against the RQs named in that
  comment before each export** and update the model named in each subsection;
  the file is a lay-readable summary, not a generated table, so nothing refreshes
  it for you.

Model and harness version are placeholders precisely because they rot: they
were hardcoded until 2026-07-28 and shipped two snapshots claiming Opus 4.7
/ CC 2.1.107 long after both had moved.

Write to `$TARGET/.claude/README.md`.

**`{{MULTI_HARNESS_NOTE}}`.** The template is Claude-Code-specific by
design: it travels *inside* `.claude/`, so a consumer who copies that one
directory keeps its documentation. On a cc-only export, substitute the empty
string. On a multi-harness export, substitute:

```markdown
> **This is the Claude Code subtree.** The same workflow ships for pi
> (`.pi/`), OpenCode (`.opencode/`), and cursor-agent (`.cursor/`) in the
> snapshot this directory came from — see the snapshot-level `README.md`
> there for the harness comparison. The four are independent; you only need
> the one your harness reads. If you received `.claude/` on its own, nothing
> is missing — it is self-contained.
```

Name only the harnesses actually exported.

**On a multi-harness export, also write a snapshot-level `$TARGET/README.md`.**
There is no template for it — it is not a per-harness document. It must carry:
the harness→directory→invocation table, the phase table (all four harnesses
delegate refactor to an isolated subagent — only the tool name differs), the
end-refactor mechanism table, the opt-in gating table, the HITL summary, install
steps including the **pi trust prompt** warning, and the provenance /
three-transformations section.

> **Both READMEs claim the same version, so both must describe the same
> snapshot.** The 2026-07-27 export shipped a four-harness snapshot README
> next to a nested `.claude/README.md` that still said "ships the `.claude/`
> directory" and knew nothing of the other three. A Claude Code user copying
> `.claude/` got the stale one. Write the snapshot README *and* substitute
> `{{MULTI_HARNESS_NOTE}}`; validation 13 checks the pair.

Keep the nested README's stack claims concrete. It may say `pnpm` where the
snapshot README says "a package manager" — `pnpm test` is hardcoded across the
phase files, so the specific form is the accurate one.

> **Normalise `test:unit:basic` to `test` before shipping.** The phase files
> call `pnpm test:unit:basic` in three places (`red.md` ×2, `green.md` ×1). That
> script exists only inside the lab: `run-batch.sh` generates a `package.json`
> per run that aliases it to `vitest run`. A consumer project has `test`, not
> `test:unit:basic`, so the command fails there — and it contradicts the
> workflow's own `tdd-with-ts-and-vitest.md`, which says to run tests with
> `pnpm test`.
>
> ```bash
> grep -rl 'test:unit:basic' "$TARGET" | while read -r p; do
>   sed -i 's/test:unit:basic/test/g' "$p"
> done
> ```
>
> This shipped broken in the 2026-07-28 snapshot and sat unnoticed in the
> consumer until the next sync. Validation 14 checks it.
>
> **The package manager itself is a sync-time decision, not an export-time
> one.** The snapshot keeps `pnpm`, matching the lab source. A consumer on npm
> needs `pnpm` → `npm` and `pnpm exec` → `npx` applied while copying — check
> the target's lockfile (`package-lock.json` vs `pnpm-lock.yaml`) rather than
> assuming. Do not rewrite the snapshot for one consumer's package manager.

### Step 4: write VERSION

```bash
echo "$DATE" > "$TARGET/.claude/VERSION"
```

### Step 5: HITL inject into copied phase files

The copied source files reference experiment-mode wording or lack HITL
references. Apply the **HITL Patches** (next section) to each of the four
phase files plus `rules/tdd.md`.

**Layout-dependent patches.** On a `v66` source, several patches are
already satisfied by the fence-strip in Step 1 — applying them again is a
no-op, and their anchor strings will not be found:

| Patch | `legacy` source | `v66` source |
|---|---|---|
| A.3 — drop `EXPERIMENT MODE:` from Task prompts | apply | already absent; instead delete the bare `Run autonomously, return when done.` line from both Task prompt examples in `rules/tdd.md` |
| A.5 — replace `@…/tdd-experiment-mode.md` reference | apply | no such reference; skip |
| A.2, A.4, A.6, A.7 | apply | apply |
| B, C, D, E | apply | apply |

Everything else is identical across layouts. If an anchor string in the
HITL Patches cannot be found, report which patch and why rather than
force-fitting it.

> **The HITL Patches are written against the cc file layout.** Patches A–E
> name `rules/tdd.md`, `commands/*.md` and `agents/refactor.md`. pi, oc and
> cursor put the same content in different files — and crucially, **the
> lab-metric justification that Patches A.2 and B.1 remove lives somewhere
> else on every harness.** Applying only the literal patches leaves it in
> place. Where it actually sits:
>
> | Harness | Metric wording lives in |
> |---|---|
> | cc | `rules/tdd.md` (A.2), `commands/red.md` (B.1) |
> | pi | `skills/tdd/SKILL.md` (marker table + intro), `skills/red/SKILL.md` |
> | oc | the `command.tdd` **prompt string** inside `opencode.json`, `skills/red/SKILL.md` |
> | cursor | `rules/tdd.mdc`, `skills/red/SKILL.md` |
>
> The oc case is the easiest to miss: the orchestration is a JSON string,
> so a plain `grep` over `*.md` will not see it. Grep the whole subtree,
> not just markdown.
>
> **Two sites sit outside the orchestration files entirely** and were missed
> by every earlier export because the patches never look there:
>
> - **`agents/end-refactor.md`, all four harnesses** (where the source has
>   that phase) — the Remember list ends with "*that's the trail of evidence
>   the experiment reads*". Replace with "that's the audit trail for every
>   decision".
> - **`skills/red/SKILL.md` on pi, oc and cursor** — carries the same
>   `predictions_correct_rate` / "a metric the experiment measures"
>   justification that Patch B.1 removes from cc's `commands/red.md`. The
>   three are byte-identical copies, so patch them in one pass.
>
> Text-marker harnesses (pi, cursor) legitimately need a marker table —
> the markers are how their phases are recognised. Keep the table; replace
> only the lab-metric framing.
>
> **Replace the frame, not just the metric names.** Renaming
> `refactorings_applied` while leaving "the measurement pipeline parses…"
> around it still tells the consumer they are being measured. The whole
> sentence has to shift from *what the lab counts* to *what the marker
> makes visible to a human reader*:
>
> | Lab framing | Consumer framing |
> |---|---|
> | "the measurement pipeline **cannot count tool invocations** to track cycles" | "because there is no tool call per phase, the phase boundaries are marked by text markers instead" |
> | column header "What the Parser Counts" | "What It Makes Visible" |
> | "red-phase cycle (`cycle_count`)" | "a new cycle started" |
> | "`predictions_correct`, `predictions_total`" | "both predictions were made and scored" |
> | "are **parsed mechanically**" | "scoring each prediction separately is what makes the Guessing Game worth playing" |
> | "unattended batch experiments … so a measurement pipeline could parse an uninterrupted sequence of tool calls" | "unattended batch runs — it ran with no human gates between phases, start to finish" |
>
> The test: a reader who has never heard of the lab should find nothing in
> the exported files that only makes sense if they had. Validation 10
> greps for the left column; it cannot check that the right column reads
> naturally.
>
> **The table's own right-hand column is part of that framing.** In the lab
> it is headed *"What the Parser Counts"* and its cells name metrics
> (`cycle_count`, `predictions_total`). Rewriting only the prose around the
> table leaves the lab vocabulary sitting in the table — which is exactly
> how it survived into the 2026-07-27 export. Re-head the column *"What It
> Makes Visible"* and restate each cell as an observable fact about the
> phase ("a new cycle started", "both predictions were made and scored"),
> not a counter the consumer has no pipeline for.
>
> Two more sentences in the same files carry lab framing and are easy to
> skip because they read as generic emphasis:
>
> | Lab wording | Export wording |
> |---|---|
> | "the measurement pipeline **cannot count tool invocations**" | "because there is no tool call per phase, the phase boundaries are marked by text markers instead" |
> | prediction lines "are **parsed mechanically**" | "scoring each prediction separately is what makes the Guessing Game worth playing" |
>
> Do **not** touch the marker strings themselves (`## Red`, `Red Phase
> Complete:`, the two `Prediction` lines). Since the 2026-10 phase-chain
> migration this is no longer a measurement argument — only `Red Phase
> Complete` and the prediction lines still feed a live metric, and the lab
> reads discipline from the test framework's event stream instead
> (`MARKERS.md` → "What still carries a metric"). They stay for the consumer's
> sake: the headings are what makes a cycle visible to someone reading along,
> and the structure has to hold at an Autonomy Level that never stops for
> approval. The SOL export keeps them for the same reason and adds the HITL
> checkpoints on top rather than replacing them
> and validation 3 checks them.

> **Shell trap.** Several patch anchors contain backticks
> (`` `predictions_correct_rate` ``, `` `cycle_count` ``). In an
> *unquoted* heredoc (`<<PY`) the shell runs those as command
> substitution and silently corrupts the patch. Always use a **quoted**
> heredoc (`<<'PY'`) and pass paths via the environment, or use the Edit
> tool instead of shell scripting for these patches.

Use the `Edit` tool for surgical changes; do not rewrite whole files unless
the surgical change would be larger than the file.

### Step 6: Convert auto-load into explicit invocation

**Read `HARNESS-MECHANISMS.md` before doing this step.** It documents each
harness's auto-load and explicit-invocation mechanisms, researched against
the pinned CLI versions.

This is transformation axis 3. In the lab the workflow loads on every
session; in a consumer project it must be requested. What moves where:

**Claude Code** — `rules/tdd.md` becomes `skills/tdd/SKILL.md`, gaining
frontmatter. Phase commands and agents stay where they are (they are
invoked by the workflow, not the user).

**Move the workflow's own rule files into the skill directory too.** Claude
Code auto-loads everything under `rules/`, so a file left there is in context
on every session regardless of the frontmatter gate on `SKILL.md` — the
workflow ends up half-gated. Files that belong to the workflow move next to
it and are referenced from their new location:

```bash
for f in human-in-the-loop tdd-execution-mode subagent-prompts; do
  [ -f "$TARGET/.claude/rules/$f.md" ] || continue
  mv "$TARGET/.claude/rules/$f.md" "$TARGET/.claude/skills/tdd/$f.md"
done
# rewrite every reference, in all files, to the new path
grep -rl '@\.claude/rules/' "$TARGET/.claude" | while read -r p; do
  sed -i -E 's|@\.claude/rules/(human-in-the-loop|tdd-execution-mode|subagent-prompts)\.md|@.claude/skills/tdd/\1.md|g' "$p"
done
```

`rules/tdd-with-ts-and-vitest.md` **stays in `rules/`** — see the next
paragraph. After the move, `rules/` holds exactly that one file; if it holds
anything else, the mover missed something.

```yaml
---
name: tdd
description: Strict Test-Driven Development workflow (Red-Green-Refactor) with configurable human-in-the-loop checkpoints. Invoke when the user explicitly asks to use TDD, do a TDD kata, or follow the Red-Green-Refactor discipline. Do NOT invoke for general coding tasks where the user has not asked for TDD.
---
```

The negative clause is load-bearing. A description that only says what the
skill does will fire on ordinary coding tasks.

`rules/tdd-with-ts-and-vitest.md` **stays a rule** — TS/Vitest conventions
are useful whenever someone edits a `*.spec.ts`, whether or not a TDD
session was requested. Gate the workflow, not the ambient conventions.

**pi** — `AGENTS.md` orchestration content becomes `.pi/skills/tdd/SKILL.md`,
registered as `/skill:tdd`. Same frontmatter contract (Agent Skills
standard: `name` ≤64 chars lowercase/digits/hyphens, `description` ≤1024).
Add `disable-model-invocation: true` if the consumer wants the skill hidden
from the system prompt entirely, loadable only by typing `/skill:tdd`.
Phase skills (`red`, `green`, `test-list`) and the subagent extension carry
over unchanged.

**OpenCode** — remove `AGENTS.md` from the `instructions` array in
`opencode.json` (that array is what makes it automatic) and add a
`command.tdd` entry whose **`template`** carries the orchestration (`template`
is the schema-required field — `prompt` is not valid and silently drops the
instructions). Phase agents
in `.opencode/agents/*.md` keep `mode: subagent` and are launched from the
command prompt.

**cursor** — flip `alwaysApply: true` → `false` on `tdd.mdc` and
`human-in-the-loop.mdc`, and make sure each has a specific `description`
(that combination is cursor's "Agent Requested" mode). Leave
`tdd-with-ts-and-vitest.mdc` on its `globs` form — same reasoning as CC.

After this step, verify the workflow is genuinely gated: a session that
never mentions TDD must not pull the workflow into context.

## HITL Patches

Each patch is described as: file → location → replacement / addition. The
exact target strings are taken from `exact-hybrid-v4-cleaned-cc`; for other
source workflows the strings might differ — in that case, use the nearest
structural anchor (e.g. "after the last numbered Step") and report any
patch that could not be applied verbatim.

### Patch A — `rules/tdd.md`

1. **Header rename** (top of file):

   - From: `# Test-Driven Development (TDD) Rules — Hybrid (hybrid)` (or
     whatever header the source uses)
   - To: `# TDD Rules — Hybrid (hybrid, exact-coding baseline)`

2. **Drop experiment-pipeline justification** in the "🚨 CRITICAL" intro
   paragraph. The source typically has a sentence like *"The experiment's
   measurement pipeline parses these tool calls to compute `cycle_count`,
   `predictions_correct_rate`, and `refactorings_applied`."* — remove the
   pipeline/metric reference and replace with the generic architectural
   justification:

   > If you write test code, implementation code, or refactorings directly
   > in the main context instead of delegating, the workflow loses the
   > architectural separation that makes the hybrid work.

3. **Drop the `EXPERIMENT MODE: Run autonomously, return when done.` line**
   from the Step 4 Refactor `Task({...})` prompt example.

4. **Append to the Overview section** (after the architectural description,
   before "TDD Workflow"):

   > This baseline supports **configurable human-in-the-loop checkpoints**
   > between phases. See `@.claude/rules/human-in-the-loop.md` for the
   > Autonomy Level setting and stop behavior.

5. **Replace reference** `@.claude/rules/tdd-experiment-mode.md`
   → `@.claude/rules/tdd-execution-mode.md`.

6. **Insert section** `## Human-in-the-Loop` after "Core TDD Principles":

   ```markdown
   ## Human-in-the-Loop

   Between phases, the workflow consults `@.claude/rules/human-in-the-loop.md`
   to decide whether to pause for human approval. The default Autonomy Level
   is `full-hitl`, which stops after Test-List, Red, and Refactor (not Green)
   and on prediction failures. Switch levels by editing the setting at the
   top of the HITL file — see that file for the full table.

   For unattended batch runs, set the level to `autonomous` to disable all
   stops.
   ```

7. **Append to "Remember" list**:

   > Consult `@.claude/rules/human-in-the-loop.md` at every phase boundary

### Patch B — `commands/red.md`

1. **Step 7 "Why this format matters"**: the source paragraph refers to
   `predictions_correct_rate` and "the experiment measures". Replace with:

   ```markdown
   **Why this format matters:** The block is mechanically parsed by tooling to
   verify the Guessing Game discipline. The parser expects two lines matching
   `(- |✅ |❌ )(Correct|Incorrect)` per cycle — one for the compilation
   prediction, one for the runtime prediction. Collapsing them into a single
   line, summarizing them as "both correct", or skipping the block entirely
   loses the signal. Format consistency here matters even outside batch runs:
   it makes the prediction quality visible to you and any future reader.
   ```

   The verbatim `🔴 Red Phase Complete:` block that follows **MUST stay
   exactly as in source** — it is one of the four MARKERS.

2. **Step 3 / Step 6 STOP lines**: source has *"❌ Prediction wrong → STOP
   and explain discrepancy"*. Replace `STOP and explain discrepancy` with
   `follow the Prediction Failure Protocol below` (the Prediction Failure
   Protocol section is updated in step B.4).

3. **Append Step 8** after the Step 7 block:

   ```markdown
   ### Step 8: Apply HITL Checkpoint

   Consult `@.claude/rules/human-in-the-loop.md`. If the current Autonomy Level
   includes a stop after Red phase, present the checkpoint template from that
   file and wait for explicit user approval before proceeding to Green. If the
   level does not stop after Red, proceed directly to Green phase.
   ```

4. **Prediction Failure Protocol section**: after the existing
   `❌ Prediction Failed:` code block, append:

   ```markdown
   Then apply the **Prediction Failure Recovery** procedure in
   `@.claude/rules/human-in-the-loop.md`. In every Autonomy Level except
   `autonomous`, this is a hard stop — the human decides whether you continue
   or investigate first.
   ```

5. **Completion section** at the end: replace whatever closing prose source
   has with:

   ```markdown
   After Step 8 (HITL checkpoint), proceed to Green phase if approved or if
   the Autonomy Level does not require a stop:

   ```
   🔴 Red Phase Complete. Proceeding to Green phase.
   ```
   ```

### Patch C — `commands/green.md`

Append at the end of the "Completion" section:

```markdown
> **HITL note:** Green has no human checkpoint by default — the default
> Autonomy Level (`full-hitl`) skips it because Green is the most mechanical
> phase and stops here mostly produce "yes, continue" with no review value.
> To enable a Green checkpoint, see `@.claude/rules/human-in-the-loop.md`.
```

### Patch D — `commands/test-list.md`

Append after Step 5 ("Provide Summary"):

```markdown
### Step 6: Apply HITL Checkpoint

Consult `@.claude/rules/human-in-the-loop.md`. If the current Autonomy Level
includes a stop after Test-List (the default `full-hitl` does), present the
checkpoint template from that file and wait for explicit user approval
before proceeding to the first Red phase. If the level does not stop after
Test-List, proceed directly to Red.
```

Adjust the trailing "Completion" section's prose to acknowledge Step 6.

### Patch E — `agents/refactor.md`

> **This patch applies verbatim on all four harnesses, cursor included.**
> The wording hands the checkpoint to "the requester" because the refactor
> phase runs as an isolated subagent that cannot pause for a human — true on
> cc, pi, oc **and** cursor, which delegates to `.cursor/agents/` via its
> native Task tool. Only the referenced HITL path differs per harness
> (`.claude/rules/…md`, `.pi/rules/…md`, `.opencode/rules/…md`,
> `.cursor/rules/…mdc`).
>
> Earlier versions of this skill carried a cursor-specific inverse of this
> patch, on the false premise that cursor had no subagent mechanism and
> refactored inline. That exception is gone — do not reintroduce it.

Append after Step 7 ("Report Completion"):

```markdown
### Step 8: Apply HITL Checkpoint

After returning the report to the requester, the requesting context will
consult `@.claude/rules/human-in-the-loop.md`. If the current Autonomy Level
includes a stop after Refactor (the default `full-hitl` does), the requester
will present the checkpoint template and wait for explicit user approval
before proceeding to the next Red phase. This step is the requester's
responsibility, not yours — your job ends with the Step 7 report.
```

## Validation

Run all checks after Step 5. Any failure means the snapshot is broken —
report immediately, do not claim success.

1. **File set**: the expected set depends on the source layout.

   ```bash
   find "$TARGET" -type f | sort
   ```

   Expected for a `legacy` source (10 files):
   ```
   .claude/README.md
   .claude/VERSION
   .claude/agents/refactor.md
   .claude/commands/{green,red,test-list}.md
   .claude/rules/{human-in-the-loop,tdd,tdd-execution-mode,tdd-with-ts-and-vitest}.md
   ```

   Expected for a `v66` source (12 files) — adds the end-refactor agent and
   the subagent prompt contracts:
   ```
   .claude/README.md
   .claude/VERSION
   .claude/agents/{end-refactor,refactor}.md
   .claude/commands/{green,red,test-list}.md
   .claude/rules/tdd-with-ts-and-vitest.md
   .claude/skills/tdd/{SKILL,human-in-the-loop,subagent-prompts,tdd-execution-mode}.md
   ```

   Both lists are written **after** Step 6, which moves `tdd.md` into
   `skills/tdd/SKILL.md` and the workflow's own rule files in beside it. Only
   `tdd-with-ts-and-vitest.md` stays in `rules/`, because it is meant to load
   ambiently. A source whose `agents/` lacks `end-refactor.md` (the hybrid-v2 line)
   yields the same set minus that file — see validation 12.

   In **neither** case may `rules/lab-only.md` or
   `rules/tdd-experiment-mode.md` appear.

   **No permission config in any harness subtree** — permissions are the
   consumer's decision, and a shipped file overwrites theirs silently:

   ```bash
   find "$TARGET" \( -name 'settings.json' -o -name 'settings.local.json' \
     -o -name 'settings.json.example' \) -print | grep . \
     && echo "FAIL: permission config shipped (consumer decides)" || \
     echo "  OK no permission config in target"
   ```

   The `opencode.json` counterpart is asserted in validation 11.

2. **Source workflow files copied** (size sanity — none of the source
   files dropped below 500 bytes during patching, which would indicate a
   destroyed file):

   ```bash
   find "$TARGET/.claude" -type f -name '*.md' -size -500c
   ```
   Must print nothing.

3. **MARKERS intact** (cross-reference
   `experiments/workflows/MARKERS.md`):

   ```bash
   grep -q 'Skill({ skill: "test-list"' "$TARGET/.claude/rules/tdd.md"
   grep -q '🔴 Red Phase Complete'        "$TARGET/.claude/commands/red.md"
   grep -q 'MUST attempt at least one refactoring' \
                                          "$TARGET/.claude/agents/refactor.md"
   grep -q 'Absolute Priority Premise\|APP.*Mass' \
                                          "$TARGET/.claude/agents/refactor.md"
   ```

   Plus the verbatim two-line prediction block in `red.md`:
   ```bash
   grep -cE '(Compilation|Runtime) Prediction.*✅ Correct' \
        "$TARGET/.claude/commands/red.md"
   ```
   Must print `2`.

4. **No lab wording leaked into the snapshot**:
   ```bash
   grep -r 'tdd-experiment-mode\|EXPERIMENT MODE\|predictions_correct_rate\|refactorings_applied\b\|LAB-ONLY\|lab-only\.md\|experiment-done' \
        "$TARGET/.claude" && echo "FAIL: lab wording leaked"
   ```
   Must print no matches. `LAB-ONLY` / `lab-only.md` / `experiment-done`
   catch an incomplete fence-strip on a `v66` source — the most likely
   failure mode of that layout, since a surviving fence marker means the
   block it delimited also survived.

   Additionally, no bare autonomy instruction may remain in the Task
   prompt examples:
   ```bash
   grep -n 'Run autonomously' "$TARGET/.claude/rules/tdd.md" \
     && echo "FAIL: autonomy line survived (see Patch A.3, v66 row)"
   ```
   Must print no matches.

5. **HITL referenced from every phase file**:
   ```bash
   for f in test-list.md red.md green.md; do
     grep -q 'human-in-the-loop.md' "$TARGET/.claude/commands/$f" \
       || echo "FAIL: HITL missing from $f"
   done
   grep -q 'human-in-the-loop.md' "$TARGET/.claude/agents/refactor.md"
   ```

6. **Autonomy Level switch present**:
   ```bash
   grep -q 'Autonomy Level' "$TARGET/.claude/rules/human-in-the-loop.md"
   grep -q 'full-hitl'      "$TARGET/.claude/rules/human-in-the-loop.md"
   ```

7. **VERSION + README version line match the requested date**:
   ```bash
   grep -qx "$DATE" "$TARGET/.claude/VERSION"
   grep -q  "Version \*\*$DATE\*\*\|Version: \*\*$DATE\*\*" \
        "$TARGET/.claude/README.md"
   ```

8. **README placeholders fully substituted**:
   ```bash
   grep -F '{{' "$TARGET/.claude/README.md" \
     && echo "FAIL: unsubstituted placeholders"
   ```
   Must print no matches.

9. **Invocation is gated** (transformation axis 3). The workflow must not
   auto-load. Per exported harness:

   ```bash
   # cc — workflow lives in skills/, not rules/; frontmatter present
   [ -f "$TARGET/.claude/skills/tdd/SKILL.md" ] || echo "FAIL cc: no skills/tdd/SKILL.md"
   [ -f "$TARGET/.claude/rules/tdd.md" ] && echo "FAIL cc: tdd.md still auto-loads from rules/"
   grep -q '^name: tdd'        "$TARGET/.claude/skills/tdd/SKILL.md" || echo "FAIL cc: no name in frontmatter"
   grep -q '^description: .*TDD' "$TARGET/.claude/skills/tdd/SKILL.md" || echo "FAIL cc: no description gate"
   grep -qi 'do not invoke'    "$TARGET/.claude/skills/tdd/SKILL.md" || echo "WARN cc: description lacks a negative clause"

   # cc — workflow rule files sit next to the skill, not in auto-loaded rules/
   for f in human-in-the-loop tdd-execution-mode subagent-prompts; do
     [ -f "$TARGET/.claude/rules/$f.md" ] \
       && echo "FAIL cc: $f.md still auto-loads from rules/"
   done
   # rules/ must hold nothing but the ambient stack conventions
   ls "$TARGET/.claude/rules" | grep -v '^tdd-with-ts-and-vitest\.md$' \
     && echo "FAIL cc: unexpected file left in rules/"
   # no reference may still point at the old location
   grep -rn '@\.claude/rules/\(human-in-the-loop\|tdd-execution-mode\|subagent-prompts\)' \
        "$TARGET/.claude" && echo "FAIL cc: stale @rules/ reference"

   # pi — skill exists; AGENTS.md must not carry the orchestration
   [ -f "$TARGET/.pi/skills/tdd/SKILL.md" ] || echo "FAIL pi: no skills/tdd/SKILL.md"

   # pi — subagent extension shipped (no native subagent tool on pi)
   for f in index.ts agents.ts README.md; do
     [ -f "$TARGET/.pi/extensions/subagent/$f" ] || echo "FAIL pi: extension missing $f"
   done

   # oc — AGENTS.md no longer in the instructions array
   grep -q '"instructions".*AGENTS.md' "$TARGET/.opencode/opencode.json" 2>/dev/null \
     && echo "FAIL oc: AGENTS.md still auto-loaded via instructions"

   # cursor — workflow rules gated, conventions may stay glob-attached
   for f in tdd human-in-the-loop; do
     grep -q 'alwaysApply: true' "$TARGET/.cursor/rules/$f.mdc" 2>/dev/null \
       && echo "FAIL cursor: $f.mdc still alwaysApply: true"
   done
   ```

   Run only the blocks for harnesses actually exported. Any `FAIL` means
   the snapshot still behaves like a lab workflow — it would load TDD
   discipline into every unrelated session in the consumer's project.

10. **Lab wording, whole subtree** (not just `*.md`). The oc orchestration
    is a JSON string, so a markdown-only grep misses it:

    ```bash
    grep -rn 'predictions_correct_rate\|refactorings_applied\b\|predictions_correct\b\|predictions_total\|cycle_count\|the experiment\|invalidating the data point\|Run autonomously\|measurement pipeline\|Parser Counts\|parsed mechanically' \
         "$TARGET" && echo "FAIL: lab wording leaked"
    ```
    Must print no matches. On a multi-harness export this check has caught
    leaks in *every* non-cc subtree — Patches A.2/B.1 only cover cc.

    > **The metric-name half of this list is the half that gets missed.**
    > The 2026-07-27 export shipped with `cycle_count`, `predictions_total`,
    > "What the Parser Counts", "measurement pipeline" and "parsed
    > mechanically" live in `.pi/skills/tdd/SKILL.md` and
    > `.cursor/rules/tdd.mdc` — and passed validation, because the token list
    > at the time only had `predictions_correct_rate` and
    > `refactorings_applied`. Those two happen to be the tokens cc uses; the
    > text-marker harnesses name *different* metrics in their marker tables.
    > Keep both halves of the alternation, and when a new metric name enters
    > a workflow, add it here.

11. **`opencode.json` is consumer-shaped and schema-valid**:

    ```bash
    python3 -c "
import json;c=json.load(open('$TARGET/.opencode/opencode.json'))
assert 'provider' not in c, 'FAIL: Requesty/Portkey provider block leaked'
assert not c.get('instructions'), 'FAIL: AGENTS.md still auto-loaded'
assert 'permission' not in c, 'FAIL: permission config shipped (consumer decides)'
for n,cmd in c.get('command',{}).items():
    assert 'template' in cmd, f'FAIL: command.{n} has no template (schema-required)'
    assert 'prompt' not in cmd, f'FAIL: command.{n} uses prompt; the field is template'
print('  OK opencode.json is consumer-shaped')"
    ```

    The `template` check is not pedantry: `prompt` parses as valid JSON, so a
    wrong key produces a command that loads with an empty instruction body and
    fails only at use time. The 2026-07-28 export shipped it that way.

12. **Feature parity across exported harnesses**. The variants are meant
    to be identical as far as each harness allows — a phase present in one
    subtree and missing from another is a port that lagged, not a design
    choice.

    **Parity is measured against the source workflow, not against a fixed
    phase list.** Which phases exist is a property of the source: the hybrid-v6
    line carries both a per-cycle refactor and a final `end-refactor` pass;
    the hybrid-v2 line has only the per-cycle one, and that absence is
    constitutive — it is why the workflow is cheap (RQ-workflow-reduction-opus5
    F-1.3: the end phase costs 16–19 % of tokens without moving mean
    decomposition). Do not require `end-refactor` from a source that never
    had it, and do not port it in to satisfy this check — that would ship a
    workflow other than the one the recommendation was measured on.

    Derive the expected phase set from the source, then require every
    exported harness to match it:

    ```bash
    # phases the source actually defines
    PHASES=$(cd "$SRC_DIR/.claude/agents" && ls *.md 2>/dev/null | sed 's/\.md$//')
    echo "source phases: $(echo $PHASES | tr '\n' ' ')"

    for h in claude pi opencode cursor; do
      [ -d "$TARGET/.$h" ] || continue
      for p in $PHASES; do
        printf '  %-9s %-14s ' "$h" "$p"
        [ -f "$TARGET/.$h/agents/$p.md" ] && echo "OK" || echo "FAIL: $p missing"
      done
    done
    ```

    A `FAIL` means the source variant needs the phase ported (see
    "Keep the harness variants feature-equal" in `HARNESS-MECHANISMS.md`)
    — fix it in `experiments/workflows/`, not in the snapshot, then
    re-export. Do not ship an uneven snapshot with a caveat.

    An agent file alone is not enough: verify each phase is actually
    invoked from the harness's orchestration file. Check that one file
    directly — piping `grep -rl` into `grep -q` gives false FAILs, because
    the second grep exits on the first non-matching line:

    ```bash
    for h in claude pi opencode cursor; do
      [ -d "$TARGET/.$h" ] || continue
      case $h in
        claude)   o="$TARGET/.claude/skills/tdd/SKILL.md" ;;
        pi)       o="$TARGET/.pi/skills/tdd/SKILL.md" ;;
        opencode) o="$TARGET/.opencode/opencode.json" ;;
        cursor)   o="$TARGET/.cursor/rules/tdd.mdc" ;;
      esac
      for p in $PHASES; do
        printf '  %-9s %-14s ' "$h" "$p"
        grep -q "$p" "$o" && echo "OK invoked" || echo "FAIL: defined but never called"
      done
    done
    ```

    **Both refactor phases must be *delegated*, not inline — on every
    harness.** "Invoked" is not enough: a workflow can name the phase and
    still execute it in the main context, which silently drops the
    isolated-context architecture. Each harness keeps its refactor phases as
    agent files, never as phase skills:

    ```bash
    for h in claude pi opencode cursor; do
      [ -d "$TARGET/.$h" ] || continue
      printf '  %-9s ' "$h"
      # agent files present
      [ -f "$TARGET/.$h/agents/refactor.md" ] || { echo "FAIL: refactor not an agent"; continue; }
      # and NOT also sitting in skills/ (that shape means inline execution)
      if [ -e "$TARGET/.$h/skills/refactor" ]; then
        echo "FAIL: refactor also present as a skill — inline regression"
      else
        echo "OK delegated"
      fi
    done

    # no orchestration file may instruct inline refactoring
    grep -rniE 'refactor (runs|is applied) inline|apply it inline|no subagent' "$TARGET" \
      && echo "FAIL: inline-refactor instruction in snapshot"
    ```

    cursor is the one to watch here: the 2026-07-27 snapshot shipped it with
    `skills/refactor/` and `skills/end-refactor/` on the false premise that
    the harness had no subagent mechanism. It does — `.cursor/agents/*.md`
    plus the native Task tool, same shape as cc.

13. **README pair agrees** (multi-harness exports only). Both READMEs carry
    the same version, so neither may describe a narrower snapshot than was
    actually shipped:

    ```bash
    # snapshot-level README exists and names every exported harness
    [ -f "$TARGET/README.md" ] || echo "FAIL: no snapshot-level README.md"
    for h in claude pi opencode cursor; do
      [ -d "$TARGET/.$h" ] || continue
      grep -q "\.$h/" "$TARGET/README.md" \
        || echo "FAIL: snapshot README omits .$h/"
    done

    # nested cc README acknowledges it is one subtree of several
    grep -q 'Claude Code subtree' "$TARGET/.claude/README.md" \
      || echo "FAIL: .claude/README.md still reads as a single-harness export"
    ```

    Both READMEs must also agree on the date:
    ```bash
    grep -qF "$DATE" "$TARGET/README.md" && grep -qF "$DATE" "$TARGET/.claude/README.md" \
      || echo "FAIL: README pair disagrees on version"
    ```

14. **Every command the snapshot names must exist outside the lab.** The lab
    generates a `package.json` per run with extra script aliases; a consumer
    project has only what its own `package.json` defines. Any script name the
    phase files call has to be one a normal project actually has:

    ```bash
    grep -rn 'test:unit:basic\|test:coverage' "$TARGET" \
      && echo "FAIL: lab-only npm script referenced"
    ```
    Must print no matches. `test` and `test:watch` are the only script names
    safe to assume.

## Consumer sync

The Opus path never writes outside the lab repo. The SOL path can synchronize
the snapshot when explicitly passed `--sync-distribution`; without that flag it
also remains snapshot-only. This section records the consumer target.

### The consumer

`exact-coding-exercises` — the one repo that actually consumes the
baseline.

| | |
|---|---|
| Local | `/home/memrich/sync/work/konferenzen_und_talks/exact_coding/exact-coding-exercises` |
| Remote | `git@github.com:marcoemrich/EXACT-Coding-Exercises.git` |
| Harnesses in use | `.claude/`, `.cursor/`, `.opencode/` — already multi-harness |

Record the remote for identification, but treat the **local path as the
write target**: syncing is a filesystem copy, and this skill neither
commits nor pushes. Verify the path with `[ -d ]` before reporting it —
a moved directory should fail loudly rather than be silently wrong.

That repo is already a **reference implementation of the invocation
transformation**: its `.claude/skills/tdd/SKILL.md` carries exactly the
frontmatter gate Step 6 produces, negative clause and all. When in doubt
about what an exported cc tree should look like, read that file.

Two things there still differ from a fresh export, and a sync should
reconcile rather than blindly overwrite:

- **Layout.** As of the 2026-07-28 snapshot it still carries the workflow's
  rule files under `.claude/rules/` — the shape exports produced before Step 6
  started nesting them inside `skills/tdd/`. A sync therefore *replaces* that
  layout rather than merging into it: delete the stale
  `rules/{human-in-the-loop,tdd-execution-mode,subagent-prompts}.md` when
  copying the new snapshot in, or CC auto-loads the old copies and the
  workflow is gated and always-on at the same time. `rules/tdd-with-ts-and-vitest.md`
  is the one file that legitimately stays in both layouts.
- **cursor rules.** `tdd.mdc` and `human-in-the-loop.mdc` are still
  `alwaysApply: true`, i.e. not yet gated. `tdd-with-ts-and-vitest.mdc` is
  already correct on its `globs` form.

`exact-coding-exercises` is the **only** sync target. Distribution is
deliberately strict: one consumer repo, one baseline. If another project
wants the workflow, it copies from that repo or from a snapshot here — do
not add a second distribution path without an explicit decision to.

## Report to the user

After successful validation:

1. Echo the resolved source workflow(s), the harnesses exported, and the
   target snapshot path.
2. Print the file tree.
3. State which of the three transformations were applied per harness —
   in particular whether invocation gating (Step 6) succeeded, since a
   snapshot that still auto-loads is the failure mode a consumer notices
   last and dislikes most.
4. Note that the skill did NOT commit/push — the user does git operations
   afterwards.
5. On a multi-harness export, confirm the subtrees are **feature-equal**
   (validation 12), and name any difference that is genuinely forced by a
   harness limitation — e.g. pi needs a bundled extension and a trust prompt
   for the `subagent` tool the other three get natively. A difference that is
   *not* harness-forced is a bug to fix in the source workflow, not a caveat
   to ship.

   Be sceptical of any claim that a harness "cannot" do something. The
   2026-07-27 export shipped cursor with inline refactoring on exactly such a
   claim, and it was false — cursor had a Task tool the whole time. Verify
   against the harness's own docs and, where feasible, a probe run before
   accepting a limitation as real.
6. Point at the consumer (`EXACT-Coding-Exercises`, path above). State whether
   PTDD distribution sync ran; if it did, list the local `main` / `harness/*` commits and say
   explicitly that no push occurred. For Opus or snapshot-only SOL exports,
   state that the snapshot was not copied.

## What this skill explicitly does NOT do

- Does **not** push, commit, or `git add` anything.
- Does **not** copy an Opus snapshot into consumer repos. For SOL only,
  `export-sol.py --sync-distribution <repo>` is the explicit opt-in that creates
  or updates the parallel distribution branches; without the flag it writes
  only the snapshot.
- Does **not** edit source workflows under `experiments/workflows/`.
- Does **not** edit `workflow-construction.md` or any RQ findings — those
  belong in their own RQ-driven flows.
- Does **not** prompt for substantive content changes. If the source
  workflow's content has drifted in a way that the surgical patches in
  this skill no longer apply cleanly, the patches above need to be
  updated in this SKILL.md first.

## Related files

- `templates/human-in-the-loop.md` — canonical HITL consumable, copied
  verbatim into every snapshot.
- `templates/tdd-execution-mode.md` — **cc-only, by design.** Do not port it
  to the other subtrees, and do not read its absence there as a gap. Its two
  halves are already covered elsewhere on every harness: the phase sequence
  sits in that harness's orchestration file (`skills/tdd/SKILL.md`,
  `command.tdd` in `opencode.json`, `rules/tdd.mdc`), and the subagent
  contracts in its own `rules/subagent-prompts.md` — cursor included, since it
  delegates refactor to `.cursor/agents/` and its subagents need the same
  prompt contract as everyone else's.
  Replaces source's
  `tdd-experiment-mode.md` (`legacy` layout). On a `v66` source there is
  no such file to replace: the lab half is dropped with `lab-only.md` and
  the methodology half already lives in the source's
  `rules/subagent-prompts.md`, which is copied through. The template is
  still written in both layouts — it is what tells the consumer the
  workflow runs in a normal, interruptible mode.
- `templates/README.template.md` — Opus/Hybrid README with `{{DATE}}` and
  `{{SOURCE_WORKFLOW}}` placeholders.
- `templates/SOL-DISTRIBUTION-README-SECTION.template.md` — shared branch
  documentation used by `export-sol.py` when synchronizing all SOL harnesses.
- `export-sol.py` — executable SOL export, validation, and optional local
  distribution-branch synchronization.
- `HUMAN-IN-THE-LOOP.md` (in this skill's directory) — methodology
  reference describing the HITL design rationale and re-enablement steps
  (transformation axis 2). Useful for understanding **why** the templates
  look the way they do, but not consumed by the export flow itself.
- `HARNESS-MECHANISMS.md` (in this skill's directory) — auto-load vs.
  explicit-invocation mechanism per harness (transformation axis 3),
  researched against the pinned CLI versions. **Read before exporting a
  harness for the first time.** Also records the pi subagent-extension
  requirement and a correction to the lab's "pi skills are auto-loaded"
  assumption.

## Quick reference

| Invocation | Action |
|---|---|
| `/exact-coding-baseline-export` | Auto-detect source, date = today, harness `cc` |
| `/exact-coding-baseline-export 2026-06-15` | Auto-detect source, custom date |
| `/exact-coding-baseline-export v6.4-some-variant` | Explicit source, today |
| `/exact-coding-baseline-export 2026-06-15 v6.4-some-variant` | Both explicit |
| `/exact-coding-baseline-export all` | All four harnesses (`cc`, `pi`, `oc`, `cursor`) |
| `/exact-coding-baseline-export pi cursor` | Named harness subset |
| `/exact-coding-baseline-export overwrite` | Same as default, but allow clobber |
| `/exact-coding-baseline-export sol` | Export the promoted SOL line for all five harnesses |
| `/exact-coding-baseline-export sol sync` | Export PTDD v1 and update local `main` / `harness/*` distribution branches; never push |

Output is line-specific: Opus writes
`research/workflow-dev/export/<DATE>-exact-coding-baseline/`; SOL writes
`research/workflow-dev/export/<DATE>-exact-coding-ptdd-v1/`. Validation
must pass before reporting success.

**Every export applies all three transformations** — lab-content removal,
HITL re-enablement, and invocation gating. An export that skips axis 3
produces a workflow that still loads on every session in the consumer's
project; that is a defect, not a variant.

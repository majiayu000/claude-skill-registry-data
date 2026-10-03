---
name: dry
description: >-
  Find the subsystems that should be one subsystem. Traces a codebase resource-first
  instead of subject-first, then reports every place N independent paths reach the same
  table, file, env var, endpoint, binary, or config key without ever meeting — or where N
  places define the same decision with different answers — the
  "we built four of these and none of them know about each other" failure that stays
  invisible until the bug count spikes. Produces a ranked Convergence Map naming the
  single gateway each cluster is missing. Trigger on /dry, and on "do we have duplicate
  subsystems", "why are there four of these", "these should go through one place",
  "find the near-duplicates", "is this already implemented somewhere", "we keep
  reimplementing this", "these paths should share a gateway", "DRY audit". Do NOT fire
  to grade one diff (that is /code-review), to trace one subject's blast radius (that
  is /recon), or to cluster recurring defects (that is /radar).
argument-hint: "[path or subsystem] [--depth quick|full]"
---

# DRY

Most duplication that hurts is not duplicated text. It is **duplicated knowledge**: four code
paths that each know how to reach the same resource, none of which know about the other three.
Text-similarity tools miss it — the four rarely look alike — and they drown the real finding in
near-miss noise until people stop reading the report.

This skill inverts the usual trace. Recon asks *"what does my subject touch?"* DRY asks the same
question backwards: **"for each resource, who touches it, and do those touchers ever meet?"**

## The one rule

**A finding must name a shared *resource* or a shared *policy*, never a shared *syntax*.** Two
functions that look alike are not a finding. Two functions that both write `users.credits` by
different paths are, whether or not they share a line of text — and so are two modules that both
define what counts as a paid order, with different value sets.

The rule forbids clustering on how code *reads*. It does not forbid clustering on what code
*decides*.

## When NOT to fire

- Grading one diff or PR → `/code-review`.
- Tracing one subject's blast radius before a change → [recon](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/recon/SKILL.md).
- Clustering recurring *defects* rather than structures → [radar](../radar/SKILL.md).
- A repo under ~30 source files. Read it; you do not need a report to see four of anything.
- Deliberate parallelism: N adapters behind one interface, N drivers registered to one registry,
  N tests of one unit. **That is the gateway pattern working.** Report it only if the adapters
  bypass their own interface.

## Step 1 — Scope and resource classes

Name the root and the change budget in one line. Then pick which resource classes to index — all
of them for a full audit, two or three for a quick pass:

| Class | What to extract |
|---|---|
| **Store** | table/collection names, SQL targets, ORM models, key prefixes, bucket names |
| **File** | concrete paths and path-building patterns, lockfiles, state dirs, log destinations |
| **Config** | env vars, config keys, feature flags, secrets names |
| **Network** | hosts, base URLs, endpoint paths, queue/topic names |
| **Process** | external binaries invoked, subprocess/`exec` targets, CLI names |
| **Boundary** | first-party references pointing *into* an excluded, vendored, or generated tree, and module-path surgery that makes them work — `sys.path` inserts, `PYTHONPATH`, `NODE_PATH`, classpath tweaks. **Reportable at any toucher count:** excluding a tree hides its contents, not the reaches into it, so this shape sits below every threshold and must be exempt from them. |
| **Policy** | named constants and the *values* they carry — status/enum value sets, thresholds, byte and row ceilings, timeouts, retry counts and backoff formulas, truncation limits, allowlists |

**Policy is the class most often missed and most often expensive.** Index the *name and its value
set together* — rival definitions of one concept rarely share a name, so identifier matching will not
group them. Use this test instead:

> **Could one real-world event — a single order, request, upload — be classified differently by the
> two value sets?**

Yes → one decision split across N sites. No → different policies, however alike they look. When the
read site is hard to follow, the cheap proxy is whether the predicates reference the same entity and
field (`order.status`, `payment.state`).

**Disagreeing values are a defect only where one owner should answer.** Touchers serving different
operations or failure domains may rightly disagree — a health probe's 2-second connect timeout and a
bulk uploader's 60-second one are not a cluster, and merging them is the wrong DRY. Say why the
decision should be single before filing it.

Language does not matter — every class above is a *literal* in almost every language, which is why
this works on a polyglot tree with no parser, no index, and no git history.

## Step 1b — Read the repo's own rules first

Before indexing, read `AGENTS.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, and any
`GUIDING-PRINCIPLES` file. Ten minutes, and it changes what every later finding means:

- A rule the repo already states turns a finding from an opinion into a **violation**. "Keep
  BigQuery access behind one thin wrapper" quoted from `AGENTS.md` beside six scattered call sites is
  an argument nobody has to win.
- A **recorded decision** turns an apparent defect into house style. Contradicting one is the most
  expensive mistake this skill can make — check the docs and the inline comments before you file.

Quote the rule in the finding. Do not paraphrase it.

## Step 2 — Build the resource index (the recon half, inverted)

Sweep the tree once and emit `resource -> [file:line, ...]`. Exclude vendor, build, and dependency
directories, and say which you excluded.

Do it with the cheapest tool that holds: `rg` with a pattern per class, one pass each. If a
`codebase-memory` graph is installed, seed from it — but every edge a finding rests on is confirmed
by reading the file, exactly as in [recon](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/recon/SKILL.md). Graph-only edges are marked and never ranked.

An empty class is a finding, not a failure: a repo with no config-key duplication should say so.

## Step 2b — Audit the guards, do not trust them

If the repo ships a CI check, lint rule, or script that guards a duplication class — a
`check_no_*.sh`, a banned-import checker, a contract test — **run it, then check its coverage against
your index.** A guard is a claim, and this skill exists to test claims.

- Read its target list. Does it walk every directory the violations live in?
- Read its pattern. Does it match the identifier names the code actually uses, or only the ones its
  author had in mind?
- Compare its result to your own index for the same class. **Green plus violations in your index is a
  finding, and usually the most urgent one in the report** — because a green guard is read as
  evidence, and everyone downstream stops looking.

## Step 3 — Pivot: group, then test for disjointness

For each resource with **≥3 touching files** (**≥2** if any toucher *writes* it — write paths
diverge faster and hurt sooner; **for Policy, a definer counts as a writer**, so two rival
definitions of one decision clear the threshold), ask the question that separates a finding from a
coincidence:

> **Do these files ever meet?**

They meet if they share an import, extend a common base, or route through a common module. Resolve
it by reading the imports of each toucher — not by proximity in the tree.

- **They all meet** → not a finding. One gateway already exists; note it in *Already converged*.
- **Some meet, some do not** → **bypass finding.** A shared owner exists and part of the tree routes
  around it — including files that import it and do the job themselves anyway. This is the most
  common shape in a maturing codebase and the one `converge` expects this skill to emit; do not let
  the existence of a gateway close the question.
- **None meet** → **convergence target.** N independent paths to one resource is the shape the user
  feels as "these should all go through one place."

## Step 4 — Corroborate — two signals or it is not reported

Disjoint-touchers alone over-reports. A target ships only with a **second independent signal**:

1. **Parallel vocabulary** — same noun, different qualifier: `*-turn.sh` ×8, `fooV2`, `new_foo`,
   `enhanced_foo`, `foo_helper` beside `foo_utils`. High signal in LLM-built trees specifically,
   because a model names the sixth implementation rather than finding the first.
2. **Literal constellation** — the same 2–3 literals (a URL *and* a magic key *and* a field name)
   co-occurring in files that do not import each other. That is copied knowledge, not coincidence.
3. **Same-shape entry** — N callables with near-identical parameters and the same output contract.
4. **Divergence evidence** — the touchers already disagree: different retry counts, different
   timeouts, one validates and the others do not. This is the strongest corroborator, because it
   is the bug the cluster will produce, already visible.

Signal 4 promotes a target to the top of the ranking on its own.

## Step 5 — Rank by what one fix retires

For each surviving target: **how many call sites collapse into the gateway, and what breaks today
because they have not?** Rank by that, not by cluster size — a 3-file cluster that already
disagrees on validation outranks an 8-file cluster that agrees on everything.

Mark each target's cost honestly: introducing a gateway is a **crossing** change, and if any
toucher is consumed by another repo it is **irreversible**. Hand the classification to
[triangulate](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/triangulate/SKILL.md) rather than deciding the fix's size here.

## Step 6 — Write the Convergence Map

Long output belongs in a file: write `convergence-<repo-or-subsystem>.md` at the root of what you
scanned. Chat gets the verdict line, the path, and the top target.

```markdown
# Convergence Map — <scope>
Scanned: <N files, M excluded dirs> · Mode: <rg-only | graph+read> · Classes: <which>

## Verdict
<N convergence targets, ranked. The one-line headline.>

## Targets
### T1 — <resource> · <N paths, disjoint> · retires <M call sites>
| Path | Where | Reads/Writes | Disagrees on |
|---|---|---|---|
| <name> | file:line | W | retry=3 |
**Missing gateway:** <the one module these should route through, and where it should live>
**Evidence:** <which corroborating signals fired>
**Cost:** <contained|crossing> x <reversible|irreversible> — hand to /triangulate

## Already converged
<resources with ≥3 touchers that DO meet — proof the audit is not trigger-happy>

## Unknowns
| Unknown | Why it matters | What would settle it |
```

The **Already converged** section is load-bearing. An audit that only reports sins reads as a tool
with its thumb on the scale, and it is the section that tells you whether the sweep was honest.

## Honesty rules

- **Search the issue tracker before reporting.** For each target, search open *and* closed issues for
  the resource or constant name, and label it `new`, `tracked (#N)`, or `closed-but-present (#N)`.
  That last label is its own finding: work that was closed without landing. Re-filing tracked work is
  how an audit loses its reader.
- Every path in a target cites `file:line`. No `file:line`, no row.
- Never claim two files "don't talk" without having read both import blocks. Say `unverified`.
- Zero targets is a real result on a small or well-factored tree. Say which, rather than
  manufacturing a cluster to look thorough.
- Do not propose the gateway's implementation. DRY names what should converge and stops;
  [triangulate](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/triangulate/SKILL.md) sizes the change and `/ponytail` shrinks it.

## Neighbors

- [recon](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/recon/SKILL.md) — traces one subject outward. DRY runs the same trace resource-first.
- [triangulate](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/triangulate/SKILL.md) — sizes and paces the convergence work this skill finds.
- [radar](../radar/SKILL.md) — clusters recurring defects; DRY clusters structures. A repo that keeps producing the
  same bug class is often a DRY target radar has already noticed from the other end.
- [ponytail](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/ponytail/SKILL.md) — a gateway is machinery; make it the smallest one that works.

---
name: gaia-triage
description: >
  Triage the Gaia issue backlog and skill-batch intake queue. Use this skill when someone
  asks to: "triage issues", "clean up the issue tracker", "review the backlog", "close
  stale issues", "process the intake queue", "review skill-batches", "evaluate draft skill
  proposals", "approve or reject pending skills", "is this issue still valid?", "what's
  clogging the backlog?", "run a triage pass", or /gaia-triage. Covers two workstreams:
  (1) GitHub issue lifecycle — identifying resolved, stale, or need-more-info issues and
  acting on them via gh CLI; (2) skill-batch intake — evaluating draft proposals in
  registry-for-review/skill-batches/ and routing them toward promotion or rejection. This
  is the gatekeeping step before new skills enter the canonical registry; and (3) a
  cross-repo triage sweep — sizing, P0-P4 prioritization, umbrella/epic synthesis, and
  assignment across every gaia-research org repo, on the one headquarters tracker.
---

# gaia-triage

Triage has three workstreams — GitHub issue hygiene, skill-batch intake review, and the
cross-repo prioritization sweep. Run them independently or together depending on what the
user asks for. All three produce documented, auditable decisions rather than silent
changes.

This skill absorbed `favorchurch/rock-steward`'s `rock-triage` (2026-09-01): its impact
sizing, priority matrix, four-step inspection, and prioritized-matrix output landed here
as **Workstream 3** rather than shipping as a second, competing triage skill. There is one
`gaia-triage`. Its priority ladder is the `P0`-`P4` ladder `/gaia-meta-audit` and
`/gaia-meta-sweep` already use — one vocabulary, not two.

Triage is **not** cartography. Sorting a backlog of known work is this skill; planning an
effort too big for one session as a map of decision tickets is `/wayfinder`. Taking one
triaged issue end-to-end to a PR is `/gaia-issue-resolver`.

---

## Headquarters

**Every issue lives on `gaia-research/gaia-skill-tree`**, regardless of which repo the fix
lands in. One tracker for the whole org.

```bash
export GAIA_HQ=gaia-research/gaia-skill-tree
```

Tag the target repo on the issue when the work lands elsewhere — a line at the top of the
body, `**Target repo:** \`gaia-research/gaia-skill-heaven\``, matching the `/wayfinder`
convention. Cross-repo references use the full `gaia-research/<repo>#<n>` form; a bare
`#<n>` always resolves to HQ.

---

## Classification taxonomy

Every triaged issue gets a size and a priority. Both are labels; neither is invented ad
hoc (see label hygiene below).

### Impact size

Blast radius, structural complexity, and data footprint — not hours.

| Size | Means |
|---|---|
| `XS` | Trivial fix, label correction, single config value, negligible blast radius |
| `S` | Minor scoped adjustment, one predicate, isolated UI touch-up |
| `M` | Standard scoped task — one command, one schema field, one localized workflow |
| `L` | Cross-component change, non-trivial data backfill, multi-surface impact |
| `XL` | Architecture-level refactor, substantial registry debt remediation |
| `XXL` | High blast radius — core schema, authorization, or site-wide parity |
| `Epic` | Umbrella spanning multiple distinct sub-issues across domains |

### Priority — `P0`-`P4`

The same ladder `/gaia-meta-audit` and `/gaia-meta-sweep` use. Read those for the
registry-specific instances of each rung.

| Priority | Means |
|---|---|
| `P0` | Critical integrity violation or active breakage — unsupported top-rank claim, security/authorization exposure, secrets in a diff, the site dark, `main` red |
| `P1` | Structural correctness — dead evidence links, Star Bar gaps, broken data contracts, lockstep drift, a prerequisite blocking milestone delivery |
| `P2` | Attribution, sourcing, and feature upgrades — wrong promoted pointer, stale catalog URL, enhancement to a working surface |
| `P3` | Registry hygiene and nice-to-haves — over-broad mappings, duplicate clusters, backlog enhancements, exploratory design |
| `P4` | Documentation cleanup — placeholder bodies, generated-output drift, comment and copy fixes |

`P0` interrupts. `P1` schedules. `P2`-`P4` queue.

### Label hygiene

- **Preflight.** Inspect the existing labels before applying any:
  ```bash
  gh label list --repo "$GAIA_HQ" --limit 200
  ```
- **Zero ad-hoc labels.** `.github/workflows/labels-sync.yml` reconciles labels from
  `.github/labels.yml` on every push to `main` with `skip-delete: false` — **a label that
  is not in that file is deleted off live issues at the next sync.** If you need a new
  label, add it to `.github/labels.yml` in a PR. Never create one with `gh label create`
  and assume it survives.
- **Idempotency.** If an issue already carries an appropriate priority and size, do not
  relabel it. Post the status update and move on.
- The five triage roles (`needs-triage`, `needs-info`, `ready-for-agent`,
  `ready-for-human`, `wontfix`) map to this repo's label strings in
  `docs/agents/triage-labels.md`. Extend that table rather than inventing labels.

---

## Workstream 1: GitHub Issue Triage

The goal is a clean, signal-rich backlog — not a closed one. Closing issues prematurely
hides real work; leaving stale issues open buries actionable items. For each issue, make
an explicit call: close (resolved), update (needs narrowing), or keep (valid, still open).

### Step 1 — Pull the open issue list

```bash
gh issue list --repo gaia-research/gaia-skill-tree --state open --limit 100
```

Group by theme (CLI bug, registry data, docs drift, enhancement). This shapes the
decision pattern — CLI bugs and registry issues require code evidence; enhancement requests
require a current-relevance check against the roadmap.

### Step 2 — Audit each issue against the codebase

Before commenting or closing, verify the claim. Check the evidence paths in
`references/evidence-check.md` for common file locations:

| Issue type | Where to look |
|---|---|
| CLI command request or bug | `src/gaia_cli/commands/` |
| Registry data or duplicate skills | `registry/gaia.json`, `registry/nodes/` |
| Documentation drift | Run `python scripts/build_docs.py --check` |
| Packaging / dependency | `pyproject.toml`, `uv.lock` |
| Test coverage | `tests/` |

### Step 3 — Act via gh CLI

**Post a triage comment** (findings without closing — use when the issue needs narrowing
or a reproduction, or when you want to flag it for a human maintainer):

```bash
gh issue comment <issue-number> --repo gaia-research/gaia-skill-tree \
  --body "Triage update: <findings and recommendation>"
```

**Close a resolved issue** (only when codebase evidence confirms it is implemented):

```bash
gh issue close <issue-number> --repo gaia-research/gaia-skill-tree \
  --reason completed \
  --comment "Closing as implemented. Evidence: <specific file + line or command output>"
```

**Dry-run first**: the `scripts/triage_batch.sh` script supports `--apply` and
`--close-resolved` flags. Run without flags to preview all comments before posting:

```bash
bash .claude/skills/gaia-triage/scripts/triage_batch.sh
# Then, when ready:
bash .claude/skills/gaia-triage/scripts/triage_batch.sh --apply --close-resolved
```

### Decision guide

| Finding | Action |
|---|---|
| Issue is implemented and tests pass | Close as completed with evidence pointer |
| Issue is valid but under-specified | Comment with narrowing questions; keep open |
| Issue references a stale command name | Comment updating the correct current command; keep open unless fully superseded |
| Issue is a duplicate | Close with a link to the canonical issue |
| Issue is an enhancement blocked on design | Comment with current blocker; keep open |

---

## Workstream 2: Skill-Batch Intake Review

Draft skill proposals land in `registry-for-review/skill-batches/` after a contributor
runs `gaia push`. This workstream gates them before they enter `registry/nodes/`.

Rejecting bad batches here is cheaper than demoting skills after promotion — every skill
that enters the canonical registry acquires timeline history, evidence links, and
downstream references that make later removal messy.

### Step 1 — List pending batches

```bash
ls registry-for-review/skill-batches/
```

Each batch is a JSON file. Read its metadata to understand the contributor and scope before
evaluating individual skills.

### Step 2 — Evaluate each skill proposal

For each skill in the batch, work through these checks in order:

1. **Schema validity** — does the node satisfy the canonical JSON schema?
   ```bash
   gaia dev validate --intake
   ```
2. **Nomenclature** — does the skill name and description match `CONTEXT.md` vocabulary?
   Flag banned synonyms; the rarity field is deprecated and should not appear in new proposals.
3. **Evidence quality** — each above-1★ claim needs graded evidence with a valid Evidence Type (arxiv|repo|github-stars) and a derived Evidence Grade;
   weak/ungraded-only evidence is grounds for `needs-info`. Ranking up gates on Trust Magnitude, not an evidence-class floor.
4. **Prerequisite existence** — all `prerequisites[]` IDs must resolve in the current registry.
   ```bash
   gaia dev list --generic | grep <prerequisite-id>
   ```
5. **Duplication check** — does a substantially equivalent skill already exist?
   ```bash
   gaia dev list --generic | grep -i "<skill-name>"
   ```

### Step 3 — Label and route

Apply one of three dispositions per skill:

| Label | Meaning | Next action |
|---|---|---|
| **approve** | Schema valid, evidence solid, no duplicate | Promote via `gaia dev add` |
| **needs-info** | Fixable gap (weak evidence, missing prereq, naming issue) | Comment on the batch file with specifics; do not promote yet |
| **reject** | Duplicate, out of scope, or unfixable schema violation | Document reason; discard batch entry |

For approved skills, promote via CLI (never hand-edit registry nodes directly):

```bash
gaia dev add "<Skill Name>" --type basic --description "<description>"
gaia dev evidence <skill-id> "<url>" --type repo --trust <value>
```

After promotion, regenerate Class S artifacts:

```bash
gaia dev docs
```

---

## Workstream 3: Cross-repo triage sweep

Use this when the ask is "triage the backlog" at scale rather than "is this one issue
still valid". It sizes, prioritizes, links, and assigns — and it ends in a matrix a human
can act on without reopening every thread.

### Four-step inspection

Run all four on every issue in scope, in order:

1. **State & relevance.** Is it still live, or already resolved/superseded? Verify against
   the codebase, merged PRs, or a read-only probe — never against the issue's own claim.
   The read-only probes are the ones in `/gaia-issue-resolver` Phase 2 (`gaia dev audit`,
   `scripts/verify_evidence.py`, `python scripts/build_docs.py --check`). If resolved,
   close with the evidence.
2. **Status update & timeline.** One concise technical comment: what is true now, and
   whether the work is starting soon, blocked on a prerequisite, or in backlog.
3. **Linkage & umbrella synthesis.** Find the shared cause across issues. Where several
   related sub-issues have no parent, create an umbrella and label it `epic`, then nest
   the children as **GitHub sub-issues** (`gh api repos/$GAIA_HQ/issues/<parent>/sub_issues
   -f sub_issue_id=<child-id>` — the child's *id*, not its number).
   An umbrella that turns out to be a fog-bound effort rather than a known set of tasks is
   a `/wayfinder` map, not an epic. The test: if the children are decisions you cannot yet
   state precisely, stop triaging and chart a map.
4. **Assignment.** Default to the original issue author unless someone is already assigned.
   Assign a synthesized umbrella to the owner of its constituent issues.

### Fan-out

Delegate parallel reads — pulling issue payloads, checking whether a claim still holds in
the tree, counting occurrences — to cheap subagents. Keep with yourself: deciding
priority, deciding size, judging whether two issues share a cause, and writing the
umbrella. Give each subagent the exact command and the exact thing to report back; a
subagent asked to "investigate" returns prose, one asked to "run X and report the integer
after `Total:`" returns data.

### Output — the prioritized matrix

```markdown
# Gaia Triage Summary — <date>

## P0 - Critical
- **#<n>** - <Title> | `<Size>` | repo: `<target repo>` | assignee: `@<who>` | <Active/Blocked/Ongoing>
  - *Umbrella*: <link>
  - *Verification*: <what was actually probed, and the result>
  - *Next action*: <the immediate step>

## P1 - Structural correctness
## P2 - Attribution & upgrades
## P3 - Hygiene & backlog
## P4 - Documentation

## Umbrellas & epics
- **Epic: <Title> (#<n>)** [assignee: `@<who>`] - sub-issues: #A, #B, #C
```

Refer to issues by **title**, not by bare number — a wall of `#42, #43, #44` is illegible.

---

## Output

At the end of a triage pass, report:

- How many issues were reviewed, closed, and left open with comments
- How many batch skills were evaluated, approved, flagged needs-info, and rejected
- The prioritized matrix, if Workstream 3 ran
- Any recurring patterns worth tracking (e.g. a common prereq that's missing from the
  registry) - a pattern seen a fourth time is a Class A detector in
  `/gaia-issue-resolver`, not another issue

This summary helps the next maintainer understand what happened without re-reading every issue thread.

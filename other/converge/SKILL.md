---
name: converge
description: >-
  Read two or more Convergence Maps produced by /dry — across repos, or across
  re-runs of one repo — and find what repeats. Clusters findings by SHAPE rather
  than by resource, so "a gateway exists and the files that import it bypass it
  anyway" surfaces as one portable finding rather than four unrelated ones, and
  tracks whether each target got fixed, ignored, or worse since the last sweep.
  Output is a fleet verdict plus house rules worth enforcing everywhere, not
  another per-repo report. Trigger on /converge, and on "do all our repos have
  this problem", "what keeps happening across projects", "did the last audit
  actually get fixed", "which of these should be a shared library", "org-level
  duplication", "fleet health". Do NOT fire with fewer than two maps — run /dry
  first — and do NOT fire to audit a single repo, which is /dry's whole job.
argument-hint: "[map paths or repo roots]"
---

# Converge

[dry](../dry/SKILL.md) audits one repo. Converge reads several of its maps and answers the questions
a single map cannot: **what repeats, and what changed.**

Both questions matter for a different reason. A target that repeats across repos is not a repo
problem — it is a production problem, and fixing it once in a shared place beats fixing it N times. A
target that survived a re-run is not a backlog item — it is evidence that naming it did not work, and
the next attempt needs a different mechanism.

## The one rule

**Cluster by shape, never by resource.** Two repos rarely share a table name or an API host, so
resource-level clustering finds nothing across a fleet. What they share is the *shape* of the
failure: "gateway exists, importers bypass it", "N rival gateways, none authoritative", "helper
specified in a closed issue, never built". Shape is what ports.

## When NOT to fire

- Fewer than two maps → run [dry](../dry/SKILL.md) first. Converge has nothing to cluster.
- One repo, one point in time → that is [dry](../dry/SKILL.md), and it already answered.
- Recurring *defects* rather than recurring *structures* → [radar](../radar/SKILL.md), per repo.
- The maps are stale relative to their repos. Re-run `dry` rather than clustering fiction; say which
  maps you refused and why.

## Step 1 — Collect the maps

Take map paths, or repo roots to search for `convergence-*.md`. For each, record the repo, the
commit it was taken at, and its date. **A map whose commit is not an ancestor of that repo's current
HEAD is stale** — either re-run `dry` or exclude it, and say which you did.

Two or more maps is the floor. Two maps of the *same* repo at different commits is the re-run case
(Step 3); two maps of *different* repos is the fleet case (Step 2). Both at once is normal.

## Step 2 — Cluster by shape

Read every target in every map and assign it a shape. These four cover most of what `dry` finds;
add one only when a target genuinely fits none, and say so:

| Shape | The tell | Why it recurs |
|---|---|---|
| **Bypassed gateway** | A single canonical module exists; files that import it still reach the resource directly | The gateway was built but never made mandatory. Nothing fails when you skip it. |
| **Rival gateways** | Two or more canonical modules for one job, mutually unaware | Two subsystems grew separately and neither was ever declared authoritative |
| **Unbuilt helper** | A closed issue or doc specifies the shared helper; it does not exist | Cleanup was tracked as a checklist and closed on the items that were easy |
| **Post-fix regression** | New bypasses added *after* the convergence work landed | No mechanism enforces the rule, so entropy resumes the day attention moves |

A shape reported by **two or more repos** is a fleet finding. One repo with one instance is that
repo's business — leave it in `dry`'s map and do not re-report it here.

## Step 3 — Diff the re-runs

Where two maps cover the same repo, classify every target from the older map:

- **Fixed** — gone, and the gateway is adopted. Name it. An audit that only reports what is still
  broken teaches people the report never improves, and they stop reading it.
- **Unchanged** — still present at the same sites. Record how long it has been open.
- **Worse** — more bypasses than before. This is the finding that outranks everything else, because
  it means the previous fix had no enforcement behind it.
- **Moved** — the resource changed but the shape survived. Still open; the fix addressed an instance
  rather than the cause.

**Same line numbers across two commits is the strongest evidence in this skill.** It proves the call
site was not merely un-fixed but never touched — nobody has looked at it since the last audit.

## Step 4 — Rank by what one rule retires

Fleet findings rank by **how many repos and call sites a single enforceable rule would retire**, not
by how bad any one instance looks.

For each fleet finding, name the mechanism honestly, cheapest first:

1. **A CI rule** — one grep with a non-increasing baseline. Prefer this. It is the only mechanism on
   this list that works while nobody is paying attention.
2. **A house rule in the repo's agent instructions** — cheap, but only binds work that reads it.
3. **A shared library** — real convergence, real cost. Justify it with the call-site count, and only
   after the same shape has appeared in three or more repos.

If a shape recurs and none of the three fits, say that plainly. "We keep doing this and there is no
cheap way to stop" is a legitimate and useful finding.

## Step 5 — Write the fleet verdict

Long output belongs in a file: `converge-<fleet-or-date>.md`, beside the maps. Chat gets the verdict
line, the path, and the top fleet finding.

```markdown
# Converge — <scope> · <date>

## Verdict
<N fleet findings across M repos; K targets fixed since last sweep; J got worse.>

## Fleet findings
### F1 — <shape> · <N repos> · one rule retires <M sites>
| Repo | Instance | Sites | Since |
|---|---|---|---|
**Mechanism:** <CI rule | house rule | shared library> — <the exact rule>
**Baseline:** <the measured count the rule must not exceed>

## Since last sweep
| Repo | Target | Was | Now | Verdict |
|---|---|---|---|---|
<fixed / unchanged / worse / moved — fixed rows first>

## Not a fleet finding
<single-repo targets, named so they are not re-clustered next time>

## Maps read
| Map | Repo | Commit | Date | Stale? |
```

**Fixed rows go first.** The section exists to show the work moves, and a fleet report that opens on
failure gets read once.

## Honesty rules

- Every instance cites the map it came from and the `file:line` that map cited. Converge adds no new
  claims about code — it clusters claims `dry` already verified. If you need a fact no map contains,
  re-run `dry`; do not grep for it here and present it as a fleet finding.
- Do not upgrade a single-repo target to a fleet finding to reach a rounder number.
- A shape appearing in every repo may be a house style rather than a defect. Ask whether it costs
  anything before ranking it, and say so if the answer is no.
- Zero fleet findings across several maps is a real and good result. Report it as one.

## Neighbors

- [dry](../dry/SKILL.md) — produces the maps this skill reads. Always runs first.
- [triangulate](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/triangulate/SKILL.md) — sizes the convergence work; a shared library is a crossing
  change and usually an irreversible one.
- [radar](../radar/SKILL.md) — per-repo defect clustering. Converge is the structural counterpart
  across repos, and a defect radar keeps re-finding is often a shape converge already named.
- [recon](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/recon/SKILL.md) — the trace underneath all of it.

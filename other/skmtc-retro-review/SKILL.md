---
name: skmtc-retro-review
version: 0.1.0
description: |
  Aggregate friction log files across a time period to identify recurring
  patterns, classify each cluster by intervention type, produce a
  prioritized action plan with success criteria, and calculate convergence
  metrics. Complements `skmtc-retro` (which captures per-session signal)
  by acting as the system's actuator: turning accumulated observations into
  decisions. The primary output is a review document that makes the "is it
  getting better?" question answerable.

  Use this skill when the user asks to "review retros", "review friction",
  "run a retro review", "what's the pattern across sessions", "what should
  we fix next", or on a periodic cadence (monthly, pre-release). Also run
  after a cluster of sessions on the same feature area to surface systemic
  issues before they compound.

  Distinct from `skmtc-retro` — that skill captures per-session
  observations; this skill synthesizes them into decisions. Do not run
  this skill as a substitute for a per-session retro.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
metadata:
  internal: true
---

# SKMTC retro review

The friction log is a sensor. This skill is the actuator. Its job is to
read accumulated observations, detect patterns the per-session view cannot
see, classify each pattern by what kind of intervention would eliminate it,
and produce an action plan the user can execute.

Without this skill, the friction log is a cemetery: observations accumulate
but nothing systematically improves. The review closes the loop.

## 1. When to invoke

**Scheduled cadence (recommended):**
- Monthly: review all sessions in the prior month.
- Pre-release: audit open entries against the release's scope to catch
  unresolved blockers before they reach users.

**On-demand:**
- After 3+ sessions in the same feature area (e.g., "three sessions on
  enrichment config in a week — what's the systemic issue?").
- When the user suspects a pattern but can't see it from individual retros.
- After a significant skill or doc update: "did the change actually work?"

**Skip if:**
- Fewer than 3 session files have accumulated since the last review.
- The friction log is empty or contains only resolved entries.

## 2. Locating files

**Friction log:**

```
<skmtc-root>/skmtc/deno/docs/friction-log/
```

**Review output:**

```
<skmtc-root>/skmtc/deno/docs/friction-log/reviews/
```

Create the `reviews/` subdirectory if it doesn't exist.

**Review filename:**

```
<YYYY-MM-DD>-review-<period>.md
```

Where `<period>` is a human-readable date range: `2026-05` (monthly),
`2026-Q2` (quarterly), or `2026-05-12-to-05-14` (targeted).

Examples:
- `2026-05-15-review-2026-05.md`
- `2026-05-15-review-pre-v0.5.md`

## 3. Reading the friction log

### Which files to read

1. **Glob** the friction log directory for `*.md` files, excluding `CLAUDE.md`,
   `README.md`, `discrepancy-catalog.md`, and anything in `reviews/`.
2. **Filter by date**: include only files whose `YYYY-MM-DD` prefix falls
   within the review period. For a monthly review, include all files from
   that month plus any older files with open entries.
3. **Always include files with open entries** regardless of date — unresolved
   observations accumulate across periods and contribute to the leak metric.

### What to extract from each file

For each retro file, extract:

- **Session date and topic** (from the filename and `# heading`)
- **All entries**: number, heading, severity tag, status
- **Knowledge acquired rows** (from `## Knowledge acquired` tables if present)
- **Version anchors** on friction entries (which version was the pain observed against?)
- **Resolution status**: `open`, `resolved <date>`, `superseded`, `wontfix`

Do not try to re-derive the root cause from entry bodies at this stage —
extract the structured fields first, then read bodies only for entries you
intend to cluster.

### Reading efficiency

With many files, read the `## Index` table first (it's a summary of the
whole file). Read entry bodies only for entries that survive initial
filtering. This avoids loading the full text of every historical file.

## 4. Clustering entries

Clustering is the hardest step and the most error-prone. The goal is to
group entries that share a **root cause**, not just a surface topic. Two
entries about "import registration" may have completely different root
causes; two entries that look unrelated (e.g., "error message was unclear"
and "I had to read the source to understand X") may share the root cause
"API behavior is not legible from its interface."

### Clustering rules

1. **Group by root cause, not by topic.** Ask: "Would fixing X also fix Y?"
   If yes, they belong in the same cluster. If not, keep them separate even
   if their surface topic is the same.

2. **A cluster must have at least 2 entries** from different sessions (or 1
   entry classified as `[blocker]`) to warrant action. Single-session
   single-occurrence friction may be genuinely incidental.

3. **One entry can belong to multiple clusters** if it has multiple root
   causes. Prefer the most specific cluster.

4. **Explicitly note your clustering hypothesis** in the review. "I'm
   grouping these because I believe they share root cause X" — this lets the
   user push back if the grouping is wrong. Do not present clusters as facts.

5. **Unclustered entries** — entries that don't fit any cluster — are still
   worth listing. Single-occurrence blockers in particular get their own
   cluster even without a second instance, because their severity warrants
   attention.

### Cluster description format (internal working note)

For each cluster before writing the review:

```
Cluster: <short name>
Root cause hypothesis: <one sentence>
Entries: <file>#<N>, <file>#<N>, ...
Severity range: <lowest> to <highest>
Resolved entries: N of total
```

## 5. Intervention taxonomy

For each cluster, classify by intervention type using the decision tree
below. Work through the questions in order — higher-ranked interventions
are more permanent than lower-ranked ones.

### Decision tree (in priority order)

**1. Can this be eliminated by invariant enforcement (tooling)?**

This is the highest-leverage intervention. A mechanically-checked rule
cannot be violated silently; documentation can.

Candidates:
- Rules that must hold for every generator (single-base, location-independence,
  no cross-package peers) → `doctor` check or bundle-time lint rule.
- Rules about file structure or import shape → custom `deno lint` plugin or
  pre-bundle validation step.
- Invariants currently only documented in skills → consider promoting to
  runtime assertion or CLI warning.

If tooling is feasible: recommend a specific check (what it tests, what
error it produces, where it runs). Label intervention type: `tooling`.

**2. Is this a footgun in the API design?**

A footgun is an API that is easy to misuse in a way that compiles and runs
but produces wrong output. Examples: `ImportNameArg` object form producing
unexpected aliasing; `.isRef() ? resolve() : schema` ternary being
redundant because the non-ref variants also implement `.resolve()`.

Footguns cannot be fully fixed by documentation — the fix is normalization,
tightening the type to block invalid input, or a better runtime error.

If a footgun: recommend the specific API change (normalize the edge case,
restrict the type, add a runtime guard). Label: `skmtc-code`.

**3. Is this a missing runtime capability (architectural limit)?**

When the task genuinely cannot be done with the current API — not a
documentation gap, but a structural absence. Example: the
one-operation-to-many-forms blocker that required the operation-variant
axis in `@skmtc/core@0.5.0`.

These are the most expensive to fix but also have the highest impact.
If it's an architectural limit: flag for core roadmap with a description
of what the API surface should look like. Label: `skmtc-core-feature`.

**4. Is this a wrong LLM prior about SKMTC behavior?**

The LLM's training data includes many frameworks. It applies defaults from
those frameworks to SKMTC. When the SKMTC behavior differs from the prior,
friction occurs even when the behavior is correctly documented — because the
LLM didn't reach for the docs.

Skill updates override priors at task time. They are most effective when
they name the prior explicitly: "In TypeScript you would do X. In SKMTC
you do Y instead, because Z."

If a wrong prior: add an operational principle to the relevant skill with
the pattern `"In <other> you would... In SKMTC you... because..."`. Label:
`skill-update`.

**5. Is this a knowledge gap in docs?**

The agent had to discover correct behavior by trial, reading source, or
asking the user — and the answer exists nowhere in docs or skills.

Sub-types:
- **API reference gap**: a method, shape, or option isn't documented.
  Fix: add to API reference.
- **Principle gap**: a design rule or philosophy isn't articulated.
  Fix: add to a how-to doc or concept doc.
- **Discoverability gap**: the doc exists but the agent couldn't find it.
  Fix: improve cross-referencing, add to agent-context surfacing, or move
  the doc closer to where agents look first.

Also consider adding the knowledge to `skmtc agent-context` output — if
an agent starts briefed with this fact, the friction never occurs. Label:
`doc-update`, `agent-context`, or `doc-discoverability`.

**6. Is this a missing worked example?**

Some principles are best taught by a concrete, working example rather than
a rule. If the friction repeatedly occurs despite the rule being documented,
the rule alone isn't working — add an example.

Examples live in test fixtures, an `examples/` directory, or inline in
skill entries. The example must be a complete, real, runnable snippet —
not pseudocode. Label: `example-addition`.

**7. Should this API or generator be removed?**

Sometimes the right fix is deletion. If an API creates persistent footguns
with no clean fix, or a generator's design is fundamentally incompatible
with SKMTC's regeneration contract, removing it is higher leverage than
continuing to document around it. The GraphQL thin-wrapper generators were
deleted rather than fixed.

Recommend removal only when: (a) the API is a persistent source of friction
across multiple sessions, (b) a skill/doc fix has already been attempted and
didn't eliminate recurrence, and (c) there is an alternative approach.
Label: `removal`.

### Intervention label reference

| Label | What it is |
|-------|------------|
| `tooling` | Doctor check, lint rule, bundle-time validation |
| `skmtc-code` | Bug fix or API normalization in `@skmtc/core` or a gen-* package |
| `skmtc-core-feature` | New capability needed in `@skmtc/core` |
| `skill-update` | New or modified operational principle in a skill |
| `doc-update` | New or expanded content in API reference or how-to docs |
| `agent-context` | Add fact to `skmtc agent-context` output |
| `doc-discoverability` | Improve cross-referencing or surfacing of existing doc |
| `example-addition` | Add a worked example to a test, examples dir, or skill |
| `removal` | Deprecate or delete the problematic API or generator |

## 6. Convergence metrics

Calculate these metrics for the review period and append a row to the
metrics history table in the review file.

### Friction Recurrence Rate (FRR)

The primary convergence signal.

```
FRR = recurrent entries / total entries (for the period)
```

A "recurrent entry" is one where the same root cause was logged in a prior
period and the prior instance has status `open` (no intervention was made
or the intervention didn't work).

- **FRR trending down**: interventions are working; new friction is mostly
  novel.
- **FRR flat**: interventions aren't landing. Check whether recommended
  actions were actually completed. Check whether the skill/doc change
  targeted the right root cause.
- **FRR trending up**: regression — something broke that was previously
  working, or a new footgun was introduced.

### Severity distribution

```
Blocker% = blocker entries / total entries
```

Convergence looks like: `Blocker% → 0`, then `Friction% → 0`, leaving
only `Polish%` and eventually silence. If `Blocker%` is flat or rising,
the system is not converging at the structural level — code changes are
needed, not just docs.

### Open entry accumulation

```
Total open entries (all time) = sum of unresolved entries across all files
```

This number should not grow unboundedly. If it grows faster than entries
are resolved, the action loop is too slow. A target: open entries should
halve within two review cycles after a recommendation is acted on.

### Knowledge backlog

```
Knowledge backlog = count of "Knowledge acquired" rows across all retro
                    files whose doc implication is not "none" and whose
                    content has not yet been added to docs/skills
```

This measures how much extracted intelligence remains un-acted. A large
backlog means the retro → doc pipeline is blocked somewhere.

### Resolution velocity

```
Resolution velocity = average days from entry creation to resolved status
                      (for entries resolved in the review period)
```

Long velocity (30+ days) indicates the action loop is slow — typically
because "recommended action" stays in a review doc without being assigned
or prioritized. Short velocity (< 7 days) is ideal.

## 7. Review file format

```markdown
# Friction Review — <period>

**Reviewed:** <YYYY-MM-DD>
**Period:** <date range>
**Sessions included:** N
**Files read:** <list of filenames>

## Summary

| Metric | Value | vs. prior period |
|--------|-------|-----------------|
| Total entries | N | +N / -N |
| Blocker% | X% | ↑ / ↓ / — |
| Friction Recurrence Rate | X% | ↑ / ↓ / — |
| Total open entries (all time) | N | +N / -N |
| Knowledge backlog | N items | +N / -N |
| Resolution velocity (period) | N days avg | |

## Convergence signal

<2-3 sentences. Is the system converging, flat, or diverging? What's the
dominant pattern? Be direct — "FRR is 60% and flat; skill updates are not
reaching the root cause" is more useful than "mixed results.">

## Clusters

| # | Cluster | Root cause hypothesis | Sessions | Severity | Open | Recommended intervention |
|---|---------|----------------------|----------|----------|------|--------------------------|
| C1 | <name> | <one sentence> | N | blocker/friction/polish | N/total | <label> |

## Action plan

### P1. <Intervention label> — <Cluster name>

**Root cause:** <one sentence>
**Evidence:** <file>#<N>, <file>#<N> (N total instances)
**What to do:** <specific, actionable change — not "improve docs" but "add
a note to §import-registration in the generator skill explaining that the
object form of ImportNameArg always produces `name as alias` output, even
when alias is omitted, and the bare string form is correct for non-type
non-aliased imports">
**Success criterion:** <falsifiable condition — "subsequent retro files
should contain zero entries about ImportNameArg object form misuse">
**Verification:** check the next 2-3 retro files after the change for
recurrence of this pattern

---

### P2. ...

## Knowledge backlog

Items from `## Knowledge acquired` tables not yet reflected in docs/skills:

| Source | Item | Doc implication | Priority |
|--------|------|-----------------|----------|
| <file> K1 | <what was learned> | <skill/doc/agent-context> | high/medium/low |

*If backlog is empty: "All knowledge-acquired items from this period are
reflected in current docs and skills."*

## Metrics history

<!-- append one row per review; do not delete prior rows -->

| Review date | Period | Sessions | FRR | Blocker% | Open (all time) | Knowledge backlog | Actions completed |
|-------------|--------|----------|-----|----------|-----------------|-------------------|-------------------|
| <YYYY-MM-DD> | <period> | N | X% | X% | N | N | N of N prior |
```

### Metrics history

The `## Metrics history` table accumulates across reviews — append one row
per review cycle, never delete prior rows. This is the convergence record.
It is the only place where the trend question ("is it getting better?") can
be answered empirically rather than by impression.

If no prior review file exists, create the table with one row. Future
reviews append to the same table in the same file, or to a new review file
that cross-references the prior one with a link.

### Action plan ordering

Order the action plan by:

1. Intervention type permanence: `tooling` > `skmtc-code` > `skmtc-core-feature` > `skill-update` > `doc-update` > `example-addition`
2. Within the same type: frequency × severity. A cluster of 4 `[friction]`
   entries outranks 1 `[friction]` entry; a `[blocker]` outranks multiple
   `[friction]` even at the same type level.
3. Recurrent clusters (FRR contributors) rank above first-occurrence clusters
   of the same severity — recurrence means a prior attempt didn't work.

### Action plan specificity requirement

Every action plan entry must name:
- The exact file/section to change (not just "update the skill")
- The exact content to add or change (not just "clarify this")
- A falsifiable success criterion
- How to verify it worked (what to look for in the next retro files)

Vague recommendations ("improve documentation of X") are not actionable and
will not close the loop. Specific recommendations ("add the following
paragraph to §3 of skmtc-generator SKILL.md, under the `register` API
section:...") can be completed in minutes.

## 8. Prior action follow-up

Before drafting new action items, check the most recent prior review file
(if one exists) and answer:

1. **What was recommended?** List the prior P1, P2, P3 items.
2. **What was completed?** For each, check whether the recommended change
   appears in the skill, doc, or code (read the target file or run a grep).
3. **Did it work?** For completed items, check whether the friction pattern
   recurred in sessions after the change. If yes: the intervention targeted
   the wrong root cause — escalate to a higher-permanence intervention.
4. **What was not completed?** List items that were recommended but not
   acted on. These carry forward to the new action plan with increased
   priority — a recommendation that's been skipped once needs a specific
   owner or a lower-effort formulation.

Record this follow-up as the first section after the summary in the new
review file.

## 9. Composing the review

Full flow:

1. **Glob** the friction log for files in scope. List them explicitly.
2. **Read the Index tables** of each file. Extract entry numbers, headings,
   severities, statuses. Do not read bodies yet.
3. **Filter**: separate open from resolved entries. Separate the review
   period entries from the all-time-open entries carried forward.
4. **Read bodies** only for open entries you intend to cluster — skip
   resolved entries unless investigating whether a fix worked.
5. **Check prior review** if one exists: list what was recommended,
   what was completed, what recurred.
6. **Cluster** open entries by root cause. State each clustering hypothesis
   explicitly. Assign intervention type per cluster using the decision tree.
7. **Calculate metrics**: FRR, Blocker%, total open, knowledge backlog,
   resolution velocity.
8. **Compile the knowledge backlog**: extract `## Knowledge acquired` rows
   from the period's retro files. Check each against current docs/skills to
   see if it's already been addressed.
9. **Write the review file**: summary → convergence signal → prior action
   follow-up → clusters → action plan → knowledge backlog → metrics history.
10. **Summarise to the user** in one short message:
    `Review written to <filename>. N clusters, top intervention: <P1 label — cluster name>. FRR: X% (prior: Y%). <convergence signal sentence>.`

## 10. After the review

The user decides which action plan items to execute. The review skill does
not execute them — it produces decisions. Each action item is a unit of
work for the relevant skill (`skmtc-generator`, `skmtc-cli`, docs editing,
or filing a SKMTC code issue).

When an action item is completed, update the corresponding retro file
entries' `**Status:**` lines and the `## Index` rows. Also update the
review file's metrics history row for the period (if the resolution
happened within the same period).

The next review cycle opens with §8 "Prior action follow-up" to verify
that completed items actually eliminated the friction. This is the
feedback loop that drives convergence: observe → cluster → intervene →
verify → observe.

**The convergence guarantee**: the system converges when every friction
cluster, on recurrence, triggers escalation to a higher-permanence
intervention. Friction that doesn't yield to docs must be taken to
skill-update. Skill-updates that don't eliminate recurrence must be
taken to code. Code changes that are blocked must be taken to the
roadmap. Clusters that cannot be addressed at any level are candidates
for removal of the offending API or feature. With this escalation
discipline, every class of friction either gets eliminated or gets
explicitly accepted as a known cost — neither outcome leaves the system
in an unexamined drift state.

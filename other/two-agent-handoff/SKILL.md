---
name: two-agent-handoff
description: Use when TWO AI agent surfaces with different capabilities collaborate on one project — a repo-access coding agent paired with a research/data-authoring agent that has no repo access, or any asymmetric pair — and their work must hand off cleanly without silent overwrites or lost context. Carries the single-handoff-file protocol, directional outboxes, exclusive-ownership lists, provenance-cited deliveries, and the audit-each-other pattern. Triggers on two agents, handoff file, outbox, Cowork, agent collaboration, second AI surface, "the other instance", agent-to-agent handoff.
---

# Two-Agent Handoff Protocol

How two AI agent surfaces with asymmetric capabilities collaborate on one
project through a single markdown file. Distilled from BOBA Playbook's
Claude Code ↔ Cowork protocol (~1,660 lines of real handoffs over three
months): one agent had repo + build access, the other had research and
data-authoring strengths but no repo. The file made the pair compound
instead of collide.

## When this applies — and when it doesn't

**Use it** when the two agents have a genuine capability asymmetry: one
can edit code and run builds, the other can do deep research, author
data, or reach systems the first can't. The asymmetry is what makes the
boundary drawable.

**Don't use it** when:
- One agent could do both jobs — the file is pure overhead; just use one
  agent.
- More than two agents are involved — a markdown file doesn't scale past
  a pair; you need real coordination infrastructure (queues, locks, a
  task system).

## The one rule

**One versioned markdown file at the repo root IS the entire channel.**
(`COWORK.md`, `HANDOFF.md` — the name doesn't matter; the singularity
does.) No side channels: no separate notes files, no "I'll tell the
human to tell the other agent," no state that lives only in one agent's
memory. If it isn't in the file, the other side doesn't know it.

## The four protocol rules

State these verbatim at the top of the handoff file:

1. **Before the human switches instances, the outgoing instance updates
   its own outbox.**
2. **The incoming instance reads the OTHER side's outbox before doing
   anything else.**
3. **After acting on an item, move it to the completed log with a
   completion note.**
4. **Keep outboxes short — one actionable item per bullet.** Detail goes
   in the item's body, not in more bullets.

## File anatomy

```markdown
# Handoff — Agent A (code/repo) ↔ Agent B (research/data)

<the four rules>

## 📤 A → B   (things A needs B to produce)
### [2026-04-22] <title>            ← dated heading
...item body...

## 📥 B → A   (things B has produced that need integrating)
### [2026-04-25] <title> ✅ DONE    ← status appended on resolution
...

## 🗂 Shared Context                 ← the invariants both sides obey
## ✅ Completed log                  ← newest-first, one line each
```

**Directional outboxes, not a shared inbox.** `📤 A → B` holds what A
needs B to produce; `📥 B → A` holds what B has produced that A must
integrate. Ownership of every item is structural — visible from which
section it sits in — never implied by wording.

**Every entry is dated and status-marked in its heading** (`✅ DONE` /
`❌ DEFERRED` appended on resolution). The completed log is newest-first,
one line per item: `[date] [direction] description — what was done`.

**Mark premature completions honestly.** A real entry read
`❌ DEFERRED (was marked DONE prematurely)`. The log's entire value
depends on it being trustworthy about its own failures — an agent that
silently re-marks its mistakes teaches the other side to re-verify
everything, which defeats the file.

## Shared Context — the invariants section

The `🗂 Shared Context` section is where the cost of a two-agent setup is
actually paid down. It carries what both sides MUST agree on:

- Canonical data locations (the master file, the derived bundles)
- The regeneration command that rebuilds derived artifacts
- The field-by-field schema, with per-field notes and cross-references
  to the decision log
- The project's core mantra / invariants (e.g. "one ID per entity")

**Shared derived identifiers live in ONE helper, mirrored on both sides,
co-changed in the same commit if the formula ever changes** — state the
co-change rule explicitly in this section (see `canonical-entity-identity`
for why the formula must never be redefined inline).

## The exclusive-ownership lists

**Two explicit "should NOT change" lists — one per side — naming the
files and directories each instance owns exclusively.** This is the
single highest-value section in the file: it prevents the merge
conflicts and silent overwrites that otherwise make two-agent work
net-negative. If a session needs to touch the other side's domain, that
becomes a handoff request, not an edit.

Note in deliveries when a session deliberately did NOT touch the other
side's domain and why ("schema is the other instance's ownership") —
restraint is information.

## What a handoff REQUEST carries

Never just "please add field X." A request the other side can execute
without a round-trip carries:

- **Background** — why this is needed now
- **The problem being solved** — including why the current approach fails
- **The concrete formula / schema** — exact, not described
- **Worked examples including the edge cases** (e.g. a null field
  producing a legitimate trailing delimiter)
- **A code sketch** of the requested change
- **A backward-compatibility fallback** — prefer the new key, fall back
  to the old logic for existing rows

## What a handoff DELIVERY carries

- A folder + a patch file + a report — not prose alone.
- **Every authored value cites its provenance.** Split rows into
  recovered-from-source vs authored-from-analog; each authored row names
  the analog(s) used, the adjustment applied, and a confidence label
  (`EXACT_ANALOG` / `CLOSE_ANALOG` / `ADJUSTED_ANALOG` / `AUTHORED`).
- **An ordered integration plan** for the receiving agent (numbered
  steps), plus **numbered open questions for the human** — decisions
  only the owner can make, separated from decisions the agents made.

**Completion notes append to the original entry**, never elsewhere:
what was decided on each open question, including deferrals, and any
reusable tooling that came out of it.

## The audit pattern — the non-repo agent's highest-value output

The second agent's best deliverable is often an **audit of the first
agent's work**, not new data. Real example: the research agent reviewed
the repo agent's integration script, found its lookup keyed on an exact
string and therefore missed 3 records with normalization variants (a
capitalization typo, a mis-tagged row, a missing apostrophe), and
delivered BOTH a recommended fix (an alias map with lowercase +
punctuation stripping) AND a fallback — "if the fix isn't worth it, here
are the three rows pre-merged so they land in the same place." An audit
that ships its own remediation is never blocked on the other side's
priorities.

## Tooling accumulates through the log

When a one-off integration script gets used twice, generalize it (add
the `--source X` flag) and **note the supersession in the handoff log**
("the new generic batch-apply script supersedes the one-off"). That note
is how the pair accumulates shared tooling instead of parallel one-offs.

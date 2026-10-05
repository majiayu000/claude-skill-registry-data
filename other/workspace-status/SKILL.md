---
name: workspace-status
description: Use this skill to orient at session start, check initiative queue state, or see what's ready to work on next. Reads workspace.toml and surfaces ready-to-start items, blocked items with reason, parallel candidates, and active signals. Triggers on "workspace status", "where am I", "orient me", "session start", "what's ready", "show the queue", "what's next", "what should I work on", "check workspace", or any cold-start orientation request. Offers to initialise workspace.toml if absent.
---

# Skill: workspace-status

Read the local `workspace.toml` and surface the current queue state across all active initiatives. Run this at every session start — it replaces reading multiple product docs by hand.

## Output rendering

Status list — Lead each row with a status glyph — ● running, ✓ done, ○ idle, ⚠ blocked — status first, one item per line, labels aligned.
Table — When presenting several items that share the same fields, render a Markdown table. Cap at ~5 columns; beyond that, switch to a per-item detail list. Right-align numeric columns.
Diagram / flow — For relationships or flow, emit a fenced ```mermaid block (it renders in chat and artifacts). If the surface is terminal-only, fall back to an ASCII box-and-arrow sketch.
Progress — Report progress inline as done/total (e.g. 3/8). Only draw a bar if you're animating in a terminal.

## When to invoke

Any time you need to orient: which initiative is active, what specs are ready to start, what is blocked and why, what signals the strategist has flagged. Also the right skill if workspace.toml does not yet exist and you want to initialise it.

## Procedure

### 1. Read workspace.toml

Open `workspace.toml` from the repo root. Parse it as TOML (`tomllib.loads()` in Python 3.11+ / `tomli.loads()` backport for earlier).

**If absent:** offer to initialise — ask the user whether to create a blank file or bootstrap with their first initiative. A blank file emits the full schema-documented template:

```toml
# workspace.toml
#
# Declared-intent coordination artifact for this repo.
# Each initiative gets its own named section. Run `workspace-status` to surface
# ready items, blocked items, and active signals.
#
# Queue entries are strings (no deps) or inline objects {path/slug, needs}
# (with dependencies). `needs` uses queue-prefix notation:
#   "work:<path>"      — depends on a work queue entry
#   "shape:<slug>"     — depends on a shaping queue entry
#   "research:<slug>"  — depends on a research entry
#   "brief:<path>"     — depends on a brief queue entry
#   "backlog:<slug>"   — depends on a repo-level [backlog] item
# Cross-initiative deps prefix the initiative slug: "ini-002:work:spec/..."
#
# shaping_queue entry types: shape | research | strategy | signal | design
#   shape    → frame-intent (or frame-situation when PE pack is available)
#   research → desk-research-project-start (requires desk-research pack)
#   strategy → frame-situation (PE pack — M2); interim: frame-intent
#   signal   → no action; surfaces in "active context" section only
#   design   → experience-status (requires experience-design pack); fallback: journey-mapping
#
# The top-level [backlog] section (repo-durable open work not scoped to any
# active initiative) is distinct from a shaping_queue's `backlog` array.

["<initiative-slug>"]
name      = "<Initiative Name>"
status    = "active"      # active | paused | closed
milestone = "<milestone>"

["<initiative-slug>".work]
queue   = []  # ordered list of spec paths to build; earliest-first
active  = []  # currently in-progress
shipped = []  # completed

["<initiative-slug>".shaping_queue]
active  = []
backlog = []

[backlog]
open = []
```

**If present and unparseable:** surface the TOML parse error and stop — do not proceed with partial data.

### 2. Resolve the DAG

For each initiative's `[work]` and `[shaping_queue]`:

- A queue entry is **ready** when all its `needs` entries are satisfied (see below).
- A queue entry is **blocked** when one or more `needs` entries are not yet satisfied.
- An entry with no `needs` field is unconditionally ready (unless already in `active` or `shipped`).

**Needs resolution:**

`needs` is a string or list of strings using queue-prefix notation:

| Prefix | Resolves against |
|--------|-----------------|
| `work:<path>` | `[work].shipped` (or `[work].active` counts as in-progress) |
| `shape:<slug>` | `[shaping_queue].active` or treated as shipped if not present |
| `research:<slug>` | `[shaping_queue]` entries of `type = "research"` — ready when that entry is not in the backlog |
| `brief:<path>` | `[brief_queue].ready` or `executing` |
| `<ini-slug>:work:<path>` | Cross-initiative: `["<ini-slug>".work].shipped` |

An entry is satisfied when its referenced item is in the appropriate shipped/done list. When `needs` is a list, ALL entries must be satisfied.

### 2a. Reconciliation — surface spec ↔ workspace.toml inconsistencies

Run three passes across `docs/specs/*/spec.md` and all initiative lists before
producing any output. Collect all findings first.

**Path resolution (all three passes):**

- Bare-string entry `"spec/foo"` → path = the string.
- Inline-object entry `{path = "spec/foo", needs = "..."}` → path = the `path` field.
- Shipped entries are always bare strings.
- From any path: strip the `spec/` prefix → slug; resolve `docs/specs/<slug>/spec.md`.
- Status extraction: read the first line in the file matching `- **Status:**` and
  extract the Status vocabulary word. When the line contains `→` (transition form,
  e.g. `Approved → Shipped`), split on `→` and take the first word of the last
  segment (stop at whitespace or `<!--`) — the right-hand token is the current
  status. Otherwise take the first word after `**Status:** ` (stop at whitespace
  or `<!--`). If no such line exists, treat as unknown status and skip this path
  in all passes.

**Forward scan — untracked live specs:**

Walk every directory under `docs/specs/` that contains a `spec.md`. For each:
1. Extract Status. Skip if not `Approved` or `Implementing`.
2. Derive the canonical path: `spec/<dirname>`.
3. Check whether this path appears in any initiative's queue, active, or shipped
   list across all initiatives. If absent from all three → **Type 1** finding.

**Backward scan — stale queue/active entries:**

For each initiative, for each path in `[work].queue` and `[work].active`:
1. Resolve `docs/specs/<slug>/spec.md`. If absent, skip without warning.
2. Extract Status. If `Shipped` or `Archived` → **Type 2** finding. Record the
   path, the list name (queue or active), and the initiative slug.

**Shipped scan — prematurely-shipped entries:**

For each initiative, for each path in `[work].shipped`:
1. Resolve `docs/specs/<slug>/spec.md`. If absent, skip without warning.
2. Extract Status. If `Approved` or `Implementing` → **Type 3** finding. Record
   the path and the initiative slug.

**Reconciliation block:**

Let N = total count across all three types. When N = 0, omit the block entirely.
When N > 0, output the following block **before** Step 3; omit subsections with no
entries; name the initiative for each stale/shipped entry (e.g. `[ini-002 work]`):

```
**Reconciliation** — N inconsistenc(y/ies) detected:

  Untracked live specs (Approved or Implementing, not in any initiative list):
  - `spec/<slug>` (Status: Approved) — add to [work].queue or run capture-work

  Stale queue/active entries (spec shows Shipped or Archived):
  - `spec/<slug>` in [ini-002 work].queue — Status: Shipped
  - `spec/<slug>` in [ini-002 work].active — Status: Archived

  Prematurely-shipped entries ([work].shipped, spec shows live status):
  - `spec/<slug>` in [ini-002 work].shipped — Status: Implementing
    Possible causes: (1) spec Status was not updated after shipping, or
    (2) the workspace.toml entry was moved before the work was done.
```

When Type 2 findings exist, build the cleanup offer. For any Type 2 entry found in
`[work].active`, ask first: "Is `<path>` actively being worked on in this session?"
— include it in the offer only after the user confirms it is not active. Then append:

```
Stale entries found — clean up now?
  Shipped entries move to [work].shipped (bare string, `needs` dropped).
  Archived entries are removed from [work].queue or [work].active.
  Reply Y to apply, or edit workspace.toml manually.
```

**Cleanup write — after Y confirmation (Type 2 only):**

For each Type 2 finding in the confirmed offer:
- **Shipped, in queue/active**: remove from queue/active; append `"spec/<slug>"` as
  a bare string to the same initiative's `[work].shipped` (skip if already present).
- **Archived, in queue/active**: remove from queue/active; add nothing to shipped.

Use a comment-preserving write — targeted text insertion or `tomlkit`; never a
`tomllib` + `tomli_w` round-trip (strips comments).

### 3. Surface results

If the Reconciliation block from Step 2a is non-empty (N > 0), it has already been
output first. Continue with the following sections.

Format output in four sections (omit sections with no entries):

---

**Active initiatives:** `<ini-slug>` — `<name>` (milestone: `<milestone>`)

**Active context — signals** _(ongoing; do not need action):_
- `<slug>` (`signal`) — no action needed; informs shaping decisions

**Ready to start:**
- `[build]` `<path>` — run `work-loop` on `docs/specs/<path>/`
- `[shape]` `<slug>` (`shape`) — run `frame-intent`
- `[shape]` `<slug>` (`research`) — run `desk-research-project-start`
- `[shape]` `<slug>` (`strategy`) — route through `frame-situation` (PE pack — M2); if not yet available, run `frame-intent` as interim
- `[shape]` `<slug>` (`design`) — run `experience-status` (requires experience-design pack); fallback: `journey-mapping`
- `[brief]` `<path>` (Ready) — run `receive-brief` on `docs/product/briefs/<path>.md`

**Parallel candidates:** _(all of the above with no inter-dependencies can start concurrently)_

**Blocked:**
- `<path>` — waiting on `<needs-entry>` (status: `<queued|in-progress>`)

**Brief queue:**
- Executing: `<path>` (or "none")
- Ready: `<count>` item(s)
- Draft: `<count>` item(s)

**Closeout check:** if `[work].queue` is empty and `[work].active` is empty and `[work].shipped` is non-empty → surface: "`<ini-slug>`: all specs shipped — ready to close out? Run closeout to remove this section (git history preserves the record)."

**Findings:** Read `docs/product/findings/rfc-candidates.md` and `docs/product/findings/roadmap-intents.md` if they exist. Count non-header rows in each (a non-header row is any `|…|` line after the header separator row — the `|---|...|` line of dashes).

- **When either file has data rows:** output a `**Findings:**` section with both tables printed inline — paste each file's full markdown table (column header row + separator + data rows) under a sub-label (`RFC candidates:` / `Roadmap intents:`). If one file is absent or has no data rows, output its sub-label followed by `_(empty)_`.
- **When both are empty or absent:** emit a single line: `0 rfc candidates · 0 roadmap intents — both registers empty`

**Backlog:** when `[backlog].open` in `workspace.toml` is non-empty, render:

```
**Backlog** — N open item(s):
- `[shape]` `<slug>` — <first # comment line above the entry>
- `[build]` `<slug>` — <first # comment line above the entry>
  ...
```

Each entry is prefixed with its room: `[shape]` when the entry carries a `type` field (shaping work); `[build]` when it does not (build work). To extract the first comment line: read `workspace.toml` as text; for each entry in `[backlog].open`, find the nearest `# ` comment line immediately preceding `{slug = "<slug>"}`. Use the comment text (without the leading `# `) as the item's summary. If no comment line is present, omit the summary and render just the slug. Omit this section entirely when `[backlog].open` is empty or absent.

---

### 4. Skill prompts by type

When surfacing shaping_queue entries, append the right skill invocation based on what's installed:

| Entry type | Skill to suggest |
|-----------|-----------------|
| `shape` (default) | `frame-intent` (available now); `frame-situation` (M2, when available) |
| `research` | `desk-research-project-start` (requires desk-research pack) |
| `strategy` | route through `frame-situation` (PE pack — M2); if not yet available, run `frame-intent` as interim |
| `signal` | no action — surface in "active context" section only |
| `design` | `experience-status` (requires experience-design pack); if experience-design is not installed: `journey-mapping` |

If the required pack is not installed, surface: "requires `<pack-name>` pack — install to work this item."

### 5. Missing fields

`workspace.toml` evolves: older entries may lack a `type` field (treat as `shape`), a `milestone` field (omit from output), or a `parent` field (omit). Never fail on missing optional fields.

### 6. Next-actions

Using Step 2 DAG state only — do not re-read `workspace.toml`:

**6a. Resolve choices**

From the state already computed in Step 2:

- `active_spec` = first entry in `[work].active` (if any)
- `next_queue` = first entry in `[work].queue` whose `needs` are all satisfied (queue order); if an entry is an inline object, use its `path` field
- `unblocked` = all entries in `[work].queue` whose `needs` are all satisfied
- `next_shape` = first entry in `[shaping_queue].active` whose `type` is not `signal` (if any); else first entry in `[shaping_queue]` that is ready (unblocked, not in `active` or `shipped`) and whose `type` is not `signal`

**Path resolution:** workspace.toml paths carry a `spec/` prefix (e.g. `"spec/m1-workspace-core"`). Strip it before building file-system paths — the slug is the part after `spec/`, and the command uses `docs/specs/<slug>/`.

**6b. ASCII dependency graph (when ≥2 unblocked work items)**

If `len(unblocked) ≥ 2`, render the following block _before_ the numbered choices:

```
Work queue — parallel opportunities:

  <slug-A>  [ready]
  <slug-B>  [ready]
  <slug-C>  [blocked by <dep-slug>]
```

- Right-pad the slug column to the longest slug for alignment. Use the bare path (with `spec/` prefix preserved) for both `[ready]` and `[blocked by]` rows — e.g. `spec/alpha [ready]` and `spec/gamma [blocked by spec/alpha]`.
- Unblocked entries: annotate `[ready]`.
- Blocked entries: annotate `[blocked by <dep-slug>]`, where `<dep-slug>` is the path with the queue-prefix domain stripped (e.g. `needs = "work:spec/alpha"` → `spec/alpha`).

**6c. Harness detection and parallel-session offer (when graph rendered)**

When the graph was rendered, offer a parallel-session choice as the **first** numbered slot. Check whether `--bg` appears in `claude --help` output (via the Bash tool if available):

- **`--bg` found:** emit a numbered choice listing `claude --bg "work-loop docs/specs/<slug>/"` for each parallel-ready root node.
- **`--bg` absent or Bash tool unavailable:** emit a numbered choice with prose instructions for each parallel-ready root node (no automated spawn).

**6d. Numbered choices**

Emit the following choices in order. Omit any whose source is empty; renumber sequentially. The parallel-session offer from 6c (when present) occupies the first slot and the remaining choices follow.

- **Active spec:** `work-loop docs/specs/<slug>/` — continue active spec. Present when `active_spec` is non-empty.
- **Next queue item:** `work-loop docs/specs/<slug>/` — next unblocked queue item. Present when `next_queue` is non-empty.
- **First shaping item:** skill command per Step 4 routing table for the entry's type. Present when `next_shape` is non-empty. If the required pack is not installed, emit `requires \`<pack-name>\` pack — install to work this item` instead of the skill command.
- **Start new work (always — final choice):** `new-spec` · `new-rfc` · `new-adr` · `capture-work`

## See also

- `references/agentbundle-layout.md` — the `[product]` table: configurable `projects/` and `shaping/` paths used by product-facing skills

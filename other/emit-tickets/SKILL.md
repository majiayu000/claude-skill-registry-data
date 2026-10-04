---
model_tier: high
name: emit-tickets
description: "Use when materialising a roadmap into a ticket bundle — 'turn this roadmap into tickets', 'materialise tickets', 'mach Tickets aus der Roadmap', 'emit tickets for this plan'."
domain: process
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# emit-tickets

Materialise a roadmap into an `agents/tickets/{slug}/` bundle — one ticket per
buildable step — then wire the markers back and run the buildability gate.

## When to use

| Signal | Match |
|---|---|
| "turn this roadmap into tickets" | yes |
| "materialise / emit tickets for \<roadmap\>" | yes |
| "mach Tickets aus der Roadmap" | yes |
| "plan the work for \<roadmap\>" | yes |
| User wants a YAML ticket bundle, not a prose plan | yes |
| Refining or splitting an existing ticket | no → use `refine-ticket` |
| Estimating a single ticket | no → use `estimate-ticket` |

**Upstream:** `roadmap-writing` — author the roadmap first.
**Downstream:** `src/scripts/lint_ticket_buildable.ts` (the build-readiness gate). A ticket reaches a tracker by paste or MCP (ADR-102) — no export script.

## Procedure

Steps at a glance:

1. Locate and parse the roadmap.
2. Create `agents/tickets/{slug}/` and draft one ticket YAML per materializable step.
3. Assign `model_tier` via the granularity floor; split oversized steps.
4. Compute SHA refs for `adr_refs` / `source_refs`.
5. Write `manifest.yml` with acyclic `dependency_graph` and empty `linear_state`.
6. Append `<!-- ticket: T-NNN -->` markers back into the roadmap.
7. (Re)generate `agents/tickets/_registry.yml`.
8. Run `lint_ticket_buildable` until exit 0 (max 3 attempts).
9. Tell the user the bundle is ready: paste a ticket into Linear/Jira, or have the agent create it via a tracker MCP server (ADR-102 — no API export).

### §0 — Locate the roadmap

Confirm the roadmap slug and open `agents/roadmaps/{slug}.md`. Identify all
materializable steps (checkbox items that describe a code or docs change). Skip
informational steps, phase headings, and acceptance-criteria prose.

### §1 — Derive the bundle slug

`agents/tickets/{slug}/` — same slug as the roadmap. Create the directory.

### §2 — One ticket per step

For each materializable step, draft a ticket YAML:

~~~yaml
id: T-NNN
roadmap: {slug}
phase: {N}
title: "{step text, ≤80 chars}"
status: ready
model_tier: {lite | medium | high}   # see §3
estimate: {story-points, integer}
priority: {1=critical … 4=low}
labels: []
parent: null
blocked_by: []
adr_refs: []
source_refs: []
assets: none
acceptance:
  - "{measurable done criterion}"
boundaries:
  must_touch: []
  may_touch: []
  must_not_touch: []
~~~

Use `estimate-ticket`, `technical-specification`, or `refine-ticket` when a
step needs deep estimation or spec work.

### §3 — Assign model_tier by granularity floor

Apply this floor **before** marking any ticket `lite`:

| Criterion | Required for `lite` |
|---|---|
| Files touched | ≤ 5 |
| Lines changed | ≤ 200 |
| Isolation-testable | yes — no cross-module side effects |

- All three pass → `lite`
- Any miss → split the ticket further, or escalate to `medium`
- Architectural / multi-module → `high` (use `adr-create` first)

**Gate:** run `./scripts-run src/scripts/lint_ticket_buildable.ts agents/tickets/{slug}/`
and fix all errors before declaring any ticket `lite`. This is the only
authoritative check — do not skip it.

### §4 — Compute SHA refs

For each `adr_refs` and `source_refs` entry:

```bash
git rev-parse HEAD:path/to/file
```

Fill the `sha:` field with the result, or `pending` for files not yet committed.

### §5 — Write manifest.yml

~~~yaml
bundle: {slug}
generated: {ISO-8601 date}
dependency_graph:
  T-001: []
  T-002: [T-001]
  # … acyclic; no circular deps
linear_state: {}   # always empty at emit time
~~~

Verify acyclicity by tracing every `blocked_by` chain — no ticket may appear
in its own transitive dependency set.

### §6 — Write markers back into the roadmap

For each materializable step in `agents/roadmaps/{slug}.md`, append
`<!-- ticket: T-NNN -->` to the end of the step line:

```
- [ ] Add X to Y  <!-- ticket: T-003 -->
```

One marker per step; do not duplicate on re-run (check before appending).

### §7 — (Re)generate _registry.yml

Append or update the bundle entry in `agents/tickets/_registry.yml`:

~~~yaml
bundles:
  - slug: {slug}
    path: agents/tickets/{slug}/
    status: draft
    ticket_count: {N}
~~~

If the file does not exist, create it with the `bundles:` root.

### §8 — Run the buildability gate

```bash
./scripts-run src/scripts/lint_ticket_buildable.ts agents/tickets/{slug}/
```

Fix every reported error. Re-run until exit code 0. Max 3 attempts; if still
failing, surface the linter output and ask for guidance.

### §9 — Hand off (paste / MCP)

Tell the user:

> Bundle written to `agents/tickets/{slug}/`. Each ticket's body is
> paste-ready Markdown for a Linear/Jira issue; or create issues via a
> tracker MCP server. No API export (ADR-102).

Do NOT auto-create tracker issues — paste/MCP is the user's call.

## Output format

1. `agents/tickets/{slug}/manifest.yml` — bundle manifest (acyclic graph, empty linear_state)
2. `agents/tickets/{slug}/T-NNN-{slug}.md` — one file per ticket (YAML frontmatter)
3. `agents/tickets/_registry.yml` — updated bundle registry
4. Inline `<!-- ticket: T-NNN -->` markers in the source roadmap

## Do NOT

- Implement or invent ticket content not traceable to a roadmap step.
- Touch `src/scripts/**` — orchestrate; do not reimplement.
- Mark a ticket `lite` before `lint_ticket_buildable` passes.
- Create a circular `dependency_graph` — verify acyclicity before writing.
- Auto-create tracker issues — paste/MCP is the user's call (ADR-102, no API export).
- Reuse T-NNN numbers from another bundle in the same registry.

## Gotchas

- **Re-run safety:** before appending `<!-- ticket: T-NNN -->` markers, grep
  for existing markers so a re-run does not duplicate them.
- **SHA = pending:** new files not yet committed get `sha: pending`; remind
  the user to re-run after commit to update SHAs.
- **Split signals:** if a step touches > 5 files or > 200 lines, split it
  into two tickets and add a `blocked_by` dependency before continuing.
- **Format contract:** `docs/contracts/ticket-bundle-format.md` is the
  authoritative schema; `src/agent-src/templates/tickets.md` is the template.

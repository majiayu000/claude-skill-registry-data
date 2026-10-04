---
name: research-dashboard
description: "Use when building, serving, repairing, or validating the read-only .research/interface projection."
---

# Research Dashboard

Build and serve the human research interface without turning HTML into a second
state store. The interface is a disposable projection of the managed research
root. It must remain useful to people while staying irrelevant to agent
authority.

Read [references/dashboard-contract.md](references/dashboard-contract.md)
before changing the projection or its tests.

## Boundary

Resolve one `ResearchPaths` instance from:

1. `--research-root`, when supplied.
2. `RESEARCH_ROOT`, when set.
3. `<workspace>/.research`, otherwise.

The managed root has four distinct responsibilities:

```text
.research/
├── VERSION
├── state/          # authoritative management state and content-addressed notes
├── audit/          # authoritative command audit
├── experiments/    # durable experiment runs and outputs
└── interface/      # generated, read-only human projection
```

Treat `.research/state/` and `.research/experiments/` as inputs.
Treat `.research/interface/` as output. Agents must never recover facts from the
interface, edit it as state, or place experiment outputs inside it. Deleting the
entire interface must be safe because a build can recreate it from authority.

The projection contains HTML, CSS, JavaScript, and generated data files. It
must not contain Python files or a `scripts/` directory.

## Build

From the pipeline checkout, rebuild an existing versioned store:

```bash
python3 skills/research-dashboard/scripts/ensure_dashboard.py \
  --workspace . \
  build
```

Pass `--research-root <path>` when the managed root is not
`<workspace>/.research`. The command prints the interface root, source event
sequence, source hash, file count, and every generated file.

The builder creates the complete projection in a staging directory and swaps it
into place. A rebuild therefore repairs missing files and removes stale files.
Do not patch generated files to repair drift. Rebuild them.

`build` never initializes managed state. A missing, legacy, unversioned, or
unsupported root must stop with a handoff to `research-init`.

## Serve

The server document root is exactly `.research/interface`. It adds only
read-only health and live-run endpoints:

- `/api/health`
- `/api/live/runs`
- `/api/live/status/<run-id>`
- `/api/live/log/<run-id>`

Run a foreground server when the process should remain attached:

```bash
python3 -m lib.interface.serve \
  --workspace . \
  serve \
  --host 127.0.0.1 \
  --port 8904
```

Build and start a background server, or reuse a healthy one:

```bash
python3 -m lib.interface.serve \
  --workspace . \
  ensure \
  --host 127.0.0.1 \
  --port 8904 \
  --json
```

Check the recorded server:

```bash
python3 -m lib.interface.serve \
  --workspace . \
  status \
  --json
```

Stop only the healthy server recorded for this workspace:

```bash
python3 -m lib.interface.serve \
  --workspace . \
  stop \
  --json
```

`ensure` and `serve` require a versioned root. They compare the cheap projection
marker with transactional state and rebuild only when the interface is absent
or stale. While the server is running, the next static-page request performs
the same check, so multiple management commits produce at most one rebuild
before the page is served.

Server PID metadata and logs are volatile runtime state. They live below
`$XDG_RUNTIME_DIR/trustworthy-research/<workspace-hash>/` when
`XDG_RUNTIME_DIR` is set, or below the per-user temporary fallback otherwise.
They must not be written into `.research/interface`.

For a remote workspace, keep the server bound to loopback and forward it:

```bash
ssh -L 8904:127.0.0.1:8904 <host>
```

Then open `http://127.0.0.1:8904/index.html`.

## Human interface contract

Keep the current human layout and navigation:

- Global pages remain `index.html`, `live.html`, and `learnings.html`.
- The four category pages remain separate pages.
- A Draft Package appears in `RESEARCH_PACKAGES` with category `brainstorm` and
  uses the same package-card component as every other lane.
- Its `detailPath` is `packages/<id>/docs/proposal.html`, a full document
  assembled from `templates/brainstorm-document.html`,
  `assets/brainstorm.css`, and the state-backed `document_note` fragment.
- Activation keeps the same route and NoteRef. The renderer changes only the
  presentation from non-executable draft to Package-owned source context.
- A Package Overview Hero lead renders the state-backed `Package.abstract` as
  its Abstract / TLDR. Only legacy Packages without `abstract` fall back to
  `problem`; the renderer never derives this copy from Direction intent.
- The Research Intent card renders the canonical state-backed Problem,
  Motivation, Hypothesis, and Objective in that order. It neither hides
  duplicate rows nor reads optional `*Tldr` aliases; invalid intent is repaired
  through Package authority rather than in the projection.
- A Package Overview contains no Agent Content or Agent context module.
  Source package and evidence root remain visible to the user in one compact
  Source & Evidence card; duplicated identity, page indexes, and agent-only
  continuity instructions do not render in Package pages.
- The Plan page has no Package-level Plan invariants card. It renders one
  ordered Pipeline timeline whose Experiment nodes preserve status, purpose,
  dependency, output, gate, evidence, lock state, and task links while adding
  the canonical configuration reference, control mode, and reviewed Resource
  preset/profile order. Planned order is a presentation sequence; `after`
  remains the separate declared dependency. Dynamic availability and the chosen
  allocation remain Run-time facts.
- The Implementation page is one code change map grouped by Experiment. Every
  Change renders Code locations, How it changes, and Verification. Native
  disabled checkboxes are checked only for state-backed `PASS` observations;
  unchecked means pending, failed, or stale. Hypothesis restatement, Plan
  coverage, pseudo-code, test catalogs, and adjudication do not appear here.
  Beside Contract detail, each Experiment links to its state-backed
  `docs/<local-id>-design-guide.html` when that canonical NoteRef exists.
- The Results page contains only Experiment-grouped Result tables. It does not
  restate the Hypothesis, repeat the evaluation contract, or maintain a
  package-level gate ledger. The current state-backed schema pre-renders every
  planned row and column with `/` for null values. A schema row may render
  cited paper values as `REPORTED`; those cells remain distinct from local
  `MEASURED` Run values. A finalized Run may fill matching cells only after its
  comprehensive metrics EvidenceRef and CSV bytes verify. Table CRUD changes
  the current view only; it never changes a finalized Run or its verdict.
  Main tables are open; ablation tables are collapsed. Wide tables scroll
  inside their own container without widening the document. Measured values
  render only from a finalized Run whose comprehensive metrics EvidenceRef and
  source CSV verify.
- The Tracker page contains only an Experiment-grouped `To-Do` and Artifact
  locations. It derives Change tasks from the same observations as
  Implementation and Run tasks from Run evidence, keeps exactly one current
  task when tasks exist, and advances tasks within each Experiment before
  moving to the next Experiment in Plan order. It never owns editable
  checklist state and does not render latest checks, readiness, allocations,
  route selection, or agent context.
- The Docs index preserves its state-backed groups, cards, table of contents,
  metadata, links, and copy while using the shared Package visual system. Its
  table of contents has a compact clay accent; each group spans the content
  width; one document spans its group, while multiple documents use two equal
  columns. The layout becomes one column below `720px`. Doc-source pages reuse
  the same table-of-contents treatment.
- Legacy standalone Brainstorms remain readable through their historical
  routes, but new work must not create a second card type.
- Each package keeps its own plan, implementation, results, analysis, tracker,
  and docs pages.
- Each Package page uses the shared first-view status strip: Current State,
  Current Process, Last Transition, and ordered
  `IF transition condition → next state` pairs. Current Process describes only
  the work owned by the current phase; it must never be derived from the
  future-facing `nextAction`. Blockers are shown inside Current State without
  replacing the canonical phase. Next-state rows come from the central phase
  graph and remain neutral until a verified transition occurs. Gates and
  measurements remain in ExperimentSpecs, Plan, and Results rather than the universal
  status strip.
- Every user-facing Package page uses the same compact masthead structure,
  `Research Package` eyebrow, single Dashboard action, status strip, and
  Package navigation. Only the page title and head abstract vary by page.
- The Package Overview keeps identity compact enough for the complete status
  strip to remain in the first viewport. Current State has the strongest
  emphasis; Current Process and Last Transition are supporting context; legal
  next-state branches have equal, neutral weight until a transition occurs.
- `module.html` remains available. Preserve the existing
  `module.html?package=<id>&module=<name>` route.
- `live.html` keeps its own API poller. Other pages may use
  `assets/live-data.js` to refresh projected data in place.

Do not consolidate these pages into a single-page application. Do not remove
the module route. Do not redesign the UI as part of a storage or authority
change.

Legacy Brainstorm `detail_note` remains a compatibility override for migrated
self-contained pages. Draft Packages use `document_note`; do not copy the
outer page, navigation, ToC, scripts, or CSS into that fragment.

The DOM hierarchy, contract-bearing attributes, CSS bytes, viewport, browser
major, and screenshot baselines are frozen by
`assets/interface-contract.json`. State-source paths and narrowly necessary
serve guidance may change, but IDs, classes, navigation, page layout, and
visual styling require explicit user approval.

## Validation

After a dashboard change:

```bash
python3 skills/research-dashboard/scripts/ensure_dashboard.py \
  --workspace . \
  build
python3 -m lib.interface.parity check
```

Use `python3 -m lib.interface.parity check --no-visual` only as a fast
intermediate DOM and CSS check. Final interface validation includes the visual
pages and their bounded perceptual hash comparison.

Also verify:

1. `.research/interface` contains no `scripts/` directory or Python files.
2. All global, category, module, and package URLs load from the interface root.
3. `/api/*` endpoints remain read-only.
4. Rebuilding after deleting `.research/interface` recreates the same human
   surface from state and experiment authority.
5. Server metadata and logs remain outside the managed projection.

The dashboard can show that Project intent is absent, but it does not define or
ratify it. Check that boundary through the onboarding query:

```bash
python3 skills/research-onboard/scripts/onboard.py \
  --workspace . \
  has-project
```

If managed state is absent, hand off to `research-init`. If no Project exists
in a valid setup, hand the next decision to `research-onboard`. Do not invent
Project, Direction, or Experiment intent in dashboard data.

## Report

Report the resolved research root, generated interface root, source sequence and
hash, server URL and stop command when started, parity result, and whether a
committed Project exists. If setup is missing or invalid, report the
`research-init` handoff and that no initialization or overwrite was attempted.

---
name: "Web: Conventions"
description: "Shared ground for the web-* family: how every design task starts, what it produces, where each product goes and how an artefact is shelved for reuse"
when_to_use: "Loaded by every web-* skill before it collates, draws, records or captures anything; also when an interface review or a new interface is being discussed and no web-* skill has been named yet."
user-invocable: false
metadata:
  family: web
  goblin-spinner: taking inventory|naming the gaps|minding the principles
allowed-tools: ["Read", "Glob", "Grep", "Bash", "AskUserQuestion"]
---

# Web design conventions

Shared ground for `web-review`, `web-design`, `web-walkthrough` and `web-check`. The eleven principles live in `principles.md` beside this file; the artefact library in `library/`; the scope template at `~/.claude/library/templates/web-scope.md`; the deterministic halves under `~/.claude/library/scripts/web/`. `artefact-conventions` and `asset-conventions` still govern where artefacts and captures go; this skill adds what is specific to designing an interface and never repeats them.

Accessibility is out of scope until after CHIRPdb's 2RT.20. The `accessibility` area in the logger is a place to record a thing noticed, not a pass.

## How every task starts

No file is mandatory, because every project is different. Every mode begins the same way.

### 1. Collate

Search for each asset kind and say where it was found or that it was not. Explicit paths in the invocation override the search.

| Asset | Where to look |
|---|---|
| Tokens and themes | `.claude/themes/` (resolution per `theme-conventions.md`); the product's own `:root` blocks in `src/**/*.css`, `app.css`, `tailwind.config.*`; the UI library in `package.json` (skeleton, shadcn, daisyui, bits-ui, melt and the like) |
| Component library | `src/lib/components/`, `src/components/`, a Storybook, a `ui/` package in a monorepo |
| Scope documents | `docs/**/*scope*.md`, `docs/specs/`, feature specs from `library/templates/feature-spec.md`, the roadmap task's own text (`roadmap.py open --json`) |
| Brand files | `docs/brand/`, `static/`, logo and wordmark files, a brand guide PDF |
| Device intent (principle 8) | The scope document, the client's brief, analytics where they exist |
| Copy brief (principle 10) | `docs/**/copy*.md`, a tone-of-voice document, the scope document's audience section |
| Prior artefacts | `docs/artefacts/` and `site/`, read as `artefact-conventions` Step 2 says |
| Routes | Per `asset-conventions` project type detection |

Print the result as one table, `Asset | Found at | Gap`, before asking anything.

### 2. Name the gaps

Every row without a find is a gap. Say which gaps block the task (device intent always does; a copy brief does whenever user-facing wording will be written) and which only narrow it.

### 3. Fill them with Jason

Rounds of 2 to 4 questions, the `roadmap:create-interview` discipline: never a long list at once, and every round ends with *"Anything else, or shall I go ahead?"*. Skip any question the found assets already answer. A gap Jason declines to fill is written down as an assumption in the scope document (design) or the artefact index (review), never silently guessed.

- [ ] Inventory table printed
- [ ] Blocking gaps named before the first question
- [ ] Every unfilled gap recorded as an assumption

## What every task produces

### Wireframes

Drawn while brainstorming, under `docs/artefacts/<task>/`, one page per proposal. Principle 6 governs the drawing:

- **The product's own tokens.** Copy the `:root` block from the product's CSS and cite the file in a mapping-notes comment. The artefact theme is for internal docs and shareables; a wireframe must look like the product it proposes. Masthead, honesty rule and technical hygiene from `artefact-conventions` still apply.
- **Numbered callouts**, each mapped to what it answers: an observation id (`#12`) in review mode, a scope requirement (`R3`) or an inventory row in design mode. A callout that answers nothing is decoration and comes out.
- **Approval before build.** The approved wireframe is the build spec; a change after approval goes back through the wireframe, not straight into code.

### Dev util artefacts

Built for the task in hand and placed in `docs/artefacts/<task>/`. Publish through the `Artifact` tool when Jason needs to use the page from a browser (a logger, a checklist, a comparison that collects input); a page that is only read stays a repo file. Start from a library entry when one fits and resolve every `ADAPT:` marker before publishing; never publish a page that still names another project.

### The observation store (principle 7)

Review mode's working surface, also used by the check and the walkthrough for anything they find.

| Field | Values |
|---|---|
| `seq` | Running integer, assigned at creation |
| `where`, `whereDetail` | A region from the inventory; an optional narrower place |
| `severity` | `blocker`, `major`, `minor`, `nit`, `praise` |
| `areas` | Any of `layout`, `copy`, `colour-type`, `interaction`, `navigation`, `feedback`, `accessibility`, `performance`, `data` |
| `title`, `detail` | First line of the note; the rest |
| `status` | `open`, `fixed`, `declined`, `waived` |
| `resolution` | One line, required for every status but `open` |
| `source` | `jason` (recorded in the page), `check` (a principles finding), `walkthrough` (a capture that failed the quality gate) |
| `principle` | The principle number, present when `source` is `check` |
| `screenshot` | Asset id in the artefact's store, optional |
| `createdAt`, `updatedAt` | ISO timestamps |

The live store is the artefact's `db` collection `observations`, read with `ArtifactData`. **At the end of every pass**, after statuses and resolutions are written back, export the whole collection to `docs/artefacts/<task>/observations.json` as `{ "exported": <iso>, "artifact": <url>, "entries": [...] }` and commit it with the pass. The repo file is the durable record; sign-off, the check and the next session read it without claude.ai. A pass that has not exported is not finished.

`declined` means the observation stands but will not be acted on, with the reason. `waived` is reserved for a principles finding Jason has chosen to let through; the resolution carries his reason.

### The principles check

Runs at three moments: after a wireframe is approved, at the end of each observation pass and at sign-off before the walkthrough. `web-check` holds the procedure; findings land in the store with `source: check`; an unwaived fail blocks sign-off. The hook on `gh pr create` refuses a branch whose latest export still holds open entries or unwaived findings.

### The sign-off walkthrough

After sign-off, `web-walkthrough` captures every route on every intended device in every open state into `docs/assets/walkthrough/`, named as below, through `asset-shot`.

## Capture naming

`<(device||viewport)?>-<route>-<specifier?>.<filetype>`

- **Device or viewport** appears only when more than one is captured: `phone`, `tablet`, `desktop` when the scope names devices; `390`, `1440` when it names widths.
- **Route** is always present: the slug of what was captured. A served app's URL path (`/` becomes `home`, `/documents/42` becomes `document`, `/invite/[secret]` becomes `invite`); the file stem for a static page or an artefact.
- **Specifier** appears only when several captures share prefix and route: the open state or scroll position (`filters-open`, `records-open`, `900`).
- Lowercase, hyphenated, no spaces.

`asset-conventions` carries the same rule for every `asset-*` skill, so a walkthrough's captures and a README's screenshots share one naming rule and keep separate directories (`docs/assets/walkthrough/` and `docs/assets/shots/`): the same route on one device gets the same name in both, so a shared directory would overwrite.

## Shelving an artefact

At the end of a review or a design, offer once: *"Shelve any of this task's artefacts in the library?"* An artefact earns a place when it proved particularly useful or is a new kind of thing. To shelve:

1. Copy the page to `library/<slug>.html` beside this skill.
2. Replace every project-specific value with a generic one and an `ADAPT:` comment saying what to put there: the title, the eyebrow, hosts and ports, routes and region names, branch and task ids, the sources list, a palette that came from the project's artefact aesthetic.
3. Grep the copy for the project's name, its hosts, its branch names and its routes. Nothing may remain.
4. Add a row to `library/README.md`: slug, what it is, which task it came from, the runtime capabilities it needs, the `ADAPT:` count.

The library holds examples, not templates: a new task reads one for its shape and builds its own.

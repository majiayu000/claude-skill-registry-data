---
name: architecture-command-center
description: >
  Architecture Command Center — an interactive 3D model of the documented architecture as one
  self-contained HTML file: layers as floors, C4 L2 containers as blocks, connections and animated
  use-case walkthroughs, a physical deployment view, findings on the stage, a load simulation, and
  Alia, the navigator who answers from the dossier (onboarding and compliance health included).
  Use for "command center", "centro de mando", "3D view", "vista 3D", "maqueta 3D", "modelo 3D",
  "physical view", "vista física", "deployment view", walking through use cases visually, or any
  spatial, navigable or animated view of the architecture — even without the word "3D". Requires
  ARCHITECTURE.md. Not for Mermaid / C4 diagrams in docs (architecture-docs Workflow 8) or IcePanel sync.
triggers:
  - command center
  - centro de mando
  - architecture command center
  - 3D view
  - vista 3D
  - maqueta 3D
  - modelo 3D
  - architecture in 3D
  - ver la arquitectura en 3D
  - interactive architecture model
  - explore the architecture in 3D
  - walk through use cases visually
  - 3D architecture viewer
  - vista física
  - physical view
  - deployment view
  - vista de despliegue
  - check compliance health
  - compliance portfolio review
  - concept gaps across contracts
  - onboard to architecture
  - new team member onboarding
---

# Architecture Command Center Skill

## Purpose

This skill turns the written architecture into a **spatial, navigable model** that a person can
orbit, pan, filter and click. It exists because two things are hard to convey in prose and flat
diagrams and easy to see in 3D:

- **Where things live** — which layer each container sits on, what is inside the ownership
  boundary and what is consumed from other systems.
- **How the data moves** — which route a use case takes, in what order, through which layers,
  and where the architecture breaks its own layering rule (a connection that skips floors is the
  most visible object in the scene, on purpose).
- **Where it runs** — the **physical view**: the same containers as instances on deployment
  nodes (region › cluster › namespace, appliances, managed services, the customer's device),
  stacked by trust-zone tier, joined by undirected paths in transport form and colored by Path
  Class. A use case projected onto it animates through the real chain — client → WAF → front
  door → firewall → gateway → cluster — and a logical connection with no declared path shows up
  as a finding instead of disappearing. One **View** switch in the viewer flips between the two;
  both are drawn by the same engine from the same scene file.

The output is one HTML file with everything inlined except the Three.js runtime, which loads
from cdnjs. It is a **presentation and exploration artifact**, not a source of truth: the
Mermaid diagrams in `docs/` and the component descriptors remain canonical, and this view is
regenerated from them. It never writes to `ARCHITECTURE.md`, `docs/`, `adr/` or
`docs/components/`.

**Distinct from** `architecture-docs` Workflow 8 (Mermaid diagrams embedded in the docs). Onboarding
and compliance portfolio questions — which contracts fall short, which requirements are Non-Compliant
or Unknown, where the gaps cluster — are Alia's: a new team member walks the model with her, and her
dossier carries every contract's requirement rows.

---

## Documentation Language

Resolve the project's documentation language **before writing anything**, using the protocol in
`skills/architecture-docs/references/LANGUAGE_POLICY.md` §3:

```bash
rg -m1 '<!-- DOC_LANGUAGE:' ARCHITECTURE.md || rg -m1 '<!-- LANGUAGE:' ARCHITECTURE.md
```

`DOC_LANGUAGE` → use it. Legacy `LANGUAGE` → use it and rewrite the marker as `DOC_LANGUAGE`.
Neither → infer from headings (§5.5), ask the user to confirm **once**, stamp `DOC_LANGUAGE` into
`ARCHITECTURE.md`, and never infer again. Messages this skill displays to the user stay English
in every case; only authored file content follows `doc_language`.

**In this skill**: the viewer chrome (tabs, buttons, legend, hints) comes from a `UI_STRINGS`
object inside `VIEWER_TEMPLATE.html`, keyed `en` / `es`; the renderer selects it with
`--lang`. Everything the scene *displays* — component notes, phase names, use-case
descriptions, edge labels, the thesis line — is authored by you in `doc_language` inside the
scene JSON. Component canonical names, ADR ids, use-case ids (`UC-01`) and node ids stay
exactly as the docs write them (`LANGUAGE_POLICY.md` §4).

---

## When to Invoke This Skill

- User asks for a 3D, spatial, interactive or animated view of the architecture
- User wants to show stakeholders how a use case moves through the layers
- User asks to "see" the layer-skipping exception, the ownership boundary, or which systems are external
- User uses `/skill architecture-command-center` (or asks for the "command center" of the system)
- A new team member needs to learn the architecture, or the user asks about compliance portfolio health or gaps across contracts — Alia answers from the dossier (run `dossier.js` after `compliance-docs/` changes)

**Do NOT invoke for:**
- Mermaid / C4 diagrams inside `docs/` → `architecture-docs` Workflow 8
- IcePanel model sync → `architecture-icepanel-sync`
- Editing any architecture content → `architecture-docs`

---

## Files in This Skill

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — entry point and workflow |
| `VIEWER_REFERENCE.md` | What the viewer does — Alia, the Simulation mode, findings on the stage, the HUD, the capabilities handed to the user, the themes. Read at Step 4 and on demand |
| `VIEWER_TEMPLATE.html` | The Three.js viewer. Data-driven: reads one `SCENE` object, lays out floors and blocks, draws routes, animates use cases. Do not edit per project. Alia's channel to the brain (`claude.use("sample")`) lights up only in a hosted copy that declares the capability; the file is otherwise self-contained |
| `scripts/dossier.js` | `bun <skill_dir>/scripts/dossier.js <project-root> <scene.json> --write` — **Alia's dossier**, seven deterministic extracts baked into `scene.dossier`: `adrs` (every ADR the scene cites: title, status, date, scope, amendment, Decision summary, consequences, related — both ADR layouts), `tdrs` (every `tdr/TDR-*.md`: status, date, affected components resolved to scene nodes through the descriptor filenames, ADRs, tags, description, impact, owner), `compliance` (the manifest rows and every requirement row per contract: code, name, status, evidence, owner), `components` (each container's descriptor: meta fields and every H2 section as paragraphs, bullets and tables), `integrations` (the `I-nn` inventory of `docs/05`, endpoints resolved to nodes), `findings` (every report in `analysis/`, read through `architecture-analysis/scripts/findings.js` — the contract the analysis skill's `check-report.js` enforces on every report it writes, so what the check accepts is what Alia reads: each Markdown table whose first column is `#` / `ID` and whose rows open with a finding id in the analysis skill's grammar — `C1`, `B1 ⚡`, `K2-01`, `T1-S`, `TB-01`, `T1-01`, `OB-01` … — or the HTML report's embedded data; id, label — the first naming column (component, technology, data store, threat …), never a Tier or Flow cell — every column, the containers or deployment nodes the row names, the scene edges it is about (`edges`, from the `I-nn` ids it cites through the `docs/05` inventory and from the `X → Y` pairs it writes) with their integration ids (`ints`), and a severity read from an explicit `Severity` / `Risk` column, else the `Tier` column, else the id's prefix through the registry in `architecture-analysis/SKILL.md` § Finding IDs, else the section title; a finding listed twice is one entry), `sections` (every `docs/NN-*.md`: title, the `EXPLORER_HEADER` fields with the named components resolved to scene nodes, the 30-second summary blockquote, an outline of H2 / H3 headings with each H2's first paragraph, the byte size — the page Alia opens for a section, the same rows the explorer manifest lists). Reports every reference without a file |
| `scripts/scene-from-docs.js` | `bun <skill_dir>/scripts/scene-from-docs.js <project-root> [--base <scene.json> \| --no-base] [--overrides <json>] [--out <scene.json>] [--capacity-check]` — writes `visualizations/architecture-command-center.scene.json` with the previous scene as base unless told otherwise, and retires the dated pairs of earlier versions — **the logical scene, generated from the documents** (8.5.0): systems and containers from `component-cli`'s facts and the external descriptors' `## Containers` tables, layers from `docs/03` § 4.1, edges from `docs/05` `I-nn` rows and every descriptor's `## Communication` table, phases from the `docs/04` Phase Catalog walked over the edge graph, use cases from the Flow Inventory and the flow blocks. `--base` keeps node ids, positions, thesis, phase kinds and the `deployment` block of the previous scene; `--overrides` is the architect's word, merged last. The report on stderr names every actor created, every edge synthesized for a hop the docs chain but never table, every phase kind inferred and every row it could not resolve — the review reads that report, not the JSON. See `SCENE_SCHEMA.md` § Generation | Since 8.33.0 the scene carries a `capacity` block (demand per use case from docs/08 § Demand by Use Case, capacity per container from the descriptors' `## Capacity` tables, normalized to rps) that the load simulation reads; `--capacity-check` prints it with every `Not documented` gap. Since 8.54.0 each capacity row also carries `requestSize`, `responseSize` and `sessionTransfer` (bytes, from the same table), `overrides.deploymentNodes` sets a deployment node's `metered` (what its provider bills) without rewriting the array, and `overrides.capacity.pricing` prices a metered node per GB — assumptions, marked as such.
| `scripts/simulation.js` | The load model — pure JS shared by the viewer (inlined by `render.js`), Alia's tools and the tests: demand × phases → ρ per instance, findings, compare, proposed rows |
| `scripts/render.js` | `bun <skill_dir>/scripts/render.js <scene.json> <out.html> --lang <es|en> [--theme <skin id>] [--skins <dir>] [--view logical|physical]` — validates the scene (unknown nodes, dangling hops, unknown phases, and the `deployment` block: tiers, parents, instances, path endpoints, transport form) and substitutes it into the template. Zero dependencies; Bun is the plugin's only authorized runtime |
| `scripts/snapshot.js` | `bun <skill_dir>/scripts/snapshot.js <viewer.html> <out.png> [--plan <component id>] [--width 1600] [--height 1000] [--scale 1\|2\|3] [--wait <ms>] [--chrome <path>]` — the viewer's photo mode as a file (10.6.0): headless Chrome over the DevTools protocol, no dependency; the PNG is captioned with the project, the version, the view and the date, and the caption is printed. `--plan` (10.21.0) frames the plan page of that component's floor with it selected, and the caption adds the floor and the component. The evidence a release carries: `architecture-lifecycle`'s `ci/architecture-handoff.yml` takes one picture per component the release changed (its `payload_hash` in the kit's manifest moved, at most three), each with `--plan`, or the whole model when none changed, commits them with the scene and embeds them in the kit's PR. Browser: `--chrome`, `SA_CHROME` / `PUPPETEER_EXECUTABLE_PATH` / `CHROME_PATH`, Puppeteer's download, then `PATH` |
| `references/SCENE_SCHEMA.md` | The scene JSON contract: every field, the classification rules for routes and phases, the `deployment` block behind the physical view, and the layout hints |
| `examples/order-desk.scene.json` | A complete worked scene of **Order Desk**, a synthetic order-taking system (every name invented — an example never carries a real project's): the logical part generated by `scene-from-docs.js` from the test fixture, plus an authored `deployment` block (four trust-zone tiers, a region with a nested cluster and namespace, a provider-managed store, the customer's device, paths of three classes). Read it once before authoring a `deployment` block. Rebuilt by `bun examples/build-example.ts` with a judge answering (since 8.119.0 a name the judge has not answered stays undecided, so the default `agent` engine yields a partial scene until its worksheets are answered); a test holds the committed file to it under a fake judge |

---

## Workflow

### Step 0 — Gates

1. `ARCHITECTURE.md` must exist at the project root (or one level up). If not, abort with:
   > *"No ARCHITECTURE.md found. Use `/skill architecture-docs` to create one first."*
2. Resolve `doc_language` (section above).
3. `docs/03-architecture-layers.md` (Section 4) and `docs/components/README.md` (Section 5) are
   required — without them there is nothing to place on floors. `docs/04-data-flow-patterns.md`
   (Section 6) is what makes the use-case filter possible; if it is missing, still build the
   model and say plainly that the use-case tab will be empty.
4. Resolve `skill_dir` — the renderer and template are read from there, never copied into the
   project: `skill_dir = $plugin_dir/skills/architecture-command-center`, with `plugin_dir` from
   `bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-visualization`
   — this skill ships in the **sa-visualization** plugin, which `sa-skills` depends on and installs; its scripts
   read the architecture through sa-skills and find it on their own (`scripts/sa-skills.js`: `--sa-skills`,
   `SA_SKILLS_DIR`, the repo layout, the install registry), stopping with the install command when it is absent
   (Claude Code's install registry — the project-scope install, else user scope, else the copy the
   script runs from; it warns on stderr when a newer version is on the machine: show the warning).
   **Never a Glob over `~/.claude/plugins/cache/`** — it keeps every version ever installed and a glob
   returns an arbitrary one. Without the
   marketplace clone: Glob `**/{sa-skills,solutions-architect-skills}/.claude-plugin/plugin.json`
   outside the cache, strip the suffix and append `/plugins/sa-visualization`.

### Step 1 — Corpus overview, then targeted reads

The **logical scene reads the corpus itself** (Step 2): `scene-from-docs.js` takes the layer
table of `docs/03`, every descriptor under `docs/components/`, the Phase Catalog and Flow
Inventory of `docs/04` and the `I-nn` rows of `docs/05`. You read, whole, only what feeds the
overrides and the review:

| Read | Take from it |
|------|--------------|
| `docs/03-architecture-layers.md` | Any section that names an exception to the layering rule (a connection that skips layers, a channel that owns data) — that exception is usually the **thesis** |
| `docs/01-system-overview.md` | Use-case titles as written, to check the generated use cases against; the architecture type when `ARCHITECTURE.md` carries no marker |
| The generator's report | Every actor, synthesized edge, inferred kind and unresolved row — each one is either a docs finding or an overrides entry |

For the **physical view** (Step 2b), read as well — and build the `deployment` block only from
what these say, never from what a typical cloud looks like:

| Read | Take from it |
|------|--------------|
| `docs/09-operational-considerations.md` (Section 11) | § Deployment: environments, region, cloud, cluster, deployment mechanism per component, IaC. Any ingress or network chain it names |
| `docs/06-technology-stack.md` § Infrastructure | Orchestrator, mesh, gateway, WAF, secrets, streaming platform, observability — the products the nodes are named after |
| `docs/07-security-architecture.md` (Section 9) | Trust zones, perimeter controls (WAF, firewall, front door), what is exposed publicly, private links, mTLS, jurisdiction of data at rest |
| `docs/08-scalability-and-performance.md` (Section 10) and each container's `## Deployment` / `## Despliegue` section | Replicas, HPA bounds, resource class, resilience role per instance |
| ADRs on cloud, region, runtime, connectivity and ingress (institutional or project) | Region mandates, primary / secondary cloud, cloud ↔ on-premise and cloud ↔ cloud transports, the ingress chain order |

Architecture types other than ENTERPRISE still have a Section 4 layer/tier table (3-Tier, N-Layer)
or zones (Microservices, BIAN). Use whatever Section 4 groups the containers by, top to bottom,
as the floors. If Section 4 gives no ordering at all, fall back to three floors — channels,
services, data — and say so in the report.

### Step 2 — Generate the scene JSON, then review it against the docs

The logical scene is **generated, not authored**. **One scene per project**, rewritten in place:
the generator writes `visualizations/architecture-command-center.scene.json` and takes the
previous one as its base (node ids kept, so the `deployment` block and any `x` / `z` still point
at the same containers; `--no-base` starts fresh):

```bash
bun <skill_dir>/scripts/scene-from-docs.js <project_root> [--overrides <json>]
```

A project rendered before 8.150.0 holds dated pairs (`architecture-command-center-<date>.*`,
`architecture-3d-view-<date>.*`): the newest dated scene becomes the base, and the generator deletes
every dated scene and page once the current scene is written and lists them — git keeps the
history. Never pass `--out` with a date.

Then read the **report on stderr** — it is the review checklist, and every line of it is a
decision the docs left to you:

- **Actors** — a chain participant that is no container (a device-integrity SDK, a security
  team). Right when the docs mean a participant outside the architecture; wrong when a
  container is named by an alias the docs never use elsewhere (fix the docs, never the scene).
- **Synthesized edges** — a hop the Phase Catalog chains that neither `docs/05` nor a
  Communication table documents. Each one is a missing integration row or an over-specified
  chain; report it as a finding and let the docs decide. The scene keeps the hop so the
  walkthrough is complete, unlabelled.
- **Inferred phase kinds** — kinds the base scene and the overrides did not state, read from
  the protocols on the hops (`kafka` / `cdc` / `wss` → `async`, a batch word → `batch`, every hop
  on the top layer → `local`, an integrity / session / revocation / parameter name → `control`,
  else `online`). Confirm or pin them in the overrides — the colors are the legend.
- **Warnings** — a Communication row whose endpoint is a system and whose Description names
  none of its containers, a `docs/03` layer that names an unknown container, a flow without a
  `**Phases**` line, a base `deployment` instance of a container that no longer exists.

What the documents cannot state goes in an **overrides file** (`--overrides`, see
`SCENE_SCHEMA.md` § Generation): the thesis, a phase's color family, a `jump`, a node `code`, an
edge the docs describe only in prose. Overrides are merged last and survive every regeneration;
a hand edit of the scene JSON does not. Never patch the generated JSON.

The rules the generator applies — and the ones you check when you read the result:

- **Every C4 L2 container of the internal system is a node, with its canonical full name**
  (`name` from `component-cli.ts list`). The viewer is often the first thing a stakeholder sees; a
  truncated or aliased name there propagates into conversations and tickets. The descriptor's
  `**Internal Name:**` rides along as `internal`: the inspector and Alia show it beside the
  canonical name, the brain receives it as a second identifier, and it is the natural id for
  the container's deployment instance. It is never the `name`.
- **External systems are systems with `owned: false`; their containers are nodes too**, read
  from the descriptor's `## Containers` table. An external system with no such table is one
  node named after the system.
- **Actors are not containers.** They are drawn as small octahedra, labelled in italics and
  badged "phase actor" so nobody mistakes them for architecture, on the layer of the container
  they touch.
- **Edges come from the tables, not from inference.** One edge per documented pair; the label
  is the protocol and the `I-nn` id. `jump` is set when the endpoints are two or more layers
  apart. A Communication row of an L1 descriptor whose endpoint column holds a **system** is
  resolved through the containers its Description names by canonical name — write one row per
  container pair, name the containers in the order the data passes, and cite the `I-nn` when
  `docs/05` already carries the row.
- **Routes are the phase kinds in use**: `local` (a read that stays on the edge / device),
  `online` (request-response descending the layers), `async` (events, CDC, replication),
  `control` (integrity, session, revocation, restoration — lifecycle of the data), `batch` (off
  the critical path, drawn dashed). An edge carries the routes of the phases that travel it.
- **Phases are the Phase Catalog's owner chains walked over the edge graph** — a `**Hops**`
  line in the phase block wins over the chain. A system in the chain is entered through the
  documented edge and crossed through its own containers to the next participant, or walked to
  its last container. A store never initiates: a hop leaving a store fans out from the last node
  that reaches the target. `A y B` / `A and B` both travel; a name that covers several containers
  (`Topicos CDC`) sends the first and lights the rest as `extra`. The p95 budget is the phase
  block's `**Latency budget (p95)**` line.
- **Use cases are the Flow Inventory rows** with the flow block's `**Phases**` line, latency
  target, `**Governed by**` ADRs and `**Delta**`. A flow that lists one use case takes its id;
  one that lists several keeps `FLOW-<code>`. A flow without a block is skipped and reported.
- **Positions** come from the base scene by node id; leave the rest to the auto-layout.

Before rendering, read the report once more: no synthesized edge you cannot explain, no actor
that is really a container, every inferred kind confirmed. The thesis is the one sentence the
docs actually support — it lives in the overrides.

### Step 2b — Author the physical view (`deployment`)

Add a `deployment` block to the same scene file when Section 11 documents where the system runs
(see `SCENE_SCHEMA.md` § Deployment). Skip it — and say so in the report — when the docs give
no deployment material; the viewer then hides the **Physical** button and nothing else changes.
The rules, and why:

- **Tiers are trust zones when the docs declare them** (`Public` → `DMZ` → `Internal` →
  `Restricted` → `CDE`, top to bottom); otherwise whatever Section 11 groups the infrastructure
  by. The stratification is the story of the view: what is exposed, what is one hop behind the
  perimeter, what holds the data. Mark `owned: false` on tiers the organization does not operate
  (the public internet, the customer's device).
- **Nodes are named after the products and places the docs name**, nested with `parent`
  (namespace › cluster › region, on-premise data center, SaaS platform). A node that contains or
  hosts something is a box; an appliance with nothing inside — WAF, firewall, front door,
  gateway, HSM — is a slab. Never invent a component of the chain: if Section 11 names four hops
  between the client and the cluster, the model has four.
- **Every internal container gets at least one instance**, on the node its `Deployment`
  section or Section 11 assigns it, carrying replicas and resilience role as written
  (`10–30 (HPA)`, `Active`). External containers get instances too when the docs place them
  (a PaaS gateway, a SaaS broker); a provider-managed node is `owned: false`.
- **Paths are undirected and in transport form** — `TLS:443`, `TCP:9092` — one per documented
  link between nodes, each with its **Path Class** (`Private Link` · `Peering` · `VPN` ·
  `Service Mesh` · `Direct Connect` · `Public Internet`). Direction is the logical view's job;
  a deployment path that needs an arrow is a modelling error. Declare the chain the docs
  describe hop by hop; the viewer routes every logical edge through the shortest chain of
  declared paths, so an ingress chain declared once carries every use case that crosses it.
- **Run `render.js` and read its warnings**: internal containers no instance places, paths
  without a class, transports that are not `<TRANSPORT>[:<port>]`. In the viewer, switch to
  **Physical** and open **Paths → No declared path**: each dashed link there is a logical
  connection the deployment docs do not realize — report those as findings, never paper over
  them with a guessed path.
- **Trust zone and jurisdiction inherit by containment** (an instance inside a cluster inside a
  region carries the region's jurisdiction unless raised); set them on the outermost node that
  the docs state them for, not on every child.

### Step 2c — Build Alia's dossier

```bash
bun <skill_dir>/scripts/dossier.js . visualizations/architecture-command-center.scene.json --write
```

Run it from the project root after the scene is written and before rendering. It bakes what the
files say into `scene.dossier` — the cited ADRs, every TDR, the compliance manifest and its
requirement rows, each container's descriptor and the integration inventory — so a click in the
viewer opens Alia with what is on file: offline, and never more than the file states. Read its
output: every cited ADR without a file, every container whose descriptor H1 does not match its
canonical name, and every contract the manifest names but the folder lacks are listed, and Alia
says so when they are clicked. Do not write dossier entries by hand; if something is missing, fix
the citation, the descriptor's H1 or the folder.

### Step 3 — Render

```bash
bun <skill_dir>/scripts/render.js visualizations/architecture-command-center.scene.json \
    visualizations/architecture-command-center.html --lang <doc_language> [--theme <skin id>] [--skins <dir>] [--view logical|physical]
```

`--theme` picks the look the file opens with — `holo`, `atlas`, `corporate` or a project skin from `visualizations/skins/` beside the scene (see `skins/README.md`); omit it for `holo`, or set
`"theme"` in the scene JSON. `--view physical` opens on the physical view (needs `deployment`);
omit it for `logical`, or set `"view"` in the scene. The viewer keeps runtime switches for both.

Bun is the plugin's only authorized runtime (`Bash(bun *)` is already granted; `node` is not).
The renderer fails with a list of dangling references rather than producing an empty scene — fix
the JSON, never the HTML. Nothing is installed and no network is needed to render; the viewer
itself loads Three.js r128 from cdnjs when opened.

### Step 4 — Open and hand over

- Open the file locally (`xdg-open` / `open`). The local file is the review surface.
- **Never publish the HTML online on your own.** An architecture model names systems,
  technologies, budgets and boundaries; whether that leaves the machine is the user's decision,
  not the skill's. If an artifact-publishing tool is available in the session, end the report
  with one line offering it ("Say *publish* to also host it as a private artifact and get a
  link — a hosted copy also opens Alia's channel to the brain") and publish only when the user
  says so. Never publish when they do not answer.
- Read `VIEWER_REFERENCE.md` § Viewer capabilities for what to hand over.
- Report, in the user's language: where the two files are, the thesis sentence, the list of use
  cases and routes available as filters, whether the **Physical** view is available and what it
  is stratified by, the containers no instance places and the logical connections with no
  declared path, and anything left out (missing Section 6 or Section 11, undocumented protocols,
  external systems not decomposed).

### Step 4b — Publish, only when the user says so

The same HTML serves both surfaces; nothing is re-rendered for the hosted copy. **Two steps, in
this order, every time:**

1. **Load the `artifact-capabilities` skill first** (`Skill: artifact-capabilities`). The Artifact
   tool requires it before any `capabilities` value is passed; a publish attempted without it is
   the usual reason a hosted copy comes up with the channel closed ("Alia's channel needs
   `sample`" — the viewer's `claude.use('sample')` resolved `null` because the page declared
   nothing).
2. Publish the rendered file **declaring `sample` and `downloads` in the same call**:

```
Artifact  file_path: visualizations/architecture-command-center.html
          capabilities: { "sample": {}, "downloads": true }      # sample: Alia's channel to the brain · downloads: the Excel export of the scenarios — never omit on a first publish, never pass {}
          favicon: "🧭"  (first publish only)   description: one sentence naming the system
```

A non-empty `capabilities` is a full-set declaration, an omitted one carries the stored
declaration forward on a redeploy, and `{}` revokes everything — so a redeploy may omit it, a
first publish may not, and `{}` is never right for this page. After the call, read the result:
when it does not confirm the capability, or the user reports the box absent and Alia saying the
channel is closed, republish the same file path with the declaration — nothing in the HTML needs
to change.

`sample` lets the page ask Claude a question on the **viewer's** account: the first question in a
view asks that viewer's consent, a decline closes the channel for that view, and the usage is
theirs, not the publisher's. Declare nothing else — the viewer needs no database, room or
connector. Without the declaration the hosted copy behaves exactly like the local file: Alia
answers from the dossier and says the channel is closed. Redeploys to the same file path keep
the URL; pass the artifact's `url` to update a copy published in an earlier session. Report with this fixed text — nothing else about the publish, no asides about the capability's name:

```
Publicado: <url>
Copia: <actualizada — la del render del <fecha> | nueva>. <Las copias anteriores siguen en su enlace y no se tocaron.>
Canal de Alia: abierto — la copia declara `sample`; cada pregunta corre con el uso de Claude del visitante, y la primera pide su consentimiento.
Privado hasta que lo compartas desde el menú de la página.
```

(In `en`: `Published`, `Copy: updated — the render of <date> | new`, `Alia's channel: open — the copy declares \`sample\`; every question runs on the viewer's own Claude usage, and the first one asks for consent`, `Private until shared from the page menu`.)

### Step 5 — Refresh after doc changes

The scene is regenerable. When `docs/` or `docs/components/` change, run `scene-from-docs.js`
with the same `--overrides` file (the current scene is the base), rebuild the dossier and
re-render over the same two files; node ids, positions, phase kinds and the `deployment` block carry over, so the model
does not reshuffle for no reason. Do not patch the HTML, or the scene JSON, by hand.

---

## Alia, the viewer and the themes

The viewer's behaviour — Alia's dossier and her channel to the brain, the Simulation mode, findings on
the stage, the HUD cues, every capability handed to the user and both themes — is described in
`VIEWER_REFERENCE.md` in this directory. Step 4 reads its § Viewer capabilities; read the rest when a
user asks how the viewer behaves or when the viewer itself is being changed.

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `architecture-docs` | Source of every fact in the scene; Workflow 8 owns the Mermaid diagrams the 3D view complements |
| `architecture-component-guardian` | Owns `docs/components/README.md`; canonical names come from the container files it writes |
| `explorer-cli.ts manifest` (code) | Corpus overview in Step 1 for corpus overview |
| `architecture-icepanel-sync` | The maintained C4 model with drift detection; recommend it when the user wants a living model rather than a presentation artifact |

---

## Example Invocations

- "Crea una vista 3D de esta arquitectura"
- "Show me the architecture in 3D so I can walk the product owner through the use cases"
- "I want an interactive model of the layers with the replication path highlighted"
- `/skill architecture-command-center`
- "Open the command center for this system" · "el centro de mando de la arquitectura"

---

## Permissions Required

Add to your project's `.claude/settings.json` (already present in the plugin's
`.claude/settings.json.example`, which `/sa-skills:setup` merges):

```json
"Bash(bun *)",
"Bash(rg *)",
"Edit(visualizations/*)",
"Read(visualizations/*)",
"Bash(bun *)"
```

The skill writes only under `visualizations/`. It reads `ARCHITECTURE.md`, `docs/**` and `adr/**`
and never writes to them.

---

## Success Criteria

- [ ] `ARCHITECTURE.md`, Section 4 and Section 5 located; `doc_language` resolved
- [ ] Scene JSON **generated** by `scene-from-docs.js` as `visualizations/architecture-command-center.scene.json` (the previous scene its base), never hand-written; the report on stderr read, every synthesized edge and inferred kind either confirmed in the overrides or reported as a docs finding
- [ ] External systems flagged `owned: false`; actors, if any, flagged `kind: "actor"`
- [ ] Every edge traceable to a `docs/05` row or a Communication table (synthesized hops reported as findings); layer-skipping edges marked `jump`; the thesis and every hand decision in the overrides file, not in the JSON
- [ ] Phases and use cases match Section 6 verbatim in order and budgets
- [ ] `render.js` ran clean (no dangling references) and the HTML opened locally
- [ ] Theme matches what the user asked for (`holo` unless they asked for the neutral `atlas` look, the `corporate` business look, or the project's own skin)
- [ ] `deployment` authored when Section 11 documents where the system runs: tiers by trust zone (or Section 11's own grouping), nodes named as the docs name them, one instance per internal container, paths undirected in transport form with a Path Class
- [ ] `render.js` warnings read; unplaced containers and *No declared path* links reported as findings, not patched with guesses
- [ ] `dossier.js --write` run from the project root after the scene; cited ADRs without a file, descriptors whose H1 does not match, missing contracts and unresolved findings reported, never hand-written into the dossier
- [ ] Nothing was published online unless the user explicitly asked for it; a requested publish declared `capabilities: { "sample": {}, "downloads": true }` so Alia's channel to the brain opens and the Excel export can hand the viewer the file (a published page cannot download by link — the viewer confirms the save), and the report said the brain runs on each viewer's own usage
- [ ] Report names the thesis, the filters available, and what was left out

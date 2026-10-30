---
name: architecture-docs-export
description: >
  Export architecture documents to professional Word (.docx) files: "export architecture to
  Word", "export handoff to Word", "stakeholder briefing", "generate .docx". On-demand only —
  never runs automatically. Two modes: Solution Architecture (a bounded role-routed stakeholder
  briefing for Product Owners, chapter leads and technical owners, its companion architecture
  reference, then individual ADR docs) and Handoff (the four-part handoff kit). Content is
  extracted verbatim from existing files.
  This skill only produces .docx files. A request to release, publish, ship, tag, freeze, bump or
  finalize an architecture version is a release, not an export: it routes to `architecture-docs`
  (`architecture-lifecycle`).
triggers:
  - export architecture to Word
  - export handoff to Word
  - stakeholder briefing
  - generate .docx
---

# Architecture Doc Export Skill — Orchestrator

Exports architecture documents to professional Word files on demand.

> **On-demand only** — this skill never runs automatically after document generation. Invoke it explicitly when you are ready to produce deliverable Word files.

---

## Architecture — Orchestrator + Sub-Agent

This skill is an **orchestrator** for two export modes: Solution Architecture and Handoff Kit. It reads nothing compliance writes. **Both are assembled and rendered by code**: `scripts/sa-export-assemble.js` writes the briefing and the reference, and the orchestrator runs `generate-doc.js`; `scripts/handoff-export.js` discovers the kit, composes each component package and runs `generate-doc.js` for every selected part. The `docs-export-generator` sub-agent (its model pin keeps cost per run stable) runs only for a **translated** export — it translates the parts a script laid out, one file per `Write`; the scripts render them.

**Orchestrator responsibilities** (main context):
- User interaction: listing ADRs and the handoff kit, parsing selection ("all", numbers, ranges)
- Plugin directory resolution
- Running the scripts; spawning the sub-agent for a translated export

**Sub-agent responsibilities** (`agents/generators/docs-export-generator.md`) — translated exports only:
- SA mode: translate the assembler's parts, join them, call docgen
- Handoff: translate the parts `handoff-export.js` laid out; the script renders them
- Report a structured `EXPORT_RESULT:` block back

---

> **Runtime: Bun only — never Node.** All generator calls inside the sub-agent use `bun run $sa_skills_dir/tools/docgen/generate-doc.js` (absolute path). If `bun run` hangs:
> 1. Ensure the docgen packages (`docx`, `pdfmake`) are installed: `bun install` in `$sa_skills_dir` (the workspace root — `bun scripts/setup-docgen.ts` there reports what is missing or off its pin)
> 2. Confirm `plugin_dir` was resolved correctly in Step 0 — re-run the Glob if unsure
> 3. Never fall back to `node` — it is not an authorized runtime

> **Documentation Fidelity**: In **native** exports — where the deliverable language matches the
> project's `doc_language`, which is the default — all content is extracted verbatim from source
> files. No paraphrasing, no embellishment. If a required section exists in the source but is empty,
> the sub-agent writes `[NOT DOCUMENTED — add content to <source-file>]`.
>
> In a **translated** export (Step 0.6), the body is rendered into the target language under the
> translation contract — structure preserved exactly, machine layer preserved literally, nothing
> added — and the cover carries a `Translation` row naming the source language. Translation is the
> one sanctioned departure from verbatim extraction, it is opt-in per export, and the
> source-language document stays authoritative.

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

**In this skill**: `doc_language` is the language the **source documents** are authored in. It is
not necessarily the language the **deliverable** must be read in — see Step 0.6 below. Export
**filenames** (`SA-<slug>.docx`, `KIT-01-runtime-view-*.docx`, …) stay English in every case; a
translated export appends a language suffix (`-en`, `-es`) but the stem never localizes.

### Step 0.6 — Resolve the export language (both workflows)

Runs once per invocation, before any workflow branches. **Every export mode honours it** —
Solution Architecture and Handoff Kit alike.

Ask only when the project has a `doc_language` and the user has not already named a target
language in their request ("export the briefing in English", "exportar en español"):

```
🌐 Export language

   This architecture is authored in Spanish (LATAM).

   1. Spanish (LATAM)  — native, exported verbatim          [default]
   2. English          — translated for this deliverable

   Both can coexist: a translation is written to SA-<slug>-en.docx and
   never overwrites the native SA-<slug>.docx.
```

Resolve to two values and pass both to the sub-agent:

| Value | Meaning |
|---|---|
| `doc_language` | source language, from `<!-- DOC_LANGUAGE: -->` |
| `export_language` | target language for this deliverable; defaults to `doc_language` |
| `lang_suffix` | `""` when the two match, otherwise `-<export_language>` |

**When they match — the default and the common case — nothing changes.** The body is extracted
verbatim exactly as before and no translation happens.

**When they differ**, the sub-agent renders the body per the translation contract
(`LANGUAGE_POLICY.md` §5.8) and passes `--translated-from <doc_language>` to `generate-doc.js`,
which stamps a `Translation` row on the cover naming the source language and stating that the
source-language document remains authoritative.

Warn once before a translated export, because the cost is real and asymmetric:

```
ℹ️  Translated export: the body is rendered into English, not extracted verbatim.
    Component names, technology names, metrics, status values, requirement codes
    and quoted evidence stay literal. The Spanish (LATAM) documents remain the
    source of record — this deliverable is a rendering of them.
```

**Translation never touches the project's `.md` files.** It renders into the export only.
`DOC_LANGUAGE` does not change, the source documents do not change, and no downstream gate ever
sees translated content — an export is a leaf.

**`es` is LATAM-neutral Spanish**, never Peninsular: `ustedes` not `vosotros`, no voseo,
`computadora` not `ordenador`, `celular` not `móvil`. Dates format as `es-419`. See
`LANGUAGE_POLICY.md` §5.7.

Structural headings this skill writes carry their English anchor comment in both languages
(`## Heading <!-- SECTION: English Name -->`). The full do-not-localize registry — codes, status
enum values, table column headers, filenames, marker names, `EXPLORER_HEADER` field keys — is
`LANGUAGE_POLICY.md` §4.

---

## What Gets Exported

| Export Mode | Input Sources | Output |
|-------------|--------------|--------|
| Solution Architecture | **Required**: `docs/01-system-overview.md` + `docs/02-architecture-principles.md` + `docs/components/README.md`. **Optional, each feeding one briefing section**: `ARCHITECTURE.md`, `docs/03-architecture-layers.md`, `docs/04-data-flow-patterns.md`, `docs/05-integration-points.md`, `docs/06-technology-stack.md`, `docs/08-scalability-and-performance.md`, `docs/09-operational-considerations.md`, `docs/10-risks-and-technical-debt.md`, `BIAN_ALIGNMENT.md`, `TRACEABILITY_REPORT.md`, `analysis/TECH_DEBT-*.md`, `docs/07-security-architecture.md` | `exports/SA-<name>.docx` (bounded role-routed stakeholder briefing) + `exports/SA-<name>-reference.docx` (the detail the briefing cites) + `exports/ADR-NNN-<title>.docx` per ADR |
| Handoff Kit | Four-part kit in `handoffs/` — `SYSTEM_RUNTIME_VIEW.md`, `CROSS_CUTTING_STANDARDS.md`, `interfaces/*.md`, `components/*.md` | `exports/KIT-01-runtime-view-<solution>.docx` + `exports/KIT-02-standards-<solution>.docx` (shared, once each) + `exports/HANDOFF-<component>.docx` per component (its Interface Contracts + Component Specification); optional `exports/INTERFACE-<up>-to-<down>.docx` |

### Diagrams

**Mermaid diagrams export as pictures when mermaid-cli is installed**. `tools/docgen/generate-doc.js` runs a pre-render pass — `tools/docgen/render-mermaid.js` — between the markdown parse and either renderer: every ````mermaid``` fence it can render becomes a PNG, embedded centred and fitted to the text column in both `.docx` and `.pdf`. The four standard diagrams and the Data Flow sequences all arrive as drawings.

The pass shells out to mermaid-cli (`mmdc`), an **`optionalDependency` of `tools/docgen`** — optional so that a machine which cannot build Puppeteer still gets a working Word path, declared because the briefing this skill produces opens on a single C4 Level 1 picture and a stakeholder reading `flowchart TB` in Courier New is reading nothing. It is auto-detected at runtime from `MMDC_PATH`, from `node_modules/.bin` at or above `tools/docgen/`, or from `PATH`. Install it once, where the exports run:

```bash
bun install                               # from the plugin directory — installs mmdc and pdfmake
bunx puppeteer browsers install chrome    # Bun skips Puppeteer's own post-install browser download
# …or point mmdc at a browser already on the machine (any Chrome/Chromium/Edge binary works):
export PUPPETEER_EXECUTABLE_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"

bun scripts/setup-docgen.ts               # report the chain, with a real render as the last check
```

`/setup` Step 7 runs that report. Step A.3a of this workflow checks the **diagrams**; the toolchain that turns them into pictures is checked there.

**The export never fails over a diagram.** With mermaid-cli absent, or when one diagram does not parse, that diagram falls back to Courier New source as before — everything else still renders. docgen prints one summary line per run:

```
3/4 Mermaid diagram(s) rendered as images, 2 from cache, 1 failed — exported as source
```

**Carry that line into the report**, together with the install hint docgen prints when the fallback was taken. A committee reader must not be the one who discovers a wall of source.

Flags (all optional, all defaulted): `--mermaid auto|on|off` — `auto` is the default and degrades silently, `on` makes a missing mermaid-cli a hard error for a pipeline whose deliverable must carry the drawings, `off` forces source; `--mermaid-theme <name>`; `--mermaid-scale <n>` (resolution only — the diagram still lands at the size Mermaid laid it out for); `--mermaid-background <color>`; `--mermaid-puppeteer-config <file.json>`. Renders are cached by source hash under the OS temp directory, so re-exporting an unchanged architecture pays for no browser launches.

---

## Step 0 — Resolve Plugin Directory (orchestrator)

Before spawning the sub-agent, the orchestrator MUST resolve the absolute path to the plugin installation and pass it in the spawn prompt.

**Resolve `plugin_dir`** — one call, never a Glob over `~/.claude/plugins/cache/` (it keeps every version ever installed and a glob returns an arbitrary one):

```bash
plugin_dir=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-delivery)
sa_skills_dir=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts)
```

`[design_language_dir]` is the Design Language Standard in force — `bun [sa_skills_dir]/scripts/shared/packs.js --path design-language` prints it (an institution pack's — the base carries none) or prints nothing and exits 1: **fallback mode**.

This skill ships in the **sa-delivery** plugin (`sa-skills` depends on it and installs it). `[plugin_dir]` is sa-delivery's install (this skill's scripts, templates and agents); `[sa_skills_dir]` is sa-skills' — the architecture is read through its facts ledger, explorer, judge and shared scripts, documents render through its `tools/docgen`, and the scripts find it on their own (`scripts/sa-skills.js`: `--sa-skills`, `SA_SKILLS_DIR`, the repo layout, the install registry) and stop with the install command when sa-skills is absent. The script answers from Claude Code's install registry — the project-scope install for this directory, else the user-scope one, else the copy it runs from — and warns on stderr when a newer version is on the machine (`claude plugin update … --scope <scope>`, then `/reload-plugins`); show that warning to the user. Without the marketplace clone (a dev clone alone): Glob `**/{sa-skills,solutions-architect-skills}/.claude-plugin/plugin.json` **outside** `~/.claude/plugins/cache/`, strip `/.claude-plugin/plugin.json` for `sa_skills_dir` and append `/plugins/sa-delivery` for `plugin_dir`.

If both fail:
```
❌ Cannot locate plugin directory. Ensure the plugin is installed correctly.
```

`plugin_dir` and `sa_skills_dir` are passed to the sub-agent in the spawn prompt — the sub-agent does NOT re-resolve them.

---

## Step 0.5 — Export Pre-Flight (conditional, orchestrator)

**Runs only when** `[design_language_dir]/llms-rules.txt` exists. If it does not, skip this step entirely and proceed to the workflow — nothing below applies.

An export is the moment a document leaves the delivery team, and the SA Design Language Standard governs that moment through **Appendix E (normative)**: eleven named deliverables, each with a required export profile, mandatory altitudes, focus tags, and a **marking ceiling**. Read the standard's §8 before the first export in a session; escalate to the Appendix E range of `llms-full.txt` (rg `^## Appendix E`) when a deliverable card's detail is needed.

Run these six checks **in order**, before spawning the generator. This step **warns and asks — it does not block**: the architect decides, and the decision is theirs to record.

1. **Name the card.** Which of the eleven deliverables is this? The usual mappings for this skill: Solution Architecture (Workflow A) → *Executive / Board briefing* (#3); Handoff Kit (B) → *Delivery work package* (#1) — the card applies to each exported part, shared documents included. If you cannot name the card, **ask the user** — the correct next action is a question, not an export.
2. **Check altitudes against the card.** Every mandatory altitude present, nothing below the card's floor, extra altitudes only if the reader asked.
3. **Check the profile against the card.** Risk audience → **Risk Overlay**. Leaving the bank → **Redacted**. Otherwise **Working**. The audience determines the profile, not the author.
4. **Check that the focus tags render, and nothing else does** — both directions.
5. **Check the marking.** Read the computed `Distribution` against the card's ceiling. Above the ceiling, the export needs a Redacted profile, a recorded AGB decision, or both. **This is the only step whose failure cannot be undone after sending** — surface it prominently.
6. **Check provenance and record the export.** Provenance complete, `Next review` not expired; then record deliverable, profile, recipient and date. The plugin has no diagram register, so state plainly that the recording is manual and belongs in the register row — do not imply it happened automatically.

Print the result as a short pre-flight block and ask for confirmation before continuing:

```
Export pre-flight (SA Design Language Standard, Appendix E)
  Deliverable card:  #3 Executive / Board briefing
  Required profile:  Risk Overlay (Criticality only)
  Marking ceiling:   no ceiling, named recipients
  Computed marking:  [Distribution value, or NOT DOCUMENTED]
  ⚠️  Recording this export in the diagram register is manual — this skill cannot write it.
Proceed? (y / adjust / cancel)
```

**Known limitation, state it rather than paper over it**: `C-15` is *Blocking* when a marking ceiling is breached, and it reads the register's Exports list. This skill writes `.docx` files and keeps no register, so its pre-flight is an advisory checklist, not a conformance gate. Never report an export as `C-15`-conformant.

---

## Workflow A — Export Solution Architecture

**Trigger phrases**: "export architecture", "export to Word", "export solution architecture",
"stakeholder briefing", "export briefing"

**What this produces**: **two documents, and the split is the point.**

`exports/SA-<name>.docx` is a **role-routed stakeholder briefing** written for the people who
receive an architecture rather than author it. It opens on **§ In One Page** — the C4 Level 1 picture
and four plain statements (what it is · why · how it works · what this briefing decides) — then the
reader guide, then a section each for the Product Owner, chapter leads and technical owners, and it
closes on the Decisions Pending register. Every extraction in it is **bounded** — a summary table, a
diagram, an inventory — never a source file pasted whole.

**It explains before it tabulates.** Every subsection opens with one plain sentence saying what the
reader is looking at; every carried table is capped so it can be taken in at a glance; the overview
prose, the wire-level sequence diagrams and the per-requirement traceability tables are the
reference's, not the briefing's. **Every use case gets a storyboard** (8.51.0): under § Data Flows,
after the flow inventory, one `flowchart TB` per flow composed by the assembler from the ledger —
the trigger, the phases by name in the flow's order, the end-to-end target — so a non-technical
reader sees what happens in each use case without the protocol-level steps; a flow that declares no
phases gets none, and `flow-check.js` names that gap. A reader who did not author this architecture must be able to
follow it: forty rows of open decisions on page one, or a Key Metrics block deriving TPS from a
client count, is the failure this shape exists to prevent.

`exports/SA-<name>-reference.docx` is its companion: the structural diagrams, the principles in
full, the per-phase flow decomposition, per-integration detail, security architecture, the
operational narrative, the per-requirement traceability evidence and the ADR index. Source-ordered,
unbounded, and read by architects and implementers.

Nothing is dropped and nothing appears twice — each block of source content lands in exactly one of
the two, and the briefing names the reference section wherever it stops short. A briefing that
carries every flow phase, every principle's trade-offs and every traceability evidence block is not
a briefing; it is the architecture with role headings on it, and its audience stops reading before
the section addressed to them. The composition rules are code:
`scripts/sa-export-assemble.js` and its tests.

### Step A.1 — Validate prerequisites (orchestrator)

Confirm `docs/01-system-overview.md` exists. If not:
```
❌ docs/01-system-overview.md not found.
   Generate architecture documentation first with /skill architecture-docs.
```

### Step A.1b — Probe the optional briefing sources (orchestrator)

Each optional source feeds one briefing subsection, the matching reference section, or both. Probe
for presence only — the sub-agent reads them — and pass the results so it does not re-discover them:

```bash
for f in ARCHITECTURE.md TRACEABILITY_REPORT.md BIAN_ALIGNMENT.md \
         docs/03-architecture-layers.md docs/04-data-flow-patterns.md \
         docs/05-integration-points.md docs/06-technology-stack.md \
         docs/07-security-architecture.md \
         docs/08-scalability-and-performance.md docs/09-operational-considerations.md \
         docs/10-risks-and-technical-debt.md; do
  [ -f "$f" ] && echo "present: $f" || echo "absent:  $f"
done
ls -1 analysis/TECH_DEBT-*.md 2>/dev/null | sort | tail -1 || echo "absent:  analysis/TECH_DEBT-*.md"
```

**A missing source never blocks the export** — the briefing writes that subsection's fallback line
naming the file and the skill that produces it. Report the absences to the user once, after the
export, as a coverage note (Step A.5); do not prompt mid-run.

Tell the user what a thin briefing means before they circulate it:

```
ℹ️  4 of 12 optional sources are missing. The briefing will name each gap
    in place rather than omit the section — but the Product Owner section
    will carry no requirements coverage, and Chapter Leads will see no
    technology currency data.
```

### Step A.2 — Discover ADRs (orchestrator)

Scan for ADR files in these locations, in order:
- `adr/ADR-*.md`
- `docs/adr/ADR-*.md`
- `docs/decisions/ADR-*.md`
- `ADR-*.md` in project root

Collect absolute paths. If zero ADRs found, still proceed — the briefing will have an empty ADR table.

### Step A.3 — Determine solution slug (orchestrator)

Read `docs/01-system-overview.md`'s H1; kebab-case it for the output filename. Pass as `solution_name_slug`.

### Step A.3a — Check the diagrams (orchestrator)

```bash
bun [sa_skills_dir]/scripts/shared/mermaid-check.js docs/03-architecture-layers.md docs/04-data-flow-patterns.md
```

A block that fails exports as source instead of a picture. Report each failing block (file, diagram, line, rule) and ask whether to fix it first (`/sa-skills:architecture-docs` — a one-line edit at the line named) or export as is; never fix a diagram from this skill.

### Step A.3b — Assemble both documents by code (orchestrator)

```bash
bun [plugin_dir]/skills/architecture-docs-export/scripts/sa-export-assemble.js <project_root> --lang <doc_language> [--slug <solution_name_slug>] [--parts]
```

It writes `.cache/sa-skills/export/sa-briefing.md` and `sa-reference.md` in the document language
— every block routed once by the rules the agent's PHASE SA states (the reader guide, the
Decisions Pending register, the fallback lines and the closing line included) — and prints the
sources found, what it routed and the Decisions Pending count. Read that report, not the files. Its last line is the **coverage receipt** — containers the
ledger knows but the § 4.1 layer table does not place (they are absent from the components-by-layer
table), containers with no internal name (their cell reads *Not documented*), systems with no
container declared — and every item in it is a documentation gap to report to the user with the
export, never something to fill from this skill.
No model token is spent on composition; on the reference project the two files take 40 ms where
the composing agent took 85 minutes. Pass `--parts --suffix -<export_language>` when `export_language != doc_language`: the parts in name order are the whole document (`briefing-00` / `reference-00` the title and metadata, `briefing-99` the closing line), and every filename they cite carries the export suffix.

### Step A.3c — Compose the plain-language layer (orchestrator)

Routing blocks is code; the plain language a non-author needs is not. The assembler writes
`.cache/sa-skills/export/plain-language.request.json` — `lang`, `max_chars`, and three requests:

- **`one_page`** — four slots (`what`, `why`, `how`, `decide`), each **≤ 240 characters**, composed
  from the `source` block it carries (the Problem Statement, Solution, Business Value and Key
  Metrics of `docs/01`). Write them for someone who knows the initiative and not the system: no
  container name, no protocol, no ADR id, no section number. This is the first page the Product
  Owner reads.
- **`metrics`** — up to `max_rows` `{ label, value }` pairs (label ≤ 40, value ≤ 90 characters)
  drawn from the Key Metrics block: the measures this initiative is judged on, as measures. A
  derivation, a caveat or a baseline that needs a paragraph is not one — leave it in the reference.
- **`leads`** — one sentence per subsection, **≤ 160 characters**, keyed by `key`. Say what the
  reader is looking at and what to do with it. The `carries` field states what the block under that
  heading contains.

All of it is **plain text**: no Markdown link, no code span, no line break. **From the sources,
nothing invented.** Write `.cache/sa-skills/export/plain-language.json` yourself, in one `Write`:

```json
{ "one_page": { "what": "…", "why": "…", "how": "…", "decide": "…" },
  "metrics": [{ "label": "…", "value": "…" }],
  "leads":   [{ "key": "po.risks", "text": "…" }] }
```

Then re-run Step A.3b with `--plain .cache/sa-skills/export/plain-language.json`. The receipt reads
`Plain language: N slot(s) applied`; a slot that breaks a rule is **refused** and named
(`lead cl.stack: 161 chars > 160 — omitted`), and the briefing renders without it — the heading
still stands, the table still follows. A refused `one_page` slot refuses the whole summary and the
briefing opens on the Problem Statement instead. Fix the named entries and re-run once.

Both composed files can be passed in the same run: `--plain <file> --risk-summaries <file>`.

### Step A.3d — Rewrite the critical risks for a non-technical forum (orchestrator)

The briefing's **Critical Risks** table is read by the Product Owner's forum, and the source rows
are written for engineers. When the receipt's `Risk summaries:` line says N rows are still
verbatim, the assembler has written `.cache/sa-skills/export/risk-summaries.request.json` —
`lang`, `max_chars` (200) and one row per critical risk: `key`, `risk`, `likelihood`, `impact`,
`mitigation`, as plain text. This is the one composed step of the export, and it is bounded: the
rows are few (the severity and Proposed-ADR rules ran first) and short. Write
`.cache/sa-skills/export/risk-summaries.json` yourself, in one `Write`, as
`{ "rows": [{ "key", "risk_plain", "mitigation_plain" }] }`, one entry per requested key:

- **`risk_plain`** — what could happen and what it costs the business, for a reader who knows the
  initiative and not the system. **`mitigation_plain`** — what is being done and who decides.
- **≤ 200 characters each**, one sentence or two, in `doc_language` (the translator handles the
  export language afterwards). Plain text: no Markdown link, no code span, no line break.
- **From the row, nothing invented.** No container, protocol, tool or ADR id unless the forum
  needs it to act — say "the movements screen", not the container's canonical name; say "the
  operational plan", not a section number. Likelihood and impact are not yours: the assembler keeps
  the row's own cells.

Then re-run Step A.3b with `--risk-summaries .cache/sa-skills/export/risk-summaries.json` (and
the same flags, `--plain` included). The receipt then reads `Risk summaries: N/N applied`; a summary that breaks a
rule is **refused** and named (`row 2: risk_plain 231 chars > 200 — original kept`), the source
row stays, and you fix that entry and re-run once. The reference keeps the source rows untouched;
the rewrite exists only in the briefing.

### Step A.4 — Render, or spawn the translator

**Native export** (`export_language == doc_language`, the common case): run `generate-doc.js`
twice yourself — the two commands of the agent's Step SA.4 with `--input
.cache/sa-skills/export/sa-briefing.md` and `sa-reference.md` — and go to Step A.5. No sub-agent.

**Translated export**: invoke `sa-delivery:generators:docs-export-generator` with a prompt providing:

- `job_type: solution-architecture`
- `plugin_dir: <absolute path from Step 0>`
- `sa_skills_dir: <absolute path from Step 0>`
- `project_dir: <CWD>`
- `doc_language: <en|es>` (resolved per "Documentation Language" above; default `en`)
- `export_language: <en|es>` (resolved at Step 0.6; defaults to `doc_language`)
- `lang_suffix: <"" | -en | -es>` (empty when native; `-<export_language>` when translated)
- `solution_name_slug: <from Step A.3>`
- `optional_sources: <JSON object from Step A.1b — {"TRACEABILITY_REPORT.md": "present", "analysis/TECH_DEBT": "analysis/TECH_DEBT-2026-08-14.md", ...}>`
- `items: <JSON array of absolute ADR file paths from Step A.2>`

- `parts_dir: <project_root>/.cache/sa-skills/export/parts` — the agent translates one part per `Write` into `parts-<export_language>/`, holds them to their source with `scripts/translation-check.js` (a dropped row, a lost identifier or a converted number fails, and the part is re-translated once), joins them with `cat`, and runs the two `generate-doc.js` commands.

Wait for the sub-agent's `EXPORT_RESULT:` block, then report to user.

### Step A.5 — Report (orchestrator)

Parse the sub-agent's `EXPORT_RESULT:` block and display:

```
✅ Solution Architecture Export Complete

   exports/SA-<solution-name>.docx            (Stakeholder briefing — PO · Chapter Leads · Technical Owners)
   exports/SA-<solution-name>-reference.docx  (Architecture reference — the detail the briefing cites)
   exports/ADR-001-<title>.docx             (Architecture Decision 001)
   exports/ADR-002-<title>.docx             (Architecture Decision 002)
   ...

   Briefing coverage:
     One page           summary ✅ (4 statements) · metrics ✅ (6 measures) · lead lines 10/10
     Product Owner      coverage ✅ · risks ✅ (4 critical, 4 rewritten for the forum)
     Chapter Leads      tech stack ✅ · currency ⬜ (no analysis/TECH_DEBT-*.md) · conformance ✅
     Technical Owners   capability scope ⬜ (no BIAN_ALIGNMENT.md) · integrations ✅ · operations ✅
```

The coverage block names every gap the briefing carries, so the architect learns what is thin
**before** circulating it rather than from the first reader who notices. Mark `✅` when the source
was present and `⬜ (no <file>)` when it was not — the same absent-versus-empty distinction the
briefing itself makes in place of the missing subsection.

If `status: PARTIAL` or `FAILED`, list the failures from the result block.

---

## Workflow B — Export Handoff Kit

**Trigger phrases**: "export handoff", "export dev handoff", "export handoff kit", "export <component-name> to Word"

The source is the four-part Service Handoff Kit produced by
`/skill architecture-dev-handoff` (TEMPLATE_VERSION 4.0.0+). The four parts have different
cardinality, and the export mirrors that exactly:

| Part | Cardinality | Source |
|------|-------------|--------|
| System Runtime View | 1 per project (shared) | `handoffs/SYSTEM_RUNTIME_VIEW.md` |
| Cross-Cutting Standards | 1 per project (shared) | `handoffs/CROSS_CUTTING_STANDARDS.md` |
| Interface Contract | 1 per adjacent-service edge | `handoffs/interfaces/<upstream>→<downstream>.md` |
| Component Specification | 1 per C4 L2 component | `handoffs/components/NN-<slug>.md` |

**Packaging rule — shared once, component parts per component.** The two shared documents
export **once** as their own `.docx` files. Each component package carries only that
component's Interface Contracts + Component Specification, prefixed with a fixed cross-reference header pointing at
the two shared files. This is deliberate: bundling the shared pair into every component
export would ship N byte-identical copies of the same two documents. The trade-off is that a
component package is **not self-contained** — it must be delivered alongside the two `KIT-*`
files.

### Step B.1 — Discover the kit and present the menu (orchestrator, by code)

```bash
bun [plugin_dir]/skills/architecture-docs-export/scripts/handoff-export.js <project_root> --list
```

It globs the four parts under `handoffs/`, maps each seam to the two components on either side of its
arrow (a seam appears in both packages — both sides are bound by its mutual assumptions), names every
component by its canonical name (`component-facts.ts`, else the specification's H1), numbers the menu —
shared documents, component packages with their seam counts, individual seams — and names a missing
shared part. Show its output to the user as the menu. An older layout (the 3.x
`SYSTEM_EKONTE.md` / `SETTEI.md` / `seams/` / `cut-sheets/`, or v2 `handoffs/*-handoff.md`) is named and
not exportable: tell the user to re-run `/skill architecture-dev-handoff`, which migrates it; an empty
`handoffs/` means the kit has not been generated yet. A partial kit is exportable.

Selections: `all` (shared documents + every component package — recommended for a full handoff),
`shared`, `components`, or numbers / ranges (`1, 3-5`; individual seams are chosen by number).

### Step B.2 — Export (orchestrator, by code)

```bash
bun [plugin_dir]/skills/architecture-docs-export/scripts/handoff-export.js <project_root> --select <selection> [--lang <export_language>]
```

The solution slug comes from the H1 of `docs/01-system-overview.md` (`--slug` overrides it), the
document language from `ARCHITECTURE.md`. **Native** (`--lang` absent or equal to `doc_language`): the
script renders every selected item with `generate-doc.js --type handoff` — the two shared documents
as `KIT-01-runtime-view-<slug>.docx` / `KIT-02-standards-<slug>.docx`, a seam as
`INTERFACE-<up>-to-<down>.docx` (never the `→` in a file name), a component package as
`HANDOFF-<slug>.docx`: a fixed cross-reference header to the two `KIT-*` files, then the component's
Interface Contracts and its Component Specification pasted byte for byte (a component with no seam gets
the `[NOT DOCUMENTED — …]` line). It removes its composed files and prints the report — show it as the
result. **Translated**: the script lays the parts out under `.cache/sa-skills/export/handoff/parts/` and
stops with `status: TRANSLATE`; go to Step B.3.

### Step B.3 — Translated export only: spawn the sub-agent

Invoke `sa-delivery:generators:docs-export-generator` with:

- `job_type: handoff`
- `plugin_dir`, `sa_skills_dir`: from Step 0
- `project_dir: <CWD>`
- `doc_language`, `export_language`: from Step 0.6
- `parts_dir`: the `parts` path the script printed; `translated_dir`: its `translate_to` path

The agent writes each part, translated, into `translated_dir` under the same file name. Then render:

```bash
bun [plugin_dir]/skills/architecture-docs-export/scripts/handoff-export.js <project_root> --render-translated
```

which renders every part with `--translated-from <doc_language>` and the `-<export_language>` suffix,
and prints the report.

Component packages are **not self-contained** — each cross-references the two `KIT-*` documents; the
report says so, and they are delivered together.

---

## Document Styling

| Document | Type Code | Color | Purpose |
|----------|-----------|-------|---------|
| Stakeholder Briefing | `SA` | Corporate blue `#1F4E79` | Role-routed architecture deliverable |
| ADR-*.md | `ADR` | Amber/Gold `#8B6914` | Architecture decisions |
| handoff kit — all four parts | `HANDOFF` | Teal `#0D7377` | Dev team deliverables |

---

## Output Location

All exports land in `exports/` at the project root.

```
exports/
├── SA-payment-gateway.docx              ← Stakeholder briefing (PO · Chapter Leads · Technical Owners)
├── ADR-001-api-gateway-choice.docx      ← Individual ADR
├── ADR-002-database-selection.docx      ← Individual ADR
├── KIT-01-runtime-view-payment-gateway.docx ← System Runtime View (shared, once)
├── KIT-02-standards-payment-gateway.docx        ← Cross-Cutting Standards (shared, once)
├── HANDOFF-payment-api.docx                  ← Interface Contracts + Component Specification for one component
├── HANDOFF-user-service.docx
└── INTERFACE-api-gateway-to-payment-api.docx ← one Interface Contract, when chosen by number
```

---

## Dependency Check

If the sub-agent reports `docx: not installed` (or off its pin), run `bun install` in sa-skills' directory — the workspace root, not `tools/docgen`:

```bash
cd "$sa_skills_dir" && bun install
```

Only needed once per plugin install.

---

## Prerequisites

- `docs/01-system-overview.md` and `docs/components/README.md` created by `/skill architecture-docs`
- ADR files created by `/skill architecture-definition-record`
- Four-part handoff kit created by `/skill architecture-dev-handoff` (TEMPLATE_VERSION 4.0.0+) (required for Workflow B). Legacy v1/v2 `handoffs/*-handoff.md` files are **not** exportable — re-run the dev-handoff skill to migrate first.

---

## Permissions required

Add to project `.claude/settings.json`:

```json
"Bash(bun *)",
"Bash(rg *)",
"Bash(mkdir *)",
"Bash(rm *)",
"Edit(exports/*)",
"Read(exports/*)",
"Read(analysis/*)",
"Read(handoffs/**)",
"Agent(sa-delivery:generators:docs-export-generator)"
```

`Read(analysis/*)` is used by Workflow A: the briefing's currency table comes from the newest Tech Debt report.

`Read(handoffs/**)` is used by Workflow B to show the kit's parts when the user asks about one; the
script reads them itself. The `**` glob is required — Interface Contracts and Component Specifications
live in subdirectories.

`Bash(rm *)` is used by the sub-agent to clean up the temporary files of a translated Solution
Architecture export (`sa-briefing.md`, `sa-reference.md`); `handoff-export.js` removes its own.

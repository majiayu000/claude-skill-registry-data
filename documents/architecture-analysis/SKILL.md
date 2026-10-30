---
name: architecture-analysis
description: >
  Run risk and design-characteristics analyses over an existing architecture: "run architecture
  analysis", "SPOF analysis", "blast radius analysis", "STRIDE threat model", "cost hotspot
  analysis", "tech debt analysis", "security posture", "all analyses". Ten lenses — SPOF, Blast
  Radius, Bottleneck, Cost Hotspots, STRIDE, Vendor Lock-in, Latency Budget, Tech Debt/EOL,
  Coupling, Data Sensitivity — one, a group or all ten, plus a Security Posture checklist that
  merges STRIDE and Data Sensitivity. Writes dated reports under analysis/ (Markdown or
  interactive HTML). Requires ARCHITECTURE.md. Not for compliance contracts
  (architecture-compliance) or ADRs (architecture-definition-record).
triggers:
  - run architecture analysis
  - SPOF analysis
  - blast radius analysis
  - STRIDE threat model
  - cost hotspot analysis
  - tech debt analysis
  - security posture
  - security posture validation
  - all analyses
---

# Architecture Analysis Skill

## Purpose

This skill produces **risk and design-characteristics analyses** over an architecture's documentation — the kind of assessments that come out of an architecture review meeting, pre-incident review, or release-readiness audit.

It bundles **ten focused analyses** across two groups, each driven by a dedicated spec and a universal sub-agent:

**HIGH-priority (runtime / security risk):**

| # | Analysis | Lens | Output |
|---|----------|------|--------|
| 1 | **SPOF** | Single points of failure → full outage / degradation / operational | `analysis/SPOF-<date>.md` |
| 2 | **Blast Radius** | Per-component downstream cascade impact | `analysis/BLAST-RADIUS-<date>.md` |
| 3 | **Bottleneck** | Throughput chokepoints and capacity headroom | `analysis/BOTTLENECK-<date>.md` |
| 4 | **Cost Hotspots** | Pareto cost concentration and over-provisioning | `analysis/COST-HOTSPOTS-<date>.md` |
| 5 | **STRIDE** | Security threats per trust boundary | `analysis/STRIDE-<date>.md` |

**Strategic / sustainability:**

| # | Analysis | Lens | Output |
|---|----------|------|--------|
| 6 | **Vendor Lock-in** | Portability risk, exit cost, vendor concentration | `analysis/VENDOR-LOCKIN-<date>.md` |
| 7 | **Latency Budget** | Per-hop SLO decomposition, over-budget hops | `analysis/LATENCY-BUDGET-<date>.md` |
| 8 | **Tech Debt / EOL** | Technology currency, deprecated SDKs, ADR debt | `analysis/TECH-DEBT-<date>.md` |
| 9 | **Coupling** | Fan-in/fan-out, instability, cyclical dependencies | `analysis/COUPLING-<date>.md` |
| 10 | **Data Sensitivity** | PII data flows, encryption gaps, retention limits | `analysis/DATA-SENSITIVITY-<date>.md` |

**Distinct from:**
- `architecture-compliance` — generates the compliance contracts. This skill produces architectural risk reports and reads nothing they write.
- `architecture-traceability` — maps PO Spec use cases to architecture sections. This skill has no dependency on a PO Spec.

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

**In this skill**: report headings, findings prose, recommendations, and the visible strings in the HTML report and its d3 visualization are authored in `doc_language`. Classification codes stay English in every language — the sensitivity tiers `S1`–`S4`, the STRIDE letters and category names, severity values (`Critical` / `High` / `Medium` / `Low`), the `<TYPE>-<YYYY-MM-DD>` filename, and every component canonical name. **Table column headers stay exactly as the spec spells them in every language** — `| # | Component | Failure Scenario | Impact | Current Mitigation |` under `es` as under `en`; a report with `| # | Componente | Escenario de falla | …` is off-policy (`LANGUAGE_POLICY.md` §4, "Table column headers"). Cell contents localize, the header row does not. Pass `doc_language` to each `architecture-analysis-agent` spawn.

Structural headings this skill writes carry their English anchor comment in both languages
(`## Heading <!-- SECTION: English Name -->`). The full do-not-localize registry — codes, status
enum values, table column headers, filenames, marker names, `EXPLORER_HEADER` field keys — is
`LANGUAGE_POLICY.md` §4.

---

## When to Invoke This Skill

- Before a release-readiness review or architecture gate
- During an annual architecture audit
- After a major architectural change (new component, ADR superseded, Redis removed, etc.)
- Pre-incident risk assessment or chaos engineering planning
- User asks: "find my SPOFs", "blast radius analysis", "where are my bottlenecks", "cost analysis of my architecture", "threat model my architecture", "run all analyses"
- Use `/skill architecture-analysis`

**Do NOT invoke for:**
- Compliance contract generation → `architecture-compliance`
- Requirements traceability → `architecture-traceability`
- ADR creation or update → `architecture-definition-record`

---

## Files in This Skill

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — dispatcher, menu, orchestration |
| `analyses/SPOF.md` | Classification rules and report spec for SPOF analysis |
| `analyses/BLAST_RADIUS.md` | Classification rules and report spec for Blast Radius analysis |
| `analyses/BOTTLENECK.md` | Classification rules and report spec for Bottleneck analysis |
| `analyses/COST_HOTSPOTS.md` | Classification rules and report spec for Cost Hotspots analysis |
| `analyses/STRIDE.md` | Classification rules and report spec for STRIDE Threat Model |
| `analyses/VENDOR_LOCKIN.md` | Classification rules and report spec for Vendor Lock-in analysis |
| `analyses/LATENCY_BUDGET.md` | Classification rules and report spec for Latency Budget analysis |
| `analyses/TECH_DEBT.md` | Classification rules and report spec for Tech Debt / EOL analysis |
| `analyses/COUPLING.md` | Classification rules and report spec for Coupling / Fan-out analysis |
| `analyses/DATA_SENSITIVITY.md` | Classification rules and report spec for Data Sensitivity & Flow analysis |
| `analyses/SECURITY_POSTURE.md` | Consolidation spec — merges the STRIDE + Data Sensitivity reports into a reviewer-fillable Security Posture validation checklist (markdown-only) |
| `templates/analysis-report-skeleton.md` | Shared section structure for all Markdown analysis reports |
| `templates/analysis-report-html-skeleton.html` | Shared HTML shell (d3.js v7 + d3-sankey, corporate styling) for the HTML output mode |
| `templates/viz/<analysis_type>.html` | One self-contained d3 viz snippet per analysis type (10 files); inlined into the HTML shell at render time |
| `analyses/plans/<lens>.json` | The **shape** of each lens's report — sections in order, anchors, titles in both languages, columns as the spec spells them, id schemes, heat-map axes, charts; `plans/README.md` is the plan and fill contract |
| `scripts/analysis-prepare.js` | Step 2.5 — cuts one payload per lens (plan, spec, ledger facts, computed graph / latency / deployment / load-model metrics, prior findings, explorer excerpts) plus the documents bundle; the explorer vocabulary lives here |
| `scripts/render-analysis.js` | The agent's fill × the plan → the report (Markdown or HTML with the d3 viz), the SPOF cross-references joined into Blast Radius, then `check-report.js` on the result |
| `scripts/security-posture.js` | Step 3.5 — the Security Posture checklist consolidated from the STRIDE and Data Sensitivity reports by code |
| `scripts/findings.js` | The **findings contract** as code — the one parser of every findings table (Markdown) and `const data` literal (HTML): id grammar, per-lens id schemes, the naming-column rule, the severity registries. The command center's `dossier.js` reads reports through this module, so what the check accepts is what Alia reads |
| `scripts/check-report.js` | `bun <skill_dir>/scripts/check-report.js analysis/` — verifies every report against the contract (§ Finding IDs); exit 1 on a violation. Run by the agent on its own report (Phase 6.5) and by Step 4 over the run |
| `tests/findings.test.ts` | The contract's tests — every lens's table shapes accepted, every violation named |
| `tests/render-analysis.test.ts` · `tests/security-posture.test.ts` | Every plan × a synthetic fill renders and passes the contract (Markdown, HTML, both languages); the consolidation's rows, missing-source rule and language |

---

## Step 0 — Resolve Plugin Directory

This skill ships in the **sa-analysis** plugin (`sa-skills` depends on it and installs it). Resolve both directories — one call each, never a Glob over `~/.claude/plugins/cache/` (it keeps every version ever installed and a glob returns an arbitrary one):

```bash
plugin_dir=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-analysis)
sa_skills_dir=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts)
```

`[plugin_dir]` is sa-analysis' install (this skill's scripts, plans and specs); `[sa_skills_dir]` is sa-skills' — the architecture is read through its facts ledger, explorer, judge and findings contract, which the scripts find on their own (`scripts/sa-skills.js`: `--sa-skills`, `SA_SKILLS_DIR`, the repo layout, the install registry) and stop with the install command when sa-skills is absent. The script answers from Claude Code's install registry — the project-scope install for this directory, else the user-scope one, else the copy it runs from — and warns on stderr when a newer version is on the machine (`claude plugin update … --scope <scope>`, then `/reload-plugins`); show that warning to the user. Without the marketplace clone (a dev clone alone): Glob `**/{sa-skills,solutions-architect-skills}/.claude-plugin/plugin.json` **outside** `~/.claude/plugins/cache/`, strip `/.claude-plugin/plugin.json` for `sa_skills_dir` and append `/plugins/sa-analysis` for `plugin_dir`.

Store `plugin_dir` and `sa_skills_dir` for use in all agent prompts. `[design_language_dir]` is the Design Language Standard in force — `bun [sa_skills_dir]/scripts/shared/packs.js --path design-language` prints it (an institution pack's — the base carries none) or prints nothing and exits 1: **fallback mode**; `analysis-prepare.js` resolves it on its own and cuts it into each payload.

---

## Step 1 — Locate Architecture Document

Search for `ARCHITECTURE.md` at the project root. Determine doc structure:

- **Multi-file**: `ARCHITECTURE.md` exists as a navigation index + `docs/NN-*.md` section files + `docs/components/` per-component files
- **Monolithic**: a single `ARCHITECTURE.md` file containing all sections

If no `ARCHITECTURE.md` is found, abort:
```
❌ No ARCHITECTURE.md found. Use /skill architecture-docs to create one first.
```

Build `doc_files` — an ordered list of absolute file paths to pass to each agent:
1. `ARCHITECTURE.md` (always)
2. `docs/NN-*.md` section files in numeric order (if `docs/` exists)
3. `docs/components/README.md` and `docs/components/**/*.md` in numeric order
4. All `adr/ADR-*.md` files in alphabetic order

---

## Step 2 — Select Analyses (BLOCKING — user must choose)

Present the analysis menu. If the user says "analyze my architecture" without specifying which, present this menu:

```
═══════════════════════════════════════════════════════════
Architecture Analysis — choose analyses to run:
═══════════════════════════════════════════════════════════

  HIGH-priority (runtime / security risk):
   1. SPOF             (Single Points of Failure)        1 agent
      Critical, Degradation, and Operational failure modes with Heat Map

   2. Blast Radius     (Downstream cascade impact)       1 agent
      Per-component fan-out, cascade severity, bulkhead assessment

   3. Bottleneck       (Throughput chokepoints)          1 agent
      Serial chokepoints, connection saturation, capacity headroom

   4. Cost Hotspots    (Cost concentration)              1 agent
      Pareto cost ranking, over-provisioning candidates, vendor lock-in cost

   5. STRIDE           (Security threats per boundary)   1 agent
      Per-trust-boundary STRIDE matrix, high-priority threats

  Strategic / sustainability:
   6. Vendor Lock-in   (Portability risk, exit cost)     1 agent
      L1/L2/L3 lock tiers, vendor concentration, exit cost ranking

   7. Latency Budget   (Per-hop SLO decomposition)       1 agent
      Per-flow budget breakdown, over-budget hops, tail-latency variance

   8. Tech Debt / EOL  (Currency, deprecated tech)       1 agent
      EOL hotlist, deprecated SDKs, unimplemented ADR replacements

   9. Coupling         (Fan-in/fan-out, cycles)          1 agent
      Critical hubs, volatile leaves, god objects, cyclical dependencies

  10. Data Sensitivity (PII flow, encryption gaps)       1 agent
      Data inventory, encryption/retention gaps, sensitive flow map

  11. All ten (parallel)                                  10 agents

  Consolidated (security):
  12. Security Posture (validation checklist)             1 agent
      Merges STRIDE (5) + Data Sensitivity (10) into one reviewer-fillable
      checklist of every security control to validate. Markdown-only.
      Requires the STRIDE and Data Sensitivity reports — runs them first if absent.

═══════════════════════════════════════════════════════════
Selection (e.g. "1", "1,3,5", "6-10", "12", or "all"):
```

**Parse user selection:**
- `all` or `11` → run analyses 1–10
- `1-5` → run only the HIGH-priority group (analyses 1–5)
- `6-10` → run only the Strategic group (analyses 6–10)
- `12` → run the **Security Posture** consolidation (see Step 2.6 — it depends on analyses 5 and 10)
- Comma-separated numbers → run only those analyses
- Single number → run one analysis

**Security Posture dependency**: whenever `12` is in the selection, analyses **5 (STRIDE)**
and **10 (Data Sensitivity)** must have produced reports first. See Step 2.6 for how the
orchestrator satisfies this (consume existing reports, or schedule 5 + 10 ahead of 12).

---

## Step 2.4 — Select Output Format (BLOCKING — user must choose)

After the analysis selection above, present the output format menu. **Do not assume.** The choice applies to **every** analysis dispatched in this run.

```
═══════════════════════════════════════════════════════════
Output format:
═══════════════════════════════════════════════════════════
   1. Markdown   analysis/<TYPE>-<date>.md
      Plain text, grep-friendly, default. ASCII heat maps / pipe tables.

   2. HTML       analysis/<TYPE>-<date>.html
      Interactive corporate-grade report rendered with d3.js v7
      (heat maps, dependency networks, Pareto charts, Sankey, chord, …).
      Loads d3.js from the jsDelivr CDN (cdn.jsdelivr.net) — internet required
      to view the visualisations. Tables/text render fine offline.

Selection (1 or 2):
═══════════════════════════════════════════════════════════
```

**One report per lens**: `analysis/` holds the newest report of each lens and nothing else. When a report
passes its check, `render-analysis.js` (and `security-posture.js` for the checklist) moves every earlier report of that
lens — any date on or before it, either format — to `analysis/archive/`, and prints what it moved. Never delete or move
a report by hand; `bun [sa_skills_dir]/scripts/shared/findings.js analysis --archive` tidies a folder that holds several reports of one lens.

**Parse user selection:**
- `1` or `markdown` or `md` → `output_format = "markdown"`
- `2` or `html` → `output_format = "html"`

Store `output_format` for use in Step 3 agent prompts. If anything else is entered, re-prompt.

**Security Posture is markdown-only**: analysis 12 has no HTML/d3 viz mode (it is a
worksheet, not a visualization). If the user selected `12` *and* chose HTML, run analysis 12
in markdown regardless and tell the user: "Security Posture is a validation checklist —
exported as markdown; the HTML format applies to the other selected analyses." Any
non-consolidation analyses in the same run still honor the chosen format.

---

## Step 2.6 — Security Posture dependency resolution (only when analysis 12 is selected)

Security Posture (`security-posture`) is a **consolidation** — it reads the `STRIDE` and
`Data Sensitivity` reports rather than the architecture docs. Before dispatching it:

1. **Locate the source reports** — glob `analysis/STRIDE-*.md` and
   `analysis/DATA-SENSITIVITY-*.md`; pick the most recent date for each.
2. **Satisfy missing sources**:
   - If the user also selected 5 and/or 10 in this run, let those run first (Step 3 dispatches
     every non-consolidation analysis, Step 3.5 consolidates after they return); use their fresh
     outputs.
   - If a source report is **not** selected and **not** found on disk, **add that analysis to
     this run** (STRIDE and/or Data Sensitivity, markdown) so it executes ahead of 12, and
     tell the user: "Security Posture requires the <STRIDE|Data Sensitivity> report — running
     it first."
   - If a source report is **not** selected but **already exists** on disk (any prior date),
     consume the most recent on-disk file as-is (do not re-run it).
3. **Record the resolved source paths** for the Step 3 dispatch of analysis 12.

Security Posture runs **last and by code** — Step 3.5, after STRIDE and Data Sensitivity have
written their reports in this run (or after confirming the on-disk files exist).

---

## Step 2.5 — Cut the payloads (code, once per run)

Run `analysis-prepare.js` once for every selected lens, in one Bash call:

```bash
bun [plugin_dir]/skills/architecture-analysis/scripts/analysis-prepare.js <project_root> --lens <a,b,c|all> --today <YYYY-MM-DD> --format <md|html>
```

It writes, under `.cache/sa-skills/analysis/`, per lens: `<lens>.payload.md` (the plan — the
report's shape from `analyses/plans/<lens>.json`; the spec's classification rules; the ledger
facts the lens cites — components with their canonical names, integrations, layers, flows and
phases, demand, TDRs, ADRs; the metrics computed from them — the dependency graph with fan-in,
fan-out, instability, direct and transitive dependents and cycles, the sum of every flow's phase
budgets against its target, the deployment inventory and the load model from the newest command
center scene; what the other lenses' latest reports already registered on each component; the
explorer's excerpts for the lens's vocabulary), `<lens>.docs.md` (ARCHITECTURE.md plus the prose
documents the plan names, whole) and `<lens>.facts.json`; and `_run.json`, the manifest. It prints
one line per lens — payload and document bytes, the explorer's status — and the inputs it could
not find (no scene: no deployment inventory and no load model; the analysis still runs).

The lens vocabulary the explorer takes lives in the script (`VOCAB`), not here. **Exclude
`security-posture`**: it is consolidated by code in Step 3.5 and has no payload.

**Degraded mode**: the script exits non-zero only when `ARCHITECTURE.md` is missing (Step 1 caught
that). A lens whose explorer call failed still gets its payload with `_explorer FAILED_` in the
excerpts section; the documents bundle carries what the judgement needs.

---

## Step 3 — Spawn Analysis Agents (Parallel)

For each selected lens (never `security-posture`), read its entry in
`.cache/sa-skills/analysis/_run.json` (`payload`, `docs`, `fill`, `output`) and dispatch:

```
subagent_type: sa-analysis:reviewers:architecture-analysis-agent

Prompt:
analysis_type: <lens>
payload_path: <absolute path to .cache/sa-skills/analysis/<lens>.payload.md>
docs_path: <absolute path to .cache/sa-skills/analysis/<lens>.docs.md>
fill_path: <absolute path to .cache/sa-skills/analysis/<lens>.fill.json>
render_command: bun [plugin_dir]/skills/architecture-analysis/scripts/render-analysis.js <fill_path> --project <project_root> --format <md|html> --today <YYYY-MM-DD>
output_format: <markdown|html>
doc_language: <en|es>
today: <YYYY-MM-DD>
```

Nothing else — no `FILES:`, no spec or skeleton path: the payload carries them. Payload and documents
are written in parts of at most ~38 KB (Claude Code's Read returns 25,000 tokens at most); part 1's
reading list names every part in order, and the agent reads each once, whole. The agent reads the
parts, writes the fill, runs the render command (which validates the fill, writes
`analysis/<LENS>-<date>.<ext>` and runs the findings contract on it) and returns one summary line.
Set each `description` to `"<Analysis Name> analysis"`.

| Analysis | `analysis_type` | Output filename |
|----------|----------------|-----------------|
| SPOF | `spof` | `SPOF-<date>.md` |
| Blast Radius | `blast-radius` | `BLAST-RADIUS-<date>.md` |
| Bottleneck | `bottleneck` | `BOTTLENECK-<date>.md` |
| Cost Hotspots | `cost-hotspots` | `COST-HOTSPOTS-<date>.md` |
| STRIDE | `stride` | `STRIDE-<date>.md` |
| Vendor Lock-in | `vendor-lockin` | `VENDOR-LOCKIN-<date>.md` |
| Latency Budget | `latency-budget` | `LATENCY-BUDGET-<date>.md` |
| Tech Debt / EOL | `tech-debt` | `TECH-DEBT-<date>.md` |
| Coupling | `coupling` | `COUPLING-<date>.md` |
| Data Sensitivity | `data-sensitivity` | `DATA-SENSITIVITY-<date>.md` |
| Security Posture | — (Step 3.5, code) | `SECURITY-POSTURE-<date>.md` (markdown-only) |

**Model per lens**: the agent's frontmatter pins `opus`; pass `model: sonnet` in the `Task()` call
for the inventory-heavy lenses — `vendor-lockin`, `tech-debt`, `cost-hotspots`, `coupling`,
`latency-budget`, `bottleneck` — whose judgement sits on tables the payload already computed;
keep `opus` for `spof`, `blast-radius`, `stride` and `data-sensitivity`.

**Dispatch every selected lens in one message** — one `Task()` call per lens, no batch cap and no
ordering between them. The agents share nothing: each reads its own payload, writes its own fill
and renders its own report.

**The one dependency is joined afterwards, by code**: the Blast Radius renderer marks the rows that
are also single points of failure (`⚡ SPOF+Blast`) by reading the SPOF report on disk, and in one
wave that report may not exist yet when Blast Radius renders. Step 3.4 re-renders Blast Radius once
every agent has returned, so the join lands whatever order the agents finished in.

**[BARRIER — wait for every dispatched agent to return before proceeding to Step 3.4]**

---

## Step 3.4 — Join the SPOF cross-references (code, only when `spof` and `blast-radius` both ran)

Re-run the Blast Radius render command from `_run.json` — same fill, same flags:

```bash
bun [plugin_dir]/skills/architecture-analysis/scripts/render-analysis.js \
  .cache/sa-skills/analysis/blast-radius.fill.json --project <project_root> \
  --format <md|html> --today <YYYY-MM-DD>
```

It re-reads the fill from disk and the newest `analysis/SPOF-*.md` and rewrites the same report
file, so the pass is idempotent — a row already carrying `(SPOF …)` is left untouched. The line it
prints (`… · <n> SPOF cross-reference(s) from analysis/SPOF-<date>.md`) is the receipt; `0` with
both reports present is a naming mismatch to report, not a failure. Skip the step when either lens
was not part of this run — Blast Radius already joined against whatever SPOF report was on disk.

---

## Step 3.5 — Security Posture (code, only when analysis 12 is selected)

After every agent has returned (Step 2.6 resolved the sources), run:

```bash
bun [plugin_dir]/skills/architecture-analysis/scripts/security-posture.js <project_root> --today <YYYY-MM-DD>
```

It reads the newest `analysis/STRIDE-*.md` and `analysis/DATA-SENSITIVITY-*.md`, turns every
matrix cell and every required control of the S1 / S2 stores into a checklist row per
`analyses/SECURITY_POSTURE.md`, reuses the source reports' recommendation prose for the
priorities, carries their gaps forward, leaves `Status` / `Owner` / `Evidence` empty for the
reviewer, and writes `analysis/SECURITY-POSTURE-<date>.md` in the architecture's language. One
source missing: the other is consolidated and the gap recorded; both missing: it aborts with the
message to run analyses 5 and 10 first. No agent is involved — the spec is a merge.

---

## Step 4 — Collect Results and Report

After all agents return, collect each agent's one-line summary.

**Check for failures**: if any agent failed to produce an output file, report:
```
⚠️ <Analysis Name> agent failed — <error summary>
   You can re-run this analysis by selecting option <N> again.
```

**Findings Contract Check** (BLOCKING — every format, every `doc_language`): each report just written must satisfy § Finding IDs, the format the command center's dossier reads. The renderer already ran it per report; this pass is the run-level receipt. Run once over the run's reports:

```bash
bun <plugin_dir>/skills/architecture-analysis/scripts/check-report.js analysis/*-<YYYY-MM-DD>.md analysis/*-<YYYY-MM-DD>.html
```

The script prints one line per report — `✓ analysis/BOTTLENECK-<date>.md: 11 finding(s) — 2 critical · 5 high · 4 medium` — and, under a `✗` report, every violation with its line: a table whose rows open with something other than a finding id (a marker before the id), an id outside the lens's scheme (`B1` in a Bottleneck report), a findings table with no naming column so the finding would be labelled by its Tier cell, a finding with no severity source, a localized header row. Exit 1 means at least one report is unreadable to Alia. The agent already ran the same check on its own report (Phase 6.5) and fixed what it found, so a `✗` here is a report the agent returned broken: show the violations verbatim, then **fix the rows named in place** (the id cell, the header row, a missing column — cells untouched otherwise) or re-run that one analysis; never silently, never by editing the contract. Warnings (a finding named differently in two tables, an HTML object without an id) are reported and do not block.

**Print completion summary** — file extension is `.md` when `output_format == "markdown"` and `.html` when `output_format == "html"` (same one-line summary content either way):

```
═══════════════════════════════════════════════════════════
✅ Architecture Analysis Complete  (format: <markdown|html>)
═══════════════════════════════════════════════════════════

  HIGH-priority analyses:
  analysis/SPOF-2026-04-16.<ext>              <n> critical · <n> degradation · <n> operational
  analysis/BLAST-RADIUS-2026-04-16.<ext>      <n> high-blast · <n> isolated components
  analysis/BOTTLENECK-2026-04-16.<ext>        <n> chokepoints · top: <component> (fan-in x<n>)
  analysis/COST-HOTSPOTS-2026-04-16.<ext>     top hotspot: <component> (<cost>)
  analysis/STRIDE-2026-04-16.<ext>            <n> high · <n> medium · <n> low priority threats

  Strategic / sustainability analyses:
  analysis/VENDOR-LOCKIN-2026-04-16.<ext>     <n> L1-locked · <n> L2-lock-prone · <vendor> <n>% concentration
  analysis/LATENCY-BUDGET-2026-04-16.<ext>    <n> flows over budget · top offender: <component> (+<n>ms)
  analysis/TECH-DEBT-2026-04-16.<ext>         <n> EOL-now · <n> EOL-within-6mo · <n> deprecated SDKs
  analysis/COUPLING-2026-04-16.<ext>          <n> critical hubs · <n> god objects · <n> cycles
  analysis/DATA-SENSITIVITY-2026-04-16.<ext>  <n> G1 encryption gaps · <n> G3 retention breaches

  Consolidated (when analysis 12 was selected):
  analysis/SECURITY-POSTURE-2026-04-16.md     <n> checks · <n> documented · <n> gaps (<n> high)

═══════════════════════════════════════════════════════════
Next steps:
  • Review reports in analysis/ — each finding includes source citations
  • Address Documentation Gaps entries to improve future analysis accuracy
═══════════════════════════════════════════════════════════
```

**When `output_format == "html"`**, append the following block before the context-reclaim hint:

```
💡 Open any report in your browser to explore the d3 visualisations:
     open analysis/SPOF-<date>.html        (macOS)
     xdg-open analysis/SPOF-<date>.html    (Linux)
     start analysis/SPOF-<date>.html       (Windows)

   The HTML reports load d3.js from the jsDelivr CDN — internet is required
   to render the charts. Tables, summaries, recommendations, and citations
   render fine offline; only the interactive viz needs the CDN.
```

**After printing the completion summary above, always append the following user-visible context-reclaim hint** (verbatim, as the final lines of the skill's output):

```
💡 Tip: all analysis reports are written to `analysis/`. To reclaim context from the analysis-agent responses before your next task, run:
    /compact
```

---

## Design Language Standard (conditional)

The SA Design Language Standard (`[design_language_dir]/`) is organization-specific; this skill tests for it and degrades gracefully when it is absent. Three analysis surfaces consume it when present — the wiring lives in the analysis specs, which the analysis agent reads:

| Surface | Spec | What the standard adds |
|---|---|---|
| Tag emission | `analyses/DATA_SENSITIVITY.md` | S1–S4 → `Data Classification` (1:1), `Data Category` values, a `Tags` column in the Data Inventory |
| Tag emission | `analyses/STRIDE.md` | zones → `Trust Zone`, auth → `Authentication` (§6 closed vocabularies); high-watermark and zone-inheritance violations become findings |
| Report Mermaid | `analyses/BLAST_RADIUS.md`, `analyses/COUPLING.md`, `analyses/DATA_SENSITIVITY.md` | the `llms-mermaid.txt` **syntax layer** binds every emitted block (`flowchart` never `graph`, `TB` never `TD`, quoting, operators, line ceiling), opened with an `%% Analysis exhibit` comment |

**Analysis exhibits are not registered views.** They carry no Diagram ID and no altitude, and their encodings — cascading/contained severity colours, per-hop protocol and encryption labels — are the analytical content. The standard's view-conformance layer (four-role palette `M-07`/`M-14`, the §12 Dynamic-view label regime, `M-12` Diagram IDs) does **not** apply to them, and applying it would delete the findings the report exists to show. Syntax governed; semantics free. When the folder is absent, every spec skips its standard subsection and reports free-text values only.

---

## Documentation Fidelity Rule

Every finding in every analysis report MUST cite the source file and section it was derived from (e.g., `(source: docs/08-scalability-and-performance.md — Section "HPA Configuration")`). Agents must NOT invent components, costs, trust boundaries, or risks not present in the architecture documentation. Where required data is absent, the finding is marked `[NOT DOCUMENTED — add to <source-file>]` and listed in a **Documentation Gaps** section at the report footer.

---

## Finding IDs

Every findings table in every report opens with a `#` column (the STRIDE boundary inventory uses `ID`) whose cell holds the **finding id** — the handle the heat map, the recommendations, the cross-references between reports and the command center's dossier all use. The grammar: one to three capitals, an optional tier digit, an optional hyphen, one to three digits, and — STRIDE threats only — a hyphenated category letter (`C1`, `B1`, `K2-01`, `T1-S`, `TB-01`). The id is the **first token of the cell**; a marker that applies to the row (`⚡ SPOF+Blast`) follows it in the same cell, never precedes it. Tables that list every component — the coupling metrics table, a per-flow hop budget, a data inventory — number their rows `1`, `2`, `3` and are **not** findings tables. A finding that appears in a second table (a hotlist, an exit-cost ranking, the STRIDE High-Priority table) keeps its id; it is never renumbered. `#` is a column header and stays English under every `DOC_LANGUAGE`.

| Lens | Findings tables | `#` | Dossier severity |
|---|---|---|---|
| SPOF | Critical / Degradation / Operational | `C1`, `D1`, `O1` … | C critical · D medium · O low |
| Blast Radius | High-Blast Components | `B1`, `B2` … (`B1 ⚡` when SPOF+Blast) | `Tier` column: S1 critical · S2 high · S3 medium · S4 low; else high |
| Bottleneck | Top Chokepoints, Scaling Risk, Fan-in Convergence | `B1-01`, `B2-01`, `B3-01`, `B4-01` | B1 critical · B2 high · B3, B4 medium |
| Cost Hotspots | Pareto, Qualitative Mentions, Over-Provisioning | `P-01`, `Q-01`, `O-01` | P medium · O low · Q info |
| STRIDE | Trust Boundary Inventory (`ID`), STRIDE Matrix, High-Priority Threats | `TB-01`; `T1-S`, `T2-R` … | `Severity` column; TB info |
| Vendor Lock-in | L1, L2, Exit Cost Ranking | `L1-01`, `L2-01` | L1 high · L2 medium |
| Latency Budget | Hops Over Budget, Tail-Latency Hotspots | `OB-01`, `TL-01` | `Severity` / `Risk` column |
| Tech Debt / EOL | Technology Currency, EOL Hotlist, Deprecated SDK Scan, Architectural Debt | `T1-01` … `T5-01`, `DEP-01`, `AD-01` | T1 critical · T2 high · T3 medium · T4 info · T5 low · DEP medium · AD `Risk` column |
| Coupling | K1–K4 | `K1-01`, `K2-01`, `K3-01`, `K4-01` | K1, K3, K4 high · K2 medium |
| Data Sensitivity | Encryption Gaps, Retention Gaps, Cross-Boundary Leakage | `G1-01`, `G2-01`, `G3-01`, `G4-01` | G1, G2 critical · G3, G4 high · G5 medium |

The last column is what `architecture-command-center/scripts/dossier.js` paints when a row has no `Severity` / `Risk` column and no `Tier` column: an explicit column always wins, the tier column next, this registry after it, the section title last. The report never carries a "dossier severity" column — the registry lives in `scripts/findings.js` (`PREFIX_SEVERITY`), which this table prints and the dossier requires.

### Mitigation, residual severity and the "what" column

The contract also reads, per lens, **the column that states what is in place against the finding** and **the column that says what the finding is about** beyond its subject — the subject (Component, Technology …) is the block's own name on the stage, so it says nothing there. Neither is a new rule for the writer: they are columns the specs already carry.

| Lens | Mitigation column (`none` / `present`) | "What" column |
|---|---|---|
| SPOF | `Current Mitigation` | `Failure Scenario` |
| Blast Radius | `Bulkhead Present` | `Cascade Risk` |
| Bottleneck | `Backpressure Mechanism` | `Bottleneck Reason` · `Scale Blocker` · `Backpressure Mechanism` |
| STRIDE | `Status` (`⚠️ Finding` none · `✅ Mitigated` / `Partial` present) | `Control / Gap` · `Threat Description` |
| Tech Debt / EOL | `Replacement Implemented?` | `Replacement` |
| Vendor Lock-in | `Exit Path` | `Proprietary Surface` · `Vendor Extension` · `Blocking Factor` |
| Coupling | — | `Risk Narrative` · `Classification` · `Coupling Type` |
| Cost Hotspots | — | `Category` · `Recommended Action` · `Estimated Monthly Waste` |
| Data Sensitivity | — | `Missing Control` · `Overage` · `Authorizing Decision` |
| Latency Budget | — | `Flow` |

A cell is `none` when it opens with a none-word (`None`, `No`, `N/A`, `[NOT DOCUMENTED]`, `Ninguna`, `Sin …`, `Pending`, `⚠️ Finding` …) and `present` otherwise — `Partial` and `Sí — …` count as present; the text is carried whole and the reader judges it. A present mitigation gives the finding a **residual severity one step below the report's** (critical → high → medium → low; info stays) — `residual` on the item, beside the untouched `severity`. The command center ranks, colours and orders by the residual and marks it `S→A` — the report's rank, then the residual — with the mitigation as its tooltip (`LV S→A`), drawing a mitigated finding's blocks hollow and an open one's filled; the finding page prints the report's severity, the mitigation and the residual rank side by side. A lens without a mitigation column invents nothing. Registries: `MITIGATION_COL`, `WHAT_COL`, `NONE_CELL` in `scripts/findings.js`; `mitigationOf`, `whatOf`, `residualSeverity`, `enrich` exported.

### The findings contract — what every report must satisfy

The dossier reads a report with `scripts/findings.js`, and `scripts/check-report.js` holds every report to the same parser before the skill accepts it (agent Phase 6.5, orchestrator Step 4). The rules, each a `✗` when broken:

| Rule | Why the dossier needs it |
|---|---|
| A findings table opens with `#` (`ID` for the STRIDE inventory) and a separator row; every other table is prose data | Only `#` / `ID` tables are read |
| The id is the **first token** of the first cell, in the lens's scheme above (`B1-01` in Bottleneck, never `B1`); a marker (`⚡ SPOF+Blast`) follows it; `—` marks a pass row; `1`, `2`, `3` an inventory | A cell that opens with anything else is skipped, and an id from another lens's scheme is painted with the wrong registry |
| Every findings table carries a **naming column** — `Component`, `Technology`, `Data Store`, `Threat`, `Trust Boundary`, `Cycle Path`, `Title` — and the finding's label is that cell | The label is the chip Alia shows and the name she resolves to a container; a Tier, Severity, Risk, Gap, Hop, Flow, Category or Status cell never labels |
| Every finding resolves a severity: a `Severity` / `Risk` column, a `Tier` column, or a prefix in the registry above | A finding with none is painted from the section title, which no report should rely on |
| A finding listed twice keeps its id and its subject; the second table adds columns | Two ids for one finding are two chips; two subjects for one id is a warning |
| Column headers are spelled as the spec spells them (English) under every `DOC_LANGUAGE`; only cells localize | The naming and severity columns are found by header (`LANGUAGE_POLICY.md` §4) |
| An HTML report embeds one `const data = { … };` literal (agent Step 5b.1) whose arrays of objects carry a label — `label`, `name`, `component` or `technology` | That literal is the only findings surface of an HTML report |
| The filename is `<LENS>-<YYYY-MM-DD>.md|html` with the lens slug of the table above | The lens picks the id scheme and the registry |

Spec table shapes already satisfy every rule; the check catches the report that drifted from its spec. `SECURITY-POSTURE-*` is a consolidation checklist with no findings tables and is skipped by design.

---

## Output Location

All analysis reports are written to `analysis/` at the project root. Files are date-stamped — re-running the same analysis on the same day with the same format overwrites the existing file; re-running on a new date creates a new file, preserving history. Re-running the same date with a different format produces a sibling file with the other extension (`.md` and `.html` can coexist).

```
analysis/
├── SPOF-2026-04-16.md            (or .html — chosen at Step 2.4)
├── BLAST-RADIUS-2026-04-16.md
├── BOTTLENECK-2026-04-16.md
├── COST-HOTSPOTS-2026-04-16.md
├── STRIDE-2026-04-16.md
├── VENDOR-LOCKIN-2026-04-16.md
├── LATENCY-BUDGET-2026-04-16.md
├── TECH-DEBT-2026-04-16.md
├── COUPLING-2026-04-16.md
├── DATA-SENSITIVITY-2026-04-16.md
└── SECURITY-POSTURE-2026-04-16.md   (consolidation of STRIDE + Data Sensitivity — markdown-only)
```

### HTML format notes

- HTML reports are **self-contained single files** — no sibling assets, no build step. Just open in a browser.
- d3.js v7 and d3-sankey are loaded from the jsDelivr CDN (`https://cdn.jsdelivr.net/npm/...`). **No internet** → tables and prose still render, but the viz `<div>` falls back to "Visualization unavailable without d3.js." A user-visible banner makes the fallback explicit.
- HTML mode is intended for socialisation with non-engineering stakeholders (architects, security, finance). Markdown mode remains the default for in-repo review, grep, and Word export via `architecture-docs-export`.
- The HTML and Markdown reports contain the **same findings** — no information is invented for the viz that isn't also in the findings tables.
- **Spec sections defined as ASCII heat maps, ASCII bar charts, ASCII histograms, or Mermaid diagrams are OMITTED in HTML mode** — the per-analysis d3 viz is the canonical HTML rendering of that content (see the agent's Phase 5b.0 omission table). Markdown mode renders the spec's ASCII / Mermaid blocks unchanged. Cascade scenarios (`blast-radius`) and cycle subgraphs (`coupling`) and per-flow sequence diagrams (`data-sensitivity`) are surfaced in HTML mode as HTML tables, not as hand-coded SVG.

---

## Prerequisites

- `ARCHITECTURE.md` created by `/skill architecture-docs`
- `docs/` directory with section files (multi-file architecture recommended for richer analysis)
- `docs/components/` with per-component files (required for Blast Radius and Bottleneck analysis)
- ADR files in `adr/` (optional — used to surface risk decisions)

---

## Permissions Required

Add to your project's `.claude/settings.json`:

```json
"Edit(analysis/*)",
"Read(analysis/*)",
"Bash(mkdir *)",
"Bash(bun *)",
"Bash(rg *)",
"Agent(sa-analysis:reviewers:architecture-analysis-agent)",
"WebSearch"
```

`Bash(bun *)` runs `analysis-prepare.js` (Step 2.5), `render-analysis.js` (the agent's Phase 3), `security-posture.js` (Step 3.5) and `check-report.js` (Step 4).

**`WebSearch` is required for the Tech Debt / EOL analysis.** The agent uses it to validate documented EOL dates against vendor product-lifecycle pages (`endoflife.date`, `learn.microsoft.com/lifecycle`, `nodejs.org`, etc.) — see `analyses/TECH_DEBT.md` § "EOL Validation Protocol". Other analyses (SPOF, Blast Radius, Bottleneck, Cost, STRIDE, Vendor Lock-in, Latency Budget, Coupling, Data Sensitivity) do not call WebSearch. If `WebSearch` is omitted, the Tech Debt analysis still completes but produces a `WebSearch unavailable` notice and may report stale EOL data.

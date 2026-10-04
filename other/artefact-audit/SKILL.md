---
name: "Artefact: Render Audit"
description: "Render verified findings as an actionable, status-grouped HTML artefact."
when_to_use: "When findings need a shareable visual surface: roadmap-review and project-audit_deps hand off here, any in-conversation findings can be mapped into its schema, and render-only mode rebuilds the page from a saved dataset JSON."
model: sonnet
effort: high
metadata:
  glyph: ᛊ
  family: artefact
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash(open:*)", "Bash(mkdir:*)", "Bash(python3:*)"]
argument-hint: "[label for in-hand findings | path to a findings JSON]"
---

Render verified findings as a self-contained, actionable HTML page: grouped by delivery status, ranked by severity, each verified before it ships. Uses the visual-explainer plugin's rendering patterns.

The output is the audit artefact this skill was distilled from: a masthead + KPI row, findings grouped into collapsible **To do / In progress / Done** sections, severity shown on both a chip and the colour of each finding number, a severity/type filter bar and a refuted section that keeps the audit falsifiable.

## Step 1: Interpret `$ARGUMENTS` (auto-detect)

- **A path to a `.json` file** (matches something like `*.json` and the file exists): **render-only mode**. Load it as the findings dataset and skip to Step 3. Expected shape is documented in Step 2.
- **Anything else, or empty**: the findings themselves come from a feeder skill's hand-off (`roadmap-review`, `project-audit_deps`) or from findings already established in the conversation; `$ARGUMENTS` supplies the label/slug when given. This skill renders findings; it does not investigate topics. If someone hands it a bare topic with nothing behind it, say so and point at the feeder skills.

## Step 2: Assemble the dataset

Map the in-hand findings into the schema below, verifying each claim still holds before including it.

Each finding must carry:

- `id`: stable integer, assigned once, never reused
- `title`: one sentence stating the defect
- `category`: one of `correction` (the source says something false/stale), `issue` (a real problem), `improvement` (reduces risk/effort), `enhancement` (valuable addition currently missing)
- `severity`: `high` | `medium` | `low`
- `evidence`: file:line references, quoted text or command output; no speculation as fact
- `file_refs`: array of repo-relative paths (with optional `:line`)
- `recommendation`: a single concrete action, not a theme
- `anchor`: 2-4 word imperative label for the action (e.g. "Split the gate")
- `theme`: a short grouping label (secondary axis, shown as a card tag)
- `confidence`: `high` | `medium` | `low` from the verification pass
- `status`: `to_do` | `in_progress` | `done` (see below)
- `outcome_note`: one sentence on what was done, or why it is where it is
- `verify_notes`: what a skeptic checked and found; corrections to the finding's own evidence belong here

**Verify before including.** For each candidate finding, check its evidence actually holds against the current tree and history. Default to dropping it if the evidence is ambiguous. Keep the dropped ones in a `refuted` list (title + why) so the artefact is honest about what did not survive.

**Status semantics** (be honest; status reflects reality, not intention):

- `done`: the fix was applied in this pass
- `in_progress`: initiated but pending external action, or only partly applied (say which part in `outcome_note`)
- `to_do`: left as a recommendation, or genuine future work

Write the dataset to `{project_root}/docs/artefacts/audit-{slug}.json` so the render is reproducible and can be re-run in render-only mode. Then gate it before any HTML: `python3 "$HOME"/.claude/library/scripts/validate_audit_findings.py {dataset}.json` must exit 0 (it checks required fields, enum values, id uniqueness, count consistency and the dash ban). Fix the dataset on failure; never render an invalid one. Render-only mode (Step 1) runs the same gate on the supplied file. Structure:

```json
{
  "meta": {
    "topic": "…", "document": "…", "generated": "YYYY-MM-DD",
    "method": "how the findings were produced",
    "counts": {"confirmed": N, "refuted": N,
               "by_severity": {"high": N, "medium": N, "low": N},
               "by_category": {"correction": N, "issue": N, "improvement": N, "enhancement": N}},
    "applied": {"date": "YYYY-MM-DD", "done": N, "in_progress": N, "to_do": N}
  },
  "findings": [ { …fields above… } ],
  "refuted": [ {"title": "…", "notes": "…"} ]
}
```

## Step 3: Load visual-explainer references

Resolve the installed path with Glob:

```text
~/.claude/plugins/cache/visual-explainer-marketplace/visual-explainer/*/
```

Read `references/css-patterns.md` (depth tiers, collapsible pattern, overflow protection) and `references/libraries.md` (font pairings, palette guidance) before writing any HTML.

## Step 4: Aesthetic and palette

Read `~/.claude/library/references/artefact-conventions.md` first: this
skill's palette and theming route through the shared conventions now, not a
standalone hex system. What stays specific to this skill (a deliberate
per-artefact choice, not a divergence from the shared rules):

- **Blueprint / editorial mood.** Near-black blueprint grid (`linear-gradient`
  grid lines at low opacity) in dark; warm off-white in light. Route both
  through the three-state theming contract (`:root` light, `@media
  (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`,
  `:root[data-theme="dark"]` for an explicit toggle) **and** the masthead
  toggle control from that reference doc (present, reachable in all three
  states, persisted to `localStorage`) on every pathway except an `Artifact`
  publish, where the host supplies its own.
- **Palette source: the project's `html` theme, as everywhere** (see
  `theme-conventions.md`; global `clod` when the project has none). Map this
  skill's severity/status accents onto theme tokens via semantic aliases
  (never a raw hex in a component): `--high` to `--danger`, `--medium` to
  `--warn`, `--low` to `--ok`; `--done`/`--progress`/`--todo` to `--ok`/
  `--info`/`--ink-muted`. Document the mapping the way the shared reference
  models, the way `site/assets/site.css` does.
- Fonts: **Space Grotesk** (head + body) + **IBM Plex Mono** (mono, code,
  labels), this skill's own choice within the shared pairing *structure*
  (one display/body voice + one monospace workhorse); not mandatory elsewhere.
- **Vocabulary**: severity (`high`/`medium`/`low`) and status
  (`done`/`in_progress`/`to_do`) are this skill's own contextual status
  vocabulary per the shared honesty rule; appropriate for an audit trail,
  not meant to be forced onto other artefact types.
- **British spelling throughout. No em dashes** (use semicolons, colons, parentheses). No contrastive "not X but Y" couplets.
- Forbidden for this skill specifically: Inter/Roboto body font (fights the
  chosen pairing); gradient-text headings; animated glow/pulse on static
  content. Violet/indigo stays off *this* skill's palette only to keep
  severity-red unambiguous against everything else on the page; not a
  house-wide ban (other artefacts use violet deliberately).

## Step 5: Generate the HTML

### Output location

```bash
mkdir -p {project_root}/docs/artefacts
```

Write to `{project_root}/docs/artefacts/audit-{slug}.html`, self-contained (embedded CSS + JS, only Google Fonts external).

### Page structure

1. **Masthead**: eyebrow, title, a lede that names the source document and explains the status grouping and the severity colour key inline, and a mono `method` line (`N confirmed · N refuted`).
2. **KPI row**: four cards: Done, In progress, To do and total Confirmed (with a severity breakdown sub-line). Colour each card's accent bar by what it counts.
3. **Filter bar**: sticky, `backdrop-filter` blur. Severity buttons (All / High / Medium / Low) and type buttons (Corrections / Issues / Improvements / Enhancements). Active button tints to the severity colour.
4. **Status sections**: three `<details>` blocks in order **To do**, **In progress**, **Done**, all rendered **collapsed** (no `open` attribute); the reader chooses what to expand. Each summary shows the label, a count and a right-aligned severity tally. Inside, a responsive card grid (`minmax(340px, 1fr)`), findings sorted by severity then id. An empty To-do section shows a short "nothing outstanding" note rather than vanishing.
5. **Refuted section**: the dropped candidates, so the page is falsifiable not selective.
6. **Footer**: source, method, applied date.

### Finding card

- Header: the **finding number** (mono, bold) whose **colour is set by `data-sev`** via a rule like `.finding[data-sev="high"] .finding__num{color:var(--high)}`; this is the second severity signal alongside the chip. Right-aligned badges: a severity chip, a category badge and a theme chip.
- Title (may contain `<code>` spans; convert `` `backticks` `` and strip any orphan).
- An outcome line: a mono status label + the `outcome_note`.
- A collapsible `<details>` holding the recommendation (led by a `▶ {anchor}` label), the file-ref chips, the evidence and the verification note.
- Every card carries `data-sev`, `data-cat`, `data-status` for the filter JS.

### Filter JS

Vanilla, inline. Buttons toggle a `.hidden` class on findings by `data-sev` or `data-cat`; status blocks whose visible-finding count drops to zero hide themselves (and auto-open when a non-`all` filter is active); a `#noresults` line shows when nothing matches.

### Reliability

Prefer writing the HTML directly. If the finding set is large, it is acceptable to drive a short Python generator (loop the dataset into card markup, escaping with `html.escape` and converting backticks to `<code>`) to avoid hand-escaping errors, then write the single output file. Do not leave a generator script behind as an artefact; the output is the HTML (and the dataset JSON from Step 2).

## Step 6: Quality checks

Before opening:

- [ ] Complete self-contained HTML document; only Google Fonts is external
- [ ] Tag balance holds (`article`, `details`, `div`, `script`, `style`)
- [ ] Every finding `id` is unique; all findings present
- [ ] Three status sections, all collapsed by default (filter interaction may auto-open)
- [ ] Severity shown by BOTH the chip and the finding-number colour (`data-sev` rule present for high/medium/low)
- [ ] Every `var(--x)` resolves to a definition; light and dark both intentional
- [ ] Masthead toggle control present (light/system/dark), persisted, unless this is an `Artifact` publish relying on the host control
- [ ] Any JS-rendered diagram follows the theme (CSS-variable-driven, or watches both `matchMedia` and `data-theme` mutation)
- [ ] All grid/flex children have `min-width: 0`; `overflow-wrap` on long text; refs wrap
- [ ] Filter JS targets exist (`#statuses`, `.finding`, `.statusblock`, `#noresults`)
- [ ] KPI and section counts match the dataset
- [ ] British spelling; no em dashes; no orphan backticks left in text
- [ ] No Inter/Roboto, no violet/indigo accents, no gradient-text headings, no animated glow

Run a quick static check (a few lines of Python: tag counts, `id` uniqueness, `var()` vs definitions, `data-status` tallies) rather than trusting a visual scan.

## Step 7: Open and report

```bash
open {project_root}/docs/artefacts/audit-{slug}.html
```

Report:

- File path written (HTML and the dataset JSON)
- Topic, total confirmed, refuted count
- The severity split and the status split (done / in progress / to do)
- The high-severity findings, surfaced inline so the user sees them without opening the file

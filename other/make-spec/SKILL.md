---
name: make-spec
category: tooling
description: |
  Scaffold a substantive human-readable design doc (spec / plan / ADR /
  report / PR explainer) as native HTML using the workspace's canonical
  Broomva dark theme. Implements P18 (Format-Follows-Audience) for
  Category-C native artifacts — distinct from `bookkeeping render`,
  which projects Category-B markdown canonicals to HTML.
  Use when: (1) drafting a substantive design doc a human will actually
  read (>100 lines OR contains tables/diagrams/decision matrices),
  (2) writing an ADR (architectural decision record), (3) producing a
  plan a non-agent stakeholder will review, (4) writing a PR explainer
  for a substantive PR, (5) producing a report that synthesizes prior
  research. The skill ships theme.css + the spec HTML template, and
  generates the plan / adr / report / pr-explainer variants from that
  same theme + the prose skeletons below — so the agent doesn't
  rebuild the 70-line :root + h1-h4 + table + callout boilerplate
  every time.
  Triggers on "spec", "plan", "ADR", "decision record", "design doc",
  "explainer", "report", "html spec", "html doc", "Broomva html",
  "dark theme spec".
---

# make-spec — HTML design-doc scaffold (P18 Category-C)

**One template + one theme + one filename convention — so the writer
spends 100% of energy on substance, 0% on boilerplate.**

## Why this skill exists

Since P18's promotion 2026-05-13, the workspace produces substantive
design docs as native HTML rather than markdown:

| Type | Location | Examples (last 7d) |
|---|---|---|
| Spec | `docs/specs/` | `2026-05-22-broker-selection-cross-asset.html`, `2026-05-23-life-houston-runtime-integration.html` |
| Plan | `docs/plans/` | `2026-05-22-feature-flag-design.html`, `2026-05-22-houston-advanced-settings.html`, `2026-05-22-houston-developer-mode.html` |
| Report | `docs/reports/` | `2026-05-22-houston-dogfood-pattern.html`, `2026-05-22-mission-control-vs-houston.html` |
| ADR | `docs/adrs/` | (folder reserved; pattern proven via broker-selection ADR in `docs/specs/`) |
| PR explainer | `docs/pr-explainers/PR-<n>.html` | (P18-reserved path) |

All 7 hand-rolled HTMLs above share the same 70-line CSS preamble:
`--bg #0e1116`, `--ink #e7ecf2`, `--accent #7ec4ff`, `--accent-2 #b58cff`,
h1-h4 with identical sizes/margins/colors, table with hover, callout
classes (warn/bad/ok/big), tag chips (info/warn/ok/bad/pick/cfd),
TOC block, footnote/cite styling.

Before this skill, every HTML doc rebuilt that boilerplate from
memory or copy-paste. The boilerplate IS the Broomva visual identity for
internal docs; centralizing it makes the visual identity stable AND
saves ~5 minutes per doc.

## What this skill provides

1. **`references/theme.css`** — the canonical 70-line stylesheet,
   verbatim from the proven specs. Reference, don't recopy.
2. **`references/template-spec.html`** — the one shipped base
   template (the spec layout). Every variant below is **generated
   from this base**, not loaded from its own file: start from
   `template-spec.html`, then swap the title prefix, TOC sections,
   and section skeleton per the variant's section list. No separate
   `template-plan/adr/report/pr-explainer.html` files ship — the
   variants are prose skeletons applied to the spec base.

The four variants (generated, not shipped — apply to the
`template-spec.html` base + the canonical skeleton below):

> **The base template has no Non-goals or Alternatives-considered slot**, and
> `spec-contract` requires both on the `spec` profile — so the shipped scaffold
> fails the content gate it now composes with. Add both sections when generating
> from it; they are the two classes the workspace corpus is weakest on (7.6%
> each), which is exactly why a scaffold that omits them perpetuates the gap.

3. **Plan variant** — base + sub-phase table + acceptance-criteria
   sections.
4. **ADR variant** — base + Status / Context / Decision /
   Consequences / Alternatives sections — the `adr` profile in
   `spec-contract`, which enforces them rather than listing them.
5. **Report variant** — base + Executive summary / Findings /
   Recommendations / Appendix sections.
6. **PR-explainer variant** — base + What changed / Why / Test plan
   / Risk / Rollout sections.

## When to invoke

- **Substantive design doc** (>100 lines OR contains ≥1 of: decision
  matrix, multi-row PR table, regulatory citations, multi-stage plan).
- **ADR** for any architectural decision worth keeping for posterity.
- **PR explainer** for a substantive PR (>200 LOC OR public API OR
  governance-class change — same trigger as P20's review requirement).
- **Plan** for any multi-week / multi-PR arc that a stakeholder will
  review (not just the executor).
- **Report** synthesizing prior research, briefings, or post-mortems.

## Carve-outs (do not invoke)

- Brief docs <100 lines → markdown is fine (P18 audience rule: the
  HTML payoff doesn't justify the 2-4× generation cost on short docs).
- Agent-loaded references (SKILL.md, entity pages, AGENTS.md) →
  always markdown (Category A: substrate stays markdown).
- README / CHANGELOG / docs that GitHub renders → markdown (GitHub's
  markdown renderer is the audience layer).
- PR descriptions (`gh pr create --body`) → markdown (GitHub renders).
- Throw-away interactive UI → use Webdesign / impeccable / arcan-glass
  skills; this skill is for static design docs only.

## The canonical structure

Every variant follows the same skeleton:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title><Doc type> — <Doc title></title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    /* paste references/theme.css verbatim */
  </style>
</head>
<body>
  <h1><Doc title></h1>
  <p class="subtitle"><One-line summary></p>
  <p class="meta">
    Author: <agent | user> · Generated: YYYY-MM-DD · Status: <draft | accepted | superseded><br>
    Decision-class: <span class="tag info">substantive</span> · risk-class: <span class="tag warn">…</span><br>
    Upstream context: <code>…</code>
  </p>

  <div class="callout warn">
    <strong>Verification scope</strong>. <When this doc requires
    out-of-band verification before action — e.g. CPA review, legal
    review, deploy approval — state it here.>
  </div>

  <div class="toc">
    <strong>Contents</strong>
    <ol>
      <li><a href="#section-1">…</a></li>
    </ol>
  </div>

  <h2 id="section-1">1. <Section title></h2>
  <!-- … -->
</body>
</html>
```

## CSS theme (load from `references/theme.css`)

The theme is **not** open for tweaking inside individual docs. The
visual identity is stable across all internal Broomva HTMLs:

- **Background**: `#0e1116` (the deep ink that lets the `--accent`
  blue and `--accent-2` purple read cleanly)
- **Ink**: `#e7ecf2` primary, `#98a2b3` dim, `#6b7280` muted
- **Accents**: `#7ec4ff` (h3 + tag.info) and `#b58cff` (tag.pick, the
  "this is the decision" highlight)
- **Status colors**: `#66d699` ok, `#ffd166` warn, `#ff7a7a` bad
- **Code**: `#0b0f15` background; monospaced via system stack
  (`ui-monospace, SFMono-Regular, "JetBrains Mono", Menlo`)
- **Sans**: `-apple-system, "SF Pro Text", system-ui, sans-serif`

To change the theme: amend `references/theme.css` and the change
propagates to every new doc. Existing docs are not retro-updated
(P13 stability budget — don't rewrite history for cosmetic deltas).

## Tag system

The `<span class="tag X">…</span>` chips are the doc's status
vocabulary. Always-supported classes:

| Class | Use | Color |
|---|---|---|
| `info` | neutral metadata / classification | `--accent` blue |
| `ok` | confirmed / passing / accepted | `--ok` green |
| `warn` | needs verification / blocked-on-external | `--warn` yellow |
| `bad` | rejected / failing / unsafe | `--bad` red |
| `pick` | THE decision (uniquely highlighted) | `--accent-2` purple, bold |
| `cfd` | specific anti-pattern marker (synthetic exposure / not-real-ownership; from the broker-selection ADR vocabulary) | `--bad` muted |

## Callout system

Four callout flavors:

```html
<div class="callout">…</div>        <!-- neutral; accent border -->
<div class="callout ok">…</div>     <!-- success / confirmed -->
<div class="callout warn">…</div>   <!-- needs verification -->
<div class="callout bad">…</div>    <!-- rejected / unsafe -->
<div class="callout big">…</div>    <!-- the headline decision / TL;DR -->
```

## File placement

| Doc type | Path | Filename |
|---|---|---|
| Spec | `docs/specs/` | `YYYY-MM-DD-<slug>.html` |
| Plan | `docs/plans/` | `YYYY-MM-DD-<slug>.html` |
| ADR | `docs/adrs/` (or `docs/specs/` until the dir is canonical) | `YYYY-MM-DD-adr-<slug>.html` |
| Report | `docs/reports/` | `YYYY-MM-DD-<slug>.html` |
| PR explainer | `docs/pr-explainers/` | `PR-<n>.html` (no date — PR number is the identifier) |

Slug names the **topic**, not the date. The date is the mtime.

## The five anti-patterns this skill exists to prevent

| Anti-pattern | Failure mode | Fix |
|---|---|---|
| **Rebuilding the theme inline** | 70-line :root drift across docs; visual identity erodes. | Always reference `references/theme.css`; don't paraphrase. |
| **Markdown for a 200-line spec** | Tables don't render the way the writer pictured; ASCII pseudo-diagrams; reader bounces by line 80 (the trq212 ceiling). | Apply the audience test: human-read substantive → HTML. |
| **HTML for a 30-line note** | 2-4× generation cost for no information-density payoff. | Brief docs stay markdown. |
| **Title in `<h1>` differs from `<title>`** | Tab-bar text doesn't match doc heading; reader gets confused when 5 tabs open. | Keep `<title>` and `<h1>` in sync; `<title>` adds the doc-type prefix (`"ADR — …"`). |
| **No `meta` line** | Reader can't tell author / date / status / risk-class without skimming. | The `<p class="meta">` line is mandatory: author + date + status + risk + upstream context. |

## Composition rules

| Compose with | When |
|---|---|
| **`spec-contract`** | **Always, for a design doc.** This skill owns how the doc LOOKS; `spec-contract` owns what is IN it (reversal-cost inclusion rule, required sections by class, ≥2 alternatives with rejection reasons, measurable acceptance, implementation-manual detector) plus the judgment rubric a script cannot run. Scaffold here, then gate with `python3 skills/governance/spec-contract/scripts/spec_check.py <doc>`. |
| **`bookkeeping render`** | NEVER for native HTML — `bookkeeping render` is for Category-B (MD canonical → HTML projection). This skill produces Category-C natives. They're disjoint per P18. |
| **`handoff`** | A handoff is markdown (agent-loaded) but may *link to* a make-spec HTML companion when the arc warrants. Handoff stays MD; companion is HTML. |
| **`autonomous`** | When `/autonomous` is mid-arc and a substantive plan emerges, fork the plan into `docs/plans/<slug>.html` via this skill, then continue execution. |
| **`Webdesign` / `impeccable` / `arcan-glass`** | Disjoint — those are for product-surface UI; this is for internal design docs. |

## Validation (spec self-test)

> **These checks are about the shell, not the contents.** Every item below can
> pass on a document that argues nothing — that is not a defect in the list, it
> is its scope. The contents are gated by `spec-contract`, whose checker is the
> last item here and is the only one that reads what the doc says.

- [ ] `<title>` and `<h1>` match (with doc-type prefix on `<title>`)
- [ ] `<p class="meta">` line present with author + date + status + risk
- [ ] Theme CSS is the `references/theme.css` content verbatim (or `<link>` to it if hosted) — no inline drift
- [ ] At least one `<div class="toc">` if the doc has ≥4 H2 sections
- [ ] All `tag` chips use one of the six canonical classes (info/ok/warn/bad/pick/cfd)
- [ ] Filename matches `YYYY-MM-DD-<slug>.html` (date = mtime, slug = topic)
- [ ] **Contents gated**: `python3 skills/governance/spec-contract/scripts/spec_check.py <doc>` exits 0, and the `spec-contract` rubric scores ≥11/15 with no axis at 0

## References

- Canonical theme source: `docs/specs/2026-05-22-broker-selection-cross-asset.html` lines 8–71 (extracted into `references/theme.css`)
- P18 audience rule: `CLAUDE.md` §P18 + `AGENTS.md` §P18
- trq212 thesis: *The Unreasonable Effectiveness of HTML* (May 2026, Claude Code team) — the empirical case behind P18
- Related skills: `bookkeeping` (Category-B render), `handoff` (companion MD artifact), `Webdesign` (product UI, disjoint)

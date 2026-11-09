---
name: "seo-audit-orchestration"
description: "Coordinate a full or explicitly partial SEO audit using available tools and supplied exports. Use this skill when running a comprehensive SEO audit, scoping a quarterly health check, doing pre-acquisition SEO due diligence, or post-migration verification. Triggers on full SEO audit, comprehensive SEO review, SEO health check, audit my site, SEO due diligence, audit suite, comprehensive audit, end-to-end SEO. Also triggers when a stakeholder wants the complete picture rather than a single-dimension audit."
---

# SEO Audit Orchestration

Run a complete SEO audit by sequencing the sibling audit skills in a defined order. Stack-agnostic. Check available capabilities first; Ahrefs is one supported data source, not an unconditional prerequisite. Produces a single rollup report that synthesizes findings across backlinks, keywords, content, traffic, technical health, and rankings.

---

## When to use

- Running a full SEO audit (quarterly, biannual, annual)
- Pre-acquisition SEO due diligence
- Post-migration verification (after content move, replatform, or domain change)
- Onboarding a new client or new property
- Building a baseline before a major SEO investment
- Diagnosing chronic underperformance

## When NOT to use

- Single-dimension audits (use the specific child skill: `seo-onpage`, `seo-backlink-audit`, etc.)
- Investigating a specific traffic drop (use `seo-traffic-diagnosis`)
- Tactical questions like "which keywords should we target" (use `seo-keyword-gap-audit`)
- Routine monitoring (use `seo-rank-tracking`)

---

## Required inputs

- The site or properties in scope
- Target market and primary languages
- Competitor set (3-5 properties)
- Goal of the audit (baseline, due diligence, fix plan, growth roadmap)
- Time and reporting constraints
- Available sources and access: Ahrefs if connected, user-provided exports, Search Console, analytics, crawl results or server logs; record missing coverage

---

## The framework: 6 phases of an end-to-end audit

Use the six phases as coverage dimensions. A partial audit completes supported dimensions and explicitly lists unavailable ones; do not require inaccessible sources or unrelated phases.

### Phase 1: Scope and baseline

Define the audit before running it.

- What is in scope (subdomains, paths, languages)
- What is out of scope
- Goal of the audit (baseline, fix plan, growth roadmap, due diligence)
- Stakeholders and their priorities
- Reporting format and length expectations

Output: a 1-page audit charter.

### Phase 2: Data gather

Collect raw data from available authorized sources. If Ahrefs is connected, the following is its full-audit coverage checklist; otherwise use the source-fallback reference and mark unsupported dimensions:

- Site Explorer: organic keywords, organic traffic, top pages, top countries, referring domains, backlinks, anchor text profile
- Site Audit: full crawl results
- Keywords Explorer: target keyword universe and competitor keyword overlap
- Content Explorer: top performing content in target topics
- Rank Tracker: current tracked positions if set up

Companion pulls (not Ahrefs-native):

- Search Console: query and page data, coverage issues
- Analytics: traffic, conversions, segment by source
- Server logs (if available): bot crawl behavior

Document data freshness for every pull. Stale data yields wrong conclusions.

### Phase 3: Run the sub-audits

Run child audits supported by the requested scope and available evidence. For unsupported dimensions record the gap instead of fabricating a findings document.

| Sub-audit | Skill | What it produces |
| --- | --- | --- |
| Site health | `seo-site-health-audit` | Prioritized technical fix backlog |
| Backlinks | `seo-backlink-audit` | Profile health, toxic list, reclamation list |
| Keywords | `seo-keyword-gap-audit` | Prioritized opportunity list |
| Content | `seo-content-gap-audit` | Create/update/merge roadmap |
| Page-level | `seo-onpage` | Per-page audit on top pages |
| AI search | `seo-aeo-geo` | AI search readiness gaps |

The child skills do the analysis. This skill sequences them and integrates the outputs.

### Phase 4: Synthesize

Combine findings into themes. A list of 200 issues is not an audit. A short list of themes is.

Themes typically emerge in categories like:

- Technical foundation gaps that cap upside
- Content depth gaps in priority topics
- Backlink profile concentration risks
- Keyword opportunities the site is leaving on the table
- Cannibalization or thin coverage
- AI search readiness

Each theme should answer: what is happening, why it matters, what is the size of prize, what is the fix.

### Phase 5: Prioritize

Rank the themes. Use a simple impact/effort matrix.

- Quick wins: high impact, low effort. Do now.
- Strategic plays: high impact, high effort. Plan and resource.
- Maintenance: low impact, low effort. Backlog.
- Avoid: low impact, high effort. Drop.

Tie each theme to a measurable target (organic clicks, ranked keywords in target band, conversions from organic).

### Phase 6: Deliver

Produce the rollup report. See [`references/audit-rollup-template.md`](references/audit-rollup-template.md).

Structure:

- Executive summary (1 page)
- Themes and recommendations (1 page each; count per audit type, from the template's length-targets table)
- Sub-audit findings (linked or appended)
- Roadmap (next 90 days)

Walk stakeholders through it. Get commitment to the next 90 days of work.

---

## Workflow

1. **Charter the audit.** 1-page scope, goal, stakeholders, format.
2. **Discover data access.** Use Ahrefs when available; otherwise inspect supplied exports and available first-party sources. Read [source fallbacks](references/source-fallbacks.md).
3. **Collect available evidence.** Apply the relevant gather list in phase 2, document freshness and record missing coverage.
4. **Run supported sub-audits.** Use available child skills for scoped dimensions with sufficient evidence; report remaining dimensions as unverified.
5. **Synthesize themes.** Hold to the theme count the template's length-targets table gives for this audit type. Each theme ties to an impact and a fix.
6. **Prioritize.** Impact/effort matrix. Quick wins surface to the top.
7. **Draft the rollup.** Use the template. Executive summary first.
8. **Review with the team.** Pressure-test conclusions before stakeholder readout.
9. **Deliver.** Walk stakeholders through. Get commitment to next 90 days.
10. **Schedule the next one.** Audits decay. Rerun on a cadence.

---

## Failure patterns

- **Audit without a goal.** Produces a 60-page document nobody reads. Charter the audit first.
- **All findings, no themes.** A list of 200 issues is data, not an audit. Synthesize into themes.
- **Unreported coverage gaps.** A broad audit needs dimension-specific evidence; an explicitly partial audit is valid when missing dimensions and their consequences are stated.
- **No prioritization.** "Here are 47 things to fix" gets nothing fixed. Rank them.
- **Stale data.** Ahrefs index updates on a delay. Note freshness. Do not draw conclusions from week-old movement.
- **Tool worship.** Ahrefs is one source. Search Console, analytics, and logs add ground truth. Triangulate.
- **Audit-to-audit drift.** Running every audit differently makes trends impossible to spot. Standardize the structure.
- **No 90-day roadmap.** Without a plan after the audit, the audit is shelfware.
- **Solo audit.** Audits done alone miss context. Pull in the people who own the work.

---

## Output format

A rollup audit report with:

1. **Executive summary.**
2. **Audit charter** (scope, goal, methodology).
3. **Themes and recommendations** (each theme with what, why, size of prize, fix).
4. **Sub-audit appendix** (linked outputs from each child skill).
5. **90-day roadmap** (sequenced work with owners and targets).
6. **Methodology notes** (data sources, pull dates, caveats).

Total length, executive summary length, and theme count all vary by audit type: a quarterly health check is not a due-diligence audit. The length-targets table in [`references/audit-rollup-template.md`](references/audit-rollup-template.md) owns those numbers per type. Whatever the type, the executive summary stays readable in 5 minutes.

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/audit-rollup-template.md`](references/audit-rollup-template.md) - Template for the rollup report including executive summary, theme structure, and roadmap format.


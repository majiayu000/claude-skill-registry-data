---
name: career-ops
description: >
  AI job search command center — evaluates job offers with A-F scoring, generates ATS-optimized CV PDFs, scans multiple job portals in parallel, tracks application pipelines, and analyzes rejection patterns to surface actionable improvements. Routes to specialized sub-agents based on mode: `scan` (portal discovery), `oferta`/`ofertas` (offer scoring and comparison), `pdf` (CV generation), `pipeline` (URL inbox processing), `tracker` (funnel metrics), `batch` (parallel bulk evaluation), `patterns` (rejection pattern detection), `deep` (company research), `apply` (live form assistant), `contacto` (LinkedIn outreach), `training` (course/cert evaluation), `project` (portfolio project idea assessment), `interview-prep` (company-specific STAR+R story bank). Also triggers when pasting a job description or URL — auto-routes to Pipeline Strategist. Ethical gate: scores below 4.0/5 are discouraged; never submits applications on the user's behalf. Built on santifer/career-ops (28K GitHub stars). Ideal for job seekers who want systematic, evidence-backed career decisions. Also for: salary negotiation preparation, resume optimization, and competitive market analysis.
user_invocable: true
args: mode
argument-hint: "[scan | oferta | pdf | tracker | pipeline | batch | patterns | deep | apply | contacto | ofertas | training | project | interview-prep]"
---

# career-ops -- AI Job Search Command Center

Skill for The Agency. Delegates to the most relevant specialized agent based on the mode requested. **For any career-ops task, invoke the right sub-agent rather than handling it directly.**

## Mode → Agent Routing

| Mode | Agent | Description |
|------|-------|-------------|
| `scan` | **Job Portal Scanner** | Scrape portals + on-demand: `node scan-positions.mjs --position "AI Engineer" --location hanoi` |
| `scan:pos` | **scan-positions.mjs** | On-demand scan for a specific position title + location. Usage: `npm run scan -- --position "Digital Marketing Manager" --location hanoi` |
| `oferta` / `ofertas` | **Offer Evaluator** | A-F scoring, archetype detection, gap analysis, comparison/ranking |
| `pipeline` | **Pipeline Strategist** | Process inbox URLs: evaluate → report → PDF → tracker (never touch applications.md directly) |
| `batch` | **Batch Processing Lead** | Parallel worker pipeline for bulk evaluations |
| `patterns` | **Pattern Analysis Specialist** | Rejection pattern detection, actionable recommendations from tracker + reports |
| `pdf` | **CV Specialist** | ATS-optimized CV generation with Playwright HTML→PDF |
| `tracker` | **Pipeline Analyst** | Application status overview, funnel metrics |
| `deep` | **Discovery Coach** | Deep company research |
| `apply` | **Outbound Strategist** | Live application form assistant with Playwright |
| `contacto` | **Outbound Strategist** | LinkedIn outreach: find contacts + draft messages |
| `training` | **Trend Researcher** | Evaluate course/cert against career goals |
| `project` | **Game Designer** | Evaluate portfolio project idea |
| `interview-prep` | **Discovery Coach** | Company-specific interview prep with STAR+R story bank |

## Routing Logic

1. Parse `{{mode}}` from the invocation args
2. If empty/no args → show the discovery menu inline (no sub-agent needed)
3. If JD text or URL → auto-route to **Pipeline Strategist** (`pipeline` mode)
4. Otherwise → spawn the matching specialized agent with the mode as the task description
5. Spawn the matching specialized agent from the Mode → Agent Routing table above.
   - Use the agent name/type from column 2 of the table
   - Pass prompt: "mode: {mode}, project: {current_project}"
   - **Never use general-purpose here** — every career-ops mode has a named agent

## Discovery Menu (no args)

```
career-ops -- Command Center

Available commands:
  scan        → Discover new offers across portals (3-level scanner)
  oferta      → Evaluate a job offer (A-F scoring, archetype detection)
  ofertas     → Compare and rank multiple offers
  pipeline    → Process pending inbox URLs (evaluate → report → PDF → tracker)
  batch       → Bulk evaluations via parallel workers
  patterns    → Analyze rejection patterns from tracker + reports
  pdf         → Generate ATS-optimized CV PDF
  tracker     → Application funnel and status overview
  apply       → Live application form assistant
  contacto    → LinkedIn outreach (find contacts + draft message)
  deep        → Deep company research
  interview-prep → Company-specific interview prep (STAR+R stories)
  training    → Evaluate course/cert against your career goals
  project     → Evaluate a portfolio project idea

Paste a job description or URL → runs the full pipeline automatically.
```

## Sub-Agent Prompt Template

When spawning a specialized agent:

```
You are running in career-ops mode: {MODE}

Your task: {MODE_DESCRIPTION}

Project context:
- career-ops root: {current_project_dir}
- CV: cv.md (read this first)
- Profile: config/profile.yml
- Tracker: data/applications.md
- Pipeline inbox: data/pipeline.md

Key rules:
- NEVER submit applications on the user's behalf
- Scores below 4.0/5 → recommend against applying
- NEVER edit applications.md directly — write TSV to batch/tracker-additions/
- After every batch: run node merge-tracker.mjs
- All reports must include **URL:** in header
- Use Playwright (not WebSearch) to verify offers are active

Execute the {MODE} mode fully. Report results back to the parent session.
```

## Global Conventions (all agents)

- **Ethical gate**: Always discourage scores < 4.0/5. Quality > quantity.
- **User review before submit**: Draft everything, STOP before clicking Submit.
- **TSV pipeline additions**: Write to `batch/tracker-additions/{num}-{slug}.tsv`, never touch `data/applications.md` directly.
- **Report numbering**: Sequential 3-digit zero-padded, max existing + 1.
- **Verification**: Always use Playwright to verify offer is still active before evaluating.
- **Canonical states**: `Evaluated` | `Applied` | `Responded` | `Interview` | `Offer` | `Rejected` | `Discarded` | `SKIP` — no bold in status field.

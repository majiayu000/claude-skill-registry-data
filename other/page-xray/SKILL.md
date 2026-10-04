---
name: page-xray
description: Exhaustive URL/page interrogation for ChefFlow. 1261 questions across 27 dimensions + meta. Tracks findings across scans with closed-loop lifecycle. Creates Rail Profiles, build opportunities, developer notes, domain wiring reports, role/security audits, client intelligence maps. Maintains file-based scan matrix at docs/xrays/. Use when /page-xray, auditing a page, designing Rail, checking domain wiring, pre-build intelligence, or scanning pages with stale/missing X-Ray data.
---

# Page X-Ray

Permanent codebase intelligence layer. Exhaustive interrogation of any ChefFlow URL/page.

Not a one-time audit. A closed-loop scan system that improves page cohesiveness over time.

Every time this skill runs, it helps future agents build better, wire better, secure better, test better, and understand the page before touching it.

## Invocation

```
/page-xray /events/[id]                    # Single page, full scan
/page-xray /events/*                        # Route group
/page-xray /events/[id] --rail-only         # Rail-focused scan
/page-xray /events/[id] --security-only     # Security-focused scan
/page-xray /events/[id] --domain-only       # Domain wiring scan
/page-xray /events/[id] --codex-only        # Mechanical questions only (cheap)
/page-xray /events/[id] --delta             # Re-check open findings only
/page-xray --all                            # Every route (batch mode)
/page-xray --gaps-only                      # Pages missing Rail Profiles
/page-xray --unwired                        # Pages with weak domain wiring
/page-xray --stale                          # Pages not scanned in 30+ days
/page-xray --never-scanned                  # Pages with zero scans
/page-xray --unresolved                     # Pages with open findings
/page-xray --domain events                  # All pages in a domain
/page-xray --portal client                  # All client-portal pages
/page-xray --summary                        # Matrix summary, no scan
/page-xray /events/[id] --quick              # P1 dimensions only (~400 questions, cheap)
/page-xray /events/[id] --deep               # All dimensions including P3 strategic
/page-xray /events/[id] --full               # Force full scan even if previously scanned
/page-xray --regressions                     # Show all score regressions
```

## Scan Modes

| Mode          | Flag              | Dimensions    | Questions | Purpose                                  |
| ------------- | ----------------- | ------------- | --------- | ---------------------------------------- |
| Full          | (default)         | All 27 + meta | ~1261     | Complete interrogation                   |
| Rail-only     | `--rail-only`     | 0, 11, 12, 23 | ~326      | Rail Profile design                      |
| Security-only | `--security-only` | 0, 9, 11, 16  | ~361      | Security + role + client intel audit     |
| Domain-only   | `--domain-only`   | 0, 2, 18, 22  | ~165      | Domain wiring check                      |
| Codex-only    | `--codex-only`    | All           | ~530      | Mechanical scan (cheap triage)           |
| Delta         | `--delta`         | Varies        | Varies    | Re-check previous open findings only     |
| Quick         | `--quick`         | P1 only       | ~400      | Cheap health check, core dimensions only |

## Dimension Priority Tiers

Each of the 27 dimensions is classified into a priority tier. This controls which dimensions run in which scan mode.

| Tier              | Dimensions                                                                                                                  | ~Questions | When Run                                                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| **P1 (Core)**     | 0 (Page Identity), 1 (Content Inventory), 9 (Security/Auth), 11 (Client Intelligence), 13 (Data Flow), 16 (Role/Permission) | ~400       | Always. Every scan mode except `--delta` runs these. High signal, low noise.                                           |
| **P2 (Standard)** | 2-8, 10, 12, 14-15, 17-22                                                                                                   | ~740       | Full scan, Rail-only, Security-only, Domain-only. The bulk of the survey.                                              |
| **P3 (Deep)**     | 23 (Rail Profile Design), 24 (Strategic Vision), 25 (Competitive Analysis), 26 (Future Opportunity)                         | ~120       | Only on explicit `--deep` flag or when scan count >= 10. Strategic/vision questions that only matter for mature pages. |

Tier rules:

- `--quick` runs P1 only. Fast, cheap, answers "is this page healthy?"
- `--deep` runs P1 + P2 + P3. Everything including strategic dimensions.
- Full scan (default for first scan) runs P1 + P2. Standard thoroughness.
- Delta scan runs only the dimensions relevant to open findings and changed files.
- Focused modes (`--rail-only`, `--security-only`, `--domain-only`) run their specific dimension sets regardless of tier.

## Workflow

### Phase 0: Matrix Check

1. Read `docs/xrays/index.json` (create if missing with empty structure)
2. Identify target page(s) from invocation args
3. For each target, load scan history from `docs/xrays/pages/{route-slug}.json`
4. Report: scan count, last scanned, open findings, prior mode
5. If page scanned before: load previous findings for diff comparison
6. If `--summary`: output matrix stats and stop

### Phase 1: Target Resolution

1. Parse argument into route pattern(s)
2. Route enumeration:
   - Single route: resolve file path directly
   - Glob pattern (`/events/*`): glob `app/(chef)/events/**/page.tsx`
   - `--all`: glob all route groups: `app/(chef)/**/page.tsx`, `app/(public)/**/page.tsx`, `app/(client)/**/page.tsx`
   - Filter flags: cross-reference against `docs/xrays/index.json`
   - `--domain X`: filter routes by primary domain from index
   - `--portal X`: filter routes by route group
3. Confirm target list if > 5 pages, proceed silently if <= 5
4. Determine scan mode from flags:
   - If `--full` or `--delta` explicitly set: use that mode
   - If page has been scanned before (exists in `docs/xrays/pages/{slug}.json`): default to `--delta` mode. Re-checks open findings plus areas changed in git since last scan (`git diff --name-only {last_scan_hash}..HEAD`). Full scan only on first scan or explicit `--full` flag. This cuts cost dramatically for maintenance scans.
   - If page never scanned: default to full scan

### Phase 2: Code Read [CODEX tier]

Per target page, read and catalog:

1. `page.tsx` (and `layout.tsx` chain)
2. Co-located files: `loading.tsx`, `error.tsx`, `not-found.tsx`, components, actions
3. Imported server actions (trace to file, list function names)
4. Imported lib/ modules (trace domain, list exported functions used)
5. Imported components (shared vs domain-specific)
6. Database tables read (trace through domain queries)
7. Database tables written (trace through mutations)
8. API routes hit (client-side fetches)
9. Type imports (shared types/ vs inline)
10. External dependencies (third-party, PIE, CIL, weather)
11. Permissions/auth checks (middleware, layout, page level)
12. Cache usage (unstable_cache tags, revalidatePath, revalidateTag)

Output: structured code inventory per page (used as input for all subsequent phases).

### Phase 3: Survey Execution

Run questions from [XRAY-SURVEY.md](XRAY-SURVEY.md) matching active scan mode.

Rules:

- Answer EVERY question. N/A is valid and informative (tells Rail what to exclude).
- Tag every answer with an answer class (see [SCHEMAS.md](SCHEMAS.md)).
- `[CODEX]` questions: answer from code analysis only. No judgment needed.
- `[CLAUDE]` questions: answer with product judgment, domain knowledge, chef context.
- `[OPUS]` questions: answer with deep synthesis, cross-domain reasoning, strategic vision.
- `[BOTH]` questions: mechanical analysis first, then judgment overlay.
- Compare each answer against previous scan's answer if exists.
- Flag: new findings, resolved findings, repeated findings, changed answers.

### Phase 4: Answer Classification

Classify every non-N/A answer using the 15 answer classes:

| Class                        | Meaning                                                       |
| ---------------------------- | ------------------------------------------------------------- |
| `EXISTS_WIRED`               | Data/behavior exists and is correctly wired                   |
| `EXISTS_UNWIRED`             | Exists somewhere but not connected to this page/Rail/workflow |
| `MISSING`                    | Should exist but does not                                     |
| `NOT_APPLICABLE`             | Question doesn't apply (tells Rail what to exclude)           |
| `SYSTEM_ONLY`                | Known by system, not shown to user                            |
| `USER_VISIBLE`               | Should be surfaced somewhere in UI                            |
| `RAIL_VISIBLE`               | Should appear in contextual Rail                              |
| `ROLE_GATED`                 | Must only appear for specific roles                           |
| `DENSITY_GATED`              | Appears only when context requires it                         |
| `FUTURE_BUILD_SIGNAL`        | Should become a build, spec, test, or design note             |
| `REQUIRES_RESOLVER`          | Needs a resolver before it can appear in Rail                 |
| `REQUIRES_SCHEMA`            | Needs database/schema support                                 |
| `REQUIRES_UI`                | Data exists but needs a surface                               |
| `REQUIRES_ACTION`            | Data exists but needs an action/button/workflow               |
| `REQUIRES_PERMISSION_REVIEW` | May be sensitive, needs permission audit                      |

Each classified answer gets:

- **Home**: where this data/behavior lives (file path, table, component)
- **Property**: specific field, function, or element
- **Source**: database, API, computed, external, user input
- **Freshness rule**: real-time, cached (duration), static, event-driven
- **Visibility rule**: always, conditional, role-based, density-based
- **Role rule**: which roles see this
- **Wiring path**: how data flows from source to display
- **Rail implication**: what this means for Rail Profile
- **Developer note**: technical note for future agents
- **Build opportunity**: if this answer produces a build, describe it

### Phase 5: Finding Extraction

Extract findings from classified answers:

1. **Finding ID**: `{route-slug}-S{scan-number}-F{sequence}` (e.g., `events-id-S3-F017`)
2. **Initial status**: `new` (first seen) or `seen_before` (matches prior finding)
3. **Severity**: `critical` / `high` / `medium` / `low` / `info`
4. **Category**: dimension name (e.g., "domain-wiring", "security", "rail-gap")
5. **Source question**: question ID from survey
6. **Explanation**: what was found
7. **Recommended fix**: concrete action
8. **Rail implication**: how this affects Rail Profile
9. **Build implication**: whether this becomes a build opportunity
10. **Security implication**: whether this is a security concern
11. **Files involved**: file paths likely needing modification
12. **Codex-buildable**: boolean (can Codex fix this, or does it need Claude/Opus?)

Compare against previous scan:

- Same finding present again: status -> `open`, bump `last_seen_scan`
- Finding no longer present: status -> `resolved`
- New finding not seen before: status -> `new`
- Finding matched but changed: update explanation, keep history

### Phase 6: Rail Profile Auto-Wiring

From Dimensions 0, 11 (Client Intelligence), 12 (Intelligence Categories), 13 (Data Flow), 23 (Rail Profile Design):

1. Read existing profiles from `lib/discovery/rail-profiles.ts`
2. Check if a profile already exists for this route pattern
3. **If profile exists**: update it based on new findings (new categories, resolver changes, layout adjustments). Preserve any manually-added configuration. Write the updated profile back to `lib/discovery/rail-profiles.ts`.
4. **If no profile exists**: generate a complete profile from scan data (categories, resolvers, collapsed metrics, layout, entity scoping) and WRITE it directly into `lib/discovery/rail-profiles.ts` in the registry object.
5. Cross-reference `docs/specs/contextual-rail-research.md` (8 categories)
6. For any `REQUIRES_RESOLVER` findings: generate resolver stub files in `lib/discovery/resolvers/{domain}/`. Each stub exports a resolver function matching the Rail resolver interface, with a TODO body and the correct type signature.
7. The scan MUST leave the page with a working Rail Profile in the registry, not a recommendation. If the profile cannot be auto-generated (ambiguous domain, conflicting signals), flag it as `NEEDS_HUMAN` in the scan record and explain why.

### Phase 7: Build Opportunity Extraction + Auto-Queue

Extract concrete, Codex-dispatchable build opportunities from findings:

Every opportunity gets:

- **ID**: `BO-{route-slug}-{sequence}`
- **Route**: page route
- **Domain**: owning domain
- **Category**: UI action, data wiring, Rail resolver, test, security, automation, etc.
- **Description**: what to build (concrete, 1-2 sentences)
- **Tier**: `CODEX` (mechanical) / `CLAUDE` (needs judgment) / `OPUS` (needs deep reasoning) / `HUMAN` (product decision)
- **Files involved**: likely file paths
- **Spec reference**: link to existing spec if relevant
- **Dependencies**: other builds that must come first
- **Estimated effort**: trivial / small / medium / large
- **Queue-ready note**: dispatch-ready prompt for Codex/agent

**Auto-Queue Integration:**

After extracting opportunities, automatically wire them into the build queue:

1. Read `docs/UNIFIED-BUILD-QUEUE.md`
2. For each extracted opportunity, check existing queue items for duplicates (match by route + description similarity). If a matching item exists, skip it.
3. Append new (non-duplicate) opportunities to the correct category section in the build queue with status `SPEC-READY`
4. Each appended item includes: route, domain, tier (CODEX/CLAUDE/OPUS), estimated effort, and the Codex-ready dispatch prompt
5. Format: `- [ ] **{route}** {description} [{tier}] [{effort}] `SPEC-READY`` followed by the dispatch prompt as a sub-bullet
6. Log appended count in the scan record: `build_opportunities_queued`

### Phase 8: Developer Notes

Write technical briefing notes for future agents, per route:

Structure:

```markdown
## {Route}: Developer Notes

### Summary

What this page does and why it exists. 1 paragraph.

### Domain Context

Primary domain, secondary domains, cross-domain wiring status.

### Before Modifying This Page

- Files to read first
- Patterns to follow
- Pitfalls to avoid
- Domain interfaces to respect

### Current Gaps

- Grouped by: domain, Rail, security, role, data, UI, automation, testing

### Unresolved Product Decisions

- Questions that need human input before building

### Build Priority

1. [highest impact build]
2. [second highest]
3. [third highest]

### Test After Modification

- What tests to run
- What to visually verify
- What caches to invalidate
- What other pages to check
```

Group notes by: route, domain, Rail, security, role visibility, data wiring, UI actions, automation, testing, unresolved decisions. Tag each note as CODEX / CLAUDE / OPUS / HUMAN task.

### Phase 9: Scan Record Update

Update `docs/xrays/pages/{route-slug}.json` with scan record (see SCHEMAS.md for full schema):

- Increment `scan_count`
- Set `last_scanned_at` to ISO timestamp
- Set `last_scanned_by` to model/agent identifier
- Set `scan_mode` to active mode
- Compute and store `current_scan_hash`
- Rotate `previous_scan_hash`
- Update all scores (0.0 to 1.0):
  - `cohesion_score`: weighted average of all scores
  - `rail_readiness_score`: Rail Profile exists + resolvers wired + categories assigned
  - `domain_wiring_score`: correct domain owner + no boundary violations + proper interfaces
  - `security_score`: auth gates + role checks + no leakage + no public exposure
  - `role_clarity_score`: every element has clear role visibility + no leakage
  - `data_completeness_score`: all expected data loaded + no stubs + no fake values
  - `page_usefulness_score`: does page justify existence (judgment)
- Update finding counts: `new`, `resolved`, `open`, `total_lifetime`
- Update: `questions_answered`, `na_count`, `user_visible_recommendations`, `system_only_findings`, `rail_visible_findings`, `build_opportunities_count`

### Phase 10: Index Update

Update `docs/xrays/index.json` and `docs/xrays/INDEX.md`:

Index-level stats:

- Total pages known
- Total pages scanned (at least once)
- Total pages never scanned
- Total findings: open / resolved / lifetime
- Total build opportunities: open / dispatched / completed
- Total Rail Profiles: exist / missing / stale
- Domain coverage: scanned domains vs total domains
- Last full scan date
- Overall codebase cohesion score

Per-page entry:

- Route, domain, portal, scan count, last scanned, open findings, scores, status

Update cross-cutting files:

- `docs/xrays/findings/open-findings.md`: append new, remove resolved
- `docs/xrays/findings/resolved-findings.md`: append newly resolved
- `docs/xrays/findings/findings.json`: machine-readable finding database
- `docs/xrays/build-opportunities.md`: append new opportunities
- `docs/xrays/rail-recommendations.md`: append/update Rail recommendations
- `docs/xrays/developer-notes.md`: append/update developer notes

Update domain rollups:

- `docs/xrays/domains/{domain}.md`: domain-level finding summary, wiring status, page list

Update matrices:

- `docs/xrays/matrices/scan-matrix.md`: scan coverage table
- `docs/xrays/matrices/domain-matrix.md`: domain wiring overview
- `docs/xrays/matrices/rail-matrix.md`: Rail readiness overview
- `docs/xrays/matrices/role-matrix.md`: role/permission overview
- `docs/xrays/matrices/unresolved-build-matrix.md`: open build opportunities

### Phase 11: Score Regression Detection

After index update, compare current scores against the previous scan:

1. Load previous scan record from `docs/xrays/pages/{route-slug}.json` (the `previous_scores` field)
2. Compare each of the 7 scores (cohesion, rail_readiness, domain_wiring, security, role_clarity, data_completeness, page_usefulness) against prior values
3. If ANY score dropped by more than 0.1: flag as `REGRESSION`
4. Append regression alerts to `docs/xrays/regressions.md`:
   ```
   ## {date} - {route}
   - **{score_name}**: {old_value} -> {new_value} (delta: -{drop})
   - **Likely cause**: {files changed since last scan, from git diff}
   - **Related findings**: {finding IDs that may explain the drop}
   ```
5. Set `has_regressions: true` in the scan record. A scan with regressions CANNOT be marked "healthy" in the index. The page status becomes `regressed` until the next scan shows recovery.
6. If no regressions: set `has_regressions: false`, page status follows normal scoring rules.

Regression detection also runs in `--delta` mode. Even a quick re-check compares scores.

## Model Tiering Strategy

| Tag        | Model          | Approx Count | Cost      | Use For                                                                                                                       |
| ---------- | -------------- | ------------ | --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `[CODEX]`  | Codex / Haiku  | ~530         | Cheap     | File existence, imports, DB tables, components, forms, links, routes, permissions, tests, cache tags, static values, patterns |
| `[CLAUDE]` | Sonnet / Opus  | ~340         | Standard  | Product judgment, UX, what matters, what is missing, Rail decisions, chef context, emotional context, competitive analysis    |
| `[OPUS]`   | Opus only      | ~120         | Expensive | Deep synthesis, strategic vision, cross-domain architecture, client intelligence decisions, future opportunities              |
| `[BOTH]`   | Codex + Claude | ~270         | Mixed     | Mechanical analysis first, then judgment overlay                                                                              |

In batch mode:

1. Dispatch `[CODEX]` questions to Haiku agents (one per route group, parallel)
2. Collect CODEX results
3. Run `[CLAUDE]`/`[OPUS]`/`[BOTH]` questions in main session or Opus agents, using CODEX results as context input
4. This 2-pass approach cuts cost by ~50% while maintaining judgment quality

## Closed-Loop Tracking

Every scan builds on previous scans. The system remembers:

- What was found before and when
- What was resolved and how
- What persists across scans
- What is new this scan
- Whether cohesion is improving or degrading
- What build opportunities have been extracted vs executed

Expected lifecycle for a page:

- Scan 1: baseline. Many findings. Low scores. Many build opportunities.
- Scan 2-5: targeted fixes. Findings resolving. Scores improving.
- Scan 10+: maintenance mode. Few new findings. High scores. Occasional new opportunities from new features.
- Scan 20+: deep maturity. Only strategic/vision findings. Near-ceiling scores.

The skill should be able to report:

- "This page has been scanned 14 times."
- "This page still has 7 unresolved findings."
- "This page has resolved 31 findings since first scan."
- "This page has produced 43 build opportunities over time."
- "Cohesion improved from 0.22 to 0.81 over 14 scans."

## Immune System Mode (PLANNED)

Vision: Page X-Ray becomes a continuous immune system for the codebase, not a manually-triggered skill.

**How it works (future state):**

1. **Post-commit hook** triggers delta scan on routes affected by changed files. If `app/(chef)/events/[id]/page.tsx` changed, auto-scan `/events/[id]` in `--quick` mode.
2. **Score regression blocks commit.** Like test failures, a score drop > 0.1 on any dimension flags the commit. Developer must acknowledge or fix before proceeding.
3. **New findings auto-append to build queue.** Every scan that discovers new `SPEC-READY` opportunities writes them directly to `docs/UNIFIED-BUILD-QUEUE.md` (already implemented in Phase 7).
4. **Weekly full scan of all routes via cron.** Scheduled job runs `--all --full` overnight, producing a fresh health report by morning.
5. **Dashboard view of page health scores.** Single page showing all routes, their cohesion scores, trend arrows (improving/degrading/stable), open finding counts, and regression alerts.
6. **Auto-heal loop.** When a regression is detected and the fix is Codex-tier (mechanical), auto-dispatch a Codex agent to fix it. Human review before merge.

This is not yet implemented. The phases above (delta-as-default, score regression detection, auto-queue integration, Rail auto-wiring) are the foundation that makes this mode possible. Each phase was designed with Immune System Mode as the end state.

## Batch Mode: Agent Dispatch

When `--all`, spawn parallel Haiku agents for CODEX pass:

| Agent | Route Group                      | Routes                                                                         |
| ----- | -------------------------------- | ------------------------------------------------------------------------------ |
| 1     | Events + Calendar                | `app/(chef)/events/**`, `app/(chef)/calendar/**`                               |
| 2     | Clients + Circles                | `app/(chef)/clients/**`, `app/(chef)/circles/**`                               |
| 3     | Menus + Recipes + Ingredients    | `app/(chef)/menus/**`, `app/(chef)/recipes/**`, `app/(chef)/ingredients/**`    |
| 4     | Finance + Invoices + Payments    | `app/(chef)/finance/**`, `app/(chef)/invoices/**`, `app/(chef)/payments/**`    |
| 5     | Cannabis + Compliance            | `app/(chef)/cannabis/**`, `app/(chef)/compliance/**`                           |
| 6     | Settings + Onboarding + Profile  | `app/(chef)/settings/**`, `app/(chef)/onboarding/**`, `app/(chef)/profile/**`  |
| 7     | Dashboard + Activity + Analytics | `app/(chef)/dashboard/**`, `app/(chef)/activity/**`, `app/(chef)/analytics/**` |
| 8     | Public routes                    | `app/(public)/**`                                                              |
| 9     | Client portal                    | `app/(client)/**`                                                              |
| 10    | Everything else                  | remaining routes                                                               |

After CODEX pass: run CLAUDE/OPUS pass in main session using collected mechanical results.

## Output Structure

```
docs/xrays/
  INDEX.md                              # Human-readable scan matrix
  index.json                            # Machine-readable index (all pages, all stats)
  build-opportunities.md                # All extracted build opportunities
  developer-notes.md                    # All developer notes (grouped by route)
  rail-recommendations.md               # All Rail Profile recommendations
  findings/
    open-findings.md                    # Currently open findings (all pages)
    resolved-findings.md                # Resolved findings log
    findings.json                       # Machine-readable finding database
  pages/
    {route-slug}.md                     # Per-page X-Ray report (human-readable)
    {route-slug}.json                   # Per-page scan data (machine-readable)
  domains/
    {domain}.md                         # Domain-level rollup
  matrices/
    scan-matrix.md                      # Which pages scanned, when, how many times
    domain-matrix.md                    # Domain wiring health across all pages
    rail-matrix.md                      # Rail readiness across all pages
    role-matrix.md                      # Role/permission coverage across all pages
    unresolved-build-matrix.md          # Open build opportunities by domain/priority
```

Route slug convention: replace `/` with `-`, remove `[]` brackets, lowercase.
Examples: `events-id`, `clients-id-preferences`, `cannabis-hub`, `dashboard`.

## Per-Page Output Checklist

Every page scan MUST produce all 15 deliverables:

1. Page X-Ray report (`pages/{slug}.md`)
2. Scan record update (`pages/{slug}.json`)
3. Rail Profile recommendation (in report + `rail-recommendations.md`)
4. Domain wiring report (in report + `domains/{domain}.md`)
5. Role/permission report (in report + `matrices/role-matrix.md`)
6. Data-property inventory (in report)
7. Missing-property proposal list (in report)
8. Resolver gap list (in report)
9. UI action gap list (in report)
10. Test gap list (in report)
11. Security gap list (in report)
12. Developer notes (`developer-notes.md`)
13. Build opportunity list (`build-opportunities.md`)
14. Score updates (all 7 scores in `pages/{slug}.json`)
15. Index/matrix updates (`index.json`, `INDEX.md`, all matrices)

## References

- Survey questions: [XRAY-SURVEY.md](XRAY-SURVEY.md)
- Data schemas: [SCHEMAS.md](SCHEMAS.md)
- Rail categories: `docs/specs/contextual-rail-research.md`
- Rail design: `docs/superpowers/specs/2026-05-18-contextual-rail-design.md`
- Rail profiles: `lib/discovery/rail-profiles.ts`
- Route inventory: `docs/app-complete-audit.md`
- Domain map: `docs/CLAUDE-DOMAINS.md`
- Nav audit: `docs/audits/navigation-audit-may2026.md`
- Domain audit: `docs/audits/domain-audit-may2026.md`
- Product blueprint: `docs/product-blueprint.md`
- Service lifecycle: `docs/service-lifecycle-blueprint.md`
- Failure rubric: `docs/failure-rubric.md`
- Build queue: `docs/UNIFIED-BUILD-QUEUE.md`
- Test coverage blueprint: `docs/test-coverage-blueprint.md`
- CONTEXT.md ubiquitous language: `CONTEXT.md`
- Interface philosophy: `docs/specs/universal-interface-philosophy.md`
- Surface grammar: `docs/specs/surface-grammar-governance.md`

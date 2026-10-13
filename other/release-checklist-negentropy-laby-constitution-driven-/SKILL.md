---
name: release-checklist
description: "Audits internal release readiness: story completion, bugs, QA sign-off, build evidence and changelog, with applicable Game or Product checks. External launch and platform/store readiness belongs to /launch-checklist."
argument-hint: "[platform: pc|console|mobile|all | product: web|api|cli|all]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
---

> **Explicit invocation only**: This skill should only run when the user explicitly requests it with `/release-checklist`. Do not auto-invoke based on context matching.

## User Guide

- When to use: Audits internal release readiness: story completion, bugs, QA sign-off, build evidence and changelog, with applicable Game or Product checks. External launch and platform/store readiness belongs to /launch-checklist.
- Inputs: Command arguments: `/release-checklist [platform: pc|console|mobile|all | product: web|api|cli|all]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Detection

**Required Read before domain-dependent routing:** read `CLAUDE.md` and
`standards/technical-preferences.md`, the existing explicit domain decision for
the current scope, and any existing `design/cdd/game-concept.md` or
`design/cdd/product-concept.md` bodies. Read actual configuration before deciding
what the absence of a concept means. Filenames, copied templates, placeholders
and shared file extensions do not establish a domain.

In technical preferences, read populated legacy Product sections as valid aliases:
`Language & Framework` supplies language/framework/runtime choices;
`Platform & Deployment` supplies targets/deployment; `Agent Routing`, including
its `File Extension Routing`, supplies specialist routing in its owning domain.
Compare their actual values with `Product Stack` and applicable concept/decision
evidence. A missing parallel section does not erase valid configured facts or
require relocating them. Conflicting values block the affected route.

Classify the current scope after these reads:

- **Game**: consistent substantive Game concept/decision evidence, or actual
  configured engine/domain plus Game behavior evidence, supports `[Game]` paths.
- **Product**: consistent substantive Product concept/decision evidence or actual
  configured Product facts supports `[Product]` paths. Populated legacy
  TypeScript/Bun API/CLI targets and Product specialist routing, for example,
  remain Product without a concept or a new `Product Stack` section.
- **Unknown**: evidence is insufficient, conflicting or mixed without a concrete
  governing scope. Resolve Game or Product using an existing scoped decision or
  confirmation from the user/configured project lead before dependent branches.
  Both concept filenames do not select a branch; independent neutral reporting
  continues while the affected domain-specific work waits.

Record the chosen domain and the actual source sections/values supporting it.
Never silently default to Game. Missing/inaccessible required configuration or
branch inputs leaves the affected check Incomplete; domain selection alone does
not prove runtime availability, test execution, readiness or completion.

## Dual-Domain Parity Contract

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | Actual domain/platform evidence, current release stories, bugs, QA plan/sign-off, build/test outputs, changelog and previous checklist | Same internal originals plus applicable API/web/CLI/package, service, data and security contracts |
| Steps | Audit internal readiness and applicable Game checks; record evidence and existing sign-offs | Audit internal readiness and actual Product surfaces; record evidence and existing sign-offs |
| Outputs | `production/releases/release-checklist-[date].md`, version/scope, verdict, rationale, sign-offs and delta | Same dated path and decision fields, with only applicable Product checks |
| Next steps | `/launch-checklist`, then `/team-release`; fix blockers and rerun checklist when needed | `/launch-checklist`, then `/team-release`; fix blockers and rerun checklist when needed |

---

## Phase 1: Parse Arguments

**[Game]** Read the requested platform (`pc`, `console`, `mobile`, or `all`).
**[Product]** Read the requested surface (`web`, `api`, `cli`, or `all`);
retain other actually configured package/library surfaces too.

An omitted argument or `all` selects all actual targets in this release scope,
not every example below. Compare arguments with populated project configuration,
the scoped release plan and applicable CDD/contract originals. Clarify conflicting
or undeclared targets before dependent checks.

Record each surface and applicable requirement with its supporting original.
A CLI-only package does not acquire a browser, HTTP server, datastore or staging
deployment requirement. An HTTP API does not acquire graphical interaction checks.
A web/native UI retains its actual UI, accessibility and platform requirements.
Apply Game FPS, play sessions, assets and controls only to the corresponding
Game scope. Shared build, QA, severity and required-input gates still apply.

Use `NotApplicable` only when actual configuration/requirements establish that
the surface or feature is absent, with a reason. Unknown applicability or missing
required evidence is `Incomplete`, never PASS or NotApplicable. For unresolved
domain/surface scope, present neutral facts and blockers in conversation and stop
before choosing a Game/Product template or claiming release readiness.

---

## Phase 2: Load Project Context

- Read `CLAUDE.md` and actual technical preferences for version, targets, source/
  test roots and configured build/test/deployment commands; use legacy Product
  sections where populated.
- Read the current scoped milestone/release plan and sprint records from
  `production/milestones/` and `production/sprints/`, following their actual
  Story originals. Establish which stories belong to this release and verify
  each required story is Done; In Review is incomplete.
- Read the project's bug originals/registry in `production/bugs/` or its
  configured owner. An empty candidate set may mean no open bugs only after
  checking the actual registry/scope; missing required bug records are Incomplete.
- Read the applicable QA plan and actual sign-off evidence from `production/qa/`
  or its configured owner, plus current build/test results for the release.
  A planned check, checkbox or old result does not prove current execution.
- Read the current version's changelog and any previous scoped release checklist
  in `production/releases/`. Follow project-owned paths rather than inventing
  replacements. Preserve previous reports and compare resolved, new and unchanged
  items against the current originals.
- Read applicable CDD, platform/surface contracts and release requirements. These
  determine required checks and owners; a template alone does not waive them.

Missing required release, Story, bug, QA or build/test originals leave affected
checks Incomplete and prevent RELEASE READY. A changelog is advisory by default
(CONCERNS if absent); if the project requires it for release, its absence blocks.
Do not manufacture missing inputs, sign-offs or approvals.

---

## Phase 3: Scan Codebase

Scan for outstanding issues:

- Count `TODO` comments
- Count `FIXME` comments
- Count `HACK` comments
- Note their locations and severity

Read actual test outputs and build evidence from configured roots/logs. Use CI
results when CI is configured; offline/local release builds may use their actual
configured build/test evidence. If an integration is unavailable, show MANUAL
CHECK with owner and required evidence; no assumed pass. An outstanding required
manual check is Incomplete and blocks readiness. TODO/FIXME/HACK counts are
review leads, not bug severities or proof of a failed requirement.

---

## Phase 4: Generate the Release Checklist

Generate only the resolved domain/surface sections and append the shared internal
decision below. For every applicable check, record PASS, FAIL or Incomplete and
its actual evidence; unchecked examples are not results. Include the Story, bug,
QA, build/test, changelog and previous-release delta categories for both domains.

### [Game] Internal Game Release Checklist

```markdown
## Release Checklist: [Version] -- [Platform]
Generated: [Date]

### Codebase Health
- TODO count: [N] ([list top 5 if many])
- FIXME count: [N] ([list all -- these are potential blockers])
- HACK count: [N] ([list all -- these need review])

### Build Verification
- [ ] Clean build succeeds on all target platforms
- [ ] No compiler warnings (zero-warning policy)
- [ ] All assets included and loading correctly
- [ ] Build size within budget ([target size])
- [ ] Build version number correctly set ([version])
- [ ] Build is reproducible from tagged commit

### Quality Gates
- [ ] Zero S1 (Critical) bugs
- [ ] Zero S2 (Major) / HIGH bugs; record any existing producer exceptions separately without relabeling failed checks PASS
- [ ] All critical path features tested and signed off by QA
- [ ] Performance within budgets:
  - [ ] Target FPS met on minimum spec hardware
  - [ ] Memory usage within budget
  - [ ] Load times within budget
  - [ ] No memory leaks over extended play sessions
- [ ] No regression from previous build
- [ ] Soak test passed (4+ hours continuous play)

### Content Complete
- [ ] All placeholder assets replaced with final versions
- [ ] All TODO/FIXME in content files resolved or documented
- [ ] All player-facing text proofread
- [ ] All text localization-ready (no hardcoded strings)
- [ ] Audio mix finalized and approved
- [ ] Credits complete and accurate
```

### [Game] External readiness references

The following platform/store/launch examples belong to `/launch-checklist`.
This internal audit may link their actual recorded status where the scoped
release plan requires it. It does not run a second external launch audit or infer
certification, legal acceptance, publication authority or sign-off from these
examples. Include only the actual target/features; unresolved required external
dependencies remain visible and do not become PASS.

Platform-specific reference examples:

**For `pc`:**
```markdown
### Platform Requirements: PC
- [ ] Minimum and recommended specs verified and documented
- [ ] Keyboard+mouse controls fully functional
- [ ] Controller support tested (Xbox, PlayStation, generic)
- [ ] Resolution scaling tested (1080p, 1440p, 4K, ultrawide)
- [ ] Windowed, borderless, and fullscreen modes working
- [ ] Graphics settings save and load correctly
- [ ] Steam/Epic/GOG SDK integrated and tested
- [ ] Achievements functional
- [ ] Cloud saves functional
- [ ] Steam Deck compatibility verified (if targeting)
```

**For `console`:**
```markdown
### Platform Requirements: Console
- [ ] TRC/TCR/Lotcheck requirements checklist complete
- [ ] Platform-specific controller prompts display correctly
- [ ] Suspend/resume works correctly
- [ ] User switching handled properly
- [ ] Network connectivity loss handled gracefully
- [ ] Storage full scenario handled
- [ ] Parental controls respected
- [ ] Platform-specific achievement/trophy integration tested
- [ ] First-party certification submission prepared
```

**For `mobile`:**
```markdown
### Platform Requirements: Mobile
- [ ] App store guidelines compliance verified
- [ ] All required device permissions justified and documented
- [ ] Applicable privacy obligations/policy verified for actual data collection and distribution
- [ ] Data safety/nutrition labels completed
- [ ] Touch controls tested on multiple screen sizes
- [ ] Battery usage within acceptable range
- [ ] Background behavior correct (pause, resume, terminate)
- [ ] Push notification permissions handled correctly
- [ ] In-app purchase flow tested (if applicable)
- [ ] App size within store limits
```

**Store and launch sections (all platforms):**
```markdown
### Store / Distribution
- [ ] Store page metadata complete and proofread
  - [ ] Short description
  - [ ] Long description
  - [ ] Feature list
  - [ ] System requirements (PC)
- [ ] Screenshots up to date and per-platform resolution requirements met
- [ ] Trailers up to date
- [ ] Key art and capsule images current
- [ ] Age rating obtained and configured:
  - [ ] ESRB
  - [ ] PEGI
  - [ ] Other regional ratings as required
- [ ] Legal notices, EULA, and privacy policy in place
- [ ] Third-party license attributions complete
- [ ] Pricing configured for all regions

### Launch Readiness
- [ ] Analytics / telemetry verified and receiving data
- [ ] Crash reporting configured and dashboard accessible
- [ ] Day-one patch prepared and tested (if needed)
- [ ] On-call team schedule set for first 72 hours
- [ ] Community launch announcements drafted
- [ ] Press/influencer keys prepared for distribution
- [ ] Support team briefed on known issues and FAQ
- [ ] Rollback plan documented (if critical issues found post-launch)

```

### [Product] Internal Product Release Checklist

Select checks using the applicability record from Phase 1. Shared package,
build/test, vulnerability/secrets and QA checks remain; service, HTTP, database
and UI checks require those actual surfaces/features. Keep required project
checks even when their evidence is missing.

```markdown
## Release Checklist: [Version] — [Product Release Type]
Generated: [Date]

### Codebase Health
- TODO count: [N] ([list top 5 if many])
- FIXME count: [N] ([list all — these are potential blockers])
- HACK count: [N] ([list all — these need review])
- Dependency audit: [N] outdated, [N] with known vulnerabilities

### Build & Deploy Verification
- [ ] Configured release build succeeds; actual CI result when CI is configured, otherwise actual local/offline build evidence
- [ ] No compiler/linter warnings (zero-warning policy)
- [ ] Required package files included; assets/static files load correctly when delivered
- [ ] Build artifact size within budget
- [ ] Build version number correctly set ([version])
- [ ] Service/deployment pipeline tested, including staging when required by the actual deployment contract
- [ ] Applicable database migrations tested forward and reverse under the actual data/rollback contract

### Quality Gates
- [ ] Zero S1 (Critical) bugs
- [ ] Zero S2 (Major) / HIGH bugs; record existing product-owner exceptions separately without relabeling failed checks PASS
- [ ] All critical path workflows tested and signed off by QA
- [ ] Performance within budgets:
  - [ ] API latency (p95) within target when an API surface is delivered
  - [ ] Memory usage within budget
  - [ ] CLI/package or service startup time within its actual target
  - [ ] No memory leaks under the workload required for the actual surface
- [ ] No regression from previous release
- [ ] Required endurance/load test passed for the actual CLI/package or service workload

### Security
- [ ] Dependency vulnerability scan clean
- [ ] Secrets audit: no credentials in code, logs, or build artifacts
- [ ] Delivered API authentication/authorization meets the actual contract, including any explicitly public endpoints
- [ ] Public endpoint rate limiting tested where required by the API/security contract
- [ ] CORS policy tested when cross-origin browser access is supported
- [ ] CSP headers tested for applicable served web UI
- [ ] Network transport meets the applicable TLS/HTTPS security contract
- [ ] Applicable privacy obligations/policy verified for actual data collection and distribution

### Product-Specific Sections

**For `api`:**
- [ ] OpenAPI/Swagger spec up to date and matches implementation
- [ ] All endpoints respond within budget at p95
- [ ] Error responses follow project convention (consistent format)
- [ ] Applicable rate limiting and pagination contracts tested; absent features have evidenced NotApplicable reasons
- [ ] API versioning strategy clear and communicated
- [ ] Deprecated endpoints have sunset dates documented

**For `web`:**
- [ ] Responsive layout tested (mobile, tablet, desktop)
- [ ] Browser compatibility verified (Chrome, Firefox, Safari, Edge)
- [ ] Accessibility audit passed (target tier)
- [ ] Core Web Vitals within budget (LCP, FID, CLS)
- [ ] Progressive enhancement works without JS (if applicable)
- [ ] Sitemap and robots.txt correct

**For `cli`:**
- [ ] Help text accurate for all commands and subcommands
- [ ] Exit codes consistent (0=success, others = specific errors)
- [ ] Shell completion scripts tested when delivered/required
- [ ] Required man page or reference docs accurate
- [ ] Installation documented and tested for actual supported package managers
```

---

## Shared Internal Release Decision (both domains)

Append these fields to the Game or Product report, including CLI-only reports:

```markdown
### Internal Readiness
| Category | Result | Current original/evidence | Outstanding action / owner |
|---|---|---|---|
| Release stories Done | [PASS / FAIL / Incomplete] | [story originals] | [action] |
| Open bug severity | [PASS / FAIL / Incomplete] | [bug originals / verified empty set] | [action] |
| QA plan and sign-off | [PASS / FAIL / Incomplete] | [plan and actual authority/time] | [action] |
| Build/test stability | [PASS / FAIL / Incomplete] | [applicable executed results] | [action] |
| Changelog | [PASS / advisory concern / FAIL if required] | [current entry / missing] | [action] |

### Delta From Previous Release
- Previous checklist: [actual original / none exists]
- Resolved: [items and current evidence]
- New: [items and current evidence]
- Unchanged / comparison gaps: [items and scope differences]

### Verdict: [RELEASE READY / RELEASE BLOCKED / CONCERNS]
**Rationale:** [current blockers, incomplete required checks, advisory concerns
and evidenced NotApplicable decisions; cite originals and actions/owners]

### Recorded Sign-offs
- QA owner: [actual person/role, decision, authority/time/evidence / pending]
- Project release owner: [actual configured person/role and decision / pending]
- Other project-required roles: [actual requirements and decisions / pending]
```

S1/CRITICAL and S2/HIGH bugs, incomplete release stories, missing
required QA/sign-off, failed required checks or Incomplete required evidence yield
**RELEASE BLOCKED**. Determine severity from the project's actual definitions,
not a blind label conversion. Record exceptions with scope/authority and remaining
risk; a documented exception does not conceal a failed check.

With no blocker, advisory MEDIUM/LOW issues or a default-advisory missing changelog
yield **CONCERNS**. Only all applicable required checks with current evidence and
required sign-offs satisfied, with no unresolved concerns, yield **RELEASE READY**.
The verdict reflects current evidence, not the previous report.

Record existing sign-offs for actual owners; do not synthesize them, spawn director
gates or grant phase advancement. A Game project may require QA Lead, Technical
Director, Producer or Creative Director; a Product project uses its configured QA,
product/release, engineering, security or operations owners as applicable.
`/gate-check` owns formal phase gates. This report grants no deploy, store
submission, external communication or publication authority.

## Phase 5: Save Checklist

Present the checklist with its verdict, rationale, sign-offs, delta, applicable
check counts, blockers and concerns. Keep code-comment counts distinct from bugs.

Use `production/releases/release-checklist-[date].md` with version and scope in
the report. If that path already exists, preserve the prior original and propose
a dated revision path under the project's existing evidence lifecycle; do not
silently overwrite history. Show the exact path/effect draft.

Ask: "May I write this to `[exact selected report path]`?"
Replace the placeholder with the selected new dated path or collision-safe
revision path before asking; never request an overwrite of the preserved original.
Reuse matching existing write authority. If approved, write only that report,
creating its directory within the same scope; report authority does not update
Story, QA, stage, checkpoint, manifest or sign-off state.

---

## Phase 6: Next Steps

- Run `/launch-checklist` for final launch readiness.
- Coordinate final sign-offs and release execution via `/team-release`.
- If the changelog is missing, suggest `/changelog`; keep RELEASE BLOCKED when
  the project requires that changelog, otherwise retain the advisory CONCERNS.
- Fix blockers and rerun `/release-checklist` for RELEASE BLOCKED; address advisory actions for CONCERNS.

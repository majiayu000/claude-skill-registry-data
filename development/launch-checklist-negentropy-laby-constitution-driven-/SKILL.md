---
name: launch-checklist
description: "Complete launch readiness validation. Game: platform certification, store metadata, content, community. Product: deployment strategy, rollback plan, on-call, monitoring."
argument-hint: "[launch-date or 'dry-run']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
---

> **Explicit invocation only**: This skill should only run when the user explicitly requests it with `/launch-checklist`. Do not auto-invoke based on context matching.

## User Guide

- When to use: Complete launch readiness validation. Game: platform certification, store metadata, content, community. Product: deployment strategy, rollback plan, on-call, monitoring.
- Inputs: Command arguments: `/launch-checklist [launch-date or 'dry-run']`; project artifacts referenced below; user decisions and approvals before writes.
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
| Context reads | Game domain evidence/configuration, milestone, release checklist, content calendar, build/store/legal/community/QA artifacts | Product domain evidence/configuration, milestone, release checklist, deployment config/IaC, migration/rollback docs, monitoring/on-call/support/security/docs artifacts |
| Steps | Validate code, content, platform certification, store metadata, localization, analytics, community/support, team readiness | Validate code, data/migrations, deployment strategy, rollback, monitoring/alerts, on-call/support, security/privacy, docs/customer communication, team readiness |
| Outputs | `production/releases/launch-checklist-[date].md` or dry-run report with game launch readiness and sign-offs | Same path/report with product launch readiness, deployment/rollback/on-call/monitoring support sign-offs |
| Next steps | `/team-release`, final store/platform submission, monitor launch, hotfix if needed | `/team-release`, staged production deployment, monitor/on-call, incident or hotfix if needed |

---

## Phase 1: Parse Arguments

Read the argument for the launch date or `dry-run` mode. Dry-run mode generates the checklist without creating sign-off entries or writing files.

---

## Phase 2: Gather Project Context

- Read `CLAUDE.md` for tech stack, target platforms, and team structure
- Read the latest milestone in `production/milestones/`
- Read any existing release checklist in `production/releases/`
- **[Game]** Read the content calendar in `design/live-ops/content-calendar.md` if it exists
- **[Product]** Read deployment configuration and infrastructure-as-code files if they exist

---

## Phase 3: Scan Codebase Health

- Count `TODO`, `FIXME`, `HACK` comments and their locations
- Check for any `console.log`, `print()`, or debug output left in production code
- **[Game]** Check for placeholder assets (search for `placeholder`, `temp_`, `WIP_`)
- **[Product]** Check for hardcoded test/dev values (localhost, test credentials, debug flags)
- Check for exposed secrets, API keys, or credentials

---

## Phase 4: Generate the Launch Checklist

The launch checklist structure depends on domain detection from Phase 0.

### [Game] — Game Launch Checklist

```markdown
# Launch Checklist: [Game Title]
Target Launch: [Date or DRY RUN]
Generated: [Date]

---

## 1. Code Readiness

### Build Health
- [ ] Clean build on all target platforms
- [ ] Zero compiler warnings
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Performance benchmarks within targets
- [ ] No memory leaks (verified via extended soak test)
- [ ] Build size within platform limits
- [ ] Build version correctly set and tagged in source control

### Code Quality
- [ ] TODO count: [N] (zero required for launch, or documented exceptions)
- [ ] FIXME count: [N] (zero required)
- [ ] HACK count: [N] (each must have documented justification)
- [ ] No debug output in production code
- [ ] No hardcoded dev/test values
- [ ] All feature flags set to production values
- [ ] Error handling covers all critical paths
- [ ] Crash reporting integrated and verified

### Security
- [ ] No exposed API keys or credentials in source
- [ ] Save data encrypted
- [ ] Network communication secured (TLS/DTLS)
- [ ] Anti-cheat measures active (if multiplayer)
- [ ] Input validation on all server endpoints (if multiplayer)
- [ ] Privacy policy compliance verified

---

## 2. Content Readiness

### Assets
- [ ] All placeholder art replaced with final assets
- [ ] All placeholder audio replaced with final audio
- [ ] Audio mix finalized and approved by audio director
- [ ] All VFX polished and performance-verified
- [ ] No missing or broken asset references
- [ ] Asset naming conventions enforced

### Text and Localization
- [ ] All player-facing text proofread
- [ ] No hardcoded strings (all externalized for localization)
- [ ] All supported languages translated and verified
- [ ] Text fits UI in all languages (text fitting pass complete)
- [ ] Font coverage verified for all supported languages
- [ ] Credits complete, accurate, and up to date

### Game Content
- [ ] All levels/maps playable from start to finish
- [ ] Tutorial flow complete and tested with new players
- [ ] All achievements/trophies implemented and tested
- [ ] Save/load works correctly for all game states
- [ ] Difficulty settings balanced and tested
- [ ] End-game/credits sequence complete

---

## 3. Quality Assurance

### Testing
- [ ] Full regression test suite passed
- [ ] Zero S1 (Critical) bugs open
- [ ] Zero S2 (Major) bugs open (or documented exceptions)
- [ ] Soak test passed (8+ hours continuous play)
- [ ] Multiplayer stress test passed (if applicable)
- [ ] All critical user paths tested on every platform
- [ ] Edge cases tested (full storage, no network, suspend/resume)

### Platform Certification
- [ ] PC: Steam/Epic/GOG SDK requirements met
- [ ] Console: TRC/TCR/Lotcheck submission prepared
- [ ] Mobile: App Store/Play Store guidelines compliant
- [ ] Accessibility: minimum standards met (remapping, text scaling, colorblind)
- [ ] Age ratings obtained (ESRB, PEGI, regional)

### Performance
- [ ] Target FPS met on minimum spec hardware
- [ ] Load times within budget on all platforms
- [ ] Memory usage within budget on all platforms
- [ ] Network bandwidth within targets (if multiplayer)
- [ ] No frame hitches in critical gameplay moments

---

## 4. Store and Distribution

### Store Pages
- [ ] Store page copy finalized and proofread
- [ ] Screenshots current and per-platform resolution
- [ ] Trailers current and approved
- [ ] Key art and capsule images finalized
- [ ] System requirements accurate (PC)
- [ ] Pricing configured for all regions
- [ ] Pre-purchase/wishlist campaigns active (if applicable)

### Legal
- [ ] EULA finalized and approved by legal
- [ ] Privacy policy published and linked
- [ ] Third-party license attributions complete
- [ ] Music/audio licensing verified
- [ ] Trademark/IP clearance confirmed
- [ ] GDPR/CCPA compliance verified (data collection, consent, deletion)

---

## 5. Infrastructure

### Servers (if multiplayer/online)
- [ ] Production servers provisioned and load-tested
- [ ] Auto-scaling configured and tested
- [ ] Database backups configured
- [ ] CDN configured for content delivery
- [ ] DDoS protection active
- [ ] Monitoring and alerting configured

### Analytics and Monitoring
- [ ] Analytics pipeline verified and receiving data
- [ ] Crash reporting active and dashboard accessible
- [ ] Server monitoring dashboards live
- [ ] Key metrics tracked: DAU, session length, retention, crashes
- [ ] Alerts configured for critical thresholds

---

## 6. Community and Marketing

### Community Readiness
- [ ] Community guidelines published
- [ ] Moderation team briefed and tools ready
- [ ] Discord/forum/social channels set up
- [ ] FAQ and known issues page prepared
- [ ] Support email/ticketing system active

### Marketing
- [ ] Launch trailer published
- [ ] Press/influencer review keys distributed
- [ ] Social media launch posts scheduled
- [ ] Launch day blog post/dev update drafted
- [ ] Patch notes for launch version published

---

## 7. Operations

### Team Readiness
- [ ] On-call schedule set for first 72 hours post-launch
- [ ] Incident response playbook reviewed by team
- [ ] Rollback plan documented and tested
- [ ] Hotfix pipeline tested (can ship emergency fix within 4 hours)
- [ ] Communication plan for launch issues (who posts, where, how fast)

### Day-One Plan
- [ ] Day-one patch prepared (if needed)
- [ ] Server unlock/go-live procedure documented
- [ ] Launch monitoring dashboard bookmarked by all leads
- [ ] War room/channel established for launch day

---

## Go / No-Go Decision

**Overall Status**: [READY / NOT READY / CONDITIONAL]

### Blocking Items
[List any items that must be resolved prior to launch]

### Conditional Items
[List items that have documented workarounds or accepted risk]

### Sign-Offs Required
- [ ] Creative Director — Content and experience quality
- [ ] Technical Director — Technical health and stability
- [ ] QA Lead — Quality and test coverage
- [ ] Producer — Schedule and overall readiness
- [ ] Release Manager — Build and deployment readiness
```

---

### [Product] — Product Launch Checklist

```markdown
# Launch Checklist: [Product Title]
Target Launch: [Date or DRY RUN]
Generated: [Date]

---

## 1. Code Readiness

### Build Health
- [ ] Clean build in CI on all target platforms
- [ ] Zero compiler/linter warnings
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Performance benchmarks within targets
- [ ] Build artifact version correctly set and tagged in source control
- [ ] Dependency audit clean (no critical vulnerabilities)

### Code Quality
- [ ] TODO count: [N] (zero required for launch, or documented exceptions)
- [ ] FIXME count: [N] (zero required)
- [ ] HACK count: [N] (each must have documented justification)
- [ ] No debug output in production code
- [ ] No hardcoded dev/test values
- [ ] All feature flags set to production values
- [ ] Error handling covers all critical paths
- [ ] Crash/error reporting integrated and verified

### Security
- [ ] No exposed API keys or credentials in source or artifacts
- [ ] Dependency vulnerability scan clean
- [ ] Authentication/authorization on all protected endpoints
- [ ] Rate limiting configured for public endpoints
- [ ] TLS/HTTPS enforced
- [ ] Input validation on all API endpoints
- [ ] CORS configuration correct (if web/API)
- [ ] CSP headers configured (if web)
- [ ] Privacy policy compliance verified
- [ ] Secrets rotated from dev/staging values

---

## 2. Data Readiness

### Database
- [ ] All migrations tested forward and reverse
- [ ] Migration applied to staging and verified
- [ ] Database backup configured and tested
- [ ] Connection pooling configured for production load
- [ ] Query performance verified (no full table scans on critical paths)
- [ ] Data retention/pruning policies documented

### Data Integrity
- [ ] Seed/migration data verified
- [ ] Foreign key and constraint validation clean
- [ ] No orphaned or inconsistent data in staging
- [ ] GDPR/CCPA data deletion workflow tested

---

## 3. Quality Assurance

### Testing
- [ ] Full regression test suite passed
- [ ] Zero S1 (Critical) bugs open
- [ ] Zero S2 (Major) bugs open (or documented exceptions)
- [ ] Contract tests passing for all API endpoints
- [ ] E2E tests passing for critical user workflows
- [ ] Load/stress test passed (target throughput sustained)
- [ ] Smoke tests passing on staging

### Accessibility
- [ ] Accessibility tier verified (from `design/accessibility-requirements.md`)
- [ ] Keyboard navigation complete (web)
- [ ] Screen reader compatibility verified (if Comprehensive tier)
- [ ] Color contrast verified

### Performance
- [ ] API latency (p95) within budget
- [ ] Cold start time within budget
- [ ] Memory usage within budget under sustained load
- [ ] No memory leaks (verified via extended soak test)

---

## 4. Infrastructure

### Deployment
- [ ] Production infrastructure provisioned
- [ ] Auto-scaling configured and tested
- [ ] Database replicas configured (if needed)
- [ ] CDN configured (if web)
- [ ] DNS configured and propagated
- [ ] SSL certificates provisioned and auto-renewal configured
- [ ] DDoS protection active

### Monitoring and Observability
- [ ] Application monitoring dashboards live
- [ ] Infrastructure monitoring configured
- [ ] Log aggregation configured
- [ ] Error/crash tracking active
- [ ] Alerts configured for critical thresholds
- [ ] Key metrics tracked: request rate, error rate, latency, saturation
- [ ] On-call rotation set with escalation paths

---

## 5. Operations

### Team Readiness
- [ ] On-call schedule set for first 72 hours post-launch
- [ ] Incident response playbook reviewed by team
- [ ] Rollback plan documented and tested
- [ ] Hotfix pipeline tested (can ship emergency fix)
- [ ] Communication plan for launch issues (who posts, where, how fast)
- [ ] Runbook for common operational tasks documented

### Day-One Plan
- [ ] Deployment runbook step-by-step documented
- [ ] Launch sequence checklist (order of operations)
- [ ] Launch monitoring dashboard bookmarked by all leads
- [ ] War room/channel established for launch day
- [ ] Post-launch validation steps defined

---

## 6. Documentation and Communication

### Documentation
- [ ] API docs up to date (OpenAPI/Swagger or equivalent)
- [ ] Developer docs / setup guide verified (new dev can onboard)
- [ ] User docs / help center updated (if applicable)
- [ ] Changelog / release notes published
- [ ] Architecture docs reflect production deployment

### Communication
- [ ] Release announcement drafted
- [ ] Migration guide written (if breaking changes)
- [ ] Deprecation notices published (if applicable)
- [ ] Support team briefed on known issues and FAQ
- [ ] Status page updated with maintenance window (if applicable)

---

## Go / No-Go Decision

**Overall Status**: [READY / NOT READY / CONDITIONAL]

### Blocking Items
[List any items that must be resolved prior to launch]

### Conditional Items
[List items that have documented workarounds or accepted risk]

### Sign-Offs Required
- [ ] Lead Programmer — Code quality and architecture
- [ ] QA Lead — Quality and test coverage
- [ ] Product Owner — Feature completeness and user value
- [ ] Operations/SRE — Infrastructure and monitoring readiness
```

---

## Phase 5: Save Checklist

Present the completed checklist and summary to the user (total items, blocking items count, conditional items count, departments with incomplete sections).

If not in dry-run mode, ask: "May I write this to `production/releases/launch-checklist-[date].md`?"

If yes, write the file, creating directories as needed.

---

## Phase 6: Next Steps

- Run `/team-release` for final release orchestration and sign-offs.
- **[Game]** Complete final store/platform submission, then monitor launch and use `/hotfix` if needed.
- **[Product]** Complete the staged production deployment, then monitor on-call signals and use incident response or `/hotfix` if needed.

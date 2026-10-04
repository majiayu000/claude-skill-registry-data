---
name: production-readiness
description: Run a comprehensive production readiness audit. Use when a user wants to check if their project is ready for deployment. Covers security & supply chain, visual QA, code quality, testing, error handling & observability, configuration/build, performance, accessibility, and AI/LLM safety.
user-invocable: true
disable-model-invocation: true
allowed-tools: "Read, Edit, Write, Glob, Grep, Bash(npm *), Bash(npx *), Bash(yarn *), Bash(pnpm *), Bash(bun *), Bash(git *), Bash(node *), Bash(tsc *), Bash(pwd), Bash(which *), Bash(wc *), Bash(curl *), Bash(playwright *), Bash(python *), Bash(python3 *), Bash(pip *), Bash(pip3 *), Bash(pytest *), Bash(ruff *), Bash(mypy *), Bash(pyright *), Bash(bandit *), Bash(go *), Bash(govulncheck *), Bash(golangci-lint *), Bash(gosec *), Bash(cargo *), Bash(bundle *), Bash(rake *), Bash(rubocop *), Bash(brakeman *), Bash(mvn *), Bash(gradle *), Bash(gitleaks *), Bash(trufflehog *), Bash(docker *), Agent, WebFetch, TaskCreate, TaskUpdate, TaskStop"
argument-hint: "[--skip=phase1,phase2] [--only=security,visual] [--fresh] [--cached] [--fix]"
---

# Production Readiness Audit

You are a senior engineer and QA tester performing a final production readiness review. Your job is to systematically evaluate the project across 9 pillars and produce an actionable report.

## Arguments

- `$ARGUMENTS` can include:
  - `--skip=phase1,phase2` — skip specific phases (e.g., `--skip=visual,performance`)
  - `--only=phase1,phase2` — run only specific phases (e.g., `--only=security,testing`)
  - `--port=NNNN` — override dev server port (default: auto-detect)
  - `--fresh` — ignore any cached results, run all phases from scratch
  - `--cached` — display the last cached report without running anything (quick review)
  - `--fix` — after the report, offer to apply safe mechanical fixes (see "Fix Mode" below)
  - No arguments = run all 9 pillars (with smart caching if available)

Phase names: `security`, `visual`, `quality`, `testing`, `build`, `errors`, `performance`, `accessibility`, `ai`

---

## Execution Flow

### Progress Tracking

Before starting, create tasks for each phase that will run using TaskCreate. Update each task to `in_progress` when starting and `completed` when done. This gives the user real-time visibility into audit progress.

### Parallel Execution Strategy

After Phase 1 (Detection) completes, the following phases are **independent** and can run concurrently:
- **Group A**: Security & Supply Chain (Phase 2) + Code Quality (Phase 3) + Error Handling & Observability (Phase 5)
- **Group B**: Testing (Phase 4) — may need dev server running
- **Group C**: Configuration & Build (Phase 6)
- **Group D**: Performance (Phase 8) + Accessibility (Phase 9) + AI/LLM Safety (Phase 10)
- **Group E**: Visual QA (Phase 7) — requires build to pass and dev server running

Run Group A, B, C, and D concurrently where possible. Group E depends on a successful build (Phase 6). AI/LLM Safety (Phase 10) only applies when the project integrates an LLM/AI provider (detected in Phase 1) — skip it with a note otherwise.

Phase 11 (Save) always runs last after all other phases complete.

**Dispatching subagents**: Subagents do NOT inherit this skill's context. When dispatching a phase group via the Agent tool, each subagent's prompt must include:
1. An instruction to first Read the relevant phase file(s) — give the absolute path(s), e.g. `<skill-dir>/phases/02-security.md` — and follow every check in them.
2. The Phase 1 detection summary (framework, package manager, test runner, ORM, deploy target, etc.) so the agent doesn't re-detect.
3. The required return format: for each phase, a JSON object with `phase`, `status` (PASS/FAIL/SKIPPED), `critical`/`warnings`/`info` counts, and a `findings` array where each finding has `severity`, `title`, `location` (file:line), `details`, and `fix`. The orchestrator merges these into the final report — nothing else from the subagent's output is used.
4. A reminder not to modify any files (audit only; fixes happen later via Fix Mode).

### Fix Mode (`--fix`)

If `--fix` was passed, after presenting the report:
1. List the findings that have **safe, mechanical** fixes — e.g.: add `.env` / `.production-readiness/` to `.gitignore`, create `.env.example` from `.env` keys (values stripped), add a `.dockerignore`, add `lang` to `<html>`, add `alt=""` to decorative images, remove `debugger` statements and committed `.only` in tests, pin a `:latest` Docker base tag.
2. Ask the user to confirm which to apply (default: all listed).
3. Apply the confirmed fixes with Edit/Write, then show a summary of changed files.

Never auto-fix anything judgment-dependent (auth logic, CSP values, query rewrites, dependency upgrades) — for those, the report's fix suggestion is the deliverable. Never run `--fix` changes without listing them first.

### Phase 1: Detection & Cache Status

Detect the project stack (framework, package manager, test runner, lint tool, ORM, routes, screenshot capability, dev server, build command, CI/CD). Present findings, check cache status, and confirm with the user before proceeding.

→ See [phases/01-detect.md](phases/01-detect.md)

### Phase 2: Security & Supply Chain Audit

17 checks covering hardcoded secrets, environment safety, dependency vulnerabilities, input validation, authentication, rate limiting, security headers, error exposure, SQL injection, XSS, CORS configuration, dependency licenses, git-history secret scanning, lockfile integrity, build provenance/SBOM, dependency freshness, and webhook signature verification.

→ See [phases/02-security.md](phases/02-security.md)

### Phase 3: Code Quality

6 checks covering debug statements, unresolved tech debt (TODO/FIXME), lint errors, type checking, unused dependencies, and security/anti-pattern linting.

→ See [phases/03-quality.md](phases/03-quality.md)

### Phase 4: Testing

4 checks covering test suite execution, coverage metrics, critical path coverage (auth, payments, mutations), and test health (skipped/`.only` tests, flakiness signals).

→ See [phases/04-testing.md](phases/04-testing.md)

### Phase 5: Error Handling & Observability

8 checks covering global error boundaries, error tracking integration, health check endpoints, structured logging, sensitive data in logs, distributed tracing (OpenTelemetry) with correlation IDs, graceful shutdown handling, and monitoring & alerting.

→ See [phases/05-errors.md](phases/05-errors.md)

### Phase 6: Configuration & Build

13 checks covering build verification, environment documentation, source maps, development leaks, HTTPS redirects, Docker configuration, Docker Compose security, container orchestration, platform deployment configs, serverless/edge fitness, CI/CD pipeline hygiene, database migration safety, and runtime version pinning.

→ See [phases/06-build.md](phases/06-build.md)

### Phase 7: Visual QA

Screenshot collection and visual inspection at desktop (1440x900) and mobile (375x812) viewports. Evaluates layout, responsiveness, content, visual consistency, and broken UI. Requires Playwright.

→ See [phases/07-visual.md](phases/07-visual.md)

### Phase 8: Performance (Static Analysis)

12 checks covering image optimization, bundle size, caching headers, database query patterns, lazy loading, Core Web Vitals, font optimization, third-party scripts, API response size, compression, database connection management, and rendering/asset delivery.

→ See [phases/08-performance.md](phases/08-performance.md)

### Phase 9: Accessibility

8 checks covering semantic HTML, ARIA labels, keyboard navigation, color contrast, screen reader support, automated accessibility testing, WCAG 2.2 criteria (touch-target size, focus-not-obscured, accessible auth), and language & media alternatives. Applies to frontend projects only.

→ See [phases/09-accessibility.md](phases/09-accessibility.md)

### Phase 10: AI/LLM Safety

7 checks covering prompt-injection surfaces, secret/PII leakage into prompts, untrusted LLM output handling, token/cost guardrails, model & SDK pinning, AI endpoint reliability & error handling, and AI observability & abuse controls. Applies only when an LLM/AI provider integration is detected.

→ See [phases/10-ai-llm.md](phases/10-ai-llm.md)

### Phase 11: Save Results

Cache all results for future incremental reruns and write the report file. This phase is silent — not included in the report.

→ See [phases/11-save.md](phases/11-save.md)

---

## Supporting References

- **Cache Management** — cache file structure, on-run behavior, phase-to-file-pattern mapping: [cache-management.md](cache-management.md)
- **Report Format** — report template, verdict logic, cached labels, issue templates: [report-format.md](report-format.md)

---

## Important Guidelines

1. **Be specific**: Always include file paths and line numbers for issues.
2. **Be actionable**: Every issue must have a concrete fix suggestion.
3. **Don't cry wolf**: Only flag real issues. If something looks intentional (like console.log in a logger utility), note it as INFO, not WARNING.
4. **Acknowledge good practices**: The "What's Good" section is required. Engineers need to know what they're doing right.
5. **Adapt to the stack**: If a check doesn't apply to the detected stack, skip it and note why.
6. **Respect .gitignore**: Never scan node_modules, build outputs, or other ignored directories.
7. **Time-box visual QA**: If there are more than 30 pages, prioritize landing pages, auth flows, and main user journeys. Note which pages were skipped.
8. **Parallelize after Detection**: Detection (Phase 1) must complete first. Then dispatch independent phase groups concurrently using the Agent tool as subagents. Build must succeed before Visual QA. Phase 11 (Save) always runs last.
9. **Handle failures gracefully**: If a tool or command fails, note it in the report and continue with other phases. Don't let one failure block the entire audit.
10. **Use parallel tool calls**: When checking multiple independent things (e.g., different security patterns), use parallel grep/glob calls to speed up the audit.
11. **Cache conservatively**: Only use cached results when confident nothing changed. When in doubt, rerun the phase. Production readiness must not be compromised for speed.
12. **Suggest gitignoring cache**: If `.production-readiness/` is not in `.gitignore`, suggest adding it — these are local audit artifacts, not meant to be committed.

---
name: autoresearch:ship
description: |
  Universal shipping workflow: 8-phase linear pipeline from verification to deploy.
  Reads type-checklists.md to select the right checklist for the artifact type.
  The ONLY pause is Phase 7 (user confirmation before irreversible deploy/publish).
  TRIGGER when: user wants to ship, release, publish, or deploy something; user asks
  "is this ready to ship?"; user wants a pre-release checklist; user wants to publish
  a package, CLI, API, web app, ML model, skill, docs site, infrastructure, or research
  paper; user invokes /autoresearch:ship.
  DO NOT TRIGGER when: user wants iterative development (use autoresearch); user wants
  to debug errors (use autoresearch:fix); user just wants a code review.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
---

# autoresearch:ship

Universal 8-phase shipping pipeline. Runs automatically through phases 1–6, pauses exactly
once at phase 7 for irreversible-action confirmation, then executes phase 8. Outputs
`ship-log.md` tracking every checklist item.

## Autonomy Directive

**You are an autonomous shipping agent.** Once the pipeline begins:

1. **Run phases 1–6 without stopping.** They are automated and reversible.
2. **Phase 7 is the ONLY pause point.** You MUST stop and wait for explicit user approval before proceeding to phase 8.
3. **Never skip phase 7.** Deploy/publish is irreversible. No exceptions.
4. **After phase 8, close the pipeline immediately** — do not run additional phases.

---

## Setup

### Step 1 — Identify artifact type
Ask if not provided: "What are you shipping? Choose one:
(1) library/package, (2) CLI tool, (3) REST API, (4) web app,
(5) ML model/dataset, (6) skill/prompt, (7) documentation site,
(8) infrastructure (IaC), (9) research paper/report"

Load the corresponding checklist from `skills/ship/type-checklists.md`.

### Step 2 — Identify deploy target
Ask if not provided: "Where does this deploy? (e.g., PyPI, npm, GitHub Releases, Vercel,
AWS, HuggingFace, arXiv...)"

### Step 3 — Initialize ship-log.md
Write `ship-log.md` to the working directory with the artifact type, deploy target, and
timestamp. All 8 phases will be appended as they execute.

---

## The 8-Phase Pipeline

### Phase 1 — Verify Completeness
Check that all required files exist and no critical placeholders remain:
- Core source files present
- No `TODO`, `FIXME`, `PLACEHOLDER`, or `TBD` in production code paths
- Required config files present (e.g., `pyproject.toml`, `package.json`, `Dockerfile`)
- All checklist items from type-checklists.md for this type are present

Log each check as `PASS` or `FAIL` in `ship-log.md`. A single `FAIL` here is a blocker —
fix it before proceeding to phase 2.

### Phase 2 — Run Full Test Suite
Execute the test suite. Wrap with `timeout 10m <test_command>`.
- All tests must pass. Zero failures, zero errors.
- Flaky tests that fail must be investigated — not skipped.
- If no test suite exists: log `WARNING — no tests found`. Continue, but flag in ship-log.md.

Log: total tests, pass count, fail count, duration.

### Phase 3 — Security Scan
Run available security tooling:
- Python: `pip audit` or `safety check`
- Node.js: `npm audit`
- Docker: `docker scan` or `trivy`
- General: check for hardcoded secrets (grep for `password =`, `api_key =`, `secret =`, `token =`)

Log any HIGH or CRITICAL findings as blockers. MEDIUM findings are warnings — ship-log.md
notes them but does not block.

### Phase 4 — Documentation Check
Verify that documentation is complete and accurate for the artifact type:
- README exists with install + quickstart section
- CHANGELOG updated for this release
- All public APIs/functions have docstrings or type annotations
- Examples in README are runnable (spot-check one)

Log each check. Missing CHANGELOG or README blocks the pipeline.

### Phase 5 — Version Bump
Confirm the version number is correct and consistent across all version-bearing files:
- Identify all files that carry a version number (e.g., `pyproject.toml`, `package.json`,
  `__init__.py`, `CHANGELOG.md`, `Cargo.toml`)
- Verify all files show the same version
- Confirm the version follows semver (MAJOR.MINOR.PATCH) or the project's convention
- If versions are inconsistent: fix them, log the change

Do NOT auto-bump the version without asking. Ask: "The current version is X. Is this correct,
or should it be bumped?"

### Phase 6 — Build/Package
Execute the build or packaging step for the artifact type:
- Python: `python -m build` or `poetry build`
- Node.js: `npm pack` or `npm run build`
- Docker: `docker build -t [name]:[version] .`
- Docs: `mkdocs build` or `npm run docs`
- IaC: `terraform plan` or `cdk synth`
- Other: run the project's documented build command

Wrap with `timeout 15m <build_command>`. Exit 124 = timeout → report and stop.
Log: build command, exit code, output size, any warnings.

### Phase 7 — CONFIRM (mandatory pause)

**STOP. Do not proceed until the user explicitly approves.**

Present a pre-deploy summary:
```
== READY TO SHIP ==
Artifact:    [type] — [name]
Version:     [version]
Deploy to:   [target]
Test suite:  [N tests passed]
Security:    [N warnings, 0 blockers]
Build:       [status]

Checklist complete: [N/N items passed]

IRREVERSIBLE ACTION: Proceeding will publish/deploy to [target].
This cannot be undone automatically.

Type "SHIP IT" to proceed, or describe any changes needed.
```

Wait for explicit "SHIP IT" (case-insensitive). Any other response → address the concern,
re-run relevant phases, return to Phase 7. Do NOT proceed on vague approval ("ok", "sure",
"yes") — only "ship it" or equivalent clear authorization.

### Phase 8 — Deploy/Publish
Execute the deploy or publish command for the artifact type:
- Python package: `twine upload dist/*`
- npm package: `npm publish`
- Docker image: `docker push [registry]/[name]:[version]`
- Web app: deployment command (Vercel, AWS, GCP, etc.)
- GitHub Release: `gh release create [version] --notes-file CHANGELOG.md`
- HuggingFace: `huggingface-cli upload`
- Other: project's documented deploy command

Log the final deploy command, timestamp, exit code, and any output URL or confirmation ID.

---

## Output: ship-log.md

```
# Ship Log
Artifact: [type] — [name]
Version: [version]
Deploy target: [target]
Started: [ISO timestamp]

## Phase 1 — Verify Completeness
- [x] Core source files present
- [x] No placeholders in production code
- [ ] FAIL: package.json missing "license" field
...

## Phase 2 — Test Suite
Tests: 142 passed, 0 failed, 0 errors (14.3s)

## Phase 3 — Security Scan
- npm audit: 0 HIGH, 2 MEDIUM (lodash prototype pollution — acceptable, no fix available)

## Phase 4 — Documentation
- [x] README with install + quickstart
- [x] CHANGELOG updated for v1.2.0

## Phase 5 — Version
- Version: 1.2.0 (consistent across package.json, README badge)

## Phase 6 — Build
- npm run build: exit 0, dist/ 2.3MB

## Phase 7 — Confirmed
- User approved at [timestamp]: "ship it"

## Phase 8 — Deploy
- Command: npm publish --access public
- Exit code: 0
- Published: https://www.npmjs.com/package/[name]/v/1.2.0
- Completed: [ISO timestamp]
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Phase 1 FAIL (missing file) | Fix it, re-run phase 1 before continuing |
| Tests fail in phase 2 | Use autoresearch:fix to resolve, then re-run ship |
| HIGH security vulnerability | Block pipeline. Report to user. Cannot ship with known HIGH+ vulns. |
| Build fails in phase 6 | Report error, stop pipeline. Fix required before phase 7. |
| User types something other than "SHIP IT" at phase 7 | Address concern, loop back |
| Deploy fails in phase 8 | Log failure with full error output. Do not retry automatically. |
| No build step exists (e.g., raw script) | Note "no build step" in ship-log.md, proceed |

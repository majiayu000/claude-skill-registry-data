---
name: pair-capability-setup-gates
description: "Configures CI/CD quality gates per quality-assurance guidelines, producing pipeline configuration for the adopted tech stack. Reads existing gate config from way-of-working. Idempotent: detects existing configuration, confirms rather than re-configuring."
version: 0.4.1
author: Foomakers
---

# /pair-capability-setup-gates — Quality Gate Configuration

Configure CI/CD quality gates for the project. Reads quality assurance guidelines and the adopted tech stack to produce appropriate pipeline configuration. Writes gate configuration to [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) and CI/CD pipeline files.

## Arguments

| Argument | Required | Description                                                                                 |
| -------- | -------- | ------------------------------------------------------------------------------------------- |
| `$scope` | No       | Limit to specific gate type: `pre-commit`, `ci`, `pre-production`, `all` (default: `all`)   |

## Composed Skills

| Skill              | Type       | Required                                                |
| ------------------ | ---------- | ------------------------------------------------------- |
| `/pair-capability-record-decision` | Capability | Yes — records gate configuration decision               |

## Algorithm

### Step 1: Check Existing Configuration

1. **Check**: Read [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) → look for Quality Gates section and Custom Gate Registry.
2. **Check**: Scan for existing CI/CD pipeline files (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, etc.).
3. **Branch**:
   - **Gates fully configured** (Quality Gates section + Custom Gate Registry + pipeline files exist) → present current config:

     > Quality gates already configured:
     > - Quality gate command: `[command]`
     > - Custom gates: [N gates listed]
     > - CI/CD pipeline: [file(s)]
     >
     > Update configuration? (Only if developer explicitly requests.)

     If developer confirms → exit. If update requested → proceed to Step 2.

   - **Partially configured** → identify gaps and proceed to Step 2.
   - **Not configured** → proceed to Step 2.

### Step 2: Read Guidelines and Tech Stack

1. **Act**: Read quality assurance guidelines:
   - [quality-assurance.md](../../../.pair/knowledge/guidelines/technical-standards/git-workflow/quality-assurance.md) — gate types and checklists
   - [quality-gates.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-standards/quality-gates.md) — gate framework and registry format
2. **Act**: Read adopted tech stack:
   - [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — languages, test framework, linter, formatter
   - [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) — existing process
3. **Verify**: Guidelines and stack loaded.

### Step 3: Propose Gate Configuration

1. **Act**: Based on the adopted tech stack and guidelines, propose gates per scope:

   **Pre-commit gates** (local developer machine):
   - Lint check (e.g., `eslint`, `biome`)
   - Type check (e.g., `tsc --noEmit`)
   - Formatting (e.g., `prettier --check`)

   **CI gates** (pipeline on push/PR):
   - All pre-commit gates
   - Test suite with coverage
   - Build verification
   - Custom gates from registry

   **Pre-production gates** (before deployment):
   - All CI gates
   - Security scan (if adopted)
   - Performance benchmarks (if applicable)

2. **Act**: Present the proposal:

   > **Quality Gate Proposal:**
   >
   > | Stage | Gate | Command | Required |
   > |-------|------|---------|----------|
   > | Pre-commit | Lint | `[command]` | Yes |
   > | ... | ... | ... | ... |
   >
   > Accept this configuration?

3. **Verify**: Developer approves. If changes needed → adjust.

### Step 4: Write Configuration

1. **Act**: Update [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md):
   - Set quality gate command (e.g., `pnpm quality-gate`)
   - Write or update Custom Gate Registry table
2. **Act**: Generate CI/CD pipeline configuration appropriate for the adopted stack and hosting:
   - GitHub Actions → `.github/workflows/quality.yml`
   - GitLab → `.gitlab-ci.yml` quality stage
   - Other → document commands for manual pipeline setup
3. **Verify**: Configuration files written.

### Step 5: Record Decision

1. **Act**: Compose `/pair-capability-record-decision`:
   - `$type: non-architectural`
   - `$topic: quality-gate-configuration`
   - `$summary: "Quality gates configured: [gate list]. Command: [command]. CI: [pipeline type]."`
2. **Verify**: Decision recorded.

## Output Format

```text
GATE CONFIGURATION COMPLETE:
├── Quality Command: [command]
├── Pre-commit:      [N gates configured]
├── CI:              [N gates configured]
├── Pre-production:  [N gates configured | N/A]
├── Pipeline:        [file path | manual]
├── Adoption:        [way-of-working.md — updated]
├── Record:          [ADL path — created]
└── Status:          [Complete | Confirmed existing | Updated]
```

## Composition Interface

When composed by `/pair-process-bootstrap`:

- **Input**: `/pair-process-bootstrap` invokes `/pair-capability-setup-gates` during project setup to establish initial quality gates.
- **Output**: Returns gate configuration summary. `/pair-process-bootstrap` includes changes in the bootstrap commit.

When invoked **independently**:

- Full interactive flow. Developer reviews and approves gate configuration.

## Graceful Degradation

- If quality-assurance guidelines are not found, propose minimal gates based on detected package.json scripts (test, lint, build).
- If tech-stack.md is not found, ask developer for tooling choices to generate appropriate gate commands.
- If `/pair-capability-record-decision` is not installed, warn and skip decision recording.
- If no CI/CD platform is detectable, document gate commands for manual execution and skip pipeline file generation.

## Notes

- This skill **modifies files** — it writes to way-of-working.md and creates/updates CI/CD pipeline configuration.
- **Idempotent**: re-invocation on an already-configured project confirms the existing configuration. Update only on explicit developer request.
- Gate commands must be executable in the project's development environment. Verify commands exist before writing.
- Custom Gate Registry format follows the table schema from [quality-gates.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-standards/quality-gates.md): Order, Gate, Command, Scope Key, Required, Description.

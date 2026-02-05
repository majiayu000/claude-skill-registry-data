---
name: looplia-e2e
description: |
  Comprehensive E2E testing for looplia CLI. Tests Docker deployments,
  published CLI versions, and local development. Verifies workflow
  execution, skill architecture (v0.6.9+), and command initialization
  (v0.6.10+). Use when testing looplia releases, CI validation, or
  verifying Docker builds.
license: MIT
compatibility: Requires Docker, jq, and bun. Works with Claude Code.
metadata:
  author: looplia
  version: "0.6.10"
---

# Looplia E2E Test Skill

Comprehensive end-to-end testing for looplia CLI covering Docker deployments, published CLI validation, and local development testing.

## Quick Reference

| Test Mode | When to Use | Script |
|-----------|-------------|--------|
| Docker E2E | Development testing, CI | `scripts/docker-e2e.sh` |
| Published CLI | After CI passes on main | `scripts/published-cli-e2e.sh` |
| Local Development | Quick iteration | Manual commands below |
| v0.6.10 Verification | Version-specific checks | `scripts/check-v0610.sh` |

## Test Modes

### Mode 1: Docker E2E (Primary)

Build and test looplia in a Docker container. Best for CI and reproducible testing.

```bash
# Set API key
export ZENMUX_API_KEY=xxx

# Run Docker E2E test
./scripts/docker-e2e.sh
```

**What it tests:**
- Docker image builds successfully
- CLI initializes workspace
- Provider configuration works
- Workflow executes and produces outputs
- v0.6.9+ subagent architecture

See `scripts/docker-e2e.sh` for full implementation.

### Mode 2: Published CLI Testing

Test the published `@looplia/looplia-cli` package after CI passes.

```bash
# Set API key
export ZENMUX_API_KEY=xxx

# Test latest published version
./scripts/published-cli-e2e.sh

# Test specific version
./scripts/published-cli-e2e.sh 0.6.10
```

**What it tests:**
- Published package installs correctly
- Fresh workspace bootstrap works
- Workflow execution with real package

### Mode 3: Local Development

Quick testing during development.

```bash
# Build and run locally
bun run build
bun run dev build "test prompt"

# Or use installed CLI
looplia --version
looplia build --mock "test prompt"
```

### Mode 4: v0.6.10 Verification

Specific checks for v0.6.10 unified command initialization.

```bash
./scripts/check-v0610.sh
```

**What it tests:**
- Mock mode works without API key
- ZenMux API key mapping
- Error message format
- Settings loading order

## Common Verification Functions

Source `scripts/verify-workflow.sh` to access common verification functions:

```bash
source scripts/verify-workflow.sh

# Find sandbox directory
SANDBOX=$(find ~/.looplia/sandbox -maxdepth 1 -type d ! -name sandbox | head -1)

# Run verifications
verify_outputs "$SANDBOX"
verify_validation_state "$SANDBOX"
verify_subagent_usage "$SANDBOX"
verify_v0610_init
```

## Expected Outputs

A successful workflow run produces:

```
~/.looplia/sandbox/<run-id>/
├── outputs/
│   ├── summary.json      # Stage 1: Content analysis
│   ├── ideas.json        # Stage 2: Idea generation
│   └── writing-kit.json  # Stage 3: Final output
├── validation.json       # All steps validated: true
└── logs/
    └── *.log             # Execution logs
```

## v0.6.9+ Architecture Verification

The v0.6.9 architecture uses `general-purpose` subagent for all workflow steps.

**Expected in logs:**
- `"subagent_type": "general-purpose"` appears >= 3 times
- No legacy agents: `content-analyzer`, `idea-generator`, `writing-kit-builder`

**Check with:**
```bash
grep -c '"subagent_type".*"general-purpose"' ~/.looplia/sandbox/*/logs/*.log
# Expected: >= 3
```

## v0.6.10 Command Init Verification

The v0.6.10 architecture unifies command initialization.

**Key tests:**
1. `looplia build --mock "test"` - Works without API key
2. `looplia build` with ZENMUX_API_KEY - No longer fails with "API key required"
3. Error messages show all options

See `references/VERIFICATION.md` for detailed verification steps.

## Success Criteria

- [ ] CLI installed and version displayed
- [ ] Workspace bootstrapped with 2 plugins (looplia-core, looplia-writer)
- [ ] Provider configured (ZenMux or Anthropic)
- [ ] Workflow completed successfully
- [ ] All 3 output files created (summary.json, ideas.json, writing-kit.json)
- [ ] writing-kit.json passes schema validation
- [ ] All steps show `validated: true` in validation.json
- [ ] Logs show `general-purpose` subagent usage (v0.6.9+)
- [ ] No legacy agents detected in logs
- [ ] Hook count >= 2, outline sections >= 3

## Troubleshooting

See [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for common issues and solutions.

**Quick fixes:**
- API key issues: `export ZENMUX_API_KEY=xxx`
- Docker issues: `docker info` to verify Docker is running
- Workspace issues: `rm -rf ~/.looplia && looplia init --yes`

## File Structure

```
.claude/skills/looplia-e2e/
├── SKILL.md                    # This file
├── scripts/
│   ├── docker-e2e.sh           # Docker E2E test
│   ├── debug-docker-e2e.sh     # Debug Docker E2E with ZenMux
│   ├── published-cli-e2e.sh    # Published CLI test
│   ├── verify-workflow.sh      # Common verification functions
│   └── check-v0610.sh          # v0.6.10 specific checks
├── references/
│   ├── VERIFICATION.md         # Detailed verification guide
│   └── TROUBLESHOOTING.md      # Error handling guide
└── assets/
    └── ai-healthcare.md        # Test content fixture
```

## Environment Variables

| Variable | Priority | Description |
|----------|----------|-------------|
| `ZENMUX_API_KEY` | **Preferred** | ZenMux API key (cheapest - uses GLM 4.7) |
| `ANTHROPIC_API_KEY` | Fallback | Anthropic API key (more expensive) |

**Cost Optimization:** Always use `ZENMUX_API_KEY` for E2E testing. The ZenMux GLM 4.7 preset is significantly cheaper than Anthropic direct API.

*One of ZENMUX_API_KEY or ANTHROPIC_API_KEY is required (unless using --mock).

## See Also

- [references/VERIFICATION.md](references/VERIFICATION.md) - Success criteria and validation
- [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - Common issues and solutions
- `docs/DESIGN-0.6.9.md` - Subagent architecture design
- `docs/DESIGN-0.6.10.md` - Unified command initialization design

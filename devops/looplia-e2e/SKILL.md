---
name: looplia-e2e
description: |
  End-to-end testing for looplia CLI from local source. Builds the CLI,
  initializes workspace, runs the writing-kit workflow, and verifies outputs.
  Use when testing local development or validating workflow execution.
license: MIT
compatibility: Requires jq and bun. Works with Claude Code.
metadata:
  author: looplia
  version: "0.7.5"
---

# Looplia E2E Test Skill

End-to-end testing for looplia CLI from local source.

## Quick Start

```bash
# Set API key in .env
echo "ZENMUX_API_KEY=your-key" >> .env

# Run E2E test
.claude/skills/looplia-e2e/scripts/e2e.sh
```

## What It Tests

The script performs these steps:

1. **Build** - Compiles the CLI from source
2. **Reset** - Removes `~/.looplia` for fresh start
3. **Init** - Initializes workspace with plugins
4. **Configure** - Sets provider to ZenMux MiniMax M2.1
5. **Build Command** - Tests workflow generation (HN AI news aggregator)
6. **Run Command** - Executes writing-kit workflow with ai-healthcare.md
7. **Verify** - Checks outputs, validation state, and logs

## Expected Outputs

**Build command:**
```
~/.looplia/workflows/e2e-build-test.md    # Generated workflow file
~/.looplia/sandbox/build-<id>/
├── validation.json       # workflowValidated: true
└── logs/
    └── *.log             # Execution logs
```

**Run command:**
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

## Success Criteria

**Build command:**
- Workflow file created at `~/.looplia/workflows/e2e-build-test.md`
- validation.json shows `workflowValidated: true`

**Run command:**
- 3 output files created (summary.json, ideas.json, writing-kit.json)
- All 3 steps validated in validation.json
- Final output writing-kit.json exists

## Troubleshooting

**Transient API errors (retry usually works):**
The ZenMux provider may occasionally return transient errors like "duplicate tool_call id".
This is a provider-side issue, not a workflow bug. Simply run the test again:
```bash
# Just retry - second run usually succeeds
.claude/skills/looplia-e2e/scripts/e2e.sh
```

**API key issues:**
```bash
# Verify .env exists and contains ZENMUX_API_KEY
cat .env | grep ZENMUX_API_KEY
```

**Workspace issues:**
```bash
# Manual reset
rm -rf ~/.looplia && looplia init --yes
```

**Build issues:**
```bash
# Clean rebuild
rm -rf apps/cli/dist && bun run build
```

## File Structure

```
.claude/skills/looplia-e2e/
├── SKILL.md              # This file
├── scripts/
│   └── e2e.sh            # E2E test script
└── assets/
    └── ai-healthcare.md  # Test content fixture
```

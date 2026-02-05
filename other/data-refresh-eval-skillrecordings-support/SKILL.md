---
name: data-refresh-eval
description: Build and refresh eval datasets from Front, run routing evals, and analyze agent response quality.
allowed-tools: Bash(skill:*)
---

# Data Refresh & Eval Skill

Workflow for keeping the eval dataset fresh and running quality checks on agent responses.

## Quick Start

```bash
cd ~/Code/skillrecordings/support/packages/cli

# Refresh dataset from Front (last 30 days, 200 responses max)
bun src/index.ts dataset build --since $(date -d "30 days ago" +%Y-%m-%d) --limit 200 --output data/eval-dataset.json

# Run routing eval
bun src/index.ts eval routing data/eval-dataset.json
```

## Dataset Commands

### Build fresh dataset
```bash
# Recent data (recommended for ongoing work)
bun src/index.ts dataset build --since 2025-01-01 --limit 200 --output data/eval-dataset.json

# App-specific
bun src/index.ts dataset build --app total-typescript --limit 100 --output data/tt-dataset.json

# Include conversation history for context
bun src/index.ts dataset build --since 2025-01-01 --include-history --output data/dataset-with-history.json

# Only labeled responses (good/bad)
bun src/index.ts dataset build --labeled-only --output data/labeled-only.json
```

### Convert to evalite format
```bash
bun src/index.ts dataset to-evalite -i data/eval-dataset.json -o data/evalite-format.json
```

## Running Evals

### Routing eval (default thresholds)
```bash
bun src/index.ts eval routing data/eval-dataset.json
```

### Custom thresholds
```bash
bun src/index.ts eval routing data/eval-dataset.json \
  --min-precision 0.95 \
  --min-recall 0.98 \
  --max-fp-rate 0.02 \
  --max-fn-rate 0.01
```

### JSON output for CI/automation
```bash
bun src/index.ts eval routing data/eval-dataset.json --json
```

## Response Analysis

### Find bad responses for debugging
```bash
# List responses rated "bad"
bun src/index.ts responses list --rating bad

# Get details with conversation context
bun src/index.ts responses get <actionId> --context

# Export bad responses for analysis
bun src/index.ts responses export --rating bad -o bad-responses.json
```

### Analyze unrated responses
```bash
bun src/index.ts responses list --rating unrated --limit 50
```

## Recommended Workflow

### Daily data refresh
```bash
cd ~/Code/skillrecordings/support/packages/cli

# 1. Pull fresh data
bun src/index.ts dataset build --since $(date -d "7 days ago" +%Y-%m-%d) --limit 100 --output data/eval-dataset.json

# 2. Check dataset stats
cat data/eval-dataset.json | jq 'length'

# 3. Run eval
bun src/index.ts eval routing data/eval-dataset.json

# 4. Check for failures
bun src/index.ts responses list --rating bad --limit 10
```

### Pre-deploy validation
```bash
# 1. Build comprehensive dataset
bun src/index.ts dataset build --since 2025-01-01 --limit 500 --output data/full-dataset.json

# 2. Run eval with strict thresholds
bun src/index.ts eval routing data/full-dataset.json --min-precision 0.95 --min-recall 0.98 --json

# 3. Check exit code
echo "Exit code: $?"
```

## Dataset Schema

Each eval point includes:
- `id` - Action ID
- `app` - App slug (total-typescript, aihero, etc.)
- `conversationId` - Front conversation ID
- `customerEmail` - Customer email (if available)
- `triggerMessage` - The inbound message that triggered the response
  - `subject`, `body`, `timestamp`
- `agentResponse` - The agent's drafted response
  - `text`, `category`, `timestamp`
- `label` - "good" | "bad" | undefined
- `labeledBy` - Who approved/rejected
- `conversationHistory` - (optional) Full message history

## Environment

Required in `.env.local`:
```bash
FRONT_API_TOKEN=          # Front API access
DATABASE_URL=             # Database connection
```

## Troubleshooting

### "FRONT_API_TOKEN environment variable required"
```bash
source apps/front/.env.local
# or set in .env.local at repo root
```

### Dataset building slowly
Front API rate limits. Use `--limit` to control batch size.

### No labeled data
Labels come from HITL approvals/rejections. New responses start unlabeled.

---
name: fresh-install-testing
description: 'Test Orient from a clean clone to validate the full development setup and test suite'
---

# Fresh Install Testing

Test Orient from a clean clone to validate the full development setup and test suite.

## Triggers

- "fresh install test"
- "test from clean clone"
- "validate clean setup"
- "run full test suite on fresh clone"

## Clone Location

```bash
cd /Users/tombensim/code/tombensim
git clone https://github.com/orient-bot/orient.git orient-fresh-test
cd orient-fresh-test
```

**Note**: The remote URL is `https://github.com/orient-bot/orient.git` (not the personal fork).

## Phase 1: Environment Setup

### Run Doctor

```bash
./run.sh doctor --fix
```

This will:

- Validate Node.js >= 20.0.0, pnpm >= 9.0.0, Docker
- Create `.env` from `.env.example` if missing
- Create `.mcp.config.local.json` from template
- Run `pnpm install` automatically

### Copy Credentials from Main Repo

```bash
cp /Users/tombensim/code/tombensim/orient/.env /Users/tombensim/code/tombensim/orient-fresh-test/.env
```

This copies Slack credentials and other secrets needed for live testing.

### Build Packages

```bash
pnpm build:packages
```

Builds all 16 workspace packages. Required before running tests.

## Phase 2: Dev Mode Startup

### Start Without Bots (for basic testing)

```bash
./run.sh dev start --no-whatsapp --no-slack
```

### Start With Slack Only

```bash
./run.sh dev start --no-whatsapp
```

### Start With WhatsApp Only

```bash
./run.sh dev start --no-slack
```

### Stop Dev Mode

```bash
./run.sh dev stop
```

## Phase 3: Run Test Suite

### Test Categories (7 total)

| Category    | Command                                        | Expected Files |
| ----------- | ---------------------------------------------- | -------------- |
| Unit        | `pnpm test:unit`                               | ~24 files      |
| Integration | `INTEGRATION_TESTS=true pnpm test:integration` | ~1 file        |
| E2E         | `E2E_TESTS=true pnpm test:e2e`                 | ~5 files       |
| Contract    | `pnpm vitest run tests/contracts/`             | ~6 files       |
| Config      | `pnpm vitest run tests/config/`                | ~4 files       |
| Services    | `pnpm vitest run tests/services/`              | ~6 files       |
| Docker      | `pnpm test:docker:build` (optional, slow)      | ~3 files       |

### Interpreting Results

**Timeouts vs Failures**:

- Timeout errors (120s, 90s) are usually due to OpenCode server response times under load, not functional failures
- These are acceptable in fresh install testing
- True failures will show assertion errors with specific file/line references

**Expected Skips**:

- Some tests are skipped by default (e.g., Slack live tests without tokens)
- Dashboard export contract tests are skipped (no dashboard-specific tests)

## Phase 4: Slack Bot Live Testing

### Export Credentials for Test Runner

The test runner doesn't automatically read `.env`. Export credentials explicitly:

```bash
cd /Users/tombensim/code/tombensim/orient-fresh-test
export SLACK_BOT_TOKEN=$(grep SLACK_BOT_TOKEN .env | cut -d= -f2)
export SLACK_USER_TOKEN=$(grep SLACK_USER_TOKEN .env | cut -d= -f2)
E2E_TESTS=true RUN_SLACK_LIVE_TESTS=true \
  SLACK_BOT_TOKEN="$SLACK_BOT_TOKEN" \
  SLACK_USER_TOKEN="$SLACK_USER_TOKEN" \
  pnpm vitest run tests/e2e/slack-live.e2e.test.ts
```

**Note**: `source .env` often fails due to comments or special characters in .env files.

## Phase 5: WhatsApp Bot Testing

### Start Dev Mode with WhatsApp

```bash
./run.sh dev start --no-slack
```

### Scan QR Code

1. Open http://localhost:80/qr/
2. Open WhatsApp on phone > Settings > Linked Devices > Link a Device
3. Scan the QR code

### Verify Connection

```bash
curl -s http://localhost:4097/health | jq .
# Should show: {"status":"ok","connected":true,"state":"open"}
```

### Troubleshooting WhatsApp Session Conflicts

**Symptom**: Phone shows "logging in" but never completes, or immediately logs out.

**Cause**: Session conflict with another instance using the same WhatsApp account.

**Solution**:

1. Check logs for "loggedOut" reason:
   ```bash
   grep -E "(loggedOut|logged out)" logs/instance-0/whatsapp-dev.log
   ```
2. If logged out, a new QR code is automatically generated
3. Wait for "QR Code received" message in logs
4. Scan the fresh QR code

**Log Locations**:

- Main log: `logs/instance-0/whatsapp-dev.log`
- Connection debug: `logs/whatsapp-debug-*.log`

## Phase 6: Health Verification

### API Health

```bash
curl -s http://localhost:4098/health | jq .
# Should return: {"status":"ok","timestamp":"..."}
```

### Dashboard Accessibility

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:80/
# Should return: 200
```

### WhatsApp API

```bash
curl -s http://localhost:4097/health | jq .
# Should return: {"status":"ok","connected":true,"state":"open"}
```

## Cleanup

```bash
cd /Users/tombensim/code/tombensim/orient-fresh-test
./run.sh dev stop
cd ..
rm -rf orient-fresh-test
```

## Quick Reference: Full Test Run

```bash
# Clone and setup
cd /Users/tombensim/code/tombensim
rm -rf orient-fresh-test
git clone https://github.com/orient-bot/orient.git orient-fresh-test
cd orient-fresh-test
./run.sh doctor --fix
cp ../orient/.env .env
pnpm build:packages

# Start dev mode
./run.sh dev start --no-whatsapp --no-slack

# Run all tests
pnpm test:unit
INTEGRATION_TESTS=true pnpm test:integration
E2E_TESTS=true pnpm test:e2e
pnpm vitest run tests/contracts/
pnpm vitest run tests/config/
pnpm vitest run tests/services/

# Verify health
curl -s http://localhost:4098/health | jq .

# Cleanup
./run.sh dev stop
```

## Expected Results (v0.1.0 baseline)

| Category    | Tests Passed | Notes                         |
| ----------- | ------------ | ----------------------------- |
| Unit        | ~246         |                               |
| Integration | ~43          |                               |
| E2E         | ~34          | 4 timeout failures acceptable |
| Contract    | ~62          |                               |
| Config      | ~22          |                               |
| Services    | ~22          |                               |
| Slack Live  | ~9           | Requires credential export    |
| **Total**   | **~438**     |                               |

---
description: Generate and run end-to-end tests with Playwright. Creates test journeys, runs tests, captures screenshots/videos/traces, and uploads artifacts.
---

# Playwright

This command invokes the **e2e-runner** agent to generate, maintain, and execute end-to-end tests using Playwright.

## What This Command Does

1. **Generate Test Journeys** - Create Playwright tests for user flows
2. **Run E2E Tests** - Execute tests across browsers
3. **Capture Artifacts** - Screenshots, videos, traces on failures
4. **Identify Flaky Tests** - Quarantine unstable tests

## When to Use

Use `/playwright` when:
- Testing critical user journeys (login, chat, summary)
- Verifying multi-step flows work end-to-end
- Testing UI interactions with voice/text modes
- Validating integration between frontend and Mockoon mock backend
- Preparing for production deployment

## How It Works

The e2e-runner agent will:

1. **Analyze user flow** and identify test scenarios
2. **Generate Playwright test** following the existing test patterns
3. **Run tests** across multiple browsers (Chromium, Firefox, WebKit)
4. **Capture failures** with screenshots, videos, and traces
5. **Generate report** with results and artifacts

## Project Test Structure

```
frontend/
  tests/                    # E2E test files
    utils.ts                # Shared helpers (login, sendMessage, mockMediaDevices, etc.)
    login.spec.ts           # Login flow tests
    signup.spec.ts          # Signup flow tests
    chat.spec.ts            # Chat functionality (text/voice modes)
    chat_history.spec.ts    # Chat history display
    connection.spec.ts      # WebSocket connection tests
    summary.spec.ts         # Summary generation/display
    setting.spec.ts         # User settings
    assistant_selection.spec.ts  # Agent selection
    reset_conversation.spec.ts   # Conversation reset
    message_duplication.spec.ts  # Message dedup verification
  playwright.config.ts      # Playwright configuration
  mock/mockoon/             # Mockoon mock API definitions
```

## Test Conventions

### Shared Utilities (`tests/utils.ts`)

All tests should use the shared helpers:

```typescript
import { login, logoutIfNeeded, mockMediaDevices, sendMessage, waitForTextModeConnection } from './utils'

test.beforeEach(async ({ page }) => {
  await mockMediaDevices(page)   // Mock audio devices for voice tests
  await logoutIfNeeded(page)     // Ensure clean state
  await login(page)              // Login with test credentials
})
```

### Test Pattern

```typescript
import { expect, test } from '@playwright/test'
import { login, logoutIfNeeded, mockMediaDevices } from './utils'

test.describe('Feature name', () => {
  test.beforeEach(async ({ page }) => {
    await mockMediaDevices(page)
    await logoutIfNeeded(page)
    await login(page)
  })

  test('User can do X', async ({ page }) => {
    // Arrange: navigate and set up
    // Act: perform user action
    // Assert: verify expected outcome
  })
})
```

### Key Points

- Test descriptions should follow the project's existing conventions
- Use `mockMediaDevices()` for tests involving voice/audio
- Use `logoutIfNeeded()` before login to ensure clean state
- Use `waitForTextModeConnection()` or `waitForConnection()` to wait for WebSocket
- Use `sendMessage()` helper for sending chat messages with retry logic
- Environment variables: `E2E_TEST_EMAIL`, `E2E_TEST_PASSWORD` for test credentials

## Browser Configuration

```
Local:  Chromium + Firefox + WebKit (3 browsers)
CI:     Chromium only (WebKit lacks WebRTC fake device support)
```

Chromium uses `--use-fake-ui-for-media-stream` and `--use-fake-device-for-media-stream` flags for microphone permission.

## Running Tests

```bash
# Run with Mockoon mock backend (via dev script)
dev/test-frontend

# Run specific test file
cd frontend && npx playwright test tests/login.spec.ts

# Run in headed mode (see browser)
cd frontend && npx playwright test --headed

# Debug test
cd frontend && npx playwright test --debug

# View report
cd frontend && npx playwright show-report
```

## Critical User Flows

**Must Always Pass:**
1. Login with valid credentials
2. Signup flow
3. Text mode chat (connect → send message → receive response)
4. Voice mode connection
5. Chat history display
6. Summary generation and display
7. User settings update

**Important:**
1. Agent/assistant selection
2. Conversation reset
3. Message deduplication
4. Session management

## Artifacts

**On All Tests:**
- HTML Report (`playwright-report/`)

**On Failure Only:**
- Screenshot of the failing state
- Video recording of the test
- Trace file for debugging (step-by-step replay)

## Integration with Other Commands

- Use `/plan` to identify critical journeys to test
- Use `/tdd` for unit tests (faster, more granular)
- Use `/e2e-fix` to diagnose and fix failing E2E tests
- Use `/code-review` to verify test quality

## Related Agents

This command invokes the `e2e-runner` agent located at:
`.claude/agents/e2e-runner.md`

## Language

- **All user-facing output, reports, and summaries must be written in Japanese(すべてのユーザーへの出力は日本語にしてください)**

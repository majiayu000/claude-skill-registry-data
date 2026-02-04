---
name: Testing web apps with Playwright
description: Test EventOS web application end-to-end using Playwright browser automation via MCP. Use PROACTIVELY for smoke tests after deployments, validating user flows (booking, event creation, dashboard), debugging production issues, and verifying RLS policies. Supports accessibility-based interactions, network monitoring, and multi-browser testing.
---

# Playwright E2E Testing Skill

## What This Skill Does

Automates browser testing for EventOS using Playwright MCP (Model Context Protocol). Tests critical user journeys, validates Supabase RLS policies, captures screenshots of errors, and monitors network requests—all without pixel-based selectors.

**Key Capabilities**:
- ✅ Navigate and interact with pages using accessibility tree
- ✅ Fill forms, click buttons, validate flows
- ✅ Monitor network requests (Supabase queries, API calls)
- ✅ Capture console errors and screenshots
- ✅ Test responsive layouts and multi-browser compatibility

## When to Use This Skill

**Use PROACTIVELY when**:
1. 🚀 **After Vercel deployments** → Run smoke tests to verify critical paths
2. 🔒 **Testing auth flows** → Validate RLS policies allow/block correctly
3. 🐛 **Debugging production issues** → Capture network logs, console errors, screenshots
4. 📊 **Dashboard changes** → Verify data loads, stats display correctly
5. 🎫 **Booking flow updates** → Test end-to-end ticket purchase journey
6. 🧪 **Before merging PRs** → Validate new features don't break existing flows

**Don't use for**:
- ❌ Unit tests (use Vitest/Jest instead)
- ❌ Component testing in isolation (use React Testing Library)
- ❌ Static analysis (use ESLint/TypeScript)

## How to Invoke

```bash
# Invoke the skill via Skill tool
command: "playwright-e2e-skill"

# Or load specific playbook
command: "playwright-e2e-skill/playbooks/SMOKE.txt"
```

## Quick Start Examples

### Example 1: Smoke Test Dashboard
**Scenario**: Verify dashboard loads without authentication errors

```typescript
// 1. Navigate to dashboard
await browser_navigate({ url: "https://event-studio-rho.vercel.app/dashboard" })

// 2. Capture snapshot
await browser_snapshot()

// 3. Check network for RLS errors
const requests = await browser_network_requests()
// Look for 401/403 responses

// 4. Verify stats displayed
await wait_for({ text: "Total Events" })

// 5. Screenshot for docs
await browser_take_screenshot({ filename: "dashboard-loaded.png" })
```

**Expected Result**: Dashboard loads, stats show counts, no RLS errors

---

### Example 2: Event Creation Flow
**Scenario**: Create new event from wizard form

```typescript
// 1. Navigate to event creation
await browser_navigate({ url: "/events/new" })

// 2. Fill event details
await browser_fill_form({
  fields: [
    { name: "Event Name", ref: "input-name", value: "Tech Conference 2025" },
    { name: "Date", ref: "input-date", value: "2025-12-01" },
    { name: "Venue", ref: "select-venue", value: "Convention Center" }
  ]
})

// 3. Submit form
await browser_click({ element: "Create Event button", ref: "btn-submit" })

// 4. Wait for success
await wait_for({ text: "Event created successfully" })

// 5. Monitor console for errors
const logs = await browser_console_messages({ onlyErrors: true })
```

**Expected Result**: Event created, success message shown, no console errors

---

### Example 3: Booking Flow Validation
**Scenario**: Complete ticket booking as anonymous user

```typescript
// 1. Navigate to event page
await browser_navigate({ url: "/events/123/book" })

// 2. Monitor network (check RLS)
const startRequests = await browser_network_requests()

// 3. Fill booking form
await browser_fill_form({
  fields: [
    { name: "Tickets", ref: "input-quantity", value: "2" },
    { name: "Email", ref: "input-email", value: "test@example.com" }
  ]
})

// 4. Click checkout
await browser_click({ element: "Checkout button", ref: "btn-checkout" })

// 5. Wait for confirmation
await wait_for({ text: "Booking confirmed" })

// 6. Verify no auth errors
const allRequests = await browser_network_requests()
const authErrors = allRequests.filter(r => r.status === 401 || r.status === 403)
```

**Expected Result**: Booking completes, no 401/403 errors, confirmation shown

---

## Playbooks (Pre-Built Test Suites)

### Available Playbooks
1. **SMOKE.txt** → Critical path validation (dashboard, navigation, auth bypass)
2. **AUTH.txt** → Authentication flow testing (login, signup, protected routes)
3. **PITCH_DECK_WIZARD.txt** → Multi-step wizard form (drag-drop, file upload)

### Running Playbooks
```bash
# Run smoke tests
Skill("playwright-e2e-skill/playbooks/SMOKE.txt")

# Run auth tests
Skill("playwright-e2e-skill/playbooks/AUTH.txt")

# Run wizard tests
Skill("playwright-e2e-skill/playbooks/PITCH_DECK_WIZARD.txt")
```

## Key Playwright MCP Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `browser_navigate` | Load URL | Navigate to `/dashboard` |
| `browser_snapshot` | Get page structure | Capture accessibility tree |
| `browser_click` | Click element | Click "Create Event" |
| `browser_fill` | Fill single input | Enter event name |
| `browser_fill_form` | Fill multiple inputs | Complete entire form |
| `wait_for` | Wait for text | Wait for "Success" |
| `browser_network_requests` | Get API calls | Check Supabase queries |
| `browser_console_messages` | Get logs | Find React errors |
| `browser_take_screenshot` | Capture visual | Screenshot error state |

**Full feature list**: See `resources/FEATURES.md`

## Workflow Pattern

```
┌─────────────────────────────────────────┐
│ 1. NAVIGATE to page                     │
│    browser_navigate({ url })            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 2. SNAPSHOT to understand structure     │
│    browser_snapshot()                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 3. INTERACT with elements               │
│    browser_fill_form(), browser_click() │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 4. VALIDATE result                      │
│    wait_for(), browser_snapshot()       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 5. CAPTURE evidence                     │
│    browser_take_screenshot()            │
│    browser_network_requests()           │
│    browser_console_messages()           │
└─────────────────────────────────────────┘
```

## EventOS-Specific Patterns

### Pattern 1: RLS Policy Validation
**Problem**: Dashboard shows blank because RLS blocks anon users
**Solution**: Monitor network requests for 401/403 errors

```typescript
await browser_navigate({ url: "/dashboard" })
const requests = await browser_network_requests()
const blockedRequests = requests.filter(r =>
  r.status === 401 || r.status === 403
)
// If blockedRequests.length > 0, RLS policies need updating
```

### Pattern 2: Auth Bypass Verification
**Problem**: `VITE_DISABLE_AUTH=true` not working
**Solution**: Check if protected routes redirect to `/auth`

```typescript
await browser_navigate({ url: "/dashboard" })
await wait_for({ time: 2 }) // Allow redirect
const snapshot = await browser_snapshot()
// If snapshot shows /auth login form, auth bypass failed
```

### Pattern 3: Form Validation Errors
**Problem**: Forms submit but errors not displayed
**Solution**: Capture console errors and screenshot

```typescript
await browser_fill_form({ fields: [...] })
await browser_click({ element: "Submit", ref: "btn-submit" })
const errors = await browser_console_messages({ onlyErrors: true })
await browser_take_screenshot({ filename: "form-error.png" })
```

## Configuration

### Agent Config
See `resources/agent.config.json` for full agent setup.

Key settings:
- **Browser**: Chromium (default), Firefox, WebKit
- **Headless**: `true` for CI, `false` for debugging
- **Base URL**: `https://event-studio-rho.vercel.app`
- **Timeout**: 30s default

### Environment Variables
Required in `.env`:
```bash
PLAYWRIGHT_BROWSER=chromium
PLAYWRIGHT_HEADLESS=true
PLAYWRIGHT_BASE_URL=https://event-studio-rho.vercel.app
```

## Testing Strategy

### P0: Critical Smoke Tests (Run on every deploy)
1. ✅ Dashboard loads without auth
2. ✅ Event list displays
3. ✅ Navigation works (home → dashboard → events)

### P1: Feature Validation (Run before merge)
1. ✅ Event creation wizard
2. ✅ Booking flow
3. ✅ Form validation

### P2: Edge Cases (Run weekly)
1. ✅ Multi-browser testing
2. ✅ Responsive layouts
3. ✅ File uploads

## Debugging Tips

### Issue: Element not found
**Solution**: Take snapshot first to see available elements
```typescript
await browser_snapshot() // Shows all interactive elements with refs
```

### Issue: Network requests empty
**Solution**: Navigate THEN check requests (cleared on navigation)
```typescript
await browser_navigate({ url: "/dashboard" })
const requests = await browser_network_requests() // Requests since navigation
```

### Issue: Timeout waiting for text
**Solution**: Check console for errors that prevented render
```typescript
await browser_console_messages() // May show React error that blocked render
```

### Issue: Screenshots all black
**Solution**: Use headed mode locally for debugging
```bash
PLAYWRIGHT_HEADLESS=false npm test
```

## Resources

- **Feature Comparison**: `resources/FEATURES.md`
- **Agent Config**: `resources/agent.config.json`
- **Example Inputs**: `resources/examples/inputs.json`
- **Runbook**: `scripts/RUNBOOK.md`
- **Official Docs**: [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)

## Common Commands

```bash
# Run all smoke tests
npm run test:smoke

# Run auth tests
npm run test:auth

# Run wizard tests
npm run test:wizard

# Run headless (CI mode)
PLAYWRIGHT_HEADLESS=true npm test

# Run headed (debug mode)
PLAYWRIGHT_HEADLESS=false npm test

# Run specific browser
PLAYWRIGHT_BROWSER=firefox npm test
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: Run Playwright Smoke Tests
  run: npm run test:smoke
  env:
    PLAYWRIGHT_HEADLESS: true
    PLAYWRIGHT_BASE_URL: ${{ secrets.VERCEL_URL }}
```

### Vercel Deploy Hook
```bash
# After successful Vercel deploy
vercel deploy --prod
npm run test:smoke -- --base-url=$VERCEL_URL
```

## Best Practices

1. ✅ **Always take snapshot before interacting** → Understand page structure
2. ✅ **Monitor network on auth-sensitive pages** → Catch RLS issues early
3. ✅ **Capture screenshots on failures** → Visual debugging evidence
4. ✅ **Use accessibility refs from snapshot** → More reliable than CSS selectors
5. ✅ **Test critical paths first** → Dashboard, booking, event creation
6. ✅ **Run headless in CI, headed locally** → Fast automation, easy debugging
7. ✅ **Keep playbooks focused** → One user journey per playbook

## Troubleshooting

**Browser not installed?**
```bash
npx @playwright/mcp install
```

**MCP server not responding?**
```bash
# Check .mcp.json has playwright configured
cat .mcp.json | grep playwright
```

**Tests passing locally but failing in CI?**
- Verify `PLAYWRIGHT_BASE_URL` environment variable
- Check Vercel deployment completed before tests run
- Ensure headless mode enabled in CI

## Next Steps

1. ✅ Run smoke tests after next Vercel deploy
2. ✅ Add auth flow tests when implementing login
3. ✅ Expand wizard tests for multi-step forms
4. ✅ Set up GitHub Actions for automated testing

---

**Questions?** See `scripts/RUNBOOK.md` for detailed local setup and CI integration instructions.

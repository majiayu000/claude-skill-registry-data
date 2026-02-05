---
name: Chrome DevTools Automation
description: Control Chrome browser through MCP for testing, debugging, network analysis, and performance profiling. Use when testing web apps, measuring Core Web Vitals, analyzing network requests, debugging console errors, or when the user mentions Chrome DevTools, performance traces, or browser automation.
version: 1.0.0
---

# Chrome DevTools Automation

## Quick Start

Control a live Chrome browser using Chrome DevTools MCP:

1. **Navigate** to pages
2. **Take snapshot** to see page structure (with UIDs)
3. **Click/fill** elements using UIDs from snapshot
4. **Capture screenshots** for evidence
5. **Check console/network** for errors
6. **Record performance** traces for optimization

## Basic Pattern

```typescript
// 1. Navigate
await chrome.navigate_page({ url: "http://localhost:8080/dashboard" });

// 2. Get page structure (returns element tree with UIDs)
const snapshot = await chrome.take_snapshot();

// 3. Interact with elements (use UIDs from snapshot)
await chrome.fill({ uid: "input-123", value: "Test Event" });
await chrome.click({ uid: "button-456" });

// 4. Capture evidence
await chrome.take_screenshot({ filename: "dashboard.png" });

// 5. Check for errors
const errors = await chrome.list_console_messages();
if (errors.length > 0) {
  console.error("Console errors found:", errors);
}

// 6. Monitor network
const requests = await chrome.list_network_requests({
  resourceTypes: ["fetch", "xhr"]
});
console.log(`API calls: ${requests.length}`);
```

## Available Playbooks

Choose the right playbook for your task:

**Smoke test** (1 min) - Quick health check
- See [playbooks/smoke.txt](playbooks/smoke.txt)
- Verifies page loads, no console errors, basic navigation

**Auth flow** (3 min) - Authentication testing
- See [playbooks/auth.txt](playbooks/auth.txt)
- Tests login, session persistence, protected routes

**Performance trace** (5 min) - Core Web Vitals analysis
- See [playbooks/performance.txt](playbooks/performance.txt)
- Records performance trace, analyzes LCP/FID/CLS, provides AI insights

## Core Tools

### Essential (use in 90% of tasks)

| Tool | Purpose | Example |
|------|---------|---------|
| `navigate_page` | Go to URL | `navigate_page({ url: "/dashboard" })` |
| `take_snapshot` | Get element tree with UIDs | `take_snapshot()` |
| `click` | Click element | `click({ uid: "btn-123" })` |
| `fill` | Enter text/select | `fill({ uid: "input-456", value: "text" })` |
| `take_screenshot` | Capture page/element | `take_screenshot({ filename: "step1.png" })` |
| `list_console_messages` | Check errors | `list_console_messages()` |
| `list_network_requests` | Monitor API calls | `list_network_requests()` |

### Advanced (use when needed)

**Deep Debugging:**
- `get_network_request` - Get specific API request/response
- `evaluate_script` - Run JavaScript in page
- `list_processes` / `kill_process` - Process management

**Performance:**
- `performance_start_trace` - Begin profiling
- `performance_stop_trace` - End profiling
- `performance_analyze_insight` - Get AI insights

**Testing Conditions:**
- `emulate_network` - Throttle network (Slow 3G, Fast 4G, etc.)
- `emulate_cpu` - Throttle CPU (1-20x slowdown)

**Multi-page:**
- `list_pages` / `new_page` / `close_page` / `select_page` - Tab management

**Advanced Forms:**
- `fill_form` - Fill multiple fields
- `hover` / `drag` / `upload_file` - Complex interactions
- `handle_dialog` - Alert/confirm handling

## Best Practices

### 1. Always Snapshot First

```typescript
// ✅ GOOD: Get structure, find UIDs, then interact
const snapshot = await chrome.take_snapshot();
// Find "button-123" in snapshot
await chrome.click({ uid: "button-123" });

// ❌ BAD: Guessing UIDs
await chrome.click({ uid: "unknown" });
```

### 2. Check Console After Actions

```typescript
await chrome.click({ uid: "submit" });

const errors = await chrome.list_console_messages();
if (errors.length > 0) {
  throw new Error(`Console errors: ${errors.length}`);
}
```

### 3. Monitor Critical API Calls

```typescript
// Send action
await chrome.click({ uid: "generate-deck" });

// Wait, then check network
const requests = await chrome.list_network_requests({
  resourceTypes: ["fetch"]
});

const apiCall = await chrome.get_network_request({
  url: "/functions/v1/generate-pitch-deck"
});

console.log("API Status:", apiCall.status);
console.log("Response:", apiCall.response);
```

### 4. Use Performance Traces for Key Flows

```typescript
// Only trace critical paths (expensive operation)
await chrome.performance_start_trace({ reload: true, autoStop: true });

// ... user journey ...

await chrome.performance_stop_trace();

// Get AI insights
const lcp = await chrome.performance_analyze_insight({
  insightName: "LCPBreakdown"
});
console.log("LCP Issues:", lcp);
```

### 5. Reset Emulation After Tests

```typescript
// Test on slow network
await chrome.emulate_network({ throttlingOption: "Slow 3G" });

// ... test ...

// Always reset
await chrome.emulate_network({ throttlingOption: "No emulation" });
await chrome.emulate_cpu({ throttlingRate: 1 });
```

## Common Workflows

### Testing a Form Submission

```typescript
await chrome.navigate_page({ url: "http://localhost:8080/events/new" });

// Get form structure
const snapshot = await chrome.take_snapshot();

// Fill fields (use UIDs from snapshot)
await chrome.fill({ uid: "input-title", value: "Tech Summit 2025" });
await chrome.fill({ uid: "input-date", value: "2025-06-15" });

// Submit
await chrome.click({ uid: "button-submit" });

// Wait and verify
await chrome.wait_for({ text: "Event created" });

// Check network
const requests = await chrome.list_network_requests();
const createRequest = requests.find(r => r.url.includes("/api/events"));
console.log("Create event status:", createRequest.status);
```

### Analyzing Performance

```typescript
// Start trace
await chrome.performance_start_trace({ reload: true, autoStop: true });

// Navigate to page being profiled
await chrome.navigate_page({ url: "http://localhost:8080/dashboard" });

// Stop trace (automatic with autoStop: true)
await chrome.performance_stop_trace();

// Get insights
const insights = [
  await chrome.performance_analyze_insight({ insightName: "LCPBreakdown" }),
  await chrome.performance_analyze_insight({ insightName: "CLSCulprits" }),
  await chrome.performance_analyze_insight({ insightName: "RenderBlocking" })
];

console.log("Performance Insights:", insights);
```

### Testing on Slow Network

```typescript
// Emulate Slow 3G
await chrome.emulate_network({ throttlingOption: "Slow 3G" });

// Navigate and measure
await chrome.navigate_page({ url: "http://localhost:8080/presentations" });

// Check load time
const requests = await chrome.list_network_requests();
const pageLoad = requests.find(r => r.type === "document");
console.log(`Load time on Slow 3G: ${pageLoad.duration}ms`);

// Reset
await chrome.emulate_network({ throttlingOption: "No emulation" });
```

## Troubleshooting

### Element not found
- Run `take_snapshot()` to see current page structure
- Check element UID is correct
- Verify element is visible (not hidden by CSS)

### Performance trace failed
- Ensure page loaded before stopping trace
- Check Chrome has enough memory
- Use `autoStop: true` for automatic completion

### Network request missing
- Verify request actually fired (check DevTools manually)
- Check timing - request might not have completed yet
- Filter by `resourceTypes` to narrow search

### Dialog blocking test
- Handle dialogs immediately with `handle_dialog`
- Use `handle_dialog({ accept: true })` or `{ accept: false }`

## Reference

**Complete tool list**: See [FEATURES.md](FEATURES.md)

**Performance insights**: LCPBreakdown, CLSCulprits, DocumentLatency, RenderBlocking, SlowCSSSelector

**Network throttling**: No emulation, Offline, Slow 3G, Fast 3G, Slow 4G, Fast 4G

**Official docs**: https://github.com/ChromeDevTools/chrome-devtools-mcp

---
name: dev-log-monitoring
description: This skill should be used when testing ScreenGraph end-to-end flows (drift detection, agent runs) while monitoring backend and frontend logs in real-time. Use when the user wants to observe system behavior across services, debug live runs, or verify event streaming.
---

# Dev Log Monitoring

## Overview

Monitor backend (Encore.ts) and frontend (SvelteKit) logs during ScreenGraph development and testing. This skill provides a systematic workflow for starting services, capturing logs, navigating the app with Playwright MCP, and analyzing the complete event flow after execution.

## Workflow Decision Tree

**Use this skill when:**
- Testing drift detection end-to-end flow
- Debugging agent runs and observing state transitions
- Verifying WebSocket event streaming (run events + graph events)
- Analyzing performance metrics across services
- Troubleshooting backend/frontend integration issues

**Do NOT use this skill when:**
- Writing unit tests (use backend-testing skill)
- Debugging specific backend services (use backend-debugging skill)
- Writing E2E tests (use webapp-testing skill)

## Step 1: Start Services with Log Capture

### 1.1 Start Backend with Logs

Start Encore backend and pipe logs to a temporary file for later analysis:

```bash
cd /path/to/ScreenGraph/backend && encore run 2>&1 | tee /tmp/backend-logs.txt &
```

Wait for backend health check:

```bash
sleep 8 && curl -s http://localhost:4000/health
```

Expected response:
```json
{"status":"healthy","database":"connected","timestamp":"..."}
```

### 1.2 Start Frontend with Logs

Start SvelteKit frontend and pipe logs to a temporary file:

```bash
cd /path/to/ScreenGraph/frontend && bun run dev 2>&1 | tee /tmp/frontend-logs.txt &
```

Wait for frontend to be ready:

```bash
sleep 5 && curl -s http://localhost:5173 | head -n 1
```

Expected response:
```html
<!doctype html>
```

### 1.3 Verify Services Are Running

Check both services are healthy:

```bash
# Backend
curl -s http://localhost:4000/health

# Frontend
curl -s http://localhost:5173 | head -n 1
```

## Step 2: Navigate and Execute Flow with Playwright MCP

### 2.1 Navigate to Application

Use Playwright MCP to open the app:

```
mcp_playwright_browser_navigate(url: "http://localhost:5173")
```

### 2.2 Trigger Drift Detection

Click the "Detect My First Drift" button:

```
mcp_playwright_browser_click(
  element: "Detect My First Drift button",
  ref: [element_ref_from_snapshot]
)
```

Handle any alerts if backend wasn't ready:

```
mcp_playwright_browser_handle_dialog(accept: true)
```

### 2.3 Navigate to Run Page

The frontend should automatically redirect to `/run/[runId]`. If not:

```
mcp_playwright_browser_navigate(url: "http://localhost:5173/run/[runId]")
```

### 2.4 Verify Page State

Get current page snapshot to verify run page loaded:

```
mcp_playwright_browser_snapshot()
```

Look for:
- Run Timeline heading with runId
- Discovered Screens section
- Graph Events section
- Run Events timeline

### 2.5 Check Browser Console and Network

Monitor frontend activity:

```
mcp_playwright_browser_console_messages()
mcp_playwright_browser_network_requests()
```

Look for:
- `[Graph Stream] WebSocket opened`
- `[Graph Stream] Received event from stream`
- Screenshot fetch: `GET /artifacts/content?refId=obj://...`
- WebSocket upgrade status: `101` (successful)

## Step 3: Monitor Real-Time Logs

### 3.1 Check Backend Logs for Agent Flow

Grep for agent state machine activity:

```bash
tail -100 /tmp/backend-logs.txt | grep -E "(agent|graph|screenshot|drift)" -i
```

Key patterns to look for (see `references/log_patterns.md` for complete list):

**Agent Nodes:**
- `INF Node started actor=orchestrator nodeName=EnsureDevice`
- `INF Node finished actor=orchestrator nodeName=EnsureDevice outcomeStatus=SUCCESS`
- `INF Node started actor=orchestrator nodeName=ProvisionApp`
- `INF Node started actor=orchestrator nodeName=LaunchOrAttach`
- `INF Node started actor=orchestrator nodeName=Perceive`
- `INF Node started actor=orchestrator nodeName=WaitIdle`
- `INF Node started actor=orchestrator nodeName=Stop`

**Event Recording:**
- `INF Event recorded: agent.run.started eventSeq=1`
- `INF Event recorded: agent.event.screenshot_captured`
- `INF Event recorded: agent.event.screen_perceived`
- `INF Event recorded: agent.run.finished`

**Graph Projection:**
- `INF Projection batch processed projectedScreens=1`
- `INF Backfill complete runEventsCount=23 graphOutcomesCount=1`

### 3.2 Check Frontend Logs

Grep for Vite and WebSocket activity:

```bash
tail -50 /tmp/frontend-logs.txt
```

Look for:
- `VITE v6.4.1 ready in [N] ms`
- `[vite] connected`
- No repeated connection errors

## Step 4: Analyze Complete Flow After Run Completes

### 4.1 Extract Agent Flow Timeline

Get full agent execution timeline with timestamps:

```bash
grep -E "5:07PM" /tmp/backend-logs.txt | grep -E "(Node started|Node finished|Event recorded)" | head -50
```

### 4.2 Verify Event Sequence

Check all events were recorded in order:

```bash
grep "Event recorded:" /tmp/backend-logs.txt | grep "5:07PM"
```

Expected sequence:
1. `agent.run.started` (seq=1)
2. `agent.node.started` for each node
3. Device/Appium health checks
4. `agent.event.screenshot_captured`
5. `agent.event.ui_hierarchy_captured`
6. `agent.event.screen_perceived`
7. `graph.screen.discovered` (graph event)
8. `agent.run.finished` (final)

### 4.3 Extract Run Metrics

Look for Stop node output with final metrics:

```bash
grep "Stop OUTPUT" /tmp/backend-logs.txt | grep "5:07PM"
```

Example output:
```
metrics={"runDurationInMilliseconds":5326,"totalIterationsExecuted":5,"uniqueActionsPersistedCount":0,"uniqueScreensDiscoveredCount":0}
```

### 4.4 Check Stream Backfill

Verify both streams delivered all events:

```bash
grep "Backfill complete" /tmp/backend-logs.txt | grep "5:07PM"
```

Expected:
- Run stream: `runEventsCount=23`
- Graph stream: `graphOutcomesCount=1`

### 4.5 Verify Screenshot Storage

Check artifacts were stored:

```bash
grep "screenshot" /tmp/backend-logs.txt | grep "5:07PM"
```

Look for artifact reference like:
```
obj://artifacts/[runId]/screenshot/[hash].png
```

## Step 5: Generate Summary Report

### 5.1 Print Complete Flow Summary

Create a comprehensive summary with:

1. **Run Metadata:** runId, app package, duration, status
2. **Agent State Machine Flow:** All node transitions with timestamps
3. **Graph Projection:** Screens discovered, hashes computed
4. **Streaming Architecture:** Event counts, WebSocket status
5. **Frontend Activity:** Console logs, network requests
6. **Metrics:** Budget usage, counters, errors

Example summary structure:

```
═══════════════════════════════════════════════════════════════════
🎯 DRIFT DETECTION FLOW - COMPLETE LOG SUMMARY
═══════════════════════════════════════════════════════════════════

Run ID: [runId]
App: [package]
Duration: [duration]
Status: ✅ COMPLETED

─────────────────────────────────────────────────────────────────
📊 AGENT STATE MACHINE FLOW
─────────────────────────────────────────────────────────────────

Step 1: EnsureDevice ([start] → [end])
  ✅ Device check: [deviceId] online
  ✅ Appium health check: port 4723 healthy

Step 2: ProvisionApp ([start] → [end])
  ✅ App install check: [package] already installed

[... continue for all nodes ...]

─────────────────────────────────────────────────────────────────
🎨 GRAPH PROJECTION
─────────────────────────────────────────────────────────────────

✅ [N] screen(s) discovered
✅ Hashes: [hash1], [hash2], ...
✅ Screenshots stored

─────────────────────────────────────────────────────────────────
📡 STREAMING ARCHITECTURE
─────────────────────────────────────────────────────────────────

Run Events: [N] events backfilled
Graph Events: [N] events backfilled
WebSocket: ✅ Connected

─────────────────────────────────────────────────────────────────
🌐 FRONTEND ACTIVITY
─────────────────────────────────────────────────────────────────

Console Logs:
  - [LOG] [Graph Stream] WebSocket opened
  - [LOG] [Graph Stream] Received event: graph.screen.discovered

Network:
  - Screenshot fetch: ✅ 200 OK
  - WebSocket upgrade: ✅ 101

─────────────────────────────────────────────────────────────────
📈 METRICS
─────────────────────────────────────────────────────────────────

Steps: [N]
Screens: [N]
Errors: [N]
Duration: [N]ms
```

## Step 6: Cleanup

### 6.1 Stop Services (Optional)

If needed to stop services:

```bash
# Kill backend
pkill -f "encore run"

# Kill frontend
pkill -f "vite"
```

### 6.2 Preserve Logs (Optional)

If logs need to be saved for later analysis:

```bash
# Copy logs to permanent location
cp /tmp/backend-logs.txt ./logs/backend-run-$(date +%Y%m%d-%H%M%S).txt
cp /tmp/frontend-logs.txt ./logs/frontend-run-$(date +%Y%m%d-%H%M%S).txt
```

## Troubleshooting

### Backend Not Responding

**Symptom:** `Failed to load resource: net::ERR_CONNECTION_REFUSED @ http://localhost:4000/`

**Fix:**
```bash
# Check if encore is running
ps aux | grep "encore run"

# Restart if needed
cd backend && encore run 2>&1 | tee /tmp/backend-logs.txt &
sleep 8 && curl -s http://localhost:4000/health
```

### Frontend Dev Server Crashed

**Symptom:** `WebSocket connection to 'ws://localhost:5173/' failed`

**Fix:**
```bash
# Kill existing processes
pkill -f "vite"

# Restart frontend
cd frontend && bun run dev 2>&1 | tee /tmp/frontend-logs.txt &
sleep 5
```

### No Events in Stream

**Symptom:** Run page shows "0 events"

**Check:**
```bash
# Look for event recording in backend logs
grep "Event recorded:" /tmp/backend-logs.txt

# Check if run actually started
grep "agent.run.started" /tmp/backend-logs.txt
```

### Graph Not Projecting Screens

**Symptom:** `projectedScreens=0` in all projection logs

**Check:**
```bash
# Verify graph service is loaded
curl -s http://localhost:4000/graph/diagnostics

# Check if screen perceived event was emitted
grep "agent.event.screen_perceived" /tmp/backend-logs.txt
```

## Resources

### references/log_patterns.md

Complete reference of all log patterns, event types, and metrics to watch for across backend and frontend services. Load this when analyzing specific log patterns or troubleshooting issues.

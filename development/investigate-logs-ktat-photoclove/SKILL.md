---
name: investigate-logs
description: Automatically investigate logs when errors occur, debugging issues, or troubleshooting problems. Check frontend logs (LogViewer) and backend logs (daily log files) for error patterns. Use when user reports bugs, errors appear, or functionality isn't working as expected.
---

# Investigate Logs

Automatically investigate PhotoClove logs to diagnose issues and errors.

## When This Skill is Invoked

Claude automatically uses this skill when:
- User reports an error or bug
- Functionality isn't working as expected
- Need to trace what happened during an operation
- Debugging why something failed
- User says "check the logs" or similar

## Log Locations

### Frontend Logs
**Location**: LogViewer component (accessible via Ctrl+Shift+L)
- Stored in memory via `LoggerService.js`
- Structured format: `[LEVEL] Component:event_name - Message | data: {...}`
- Can be filtered by level, component, and searched

**Daily Log Files** (UTC dates):
```bash
~/.local/share/photoclove/logs/photoclove-frontend-YYYY-MM-DD.log
```
Example: `photoclove-frontend-2025-12-23.log` (December 23, 2025 UTC)

### Backend Logs
**Location**: Daily log files in the logs directory (UTC dates)
```bash
~/.local/share/photoclove/logs/photoclove-YYYY-MM-DD.log
```
Example: `photoclove-2025-12-23.log` (December 23, 2025 UTC)

**Format**: Rust `log::` macros with structured key=value pairs
```
[TIMESTAMP] [LEVEL] target: "component", "event; key1=value1; key2=value2"
```

**Important**: Log file names use **UTC dates**, not local timezone dates.

## Investigation Process

1. **Identify the issue**:
   - What operation failed?
   - What was the user doing?
   - When did it happen?

2. **Check most recent logs** (log files use UTC dates):
   ```bash
   # Frontend logs (today UTC)
   tail -100 ~/.local/share/photoclove/logs/photoclove-frontend-$(date -u +%Y-%m-%d).log

   # Backend logs (today UTC)
   tail -100 ~/.local/share/photoclove/logs/photoclove-$(date -u +%Y-%m-%d).log

   # Or simply check the latest files
   tail -100 ~/.local/share/photoclove/logs/photoclove-frontend-*.log | tail -100
   tail -100 ~/.local/share/photoclove/logs/photoclove-*.log | grep -v frontend | tail -100
   ```

3. **Search for errors**:
   ```bash
   # Find errors in frontend logs
   grep -i "error" ~/.local/share/photoclove/logs/photoclove-frontend-*.log | tail -20

   # Find errors in backend logs
   grep -i "error" ~/.local/share/photoclove/logs/photoclove-2*.log | tail -20
   ```

4. **Trace operation flow**:
   - Look for correlation_id in logs to trace a request through frontend and backend
   - Follow the sequence of events leading to the error
   - Check what data was passed at each step

5. **Identify root cause**:
   - What was the first error in the chain?
   - What state was the application in?
   - What data caused the issue?

## Common Error Patterns

### Frontend Errors
- **ReferenceError**: Undefined variable or function
- **TypeError**: Wrong type or null/undefined access
- **State errors**: Incorrect state updates or missing state

### Backend Errors
- **Database errors**: SQL errors, table not found, constraint violations
- **File system errors**: Permission denied, file not found
- **Tauri command errors**: Command not found, invalid parameters

### Integration Errors
- **500 Internal Server Error**: Backend error, check backend logs
- **No response**: Command timeout or backend crash
- **Data mismatch**: Frontend and backend data format mismatch

## Log Analysis Tips

1. **Start from the error and work backwards**
2. **Look for correlation_id to trace requests**
3. **Check timestamps to understand timing**
4. **Pay attention to data values in structured logs**
5. **Compare with successful operations**

## Reporting Findings

After investigation, provide:
- **Root cause**: What actually caused the error
- **Error location**: File and line number if available
- **Data context**: What data triggered the issue
- **Suggested fix**: How to resolve the problem
- **Related logs**: Key log entries showing the issue

## Integration with PhotoClove

- Frontend logs use `LoggerService.js` for structured logging
- Backend logs use Rust `log::` macros
- All operations should have correlation IDs for tracing
- LogViewer provides UI for browsing logs interactively

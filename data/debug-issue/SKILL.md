---
name: debug-issue
description: Systematically debug issues in PhotoClove by examining code, state, logs, and data flow. Automatically invoked when investigating bugs, errors not working as expected, or tracing problems through the codebase. Uses structured debugging approach to identify root causes.
---

# Debug Issue

Systematically debug problems in PhotoClove using a structured approach.

## When This Skill is Invoked

Claude automatically uses this skill when:
- User reports unexpected behavior or bugs
- Features aren't working correctly
- Need to understand why something failed
- Investigating error causes
- Tracing issues through frontend and backend

## Debugging Process

### 1. Reproduce the Issue

- **Understand the steps**: What exactly did the user do?
- **Expected behavior**: What should have happened?
- **Actual behavior**: What actually happened?
- **Frequency**: Does it happen every time? Intermittently?

### 2. Gather Context

**Check logs first** (use investigate-logs skill, log files use UTC dates):
```bash
# Frontend logs (today UTC)
tail -200 ~/.local/share/photoclove/logs/photoclove-frontend-$(date -u +%Y-%m-%d).log

# Backend logs (today UTC)
tail -200 ~/.local/share/photoclove/logs/photoclove-$(date -u +%Y-%m-%d).log

# Search for errors
grep -A 5 -B 5 "ERROR" ~/.local/share/photoclove/logs/*.log | tail -50
```

**Check state**:
- What was the UI state when error occurred?
- What data was in context/state?
- What mode was the app in? (view mode, filters, etc.)

### 3. Trace Data Flow

Follow the complete path from user action to error:

**Frontend → Backend → Database** (Tauri app):
1. User interaction (component event handler)
2. State update (Context, hooks)
3. Tauri command invocation (via `invoke()`)
4. Backend command handler (Rust)
5. Repository/database operation
6. Response back to frontend
7. UI update

**Key questions at each step**:
- What data is passed?
- Is it transformed correctly?
- Are there null/undefined values?
- Do types match expectations?

### 4. Identify the Break Point

Where does the data flow break?
- **Frontend**: Check LogViewer (Ctrl+Shift+L), developer console
- **Backend**: Check Rust logs in daily log files
- **Database**: Check SQL logs, table state

### 5. Examine the Code

**Read the relevant files**:
- Component handling the operation
- Context/hooks managing state
- Tauri command implementation
- Repository/database code

**Look for**:
- Incorrect logic
- Missing error handling
- Wrong assumptions about data
- Race conditions
- State synchronization issues

### 6. Test Hypothesis

**Common PhotoClove Issues**:

**ViewMode related**:
- Check if ViewMode state is correct: `viewModeObj.isXxxMode()`
- Verify display keys: `viewModeObj.getDataAttribute()`
- Ensure mode-specific data is available

**Photo operations**:
- Check if photo paths are correct
- Verify trash vs normal mode handling
- Ensure photo list updates after operations

**Album/Tag operations**:
- Verify collection IDs are defined
- Check if photos are properly associated
- Ensure UI updates after backend changes

**State management**:
- Check if useEffect dependencies are correct
- Verify state updates trigger re-renders
- Ensure context values are available

### 7. Propose Fix

Based on root cause analysis:
1. **Describe the bug**: What's actually wrong
2. **Explain the cause**: Why it happens
3. **Propose solution**: How to fix it
4. **Consider side effects**: What else might be affected
5. **Test approach**: How to verify the fix

## Debugging Tools

### Frontend (Tauri app)
- **LogViewer** (Ctrl+Shift+L): Interactive log browsing
- **Developer Console**: JavaScript console in Tauri webview
- **Console logging**: Temporary debugging (remove before commit)

### Backend (Rust)
- **Log files**: `~/.local/share/photoclove/logs/photoclove-YYYY-MM-DD.log`
- **Cargo check**: Compilation errors
- **Database inspection**: SQLite CLI for database debugging

### Code Navigation
- **docs/terms.md**: Component → file mappings
- **Glob/Grep**: Find code patterns
- **Read**: Examine specific files
- **LSP**: Go to definition, find references

## Common Bug Patterns

### Frontend
- **Undefined errors**: Missing null checks
- **State not updating**: Missing dependency in useEffect
- **Infinite loops**: Incorrect useEffect dependencies
- **Wrong data**: ViewMode/mode confusion

### Backend
- **SQL errors**: Wrong table/column names
- **Path errors**: Incorrect file paths
- **Type errors**: Data type mismatches
- **Missing data**: Null handling issues

### Integration
- **Tauri command errors**: Wrong parameter names/types
- **Response parsing**: JSON serialization issues
- **Race conditions**: Async operation ordering

## Best Practices

1. **Start with logs** - They show what actually happened
2. **Reproduce first** - Understand the exact steps
3. **Use correlation IDs** - Trace requests through the system
4. **Check assumptions** - Verify data at each step
5. **Think systematically** - Follow the data flow
6. **Test the fix** - Ensure it actually resolves the issue

## PhotoClove-Specific Debugging

### ViewMode Issues
- Check `src/domain/ViewMode.js` for mode logic
- Verify mode conditions in components
- Ensure display keys match ViewMode methods

### Photo Operations
- Check `src/hooks/usePhotoOperations.js`
- Verify photo list updates via `removePhotoFromList`
- Ensure trash mode handling in Photo entity

### Database Operations
- Check `src-tauri/src/repository/meta_db/sqlite.rs`
- Verify table names (plural: `photo_collections`, `photo_metadata`)
- Check IndexMap vs HashMap for order preservation

### State Management
- Check Context files in `src/context/`
- Verify hooks in `src/hooks/`
- Ensure state flows correctly through components

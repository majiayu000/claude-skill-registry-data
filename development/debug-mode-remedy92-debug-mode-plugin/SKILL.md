---
name: debug-mode
description: Autonomous debugging workflow mirroring Cursor IDE's debug mode. Triggers on "debug mode", "help me debug", error messages, stack traces, or debugging loops. Generates 5-7 hypotheses, narrows to top 2, adds strategic logs with [DEBUG:] prefix, collects logs via local server, analyzes, fixes, and cleans up.
---

# Debug Mode

Systematic debugging through hypothesis generation, strategic logging, and iterative analysis.

## Activation Triggers

- "debug mode" or "enter debugger mode"
- "help me debug" or "fix this bug"
- Error messages or stack traces shared
- User stuck in debugging loop
- Previous fix attempts failed

## Workflow

### Phase 1: Hypothesize

Generate 5-7 possible causes, then narrow to top 2:

```
## Hypotheses (ranked)
1. [Most likely] ...
2. [Likely] ...
3. [Possible] ...
```

Consider: type errors, null/undefined, async timing, state bugs, API mismatches, imports, dependencies.

### Phase 2: Add Logs

Insert strategic logs at:
- Function entry/exit
- Before/after data transforms
- API boundaries
- State mutations
- Conditional branches

**Format:** `[DEBUG:location] description: value`

```javascript
console.log('[DEBUG:functionName] variable:', JSON.stringify(val, null, 2));
```

```python
print(f'[DEBUG:function_name] variable: {val}')
```

### Phase 3: Collect Logs

**Terminal:** `npm run dev 2>&1 | tee debug.log`

**Log Server (recommended):**
```bash
node ~/.claude/plugins/debug-mode/skills/debug-mode/scripts/log-server.js
```
Then app sends to `http://localhost:3333/log`

**Read logs:**
```bash
node ~/.claude/plugins/debug-mode/skills/debug-mode/scripts/read-logs.js --json
```

### Phase 4: Analyze

```
## Log Analysis
- Expected: A → B → C
- Actual: A → B → ✗
- Divergence: After B, value was X not Y
- Root cause: [conclusion]
```

### Phase 5: Fix & Verify

1. Implement fix
2. Run with logs still in place
3. Verify fix works
4. If not fixed → return to Phase 1

### Phase 6: Cleanup

```bash
grep -rn "\[DEBUG:" --include="*.js" --include="*.ts" --include="*.py" .
```

Remove all `[DEBUG:` logs, run final verification.

## Quick Patterns

| Bug Type | Symptoms | Log Focus |
|----------|----------|-----------|
| Type error | TypeError, undefined | Variable types/values |
| Async race | Intermittent | Timestamps, order |
| State bug | Stale data | Before/after mutations |
| API issue | Bad response | Request/response bodies |
| Null ref | Cannot read property | Object structure |

## Scripts

- `scripts/log-server.js` - HTTP server at :3333 for collecting logs
- `scripts/read-logs.js` - CLI to fetch/filter collected logs

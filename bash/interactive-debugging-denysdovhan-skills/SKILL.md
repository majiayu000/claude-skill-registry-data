---
name: interactive-debugging
description: Use this skill when debugging runtime behavior requires live data from the running app, temporary instrumentation, or hypothesis verification through logs. Trigger for async timeouts, stale or incorrect state updates, race conditions, event ordering bugs, intermittent failures, browser/client behavior that static inspection cannot explain, or any issue where the agent should create a local debug HTTP server, insert temporary probes, ask the user to reproduce, inspect .debug/debug.log, then remove all debug instrumentation and assets.
---

# Interactive Debugging

Use this skill to run a debug loop: hypothesize, instrument, reproduce, inspect runtime logs, fix, verify, and clean up.

## Required Paths

- Debug server: `.debug/debug_server.*`
- Debug log: `.debug/debug.log`
- Default endpoint: `http://localhost:3333/debug`

The bundled servers in this skill's `scripts/` directory (next to this SKILL.md, not in the project being debugged) are intentionally thin. They accept `POST /debug`, append the raw request body to `.debug/debug.log` with a timestamp, and return `ok`.

## Steps

### Step 1: Understand the Bug

- Read the relevant code before changing anything.
- State 1-3 concrete hypotheses that runtime data can prove or disprove.
- Do not jump to a fix before collecting data unless the cause is already proven.

### Step 2: Create the Debug Server

- Create `.debug/` in the project under debug.
- Copy the matching bundled server from this skill's `scripts/` directory to `.debug/debug_server.js` or `.debug/debug_server.py` in the project.
- For another language, create the smallest equivalent server at `.debug/debug_server.<ext>`.
- Keep the server thin: no schemas, dashboards, persistence, extra routes, or broad utilities.

### Step 3: Start the Debug Server

Run it from the project root:

```bash
node .debug/debug_server.js 3333
python3 .debug/debug_server.py 3333
```

- The server is a long-running foreground process; start it in the background (or another terminal) so it does not block your shell.
- Use another port only if `3333` is occupied.
- Verify it with `curl http://localhost:3333/health`.
- Clear `.debug/debug.log` before reproduction if it already exists.

### Step 4: Instrument the Code

- Add the fewest probes needed to test the hypotheses.
- Wrap every probe or probe block in matching debug region markers:

```js
// #region DEBUG
fetch("http://localhost:3333/debug", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    event: "function-entry",
    traceId,
    value,
  }),
}).catch(() => {});
// #endregion DEBUG
```

Dependency-free examples for other languages:

```python
# #region DEBUG
import json
import urllib.request

try:
    urllib.request.urlopen(
        urllib.request.Request(
            "http://localhost:3333/debug",
            data=json.dumps({"event": "function-entry", "value": value}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        ),
        timeout=0.2,
    ).close()
except Exception:
    pass
# #endregion DEBUG
```

```ruby
# #region DEBUG
require "json"
require "net/http"
require "uri"

begin
  Net::HTTP.post(
    URI("http://localhost:3333/debug"),
    { event: "function-entry", value: value }.to_json,
    "Content-Type" => "application/json",
  )
rescue StandardError
end
# #endregion DEBUG
```

- Use the target language's matching comments:
  - JavaScript, TypeScript, Java, C#, Go, Rust, C, C++: `// #region DEBUG` and `// #endregion DEBUG`
  - Python, Ruby, Shell, YAML: `# #region DEBUG` and `# #endregion DEBUG`
  - HTML, Vue, Svelte: `<!-- #region DEBUG -->` and `<!-- #endregion DEBUG -->`
  - Lua: `-- #region DEBUG` and `-- #endregion DEBUG`

### Step 5: Choose Useful Probe Data

- Include event names such as `process-order:entry`, `state-before-set`, or `branch-empty-result`.
- Include IDs needed to correlate flow, such as `traceId`, request ID, entity ID, or attempt number.
- Include compact values that distinguish hypotheses.
- Do not log secrets, tokens, cookies, credentials, full environment dumps, or private user data.
- Redact or summarize large objects.

### Step 6: Ask for Reproduction

- Tell the user exactly what is ready and ask them to reproduce the issue.
- Stop and wait while they reproduce unless you can run the reproduction yourself.

### Step 7: Read the Logs

- Inspect `.debug/debug.log`.
- If it is large, use `tail`, `wc -l`, or targeted `rg` before reading the whole file.
- Compare the observed events, ordering, and values to the hypotheses.
- If the logs are inconclusive, add a smaller second round of probes and repeat reproduction.

### Step 8: Fix and Verify

- Make the smallest fix explained by the logs.
- Keep instrumentation until the fix is verified.
- Clear `.debug/debug.log`, ask the user to verify again when manual reproduction is required, then inspect the new log if needed.

### Step 9: Clean Up

- Remove every `#region DEBUG` / `#endregion DEBUG` block and its contents.
- Stop the debug server.
- Delete `.debug/debug_server.*` and `.debug/debug.log`; delete `.debug/` if empty.
- Verify cleanup with `rg '#region DEBUG|#endregion DEBUG|localhost:3333/debug|debug_server|\\.debug/debug.log'`, replacing `3333` with the port actually used.
- Run the relevant test or reproduction check after cleanup.

## Log Reading Checklist

- Missing events show code paths that did not run.
- Event ordering shows async races and stale updates.
- Value changes across awaited work show mutation timing.
- Duplicate events show retries, repeated subscriptions, or double handlers.
- Error payloads near a missing event often explain swallowed failures.

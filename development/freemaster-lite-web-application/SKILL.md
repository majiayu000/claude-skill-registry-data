---
name: freemaster-lite-web-application
description: >
  Builds browser-based or Node.js applications that talk to FreeMASTER Lite
  through freemaster-client.js and the PCM API. Use whenever the user wants to
  create an HTML or JavaScript client, load client libraries, create a PCM
  instance, check board connection, load ELF or TSA symbols, and read or write
  variables from a web page. Triggers on "freemaster-client.js", "PCM object",
  "browser FreeMASTER", "Node.js FreeMASTER", "web app PCM", "StartComm from
  browser", "IsBoardDetected", "ReadVariable from JavaScript".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: freemaster
  tags: '[freemaster, web, javascript, pcm, html, client]'
---

# FreeMASTER Web Application

Builds browser-based or Node.js applications that talk to a running FreeMASTER
Lite instance through the `freemaster-client.js` library and its `PCM` API.
The web app must be served from the FreeMASTER Lite `web_root` so the browser
can load the client libraries from the same origin.

## When to use

- Building an HTML, JavaScript, or Node.js client for FreeMASTER Lite.
- Using `freemaster-client.js`, `simple-jsonrpc-js.js`, or the `PCM` API.
- Reading or writing variables from a browser-side application.
- Hosting the app in FreeMASTER Lite `web_root`.

Do **not** use this skill for direct MCP JSON-RPC calls (`freemaster-lite-jsonrpc-api`),
`.fmcfg` file creation (`freemaster-lite-configuration-file`), or launching the
service (`freemaster-lite-start-server`).

## Quick start

```html
<script src="/simple-jsonrpc-js.js"></script>
<script src="/freemaster-client.js"></script>
<script>
  var pcm;
  window.onload = function() {
    pcm = new PCM('127.0.0.1:8090', function() {
      pcm.StartComm('RS232;port=COM3;speed=115200')
        .then(function() { return pcm.IsBoardDetected(); })
        .then(function() { return pcm.ReadVariable('g_speed'); })
        .then(function(r) { console.log('speed:', r.data); })
        .catch(function(e) { console.error(e); });
    });
  };
</script>
```

Both libraries are served automatically at `http://localhost:8090/` when
FreeMASTER Lite is running. Files in the configured `web_root` override the
built-in copies.

## Step-by-step Workflow

### 1. Include libraries

```html
<script type="text/javascript" src="/simple-jsonrpc-js.js"></script>
<script type="text/javascript" src="/freemaster-client.js"></script>
```

### 2. Instantiate PCM

```javascript
pcm = new PCM('127.0.0.1:8090', on_connect);
```

First argument: `host:port` (not a full URL). Second argument: callback
invoked when the WebSocket connection to FreeMASTER Lite is established.

### 3. Check board and load symbols

Inside `on_connect`, start communication and confirm the board is detected
before reading variables:

```javascript
function on_connect() {
  pcm.StartComm('RS232;port=COM3;speed=115200')
    .then(() => pcm.IsBoardDetected())
    .then(() => pcm.ReadELF())           // or pcm.ReadTSA()
    .then(() => pcm.ReadVariable('g_motorSpeed'))
    .then(r => console.log('speed:', r.data))
    .catch(e => console.error(e));
}
```

All PCM methods return a **Promise**. Actual data is in `response.data`.

## PCM API Summary

| Category | Key methods |
|----------|-------------|
| Communication | `StartComm`, `StopComm`, `IsCommPortOpen`, `EnumCommPorts` |
| Board | `IsBoardDetected`, `GetDetectedBoardInfo` |
| Symbols | `ReadELF`, `ReadTSA`, `EnumSymbols`, `GetSymbolInfo` |
| Variables | `DefineVariable`, `GetVariableInfo`, `EnumVariables`, `ReadVariable`, `WriteVariable`, `DeleteVariable` |
| Oscilloscope | `SetupOscilloscope`, `GetOscilloscopeData` |
| Recorder | `SetupRecorder`, `StartRecorder`, `StopRecorder`, `GetRecorderData` |

See `references/examples.md` for periodic polling, async/await, dynamic
variable definition, and Node.js npm usage patterns.

## Guardrails

**Scope**
- This skill covers browser-side and Node.js application code only.
- The web app must reside in or be served from the FreeMASTER Lite `web_root`;
  cross-origin setups require additional server configuration outside this skill.

**Destructive actions**
- `WriteVariable` modifies live target memory. Confirm the target variable and
  value with the user before writing, especially for safety-critical state.

**Secrets**
- No credentials involved. If SSL is enabled in `.fmcfg`, the browser
  connects over `wss://` automatically.

**Refuse-and-escalate**
- If `IsBoardDetected` fails after `StartComm`, stop and direct the user to
  check the `.fmcfg` connection settings and target hardware before continuing
  to variable access.

## Validation loop

1. Open the app in a browser; confirm no `404` errors for the client library
   scripts.
2. `on_connect` callback must fire — if it does not, the PCM WebSocket
   connection to FreeMASTER Lite failed.
3. `IsBoardDetected` must resolve (not reject) before variable access.
4. `ReadVariable` result `response.data` must be a number, not `undefined`.
5. After `WriteVariable`, read back the value to confirm the write succeeded.

## Out of scope

- Direct MCP JSON-RPC calls — use `freemaster-lite-jsonrpc-api`.
- Building the FreeMASTER Lite service or `.fmcfg` — use
  `freemaster-lite-start-server` and `freemaster-lite-configuration-file`.
- Generic web application help unrelated to FreeMASTER Lite.

## See Also

- `references/examples.md` — complete HTML page, polling, async/await, Node.js,
  and mock-API usage patterns
- `freemaster-lite-start-server` — launch FreeMASTER Lite before loading the app
- `freemaster-lite-configuration-file` — configure `web_root` and connections
- `freemaster-lite-jsonrpc-api` — low-level MCP JSON-RPC alternative
- `freemaster-lite-command-line-arguments` — `--mock_api` and `--web_root` flags

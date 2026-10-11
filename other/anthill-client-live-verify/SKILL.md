---
name: anthill-client-live-verify
description: "Use when changing or checking AntHill client UI in the running app (WebView2 remote debugging, CDP), when status says connected through an outage, or a same-route page keeps a stale query value (/source-control?asset=X then bare /source-control) or a client screen disagrees with itself."
---

# Verifying the AntHill client against the running app

`AntHill.Client` is WPF + `BlazorWebView`. bUnit cannot reproduce its router or its
input path, so UI truth claims must be checked against the running window.

## 1. Launch with a debugging port and attach

```
hub start application=src/AntHill.Client/bin/Debug/net10.0-windows10.0.19041.0/win-x64/AntHill.Client.exe
     env={"WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS": "--remote-debugging-port=9223"}
```

Then in `eval`, a one-shot CDP call per request (the socket does not survive between
`eval` calls):

```js
const cdp = async (method, params = {}) => {
  const list = await (await fetch("http://localhost:9223/json/list")).json();
  const t = list.find(x => x.type === "page");          // url is https://0.0.0.1/
  return await new Promise((res, rej) => {
    const ws = new WebSocket(t.webSocketDebuggerUrl);
    ws.onopen = () => ws.send(JSON.stringify({ id: 1, method, params }));
    ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id === 1) { ws.close(); res(d.result ?? d.error); } };
    setTimeout(() => rej(new Error("timeout")), 10000);
  });
};
const js = async e => (await cdp("Runtime.evaluate", { expression: e, returnByValue: true, awaitPromise: true })).result?.value;
```

- In-app navigation: `history.pushState({}, '', '/settings'); dispatchEvent(new PopStateEvent('popstate'))`
  (`location.href = …` reloads the host page instead).
- Screenshot a bar: `cdp("Page.captureScreenshot", { clip: { x, y, width, height, scale: 2 } })`,
  write the base64 to a png under `_diag/`, `read` it. `.gitignore` covers `t-*.log` and `_diag/`,
  not images, so delete any png written anywhere else.
- Client boot to first paint is ~10s on a real catalogue. Sample on a loop rather
  than sleeping once, or you will attribute the wrong state to the wrong moment.

## 2. Force a real outage rather than trusting a unit test

Settings live at
`%LOCALAPPDATA%\BigAntStudios\AntHill\settings.json` (NOT `%LOCALAPPDATA%\AntHill`,
which is the Velopack install and is wiped on update; see `ClientPaths`).

```json
{ "ServerUrl": "http://localhost:5252", "IsConfigured": true }
```

Back it up, repoint at a dead port, relaunch, observe, restore, verify by reading
the file back. This is the only way to see the offline branch of any status UI.

## 3. Mouse side buttons

They need real OS input, because CDP-synthesised events bypass the layer under test. For the
hook, the `mouse_event` codes and the contamination check, see `webview2-wpf-input-and-history`.

## 4. Two traps that make the client show stale truth

**Silent-null unreachability.** `CatalogueSync.RefreshIfChangedAsync` returns `null`
when the server cannot be reached, deliberately, because the local copy is still
usable. Any status UI reading *fetch outcomes* therefore sees no failure and reports
"connected" through an outage. Read `CatalogueSync.LastContact` (written by every
path that speaks to the server, including the manual sync button) instead.

**Retained query parameters.** Blazor writes a `[SupplyParameterFromQuery]` property
only when the key is present in the address. Same-route navigation reuses the page
instance, so the property keeps its previous value: `/source-control?asset=X` then a
bare `/source-control` left the "this asset" panel live on the old asset. Parse the
query out of `Nav.Uri` each render instead. bUnit re-supplies parameters and cannot
reproduce this; do not write a bUnit "regression test" for it, since it passes with the
fix stashed. Verify in the running client.

## 5. Test gate

For `MSB3026/3027/3021` with "locked by: AntHill.Web / Microsoft Visual Studio" (a file lock:
the suite never ran), see `anthill-shared-css-verify`.

---
name: webview2-wpf-input-and-history
description: "Use when mouse side buttons (XButton1/XButton2) do nothing in a WPF BlazorWebView/WebView2 app such as the AntHill client, or a Back control's label disagrees with where it lands; also when a JS mousedown listener for buttons 3/4 never fires."
---

# WebView2 (WPF) input and history

Two faults that look unrelated but share one cause: **the page and WPF each assume the other
handles navigation input, and neither does.**

## 1. Mouse side buttons: the press reaches neither obvious layer

Do not write a JS `mousedown` listener for `event.button === 3 / 4`. It is the browser answer and
it is wrong here: WebView2 **never dispatches X-button presses to the DOM**. A script listening
for them looks correct in review, ships, and does nothing.

Proven by probe, not memory:

```js
window.addEventListener("mousedown", e => probe.downs.push(e.button), true);
window.addEventListener("auxclick",  e => probe.aux.push(e.button), true);
```
A real XBUTTON1 press over the view records **nothing**.

WPF cannot see it either: the window is one web view filling it, so the press goes to the view's
child HWND and never reaches the WPF tree (no `PreviewMouseDown`, no `InputBindings`).

**What works:** a `WH_MOUSE` hook on the UI thread (`SetWindowsHookExW(7, filter, IntPtr.Zero,
GetCurrentThreadId())`; AntHill's is `src/AntHill.Client/SideButtons.cs`). Thread-scoped, so it
sees messages bound for this thread's windows, including the view's, without the system-wide
hook's cost of sitting in every app's input path.

Details that bite:
- Keep the delegate in a **field**. Windows holds no reference the GC can see; collect it while
  installed and the next press calls freed memory, crashing inside the driver callback.
- `MOUSEHOOKSTRUCTEX`: button is the **high word** of the trailing `mouseData` (`1` = back,
  `2` = forward), not the DOM's 3/4 numbering.
- Handle `WM_XBUTTONDOWN` (0x020B); **swallow** `UP` (0x020C) and `DBLCLK` (0x020D) too by
  returning `1`, or one press becomes a step back *and* a click on whatever was underneath.
- Install on `Loaded`, not in the constructor; dispose on `Closed`.
- Act via `Dispatcher.BeginInvoke` → `CoreWebView2.ExecuteScriptAsync("history.back()")`.
  Calling the view inside the hook re-enters it mid-message.

## 2. "Back" that lands somewhere else: never count your own navigations

A C# counter incremented on `NavigationManager.LocationChanged` cannot see steps the window takes
itself (side buttons, keyboard), so it counts **up** while the history goes **down**. From the
first such press the control's word is wrong, offering "Back" with nothing behind it.

**Blazor already keeps the truth.** Its own JS stamps a monotonic index into history state and uses
it to work out direction:

```js
globalThis.anthillHistory = { behind: () => (history.state && history.state._index) || 0 };
```

`behind() > 0` → a real step exists → `history.back()`. `0` → show the fixed destination and
navigate to it. Both branches true by construction; no stack, no name map, no `Replacing()`
bookkeeping, and `replace: true` navigations are handled free (they do not move `_index`).

Read it in `OnAfterRenderAsync` and `StateHasChanged` on change; catch the JS failure so
prerendering falls back to the named destination.

Reject the tempting alternative: comparing the new URI against neighbouring stack entries.
`A → B → A` is a legitimate push and is indistinguishable from a back step.

## 3. Verifying it for real

Synthetic CDP `Input.dispatchMouseEvent` **bypasses the layer under suspicion** and gives a false
pass. Use genuine OS input:

1. Launch with `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=<port>` and attach
   over CDP (`http://localhost:<port>/json/list` → WebSocket) to read state. For the AntHill
   client, the launch line and a `cdp()` helper are in `anthill-client-live-verify`.
2. Inject from PowerShell with `user32!mouse_event` (or `SendInput`): `SetForegroundWindow`,
   `SetCursorPos` to window centre, then `MOUSEEVENTF_XDOWN` `0x0080` / `MOUSEEVENTF_XUP` `0x0100`
   with `mouseData` 1 (back) or 2 (forward).
3. Assert on **`history.state._index` deltas**, not on the path. If the physical mouse is in use,
   a navigation may be the human's: record a timestamped probe (`window.__probe`) and compare;
   `button 0` events appearing in it prove a human is at the mouse.
4. Forward needs forward history: build `2 → back → 1 → forward → 2`, or you cannot tell a dead
   button from an empty stack.

## 4. bUnit coverage

Stub the read and flip it to pin the reported bug:

```csharp
_ctx.JSInterop.Setup<int>("anthillHistory.behind").SetResult(2);  // then .SetResult(0) + link.Render()
```
That second setup is the regression test: the window moved the history by itself and the control
must notice.

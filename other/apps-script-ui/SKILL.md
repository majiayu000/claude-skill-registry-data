---
name: apps-script-ui
description: Builds Google Apps Script UI — custom menus, sidebars, modal dialogs, toast notifications, and alert/prompt dialogs via HtmlService and SpreadsheetApp.getUi(). Covers the modal progress-spinner pattern for long-running operations. Use when adding a menu item, sidebar, or dialog to a Sheets/Docs/Slides add-on, or when a dialog button silently does nothing. Framework-agnostic — applies with or without bootgs. Not for the quota, locking and batching concerns behind a slow action (`apps-script-services`), nor for Marketplace review and publishing (`apps-script-marketplace-publish`).
license: Apache-2.0
metadata:
  author: Maksym Stoianov
  version: "1.0.0"
---

# Apps Script UI

## Menus

`onOpen()` runs automatically when the file opens and builds the menu:

```ts
function onOpen(): void {
  SpreadsheetApp.getUi()
    .createMenu("My Add-on")
    .addItem("Do Something", "doSomething")
    .addSeparator()
    .addSubMenu(SpreadsheetApp.getUi().createMenu("More").addItem("Option A", "optionA"))
    .addToUi();
}
```

Menu item callbacks are referenced **by function name as a string**, not a reference — the function must be public (see Gotchas) and take no arguments.

## Sidebars

```ts
function showSidebar(): void {
  const html = HtmlService.createHtmlOutput('<h3>Quick Entry</h3><input id="value"><button onclick="submit()">Add</button>')
    .setTitle("Quick Entry")
    .setWidth(300);
  SpreadsheetApp.getUi().showSidebar(html);
}
```

Client-side JS in the HTML calls server functions through `google.script.run`:

```html
<script>
  function submit() {
    google.script.run
      .withSuccessHandler((result) => alert("Added!"))
      .withFailureHandler((err) => alert("Error: " + err.message))
      .addEntry(document.getElementById("value").value);
  }
</script>
```

## Modal dialogs and the progress-spinner pattern

For anything that takes more than a second or two, show a blocking modal with a spinner instead of leaving the UI frozen with no feedback:

```ts
function showProgress(message: string, serverFunctionName: string): void {
  const html = HtmlService.createHtmlOutput(`
    <div class="spinner"></div>
    <div id="msg">${message}</div>
    <script>
      google.script.run
        .withSuccessHandler(function (r) {
          document.getElementById("msg").innerText = "Done! " + (r || "");
          setTimeout(function () { google.script.host.close(); }, 1200);
        })
        .withFailureHandler(function (err) {
          document.getElementById("msg").innerText = "Error: " + err.message;
          setTimeout(function () { google.script.host.close(); }, 3000);
        })
        .${serverFunctionName}();
    </script>
  `).setWidth(320).setHeight(140);
  SpreadsheetApp.getUi().showModalDialog(html, "Working…");
}

// Menu calls this thin wrapper.
function menuDoWork(): void {
  showProgress("Processing…", "doTheWork");
}

// Must be public — no trailing underscore — see Gotchas.
function doTheWork(): string {
  // ... do the work ...
  SpreadsheetApp.flush();
  return "Processed 50 rows"; // shown in the success message
}
```

## Toast, alert, and prompt

```ts
SpreadsheetApp.getActiveSpreadsheet().toast("Done!", "Title", 5); // duration in seconds, -1 = until dismissed

const ui = SpreadsheetApp.getUi();

const response = ui.alert("Delete this?", "This can't be undone.", ui.ButtonSet.YES_NO);
if (response === ui.Button.YES) { /* proceed */ }

const result = ui.prompt("Enter a name:", ui.ButtonSet.OK_CANCEL);
if (result.getSelectedButton() === ui.Button.OK) {
  const name = result.getResponseText();
}
```

## Recipe: exporting the active sheet as a PDF

The export URL's query parameters are undocumented but stable; build them from the spreadsheet's own URL rather than hardcoding a host:

```ts
function exportSheetAsPdf(): GoogleAppsScript.Base.Blob {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const url = ss.getUrl().replace(/\/edit.*$/, "")
    + "/export?exportFormat=pdf&format=pdf&size=A4&portrait=true"
    + "&fitw=true&sheetnames=false&printtitle=false&gridlines=false"
    + "&gid=" + ss.getActiveSheet().getSheetId();
  return UrlFetchApp.fetch(url, {
    headers: { Authorization: "Bearer " + ScriptApp.getOAuthToken() },
  }).getBlob().setName("report.pdf");
}
```

## Gotchas

- **Functions ending in `_` are private and silently unreachable from UI.** A function named `doWork_()` cannot be called from a menu item, a sidebar's `google.script.run`, or a dialog — the call simply does nothing, with no thrown error on either side. This is the single most common "my dialog button does nothing" bug. Every menu item callback and every function invoked via `google.script.run` must have a public name — no trailing underscore.
- **Changes aren't visible until `SpreadsheetApp.flush()` runs.** If a dialog calls a server function that edits the sheet and then reports success, call `flush()` before returning — otherwise the dialog can show "Done" before the edit is actually applied.
- **`google.script.run` has no return value on the calling side.** `withSuccessHandler`/`withFailureHandler` are the only way to get the result back — treating the call as synchronous, or `await`-ing it directly, does nothing.
- **Only one modal dialog at a time.** Opening a second `showModalDialog` while one is already open doesn't queue it — design flows so the current dialog closes itself (`google.script.host.close()`) before the next one opens.

## Verification

- [ ] Every function referenced by name in a menu item, or called via `google.script.run` from any dialog/sidebar, has no trailing `_`.
- [ ] Any function that both modifies the sheet and is called from a dialog calls `SpreadsheetApp.flush()` before returning.
- [ ] Long-running actions (more than ~1-2 seconds) show a progress dialog or toast instead of leaving the UI unresponsive with no feedback.

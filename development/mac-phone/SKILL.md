---
name: mac-phone
description: "Execute one explicitly requested macOS Phone action. Use to dial one telephone number through tel: plus the fresh Click to Call confirmation, or to send one numeric DTMF digit through the verified active-call keypad. Use only the actual node_repl MCP with @oai/sky for UI actions, never Shell Node. Do not verify remote acceptance, hang up, redial, or infer another action."
---

# Mac Phone

Execute exactly one authorized action and stop. Assume Phone.app, the paired iPhone, permissions, audio routing, and microphones are configured. Do not inspect them.

## Accept one action

Accept exactly one:

```text
action: dial
destination: <exact telephone number>
```

```text
action: send_dtmf
dtmf: <exactly one digit 0-9>
```

Reject combined actions, missing values, contact names, non-digit DTMF, hang-up, mute, hold, transfer, automatic redial, and state-only inspection.

## Mandatory execution transport

Use the actual persistent Node REPL MCP `js` tool for every Computer Use action. Its callable name is `mcp__node_repl__js`. When MCP tools are nested under `functions.exec`, call `tools.mcp__node_repl__js(...)`.

Never run `node`, `node -`, `node -e`, `npm`, or `npx` through `exec_command` to import or use `@oai/sky`. Shell Node is not the Node REPL MCP and cannot substitute for it. Never use AppleScript, JXA, System Events, or coordinate automation.

Before any dial side effect, invoke the actual Node REPL MCP once:

```js
globalThis.sky = (await import("@oai/sky")).sky;
var macPhoneSkyReady =
  typeof sky.get_app_state === "function" &&
  typeof sky.click === "function";
nodeRepl.write(macPhoneSkyReady ? "SKY_READY" : "SKY_UNAVAILABLE");
```

Require the exact result `SKY_READY`. Set `computer_use_ready: true` only after that result. If the MCP tool is absent, the import fails, or readiness is not `SKY_READY`, return `NODE_REPL_UNAVAILABLE` with every action field false. For `dial`, do not dispatch the `tel:` URL.

This is only an execution-transport gate. Do not inspect microphone selection, permissions, paired-iPhone setup, audio routing, or Phone configuration.

## Dial

Accept an optional leading `+`, digits, spaces, parentheses, and hyphens only. Remove spaces, parentheses, and hyphens before building the URL. Preserve the leading `+` and every digit.

Only after `SKY_READY`, run `/usr/bin/open` with one quoted, validated argument:

```text
tel:<normalized destination>
```

Then use the same persistent Node REPL MCP session to obtain a fresh full state:

```js
var confirmState = await sky.get_app_state({
  app: "com.apple.notificationcenterui",
  disableDiff: true
});
nodeRepl.write(confirmState.text);
```

Read only `confirmState.text` as the accessibility tree. Never use `JSON.stringify(confirmState)` to locate controls. If the first state does not contain the confirmation card, obtain one more fresh full state, then stop if it is still absent.

Require one `FACETIME_NOTIFICATION`, one description containing `Click to Call`, and exactly one `button Description: Call`. Resolve the integer at the start of that exact button line from the current tree and click it only with:

```js
await sky.click({
  app: "com.apple.notificationcenterui",
  element_index: freshCallIndex
});
```

The click argument is `element_index`, never `index`. Never use a hard-coded index, screenshot coordinate, stale state, Phone.app keypad, `Return`, contact row, Recents call button, Cancel button, or a Shell Node fallback.

Stop after the Call click. Do not check whether the paired iPhone dialed, the remote phone rang, or the call connected.

## Send DTMF

Require exactly one digit `0` through `9`.

Bootstrap and require `SKY_READY` through the actual Node REPL MCP, then obtain a fresh full state from `com.apple.notificationcenterui`. Read `state.text`, not the serialized state object. Do not run any shell command for DTMF.

If the active keypad is closed, require the `FACETIME_NOTIFICATION` to contain all of:

- a description containing `using your iPhone`
- a visible elapsed duration such as `0:06`
- `button Description: Keypad`
- `button Description: End`

Resolve the fresh Keypad integer index and click it once with `element_index`.

Then obtain a new full state from `com.apple.notificationcenterui`. If that read times out, retry it once without clicking Keypad again.

Require the opened active-call surface to contain all of:

- the active destination or contact
- a visible elapsed duration
- `button Description: End`
- `container Description: Keypad`
- digit buttons `0` through `9`

If the active keypad was already open in the first state, skip the Keypad click and use that state directly.

Locate the requested digit's fresh button. Examples of the observed labels include `3, DEF` and `0, +`. Click the exact button whose description begins with the requested single digit, using `sky.click({ app: "com.apple.notificationcenterui", element_index: freshDigitIndex })`.

Never use `press_key`, `type_text`, the ordinary Phone dial keypad, `index`, a hard-coded index, coordinates, or Shell Node for DTMF. Stop immediately after the digit button click. Do not inspect remote acceptance and do not hang up.

## Return JSON only

```json
{
  "skill": "mac-phone",
  "action": "dial|send_dtmf",
  "requested_value": "<normalized destination or one digit>",
  "computer_use_ready": false,
  "tel_request_dispatched": false,
  "call_button_clicked": false,
  "active_call_verified_before_action": false,
  "active_call_keypad_opened": false,
  "dtmf_button_clicked": false,
  "remote_acceptance": "unknown",
  "call_status": "unknown",
  "error_code": null,
  "details": ""
}
```

Report local command execution only. Use only these error codes:

- `INVALID_REQUEST`
- `MULTIPLE_ACTIONS_NOT_ALLOWED`
- `NODE_REPL_UNAVAILABLE`
- `TEL_OPEN_FAILED`
- `CONFIRMATION_CONTROL_NOT_FOUND`
- `CONFIRMATION_CLICK_FAILED`
- `ACTIVE_CALL_NOT_VERIFIED`
- `ACTIVE_CALL_KEYPAD_NOT_FOUND`
- `DTMF_CONTROL_NOT_FOUND`
- `DTMF_CLICK_FAILED`

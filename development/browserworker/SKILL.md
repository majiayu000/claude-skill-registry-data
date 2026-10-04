---
name: BrowserWorker
description: Use this skill when a user asks to automate a website with BrowserWorker, create a reusable browser action script, inspect a page, use page_semantics/semantic_key, use browser snapshots, ask the user to record/upload a flow, or turn recorded trace/interests/script_hints into a working action. It covers the BrowserWorker daemon, Chrome extension transport, semantic-first workflow, snapshot validation, recording fallback, DOM extraction, action development, validation, and debugging.
---

# BrowserWorker Script Builder

Use this repo to either complete a one-off browser task or build a reusable browser action script. Prefer completing the user's actual task over only explaining an approach.

## Mental Model

- BrowserWorker exposes HTTP APIs and action execution through the Python daemon.
- The Chrome extension is the browser transport and can read the real rendered page, including content inserted by other extensions.
- BrowserWorker daemon startup opens only HTTP/WebSocket services. When an agent first needs browser control, the daemon may launch sandbox Chrome on demand with unpacked extensions passed through the normal Chrome `--load-extension` argument. Default Chrome startup must not add a remote debugging port and must never call CDP `Extensions.loadUnpacked`. An agent must not switch to CDP just because `/plugin/status` shows `connected: 0`.
- After plugin transport navigates to a `1688.com` page, the daemon uses `browser.evaluate` through the BrowserWorker extension to poll open Shadow DOM roots and close the 1688 onboarding guide. It prefers `.guide-container .close` and falls back to `.btn-know`; this hook must not use CDP.
- Default plugin control uses only Python stdlib plus project files. Do not add pip/npm dependencies or hard-code user-specific Chrome, virtualenv, or profile paths for browser control. `websocket-client` is optional and only needed for explicit CDP debugging.
- Resolve the daemon port in this order: `BrowserWorker_PORT`, `BrowserWorker_LOCK_FILE`, `MANAI_WORKSPACE_ROOT/MANAI_HOME` + `storage/browser_daemon.lock`, legacy `~/.BrowserWorker/BrowserWorker.lock`, then `12321`.
- One-off tasks can use `/plugin/call`, `browser.snapshot`, and small `browser.evaluate(...)` probes without creating a file.
- Built-in reusable scripts in `browser_service/actions/*.py` must stay generic and expose `metadata` plus `handler(browser, args)`.
- The `browser` object supports `goto`, `evaluate`, `click`, `fill`, `press`, `wait_ms`, `snapshot`, `detect_page_state`, `request_help`, `url`, `title`. `click` / `fill` / `press` can use a current `handle`, a `semantic_key`, a structured target, a selector, or a compatibility `@eN`.
- One task should use one `session_id`. A session can own multiple named tabs through `tab_key` values such as `main`, `search`, `detail`, or `upload`.
- Data extraction should usually run JavaScript in the real page with `browser.evaluate(...)`; this reads rendered DOM, not raw HTTP HTML.
- Long-lived scripts must use `semantic_key` or structured targets. Snapshot `handle` / `@eN` / `ref` are current-page execution handles, not persistent locators.

## Login, Captcha, And Verification Pause

Never bypass a website login, slider, captcha, or anti-bot check. When an operation reaches a `login`, `captcha`, or `blocked` page state:

1. Stop the current employee task immediately. Do not retry the browser action or continue with LLM calls.
2. Return the BrowserWorker structured intervention result to the user, including `state`, target `url`, and `message` (`status: "need_human_help"`, `code: "human_intervention_required"`).
3. Tell the user to complete the login, slider, captcha, or other verification in the open BrowserWorker Chrome window. Do not ask for account passwords, verification codes, cookies, or other credentials in chat.
4. Leave the task in `waiting_human`. The browser may become ready after the user finishes the page interaction, but the employee must not resume automatically.
5. Resume only after an explicit user action: the user clicks `继续任务` in the GUI or sends a new message in the same employee session. That action clears the old `waiting_human` state and starts a new employee task; do not gate it on a stale page-state probe. The new browser operation performs a fresh interception check and pauses again only if the page is still truly blocked.

Use `browser.request_help(...)` in an action when a known workflow reaches a verification step. Platform-level detection will also pause the task if a browser action lands on an intercepted page.

## User Help And Popup Buttons

Use this section when a user asks what BrowserWorker is, how to use the browser plugin, why the plugin says disconnected, or what the popup buttons mean. Answer in the user's language and keep guidance operational.

BrowserWorker has two parts:

- **Daemon service**: a local Python service, normally listening on `127.0.0.1:12321`, that receives browser tasks from agents and saves uploaded recordings.
- **Chrome extension**: the BrowserWorker plugin loaded in the sandbox Chrome profile. It connects to the daemon through a local WebSocket, normally `127.0.0.1:22321`, reads the real rendered page, executes browser actions, and records user-selected flows.

The extension popup is primarily for **recording a page flow for the agent**, not for starting or stopping the whole ManAI app.

Popup status:

- `已连接 / connected`: the extension is connected to the daemon. Upload and browser-control features can work.
- `未连接 / disconnected`: the extension is loaded but cannot reach the daemon. Tell the user to start ManAI/BrowserWorker daemon first, then reload the page or reopen the sandbox Chrome.
- `待上传记录 / pending records`: the number of recorded user steps currently stored in the extension and waiting to be uploaded.

Popup buttons:

- `开始` / user may say `启动`: starts recording on the current active normal web page. After clicking it, BrowserWorker injects a lightweight recorder into the page and records user clicks/hover context/navigation as candidate steps. It does **not** start Chrome, does **not** start the daemon, and does **not** submit anything to the website by itself.
- `结束`: stops the current recording session and removes the page recording overlay/listeners. The recorded steps remain in `待上传记录` so the user can still upload them. It does **not** close Chrome, stop the daemon, or delete the pending records.
- `上传记录` / user may say `上传`: sends the pending recorded trace from the extension to the connected daemon. If recording is still active, the extension automatically stops recording first, then uploads. The daemon saves generated artifacts such as `<task>.trace.json`, `<task>.interests.json`, `<task>.script_hints.json`, and updates `page_semantics.json` when applicable. After a successful upload, the extension clears the pending count to `0`.
- `清除` / user may say `清0` or `清零`: clears pending recorded steps from the extension and resets the pending count to `0`. If recording is still active, it keeps recording but clears the current accumulated steps/count. It does **not** uninstall the plugin, clear browser cookies, clear the Chrome profile, delete daemon-side files already uploaded, or reset website state.

Recommended user-facing recording flow:

1. Ask the user to open the target page in the sandbox Chrome where BrowserWorker is loaded.
2. Confirm the popup shows `已连接`. If it shows `未连接`, start or restart the BrowserWorker daemon and ask the user to reopen/reload the page.
3. Ask the user to click `开始`.
4. Ask the user to perform only the important target operation: click the desired button, fill the relevant input, choose a menu item, or navigate through the needed flow. Avoid unnecessary clicks.
5. Ask the user to click `上传记录` when done. They may click `结束` first if they want to stop and review the pending count, but it is not required because upload stops active recording automatically.
6. After upload, inspect the generated `recordings/*.trace.json`, `recordings/*.interests.json`, `recordings/*.script_hints.json`, and `recordings/page_semantics.json` before turning the flow into an action.

Troubleshooting:

- If `上传记录` is disabled, likely there are no pending records, recording is still active, or the plugin is disconnected.
- If upload says `BrowserWorker daemon 未连接，无法上传记录`, start/restart the daemon and retry upload before clearing records.
- If the user accidentally recorded useless steps, tell them to click `清除/清0` and record again.
- Do not tell users that `结束` uploads records; upload is a separate button. However, clicking `上传记录` while recording is active will automatically stop recording first and then upload.
- Do not tell users that `清除/清0` deletes already uploaded files; it only clears extension-side pending records.

## Choose the Mode

Use **one-off execution** when the user wants a simple immediate result: click one button, fill one form, read a value, export a short list, check page state, or operate one currently open page. Do not create an action file unless reuse is likely.

Use **reusable script generation** when the user asks for a repeatable workflow, batch collection, parameterized inputs, future reuse, or an action that should live in the target skill's `scripts/actions/` directory.

Both modes use the same core loop: resolve semantic intent, validate against the current page, act or extract, verify result, escalate to recording only when needed. For sites with login, rate limits, captcha, or anti-bot behavior, follow the anti-bot rules below before writing or running an action.

## Default Workflow

1. Confirm BrowserWorker/extension status when needed:

Default ports: BrowserWorker HTTP uses `127.0.0.1:12321`; the extension WebSocket uses `127.0.0.1:22321`.

```bash
python3 - <<'PY'
import json, urllib.request
print(urllib.request.urlopen("http://127.0.0.1:12321/ping", timeout=2).read().decode())
PY
```

If sandbox blocks loopback, rerun with escalation. If BrowserWorker is down, start only the daemon service:

```bash
BrowserWorker_LOCK_FILE=<workspace_root>/storage/browser_daemon.lock python3 -m browser_service.daemon --transport auto
```

GUI and packaged-app startup code controls daemon-start Chrome policy; normal builds do not open Chrome during GUI startup. Task-time Chrome launch is handled on demand by daemon code. Do not manually restart the daemon with different startup flags unless the user or task explicitly requests that mode.

2. Semantic first, snapshot for discovery and validation.

For a known page, first look for a `semantic_key` under the current `page_key + page_role` and use it directly or as a hint. For a new or uncertain page, use `browser.snapshot` or `/plugin/call` before asking the user to record. Choose the lightest snapshot that can locate and validate the element:

- `quick`: first pass for normal controls, buttons, inputs, dialogs.
- `data`: cards, rows, search results, product lists, table-like content.
- `section`: when a root selector/text/rect or known domain section is available.
- `full`: when the page has limited elements or lighter snapshots miss the target. Avoid on very large pages unless needed.
- `ax`: accessibility tree fallback when DOM snapshot misses semantic controls.

Snapshot scans accessible frames and open Shadow DOM by default. Returned nodes include a stable-in-document `handle`; frame nodes include `frame_id/frame_url`, and shadow nodes include `shadow_path`. Prefer `semantic_key` or a structured target for reusable scripts, then let BrowserWorker resolve it to the current handle. Prefer the current handle only for immediate execution so the extension dispatches the action to the exact node in the correct frame/root. `@eN` remains a compatibility/readability ref. `quick` is viewport-only, while `section/data/full` may include rendered offscreen elements. Candidate order is relevance-ranked rather than raw DOM order. `ax` merges Chrome accessibility role/name/state into DOM-backed nodes instead of replacing the DOM snapshot.

### Snapshot Compatibility Rules For Scripts

The upgraded snapshot remains compatible with normal `browser.snapshot`, `browser.click`, `browser.fill`, `browser.press`, `browser.scroll_to`, and `browser.hover` workflows, but script authors must account for these behavioral rules:

- Treat snapshot output as a ranked semantic view, not DOM order. Candidate scoring, category quotas, and deduplication can change output order. The extension now assigns a stable compatibility `@eN` from the element handle, so the same connected Element keeps its ref across snapshots, but scripts must not infer meaning from the numeric value.
- Prefer `semantic_key` or a structured target for reusable actions. Prefer `handle` only for an immediate one-off operation. A handle remains stable for the same Element across quick/data/section/full/ax snapshots, but becomes stale after document replacement or when a framework detaches and recreates the node.
- After navigation, refresh, major DOM updates, or a stale/changed-target error, resolve the semantic target again. Never persist a handle, `ref`, or `@eN` in an action script or `page_semantics.json`.
- Do not write scripts that assume a specific numeric ref such as “the search button is always `@e2`”. Match the current node by `semantic_key`, role, accessible name, stable attributes, business meaning, and relevant container, then use the resolved current handle.
- Existing snapshot fields remain available. `handle`, `semantic_key`, `frame_id`, `frame_url`, `shadow_path`, `score`, `partial`, `truncated_reason`, and `timing` are additive metadata; scripts that do not need them may ignore them.
- Pass an optional `task_hint` (`intent`, `target`, and/or `keywords`) when the page contains many otherwise valid candidates. It changes ranking only; it does not bypass current-DOM validation.
- Check `stability.stable`, `stability.quiet_ms`, and `document_revision` on frequently rerendered pages. If the target region is still mutating, wait briefly and take a new bounded snapshot before a high-impact action.
- Prefer `handle` or a resolved structured target for iframe and open Shadow DOM elements. The extension uses the attached frame/root metadata to dispatch the operation correctly; a top-document CSS selector or ordinary `document.querySelector(...)` cannot reliably reach those elements.
- `quick` intentionally excludes offscreen candidates. If the target is below the fold, first use `section`, `data`, or `full`, or scroll and take a new `quick` snapshot.
- `section`, `data`, and `full` can include rendered offscreen elements. Do not equate inclusion in their output with current viewport visibility; scroll to the resolved current handle/target before an operation when the site requires the element to be on screen.
- `ax` is now a DOM+Accessibility fusion result. Prefer DOM-backed controls that retain selector/layout/ref and use AX role/name/state as semantic evidence. Do not depend on the old AX-only node shape or duplicate `StaticText` entries.
- Accessible names may come from native `<label>`, `aria-labelledby`, `aria-label`, control value, or nearby text. Prefer role plus accessible name when visible text is absent, but verify duplicate names within the relevant form/dialog/container.
- On very large SPAs, frequently rerendered pages, virtual lists, and nested cross-origin frames, keep each operation closed-loop: resolve semantic target, snapshot or probe for current evidence, act by current handle, verify the expected state, then re-resolve before the next dependent action.
- When a lightweight snapshot misses a target, escalate in this order: scoped `section`/`data`, scroll and resnapshot, `full` on a bounded page, `ax`, a small DOM probe, then user recording. Do not immediately replace the normal extension path with CDP.

```json
{
  "method": "browser.snapshot",
  "params": {
    "session_id": "dev",
    "snapshot_mode": "data",
    "domain_hint": "1688.com",
    "section": "results",
    "task_hint": {
      "intent": "extract products",
      "keywords": ["title", "price"]
    },
    "max_nodes": 80
  }
}
```

Use snapshot output to identify semantic keys, stable selectors, current handles/refs, visible text, page state, login/captcha, cards, forms, dialogs, and data rows. Do not treat snapshot output as a script cache.

3. If snapshot is insufficient, run a small JS probe against the real rendered DOM before asking for a recording:

```python
browser.evaluate("""
(() => [...document.querySelectorAll('button,a,input,[role]')]
  .slice(0, 80)
  .map((el) => ({
    tag: el.localName,
    text: (el.innerText || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 80),
    href: el.href || '',
    cls: String(el.className || '').slice(0, 80)
  })))()
""")
```

Use JS probes to check exact selectors, inner text, href patterns, field values, lazy-loaded content, and whether an element exists after scrolling.

4. If snapshots and JS probes are insufficient, ask the user to record the flow using the extension popup (引导文案：点击[开始]，操作页面里的目标元素，点击[上传记录]；也可以先点[结束]再点[上传记录])。After upload, inspect:

```text
recordings/<task>.trace.json
recordings/<task>.interests.json
recordings/<task>.script_hints.json
recordings/page_semantics.json
```

`page_semantics.json` is an aggregate of targets and important clickable/card/form/dialog context from uploaded recordings, keyed by `page_key + page_role`. Normal snapshots do not write to it. Later snapshots use these recorded semantic hints only after re-validating them against the current DOM.

### Maintain Page Semantics From Snapshots

`page_semantics.json` may contain important semantic elements learned from either uploaded recordings or an agent-reviewed snapshot. This is an agent workflow, not an automatic rule that persists every snapshot node.

Before operating a known page:

1. Resolve the current `page_key + page_role`.
2. Read the matching entry in `page_semantics.json` when the file exists.
3. Treat stored elements as navigation and interpretation hints, not as proof that an element still exists.
4. Re-validate every stored selector, stable attribute, role, name, visibility, enabled state, and relevant page relationship against the current DOM before using it.
5. Resolve the semantic element against the current page, then use its current handle for the actual operation. A compatibility `@eN` or currently verified selector remains acceptable for old actions. Never execute a persisted handle/ref or stale locator directly.

After reviewing a snapshot, the agent may merge an element into `page_semantics.json` when it is important for understanding or operating that page. Good candidates include:

- Primary search, submit, create, save, confirm, cancel, next, upload, and navigation controls.
- Login, captcha, permission, error, empty-state, and blocking dialogs.
- Main forms and their key inputs.
- Result lists, tables, repeated cards, pagination, filters, and sort controls.
- Business-critical fields such as product title, price, stock, status, order number, supplier, totals, and validation messages.
- Containers or relationships needed to disambiguate two controls with similar names.

Do not store every node returned by snapshot. Do not add decorative nodes, transient recommendations, arbitrary list rows, unstable coordinates, handles, old `@eN` refs, current input values, cookies, tokens, personal data, or complete page text.

When updating the file:

- Merge strictly under the matching `page_key + page_role`; do not copy an element to another page role merely because the URL or text looks similar.
- Preserve existing elements and recording evidence. Update or add only the reviewed semantic element.
- Prefer stable evidence in this order: `data-testid/data-test/data-qa` -> `name/aria-label` -> stable `id` -> role plus accessible name -> structural relationship -> CSS/XPath fallback.
- Record `source: "snapshot"` for snapshot-derived knowledge when extending the schema, and retain a short semantic label, confidence, last verification time, and the compact target evidence.
- Increase confidence only after the element has been verified on the current page; successful operation plus expected result is stronger evidence than appearance in a snapshot.
- Lower confidence, replace the locator, or remove only the invalid locator evidence when repeated current-page validation fails. Do not delete unrelated page semantics.

The purpose of snapshot-derived semantics is to help future agents understand the page faster. It must not turn `page_semantics.json` into a persisted copy of the page.

Minimal `page_semantics.json` shape:

```json
{
  "schema_version": 2,
  "updated_at": "2026-07-30T14:51:19+0800",
  "pages": {
    "<page_key>::<page_role>": {
      "page_key": "example.com/search",
      "page_role": "search_results",
      "sample_url": "https://example.com/search?q=cup",
      "updated_at": "2026-07-30T14:51:19+0800",
      "elements": [
        {
          "semantic_key": "search.primary_input",
          "kind": "target",
          "label": "Search",
          "confidence": 0.86,
          "target": {
            "role": "textbox",
            "name": "Search",
            "selector": "input[name=\"q\"]"
          },
          "evidence": {
            "page_scoped": true,
            "source_kind": "target"
          },
          "verification": {
            "success_count": 1,
            "failure_count": 0,
            "last_verified_at": "2026-07-30T14:51:19+0800"
          }
        }
      ]
    }
  }
}
```

Common semantic keys:

- `search.form`, `search.primary_input`, `search.submit`
- `login.username`, `login.password`, `login.submit`
- `dialog.confirm`, `dialog.cancel`, `dialog.close`
- `pagination.next`, `pagination.previous`
- `result_list`, `result_card`, `result_card.primary_link`
- `filter.<name>`, `sort.<name>`, `upload.input`, `form.submit`

`semantic_key` is scoped by `page_key + page_role`. The same key can exist on different page roles, but it must be unique within one page entry.

When an action lives in an external skill directory, pass that skill action directory when using `semantic_key`; otherwise BrowserWorker may only search the default recordings directory:

```python
from pathlib import Path

ACTION_DIR = str(Path(__file__).resolve().parent)
browser.click(semantic_key="search.submit", action_dir=ACTION_DIR)
browser.fill(None, args["keyword"], semantic_key="search.primary_input", action_dir=ACTION_DIR)
```

Or query daemon:

```text
GET /record/latest
GET /record/interests?task_name=<task>&url=<current_url>
GET /record/script-hints?task_name=<task>&url=<current_url>
```

5. Execute through semantic keys, structured targets, current handles, or JS.

For reusable scripts, use `semantic_key` when a known page semantic exists:

```json
{"method": "browser.click", "params": {"session_id": "dev", "semantic_key": "search.submit"}}
```

Use a structured target when the semantic key is not recorded yet or the script should remain generic:

```json
{
  "method": "browser.click",
  "params": {
    "session_id": "dev",
    "target": {
      "role": "button",
      "name": "搜索",
      "within": {"role": "search"}
    }
  }
}
```

For one-off tasks immediately after a snapshot, a current handle is acceptable:

```json
{"method": "browser.click", "params": {"session_id": "dev", "handle": "<current_snapshot_handle>"}}
```

or:

```python
browser.evaluate("document.querySelector('#submit').click(); true")
```

Compatibility `@eN` refs remain accepted for current-page debugging, but do not write them into reusable actions or page semantics.

When a click can open a new tab, pass `follow_new_tab: true` and optionally `new_tab_key` so the opened tab is attached to the same BrowserWorker session. For key presses, use either `{"op":"press","args":["Enter"]}` for the active element or `{"op":"press","args":["#search-input","Enter"]}` to focus a selector first.

For reusable tasks, develop the action script in the target skill's `scripts/actions/` directory. Use `browser_service/actions/` only for generic built-in helpers such as `flexible_access.py`.

6. Validate. One-off tasks need visible/result-state verification. Reusable scripts need syntax tests, unit tests where relevant, and at least one real daemon run when the task depends on live page behavior.

## Anti-Bot And Rate Limits

Use these rules for every new website skill, not only for 1688. The goal is to reduce login challenges, sliders, captcha, temporary blocks, and accidental bulk actions.

Default execution order:

1. Resolve known `semantic_key` / page semantics first, then read the current page with `snapshot` or a small `browser.evaluate(...)` probe to validate it.
2. Reuse a user-opened or already-navigated page whenever possible.
3. Use the site's normal UI flow for search/filter/sort when practical.
4. Construct direct URLs only when UI interaction is unreliable or too expensive.
5. Keep the run bounded by explicit limits such as `limit`, `pages`, `max_items`, `max_detail_visits`, and `timeout_ms`.
6. Stop as soon as the requested data or action count is complete.

Reduce navigation frequency:

- Do not reload, reopen, or re-search if the current page already has the required data.
- Avoid opening detail pages when list cards contain the needed fields.
- Batch extraction from the current DOM instead of looping over many page loads.
- For one-off tasks, default to small scopes such as top 10 or one page.
- For reusable scripts, expose conservative defaults and require explicit args for larger runs.

Avoid mechanical behavior:

- Add jitter between scrolls, clicks, typing, and page transitions.
- Do not use the same fixed scroll sequence for every run when a few varied scrolls work.
- Before clicking, check that the target is visible, enabled, and not already completed.
- Space out repeated row/card actions; do not rapidly click many elements in a tight loop.
- Use `dry` or preview mode before executing a high-impact or multi-item action.
- Never bypass login, captcha, slider, or security checks. Use `browser.request_help(...)`.

Be careful with direct URL parameters:

- Prefer natural search: fill the search box and click the search button.
- Prefer UI controls for filters/sort when they are available and stable.
- If direct URL construction is needed, add only the minimum parameters.
- Verify Chinese query encoding before constructing search URLs: check whether the target site expects standard UTF-8 (`urllib.parse.quote(keyword)`) or legacy GBK / GB2312 (`urllib.parse.quote(keyword.encode('gbk'))`) encoding for Chinese keywords. Inspect target site form submission or live URL parameters first.
- Do not repeatedly hit filtered pagination URLs in a fast loop.
- Derive follow-up URLs from the current page URL when possible, rather than inventing full URLs from scratch.
- Record why direct URL construction is used if the site is sensitive or has known anti-bot behavior.

If a site starts showing captcha or verification:

- Stop the run or call `request_help`; do not retry aggressively.
- Report which step triggered it: first navigation, search, filter URL, scroll/load, detail opening, or repeated action.
- Reduce scope before the next run.
- Prefer current-page extraction and fewer navigations in the next script revision.

## Session Tabs

Use one `session_id` per task run. Use multiple named tabs inside that session when a workflow naturally needs separate pages, such as search results plus details, source plus target, or upload plus preview.

Default model:

```text
session_id = skill_run_id
tab_key=main   -> default tab for old actions
tab_key=search -> search/list page
tab_key=detail -> detail page
tab_key=upload -> upload/form page
```

All browser operations accept an optional `tab_key`. If omitted, the current active tab for the session is used; old single-tab actions continue to work.

```python
browser.goto(search_url, tab_key="search")
rows = browser.snapshot(tab_key="search")

browser.goto(detail_url, tab_key="detail")
title = browser.evaluate("document.title", tab_key="detail")

browser.switch_tab("search")
current_url = browser.url()
```

Available tab helpers:

- `browser.new_tab(tab_key, url=None)`
- `browser.switch_tab(tab_key)`
- `browser.active_tab()`
- `browser.list_tabs()`
- `browser.close_tab(tab_key)`
- `browser.close()`

Use business names for `tab_key`; do not expose Chrome tab IDs to action code. Examples: `search`, `detail`, `compare`, `source`, `target`, `upload`, `preview`.

The daemon has a `TabManager` registry for `(session_id, tab_key)` resources. The extension owns the actual Chrome tab IDs and enforces session-tab lookup. A task must only operate tabs inside its own `session_id`.

Domain concurrency is separate from tab ownership. `/lock/acquire` supports `domains` plus `concurrency_policy`:

- `domain`: default; sessions with the same domain are mutually exclusive.
- `none`: only session tab ownership is enforced; useful for sites that are safe to run concurrently.

Use `domain` or a stricter future policy for login-heavy or anti-bot-sensitive websites. Use `none` only when parallel access to the same domain is acceptable.

## Fast Element Location

The main skill is locating the right element quickly. Use this order:

1. Existing `page_semantics` / `semantic_key` for known pages and recurring workflows.
2. Structured target from the user's intent: role, name/text, stable attributes, container, business ID, and filters.
3. `quick` snapshot for obvious inputs/buttons/links and current viewport controls.
4. `data` snapshot for lists, cards, rows, product results, metrics.
5. `section` snapshot if you can scope to a form, dialog, card list, table, or known text.
6. `full` snapshot if the page is small or has limited elements and earlier snapshots missed.
7. Small JS probes with `querySelectorAll`, text filtering, href filtering, and `getBoundingClientRect`.
8. Scroll and repeat snapshot/probe for lazy-loaded content.
9. User recording/upload if the element is hidden behind hover, dynamic extension UI, canvas-like controls, shadowed interaction, or the page is too complex to infer.

When acting, prefer:

- `semantic_key` for reusable actions after resolving it under the current `page_key + page_role`.
- Structured target for generic scripts or newly explored pages.
- Snapshot `handle` for immediate one-off interactions; `@eN` remains supported for compatibility and human-readable snapshot output.
- Minimal CSS reliance: avoid hashed, generated, or layout-dependent CSS class names (e.g., React/Vue/Tailwind dynamic classes).
- Stable selectors for scripts: `[data-testid]`, `[name]`, `[aria-label]`, `#id`.
- Text/href/business-ID filtering in JS when selectors are unstable.
- `getBoundingClientRect()` sorting for “top N” or “first visible” tasks.

Avoid brittle absolute selectors or deep CSS path selectors (e.g. `div > div.class > span:nth-child(2)`) unless there is no better option. If using one, preserve fallback logic or raw evidence for debugging.


## Page Identity Rules

Use the shared page identity layer whenever recorded data is involved:

- `browser_service/page_identity.py`
- `TraceStore.find_page_interests(...)`
- `TraceStore.find_page_script_hints(...)`

Do not mix all trace candidates globally. First determine the current page identity, then use hints scoped by `page_key` or `page_role`.

Expected 1688 roles include:

- `1688_home`
- `1688_search_results`
- `1688_offer_detail`

If a real URL is misclassified, patch `page_identity.py` and add a test in `tests/test_page_identity.py`.

## Writing an Action

Create `browser_service/actions/<name>.py`:

```python
metadata = {
    "name": "<name>",
    "description": "...",
    "input_schema": {"type": "object", "properties": {}},
}

def handler(browser, args: dict) -> dict:
    ...
    return {"success": True, "items": items}
```

For ManAI skills or other external skills, actions should live in that skill's own `scripts/actions/` directory. Always call daemon `/execute` with `action_search_path` pointing at the target skill actions directory. The daemon must load `action_search_path` before built-in `browser_service/actions`; built-ins are fallback only. Check the `/execute` response `action_path` to confirm the file actually used.

Example target path:

```text
<workspace_root>/skills/1688-selection-upload/scripts/actions
```

Use the browser transport directly:

```python
browser.goto(url, timeout_ms=45000)
browser.wait_ms(3000)
data = browser.evaluate(JS_EXPRESSION)
```

For pages with login, captcha, or anti-bot checks, reuse or implement a `_guard(browser)` pattern. Do not bypass security systems. If human action is needed:

```python
browser.request_help(
    title="需要人工处理",
    prompt="请完成登录/验证，然后点击 Continue。",
    target=".nc_wrapper,#nocaptcha,[class*='captcha'],#login-form,.login-box",
    reason="login_or_captcha",
    domain_hint="wikipedia.org",
    timeout_ms=300000,
)
```

`request_help(validate_after=True, domain_hint="...")` is the default. It performs a framework-level second check after the user continues. It calls `detect_page_state` and raises if the page is still blocked by states such as `login`, `captcha`, `blocked`, `blank`, `restricted`, `wrong_domain`, or `page_error`. Pass `validate_after=False` only for deliberate manual demos where the action should not validate readiness.

Use `browser.detect_page_state(domain_hint=None, tab_key=None)` when you need a lightweight generic page state before acting. It returns `state`, `confidence`, `reason`, `suggested_action`, `url`, `title`, `signals`, and `evidence`. Standard states are `ok`, `login`, `captcha`, `region_prompt`, `blocked`, `not_found`, `empty_result`, `wrong_domain`, `blank`, `restricted`, `page_error`, and `unknown`. This is a generic page-readiness detector, not a product-page detector. `signals.not_target_domain` is kept only for backward compatibility; new code should use `wrong_domain`.

For actions that can wait for a user, declare the expected upper bound:

```python
metadata = {
    "name": "my_action",
    "description": "Short action description.",
    "max_runtime_ms": 330000,
}
```

For long actions, prefer the async daemon protocol: `POST /execute/start` returns `job_id`, then poll `GET /execute/status?job_id=...`. Job statuses are `queued`, `running`, `waiting_for_user`, `success`, `failed`, and `error`. CLI wrappers should poll or long-wait instead of using a short 120 second HTTP timeout when `max_runtime_ms` is high.

## DOM Extraction Pattern

Prefer JavaScript executed in the page:

- Read `document.querySelectorAll(...)`, `innerText`, `href`, and attributes.
- Use `getBoundingClientRect()` plus `scrollY` to sort visual order.
- Use stable business IDs such as `offerId` for de-duplication.
- Normalize whitespace and invisible Unicode.
- Wait and scroll for lazy-loaded or plugin-inserted content.
- Return JSON strings from JS if the payload is complex, then parse in Python.

Example principles:

```javascript
const clean = (s) => String(s || "").replace(/[\u200B-\u200F\u202A-\u202E\u2060\uFEFF]/g, "").replace(/\s+/g, " ").trim();
const rows = [...document.querySelectorAll("a.search-offer-wrapper")].map(card => ({
  text: clean(card.innerText),
  href: card.href
}));
return JSON.stringify(rows);
```

When extracting from current visible DOM, do not assume a field is native to the site. If the user says not to distinguish source, treat current page-visible content as the data source.

## Structured Target Pattern

Use structured targets when a reusable script needs to operate a class of pages without relying on a recorded semantic key. The plugin resolves the target against the current DOM, validates uniqueness, then acts on the current handle.

```python
browser.fill(
    {
        "role": "textbox",
        "name": "搜索",
        "within": {"role": "search"},
        "visible": True,
        "enabled": True,
    },
    args["keyword"],
)
browser.click({"role": "button", "name": "搜索", "within": {"role": "search"}})
```

Good target evidence:

- `role` and accessible `name` for controls.
- `within` for forms, dialogs, cards, search areas, and repeated rows.
- Stable attributes such as `data-testid`, `data-test`, `data-qa`, `name`, `aria-label`, and stable `id`.
- Business identifiers in `href`, row/card text, product/order IDs, or status fields.
- Explicit filters for repeated elements, for example visible text, href pattern, nth within a filtered list, or card index after sorting by rendered position.

Bad target evidence:

- Persisted `@eN`, `handle`, raw coordinates, or stale selector from a previous page load.
- Deep CSS paths and generated class names as the only locator.
- Ambiguous role/name without a container or filter.
- Current input values, tokens, cookies, user personal data, or complete page text.

If target resolution returns ambiguous candidates, do not silently click the first candidate. Add a `within` container, stricter name/text, stable attribute, business ID, or ask for a recording.

## Action Closed Loop

For every page operation that changes state:

1. Confirm page readiness with `detect_page_state` when login/captcha/blocked states are possible.
2. Resolve `semantic_key` or structured target against the current DOM.
3. Validate uniqueness, visibility, enabled state, and relevant container.
4. Act using the resolved current handle.
5. Verify a postcondition: URL changed, input value set, list updated, dialog closed/opened, row selected, upload completed, or expected text appears.
6. Re-resolve before the next dependent action if the page navigated, rerendered, or `stability.stable` is false.

Do not use a long chain of stale handles collected from one snapshot on a dynamic page. Resolve-and-act per step is slower than a blind click chain but materially safer on mainstream SPA pages.

## Robustness Checklist

- Use semantic keys or structured targets first, then stable selectors as evidence: IDs, business attributes, known card classes, href patterns.
- Filter out unrelated links such as chat/IM/share links.
- Deduplicate by business key, not by full URL.
- Sort by rendered position for “top N”.
- Tighten completion conditions: if the user asks for top 10 price and monthly sales, wait until top 10 have both or report missing counts.
- Keep raw evidence (`raw_text`, `href`, `selector`) when useful for debugging.
- Return explicit `missing_*` counters when data may be partially unavailable.
- Keep actions parameterized: keyword, limit/pages, timeout.

## Running and Validating

Syntax and test checks:

```bash
python3 -m py_compile browser_service/actions/<name>.py
python3 -m pytest
```

Execute through daemon:

```python
import json, urllib.request
base = "http://127.0.0.1:12321"
payload = {
  "session_id": "dev",
  "action": "<name>",
  "action_search_path": "/path/to/target/skill/scripts/actions",
  "args": {"keyword": "保温杯", "limit": 10, "timeout_ms": 60000}
}
req = urllib.request.Request(
  base + "/execute",
  data=json.dumps(payload).encode(),
  headers={"Content-Type": "application/json"},
  method="POST",
)
print(urllib.request.urlopen(req, timeout=180).read().decode())
```

Use `/lock/acquire` and `/lock/release` for real browser runs when multiple agents or tasks may conflict.
`/lock/release` only releases the concurrency lock and keeps the browser page open by default. Close browser pages explicitly with `POST /session/close`, `POST /browser/close-session`, `POST /tabs/close`, or by passing `{"close_browser": true}` to `/lock/release`.
For OAuth, login, captcha, demos, or debugging, release the lock when the protected work is done but keep the page open until the user has finished inspecting or interacting with it.

## Action Trace Logs

Every `POST /execute` / `POST /call` action, including async jobs started through `POST /execute/start`, writes one structured JSONL record to the daily workspace log directory:

```text
<workspace_root>/logs/<YYYYMMDD>/browser_action_trace.jsonl
```

The path is resolved through `PathManager.get_log_dir()` when available. If BrowserWorker runs without GUI path APIs, it falls back to `MANAI_WORKSPACE_ROOT` / `MANAI_HOME` and then `logs/<YYYYMMDD>/`. Do not hard-code user-specific local paths in skills or actions.

The `/execute` response includes `trace_id` and `trace_path`, and async start/status responses include `job_id` plus `trace_id`, so agents can answer where the action trace was written. The trace records timing, `max_runtime_ms`, `session_id`, `agent_id`, `skill`, `action`, `action_path`, domains, sanitized args, `page_state_before`, `page_state_after`, status, result summary, and error type/code.

Default trace records intentionally do not store full HTML, screenshots, cookies, auth headers, AK, tokens, passwords, or full extracted datasets.

## Debugging Order

1. Check daemon `/ping` and `/plugin/status`.
2. If no extension is connected during a browser task, allow the daemon's on-demand Chrome launch path to run first. If it still does not connect, report that the daemon is running but the browser extension is not connected, then ask the user to load/reload/enable the extension. Do not switch the daemon to CDP mode on your own.
3. Check current URL, title, page state, and page identity.
4. Read matching `page_semantics` and verify whether the intended `semantic_key` exists.
5. Use snapshot to inspect current candidates, handles, semantic hints, timing, partial result, and stability.
6. Run small `browser.evaluate(...)` probes against the current page.
7. Inspect uploaded `trace/interests/script_hints/page_semantics` if the user recorded a flow.
8. Patch semantic evidence, structured targets, selectors, or parsers and rerun the action.
9. If page identity is wrong, patch `page_identity.py` and tests.
10. If data still cannot be found, ask the user to record the exact interaction or manually handle login/captcha through `request_help`.

## Completion Standard

A task is complete when:

- A reusable action script exists.
- The script accepts relevant parameters.
- It returns structured JSON with success/error details.
- It has passed syntax/unit checks.
- Live validation has been run when the task depends on real page rendering.
- Known limitations are explicit in returned fields or the final response.

---
name: userscript-author
description: >
  The FLEET layer for Violentmonkey userscripts — what the portable plugin cannot
  know: how a script reaches this Mac, and why this repo no longer declares or
  gates any. Since 2026-09-14 delivery is PUBLICATION (Greasy/Sleazy Fork, then
  one install click), not a Nix declaration. Use alongside the
  `page-lab:userscript-author` skill when asked to "make <site> do X", "write a
  userscript for <site>", "fix my <site> script", "this site's X annoys me", or
  "can I see my userscript edits live/reflected in the browser" (Violentmonkey
  live-tracking). The authoring METHOD lives in that plugin (published at kattakath/ai);
  this skill owns only the delivery and install reality of this fleet.
---

# Userscript author — the FLEET layer

**Method is not here.** Measuring, routing, diffing, replaying, the code patterns, the probes and
the Greasy Fork rulebook all live in the **`page-lab` plugin**
([`kattakath/ai`](https://github.com/kattakath/ai/tree/main/plugins/page-lab)),
which is deliberately portable — it stops at a lint-clean, proven `.user.js` and knows nothing
about Nix. Invoke it as the `page-lab:userscript-author` skill.

**This skill owns the delivery half** — which, since 2026-09-14, is publication rather than a
Nix declaration.

```
[plugin] wish → shelf → route → measure → diff → write → lint → prove
[here]   → publish to the fork → install once → it self-updates
```

## What this repo stopped doing, and why (2026-09-14, commit 535f1ef)

One commit removed **all three at once**: the `kattakath-userscripts` input, every
`local.ungoogledChromium.userScripts.scripts` entry, and `checks.<system>.userscripts`.
nix-personal dropped its `modules/userscripts.nix`, its own `userscripts` input and **both** of
its gates the same day.

- **Publication beat materialisation on one measured fact.** A fork-installed copy is the only
  one that carries an `@updateURL`, so it updates itself; a file materialised into
  `$XDG_DATA_HOME` never could — every change needed an `activate` plus a manual click. The
  last script out, `google-photos-icon-nav`, is `greasyfork.org/scripts/595764`.
- **The gate was deleted, not re-pointed.** Aiming it at `${self}` would have been a green build
  over an empty directory — strictly worse than no gate, and exactly the failure its own comment
  warned about. See the long-form note that replaced it in `modules/parts/checks.nix`.
- **The rulebook did not move.** It is still the plugin's `scripts/userscript-meta-lint.sh`, now
  running in CI in the repositories that own the scripts. One rulebook, run where the content is.
- **The OPTION stays.** `local.ungoogledChromium.userScripts` in `modules/home/chromium.nix` is
  generic and documented, `enable` still defaults `true`, `scripts` is `{ }`. **Do not describe
  it as removed.**

## Standing preference (thin by design — append, never invent)

| # | Statement | Confidence | Evidence |
|---|---|---|---|
| **UI-1** | Give me **the site's own compact/narrow chrome at full width** — navigation shrinks, content takes the reclaimed space. | **VERIFIED** | the entire purpose of `google-photos-icon-nav`, now `greasyfork.org/scripts/595764` |

- **Correction, load-bearing:** the 80px rail, the hover peek-back, the hidden storage footer and
  the 1px `Collections` divider are **Google's own design at its own breakpoint**, inherited as
  **one package** under UI-1 — **not** four separately stated preferences.
- Any preference **not in that table** is **asked via AskUserQuestion** (click-to-select,
  recommended first), never inferred. A row is **appended only after a shipped script proves it**.
- The plugin's own method rules (degrade-to-stock; never reimplement a state the site already
  renders) are general, and live there rather than here.

## Hard rules (fleet-specific — the plugin carries the rest)

1. **Never a secret.** A published script is world-readable; so was the Nix store copy. There is
   no longer a private lane that changes this — the private userscripts repo and its gate are
   both gone.
2. **A script that must not be public has no path today.** Reviving the Nix lane needs all three
   back together (a pinned input holding the file, one line in `scripts`, the gate restored) —
   **ask the operator**, do not improvise a half of it.
3. If a change here *does* touch `.nix`, follow [git-purity](../../rules/git-purity.md) +
   [pr-title](../../rules/pr-title.md); the index is root [`CLAUDE.md`](../../../CLAUDE.md).
   Authoring and publishing a script touches **no file in this repo at all**.

## Deliver it

- [ ] Lint with the plugin's `scripts/userscript-meta-lint.sh` — the only gate left, and it is
      the same one the deleted check ran.
- [ ] **Publish** per the plugin's `greasyfork.md`: Greasy Fork, or **Sleazy Fork** for an
      adult-adjacent site (one codebase, but a site lands on only one of the two).
- [ ] Install from the fork page, once. `@updateURL` then does the rest — **this is the whole
      reason the fleet stopped materialising files**, so never hand the operator a raw file to
      install when a fork listing is possible.
- [ ] The script's source of truth is its own repo/listing, **not this tree**. The old sync URL
      `raw.githubusercontent.com/kattakath/nix-config/main/userscripts/<kebab>.user.js` is
      **dead** — there is no `userscripts/` directory here.

## Install reality on this Mac

- **Violentmonkey is still sideloaded** (`userScripts.enable` defaults `true` in
  `modules/home/chromium.nix`), so the extension is there even though zero scripts are declared.
- **`~/.local/share/userscripts/` no longer exists.** `xdg.dataFile` is gated on
  `scripts != { }`, so with an empty attrset nothing is materialised and **there is no
  `index.html` to click through** — verified absent on disk 2026-09-14. Installing now means
  navigating to the fork listing.
- One-time per profile, in `chrome://extensions`: **Allow User Scripts** + **Allow access to
  file URLs** (Chrome 138+ refuses to let policy set the first).
- Claude cannot install a script, flip a toggle, or drive Violentmonkey's dialog **unless**
  `chrome-devtools-mcp` is running with `--categoryExtensions` — see the live-tracking loop below,
  which is exactly that exception. **That flag moved out of this repo**: it used to be
  `local.mcpGateway.chromeDevtools.allowExtensions` in `modules/shared/mcp.nix`, which was
  **deleted 2026-10-02** with the MCP gateway. `chrome-devtools` is the `page-lab` plugin's server
  now, so whether the flag is passed is that plugin's `.mcp.json` to decide and **nothing here can
  assert it** — if extension pages are unreachable, check there, not in nix-config.
- **Activation is no longer part of the loop.** Publishing changes nothing in the Nix closure, so
  a userscript no longer needs `activate` at all.

## Live-tracking loop — driving Violentmonkey directly (preferred over the fallback below)

With `chrome-devtools-mcp` started with `--categoryExtensions` (**verified working in attach mode
against this fleet's Chrome 152 on 2026-09-30**, despite upstream's own `--help` claiming
otherwise — that measurement still stands). It was `local.mcpGateway.chromeDevtools.allowExtensions`
in `hosts/macos.nix` until the gateway was deleted 2026-10-02; the flag is now set in the
`page-lab` plugin's `.mcp.json`. With it on, chrome-devtools-mcp can navigate and drive
`chrome-extension://` pages — including Violentmonkey's own install/confirm dialog. This
supersedes the Kapture-injection fallback below for any script being authored against a
**local `file://` copy**; reach for that fallback only when `--categoryExtensions` is off, or the
script has no local file to track (already published, editing live in place).

1. Navigate any page (`new_page`/`navigate_page`, `background: true` is fine) to the script's
   `file://` path. Violentmonkey redirects it to
   `chrome-extension://…/confirm/index.html#<token>`.
2. On that page: click **Track external edits**, then check **Reload tab**. This tab must
   **stay open** — the tracking loop lives in it, not in a background poll or in
   `chrome.storage`. Closing it (or navigating it away) stops detection outright.
3. Get (or create) the tab the script actually targets, then force it **Chrome-active**, not
   merely "selected" by tooling:
   ```js
   const [tab] = await chrome.tabs.query({url: "https://example.com/*"});
   await chrome.tabs.update(tab.id, {active: true});
   ```
   Run this from any extension-context page (the confirm tab itself works). **This is the
   load-bearing, easy-to-miss step.** A tab created with `background: true` is `active: false`
   at Chrome's own tab-model level — a separate axis from OS window focus — and Violentmonkey's
   "Reload tab" only reloads the tab Chrome considers active. Skip this and you get a session
   that correctly detects every edit (`chrome.storage.local['code:<id>']` updates right on
   schedule, visible from any extension page) while the actual browser tab never once reloads —
   which reads exactly like a broken cache and is not one.
4. Edit the file. Detection + auto-reload typically lands within tens of seconds once steps 2–3
   are set up — no `activate`, no browser relaunch, no extension reload needed per edit after
   that.

**Verifying the edit actually landed:** don't only check `document.styleSheets` / `<style>`
tags. A script using **Constructable Stylesheets** (`document.adoptedStyleSheets`) injects CSS
in a way that is invisible to both. Check both surfaces:
```js
[...document.querySelectorAll('style')].some(s => s.textContent.includes(MARKER))
|| [...(document.adoptedStyleSheets||[])].some(s => [...s.cssRules].some(r => r.cssText.includes(MARKER)))
```
Checking only the first gives a false "still stale" reading while the real mechanism already
worked — burned a full session chasing phantom cache/registration bugs before this was caught.

## Live-edit loop — no operator at the keyboard (fallback)

When there is no human to click an installer — an agent-driven session — inject the saved body
straight into a matching Kapture tab. There is no plugin for this; it is one POST, so a wrapper
earned nothing (`plugins/userscript-preview` did exactly this and was retired 2026-09-04):

```bash
python3 - <<'PYEOF'
import json, re, urllib.request, pathlib
raw = pathlib.Path('<path to the .user.js you are editing>').read_text()
body = re.sub(r"//\s*==UserScript==.*?//\s*==/UserScript==", "", raw, flags=re.S).strip()
req = urllib.request.Request("http://127.0.0.1:61822/tab/<tabId>/evaluate",
    data=json.dumps({"code": body, "timeout": 30000}).encode(),
    headers={"Content-Type": "application/json"}, method="POST")
print(urllib.request.urlopen(req, timeout=40).read().decode()[:200])
PYEOF
```

- The file path is **wherever you are authoring it** — a scratch path or the script's own repo.
  It is no longer `userscripts/<kebab>.user.js` in this tree, and the old three-copy
  writable/read-only table died with that directory.
- Tab must have Kapture connected and **Allow JS execution** (`evalAllowed`).
- The IIFE **must** call `window.__nix<Name>Teardown()` first, or each inject stacks another
  observer. A leftover `data-*Init` early-return makes inject a no-op instead — do not add one.
- Injecting over an OLDER installed build that predates its teardown makes the two copies fight
  for last-in-head until the tab pegs, and the POST times out (measured 2026-09-04). Install the
  new version first, or edit against a clean tab.
- Injection dies on reload. Ship by publishing, as above.

## Report format (always end with this)

```markdown
## Userscript report
- **Wish:** (URL + the state asked for)
- **Shelf:** hit-adapted | hit-rejected (why) | empty — (which index/indices were fetched)
- **Measured:** (probes run, `innerWidth` A/B, cross-origin sheet count)
- **Diff verdict:** DOM-DIFFERS | DOM-IDENTICAL | STATE-B-UNREACHABLE
- **Approach:** (attribute set | rules lifted by condition in band X–Y | constructed UI)
- **Selectors shipped:** (each one, with the date measured — or "none")
- **Lint:** plugin `userscript-meta-lint.sh` ✅/❌
- **Published:** Greasy Fork | Sleazy Fork | not yet (why) — with the listing URL
- **Operator action:** install from the listing once; it self-updates thereafter
- **Verdict:** SHIPPED | BLOCKED (why) | ESCALATED (vite-plugin-monkey, in the script's own repo)
```

## Compose with existing automation

```
/userscript <site> <wish>  → this skill + page-lab:userscript-author
/eval                      → only if a .nix was actually touched (authoring touches none)
/hygiene                   → doc/index drift, if a PR here ever lands
```

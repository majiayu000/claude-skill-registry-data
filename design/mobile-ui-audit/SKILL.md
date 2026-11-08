---
name: mobile-ui-audit
description: Audit websites the way a phone visitor would fail on them — iOS zoom traps, sideways overflow, locked scroll, tap targets, tiny text, dead links — on real WebKit and Chromium phone profiles, optionally across every Vercel production alias in one run. Use when you say "the mobile site is broken", "scroll is broken on my phone", "can't get back to the header", "run the UI audit", "test all our sites on mobile", "QA this on a phone", or after any CSS change that touches inputs or layout.
---

# Mobile UI audit

One script, two phone engines, every site. Run it before believing an emulator.

    pip install playwright && playwright install webkit chromium
    python audit.py "https://example.com/" --devices iphone
    VERCEL_TOKEN=... VERCEL_TEAM_ID=... python audit.py --vercel --crawl 4 --json /tmp/audit.json --shots /tmp/shots

Exit 1 on any FAIL. `--links` HTTP-checks the order/book/shop/menu links plus 40 others;
`--hop` also audits the first same-origin order/book/shop/menu page one click deep (a site
takes ~2 min with both, so shard ~10 processes for 150 sites). Cross-origin frame errors
(Cloudflare Turnstile, booking iframes) are not the site's own JS and stay INFO.
`--vercel` reads the team's projects off the API and picks the custom domain or the
shortest `<name>.vercel.app`; team-scoped aliases sit behind Vercel SSO and audit as a
login page with a 200, so the picker skips them.

## The rule this skill exists for

**No text-entry control under 16px on a touch screen.** Mobile Safari scales the page
until a focused `input`, `textarea` or `select` reads 16px and does not scale back on blur.
A 12px field means a 1.33x page, the header off the top-left, and a visitor who says
"scroll is broken." No emulator shows it: headless Chrome, Playwright WebKit and the
iPhone device profiles all auto-zoom nothing, which is why the audit measures the static
property instead of trusting a scrolled page.

Fix shape, by stack:

- Hand-written CSS: `@media (pointer:coarse){ input:not([type=checkbox]):not([type=radio]):not([type=file]),textarea,select{font-size:16px !important} }`. `pointer:coarse` means "a finger" and leaves every desktop size alone. `!important` because small sizes often sit on id selectors.
- A plain `font-size: 15px` on inputs: raise it to 16.
- Tailwind: `text-base`, never `text-sm`, on an input.
- **Never** `maximum-scale=1` in the viewport meta. iOS ignores it for pinch but Chrome/Android honours it, so it kills pinch-zoom for the people who need it. The audit WARNs on it.

Checkboxes, radios and file inputs do not trigger the zoom and are excluded.

## What a row means

| Severity | Finding | Why it is that severity |
|---|---|---|
| FAIL | iOS zoom trap | the visitor loses the page (above) |
| FAIL | sideways overflow, unclipped | iOS does not honour `overflow-x:hidden` on body reliably; the page pans |
| FAIL | document locked, no inner scroller | content below the fold is unreachable |
| FAIL | page error, HTTP >= 400, did not load | nothing to audit |
| FAIL | page renders blank (<40 chars of visible text after load) | the visitor sees nothing |
| FAIL | sideways overflow that **pans** (`panX` > 0 after `scrollTo(400,0)`) | reproduced, not inferred; a leak that does not pan is WARN |
| FAIL | dead link (`--links`): >= 400 on two GETs | 401/403/429/503/999 are `blocked` (a bot wall), never reported dead. **Tap it before believing it**: restaurant menu tabs (`href="991408"`, SpotHopper/BentoBox-style) 404 on GET but JS swaps the tab on click |
| WARN | wrong phone keyboard: an email/phone field declared `type=text` | the letters keyboard comes up for a number |
| WARN | autofill disabled: `autocomplete=off` on a name/email/phone/address/card field | autofill reads `autocomplete`; off kills it |
| WARN | broken image (complete, `naturalWidth` 0) | visible hole on the page |
| WARN | tap target under 24px | WCAG 2.5.8 minimum; Apple asks 44 |
| WARN | text under 12px | a count, not a verdict — some designs run 10-11.5px mono on purpose |
| WARN | fixed/sticky layer covering >= 40% | usually a modal or a hero card; check it dismisses. The 'document locked' FAIL fires on the same pages while a modal is open; tap the close button by hand before calling it broken |
| WARN | header not at y=0 after a scroll round-trip | a sticky or anchor is fighting the scroll |
| WARN | viewport meta caps zoom | see above |
| INFO | scroll model, weight, inner scrollers | context for reading the rest |

The "wide element" check only counts elements no ancestor clips before `body`, so a
960px table inside a `.tscroll{overflow-x:auto}` is not a finding. A naive rect check
flags dozens of such pages.

Single-page apps whose views render client-side: `--crawl` only sees the sitemap. Audit
the real view URLs directly (e.g. `/?view=<id>`). A deliberately locked shell
(`html{overflow:hidden}` with an inner scroller) reports as INFO, not FAIL.

## When the audit says ok and the phone still disagrees

The next tier is a real Mobile Safari: **a headless iOS simulator driven by
`sim_probe.sh`** in this directory. Tap the field, close the keyboard, compare
screenshots. `zoomtest.html` is a control page: a 12px field whose page prints
`visualViewport.scale` (1.33 = trap, 1.00 = clean).

    ./sim_probe.sh "<url>" /tmp/out 201 369   # tap in points

What it takes:
- Xcode from the Mac App Store (~3.7 GB complete) may ship **no Simulator.app**;
  `xcodebuild`, `simctl` and headless rendering all work without it.
- iOS runtime: `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild -downloadPlatform iOS`
  (8 GB). It can end with a "manifest couldn't be opened" error and still register the runtime.
- Taps: `brew trust facebook/fb && brew install idb-companion`, plus `pip install fb-idb`.
  `idb connect <udid>` again after every boot. Coordinates are points; measure a field
  with Playwright WebKit at 402x874 and tap its rect centre. The first `openurl` after a
  boot times out; the second lands.
- The software keyboard appears headless, so the focus zoom runs. A control tap that "did
  nothing" is usually a dead idb companion after a reboot.
- Playwright WebKit cannot stand in for this: it does not auto-zoom. Chrome and Android
  never zoom on focus at all, which is why Android visitors never see the bug.

Other tiers: a real iPhone on USB with Safari's Develop menu; paid real-device clouds.

Interactive poking: the `playwright` MCP (`@playwright/mcp --browser webkit --device
"iPhone 13"`) and the `chrome-devtools` MCP. If the playwright MCP errors that its browser
is missing, run `npx -y @playwright/mcp install-browser webkit`. Use them for poking,
`audit.py` for the sweep, `sim_probe.sh` for the one thing only real iOS shows.

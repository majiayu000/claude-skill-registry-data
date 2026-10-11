---
name: static-file-wiki-layout-verify
description: "Verify and fix layout, readability and syntax highlighting in a build-free static docs site opened over file:// (like D:/AntHill/wiki) — the stale-stylesheet trap that makes a correct CSS edit look broken, duplicate rules that silently shadow the fix, measuring overflow and prose density headlessly instead of by eye, the two-job table wrap rule that stops columns overlapping a sticky rail or splitting keys mid-word, and vendoring highlight.js for offline colour. Use when a plain HTML/CSS/JS guide renders wrong, a wide table overlaps a side panel, code blocks need highlighting without a build step, or pages read as walls of text."
---

# Verifying a build-free static wiki

For a plain HTML/CSS/JS docs site (no bundler, opened by double-clicking `index.html`,
content in `content/*.js` calling a `Wiki.page({...})` renderer).

## 1. Before believing any "it looks broken" report

**The stale stylesheet is the first suspect.** `file://` CSS and JS are cached hard.
A screenshot showing browser-default rendering (raw `<ol>` markers where the CSS sets
`list-style: none`, unstyled panels, missing `::before` badges) means the browser is
painting an old CSS against new JS. Prove it before editing anything:

```js
const tab = await browser.open({ name: "wiki", url: "file:///D:/.../wiki/index.html",
                                 viewport: { width: 1600, height: 980 } });
await tab.evaluate(`(() => { const cs = getComputedStyle(document.querySelector('.flow'));
  return { listStyle: cs.listStyleType, display: cs.display }; })()`);
```

If computed styles match the file, the file is fine — tell the user to hard-refresh
(Ctrl+F5). The headless tab caches too: `page.setCacheEnabled(false)` before `reload`,
or a screenshot identical in byte size to the previous one is your tell.

**Second suspect: a duplicate rule shadowing the fix.** Editing by line range can insert
a new rule instead of replacing the old one, leaving both. The later one wins and the
edit looks ignored. After any CSS edit that "did nothing", check the computed value,
then grep the property:

```
grep -n "overflow-wrap|word-break" wiki/assets/wiki.css
```

## 2. Measure, never eyeball

Walk every page headlessly and get numbers. Overflow and collision:

```js
const rows = [];
for (const href of hashes) {
  await page.evaluate(h => { location.hash = h; }, href);
  await new Promise(r => setTimeout(r, 220));
  rows.push(await page.evaluate(() => {
    const p = document.querySelector(".page");
    const aside = document.querySelector(".aside").getBoundingClientRect();
    return {
      id: location.hash,
      pageOver: Math.round(p.scrollWidth - p.clientWidth),          // must be 0
      collide: Math.round(p.getBoundingClientRect().right - aside.left), // must be < 0
      scrollTables: Array.from(document.querySelectorAll(".grid-wrap"))
        .filter(x => x.scrollWidth - x.clientWidth > 1).length,
    };
  }));
}
```

Repeat at 1280 / 1440 / 1920 — a table that fits at 1920 can still overlap at 1280.

## 3. The two-job table wrap rule

A wide table painting over a sticky right rail is **not** a grid-column problem; the
column already has `min-width: 0`. The table has nothing telling it to stay inside:

```css
.grid-wrap { margin: 14px 0; max-width: 100%; overflow-x: auto; }
```

Then wrapping needs **two different rules**, and using one everywhere fails twice:

- `overflow-wrap: anywhere` on every cell collapses a column's min-content to one
  character — keys split as `Lore:Reposit / oryPath`.
- `overflow-wrap: break-word` on every cell lets one unbreakable value (a connection
  string, a repository path) set the whole table's min width, pushing the far column
  off the page.

Split by job:

```css
table.grid td, table.grid th { overflow-wrap: anywhere; }        /* values, prose */
table.grid td:first-child, table.grid th:first-child { overflow-wrap: normal; } /* the name */
```

Verify keys are not split by counting client rects:

```js
Array.from(document.querySelectorAll("table.grid td:first-child code"))
  .filter(c => c.getClientRects().length > 1).length   // must be 0
```

## 4. Prose density — measure leaves, not wrappers

"Walls of text" is measurable. Count **leaf sentences only**; a `steps` `<li>` wrapper
contains its title plus a code block, so counting every `li` reports 700-character
false positives:

```js
const els = Array.from(document.querySelectorAll(".page p, .page .points > li"));
const ns = els.map(e => e.textContent.trim().length);
// report avg, max, and count over 320
```

Targets that read well: average 130-200, nothing over ~320.

When fanning out editors to fix this, give them the measurement method — subagents that
measure raw source strings instead of rendered text will report "done" with 12 long
blocks still rendering.

**Always diff facts afterwards, mechanically**, not by reading their reports:

```js
const cite = /[A-Za-z0-9_.\/\\-]+\.(?:cs|razor|json|yaml|ps1|toml|md)(?::[0-9,\-]+)?/g;
// compare sets from `git show HEAD:<file>` vs working tree; also count
// `t: "code"` and `rows: [` occurrences before/after
```

## 5. Syntax highlighting with no build step

Never hand-roll one. Vendor highlight.js locally (a CDN link breaks the "opens off a
share" requirement):

```js
const base = "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.11.1/build";
// highlight.min.js  (common bundle)
// languages/powershell.min.js  — PowerShell is NOT in the common bundle
// plus the LICENSE (BSD-3) beside it
```

Load the vendor scripts **before** the engine, highlight at render time (not on a
timer afterwards, which shows a block plain then repaints it):

```js
if (window.hljs && hljs.getLanguage(lang)) {
    source.innerHTML = hljs.highlight(body, { language: lang }).value;
    source.classList.add("hljs");
}
```

Map content-file names to hljs names (`text`→`plaintext`, `jsonc`→`json`, `toml`→`ini`,
`sh`→`bash`). Theme `.hljs-*` against the site's own palette tokens rather than shipping
a stock theme — a stock theme is a second colour scheme fighting the product's.

Verify colour actually applied per page:

```js
blocks.filter(b => b.querySelector("span[class^='hljs-']")).length   // plaintext legitimately 0
```

## 6. Shape beats styling for reference content

A table whose first column is a long verbatim error message is the wrong container: the
thing being looked up wraps three times while the answer sits far right. Render those as
cards — message as the leading line in mono with no chip box, meaning and fix side by
side beneath — and keep the filter, with an explicit empty state when it matches nothing.

Inline `code` chips: border + padding on every noun turns a paragraph into a row of
buttons. Keep a faint tint, no border, `white-space: nowrap` in running prose only
(`p code, li code, dd code, .note code`) — never on `pre code`, which must inherit the
`pre` whitespace, and never on table cells that may hold a connection string.

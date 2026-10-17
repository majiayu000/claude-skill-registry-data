---
name: screen-mockup-html
category: design
description: Use when you draw a screen as HTML mockup documents (one per variant) - the sanitizer-safe recipe, phone and wide frames, the states grid, static control states, and the loopback self-check with screenshots at 375, 768 and 1440 attached to the task
---
# Screen Mockup HTML

## Overview

The HTML documents on the task ARE the design — one per variant, titled `design: <screen> · <letter>` (`design: Invoices — list · A`), so the review page can lay them side by side for the human to choose one. A human reviews each in a sandboxed frame, selects passages and comments on them; developers receive them in their run context as plain text. Nothing in them runs, loads or reacts — so every state is drawn, side by side, as its own static frame, and every decision a reviewer may question is text they can select.

**Core principle:** Draw states, don't simulate them. Lay each frame out by its own class, not by media queries — the review pane is not the device. It is a pan-and-zoom canvas, like Figma: frames sit at their real widths in rows as wide as they need, and the reviewer drags and pinches to move around them — so never put frames in a scrolling box.

## Document anatomy

Keep these ids stable across revisions; review comments and the hand-off cite them.

One document per variant; each holds that variant only, complete.

1. `header#top` — `<h1>` the screen and the variant (`Invoices — list · A — table first`); one meta line: task key, design system version (base and layer), date, content language.
2. `section#notes` — purpose in one sentence; this variant's idea, whom it serves, what it costs, and whether it is the one you recommend (design-variants); the decisions on palette, type and layout and why (avoid-ai-default-looks); tokens or components this design proposes to add; draft copy; any state that does not apply, with the reason; the self-check result.
3. `section#structure` — the ASCII wireframes of this variant at 375 and the wide width in `<pre>`. They survive the text rendition developers get; the pixels do not.
4. `section#variant-a` (`#variant-b` in the `· B` document, …) — `<h2>Variant A — <the idea></h2>`, one line on the trade-off, then a strip with the 375 and the wide default frames.
5. `section#states-a` (…) — the states grid: every state at 375, and at the wide frame the default plus each state whose layout differs there (every-state-designed). Dark theme frames sit in the same grid.
6. `section#controls` — each control the screen uses in default, hover, focus-visible, active, disabled and loading, side by side.

Every frame is a `<figure>` with an id carrying its variant's letter (`a-375-empty`), so a citation names one frame in one document, and a `<figcaption>` (`375 · empty — no invoices yet`). The wide frame is 1440 for web; for a mobile app it is a 768 tablet (`.w768`), plus a landscape phone frame when the screen supports landscape. Draw the platform's own chrome where it shapes the layout — status bar and home indicator safe areas on iOS, the system bars on Android.

## Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>design: Invoices — list · A</title>
<style>
:root{--doc-bg:#F6F7F8;--doc-fg:#1F2328;--doc-muted:#5C6670;--doc-line:#D0D7DE;
--doc-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;--doc-mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root{--doc-bg:#0D1117;--doc-fg:#E6EDF3;--doc-muted:#9198A1;--doc-line:#30363D}}
*{box-sizing:border-box}
body{margin:0;background:var(--doc-bg);color:var(--doc-fg);font:14px/1.55 var(--doc-sans)}
main{padding:24px}
h2{margin:40px 0 8px;font-size:18px}
pre{font:12px/1.35 var(--doc-mono);border:1px solid var(--doc-line);padding:12px;overflow:auto}
.strip{display:flex;gap:32px;align-items:flex-start;width:max-content;padding:8px 0 16px}
figure{margin:0;flex:none}
figcaption{font:12px/1.4 var(--doc-sans);color:var(--doc-muted);margin:0 0 6px}

.ds{--background:#FFFFFF;--foreground:#1C2024;--surface:#F4F6F5;--muted-foreground:#5A6560;--border:#D9DFDC;
--primary:#1F5F4A;--on-primary:#FFFFFF;--destructive:#B42318;--ring:#1F5F4A;
--radius-md:6px;--space-1:4px;--space-2:8px;--space-3:12px;--space-4:16px;--space-6:24px;
--font-sans:"Source Sans 3",-apple-system,"Segoe UI",Roboto,sans-serif;
background:var(--background);color:var(--foreground);font:16px/1.5 var(--font-sans)}
.ds.dark{--background:#111416;--foreground:#E8ECEA;--surface:#1A1F1D;--muted-foreground:#9AA5A0;--border:#2C3431;
--primary:#5FB894;--on-primary:#0B1F17;--ring:#5FB894}

.frame{border:1px solid var(--doc-line);overflow:hidden}
.w375{width:375px;min-height:720px}
.w1440{width:1440px;min-height:900px}
.w768{width:768px;min-height:1024px}
.w375 .layout{display:flex;flex-direction:column;gap:var(--space-4);padding:var(--space-4)}
.w1440 .layout{display:grid;grid-template-columns:240px 1fr;gap:var(--space-6);padding:var(--space-6)}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:var(--space-2);min-height:44px;padding:0 var(--space-4);border-radius:var(--radius-md);font-weight:600}
.btn-primary{background:var(--primary);color:var(--on-primary)}
.btn-primary.is-hover{background:color-mix(in srgb,var(--primary) 88%,#000)}
.btn-primary.is-active{background:color-mix(in srgb,var(--primary) 78%,#000)}
.is-focus{outline:2px solid var(--ring);outline-offset:2px}
.is-disabled{opacity:.5}
.label{font-weight:600;font-size:14px}
.input{display:flex;align-items:center;min-height:44px;padding:0 var(--space-3);border:1px solid var(--border);border-radius:var(--radius-md);background:var(--background)}
.input.is-invalid{border-color:var(--destructive)}
.placeholder{color:var(--muted-foreground)}
.error-text{color:var(--destructive);font-size:14px}
.skeleton{display:block;background:var(--surface);border-radius:var(--radius-md);height:16px}
.pad{padding:var(--space-4)}
</style>
</head>
<body><main>
<header id="top">
  <h1>Invoices — list · A — table first</h1>
  <p>D-14 · design system Harbor base v3 + web layer v1 · 2026-10-08 · content language: English</p>
</header>
<section id="notes"><h2>Notes</h2><ul><li>Purpose: find an invoice and see what is overdue at a glance.</li><li>Variant A — table first, recommended: finance staff scan 50+ invoices a day.</li></ul></section>
<section id="structure"><h2>Structure</h2>
<pre>375
[ Invoices            (New invoice) ]
[ Search: customer or number        ]
[ row: customer · number   amount   ]
[      due date            status   ]</pre></section>
<section id="variant-a"><h2>Variant A — table first</h2><p>Optimises scanning many invoices; summary moves below the table.</p>
<div class="strip">
  <figure id="a-375-default"><figcaption>375 · default</figcaption>
    <div class="frame w375 ds"><div class="layout">
      <div><span class="label">Search invoices</span>
        <span class="input"><span class="placeholder">Customer or invoice number</span></span></div>
      <span class="btn btn-primary">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
        New invoice</span>
    </div></div>
  </figure>
  <figure id="a-1440-default"><figcaption>1440 · default</figcaption>
    <div class="frame w1440 ds"><div class="layout"><nav>…</nav><div>…</div></div></div>
  </figure>
</div></section>
<section id="states-a"><h2>Variant A — states</h2>
<div class="strip">
  <figure id="a-375-loading"><figcaption>375 · loading</figcaption>
    <div class="frame w375 ds"><div class="layout"><span class="skeleton"></span><span class="skeleton"></span></div></div></figure>
  <figure id="a-375-error"><figcaption>375 · error — invoices could not load</figcaption>
    <div class="frame w375 ds"><div class="layout"><p>Invoices couldn't load. Check your connection and try again.</p><span class="btn btn-primary">Retry</span></div></div></figure>
  <figure id="a-375-dark"><figcaption>375 · dark · default</figcaption>
    <div class="frame w375 ds dark"><div class="layout">…</div></div></figure>
</div></section>
<section id="controls"><h2>Controls</h2>
<div class="strip">
  <figure><figcaption>default</figcaption><div class="ds pad"><span class="btn btn-primary">New invoice</span></div></figure>
  <figure><figcaption>hover</figcaption><div class="ds pad"><span class="btn btn-primary is-hover">New invoice</span></div></figure>
  <figure><figcaption>focus-visible</figcaption><div class="ds pad"><span class="btn btn-primary is-focus">New invoice</span></div></figure>
  <figure><figcaption>active</figcaption><div class="ds pad"><span class="btn btn-primary is-active">New invoice</span></div></figure>
  <figure><figcaption>disabled</figcaption><div class="ds pad"><span class="btn btn-primary is-disabled">New invoice</span></div></figure>
  <figure><figcaption>field · invalid</figcaption><div class="ds pad"><span class="label">Customer email</span>
    <span class="input is-invalid">dana.ortiz@</span><span class="error-text">Enter an email address like name@company.com</span></div></figure>
</div></section>
</main></body></html>
```

The `:root` block styles the review page itself — neutral, not the product. The `.ds` block is the design system: every token you use, as a CSS variable, light on `.ds` and dark on `.ds.dark` — one place per document, identical in every variant's document, so a token change in review is one edit in each.

Every `<h2>` is a page: the review lists them like Figma's pages, jumps to one, and lines two variants up page by page by heading. So one `<h2>` per section, and the same state carries the same heading words in every variant document (`Variant A — states` and `Variant B — states`; `Empty state`, not `B: nothing here yet`) — only the variant's own name may differ.

A strip runs as wide as its frames (`width:max-content`), wider than the page — that is the point. No `overflow:auto`/`scroll` on a strip, a section or `main`, and no `overflow-x:hidden` on `body`: a scrolling strip shows one frame and a scrollbar, and a hidden one cuts the wide frames off. The canvas opens what it can, but the document should not depend on it.

## Drawing without form controls

| You need | Draw it as |
|---|---|
| button | `span.btn` + `.is-hover` / `.is-focus` / `.is-active` / `.is-disabled` / `.is-loading` |
| text field | a label above as text, `span.input` holding the value or a `span.placeholder` |
| checkbox, radio, switch | inline SVG box / circle / track next to its label text |
| select, combobox | `span.input` with the value and an inline SVG chevron |
| link | `a` with no `href`, or `span.link` |
| icon | inline SVG, path data copied from the icon library the repository already uses, sized by token |
| image | the product's own asset as `data:image/…` when small; otherwise an inline SVG placeholder with the image's purpose written in it |
| menu, dialog, tooltip, toast | its own frame showing it open, over the screen it belongs to |

Fonts: a system font stack by default, with the real face named first in `--font-sans` and in the notes. Embed the real face only when the repository ships it as a file: subset it and inline it as `@font-face{src:url(data:font/woff2;base64,…)}` — the viewer loads fonts from `data:` and from nowhere else. A Google Fonts `<link>` is dropped.

## Size

Under 300 KB per document; the hard limit is 1 MB. Repeated markup per state is fine; a large base64 image is not. Captions on every frame keep the text rendition readable for the developers who only get the text.

## Self-check

Write, serve, look, stop — all outside the repository, every variant's document in one pass:

1. `mkdir -p /tmp/tt-<task key>/design`
2. Write each file with `run_terminal`: `cat > /tmp/tt-<task key>/design/<slug>-a.html <<'TT_HTML'` … `TT_HTML`. The quoted delimiter passes `$`, backticks and quotes through untouched; a long document goes in parts with `cat >>`.
3. Sanitizer check: `grep -nE '<(script|button|input|select|textarea|form|link|iframe)\b| on[a-z]+=' /tmp/tt-<task key>/design/*.html` — expect no output.
4. Serve it on loopback in the background and read the port: `nohup python3 -u -m http.server 0 --bind 127.0.0.1 --directory /tmp/tt-<task key>/design > /tmp/tt-<task key>/serve.log 2>&1 & echo $! > /tmp/tt-<task key>/serve.pid; sleep 1; cat /tmp/tt-<task key>/serve.log` → `Serving HTTP on 127.0.0.1 port <port>` (`python` instead of `python3` on Windows).
5. For each document, `browser_navigate` to `http://127.0.0.1:<port>/<slug>-a.html`. The response names the page's title — if it is not your document's, nothing after this is about your design.
6. For each width — `browser_set_viewport` `{device: "desktop"}` (1440), `{device: "tablet"}` (768), `{device: "mobile", width: 375}` — then `browser_screenshot` with `full_page: true`, NO `width`, `attach_to_task: true` and `title: "<slug>-<letter>-<width>"` (`invoices-list-A-375`): the shot is saved on the task, where the human sees it next to the documents. A re-check after a fix re-takes the changed widths with `-r2` on the title (`invoices-list-A-375-r2`), so the final shot is the one that says so.
7. Read every screenshot: each frame rendered with its caption; nothing spills out of its frame; the states are distinct; dark frames are dark; text is legible; icons are drawn, not blank. At 768 and 375 the document still reads — notes wrap, strips scroll sideways. The viewport report naming the 1440 frame as overflowing is the strip scrolling, expected; any other overflow is a finding. `browser_read_dom` with `contains: "<a caption>"` settles whether an ambiguous frame is there.
8. Stop the server: `kill "$(cat /tmp/tt-<task key>/serve.pid)"` — never by name (rule stop-what-you-started).

Collect every finding at all three widths, fix them in one pass, re-check once — two rounds at most. Write what you checked into `#notes` and the summary comment, naming the attached shots by title. If the browser tools are unavailable or fail to open the page, say exactly that ("self-check not run: <reason>") — never describe a look you did not take.

## Common Mistakes

- `@media` queries to switch the phone and desktop layouts — the review pane's width decides, not the frame's. Key the layout to `.w375` / `.w1440`.
- `:hover` styles — nobody can hover a sanitized static page. Draw `.is-hover` as its own frame.
- A `<button>` or `<input>` — dropped on save, the frame renders empty.
- Hard-coded hex in a component rule instead of `var(--token)`.
- Captions missing, so a reviewer cannot say which state a comment is about.

## Red Flags

- A frame that only exists at 1440.
- A document whose loading, empty or error frames are blank rectangles.
- A self-check claimed without an attached `browser_screenshot` of each document at each of the three widths.
- Two variants in one document.

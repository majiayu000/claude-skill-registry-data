---
name: explain-with-html
description: |
  Produces a rich, self-contained dark-theme HTML explainer for any codebase — covering
  architecture layers AND detailed data flows with real file paths, function names, and
  line numbers. Use whenever the user asks to explain code architecture, document a flow,
  or asks "how does X work" about their codebase. Invoke proactively on:
  "explain [flow / architecture / how this works]", "create a visual doc / diagram",
  "document the [X] pipeline", "show me how [feature] works end-to-end",
  "make an HTML explainer for [X]", or any request to understand a codebase visually.
  Always researches real code before writing — do NOT invoke without reading relevant files first.
user-invocable: true
argument-hint: "[topic, flow name, or 'this' to explain current context]"
---

# explain-with-html

Produces a self-contained HTML explainer artifact. Two tiers: (1) high-level
architecture — which layers exist and how they relate, and (2) deep-dive flows —
the exact function call chain, arguments, data transformations, and `file:line`
references for every meaningful step.

The document's value is entirely in its accuracy. Read the code first.

---

## Phase 1 — Research

Before writing one line of HTML, understand the code.

**What to read:**
- `CLAUDE.md`, `README.md`, `AGENTS.md`, or any top-level docs — absorb the project's own vocabulary first
- The entry points relevant to the user's question
- Follow the call chain from trigger to output: read the actual functions, not just file names
- Note real `file:line` references for every function you'll cite

**What to capture:**
- **Layer structure**: what are the logical tiers? (UI, pure core, API client, server, execution layer, cache, etc.)
- **Per flow**: exact sequence of function calls, what each one receives and returns, any side effects (writes a file, spawns a thread, calls FFmpeg, sends HTTP, etc.)
- **Non-obvious design decisions** worth calling out: why is something immutable? what's the cache key? what guards against a race?

**Depth calibration:**
- "Explain the whole architecture" → broad survey of all layers, one section per major flow
- "Explain how X works" → go deep on one flow with full argument detail
- "Explain X and Y" → two detailed flows plus any shared infrastructure they both use

---

## Phase 2 — Design

### Color system

Assign one accent color per logical layer. Use these colors **consistently** — every time a layer appears (arch diagram, flow steps, reference table) it gets its color.

Suggested defaults (reassign based on what fits the codebase):
```
sky    #58b6f8  → UI / presentation / frontend
teal   #42c8a8  → pure logic / domain / immutable core
amber  #f0a44d  → API client / config / adapters
violet #9d8eff  → server / infrastructure / persistence
rose   #f06a6a  → execution / render / heavy ops / FFmpeg / build
green  #5ec47a  → caching / optimization (spare)
```

Use fewer colors if the codebase has fewer meaningful layers — don't force a color just to use them all.

### Base palette (use verbatim)
```
--bg        #0c1018   page background
--surface   #131a24   nav, elevated surfaces, code block bg
--card      #1a2232   layer cards, flow containers
--card-2    #1f2a3c   nested chips, inline code bg
--border    #253044   primary borders
--border-2  #2e3d56   secondary borders, chip borders
--text      #d8e4f0   primary text
--text-2    #8fa3bb   secondary / descriptions
--text-3    #536478   muted — file paths, line numbers, comments
```

---

## Phase 3 — Build

### Page structure

Every artifact has:
1. **Sticky left nav** (220px) with scroll-spy JS
2. **Hero** — title + description + layer pills
3. **Architecture layers section** — stacked cards
4. **One section per flow** — numbered steps
5. **Function reference table** at the end

Include a `<section id="...">` for every section; the nav links to them.

---

### Component: Architecture stack

One card per layer, connected by `arch-arrow` dividers:

```html
<div class="arch-stack">
  <div class="arch-layer">
    <div class="arch-layer-head">
      <span class="layer-tag lt-ui">UI</span>
      <span class="layer-name">React Studio — presentation &amp; pointer math</span>
      <span class="layer-path">web/src/studio/</span>
    </div>
    <div class="arch-layer-body">
      <span class="module-chip hi-sky">Studio.jsx</span>
      <span class="module-chip">StudioTimeline.jsx</span>
    </div>
  </div>
  <div class="arch-arrow">calls pure mutators on every edit →</div>
  <!-- next layer ... -->
</div>
```

`layer-tag` classes: `lt-ui` `lt-core` `lt-api` `lt-server` `lt-render` `lt-green`
`module-chip` highlight classes: `hi-sky` `hi-teal` `hi-amber` (or just `hi`) `hi-violet` `hi-rose` `hi-green`

---

### Component: Flow steps

Each step has a number, a `file:line` reference, the function name colored by its layer, a description, and an optional argument block:

```html
<div class="flow-wrap">
  <div class="flow-steps">
    <div class="flow-step">
      <div class="step-num">1</div>
      <div class="step-body">
        <div class="step-where">Studio.jsx :218</div>
        <div class="step-fn fn-color-sky">render()</div>
        <div class="step-desc">
          Saves the doc first, then calls <code>api.startRender()</code>
          and enters a 500ms poll loop.
        </div>
        <div class="step-args"><span class="k">const</span> { <span class="v">job_id</span> } = <span class="k">await</span> api.<span class="v">startRender</span>(projectId)</div>
      </div>
    </div>
  </div>
</div>
```

`fn-color-*` classes: `fn-color-sky` `fn-color-teal` `fn-color-amber` `fn-color-violet` `fn-color-rose` `fn-color-green`

**The `step-args` block MUST use `white-space: pre`** (the CSS below already does this). Use span classes `.k` (keyword/violet), `.v` (value/teal), `.s` (string/amber), `.c` (comment/muted).

---

### Component: Code block (JSON / multi-line code)

```html
<div class="code-block">
  <div class="cb-file">path/to/file.json</div>
<span class="cb-kw">{</span>
  <span class="cb-key">"version"</span>: <span class="cb-str">"1.0"</span>,   <span class="cb-cmt">// comment here</span>
  <span class="cb-key">"count"</span>: <span class="cb-num">42</span>
<span class="cb-kw">}</span>
</div>
```

**Critical:** `white-space: pre` is set on `.code-block` in the CSS below. Indentation is preserved because the span content is placed at the correct column in the source HTML — do NOT wrap spans in extra divs that would break the whitespace.

---

### Component: Pipeline (horizontal stages)

For sequential multi-stage processes:

```html
<div class="pipeline">
  <div class="pipe-stage">
    <div class="pipe-num">01</div>
    <div class="pipe-name">Stage Name</div>
    <div class="pipe-fn">functionName()</div>
    <div class="pipe-desc">One sentence on what this stage does.</div>
  </div>
  <!-- more stages ... -->
</div>
```

---

### Component: Note boxes

```html
<div class="note">teal — important invariants, design reasoning</div>
<div class="note warn">amber — gotchas, caveats, known limitations</div>
<div class="note rose">red — sharp edges, easy mistakes, performance traps</div>
```

---

### Component: Branch comparison (two-column)

```html
<div class="branch-wrap">
  <div class="branch-card">
    <div class="branch-label">Path A label</div>
    <h4 class="fn-color-amber">functionName()</h4>
    <p>When and why this path is used.</p>
  </div>
  <div class="branch-card">…</div>
</div>
```

---

### Function reference table

Last section, always present:

```html
<table class="ref-table">
  <thead><tr><th>Function</th><th>File</th><th class="line">Line</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr><td>functionName()</td><td><span class="fpath">path/to/file.py</span></td><td class="line">142</td><td>One-sentence purpose.</td></tr>
  </tbody>
</table>
```

---

## Phase 4 — Deliver

Publish with the `Artifact` tool:
- **`favicon`**: subject-matching emoji (`🎬` video · `🔐` auth · `🗄️` data · `⚙️` build · `🌐` web · `🔄` sync · `💾` storage)
- **`label`**: short kebab-case description of this version (e.g. `render-pipeline-v1`)
- The file must be fully self-contained — no CDN links, no external fonts, no remote images
- Wide content (tables, code blocks, pipelines) must sit in `overflow-x: auto` containers

---

## Full CSS (paste verbatim into every artifact)

```css
:root{
  --bg:#0c1018;--surface:#131a24;--card:#1a2232;--card-2:#1f2a3c;
  --border:#253044;--border-2:#2e3d56;
  --amber:#f0a44d;--teal:#42c8a8;--rose:#f06a6a;--violet:#9d8eff;--sky:#58b6f8;--green:#5ec47a;
  --text:#d8e4f0;--text-2:#8fa3bb;--text-3:#536478;
  --mono:'SF Mono','Fira Code','JetBrains Mono','Cascadia Code',monospace;
  --sans:-apple-system,'Inter','Segoe UI',system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:var(--sans);font-size:14px;line-height:1.6;display:flex}
nav{position:sticky;top:0;height:100vh;width:220px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);padding:28px 0;overflow-y:auto;display:flex;flex-direction:column;gap:2px}
.nav-header{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--text-3);padding:0 20px 12px}
nav a{display:block;padding:6px 20px;color:var(--text-2);text-decoration:none;font-size:12.5px;border-left:2px solid transparent;transition:color .15s,border-color .15s}
nav a:hover,nav a.active{color:var(--amber);border-left-color:var(--amber);background:rgba(240,164,77,.05)}
.nav-section{margin-top:20px}
.nav-sub{padding-left:30px!important;font-size:11.5px}
main{flex:1;min-width:0;padding:48px 60px;max-width:1100px}
.hero{margin-bottom:64px}
.hero h1{font-family:var(--mono);font-size:26px;font-weight:600;color:var(--amber);letter-spacing:-.02em;margin-bottom:10px}
.hero p{color:var(--text-2);max-width:680px;line-height:1.75}
.pill-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.pill{font-family:var(--mono);font-size:11px;padding:3px 10px;border-radius:4px;border:1px solid}
.pill-amber{color:var(--amber);border-color:rgba(240,164,77,.3);background:rgba(240,164,77,.06)}
.pill-teal{color:var(--teal);border-color:rgba(66,200,168,.3);background:rgba(66,200,168,.06)}
.pill-rose{color:var(--rose);border-color:rgba(240,106,106,.3);background:rgba(240,106,106,.06)}
.pill-violet{color:var(--violet);border-color:rgba(157,142,255,.3);background:rgba(157,142,255,.06)}
.pill-sky{color:var(--sky);border-color:rgba(88,182,248,.3);background:rgba(88,182,248,.06)}
.pill-green{color:var(--green);border-color:rgba(94,196,122,.3);background:rgba(94,196,122,.06)}
section{margin-bottom:80px}
.section-label{font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--text-3);margin-bottom:8px}
h2{font-size:20px;font-weight:600;color:var(--text);margin-bottom:6px;letter-spacing:-.01em}
h3{font-size:14px;font-weight:600;color:var(--amber);margin-bottom:14px;font-family:var(--mono)}
.lead{color:var(--text-2);max-width:720px;margin-bottom:32px;line-height:1.75}
hr.divider{border:none;border-top:1px solid var(--border);margin:48px 0}
.arch-stack{display:flex;flex-direction:column;gap:0;max-width:860px}
.arch-layer{border:1px solid var(--border-2);border-radius:8px;overflow:hidden;background:var(--card)}
.arch-layer+.arch-layer{margin-top:-1px;border-top:none;border-radius:0}
.arch-layer:first-child{border-radius:8px 8px 0 0}
.arch-layer:last-child{border-radius:0 0 8px 8px}
.arch-layer-head{display:flex;align-items:center;gap:12px;padding:10px 18px 10px 14px;border-bottom:1px solid var(--border)}
.layer-tag{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:2px 8px;border-radius:3px;flex-shrink:0}
.lt-ui{background:rgba(88,182,248,.12);color:var(--sky)}
.lt-core{background:rgba(66,200,168,.12);color:var(--teal)}
.lt-api{background:rgba(240,164,77,.12);color:var(--amber)}
.lt-server{background:rgba(157,142,255,.12);color:var(--violet)}
.lt-render{background:rgba(240,106,106,.12);color:var(--rose)}
.lt-green{background:rgba(94,196,122,.12);color:var(--green)}
.layer-name{font-size:13px;font-weight:600;color:var(--text)}
.layer-path{font-family:var(--mono);font-size:11px;color:var(--text-3);margin-left:auto}
.arch-layer-body{padding:12px 18px 14px;display:flex;flex-wrap:wrap;gap:8px}
.module-chip{font-family:var(--mono);font-size:11.5px;padding:4px 10px;border-radius:4px;background:var(--card-2);border:1px solid var(--border-2);color:var(--text-2)}
.module-chip.hi,.module-chip.hi-amber{color:var(--amber);border-color:rgba(240,164,77,.3);background:rgba(240,164,77,.06)}
.module-chip.hi-teal{color:var(--teal);border-color:rgba(66,200,168,.3);background:rgba(66,200,168,.06)}
.module-chip.hi-rose{color:var(--rose);border-color:rgba(240,106,106,.3);background:rgba(240,106,106,.06)}
.module-chip.hi-violet{color:var(--violet);border-color:rgba(157,142,255,.3);background:rgba(157,142,255,.06)}
.module-chip.hi-sky{color:var(--sky);border-color:rgba(88,182,248,.3);background:rgba(88,182,248,.06)}
.module-chip.hi-green{color:var(--green);border-color:rgba(94,196,122,.3);background:rgba(94,196,122,.06)}
.arch-arrow{display:flex;align-items:center;gap:10px;padding:6px 18px;background:var(--surface);border-left:1px solid var(--border-2);border-right:1px solid var(--border-2);color:var(--text-3);font-family:var(--mono);font-size:11px}
.arch-arrow::before{content:'↓';font-size:14px;color:var(--border-2)}
.flow-wrap{max-width:860px}
.flow-steps{display:flex;flex-direction:column;gap:0}
.flow-step{display:flex;gap:16px;padding:14px 0;border-bottom:1px solid var(--border);align-items:flex-start}
.flow-step:last-child{border-bottom:none}
.step-num{flex-shrink:0;width:24px;height:24px;border-radius:50%;background:var(--card-2);border:1px solid var(--border-2);display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:10px;color:var(--text-3);margin-top:2px}
.step-body{flex:1;min-width:0}
.step-where{font-family:var(--mono);font-size:10px;color:var(--text-3);margin-bottom:4px;letter-spacing:.04em}
.step-fn{font-family:var(--mono);font-size:13px;font-weight:600;margin-bottom:6px}
.step-desc{font-size:12.5px;color:var(--text-2);line-height:1.65}
.step-args{margin-top:8px;font-family:var(--mono);font-size:11px;background:var(--surface);border:1px solid var(--border);border-radius:5px;padding:8px 12px;color:var(--text-2);line-height:1.8;overflow-x:auto;white-space:pre}
.step-args .k{color:var(--violet)} .step-args .v{color:var(--teal)} .step-args .s{color:var(--amber)} .step-args .c{color:var(--text-3)}
.fn-color-amber{color:var(--amber)} .fn-color-teal{color:var(--teal)} .fn-color-rose{color:var(--rose)}
.fn-color-violet{color:var(--violet)} .fn-color-sky{color:var(--sky)} .fn-color-green{color:var(--green)}
.branch-wrap{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:20px 0;max-width:860px}
.branch-card{background:var(--card);border:1px solid var(--border-2);border-radius:8px;padding:16px}
.branch-label{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text-3);margin-bottom:8px}
.branch-card h4{font-family:var(--mono);font-size:12px;font-weight:600;margin-bottom:8px}
.branch-card p{font-size:12px;color:var(--text-2);line-height:1.65}
code{font-family:var(--mono);font-size:11.5px;background:var(--card-2);border:1px solid var(--border);padding:1px 5px;border-radius:3px;color:var(--amber)}
.code-block{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 16px;font-family:var(--mono);font-size:11.5px;line-height:1.75;overflow-x:auto;color:var(--text-2);margin:12px 0;white-space:pre}
.cb-file{font-size:10px;color:var(--text-3);letter-spacing:.04em;margin-bottom:8px;padding-bottom:8px;border-bottom:1px solid var(--border);white-space:normal}
.cb-fn{color:var(--sky)} .cb-kw{color:var(--violet)} .cb-str{color:var(--teal)}
.cb-num{color:var(--amber)} .cb-cmt{color:var(--text-3);font-style:italic} .cb-key{color:var(--amber)}
.fpath{font-family:var(--mono);font-size:11px;color:var(--text-3);background:var(--surface);padding:2px 8px;border-radius:3px;border:1px solid var(--border)}
.ref-table{width:100%;border-collapse:collapse;max-width:860px}
.ref-table th{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text-3);padding:8px 14px;border-bottom:1px solid var(--border);text-align:left}
.ref-table td{padding:9px 14px;border-bottom:1px solid var(--border);font-size:12.5px;vertical-align:top;color:var(--text-2)}
.ref-table tr:last-child td{border-bottom:none}
.ref-table td:first-child{font-family:var(--mono);font-size:11.5px;color:var(--amber);white-space:nowrap}
.ref-table td.line{color:var(--text-3);font-family:var(--mono);font-size:11px}
.note{border-left:3px solid var(--teal);background:rgba(66,200,168,.06);padding:12px 16px;border-radius:0 6px 6px 0;margin:16px 0;max-width:860px;font-size:12.5px;color:var(--text-2);line-height:1.7}
.note.warn{border-color:var(--amber);background:rgba(240,164,77,.06)}
.note.rose{border-color:var(--rose);background:rgba(240,106,106,.06)}
.note strong{color:var(--text)}
.pipeline{display:flex;align-items:stretch;gap:0;max-width:860px;overflow-x:auto;border:1px solid var(--border-2);border-radius:8px;background:var(--card)}
.pipe-stage{flex:1;min-width:120px;padding:14px;display:flex;flex-direction:column;gap:6px;border-right:1px solid var(--border);position:relative}
.pipe-stage:last-child{border-right:none}
.pipe-stage:not(:last-child)::after{content:'→';position:absolute;right:-11px;top:50%;transform:translateY(-50%);color:var(--border-2);font-size:16px;z-index:1}
.pipe-num{font-family:var(--mono);font-size:9px;color:var(--text-3);font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.pipe-name{font-size:12px;font-weight:600;color:var(--text)}
.pipe-fn{font-family:var(--mono);font-size:10px;color:var(--amber);margin-top:2px}
.pipe-desc{font-size:11px;color:var(--text-3);line-height:1.55;margin-top:4px}
@media(max-width:900px){nav{display:none}main{padding:32px 24px}}
```

---

## Scroll-spy JS (paste verbatim at end of every artifact)

```html
<script>
const links = document.querySelectorAll('nav a[href^="#"]')
const sections = [...links].map(l => document.querySelector(l.getAttribute('href'))).filter(Boolean)
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      links.forEach(l => l.classList.remove('active'))
      const a = document.querySelector(`nav a[href="#${e.target.id}"]`)
      if (a) a.classList.add('active')
    }
  })
}, { rootMargin: '-20% 0px -70% 0px' })
sections.forEach(s => obs.observe(s))
</script>
```

---

## Quality checklist

Before publishing:
- Every function in a flow step has a **real** `file:line` reference — never invented line numbers; omit the number rather than guess
- Code blocks use `white-space: pre` (included in the CSS) — indentation is placed in the HTML source, not via CSS padding
- Layer colors are **consistent** — same layer, same color, everywhere
- Nav anchor `href="#id"` values match `section id="id"` attributes exactly
- No external resources (no CDN, no remote fonts, no remote images)
- The page body does not scroll horizontally — wide content is in `overflow-x: auto` containers

## Pitfalls

**Skip research → worthless output.** The whole value is specificity: real file paths, real function names, real line numbers, real data structures. Generic HTML with plausible-sounding names is noise.

**`white-space: pre` is required on `.code-block`.** It's in the CSS above. Don't override it. Indentation in the HTML source IS the indentation in the rendered block.

**Don't compress unrelated flows into one section.** If the user asked about multiple things, each gets its own section with its own title, its own numbered steps, and its own color context.

**`step-args` is for the KEY DATA being passed** — the dict/object/arguments that matter for understanding. Don't paste entire functions; paste the 3–6 lines that show what's being handed off and why.

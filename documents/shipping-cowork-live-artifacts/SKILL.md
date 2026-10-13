---
name: shipping-cowork-live-artifacts
description: >
  Use whenever the user says "make this a live artifact", "make my [thing] a
  live artifact", "add file upload to my artifact", "add a zip import suite",
  "let me upload PDFs/docx/spreadsheets to this" — even if "live artifact"
  isn't said and an HTML file is just attached with a ship/persist instruction.
  Also triggers on: add PDF/DOCX/XLSX parsing to an artifact, batch zip import,
  keep the artifact self-contained (no CDN), smoke-test an artifact before
  shipping, headless Playwright check on an HTML artifact. Not for scaffolding
  a new React/shadcn artifact from scratch (use web-artifacts-builder) or
  FlashFusion dashboards (use building-flashfusion-live-artifacts).
metadata:
  version: 1.0.0
---

# Shipping Cowork Live Artifacts

## TL;DR

Persist a self-contained HTML file as a Cowork live artifact via
`SendUserFile` → `create_artifact` (first time) / `update_artifact` (after
that). If the file assumes claude.ai-artifact-only browser APIs
(`window.storage`, unauthenticated `fetch` to `api.anthropic.com`), flag that
assumption explicitly — it is unverified in the Cowork runtime. When asked to
add real document parsing (PDF/DOCX/XLSX/ZIP), inline the parser libraries at
build time via npm + direct file splicing rather than pasting megabytes of
minified code through your own context, and smoke-test the result headlessly
with Playwright and generated fixtures before shipping.

---

## Decision Tree

```
Does the artifact already exist as a file (uploaded or previously built)?
  ├─ Yes → read it fully first (Read tool). Note any window.storage / raw
  │        fetch("https://api.anthropic.com/...") calls — flag them (see
  │        "The Unverified Runtime Assumption" below), don't silently assume
  │        they work.
  └─ No, building from scratch with React/shadcn/routing → use
       web-artifacts-builder instead. This skill is for persisting/extending
       an existing self-contained single-file artifact.

Is this the first time this artifact is being persisted?
  ├─ Yes → SendUserFile → mcp__remote-devices__create_artifact (id, file_uuid,
  │        description)
  └─ No, it already exists as a Cowork artifact → SendUserFile → 
       mcp__remote-devices__update_artifact (id, file_uuid, update_summary)
       — list_artifacts first if you don't already know the id.

Does the request add new capability (parsing, uploads, new panels)?
  ├─ Small/CSS/markup/logic change → Edit tool, str_replace, targeted diffs
  └─ Needs a real parser library (PDF, DOCX, XLSX, ZIP, etc.)
       └─ See "Adding Real Parsers Without Breaking Self-Containment" below

Before delivering:
  └─ Run the headless Playwright smoke test (see below) with generated
     fixtures. Report exactly what was verified and what wasn't — don't
     imply full coverage from a partial test.
```

---

## Usage Examples

**User: "make this a live artifact"** (with an HTML file attached)
1. Read the file fully. Note any assumptions it makes about its runtime
   (storage API, unauthenticated fetch to an LLM endpoint).
2. Copy it into the workspace, `SendUserFile`, then `create_artifact` with a
   kebab-case id and a description of what the tool does.
3. Tell the user what shipped, and flag any runtime assumption you couldn't
   verify — don't claim it works if you didn't test it.
→ Outcome: artifact persisted to the desktop sidebar, unverified assumptions
  stated plainly instead of silently hoped to work.

**User: "I need you to include upload feature where I can upload pdfs, docx,
markdown, .txt, spreadsheets, csv, .jsx, .json... Include a separate suite
where I can upload a zip from device and."** (message cuts off)
1. Don't guess the missing half of a cut-off instruction if it changes the
   architecture (here: what happens after unzip). If the clarifying-question
   tool is failing, don't infinite-retry it — state the default you're taking
   in plain text and proceed (see Gotcha #6).
2. Route text formats (txt/md/json/csv/js/etc.) through `file.text()` /
   `TextDecoder` directly — zero new dependencies.
3. Route binary formats through inlined parser libraries (see below).
4. Build the zip suite to cover both plausible readings of the cut-off
   instruction (survey separately vs. combined) as two buttons, rather than
   picking one and hoping.
→ Outcome: full multi-format upload plus a batch-zip suite shipped in one
  pass, with the ambiguous half of the spec resolved by building both options
  instead of blocking on an unanswered question.

**User: "can u make my punch list thing a live artifact and let me upload
docs too"**
Same flow as above, casually phrased — trigger on it exactly the same way.
→ Outcome: no separate handling needed for casual phrasing; same two flows
  apply.

---

## Eval Scenarios

```
Should trigger:
1. "make this a live artifact" (HTML file attached)
2. "can u turn my [x] into a live artifact real quick"
3. "add PDF and zip upload to my artifact"
4. "keep it self-contained, no CDN — inline whatever library you need"
5. "smoke-test this artifact before you send it back"

Should NOT trigger:
1. "build me a dashboard artifact from scratch with shadcn" (→ web-artifacts-builder —
   scaffolding new, not persisting/extending an existing self-contained file)
2. "update the FlashFusion control center panel" (→ building-flashfusion-live-artifacts —
   brand-specific artifact, its own skill)
3. "review this PR for bugs" (→ auditing-logic / code-auditor — review, not shipping)
```

---

## Persisting or Updating a Live Artifact

```
Write(path, htmlContent)                 // build/edit in the workspace first
SendUserFile({ files: [path], status: "normal" })   // → returns file_uuid
mcp__remote-devices__create_artifact({   // first time only
  id: "kebab-case-slug",
  file_uuid: "<from above>",
  description: "What it does and where its data comes from"
})
// later edits:
mcp__remote-devices__update_artifact({
  id: "kebab-case-slug",
  file_uuid: "<new file_uuid from a fresh SendUserFile call>",
  update_summary: "What changed in this update"
})
```

To read an existing artifact's current HTML before editing it further, use
`device_stage_files` with `artifact_ids: ["<id>"]`, then `Read` the staged
copy — don't reconstruct it from memory.

## The Unverified Runtime Assumption

Files built for claude.ai's artifact sandbox often use two APIs that are
**not** standard browser APIs:
- `window.storage.get(key, immediate)` / `.set(key, value, immediate)` — a
  host-provided KV store, not localStorage.
- `fetch("https://api.anthropic.com/v1/messages", ...)` with **no**
  `Authorization` header — the host sandbox is expected to intercept and
  authenticate the request.

Whether Cowork's `create_artifact`-rendered sandbox provides the same two
shims was **not verified** in the source session for this skill, despite
asking directly. Treat this as an open question every time, not a known
fact:
1. State the assumption explicitly to the user (e.g. "assuming the live
   artifact runtime proxies fetch + storage the same way claude.ai does").
2. Recommend they exercise the AI/persistence feature immediately after
   shipping and report back what happens.
3. If it turns out NOT to work, the tool should still degrade gracefully —
   check that the source file already has a fallback path (offline
   field-notes pattern, `hasStorageApi()` guard) rather than crashing.

## Adding Real Parsers Without Breaking Self-Containment

Many hand-built artifacts deliberately avoid CDN dependencies ("nothing
outside this file can break the tool"). Preserve that property when adding
PDF/DOCX/XLSX/ZIP support by inlining the parser libraries at build time
instead of fetching them at runtime.

**Do not paste multi-hundred-KB minified library code through your own model
context via the Edit tool.** Install and splice with direct file I/O:

```bash
mkdir -p libbuild && cd libbuild && npm init -y >/dev/null
npm install pdfjs-dist@3 mammoth xlsx jszip --no-audit --no-fund
```

Then splice with a Python script that reads/writes files on disk directly
(the library text never has to pass through your reasoning tokens):

```python
def safe(code):  # escape literal "</script" so it can't close the tag early
    return code.replace("</script", "<\\/script")

block = (
    "<script>\n" + safe(jszip)   + "\n</script>\n" +
    "<script>\n" + safe(xlsx)    + "\n</script>\n" +
    "<script>\n" + safe(mammoth) + "\n</script>\n" +
    "<script>\n" + safe(pdfjs)   + "\n</script>\n" +
    '<script type="text/plain" id="pdfWorkerSrc">\n' + safe(pdf_worker) + "\n</script>\n"
)
html = html.replace(marker, block + marker, 1)  # insert right before the main <script>
```

Per-library integration notes:
- **pdf.js** needs a Worker. Keep it in one file: embed `pdf.worker.min.js`
  in a non-executing `<script type="text/plain" id="pdfWorkerSrc">`, then at
  init time: `new Blob([workerText], {type:"application/javascript"})` →
  `URL.createObjectURL(blob)` → `pdfjsLib.GlobalWorkerOptions.workerSrc = url`.
  Extract text with `doc.getPage(n).getTextContent()`, join `.items[].str`.
- **mammoth** (docx): `mammoth.extractRawText({arrayBuffer}).value` — no
  worker needed, browser build only.
- **xlsx / SheetJS**: `XLSX.read(arrayBuffer, {type:"array"})`, then
  `XLSX.utils.sheet_to_csv(wb.Sheets[name])` per sheet name. Use
  `xlsx.full.min.js`, not `.core.min.js`, for broader codepage support.
- **JSZip**: `await JSZip.loadAsync(arrayBuffer)`, then
  `Object.values(zip.files).filter(f => !f.dir)`, `entry.async("arraybuffer")`
  per entry — reuse the same per-file extraction routing recursively.

Approximate inlined sizes (v3 pdfjs-dist, current npm as of this writing):
pdf.min.js ~320KB, pdf.worker.min.js ~1.1MB, mammoth.browser.min.js ~640KB,
xlsx.full.min.js ~880KB, jszip.min.js ~100KB. Total addition: ~3MB. That's
fine for a local desktop artifact; don't reach for the CDN option just to
save file size unless the user says so — it trades away the reliability
property the original file was built around.

## Headless Smoke-Testing Before Shipping

The pre-installed Chromium is under a *versioned* subdirectory — don't guess
the path, find it first:

```bash
find /opt/pw-browsers/chromium* -maxdepth 2 -iname "*chrome*"
# → /opt/pw-browsers/chromium-1194/chrome-linux/chrome  (version number varies)
npm install playwright --no-audit --no-fund
```

```js
const { chromium } = require('./node_modules/playwright');
const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-<version>/chrome-linux/chrome',
  args: ['--no-sandbox']
});
const page = await browser.newPage();
const errors = [];
page.on('pageerror', e => errors.push('pageerror: ' + e.message));
page.on('console', m => { if (m.type() === 'error') errors.push('console.error: ' + m.text()); });
await page.goto('file://' + path.resolve('artifact.html'));
await page.setInputFiles('#fileInput', [path.resolve('fixture.txt')]);  // simulate a real upload
// assert on page.locator(...).innerText(), typeof window.<global>, etc.
```

Generate binary-format fixtures instead of sourcing real files — it's faster
and you control exactly what's being tested:
- **xlsx**: use the just-installed `xlsx` package's own `XLSX.writeFile()`.
- **docx**: hand-build a minimal valid one with JSZip — `[Content_Types].xml`
  + `_rels/.rels` + `word/document.xml` is enough for mammoth to read it.
- **zip**: bundle several fixtures together for the batch-import path.

Report the verification honestly: which formats were round-tripped
end-to-end vs. which only had "library loaded, API present" checked (e.g. no
real PDF fixture = pdf.js verified to load, not verified to extract).

---

## Gotchas

1. **Literal `</script` inside inlined library code closes your wrapper tag
   early.** Escape it to `<\/script` before splicing, or the page silently
   truncates mid-library and everything after breaks with no clear error.
2. **Literal "&lt;script&gt;" text inside an HTML/JS *comment* is harmless to
   real browsers** (comments aren't parsed for tags) but breaks naive
   regex-based self-checks. Avoid writing angle-bracket tag mentions in
   comments so your own verification tooling isn't misled by them.
3. **The Chromium path under `/opt/pw-browsers/` is versioned** — hardcoding
   a guessed path fails; `find`/`ls` it first.
4. **`Edit` tool requires a prior `Read` of that exact path in this
   session**, even if you already read the same content from a different
   path (e.g. an upload dir vs. a workspace copy) — read the copy you're
   about to edit, not just the original.
5. **`MAX_INPUT_CHARS`-style truncation constants tuned for pasted text may
   be too small once file uploads are added** — a whole PDF can dwarf a
   hand-typed paste. Reconsider the constant, and say so explicitly rather
   than leaving it silently mismatched to the new feature.
6. **If an interactive clarifying-question tool fails, don't retry it in a
   loop.** After 1–2 failures, switch to stating the assumption in plain text
   and proceeding — per the "pick defaults and label them" clarifier
   protocol. Silently retrying burns turns without getting an answer.
7. **A "separate suite" or "batch" request that reads ambiguously** (e.g.
   "survey separately" vs. "survey combined" after unzip) is often cheaper
   to resolve by building both as explicit buttons than by guessing one.

---

## Self-Verification Checklist

0. Read the target artifact fully before editing it — including any
   comments describing its own design constraints (e.g. "no external
   dependency" — honor or explicitly override that, don't silently break it).
1. Confirmed whether this is a first `create_artifact` or a follow-up
   `update_artifact`, and used the correct one.
2. Any claude.ai-artifact-only API usage (`window.storage`, unauthenticated
   fetch to `api.anthropic.com`) flagged as an unverified runtime assumption
   — not silently assumed to work, not silently assumed to fail.
3. New binary-format support inlined rather than CDN-loaded, unless the user
   explicitly chose CDN after being told the tradeoff.
4. Ran a headless smoke test with real (generated) fixtures for at least the
   formats claimed to work; reported which formats were fully round-tripped
   vs. only structurally checked.
5. Any silently-changed constant (truncation limits, defaults) called out
   in the summary, not buried.

---

## CLAIMS

- [SOURCED] `SendUserFile` → `mcp__remote-devices__create_artifact` /
  `update_artifact` is the documented Cowork flow for persisting HTML as a
  live, revisitable artifact — Cowork system prompt, `<persisted_artifacts>`.
- [SOURCED] pdf.js requires a separate worker script; running it fully inline
  via a Blob-URL-sourced `GlobalWorkerOptions.workerSrc` is a standard
  offline-embedding technique for pdf.js — verified working in a live headless
  Playwright run (worker src resolved to a `blob:` URL, zero console errors).
- [GENERATED] Whether Cowork's live-artifact runtime proxies `fetch` to
  `api.anthropic.com` and provides `window.storage` the same way claude.ai's
  artifact sandbox does is unverified — flagged, not confirmed, in the
  session this skill was extracted from.
- [SOURCED] `xlsx.full.min.js`, `mammoth.browser.min.js`, `pdf.min.js` +
  `pdf.worker.min.js`, and `jszip.min.js` were installed via npm and
  round-tripped real/generated fixtures (txt, csv, json, xlsx, docx, zip)
  with zero console errors in a headless Chromium run performed directly in
  the source session.

## COUNTEREXAMPLE

- An artifact that never touches `window.storage` or the Anthropic API
  doesn't need the runtime-assumption flag at all — don't add it reflexively
  to every artifact, only ones that actually use those APIs.
- Not every upload feature needs binary parsers — if the user only ever
  pastes plain text, inlining 3MB of PDF/DOCX/XLSX libraries is unjustified
  bloat. Ask what formats are actually needed before assuming "everything."
- Real PDF fixtures were not available in the source session; "pdf.js loads
  and its API surface is present" is weaker evidence than an actual
  extraction round-trip — don't claim full PDF support from library-load
  checks alone.

## CONTRADICTIONS

! This skill recommends inlining parsers to preserve a "no external
  dependency" design philosophy, while also adding ~3MB to the artifact —
  the tradeoff (reliability vs. size) should be surfaced to the user, not
  resolved unilaterally, unless a prior tool failure genuinely blocks asking.
! "Don't guess the missing half of a cut-off instruction" is in tension with
  "don't infinite-retry a broken clarifying-question tool." Resolution used
  in the source session: build both plausible interpretations as separate
  UI actions instead of picking one, when that's structurally cheap to do.

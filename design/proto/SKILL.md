---
name: proto
description: Rebuilds a Figma design as code so that input, validation, state, and branching actually work in a single HTML file. Not a click-through screenshot demo — something you press to check the UX and get a feel for the implementation spec. The pipeline runs as settle scope by interview, read Figma faithfully (structure, exact labels, visual tokens), build as vanilla single-file HTML, then verify real behavior in a browser. Triggers - "/fig:proto", "make a working prototype", "make this design actually clickable", "동작 프로토타입 만들어", "프로토타이핑 해줘", "실제로 눌러보고 입력되게".
allowed-tools: AskUserQuestion, Bash, Read, Write, Edit, mcp__plugin_figma_figma__get_design_context, mcp__plugin_figma_figma__get_screenshot, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__use_figma, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__browser_batch, mcp__claude-in-chrome__read_console_messages
---

# fig:proto — Figma design → working prototype (rebuilt in code)

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install fig@byjunyoung`), rather than improvising what the scripts do.

**Rebuilds in code** what is drawn in Figma, producing a single HTML prototype where form input, validation, state changes, and dynamic branching actually work. Not a click-through demo of screenshots but something for **checking behaviour and getting a feel for the implementation spec** — you type a real value and watch the save land in the list.

**The premise:** because it is rebuilt in code, **the visuals are an approximation** (not pixel-perfect against the design) — in exchange, it actually runs. Build-less, dependency-less, single HTML, so it opens on a double click. For a presentation demo where pixel fidelity comes first, this is the wrong approach and a screenshot-based one is right (no dedicated skill for that; capture manually).

**How far "approximation" goes — layout, colour, and spacing. Not assets.** Drawings, illustrations, icons, photographs — **anything that already exists in the design as an image is inlined from the original rather than redrawn in code** (step 3). A drawing imitated in code is always worse than the original, and above all **it ends up inventing behaviour the design never had** — the moment a still image gets redrawn as vectors and made to "move with the value", the prototype hands an engineer a spec that does not exist.

**Prerequisites**: always load the `figma:figma-use` skill before calling `use_figma`. **Zero writes** — the Figma file is only read.

## When to invoke

- "a working prototype", "make it actually pressable", "make input and validation work", "make it behave the way it is drawn in Figma"
- "prototype this" (in a context where input and state are expected to work)
- An explicit "/fig:proto"

## When NOT to invoke

- A pixel-exact demo that only clicks between screens (no input needed) → screenshot-based (no dedicated skill; manual)
- Porting into production code (a frontend repo) → `/fig:code`
- Just seeing the frame list and structure → `/fig:read`
- Auditing the structure and flow of what is drawn → `/fig:lint`

## Inputs

- `figma_url` (required): figma.com/design/:fileKey/...?node-id=... — the target page or screen. Ask if it is missing.
- Target flow (optional): which screen or flow is the centre. Without it, settled in the step-1 interview.

## Where the deliverable goes / publishing

The path and the publish target are set by the `tools` section of `figma-conventions.yaml` — read with `python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py`.

- The default is a local single HTML file. The location is `tools.proto_output_dir` and the filename is `<name>-prototype.html`. Being one file, it opens on a double click.
- Publishing (optional) follows `tools.proto_publish`. When its `repo` is unset, stop at local and do not offer to publish. Never hardcode a repo or an account in this document.

---

## Procedure

### 1. Interview — what counts as done

Fidelity is fixed for this skill: **behavioural**. Confirm the rest in sequence (AskUserQuestion, a recommendation attached to each, one at a time). Share the full list of what needs settling first so the scale is visible, then:

- **Scope**: every screen, or one core flow (create → list → detail, say). A working prototype gets a better token-to-value ratio from **concentrating on the core flow** than from covering everything — usually weighted toward the form, where the input logic lives.
- **Data**: fixed mock-ups, or state held for the session (what you make shows up in the list). For a creation flow, holding state is effectively mandatory.
- **Reference width**: desktop or mobile (as Figma has it).
- **Tech and deployment**: vanilla single HTML (recommended) versus React and the like; local only versus published.

Pin the definition of done in verifiable form (which cards, branches, and states have to work), and for several stages, share the plan before starting.

### 2. Read Figma accurately (read-only — no confirmation needed, explore freely)

Moving it "as drawn" means securing the labels, the structure, and the visuals alike. The target frame id comes from the URL's `node-id` (that frame or page), or from `get_metadata` (the page nodeId) enumerating sections down to screen frames. Then combine four sources:

- **Structure** — `get_design_context` on the target screen. It gives the frame tree, field placement, and the component skeleton. But **large frames come back sparse with text masked as `text`**, so the real labels are missing (layout only).
- **Exact labels** — so a read-only `use_figma` script collects `characters`, absolute coordinates, and hidden status for every TEXT in the frame in one pass (far cheaper in tokens than repeating get_design_context for each sublayer). Map fields to labels by coordinate, and read **required markers (*), defaults, branching hints, and helper text out of the hidden text**. **Harvest the example rows and values** of lists and detail views here too, as the prototype's seed data.

```js
// Collect characters + absolute coordinates for every TEXT in a frame (read-only, return only)
const page = figma.root.children.find(p => p.id === "<PAGE_ID>");
await figma.setCurrentPageAsync(page);
const g = (n,k)=>{try{return n[k]}catch(e){return undefined}};   // phantom-safe
const collect = async (id) => {
  const root = await figma.getNodeByIdAsync(id), out = [];
  const walk = (n) => { if(!n) return;
    if (n.type==="TEXT") { const ch=g(n,"characters");
      if (ch && ch.trim()) { const b=n.absoluteBoundingBox;
        out.push({ y:b?Math.round(b.y):0, x:b?Math.round(b.x):0, t:ch, h:!n.visible?1:0 }); } }
    const kids=g(n,"children"); if(kids) for(const k of kids) walk(k); };
  walk(root); out.sort((a,b)=> a.y-b.y || a.x-b.x); return out;
};
return { form: await collect("<FRAME_ID>") };   // for several frames, bundle them into one script's return
```

- **Visual tokens** — do not shoot every screen; take **one or two representatives only** with `get_screenshot` (maxDimension set for legibility) → save with `curl` → `Read`. Pull nothing but colour, spacing, corner radius, component look, and button styles (the labels are already secured by the TEXT walk). One list-type and one form-type screen is usually enough.

- **The image-asset list** — scan for **nodes carrying an IMAGE fill** the same way as the TEXT walk, and build a list. This becomes the settled list of "fetch, do not draw". Check alongside it whether that node has **overlays laid on as children** (markers, numbers, badges) — if it does, exporting the node whole brings the overlays along exactly as they are.

```js
// Scan for IMAGE fill nodes (read-only) — the result is the asset list to inline in step 3
const g=(n,k)=>{try{return n[k]}catch(e){return undefined}};
const scan = async (frameId) => {
  const root = await figma.getNodeByIdAsync(frameId), hits = [];
  const walk = n => { if(!n) return;
    const fills = g(n,"fills");
    if (Array.isArray(fills) && fills.some(f => f.type === "IMAGE"))
      hits.push({ id:n.id, name:n.name, type:n.type,
                  w:Math.round(n.width), h:Math.round(n.height),
                  kids:(g(n,"children")||[]).length });   // kids>0 = has overlays
    for (const k of (g(n,"children")||[])) walk(k); };
  walk(root); return hits;
};
return await scan("<FRAME_ID>");
```

### 3. Build the single working HTML (vanilla, no build, no dependencies)

Make it **a self-contained single file** — CSS, JS, **and images all inlined**, with no external font, CDN, or image **links** (system font stack). That is what lets it open on a `file://` double click and run in the user's hands with no server for verification. **"No links" is not "no assets"** — putting images in as `data:` URIs rather than links is how the principle is kept.

- **Inline the image assets (the default — ask before dropping any)**: export the IMAGE nodes scanned in step 2 as PNG with `get_screenshot` → save with `curl` → **substitute in as base64 `data:` URIs**. In practice each is tens of KB and several together are a few hundred, no burden on a single HTML file (meaning there is almost never a size reason to drop one — only when it really is large do you flag it and let the user decide).
  - Write **only a placeholder** such as `__IMG_<NAME>__` in the HTML and substitute the base64 in with Bash and Python. Writing long base64 directly through an editor tool wastes whole tokens.
  - The export scale is capped at the original size (a small node blown up with maxDimension does not gain resolution). For sharpness, pick a larger node in Figma or check the original scale.
  - Shooting with `contentsOnly: true` drops unrelated overlapping elements while **keeping that node's child overlays intact**.

```bash
# placeholder → base64 data URI substitution (write __IMG_A__ into the HTML first, then run)
python3 - <<'PY'
import base64, pathlib
html = pathlib.Path('<output.html>')
s = html.read_text()
for token, f in (('__IMG_A__','a.png'), ('__IMG_B__','b.png')):
    if token not in s: raise SystemExit(f'placeholder missing: {token}')
    s = s.replace(token, 'data:image/png;base64,' + base64.b64encode(pathlib.Path(f).read_bytes()).decode())
html.write_text(s)
print('substituted', round(html.stat().st_size/1024), 'KB')
PY
```

- **What to draw in code versus what to fetch**: draw in code only what **actually has to change** with a value or a state (a gauge that fills, a cell that lights up by state, an element that rotates in response to input — **and only where that variation is drawn in the design**). A picture fixed as a single image in the design is fetched as it is. When the call is unclear, settle it with "is this element drawn differently in this screen's state-variant frames?" — if not, it is static.

- **Design tokens**: the colours, spacing, and radii pulled from the screenshots go into `:root` CSS variables. Do not scatter hardcoded values; route through tokens. Match the original mood (light, admin tone, and so on).
- **Layout and routing**: an SPA — `render()` off `state.view`, with **event delegation** (one click, input, and change handler on `#app`, branching on `data-action` / `data-field`). Full re-render only on **structural change** (radio, tab, row added or removed). **Text input updates the model without re-rendering** (so focus survives).
- **The form model and dynamic branching**: one `form` object is the truth. Branches (value fields per type, targets per range, issuance methods) go model → conditional render. Repeating blocks (N rules) are arrays.
- **Validation**: on save, `validate()` → red field + helper error + toast, scrolled to the first error. Rules (blocking mutually exclusive options, say) are disabled at render time and re-checked at save time.
- **Holding state**: save → push to the array → the list reflects it, with an auto id and a success toast. Implement the dialogs as drawn (leave-confirmation, delete, deactivate).
- **Custom widgets** (a multi-select, for example): one piece of state (open, selected), closing on an outside click. Mark with something like `data-stop` so the delegated handler can tell inside from outside.
- **Fidelity**: labels, terminology, order, and seed data exactly as Figma has them. **An obvious clone-residue mislabel** (a coupon list whose column reads 'product ID') is corrected to fit the context but **stated in the report** — no improving on your own; report it.

### 4. Verify in a browser (mandatory)

- **claude-in-chrome cannot open `file://`** → serve with `python3 -m http.server <port>` (from the output folder) and `navigate` to http://localhost:<port>/<file>.
- **Actually click** the core flow through claude-in-chrome: list render / dynamic form branching (one or two representatives) / validation (the error showing) / save → list reflection / detail / dialogs. Bundle clicks and screenshots with `browser_batch` to cut round trips (coordinates are relative to the previous screenshot).
- Fix bugs where they are found and **re-confirm** (never wave one through on a screenshot alone). Shut the server down when verification ends. The user opens the file with a double click (file://) — zero external resources, so it runs.
- A click right after a refresh can land before the render (timing) — do not pile navigate and clicks into one batch; confirm the load first.

### 5. Handoff report

- Where the deliverable is, and **which flows were verified** (what was actually pressed).
- Scope (In/Out): the flows included versus what was left out (cases not demonstrated, whether it was published).
- Mislabels corrected, mock-up limits (reset on refresh, and so on), and non-working elements (a search box that is only shown) — honestly.

## Publishing (optional)

An external write, so it goes through the **preview → "go"** gate — and it happens only when the user asks for it. Never put it in the completion report as a remaining item or a next step.

Read `tools.proto_publish` first. When its `repo` is unset, stop at local and ask where it should go rather than guessing a destination. Otherwise it carries `repo`, `account` (the gh keyring name, which can differ from the actual login), `local` (the working copy), `visibility`, `pages_url`, and `landing` (the file that holds the project cards).

1. **When `visibility` is `public`, confirm the exposure.** An internal admin screen, with figures on it that are not settled yet, goes out to anyone holding the URL. Name what is in it and get the go — earlier publishes to the same repo are not standing consent.
2. **Pull the working copy** at `local` first, so the landing page is not rewritten from a stale copy.
3. **Place the file** as `<local>/<slug>/index.html` — one HTML file, one folder. The slug becomes the URL, so keep it short and in English.
4. **Add one card** to `landing`, matching the markup of the cards already there. Write what actually works in it, not what the screen is about.
5. **Switch the account, push, and switch back inside the same call.** `gh auth switch` is global and nothing restores it for you; leaving it switched makes the next write in another namespace fail with a 404 that reads like a missing repo.
6. **Verify through the published URL**, not the local file. Pages takes a moment to build, so a 404 straight after the push means wait and retry — not that it failed.

Being a code rebuild there is no pixel-diff refresh to run: edit the source, verify in the browser again, push again.

## Constraints

- A code rebuild — the visuals are an approximation (not 100% pixel). If pixel fidelity comes first, this is the wrong approach. **Image assets are not part of the approximation — the originals get inlined** (step 3).
- **Never build behaviour the design does not have.** Turning a static element into something that "responds to a value" is not an improvement; it is inventing a spec that does not exist. Confine dynamic handling to elements whose state variants are drawn in the design, and where an interpretation went in, state it in the report.
- No project-specific proper nouns hardcoded in this document (repo, account, file key, particular screen names) — those come from memory.
- Labels, terminology, and seed data match Figma — do not improve them; report mislabels.
- Never declare "it works" without verifying — actually click it in a browser.
- `file://` will not work → verify through http.server.

## Notes

- The four sources complement each other: `get_design_context` = structure and coordinates, the TEXT walk = strings (labels, seeds, hidden), screenshots = visual tokens, the IMAGE fill scan = assets to fetch as they are. No single one of them does the job.
- REST `get_screenshot` can return an old state right after a write (stale) → work around it with an inline `node.screenshot()` render (rare here, this skill being mostly reads).
- Project-specific values are read from the `tools` section of the config. Do not write repos, accounts, file keys, or screen names into this document.
- Related skills: `/fig:read` (structure only), `/fig:code` (into a frontend repo), `/fig:lint` (auditing what is drawn).

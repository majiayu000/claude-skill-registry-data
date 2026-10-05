---
name: readme-quality
description: >
  Use this skill whenever the user asks to create, improve, audit, or standardize
  a README.md file for any of their projects. Triggers include: "write a README",
  "improve my README", "make my README consistent", "create a README for my project",
  "review my README quality", "my README needs work", or any request to produce
  project documentation. Also use when user provides project code/description and
  wants documentation generated from scratch. Applies the author's personal style
  DNA — bilingual structure, banner-first layout, table-heavy feature presentation,
  AI-Assisted Development disclosure, MIT license footer — and selects the correct
  structural template based on detected project type.
---

# README Quality Skill

Produces or improves README.md files that precisely match the author's established
cross-project style. Always bilingual (EN primary + `README.zh-TW.md` companion).

---

## Step 0 — Read the right template

Before writing anything, identify the project type and read the matching reference file:

| Project type | Signs | Reference file |
|---|---|---|
| `web-app` | React/Vue/HTML, `npm run dev`, deployed URL, browser tool | `references/template-web-app.md` |
| `browser-extension` | `manifest.json`, Chrome/Firefox extension, MV3 | `references/template-browser-extension.md` |
| `cli-tool` | Python/Node CLI, `pip install`, `npm install -g`, library/SDK | `references/template-cli-tool.md` |
| `utility-installer` | PowerShell/Bash scripts, Windows-first, local launcher, no publish | `references/template-utility-installer.md` |

If the project is ambiguous, prefer `cli-tool`. Read the reference file now.

---

## Step 1 — Gather project context

Before writing, collect:

1. **Project name** — exact casing for H1 (ALL CAPS for consumer web apps, title case for everything else)
2. **One-line tagline** — matches repo description on GitHub
3. **Features list** — bullet points or a capability table
4. **Install / Quick Start commands** — exact shell commands
5. **Screenshots / GIFs / banner image** — paths or URLs
6. **Live URL** (web-app only)
7. **AI models used** in development (for AI-Assisted section)
8. **Any existing documentation files** (ARCHITECTURE.md, INSTALL.md, etc.)

If context is incomplete, ask the user for the missing pieces before proceeding.

---

## Step 2 — Apply universal style rules

These rules apply to **every project type** without exception.

### Structure rules

- **Banner image first** — `[![alt](path)](path)` before everything else. If no banner exists, note this to the user and suggest creating one.
- **H1 = project name** — ALL CAPS for consumer-facing web apps; title case for tools/libraries.
- **Tagline line** — either `**Bold subtitle**` inline or `> blockquote tagline`. Pick blockquote for technical tools.
- **Badge row** — shields.io badges for: version/status · platform/runtime · license. One line, space-separated.
- **Navigation links** — anchor link row: `[Section](#anchor) · [Section](#anchor) · [繁體中文](README.zh-TW.md)`. Required for projects with 4+ sections.
- **繁體中文 link** — always present, either in nav row or standalone `[繁體中文](README.zh-TW.md)` near top.
- **`---` dividers** — between every major H2 section.
- **AI-Assisted Development section** — mandatory in every README. See boilerplate below.
- **License** — always MIT, one-liner `[MIT License](LICENSE)`.

### Writing style rules

- **Sentence fragments in feature lists**: write `Auto-detects players, adds controls, popup playback button` not `This tool auto-detects players and adds controls.`
- **Em dash (—) as separator** in two-column description tables: `| **Feature** | Auto-detects overlays — removes click-hijack layers |`
- **Tables over prose** for any list of 3+ items that has attributes.
- **Blockquotes for tips/warnings**: `> 💡 **Recommended:** Use alongside X for Y.`
- **Code blocks with inline guidance**: include comments in multi-step install blocks.
- **Platform-labeled sections** when OS-specific: `### Linux / macOS`, `### Windows`.
- **Never write "This project is..."** — open with the thing itself, not a meta-statement.

### Mermaid diagram rules

- Prefer Mermaid for compact architecture/workflow diagrams when the target renderer supports it; use ASCII when the audience or platform cannot reliably render Mermaid.
- Keep diagrams readable before styling them: short node labels, details in prose/tables, and no raw paths, URLs, or long command lines inside nodes.
- For large workflow maps, split by concern when possible. If a single diagram is still necessary, prefer `flowchart LR` for pipelines, reduce `flowchart.nodeSpacing` / `rankSpacing`, and use `curve: linear`.
- Use Mermaid frontmatter `config` for per-diagram configuration. Avoid new `%%{init: ...}%%` directives because Mermaid deprecated directives in favor of frontmatter.
- For complex flowcharts, try `layout: elk` with conservative ELK options such as `nodePlacementStrategy: LINEAR_SEGMENTS`; fall back to `layout: dagre` when the renderer does not support ELK.
- Do not rely on SVG stretch controls as the primary fix for an unreadable diagram. Fix the graph structure and layout first, then use viewer zoom/fit controls for inspection.

Recommended large-flowchart starting point:

```mermaid
---
config:
  layout: elk
  htmlLabels: true
  flowchart:
    nodeSpacing: 35
    rankSpacing: 55
    curve: linear
    diagramPadding: 8
  elk:
    mergeEdges: false
    nodePlacementStrategy: LINEAR_SEGMENTS
---
flowchart LR
  A["Short label"] --> B["Next step"]
```

### Private data boundary

README files are public or team-shareable documentation. They must not absorb private AI collaboration material.

Keep these local-only folders out of Git and out of README content:

```text
ai-private/
  memo/
  decisions-private/
  credentials-notes/
  environment/

ai-discussion/
  sessions/
  handoffs/
  context-packs/

local/
  logs/
  cache/
  diagnostics/
```

README may mention that local/private notes are ignored, but must not include prompt transcripts, handoff bodies, context packs, secret hints, raw host paths, account/deployment details, unpublished roadmap, or private strategy notes.

### AI-Assisted Development boilerplate

Every README ends with this section before License:

```markdown
## 🤖 AI-Assisted Development

This project was developed with AI assistance.

| Model | Role |
|---|---|
| [Model Name] | [Role: primary architect / code review / documentation / UI design] |

> ⚠️ **Disclaimer:** While the author has made every effort to review and validate
> the AI-generated code, no guarantee can be made regarding its correctness, security,
> or fitness for any particular purpose. Use at your own risk.
```

Fill in the actual models used. Common entries: `Claude Opus 4.6 (Anthropic)`, `Gemini 2.5 Pro (Google DeepMind)`, `OpenAI Codex CLI`.

---

## Step 3 — Generate README

Follow the template for the detected project type. Do not invent sections not in the template unless the project has a genuinely unique feature that requires explanation (e.g., a Human Intervention system, a Policy Gate, a NANO Exchange Layer).

After generating the English README, also generate `README.zh-TW.md` in Traditional Chinese with identical structure.

---

## Step 4 — Quality checklist

Before delivering, verify:

- [ ] Banner image present (or flagged as missing)
- [ ] H1 casing matches project type rule
- [ ] Language switch link present
- [ ] Badge row present
- [ ] Navigation anchor links present (if 4+ sections)
- [ ] All section dividers (`---`) in place
- [ ] Feature presentation uses tables or fragment-style bullets (not full sentences)
- [ ] Code blocks present for all install/run commands
- [ ] AI-Assisted Development section present with model table
- [ ] Disclaimer blockquote present
- [ ] License line present
- [ ] No "This project is..." opener
- [ ] No trailing redundant sections not in template
- [ ] zh-TW companion README also generated
- [ ] README does not include private AI discussion, memo content, context packs, secret hints, raw host paths, account/deployment details, or unpublished roadmap/timeline
- [ ] New-project docs recommend ignored `ai-private/`, `ai-discussion/`, and `local/` folders instead of committing private collaboration notes

---

## Step 5 — Audit mode (existing README)

When auditing an existing README, produce:

1. **Score card** — rate each checklist item above as ✅ / ⚠️ / ❌
2. **Gap summary** — 2–3 sentences on what's missing or inconsistent
3. **Revised README** — full rewrite applying all rules, or targeted diff patches if user prefers minimal changes

---

## Reference files

Read the matching template file for the detected project type:

- `references/template-web-app.md` — Frontend web app / SPA / online tool
- `references/template-browser-extension.md` — Chrome/browser extension
- `references/template-cli-tool.md` — CLI tool / Python package / library / MCP server
- `references/template-utility-installer.md` — Local utility / Windows launcher / installer script

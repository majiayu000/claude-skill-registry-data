---
name: present-doc
description: >-
  Prepare and deliver Markdown or HTML document assets to Leonardo Acosta.
  Use whenever an .md or .html document is being considered, created, revised,
  or selected as an asset to present at the end of the current turn: reports,
  plans, explanations, comparisons, README previews, or review pages. Always use
  the dark Markdown Graphs schema; render every Mermaid diagram with Mermaid and
  frame it in mdxcn style. Deliver with ropen and return its verified tailnet URL.

  Do not trigger for an inline-only answer or a repository file edit that is
  not being offered as a document asset.
compatibility: >-
  Requires installed `ropen`, configured tailnet preview access, local Markdown
  Graphs design resources, and the `mdxcn`, `markdown-graphs`,
  `mermaid-diagrams`, `crafting-effective-readmes`, `bro`, and `ropen-preview`
  skills. Mermaid rendering requires an available Mermaid renderer.
metadata:
  author: leonardoacosta
  source: leonardoacosta/skills
---

# Present a document

Own presentation, not the underlying task. Keep its evidence, requested format,
and scope. A possible document asset activates this workflow before drafting;
it does not justify creating a file for a one-sentence answer or publishing
unrequested repository changes.

## Compose, do not duplicate

Resolve dependencies through the runner's skill loader or the installed
`~/.agents/skills/<name>/SKILL.md`. Read the selected skill before using it.

| Decision | Resource and boundary |
| --- | --- |
| Plain-language explanation | Read `bro`; apply plain-language clarity and exact-fact rules to explanatory content, but do not apply its invocation-wide `/bro` rewrite protocol. Preserve paths, commands, numbers, names, URLs, and decisions. |
| README or project setup document | Read `crafting-effective-readmes`; select its matching project template. Inspect the actual stack: T3 examples are not evidence that another project uses T3. |
| Any Mermaid diagram | Read `mermaid-diagrams`; always obtain an actual rendering from the available Mermaid renderer and place the rendered figure in the presented document. A Mermaid source fence alone is not rendered output. |
| Figure framing | Read `mdxcn` for the frame style: dashed rectangular border, `+` corners, and monospace `[ LABEL ]` on the rail. Apply this style to rendered Mermaid without redrawing its nodes or arrows. For other figures, read `markdown-graphs` and obey host support; do not invent formats. |
| Every document delivery | Read `ropen-preview` for private preview paths, escaping, content safety, and transport failure handling. Present with `ropen` and return the exact verified tailnet URL. |

Choose one visual form per idea. Numbers belong in a table, without duplicating
the same data in a chart. Include a Mermaid diagram only when real structural
relationships improve understanding; when included, always render it.

## Always-dark document system

Every document and rendered Mermaid figure uses the dark Markdown Graphs theme,
regardless of source format. Read `~/.designs/markdown-graphs/design.md` and
`~/.designs/markdown-graphs/design-tokens.json`; use resolved `dark` values,
never light-theme tokens. Core values: `#040404` background, `#D1D1D1`
foreground, `#090909` card, `#121212` muted surface, `#989898` secondary ink,
`#5D5D5D` figure frame, `#292929` rail/border, Ocean accents `#02C5FF`,
`#5196FF`, `#4CABFD`. Use Geist/Geist Mono where installed, otherwise sensible
local fallbacks. Keep square corners, restrained dashed rails, clear text, and
semantic alternatives. `#696969` graph-muted is not required body text.

Frame each rendered Mermaid image in mdxcn style: square dashed rail, `+`
corners, and a Geist Mono-style `[ LABEL ]` caption interrupting the top rail.
Do not replace the Mermaid renderer's image with a handmade diagram. Follow the
reference image's proportions and restrained composition when available. The
optional high-contrast override is approved for light documents only; it never
overrides the always-dark requirement. Verify actual foreground/surface
contrast before claiming conformance.

Keep Markdown source portable; its browser presentation carries the dark theme.
If the preview shows raw Markdown, produce a self-contained dark HTML view in the
private preview directory. Do not fetch CDN scripts/fonts or install a renderer.
Use an available Mermaid rendering tool for every included Mermaid diagram. If
no renderer is reachable, retain its source and report the missing prerequisite;
do not substitute a raw fence, ASCII, or another format. Delivery is incomplete
until required Mermaid figures are actually rendered.

## Deliver before ending the turn

1. Finish the asset. Keep repository documents in their intended location;
   stage only the presentation and required local resources under the private
   session directory defined by `ropen-preview`. Revisions reuse a stable path.
2. Check that only intended content is served. No secrets, confidential content
   without explicit content-class approval, remote trackers, write actions, or
   browser-to-agent callbacks. Escape untrusted HTML. Do not mount a repository
   or home directory to show one document.
3. Inspect `command -v ropen`, `ropen --version`, and `ropen --help` once per
   session. Run `ropen "<absolute-file-path>"` as one quoted argument. Retain its
   exit status and non-quiet output; let ropen own networking and live reload.
4. Get the exact tailnet URL from successful ropen output. `ropen --list` shows
   mounts and server state, not document URLs. Never guess a hostname, port,
   mount code, or URL. Do not substitute localhost, file://, a public tunnel,
   or a local path.
5. Fetch that exact URL and inspect the intended document, not just HTTP 200.
   The exact-link handoff intentionally overrides `ropen-preview`'s quiet/no-URL
   default only. Preserve its privacy and transport rules. Opening authorizes only
   that preview; any browser inspection must be read-only, session-owned, and
   within applicable browser-consent policy.
   Use browser inspection when available; check content, actual rendered figures,
   relative assets and narrow-screen overflow. Report any visual verification
   limit.
6. Return `[Read the report](<verified-tailnet-url>)` plus only the decision or
   limitation the reader needs. Keep the served file while the link is in use;
   clean it only at session end or when asked.

A failed rendering, command, unavailable URL, or failed content check means
delivery is incomplete. Preserve the local asset and report the exact blocker
and path. Never claim successful opening; do not start another server, alter
Tailscale/firewall/systemd, or switch transports to hide a failure.

---
name: "Asset: Card"
description: "Generate the project's social card (OG 1200×630 and GitHub 1280×640) from a committed card.json and the card theme block; optionally upload it as the GitHub repo's social preview through the user's own browser"
when_to_use: "When a project needs an Open Graph image, a GitHub social preview or a portfolio thumbnail; when the user mentions OG image, social card, link preview or repo preview."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: asset
disable-model-invocation: true
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion", "ToolSearch", "mcp__claude-in-chrome__tabs_context_mcp", "mcp__claude-in-chrome__tabs_create_mcp", "mcp__claude-in-chrome__navigate", "mcp__claude-in-chrome__find", "mcp__claude-in-chrome__computer", "mcp__claude-in-chrome__file_upload", "mcp__claude-in-chrome__read_page"]
argument-hint: "[og|github|both] [upload] [theme family] [title or tagline overrides in plain words]"
---

# Social cards

Load `asset-conventions` first. Renderer: `~/.claude/library/scripts/asset/card.ts` (satori → resvg); upload facts in `~/.claude/library/references/asset-tools.md`.

```xml
<asset-card>
	<arguments>
		<axis name="sizes">`og`, `github` or `both` (default both).</axis>
		<axis name="upload">The word `upload` (or "set it on the repo") enables step 6. Never inferred.</axis>
		<axis name="overrides">Plain-word title/tagline/meta overrides go into `card.json`. A theme family name selects the card block.</axis>
	</arguments>

	<steps>
		<step num="1">Resolve the `card` theme (`theme.ts card --project .`). Gather: project name (`package.json` `name` or repo name), one-line description (`package.json` `description`, README first paragraph), meta (`owner/repo`, version tag, or a stack line), hero candidate (`docs/assets/shots/home.png` or the first framed shot if any; run `asset-shot` first if none exist and the project has a UI).</step>
		<step num="2">Write or update `docs/assets/cards/card.json` (`title`, `tagline`, `meta`, `hero` relative to the cards dir, `logo`). Title ≤ 40 characters, tagline ≤ 90; rewrite rather than let satori wrap into a third line. Show the JSON and stop for approval.</step>
		<step num="3">Render: `bun ~/.claude/library/scripts/asset/card.ts docs/assets/cards/card.json docs/assets/cards/og.png --size og --project .` and the same with `--size github` → `github.png`. Ensure fonts are present (`bun ~/.claude/library/scripts/asset/fonts.ts` if card.ts complains).</step>
		<step num="4">Quality gate: Read both PNGs. Check title fits in two lines, hero isn't clipped, text clears the accent bar, file size under 1 MB (`stat -f %z`); if over, re-encode with `sharp` at quality 85 or drop the hero to a smaller `max_width_ratio` via the theme.</step>
		<step num="5">For a SvelteKit/Next project, offer the `&lt;meta property="og:image"&gt;` tag pointing at the deployed `docs/assets/cards/og.png` (or `static/og.png` copy) and where it goes (`src/app.html` or the root layout). Report per the conventions.</step>
		<step num="6">
			Upload (only with the `upload` argument). Say exactly what will happen: open `https://github.com/&lt;owner&gt;/&lt;repo&gt;/settings` in the user's Chrome via the claude-in-chrome MCP, click Edit under Social preview, choose `github.png`. **Stop and get explicit consent in the conversation.** Then: load the MCP tools in one ToolSearch call, `tabs_context_mcp`, create a tab, navigate, `find` "Social preview Edit", click, `file_upload` with the absolute path of `github.png`, wait, screenshot to confirm the preview changed. If the page or selectors don't match, stop and hand back the URL rather than guessing at clicks. No credentials are stored or entered by the skill; the browser session is the user's.
		</step>
	</steps>

	<rules>
		<rule>One template. Layout variety comes from the theme's card block and the hero, not from per-project template edits; if a project truly needs a different composition, that is a `theme-target` or a new card variant in the toolkit, discussed first.</rule>
		<rule>Uploading is the only outward action in the asset family and it always gates on explicit consent, per invocation.</rule>
		<rule>`card.json` is committed; the PNGs are regenerated from it, never hand-edited.</rule>
	</rules>
</asset-card>
```

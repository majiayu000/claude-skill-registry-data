---
name: "Asset: Demo"
description: "Produce a demo GIF/MP4: VHS tape for CLI tools, shot-scraper storyboard for web flows, Playwright recording when the storyboard vocabulary can't express the flow; engine chosen from what the demo must show"
when_to_use: "When a project needs an animated demo for its README or portfolio; when the user mentions a GIF, demo, recording, walkthrough or 'show it working'."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: asset
disable-model-invocation: true
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion"]
argument-hint: "[cli|web] [what the demo should show, in plain words] [name]"
---

# Demo recordings

Load `asset-conventions` first; tool syntax is in `~/.claude/library/references/asset-tools.md`.

```xml
<asset-demo>
	<arguments>
		<axis name="kind">`cli` or `web`; inferred from project type when absent (CLI project → cli, anything with routes → web). Ask only if both are plausible.</axis>
		<axis name="outcome">Everything else is the desired outcome in plain words ("install, run init, show the generated file"; "sign in, create a board, drag a card"). This is the spec the flow is written from.</axis>
		<axis name="name">A short slug if given; otherwise derived from the outcome (`init-flow`, `create-board`).</axis>
	</arguments>

	<steps>
		<step num="1">Detect project type; resolve the `vhs` theme for cli (`theme.ts vhs --project .`). Draft the flow as a numbered list of steps from the outcome, each one action, with the sleeps/waits a viewer needs to read the screen. Say the list.</step>
		<step num="2">
			Engine choice (web only). Check every step against the storyboard vocabulary: navigate, click, type, fill, press, scroll, pause, wait_for, screenshot, javascript. If every step fits → storyboard. If any step needs hover, drag, a keyboard chord mid-flow, file upload, waiting on a specific network response, or a second tab → Playwright flow. State the engine and the step that decided it in one line.
		</step>
		<step num="3">
			Write the source into `docs/assets/demo/`:
			- cli: `&lt;name&gt;.tape` opening with the emitted theme lines (`bun ~/.claude/library/scripts/theme/emit.ts &lt;vhs theme file&gt;`), then `Output docs/assets/demo/&lt;name&gt;.gif` and `Output docs/assets/demo/&lt;name&gt;.mp4`, `Require` for each binary used, then the flow. Use `Hide`/`Show` around setup the viewer needn't see; `Wait /prompt/` rather than long sleeps where output is deterministic.
			- storyboard: `&lt;name&gt;.storyboard.yml` with `viewport`, `cursor: true`, `server:` when a dev server is needed, and scenes named after the steps.
			- flow: `&lt;name&gt;.flow.ts` default-exporting `async (page) => {}` with `page.waitForTimeout` beats so the viewer can follow.
			Show the source and stop for approval.
		</step>
		<step num="4">
			Render: `vhs docs/assets/demo/&lt;name&gt;.tape`; or `shot-scraper video docs/assets/demo/&lt;name&gt;.storyboard.yml -o docs/assets/demo/&lt;name&gt;.webm --mp4`; or `cd ~/.claude/library/scripts/asset && node --experimental-strip-types record.ts &lt;abs flow path&gt; &lt;abs out.webm&gt; --mp4`. For web outputs also make a GIF for the README: `ffmpeg -i &lt;name&gt;.mp4 -vf "fps=12,scale=960:-1:flags=lanczos" -loop 0 &lt;name&gt;.gif`.
		</step>
		<step num="5">Quality gate: extract frames at 1s, the midpoint and the end (`ffmpeg -ss T -frames:v 1`) and Read them; check the first frame isn't a blank terminal or a loading page and the last frame shows the outcome. Fix timing and re-render once. Report per the conventions, with the GIF line plus MP4 link.</step>
	</steps>

	<rules>
		<rule>The tape/storyboard/flow is committed source; the outcome text goes in a comment at its top so a future re-render knows what it was for.</rule>
		<rule>Keep demos under 20 seconds; if the outcome needs longer, propose splitting into two named demos.</rule>
		<rule>Web recordings run against a dev server with seeded data, never production with real accounts.</rule>
		<rule>Terminal colours, fonts, margins and window bar come from the vhs theme block only.</rule>
	</rules>
</asset-demo>
```

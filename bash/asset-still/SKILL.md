---
name: "Asset: Still"
description: "Render a styled image of a code snippet or a command's output with freeze, using the project's freeze theme block"
when_to_use: "When a README, article or card needs a code image or a picture of terminal output; when the user says code screenshot, snippet image, carbon-style or 'show this function'."
model: sonnet
effort: low
metadata:
  glyph: ᛊ
  family: asset
disable-model-invocation: true
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash"]
argument-hint: "<file [lines a-b] | run: <command>> [svg] [theme family]"
---

# Code and terminal stills

Load `asset-conventions` first; freeze flags are in `~/.claude/library/references/asset-tools.md`.

```xml
<asset-still>
	<arguments>
		A file path with an optional line range ("src/auth.ts 40-72", "lines 40 to 72"), or `run:` followed by a command whose output to capture. "svg" switches output format. A theme family name selects the freeze block.
	</arguments>
	<steps>
		<step num="1">Resolve the `freeze` theme (`theme.ts freeze --project .` prints the theme file path) and emit its config to `docs/assets/stills/.freeze.json` (`bun ~/.claude/library/scripts/theme/emit.ts &lt;resolved theme file&gt; -o docs/assets/stills/.freeze.json`).</step>
		<step num="2">
			Render:
			- file: `freeze &lt;file&gt; --config docs/assets/stills/.freeze.json [--lines a,b] -o docs/assets/stills/&lt;file-slug&gt;[-a-b].png`. Language is auto-detected; pass `--language svelte` for `.svelte` when detection misses.
			- command: `freeze --execute "&lt;command&gt;" --config … -o docs/assets/stills/&lt;command-slug&gt;.png`. Commands run in the project root; anything with side effects gets shown to the user first.
		</step>
		<step num="3">Quality gate: Read the PNG; check nothing is clipped at the right edge (add `--wrap 100` if so) and the window bar renders. Report path, dimensions, README snippet.</step>
	</steps>
	<rules>
		<rule>Line ranges keep at most ~40 lines; longer snippets get split or cropped to the interesting part and the crop is stated.</rule>
		<rule>Never capture output that could contain secrets (`env`, tokens, `.env` contents).</rule>
	</rules>
</asset-still>
```

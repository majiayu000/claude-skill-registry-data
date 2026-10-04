---
name: "Theme: Target"
description: "Define a new theme target type (a consumer of colour/type tokens the theme system doesn't cover yet): template, core→target mapping rule, emitter case, so theme-factory can extend any family to it"
when_to_use: "When a skill or script needs a themed output for a consumer with no entry in theme-conventions.md's target table (a new renderer, a TUI framework, a slide tool) or when the user says a theme should also drive some new kind of output."
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: theme
disable-model-invocation: true
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "WebFetch", "AskUserQuestion"]
argument-hint: "<target-name> [consumer: tool, library or file format]"
---

# Add a theme target type

A target type is defined by three things: a template (`~/.claude/library/templates/themes/<target>.json`), a mapping row in `~/.claude/library/references/theme-conventions.md`, and an emitter case in `~/.claude/library/scripts/theme/emit.ts`. This skill adds all three; `theme-factory` then does the per-family work.

```xml
<theme-target>
	<steps>
		<step num="1">Read `theme-conventions.md`. If the target already exists in the table, stop and say so; the user wants `/theme-factory`.</step>
		<step num="2">
			Establish the consumer's exact config shape from its documentation (context7 MCP or WebFetch on the upstream docs, never memory): which keys it reads, value formats (hex with or without `#`, named colours, ANSI indices), whether it wants one variant or both, and how the file reaches it (flag, config path, inline). Record the source URL.
		</step>
		<step num="3">
			Ask, in one AskUserQuestion, only what the docs can't settle: which core swatches map to which consumer keys when the mapping isn't obvious, and whether the consumer is dark-only (terminals) or variant-aware.
		</step>
		<step num="4">
			Write the template: `family`, `target`, `extends`, `rationale.mapping_notes`, then a block named after the target holding every consumer key with `null` values and sensible non-colour defaults (sizes, radii) filled in.
		</step>
		<step num="5">
			Add the mapping rule to `theme-conventions.md`: a row in the target table and a paragraph under "Core → target mapping" written so two runs produce the same file (name the swatch for every key; say how extra colours are synthesised).
		</step>
		<step num="6">
			Add the emitter case to `emit.ts`: a function that turns the block into the consumer's native text, and a `case` in the switch. Raw-JSON passthrough is acceptable only when the consumer is one of our own scripts. Run `bun emit.ts` on a hand-filled copy of the template to prove it.
		</step>
		<step num="7">
			Add the target to the `theme-factory` preview list (step 6 of that skill) with how to render a preview of it, and to `asset-tools.md` if a new tool is involved. Report the three files touched and the `/theme-factory "&lt;target&gt;" from &lt;family&gt;` invocation that comes next.
		</step>
	</steps>
	<rules>
		<rule>The block mirrors the consumer's shape, not ours. If the consumer wants `bg`/`fg`, the block says `bg`/`fg`; the semantic names live in the mapping paragraph.</rule>
		<rule>No colour values in the template. Values come from a family via theme-factory.</rule>
		<rule>Cite the docs URL in `mapping_notes` of the template so the next person can re-verify.</rule>
	</rules>
</theme-target>
```

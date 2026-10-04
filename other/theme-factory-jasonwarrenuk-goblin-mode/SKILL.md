---
name: "Theme: Factory"
description: "Create, update, extend, print or display a project theme family: a core palette plus per-target files (html, vhs, freeze, card, frame, ghostty, tui) that every asset and artefact skill reads deterministically"
when_to_use: "When a project needs a theme for any rendered output, when an asset skill reports that no theme exists for its target, or when the user says theme, palette, colours, look, brand for artefacts, terminal GIFs, cards or screenshots."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: theme
disable-model-invocation: true
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion", "Artifact"]
argument-hint: "print|display [all|<target>|<family>] | <target>|<family> [new] [from <family>]"
---

# Theme factory

Owns `.claude/themes/` in the current project. Conventions, schema, derivation rule and quality gates live in `~/.claude/library/references/theme-conventions.md`; read it before doing anything, every time.

```xml
<theme-factory>
	<arguments>
		<axis name="verb">
			`print [all|target|family]` lists themes in the terminal (project first, then global), one line each: family, targets present, anchor, mood, stale flags. `display [all|target|family]` renders the swatch page (`bun ~/.claude/library/scripts/theme/swatch.ts --themes-dir .claude/themes [--family X] -o …`) and publishes it with the Artifact tool. Anything else is create-or-update.
		</axis>
		<axis name="subject">
			A target name (`html`, `vhs`, `freeze`, `card`, `frame`, `ghostty`, `tui`; fuzzy: "html artefacts" → html, "terminal" → vhs) or a family name. Resolve by checking `.claude/themes/`: a matching `<family>.json` means the subject is a family; otherwise it is a target.
		</axis>
		<axis name="new">The token `new` forces creation of a second family (or second target file) rather than updating the one found. Without it: update if exactly one match exists, create if none, ask if several.</axis>
		<axis name="from">`from <family>` names the core to extend when creating a target file. Required when more than one family exists; inferred when exactly one does.</axis>
	</arguments>

	<steps>
		<step num="1">Read `theme-conventions.md`. List `.claude/themes/` (create the directory if missing) and `~/.claude/library/themes/`. Decide the verb, subject, mode (create family / create target / update family / update target) and say it in one line.</step>
		<step num="2">
			Seed. For a new family, gather candidates before asking: the project's CSS custom properties (`src/app.css`, `globals.css`, `tailwind.config`), any logo or hero image under `static/` or `docs/assets/`, the project README's first paragraph for mood words. Offer the user: derive from CSS, derive from an image (sampled via sharp), mood words, a reference palette (`reasonable-colors-reference.md` is one), or "surprise me within these constraints". One AskUserQuestion, at most three questions: seed, family name, anything the theme must avoid.
		</step>
		<step num="3">
			Judgement gate. Before writing, state in three lines: the mood, the anchor hue and why it survives both surfaces, the one rule bent. If the seed is an existing family (update mode), state instead what changes and what stays.
		</step>
		<step num="4">
			Write the file from the template in `~/.claude/library/templates/themes/` (core or target), following the derivation rule and the core → target mapping table exactly. `rationale` fields are sentences; `rejected` lists what was considered and turned down. For target files copy the core verbatim into the mapping; never re-derive. Set `provenance.created` / `updated` to today.
		</step>
		<step num="5">
			Mechanical gate: `bun ~/.claude/library/scripts/theme/validate.ts .claude/themes/&lt;family&gt;.json`. Exit 1: fix and re-run (up to three passes; then show the findings and ask). Exit 2 (originality or blocklist warning): **stop**. Print the finding verbatim, name the nearest theme, and wait. Proceed only on the user's explicit instruction (`anyway`, "keep it", "I want it close to X"); then record that in `rationale.rule_bent` and re-run with `--register`. Never lift the warning yourself. Target files are validated by emitting them: `bun ~/.claude/library/scripts/theme/emit.ts .claude/themes/&lt;family&gt;-&lt;target&gt;.json` must succeed.
		</step>
		<step num="6">
			Preview. Core: run the swatch page and publish it (Artifact). Target: render the real thing with the toolkit (`vhs` a five-second tape via emit + `vhs`; `freeze` a still of the theme file itself; `card` a card with the family name; `frame` the swatch screenshot framed; `html` the swatch page with the emitted tokens applied; `ghostty`/`tui` the emitted text). Open the PNG with Read and check it yourself before showing it: blank areas, unreadable text, clipped edges get fixed first.
		</step>
		<step num="7">Stop for approval. On changes, return to step 4. On approval: `validate.ts --register` for a core, then report the file paths and which skills now pick the theme up.</step>
	</steps>

	<rules>
		<rule>Both variants always. A theme with only a dark palette is incomplete; terminals use the dark variant, everything else may switch.</rule>
		<rule>Colours are decided here and nowhere else. Asset and artefact skills consume theme files; if one needs a colour the theme lacks, the fix is a theme change, not an inline hex.</rule>
		<rule>The originality warning belongs to the user. The model does not argue it away, restate it as fine, or nudge the palette a fraction to slip under the threshold.</rule>
		<rule>Updating a core marks every target file of that family stale (`print` shows it). Offer to re-emit them; do not silently rewrite target files the user didn't ask about.</rule>
		<rule>Family names are short lowercase slugs with no hyphen (the hyphen separates family from target).</rule>
		<rule>British spelling in every rationale field and mapping note.</rule>
	</rules>
</theme-factory>
```

## Print format

```
.claude/themes/            (project)
  ember        html vhs card         anchor rust #B7410E   "Foundry at dusk: …"   vhs stale (core updated 2026-09-02)
~/.claude/library/themes/  (global fallback)
  clod         html vhs freeze card frame ghostty   anchor brass #D9A441   "Ink and brass: …"
```

A target argument filters to families that have that target; a family argument shows that family's full rationale and contrast table.

---
name: "Artefact: Design Conventions"
description: "Jason's structural and epistemic-honesty conventions for every artefact Claude creates"
when_to_use: "Before writing any artefact (a claude.ai/Cowork Artifact, a Claude Code project artefact or the styling pass inside import-scaffold_artefact), alongside whatever medium-specific requirements already apply (e.g. the Artifact tool's own artifact-design skill)."
disable-model-invocation: false # the trigger moment (about to write an artefact) is one Claude recognises before the user does; the per-project interview (Step 2b) is its own approval gate before anything gets written
metadata:
  family: artefact
allowed-tools: ["Read", "Glob", "Grep", "Write", "AskUserQuestion"]
---

# Artefact design conventions

Every artefact Claude writes for Jason (a claude.ai/Cowork Artifact, a
Claude Code project artefact, a ported real app's styling pass) follows the
same location rule and the same values, expressed in a bespoke way each
time. The full ruleset lives in
`~/.claude/library/references/artefact-conventions.md`; this skill is the
procedure that gets it applied.

**Announce at start** (briefly, not a whole paragraph): which artefact
you're about to write and where.

## Step 1: Location, always

Every artefact (named-skill output or something created ad hoc
mid-conversation) writes under `<project-root>/docs/artefacts/`, defaulting
to `{slug}.html` at the top level. Any depth of nesting beneath that
directory is valid when the artefact joins a set:
`docs/artefacts/{collection}/{slug}.html`, with an `index.html` hub in the
collection directory linking its members.

`<project-root>/site/` is the one other valid location, **only when Jason
asks for it explicitly**. Never infer it, never relocate an artefact there
unprompted.

If there's no obvious project root (a bare claude.ai conversation with no
repo), this step doesn't apply: that's the `Artifact` tool's territory, not
a repo file.

- [ ] Target path resolved under `<project-root>/docs/artefacts/` (or `site/`, if Jason asked)
- [ ] If joining an existing collection, its `index.html` gets a link to the new page

## Step 2: Check what's already there

Search **both** locations, recursively, because collections nest and because
a project's artefacts can be split across the two:

```bash
find <project-root>/docs/artefacts <project-root>/site -name '*.html' 2>/dev/null
```

`docs/artefacts/` being empty proves nothing on its own. A project that has
published its artefacts keeps them under `site/`, and that is where its
established aesthetic lives; treating it as a first-artefact project would
throw away a convention that already exists.

**Existing artefacts found** → read one (or a couple, if they look
stylistically inconsistent with each other). Extract the established
palette/hue-mapping (read the CSS `:root` block and its mapping-notes
comments if present), font pairing and tone. State it back in one line,
*"this project already has an artefact aesthetic: {short description};
reusing it"*, and carry it into the new artefact. **No interview.**
Consistency with the project's own prior artefacts wins over inventing
something new.

**Found under `site/`** → same rule, plus two things that only apply there.
Read `site/CLAUDE.md` if one exists, since a published directory carries its
own constraints on what may be written. And say plainly that the aesthetic
being matched is the live one, so a new page joining it is a page going
public.

**This is the project's first artefact** → go to Step 2b.

- [ ] Both `docs/artefacts/` and `site/` checked before writing anything
- [ ] `site/CLAUDE.md` read, if the project has one
- [ ] Existing aesthetic (if any) read and stated back in one line

## Step 2b: Brief interview for a project's first artefact

Run a short, round-based interview, same discipline as
`import-scaffold_artefact` Step 3 and `roadmap-create-interview`: **2-4
questions per round**, never a long list at once, and end each round with
*"Anything else, or shall I go ahead?"*. Skip any question the content
itself already answers (a pipeline-metrics doc doesn't need to ask if this
is a data-heavy artefact).

Cover:
- **Palette mood**: what hue(s) should this artefact's semantic aliases map
  to, and why (the reference doc's mapping rule expects a stated reason,
  not just a colour pick).
- **Font pairing**: display/body voice + monospace workhorse; free choice,
  but ask rather than default silently. **Offer from Jason's shortlist
  first** (below); reach outside it only when none of the five suit the
  artefact's mood, and say why.
- **Tone**: reference/data page, narrative piece or something between; this
  determines whether Step 3's honesty rule expresses as status chips or a
  footnote (see the reference doc).

Once agreed, **write the outcome into the CSS as explicit mapping-notes
comments**, the way `site/assets/site.css` does:
document *why* each alias maps to which theme token. This first artefact becomes
the self-documenting spec Step 2 reads back on every artefact after it in
this project; nobody should have to re-ask these questions for the second
artefact.

### Jason's shortlist (display/body faces)

Chosen from a fourteen-way bakeoff, August 2026. All are on Google Fonts, so
one `@import` or `<link>` covers any of them. Present these first.

| Face | Setting | Reads as |
|------|---------|----------|
| **Texturina** | `opsz` 12–72, `wght` 400–800 | Rough and literary. Titles only: rejected as body text on the goblin-mode site, where it now sets `h1`, section titles and card titles |
| **Fraunces** | `SOFT` 100, `WONK` 1, `opsz` 144 | Soft, lopsided, high contrast. The wonk axis is the whole point; without it Fraunces is ordinary |
| **Grenze** | static, 400/600/700 | Roman and blackletter hybrid, angular and gnarled without tipping into costume |
| **Eczar** | `wght` 400–800 | High contrast and loud. Strong personality at display sizes |
| **Young Serif** | static, single weight | Blunt heavy slab. Display only; it has no body-text weight |

Rejected in the same bakeoff and worth not re-proposing: Instrument Serif
(too severe), Bricolage Grotesque and Fraunces-without-wonk (both
unremarkable), Iowan Old Style (the well-mannered default these replace).

Two of the five carry variable axes that do the actual work, so record the
axis values in the mapping-notes comment alongside the palette. `Fraunces`
without `WONK 1` is a different typeface for these purposes.

**All five are display faces.** Pair each with a plain book serif for body
text and keep monospace for labels: three voices, not two. An optical-size
axis lowers contrast at small sizes; it does not sand off the character that
made the face worth choosing. Judge any candidate at body size over a long
page before letting it near a paragraph.

- [ ] Interview run in 2-4-question rounds, none dumped at once
- [ ] Font offered from the shortlist first, with variable-axis values named
- [ ] Outcome written as mapping-notes comments in the artefact's own CSS

## Step 3: Apply the shared rules

Read `~/.claude/library/references/artefact-conventions.md` in full and
apply: masthead structure, theme-sourced semantic palette (this project's own
mapping from Step 2/2b), the three-state theming contract and its toggle
control, typography pairing, the collapsibility threshold, the
epistemic-honesty rule (structural marking, never hedging prose) and the
technical-hygiene list (self-contained, `overflow-x` scrollers,
`tabular-nums`, British spelling).

For a claude.ai/Cowork `Artifact` publish specifically: this skill's rules
are additive to Anthropic's built-in `artifact-design` /
`artifact-diagramming` / `artifact-capabilities` skills, not a replacement;
favicon, CSP self-containment and runtime capabilities stay owned by those.
Load both.

- [ ] Masthead present (or deliberately compressed for a short narrative piece)
- [ ] Palette routes through theme tokens via semantic aliases only
- [ ] If the artefact documents a skill, its hue is keyed to that skill's `metadata.family`, reusing an established family mapping where one exists; a cross-family index takes no hue of its own
- [ ] Three-state theming contract present, or single-look justified explicitly
- [ ] Toggle control present (light/system/dark, masthead-anchored, persisted) on every pathway except an `Artifact` publish, which relies on the host's own control
- [ ] Any JS-rendered diagram follows the theme (CSS-variable-driven, or re-rendered on both `matchMedia` change and `data-theme` mutation)
- [ ] Collapsibility applied if past the threshold
- [ ] Table of contents added if past the threshold, in a closed `<details>` or its own sticky sidebar
- [ ] Honesty rule expressed structurally, not as hedging prose
- [ ] Self-contained; `overflow-x` scrollers on wide content; British spelling

## Step 4: Write

Show the draft (or its key structural decisions, for a long artefact) before
writing, following the same approval convention `artefact-audit` and
`artefact-roadmap` already use. Write to the Step 1 path. Report the file
path, the aesthetic decision (reused or newly interviewed), and anything
notable in how the honesty rule was expressed.

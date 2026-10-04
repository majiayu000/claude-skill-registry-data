---
name: custom-hud-layout
license: MIT
description: Builds and designs a custom hud (HUD) in CS2 — menus, shops, scoreboards, timers, modals, overlays and interactive screens — with the custom_hud_layout entity (CCSCustomHudLayout), covering Panorama XML markup, VCSS styling, layout and animation, the server-side JS API and click handling. Panorama is HTML/CSS-shaped but is not the web; panels replace divs, flow and alignment replace flex and grid, colours are hex, and there is no client script, no inline styles, no markup event handlers, no calc() and no variables. Use when authoring, laying out, styling, theming or animating a CS2 hud, when translating a web or Figma design into Panorama, when you need to know which tags and attributes a custom hud allows, why a layout fails validation, how to toggle panel classes and text from the server, how to receive button clicks, how to give a player a mouse cursor, or how to use custom fonts, SVG icons, localised text or video in a hud
---

# Source 2 | Custom Hud Layout

The `custom_hud_layout` entity (C++ `CCSCustomHudLayout`) lets a map or server-side plugin
present players with a HUD authored in Panorama XML + VCSS.

**Read this first:** a custom hud is *not* an ordinary Panorama document. The loaded XML is
run through a dedicated whitelist validator that permits **only four panel types and a fixed
attribute set**. There is no `style=`, no `<script>`, and no event handlers in markup.
All dynamic behaviour is driven from the server.

## `ADDON` in these documents

A hud ships inside a **Workshop addon** — the unit the game mounts and the client downloads — and
every path in these documents is written relative to one. `ADDON` is the placeholder for that
addon's name: the project you are building lives in `content/csgo_addons/ADDON/`, and the
compiler writes its `_c` resources to `game/csgo_addons/ADDON/`. Substitute your own addon's
directory name wherever it appears.

It shows up in two different roles, and they are worth telling apart:

| Where | What `ADDON` is |
|-------|-----------------|
| `content/csgo_addons/ADDON/panorama/...` | the addon directory on disk — the mount root |
| `s2r://panorama/styles/custom_game/ADDON/main.vcss_c` | a namespace folder *inside* the addon |

An `s2r://` path is resolved against every mounted content path, so it begins at the addon's
`panorama/` — the addon directory itself never appears in it. The `ADDON` segment in the second
row is a folder you create and name after your addon, by convention, so your resources cannot
collide with the base game's or another addon's at the same path. Nothing enforces it; the
collision it prevents is silent.

Compiling those sources is a separate job from authoring them — see the `resource-compiler`
skill.

## The full pipeline

```
custom_hud_layout (server, keyvalue layout="...")
   │  m_strLayout is replicated to the client
   ▼
CSGOCustomHuds (Panorama window) → layout/hud/customhuds.xml
   └─ <Panel class="WindowRoot" hittest="false">
        └─ <CSGOCustomHud id="CustomHud" style="width:100%; height:100%; flow-children:none;">
             └─ CSGOCustomHudLayoutRoot   ← created from C++, one per entity,
                  └─ YOUR XML                with no id and no class
```

Return path (a click): user message `CS_UM_CustomHudClicked` (390) → server-side JS event
`OnCustomHudClicked` carrying `{ player, layout, buttonId }`.

## Two kinds of hud

Every custom hud is one of two things, and the difference is a single per-player call:

| | **Overlay** — the default | **Cursor** — `SetInputCaptureEnabled(slot, true)` |
|---|---|---|
| What it is | pixels on the screen | a screen the player can use |
| Mouse | none; the crosshair keeps aiming | a cursor appears over the hud |
| Clicks | nothing is clickable | `Button` clicks reach the server |
| `:hover` | never matches | works, and costs the server nothing |
| Build | timers, scoreboards, kill feeds, banners | shops, vote dialogs, pickers, menus |

Capture is **off every time the layout is built**, so it has to be turned on again after the
entity spawns — see [entity.md](references/entity.md), *Input capture*. Within a
captured hud, `hittest="false"` decides which panels the cursor passes through; write it on
everything and take it off the few containers that must catch the mouse.

## What a hud can actually contain

The markup vocabulary is four tags, but what you can put *through* them is wider than it looks:

- **SVG icons** (`.vsvg`) that stay sharp at any ui-scale, tinted at runtime with `wash-color`;
- **your own fonts**, by dropping `.ttf` files into the addon's `panorama/fonts/`;
- **per-player localised text**, via `text="#Token"` resolved client-side in each player's own
  language, drawing on your own strings or the whole base-game catalogue;
- **the base game's artwork**, referenced by `s2r://` path with nothing added to your download;
- **animations and transitions**, including entry/exit pairs driven by class toggles;
- **video**, as a `background-image` layer on an ordinary `Panel`;
- **sound**, as a `sound:` property on a rule — played when the rule starts matching, so a
  class the server toggles is a sound cue (see [patterns.md](references/patterns.md), *Sound is a
  class*).

## If you are coming from the web

Panorama is HTML/CSS-shaped, which is a help and a trap: the syntax reads as familiar, and then a
property silently does nothing. The mental model that works is **a server-rendered page with no
client script at all**, where the only two updates that exist are *toggle a class on a panel* and
*set a string on a panel*. Everything else — every variant, every state, every branch — is
authored ahead of time and merely revealed.

| You would write | Here you write |
|-----------------|----------------|
| `<div>` | `<Panel>` |
| `<span>`, a text node | `<Label text="...">` — text lives in an attribute, not between tags |
| `<img src>` | `<Image src>`, or a `background-image` on any panel |
| `<button onclick>` | `<Button id>` — the click goes to the server, not to script |
| `style="..."` | nothing; `class` is the only styling hook |
| `display: none` | `visibility: collapse` |
| `visibility: hidden` | `opacity: 0` — still in layout, still clickable |
| `position: absolute` | `x` / `y` plus `ignore-parent-flow: true` |
| flexbox, grid | `flow-children` on the parent, `horizontal-align` / `vertical-align` on the child |
| `gap` | `margin` on the children |
| `filter: blur(4px)` | `blur: gaussian( 4, 4, 1 )` |
| `rgba(0, 0, 0, 0.5)` | `#00000080` — colours are hex only, alpha is the last byte |
| `linear-gradient(...)` in `background-image` | `gradient( ... )` in `background-**color**` |
| `@font-face` | drop the `.ttf` into `panorama/fonts/`; nothing to declare |
| `:hover` | `:hover` — one of the few things that works exactly as expected |
| a JS event handler | the server event `OnCustomHudClicked`, keyed by the button's `id` |
| `data-*` read by JS | `{s:name}` dialog variables, set from the server |
| a loop or `<template>` | neither exists — enumerate the rows in markup or in the stylesheet |
| `calc()`, custom properties | neither exists — enumerate the values in the stylesheet |

Two habits from web work cause most of the wasted time here. **Reaching for a computed value**:
there is no `calc()`, no variables, and the server cannot send a number, so a progress bar is a
class per step and a coordinate is a literal in a rule. And **reaching for client behaviour**: a
dropdown that opens itself, a tab strip that switches itself, a form that validates itself — none
of that can happen without a round trip, so design the interaction around a click going to the
server and a class coming back.

What survives intact is the part designers care about most: the box model, alignment, colour,
typography, shadows, rounded corners, transitions and keyframe animations all behave close enough
to the web that visual work transfers directly. See
[references/css.md](references/css.md) for the complete property set and the full list of what is
absent.

## Quick start

A worked example: a **capture-point indicator** — a read-only strip anchored to the bottom of
the screen with a radial progress ring, driven entirely by dialog variables and class toggles.
It needs no input capture, because nothing in it is clickable.

Authored sources live under `panorama/layout/custom_game/ADDON/` and
`panorama/styles/custom_game/ADDON/` in the addon's content root; the compiler turns them into
`.vxml_c` / `.vcss_c`:

```
panorama/layout/custom_game/ADDON/capture_point.xml
panorama/styles/custom_game/ADDON/capture_point.css
```

**1. Markup** — `panorama/layout/custom_game/ADDON/capture_point.xml`

```xml
<root>
	<styles>
		<include src="s2r://panorama/styles/custom_game/ADDON/capture_point.vcss_c" />
	</styles>

	<!--
		The outer panel must NOT carry an id — the loader assigns it, and the compiler
		rejects one. Keep it an anonymous full-screen wrapper and put the real root inside.
	-->
	<Panel class="cp-screen" hittest="false">

		<!-- Starts hidden: the entity shows this layout to EVERY player the moment it spawns, so the authored state has to be the empty one. -->
		<Panel id="CaptureRoot" class="cp-root hidden" hittest="false">

			<Panel class="cp-ring">
				<Panel class="cp-ring-track" hittest="false" />
				<!-- The server rewrites cp-fill's class to cp-fill-0 … cp-fill-100;
				     the stylesheet turns each step into a clip: radial() sweep. -->
				<Panel id="CaptureFill" class="cp-ring-fill cp-fill-0" hittest="false" />
				<Label id="CapturePct" class="cp-pct" text="{s:pct}" />
			</Panel>

			<Panel class="cp-copy">
				<Label id="CaptureName" class="cp-name" text="{s:point_name}" />
				<Label id="CaptureHint" class="cp-hint" text="{s:hint}" />
			</Panel>

		</Panel>
	</Panel>
</root>
```

**2. Styles** — `panorama/styles/custom_game/ADDON/capture_point.css` (there are no inline styles at all)

```css
/* Full-screen wrapper. noclip lets the ring's glow spill past the panel edge instead of
   being cut off; the wrapper itself is never hit-tested. */
.cp-screen
{
	width: 100%;
	height: 100%;
	overflow: noclip;
}

/* The strip itself, parked above the bottom edge. It starts invisible and offset, and the
   server adds "show" to play the reveal — which is why this is an alternative to .hidden,
   not an addition: a collapsed panel is out of layout and has nothing to animate from. */
.cp-root
{
	flow-children: right;
	horizontal-align: center;
	vertical-align: bottom;
	margin-bottom: 96px;
	opacity: 0;
	transform: translateY(20px);
	transition-property: opacity, transform;
	transition-duration: 0.15s;
	transition-timing-function: ease-out;
}

/* The revealed state. Both properties are listed in transition-property above, so adding and
   removing the class animates in each direction. Write the longhands, not the `transition`
   shorthand — see css.md §11. */
.cp-root.show
{
	opacity: 1;
	transform: translateY(0px);
}

/* Removes a panel from layout entirely, so neighbours close up rather than leaving a hole.
   Nothing else collapses a panel — opacity: 0 keeps the space reserved. */
.hidden
{
	visibility: collapse;
}

/* Square box the two ring images stack inside. Both fill it, so they line up exactly. */
.cp-ring
{
	width: 56px;
	height: 56px;
}

/* The unfilled ring underneath, dimmed so the fill on top reads as progress. Artwork comes
   from a compiled texture over s2r:// — the standard form. */
.cp-ring-track
{
	width: 100%;
	height: 100%;
	background-image: url( "s2r://panorama/images/custom_game/ring_png.vtex" );
	background-size: contain;
	background-repeat: no-repeat;
	opacity: 0.25;
}

/* The same artwork on top, recoloured by wash-color and revealed a sector at a time by the
   .cp-fill-* rules below. Tinting one grey source beats shipping a texture per team. */
.cp-ring-fill
{
	width: 100%;
	height: 100%;
	background-image: url( "s2r://panorama/images/custom_game/ring_png.vtex" );
	background-size: contain;
	background-repeat: no-repeat;
	wash-color: #4caf6dff;
}

/* One rule per step the server can select, because it can toggle a class but cannot send a
   number. clip is free of layout cost and animates, so more steps are cheap. */
.cp-fill-0
{
	clip: radial( 50% 50%, 0deg, 0deg );
}

.cp-fill-25
{
	clip: radial( 50% 50%, 0deg, 90deg );
}

.cp-fill-50
{
	clip: radial( 50% 50%, 0deg, 180deg );
}

.cp-fill-75
{
	clip: radial( 50% 50%, 0deg, 270deg );
}

.cp-fill-100
{
	clip: radial( 50% 50%, 0deg, 360deg );
}

/* Text column to the right of the ring, centred against it. */
.cp-copy
{
	flow-children: down;
	vertical-align: center;
	margin-left: 12px;
}

/* Point name — the line the player reads first. */
.cp-name
{
	font-size: 20px;
	font-weight: bold;
	color: #ffffffff;
}

/* Supporting line, held back with alpha rather than a second colour. */
.cp-hint
{
	font-size: 14px;
	color: #ffffff99;
}

/* Team accent. The server sets team-ct or team-t on the root, and the descendant selector
   repaints the fill — so team colour and progress stay independent of each other. */
.cp-root.team-ct .cp-ring-fill
{
	wash-color: #56a0ddff;
}

.cp-root.team-t .cp-ring-fill
{
	wash-color: #f0a531ff;
}
```

**3. Entity** — in Hammer or via `CreateEntityByName`

| Keyvalue | Value |
|----------|-------|
| `layout` | `panorama/layout/custom_game/ADDON/capture_point.vxml` |

**4. Driving it from the server** (server-side JS under `cs_script`) — see [entity.md](references/entity.md)

```js
const hud = Instance.FindEntityByName("capture_hud"); // JS wrapper class: CustomHudLayout

function showCapture(slot, name, pct, team) {
	hud.SetHasClassForPlayer(slot, "CaptureRoot", "show", true);
	hud.SetHasClassForPlayer(slot, "CaptureRoot", "team-" + team, true);

	// swap the step class: clear the old one, set the new one
	hud.SetHasClassForPlayer(slot, "CaptureFill", "cp-fill-" + roundTo25(pct), true);

	hud.SetDialogVariableStringForPlayer(slot, "CapturePct", "pct", pct + "%");
	hud.SetDialogVariableStringForPlayer(slot, "CaptureName", "point_name", name);
	hud.SetDialogVariableStringForPlayer(slot, "CaptureHint", "hint", "Hold the point");
}

function hideCapture(slot) {
	hud.SetHasClassForPlayer(slot, "CaptureRoot", "show", false);
}
```

Because the server can only toggle classes and set strings — it cannot send a number — a
continuous value like a progress ring has to be quantised into a class per step. Five steps are
enough for a capture ring; a smoother bar just needs more rules.

## Common rejections

| What you want | Why it fails |
|---------------|---------|
| `<TextEntry>`, `<ProgressBar>`, `<Movie>`, `<ToggleButton>`, any other tag | only `Panel`, `Label`, `Image`, `Button` — for video use a `background-image` layer instead of `<Movie>` |
| `style="..."` on an element | no panel type has a `style` attribute |
| `onactivate="..."` or any markup event handler | none; clicks reach the server keyed by `id` |
| `<scripts>`, `<snippets>`, `<snippet>` | rejected at the AST node-type level |
| `<include>` of another `.xml` | only a `.vcss` resource may be referenced |
| `dialogvariable="..."` as an attribute | the server sets variables via `SetDialogVariableString` |
| `hittest` on `<Button>` | `Button` accepts only `id` and `class` |

Full permitted set: [xml.md](references/xml.md).

## Debugging

The validator logs to the **`custom_hud`** logging channel at warning severity:

| Message | Cause |
|---------|-------|
| `Layout xml is an invalid resource name "%s"` | `layout` does not resolve to a resource name |
| `Failed to load layout '%s'.` | file missing or not compiled |
| `Layout contains disallowed node '%s' (type: %d).` | `<scripts>`/`<snippets>`/`<snippet>` etc. |
| `Layout contains disallowed panel type '%s'.` | tag outside the four permitted |
| `Layout contains disallowed attribute %s for panel type '%s'.` | attribute not on that tag's list |
| `Layout contains reference to disallowed resource type '%s'.` | `<include>` targets a non-`.vcss` resource |
| `Layout xml did not pass CustomHud validation "%s"` | final rejection |
| `Layout is invalid.` | an attribute node whose parent is not a panel |

On a validation failure the panel is **never created** — a blank screen, no partial render.
Hot-reloading a live layout into an invalid state **destroys** the existing HUD.

### A stylesheet that compiles is not a stylesheet that loads

`resourcecompiler` checks that a `.css` parses structurally. It does **not** interpret property
values, so a sheet full of values the runtime will reject compiles clean, every time — `OK: 1
compiled, 0 failed` and exit 0. The values are interpreted by the client at load, and a bad one
surfaces only as a parse-warning dialog in the game or the tools.

Never report a stylesheet as working on the strength of an exit code.

### Reading the `Error parsing layout and style files` dialog

Two behaviours of that dialog cost more time than the warnings themselves:

- **It shows one warning at a time.** Dismissing it can surface the next warning from the same
  load, which reads like a new bug appearing after a fix but is the same parse continuing. Keep
  dismissing until it stops before concluding anything.
- **The line numbers belong to the sheet the game loaded** — the last compiled one, not the file
  on disk. Edit the source without recompiling and the numbers point into the previous version,
  where the named line can be a comment or an `@define`.

So before believing a reported line, check the mtime of the `_c` output against its source, and
read the line in the version that was actually compiled.

## References

| File | Contents |
|------|----------|
| [xml.md](references/xml.md) | Complete tag/attribute whitelist, AST node types, validator rules |
| [css.md](references/css.md) | All 140 Panorama CSS properties, units, flow/align value sets, preprocessor |
| [entity.md](references/entity.md) | Entity schema, server-side JS API, click protocol, limits |
| [patterns.md](references/patterns.md) | Idioms for addressing, server-driven state, lookup tables and the pool budget |
| [localisation.md](references/localisation.md) | `#Token` text, the addon's own string files, the catalogues the game ships and what is in them |
| [internals.md](references/internals.md) | How this was derived, and the anchors to re-verify it after a game update |

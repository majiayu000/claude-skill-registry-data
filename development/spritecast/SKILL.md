---
name: spritecast
description: Make game sprites at their real size and exact camera angle (2:1 or true isometric, 3/4 top-down, front view) in the user's art style - props, furniture and objects, standing figures, characters walking, running, jumping, slashing and throwing in 8 facings (painted, or as pixel art about 96 px tall for arcade games; props as pixel art too, from every side) and seated in 8 facings, seated on the user's own chairs and benches with the chair's front piece in front of them - from a 3D guide an image model redraws; then cut out, fitted to the guide, given a baked shadow and an anchor, and fixed by hand on a local touch-up page. Use when the user asks for an isometric or top-down prop, furniture, object or character sprite, a walk cycle or another animation (run, jump, attack, throw, a Mixamo FBX clip), pixel-art sprites or a sprite sheet of a character, fixing pixel sprites by hand, a seated or sitting character, putting a character on a chair or bench, or fixing a sprite's cut-out, halo or what covers what.
license: MIT
compatibility: Claude Code (runs Python, Playwright and a local Chrome/Chromium on the user's machine; calls the OpenAI Images API with the user's own key)
---

# SpriteCast: isometric props and characters at true scale

Image models draw isometric objects at slightly wrong angles and sizes. This skill gives the model a guide it cannot misread: the
object built from simple blocks at its real size, rendered with an exact 2:1 isometric camera. The model only redraws the guide in the
art style of a reference picture; the result is laid back onto the guide, so the angle, size and footprint stay exact.

Scripts: `${CLAUDE_SKILL_DIR}/scripts/isoprop.py` (steps `render`, `draw`, `finish`, `preview`). The spec format is in
[reference/spec.md](reference/spec.md); how to build good guides in [reference/tips.md](reference/tips.md) - read both before writing a spec.

## Setup (once)
1. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/doctor.py` (any Python 3.9+; `python` on Windows). It lists what is there and what each
   thing is for; its last line `PYTHON=<path>` is the interpreter to use for every script below. If it says "not ready", tell the user
   in a line what is missing and run it again with `--fix` (a venv in ~/.cache/spritecast/, the packages, about 10 s). No Chrome or Edge: ask first, then `--fix --browser`
   (Playwright's Chromium, ~150 MB). For characters add `--characters` (the 224 MB cut-out
   model, once). If it says the Python cannot make a venv, pass on its one-line fix.
2. Keys: `OPENAI_API_KEY` for `draw`, `TRIPO_API_KEY` for characters. They come from the plugin's settings (the user gives them in
   `/plugin` → SpriteCast; a session-start hook hands them to the scripts), else from the environment. Missing: tell the user to put it
   in the plugin's settings and restart Claude Code. Never ask the user to paste a key into the chat, never write it into a file,
   never print it.
3. **A first-time user, or "try it" / "체험":** `PYTHON isoprop.py try [--out DIR]` - free, no key: an example's guide rendered on
   their computer and finished with the drawing that came with it → show them `preview.png` and `render.png`, then offer to make
   their own prop.

## Making a prop
1. **Ask only what is missing**: what it is, its real size if it matters, which way it faces, the game's view (`camera`: 2:1
   isometric by default, true isometric, 3/4 top-down, front; or their own angle), whether it must turn (`views`), and the art style (a bundled style name
   - `cozy` - or the user's own reference picture: one finished prop in the look they want, ideally on a flat background).
2. **Write the spec** (`<name>.json` in the user's asset folder): footprint in metres, the blocks at real size, a `description` of the
   finished object (materials, colours, details), `facing`. Real-world sizes matter: look them up if unsure (a dining chair seat
   ~45 cm, a door 2.0-2.1 m).
3. **Render the guide (free)**: `python ${CLAUDE_SKILL_DIR}/scripts/isoprop.py render <spec>`. Look at `render.png` and
   `render-shadow.png` yourself, then show the user `render.png`. Fix the blocks until the shape, proportions and facing are right -
   this is the cheap step; everything after it follows the guide.
4. **Draw (paid)**: run `draw <spec>` without `--yes` first - it prints the model and the cost (about $0.07 at `high`). Tell the user
   the cost and wait for a yes before running it with `--yes`. With `views`, the first view is drawn first and the others follow it
   (about $0.09 each) - check the first before drawing the rest when it is a new design. Several props: say the total. Never redraw without asking
   (`--again`); a drawing that came out wrong is usually a guide or description problem - fix that first.
5. **Finish and check**: `finish <spec>` then `preview <spec>`. If `finish` warns (or `sprite.json` `fit.ok` is false), the model
   drew another angle or shape: it was NOT squeezed to fit. Tell the user, say why (often an angled style picture pulled it off the
   guide's view), fix the description, and ask before drawing again. Look at `preview.png`; show it to the user. If the drawing added or
   moved parts, adjust the description (say what must NOT be there) and ask before drawing again.
6. Hand over `sprite.png`, `shadow.png`, `sprite.json` (anchor, footprint corners, px per metre, shadow offset) and say how to place it
   in their engine: put the sprite so its anchor sits on the footprint's front corner; draw the shadow under all sprites.

## More detail with a 3D model (Tripo)
When the user wants more detail than blocks give (curves, carving, tapered legs) and has `TRIPO_API_KEY`: after the block guide is
right, `model <spec>` (prints the cost; ~20 Tripo credits, ~2 min; ask first, then `--yes`) makes a Tripo model from the description
and puts it in the spec at the blocks' HEIGHT, in its own proportions - the shape is the model's, never pressed into the blocks' box (blocks → `blocks_draft`). Then `yaws <spec>` (free): look at yaws.png and set
`model.yaw` to the turn whose front faces where the blocks' did. Then render, show, draw as usual. Blocks alone are fine when the
arrangement matters more than detail.

## Characters
A standing person: a `character` spec (see spec.md) instead of blocks - a mannequin at their real height, one view per facing, the
first facing drawn first and the rest from it. Ask the height, the build, the facings (4 diagonals unless their game uses 8) and what
they wear. Look at every facing yourself before showing them: the outline check can't see a body turned the wrong way inside a right
outline (a back view with the front of the clothes). Redraw just that one: `draw <spec> --yes --again --only <facing>` (ask first).
Poses (`character.pose`): stand, wave, point, hold, arms-crossed, walk (a single mid-stride picture) - say the pose in the description too
("waving hello"). Anything else, or "raise the arm higher": write the angles (`{"base": ..., "arm": {...}}`, spec.md "Custom poses"),
render (free), look, adjust the numbers, and only then draw. Their shadows are cast from the finished drawing (hair, clothes), each pixel moved by the 3D guide's height under it, so every foot starts its own shadow; solid props keep the 3D shadow. No animation: for
walk cycles or other animation say this plugin doesn't make them (it needs a rigged 3D model and every frame
drawn to match).

## Walking characters
**Ask first: eight facings or four.** `"facings": 4` in the spec renders and draws only the diagonals (south-east, south-west, north-east, north-west): about half the drawing (a walk ~$1 instead of ~$2; pixel art ~$0.7 instead of ~$1.35). Most isometric games draw only these four; offer it whenever cost matters. The exported character (`export.py`) still takes all eight directions - `play("walk", "east")` shows the nearest facing drawn, keeping the one shown last between two as near, so walking straight across does not flicker. With four, south-east is drawn first and the rest follow it (with eight, south). `pixelart.py` draws the spec's facings too.
For an animated character (an 8-direction walk and standing views), use `${CLAUDE_SKILL_DIR}/scripts/charpipe.py` and read
[reference/character.md](reference/character.md) first. It needs one finished illustration of the character - facing front, standing straight, arms down, no pose (if theirs is posed, draw a neutral one from it first and show it) - and TRIPO_API_KEY besides OPENAI_API_KEY (or the user's own rigged GLB as `rig_glb`). Ask how tall the character will be on screen in their game and offer the sizes - 512 (HD), 256 (the default), 128, 64 - as
`"frame_px"` (the frame's height; no answer: 256; another size later is `pack --px`, free). Ask the game's view and set it as `pitch`, not `camera` (30 = 2:1, the default; 35.26 true isometric; 50 3/4 top-down; 12 front - the 8 facings stay 45° apart). Tripo makes the model
and the rig; with `"modeler": "meshy"` (and MESHY_API_KEY) Meshy makes the model (the author's way). Offer it when they have a Meshy account. Three steps, the user's OK before each:
`turnaround` (~$0.09; show it: both sides the same, nothing over the arms) → `3d` (~75 Tripo credits: model, rig, walk, then the
renders by themselves - show the front and a side: the face, not the back of the head) → `draw` (~$2, every facing drawn; when every facing is drawn,
`finish` and `preview` run by themselves - show `out/sheet.png` and a GIF). Every paid step prints its cost and needs `--yes`; ask the user for each one, and
never run the next paid step because the previous one "looked fine": a problem seen in one step is fixed there, not carried on.
**A four-legged animal** (a cat, a dog, a fox...): `"kind": "animal"` in the spec. The same three steps, but `3d` makes only the model
(~30 Tripo credits - no rig: Tripo's animal rig is poor, so the skeleton is found from the mesh and walked in a cat's gait). The
turnaround on all four legs, each leg clear, the tail out behind; clothes only snug ones (a vest, not a cape or a scarf). Check the
renders before `draw`: four legs, the head forward, the tail behind.
**Cheaper, softer** (`"draw": false`): no image model draws the frames - the 3D renders are the frames; after `3d` it finishes by itself.
The turnaround is still drawn by the image model (~$0.09) unless the user brings a rigged GLB (`rig_glb`): only then is no image model used at all.
Offer it when cost matters more than detail (prototypes, background walkers); say it is softer (no drawn lines, a simpler face).
**Every facing is drawn by default** (`"mirror": false`): a flipped facing is only as good as its pair and swaps anything that isn't
the same on both sides (hair over one shoulder, a logo, a bag, one bunny ear up). Flipping comes in only by the rules below - a facing
still under `redo_below` after two redraws is mixed frame by frame with its flipped pair - or when the user asks to save ~$0.66 on a
design that is the same on both sides (`"mirror": true`, or a list such as `["north-east"]`). Before agreeing to a mix on a design
that isn't symmetrical, check that what is on one side stays on that side.
After `draw` (people and animals alike), `finish` names the sheets with a frame fitting its render under `redo_below` (0.75). Show the user `out/walk-all.mp4` (every facing walking at once; with ffmpeg) - a head that grows and shrinks, a
jumping frame or an odd stride shows there, not in the numbers. Look at the back views yourself for anything worn on the head (ears,
antennae, a bow): each on its side and, from behind, only its back (the 3D model makes such things rough).
Then, asking for each paid round:
1. Show the user the renders beside the drawn frames for those facings (the overlap of each frame on it), and the cost.
2. `redraw --yes`: those sheets drawn again (up to twice each); each keeps whichever drawing fits better.
3. **Stop after a sheet's second try and show the result** before going on. Only if the user says so, `redraw --yes` again: a facing
   still under the line is mixed with its mirror pair (east/west, north-east/north-west, south-east/south-west) - the pair drawn too if
   it was being flipped (2 sheets, ~$0.22; free if it's drawn already), then each frame of both the better of its own drawing and the
   other's flipped; south and north, which have no pair, get their low frames drawn one at a time (~$0.11 each, once each).
A low score is not always a bad drawing: lay the render's outline over the frame and look. For an animal the size is matched by overlap
per sheet (its height is mostly the tail), so a low score there is the drawing itself - a head turned another way, legs bunched.
Then tell the user the shadows are per frame (`out/shadows/`, draw them under the sprites at character.json's `shadow_alpha`: 0.56 - since 0.20 a shadow is light as it falls, deep under the feet and pale at its far edge; `"shadow": "flat"` in the spec for the old one hard shape at 0.3; the render takes longer for it, ~9 min a character with three actions). **How deep the shadow is**: `"shadow_strength"` in the spec, the shadow as if laid that many times - a painted set's default is 1 (as the light gives it, 56 % at its deepest); a **pixel set's is 1.5** (71 %: pixel art says things a little louder than they are, so a figure stands on the ground). On dark ground offer more (1.6-2), on a light floor where it looks heavy offer 1; `pack` (or `pixelart.py`) again is free, and `shadow_alpha` in character.json goes with it. The same number for the game's props (below), so they agree. Matching outfits (`facecheck`),
the anchor on the soles, and what to do when the cut-out stops for want of onnxruntime: [reference/character.md](reference/character.md#notes).

## More actions: run, jump, a slash with something held (people)
**Which source - say it when the user asks for an action:** Tripo to save time, Mixamo when the result matters (the author's advice). Tripo: one step, no download; moves with nothing in the hands (walk, run, jump) come out fine from it. When the result matters - attacks above all - recommend Mixamo, though it takes a little longer (more natural - motion capture; free; thousands; one set's attacks share a stance, so they link into combos): give a Mixamo search link for the move - `https://www.mixamo.com/#/?page=1&query=<words+joined+by+plus>&type=Motion%2CMotionPack` (e.g. `query=Standing+Melee+Attack+Downward`) - the download settings (FBX Binary, 30 fps, Without Skin, no keyframe reduction), then `addclip.py` (free). Mixamo has no API: the skill cannot fetch from it - say so; the user goes to the site, looks, downloads, and puts the file beside the spec. Never put the FBX in a public repo.
`"actions": ["run", "jump", {"name": "slash", "hold": "umbrella"}]` in the spec, before `3d` or `rig --again` (~10 Tripo credits an
action; Tripo's biped presets: run, jump, slash, shoot, dive, climb, fall, hurt, turn - three at most beside the walk and idle; with
the user's own rig, any clip by name: `{"name": "attack", "clip": "Sword Slash"}`). `render` renders each in 8 facings, `draw` draws
them after the walk (~$0.11 a sheet, 2 sheets a facing), `finish` fits and packs → `out/<name>-<facing>.png` and `"actions"` in
`character.json` (frame, anchor, frames, loop, fps, shadows). `"draw": false`: the renders are the frames. A one-shot action (jump,
slash) plays once, its first frame to its last; a slash or a shot needs something in the hand - `"hold"` builds it from shapes on the
hand (`umbrella`, `pistol`, `watergun`; `{"kind", "hand": "left"|"right", "length", "color", "grip"}`), so it is in every render and drawn where the render has it.
`"hold"` in the spec itself (not in one action) is carried all the time - walk, standing, every action - and then nothing is ever flipped
(`"mirror": "never"`, also on its own for a character that is not the same on both sides). The hand closes on the handle by itself:
**open `render/hand-<name>.png` and read the line `render` prints before any paid sheet** (reference/character.md, "the hand closes on it").
**Joining two animations** (`{"name": "ready", "between": ["walk", "slash"], "frames": 3}`; `"slash:end"` for an action's last pose): the rig's
poses part-way from one to the other, so a walk goes into an attack and back out without a jump. Free to render - look - then drawn like any
action (reference/character.md, "The poses between two animations").
**See animations joined**: `charpipe.py loop SPEC --only walk,ready,slash,recover --facing <f>` (free) → `out/loop-<f>.gif` - show it
after drawing in-betweens: a frame that jumps shows there.
**One frame of an action wrong**: `"frame_words": {"5@south-east": "..."}` says what the render cannot show for that frame, and
`charpipe.py frame SPEC --only <action> --facing <f> --frame <n> --yes` (~$0.08) draws it alone. A hand the head hides is drawn pulled into
sight unless that frame says it is hidden (reference/character.md, "One frame wrong").
**A swing's effect** (`"trail"` in an action that holds something: `"trail": "water"`): what the held thing leaves in the air - `plain`,
`wind`, `water`, `drops`, `fire`, `flames`, `leaves`, `greenleaves`, `petals`, `snow`, `sparkle`. Free and no drawing: `render` reads the
held thing's path off the rig and writes the effect as a sprite of its own (`out/<action>-<facing>-trail.png`, `"trail"` in
`character.json`), laid over the body; an action already drawn gets one with `render --only <action>` then `pack`. Offer it for a slash
(reference/character.md, "A swing's effect").
Show the renders first; a clip with a long still tail (Tripo's slash is 6.6 s, its swing 0.6-2.7) takes `"t0"` / `"t1"`.
**The head:** the walk's prompt tells the model to keep the eyes ahead and the chin level (a rig's walk looks down). For an action whose
head bows or turns with the motion - a slash, a crouch, a shot aimed low - set `"head": "as_render"` (the slash has it by default): the
head is drawn bowed and turned exactly as the render, never lifted to face the viewer - in the facings where the face shows (south,
south-east, south-west); the side and back views keep the walk's words. Measured on the slash, every frame both ways: the face-on facings
went from 0.786 to 0.837 overlap (17 → 20 of 24 frames passing), the side and back views did slightly worse with it (0.791 → 0.771). **What `redraw` does with actions:** a held thing drawn in the wrong place is redrawn by itself (twice at most, the better kept) -
the render's held thing is rendered apart, so a frame is wrong when the drawing covers under half of where it sticks out of the body
(`HELD_MIN`), or more than 8 % of the drawing lies well off the render's outline (`EXTRA_MAX`: the umbrella on the other side, or
raised where the render has it low - seen from behind the model swaps the hands). A frame that is only a little off (a lower overlap,
the pose right) is listed, not redrawn: show the user those frames beside their renders and let them choose; `redraw --low` redraws
them too. **The prompt** names the action only (`words`) and leaves the pose to the renders (`pose`: each cell one moment, the arm and the
held thing where its render has them) - moves spelled out ("raise it overhead, swing it down") had it drawn overhead where the render
has it at the side. Each cell gets the held thing's place in its render; where the body hides it (seen from behind) the cell says so and
not to draw it, and the checks count only the part that shows. **A held thing is described part by part** (`"hold": {"kind": ..., "words": "..."}`
overrides the built-in sentence): each part, its colour, and what it must not turn into - above all the end AT THE HAND (a handle, a hilt, a
grip). That end is small, half under the fingers and against the body, and it is where the image model guesses: an umbrella's silver shaft
came out brown on one sheet, the two fists moved together and the gap filled with handle. "As the render shows it" is not enough there;
"a dark brown handle in the fist, then a bare silver shaft as long as the render has it, never brown, the hands as far apart as the render"
was right on the first drawing. When a user points at a held thing whose colour or shape changes between frames, fix the words, then
`draw --only <action>` for the sheets moved aside (reference/character.md). A thin thing drawn a few degrees off misses its render's pixels: one
pointing the same way (within 25°) from the same side passes. The rain girl's run and jump fit at 0.78+ in every frame on the
first drawing; the slash's lower frames are mostly deep bends drawn a touch upright - fine in motion: show them beside their renders and
let the user keep them or redraw. When a frame is still wrong, show it beside its render before redrawing.

## Other sizes
Frames come out 256 px tall (`"frame_px"`); the finished frames in `frames/` keep the drawings' detail (rendered at `"render_px"`
1024 - a project rendered before at 512 keeps it until `render_px` is set and `render` + `finish` run again, nothing redrawn), so
bigger stays sharp too. Only when the user asks for another size: `charpipe.py pack
CHAR.json --px <height>` (free, nothing redrawn) → `out-<height>px/` with its own strips, shadows and character.json; `out/` is left as
it is.

## Pixel-art sprites (arcade size) - details in [reference/pixel.md](reference/pixel.md)
When the game is drawn in pixels (a belt-scroller, a fighter, an arcade game) or the user asks for pixel art. Not a filter over the
illustrated frames: the 3D renders are pixelized into a guide, the image model redraws the guide as pixel art, and the answer is read
back onto the grid it was drawn on - so it needs the renders only (`render`; the illustrated `draw` is not needed for this).
`PYTHON pixelart.py CHAR.json` prints the plan and the cost and spends nothing; `--yes` draws (~$0.075 a sheet; a walk is 2 sheets a
facing, 3 for a side view; an action with something held 4). Offer 96 px (`--px`; the image model's "pixels" do not get smaller, so
128 comes out about 104 - say so). **64 px only for a character designed small** (about three heads tall, its own 3D model:
reference/pixel.md "Sizes") - and **never less than 64 asked of the image model**: `--px 32` draws at 64 and makes the 32 set from it;
say that 64 is the one that comes out well. One facing of one animation first, as the sample: show `out-pixel96/preview.gif`, then the rest.
Every run ends with its review (`REVIEW: N of M frames to look at`: a pose unlike the render's - overlap under `redo_below` - or the
held thing missing, left in the hand after the release, or drawn in a frame where the figure hides it - a ball in the far hand or behind
the head): show the user `review.png` (each marked frame beside its guide), not every frame;
`--redraw` says what drawing those sheets again would cost, `--redraw --yes` does it and keeps the better; `--again <sheet>` redraws one sheet. **Fewer colours or the game's own palette**: `--colours N` / `--palette NAME|FILE` (free, also on `proppixel.py`; `--palette list` shows the 15 that come with the skill; reference/pixel.md). Out: `<clip>-<facing>.png` strips, `shadows/`
(each frame's 3D shadow), `pixel.json`. **By hand, for what is left** (white between an arm and the body, a face in one frame): `PYTHON pixeledit.py CHAR.json` - a local page
(a server: run it in the background, give the address) to erase a patch, draw, or copy a good face into another frame; the edits are
kept and laid on again by every later `pixelart.py` run. Animations a game plays one after another (walk > ready > slash > recover):
`pixeledit.py CHAR.json --join walk,ready,slash,recover --facing south-east` shows them as one, to be played through and fixed where
a part jumps - each edit goes to its own animation's frame. **Something thrown** (a snowball): `"hold": {"kind": "snowball", "color": "#bcd6f2",
"final": "#ffffff", "until": "auto"}` on the action - drawn pale blue so that it shows on white paper, white in the end, let go when
the hand is fastest; the folder then has the thing's own sprites and `release` in `pixel.json` (frame, point, direction, speed), and
`<clip>-<facing>-flying.gif` to show. **An animation the rig lacks** (a throw): `PYTHON addclip.py CHAR.json Throw.fbx throw` puts a
Mixamo FBX (with or without its character) into a copy of the rig, free, bone by bone BY DIRECTION - render it and look before drawing. Never put a Mixamo file
in a public repository: its animations may be used, not handed on. **Attacks that work together** (free, `PYTHON motion.py`, reference/character.md "Moves that join"):
`ground` puts a carried clip's feet on the ground (a Mixamo clip stood 8-15 cm in the air on a child's rig), `plant` holds them where they
stand, `link SPEC A@t B@t0-t1 NAME` starts move B from the pose A is in - the way a game joins a combo, B's stroke its own - `blade` makes
an axe's chop a sword's cut (less bend, the blade running on from the arm on an arc), `join` makes a combo one clip to render at 24 a
second and look at the joins. A swing's water reaching further: `"trail_reach": 2` in the action (the frame renders bigger; free). Ask for Mixamo moves of one set (one actor: "Standing Melee Attack ...") - they start and end in one stance. **No moves come with SpriteCast - only the changes made to them.** Asked for a combo like Rain Girl's: `PYTHON motion.py preset SPEC.json rain-girl-combo [--fbx DIR]` (presets/rain-girl-combo.json: Mixamo's two moves carried on, then the same blade, ground and link with the same numbers, and the two actions in the spec - checked against the game's rig: within 3 mm). It needs the user's own downloads - give the user each move's `url` from the preset's `needs` (a Mixamo search for that move: one click to see it playing and download it) and say what to download: on mixamo.com (free, an Adobe account) `Standing Melee Attack Downward` and `Standing Melee Attack Backhand`, each as FBX Binary, 30 fps, Without Skin, keyframe reduction none - then the recipe in reference/character.md ("A combo"); Mixamo's moves may be used, not handed on. **Standing still**: SpriteCast's own idle is the default (`idleclip.py`; `"idle_from": "tripo"` for Tripo's).

**Effects for the game round the sprites** (free, nothing drawn, reference/pixel.md "Effects from the pack"): 253 pixel effects of PVFX
Foundry (CC0 1.0) come with SpriteCast (`effects/pvfx/`) - hits, splashes, fire, explosions, ice, lightning, smoke, sword trails, projectiles,
pickups, status. `PYTHON fxpack.py list --search water`, `preview ID ...` (show the picture), `export ID --out assets/fx --as hit
[--scale 2] [--palette CHAR.json] [--hue 210]` - a sheet and fx.json (cell, pivot, frames, ms) at the sprites' pixel size and, asked, in
their colours. Offer it when a game wants hits, pickups or a finisher's flourish. A swing round the character: `export --set water-swing`
(shockwave ring + ripple + spin) or `--set fire-swing` (flame ring + the spin as fire) - the pairing the user chose, with when and on which layer. A ring round a character is cut at its pivot's line:
the far half behind, the near half in front. Say where an effect came from (the pack's licence: effects/pvfx/LICENSE.txt).

**One angle for everything** (the user's rule, Rain Girl 2026-11-22: "an iso game looks less like AI slop when everything is made at the same iso view"): pickups, items and anything lying in the world - a heart, a potion - are props too, made from a 3D model at the game's camera with their shadow (isoprop.py model, proppixel.py), never front-on icons from a pack beside an iso character; only what is fixed to the screen (a HUD's hearts, a gauge) may be front-on, best from the same 3D model turned to face the camera. Suggest it when a user brings flat icons into an iso game. **The ground** (free, reference/ground.md): `ground.py meadow GROUND.json` - one picture of the whole map's ground: Tripo-made 3D grass, ferns, wildflowers and clover (they come with the skill) planted by a Gaussian density, a path of earth and 3D gravel, lit by the props' sun, in the props' palette, plus strips so the grass hides feet and props' feet (minutes); `terrain` (the ground's rise and fall), `puddles`, `grass2d` (from one tile, no 3D). Never a repeated square tile (the user: its grid and seams showed). For an illustrated (not pixel) game: `"style": "smooth"` in GROUND.json - continuous light and colour, soft-edged strips, gradient terrain and puddles. **A creature that moves** (a ghost's tail and arms): `proprig.py PROP.json` (free: bones from the mesh, a loop of poses rendered - show rig/poses.gif) then `propanim.py PROP.json` (~$0.08 a sheet of four frames; say the cost) -> out-pixel/anim.png (reference/pixel.md); for a smooth prop (finished with isoprop.py, no out-pixel/) or with `--smooth`, the sheet copies its sprite.png -> <prop>/anim.png, soft alpha. **See-through things** (a flame, a ghost, water): `"translucent": "fire" | "ghost" | "water"` in the prop's spec - alpha from its 3D model's thickness, free, after drawing (`"style": "smooth"` or `--smooth`: continuous alpha, not steps; `translucent.py`, presets/translucent.json; reference/pixel.md). **A prop as pixel art** (`PYTHON proppixel.py PROP.json`, reference/pixel.md "Props as pixel art"): the prop's guide pixelized and redrawn the same way, at the
pixel character's pixels per metre (`--ppm` = its `figure_px` / its `height_m`) so they stand on one floor. One view of a simple thing works from blocks. **From
several sides the guide must be a 3D model** (`isoprop.py model`, ~20 Tripo credits: say the cost and wait) - from blocks the image model cannot tell which face has
what on it. Show `out-pixel/preview.png` beside the renders. With a model, its **shadow** is baked from it by itself (free): show
`out-pixel/preview-shadow.png`; for a rainy or grey scene offer `--shadow overcast` (or `propshade.py PROP.json --weather overcast`, no drawing); the shadow is 1.5 times as deep as the light gives it by default (pixel art; a smooth one 1) - if it looks heavy on a light floor offer `--shadow-strength 1`, if it is lost on dark ground 1.6-2 (or `"shadow_strength"` in the spec, or `propshade.py PROP.json --strength K`; free - show both previews and let the user choose); indoors ask where the lamp is
(`--lamp x,y,z --lamp-size r`) or offer `PYTHON lightedit.py PROP.json` (free, 127.0.0.1) - the user drags a lamp round the prop and sees the shadow and the
floor's light as it moves; a lamp of their own (any picture - "Load a picture...", kept in `~/.spritecast/lamps` for every prop; SpriteCast's in `examples/lamps/`) stands
on the floor in front or behind, its light point and foot set by a click on it, scaled 0.05-3x (pixel art stays pixel art), its settings saved with it, deleted in two clicks;
"Bake & save the scene" writes `shadow-<side>.png`, `light-<side>.png` (the floor's light, ADD), `lamp.png` and where it all goes in `pixel.json` for the game. Pixel or
smooth light (`"light_style"`). For wicker, leaves or a net offer `"see_through"` (reference/pixel.md).
**The wind**: for a tree, a bush or a plant offer `"sway": "leaves"` (free) - its leaves cut into clumps from the model, each moving whole a pixel at a time: `sway-<side>.png`
(12 frames x still / breeze / gust), `clumps-<side>.png`, `preview-sway.gif` - show the GIF. A small thing (mushrooms: `"sway": "caps"`) has its parts read off the sprite
instead, lifted as they move - chosen by itself under 700 moving pixels.
**For the game's rules** (free, baked with the shadow): `solid-<side>.png`, where a walker cannot stand (the prop's footprint, cut from the model below 0.4 m), and for
`"collide": {"cover": [0.55]}` `cover-<h>-<side>.png`, what stops a thing flying at that height (a trunk does, the crown over it does not) - show `preview-collide.png`.
Each side's `shadow` in pixel.json says how to **darken a character in its shade** (`per_m_up`, `height_m`). **Into the engine**: `export.py PROP/out-pixel` ->
`export/godot/` (a scene: Light, Shadow, Body that sways, Solid polygon; `shade_at()`, `cover_at()`) and `export/phaser/` (a module: `add()`, `.wind()`, `.solid()`,
`.cover()`, `.shade()`, `shadeOf()`). Unity and Aseprite: not for props yet - say so.

## Sitting (people) - details in [reference/sitting.md](reference/sitting.md)
Offer it once a character walks. 1) `charpipe.py sit CHAR.json` (free): the rig seated in 8 facings, on nothing - show the renders.
2) `sit CHAR.json --draw` (~$0.22, after the user agrees; `--yes`): drawn and finished → `out/sit-<facing>.png` and `"sit"` in
`character.json` (each facing's seat point). 3) On one of their props: `${CLAUDE_SKILL_DIR}/scripts/seat.py PROP.json CHAR.json
--height <m>` (free; ask the character's height): placed on the seat, the prop's front piece for them worked out from both 3D heights
→ `<view>/seat/<char>-<facing>/` (front.png, seat.json, preview.png). Show the preview.

## Into the user's engine
When a character is finished and the user names their engine (or asks for Aseprite files), run
`${CLAUDE_SKILL_DIR}/scripts/export.py <name>/out` (free): `out/export/godot/` (a scene to drop into a Godot 4 project),
`out/export/phaser/` (an ES module for Phaser 3), `out/export/aseprite/` (one `.aseprite` an action, a tag per facing),
`out/export/unity/` (copy its contents into `Assets/`: the prefab and the clips build themselves). A swing's effect goes along as a third
sprite over the body. Pixel sets are not read yet:
for those give the numbers in `pixel.json` as before.

## Touching up by hand - details in [reference/touchup.md](reference/touchup.md)
`${CLAUDE_SKILL_DIR}/scripts/touchup.py SPEC.json` (free) is a local page where the user paints fixes: red clears (paper between the
limbs, a halo), green brings pixels back from the drawing (a white shirt the cut-out took for paper), blue paints a prop's front piece,
⬠ a polygon, 🪑 drags a seated character into place. **It is a server: start it in the background**, give the user the address it
prints, and stop it when they are done; then `touchup.py SPEC.json --apply`. Offer it whenever a cut-out, a front piece or a seat
looks off, and tell the user painting by hand is the most accurate step. Never paint for them without asking.

## Rules
- Spend money only after the user agreed to that amount. Show the free render before any paid step.
- Keep everything in the user's project folder; don't touch other files.
- Real brands, logos and characters from existing games or films: leave them out of descriptions (write "no logos").
- The output is the user's; the bundled `cozy` style picture may be used freely (MIT).

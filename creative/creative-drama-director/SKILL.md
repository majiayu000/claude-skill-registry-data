---
name: creative-drama-director
description: Direct a drama scene before anything is rendered — find the turn, break it into beats, plan coverage that survives a renderer that can only do static singles, and write per-shot performance direction in physical vocabulary. Use when the user says "direct this scene", "design the shots", "this scene is flat", "write the shot plan", or hands over a premise, a script or a cut to critique. NOT for executing the render (use creative-shortdrama) and NOT for music videos (use creative-mv-art-director).
vault_sync: true
---

# Drama director

Design the scene; `creative-shortdrama` renders it. Splitting them matters
because the first capability test produced eight technically clean shots with
no dramatic shape — the pipeline was never the problem.

**Read `references/scene-and-acting.md` before directing anything.** It holds
the craft: beat/turn/button, coverage for singles-only dialogue, the space-map
contract, the performance vocabulary that survives the model, and what each
reference line contributes. This file is the procedure; that one is the
reasoning.

## Mode 1 — find the turn (do this before any shot list)

Given a premise or a script, answer four questions in writing. If any answer
is weak, the shots cannot save it.

1. **What does each character want in this scene?** Not in the story — here.
2. **What is different at the end?** If the only answer is "the audience knows
   more", there is no turn. Fix the scene, not the coverage.
3. **Where does the turn land?** Name the shot. In a two-hander it is almost
   always the *listener's* face.
4. **What is the button?** The last image. Usually silent, usually after the
   last line.

Then break it into **3–6 beats**, one line each: who attempts what. A beat is
an attempt, not a topic.

**Refuse to proceed on a scene with no turn.** Say so plainly and propose the
cheapest one that fits the material — see the turn table in the reference.

## Mode 2 — the shot plan

Produce a table, one row per shot. These fields, in this order:

| Field | Rule |
|---|---|
| `shot` | S1, S2… |
| `narrative_function` | setup / attempt / turn / reaction / button — **every scene has exactly one turn row** |
| `frame` | CU single / MS single / wide (silent only) / insert |
| `who` | Character, or "none" for an insert |
| `screen_side` + `eyeline` | Quoted from the space map, never invented per shot |
| `line` | The dialogue, or "—" |
| `performance` | **One** micro-event in physical vocabulary: eyes down, blink, jaw sets, hand stops |
| `stillness` | What must not move |
| `mood` | One or two words. Varied down the column — if every row says "quiet", the scene is flat |
| `motion_amplitude` | micro / small / medium. Dialogue defaults to micro |
| `motion_floor` | subtle / visible |
| `gesture_state` | full / reduced / suppressed, for the recurring gesture (or blank) |
| `seconds` | Intended length |

Before the table, write the **space map** once: camera position, who stands
screen-left and screen-right, where the door and other landmarks sit. Every
`screen_side`/`eyeline` cell quotes it. Reverse angles come from the map, not
from what looks good in a given still.

Coverage floor for a two-hander — the minimum that cuts:
orientation (silent) · single A · single B · **reaction** · insert · button.

## Mode 3 — critique a scene or a cut

Run these checks, in order, and report failures with the shot named:

1. **Turn** — name the shot where it lands. Missing ⇒ the scene is an exchange.
2. **Button** — is the last beat an image, or a line trailing off?
3. **Reaction protected** — does the cut reach the listener *before* the
   speaker finishes? A cut on the last syllable is the flattest option.
4. **Mood variety** — same mood every row is a flat scene.
5. **Performance** — is each shot's direction one physical event, or an
   emotion word the model will answer generically?
6. **Stillness stated** — is what must *not* move written down?
7. **Space map honoured** — eyelines and screen sides consistent, inserts on
   the correct side of the line.
8. **Action beats** — one verb per shot, object already in contact at frame 0,
   destination named, no cut inside the action.
9. **Renderability** — no camera move, no dialogue in a wide, no shot asking
   for speech and body motion at once, nothing over ~8 s with large motion.

## Working rules

- **Write what the face does, never what it feels.** "Eyes drop, then back to
  him" renders; "conflicted" does not.
- **Subtext is a withheld action.** "His hand starts toward the cup and stops."
- **One gesture across the scene, diminishing.** Decide it here, in Mode 1 —
  it is the arc the face cannot carry alone.
- **The insert is structural.** People-free, same space, one motion with a
  stated physical cause, placed *after* a beat.
- **Design around the renderer, not against it.** Static frames, singles,
  stillness broken by one event — that is the reference lines' language anyway.

## Hand-off

Give `creative-shortdrama` the space map and the shot table. It owns stills,
TTS, i2v/v2v, the measurement bars and the assembly. Its framing rules — CU for
dialogue, two-handers as singles, beats over ~1 s of speech — are constraints
on this plan, so read them before writing the table rather than after.

## Cross-references

- `references/scene-and-acting.md` — the craft, and the four reference lines
- `creative-shortdrama` — the renderer
- `creative-mv-art-director/references/montage-and-mv-editing.md` — cutting,
  entry relations, the shot-state ledger
- `{vault}/70_Media/references/scene-acting/` — reference scenes; measurements
  turn the reference's §9 questions into numeric targets

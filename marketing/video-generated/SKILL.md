---
name: video-generated
description: >-
  Generates people, rooms and objects for a video through Atlas Cloud - the client and key, which
  model for which job (Seedance 2.0 for shots, OmniHuman 1.5 to play your own audio as a talking
  person, MiniMax H3 in reserve, Nano Banana Pro for keyframes and multi-reference edits), prices
  as billed, the doctrine (one scene = one generation; identity, geometry and composition checked
  at image prices; the reference beats the prompt; approved takes are upscaled, not regenerated),
  looping and transparent shots, and assembly traps. An executor under video-studio. Use when a
  film needs shots that do not exist as footage or UI. Triggers: "generate a scene", "a character
  in the video", "people in the ad", "talking head", "Seedance", "OmniHuman", "Atlas Cloud",
  "generated video".
---

# video-generated

Shots that do not exist as footage or UI. Everything spoken, written or branded stays out of
the generated picture: text, captions, UI and the end card are layered on top in
video-build. video-studio's laws apply to the content of every shot.

**Input: the film's `brief.md`** (`../video-studio/references/brief.md`). It owns copy, claims,
tone, material, moments and private data; this skill owns the implementation. If the brief
cannot be met, say so to video-studio - never change it silently.

**Setup.** An Atlas Cloud account with balance and `ATLAS_API_KEY` in
`~/.config/marketing-agent-kit/.env` - how to get one: `references/atlas.md` "Get a key" (and the
kit's `connections/atlas-cloud.md`). Python 3 only, no packages. Every call costs money.

```bash
A=${CLAUDE_SKILL_DIR}/scripts/atlas.py
python3 $A upload keyframe.jpg
python3 $A --jobs <film>/jobs run video shot.json --tag s01 --out <film>/shots
```

`references/atlas.md` holds the client, the model table with billed prices, the doctrine,
looping and transparent shots, and the assembly traps. **On any new model: one paid call, then
read the dashboard, before the second.**

Camera terms for a shot's prompt (one move per shot; term + subject + direction + duration):
`../video-moves/references/prompts.md`.

## Adapt it

- Put your own character sheets, set plates and brand ground colours in your film folder and
  reference them; the model follows the reference, not the prose.
- Re-check every price on your dashboard after the first call of each model, and update the
  table in `references/atlas.md` with the date.
- If you use another provider, keep the doctrine and the traps, and swap `scripts/atlas.py` for
  that provider's client with the same upload / submit / poll / download shape.
- Add your own realism rules (what your customers' world looks like) to video-studio's
  "Brand laws (yours)" - they bind every generated shot.

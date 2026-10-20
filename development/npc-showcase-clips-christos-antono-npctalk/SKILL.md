---
name: npc-showcase-clips
description: Record short clips of NPC conversations that look like real gameplay, ready to post. Covers scripted exchanges at chosen places and times, the gameplay camera held still behind the player, both lines rendered before the clip rolls so it plays back to back, the game's own HUD and subtitles with nothing of the mod on screen, timeline markers for cutting, screen and audio sync, 5-10 s cuts in 16:9 (and 9:16), pinning lines to re-voice an approved take, and re-taking clips that run long. Use when the user wants demo videos, clips or a montage of talking NPCs.
---

# Gameplay-style clips of talking NPCs

What worked for 20 GTA V clips (`examples/gta-v`, `DirectorClips.cs`, `tools/shoot.ps1`, `tools/edit.ts`):
a clip is one exchange, 5-10 s, that could be a moment of someone's ordinary play.

## Script it
```
clip: Water pistol
at: grove                         a street spot, a home, or "x, y, z, heading"
time: 21                          hour of day
a: player                         who speaks first: the player, a character, or a ped model with a voice
b: LamarDavis
line: Lamar, put the gun away. It's a water pistol.
reply: insist it's still scary and he's the most feared man on Grove Street    (the LLM writes it live)
# or pin an approved take:
say: [shouting] Scared of a water pistol? This the most feared shit on Grove Street!
do: none                          the action to play (an action name, or none)
```
NPC-only clips (a cop and a hillbilly, a marine and a tourist) are some of the best: hide the player and let two
NPCs go at it.

## Look like gameplay
- **The gameplay camera, held still:** every frame, set the follow camera's view mode and its heading and pitch
  relative to the player, and disable look input. Fixed is fine; cinematic cameras read as a trailer.
- **Frame the partner:** stand them in front and a little to the side (2 m forward, 1 m right) so the player
  doesn't hide them; raycast around the spot and turn away from walls, kiosks and doorways.
- **Ground them:** snap to pavement, and raycast down for the ground (awnings and roofs fool height lookups).
- **Clean screen:** the game's HUD and subtitles on, nothing of the mod (no notifications, dev panels or help
  text). Suppress phone calls and help text during a take.
- **Render first, then roll:** write the reply, pick the action and render both voices before the clip starts,
  then play them back to back. Nobody waits on camera for a GPU.

## Record, sync, cut
- `shoot.ps1`: brings the game to the front, reloads the mod, records the screen (ffmpeg `ddagrab`) and the PC's
  audio (WASAPI loopback) as separate files, starts the script, and restarts capture if focus is lost (the game
  pauses).
- **Sync:** each capture segment starts with a white flash and a 1 kHz beep logged with a timestamp; the mod
  logs `clip_start`/`clip_end` and every line's `audio_on`/`audio_off` to a timeline.
- `edit.ts --clips <take>`: one MP4 per clip, from 0.2 s before `clip_start` until the last word or action,
  cropped to the game window, 1920 wide, loudness-normalised. It caps clips at 10 s and **reports any line
  that would be cut off**, instead of cutting it.
- **Re-take, don't cut words:** a clip that runs long gets re-shot (new renders come out different lengths) or its
  line tightened by a few words. Pin approved replies with `say:`/`do:` so a re-take keeps the joke.
- **Look before you send:** a contact sheet of one frame per clip (`ffmpeg -ss 5 ... tile=5x4`) catches a
  hidden partner or a wall in the shot in seconds.

## Gotchas
1. **Nothing happens / the mod didn't come back after a reload.** Windows Smart App Control refused the new
   DLL (Code Integrity event 3077). Test-load a new build first; keep the last one that loaded.
2. **The take has no video start in its log.** Another process held the log file open (`tail -F` on Windows
   blocks the writer). Don't watch a file another script appends to; watch a different one.
3. **A phone call or help text lands mid-clip.** Suppress them every frame while a clip rolls.
4. **Voices in clips are clones.** Before posting a clip anywhere, the human decides; say it's AI.

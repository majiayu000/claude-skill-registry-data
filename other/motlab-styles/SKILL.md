---
name: motlab-styles
description: "Ready-made looks for motlab videos: rules in numbers for shots, transitions, camera, easing, text and sound, with a template. Use only when the user asks for a style, names one from this skill, asks which styles there are, or wants the look of a reference video written down as a style. Never a default. The motlab skill builds the video; this one only sets the look."
---

# motlab-styles

The motlab skill knows the engine and how to work: the brief, the references, the shot plan, the page contract, the
viewer, notes and export. It does not choose a look. A look comes from the user's references, from another skill the
user has, or from a style in this folder when the user asks for one. This skill never installs, renders or builds
anything itself; the motlab skill does all of that.

## Using a style

1. Read the style's file all the way through before planning. A style changes the shot plan, not only the finish.
2. Copy its template, if it has one, into `<video>/scenes/` next to the motlab skill's scripts it uses.
3. Apply it to every scene, and check its checklist with stills before opening the viewer.
4. The user's material still comes first: their logo, fonts, colours, screens and footage. The style decides how they
   are framed and how they move.
5. With an asset kit, the kit's `style.md` sets how things are drawn and the video style sets how they move. Where the
   two disagree, ask the user.
6. A note from the user beats a rule of the style. Make the change, and say which rule it breaks in case they want the
   rest of the video to follow.

## Styles

| Style | For | Files |
|---|---|---|
| Ad morph | Short product, app and brand ads (8 to 20 s) where every shot grows into the next, with no cuts | `styles/ad-morph.md`, `templates/ad-morph-2d.html` |

## A style from a reference video

When the user gives a video whose look they want:

1. Look at it. A sheet of one frame a second, and the frames around each cut:
   `ffmpeg -i ref.mp4 -vf "fps=1,scale=480:-1,tile=6x10" -frames:v 1 sheet.jpg`, and
   `ffmpeg -i ref.mp4 -vf "select='gt(scene,0.3)',scale=480:-1,tile=6x4" -fps_mode vfr -frames:v 1 cuts.jpg` for the cuts.
   `ffprobe` gives its size and frame rate.
2. Write down what it does, in numbers where you can: shot lengths; how each shot changes (a hard cut, which shader
   transition, a shape carried across, a wipe); camera moves and how they ease; text (kind of typeface, size against
   the frame height, how it comes in and goes out, how long it stays); colours; finish (grain, blur, shadows, glow);
   and where the sound hits.
3. Save it as `<video>/style.md`, in the same sections as `styles/ad-morph.md`, and build from it.
4. Only when the user wants it for other videos too, add it to this folder as `styles/<name>.md` with a line on where
   it came from, and add a row to the table above.

A style is how things are framed and move. It does not copy someone else's footage, artwork, characters or campaign
lines, and it is not a way to pass a video off as a brand's own.

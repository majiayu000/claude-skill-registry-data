---
name: color-grading
description: Color grading video in the AI Edit Video system - delog/tonemap HDR-HLG-log footage, apply the color preset the user approved in the UI, and the visual verification workflow. Read when the edit prompt has a "Chỉnh màu" (color grading) section, when the source footage is HDR/log, or when the user asks for grading/delog.
---

# Color Grading - grading video footage

## Rule #1: the preview IS the final result

The user already APPROVED the color in the web UI based on a preview generated from the canonical filter chains in
`apps/server/src/color.ts` (`GRADE_PRESETS`). When applying it to the real video you MUST use **that exact filter chain**
- do not invent your own, do not "improve it further". A different chain = a color that no longer matches what the user picked.

## Source of truth for presets + manual adjustments

Read `apps/server/src/color.ts`:
- `GRADE_PRESETS` - 14 color templates (tu-nhien, tuoi-sang, vivid, cinematic, teal-orange,
  film-vintage, mau-phim, golden-hour, am, lanh, dem-xanh, moody, pastel, den-trang) with their -vf chains.
- `GradeAdjust` - the user's manual tweaks stacked ON TOP of the preset (brightness/contrast/
  saturation/gamma via `eq`, `colortemperature`, `vibrance`); the `buildFilterChain(preset, tonemap, adjust)` function
  assembles them in the correct order: tonemap -> preset -> manual adjustments.
- The edit prompt already prints the complete -vf chain for each asset - JUST USE IT VERBATIM.

## Delog / HDR tonemap (insert BEFORE the preset)

Inspect the footage with ffprobe:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer,color_primaries -of csv=p=0 input.mp4
```
If `color_transfer` is `arib-std-b67` (HLG - iPhone/Android HDR capture) or `smpte2084` (HDR10),
or `color_primaries` is `bt2020` -> insert the tonemap BEFORE the preset:

```
zscale=t=linear:npl=100,tonemap=hable:desat=0,zscale=p=bt709:t=bt709:m=bt709:r=tv,format=yuv420p
```

Professional camera log (S-Log3, D-Log, V-Log...) whose metadata does not declare HDR needs the vendor's `.cube` LUT -
if that LUT is not in the system, tell the user instead of guessing.

## Workflow for grading one video

1. Probe the color (command above) -> decide whether a tonemap is needed.
2. Produce the graded version (high quality encode, audio untouched):
```bash
ffmpeg -y -i assets/source.mp4 -vf "<tonemap-if-needed>,<preset-chain>" -c:v libx264 -crf 16 -preset medium -c:a copy assets/source.graded.mp4
```
3. **Visual verification (mandatory)**: extract 3 frames (start / middle / end) of the graded version and LOOK at each one:
   are skin tones natural and not blown out orange? are highlights not clipped? are blacks not crushed? If something is
   wrong -> report back, do NOT silently change the filter (the user locked in the preset).
4. Use the `.graded.mp4` version throughout the ENTIRE pipeline instead of the original (meta.json srcVideo; transcription
   can use either file since the audio is copied unchanged).
5. Record in the asset description (assets.json) which preset was used to grade it, so it does not get graded twice later.

## Known issues

- **Grading twice**: the `.graded.mp4` gets the preset applied again in a later session -> harsh color. ALWAYS check the
  filename and assets.json before grading.
- **Grading only the main video and forgetting b-roll/inserted images**: inserted images usually do not need grading
  (they are graphics), but b-roll shot on the same camera needs the same preset - check the asset descriptions to know
  which files came from the camera.
- **Missing `format=yuv420p` at the end of the tonemap chain** -> the output is 10-bit and HyperFrames/browsers may not play it.

---
name: screenshot-review
description: Review image shots (screenshots, snapshot baselines, montages, renders) two ways — critique mode spawns an unprimed sub agent as a second set of eyes, MANDATORY before declaring any user-reported visual bug fixed or claiming a visual change verified; preview mode opens shots in ONE macOS Preview window when the user asks to open / show / pull up / review shots, or right after producing visual artifacts the user should eyeball before signing off.
---

# Screenshot Review

Two modes for putting eyes on visual artifacts. Pick by audience:

- **Critique** — agent eyes: spawn an unprimed sub-agent to find defects before
  you accept visual work. Mandatory before declaring a visual bug fixed.
- **Preview** — user eyes: open the review-worthy shots in a single macOS
  Preview window so the user can flip through them.

They compose: run the critique first, then preview the surviving candidate
shots for the user's sign-off. This skill is for visual defects and human
review, not pixel metrics; pair with `compare-screenshots` when you also need
numbers.

## Critique mode

Use an unprimed sub-agent as a second set of eyes before accepting visual work.

### Workflow

1. Capture or locate the exact PNGs/GIF frames under review.
2. Create tight 2x-4x crops for every key feature under judgment, plus the full
   screenshot for context. Crop selected units, city/town stacks, flags/poles,
   shadows, selection rings, labels/icons, roads, terrain features, water, and
   any artifact-prone area. If the complaint is about "too faint", "wrong
   order", or "not in perspective", the crop is mandatory.
3. Spawn one fresh explorer with `fork_context: false`; pass only the full
   images, the crops, and a short neutral task. Do not include the main thread
   history, implementation details, or expected answer.
4. Ask for concrete visible defects with confidence levels. Name likely risk
   categories: unit/prop depth ordering, layering, shadows, selection-marker
   contrast, ground-plane perspective, flag/pole attachment, label style and
   icon readability, blur, scale, lighting, artifacts, missing models, terrain
   feature readability, roads, water, and overall scan readability.
5. Compare the sub-agent's critique against your own inspection. Treat overlap
   as high-priority evidence. Treat novel high-confidence findings as bugs to
   inspect, not as taste notes to dismiss.
6. Record actionable findings in the spec, visual report, or next task plan
   before claiming the screenshot is accepted.

### Sub-Agent Prompt

Use this shape, replacing the bracketed surface and attaching local images:

```text
Fresh visual critique task. You have no project backstory and should only
inspect the supplied screenshots and crops. First inspect the full screenshot
for context, then inspect each crop at zoomed scale. Look for concrete
visual/layout defects in [surface], especially unit/prop depth ordering,
layering, shadows, selection-marker contrast, ground-plane perspective,
flag/pole attachment, label style/icons, blur, scale, lighting, artifacts,
missing models, terrain feature readability, roads, water, and scan
readability. Do not assume these are correct. Return a concise list of issues
you can see, with confidence and whether the issue is visible in the full image,
the crop, or both.
```

Spawn config:

- `agent_type`: `explorer`
- `fork_context`: `false`
- attach screenshots as `local_image` items
- omit model overrides unless the user explicitly requests one

### Critique rules

- **Mandatory before "fixed":** never declare a user-reported visual bug fixed
  on your own inspection — your eyes are primed by the fix you just made. Run
  the unprimed critique on the candidate shot first; "mild residue" you are
  tempted to wave through is exactly what it exists to catch. (Recorded
  failure: a "fixed" sky that an unprimed agent identified as the terrain
  mesh's underside filling the entire sky region.)
- **Reproduce the reporter's framing.** When the user supplied a screenshot,
  the critique must include a capture at that framing (same camera/zoom/spot,
  or as close as reproducible) — a defect that lives at their framing can be
  invisible at yours. Your chosen probe framing is a supplement, never the
  substitute.
- **Prove the change is real before critiquing it.** Byte/pixel-diff the
  candidate against the pre-change baseline first: a critique of an unchanged
  image "verifies" a no-op. (Recorded failure: a palette pass that never
  reached the production render path — before/after were byte-identical and
  only the diff caught it.)
- Never tell the sub-agent the defect you expect it to find.
- Use the current candidate screenshot, not a stale report or baseline image.
- Do not rely on full-page report scale for small visual features. Attach
  crops around the exact features a player would read: selected army/city,
  label/icon clusters, flags, shadows, ring edges, road crossings, terrain
  feature patches, water labels, and suspicious debug/artifact regions.
- If the sub-agent says a crop reveals an issue that is weak or invisible in
  the full shot, treat it as a real usability defect when the player can zoom
  to that scale in-game.
- For animation, attach a short set of deterministic still frames first; GIFs
  are useful for human review, but still frames make specific defects easier to
  name.
- A passing sub-agent critique does not replace direct inspection by the main
  agent or screenshot regression gates.
- If the sub-agent catches an issue the main agent missed, add that failure mode
  to the relevant feature plan or visual checklist immediately.

## Preview mode

Put the review-worthy images in front of the user in a single Preview window
they can flip through.

### Workflow

1. **Curate the set** — the images that answer "is this right?": the
   just-changed or just-blessed baselines, the integrated result, and the
   reference image when there's something to compare against. Don't dump every
   PNG in the folder; pick the smallest set that lets the user judge the
   change. If the user named specific shots, open exactly those.
2. **One window** — open them with a single `open -a Preview <path> <path> ...`
   call. One `open` invocation lands all the files in one window with a
   thumbnail sidebar; separate calls spawn separate windows.
3. **Caption them** — list one line per shot (what it is) so the user knows
   what they're flipping through.

### Preview rules

- macOS only (`open`); pass absolute or repo-root-relative paths.
- Order the files most-important-first; the first one is what Preview shows on open.
- Review saved PNG/GIF artifacts, not live Chrome. Exact regression capture
  should run headless by default; only open Chrome when the user explicitly asks
  for a live browser or when reproducing a headful-only bug.
- **One set at a time — never pile up windows.** Before opening a new set, close
  any open ones: `osascript -e 'tell application "Preview" to close every window'`.
- **Close on unattended proceed.** When you opened shots for a non-blocking review
  and then move on without the user's response, close Preview afterward:
  `osascript -e 'quit app "Preview"'`. An overnight autonomous run must never wake
  the user to a wall of Preview windows — at most one set open, and none once
  you've proceeded past the checkpoint.

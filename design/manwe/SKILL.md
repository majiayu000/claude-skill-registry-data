---
name: manwe
description: Use when a built UI component or screen needs weighing against what it should be — whether phrased as /manwe <target> [<spec>], or in plain words such as "does this look right", "check this against the mockup", "review the render". <target> is the built page or app view to weigh (a served http(s):// URL, or a Flutter app already running on a booted emulator/simulator — captured via feanor-flutter-shot, never auto-launched). <spec> is optional — a PNG, or an HTML page/URL rendered to one, or a Henneth-approved wireframe from the same working session. With a spec, shoots the target once and names the perceptual deltas against it, the same oracle Fëanor uses. Without one, reads the target's source beside at least one sibling component (same screen or widget family) and flags divergence in layout properties — padding, spacing, sizing, typography. A single pass, never a loop, and it never edits source — findings only. Reuses Fëanor's shot hooks; never launches a browser tab or a device itself.
purpose: Weighs a built UI component's render against a spec, or against a sibling's actual values when no spec exists, and reports findings without editing source.
user_invocable: true
stage: forge
composes: narya:dispatch
---

# Manwë

Farthest-sighted of the Valar, who from his throne on Taniquetil sees furthest
and clearest. This skill does not mend what it sees, as [Fëanor](../feanor/SKILL.md)
does — it only looks, and says plainly what does not match.

## What it needs

- **`<target>`** — the built page or app view, as a **browser-loadable URL** (a
  running dev server, a Henneth-served page, a `file://` URL) or a **Flutter app
  already running** on a booted emulator/simulator. You boot the device and
  navigate to the target screen; Manwë only captures it.
- **`<spec>`** (optional) — the ideal to weigh against: a **PNG**, an **HTML
  page/URL** (shot to a PNG first), or a Henneth wireframe already sitting in
  `~/.skadi/henneth/` from the same session's *Previews* step. Absent a
  spec, Manwë falls back to the sibling comparison below.

## With a spec

1. Resolve the spec image once — copy a PNG as-is, or shoot an HTML/URL spec —
   exactly as Fëanor's *"Resolve the spec image once"* step does, into
   `~/.skadi/henneth/manwe-spec.png`.
2. Shoot `<target>` once into `~/.skadi/henneth/manwe-shot.png`, via
   `feanor-shot.sh` (web) or `feanor-flutter-shot.sh` (Flutter). If the hook exits
   non-zero, stop and fail loud — there is nothing to weigh. For a Flutter target
   whose source has moved since the app was last reloaded, reload it first
   (`~/.claude/hooks/flutter-daemon.sh reload`, the `/narya` skill) and shoot only
   on a `0` — a verdict weighed against a stale binary is worse than none.
3. Read both images and name the deltas — Fëanor's oracle (*"The oracle"* in
   `feanor/SKILL.md`): perceptual, not pixel diff; color, layout, proportion,
   spacing, presence, typography, ordered by how much each moves the eye.
4. Report `ALIGNED` (no material deltas) or `DELTAS` (the checklist) — one pass,
   no retry, no edit. A `DELTAS` verdict is a finding for the caller to act on or
   name as a knowing exception, not a defect Manwë fixes itself.

## Without a spec

1. Shoot `<target>` once, the same way, for a visual sanity check — obvious
   breakage (overflow, misalignment, a missing element) is worth naming even with
   no spec to measure against. Where an icon and a text share a row, measure both
   ink centres with `feanor-ink-centre.sh`, per Fëanor's *"Judge an icon and a
   text sharing a row by their ink"* rule, and flag a gap over 1 logical px. The
   sibling comparison below reads source values and cannot see this, because
   both boxes can sit centred while the glyphs do not.
2. Find at least one sibling of the component being weighed — another instance of
   the same widget in the same screen, or the same component family elsewhere in
   the working tree. Infer it from the target's source location; ask once if more
   than one plausible sibling exists and they disagree.
3. Read the sibling's actual current source values — not its name or intent —
   for the properties a reader expects to match: padding, margin, spacing, sizing,
   typography. This is the same discipline the Compliance Review's sibling-string
   check already applies to user-facing text, generalized to layout.
4. Report `REASONABLE` (the shot looks sound and no compared property diverges) or
   `DIVERGENT` (name each divergent property, target's value beside the sibling's).

## Notes

- **Single pass, not a loop.** Fëanor mends until aligned or capped; Manwë looks
  once and reports. Chase a `DELTAS` or `DIVERGENT` verdict by editing the source
  and re-running Manwë, or hand the fix to Fëanor when a spec is in hand and the
  loop is wanted.
- **The review reads, it does not write** — same rule as the Compliance Review's.
  A finding is surfaced, never silently patched.
- **Shots land in Henneth** the same way Fëanor's do, newest first, so the target
  and (when present) the spec sit side by side for the eye as well as the model.
- **Headless browser / Flutter requirements** are Fëanor's — see its *Notes* — since
  the same hooks are reused verbatim.

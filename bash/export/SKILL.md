---
name: export
description: >
  Step 7, the last step of the content pipeline. Promotes the newest
  render to outputs/<job>.final.mp4, copies it to ~/Downloads, then
  reclaims regenerable build cache. Use when a job's render (rough cut,
  graphics, captions, or music mix — whichever is furthest along) is
  approved and ready to ship.
---

# Export

## 1. Finalize

```bash
projects/<job>/finalize.sh
```

Picks the most recently modified render in `outputs/` (skipping dotfile
caches like `.roughcut.mp4` and `.transcript.json` — those are
intermediates, not candidates), copies it to
`outputs/<job>.final.mp4`, and copies that to `~/Downloads/<job>.final.mp4`.

If the wrong file gets picked (e.g. an old render is newer on disk than
a fresh one due to a copy that touched mtimes), pass the intended file
explicitly instead of trusting "newest" — check `ls -la outputs/` first
if anything looks off.

## 2. Prune

```bash
projects/<job>/prune.sh
```

Reclaims regenerable cache only: the extracted raw-audio WAV, the
lossless assembled intermediate, and the HyperFrames graphics build
cache. **Never touches `raw/` or `outputs/`.** Safe to run any time
after finalize — everything it deletes is rebuildable by re-running the
relevant script (`build_cutlist.py` re-extracts the WAV;
`assemble_rough_cut.sh` rebuilds the intermediate; `render-part.sh` /
`render-final.sh` rebuild the graphics cache).

## 3. Done

The job is shipped. `hf-graphics/PROJECT.md`'s Status checklist should
be fully checked at this point — if it isn't, that's a sign a step got
skipped, not just a formality.

---
name: unfk-image
description: Strip or fake EXIF/metadata in images to make AI-generated photos look like they were captured by a real camera/phone (un-AI provenance). Use when asked to remove, rewrite, or spoof image metadata, EXIF, GPS location, device model, or timestamps.
category: media
---

# unfk-image

Rewrite an image's metadata so it looks like it was taken by a real device instead of AI-generated. Three modes: **strip** (remove all EXIF/GPS), **fake** (replace with a realistic iPhone/Pixel/Canon/Sony template), and **random** (pick a random *real* device per file, mixed brands). Pixel data is never touched — only the metadata block.

## When to use
- User wants to "un-AI" an image, hide provenance, or make a photo look camera-shot.
- Privacy: scrub GPS/device info before sharing.
- Forensics/testing: inject known metadata to check detector heuristics.

## The tool: `unfk.py`
Located at `C:/Users/Gary/unfk.py`. Uses `piexif` (metadata read/write) and `pillow` (image I/O). Run via `uv run --with piexif --with pillow python unfk.py ...`.

### Commands
```bash
# Strip all metadata from a single file or directory (in place)
uv run --with piexif python C:/Users/Gary/unfk.py /path/to/image.jpg --mode strip

# Fake iPhone metadata on a whole directory (recursive), output to DIR
uv run --with piexif python C:/Users/Gary/unfk.py /path/to/dir --mode fake --device iphone --out /path/out

# Random real device per file, mixed brands (iPhone/Pixel/Samsung/Canon/Sony)
uv run --with piexif python C:/Users/Gary/unfk.py /path/to/dir --mode fake --random

# Put the photos somewhere else entirely (keeps originals intact)
uv run --with piexif python C:/Users/Gary/unfk.py /path/to/dir --mode fake --random --out /path/out
```

- `--mode`: `strip` | `fake` (required)
- `--device`: `iphone` (default), `pixel`, `canon`, `sony`
- `--random`: pick a random real device per file instead of `--device`
- `--out`: output directory; omit to overwrite in place
- Directory input is recursive and only processes `.jpg/.jpeg/.tif/.tiff/.png/.heic`

### Random mode: brand-mixed AND resolution-coherent
`--random` doesn't just pick a random phone — it picks one whose **real sensor can actually produce the image's pixel dimensions**. It reads each file's width×height, then filters out any device whose max photo resolution is smaller than the image. So a 60MP image never gets attributed to an iPhone (48MP) or A7M4 (33MP); it only lands on a Pixel/Canon R5/S23 Ultra/A7RM5 that could have captured it.

Every device also carries coherent specs:
- **Lens model** matches the real body's lens label, not a generic string.
- **Focal length / aperture** are the actual values for that device.
- **Timestamp** falls inside the device's real release-and-usage window (an iPhone 15 Pro never gets a photo dated before Sept 2023).

Verified: 40 images across 8 random trials, zero resolution violations.

### What each mode writes
- **fake**: 0th IFD `Make`/`Model`, ExifIFD `DateTimeOriginal`, `LensModel`, `ImageUniqueID`, plus GPS coordinates (San Francisco by default).
- **strip**: removes all EXIF blocks; leaves a bare, plausible file.

## Verified behavior
Tested on Windows with piexif + pillow: fake writes Make/Model/GPS correctly and round-trips through `piexif.load`; strip clears 0th IFD tags and empties GPS. Pixel data is preserved in both modes.

## Notes / gotchas
- **piexif API**: use `piexif.insert(blob, src, dst)` to write (not PIL's missing `putexif`), `piexif.load(path)` reads a path or bytes, `piexif.remove(src, dst)` strips.
- **Tag namespaces**: `Make`/`Model` live in `piexif.ImageIFD`, not `ExifIFD`. GPS tags are accessed as `getattr(piexif.GPSIFD, "GPSLatitude")` — the module-level `piexif.GPSIFD_GPSLatitude` form does NOT exist.
- **GPS format**: values are rational tuples `(num, den)`; refs are byte strings (`b"N"`).
- HEIC requires `libheif`; if unavailable, fall back to stripping only (metadata removal still works on the container).

## Extending
Add a device by appending to the `TEMPLATES` dict in `unfk.py`. Each entry is `{IFD: {tag: bytes}}` where IFD is `"0th"` or `"Exif"`. Keep Make/Model in 0th, camera details in Exif.

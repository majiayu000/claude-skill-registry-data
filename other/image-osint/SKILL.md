---
name: image-osint
description: Use when extracting intelligence from images on an
  authorized investigation. Covers metadata analysis, reverse image
  search, geolocation from visual clues, and authenticity checks.
  Also use when a photo needs verification before it informs a
  decision.
version: 1.0.0
domain: osint
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [osint-methodology, social-media-osint, domain-osint]
tools:
  - name: Python
    version: "3.12"
---

Images carry metadata, locations, and history: EXIF with GPS, visual
landmarks, and copies across the web. This skill covers the
authorized OSINT method: extracting metadata, searching by image,
geolocating from clues, and checking authenticity. Work on images
you are authorized to analyze, and respect privacy and platform
terms.

## Quick Workflow

1. Preserve the original: hash it before any processing.
2. Extract metadata: EXIF, GPS, device, and timestamps.
3. Reverse image search: find where else it appears and the
   earliest copy.
4. Geolocate from visual clues: landmarks, signs, vegetation, and
   shadows.
5. Check authenticity: signs of manipulation and consistency.
6. Corroborate: does the metadata agree with the visual evidence.
7. Document sources and confidence per claim.
8. Handle personal data in images per policy.

## 1. Metadata extraction

```bash
# Hash first, then extract
sha256sum /tmp/osint/photo.jpg | tee /tmp/osint/photo.sha256
exiftool /tmp/osint/photo.jpg | head -40
# Key fields: GPSPosition, CreateDate, Make/Model, Software
```

```python
#!/usr/bin/env python3
"""EXIF GPS extractor (Pillow as tooling, or exiftool output)."""
print("if GPS present: plot it, but verify against visual clues")
print("if absent: social platforms strip EXIF; check the original source")
print("timestamps: compare CreateDate vs GPS timestamp vs file dates")
```

## 2. Reverse search and geolocation

```bash
# Reverse image search engines (manual, authorized use):
# - TinEye, Google Lens, Yandex Images: upload and compare
# - look for: earliest publication, other contexts, cropped variants
echo "record: first seen date, distinct contexts, any contradictions"
```

```bash
# Geolocation checklist from visual clues:
# - text on signs: language, place names, phone formats
# - architecture and vegetation: region indicators
# - sun angle and shadows: hemisphere and rough time
# - license plates, street furniture, shop brands
# Verify with map imagery before claiming the location
echo "confidence: tentative until map confirmed"
```

## 3. Authenticity checks

```bash
# Error level analysis and metadata consistency (as indicators, not proof)
# - ELA highlights differing compression (possible edits)
# - check: does the lighting direction match across the scene
# - check: do reflections and shadows agree
echo "no single test proves fake; converge multiple indicators"
```

## Edge cases

- Metadata stripped. Work from pixels only; say the metadata was
  absent.
- AI generated images. Look for the classic artifacts, and check
  provenance standards (C2PA) where present.
- The image shows private individuals. Minimize exposure and follow
  policy on personal data.

## Escalation

- High stakes verification (news, legal): get a second analyst and
  document the full chain.
- Need video: apply the same method frame by frame, plus audio
  clues.

## Detection and defender view

For investigators, image OSINT detects fraud, verifies claims, and
attributes activity. For defenders of organizations, it means
monitoring for leaked photos of facilities and documents. The
durable practices are provenance (hash originals), corroboration
(never one source), and humility about confidence levels.

## Key references

- EXIF standard and exiftool documentation.
- Geolocation verification methodology (Bellingcat style guides).

## See also

- `osint-image-geolocation`: Use it instead for location-only depth, including EXIF and GPS extraction, landmark analysis, and sun and shadow analysis.
- `ctf-osint-challenges-image-geolocation`: Use it instead for the competition version, framed around locating a photo to find a flag.

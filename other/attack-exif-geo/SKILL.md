---
name: attack-exif-geo
description: "EXIF geo data not stripped — extract GPS and metadata from uploaded images for privacy leakage"
category: "information-gathering"
version: "1.0"
author: "bountyreper-official"
tags:
  - exif
  - privacy
  - metadata
tech_stack:
  - web
cwe_ids:
  - CWE-200
chains_with:
  - wstg-info-02
prerequisites: []
---

# EXIF Geo Data Not Stripped

## Objective

Check if uploaded images retain EXIF metadata (GPS, device, timestamps).

> **Attribution:** Methodology from [KathanP19/HowToHunt — EXIF_Geo_Data_Not_Stripped](https://github.com/KathanP19/HowToHunt/tree/master/EXIF_Geo_Data_Not_Stripped). Licensed GPL-3.0.

## Testing Methodology

```bash
# Upload image with GPS EXIF
exiftool -GPSLatitude="37.7749" -GPSLongitude="-122.4194" test.jpg
curl -X POST https://target.com/upload -F "file=@test.jpg" | grep -o '"url":"[^"]*"'

# Download and check retained EXIF
curl -s https://target.com/uploads/test.jpg -o out.jpg
exiftool out.jpg | grep -i "gps\|make\|model\|create date"
# Or use exiftool online: https://exiftool.org/

# Also check: profile pictures, document uploads, avatar
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| GPS coordinates retained | Medium (P3) |
| Device info retained | Low (P4) |

## References

- [HowToHunt — EXIF Geo](https://github.com/KathanP19/HowToHunt/tree/master/EXIF_Geo_Data_Not_Stripped)

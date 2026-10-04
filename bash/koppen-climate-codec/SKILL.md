---
name: koppen-climate-codec
description: Use this skill when you need to derive a Koppen-Geiger climate label from input latitude and longitude, then convert between the letter code such as `Csa` and the EcoSIM-style numeric code such as `34`.
---

# Koppen Climate Codec

## Use When

Use this skill when:

- the user gives a latitude and longitude
- you need a Koppen-Geiger climate label such as `Csa` or `Dfb`
- you need to convert between letter codes and numeric codes used by EcoSIM-style workflows

## What this skill does

- Derives a Koppen climate label from input coordinates
- Encodes the letter label to the numeric code
- Decodes the numeric code back to the letter label
- Returns a normalized JSON-shaped result for downstream tools

## Required behavior

1. Validate the input coordinates.
2. Derive the Koppen letter code from the latitude and longitude.
3. Convert the result using the bundled codec mapping.
4. Return both forms:
   - `koppen_letter_code`
   - `koppen_numeric_code`
5. If the coordinate lookup is approximate rather than exact, say so clearly.

## Lookup workflow

There is no local Koppen raster bundled in this project, so derive the climate label in this order:

1. If the user provides a known Koppen label already, skip directly to encoding or decoding with the bundled script.
2. If a local workflow later provides a site metadata object with `climate_code`, use that value and encode it.
3. Otherwise, use web lookup to identify the Koppen label for the coordinates.

For web lookup:

- prefer a direct coordinate-based Koppen lookup source
- if a direct lookup is unavailable, use a credible interactive Koppen map and nearest-point interpretation
- record that the result came from an online lookup

## Codec script

Use the bundled script for code conversion:

```bash
python3 scripts/koppen_codec.py --letter Csa
python3 scripts/koppen_codec.py --numeric 34
python3 scripts/koppen_codec.py --latitude 38.8951 --longitude -120.6328 --letter Csb
```

The script does not derive the climate label from coordinates by itself. It validates coordinates and converts codes using the project mapping. The latitude and longitude are included in the output payload when provided.

## Mapping rules

- Letter code example: `Csa`
- Numeric code example: `34`
- Preserve canonical capitalization from the bundled mapping
- Treat numeric codes as strings in output JSON

## Output shape

Return a JSON object with:

- `latitude`
- `longitude`
- `koppen_letter_code`
- `koppen_numeric_code`
- `lookup_source`
- `confidence_note`

## Bundled references

Read [references/koppen_mapping.md](references/koppen_mapping.md) when you need the canonical mapping table.

## Notes

- This skill handles conversion deterministically with the bundled script.
- Coordinate-to-label derivation is currently web-assisted because no local raster or API dataset is bundled in the project.

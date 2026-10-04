---
name: privacy-masking
description: Mask sensitive visual data in video evidence such as faces, license plates, phone numbers, and doorplates. Use when Codex has an evidence image URI, sensitive_regions, or privacy_masking config and needs a masked URI before exposing snapshots or clips externally. This skill exposes OpenCV image read/write and Gaussian blur masking for real files.
---

# Privacy Masking

## Execution Priority

Prioritize calling this skill's `scripts/run.py` entrypoint first. Only write custom code after the script result is unsuitable or the script cannot cover the requested task.

## Input Resolution

If an evidence image URI is missing but the user provided an event or video analysis request, do not write custom masking code. First call `evidence-snapshot/scripts/run.py` to create snapshot evidence, then call this skill on the resulting evidence URI when masking is required.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python privacy-masking/scripts/run.py --image-uri <image.jpg> --sensitive-regions-json <regions.json> --config <config.json> --output <masked.json>
```

Parameters: `--image-uri`, `--sensitive-regions-json`, `--method`, `--disabled`, `--config`, `--output`.

## Workflow

1. Read evidence URI and configured mask types.
2. Locate or accept sensitive regions.
3. Apply configured blur, mosaic, or solid mask.
4. Return masked URI, mask status, regions, and method.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `uri` or `image_uri`
- Optional `sensitive_regions`: list of bboxes or region dicts
- Optional `output_key` for memory storage mode

## Outputs

Returns `uri`, `privacy_masked`, `masked_regions`, and `method`.

## Failure Modes

- `MISSING_URI`
- `IMAGE_READ_FAILED`

## Constraints

Do not delete original evidence needed for traceability.

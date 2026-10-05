---
name: keria-plus-pickup
description: Use when redeem-code pickup from plus.keria.cc.cd needs to be automated into a downloaded ZIP and an unpacked local directory, with an explicit choice between plus_json and sub2api output bundles.
---

# Keria Plus Pickup

Use this skill to automate bulk pickup from `plus.keria.cc.cd`.

The site frontend posts a multipart form directly to `/pickup` and the response
body is already the ZIP file. There is no extra signed download URL step in the
basic pickup flow.

## When To Use

- You already have valid pickup codes.
- You want a local ZIP plus an unpacked directory.
- The target site is `plus.keria.cc.cd` or a compatible deployment.

## Required Operator Confirmation

Before any real pickup, confirm these two inputs with the user:

1. Which local directory should receive the ZIP and unpacked files.
2. Which bundle format is required:
   - `plus_json`
   - `sub2api`

## Request Shape

Required form fields:

- `codes`
- `output_format`
- `progress_id`

Supported output formats:

- `plus_json`
- `sub2api`

## Helper Script

Show help:

```bash
bash skills/keria-plus-pickup/scripts/fetch_pickup_bundle.sh --help
```

Typical use:

```bash
bash skills/keria-plus-pickup/scripts/fetch_pickup_bundle.sh \
  --codes-file /path/to/codes.txt \
  --output-dir /path/to/output \
  --output-format plus_json
```

With explicit base URL:

```bash
bash skills/keria-plus-pickup/scripts/fetch_pickup_bundle.sh \
  --base-url https://plus.keria.cc.cd \
  --codes-file /path/to/codes.txt \
  --output-dir /path/to/output \
  --output-format sub2api
```

Dry run:

```bash
bash skills/keria-plus-pickup/scripts/fetch_pickup_bundle.sh \
  --codes-file /path/to/codes.txt \
  --output-dir /path/to/output \
  --output-format plus_json \
  --dry-run
```

## Output

The script writes:

- `pickup-<format>.zip`
- `pickup.headers.txt`
- `unpacked/`

If the archive contains `取件结果.txt`, read it first to confirm success and
failure counts.

## Notes

- The script sends browser-like `Origin`, `Referer`, and `User-Agent` headers.
- One line per code is preferred.
- Do not assume the format; pass `--output-format` explicitly.

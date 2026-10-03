---
name: callesnikov-qrify
description: Generate professional QR codes locally into the current working directory. Use when Codex needs to create PNG or SVG QR codes for links, text, contacts, Wi-Fi strings, event payloads, branded color schemes, high error correction, batch QR generation, scan-safe validation, filename cleanup, or styled QR codes with solid colors, gradients, quiet zones, and custom output names.
---

# Callesnikov QRify

Use this skill to generate scan-safe QR codes from URLs or arbitrary text while saving outputs to the current task directory, not inside the skill folder.

## Core Rule

Always write QR output to the current working directory unless the user explicitly provides another output path. The skill folder only stores reusable scripts and optional local dependencies.

Primary script:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-qrify\scripts\qrify.py" "https://example.com" --output "example-qr.png"
```

## Dependency Check

The script needs Python packages `qrcode` and `Pillow`. Before first use in a new environment, run:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-qrify\scripts\qrify.py" --self-check
```

If `qrcode` is missing, install it locally into the skill folder, not globally:

```powershell
python -m pip install --target "C:\Users\User333\.codex\skills\callesnikov-qrify\tools\python" "qrcode[pil]"
```

After installing, rerun `--self-check`.

## Defaults

Use conservative scan-safe defaults unless the user asks for a specific style:

- error correction: `H` for maximum robustness, especially with styling or gradients
- border: `4` modules minimum
- box size: `16` for normal PNG output, larger for print
- format: infer from `--output` extension, default to PNG
- foreground: black
- background: white

Do not use low contrast, transparent backgrounds, or a border below `4` unless the user explicitly accepts the scan risk.

## Color And Gradient Guidance

For plain QR codes, use `--fill` and `--back`.

For styled PNG QR codes, use:

```powershell
--gradient "#ff8fb3" "#8ec5ff" --back "#5C4033"
```

Prefer gradients only on QR modules, not on the quiet-zone background. Keep a strong luminance contrast between the darkest foreground modules and the background. When the user asks for a decorative or branded QR, keep error correction at `H`.

SVG output supports solid foreground/background colors. For gradients, use PNG unless the user specifically asks for SVG and accepts a simpler solid-color result.

## URL Handling

For links:

- trim surrounding whitespace
- preserve query strings and fragments
- do not shorten URLs unless the user explicitly asks
- if a domain-like value lacks a scheme, add `https://` only when the user clearly intended a web URL
- keep non-URL payloads unchanged, including Wi-Fi strings, vCards, calendar payloads, and plain text

## Common Commands

Simple QR:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-qrify\scripts\qrify.py" "https://example.com" --output "qr.png"
```

High-resolution print QR:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-qrify\scripts\qrify.py" "https://example.com" --output "qr-print.png" --box-size 32 --border 4 --error-level H
```

Soft gradient QR:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-qrify\scripts\qrify.py" "https://example.com" --output "qr-gradient.png" --gradient "#ff9ec7" "#8fd3ff" --back "#5C4033"
```

SVG QR:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-qrify\scripts\qrify.py" "https://example.com" --output "qr.svg" --format svg --fill "#111111" --back "#ffffff"
```

Batch from a JSON list:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-qrify\scripts\qrify.py" --batch "qr-batch.json"
```

Batch JSON shape:

```json
[
  {
    "data": "https://example.com",
    "output_path": "example.png",
    "error_level": "H",
    "box_size": 16,
    "border": 4,
    "fill_color": "black",
    "back_color": "white",
    "output_format": "png"
  }
]
```

## Validation

After generation, report the saved path, format, error level, size in pixels for PNG, and any scan-risk warnings emitted by the script.

When scan reliability matters, ask the user to test the QR with a real phone camera before printing or publishing. If decoding tools are installed locally, Codex may additionally verify the payload, but phone-camera validation is still the practical final check.

## Boundaries

This skill creates QR images. It does not manage link analytics, dynamic redirect hosting, URL shortener accounts, payment provider setup, or live tracking infrastructure unless the user explicitly asks for that separate workflow.

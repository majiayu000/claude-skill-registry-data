---
name: qr-code
description: Generate accurate, phone-scannable QR codes as PNG or SVG from URLs, local preview links, text, contact/payment/event/Wi-Fi payloads, or shareable deliverables. Use automatically when Codex decides a user may need to scan with a phone, when a generated website/app/art/design/social asset/demo needs a QR code, when sharing localhost/tunnel/public links, or when the user asks for QR, qrcode, QR code, QR 碼, 二維碼, or 手機掃描. Prefer scripts/make_qr.py for deterministic local generation; ask before encoding secrets, private tokens, or sensitive personal data.
---

# QR Code

## Core Workflow

Use `scripts/make_qr.py` to generate QR codes locally without web APIs or external packages.

1. Confirm the exact payload to encode.
   - For websites and apps, encode the final reachable URL.
   - For phone scanning, avoid `localhost` unless the user explicitly wants a same-machine test. Use a public, tunnel, or LAN URL when the phone must open it.
   - Do not encode API keys, private tokens, passwords, or sensitive personal data unless the user explicitly asks for that payload.

2. Choose output for the deliverable.
   - Use PNG for previews, screenshots, social posts, and general user-facing assets.
   - Use SVG for print, design tools, websites, and scalable artwork.
   - Generate both PNG and SVG when the QR code may be reused in design or publishing work.

3. Choose scan settings.
   - Default to error correction `M` for ordinary URLs and short text.
   - Use `Q` for print, posters, stickers, or image-heavy layouts.
   - Use `H` when a designer may recolor, overlay a logo, crop tightly, or place the code on busy artwork.
   - Keep quiet zone at `4` modules or more. Do not crop it away.

4. Run the script from the skill directory:

```powershell
python .\scripts\make_qr.py "https://example.com" --output ".\out\example.png" --error-correction M --scale 10 --print-json
```

For SVG:

```powershell
python .\scripts\make_qr.py "https://example.com" --output ".\out\example.svg" --format svg --error-correction Q --print-json
```

## Verification

After generation:

- Confirm the output file exists and is non-empty.
- If the QR points to a website, verify the target URL itself is reachable before presenting the QR as final.
- When possible, open or inspect the generated image to ensure the quiet zone is visible and the modules are crisp.
- Report the encoded payload, output path, format, and error correction level.

## Script Notes

`scripts/make_qr.py` is a pure Python QR generator. It supports byte-mode QR codes, automatic QR version selection, Reed-Solomon error correction, mask scoring, PNG output, and SVG output. It intentionally avoids online QR services so generated assets are private, fast, and reproducible.

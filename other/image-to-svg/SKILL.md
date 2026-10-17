---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: image-to-svg
description: >
  Convert a raster image (PNG, JPEG, WebP, GIF) or local image file into SVG
  with the QuiverAI vectorization API. Use when the user wants image to SVG,
  vectorize an image, trace a logo or icon, or save an SVG from a picture.
---

# Image to SVG

Vectorize an image with QuiverAI `POST /v1/svgs/vectorizations`, then write
the returned SVG markup to a file.

Always fetch the current docs first. Never pipe through `head`, `tail`,
`sed -n`, `awk`, `| less`, or any command that truncates:

```bash
curl -sL https://docs.quiver.ai/api/models/image-to-svg
curl -sL https://docs.quiver.ai/api-reference/vectorize-svg/vectorizesvg
```

API key lives in `~/.config/opencode/skills/image-to-svg/.env` as
`QUIVERAI_API_KEY`. Load it. Never print the key. Never commit `.env`.
If the value is empty, stop and ask the user to paste a key from
https://platform.quiver.ai/api-keys

```bash
set -a
source ~/.config/opencode/skills/image-to-svg/.env
set +a
test -n "$QUIVERAI_API_KEY"
```

## Convert

Default model is `arrow-1.1` (logos, icons, most images). Use
`arrow-1.1-max` for dense illustrations or technical drawings.

Keep `stream` false. The JSON body has the full SVG. Do not use SSE.

Crop the subject tightly when you can. Set `auto_crop: true` only when
the image has extra empty space you cannot crop yourself.

**Public URL**

```bash
OUT=/tmp/vectorized.svg

curl -sS --fail-with-body -X POST 'https://api.quiver.ai/v1/svgs/vectorizations' \
  -H "Authorization: Bearer $QUIVERAI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "arrow-1.1",
    "auto_crop": true,
    "image": { "url": "https://example.com/logo.png" }
  }' \
  | jq -r '.data[0].svg' > "$OUT"

test -s "$OUT"
```

**Local file** (PNG, JPEG, WebP, GIF, SVG). Send raw base64, not a data URI.
Decoded input must stay under 12,582,912 bytes, 4096x4096, and 16,777,216 pixels.

```bash
SRC=/path/to/image.png
OUT=/tmp/vectorized.svg
B64=$(base64 -i "$SRC" | tr -d '\n')

jq -n --arg b64 "$B64" '{
  model: "arrow-1.1",
  auto_crop: true,
  image: { base64: $b64 }
}' | curl -sS --fail-with-body -X POST 'https://api.quiver.ai/v1/svgs/vectorizations' \
  -H "Authorization: Bearer $QUIVERAI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d @- \
  | jq -r '.data[0].svg' > "$OUT"

test -s "$OUT"
```

Save next to the source when the user did not name an output path:
`/path/to/image.svg` from `/path/to/image.png`. Otherwise use the path they
gave. Always confirm the file exists and starts with `<svg`.

## Logos for websites

After vectorization, rewrite **logos and wordmarks** so they drop into
sites without extra CSS hacks:

1. **Transparent background.** Delete full-canvas white/black `<rect>`
   fills, `fill` on `<svg>`, and any path that is only the backdrop.
   The SVG must have no opaque background.
2. **`currentColor` for the mark.** Replace the logo fill and stroke
   (`#000`, `#000000`, `black`, and the dominant ink color) with
   `currentColor`. Sites can then set `color` in CSS for light and dark
   mode.
3. Do this when the input is a logo, icon, or wordmark, or when the
   user asks for website/asset use. Skip it for full-color illustrations
   where hue is part of the art.

Do the rewrite on the saved SVG before you upload it. Do not leave
hardcoded black or white on a logo meant for a site.

## Response

Success JSON (non-stream):

```json
{
  "id": "resp_...",
  "created": 1704067200,
  "data": [{ "svg": "<svg ...>", "mime_type": "image/svg+xml" }],
  "credits": 1
}
```

Write **only** `.data[0].svg` to the file. Do not write the wrapper JSON.

A `sk_test_...` key returns a mock. Reject it for real work if the SVG has
`data-quiver-sandbox="true"` or the response header is
`x-quiver-environment: test`.

On HTTP errors, show `status`, `code`, `message`, and `request_id`. For
`429`, wait `Retry-After` seconds then retry once.

## Discord

After a successful save, upload the SVG with
`kimaki upload-to-discord --session <current-session> "$OUT"` so the user
can open the file. Do not paste the full SVG markup into chat.

---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: ray-so
repo: raycast/ray-so
description: >
  Generate beautiful code snippet images using ray.so and Playwriter.
  Builds a URL with code, theme, and settings encoded in the hash fragment,
  navigates to it in Chrome, and exports the image via Cmd+C clipboard copy.
  Use this skill when the user asks to create a code image, code screenshot,
  or code snippet image.
---

# ray.so Code Image Generation

Generate code snippet images by constructing a ray.so URL, navigating in Chrome via Playwriter,
pressing `Cmd+C` to copy the rendered image to clipboard, and saving the clipboard to a file.

Always use the **vercel** theme unless the user specifies a different one.

## URL structure

All settings live in the **hash fragment** (`#key=value&key2=value2`), not query params.
Code is Base64url-encoded using Node.js `Buffer.from(code).toString('base64url')`.

```
https://ray.so/#code=BASE64URL_CODE&theme=vercel&darkMode=true&background=true&padding=64&language=typescript&title=example.ts
```

## Parameters

| Parameter | Default | Values |
|-----------|---------|--------|
| `code` | (sample) | `Buffer.from(code).toString('base64url')` |
| `theme` | `candy` | `vercel`, `supabase`, `tailwind`, `openai`, `mintlify`, `prisma`, `clerk`, `elevenlabs`, `resend`, `triggerdev`, `nuxt`, `browserbase`, `cloudflare`, `gemini`, `stripe`, `bitmap`, `noir`, `ice`, `sand`, `forest`, `mono`, `breeze`, `candy`, `crimson`, `falcon`, `meadow`, `midnight`, `raindrop`, `sunset`, `rabbit`, `firecrawl`, `aws`, `auth0` |
| `darkMode` | `true` | `true`, `false` |
| `background` | `true` | `true`, `false` |
| `padding` | `64` | `16`, `32`, `64`, `128` |
| `language` | auto-detect | `javascript`, `typescript`, `tsx`, `jsx`, `python`, `go`, `rust`, `swift`, `shell`, `css`, `html`, `json`, `sql`, `ruby`, `java`, `kotlin`, `cpp`, `csharp`, `dart`, `elixir`, `graphql`, `haskell`, `lua`, `markdown`, `php`, `scala`, `toml`, `yaml`, `zig`, `diff`, `dockerfile`, `plaintext`, and more |
| `title` | `""` | Filename shown in the title bar |
| `subtitle` | `""` | Subtitle text |
| `width` | auto | Pixel width (number) |
| `lineNumbers` | `undefined` | `true`, `false` |
| `highlightedLines` | `""` | Comma-separated line numbers |

## Workflow: generate and save a code image

Single Playwriter call. Use the script below **exactly as-is**, only changing the
`code`, `language`, `title`, `theme`, and output path variables. Do not restructure,
reorder, or simplify the script; the clipboard interceptor must be injected before
`Cmd+C` is pressed, and the poll loop must run after.

```bash
playwriter -s <sessionId> --timeout 30000 -e "$(cat <<'PYEOF'
const code = `export function hello() {
  return "world"
}`
const encoded = Buffer.from(code).toString('base64url')
const params = new URLSearchParams()
params.set('code', encoded)
params.set('theme', 'vercel')
params.set('darkMode', 'true')
params.set('background', 'true')
params.set('padding', '64')
params.set('language', 'typescript')
params.set('title', 'hello.ts')

// Navigate (always fresh page)
state.page = await context.newPage()
await state.page.goto('https://ray.so/#' + params.toString(), { waitUntil: 'domcontentloaded' })
await state.page.waitForSelector('#frame', { timeout: 10000 })

// Intercept clipboard write to capture the PNG blob
await state.page.evaluate(() => {
  window.__clipboardBlob = null
  const origWrite = navigator.clipboard.write.bind(navigator.clipboard)
  navigator.clipboard.write = async (items) => {
    for (const item of items) {
      if (item.types.includes('image/png')) {
        window.__clipboardBlob = await item.getType('image/png')
      }
    }
    return origWrite(items)
  }
})

// Press Cmd+C and poll until the blob is captured (no fixed sleep)
await state.page.keyboard.press('Meta+c')
let attempts = 0
while (attempts < 50) {
  const hasBlob = await state.page.evaluate(() => !!window.__clipboardBlob)
  if (hasBlob) break
  await state.page.waitForTimeout(100)
  attempts++
}
if (attempts >= 50) throw new Error('Clipboard blob not captured after 5s')

// Read blob as base64 and save via Node.js fs
const base64 = await state.page.evaluate(async () => {
  const blob = window.__clipboardBlob
  const buf = await blob.arrayBuffer()
  const bytes = new Uint8Array(buf)
  let binary = ''
  for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i])
  return btoa(binary)
})

const fs = require('node:fs')
const buffer = Buffer.from(base64, 'base64')
fs.writeFileSync('/absolute/path/to/output.png', buffer)
console.log('Saved', buffer.length, 'bytes')

// Close the page
await state.page.close()
PYEOF
)"
```

The clipboard poll checks every 100ms until the PNG blob is captured, with a 5s timeout.
After saving, verify the output image with the `read-media` tool.

## Agent rules

- Always use `vercel` theme unless the user asks for something else
- Always use `darkMode=true`, `background=true`, `padding=64` by default
- Set `language` explicitly when known; do not rely on auto-detect
- Set `title` to the filename when available (e.g. `greet.ts`)
- Use absolute paths for the output PNG
- Do **not** use `js-base64` npm package in Playwriter; use `Buffer.from(code).toString('base64url')` instead (Playwriter sandbox only allows Node.js built-ins)
- Do **not** inspect the page between navigate and `Cmd+C`; the URL params are deterministic
- After saving, verify the image with `read-media` tool to confirm it rendered correctly

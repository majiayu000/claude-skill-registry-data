---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: grok-imagine
description: >
  Generate images on grok.com/imagine with the signed-in Grok session.
  Use when the user wants Grok Imagine, a landscape image, or to replay
  a recorded Imagine prompt. Prefer the in-page network API, not UI clicks.
---

# Grok Imagine

Preconditions: the user is signed in on [grok.com](https://grok.com/imagine).
Playwriter drives that tab. Do not copy cookies or tokens.

Recorded flow: type a prompt, set aspect **Ampio** (wide / `16:9`), click
**Invia**. The only useful recorded network call is quota. Image generate
is not REST. It uses `wss://grok.com/ws/imagine/listen`. Both run inside
`state.page.evaluate` so the page cookies apply.

Drop: empty paragraph click, analytics (`/_data/`, Stripe, Appsflyer),
and the `.scheme-light` CSS click.

## Parameters

- `prompt` — recorded demo: `a nice landscape`
- `aspectRatio` — `16:9` for Ampio. Also `1:1`, `9:16`

## 1. Open Imagine

```bash
playwriter -s 1 -e 'state.page = context.pages().findLast((p) => p.url().startsWith("https://grok.com/")) ?? await context.newPage(); await state.page.goto("https://grok.com/imagine", { waitUntil: "domcontentloaded" })'
```

## 2. Check quota with fetch

```bash
playwriter -s 1 -e 'const q = await state.page.evaluate(async () => { const r = await fetch("/rest/media/imagine/quota_info", { method: "POST", headers: { "content-type": "application/json" }, credentials: "include", body: "{}" }); return { status: r.status, body: await r.json() } }); console.log(q)'
```

Expect `status: 200` and `image.available: true`. If 401/403, ask the user
to sign in.

## 3. Generate with the Imagine websocket

Do not fill the textbox or click **Invia**. `POST /rest/media/post/create`
only creates an empty post. Generate from `evaluate`:

```bash
playwriter -s 1 -e 'const { join } = require("node:path"); const { homedir } = require("node:os"); const { generateImagineImage } = await import(join(homedir(), ".agents/skills/grok-imagine/utils.js")); console.log(await generateImagineImage({ page: state.page, prompt: "a nice landscape", aspectRatio: "16:9", count: 1 }))'
```

Expect `images[].url` on `https://imagine-public.x.ai/imagine-public/images/<id>.jpg`.

For a project-local copy of this skill:

```bash
playwriter -s 1 -e 'const { generateImagineImage } = await import("./.agents/skills/grok-imagine/utils.js"); console.log(await generateImagineImage({ page: state.page, prompt: "a nice landscape", aspectRatio: "16:9" }))'
```

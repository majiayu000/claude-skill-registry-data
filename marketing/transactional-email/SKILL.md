---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: transactional-email
description: >
  How to write and send transactional emails (welcome, first-deploy, notifications)
  from Cloudflare Workers. Covers the preferred personal writing style (no headings,
  Gmail-default look, dark mode), building HTML with plain template strings,
  the send_email wrangler binding, previewing in light/dark mode with Playwriter,
  test-sending real emails via a temp worker without deploying, and one-off scripts
  that email specific users via the cloudflare SDK (plan changes, bug notices).
  ALWAYS load this skill when adding, editing, testing, or sending transactional
  emails in a project.
---

# Transactional email on Cloudflare

Emails must look like they were **manually written by a person**, not designed by a marketing
team. Build them as plain HTML template strings, send them through the Cloudflare `send_email`
binding, and always preview them in light + dark mode before shipping.

## Every email MUST set a reply_to

Sending subdomains (like `tommy.akarso.co`) usually have **no MX or A records**, so replies
to the from address silently bounce — while the email copy actively invites replies
("just reply to this email"). Every send, whether via the `send_email` binding or the
`cloudflare` SDK, MUST include a `reply_to`.

Rules:

- The reply-to address is a **user choice** — never guess it. Ask the user which email to
  use, then save it in the project's AGENTS.md (see the "Record the sending domain" section)
  as the preferred reply-to so future agents don't have to ask again.
- Prefer an address connected to a **real inbox the user reads (usually Gmail)**, NOT an
  address behind Cloudflare Email Routing or other forwarding — a chain of routing hops adds
  failure points and hurts deliverability of the reply.
- Verify the from domain's DNS when in doubt: `dig +short MX <sending-domain>`. No MX and no
  A record means replies to that address bounce.

```ts
const FROM = { address: 'tommy@tommy.akarso.co', name: 'Tommy' }
const REPLY_TO = { address: 'tommy@holocron.so', name: 'Tommy' } // from AGENTS.md

await client.emailSending.send({
  account_id: ACCOUNT_ID,
  from: FROM,
  reply_to: REPLY_TO, // single { address, name } object, NOT an array
  to,
  subject,
  html,
})
```

## Writing style rules

- **NO headings** (`h1`/`h2`), no logo header, no URL cards/boxes, no `<hr>` dividers, no branded footer.
- Only formatting a human would use in Gmail's compose box: **bold**, links, lists, inline code.
- Personal tone: open with "Hey,", end with "If anything looks off, just reply to this email"
  and a first-name sign-off. Encourage replies — replies build trust and surface bugs.
- Subjects are plain sentences: `Your docs for owner/repo are live`. No em-dashes, no
  "🎉 Announcing…" style.
- Keep it short. One purpose per email: the key link, one short list of next steps, sign-off.

## Gmail-default styling

Match Gmail compose defaults so the email blends in with human-written mail:

- `font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height: 1.5; color: #222`
- Links: default blue `#15c`, **keep the underline** (never `text-decoration: none`)
- Content wrapper `max-width: 600px`, left-aligned, no centering chrome
- Inline code: `font-family: monospace; font-size: 0.9em; background: rgba(128,128,128,0.15); padding: 1px 4px; border-radius: 3px`.
  The gray-alpha background works in BOTH light and dark mode without a media query.

## Dark mode

Include `color-scheme` metas and one small `prefers-color-scheme` block. Nothing else:

```html
<meta name="color-scheme" content="light dark" />
<meta name="supported-color-schemes" content="light dark" />
<style>
  body { background-color: #ffffff; }
  a { color: #15c; }
  @media (prefers-color-scheme: dark) {
    body { background-color: #1f1f1f !important; color: #e3e3e3 !important; }
    a { color: #8ab4f8 !important; }
  }
</style>
```

`#8ab4f8` is Gmail's dark-mode link blue.

## Build HTML with plain template strings — never React/JSX

**Never render emails with React or framework-tied renderers.** `renderToStaticMarkup` from
spiceflow/federation only works inside the Vite RSC runtime; react-dom/server is unavailable
under the react-server condition. Framework-rendered emails cannot be previewed from node
scripts or test-sent from plain workers. Plain strings work in every runtime.

Reference template (adapt the body copy per email):

```ts
import dedent from 'string-dedent'

function escapeHtml(text: string): string {
  return text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
}

function code(text: string): string {
  return `<code style="font-family: monospace; font-size: 0.9em; background-color: rgba(128, 128, 128, 0.15); padding: 1px 4px; border-radius: 3px;">${escapeHtml(text)}</code>`
}

function link(href: string, text: string): string {
  return `<a href="${escapeHtml(href)}">${escapeHtml(text)}</a>`
}

export function buildWelcomeEmailHtml(data: { repo: string; url: string; branch: string }): string {
  const HTML = dedent`
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="color-scheme" content="light dark" />
        <meta name="supported-color-schemes" content="light dark" />
        <style>
          body { background-color: #ffffff; }
          a { color: #15c; }
          @media (prefers-color-scheme: dark) {
            body { background-color: #1f1f1f !important; color: #e3e3e3 !important; }
            a { color: #8ab4f8 !important; }
          }
        </style>
      </head>
      <body style="font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height: 1.5; color: #222; margin: 0; padding: 16px; -webkit-text-size-adjust: 100%;">
        <div style="max-width: 600px;">
          <p>Hey,</p>

          <p>your docs site for <strong>${escapeHtml(data.repo)}</strong> just went live:</p>

          <p><a href="${escapeHtml(data.url)}">${escapeHtml(data.url)}</a></p>

          <p>Every push to the ${code(data.branch)} branch deploys automatically.</p>

          <ul style="margin: 0 0 16px 0; padding-left: 24px;">
            <li>${link('https://example.com/docs/domains', 'custom domain')} for production</li>
          </ul>

          <p>If anything looks off, just reply to this email and I'll take a look.</p>

          <p>Tommy<br /><a href="https://example.com">example.com</a></p>
        </div>
      </body>
    </html>
  `
  return HTML
}
```

Rules:

- **Escape every interpolated value** with `escapeHtml` (user names, repo names, URLs).
- `<ul>` needs `margin: 0 0 16px 0; padding-left: 24px` to look right in mail clients.
- **Validate every URL** in the email with curl (expect 200) before shipping.

## Sending via the Cloudflare send_email binding

wrangler.jsonc — `remote: true` makes the binding work in local dev / `wrangler dev`:

```jsonc
{
  "send_email": [{ "name": "EMAIL", "remote": true }]
}
```

The binding has a builder-style `send()` overload — no need to construct raw MIME
`EmailMessage` objects. Workers use spiceflow; get `env` and `waitUntil` from
`cloudflare:workers` and send from inside a route handler:

```ts
import { env, waitUntil } from 'cloudflare:workers'
import { Spiceflow } from 'spiceflow'

const app = new Spiceflow().route({
  method: 'POST',
  path: '/api/signup',
  handler: async ({ request }) => {
    // ... do the actual work first ...
    waitUntil(sendWelcomeEmail({ to: userEmail }))
    return { ok: true }
  },
})

async function sendWelcomeEmail({ to, data }: { to: string; data: WelcomeEmailData }): Promise<void> {
  try {
    await env.EMAIL.send({
      from: { email: 'tommy@yourdomain.com', name: 'Tommy' },
      replyTo: { email: 'tommy@real-inbox.com', name: 'Tommy' }, // preferred reply-to from AGENTS.md
      to,
      subject: buildWelcomeEmailSubject(data),
      html: buildWelcomeEmailHtml(data),
    })
  } catch (err) {
    // Email is best-effort; never fail the request because an email failed
    captureException(err instanceof Error ? err : new Error(String(err)), {
      tags: { route: 'signup', reason: 'welcome-email-failed' },
    })
  }
}
```

Email must be **best-effort**: fire it via `waitUntil()`, wrap in try/catch, report failures
to error tracking. Never await it in the response path and never let it throw.

The `from` domain must have Cloudflare Email Routing enabled with the sender address configured.

## Record the sending domain in the project's AGENTS.md

The sending domain, from address, and **preferred reply-to address** are a **user choice** —
never guess them. Ask the user which sender and reply-to to use, and once they provide them,
save both in the project's AGENTS.md so future agents don't have to ask again:

```md
## Email sending

Transactional emails send via Cloudflare Email Service. The sending domain is
`tommy.akarso.co`; the from address is `tommy@tommy.akarso.co` (name "Tommy").
Every email MUST set `reply_to` to the preferred reply-to address
`tommy@holocron.so` — the sending subdomain has no MX records, replies to it bounce.
```

If AGENTS.md already documents a sending domain and reply-to, use them without asking.

## Previewing an email

Add a small tsx script per email that writes the rendered HTML to `tmp/`:

```ts
// scripts/preview-welcome-email.ts
import fs from 'node:fs'
const html = buildWelcomeEmailHtml({ repo: 'owner/repo', url: 'https://example.com', branch: 'main' })
fs.mkdirSync('tmp', { recursive: true })
fs.writeFileSync('tmp/welcome-email.html', html)
```

Then screenshot BOTH color schemes with Playwriter and inspect them:

```js
await state.page.goto('file:///abs/path/tmp/welcome-email.html')
await state.page.emulateMedia({ colorScheme: 'light' })
await state.page.screenshot({ path: '/tmp/email-light.png', scale: 'css' })
await state.page.emulateMedia({ colorScheme: 'dark' })
await state.page.screenshot({ path: '/tmp/email-dark.png', scale: 'css' })
```

Always check both screenshots yourself before telling the user the email is done.

## Test-sending a real email without deploying

Use a throwaway worker with the remote binding — `wrangler dev` proxies `send_email` to the
real Cloudflare account, so the email actually sends. No deploy needed.

1. Create the two files inside the project's gitignored `tmp/` dir (NOT `/tmp`) so wrangler's
   bundler resolves `spiceflow` and the email builder from the project's `node_modules`:

```jsonc
// tmp/email-test/wrangler.jsonc
{
  "name": "email-test",
  "main": "worker.ts",
  "compatibility_date": "2026-04-14",
  "send_email": [{ "name": "EMAIL", "remote": true }]
}
```

```ts
// tmp/email-test/worker.ts
import { env } from 'cloudflare:workers'
import { Spiceflow } from 'spiceflow'
import { z } from 'zod'

const app = new Spiceflow().route({
  method: 'POST',
  path: '/',
  request: z.object({ to: z.string(), subject: z.string(), html: z.string() }),
  handler: async ({ request }) => {
    const { to, subject, html } = await request.json()
    await env.EMAIL.send({ from: { email: 'tommy@yourdomain.com', name: 'Tommy' }, to, subject, html })
    return { sent: true }
  },
})

export default {
  fetch(request: Request) {
    return app.handle(request)
  },
}
```

2. Run it with the project's wrangler (so auth/account come from the real project), in a
   tuistory background session:

```bash
bunx tuistory launch "pnpm --dir <project> exec wrangler dev --config <project>/tmp/email-test/wrangler.jsonc --port 8799" -s email-test
bunx tuistory -s email-test wait "/Ready on/i" --timeout 60000
```

3. POST the rendered HTML:

```bash
node --input-type=module -e "
import fs from 'node:fs'
const html = fs.readFileSync('tmp/welcome-email.html', 'utf8')
const res = await fetch('http://localhost:8799', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ to: 'user@example.com', subject: 'Test subject', html }) })
console.log(res.status, await res.text())
"
```

4. Clean up: `bunx tuistory -s email-test press ctrl c` then `bunx tuistory -s email-test close`.

## One-off emails to specific users from a script

When the user asks to email **specific customers** — a plan change that affects them, a bug
they hit, a refund notice — do it with a plain tsx script using the official `cloudflare`
npm SDK. No worker, no wrangler dev: `client.emailSending.send()` hits the Email Service
REST API (`POST /accounts/{id}/email/sending/send`) directly from Node.

Auth reuses the local wrangler login. On macOS with current wrangler the OAuth token lives at
`~/Library/Preferences/.wrangler/config/default.toml`. Tokens expire after ~1h; on a 401 just
run `wrangler whoami` to refresh.

```ts
// scripts/send-plan-change-email.ts
// Run: pnpm tsx scripts/send-plan-change-email.ts
import fs from 'node:fs'
import Cloudflare from 'cloudflare'
import dedent from 'string-dedent'

const ACCOUNT_ID = '<cloudflare account id>' // from `wrangler whoami`
const FROM = { address: 'tommy@yourdomain.com', name: 'Tommy' } // from AGENTS.md
const REPLY_TO = { address: 'tommy@real-inbox.com', name: 'Tommy' } // preferred reply-to from AGENTS.md

function getWranglerOAuthToken(): string {
  const path = `${process.env.HOME}/Library/Preferences/.wrangler/config/default.toml`
  const token = fs.readFileSync(path, 'utf8').match(/oauth_token\s*=\s*"([^"]+)"/)?.[1]
  if (!token) {
    console.error(`no oauth_token in ${path}, run 'wrangler login' first`)
    process.exit(1)
  }
  return token
}

// Affected users: hardcode the list, or query the production DB (e.g. the
// db package's node.ts entrypoint for remote D1) to select them.
const recipients = ['user1@example.com', 'user2@example.com']

// Tiny semaphore: caps in-flight sends at `max` while Promise.all drives the rest.
function createSemaphore(max: number) {
  let active = 0
  const waiters: Array<() => void> = []
  return async function run<T>(fn: () => Promise<T>): Promise<T> {
    if (active >= max) await new Promise<void>((resolve) => waiters.push(resolve))
    active++
    try {
      return await fn()
    } finally {
      active--
      waiters.shift()?.()
    }
  }
}

async function main() {
  const client = new Cloudflare({ apiToken: getWranglerOAuthToken() })
  const limit = createSemaphore(10)
  const results = await Promise.all(
    recipients.map((to) =>
      limit(async () => {
        console.log(`sending to ${to}...`)
        const result = await client.emailSending.send({
          account_id: ACCOUNT_ID,
          from: FROM,
          reply_to: REPLY_TO,
          to,
          subject: 'A change to your plan',
          html: buildEmailHtml(), // same plain-string builder pattern as above
          text: dedent`
            Hey,

            ... plain text fallback ...

            Tommy
          `,
        })
        console.log(`sent to ${to}: ${result.message_id}`)
        return { to, messageId: result.message_id }
      }),
    ),
  )
  console.log(`done, ${results.length} emails sent`)
}

main().catch((err) => {
  console.error('send failed:', err)
  process.exit(1)
})
```

Rules for these scripts:

- **Log progress per recipient** (email + returned `message_id`) so a crash mid-run shows
  exactly who already got the email; the response also has `delivered` / `queued` /
  `permanent_bounces` arrays worth logging on failure.
- **SDK gotcha:** `from` / `reply_to` objects are `{ address, name }`, NOT `{ email, name }`.
  Getting it wrong returns a vague 400 `email.sending.error.invalid_request_schema`.
- Send with **Promise.all capped by a semaphore at 10 concurrent** — fast, but bounded so a
  big list doesn't blast the API. If any send rejects, the logged per-recipient lines tell
  you who already got the email before resuming.
- Preview the HTML (light + dark screenshots) and **send to the user's own address first** for
  approval before emailing customers.
- Same writing style rules as every other email: personal, short, no headings, reply-friendly.

## Attachments (ICS, PDF, etc.)

The `send_email` binding's builder `send()` supports attachments natively. No hand-rolled MIME or `mimetext` needed:

```ts
await env.EMAIL.send({
  from: { email: 'notifications@example.com', name: 'App' },
  to,
  subject,
  html,
  attachments: [
    {
      disposition: 'attachment',
      filename: 'invite.ics',
      type: 'text/calendar',
      content: icsString,
    },
  ],
})
```

Only use the raw `new EmailMessage(from, to, rawMime)` overload from `cloudflare:email` when you need full MIME control (e.g. inline images with Content-ID references).

## Gotchas

- **spiceflow/federation `renderToStaticMarkup` throws outside Vite RSC** — this is why emails
  must be plain strings, not JSX.
- Cloudflare Email Routing may restrict which destination addresses accept mail depending on
  the zone setup; if a test send errors on the destination, verify the address in Email Routing.
- `tmp/` preview output should be gitignored; check with `git check-ignore` before committing.
- Real-world reference implementation: `website/src/deploy-email.ts` in the holocron repo.
- **`remote: true` can crash the vite dev worker.** With `send_email` set to `remote: true`, the dev worker sometimes dies with `Error: internal error; reference = ...` and stops accepting connections. Restart the dev server session; nothing is wrong with the code.

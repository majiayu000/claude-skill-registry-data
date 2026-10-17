---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: x-bookmarks
description: >
  Read the user's latest X (Twitter) bookmarks as typed data (text, author,
  metrics, media, links, quoted posts, articles) with a TypeScript SDK that
  calls X's Bookmarks GraphQL API via fetch inside the signed-in x.com tab
  through playwriter. Use when the user asks for their bookmarks, saved
  tweets, or wants to export, summarize, or process X bookmarks.
---

# X bookmarks

`sdk.ts` in this folder reads bookmarks with **network calls only**. It runs
`fetch()` inside an x.com page via `page.evaluate`, so the user's cookies
apply. No clicks, no scrolling, no DOM scraping. Do not copy cookies or
tokens out of the browser.

Preconditions: Chrome has the playwriter extension, and the user is logged
into x.com. Read `playwriter skill` in full first if you have not used it.
If `playwriter session new` fails with `extension_not_connected`, show the
user the printed install steps and stop. Do not try other workarounds.

## Get the latest bookmarks

```bash
playwriter session new --tab-group x
playwriter -s <id> --timeout 60000 -e "$(cat <<'EOF'
const { getLatestBookmarks } = await import(require('node:os').homedir() + '/.config/opencode/skills/x-bookmarks/sdk.ts')
const bookmarks = await getLatestBookmarks({ context, limit: 50 })
require('node:fs').writeFileSync('/tmp/x-bookmarks.json', JSON.stringify(bookmarks, null, 2))
console.log(bookmarks.length, bookmarks.map((b) => `@${b.author.screenName}: ${b.text.slice(0, 80)}`).join('\n'))
EOF
)"
```

The playwriter sandbox runs Node 24, so `import()` of a `.ts` file works
(type stripping). Write big results to `/tmp` instead of printing them;
console output gets truncated.

`getLatestBookmarks` returns `XTweet[]`, newest bookmark first. See the
interfaces at the top of `sdk.ts` for all fields. It opens its own tab and
**always closes it** (also on error), so no x.com tab is left open.

## Manual pagination

Only use this when you need cursors. You own the tab, so close it in
`finally`. Never leave the page open after the export.

```js
const sdk = await import(require('node:os').homedir() + '/.config/opencode/skills/x-bookmarks/sdk.ts')
const page = await context.newPage()
try {
  const query = await sdk.discoverBookmarksQuery({ page })
  const first = await sdk.fetchBookmarksPage({ page, query, count: 100 })
  const second = await sdk.fetchBookmarksPage({ page, query, cursor: first.nextCursor })
} finally {
  await page.close()
}
```

Only `discoverBookmarksQuery` navigates.

## How it works

1. `discoverBookmarksQuery` opens `https://x.com/i/bookmarks` and waits for
   the web app's own `GET /i/api/graphql/<queryId>/Bookmarks` request. It
   copies `queryId`, the `features` param and the bearer header from it.
2. `fetchBookmarksPage` replays that GraphQL call with `fetch()` in the page,
   adding `x-csrf-token` from the `ct0` cookie.
3. The response is parsed into `XTweet` objects. The `cursor-bottom-*` entry
   gives `nextCursor`.

## Gotchas

- **Never hardcode the queryId or features.** They change with X deploys.
  Always discover them from the live request.
- The queryId is **not** in `main.js`. It is in a lazy chunk. Do not waste
  time scanning bundles.
- `x-client-transaction-id` is **not** required for this read endpoint.
- The recording started from **History** (`/i/history`), which shows the same
  Bookmarks tab. The `flow/timeline.json`, `live_pipeline` and
  `viewer_context` calls in the recording are noise.
- `UsersByRestIds HTTP-403` page errors in playwriter output come from x.com
  itself. Ignore them.
- Long posts: full text is in `note_tweet`; the SDK handles this.
- On `401`/`403` from Bookmarks, or `missing ct0 cookie`, ask the user to log
  into x.com in Chrome.

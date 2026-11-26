---
name: accountToDryRun
description: Take one Facebook account from imported (NEEDSLOGIN) to ACTIVE and run a full publish dry run, through the `log` MCP tools. Proxy, sign-in, a Twenty listing, then the publish machine all the way to the filled create form, stopping before Publish. Use when a new or vendor account has to start working, or to prove an account can post before going live.
---

# accountToDryRun

Every step is an `mcp__log__*` tool (the `log` MCP server, `bun run mcp`).
The same thing works in a terminal as `log <command> <args>`.
Nothing here posts to Facebook. Going live is the last step, and only when
the owner says so.

## Hard boundaries

1. **Waking hours (rule 35).** Steps 3 to 6 open the browser, so they only run
   between 08:00 and 22:00 in the account's home timezone. For Pennsylvania
   that's 12:00-02:00 GMT (EDT, until 1 Nov) or 19:00-09:00 in Vietnam. Outside
   that, every step returns `outsideActiveHours`. When the owner asks for a run
   outside those hours, add `"--bypass"` to the args. It skips only
   the hours; the proxy gate and self-check still run.
2. **No browser without the proxy (rule 35).** Step 1 must pass first.
3. **Someone watches the window (rule 35).** Camoufox is always visible. If
   the cookies don't hold, the owner signs in in that window during step 3.
4. **`checkpointed` or `suspended`: stop.** Tell the owner and don't retry.
5. **Dry run only.** `facebookPublish` without `--live` stops before the Publish
   button. Live is its own tool, `facebookPublishLive`, with `confirmLive: true` and the owner's go (rule 8).

## The steps

`<a>` is the account's name (the Facebook id, e.g. `99900000000029`).

### 1. Proxy (no browser)

```text
mcp__log__facebookAccountShow   { account: "<a>" }                  Proxy set? Exit checked?
mcp__log__proxy     args ["check", "--account", "<a>"]    exit IP in the home country
```

If no proxy: `["assign", "--account", "<a>", "--region", "<state>"]`. It
retries until the exit is within 100 km of the home city, or says
`proxyTooFar` and saves nothing.

### 2. Setup (no Facebook)

```text
mcp__log__facebookDoctor    args ["--json"]    Python, Camoufox and Twenty OK
```

### 3. Sign in: NEEDSLOGIN → ACTIVE

```text
mcp__log__facebookConnect   args ["--account", "<a>"]
```

The tool always runs `--noPrompt`. Camoufox opens through the proxy on the
account's device. If the vendor cookies are still logged in, it saves them
and ends within seconds. If not, it **signs in by itself**: it types
the Twenty email and password, then on the two-step page the current code
from `totpSecret` (switching to "Authentication app" if Facebook offers
another method first), and trusts the device. This is the connect machine
(`platformKit/connect/machine.ts`): each page is printed as its kind and
state; nothing secret is. Every page takes the proven path: the
cookie banner is accepted, "We suspect automated behaviour" dismissed, login
puzzles solved (CaptchaKraken, then 2Captcha). Only an identity, photo, video
or SMS checkpoint is never clicked: it waits for the owner in the window. It reads for up to 600 s
(`--wait <s>` to change it). Signed in: the session is saved to Twenty and
the account set **ACTIVE**. It can also end `checkpointed` (status
CHECKPOINT), `wrongPassword`, `disabled` (BANNED) or `signInNotFinished`
(NEEDSLOGIN), each naming the last page.

Before the first connect, the account needs `email`, `password` and
`totpSecret` in Twenty: `node scripts/twenty/importVendorAccounts.mjs` (dry run, each
field `<set>`/`<empty>`), then `--apply`. It reads every `docs/vendors/*.txt`.

Check it:

```text
mcp__log__facebookAccountShow   { account: "<a>" }    Status ACTIVE, May run yes
```

`signInNotFinished` or `checkpointed` means the wait ran out on the page it
names. Run step 3 again with someone at the window.

### 4. Read the account (read-only)

```text
mcp__log__facebookScan      args ["--account", "<a>"]    Marketplace > Selling loads
```

### 5. The listing row in Twenty

Write the ad as JSON. Photos are local paths or URLs, and the first one is
the cover:

```json
{ "title": "...", "description": "...", "price": 99, "priceCurrency": "USD",
  "category": "Miscellaneous", "condition": "new", "photos": ["C:/.../1.jpg"],
  "locationQuery": "Philadelphia, PA", "locationCity": "philadelphia", "locationCountry": "US" }
```

```text
mcp__log__facebookListingCreate   { account: "<a>", file: "<path.json>" }
mcp__log__facebookListing         { id: "<listingId>" }
```

`create` checks the ad the way `facebookPublish` will (price, category, photos,
location) and refuses one that can't post.

### 6. Dry run

```text
mcp__log__facebookPublish   { listing: "<listingId>", formUrl: "file:///<repo>/python/fixtures/createItem.html" }
mcp__log__facebookPublish   { listing: "<listingId>" }
```

The first run fills the saved copy of the form and never touches Facebook. The
second goes to the real create page and runs every machine step (proxy gate,
self-check, session, photos varied and attached, title, price, category,
condition, description, location picked in the home country), then stops
before Publish. Each step is printed. Look for `dryRun` at the end. Any other
ending is a code: `mcp__log__errors { code: "<code>" }`.

Before photos go up, the open step reads the account's Marketplace location
from the page (`sell_location`). The US form has no Location field: if that
isn't the listing's city, it stops there with `locationNotSet` and names the
place ("Kearney (68847, US)"), and nothing is uploaded. The listing's
`locationQuery` is "City, State" with the state written out ("Reading,
Pennsylvania"): a `--live` run then sets the account's Marketplace location
to it first (Marketplace > Location > Change location > the place > the
suggestion Facebook names as that place > Apply,
`CometMarketplaceSetBuyLocationMutation`) and checks the form again. A dry
run never changes it. A zip, a number or an abbreviation ("Reading, PA") is
never typed: it is refused with `locationAbbreviated` before the run, because
"Bethlehem, PA" was offered only as the West Bank and a bare zip offered
Granada, Spain. A login wall or checkpoint on the form is signed
through in the same browser (rule 35).

**Rule 35: launches cost.** Each account opens on Facebook at most 8 times
per local day, 10 minutes apart, dry runs counted (`launchTooSoon`,
`launchBudgetSpent`). The fixture-form run doesn't count. Fix what a run
reports before running it again; don't loop dry runs. On 2026-10-19 one
account opened 14 times in 90 minutes and went to a video-selfie checkpoint
(`RESEARCH/LOG_CLI_RUN_CAPTURES_2026_10_19.md`).

### 7. Live (only on the owner's go)

A new account's listing is published but **held for review**: Facebook's
Selling page carries `integrity_status_indicator: "This listing is being
reviewed."` (with `is_live: true`). It is listed, but buyers who open its
link are sent to the city's Marketplace page until the review clears, and
Facebook offers no way to hurry it (`appeal_status: appeal_not_exist`; an
appeal exists only after a rejection). The run reads the id from Facebook's
own answer to Publish (`useCometMarketplaceListingCreateMutation`), says
"Held for review", and writes the row UNDER_REVIEW, not ACTIVE. A later
`log facebook scan` moves it to ACTIVE once the badge is gone. Reading's first listing,
2026-10-19, was held this way.

```text
mcp__log__facebookPublishLive   { listing: "<listingId>", confirmLive: true }
mcp__log__facebookScan      args ["--account", "<a>"]
```

Once Publish is clicked nothing is retried.

---
name: lead-gen-scan
version: 2026-08-26
description: Run a one-shot buying-intent lead scan across Reddit, Twitter/X, Instagram, and TikTok using Xpoz. Finds fresh posts from people actively looking for what a product does or frustrated with its competitors, classifies and prioritizes them, and reports where to engage and who to reach. Use when asked to "find leads", "who is asking for a tool like mine", "find people complaining about [COMPETITOR]", "buying-intent scan", or "social selling opportunities".
---

# Lead Gen Scan

## Overview

Find the people who want to buy right now. This skill scans the four platforms for fresh buying-intent posts (people asking for what a product does, or frustrated with the alternatives), qualifies the real asks, and delivers a prioritized report of where to comment and who to reach while the intent is still live. It finds and reports; **humans do all engagement**. The skill never posts, comments, DMs, or contacts anyone.

## When to Use

Activate when the user asks:
- "Find leads for [PRODUCT]"
- "Who's looking for a tool like [PRODUCT] right now?"
- "Find people complaining about [COMPETITOR]"
- "Scan Reddit/X for buying intent in [CATEGORY]"
- "Where should I engage this week to find customers?"
- "Social selling opportunities for [PRODUCT]"

## Setup & Authentication

Before fetching data, ensure Xpoz access is configured. Follow these checks in order.

### Check 1: Already authenticated?

**If you have MCP tools**, try calling any Xpoz tool (e.g., `checkAccessKeyStatus`). If it works → skip to Step 1.

**If you have the SDK**, try:
```python
from xpoz import XpozClient
client = XpozClient()  # reads XPOZ_API_KEY env var
```
If this succeeds without error → skip to Step 1.

If neither works, you need to authenticate. Get a free access key (below).

---

### Recommended: a free access key

Real analyses need a real key: [get a free access key](https://xpoz.ai/get-token) (free tier, up to 75K results, no credit card). SDK and CLI users set it as `XPOZ_API_KEY`; MCP connections sign in with the same account via OAuth on first tool call (paths below).

---

### Path A: MCP via mcporter (OpenClaw agents)

If `mcporter` is available:

```bash
mcporter call xpoz.checkAccessKeyStatus
```

If `hasAccessKey: true` → ready. If not:

```bash
mcporter config add xpoz https://mcp.xpoz.ai/mcp --auth oauth
```

Then authenticate — generate the OAuth URL and send it to the user:

**Step 1: Generate authorization URL**
```python
import secrets, hashlib, base64, urllib.parse, json, urllib.request, os

verifier = secrets.token_urlsafe(64)
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
state = secrets.token_urlsafe(32)

# Dynamic client registration
reg_req = urllib.request.Request(
    'https://mcp.xpoz.ai/oauth/register',
    data=json.dumps({
        'client_name': 'Agent Skills',
        'redirect_uris': ['https://www.xpoz.ai/oauth/openclaw'],
        'grant_types': ['authorization_code'],
        'response_types': ['code'],
        'token_endpoint_auth_method': 'none',
    }).encode(),
    headers={'Content-Type': 'application/json'},
)
reg_resp = json.loads(urllib.request.urlopen(reg_req).read())

params = urllib.parse.urlencode({
    'response_type': 'code',
    'client_id': reg_resp['client_id'],
    'code_challenge': challenge,
    'code_challenge_method': 'S256',
    'redirect_uri': 'https://www.xpoz.ai/oauth/openclaw',
    'state': state,
    'scope': 'mcp:tools',
    'resource': 'https://mcp.xpoz.ai/',
})

auth_url = 'https://mcp.xpoz.ai/oauth/authorize?' + params

# Save state for token exchange
os.makedirs(os.path.expanduser('~/.cache/xpoz-oauth'), exist_ok=True)
with open(os.path.expanduser('~/.cache/xpoz-oauth/state.json'), 'w') as f:
    json.dump({'verifier': verifier, 'state': state, 'client_id': reg_resp['client_id'],
               'redirect_uri': 'https://www.xpoz.ai/oauth/openclaw'}, f)

print(auth_url)
```

**Step 2: Send the URL to the user**

Tell them:
> "I need to connect to Xpoz for social media data. Please open this link and sign in:
>
> [auth_url]
>
> After authorizing, you'll see a code. Paste it back to me here."

**Step 3: WAIT for the user to reply with the code.** Do not proceed until they respond.

**Step 4: Exchange the code for a token**

Once the user provides the code (either a raw code or a URL containing `?code=...`), extract the code and exchange it:

```python
import json, urllib.request, urllib.parse, subprocess, os

with open(os.path.expanduser('~/.cache/xpoz-oauth/state.json')) as f:
    oauth = json.load(f)

code = "THE_CODE_FROM_USER"  # Extract from user's reply

data = urllib.parse.urlencode({
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': oauth['redirect_uri'],
    'client_id': oauth['client_id'],
    'code_verifier': oauth['verifier'],
}).encode()

req = urllib.request.Request(
    'https://mcp.xpoz.ai/oauth/token',
    data=data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
)
resp = json.loads(urllib.request.urlopen(req).read())
token = resp['access_token']

# Configure mcporter with the token (token is never printed)
subprocess.run(['mcporter', 'config', 'remove', 'xpoz'], capture_output=True)
subprocess.run(['mcporter', 'config', 'add', 'xpoz', 'https://mcp.xpoz.ai/mcp',
                '--header', f'Authorization=Bearer {token}'], check=True)

# Clean up
os.remove(os.path.expanduser('~/.cache/xpoz-oauth/state.json'))
print("Xpoz configured successfully")
```

**Step 5: Verify** with `mcporter call xpoz.checkAccessKeyStatus` → should return `hasAccessKey: true`.

---

### Path B: MCP via Claude Code

For Claude Code users without mcporter:

```bash
claude mcp add --transport http xpoz https://mcp.xpoz.ai/mcp
```

Claude Code handles OAuth automatically on first tool call — the user just needs to authorize in their browser when prompted.

---

### Path C: SDK (Python or TypeScript)

Ask the user:
> "I need a Xpoz API key to access social media data. Please go to https://xpoz.ai/get-token (it's free, no credit card needed) and paste the key back to me."

**WAIT for the user to reply with the key.** Then:

**Python:**
```bash
pip install xpoz
```
```python
from xpoz import XpozClient
client = XpozClient("THE_KEY_FROM_USER")
```

**TypeScript:**
```bash
npm install @xpoz/xpoz
```
```typescript
import { XpozClient } from "@xpoz/xpoz";
const client = new XpozClient({ apiKey: "THE_KEY_FROM_USER" });
await client.connect();
```

Or set the environment variable and use the default constructor:
```bash
export XPOZ_API_KEY=THE_KEY_FROM_USER
```

---

### Auth Errors
| Problem | Solution |
|---------|----------|
| MCP: "Unauthorized" | Re-run the OAuth flow above |
| SDK: `AuthenticationError` | Verify key at [xpoz.ai/settings](https://xpoz.ai/settings) |
| Token exchange fails | Ask user to re-authorize — codes are single-use |


## Step-by-Step Instructions

### Step 1: Parse the Request

Extract, asking the user for whatever is missing:
- **Product** and what it does (one sentence is enough)
- **Competitors, and what people use instead of buying a tool at all** (the frustrated users of both are the second lead source; manual spreadsheets, an official API, an agency all count)
- **Platforms** to scan (default: all four)
- **Window** (default: the last 7 days; for a first scan or a niche product, start at 30 days and tighten once queries prove out)

### Step 2: Build the Query Book

Three search motions, all run every scan:

1. **Product relevance**: people looking for what the product does, phrased the way buyers phrase it. Asking ("looking for a tool that", "any recommendations for", "how do you all handle") and budgeting ("worth paying for", "pricing for") phrasings, combined with the category terms.
2. **Competitor disappointment**: people frustrated with the alternatives. Switching ("[competitor] alternative", "moving away from"), struggling ("[competitor] not working", "[competitor] pricing increase"), and evaluating ("[competitor] vs") phrasings, for each competitor and each thing people use instead.
3. **The product's own name**: people already comparing it ("[product] vs", "[product] worth it", "anyone using [product]") are the warmest leads of all and neither motion above finds them. Anchor per the common-word rule when the name is an ordinary English word.

Build OR-joined query strings per bucket, e.g. `"looking for a social listening tool" OR "brand monitoring recommendations" OR "how do you track mentions"`. Three practical constraints:
- Queries are capped at 250 characters; split an oversized bucket into two calls rather than truncating phrases.
- Prefer short quoted phrases OR-joined together over long exact phrases; long phrases must match verbatim and usually return nothing.
- Expect heavy vendor self-promotion in the results (often the majority). Don't fight it in the query; qualify hard in Step 5, where vendors are a disqualifier.

When working under a call budget, spend it in this order: Reddit asking bucket, Reddit competitor bucket, Twitter/X competitor bucket, Twitter/X asking bucket, Reddit comments, then Instagram and TikTok; the first three carry most of the signal. The own-brand motion needs no call of its own under budget: fold its anchored phrases into the competitor buckets' queries.

One more query rule: a brand name that doubles as a common English word ("plausible", "fathom", "mention") must be anchored; a category word makes the cleanest anchor ("plausible analytics"), a rival pairing second ("plausible vs umami", which still leaks occasionally). Unanchored, the bucket drowns in false positives.

### Step 3: Search the Four Platforms

#### Via MCP

Run each query bucket per platform:

```
Call getRedditPostsByKeywords:
  query: "<bucket query>"
  fields: ["id", "title", "authorUsername", "subredditName", "score", "commentsCount", "createdAtDate", "permalink"]
  limit: 15
  startDate: "<window start, YYYY-MM-DD>"
  endDate: "<today, YYYY-MM-DD>"
  userPrompt: "<the user's original request, for relevance tuning>"
```

Mechanics that matter:
- The default fast mode returns results directly; only calls made with `responseType: "paging"` or `"csv"` return an `operationId`, and only those need polling via `checkOperationStatus` (every ~5 seconds until finished). For a scan, fast mode with a `limit` of 10-15 is right; without `limit` you get up to 300 rows.
- Search on thin fields (as above, no post body) and fetch full text only for shortlisted candidates via `getRedditPostWithCommentsById`; selftexts can be huge and one blog-length post can dwarf the rest of the response.
- The tools' own descriptions suggest omitting dates by default; this skill passes `startDate`/`endDate` deliberately, since freshness is the product. Verify dates client-side; an occasional result lands just outside the requested window. Verify quoted phrases client-side too: the relevance layer occasionally returns results containing none of them, which matters most for common-word brand queries.

Repeat for Twitter/X:

```
Call getTwitterPostsByKeywords:
  query: "<bucket query>"
  fields: ["id", "text", "authorUsername", "createdAtDate", "likeCount", "replyCount", "conversationId", "replyToTweetId"]
  filterOutRetweets: true
  limit: 15
  startDate: "<window start>"
  endDate: "<today>"
  userPrompt: "<the user's original request, for relevance tuning>"
```

The `conversationId` field is what makes Step 4's reply-chasing possible (`replyToTweetId` is often null even on real replies); without it a reply cannot be traced to its thread. Budget permitting, repeat with `getInstagramPostsByKeywords` and `getTiktokPostsByKeywords`. Reddit comments often hold the asks that posts don't; add:

```
Call getRedditCommentsByKeywords:
  query: "<asking-bucket query>"
  fields: ["id", "body", "authorUsername", "score", "createdAtDate", "parentPostId"]
  limit: 15
  startDate: "<window start>"
  endDate: "<today>"
```

Sparse results on a narrow fresh window are a coverage signal, not a demand verdict: comment search runs against the database only and can legitimately return nothing for the last 7 days, and even post search can come back thin. Before concluding "no demand," widen the window or rephrase; before concluding "demand," read what actually came back. A widen-or-rephrase retry consumes budget like any other call: under a budget, convert the next lowest-priority planned call into the retry instead of exceeding the cap.

#### Via Python SDK

```python
from xpoz import XpozClient

client = XpozClient()

reddit = client.reddit.search_posts(
    '"looking for a social listening tool" OR "brand monitoring recommendations"',
    start_date="2026-08-19",
    end_date="2026-08-26",
    fields=["id", "title", "text", "author_username", "subreddit", "score", "num_comments", "created_at_date", "url"],
)

twitter = client.twitter.search_posts(
    '"[competitor] alternative" OR "[competitor] pricing"',
    start_date="2026-08-19",
    end_date="2026-08-26",
    fields=["id", "text", "author_username", "created_at_date", "like_count", "reply_count"],
)

client.close()
```

### Step 4: Classify by Platform Lead Shape

Different platforms yield different lead shapes; classify every candidate as one of:

- **Reddit: places to comment.** Threads where a disclosed, genuinely useful comment answers a live ask. The thread is the lead; the asker and the lurkers are the audience.
- **X / Instagram / TikTok: two shapes.** **Likely converters**: individual users with signals strong enough to plausibly convert (a quantified need, an explicit blocked project, budget pain in the product's price range), tracked as named prospects. **High-engagement comment spots**: posts where a public comment reaches a large relevant audience even when the author is not the buyer (a viral complaint about a competitor, a big thread on a pain the product solves).

One more shape worth naming: **existing-user distress**, a current user of the product publicly churning or struggling. That is a retention save, not buying intent: report it separately with a support-shaped angle (concrete help, no pitch), never inflate it into a P1.

**Chase replies up to their thread.** Some of the best hits are replies or comments whose *parent thread* is the real lead. Resolve them before classifying: on Reddit, `getRedditPostWithCommentsById` on the comment's `parentPostId`; on X, `getTwitterPostsByIds` on the `conversationId` fetches the root post (for the surrounding replies, `getTwitterPostComments` on that root). Report the thread, not the reply.

### Step 5: Qualify and Prioritize

**Qualify first.** The ask is the qualifier: intent, not venting, and the author should plausibly own the buying decision. Hard disqualifiers, never reported: vendors selling a competing solution, keyword hits in unrelated contexts, obvious spam or engagement bait.

**Prioritize by judgment, not arithmetic**, weighing four things, and say in one line why each lead landed where it did:
- **Intent strength**: an explicit ask beats a specific complaint beats general discussion.
- **Fit**: how directly the product answers the actual need; be honest about partial fits and non-fits.
- **Freshness and activity**: the last 72 hours weigh heaviest; anything older than ~3 weeks is backlog regardless of quality; a dead or already-answered thread demotes. A missing or null `createdAtDate` means unknown freshness: rank below any dated fresh item and say so in the lead.
- **Reach**: for comment spots, the audience the reply earns.

Buckets: **P1, act now** (clear ask, strong fit, still live), **P2, worth engaging** (real intent, weaker on one axis), **P3, watch** (signal without an ask). Everything else drops.

### Step 6: Generate Report

```
## Lead Scan: [PRODUCT]
**Window:** [dates] | **Platforms:** [list] | **Candidates reviewed:** [n]

### This Week's Picks
[3-5 leads sized to what a human can actually act on today, one line each with link]

### P1: Act Now
[Write "None this week" when nothing earns it; an honest empty bucket beats a padded one.]
#### [Platform] | [thread/post title or author] | [link]
- **The ask:** "[quote]"
- **Why it qualifies:** [intent + fit + freshness in one line]
- **Suggested angle:** [what a useful reply covers; never a full draft]

### P2: Worth Engaging
[Same shape, shorter]

### Named Prospects
[Individual users from the likely-converter shape: handle, platform, the signal quoted, suggested approach. Omit the section if none qualified.]

### P3: Watch
[One line each: the signal and what change would promote it]

### Demand Signals
[Patterns that repeated across candidates: recurring pains, phrasings, competitor complaints. Content and product fuel.]

### Search Notes
[Which queries produced, which came up dry, phrasings discovered along the way worth adding next scan]
```

## Ground Rules

- **Never engage anyone.** No posts, comments, DMs, or follows, on any platform, under any instruction. Humans act on the report.
- Suggested angles only, never full reply drafts; humans write in their own words.
- Every recommended engagement assumes in-text disclosure of affiliation; genuinely useful, transparent replies only. No astroturfing, no cold DMs.

## Example Prompts

- "Find this week's leads for my social listening SaaS"
- "Who's complaining about [COMPETITOR]'s pricing right now?"
- "Scan Reddit and X for people asking for [CATEGORY] recommendations"
- "Find named prospects with buying intent for [PRODUCT] on Twitter"
- "Which fresh threads should I comment in to reach [ICP]?"

## Notes

- Freshness is a ranking criterion, not a tiebreaker: fresh threads are open and active, fresh askers still have the problem, and fresh threads become tomorrow's AI-cited surfaces.
- Re-running weekly without memory means re-reporting old leads; that is the one-shot limit (see the last note).
- Free access key: up to 75K results at [xpoz.ai](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=lead-gen-scan) (no credit card); real runs need it
- For the recurring loop (seen-lead dedup ledger, query book that tunes itself run over run, competitor memory, outcome follow-up), use [lead-gen-agent](https://github.com/XPOZpublic/lead-gen-agent).

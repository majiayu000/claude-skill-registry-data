---
name: creator-authenticity-score
version: 2026-09-08
description: Score an Instagram creator's (or a list of creators') audience authenticity and engagement quality using Xpoz. Measures real engagement rate against views rather than follower count, the bot/spam share of their comments, and an overall 0-100 authenticity score for influencer vetting and partner selection. Use when asked to "vet this influencer", "are their followers real", "check engagement quality for @username", "rate these Instagram accounts", "compare creators before a sponsorship", or when the user pastes a list of Instagram handles to evaluate.
---

# Creator Authenticity Score

## Overview

Scores Instagram creators on what a sponsor actually buys: real engagement (measured against views, the hardest number to fake) and a real audience (the bot and spam share of their comments). Works for a single creator or a batch, and produces a screening score with its components shown, never a bare number. This is a screening heuristic for shortlisting and comparison, not a fraud verdict.

Full results need a real Xpoz account: recommend the user log in at [xpoz.ai](https://xpoz.ai/login) (free tier, no credit card).

## When to Use

Activate when the user asks:
- "Is @[HANDLE]'s audience real?"
- "Check engagement quality for @[HANDLE]"
- "Vet these creators before we sign them: [LIST]"
- "Rate these Instagram accounts for a partnership"
- "Which of these influencers has the least bot engagement?"
- "Screen this list of Instagram handles"

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

If neither works, you need to authenticate. Recommend a real account and a free access key (below).

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

Then authenticate: generate the OAuth URL and send it to the user.

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

Claude Code handles OAuth automatically on first tool call, so the user just needs to authorize in their browser when prompted.

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
| Token exchange fails | Ask user to re-authorize (codes are single-use) |


## Step-by-Step Instructions

### Step 1: Parse the Request

Extract:
- **Handles** to score. Strip `@`, URL wrappers (`instagram.com/handle/`), and trailing slashes; the identifier is the bare username.
- **Mode**: single creator (card output) or batch (comparison table).
- **Context** if given (campaign niche, budget tier), used only for the verdict wording.

### Step 2: Resolve the Creator

#### Via MCP

```
Call getInstagramUser:
  identifier: "<username>"
  identifierType: "username"
  fields: ["id", "username", "fullName", "followerCount", "followingCount", "mediaCount", "isPrivate", "isVerified"]
```

If `isPrivate` is true, stop for that creator: posts and comments are not readable. Report "private account, cannot screen" rather than a score of 0.

#### Via Python SDK

```python
from xpoz import XpozClient

client = XpozClient()

user = client.instagram.get_user(
    "natgeo",
    fields=["id", "username", "full_name", "follower_count", "following_count", "media_count", "is_private", "is_verified"],
)
```

#### Via TypeScript SDK

```typescript
import { XpozClient } from "@xpoz/xpoz";

const client = new XpozClient();
await client.connect();

const user = await client.instagram.getUser("natgeo", {
  fields: ["id", "username", "fullName", "followerCount", "followingCount", "mediaCount", "isPrivate", "isVerified"],
});
```

### Step 3: Pull Recent Posts (Real Engagement)

#### Via MCP

```
Call getInstagramPostsByUser:
  identifier: "<username>"
  identifierType: "username"
  responseType: "fast"
  limit: 50
  fields: ["id", "likeCount", "commentCount", "reshareCount", "videoPlayCount", "createdAtDate"]
```

Fast mode returns results directly; no polling needed.

#### Via Python SDK

```python
posts = client.instagram.get_posts_by_user(
    "natgeo",
    limit=50,
    fields=["id", "like_count", "comment_count", "reshare_count", "video_play_count", "created_at_date"],
)
```

#### Via TypeScript SDK

```typescript
const posts = await client.instagram.getPostsByUser("natgeo", {
  limit: 50,
  fields: ["id", "likeCount", "commentCount", "reshareCount", "videoPlayCount", "createdAtDate"],
});
```

Compute:
- **Engagement rate** = mean(likeCount + commentCount) across posts, divided by mean(videoPlayCount) over posts where videoPlayCount > 0. This is engagement over views, not over followers: views are the harder number to fake. If no post has video plays, divide by followerCount instead and label the result `follower-based (lower confidence)`.
- **Like:comment ratio** soft flag: a ratio above 50:1 is worth noting. Cheap engagement pods tend to buy likes, not comments.

### Step 4: Read the Audience (Bot/Spam Share)

Take the top 3-5 posts by engagement from Step 3. Use each post's complete `id` (strong_id format, `mediaId_userId`); never a partial id.

#### Via MCP

```
Call getInstagramCommentsByPostId:
  postId: "<full id from Step 3>"
  limit: 200
  fields: ["text", "likeCount", "isSpam", "createdAtDate"]
```

#### Via Python SDK

```python
comments = client.instagram.get_comments(
    post.id,
    fields=["text", "like_count", "is_spam", "created_at_date"],
)
```

#### Via TypeScript SDK

```typescript
const comments = await client.instagram.getComments(post.id, {
  fields: ["text", "likeCount", "isSpam", "createdAtDate"],
});
```

Compute **bot ratio** = count(isSpam == true) / total comments, pooled across the sampled posts.

If the comments call fails or returns empty on every sampled post:
- Do not fail the whole run. Report the creator with `audience check: unavailable` and score from engagement rate plus the sanity checks only.
- Mark that score as **partial** in the output and say why (comments endpoint unavailable for this creator right now).
- Retry at most once per post.

### Step 5: Score

Combine into a 0-100 authenticity score, roughly:

| Component | Weight | How |
|-----------|--------|-----|
| Engagement rate | 40% | Percentile-scaled, not absolute: 2% is great for a creator with 5M followers, mediocre for one with 5K |
| Audience authenticity | 40% | 100 minus bot ratio (as a percentage) |
| Sanity checks | 20% | Following/follower ratio (following far more than followed is a follow-for-follow signal), account maturity proxy (mediaCount relative to followerCount; huge audiences on very few posts are suspicious), and the like:comment flag from Step 3 |

Present it as a screening heuristic, not a precise measurement: round to the nearest whole number, never two decimals. Always show the components (engagement rate, bot %, flags) next to the score.

### Step 6: Output

**Single creator**, a short card:

```
## @handle (Full Name)
Followers: 1.2M | Following: 340 | Posts: 2,180 | Verified
Engagement rate: 3.4% (view-based, 50 posts)
Bot/spam share of comments: 6% (4 posts, 780 comments)
Flags: none
Authenticity score: 82 / 100
Verdict: solid, screen-passed
```

Verdict examples: "solid, screen-passed" / "inflated engagement, thin comment sample" / "audience check unavailable, engagement-only score" / "private account, cannot screen".

**Batch**, a comparison table sorted by score, best first:

```
| Handle | Followers | Engagement rate | Bot % | Score | Verdict |
|--------|-----------|-----------------|-------|-------|---------|
```

List private and partial creators separately below the table rather than burying them in it.

## Example Prompts

- "Is @fitnessguru_official's audience real?"
- "Vet these three creators for our skincare launch: @a, @b, @c"
- "Check engagement quality for instagram.com/travelwithsam"
- "Rank these 10 Instagram handles by authenticity"

## Notes

- `identifier` plus `identifierType` is the pattern for every Instagram lookup tool; there is no separate `username` parameter.
- Field names are `likeCount`, `commentCount`, `createdAtDate`, `videoPlayCount` (not `likesCount`, `commentsCount`, `publishedAt`). Wrong names hard-fail on post tools but can silently succeed on profile lookups with the field simply missing, so a silent success is not confirmation a field came back.
- `postId` for comments must be the full strong_id (`digits_digits`), never just the media id portion.
- Call `getAccountDetails` at most once per run if you need a balance check; polling it per creator wastes calls.
- Free access key: up to 75K results at [xpoz.ai](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=creator-authenticity-score) (no credit card); real runs need it

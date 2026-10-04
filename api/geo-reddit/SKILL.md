---
name: geo-reddit
version: 2026-08-26
description: Map the most influential Reddit venues for a brand's AI visibility using Xpoz. Finds which subreddits and threads AI engines actually cite when answering buyer questions, where those questions get asked, and which live threads are worth answering. Use when asked to "get cited by AI through Reddit", "which subreddits matter for my brand", "Reddit influence map", "where should we engage on Reddit", or "why does ChatGPT cite Reddit for my category".
---

# GEO Reddit

## Overview

Reddit is among the most-cited domains in AI answers, and a helpful comment in a thread the engines already cite inherits that thread's citation. This skill builds a **Reddit influence map**: the ranked list of subreddits and threads where presence would actually move AI answers for a brand, grounded in two evidence streams. First and most important, the citations themselves: which Reddit URLs the AI engines cite when answering the brand's buyer questions, including the answers where competitors win. Second, the demand side via Xpoz: where those questions are actually asked and which live threads are answerable right now. The output is where and what; a human writes and posts everything.

## When to Use

Activate when the user asks:
- "How do I get my brand cited by ChatGPT/Claude/Gemini via Reddit?"
- "Which subreddits matter for [BRAND/CATEGORY]?"
- "Build a Reddit influence map for [PRODUCT]"
- "Where on Reddit should we engage to improve AI visibility?"
- "AI engines cite Reddit for my category. Which threads?"
- "Find Reddit threads worth answering for [TOPIC]"

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

Extract:
- **Brand/product** and its category
- **Competitors** (ask if not given; competitor-winning answers are prime evidence)
- **Target prompts**: 3-8 questions buyers ask AI engines where the brand should appear. If the user has none, derive a starter set: take the problems the product solves and phrase them as a buyer would ask an assistant ("best [category] tool for [persona]", "how do I [job to be done]", "[current tool] alternatives")

### Step 2: Trace the Engine Citations (the primary evidence)

Run each target prompt through the AI engines and capture what they cite. Use the `ai-answer-trace` skill if it is installed. Otherwise fetch `https://raw.githubusercontent.com/XPOZpublic/xpoz-agent-skills/main/skills/ai-answer-trace/SKILL.md` and follow it. If neither is possible, use the degradation ladder that skill describes (host web search, or user-pasted AI answers with sources).

From the traces, extract every `reddit.com` URL in `cited_urls` and in `searches[].results`:
- **Cited threads**: the exact threads whose content shaped answers. Record which prompt, which engine, cited or only retrieved, and whether the answer named a competitor.
- **Subreddits behind them**: parse `/r/<subreddit>/` from each URL.
- Count instances across prompts and samples: a subreddit cited on 3 prompts outranks one cited once.

If no Reddit URLs appear at all, say so plainly: it means Reddit is currently not an influencing surface for these prompts, and the map's value flips to the demand side only.

### Step 3: Research the Venues with Xpoz

Fill in what the citations alone cannot tell you: where the questions live and what is answerable now.

#### Via MCP

Find where the target questions are asked:

```
Call getRedditPostsByKeywords:
  query: "<question phrasing variants, OR-joined, short quoted phrases>"
  fields: ["id", "title", "authorUsername", "subredditName", "score", "commentsCount", "createdAtDate", "permalink"]
  limit: 15
  startDate: "<90 days ago, YYYY-MM-DD>"
  endDate: "<today, YYYY-MM-DD>"
```

The default fast mode returns results directly (pass `limit`; queries cap at 250 characters). Only calls made with `responseType: "paging"` or `"csv"` return an `operationId` to poll via `checkOperationStatus` (every ~5 seconds until finished). Fetch full post text only for the threads you shortlist, via the thread fetch below.

Explore the subreddits the traces surfaced (and discover adjacent ones):

```
Call searchRedditSubreddits:
  query: "<category / topic>"
  fields: ["name", "title", "description", "subscribers"]
```

Read the winning threads in full before judging what a good answer looks like:

```
Call getRedditPostWithCommentsById:
  postId: "<id of a cited thread>"
```

#### Via Python SDK

```python
from xpoz import XpozClient

client = XpozClient()

posts = client.reddit.search_posts(
    '"best social listening tool" OR "how do I monitor brand mentions"',
    start_date="2026-05-28",
    end_date="2026-08-26",
    fields=["id", "title", "text", "subreddit", "score", "num_comments", "created_at_date", "url"],
)

all_posts = posts.data
while posts.has_next_page():
    posts = posts.next_page()
    all_posts.extend(posts.data)

subreddits = client.reddit.search_subreddits("social listening")

client.close()
```

### Step 4: Build the Influence Map

Rank venues by expected influence on AI answers, in this order:

1. **Cited threads** from Step 2: threads engines already cite for the target prompts. Highest value; a quality answer there inherits an existing citation path. Weight by how many prompts and engines cite them and by the prompts' business value.
2. **Cited subreddits**: subreddits whose other threads engines cite. New threads and answers there sit on trusted ground.
3. **Live demand threads** from Step 3: fresh, active threads asking the target questions. Not yet cited, but they are tomorrow's citations and today's direct audience.
4. **Demand-heavy subreddits** with no citations yet: where questions concentrate. Lowest AI-influence confidence; note them as watch items, not recommendations.

For each recommended venue, read enough (Step 3's thread fetch) to write one line on what a winning contribution contains: what the currently-cited or top-voted answers do well, and what gap a better answer would fill.

### Step 5: Generate Report

```
## Reddit Influence Map: [BRAND]
**Prompts traced:** [N] | **Engines:** [list] | **Date:** [date]

### Verdict
[2-3 sentences: how much of the AI answer surface for these prompts runs through Reddit, and the single highest-leverage venue]

### Cited Threads (engines already cite these)
| Thread | Subreddit | Cited by | Prompts | Competitor named? | What a winning answer adds |
|--------|-----------|----------|---------|-------------------|----------------------------|
| [title + link] | r/[sub] | [engines] | [which] | [yes/no, who] | [one line] |

### Influential Subreddits
| Subreddit | Citation instances | Subscribers | Why it matters |
|-----------|--------------------|-------------|----------------|
| r/[sub] | [n] | [n] | [one line] |

### Live Threads Worth Answering Now
| Thread | Subreddit | Age | Engagement | The ask |
|--------|-----------|-----|------------|---------|
| [title + link] | r/[sub] | [days] | [score/comments] | [one line] |

### Watch List
[Demand-heavy venues with no citations yet, one line each]

### Before Anyone Posts
[Per-venue notes: each sub's self-promotion rules as stated in its sidebar/wiki, disclosure requirements, tone of the currently-winning answers]
```

## Ground Rules

- This skill recommends where and what. **A human writes and posts everything.** Never post, comment, or message anyone.
- Any brand-affiliated answer must disclose the affiliation in the post itself; a profile bio is not enough.
- Check and respect each subreddit's self-promotion rules before recommending it as a posting venue; if a sub bans vendor participation, say so in the report instead of suggesting workarounds.
- Recommend genuinely useful contributions to real questions. Manufactured threads, vote manipulation, or sockpuppet accounts are off the table and poison the citation well for everyone.

## Example Prompts

- "Build a Reddit influence map for xpoz in the social data API category"
- "ChatGPT cites Reddit when people ask about [CATEGORY]. Which threads and subreddits?"
- "Where should [BRAND] earn Reddit presence to show up in AI answers?"
- "Find live Reddit threads asking about [PROBLEM] that we could answer"
- "Which subreddits do AI engines trust for [TOPIC]?"

## Notes

- Step 2 needs AI engine API keys (see `ai-answer-trace`); Step 3 needs only xpoz. With no engine access, deliver the demand-side map and label it as such.
- Re-run the map after meaningful engagement: the point is watching venues move from "live thread" to "cited thread".
- Free access key: up to 75K results at [xpoz.ai](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=geo-reddit) (no credit card); real runs need it
- For the ongoing program (weekly visibility measurement, gap analysis, content production, and engagement tracking around these venues), use [geo-seo-agent](https://github.com/XPOZpublic/geo-seo-agent).

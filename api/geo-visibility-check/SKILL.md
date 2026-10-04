---
name: geo-visibility-check
version: 2026-08-26
description: One-shot GEO visibility check for a brand using Xpoz. Runs the buyer questions that matter through Claude, ChatGPT, and Gemini, and reports where the brand appears, who wins instead, and which surfaces the answers are assembled from. Use when asked to "check my AI visibility", "does ChatGPT recommend us", "GEO audit", "where do we show up in AI answers", or "who wins our category in AI answers".
---

# GEO Visibility Check

## Overview

Buyers increasingly start, and often finish, their research inside AI engines. This skill answers the first question of any GEO effort: for the questions that matter, does the brand appear in AI answers, and if not, who does and through which sources? It assembles a small panel of buyer prompts, runs each through the engines with full citation tracing, and delivers a per-prompt visibility verdict plus a read on where the winning answers come from. One-shot by design; it is the measurement pass that tells you whether a full GEO program is worth running.

## When to Use

Activate when the user asks:
- "Do AI assistants recommend [BRAND]?"
- "Check our AI/GEO visibility"
- "Where does [BRAND] show up in ChatGPT/Claude/Gemini answers?"
- "Who wins [CATEGORY] in AI answers, and why?"
- "Run a GEO audit for [PRODUCT]"
- "Which sources do AI engines use for our category?"

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

### Step 1: Build the Prompt Panel

Collect 5-10 buyer prompts. Sources, best first:

1. **The user's own list**: the questions they believe buyers ask. Take these as given.
2. **Community demand via Xpoz**: mine the real phrasings buyers use. Search for questions around the problems the product solves:

```
Call getRedditPostsByKeywords:
  query: "<problem phrasings, OR-joined, e.g. 'best tool for X' OR 'how do I X' OR 'X alternative'>"
  fields: ["id", "title", "subredditName", "score", "commentsCount", "createdAtDate"]
  limit: 15
  startDate: "<90 days ago, YYYY-MM-DD>"
  endDate: "<today, YYYY-MM-DD>"
```

The default fast mode returns results directly (pass `limit`; queries cap at 250 characters); only `responseType: "paging"`/`"csv"` calls return an `operationId` to poll via `checkOperationStatus` (every ~5 seconds until finished). Repeat with `getTwitterPostsByKeywords` (pass `filterOutRetweets: true`) for the developer/founder conversation.

3. **Derived**: phrase the product's jobs-to-be-done as assistant questions ("best [category] for [persona]", "how do I [job]", "[current tool] alternatives", "how much does [category thing] cost").

Balance the panel across intents: category ("best X"), comparison ("X vs Y", "X alternatives"), problem-solution ("how do I..."), and pricing. Confirm the panel with the user before spending engine calls on it.

### Step 2: Trace Every Prompt

Run each panel prompt through the AI engines with citation capture. Use the `ai-answer-trace` skill if it is installed. Otherwise fetch `https://raw.githubusercontent.com/XPOZpublic/xpoz-agent-skills/main/skills/ai-answer-trace/SKILL.md` and follow it. If neither is possible, use the degradation ladder that skill describes.

Defaults: every engine with a key configured, 2 samples per engine per prompt. That is `prompts x engines x 2` paid API calls; state the number and get a nod before running a large panel.

No engine keys at all? Deliver the demand-side half only: the panel itself, built from real community phrasings, plus where those questions concentrate. Label the report clearly as demand research without engine measurement.

### Step 3: Judge Visibility Per Prompt

For each prompt and engine, from the trace JSONs:

- **Present**: is the brand named in the answer? How: recommended outright, listed among options, mentioned in passing, or absent?
- **Cited**: does any brand-owned URL appear in `cited_urls` (site, docs, listings)? An answer can name the brand while citing someone else's page about it; record the actual citation path.
- **Winners**: who is recommended instead or above, and via which cited URLs?
- **Stability**: consistent across samples, or a coin flip?

Aggregate cited domains across all traces (the `cited-domains.py` chunk in `ai-answer-trace`) and classify the top domains by surface type: own sites, review sites and directories, community threads, documentation, publisher listicles.

### Step 4: Generate Report

```
## GEO Visibility Check: [BRAND]
**Panel:** [N] prompts | **Engines:** [list] | **Samples:** [N] per engine | **Date:** [date]

### Verdict
[2-3 sentences: overall visibility, the strongest and weakest surface, the single most valuable lost prompt]

### Per-Prompt Visibility
| Prompt | Claude | ChatGPT | Gemini | Who wins |
|--------|--------|---------|--------|----------|
| [prompt] | [recommended / listed / absent] | ... | ... | [competitor + citation path] |

### Where the Answers Come From
| Domain | Instances | Surface type |
|--------|-----------|--------------|
| [domain] | [n] | [own site / review site / community / docs / listicle] |

### Brand Citation Paths
[For each prompt where the brand appears: which URL carried it into the answer]

### Lost Prompts, Diagnosed
[For each absent/losing prompt: what the winning citations are, and what kind of asset could enter that surface]

### Recommended Next Steps
[3-5 bullets tied to the evidence: which surface to work first, which prompts are winnable]
```

## Example Prompts

- "Check whether AI assistants recommend xpoz for social media data"
- "GEO audit for [BRAND]: 8 prompts, all three engines"
- "Does ChatGPT know about our product? Who does it recommend for [CATEGORY]?"
- "Which sources do AI engines assemble [CATEGORY] answers from?"
- "Find the buyer questions where we're absent from AI answers"

## Notes

- Step 2 needs AI engine API keys (see `ai-answer-trace`); Step 1's community mining needs only xpoz.
- Engine answers are nondeterministic; the per-prompt verdict needs 2+ samples to mean anything.
- Keep the trace JSONs and the report; a re-run next month against the same panel is a real before/after.
- If community citations dominate the lost prompts, run [geo-reddit](../geo-reddit/SKILL.md) next to map the exact venues.
- Free access key: up to 75K results at [xpoz.ai](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=geo-visibility-check) (no credit card); real runs need it
- For the weekly program this check previews (tracked prompt panel, dated snapshots, gap analysis, content production and rework), use [geo-seo-agent](https://github.com/XPOZpublic/geo-seo-agent).

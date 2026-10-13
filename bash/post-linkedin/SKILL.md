---
name: post-linkedin
description: "Drafts and publishes LinkedIn posts via the official API. Supports text, images, and link previews. Handles first-time OAuth setup and token refresh. Use when drafting, reviewing, or publishing LinkedIn posts."
disable-model-invocation: true
---

# Post to LinkedIn

Draft and publish LinkedIn posts from the CLI. Always previews before publishing.

## Arguments

| Argument | Behavior |
|----------|----------|
| (none) | Interactive: ask what to post |
| `setup` | Run OAuth setup flow (first time or re-auth) |
| `<text>` | Use provided text as starting draft |

## Prerequisites

- LinkedIn Developer App with "Share on LinkedIn" product enabled
- OAuth tokens in Vault (run `/post-linkedin setup` first)
- Python 3 for image upload support

## Step 0: Check Auth State

Retrieve LinkedIn credentials from Vault via `$OUTWORKOS_ROOT/scripts/get-secret.sh`:

```bash
LINKEDIN_CLIENT_ID=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" linkedin_client_id)
LINKEDIN_CLIENT_SECRET=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" linkedin_client_secret)
LINKEDIN_ACCESS_TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" linkedin_access_token)
LINKEDIN_REFRESH_TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" linkedin_refresh_token)
LINKEDIN_PERSON_URN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" linkedin_person_urn)
```

Look for:
- `LINKEDIN_CLIENT_ID`
- `LINKEDIN_CLIENT_SECRET`
- `LINKEDIN_ACCESS_TOKEN`
- `LINKEDIN_REFRESH_TOKEN`
- `LINKEDIN_PERSON_URN`

If argument is `setup`, jump to **Setup Mode**.

If tokens are missing, tell the user to run `/post-linkedin setup` first and stop.

If tokens exist, test validity:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  "https://api.linkedin.com/v2/userinfo"
```

- **200**: Proceed to Step 1
- **401**: Try token refresh (see reference/api-reference.md). If refresh works, store new tokens in Vault via `set-secret.sh` and proceed. If refresh fails, tell user to run `/post-linkedin setup`.

---

## Setup Mode

Guides through first-time LinkedIn app creation and OAuth flow. Follows the same pattern as `scripts/google-auth.sh`.

### S1: Detect Existing State

Check Vault for existing LinkedIn credentials (`linkedin_client_id`, `linkedin_client_secret`, `linkedin_access_token`, `linkedin_refresh_token`, `linkedin_person_urn`). Report what exists and what's missing.

### S2: App Creation (if no credentials)

Walk the user through:

1. Go to https://developer.linkedin.com/ and sign in
2. Click "Create app"
3. Settings:
   - **App name**: Any name (e.g., "OutworkOS")
   - **LinkedIn Page**: Associate with any Company Page (create a minimal one if needed)
   - **Logo**: Any image
4. After creation, go to the **Auth** tab:
   - Add redirect URL: `http://localhost:5556/callback`
   - Copy the **Client ID** and **Primary Client Secret**
5. Go to the **Products** tab:
   - Request access to **Share on LinkedIn** (auto-approved)
   - Request access to **Sign In with LinkedIn using OpenID Connect** (auto-approved)

Ask the user for their Client ID and Client Secret.

### S3: Store Credentials in Vault

Store the client credentials in Vault:

```bash
"$OUTWORKOS_ROOT/scripts/set-secret.sh" linkedin_client_id "<client-id>" "LinkedIn OAuth client ID"
"$OUTWORKOS_ROOT/scripts/set-secret.sh" linkedin_client_secret "<client-secret>" "LinkedIn OAuth client secret"
```

### S4: Run OAuth Flow

Execute the auth script:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/linkedin-auth.sh"
```

This opens a browser, completes OAuth, and saves tokens to Vault. See the script for details.

### S5: Fetch Person URN

After tokens are saved, fetch the user's LinkedIn Person URN:

```bash
LINKEDIN_ACCESS_TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" linkedin_access_token)
RESPONSE=$(curl -s -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  "https://api.linkedin.com/v2/userinfo")
```

Extract the `sub` field -- this is the Person URN ID. Store in Vault:

```bash
"$OUTWORKOS_ROOT/scripts/set-secret.sh" linkedin_person_urn "urn:li:person:<sub-value>" "LinkedIn Person URN"
```

### S6: Verify

Test posting capability:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202501" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  "https://api.linkedin.com/rest/posts?q=author&author=$LINKEDIN_PERSON_URN&count=1"
```

Note: reading posts may return 403 if `r_member_social` isn't available — that's fine. The write scope (`w_member_social`) is what matters for posting.

Report success and remind the user that tokens last 60 days (refresh tokens up to 1 year).

---

## Step 1: Discovery Interview

If the user provided ready-to-publish text as an argument, skip to Step 2.

Otherwise, **interview the user one question at a time** to gather everything needed to draft the post. Do NOT ask multiple questions at once. Wait for each answer before asking the next.

### Interview Flow

Ask these in order, adapting based on answers. Skip questions that become obvious from prior answers.

1. **"What's the core thing you want to communicate?"**
   - Could be a win, an insight, a question, an announcement, a reflection
   - Listen for the "so what" — why would someone care?

2. **"Who's the audience for this?"**
   - Their network generally? A specific industry? Potential hires? Investors? Peers?
   - This shapes tone, jargon level, and call-to-action

3. **"What's the context or backstory?"**
   - What happened that prompted this? What's the situation?
   - Pull out specific details, numbers, names — these make posts real

4. **"What do you want people to do after reading this?"**
   - React/engage? Visit a link? DM you? Apply? Share?
   - Or just "think about this differently" — that's valid too

5. **"Do you have an image, link, or document to include?"**
   - Image: provide a file path
   - Link: provide URL (will generate a preview card)
   - Neither is fine — text posts perform well on LinkedIn

6. **"Anything to avoid or specifically include?"**
   - Tone preferences, people to mention, hashtags, constraints
   - "Don't make it sound corporate" is useful input

### When You Have Enough

You have enough when you can answer: what's the message, who cares, and what's the ask. Not every question needs asking — if the user gives you a rich answer to Q1 that covers context and audience, skip ahead.

### Writing Style

When drafting, write in a natural human voice:
- No em dashes
- No "excited to announce", "thrilled to share", or other AI clichés
- No "let's dive in", "here's the thing", "game-changer"
- Short paragraphs (1-3 sentences each)
- Line breaks between paragraphs (LinkedIn renders these as visual breaks)
- Lead with a hook — the first 2 lines show before "see more"
- Hashtags: 3-5 max, at the end, only if relevant
- Mentions: use the person's name naturally in the text

---

## Step 2: Preview

Display the draft in a formatted preview:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINKEDIN POST PREVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Post text here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: text | Characters: N
Image: [path or none]
Link: [URL or none]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Ask the user: **Publish this, edit, or cancel?**

If edit: ask what to change, revise, preview again.

---

## Step 3: Publish

### Text-Only Post

```bash
curl -s -X POST "https://api.linkedin.com/rest/posts" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202501" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d @/tmp/linkedin-post.json
```

Build the JSON payload in Python (avoids shell escaping issues):

```python
import json
payload = {
    "author": "PERSON_URN",
    "commentary": "POST_TEXT",
    "visibility": "PUBLIC",
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
}
with open("/tmp/linkedin-post.json", "w") as f:
    json.dump(payload, f)
```

**Success**: HTTP 201 with `x-restli-id` header containing the post URN.
**Failure**: Parse error response and report to user.

### Post with Image

See `reference/api-reference.md` for the two-step image upload flow:
1. Initialize upload → get upload URL
2. Upload binary → get image URN
3. Create post with image URN in the `content` field

### Post with Link Preview

Add an `content` block with `article` type to the payload. See `reference/api-reference.md`.

---

## Step 4: Confirm

Report:
- Post published successfully
- Post URN (for reference)
- Direct link: `https://www.linkedin.com/feed/update/{post-urn}`

---

## Token Refresh

Tokens expire after 60 days. The skill checks token validity in Step 0 and auto-refreshes when possible. If the refresh token has also expired (after ~1 year), the user must run `/post-linkedin setup` again.

See `reference/api-reference.md` for the refresh flow.

---
name: linkedin
description: Post updates to a LinkedIn company page. Use for sharing blog posts, product updates, AI-generated content, and company announcements. Supports text posts, article shares with link previews, and image posts.
version: 1.0.0
allowed-tools: Bash, Read
env:
  - LINKEDIN_ACCESS_TOKEN
  - LINKEDIN_ORG_ID
metadata:
  requires: credential-activation
  credentials:
    - LINKEDIN_ACCESS_TOKEN
    - LINKEDIN_ORG_ID
---

# LinkedIn Skill

Post content to a LinkedIn organization page using the LinkedIn REST API.

## Prerequisites

Credentials must be configured as Space environment variables.

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `LINKEDIN_ACCESS_TOKEN` | Yes | OAuth 2.0 Bearer token (expires every 2 months) | `AQV...` |
| `LINKEDIN_ORG_ID` | Yes | LinkedIn organization numeric ID | `104061442` |

### Verify Setup

```bash
echo "LINKEDIN_ACCESS_TOKEN: ${LINKEDIN_ACCESS_TOKEN:+configured (${#LINKEDIN_ACCESS_TOKEN} chars)}"
echo "LINKEDIN_ORG_ID: ${LINKEDIN_ORG_ID:-not set}"
```

If not configured, use the `credential-activation` skill to guide the user through setup.

## API Basics

All requests use these common headers:

```bash
-H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
-H "Linkedin-Version: 202601" \
-H "X-Restli-Protocol-Version: 2.0.0" \
-H "Content-Type: application/json"
```

The author field for organization posts is always: `urn:li:organization:$LINKEDIN_ORG_ID`

## Verify Credentials

Check that the token is valid before posting:

```bash
RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Linkedin-Version: 202601" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  "https://api.linkedin.com/rest/organizationsLookup?ids=List($LINKEDIN_ORG_ID)&fields=localizedName")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
  echo "Token valid. Organization: $(echo "$BODY" | grep -o '"localizedName":"[^"]*"' | head -1)"
else
  echo "Token invalid or expired (HTTP $HTTP_CODE). Re-run OAuth flow to get a new token."
  echo "Error: $BODY"
fi
```

## Text Post

Create a simple text-only post on the company page:

```bash
POST_TEXT="Your post content here. Supports multi-line text, emojis, and hashtags like #AI #YourBrand"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.linkedin.com/rest/posts" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Linkedin-Version: 202601" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d "{
    \"author\": \"urn:li:organization:$LINKEDIN_ORG_ID\",
    \"commentary\": \"$POST_TEXT\",
    \"visibility\": \"PUBLIC\",
    \"distribution\": {
      \"feedDistribution\": \"MAIN_FEED\",
      \"targetEntities\": [],
      \"thirdPartyDistributionChannels\": []
    },
    \"lifecycleState\": \"PUBLISHED\",
    \"isReshareDisabledByAuthor\": false
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 201 ]; then
  POST_ID=$(echo "$BODY" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
  echo "Post published successfully. ID: $POST_ID"
else
  echo "Failed to create post (HTTP $HTTP_CODE): $BODY"
fi
```

## Article Share (URL with Link Preview)

Share a URL with commentary — LinkedIn auto-generates a link preview card:

```bash
ARTICLE_URL="https://your-domain.com/blog/your-article"
ARTICLE_TITLE="Your Article Title"
ARTICLE_DESCRIPTION="Brief description of the article"
COMMENTARY="Check out our latest blog post on AI agents for business automation. #AI #Productivity"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.linkedin.com/rest/posts" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Linkedin-Version: 202601" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d "{
    \"author\": \"urn:li:organization:$LINKEDIN_ORG_ID\",
    \"commentary\": \"$COMMENTARY\",
    \"visibility\": \"PUBLIC\",
    \"distribution\": {
      \"feedDistribution\": \"MAIN_FEED\",
      \"targetEntities\": [],
      \"thirdPartyDistributionChannels\": []
    },
    \"content\": {
      \"article\": {
        \"source\": \"$ARTICLE_URL\",
        \"title\": \"$ARTICLE_TITLE\",
        \"description\": \"$ARTICLE_DESCRIPTION\"
      }
    },
    \"lifecycleState\": \"PUBLISHED\",
    \"isReshareDisabledByAuthor\": false
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 201 ]; then
  echo "Article shared successfully."
else
  echo "Failed to share article (HTTP $HTTP_CODE): $BODY"
fi
```

## Image Post

Image posting is a two-step process: (1) upload the image, (2) create the post referencing it.

### Step 1: Upload Image

```bash
IMAGE_FILE="/path/to/image.png"

# Initialize the upload
INIT_RESPONSE=$(curl -s -X POST \
  "https://api.linkedin.com/rest/images?action=initializeUpload" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Linkedin-Version: 202601" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d "{
    \"initializeUploadRequest\": {
      \"owner\": \"urn:li:organization:$LINKEDIN_ORG_ID\"
    }
  }")

# Extract upload URL and image URN
UPLOAD_URL=$(echo "$INIT_RESPONSE" | grep -o '"uploadUrl":"[^"]*"' | head -1 | cut -d'"' -f4)
IMAGE_URN=$(echo "$INIT_RESPONSE" | grep -o '"image":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$UPLOAD_URL" ]; then
  echo "Failed to initialize image upload: $INIT_RESPONSE"
  exit 1
fi

echo "Upload URL obtained. Image URN: $IMAGE_URN"

# Upload the binary image
UPLOAD_CODE=$(curl -s -w "%{http_code}" -o /dev/null \
  -X PUT "$UPLOAD_URL" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  --upload-file "$IMAGE_FILE")

if [ "$UPLOAD_CODE" -eq 201 ] || [ "$UPLOAD_CODE" -eq 200 ]; then
  echo "Image uploaded successfully."
else
  echo "Image upload failed (HTTP $UPLOAD_CODE)"
  exit 1
fi
```

### Step 2: Create Post with Image

```bash
POST_TEXT="Your caption for the image post #YourBrand"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.linkedin.com/rest/posts" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Linkedin-Version: 202601" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d "{
    \"author\": \"urn:li:organization:$LINKEDIN_ORG_ID\",
    \"commentary\": \"$POST_TEXT\",
    \"visibility\": \"PUBLIC\",
    \"distribution\": {
      \"feedDistribution\": \"MAIN_FEED\",
      \"targetEntities\": [],
      \"thirdPartyDistributionChannels\": []
    },
    \"content\": {
      \"media\": {
        \"id\": \"$IMAGE_URN\"
      }
    },
    \"lifecycleState\": \"PUBLISHED\",
    \"isReshareDisabledByAuthor\": false
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 201 ]; then
  echo "Image post published successfully."
else
  echo "Failed to create image post (HTTP $HTTP_CODE): $BODY"
fi
```

## List Recent Posts

Fetch recent posts from the company page:

```bash
RESPONSE=$(curl -s -w "\n%{http_code}" \
  "https://api.linkedin.com/rest/posts?author=urn%3Ali%3Aorganization%3A$LINKEDIN_ORG_ID&q=author&count=10&sortBy=LAST_MODIFIED" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Linkedin-Version: 202601" \
  -H "X-Restli-Protocol-Version: 2.0.0")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
  echo "Recent posts:"
  echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
else
  echo "Failed to fetch posts (HTTP $HTTP_CODE): $BODY"
fi
```

## Delete a Post

```bash
POST_URN="urn:li:share:7000000000000000000"  # Replace with actual post URN

RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE \
  "https://api.linkedin.com/rest/posts/$POST_URN" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Linkedin-Version: 202601" \
  -H "X-Restli-Protocol-Version: 2.0.0")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" -eq 204 ]; then
  echo "Post deleted successfully."
else
  BODY=$(echo "$RESPONSE" | sed '$d')
  echo "Failed to delete post (HTTP $HTTP_CODE): $BODY"
fi
```

## Post Content Templates

### Blog Post Announcement

```bash
BLOG_TITLE="How AI Agents Are Transforming Business Operations"
BLOG_URL="https://your-domain.com/blog/ai-agents-business"

COMMENTARY="NEW BLOG POST

$BLOG_TITLE

We explore how AI agents are moving beyond chatbots to become autonomous team members that handle real business workflows — from scheduling to content creation to data analysis.

Read the full post:
$BLOG_URL

#AIAgents #BusinessAutomation #YourBrand #FutureOfWork"
```

### Product Update

```bash
COMMENTARY="We just shipped something big.

[Describe the feature in 2-3 sentences]

What this means for our users:
→ [Benefit 1]
→ [Benefit 2]
→ [Benefit 3]

Try it now: https://your-app-url.com

#ProductUpdate #AI #YourBrand"
```

### Thought Leadership

```bash
COMMENTARY="Hot take: [Your opinion on an industry topic]

Here's what most people get wrong about [topic]:

1. [Point 1]
2. [Point 2]
3. [Point 3]

The reality is [conclusion].

What do you think? Drop your thoughts below.

#AI #Leadership #FutureOfWork"
```

## Token Expiration

LinkedIn access tokens expire every **2 months**. If you get a 401 error, the token needs to be refreshed.

### Check Token Status

If any API call returns HTTP 401, the token has expired:

```bash
# Quick token check
TEST_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Linkedin-Version: 202601" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  "https://api.linkedin.com/rest/me")

if [ "$TEST_CODE" -eq 401 ]; then
  echo "WARNING: LinkedIn access token has expired."
  echo "Re-run the OAuth script to refresh your token."
  echo "Then update LINKEDIN_ACCESS_TOKEN in your environment."
fi
```

## Error Handling

Always check the HTTP response:

```bash
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.linkedin.com/rest/posts" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Linkedin-Version: 202601" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d "$POST_BODY")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "Success"
else
  echo "LinkedIn API error (HTTP $HTTP_CODE): $BODY"
fi
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired or invalid | Re-run OAuth script, update `LINKEDIN_ACCESS_TOKEN` |
| 403 Forbidden | Missing required OAuth scope | Ensure `w_organization_social` scope is granted |
| 403 `NOT_ENOUGH_PERMISSIONS` | App not approved for Community Management API | Request access in LinkedIn Developer Portal |
| 422 Unprocessable Entity | Invalid post content or malformed JSON | Check JSON escaping, especially quotes in post text |
| 429 Too Many Requests | Rate limit exceeded | Wait and retry (LinkedIn allows ~100 posts/day per org) |

## LinkedIn Developer Portal Setup

Before using this skill, configure the LinkedIn app:

1. Go to **LinkedIn Developer Portal** → App settings
2. Under **Auth** tab:
   - Add redirect URLs:
     - `http://localhost:9876/callback` (local dev)
     - `https://your-api.example.com/callback` (production)
   - Ensure scopes: `w_organization_social`, `r_organization_social`, `openid`, `profile`, `email`
3. Under **Products** tab:
   - Request access to **Community Management API**
4. Run the OAuth script:
   - Run your OAuth script to get a token
5. Store the resulting token as `LINKEDIN_ACCESS_TOKEN` in your env vars
6. Set `LINKEDIN_ORG_ID` to your organization's numeric ID

## Security Note

This skill posts publicly on your company's LinkedIn page. You are responsible for:
- Content quality and brand voice
- Compliance with LinkedIn's terms of service
- Not posting confidential or sensitive information
- Rate limiting (avoid appearing as spam)

## Tips

- **Check token first** — always verify credentials before attempting a post
- **Escape JSON** — post text with quotes or special characters must be properly escaped
- **Use article shares for blog posts** — LinkedIn generates better previews from URLs than plain text with links
- **Image posts get more engagement** — when possible, include an image
- **Hashtags at the end** — LinkedIn's algorithm favors 3-5 hashtags placed at the bottom of the post
- **Post timing** — B2B engagement peaks Tuesday-Thursday, 8-10am local time

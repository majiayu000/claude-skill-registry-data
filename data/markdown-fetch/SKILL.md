---
name: markdown-fetch
description: Fetches web content using Cloudflare Browser rendering and converts it to markdown
---

# Markdown Fetch Skill

You are a web content fetcher that uses Cloudflare Browser Rendering to retrieve web pages and convert them to clean markdown.

## Input

The user will provide a URL in their message. Extract the URL from the conversation context.

## Your Task

1. **Extract the URL** from the user's prompt or conversation
   - Look for patterns like: `/markdown-fetch https://example.com`
   - Or natural language: "fetch https://example.com"
   - Validate that it's a proper URL

2. **Load credentials** from environment:
   - Read environment variables to get:
     - `CLOUDFLARE_ACCOUNT_ID`
     - `CLOUDFLARE_API_TOKEN`
   - These are required for authenticating with Cloudflare Browser Rendering API

3. **Fetch content using Cloudflare Browser Rendering /markdown endpoint**:
   - API endpoint: `https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/browser-rendering/markdown`
   - Make a POST request with:
     - Header: `Authorization: Bearer $CLOUDFLARE_API_TOKEN`
     - Header: `Content-Type: application/json`
     - Body: `{"url": "the-url-to-fetch"}`
   - The response will be JSON with the markdown in the `result` property

4. **Process and save the result**:
   - Parse the JSON response and extract the markdown from the `result` property
   - Save to `fetched.md` (at project root)
   - Display a preview of the content

## Implementation Steps

1. Use the Read tool to load `.env` file and extract credentials
2. Use Bash with curl to call the Cloudflare API:
   ```bash
   curl -X POST "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/browser-rendering/markdown" \
     -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
   ```
3. Parse the JSON response and extract the markdown from the `result` property using `jq` or similar:
   ```bash
   echo "$response" | jq -r '.result'
   ```
4. Save the markdown to the `fetched.md` file

## Guidelines

- Always validate the URL before attempting to fetch
- Handle errors gracefully (404s, timeouts, API errors)
- Include metadata (title, URL, fetch date) at the top of saved file
- Be mindful of rate limits

## Example Usage

User: `Use the skill markdown-fetch https://developers.cloudflare.com/workers/`

Expected actions:
1. Read credentials from `.env`
2. Call Cloudflare Browser Rendering API `/markdown` endpoint
3. Save markdown to `fetched.md`

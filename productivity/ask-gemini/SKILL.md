---
name: ask-gemini
description: >
  Ask Google Gemini a question via browser automation at gemini.google.com.
  Use when the user asks to ask Gemini a question, wants to interact with
  Google Gemini, or wants to pose a question or get information from Gemini.
---

# Ask Gemini (Google)

Ask Google Gemini a question via browser automation at gemini.google.com.

## Prerequisites

- User must already be logged into Google account in browser (check for account avatar in top-right)
- Browser session already initialized (`browser_navigate` required)

## Steps

1. **Navigate to Gemini:**
   ```
   browser_navigate(url='https://gemini.google.com')
   ```

2. **Verify the correct page loaded:** Immediately check `browser_snapshot`. If the page is NOT Gemini (e.g., landed on AssetSentry, Facebook, etc.), the browser has a tab-switching issue:
   ```
   # Check all open tabs via CDP
   browser_cdp(method='Target.getTargets', params={})
   # Navigate again with full URL including /app if needed
   browser_navigate(url='https://gemini.google.com/app')
   ```

3. **Wait for page to load and find input field.** Use `browser_snapshot` to locate the textarea. Look for a textbox labeled "Enter a prompt for Gemini". Note its ref (e.g., `@e17`). Also note the send button ref (e.g., `@e13`).

4. **Type the question:**
   ```
   browser_type(ref='@<input_ref>', text='<your question>')
   ```

5. **Submit:** Click the send button OR press Enter:
   ```
   browser_click(ref='@<send_button_ref>')
   # OR
   browser_press(key='Enter')
   ```

6. **Wait for response:** Gemini's response may take multiple polling cycles before rendering. Poll with `browser_vision` or `browser_snapshot` until you see the response text appear (indicated by a sparkle/typing indicator disappearing).

7. **Read the answer — use `browser_console` for long responses (RECOMMENDED):**
   ```
   browser_console(expression='document.querySelector("main")?.innerText || document.querySelector(".wEwyrc")?.innerText || "not found"')
   ```
   ⚠️ The old selector `document.querySelector("main").innerText` often returns `null` and fails. Always use optional chaining (`?.`) and fallback selectors.

   If `browser_console` fails or returns empty, fall back to `browser_vision`:
   ```
   browser_vision(question='Read ALL of Gemini\\'s response text from the beginning. Include ALL sections, bullet points, and data. Don\\'t stop until you\\'ve read everything Gemini wrote.')
   ```

8. **Send text result via Discord** (default — no screenshot):
   ```
   send_message(message='<formatted text summary>', target='discord')
   ```

   除非使用者特別要求截圖，否則預設只傳文字結果。

## Important Notes

- **Always verify page URL after navigation.** The browser tool may land on a different tab (AssetSentry, Facebook, etc.) — check `browser_snapshot` title/URL immediately.
- **CDP for tab debugging:** If navigation lands on the wrong page, use `browser_cdp(method='Target.getTargets')` to inspect all open tabs.
- **`browser_console` requires robust selectors:** Never use `document.querySelector("main").innerText` (it returns null). Use `?.` optional chaining and fallback selectors.
- **預設不傳截圖**，只傳送文字結果摘要。使用者明確要求時才額外傳截圖。
- If the send button is disabled, the input might be empty. Try clicking elsewhere first.
- Gemini's response rendering can be delayed — poll with vision/snapshot until text appears.
- The page may show a "Temporary chat" banner near the top — this is normal, proceed regardless.

## When to Use

- User asks to ask Gemini a question
- User wants to interact with Google Gemini
- User wants to pose a question or get information from Gemini
- User asks to chat with or query Gemini

## When NOT to Use

- Use `web_search` for simple factual queries
- Use `google-workspace` skill for Gmail/Calendar/Docs tasks
- Use `browser` skill only if user needs general browser navigation tasks
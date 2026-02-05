---
name: gameplay-browser
description: >-
  Test game via browser with Chrome DevTools. Navigate UI, play through
  game flow, observe behavior and report issues.
---

# Browser Gameplay

Test the game through the browser UI using Chrome DevTools MCP tools.

> **Announce:** "I'm using gameplay-browser to test via UI."

## Chrome DevTools Tools

Use these MCP tools for browser testing:

| Tool | Purpose |
|------|---------|
| `chrome-devtools_navigate_page` | Go to URL |
| `chrome-devtools_take_snapshot` | Get page accessibility tree (find elements) |
| `chrome-devtools_take_screenshot` | Capture visual state |
| `chrome-devtools_click` | Click buttons/elements by ref |
| `chrome-devtools_fill` | Enter text in inputs |
| `chrome-devtools_select_option` | Select from dropdowns |
| `chrome-devtools_hover` | Hover over elements |
| `chrome-devtools_scroll` | Scroll page |
| `chrome-devtools_list_console_messages` | Check for errors |
| `chrome-devtools_list_network_requests` | Check API calls |

## Start Testing

```
1. Navigate to game:
   chrome-devtools_navigate_page(url: "http://localhost:5173")

2. Take snapshot to find elements:
   chrome-devtools_take_snapshot()
   
3. Look for element refs in snapshot output
```

## Game Flow

### 1. Start Game

```
1. Take snapshot to find description input
2. Fill description:
   chrome-devtools_fill(ref: "input_ref", value: "A famous tower in Paris")
3. Take snapshot to find Start button
4. Click Start:
   chrome-devtools_click(ref: "button_ref")
5. Wait for loading, take new snapshot
```

### 2. Answer Questions

```
1. Take snapshot - read current question from page
2. Find Yes/No/Not Sure buttons
3. Click answer:
   chrome-devtools_click(ref: "yes_button_ref")
4. Take new snapshot to see next state
```

### 3. Handle Guesses

When the game makes a guess:

```
1. Take snapshot - see guess displayed
2. Click "Yes" to confirm or "No" to deny
3. Take new snapshot to see result
```

### 4. Give Up

```
1. Find and click "Give Up" button
2. Take snapshot - find search input
3. Fill search:
   chrome-devtools_fill(ref: "search_ref", value: "Eiffel Tower")
4. Take snapshot - find result
5. Click on correct place to submit
```

## Finding Element Refs

After `chrome-devtools_take_snapshot()`, look for elements like:

```
- button "Start Game" [ref: 15]
- textbox "Enter description" [ref: 12]
- button "Yes" [ref: 23]
- button "No" [ref: 24]
```

Use the `ref` number in click/fill commands.

## Check for Errors

```
1. Console errors:
   chrome-devtools_list_console_messages()

2. Failed API calls:
   chrome-devtools_list_network_requests()
   Look for non-200 status codes
```

## Screenshot for Evidence

```
chrome-devtools_take_screenshot(filename: "game-state.png")
```

## Complete Game Example

```
1. chrome-devtools_navigate_page(url: "http://localhost:5173")
2. chrome-devtools_take_snapshot()  → find input ref
3. chrome-devtools_fill(ref: "X", value: "A castle in Poland")
4. chrome-devtools_take_snapshot()  → find Start button ref
5. chrome-devtools_click(ref: "Y")
6. chrome-devtools_take_snapshot()  → read question, find answer buttons
7. chrome-devtools_click(ref: "yes_ref")
8. chrome-devtools_take_snapshot()  → check next state
9. Repeat 7-8 until game ends
10. chrome-devtools_take_screenshot(filename: "result.png")
11. chrome-devtools_list_console_messages()  → check for errors
```

## Common Issues

**Page not loading**
- Dev server not running
- Try: `bun run dev` in project root first

**Elements not found in snapshot**
- Page still loading - wait and take new snapshot
- Element may be hidden/conditional

**Click not working**
- Element may be disabled or loading
- Take snapshot to verify element state

**Place search returns "No places found"**
- Use partial name: "Angkor" instead of "Angkor Wat"
- Search is case-insensitive but needs substring match
- Try shorter, more general terms

**Pressing Enter/Return**
- Use `chrome-devtools_press_key(key: "Enter")` or `NumpadEnter`
- NOT "Return" (invalid key name)

**Element ref expired**
- DOM changed between snapshot and click
- Take fresh snapshot and use new ref numbers

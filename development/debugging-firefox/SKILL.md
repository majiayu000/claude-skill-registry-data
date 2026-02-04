---
name: debugging-firefox
description: Use when user wants to debug web pages, inspect network requests, monitor console logs, or interact with web applications using Firefox DevTools
---

# Debugging with Firefox DevTools

Debug web applications using Firefox DevTools MCP tools. Use this skill for web debugging, network inspection, console monitoring, and page interaction.

## Core Workflows

### 1. Network Debugging
**When to use**: Investigate failed requests, slow loading, API issues, or CORS problems.

**Pattern**:
```
1. list_network_requests - Get overview (use filters: sinceMs, urlContains, status)
2. get_network_request - Deep dive on specific request using ID
3. Look for: status codes, timing, headers, response data
```

**Key filters**:
- `sinceMs`: Recent requests only (e.g., 5000 for last 5 seconds)
- `urlContains`: Filter by URL substring
- `status`, `statusMin`, `statusMax`: Filter by HTTP status
- `method`: GET, POST, etc.
- `isXHR`: true for fetch/XHR requests only

**Example**:
```
list_network_requests(sinceMs=10000, status=404, limit=20)
get_network_request(id="47-abc123...")
```

### 2. Console Monitoring
**When to use**: Debug JavaScript errors, warnings, or logs.

**Pattern**:
```
1. clear_console_messages - Clear old messages (optional but recommended)
2. Trigger the behavior (navigate, click, etc.)
3. list_console_messages - Check for errors/warnings
```

**Key filters**:
- `level`: debug, info, warn, error
- `sinceMs`: Recent messages only
- `textContains`: Filter by content
- `source`: console-api, javascript, network

**Example**:
```
clear_console_messages()
# ... trigger behavior ...
list_console_messages(level="error", sinceMs=5000)
```

### 3. Page Inspection & Interaction
**When to use**: Understand page structure or interact with elements.

**Critical rule**: ALWAYS take a fresh snapshot after navigation. UIDs become stale.

**Pattern**:
```
1. take_snapshot - Get page structure with UIDs
2. Use UIDs for interaction:
   - click_by_uid
   - fill_by_uid
   - hover_by_uid
   - screenshot_by_uid
3. After navigation/DOM changes - take_snapshot again!
```

**Snapshot parameters**:
- `maxLines`: Control output size (default 100)
- `includeText`: Show element text (default true)
- `includeAttributes`: Detailed ARIA/attributes (default false)
- `maxDepth`: Tree depth limit

**Example**:
```
take_snapshot(maxLines=50)
click_by_uid("2_10")
take_snapshot()  # Fresh snapshot after click!
```

### 4. Tab Management
**When to use**: Test multiple pages or compare behavior.

**Pattern**:
```
1. list_pages - See all open tabs
2. select_page(pageIdx=1) - Switch tabs by index
3. new_page(url="...") - Open new tab
4. close_page(pageIdx=2) - Close tab
```

**Example**:
```
list_pages()
new_page("https://example.com")
select_page(pageIdx=1)
```

## Common Debugging Scenarios

### Scenario: "Page loads but API call fails"
1. `list_network_requests(isXHR=true, statusMin=400)` - Find failed API calls
2. `get_network_request(id="...")` - Check request/response details
3. Look for: wrong URL, CORS headers, 401/403 auth issues

### Scenario: "Button click doesn't work"
1. `take_snapshot()` - Get page structure
2. `click_by_uid("...")` - Click the button
3. `list_console_messages(level="error")` - Check for JS errors
4. `list_network_requests(sinceMs=2000)` - Check for triggered requests

### Scenario: "Form submission issues"
1. `take_snapshot()` - Get form structure
2. `fill_form_by_uid(elements=[{uid: "...", value: "..."}])` - Fill multiple fields
3. `click_by_uid("submit_button_uid")` - Submit
4. `list_console_messages()` + `list_network_requests(method="POST")` - Debug

### Scenario: "Performance investigation"
1. `clear_console_messages()` + clear before measurement
2. Navigate or trigger action
3. `list_network_requests(sortBy="duration", limit=20)` - Find slow requests
4. `get_network_request(id="...")` - Check timing details

## Best Practices

1. **Clear before measuring**: Use `clear_console_messages()` before testing to focus on new messages

2. **Use filters aggressively**: Don't list all requests - filter by time, status, or URL

3. **Always snapshot after navigation**: UIDs become stale after DOM changes

4. **Start broad, then narrow**:
   - First: `list_network_requests()` overview
   - Then: `get_network_request(id)` for details

5. **Check both console and network**: Errors can appear in either place

6. **Use screenshots sparingly**: Snapshots are more useful for structure and interaction

7. **Leverage sinceMs**: Focus on recent activity (e.g., `sinceMs=5000` for last 5 seconds)

## Additional Resources

- **Complete Tool Reference**: @tools-reference.md
- **Practical Examples**: @examples.md - Real-world debugging scenarios
- **Troubleshooting Guide**: @troubleshooting.md - Common issues and solutions

## Tips & Tricks

- **Stale UID error?** → Take a fresh snapshot
- **Too much network noise?** → Use `sinceMs` or `urlContains` filters
- **Need to test dialogs?** → Use `accept_dialog()` or `dismiss_dialog()`
- **Need specific viewport?** → Use `set_viewport_size(width, height)`
- **Multiple pages open?** → Use `list_pages()` and `select_page()`
- **Console shows [Object object]?** → Use `JSON.stringify()` when logging objects (see @troubleshooting.md)

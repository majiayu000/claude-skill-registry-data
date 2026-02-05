---
name: web-load2
description: Loads and extracts all content from web URLs. Use when the user asks to fetch, load, or retrieve content from a website or URL.
allowed-tools:
  - WebFetch
  - Read
  - Write
  - Bash
---

# Web Content Loader

This skill helps you load and extract all content from web URLs efficiently.

## Instructions

When loading content from a URL:

1. **Use WebFetch** to fetch the content from the provided URL
   - The URL must be fully-formed and valid
   - Provide a clear prompt describing what information to extract
   - HTTP URLs will be automatically upgraded to HTTPS

2. **Extract all content** by using an appropriate prompt like:
   - "Extract all text content from this page"
   - "Get the complete page content including all sections"
   - "Retrieve all information from this webpage"

3. **Handle redirects** properly:
   - If WebFetch returns a redirect message, make a new request with the redirect URL

4. **Save content if requested**:
   - If the user wants to save the content, use the Write tool to save to a file
   - Suggest appropriate filenames based on the URL or content

## Examples

**Basic URL fetch:**
```
User: Load content from https://example.com
Action: Use WebFetch with prompt "Extract all text content from this page"
```

**Fetch and save:**
```
User: Load https://docs.example.com/guide and save it
Action: 
1. Use WebFetch to get content
2. Use Write to save to a markdown file
```

**Multiple URLs:**
```
User: Load content from these URLs: url1, url2, url3
Action: Use WebFetch for each URL in parallel when possible
```

## Best Practices

- Always validate that URLs are well-formed before fetching
- Use descriptive prompts when calling WebFetch to get complete content
- For large amounts of content, consider saving to files
- Process multiple URLs in parallel when they're independent

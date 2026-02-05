---
name: detect_non_localizable
description: Determine if a string value should be translated or left as-is. Use when filtering localization keys, validating translation files, or building translation task lists.
---

# Detect Non-Localizable Strings

Analyze a string value to determine if it should be translated or left unchanged.

## Input

- **value**: The string to check

## Output

Return a boolean:
- **true**: String should NOT be translated (non-localizable)
- **false**: String should be translated (localizable)

When returning `true`, log which pattern matched.

## Detection Patterns

Check patterns in this order. Return `true` (non-localizable) if any pattern matches:

### 1. Empty or Whitespace Only

```
Pattern: /^\s*$/
Examples: "", "   ", "\n\t"
```

### 2. Pure Numbers

```
Pattern: /^-?\d+([.,]\d+)?%?$/
Examples: "42", "3.14", "-100", "50%", "1,234"
```

### 3. Single Special Characters

```
Pattern: /^[^\w\s]$/ (single non-word, non-space character)
Examples: ":", "-", "•", "→", "|"
```

### 4. URLs

```
Pattern: /^(https?:\/\/|www\.)|(\.(com|org|net|io|dev|edu|gov|co|app)\b)/i
Examples:
  - "https://github.com/example"
  - "www.example.com"
  - "Visit example.com for more"
```

### 5. Email Addresses

```
Pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
Examples: "user@example.com", "support@company.org"
```

### 6. File Paths and Extensions

```
Pattern: /^[.\/\\]|[\/\\][\w.-]+[\/\\]|\.(?:json|xml|ts|js|html|css|scss|png|jpg|svg|pdf|md|txt|yaml|yml)$/i
Examples:
  - "/path/to/file"
  - "./relative/path"
  - "C:\Windows\path"
  - "config.json"
  - "image.png"
```

### 7. Version Numbers

```
Pattern: /^v?\d+\.\d+(\.\d+)?(-[\w.]+)?(\+[\w.]+)?$/i
Examples: "1.2.3", "v2.0", "1.0.0-beta", "2.1.0+build.123"
```

### 8. API Endpoints

```
Pattern: /^\/(?:api|v\d+|rest|graphql)\//i
Examples: "/api/users", "/v1/auth/login", "/rest/resources"
```

### 9. UUIDs

```
Pattern: /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
Examples: "550e8400-e29b-41d4-a716-446655440000"
```

### 10. Hash-like Strings

```
Pattern: /^[0-9a-f]{32,}$/i (32+ hex characters, like MD5/SHA hashes)
Examples: "d41d8cd98f00b204e9800998ecf8427e"
```

### 11. Configuration Keys (SCREAMING_SNAKE_CASE)

```
Pattern: /^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$/
Examples: "API_KEY", "MAX_RETRY_COUNT", "DATABASE_URL"
Note: Must have at least one underscore to distinguish from acronyms
```

### 12. Template Variables Only

```
Pattern: /^\{\{[\w.]+\}\}$/
Examples: "{{common.name}}", "{{user.email}}"
Note: Only if the ENTIRE value is a template variable
```

### 13. Icon Identifiers

```
Pattern: /^(material-symbols|fa|mdi|icon)[-:][\w-]+$/i
Examples: "material-symbols:security", "fa-regular fa-user", "mdi-account"
```

### 14. CSS/Style Values

```
Pattern: /^(#[0-9a-f]{3,8}|rgba?\(|hsla?\(|\d+px|\d+em|\d+rem|\d+%)$/i
Examples: "#fff", "#ff5500", "rgba(0,0,0,0.5)", "16px", "1.5em"
```

## Patterns That Are Localizable (return false)

These should always be translated even if they might look technical:

- Strings containing readable words mixed with numbers: "Step 1", "Version 2 Released"
- Strings with template variables embedded in text: "Hello {{name}}"
- Acronyms without underscores: "API", "URL", "HTTP" (might be used in sentences)
- Short codes that could be labels: "OK", "N/A"

## Implementation Notes

1. **Be conservative**: When in doubt, return `false` (localizable). It's better to have a translator skip an obvious non-translatable than to miss a string that needs translation.

2. **Order matters**: Check patterns from most specific to least specific to avoid false positives.

3. **Logging**: When returning `true`, output which pattern matched:
   ```
   Non-localizable: "https://example.com" (matched: URL pattern)
   ```

4. **Edge cases**:
   - Mixed content like "Visit https://example.com" should be `false` (localizable) because the surrounding text needs translation
   - Interpolated strings like "{{count}} items" should be `false` (localizable)

## Example Usage

```
Input: "https://github.com/ericfitz/tmi"
Output: true (matched: URL pattern)

Input: "Delete"
Output: false (localizable text)

Input: "{{common.name}}"
Output: true (matched: template variable only)

Input: "Hello {{name}}, welcome!"
Output: false (localizable - contains translatable text)

Input: "API_ENDPOINT_URL"
Output: true (matched: configuration key)

Input: "1.2.3"
Output: true (matched: version number)

Input: "Step 1"
Output: false (localizable - contains readable text)
```

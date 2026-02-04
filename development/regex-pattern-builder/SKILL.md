---
name: regex-pattern-builder
description: Builds and explains regex patterns from natural language, tests patterns, and provides examples. Use when user asks to "create regex", "regex pattern", "match pattern", "validate email/phone", or "regex help".
allowed-tools: [Read, Write]
---

# Regex Pattern Builder

Creates regex patterns from natural language descriptions, explains existing patterns, and helps test and debug regex.

## When to Use

- "Create a regex to match emails"
- "Regex pattern for phone numbers"
- "How do I match URLs"
- "Explain this regex"
- "Test my regex pattern"
- "Validate password regex"

## Instructions

### 1. Understand the Requirement

Ask clarifying questions if needed:
- What format are you trying to match?
- Should it be strict or permissive?
- What language/flavor (JavaScript, Python, etc.)?
- Full match or contains?
- Case sensitive?

### 2. Build Pattern from Description

## Common Patterns

**Email validation:**
```javascript
// Simple (permissive)
/^[^\s@]+@[^\s@]+\.[^\s@]+$/

// More strict (RFC 5322 simplified)
/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

// Explanation:
// ^              - Start of string
// [a-zA-Z0-9._%+-]+ - Username: letters, numbers, dots, etc.
// @              - Literal @ symbol
// [a-zA-Z0-9.-]+ - Domain name
// \.             - Literal dot
// [a-zA-Z]{2,}   - TLD (2+ letters)
// $              - End of string
```

**Phone numbers:**
```javascript
// US phone (flexible)
/^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$/

// Matches:
// 123-456-7890
// (123) 456-7890
// 123.456.7890
// 1234567890

// International (E.164)
/^\+?[1-9]\d{1,14}$/

// Explanation:
// ^\+?           - Optional + at start
// [1-9]          - First digit 1-9
// \d{1,14}       - 1-14 more digits
// $              - End of string
```

**URLs:**
```javascript
// Simple URL
/^https?:\/\/[\w\-._~:/?#[\]@!$&'()*+,;=]+$/

// With capture groups
/^(https?):\/\/([\w.-]+)(:\d+)?(\/[\w\-._~:/?#[\]@!$&'()*+,;=]*)?$/

// Groups:
// $1 - protocol (http/https)
// $2 - domain
// $3 - port (optional)
// $4 - path (optional)
```

**Passwords:**
```javascript
// At least 8 chars, 1 uppercase, 1 lowercase, 1 number
/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/

// At least 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special
/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/

// Explanation:
// (?=.*[a-z])    - Lookahead: contains lowercase
// (?=.*[A-Z])    - Lookahead: contains uppercase
// (?=.*\d)       - Lookahead: contains digit
// (?=.*[@$!%*?&])- Lookahead: contains special char
// [A-Za-z\d@$!%*?&]{8,} - 8+ valid characters
```

**Dates:**
```javascript
// YYYY-MM-DD
/^\d{4}-\d{2}-\d{2}$/

// MM/DD/YYYY or M/D/YYYY
/^(0?[1-9]|1[0-2])\/(0?[1-9]|[12]\d|3[01])\/\d{4}$/

// ISO 8601 (with time)
/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z?$/
```

**Credit card:**
```javascript
// Any 13-19 digits with optional spaces/dashes
/^[\d\s-]{13,19}$/

// Specific cards:
// Visa: /^4\d{12}(?:\d{3})?$/
// Mastercard: /^5[1-5]\d{14}$/
// Amex: /^3[47]\d{13}$/
```

**IP addresses:**
```javascript
// IPv4
/^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$/

// IPv4 (simple)
/^(\d{1,3}\.){3}\d{1,3}$/

// IPv6 (simplified)
/^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/
```

**Usernames:**
```javascript
// 3-16 chars, alphanumeric + underscore/hyphen
/^[a-zA-Z0-9_-]{3,16}$/

// Must start with letter, 3-16 chars
/^[a-zA-Z][a-zA-Z0-9_-]{2,15}$/
```

**Hex colors:**
```javascript
// #RGB or #RRGGBB
/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/

// With optional alpha (#RRGGBBAA)
/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{8}|[A-Fa-f0-9]{3}|[A-Fa-f0-9]{4})$/
```

**HTML tags:**
```javascript
// Match opening tags
/<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)/

// Strip all HTML tags
/<[^>]*>/g

// Match specific tag
/<div\b[^>]*>(.*?)<\/div>/gs
```

**File paths:**
```javascript
// Windows path
/^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$/

// Unix path
/^\/(?:[^\/\0]+\/)*[^\/\0]*$/

// File extension
/\.([a-zA-Z0-9]+)$/
```

### 3. Provide Test Cases

For each pattern, show examples:

```javascript
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

// Valid emails
console.log(emailRegex.test('user@example.com'))        // true
console.log(emailRegex.test('first.last@company.co.uk')) // true
console.log(emailRegex.test('user+tag@domain.org'))     // true

// Invalid emails
console.log(emailRegex.test('@example.com'))            // false
console.log(emailRegex.test('user@'))                   // false
console.log(emailRegex.test('user example.com'))        // false
console.log(emailRegex.test('user@domain'))             // false
```

### 4. Explain Pattern Components

**Basic syntax:**
```
.       - Any character except newline
\d      - Digit [0-9]
\D      - Not digit
\w      - Word character [a-zA-Z0-9_]
\W      - Not word character
\s      - Whitespace [\t\n\r ]
\S      - Not whitespace

^       - Start of string/line
$       - End of string/line
\b      - Word boundary
\B      - Not word boundary

*       - 0 or more (greedy)
+       - 1 or more (greedy)
?       - 0 or 1 (greedy)
{n}     - Exactly n times
{n,}    - n or more times
{n,m}   - Between n and m times

*?      - 0 or more (lazy)
+?      - 1 or more (lazy)
??      - 0 or 1 (lazy)

[abc]   - Any of a, b, or c
[^abc]  - Not a, b, or c
[a-z]   - Any lowercase letter
[0-9]   - Any digit

(...)   - Capture group
(?:...) - Non-capturing group
(?=...) - Positive lookahead
(?!...) - Negative lookahead
(?<=...)- Positive lookbehind
(?<!...)- Negative lookbehind

|       - OR
\       - Escape special character
```

### 5. Language-Specific Variations

**JavaScript:**
```javascript
// Flags
const regex = /pattern/gi
// g - global (find all matches)
// i - case insensitive
// m - multiline (^ and $ match line breaks)
// s - dotall (. matches newlines)
// u - unicode
// y - sticky

// Methods
'text'.match(/pattern/g)           // Array of matches
'text'.matchAll(/pattern/g)        // Iterator of matches
'text'.search(/pattern/)           // Index of first match
'text'.replace(/pattern/g, 'new')  // Replace matches
/pattern/.test('text')             // Boolean
/pattern/.exec('text')             // Match details
```

**Python:**
```python
import re

# Flags
re.IGNORECASE  # Case insensitive
re.MULTILINE   # ^ and $ match line breaks
re.DOTALL      # . matches newlines
re.VERBOSE     # Allow comments in regex

# Methods
re.match(pattern, string)      # Match at start
re.search(pattern, string)     # Find anywhere
re.findall(pattern, string)    # All matches
re.finditer(pattern, string)   # Iterator
re.sub(pattern, repl, string)  # Replace
re.split(pattern, string)      # Split
```

**PHP:**
```php
// Functions
preg_match($pattern, $subject)         // Single match
preg_match_all($pattern, $subject)     // All matches
preg_replace($pattern, $replace, $subject)  // Replace
preg_split($pattern, $subject)         // Split

// Pattern modifiers
/pattern/i  // Case insensitive
/pattern/m  // Multiline
/pattern/s  // Dotall
/pattern/x  // Ignore whitespace
```

### 6. Common Use Cases

**Extract data:**
```javascript
const text = "Contact: john@example.com or jane@company.org"
const emails = text.match(/[^\s@]+@[^\s@]+\.[^\s@]+/g)
console.log(emails)  // ['john@example.com', 'jane@company.org']
```

**Validate input:**
```javascript
function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}
```

**Replace content:**
```javascript
const text = "Call us at 555-1234 or 555-5678"
const censored = text.replace(/\d{3}-\d{4}/g, 'XXX-XXXX')
console.log(censored)  // "Call us at XXX-XXXX or XXX-XXXX"
```

**Parse structured data:**
```javascript
const log = "2024-01-15 ERROR: Failed to connect"
const match = log.match(/^(\d{4}-\d{2}-\d{2}) (\w+): (.+)$/)

if (match) {
  const [, date, level, message] = match
  console.log({ date, level, message })
}
```

### 7. Advanced Patterns

**Lookaheads and lookbehinds:**
```javascript
// Password: 8+ chars, must include uppercase, lowercase, number
/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/

// Match word not followed by another word
/\b\w+\b(?!\s+\w+)/

// Match number preceded by $
/(?<=\$)\d+(\.\d{2})?/
```

**Capture groups:**
```javascript
const text = "John Doe (john@example.com)"
const regex = /(\w+)\s+(\w+)\s+\(([^)]+)\)/
const [, firstName, lastName, email] = text.match(regex)

console.log({ firstName, lastName, email })
// { firstName: 'John', lastName: 'Doe', email: 'john@example.com' }
```

**Named groups (modern):**
```javascript
const regex = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/
const match = '2024-01-15'.match(regex)

console.log(match.groups)
// { year: '2024', month: '01', day: '15' }
```

### 8. Performance Tips

**Avoid catastrophic backtracking:**
```javascript
// ❌ BAD: Catastrophic backtracking
/(a+)+b/

// ✅ GOOD: Atomic grouping or possessive quantifiers
/a+b/
```

**Be specific:**
```javascript
// ❌ BAD: Too greedy
/<.*>/

// ✅ GOOD: Lazy quantifier
/<.*?>/

// ✅ BETTER: Specific negation
/<[^>]*>/
```

**Anchor patterns:**
```javascript
// ❌ BAD: Scans entire string
/\d{3}-\d{4}/

// ✅ GOOD: Anchored
/^\d{3}-\d{4}$/
```

### 9. Testing Tools

Provide testing code:

```javascript
function testRegex(pattern, testCases) {
  console.log(`Testing: ${pattern}\n`)

  testCases.forEach(({ input, expected }) => {
    const result = pattern.test(input)
    const status = result === expected ? '✓' : '✗'

    console.log(`${status} "${input}" -> ${result} (expected ${expected})`)
  })
}

// Usage
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

testRegex(emailRegex, [
  { input: 'user@example.com', expected: true },
  { input: 'invalid@', expected: false },
  { input: '@example.com', expected: false },
  { input: 'user example.com', expected: false }
])
```

### 10. Common Mistakes

**Forgetting to escape:**
```javascript
// ❌ BAD: . matches any character
/user.example.com/

// ✅ GOOD: Escaped dot
/user\.example\.com/
```

**Not anchoring:**
```javascript
// ❌ BAD: Matches anywhere in string
/\d{3}-\d{4}/  // "xxx-555-1234-yyy" passes

// ✅ GOOD: Anchored to start and end
/^\d{3}-\d{4}$/  // Only "555-1234" passes
```

**Greedy vs lazy:**
```javascript
const html = '<div>content</div><span>more</span>'

// ❌ BAD: Greedy, matches too much
html.match(/<.*>/)  // '<div>content</div><span>more</span>'

// ✅ GOOD: Lazy, matches minimally
html.match(/<.*?>/)  // '<div>'
```

**Case sensitivity:**
```javascript
// ❌ BAD: Case sensitive
/^[a-z]+$/  // Only lowercase

// ✅ GOOD: Case insensitive
/^[a-z]+$/i  // Any case
```

### Regex Cheat Sheet

**Character classes:**
- `\d` = `[0-9]`
- `\D` = `[^0-9]`
- `\w` = `[a-zA-Z0-9_]`
- `\W` = `[^a-zA-Z0-9_]`
- `\s` = `[ \t\n\r\f\v]`
- `\S` = `[^ \t\n\r\f\v]`

**Quantifiers:**
- `*` = {0,∞}
- `+` = {1,∞}
- `?` = {0,1}
- `{n}` = exactly n
- `{n,}` = n or more
- `{n,m}` = between n and m

**Anchors:**
- `^` = start of string/line
- `$` = end of string/line
- `\b` = word boundary
- `\A` = start of string (Python)
- `\Z` = end of string (Python)

**Groups:**
- `(...)` = capture
- `(?:...)` = non-capture
- `(?<name>...)` = named capture
- `(?=...)` = lookahead
- `(?!...)` = negative lookahead
- `(?<=...)` = lookbehind
- `(?<!...)` = negative lookbehind

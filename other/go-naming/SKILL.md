---
name: go-naming
description: "Go (Golang) naming conventions for packages, types, variables, and errors. Follows the principle: 'Clear is better than clever'."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 04:40:00 GMT
---

## Quick Reference Table

| Element | Convention | Example |
| --- | --- | --- |
| Package | lowercase, singular, single word | `json`, `http`, `user` |
| File | lowercase, underscores allowed | `user_handler.go` |
| Exported name | `UpperCamelCase` | `ReadAll`, `HTTPClient` |
| Unexported | `lowerCamelCase` | `parseToken`, `userCount` |
| Interface | method name + `-er` suffix | `Reader`, `Writer`, `Stringer` |
| Receiver | 1-2 letter abbreviation | `func (s *Server)`, `func (b *Buffer)` |
| Error variable | `Err` prefix | `ErrNotFound`, `ErrTimeout` |
| Error type | `Error` suffix | `PathError`, `SyntaxError` |
| Constructor | `New` (primary) or `NewTypeName` | `user.New()`, `http.NewRequest()` |
| Boolean | `is`, `has`, `can` prefix | `isReady`, `IsConnected()` |
| Acronym | All caps or all lower | `URL`, `HTTP`, `xmlParser` |

## Core Principles

### 1. MixedCaps (No Underscores)
Always use `MixedCaps` or `lowerCamelCase`. Never use underscores in identifiers (except in tests or generated code).
- ✅ `maxPacketSize`
- ❌ `max_packet_size`

### 2. Avoid Stuttering
Call sites include the package name, so don't repeat it in the type or function name.
- ✅ `http.Client`
- ❌ `http.HTTPClient`
- ✅ `user.New()`
- ❌ `user.NewUser()`

### 3. Receiver Names
Use 1-2 letter abbreviations of the type name. Never use `this` or `self`.
- ✅ `func (r *Reader) Read(...)`
- ❌ `func (this *Reader) Read(...)`

### 4. Acronyms
Acronyms should be consistently capitalized.
- ✅ `userID`, `APIClient`, `parseXML`
- ❌ `userId`, `ApiClient`, `parseXml`

### 5. Error Strings
Error strings returned by `errors.New` or `fmt.Errorf` should be **lowercase** and have **no trailing punctuation**.
- ✅ `errors.New("user not found")`
- ❌ `errors.New("User Not Found!")`

## Anti-patterns

- ❌ **`ALL_CAPS` constants**: Go uses casing for visibility, not to denote constants. Use `MixedCaps`.
- ❌ **`Get` prefix on getters**: `user.Name()` is preferred over `user.GetName()`.
- ❌ **Generic package names**: `util`, `common`, `helper` are anti-patterns. Use descriptive names like `netutil`, `jsonutil`.
- ❌ **Package names with underscores**: Import paths should be clean and easy to type.
- ❌ **Plural package names**: Use `model`, not `models`; `user`, not `users`.

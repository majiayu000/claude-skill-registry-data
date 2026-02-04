---
name: go-doc
description: This skill should be used when drafting or reviewing Go doc comments so they align with the official Go documentation style and pkgsite rendering rules.
---

# Go Doc Comments

## Overview
Produce doc comments that render cleanly in `go doc`, pkgsite, and IDEs by following the Go project's official guidance. Apply this skill whenever documenting exported Go identifiers or packages.

## When to Use
- Document exported Go packages, commands, types, funcs, consts, or vars.
- Review existing comments for compliance during code review or refactors.
- Convert informal inline comments into doc comments intended for pkgsite.

Avoid invoking this skill for unexported identifiers unless the repository mandates internal documentation parity.

## Workflow
1. **Locate the target declaration**  
   Place the comment immediately above the top-level declaration with no blank lines between the comment and the declaration.

2. **Draft the lead sentence**  
   - Start package comments with `Package <name> ...` in complete sentences.  
   - Start command package comments with the capitalized program name, e.g., `Gofmt formats Go programs.`  
   - Start other doc comments with the identifier name followed by a verb phrase that explains what it does (e.g., `Serve starts an HTTP server.`).

3. **Expand the description**  
   - Describe behavior, usage, and key arguments succinctly.  
   - Link to related APIs using square brackets (`[net/http]`) so pkgsite creates hyperlinks.  
   - Use semantic linefeeds (one sentence per line) when it improves diffs; pkgsite rewraps automatically.

4. **Format structured content**  
   - Indent lists and code blocks with either a tab or two spaces so they render correctly.  
   - Create numbered or bulleted lists with a leading tab/space and a marker (`-` or digits).  
   - Avoid nested lists; rewrite as multiple paragraphs or mixed markers if hierarchy is essential.  
   - Indent multi-line shell commands or code samples consistently, and add blank lines before and after blocks.

5. **Preserve tone and accuracy**  
   - Use present tense and active voice.  
   - Keep comments factual; avoid marketing language.  
   - Mention exported error conditions, side effects, and concurrency guarantees as needed.

6. **Validate rendering**  
   - Run `go doc <pkg>.<Symbol>` or view via pkgsite to confirm wrapping, lists, and links render as expected.  
   - Run `gofmt` (Go 1.19+) to ensure indentation aligns with the doc-comment heuristics.  
   - Adjust spacing if gofmt highlights ambiguous paragraphs (add or remove blank lines).

## Quick Checklist
- Begin with the correct identifier prefix (`Package`, symbol name, or command).  
- Keep sentences complete and punctuated.  
- Use links `[package]` or `[Type.Method]` for cross references.  
- Indent lists, code blocks, and shell snippets.  
- Avoid nested lists; restructure instead.  
- Verify formatting with `go doc` and `gofmt`.

## Good and Bad Examples

**Good – Package comment introducing scope and linking APIs**
```go
// Package cache provides in-memory caches with automatic eviction policies.
//
// The package exposes [LRU] and [TTL] caches that guard concurrent access with
// sync.RWMutex. Use [NewLRU] for bounded caches and [NewTTL] when entries expire
// after a fixed duration.
package cache
```
Why it works:
- Opens with `Package cache`.
- Summarises primary types and cross-links constructors.
- Uses short sentences and a blank line for readability.

**Bad – Missing identifier prefix and malformed list**
```go
// Provides caches that can evict entries.
// - LRU policy
// - TTL policy
package cache
```
Issues:
- First sentence omits the `Package` prefix, so the synopsis becomes unclear.
- List items are unindented, so pkgsite renders them as plain text.
- Does not explain when to choose each policy.

**Good – Function comment covering behavior and errors**
```go
// Fetch retrieves the value for key from the remote store.
//
// Fetch retries transient failures using exponential backoff and returns an
// error that implements [net.Error] when the deadline expires.
func Fetch(ctx context.Context, key string) ([]byte, error) {
```
Highlights:
- Begins with the function name.
- Documents retry policy and exported error semantics.
- Uses semantic linefeeds to keep diffs focused on changed sentences.

**Bad – Narrative tone and misleading code block**
```go
// This function is going to try to get your data, but it might fail!!
// If it fails we waited too long and the store is DEAD.
//    retryCount++
func Fetch(ctx context.Context, key string) ([]byte, error) {
```
Problems:
- Uses second-person narrative and emotional language.
- Fails to mention the function name or concrete behavior.
- Indented `retryCount++` is treated as a code block even though it provides
  no context.

## Validation Tools
- `go doc <package>` or `go doc <package>.<Symbol>` – preview rendered documentation.  
- `pkgsite` (local or hosted) – inspect pkgsite rendering.  
- `gofmt` – verify indentation heuristics for doc comments.

## Quick Checklist
- [ ] Comment sits immediately above the exported declaration with no blank line.
- [ ] Lead sentence starts with `Package`, the program name, or the symbol name.
- [ ] Sentences are complete, factual, and written in present tense.
- [ ] Links use square brackets (`[pkg.Symbol]`) to enable pkgsite cross references.
- [ ] Lists and code snippets are indented; nested lists are avoided.
- [ ] Error contracts, side effects, and concurrency guarantees are documented.
- [ ] `go doc` preview looks correct and `gofmt` leaves formatting untouched.

---
name: convert-code
description: "Converts code between programming languages while preserving logic, error handling, and idiomatic patterns. Use when migrating modules between languages or frameworks."
argument-hint: "[source file] to [target language]"
allowed-tools: Read, Bash, Write, Grep
---

# Code Conversion

## Instructions

### Step 1: Analyze Source Code
1. Read the source file completely
2. Identify:
   - All functions, classes, and types
   - External dependencies and their equivalents in the target language
   - Error handling patterns
   - Async/concurrent patterns
   - Data structures and their representations
   - Tests (if present)

### Step 2: Map Language Idioms

Don't transliterate — convert to idiomatic target code:

| Source Pattern | Target Equivalent |
|---------------|-------------------|
| Python list comprehension | Java streams / Go slices / Rust iterators |
| JS Promise.all | Python asyncio.gather / Go goroutines+WaitGroup / Rust tokio::join |
| Python dict | Go map / Rust HashMap / Java Map |
| JS destructuring | Go multiple returns / Python tuple unpacking |
| Python decorator | Java annotation / Go middleware / Rust macro |
| C# LINQ | Python generators / JS array methods / Rust iterators |
| Ruby blocks | Python context managers / Go defer / Rust closures |

### Step 3: Handle Dependencies
For each import/dependency in the source:
1. Find the equivalent package/library in the target ecosystem
2. If no direct equivalent exists, note it and implement the functionality
3. Map API calls to the target library's conventions

### Step 4: Convert Error Handling
Different languages handle errors differently:

| Language | Pattern |
|----------|---------|
| Python | try/except, raise |
| JavaScript/TypeScript | try/catch, throw, Promise rejection |
| Go | Multiple return values (value, error) |
| Rust | Result<T, E>, Option<T>, ? operator |
| Java/C# | try/catch, checked/unchecked exceptions |
| Ruby | begin/rescue/ensure |
| Elixir | {:ok, value} / {:error, reason} tuples |

Convert error handling to the idiomatic pattern of the target language.

### Step 5: Convert Types
Map type systems:
- Dynamic → Static: Infer and add explicit types
- Static → Dynamic: Simplify but add runtime checks where safety-critical
- Generics: Map to target language's generic system
- Null safety: Map Optional/Maybe/Option patterns appropriately

### Step 6: Generate Output
1. Write the converted file with proper formatting
2. Add a header comment noting the source and conversion
3. Include all necessary imports
4. Preserve comments (translate them to the target language's convention)
5. Generate a companion test file if tests existed in the source

### Step 7: Conversion Notes
Document:
- Patterns that couldn't be directly converted and the approach taken
- Dependencies that have no direct equivalent
- Behavioral differences to be aware of
- Performance characteristics that differ between implementations

---

## Rules
- **Idiomatic over literal** — code should look like it was written by a native developer
- **Preserve behavior** — the converted code must do the same thing
- **Preserve tests** — convert tests too, not just implementation
- **Flag risks** — note where behavior might differ (floating point, string encoding, concurrency)
- **Don't assume** — if unsure about a language feature, ask rather than guess

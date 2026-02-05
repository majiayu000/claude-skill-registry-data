---
name: serena-code-reading
description: Token-efficient code reading protocol using Serena's progressive disclosure pattern (90-95% token savings). Provides mandatory workflow, tool reference, and common patterns for symbol-level code navigation.
---

# Serena Code Reading Protocol

**Purpose:** Achieve 90-95% token savings by using Serena's progressive disclosure instead of reading entire files.

---

## Mandatory Pattern (93% Token Savings)

**ALWAYS use progressive disclosure instead of reading entire files:**

### 1. Overview First (~200 tokens)

```javascript
mcp__serena__get_symbols_overview({
  relative_path: "src/services/auth.service.ts",
});
```

**Returns:** File structure showing all top-level symbols (classes, functions, interfaces) with their signatures.

**Use when:** You need to understand what's in a file before diving into specific code.

---

### 2. Check Signatures (~50 tokens per symbol)

```javascript
mcp__serena__find_symbol({
  name_path_pattern: "AuthService/login",
  relative_path: "src/services/auth.service.ts",
  include_body: false, // Just the signature
  depth: 0,
});
```

**Returns:** Method/function signature without implementation details.

**Use when:** You need to understand the interface (parameters, return type) but not the implementation.

---

### 3. Read Bodies Selectively (~100 tokens per symbol)

```javascript
mcp__serena__find_symbol({
  name_path_pattern: "AuthService/login",
  relative_path: "src/services/auth.service.ts",
  include_body: true, // Full implementation
  depth: 0,
});
```

**Returns:** Complete symbol definition including implementation.

**Use when:** You actually need to read/edit the implementation.

---

## Token Impact Comparison

```
❌ Traditional Approach (Read entire file):
   Read file (2,000 lines) = ~5,000 tokens

✅ Serena Progressive Disclosure:
   get_symbols_overview     → ~200 tokens (file structure)
   find_symbol (no body)    → ~50 tokens (signature)
   find_symbol (with body)  → ~100 tokens (implementation)
   ─────────────────────────────────────────
   Total:                     ~350 tokens

   SAVINGS: 93% (4,650 tokens saved)
```

**Real-world impact:**

- Exploring 10 files: 50,000 tokens → 3,500 tokens (93% savings)
- Editing 5 symbols: 25,000 tokens → 500 tokens (98% savings)

---

## Core Tools Reference

### File Structure

- `get_symbols_overview` - Get file outline with all top-level symbols
- `list_dir` - List directory contents
- `find_file` - Find files by pattern

### Symbol Navigation

- `find_symbol` - Search for symbols by name path
- `find_referencing_symbols` - Find all references to a symbol
- `search_for_pattern` - Regex search across codebase

### Precise Editing

- `replace_symbol_body` - Replace symbol implementation without reading full file
- `insert_after_symbol` - Add content after symbol
- `insert_before_symbol` - Add content before symbol
- `rename_symbol` - Rename with cross-codebase updates

---

## Common Workflows

### Workflow 1: Understanding a New File

```javascript
// Step 1: Get overview
const overview = await mcp__serena__get_symbols_overview({
  relative_path: "src/services/payment.service.ts",
});

// Step 2: Check interesting symbol signatures
const processPaymentSignature = await mcp__serena__find_symbol({
  name_path_pattern: "PaymentService/processPayment",
  include_body: false, // Just signature
});

// Step 3: Read only what you need
const processPaymentBody = await mcp__serena__find_symbol({
  name_path_pattern: "PaymentService/processPayment",
  include_body: true, // Full implementation
});

// Result: ~350 tokens vs 5,000 tokens (93% savings)
```

---

### Workflow 2: Finding Where Something Is Used

```javascript
// Find all references to a function
const references = await mcp__serena__find_referencing_symbols({
  name_path: "validateToken",
  relative_path: "src/utils/auth.utils.ts",
});

// Returns: List of all places that call validateToken
// With code snippets showing context
// ~500 tokens vs 20,000 tokens (97.5% savings)
```

---

### Workflow 3: Editing a Specific Method

```javascript
// No need to read the entire file!
// Just replace the symbol body directly

await mcp__serena__replace_symbol_body({
  name_path: "AuthService/login",
  relative_path: "src/services/auth.service.ts",
  body: `async login(email: string, password: string): Promise<User> {
    // New implementation
    const user = await this.userRepository.findByEmail(email);
    if (!user) throw new UnauthorizedException();

    const isValid = await bcrypt.compare(password, user.passwordHash);
    if (!isValid) throw new UnauthorizedException();

    return user;
  }`,
});

// Result: ~100 tokens vs 5,000 tokens (98% savings)
```

---

### Workflow 4: Adding a New Method to a Class

```javascript
// Insert after existing method without reading full file
await mcp__serena__insert_after_symbol({
  name_path: "AuthService/login",
  relative_path: "src/services/auth.service.ts",
  body: `
  async logout(userId: string): Promise<void> {
    await this.sessionRepository.deleteByUserId(userId);
    this.logger.info('User logged out', { userId });
  }`,
});

// Result: ~100 tokens vs 5,000 tokens (98% savings)
```

---

## Name Path Syntax

Serena uses "name paths" to identify symbols (like file paths for code):

### Basic Patterns

```typescript
// Find any symbol with this name
"UserService"; // Matches: class UserService, interface UserService, etc.

// Find method inside class
"UserService/createUser"; // Matches: createUser method in UserService

// Find nested class
"AuthModule/AuthService"; // Matches: AuthService inside AuthModule

// Absolute path (exact match from file root)
"/UserService/createUser"; // Must be at file root level
```

### TypeScript/JavaScript Examples

```typescript
// File: auth.service.ts
export class AuthService {
  async login() { ... }      // Name path: "AuthService/login"
  async logout() { ... }     // Name path: "AuthService/logout"

  private validateToken() { ... }  // Name path: "AuthService/validateToken"
}

export function hashPassword() { ... }  // Name path: "hashPassword"
```

### Advanced Patterns

```typescript
// Substring matching (find all methods starting with "get")
find_symbol({
  name_path_pattern: "UserService/get",
  substring_matching: true,
});
// Matches: getUserById, getUserByEmail, getUserProfile

// Search by symbol kind (only classes)
find_symbol({
  name_path_pattern: "Service",
  include_kinds: [5], // 5 = Class
});

// Exclude certain kinds
find_symbol({
  name_path_pattern: "User",
  exclude_kinds: [13], // 13 = Variable
});
```

---

## Symbol Kinds Reference

```typescript
// Common LSP symbol kinds:
1 = File;
2 = Module;
3 = Namespace;
4 = Package;
5 = Class;
6 = Method;
7 = Property;
8 = Field;
9 = Constructor;
10 = Enum;
11 = Interface;
12 = Function;
13 = Variable;
14 = Constant;
```

---

## Best Practices

### ✅ DO

1. **Always start with overview**

   ```javascript
   get_symbols_overview(file); // See what's there first
   ```

2. **Check signatures before reading bodies**

   ```javascript
   find_symbol(name, (include_body = false)); // Interface only
   ```

3. **Read only what you need**

   ```javascript
   find_symbol(specific_symbol, (include_body = true)); // One symbol at a time
   ```

4. **Use find_referencing_symbols for impact analysis**

   ```javascript
   find_referencing_symbols(symbol); // Before refactoring
   ```

5. **Edit at symbol level when possible**
   ```javascript
   replace_symbol_body(); // Precise changes
   ```

### ✅ DO INSTEAD

1. **Use Serena tools for all code exploration**

   ```javascript
   ✅ get_symbols_overview("src/services/huge-file.ts") // ~200 tokens
   ❌ Read("src/services/huge-file.ts") // 5,000 tokens wasted
   ```

2. **Use include_body=false for exploration; true only for implementation**

   ```javascript
   ✅ get_symbols_overview() // Efficient overview
   ✅ find_symbol("*", include_body=false) // Signature only
   ❌ find_symbol("*", include_body=true) // Wasteful
   ```

3. **ALWAYS check overview first before guessing symbol names**
   ```javascript
   ✅ get_symbols_overview() → see actual names → find_symbol()
   ❌ find_symbol("createUser") // Might not exist
   ```

---

## When to Use Traditional Read Tool

**Rare cases where reading entire file is acceptable:**

1. **Very small files** (< 50 lines)
   - Config files: `.env.example`, `.nvmrc`
   - Simple utilities with 1-2 functions

2. **Non-code files**
   - Documentation: `README.md`, `CHANGELOG.md`
   - Data files: `package.json`, `tsconfig.json`

3. **When you need full context**
   - Understanding complex interdependencies within a single file
   - After using Serena tools and still need more context

**Rule of thumb:** If a file has symbols (classes, functions), use Serena. Otherwise, Read is fine.

---

## Troubleshooting

### Symbol Not Found

```javascript
// Error: Symbol "UserService/createUser" not found

// Solutions:
1. Check spelling: get_symbols_overview(file) to see actual names
2. Use substring matching: find_symbol("create", substring_matching=true)
3. Search pattern: search_for_pattern("createUser")
```

### Multiple Matches

```javascript
// Multiple symbols match "User"

// Solutions:
1. Use more specific path: "UserService/User" instead of "User"
2. Use absolute path: "/UserService/User"
3. Filter by kind: include_kinds=[5] for classes only
```

### Need to Find Symbol Location

```javascript
// Don't know which file has the symbol

// Solutions:
1. Omit relative_path: find_symbol("UserService") // Searches entire codebase
2. Restrict to directory: relative_path="src/services"
3. Use pattern search: search_for_pattern("class UserService")
```

---

## Integration with Other MCPs

### Serena + Context7 (Library Documentation)

```javascript
// 1. Get library docs
const docs = await mcp__Context7__get_library_docs({
  context7CompatibleLibraryID: "/prisma/prisma",
});

// 2. Find where it's used in your code
const prismaUsage = await mcp__serena__search_for_pattern({
  substring_pattern: "PrismaClient",
});

// 3. Understand implementation
const schema = await mcp__serena__get_symbols_overview({
  relative_path: "packages/database/schema.prisma",
});
```

### Serena + Memories (Pattern Storage)

```javascript
// 1. Check for prior patterns in Serena memories
const memories = await list_memories();
const authPatterns = memories.filter(
  (m) => m.includes("auth") || m.includes("pattern"),
);
for (const pattern of authPatterns) {
  const content = await read_memory({ memory_file_name: pattern });
}

// 2. Find existing auth code
const authService = await mcp__serena__find_symbol({
  name_path_pattern: "AuthService",
  include_body: true,
});

// 3. Store new pattern in memory
write_memory({
  memory_file_name: "pattern-jwt-auth.md",
  content: `# Pattern: JWT Auth with Refresh Tokens

## Implementation
- Access token: 15min TTL
- Refresh token: 7 days in httpOnly cookie
- Refresh rotation on each use

## Tags
auth, jwt, security`,
});
```

---

## Summary

**Remember: Progressive Disclosure**

1. Overview → See structure
2. Signatures → Understand interfaces
3. Bodies → Read only what's needed

**Token Savings: 90-95%**

- 10 files explored: 50,000 → 3,500 tokens
- 5 symbols edited: 25,000 → 500 tokens

**When in doubt:** Start with `get_symbols_overview` and work your way down to specific symbols.

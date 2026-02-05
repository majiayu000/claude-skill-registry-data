---
name: dry-check
description: Scans new/modified code against multi-mono shared libraries (@metasaver/core-utils, @metasaver/core-service-utils, @metasaver/core-components) to detect DRY violations. Use when auditing code for duplicate functions, types, or components that already exist in shared packages. Returns violation reports with suggested import replacements.
---

# DRY Check Skill

**Purpose:** Prevent code duplication by scanning new/modified code against multi-mono shared libraries.

**Use when:**

- Running Standards Audit phase
- Reviewing pull requests for DRY violations
- Checking if utility function already exists
- Validating components use @metasaver/core-components
- Ensuring services use @metasaver/core-service-utils

**Target libraries (packages/):**

- `@metasaver/core-utils` - String helpers (capitalize, toKebabCase, toCamelCase), color helpers, style helpers (cn)
- `@metasaver/core-service-utils` - Service factory, middleware, auth, health checks
- `@metasaver/core-database` - Database client utilities
- `@metasaver/core-agent-utils` - Agent factory patterns
- `@metasaver/core-mcp-utils` - MCP server utilities
- `@metasaver/core-workflow-utils` - Workflow with HITL

**Target components (components/):**

- `@metasaver/core-components` - Core UI: ZButton, ZCard, ZDataTable, ZErrorBoundary, ZLoading
- `@metasaver/core-layouts` - Layouts: ZAdminLayout, ZUserDropdown, useImpersonation

---

## What This Skill Catches

| Violation Type     | Library                       | Examples                                               |
| ------------------ | ----------------------------- | ------------------------------------------------------ |
| String utilities   | @metasaver/core-utils         | `capitalize()`, `toKebabCase()`, `toCamelCase()`       |
| Style utilities    | @metasaver/core-utils         | `cn()`, `getColorClasses()`                            |
| Service patterns   | @metasaver/core-service-utils | `createService()`, `authMiddleware()`, `healthCheck()` |
| Database clients   | @metasaver/core-database      | `createClient()`, database types                       |
| Core UI components | @metasaver/core-components    | `ZButton`, `ZCard`, `ZDataTable`, `ZErrorBoundary`     |
| Layout components  | @metasaver/core-layouts       | `ZAdminLayout`, `ZUserDropdown`, `useImpersonation`    |

---

## Workflow

### 1. Identify Modified Files

Get list of new/modified files from git:

```bash
# Staged files
git diff --cached --name-only --diff-filter=AM

# Uncommitted changes
git diff --name-only --diff-filter=AM

# Specific branch vs main
git diff main...HEAD --name-only --diff-filter=AM
```

Filter to code files only: `.ts`, `.tsx`, `.js`, `.jsx`

### 2. Extract Signatures

For each modified file, extract:

- **Function signatures**: `export function functionName()`, `export const functionName = ()`
- **Type definitions**: `export type TypeName`, `export interface InterfaceName`
- **Component definitions**: `export function ComponentName()`, `export const ComponentName: React.FC`
- **Zod schemas**: `export const schemaName = z.object()`

Use Grep tool with patterns from `templates/extraction-patterns.txt`

### 3. Scan Shared Libraries

For each extracted signature, check if similar exists in shared packages:

**Scan multi-mono packages/:**

```bash
# Search utils for function
grep -r "export.*functionName" packages/utils/src/

# Search service-utils for middleware/factory
grep -r "export.*functionName" packages/service-utils/src/

# Search database for client utilities
grep -r "export.*functionName" packages/database/src/
```

**Scan multi-mono components/:**

```bash
# Search core components
grep -r "export.*ZComponentName" components/core/src/

# Search layouts
grep -r "export.*ZLayoutName" components/layouts/src/
```

Use fuzzy matching for similar names (e.g., `capitalize` matches `toCapitalize`, `capitalizeFirst`)

### 4. Compare Implementations

If potential match found:

1. Read both implementations (new code vs library)
2. Compare function signatures and logic
3. Calculate similarity score (0-100%)
4. Flag if similarity > 70%

**Comparison heuristics:**

- Same parameter count and types = +30%
- Same return type = +20%
- Similar variable names = +20%
- Similar control flow = +30%

### 5. Generate Report

For each violation, output using format from `templates/violation-report.txt`:

```
❌ VIOLATION: [file]:[line] [signature]
   Duplicates: @metasaver/[package]/[module].[export]
   Similarity: [score]%
   FIX: import { [export] } from '@metasaver/[package]/[module]'

   [Brief comparison of implementations]
```

For clean scans:

```
✅ DRY CHECK PASSED
   Files scanned: [count]
   Signatures checked: [count]
   No duplications found
```

---

## Output Format

See `templates/violation-report.txt` for complete format specification.

**Console output example:**

```
🔍 DRY CHECK: Scanning 3 modified files...

❌ VIOLATION: src/utils/text.ts:5 capitalize()
   Duplicates: @metasaver/core-utils.capitalize()
   Similarity: 95%
   FIX: import { capitalize } from '@metasaver/core-utils'

   Both implementations capitalize first letter using same algorithm.

❌ VIOLATION: src/components/Button.tsx:10 Button
   Duplicates: @metasaver/core-components.ZButton
   Similarity: 85%
   FIX: import { ZButton } from '@metasaver/core-components'

   Local Button component has same props and styling as ZButton.

📊 SUMMARY:
   Files scanned: 3
   Signatures checked: 12
   Violations: 2
   Clean signatures: 10
```

---

## Examples

### Example 1: String Helper Violation

**Input:**

```typescript
// src/utils/text.ts
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}
```

**Output:**

```
❌ VIOLATION: src/utils/text.ts:2 capitalize()
   Duplicates: @metasaver/core-utils.capitalize()
   Similarity: 100%
   FIX: import { capitalize } from '@metasaver/core-utils'
```

### Example 2: Component Duplication

**Input:**

```typescript
// src/components/Button.tsx
export function Button({ children, variant, onClick }) {
  return (
    <button className={buttonVariants({ variant })} onClick={onClick}>
      {children}
    </button>
  );
}
```

**Output:**

```
❌ VIOLATION: src/components/Button.tsx:2 Button
   Duplicates: @metasaver/core-components.ZButton
   Similarity: 90%
   FIX: import { ZButton } from '@metasaver/core-components'
```

### Example 3: Clean Scan

**Input:** 3 modified files with unique implementations

**Output:**

```
✅ DRY CHECK PASSED
   Files scanned: 3
   Signatures checked: 8
   No duplications found
```

---

## Template Files

- `templates/extraction-patterns.txt` - Regex patterns for extracting signatures
- `templates/violation-report.txt` - Output format specification
- `templates/scan-script.sh.template` - Shell script for batch scanning

---

## Tool Usage

| Step | Tool          | Purpose                            |
| ---- | ------------- | ---------------------------------- |
| 1    | Bash          | Run git diff to get modified files |
| 2    | Grep          | Extract function/type signatures   |
| 3    | Bash/Grep     | Search shared library packages     |
| 4    | Read          | Compare implementations            |
| 5    | Direct output | Format and display results         |

---

## Related Skills

- `/skill cross-cutting/coding-standards` - DRY principle reference
- `/skill cross-cutting/serena-code-reading` - Code analysis workflow
- `/skill domain/monorepo-audit` - Monorepo structure validation

---
name: eslint-plugin
description: Author custom ESLint plugins and rules with test-driven development. Supports flat config (eslint.config.js) and legacy (.eslintrc.*) formats. Uses @typescript-eslint/rule-tester for testing. Covers problem, suggestion, and layout rules including auto-fixers.
---

# ESLint Plugin Author

You are an expert at writing custom ESLint plugins and rules using test-driven development. This skill guides you through creating robust, well-tested rules that follow established patterns.

## When to Use This Skill

- Enforcing project-specific coding standards
- Creating custom rules for domain-specific patterns
- Building rules with auto-fix capabilities
- Creating TypeScript-aware rules using type information
- Developing rules that provide suggestions for manual fixes
- Migrating from deprecated rules to custom implementations

## Project Setup Detection

Before writing rules, detect the project's ESLint configuration format and testing infrastructure.

### Config Format Detection

```bash
# Check for flat config (ESLint 9+)
# - eslint.config.js / eslint.config.mjs / eslint.config.cjs / eslint.config.ts

# Check for legacy config
# - .eslintrc.js / .eslintrc.cjs / .eslintrc.json
# - .eslintrc.yaml / .eslintrc.yml
# - "eslintConfig" in package.json
```

### Test Framework Detection

Check `package.json` for test runner:

- **Bun**: `bun:test` or bun in devDependencies (preferred)
- **Vitest**: vitest in devDependencies
- **Jest**: jest in devDependencies

### TypeScript Detection

Check for TypeScript setup:

- `tsconfig.json` exists
- `@typescript-eslint/parser` in dependencies
- `@typescript-eslint/eslint-plugin` in dependencies

## Edge Case Discovery

**CRITICAL: Before writing ANY code or tests, you MUST ask clarifying questions about edge cases.**

### Standard Questions (Always Ask)

1. "What should happen when the pattern appears inside comments? Should it be ignored?"
2. "Should this rule apply to all file types, or only specific extensions (`.ts`, `.tsx`, `.js`, `.jsx`)?"
3. "Should the rule be auto-fixable, provide suggestions, or just report errors?"
4. "Are there any existing patterns that should be exempt (e.g., test files, generated code)?"

### Rule-Type-Specific Questions

#### For Identifier/Naming Rules

- "Should the rule apply to variables, functions, classes, or all identifiers?"
- "What about destructured variables? Should `const { oldName } = obj` be flagged?"
- "How should renamed imports be handled? `import { thing as alias }`"
- "Should type-only imports/exports be included?"

#### For Import/Export Rules

- "How should re-exports be handled? `export { foo } from './bar'`"
- "Should dynamic imports be included? `import('./module')`"
- "What about type-only imports in TypeScript? `import type { Foo }`"
- "Should side-effect imports be considered? `import './styles.css'`"

#### For Function/Method Rules

- "Should arrow functions be treated the same as function declarations?"
- "What about methods in classes vs. standalone functions?"
- "Should async functions be handled differently?"
- "How should generator functions be treated?"

#### For JSX/React Rules

- "Should the rule apply to both JSX elements and `React.createElement` calls?"
- "What about fragments (`<>...</>` vs `<React.Fragment>`)?"
- "Should self-closing tags be treated differently?"
- "How should spread props be handled? `<Component {...props} />`"

#### For TypeScript-Specific Rules

- "Should the rule only run when type information is available?"
- "How should `any` types be handled - flag, ignore, or special case?"
- "Should generic type parameters be considered?"
- "What about type assertions (`as` or `<Type>`)?"

### Edge Case Scenario Example

```typescript
// Scenario: Rule that disallows console.log
// Edge cases to clarify:

// 1. What about console.warn, console.error, console.info?
console.warn("warning"); // Flag or allow?

// 2. What about computed property access?
const method = "log";
console[method]("indirect"); // Can we detect this?

// 3. What about destructuring?
const { log } = console;
log("destructured"); // Flag or allow?

// 4. What about reassignment?
const myLog = console.log;
myLog("aliased"); // Flag or allow?

// 5. What about in try-catch for debugging?
try {
} catch (e) {
  console.log(e);
} // Exception?
```

## Rule Creation Process (TDD)

### Step 1: Understand the Rule Intent

Before proceeding, clarify:

- **What pattern are we detecting?** (Provide code examples)
- **What should the error message say?**
- **What is the correct code?** (Provide "after" examples)
- **Rule category:** Is this a problem (error), suggestion (improvement), or layout (formatting)?

### Step 2: Identify Edge Cases (ASK QUESTIONS)

**This step MUST involve asking the user clarifying questions.**

```markdown
Before I write any tests, I want to make sure we handle edge cases correctly.
Let me ask about a few scenarios:

1. [Edge case question 1]
2. [Edge case question 2]
3. [Edge case question 3]

Please let me know how each of these should be handled.
```

### Step 3: Write Tests First

**Always write tests before implementing the rule.** Tests serve as:

- The specification for what the rule should do
- The primary documentation for human reviewers
- A safety net for iterating on the implementation

**Test file structure with `@typescript-eslint/rule-tester` and Bun:**

```typescript
// Location: src/rules/__tests__/rule-name.test.ts

import { afterAll, describe, it } from "bun:test";
import { RuleTester } from "@typescript-eslint/rule-tester";
import rule from "../rule-name";

// Configure RuleTester for Bun BEFORE creating instance
RuleTester.afterAll = afterAll;
RuleTester.describe = describe;
RuleTester.it = it;
RuleTester.itOnly = it.only;

const ruleTester = new RuleTester({
  languageOptions: {
    parser: require("@typescript-eslint/parser"),
    parserOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      ecmaFeatures: { jsx: true },
    },
  },
});

ruleTester.run("rule-name", rule, {
  valid: [
    // ─── VALID: Basic case ─────────────────────────────────────
    `const x = 1;`,

    // ─── VALID: Already correct pattern ────────────────────────
    {
      code: `/* already correct */`,
      name: "ignores already-correct code",
    },
  ],

  invalid: [
    // ─── INVALID: Main transformation ──────────────────────────
    {
      code: `/* problematic code */`,
      output: `/* fixed code */`, // For auto-fixable rules
      errors: [{ messageId: "errorId" }],
      name: "detects and fixes the main case",
    },

    // ─── INVALID: Edge case with options ───────────────────────
    {
      code: `/* edge case */`,
      options: [{ someOption: true }],
      errors: [
        {
          messageId: "errorId",
          line: 1,
          column: 5,
        },
      ],
      name: "handles edge case with option",
    },
  ],
});
```

**Required test categories for every rule:**

| Category    | Purpose                         | Example                      |
| ----------- | ------------------------------- | ---------------------------- |
| Main case   | Core transformation             | The primary before/after     |
| No-op       | Files without pattern unchanged | Unrelated code passes        |
| Idempotency | Running twice = running once    | Already-fixed code           |
| Edge cases  | Variations from Q&A             | Destructuring, aliases, etc. |
| Options     | Different configurations        | With/without flags           |

### Step 4: Implement the Rule

**Rule structure template:**

```typescript
// Location: src/rules/rule-name.ts

import { ESLintUtils, TSESTree } from "@typescript-eslint/utils";

// Create rule with documentation URL
const createRule = ESLintUtils.RuleCreator(
  (name) => `https://example.com/rules/${name}`,
);

// Type for rule options
type Options = [
  {
    someOption?: boolean;
  },
];

// Type for message IDs
type MessageIds = "errorMessageId" | "suggestionMessageId";

export default createRule<Options, MessageIds>({
  name: "rule-name",
  meta: {
    type: "problem", // "problem" | "suggestion" | "layout"
    docs: {
      description: "Description of what the rule does",
    },
    fixable: "code", // Include only if auto-fixable
    hasSuggestions: true, // Include only if has suggestions
    messages: {
      errorMessageId: "Error message with {{ placeholder }}",
      suggestionMessageId: "Suggestion: do this instead",
    },
    schema: [
      {
        type: "object",
        properties: {
          someOption: { type: "boolean" },
        },
        additionalProperties: false,
      },
    ],
  },
  defaultOptions: [{ someOption: false }],

  create(context, [options]) {
    return {
      // Visitor methods using AST selectors
      Identifier(node) {
        // Rule logic
      },
    };
  },
});
```

### Step 5: Run Tests and Iterate

```bash
# Run tests with Bun
bun test src/rules/__tests__/rule-name.test.ts

# Watch mode during development
bun test --watch src/rules/__tests__/rule-name.test.ts
```

### Step 6: Document the Rule

```markdown
# rule-name

Description of what the rule does.

## Rule Details

This rule [enforces/disallows/suggests] ...

### Examples of **incorrect** code:

\`\`\`javascript
/_ eslint my-plugin/rule-name: "error" _/
// bad code example
\`\`\`

### Examples of **correct** code:

\`\`\`javascript
/_ eslint my-plugin/rule-name: "error" _/
// good code example
\`\`\`

## Options

- `someOption` (boolean, default: `false`) - Description
```

## Code Patterns

### Rule Meta Object Patterns

```typescript
// Problem rule (code likely to cause errors)
meta: {
  type: "problem",
  docs: { description: "Disallow X because it causes Y" },
  fixable: "code",
  messages: { detected: "Found X, which causes Y" },
  schema: [],
}

// Suggestion rule (code style improvement)
meta: {
  type: "suggestion",
  docs: { description: "Prefer X over Y for consistency" },
  hasSuggestions: true,
  messages: {
    prefer: "Prefer {{ preferred }} over {{ actual }}",
    useSuggestion: "Replace with {{ preferred }}",
  },
  schema: [],
}

// Layout rule (whitespace, formatting)
meta: {
  type: "layout",
  docs: { description: "Enforce consistent spacing" },
  fixable: "whitespace",
  messages: { spacing: "Expected {{ expected }} spaces" },
  schema: [],
}
```

### Context API Patterns

```typescript
create(context) {
  // Access options
  const options = context.options[0] ?? {};

  // Access source code
  const sourceCode = context.sourceCode;

  // Get text of a node
  const text = sourceCode.getText(node);

  // Get tokens
  const token = sourceCode.getTokenBefore(node);
  const nextToken = sourceCode.getTokenAfter(node);

  // Get comments
  const comments = sourceCode.getCommentsBefore(node);

  // Get scope information
  const scope = sourceCode.getScope(node);

  // Get ancestor nodes
  const ancestors = sourceCode.getAncestors(node);

  return { /* visitors */ };
}
```

### Reporting Patterns

```typescript
// Basic report
context.report({
  node,
  messageId: "errorId",
});

// Report with data placeholders
context.report({
  node,
  messageId: "errorWithData",
  data: {
    name: node.name,
    expected: "something",
  },
});

// Report with specific location
context.report({
  node,
  loc: node.loc.start, // or { line, column }
  messageId: "errorId",
});

// Report with fix
context.report({
  node,
  messageId: "fixable",
  fix(fixer) {
    return fixer.replaceText(node, "replacement");
  },
});

// Report with multiple fixes
context.report({
  node,
  messageId: "multipleChanges",
  fix(fixer) {
    return [
      fixer.insertTextBefore(node, "prefix"),
      fixer.insertTextAfter(node, "suffix"),
    ];
  },
});

// Report with suggestions
context.report({
  node,
  messageId: "hasSuggestions",
  suggest: [
    {
      messageId: "suggestion1",
      fix(fixer) {
        return fixer.replaceText(node, "option1");
      },
    },
    {
      messageId: "suggestion2",
      fix(fixer) {
        return fixer.replaceText(node, "option2");
      },
    },
  ],
});
```

### Fixer API Reference

```typescript
fix(fixer) {
  // Insert text
  fixer.insertTextBefore(node, "text");
  fixer.insertTextAfter(node, "text");
  fixer.insertTextBeforeRange([start, end], "text");
  fixer.insertTextAfterRange([start, end], "text");

  // Remove
  fixer.remove(node);
  fixer.removeRange([start, end]);

  // Replace
  fixer.replaceText(node, "newText");
  fixer.replaceTextRange([start, end], "newText");
}
```

### AST Traversal Patterns

```typescript
create(context) {
  return {
    // Simple node type
    Identifier(node) { },

    // Descending (default) vs ascending
    "FunctionDeclaration:exit"(node) { },

    // CSS selector syntax
    "CallExpression[callee.name='forbidden']"(node) { },

    // Multiple node types
    "FunctionDeclaration, ArrowFunctionExpression"(node) { },

    // Nested selectors
    "CallExpression > Identifier[name='console']"(node) { },

    // With attribute conditions
    "Literal[value=true]"(node) { },

    // Parent selector
    "ImportDeclaration:has(ImportSpecifier[imported.name='deprecated'])"(node) { },
  };
}
```

### Type-Aware Rule Patterns

```typescript
import { ESLintUtils } from "@typescript-eslint/utils";

create(context) {
  // Get TypeScript services
  const services = ESLintUtils.getParserServices(context);
  const checker = services.program.getTypeChecker();

  return {
    CallExpression(node) {
      // Get TypeScript node from ESTree node
      const tsNode = services.esTreeNodeToTSNodeMap.get(node);

      // Get type at location
      const type = checker.getTypeAtLocation(tsNode);

      // Check if type matches
      if (checker.typeToString(type) === "Promise<void>") {
        // Handle Promise return
      }

      // Get return type of function
      const signatures = type.getCallSignatures();
      if (signatures.length > 0) {
        const returnType = signatures[0].getReturnType();
      }
    },
  };
}
```

## Test Patterns

### Basic Test Structure

```typescript
import { afterAll, describe, it } from "bun:test";
import { RuleTester } from "@typescript-eslint/rule-tester";
import rule from "../rule-name";

// Setup BEFORE creating RuleTester
RuleTester.afterAll = afterAll;
RuleTester.describe = describe;
RuleTester.it = it;
RuleTester.itOnly = it.only;

const ruleTester = new RuleTester();

ruleTester.run("rule-name", rule, {
  valid: [],
  invalid: [],
});
```

### Valid Test Cases

```typescript
valid: [
  // Simple string
  `const x = 1;`,

  // Object with name
  {
    code: `const x = 1;`,
    name: "allows basic assignment",
  },

  // With options
  {
    code: `const x = 1;`,
    options: [{ allowX: true }],
    name: "allows X when option enabled",
  },

  // With JSX
  {
    code: `<Component />`,
    languageOptions: {
      parserOptions: {
        ecmaFeatures: { jsx: true },
      },
    },
    name: "handles JSX",
  },

  // Different filename
  {
    code: `console.log('test');`,
    filename: "test.spec.ts",
    name: "allows in test files",
  },
],
```

### Invalid Test Cases

```typescript
invalid: [
  // Basic error
  {
    code: `const bad = 1;`,
    errors: [{ messageId: "forbidden" }],
    name: "detects forbidden pattern",
  },

  // With fix output
  {
    code: `const bad = 1;`,
    output: `const good = 1;`,
    errors: [{ messageId: "forbidden" }],
    name: "fixes forbidden pattern",
  },

  // With specific error location
  {
    code: `const bad = 1;`,
    errors: [
      {
        messageId: "forbidden",
        line: 1,
        column: 7,
        endLine: 1,
        endColumn: 10,
      },
    ],
    name: "reports correct location",
  },

  // With data validation
  {
    code: `const bad = 1;`,
    errors: [
      {
        messageId: "forbidden",
        data: { name: "bad" },
      },
    ],
    name: "includes correct data",
  },

  // Multiple errors
  {
    code: `const bad1 = 1; const bad2 = 2;`,
    errors: [
      { messageId: "forbidden" },
      { messageId: "forbidden" },
    ],
    name: "detects multiple violations",
  },

  // No fix expected
  {
    code: `const complexBad = 1;`,
    output: null, // Assert no fix
    errors: [{ messageId: "tooComplex" }],
    name: "does not fix complex cases",
  },
],
```

### Testing Suggestions

```typescript
{
  code: `const problematic = 1;`,
  errors: [
    {
      messageId: "hasOptions",
      suggestions: [
        {
          messageId: "option1",
          output: `const fixed1 = 1;`,
        },
        {
          messageId: "option2",
          output: `const fixed2 = 1;`,
        },
      ],
    },
  ],
  name: "provides multiple suggestions",
},

// Assert NO suggestions
{
  code: `const edge = 1;`,
  errors: [
    {
      messageId: "noSuggestions",
      suggestions: null,
    },
  ],
  name: "does not suggest for edge case",
},
```

### Type-Aware Rule Testing

```typescript
const ruleTester = new RuleTester({
  languageOptions: {
    parser: require("@typescript-eslint/parser"),
    parserOptions: {
      projectService: {
        allowDefaultProject: ["*.ts*"],
      },
      tsconfigRootDir: __dirname,
    },
  },
});

ruleTester.run("type-aware-rule", rule, {
  valid: [
    {
      code: `
        async function foo(): Promise<void> {
          await someAsyncOp();
        }
      `,
      name: "allows awaited promises",
    },
  ],
  invalid: [
    {
      code: `
        async function foo(): Promise<void> {
          someAsyncOp(); // Not awaited
        }
      `,
      errors: [{ messageId: "floatingPromise" }],
      name: "detects floating promises",
    },
  ],
});
```

## Plugin Structure

### Flat Config Plugin (eslint.config.js)

```typescript
// src/index.ts
import rule1 from "./rules/rule1";
import rule2 from "./rules/rule2";

const plugin = {
  meta: {
    name: "eslint-plugin-my-plugin",
    version: "1.0.0",
  },
  configs: {} as Record<string, unknown>,
  rules: {
    rule1: rule1,
    rule2: rule2,
  },
};

// Self-referential configs (must be after plugin definition)
Object.assign(plugin.configs, {
  recommended: {
    plugins: {
      "my-plugin": plugin,
    },
    rules: {
      "my-plugin/rule1": "error",
      "my-plugin/rule2": "warn",
    },
  },
});

export default plugin;
```

**Usage in flat config:**

```javascript
// eslint.config.js
import myPlugin from "./eslint-plugin-my-plugin";

export default [
  myPlugin.configs.recommended,
  // or individual rules:
  {
    plugins: {
      "my-plugin": myPlugin,
    },
    rules: {
      "my-plugin/rule1": "error",
    },
  },
];
```

### Legacy Config Plugin (.eslintrc.\*)

```typescript
// src/index.ts
import rule1 from "./rules/rule1";
import rule2 from "./rules/rule2";

module.exports = {
  rules: {
    rule1: rule1,
    rule2: rule2,
  },
  configs: {
    recommended: {
      plugins: ["my-plugin"],
      rules: {
        "my-plugin/rule1": "error",
        "my-plugin/rule2": "warn",
      },
    },
  },
};
```

**Usage in legacy config:**

```json
// .eslintrc.json
{
  "plugins": ["my-plugin"],
  "extends": ["plugin:my-plugin/recommended"]
}
```

### Dual-Format Support

```typescript
// src/index.ts
import rule1 from "./rules/rule1";

const rules = {
  rule1: rule1,
};

// For flat config
const plugin = {
  meta: {
    name: "eslint-plugin-my-plugin",
    version: "1.0.0",
  },
  configs: {} as Record<string, unknown>,
  rules,
};

// Flat config presets
Object.assign(plugin.configs, {
  recommended: {
    plugins: { "my-plugin": plugin },
    rules: { "my-plugin/rule1": "error" },
  },
});

// Legacy config presets
const legacyConfigs = {
  recommended: {
    plugins: ["my-plugin"],
    rules: { "my-plugin/rule1": "error" },
  },
};

// Export for both systems
export default plugin;
export { rules, legacyConfigs as configs };
```

## Project Setup Template

### Directory Structure

```
eslint-plugin-my-plugin/
├── src/
│   ├── index.ts              # Plugin entry point
│   └── rules/
│       ├── rule-name.ts      # Rule implementation
│       └── __tests__/
│           └── rule-name.test.ts
├── package.json
├── tsconfig.json
└── bunfig.toml               # Bun configuration (optional)
```

### package.json

```json
{
  "name": "eslint-plugin-my-plugin",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": ["dist"],
  "scripts": {
    "build": "tsc",
    "test": "bun test",
    "test:watch": "bun test --watch",
    "lint": "eslint src"
  },
  "peerDependencies": {
    "eslint": ">=8.0.0",
    "@typescript-eslint/parser": ">=7.0.0"
  },
  "dependencies": {
    "@typescript-eslint/utils": "^8.0.0"
  },
  "devDependencies": {
    "@typescript-eslint/parser": "^8.0.0",
    "@typescript-eslint/rule-tester": "^8.0.0",
    "bun-types": "latest",
    "eslint": "^9.0.0",
    "typescript": "^5.0.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### Test Setup File (Optional)

```typescript
// test-setup.ts
import { afterAll, describe, it } from "bun:test";
import { RuleTester } from "@typescript-eslint/rule-tester";

RuleTester.afterAll = afterAll;
RuleTester.describe = describe;
RuleTester.it = it;
RuleTester.itOnly = it.only;
```

```toml
# bunfig.toml
[test]
preload = ["./test-setup.ts"]
```

## Best Practices

### Rule Implementation

1. **Idempotency** - Fixes must be idempotent; running twice produces same result as once
2. **Minimal changes** - Fix only what's necessary; preserve formatting and comments
3. **Atomic fixes** - One fix per error; don't combine unrelated changes
4. **No runtime changes** - Fixes must not alter code behavior
5. **Range awareness** - Multiple fixes must not have overlapping ranges

### Error Messages

1. **Be specific** - "Unexpected `console.log`" not "Bad code"
2. **Explain why** - "Floating Promise may cause unhandled rejection"
3. **Suggest action** - "Use `await` or handle with `.catch()`"
4. **Use placeholders** - Dynamic values via `{{ name }}` syntax

### Performance

1. **Exit early** - Check preconditions before expensive operations
2. **Cache lookups** - Store repeated `getScope()` or type lookups
3. **Use selectors** - CSS selectors are optimized; prefer them over filtering
4. **Avoid reparse** - Don't call `getText()` on entire source repeatedly

### TypeScript Rules

1. **Version alignment** - Keep all `@typescript-eslint/*` packages at same version
2. **Optional type info** - Don't crash if type information unavailable
3. **Document requirements** - Note if rule requires `projectService`

## Troubleshooting

### Common Issues and Solutions

| Issue                     | Cause                             | Solution                                                      |
| ------------------------- | --------------------------------- | ------------------------------------------------------------- |
| "afterAll is not defined" | RuleTester not configured for Bun | Set `RuleTester.afterAll = afterAll` before creating instance |
| Fix not applied           | `meta.fixable` not set            | Add `fixable: "code"` to meta object                          |
| Suggestions not showing   | `meta.hasSuggestions` missing     | Add `hasSuggestions: true` to meta                            |
| Type info unavailable     | Missing parser options            | Configure `parserOptions.projectService`                      |
| Test timeout              | Type-aware rule slow              | Use `projectService.allowDefaultProject`                      |
| "Unknown rule"            | Plugin not registered             | Check plugin is in config's `plugins` object                  |
| Fix creates syntax error  | Invalid range or text             | Use AST explorer to verify node boundaries                    |

### Debugging Techniques

```typescript
// Log AST node structure
console.log(JSON.stringify(node, null, 2));

// Check what text will be replaced
console.log(context.sourceCode.getText(node));

// Verify token boundaries
const before = context.sourceCode.getTokenBefore(node);
const after = context.sourceCode.getTokenAfter(node);
console.log({ before, after });
```

### AST Exploration Tools

- **AST Explorer**: https://astexplorer.net (select @typescript-eslint/parser)
- **ast-grep**: `sg --lang ts -p 'pattern'` for structural searches

## Example Workflow

When a user requests an ESLint rule:

1. **Clarify the transformation** - Get before/after code examples
2. **Identify the rule type** - problem, suggestion, or layout?
3. **ASK about edge cases** - Use questions from Edge Case Discovery section
4. **Confirm understanding** - Summarize what the rule will do
5. **Write tests first** - Cover main case, edge cases, idempotency
6. **Implement the rule** - Make tests pass
7. **Run tests** - `bun test`
8. **Document** - Add rule documentation

## Notes

- Keep rules focused and testable
- When in doubt, ask the user what they want to do

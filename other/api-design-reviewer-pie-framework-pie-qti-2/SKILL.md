---
name: api-design-reviewer
description: Reviews public APIs in framework code for consistency, usability, type safety, breaking changes, and maintainability. Use when designing new APIs, reviewing API changes, or conducting framework code reviews.
allowed-tools: Read, Glob, Grep, Bash
model: Codex-sonnet-4-20250514
---

# API Design Reviewer

This skill helps review public APIs in framework and library code to ensure they are consistent, usable, type-safe, and maintainable.

## When to Use This Skill

Invoke this skill when:
- Designing a new public API for a package or module
- Reviewing changes to existing public APIs
- Conducting code reviews for framework/library code
- Ensuring consistency across multiple packages in a monorepo
- Evaluating breaking changes and their impact
- Checking TypeScript type definitions for correctness
- Reviewing plugin/extension architectures

## Review Checklist

### 1. API Consistency

**Cross-Package Consistency**
- Do similar features use similar patterns across packages?
- Are configuration objects structured consistently?
- Do function signatures follow similar conventions?
- Is error handling consistent across the API surface?

**Naming Conventions**
- Are names clear, descriptive, and unambiguous?
- Is terminology consistent throughout the codebase?
- Do names follow the project's established conventions?
- Are domain-specific terms used consistently (e.g., in QTI: "interaction" vs "component", "response" vs "answer")?

**Example Issues to Catch:**
```typescript
// ❌ Inconsistent: One package uses `config`, another uses `options`
class ItemPlayer {
  constructor(config: PlayerConfig) {}
}
class AssessmentPlayer {
  constructor(options: AssessmentOptions) {} // Should be `config`
}

// ✅ Consistent
class ItemPlayer {
  constructor(config: PlayerConfig) {}
}
class AssessmentPlayer {
  constructor(config: AssessmentPlayerConfig) {}
}
```

### 2. Type Safety

**TypeScript Best Practices**
- Are types properly exported for consumers?
- Are generics used appropriately and not over-engineered?
- Are union types and discriminated unions used correctly?
- Are types covariant/contravariant where appropriate?
- Are `any` and `unknown` used judiciously?
- Are brand types used for type-safe IDs when appropriate?

**Type Completeness**
- Do all public functions have return type annotations?
- Are complex types documented with TSDoc?
- Are type parameters constrained appropriately?
- Are utility types (Partial, Required, Pick, Omit) used correctly?

**Example Issues to Catch:**
```typescript
// ❌ Weak typing: String-based discriminator without literal types
type Interaction = {
  type: string; // Could be anything!
  data: any;
}

// ✅ Strong typing: Discriminated union with literal types
type Interaction =
  | { type: 'choice'; data: ChoiceData }
  | { type: 'text'; data: TextData }
  | { type: 'match'; data: MatchData };

// ❌ Missing constraints on generic
function registerRenderer<T>(renderer: T) {}

// ✅ Properly constrained generic
function registerRenderer<T extends InteractionRenderer>(renderer: T) {}
```

### 3. Breaking Changes

**Semantic Versioning**
- Would this change require a major version bump?
- Can the change be made backward-compatible?
- Should deprecated APIs be introduced first?
- Are there migration paths for breaking changes?

**Deprecation Strategy**
- Are deprecated APIs marked with `@deprecated` JSDoc tags?
- Do deprecation notices explain what to use instead?
- Is there a timeline for removal?

**Example Issues to Catch:**
```typescript
// ❌ Breaking change without deprecation period
// OLD: export function render(item: Item, mode: Mode): string
// NEW: export function render(item: Item, role: QTIRole): string

// ✅ Graceful deprecation path
/**
 * @deprecated Use `role` parameter instead of `mode`. Will be removed in v3.0.
 */
export function render(item: Item, mode: Mode): string;
export function render(item: Item, role: QTIRole): string;
export function render(item: Item, modeOrRole: Mode | QTIRole): string {
  // Support both during transition
}
```

### 4. Usability & Developer Experience

**API Surface**
- Is the API minimal yet complete (no feature envy)?
- Are common use cases easy and uncommon cases possible?
- Are there sensible defaults?
- Is configuration progressive (simple by default, advanced when needed)?

**Error Messages**
- Are errors descriptive and actionable?
- Do errors guide users toward solutions?
- Are validation errors thrown early with clear messages?

**Documentation**
- Do all public APIs have TSDoc comments?
- Are examples provided for complex features?
- Are edge cases and limitations documented?

**Example Issues to Catch:**
```typescript
// ❌ Poor DX: Complex API for common case
const player = new ItemPlayer({
  renderer: new RendererRegistry(),
  validator: new ResponseValidator(),
  scorer: new ResponseScorer(),
  formatter: new OutputFormatter()
});

// ✅ Good DX: Simple defaults, advanced options available
const player = new ItemPlayer(); // Works with sensible defaults
const advancedPlayer = new ItemPlayer({
  customRenderer: myRenderer, // Only specify what you need
});

// ❌ Vague error
throw new Error('Invalid input');

// ✅ Actionable error
throw new Error(
  `Invalid interaction type "${type}". Expected one of: ${VALID_TYPES.join(', ')}.`
);
```

### 5. Plugin Architecture & Extensibility

**Extension Points**
- Are extension points clearly defined and documented?
- Is the plugin interface minimal yet powerful?
- Can users extend behavior without forking?
- Are there hooks for common customization needs?

**Registry Patterns**
- Is registration/lookup type-safe?
- Are conflicts handled gracefully?
- Can plugins be removed/replaced?
- Is plugin loading lazy when possible?

**Dependency Injection**
- Are dependencies injected rather than hard-coded?
- Can dependencies be mocked for testing?
- Is circular dependency avoided?

**Example Issues to Catch:**
```typescript
// ❌ Hard to extend: Implementation details leaked
export class Player {
  private renderChoice(data: ChoiceData) { /* ... */ }
  private renderText(data: TextData) { /* ... */ }
  // Users can't add custom interaction types!
}

// ✅ Extensible: Plugin registry pattern
export interface InteractionRenderer<T = unknown> {
  type: string;
  render(data: T, config: RenderConfig): string;
}

export class InteractionRegistry {
  register<T>(renderer: InteractionRenderer<T>): void;
  get<T>(type: string): InteractionRenderer<T> | undefined;
}

export class Player {
  constructor(private registry: InteractionRegistry) {}
  // Users can register custom renderers!
}
```

### 6. Performance & Bundle Size

**Framework-Level Concerns**
- Are heavy dependencies conditionally imported?
- Can features be tree-shaken if unused?
- Are there opportunities for code-splitting?
- Are large data structures lazy-loaded?

**Example Issues to Catch:**
```typescript
// ❌ Always imports heavy dependencies
import { FullRichTextEditor } from 'heavy-editor'; // 500KB

export class Player {
  // Editor might not be needed for all interaction types!
}

// ✅ Lazy-load heavy dependencies
export class Player {
  async loadRichTextEditor() {
    const { FullRichTextEditor } = await import('heavy-editor');
    return FullRichTextEditor;
  }
}
```

### 7. Framework-Specific Considerations

**For QTI/Educational Assessment Projects:**
- Does the API respect QTI standard terminology for the relevant version?
- Are QTI roles (candidate, scorer, author, etc.) properly typed?
- Is response processing type-safe?
- Are interaction types properly discriminated?
- Does the API work for both single items and full assessments?

**For Monorepos:**
- Are package boundaries clear?
- Are internal vs. public APIs clearly separated?
- Are shared types in a common package?
- Do packages have clear, non-circular dependencies?

## Review Process

When conducting an API review:

1. **Read the public API surface** - Look at exports, type definitions, and main entry points
2. **Check consistency** - Compare with similar APIs in other packages
3. **Evaluate types** - Ensure TypeScript types are correct and helpful
4. **Identify breaking changes** - Flag anything that would break existing code
5. **Test usability** - Consider the developer experience for common and advanced cases
6. **Review documentation** - Ensure TSDoc is complete and examples are present
7. **Check extensibility** - Verify plugin points are well-designed
8. **Provide specific feedback** - Use code examples to illustrate issues

## Output Format

Provide feedback in this structure:

### ✅ Strengths
- What's working well
- Good patterns to reinforce

### ⚠️ Issues Found
For each issue:
- **Severity**: Critical (breaking) / High (usability) / Medium (consistency) / Low (polish)
- **Description**: What's wrong
- **Example**: Code showing the issue
- **Recommendation**: Specific fix with code example

### 💡 Suggestions
- Optional improvements
- Future enhancements to consider

## Examples

### Good API Design Patterns

**Progressive Complexity:**
```typescript
// Simple case: just works
const player = new ItemPlayer();

// Advanced case: full control
const player = new ItemPlayer({
  registry: customRegistry,
  config: { locale: 'es', theme: 'dark' }
});
```

**Type-Safe Plugins:**
```typescript
interface InteractionRenderer<T = unknown> {
  type: string;
  render(data: T, config: RenderConfig): string;
}

class ChoiceRenderer implements InteractionRenderer<ChoiceData> {
  type = 'choice' as const;
  render(data: ChoiceData, config: RenderConfig): string {
    // TypeScript knows data is ChoiceData
  }
}
```

**Clear Deprecation:**
```typescript
/**
 * @deprecated Use `role` parameter instead. The `mode` parameter will be
 * removed in v3.0. See migration guide: https://example.com/migration
 */
export function render(item: Item, mode: 'gather' | 'view'): string;
```

## Tool Usage

- **Read**: Examine TypeScript files, type definitions, and exports
- **Glob**: Find all public API entry points (`index.ts`, `*.d.ts`)
- **Grep**: Search for patterns like `export`, `@deprecated`, `@public`, interface definitions
- **Bash**: Run TypeScript compiler to check for type errors, or `tsc --noEmit` for validation

## Important Notes

- Focus on PUBLIC APIs (exported from package entry points)
- Don't review internal implementation details unless they leak into the public API
- Consider both current consumers and future extensibility
- Balance idealism with pragmatism (perfect APIs are rare)
- Remember that consistency > individual perfection

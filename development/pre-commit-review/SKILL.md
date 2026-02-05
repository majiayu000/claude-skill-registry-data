---
name: pre-commit-review
description: ADVISORY validation of code against design principles, accessibility, and best practices that linters cannot fully enforce. Use after linter passes and tests pass to validate design quality. Categorizes findings as Design Debt, Readability Debt, or Polish Opportunities. Does NOT block commits.
---

# Pre-Commit Design Review (React/TypeScript)

ADVISORY validation of code against design principles, accessibility, and practices that linters cannot fully enforce.
Categorizes findings as Design Debt, Readability Debt, or Polish Opportunities.

## When to Use
- Automatically invoked by @linter-driven-development (Phase 4)
- Manually before committing (to validate design quality)
- After linter passes and tests pass

## What This Reviews
- **NOT code correctness** (tests verify that)
- **NOT syntax/style** (ESLint/Prettier enforce that)
- **YES design principles** (primitive obsession, composition, architecture)
- **YES maintainability** (readability, complexity, testability)
- **YES accessibility** (semantic HTML, ARIA, keyboard nav)

## Review Scope

**Primary Scope**: Changed code in commit
- All modified lines
- All new components/hooks
- Specific focus on design principle adherence
- Accessibility compliance

**Secondary Scope**: Context around changes
- Entire files containing modifications
- Flag patterns/issues outside commit scope
- Suggest broader refactoring opportunities

## Finding Categories (Debt-Based)

### 🔴 Design Debt
**Will cause pain when extending/modifying code**

Violations:
- **Primitive obsession**: string IDs, unvalidated inputs, no branded types
- **Wrong architecture**: Technical layers instead of feature-based
- **Prop drilling**: State passed through 3+ component levels
- **Tight coupling**: Components tightly coupled to specific implementations
- **Missing error boundaries**: No error handling for async operations
- **No type validation**: Runtime data not validated (no Zod schemas)

Impact: Future changes will require more work and introduce bugs

### 🟡 Readability Debt
**Makes code harder to understand and work with**

Violations:
- **Mixed abstractions**: Business logic mixed with UI in same component
- **Complex conditions**: Deeply nested or complex boolean expressions
- **Inline styles/logic**: Complex logic directly in JSX
- **Poor naming**: Generic names (data, handler, manager, utils)
- **God components**: Components doing too many things
- **Missing extraction**: Logic that should be custom hooks

Impact: Team members (and AI) will struggle to understand intent

### 🟢 Polish Opportunities
**Minor improvements for consistency and quality**

Violations:
- **Missing JSDoc**: Complex types/hooks without documentation
- **Accessibility enhancements**: Could be more accessible (but not broken)
- **Type improvements**: Could use more specific types (vs any/unknown)
- **Better naming**: Non-idiomatic or unclear names
- **Performance**: Unnecessary rerenders, missing memoization
- **Bundle size**: Unused dependencies, large imports

Impact: Low, but improves codebase quality

## Review Workflow

### 0. Architecture Pattern Validation (FIRST CHECK)

**Expected: Feature-based architecture. Design Debt (ADVISORY) - never blocks commit.**

Check file patterns:
- `src/features/[feature]/{components,hooks,context}/` → ✅ Feature-based
- `src/{components,hooks,contexts}/[feature].tsx` → 🔴 Technical layers (Design Debt)

**Advisory Categories**:
1. **✅ Feature-based** → Praise, note migration progress if applicable
2. **🟢 Mixed without docs** → Suggest creating `docs/architecture/feature-based-migration.md`
3. **🔴 Technical layers (advisory)** → Suggest feature-based alternative, respect constraints

**Report Template**:
```
🔴 Design Debt (Advisory): Technical Layer Architecture
- Current: Code organized by technical type (components/, hooks/, etc.)
- Preferred: Feature-based structure for better cohesion/maintainability
- Alternative: Continue as-is (time constraints, team decision valid)
- Offer: Create migration docs? Refactor? Proceed as-is?
```

**Always acknowledge**: Time pressure, consistency needs, team decisions are valid reasons to proceed.

---

### 1. Analyze Commit Scope
```bash
# Identify what changed
git diff --name-only

# See actual changes
git diff
```

### 2. Review Design Principles

Check for each principle in changed code:

#### Primitive Obsession
**Look for**:
- String types for domain concepts (email, userId, etc.)
- Numbers without validation (age, price, quantity)
- Booleans representing state (use discriminated unions)

**Example violation**:
```typescript
// 🔴 Design Debt
interface User {
  id: string  // What if empty? Not UUID?
  email: string  // What if invalid?
}

// ✅ Better
type UserId = Brand<string, 'UserId'>
const EmailSchema = z.string().email()
```

#### Component Composition
**Look for**:
- Prop drilling (state passed through 3+ levels)
- Giant components (>200 lines)
- Mixed UI and business logic
- Inline complex logic in JSX

**Example violation**:
```typescript
// 🔴 Design Debt: Prop drilling
<Parent>
  <Middle user={user} onUpdate={onUpdate}>
    <Deep user={user} onUpdate={onUpdate}>
      <VeryDeep user={user} onUpdate={onUpdate} />
    </Deep>
  </Middle>
</Parent>

// ✅ Better: Use context or composition
<UserProvider>
  <Parent>
    <Middle><Deep><VeryDeep /></Deep></Middle>
  </Parent>
</UserProvider>
```

#### Custom Hooks
**Look for**:
- Complex logic in components (should be in hooks)
- Duplicated logic across components
- useEffect with complex dependencies

**Example violation**:
```typescript
// 🟡 Readability Debt: Logic in component
function UserProfile() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(false)
  useEffect(() => {
    // 50 lines of fetch logic
  }, [])
  // More logic...
}

// ✅ Better: Extract to hook
function useUser(id) { /* fetch logic */ }
function UserProfile() {
  const { user, loading } = useUser(userId)
  return <UI user={user} loading={loading} />
}
```

### 3. Review Accessibility

**Check for each component** (jsx-a11y rules + manual review):

#### Semantic HTML
- Using correct HTML elements (<button>, <form>, <nav>, <main>)
- Proper heading hierarchy (h1 → h2 → h3, no skipping)
- Lists for list content (<ul>, <ol>)

**Example violations**:
```typescript
// 🔴 Design Debt: Non-semantic
<div onClick={handleClick}>Click me</div>  // Should be <button>

// 🟡 Readability Debt: Wrong heading order
<h1>Title</h1>
<h3>Subtitle</h3>  // Skipped h2

// ✅ Better
<button onClick={handleClick}>Click me</button>
<h1>Title</h1>
<h2>Subtitle</h2>
```

#### ARIA Attributes
- Form inputs have labels
- Interactive elements have accessible names
- Images have alt text
- Dialogs have proper roles and labels

**Example violations**:
```typescript
// 🔴 Design Debt: Missing label
<input type="text" placeholder="Email" />

// 🟢 Polish: Could improve alt text
<img src="avatar.jpg" alt="image" />  // Generic

// ✅ Better
<label htmlFor="email">Email</label>
<input id="email" type="text" />

<img src="avatar.jpg" alt="John Doe's profile picture" />
```

#### Keyboard Navigation
- All interactive elements keyboard accessible
- Focus styles visible
- Logical tab order
- Escape closes modals

**Example violations**:
```typescript
// 🔴 Design Debt: No keyboard support
<div onClick={handleClick}>Action</div>

// ✅ Better
<button onClick={handleClick}>Action</button>

// Or if div required:
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  Action
</div>
```

#### Color and Contrast
- Text readable (sufficient contrast)
- Not relying on color alone for meaning
- Focus indicators visible

**Example violations**:
```typescript
// 🟡 Readability Debt: Color only indicates error
<Input style={{ borderColor: 'red' }} />

// ✅ Better: Visual + text indicator
<Input
  aria-invalid="true"
  aria-describedby="email-error"
  style={{ borderColor: 'red' }}
/>
<span id="email-error">Email is invalid</span>
```

#### Screen Reader Support
- Dynamic content announces updates (aria-live)
- Loading states communicated
- Error messages associated with fields

**Example violations**:
```typescript
// 🟢 Polish: Loading not announced
{isLoading && <Spinner />}

// ✅ Better
{isLoading && (
  <div role="status" aria-live="polite">
    Loading user data...
    <Spinner aria-hidden="true" />
  </div>
)}
```

### 4. Review TypeScript Usage

**Type safety**:
- Using `any` or `unknown` without validation
- Missing type definitions for props
- Not using branded types for domain concepts
- Not using Zod for runtime validation

**Example violations**:
```typescript
// 🔴 Design Debt: Using any
function processData(data: any) { }

// 🟡 Readability Debt: Inline type
function Button(props: { label: string; onClick: () => void }) { }

// ✅ Better
const DataSchema = z.object({ /* ... */ })
function processData(data: z.infer<typeof DataSchema>) { }

interface ButtonProps {
  label: string
  onClick: () => void
}
function Button({ label, onClick }: ButtonProps) { }
```

### 5. Review Testing Implications

**Testability**:
- Components too complex to test
- Logic not extracted to testable units
- Testing implementation details (bad)

**Example violations**:
```typescript
// 🟡 Readability Debt: Hard to test
function ComplexForm() {
  // 200 lines of intertwined logic and UI
  // Would need to test implementation details
}

// ✅ Better: Separated concerns
function useFormLogic() { /* testable hook */ }
function FormUI({ state, actions }) { /* testable UI */ }
```

### 6. Broader Context Review

After reviewing changed code, scan entire modified files for:
- Similar violations elsewhere in file
- Patterns suggesting broader refactoring
- Opportunities for consistency improvements

**Report format**:
```
📝 BROADER CONTEXT:
While reviewing LoginForm.tsx, noticed similar validation patterns in
RegisterForm.tsx and ProfileForm.tsx (src/features/user/). Consider
extracting shared validation logic to a useFormValidation hook or
creating branded types for Email, Password used across features.
```

## Output Format

After review:

```
⚠️  PRE-COMMIT REVIEW FINDINGS

Reviewed:
- src/features/auth/LoginForm.tsx (+45, -20 lines)
- src/features/auth/types.ts (+15, -0 lines)
- src/features/auth/useAuth.ts (+30, -5 lines)

🔴 DESIGN DEBT (2 findings) - Recommended to fix:

1. src/features/auth/LoginForm.tsx:45 - Primitive obsession
   Current: email validation with regex inline
   Better:  Use Zod schema or branded Email type
   Why:     Type safety, validation guarantee, reusable across features
   Fix:     Use @component-designing to create Email type

2. src/features/auth/LoginForm.tsx:89 - Missing error boundary
   Current: Async login can fail silently
   Better:  Wrap with ErrorBoundary or add error handling
   Why:     Better user experience, prevents broken UI
   Fix:     Add ErrorBoundary or try-catch with user feedback

🟡 READABILITY DEBT (3 findings) - Consider fixing:

1. src/features/auth/LoginForm.tsx:120 - Mixed abstractions
   Component mixes validation logic with UI rendering
   Why:     Harder to understand and test independently
   Fix:     Extract validation to useFormValidation hook

2. src/features/auth/LoginForm.tsx:67 - Complex condition
   if (email && email.length > 0 && /regex/.test(email) && !isSubmitting && !error)
   Why:     Hard to understand intent
   Fix:     Extract to: const canSubmit = isFormValid(email, isSubmitting, error)

3. src/features/auth/useAuth.ts:34 - Missing hook extraction
   Complex useEffect with multiple concerns
   Why:     Hard to test, hard to reuse
   Fix:     Split into useLogin and useAuthState hooks

🟢 POLISH OPPORTUNITIES (4 findings) - Optional improvements:

1. src/features/auth/types.ts:10 - Missing JSDoc
   Public Email type should have documentation
   Suggestion: Add JSDoc explaining validation rules

2. src/features/auth/LoginForm.tsx:12 - Accessibility enhancement
   Form could use aria-describedby for better screen reader support
   Current:  <input type="email" />
   Better:   <input type="email" aria-describedby="email-hint" />
   Impact:   Better accessibility for screen reader users

3. src/features/auth/LoginForm.tsx:55 - Keyboard navigation
   Close button could have Escape key handler
   Suggestion: Add onKeyDown handler for Escape key

4. src/features/auth/useAuth.ts:89 - Type improvement
   Return type could be more specific than { user: User | null }
   Suggestion: Use discriminated union for different states

📝 BROADER CONTEXT:
While reviewing LoginForm.tsx, noticed similar validation patterns in
RegisterForm.tsx (lines 45-67) and ProfileForm.tsx (lines 89-110).
Consider:
- Extract shared validation to useFormValidation hook
- Create branded Email and Password types used across auth feature
- Add error boundaries to all auth forms consistently

────────────────────────────────────────

💡 RECOMMENDATION:
Fix design debt (🔴) before committing if possible. Design debt compounds
over time and makes future changes harder. Readability and Polish can be
addressed in follow-up commits.

Would you like to:
1. Commit as-is (accept debt)
2. Fix design debt (🔴), then commit
3. Fix design + readability (🔴 + 🟡), then commit
4. Fix all findings (🔴 🟡 🟢), then commit
5. Refactor broader scope (address validation patterns across features)
```

## Key Principles

See reference.md for detailed principles:
- Primitive obsession prevention
- Component composition over prop drilling
- Custom hooks for reusable logic
- Semantic HTML and ARIA
- Type safety with TypeScript and Zod
- Testability and separation of concerns
- Accessibility is not optional

## After Review

This is **ADVISORY** only. User decides:
- Accept debt knowingly
- Fix critical issues (design debt)
- Fix all findings
- Expand refactoring scope

The review never blocks commits. It informs decisions.

See reference.md for complete review checklist and examples.

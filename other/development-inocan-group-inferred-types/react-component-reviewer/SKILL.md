---
name: react-component-reviewer
description: Review React components for best practices, hooks usage, performance issues, accessibility, and TypeScript type safety. Use when you need to audit existing React components or provide code review feedback.
---

# React Component Reviewer

## Overview
This skill provides a systematic approach to reviewing React components, identifying issues, and suggesting improvements across multiple dimensions: best practices, hooks usage, performance, accessibility, and TypeScript type safety.

## Prerequisites
- The React component code to review
- Understanding of the component's purpose and context
- Knowledge of the project's React version and conventions

## Review Checklist

### 1. React Best Practices
- [ ] Component naming follows PascalCase convention
- [ ] Props are properly typed (TypeScript interfaces/types)
- [ ] Component has a single, clear responsibility
- [ ] Avoid unnecessary wrapper divs (use fragments)
- [ ] Event handlers follow naming convention (handle*, on*)
- [ ] No inline object/array literals in JSX (causes re-renders)
- [ ] Keys are stable and unique for lists (not using index)
- [ ] Conditional rendering is clear and readable
- [ ] No console.log or debug code left behind

### 2. Hooks Usage
- [ ] Hooks are called at top level (not inside conditions/loops)
- [ ] Hooks follow the rules of hooks
- [ ] useEffect dependencies are complete and correct
- [ ] No missing dependencies (ESLint warnings)
- [ ] Cleanup functions in useEffect where needed
- [ ] useMemo/useCallback used appropriately (not prematurely)
- [ ] Custom hooks follow naming convention (use*)
- [ ] useState initial values are properly typed
- [ ] useRef usage is correct for DOM refs and mutable values

### 3. Performance
- [ ] No unnecessary re-renders (React.memo where appropriate)
- [ ] Expensive calculations wrapped in useMemo
- [ ] Event handlers wrapped in useCallback when passed to children
- [ ] No premature optimization (only optimize if there's a problem)
- [ ] Large lists use virtualization if needed
- [ ] Images have proper dimensions and loading strategies
- [ ] No N+1 rendering patterns
- [ ] Component splits are logical and performance-conscious

### 4. Accessibility (a11y)
- [ ] Semantic HTML elements used (button, nav, main, etc.)
- [ ] Interactive elements are keyboard accessible
- [ ] ARIA labels present where needed
- [ ] Form inputs have associated labels
- [ ] Focus management is correct (modals, dynamic content)
- [ ] Color contrast meets WCAG standards
- [ ] Alt text for images (or empty alt for decorative)
- [ ] Headings follow hierarchical order (h1, h2, h3)
- [ ] No accessibility violations (test with axe-core)

### 5. TypeScript Type Safety
- [ ] No use of `any` type (use `unknown` if truly unknown)
- [ ] Props interface is well-defined and exported if needed
- [ ] Event handlers have correct types (React.MouseEvent, etc.)
- [ ] Generic types used correctly (React.FC vs function components)
- [ ] Return types are explicit for complex functions
- [ ] Discriminated unions for variant components
- [ ] Optional props marked with `?`
- [ ] ReadonlyArray for props that shouldn't mutate

### 6. Testing Considerations
- [ ] Component is testable (not too many side effects)
- [ ] Props are mockable/injectable
- [ ] External dependencies can be stubbed
- [ ] Component has corresponding test file
- [ ] Critical user interactions are covered by tests

### 7. Code Quality
- [ ] DRY principle followed (no repeated logic)
- [ ] Magic numbers/strings extracted to constants
- [ ] Error handling is present and appropriate
- [ ] Loading and error states are handled
- [ ] Comments explain "why" not "what"
- [ ] Consistent formatting (Prettier)

## Review Output Format

Structure your review as follows:

```markdown
## Component Review: [ComponentName]

### Summary
[1-2 sentence overview of the component and overall code quality]

### Critical Issues 🔴
[Issues that must be fixed - security, accessibility, breaking bugs]

### Performance Issues 🟡
[Performance problems that should be addressed]

### Best Practice Improvements 🔵
[Non-critical improvements for better code quality]

### Positive Highlights ✅
[Things the component does well - always include this!]

### Detailed Findings

#### [Category Name]
**Issue**: [Description with file:line reference]
**Current Code**:
```typescript
// problematic code
```
**Recommendation**:
```typescript
// improved code
```
**Rationale**: [Why this change matters]

[Repeat for each finding]

### Priority Recommendations
1. [Most important fix]
2. [Second priority]
3. [Third priority]
```

## Examples

### Example Review

```markdown
## Component Review: UserProfile

### Summary
Well-structured component with good TypeScript usage, but has accessibility issues and unnecessary re-renders.

### Critical Issues 🔴

1. **Missing Keyboard Accessibility** (UserProfile.tsx:45)
   - Custom dropdown not keyboard accessible
   - Add onKeyDown handlers and ARIA attributes

2. **Incorrect Hook Dependencies** (UserProfile.tsx:23)
   - useEffect missing `userId` dependency
   - Can cause stale data issues

### Performance Issues 🟡

1. **Inline Function in JSX** (UserProfile.tsx:67)
   ```typescript
   // Current
   <Button onClick={() => handleClick(userId)}>Click</Button>

   // Better
   const handleButtonClick = useCallback(() => {
     handleClick(userId);
   }, [userId]);

   <Button onClick={handleButtonClick}>Click</Button>
   ```

### Best Practice Improvements 🔵

1. **Props Interface Could Be More Specific** (UserProfile.tsx:5)
   - Use discriminated union for `status` instead of string

2. **Magic Number** (UserProfile.tsx:89)
   - Extract `100` to named constant `MAX_BIO_LENGTH`

### Positive Highlights ✅

- Excellent TypeScript typing for props and state
- Good separation of concerns with custom hooks
- Proper error boundary implementation
- Clean, readable JSX structure

### Priority Recommendations
1. Fix keyboard accessibility (Critical for WCAG compliance)
2. Fix useEffect dependencies (Prevents bugs)
3. Optimize re-renders with useCallback (Performance)
```

## Guidelines

### When Reviewing
- **Be Specific**: Always reference file names and line numbers
- **Provide Context**: Explain why something is an issue
- **Show Examples**: Include before/after code snippets
- **Be Constructive**: Balance criticism with positive feedback
- **Prioritize**: Not everything needs to be fixed immediately
- **Consider Trade-offs**: Performance optimizations have complexity costs

### What to Prioritize
1. **Critical Issues**: Security, accessibility violations, bugs
2. **Performance**: Only if there's actual evidence of problems
3. **Best Practices**: Code quality and maintainability
4. **Style**: Lowest priority, unless it affects readability

### What NOT to Flag
- Personal style preferences (if project has Prettier/ESLint)
- Premature optimizations without performance data
- Minor naming nitpicks
- Things that are already handled by automated tools

### Code Review Tone
- Professional and respectful
- Educational (explain the "why")
- Actionable (provide clear next steps)
- Balanced (acknowledge good code too)

## Common React Anti-Patterns to Watch For

1. **State Management Issues**
   - Derived state that should be computed
   - State that should be props
   - Multiple setState calls that should be batched

2. **Effect Issues**
   - useEffect that should be event handlers
   - Missing cleanup functions
   - Infinite loops from missing dependencies

3. **Performance**
   - Creating components inside components
   - Inline objects/arrays in JSX
   - Not memoizing context values

4. **TypeScript**
   - Using `any` instead of proper types
   - Not typing event handlers
   - Missing generic constraints

## Testing the Component

After reviewing, consider suggesting:
- Unit tests for logic
- Integration tests for user flows
- Accessibility tests with @testing-library/jest-dom
- Visual regression tests if applicable

## Limitations

This skill focuses on React component code review. It does not:
- Run automated tests (suggest running them separately)
- Check runtime performance (requires profiling)
- Verify design system compliance (requires design specs)
- Test in multiple browsers (requires manual/automated testing)

## Next Steps After Review

1. Create a prioritized list of changes
2. Discuss critical issues with the team
3. Create tickets/issues for non-trivial fixes
4. Consider refactoring if issues are widespread
5. Update team guidelines if patterns emerge

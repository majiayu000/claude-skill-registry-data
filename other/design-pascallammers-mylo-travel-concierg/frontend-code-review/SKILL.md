---
name: frontend-code-review
description: Teetsh frontend code review for React/TypeScript PRs. Reviews component architecture, React Query, twin.macro styling, i18n, accessibility, responsive design, and testing. Use for PR reviews to ensure adherence to Teetsh patterns.
---

# Frontend Code Review

Perform thorough frontend code reviews for the Teetsh React/TypeScript codebase.

## Review Process

### 1. Understand the Context

Before reviewing, gather context:
- Read the PR description or understand the change purpose
- Identify which features/containers are affected
- Check if this affects shared components, queries, or styling

### 2. Load Relevant References

Based on the review type, read appropriate references:

- **Always read**: `references/common-mistakes.md` for Teetsh-specific antipatterns
- **For components/hooks**: `references/react-patterns.md`
- **For data fetching**: `references/react-query.md`
- **For UI/styling**: `references/styling.md`
- **For translations**: `references/i18n.md`
- **For test changes**: `references/testing.md`

### 3. Review Scope by Type

**Full PR Review**: Check all aspects - architecture, implementation, styling, i18n, tests

**Component Review**: Focus on patterns, props typing, accessibility, responsive design

**Query Review**: Focus on query keys, serializers, error handling, mutations

**Styling Review**: Focus on twin.macro usage, theme constants, responsive classes

### 4. Provide Structured Feedback

Organize feedback by priority:

#### Critical Issues
Security vulnerabilities, broken functionality, accessibility blockers, data loss risks

#### Important Issues
Missing error/loading states, incorrect patterns, i18n gaps, test gaps

#### Suggestions
Code clarity, performance optimizations, better patterns

#### Positive Feedback
Well-designed components, good test coverage, clean patterns

### 5. Code Examples

For each issue, provide:
- **What**: Describe the problem
- **Why**: Explain the risk or impact
- **How**: Show code example of the fix

## Key Review Areas

### React Patterns

Check adherence to Teetsh patterns:
- Container vs Component separation (containers handle logic, components are presentational)
- Compound components for complex UI groups (Disclosure, FormGroup)
- Context hooks with validation (`useUser`, `useSchoolSchoolyear`)
- Custom hooks naming (`useXxx`)
- Prefer CSS-based responsive (`tw="lg:flex"`), use `useIsBelowBreakpoint` only when layouts differ completely
- Default export for components, named export for utilities

### React Query

- Query keys include all dependencies: `[schoolyearId, schoolId, KEY_CONSTANT, ...params]`
- Data transformation in serializer functions, not components
- Appropriate `staleTime` for data type
- Error handling with `AxiosError` typing
- Mutations with proper cache invalidation

### Styling

- Use `tw` macro, not className strings
- Colors from `themeConstants.ts`, never hardcoded
- Conditional styles: `css={[tw`...`, condition && tw`...]}`
- Form inputs wrapped with `FormGroup`
- Responsive: mobile-first, `lg:` breakpoint for desktop

### i18n

- `useTranslation(['namespace'])` with namespace array
- Keys: `namespace:section.key`
- Dates: use `format()` utility with locale
- No hardcoded user-facing strings

### Accessibility

- Semantic HTML (button vs div, etc.)
- ARIA labels on interactive elements
- Labels linked to inputs with `htmlFor`
- Keyboard navigation support

### Testing

- Browser tests (Vitest browser) for components: `Component.browser.test.tsx`
- jsdom tests for unit/logic: `utils.test.tsx`
- Playwright E2E for critical user flows
- Storybook stories for design system components
- Descriptive test names: `it('should return X when Y')`

## Review Output Format

Structure your review as:

```
## Critical Issues
[Issues that must be fixed before merge]

## Important Issues
[Issues that should be fixed]

## Suggestions
[Optional improvements]

## Positive Feedback
[What was done well]
```

For each issue:
```
### [Area]: [Brief description]

**Problem**: [What's wrong and why it matters]

**Current code**:
```tsx
[Show problematic code]
```

**Suggested fix**:
```tsx
[Show corrected code]
```

**Reference**: [Link to specific pattern]
```

## Example Review Snippets

### Missing FormGroup Wrapper
```
### Styling: Input missing FormGroup wrapper

**Problem**: Form inputs should be wrapped with FormGroup for consistent styling and accessibility

**Current code**:
```tsx
<Input
  id="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
/>
```

**Suggested fix**:
```tsx
<FormGroup
  id="email"
  label={t('common:form.email')}
  error={errors.email}
>
  <Input
    id="email"
    value={email}
    onChange={(e) => setEmail(e.target.value)}
    hasError={!!errors.email}
  />
</FormGroup>
```

**Reference**: See `references/styling.md` - FormGroup Pattern
```

### Query Key Missing Dependencies
```
### React Query: Query key missing school context

**Problem**: Query key must include schoolyearId and schoolId for proper cache isolation

**Current code**:
```tsx
useQuery({
  queryKey: [STUDENTS_KEY, classId],
  queryFn: () => getStudents(classId),
});
```

**Suggested fix**:
```tsx
const { schoolyear, school } = useSchoolSchoolyear();

useQuery({
  queryKey: [schoolyear.id, school.id, STUDENTS_KEY, classId],
  queryFn: () => getStudents({ schoolyearId: schoolyear.id, schoolId: school.id, classId }),
});
```

**Reference**: See `references/react-query.md` - Query Key Structure
```

### Hardcoded String
```
### i18n: Hardcoded user-facing string

**Problem**: All user-facing text must use i18n for localization support

**Current code**:
```tsx
<Button>Delete</Button>
```

**Suggested fix**:
```tsx
const { t } = useTranslation(['common']);
<Button>{t('common:buttons.delete')}</Button>
```

**Reference**: See `references/i18n.md` - Translation Usage
```

### Using className Instead of tw
```
### Styling: Using className instead of tw macro

**Problem**: Project uses twin.macro for Tailwind, not className strings

**Current code**:
```tsx
<div className="flex items-center gap-2">
```

**Suggested fix**:
```tsx
<div tw="flex items-center gap-2">
```

**Reference**: See `references/styling.md` - twin.macro Usage
```

## When NOT to Comment

Avoid feedback on:
- Trivial formatting issues (Prettier handles this)
- Personal style preferences not in project patterns
- Nitpicks that don't affect functionality or maintainability
- Issues already addressed in other comments

## Multi-file Review Strategy

For PRs with many files:
1. Start with architecture overview (new containers, major changes)
2. Review core component/container logic first
3. Review queries and data handling
4. Review styling and i18n
5. Review tests
6. Summarize overall assessment

## After Review

If significant issues found:
- Summarize the most important themes
- Suggest whether changes are required before merge
- Offer to explain any patterns or practices in detail

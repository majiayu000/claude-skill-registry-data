---
name: ui-library-usage-auditor
description: This skill should be used when reviewing shadcn/ui component usage to ensure accessibility, consistency, and proper patterns. Applies when auditing UI code, checking component patterns, reviewing layout structure, identifying component extraction opportunities, or ensuring design system compliance. Trigger terms include audit UI, review components, check shadcn, accessibility audit, component review, UI patterns, design system compliance, layout review, refactor components, extract component.
allowed-tools: Read, Grep, Glob, Bash
---

# UI Library Usage Auditor

Review and audit shadcn/ui component usage across the codebase to ensure accessible, consistent, and maintainable UI patterns. This skill identifies issues, suggests improvements, and recommends component extractions or layout optimizations.

## When to Use This Skill

Apply this skill when:
- Auditing UI components for accessibility compliance
- Reviewing shadcn/ui usage patterns for consistency
- Identifying opportunities for component extraction
- Checking layout structure and responsive design
- Ensuring proper ARIA attributes and semantic HTML
- Finding duplicate component patterns
- Reviewing form implementations
- Checking for proper error handling in UI
- Validating design system adherence

## Audit Categories

### 1. Accessibility Audit

Check for:
- Missing ARIA labels and descriptions
- Improper heading hierarchy
- Missing alt text on images
- Insufficient color contrast
- Missing keyboard navigation support
- Form fields without labels
- Non-semantic HTML usage
- Missing focus indicators
- Improper button vs link usage
- Missing skip links for navigation

### 2. Component Consistency Audit

Check for:
- Inconsistent component variants across pages
- Mixed styling approaches (inline vs className)
- Duplicate component implementations
- Inconsistent spacing patterns
- Mixed icon libraries or icon sizes
- Inconsistent typography usage
- Non-standard button patterns
- Inconsistent error message displays
- Mixed loading state implementations

### 3. Component Extraction Opportunities

Identify:
- Repeated component patterns (3+ instances)
- Complex inline JSX that could be components
- Reusable form field groups
- Common layout patterns
- Shared modal/dialog content
- Repeated table structures
- Common card layouts
- Shared empty states
- Repeated loading skeletons

### 4. Layout and Responsiveness

Review:
- Responsive breakpoint usage
- Container max-width consistency
- Grid and flexbox usage patterns
- Mobile-first responsive design
- Overflow handling
- Scroll behavior
- Fixed positioning issues
- Z-index management

### 5. shadcn/ui Best Practices

Verify:
- Correct component imports from @/components/ui
- Proper use of composition patterns
- Correct variant prop usage
- Proper form component structure
- Correct dialog/modal patterns
- Proper toast/notification usage
- Appropriate dropdown/select usage
- Correct table implementations

## Audit Process

### Step 1: Scan Codebase for Components

Use Glob to identify all component files:

```bash
# Find all component files
Glob: **/*.tsx
Glob: app/**/*.tsx
Glob: components/**/*.tsx
```

### Step 2: Grep for Specific Patterns

Search for common patterns and potential issues:

```bash
# Find form implementations
Grep: pattern="<form" output_mode="files_with_matches"

# Find button usage
Grep: pattern="<Button" output_mode="files_with_matches"

# Find ARIA usage
Grep: pattern="aria-" output_mode="content"

# Find inline styles
Grep: pattern='style=' output_mode="files_with_matches"

# Find accessibility issues
Grep: pattern="<img" output_mode="content"  # Check for alt text
Grep: pattern="onClick.*<div" output_mode="content"  # Div as button antipattern

# Find repeated patterns
Grep: pattern="className=\".*flex.*items-center.*gap" output_mode="count"
```

### Step 3: Read and Analyze Components

Read identified files to perform detailed analysis:

```bash
Read: /path/to/component.tsx
```

Analyze for:
- Component structure and complexity
- Props interface design
- State management approach
- Event handler patterns
- Conditional rendering logic
- Accessibility attributes

### Step 4: Generate Audit Report

Create structured report with findings organized by:
- **Critical Issues**: Accessibility violations, broken patterns
- **Warnings**: Inconsistencies, suboptimal patterns
- **Suggestions**: Refactoring opportunities, extractions
- **Best Practices**: Recommendations for improvement

## Common Issues and Solutions

### Issue 1: Missing Form Labels

**Problem:**
```tsx
<Input
  type="text"
  value={name}
  onChange={(e) => setName(e.target.value)}
/>
```

**Solution:**
```tsx
<FormField
  control={form.control}
  name="name"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Name</FormLabel>
      <FormControl>
        <Input {...field} />
      </FormControl>
      <FormMessage />
    </FormItem>
  )}
/>
```

### Issue 2: Div as Button

**Problem:**
```tsx
<div onClick={handleClick} className="cursor-pointer">
  Click me
</div>
```

**Solution:**
```tsx
<Button onClick={handleClick}>
  Click me
</Button>
```

### Issue 3: Missing Image Alt Text

**Problem:**
```tsx
<img src="/avatar.jpg" className="rounded-full" />
```

**Solution:**
```tsx
<img
  src="/avatar.jpg"
  alt="User profile avatar"
  className="rounded-full"
/>
```

### Issue 4: Inconsistent Spacing

**Problem:**
```tsx
// File 1
<div className="flex gap-4">

// File 2
<div className="flex gap-2">

// File 3
<div className="flex space-x-3">
```

**Solution:**
```tsx
// Standardize spacing scale
<div className="flex gap-4">  // Use consistent gap values (2, 4, 6, 8)
```

### Issue 5: Complex Inline Component

**Problem:**
```tsx
// Repeated in multiple files
<Card>
  <CardHeader>
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-3">
        <Avatar>
          <AvatarImage src={user.avatar} />
          <AvatarFallback>{user.initials}</AvatarFallback>
        </Avatar>
        <div>
          <CardTitle>{user.name}</CardTitle>
          <CardDescription>{user.role}</CardDescription>
        </div>
      </div>
      <DropdownMenu>
        {/* Menu items */}
      </DropdownMenu>
    </div>
  </CardHeader>
</Card>
```

**Solution:**
Extract to reusable component:
```tsx
// components/UserCard.tsx
export function UserCard({ user }: UserCardProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Avatar>
              <AvatarImage src={user.avatar} alt={user.name} />
              <AvatarFallback>{user.initials}</AvatarFallback>
            </Avatar>
            <div>
              <CardTitle>{user.name}</CardTitle>
              <CardDescription>{user.role}</CardDescription>
            </div>
          </div>
          <UserMenu user={user} />
        </div>
      </CardHeader>
    </Card>
  )
}
```

### Issue 6: Improper Heading Hierarchy

**Problem:**
```tsx
<div className="page">
  <h1>Dashboard</h1>
  <div className="section">
    <h3>Recent Activity</h3>  {/* Skipped h2 */}
  </div>
</div>
```

**Solution:**
```tsx
<div className="page">
  <h1>Dashboard</h1>
  <div className="section">
    <h2>Recent Activity</h2>  {/* Proper hierarchy */}
  </div>
</div>
```

### Issue 7: Missing Loading States

**Problem:**
```tsx
<Button onClick={handleSubmit}>
  Submit
</Button>
```

**Solution:**
```tsx
<Button onClick={handleSubmit} disabled={isSubmitting}>
  {isSubmitting ? (
    <>
      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      Submitting...
    </>
  ) : (
    'Submit'
  )}
</Button>
```

### Issue 8: Inconsistent Error Display

**Problem:**
```tsx
// Mixing different error patterns
{error && <p className="text-red-500">{error}</p>}
{error && <span style={{ color: 'red' }}>{error}</span>}
{error && <Alert variant="destructive">{error}</Alert>}
```

**Solution:**
```tsx
// Standardize on Alert component
{error && (
  <Alert variant="destructive">
    <AlertCircle className="h-4 w-4" />
    <AlertDescription>{error}</AlertDescription>
  </Alert>
)}
```

## Audit Report Template

Generate audit reports using this structure:

```markdown
# UI Library Usage Audit Report

**Generated:** [Date]
**Scope:** [Files/directories audited]
**Total Components Reviewed:** [Count]

## Executive Summary

[Brief overview of findings and overall code health]

## Critical Issues (Must Fix)

### 1. Accessibility Violations

- **Issue:** Missing alt text on images
  - **Files:** `app/characters/[id]/page.tsx:45`, `components/CharacterCard.tsx:23`
  - **Fix:** Add descriptive alt attributes to all images
  - **Priority:** High

- **Issue:** Form inputs without labels
  - **Files:** `app/create-location/page.tsx:78`
  - **Fix:** Wrap inputs in FormField with FormLabel
  - **Priority:** High

### 2. Broken Patterns

- **Issue:** Divs used as buttons with onClick handlers
  - **Files:** `components/Navigation.tsx:34`, `app/timeline/page.tsx:102`
  - **Fix:** Replace with Button component
  - **Priority:** High

## Warnings (Should Fix)

### 1. Inconsistent Patterns

- **Issue:** Mixed spacing scales (gap-2, gap-3, gap-4, space-x-2)
  - **Occurrences:** 47 instances across 23 files
  - **Recommendation:** Standardize on gap-{2,4,6,8} scale
  - **Priority:** Medium

- **Issue:** Inconsistent loading states
  - **Files:** `app/characters/actions.ts`, `app/locations/actions.ts`
  - **Recommendation:** Create shared LoadingButton component
  - **Priority:** Medium

### 2. Component Duplication

- **Issue:** Character card pattern repeated 5 times
  - **Files:** Multiple files listed
  - **Recommendation:** Extract CharacterCard component
  - **Priority:** Medium

## Suggestions (Consider)

### 1. Component Extraction Opportunities

#### EntityCard Component
**Occurrences:** 8 similar patterns
**Files:**
- `app/characters/page.tsx:67-89`
- `app/locations/page.tsx:54-76`
- `app/items/page.tsx:43-65`

**Proposed Component:**
```tsx
interface EntityCardProps {
  title: string
  description: string
  image?: string
  tags?: string[]
  actions?: ReactNode
}

export function EntityCard({ ... }: EntityCardProps) {
  // Unified card implementation
}
```

#### FormSection Component
**Occurrences:** 12 similar patterns
**Recommendation:** Extract reusable form section with heading and fields

### 2. Layout Improvements

- **Issue:** Inconsistent container max-width
  - **Recommendation:** Use standard container classes
  - **Files:** Multiple page components

- **Issue:** Missing responsive breakpoints
  - **Recommendation:** Add mobile-first responsive design
  - **Files:** `app/timeline/page.tsx`, `components/WorldMap.tsx`

## shadcn/ui Best Practices

### Correct Usage [OK]

- [OK] Forms using FormField pattern (23 components)
- [OK] Proper Button variants (89 instances)
- [OK] Consistent Dialog usage (14 components)

### Needs Improvement

- Use Card composition (found 7 instances using raw divs)
- Use Table component instead of custom tables (3 instances)
- Replace custom dropdowns with DropdownMenu (4 instances)

## Accessibility Score

**Overall Score:** 72/100

- **Semantic HTML:** 85/100
- **ARIA Attributes:** 65/100
- **Keyboard Navigation:** 78/100
- **Focus Management:** 70/100
- **Color Contrast:** 88/100

## Recommendations Priority

1. **Immediate (This Week)**
   - Fix missing alt text on images
   - Add labels to all form inputs
   - Replace div buttons with Button component

2. **Short-term (This Month)**
   - Extract repeated CharacterCard pattern
   - Standardize loading state patterns
   - Standardize spacing scale

3. **Long-term (This Quarter)**
   - Implement comprehensive component library documentation
   - Create storybook for all shared components
   - Establish component extraction guidelines

## Metrics

- **Total Files Scanned:** 127
- **Components Reviewed:** 89
- **Issues Found:** 34 critical, 67 warnings, 45 suggestions
- **Average Component Complexity:** Medium
- **Code Duplication Score:** 23% (target: <15%)

## Next Steps

1. Create GitHub issues for critical accessibility violations
2. Schedule team review of component extraction opportunities
3. Update style guide with standardized patterns
4. Plan refactoring sprint for high-priority warnings
```

## Automation with Scripts

Use references/audit-checklist.md for comprehensive checklist of items to verify during audit.

## Best Practices for Auditing

1. **Start Broad, Then Focus**: Begin with file scanning, then drill into specific issues
2. **Prioritize by Impact**: Accessibility issues > Broken patterns > Inconsistencies > Optimizations
3. **Provide Context**: Include file paths, line numbers, and code snippets
4. **Suggest Solutions**: Don't just identify problems, provide concrete fixes
5. **Quantify Issues**: Use metrics to show scope and track improvement
6. **Group Related Issues**: Cluster similar problems for efficient fixing
7. **Consider User Impact**: Prioritize issues affecting end-user experience
8. **Balance Perfection vs Pragmatism**: Focus on high-value improvements

## Common Grep Patterns for Auditing

```bash
# Find potential accessibility issues
Grep: pattern="<img(?![^>]*alt=)" output_mode="files_with_matches"
Grep: pattern="onClick.*<(div|span)" output_mode="content"
Grep: pattern="<input(?![^>]*aria-label)" output_mode="content"

# Find inconsistent patterns
Grep: pattern="className=\"[^\"]*gap-[13579]" output_mode="count"
Grep: pattern="style=" output_mode="files_with_matches"

# Find component usage
Grep: pattern="from ['\"]@/components/ui" output_mode="content"
Grep: pattern="<Button" output_mode="count"
Grep: pattern="<Form" output_mode="count"

# Find potential duplications
Grep: pattern="<Card>" -A 10 output_mode="content"
Grep: pattern="className=\".*flex.*items-center.*justify-between" output_mode="count"

# Find error handling patterns
Grep: pattern="(error|Error)" output_mode="content"
Grep: pattern="toast\\." output_mode="content"

# Find loading states
Grep: pattern="(isLoading|loading|isPending)" output_mode="content"
```

## Worldbuilding App Specific Checks

### Entity Display Patterns

Check for consistent entity card layouts across:
- Character listings
- Location browsing
- Item inventories
- Faction displays
- Timeline events

### Form Patterns

Audit form consistency for:
- Character creation/editing
- Location forms
- Item/artifact forms
- Event timeline forms
- Relationship management forms

### Data Visualization

Review accessibility of:
- World maps (keyboard navigation, screen reader support)
- Timeline visualizations
- Relationship graphs
- Stat displays
- Progress indicators

## Integration with Development Workflow

Use audit findings to:
1. Create linting rules for common issues
2. Update team documentation
3. Create component templates
4. Establish PR review checklist
5. Track technical debt
6. Plan refactoring sprints
7. Improve component library

## Continuous Improvement

After implementing fixes:
1. Re-run audit to measure improvement
2. Document new patterns in style guide
3. Update component library
4. Share learnings with team
5. Adjust audit criteria based on findings
6. Schedule regular audits (monthly/quarterly)

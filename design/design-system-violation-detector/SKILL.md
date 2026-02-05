---
name: Design System Violation Detector
description: Automated detection and enforcement of design system guidelines including dark mode, colors, spacing, typography, focus states, and accessibility compliance
---

# Design System Violation Detector

Automated detection and enforcement of design system guidelines for React components in the My Prompt Manager Chrome extension.

## Purpose

Scan React components (*.tsx, *.jsx) to identify violations of the design system guidelines documented in `docs/DESIGN_GUIDELINES.md`. Ensure consistency, accessibility, and adherence to the established purple-indigo visual language across all UI components.

## When to Use This Skill

Use this skill:
- ✅ After creating or modifying any React component
- ✅ Before submitting a PR with UI changes
- ✅ When reviewing existing components for compliance
- ✅ As part of the quality workflow (alongside `npm test` and `npm run lint`)
- ✅ When onboarding new components from external sources
- ✅ During design system refactoring efforts

DO NOT use this skill for:
- ❌ Non-UI files (services, utils, hooks without JSX)
- ❌ Test files (*.test.tsx)
- ❌ Configuration files
- ❌ Content scripts without UI components

## Design System Rules

### 1. DARK MODE (CRITICAL - ERROR LEVEL)

**Rule**: Every color class must have a `dark:` variant.

**Checks:**
- `bg-*` → must have `dark:bg-*`
- `text-*` → must have `dark:text-*`
- `border-*` → must have `dark:border-*`
- `placeholder-*` → must have `dark:placeholder-*`
- `ring-*` → must have `dark:ring-*`

**Exceptions:**
- `bg-transparent`, `text-inherit`, `border-none` don't need dark variants
- Utility classes like `bg-linear-to-r` don't need dark variants
- White text on colored backgrounds: `text-white` (no dark variant needed)

**Examples:**

❌ **VIOLATION:**
```tsx
<div className="bg-white text-gray-900 border border-purple-200">
```

✅ **CORRECT:**
```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 border border-purple-200 dark:border-gray-600">
```

---

### 2. COLORS & GRADIENTS (ERROR LEVEL)

**Rule**: Use only predefined color palette, no arbitrary colors.

**Primary Actions:**
- Must use: `bg-linear-to-r from-purple-600 to-indigo-600`
- Hover: `hover:from-purple-700 hover:to-indigo-700`
- Text: `text-white` (on gradient backgrounds)

**Status Colors:**
- Success: `bg-green-600`, `text-green-600`
- Error: `bg-red-600`, `text-red-600`
- Warning: `bg-yellow-600`, `text-yellow-600`
- Info: `bg-blue-600`, `text-blue-600`

**Text Colors:**
- Primary: `text-gray-900 dark:text-gray-100`
- Secondary: `text-gray-600 dark:text-gray-400`
- Tertiary: `text-gray-500 dark:text-gray-500`

**Background Colors:**
- Page: `bg-white dark:bg-gray-900`
- Section: `bg-gray-50 dark:bg-gray-800`
- Card: `bg-white/70 dark:bg-gray-800/70` (glassmorphism)

**Border Colors:**
- Input: `border-purple-200 dark:border-gray-600`
- Divider: `border-purple-100 dark:border-gray-700`
- Error: `border-red-300 dark:border-red-500`

**Examples:**

❌ **VIOLATION:**
```tsx
<button className="bg-blue-500 text-white">Save</button>
```

✅ **CORRECT:**
```tsx
<button className="bg-linear-to-r from-purple-600 to-indigo-600 text-white">Save</button>
```

❌ **VIOLATION:**
```tsx
<div className="bg-[#f3f4f6]">
```

✅ **CORRECT:**
```tsx
<div className="bg-gray-50 dark:bg-gray-800">
```

---

### 3. BORDER RADIUS (WARNING LEVEL)

**Rule**: Use consistent border radius values.

**Standard Sizes:**
- Cards, inputs, buttons: `rounded-xl` (12px)
- Icons, small elements: `rounded-lg` (8px)
- Badges, pills: `rounded-full`

**Examples:**

⚠️ **VIOLATION:**
```tsx
<div className="bg-white border rounded-lg p-5">
```

✅ **CORRECT:**
```tsx
<div className="bg-white border rounded-xl p-5">
```

---

### 4. SPACING (WARNING LEVEL)

**Rule**: Use consistent spacing patterns.

**Standard Spacing:**
- Cards/sections: `p-5`
- Containers: `p-6`
- Button groups: `space-x-3`
- Vertical stacks: `space-y-3` or `space-y-4`
- Form fields: `gap-4`

**Examples:**

⚠️ **VIOLATION:**
```tsx
<div className="p-3 space-x-2">
```

✅ **CORRECT:**
```tsx
<div className="p-5 space-x-3">
```

---

### 5. TYPOGRAPHY (WARNING LEVEL)

**Rule**: Use consistent typography scale.

**Font Sizes:**
- Body text, buttons: `text-sm` (14px)
- Helper text, badges: `text-xs` (12px)
- Large headings: `text-lg` (18px)

**Font Weights:**
- Emphasis: `font-semibold`
- Normal: no class (default 400)
- Light: `font-light` (rare)

**Font Family:**
- Use system fonts (no custom fonts)
- Applied globally via Tailwind config

**Examples:**

⚠️ **VIOLATION:**
```tsx
<button className="text-base font-bold">Click me</button>
```

✅ **CORRECT:**
```tsx
<button className="text-sm font-semibold">Click me</button>
```

---

### 6. EFFECTS & TRANSITIONS (WARNING LEVEL)

**Rule**: Use consistent effects and transitions.

**Backdrop Blur (Glassmorphism):**
```tsx
className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm"
```

**Shadows:**
- Buttons: `shadow-lg hover:shadow-xl`
- Cards: `shadow-xs` (subtle) or none
- Modals: `shadow-xl`

**Transitions:**
- Default: `transition-all duration-200`
- Color-only: `transition-colors duration-200`

**Examples:**

⚠️ **VIOLATION:**
```tsx
<button className="bg-purple-600 hover:bg-purple-700">
```

✅ **CORRECT:**
```tsx
<button className="bg-purple-600 hover:bg-purple-700 transition-all duration-200">
```

---

### 7. FOCUS STATES (ERROR LEVEL)

**Rule**: All interactive elements must have predefined focus classes.

**Predefined Focus Classes:**
- `.focus-primary` - Primary actions (buttons)
- `.focus-secondary` - Secondary actions
- `.focus-danger` - Destructive actions
- `.focus-input` - Input fields
- `.focus-interactive` - Links, icon buttons

**DO NOT use raw Tailwind focus classes** like `focus:ring-2 focus:ring-purple-500`.

**Examples:**

❌ **VIOLATION:**
```tsx
<button className="bg-purple-600 focus:ring-2 focus:ring-purple-500">
```

✅ **CORRECT:**
```tsx
<button className="bg-purple-600 focus-primary">
```

❌ **VIOLATION:**
```tsx
<input className="border border-gray-300" />
```

✅ **CORRECT:**
```tsx
<input className="border border-purple-200 dark:border-gray-600 focus-input" />
```

---

### 8. ACCESSIBILITY (ERROR LEVEL)

**Rule**: Ensure accessibility compliance.

**Required Attributes:**
- Interactive elements need `aria-label` or visible label
- Images need `alt` attribute
- Inputs need associated `<label>` or `aria-label`
- Buttons should have descriptive text or `aria-label`
- Toggles need `role="switch"` and `aria-checked`

**Semantic HTML:**
- Use `<button>` not `<div onClick>`
- Use `<article>` for cards
- Use `<time>` for dates
- Use `<nav>` for navigation

**Color Contrast:**
- Text on background: 4.5:1 minimum (WCAG AA)
- Large text (18px+): 3:1 minimum

**Examples:**

❌ **VIOLATION:**
```tsx
<div onClick={handleClick} className="cursor-pointer">
  <svg>...</svg>
</div>
```

✅ **CORRECT:**
```tsx
<button onClick={handleClick} aria-label="Delete prompt" className="focus-interactive">
  <svg>...</svg>
</button>
```

---

### 9. COMMON COMPONENT PATTERNS (INFO LEVEL)

**Primary Button Pattern:**
```tsx
<button className="
  px-6 py-3 text-sm font-semibold text-white
  bg-linear-to-r from-purple-600 to-indigo-600
  rounded-xl hover:from-purple-700 hover:to-indigo-700
  transition-all duration-200 shadow-lg hover:shadow-xl
  disabled:opacity-50 focus-primary
">
  {text}
</button>
```

**Text Input Pattern:**
```tsx
<input className="
  w-full px-4 py-3
  border border-purple-200 dark:border-gray-600
  rounded-xl focus-input
  bg-white/60 dark:bg-gray-700/60 backdrop-blur-sm
  transition-all duration-200
  text-gray-900 dark:text-gray-100
  placeholder-gray-500 dark:placeholder-gray-400
" />
```

**Card Container Pattern:**
```tsx
<article className="
  bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm
  border-b border-purple-100 dark:border-gray-700
  p-5 hover:bg-white/90 dark:hover:bg-gray-800/90
  transition-all duration-200
">
  {content}
</article>
```

**Icon Button Pattern:**
```tsx
<button className="
  p-2 text-gray-400 dark:text-gray-500
  hover:text-purple-600 dark:hover:text-purple-400
  rounded-lg hover:bg-purple-50 dark:hover:bg-purple-900/20
  transition-colors focus-interactive
" aria-label="Action description">
  <svg>...</svg>
</button>
```

---

## Execution Workflow

### Phase 1: File Discovery
1. Use Glob to find all React component files:
   ```
   src/components/**/*.tsx
   src/components/**/*.jsx
   ```
2. Exclude test files: `**/*.test.tsx`, `**/__tests__/**`
3. If user specifies files, only check those

### Phase 2: Component Analysis
For each file:
1. **Read file** using Read tool
2. **Extract className strings** from JSX
3. **Parse Tailwind classes** (split by whitespace)
4. **Run violation checks** (see checklist below)
5. **Collect violations** with metadata:
   - File path
   - Line number (if determinable)
   - Severity (ERROR/WARNING/INFO)
   - Rule violated
   - Current code snippet
   - Suggested fix
   - Documentation reference

### Phase 3: Violation Detection Checklist

Run these checks in order:

#### 🔴 CRITICAL CHECKS (ERROR - Must Fix)

1. **Dark Mode Variants Missing**
   - Scan for: `bg-white`, `bg-gray-*`, `text-gray-*`, `border-gray-*`, `border-purple-*`
   - Check: Does corresponding `dark:*` variant exist?
   - Exception: `bg-transparent`, `text-white`, `border-none`

2. **Focus States Missing**
   - Scan for: `<button`, `<input`, `<a`, `role="button"`
   - Check: Does it have a `.focus-*` class?
   - Required: `.focus-primary`, `.focus-input`, `.focus-interactive`, etc.

3. **Arbitrary Colors Used**
   - Scan for: `bg-[#`, `text-[#`, `border-[#`, hex color patterns
   - Flag: All arbitrary color values
   - Suggest: Use Tailwind theme colors

4. **Accessibility Violations**
   - Scan for: `<button>` without text/aria-label
   - Scan for: `<img>` without alt
   - Scan for: `<input>` without label/aria-label
   - Scan for: Interactive divs (`onClick` on `<div>`)
   - Scan for: Missing `role="switch"` on toggles

#### ⚠️ WARNING CHECKS (Should Fix)

5. **Border Radius Inconsistencies**
   - Scan for: `rounded-md`, `rounded-lg` on cards/inputs/buttons (Note: `rounded-xs` doesn't exist in Tailwind v4 - use `rounded-sm` for small radii)
   - Suggest: Use `rounded-xl` for standard components, `rounded-sm` for small UI elements

6. **Spacing Inconsistencies**
   - Scan for: `p-3`, `p-4`, `p-7` on cards
   - Suggest: Use `p-5` (cards) or `p-6` (containers)

7. **Typography Violations**
   - Scan for: `text-base`, `text-md`, `font-bold` on buttons/body text
   - Suggest: Use `text-sm` (body) and `font-semibold` (emphasis)

8. **Missing Transitions**
   - Scan for: Interactive elements with hover but no transition
   - Suggest: Add `transition-all duration-200`

9. **Shadow Misuse**
   - Scan for: Non-standard shadow classes
   - Suggest: `shadow-lg hover:shadow-xl` (buttons), `shadow-xs` (cards)

#### ℹ️ INFO CHECKS (Consider)

10. **Pattern Optimization**
    - Detect: Components that could use common patterns
    - Suggest: Refactor to match established patterns

11. **Glassmorphism Pattern**
    - Scan for: `bg-white/` without `backdrop-blur-sm`
    - Suggest: Add backdrop blur for glassmorphism effect

### Phase 4: Report Generation

Generate a structured report:

```
═══════════════════════════════════════════════════════════
DESIGN SYSTEM VIOLATION REPORT
═══════════════════════════════════════════════════════════

Files Checked: 42
Components Analyzed: 45

SUMMARY:
  🔴 ERRORS:   12 (Must fix)
  ⚠️  WARNINGS: 8  (Should fix)
  ℹ️  INFO:     3  (Consider)

═══════════════════════════════════════════════════════════
ERRORS (Must Fix)
═══════════════════════════════════════════════════════════

1. Missing Dark Mode Variant
   File: src/components/PromptCard.tsx:45

   Current:
   <div className="bg-white border border-purple-200">

   Problem: Missing dark mode variants for background and border

   Fix:
   <div className="bg-white dark:bg-gray-800 border border-purple-200 dark:border-gray-700">

   Docs: docs/DESIGN_GUIDELINES.md#dark-mode

   ─────────────────────────────────────────────────────────

2. Missing Focus State
   File: src/components/Button.tsx:23

   Current:
   <button className="bg-purple-600 rounded-xl">

   Problem: Interactive element missing focus state

   Fix:
   <button className="bg-purple-600 rounded-xl focus-primary">

   Docs: docs/DESIGN_GUIDELINES.md#focus-states

   ─────────────────────────────────────────────────────────

═══════════════════════════════════════════════════════════
WARNINGS (Should Fix)
═══════════════════════════════════════════════════════════

[Similar format for warnings...]

═══════════════════════════════════════════════════════════
INFO (Consider)
═══════════════════════════════════════════════════════════

[Similar format for info...]

═══════════════════════════════════════════════════════════
RECOMMENDATIONS
═══════════════════════════════════════════════════════════

Priority Actions:
1. Fix all 12 ERRORS before PR submission
2. Address 8 WARNINGS for consistency
3. Review 3 INFO suggestions for optimization

Next Steps:
- Run this check again after fixes: [command to re-run]
- Review design guidelines: docs/DESIGN_GUIDELINES.md
- Check existing components for patterns: src/components/

Quality Gate: ❌ FAILED (12 errors must be fixed)
```

### Phase 5: Auto-Fix Suggestions (Optional)

For certain violations, offer to auto-fix:

**Safe Auto-Fixes:**
1. Add missing `dark:` variants (follow standard patterns)
2. Replace `rounded-lg` → `rounded-xl` on cards/buttons
3. Add `transition-all duration-200` to interactive elements
4. Replace raw focus classes with predefined `.focus-*`

**Manual Review Required:**
- Color scheme changes (affects branding)
- Layout restructuring (affects functionality)
- Accessibility fixes (need context)

**Auto-Fix Workflow:**
```
1. Ask user: "Found 8 auto-fixable violations. Apply fixes? (y/n)"
2. If yes:
   - Use Edit tool for each fix
   - Show diff of changes
   - Re-run checks to verify fixes
3. If no:
   - Provide manual fix instructions
```

---

## Integration with Existing Workflow

### 1. Manual Check Command

Add to `package.json`:
```json
{
  "scripts": {
    "check-design": "echo 'Run Claude Code skill: design-violation-detector'"
  }
}
```

### 2. Quality Gate Integration

Update quality workflow:
```bash
# Mandatory checks before commit
npm test                    # ✓ Existing
npm run lint               # ✓ Existing
# Run design check manually via Claude Code skill
```

### 3. Pre-PR Checklist

Before submitting PR with UI changes:
- [ ] `npm test` passes
- [ ] `npm run lint` passes
- [ ] Design violation check passes (0 errors)
- [ ] Warnings addressed or documented
- [ ] Accessibility verified

---

## Usage Examples

### Example 1: Check Single Component

**User Request:**
> "Check PromptCard.tsx for design violations"

**Skill Actions:**
1. Read `src/components/PromptCard.tsx`
2. Extract and analyze className strings
3. Run all violation checks
4. Generate focused report for this file
5. Suggest fixes with code snippets

### Example 2: Check All Components

**User Request:**
> "Scan all components for design violations"

**Skill Actions:**
1. Glob `src/components/**/*.tsx`
2. Exclude test files
3. Analyze each component (42 files)
4. Generate comprehensive report
5. Sort by severity (errors first)
6. Provide summary statistics

### Example 3: Check Modified Components

**User Request:**
> "Check design system compliance for components I just changed"

**Skill Actions:**
1. Run `git diff --name-only` to find modified files
2. Filter for `src/components/**/*.tsx`
3. Analyze only changed components
4. Generate targeted report
5. Suggest fixes for new violations

### Example 4: Auto-Fix Mode

**User Request:**
> "Check and fix design violations in Button.tsx"

**Skill Actions:**
1. Analyze Button.tsx
2. Identify violations
3. Separate auto-fixable vs manual
4. Ask user for permission to auto-fix
5. Apply fixes using Edit tool
6. Re-run check to verify
7. Report remaining manual fixes needed

---

## Common Violation Patterns & Fixes

### Pattern 1: New Component Without Dark Mode

**Before:**
```tsx
const MyComponent = () => (
  <div className="bg-white border border-gray-200 text-gray-900">
    <h2 className="text-lg font-bold">Title</h2>
    <p className="text-gray-600">Description</p>
  </div>
);
```

**After:**
```tsx
const MyComponent = () => (
  <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100">
    <h2 className="text-lg font-bold">Title</h2>
    <p className="text-gray-600 dark:text-gray-400">Description</p>
  </div>
);
```

### Pattern 2: Button Without Focus State

**Before:**
```tsx
<button className="px-6 py-3 bg-purple-600 text-white rounded-xl hover:bg-purple-700">
  Save
</button>
```

**After:**
```tsx
<button className="px-6 py-3 bg-purple-600 text-white rounded-xl hover:bg-purple-700 transition-all duration-200 focus-primary">
  Save
</button>
```

### Pattern 3: Arbitrary Colors

**Before:**
```tsx
<div className="bg-[#f3f4f6] text-[#1a202c] border-[#e5e7eb]">
```

**After:**
```tsx
<div className="bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 border-gray-200 dark:border-gray-700">
```

### Pattern 4: Div with onClick

**Before:**
```tsx
<div onClick={handleClick} className="cursor-pointer">
  <TrashIcon />
</div>
```

**After:**
```tsx
<button onClick={handleClick} aria-label="Delete item" className="focus-interactive">
  <TrashIcon />
</button>
```

---

## Output Format

Always structure output as:

1. **Summary Statistics**
   - Files checked
   - Total violations by severity
   - Quality gate status (PASS/FAIL)

2. **Critical Errors** (if any)
   - File path and line number
   - Current code
   - Problem description
   - Suggested fix
   - Documentation reference

3. **Warnings** (if any)
   - Same format as errors

4. **Info** (if any)
   - Same format as errors

5. **Recommendations**
   - Priority actions
   - Next steps
   - Links to documentation

6. **Auto-Fix Options** (if applicable)
   - List of auto-fixable violations
   - Ask for permission to apply fixes

---

## Success Criteria

The skill is successful when:
1. ✅ All design violations are identified
2. ✅ Specific fixes are provided with code snippets
3. ✅ Violations are categorized by severity
4. ✅ Documentation references are included
5. ✅ Report is actionable (developer knows exactly what to fix)
6. ✅ Quality gate status is clear (PASS/FAIL)

---

## Limitations & Caveats

1. **Dynamic ClassNames**: Cannot analyze runtime-generated classes
   ```tsx
   // Cannot analyze
   <div className={`bg-${color}-500`}>
   ```

2. **Component Libraries**: External component libraries (if added) may have their own patterns

3. **Inline Styles**: While flagged, inline styles might be necessary for dynamic values

4. **Context Required**: Some violations need human judgment (e.g., when arbitrary values are justified)

5. **False Positives**: Edge cases may trigger false alarms (user should verify)

---

## References

- **Design Guidelines**: `/Users/e0538224/Developer/My-Prompt-Manager/docs/DESIGN_GUIDELINES.md`
- **Component Catalog**: `/Users/e0538224/Developer/My-Prompt-Manager/docs/COMPONENTS.md`
- **Existing Components**: `/Users/e0538224/Developer/My-Prompt-Manager/src/components/`
- **Tailwind Config**: `/Users/e0538224/Developer/My-Prompt-Manager/tailwind.config.js`

---

## Implementation Notes

**Tools Used:**
- `Glob`: Find component files
- `Read`: Read component source
- `Grep`: Search for specific patterns (optional optimization)
- `Edit`: Apply auto-fixes (if user approves)

**Performance:**
- Check ~40 components in < 30 seconds
- Provide incremental feedback for large batches
- Cache results for re-checks

**Testing:**
- Test on known good components (PromptCard, AddPromptForm)
- Test on known violations (create test files)
- Verify auto-fix doesn't break components

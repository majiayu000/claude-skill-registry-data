---
name: audit-experience
description: Audit the course learn experience for section coverage, sidebar rendering, layout, design token compliance, tenant isolation, accessibility, data flow, and component quality. Use when reviewing course UI code quality or diagnosing learn experience issues. Pass a course slug or "all".
disable-model-invocation: true
---

Audit the course learn experience: $ARGUMENTS

$ARGUMENTS should be a course slug or "all" for the full learn system. If empty, audit the shared learn infrastructure.

## Before Starting

1. Read `{{COURSE_SECTIONS_DIR}}/SectionContent.tsx` — the section router
2. Read `src/lib/config/lesson-types.ts` — canonical types, labels, icons
3. Read `{{SCHEMAS_DIR}}/course-learn.ts` — SECTION_TYPES
4. Read `{{COURSE_COMPONENTS_DIR}}/learn/CourseLearnLayout.tsx` — layout structure
5. Read `{{COURSE_COMPONENTS_DIR}}/learn/CourseLearnSidebar.tsx` — sidebar
6. Read `{{COURSE_COMPONENTS_DIR}}/learn/LessonPanel.tsx` — lesson wrapper
7. Read `{{COURSE_COMPONENTS_DIR}}/learn/LessonContent.tsx` — content dispatcher

## Audit Checks

### 1. SECTION COMPONENT COVERAGE

For every type in SECTION_TYPES, verify a component exists:

- [ ] Grep `SectionContent.tsx` for each section_type case
- [ ] Verify the import exists and the component file is present
- [ ] Check the fallback case (should be ReadingSection)
- [ ] Flag any SECTION_TYPES that have no dedicated component

If auditing a specific course, also check:
- [ ] All section_types used in the course data have matching components
- [ ] No unknown types in the course data

### 2. SIDEBAR RENDERING

- [ ] All lesson types have entries in LESSON_TYPE_LABELS (no raw keys shown)
- [ ] All lesson types have entries in LESSON_TYPE_ICONS (no missing icons)
- [ ] Week grouping renders correctly (weeks numbered 1-8)
- [ ] Section count per week is displayed
- [ ] Progress indicators work (completed badge, percentage)
- [ ] Active section is highlighted
- [ ] Mobile drawer opens/closes correctly (check responsive logic)

### 3. LEARN LAYOUT

- [ ] Desktop: Sidebar (280px) + flex-1 main content
- [ ] Mobile: Drawer sidebar with backdrop
- [ ] Sticky sidebar with correct height calc (`calc(100vh - var(--header-height))`)
- [ ] Content max-width: `max-w-[var(--measure,65ch)]`
- [ ] Prev/next navigation works across week boundaries
- [ ] URL deep linking: `?week=N&section=slug` params handled
- [ ] Keyboard: Escape closes mobile sidebar

### 4. DESIGN TOKEN COMPLIANCE

Scan all course components for violations:

- [ ] No hardcoded colors (`bg-blue-*`, `text-gray-*`, hex values, rgb())
- [ ] All colors use semantic tokens (`bg-primary`, `text-muted-foreground`, `border-border`)
- [ ] No hardcoded font sizes (use Tailwind scale)
- [ ] No hardcoded spacing (use Tailwind/CSS variable scale)
- [ ] `course-content-html` class used on all dangerouslySetInnerHTML containers
- [ ] Dark mode works (no light-only styles)

Search patterns:
```
# Hardcoded colors (should find zero)
grep -r "bg-\(red\|blue\|green\|yellow\|gray\|slate\|zinc\|neutral\|stone\)" {{COURSE_COMPONENTS_DIR}}/
grep -r "#[0-9a-fA-F]\{3,6\}" {{COURSE_COMPONENTS_DIR}}/
grep -r "rgb\|rgba" {{COURSE_COMPONENTS_DIR}}/
```

### 5. TENANT ISOLATION

- [ ] No hardcoded tenant-specific strings in course components
- [ ] Course titles/descriptions come from data, not hardcoded
- [ ] Feature flags checked where applicable (e.g., `brand.features.chat` for Formation Companion)
- [ ] Uses `brandConfig` or `useBrand()` for any tenant-varying text

### 6. ACCESSIBILITY

- [ ] All interactive elements have visible focus states
- [ ] ARIA labels on icon-only buttons (sidebar collapse, prev/next)
- [ ] Heading hierarchy: H1 (course title) → H2 (section title) → H3+ (content headings)
- [ ] Tab order is logical (sidebar → main content → navigation)
- [ ] Screen reader: section type announced (via labels, not just icons)
- [ ] Tap targets minimum 44x44px (sidebar items, navigation buttons)
- [ ] `prefers-reduced-motion` respected on any animations
- [ ] Video sections: captions/transcript available (or flagged as needed)

### 7. DATA FLOW & HOOKS

- [ ] No raw `fetch()` calls — all data via React Query hooks
- [ ] Error states handled (course not found, section not found)
- [ ] Loading states shown (skeleton or spinner)
- [ ] Empty states handled (no sections in a week, no content in a section)
- [ ] Progress mutations use optimistic updates (or at minimum, invalidate correctly)

### 8. SECTION COMPONENT QUALITY (spot check 3-4 sections)

For each section component checked:
- [ ] Props: `{ section: CourseSection }` — correct type
- [ ] HTML content: rendered via `dangerouslySetInnerHTML` with `course-content-html` class
- [ ] Child items: maps reflection_questions/discussion_prompts/exercises arrays correctly
- [ ] Local state: managed with useState, not leaking to parent
- [ ] shadcn/ui: uses Card, Button, Textarea etc. — not raw HTML
- [ ] No console.log or debug code

## Output Format

```
## Course Learn Audit: [slug or "Infrastructure"]

### Overall: X/8 checks passing

### 1. Section Coverage: ✅/❌
- Covered: [N] / [total SECTION_TYPES]
- Missing components: [list]
- Unused components: [list]

### 2. Sidebar: ✅/❌
- [details]

### 3. Layout: ✅/❌
- [details]

### 4. Design Tokens: ✅/❌
- Violations found: [N]
- [file:line — violation description]

### 5. Tenant Isolation: ✅/❌
- [details]

### 6. Accessibility: ✅/❌
- [details]

### 7. Data Flow: ✅/❌
- [details]

### 8. Component Quality: ✅/❌
- Spot-checked: [component names]
- [details]

### Priority Fixes
1. [HIGH] — [description] — [file:line]
2. [MEDIUM] — [description] — [file:line]
3. [LOW] — [description] — [file:line]
```

## Rules

- 8 weeks, numbered 1-8. No Week 0.
- Read actual code — don't assume based on file names
- Use Grep and Glob for systematic scans, not manual file-by-file
- Be specific: report file paths and line numbers for every issue
- Distinguish between issues in shared infrastructure vs. course-specific content
- This audit is about the learn experience UX/code quality — for Charter/content validation use `/course-validate`

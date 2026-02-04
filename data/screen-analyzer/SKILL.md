---
name: Screen Analyzer
description: Comprehensive React Native screen analysis tool that systematically extracts every feature, component, interaction, and detail from existing screens. Use BEFORE recreating ANY screen to ensure 100% feature parity. Triggers when user says "analyze screen", "analyze [filename]", "extract features from", or before screen recreation.
allowed-tools: Read, Grep, Glob, Bash
---

# Screen Analysis Skill - Complete Feature Extraction

You are a specialized screen analysis assistant that systematically analyzes React Native screens to extract EVERY feature, section, component, and detail without missing anything. This skill is used BEFORE recreating a screen to ensure 100% feature parity.

## 🎯 PURPOSE

**Goal:** Analyze an old/existing screen file and create a comprehensive feature inventory that captures:
- Every UI section and component
- All data sources and API calls
- Complete navigation flows
- Props, params, and state management
- Dependencies and imports
- Styling patterns
- Business logic and calculations
- User interactions and events
- Edge cases and conditional rendering

**Use Case:** Before recreating a screen, use this skill to ensure you don't miss any functionality.

---

## 📋 ANALYSIS WORKFLOW

### Step 1: File Identification

Ask the user:
1. **Screen to analyze** - Full file path or screen name
2. **Purpose** - Why are you analyzing this? (recreation, enhancement, documentation)
3. **Focus areas** - Any specific features to pay extra attention to?

If user provides a screen name without path, search for it:
```bash
# Search for the file
find /c/PC/OLD -name "*ScreenName*.tsx" -o -name "*ScreenName*.ts"
```

### Step 2: Read Complete File

Read the ENTIRE file - don't skip any lines:
```typescript
Read(file_path)  // No offset/limit - read everything
```

### Step 3: Systematic Analysis

Go through the file section by section using this checklist:

---

## 🔍 COMPREHENSIVE ANALYSIS CHECKLIST

### A. FILE METADATA
- [ ] File path and name
- [ ] File size (lines of code)
- [ ] Last modified date (if available)
- [ ] Component name
- [ ] Component type (Screen, Component, Hook, etc.)

### B. IMPORTS ANALYSIS
Extract ALL imports with categories:

```typescript
// External Libraries
import React from 'react';
import { View } from 'react-native';

// Navigation
import { useNavigation } from '@react-navigation/native';

// Data Fetching
import { useQuery } from '@tanstack/react-query';

// Database
import { supabase } from '../../lib/supabase';

// UI Components
import { Card, Button } from '../../ui';

// Utils
import { formatDate } from '../../utils/dateUtils';

// Types
import type { ParentStackParamList } from '../../types/navigation';
```

**Document:**
1. Count of imports by category
2. External vs internal dependencies
3. Unused imports (if obvious)
4. Missing imports (if any compilation errors)

---

### C. TYPESCRIPT TYPES ANALYSIS
Extract ALL type definitions:

```typescript
// Props interface
interface Props {
  // Document each prop with purpose
}

// Data interfaces
interface Student {
  // Document structure
}

// Enums and unions
type Status = 'active' | 'inactive';
```

**Document:**
1. Props interface - every property
2. State types
3. Data model interfaces
4. Enum/union types
5. Generic types used

---

### D. COMPONENT PROPS & PARAMS
Extract route params and props:

```typescript
const { childId, childName, mode } = route.params;
```

**Document:**
1. All route params (required vs optional)
2. Default values
3. Validation logic
4. Type safety measures

---

### E. STATE MANAGEMENT
Identify ALL state:

```typescript
// Local state
const [filter, setFilter] = useState('all');
const [expanded, setExpanded] = useState(null);

// Derived state (useMemo)
const filteredData = useMemo(() => { ... }, [deps]);

// Refs
const scrollRef = useRef(null);

// Context
const { theme } = useTheme();
```

**Document:**
1. All useState calls with initial values
2. All useMemo with dependencies
3. All useRef usage
4. All useContext usage
5. State update patterns

---

### F. DATA FETCHING ANALYSIS
Identify ALL data sources:

```typescript
// TanStack Query
const { data, isLoading, error } = useQuery({
  queryKey: ['students', parentId],
  queryFn: async () => { ... }
});

// Supabase queries
const { data } = await supabase
  .from('students')
  .select('*')
  .eq('parent_id', parentId);

// API calls
fetch('/api/students');

// Mock data (if any)
const mockData = [...];
```

**Document:**
1. Query keys used
2. Tables queried
3. Filters applied (.eq, .in, .filter)
4. Joins used (.select with foreign keys)
5. Ordering and pagination
6. Cache configuration (staleTime, cacheTime)
7. Error handling
8. Loading states
9. **⚠️ Any mock/hardcoded data**

---

### G. COMPUTED VALUES & CALCULATIONS
Identify ALL business logic:

```typescript
// Stats calculations
const stats = useMemo(() => {
  const total = data.length;
  const average = data.reduce(...) / total;
  return { total, average };
}, [data]);

// Percentage calculations
const percentage = (completed / total) * 100;

// Date calculations
const daysRemaining = targetDate - today;

// Sorting/filtering logic
const sortedData = data.sort((a, b) => ...);
```

**Document:**
1. All useMemo computations
2. Mathematical formulas
3. Aggregations (sum, average, count)
4. Sorting algorithms
5. Filtering logic
6. Date/time calculations
7. String formatting
8. Number formatting

---

### H. UI SECTIONS INVENTORY
Map out EVERY visual section in render order:

```markdown
## Screen Layout Structure

1. **Header Section**
   - Title: "Student Details"
   - Subtitle: Student name
   - Action buttons: Edit, Share

2. **Stats Summary Card**
   - Total students: Number display
   - Average grade: Percentage with color
   - Attendance: Percentage with icon

3. **Filter Bar**
   - Dropdown: Subject filter
   - Buttons: All | Math | Science | English
   - Search: Text input with icon

4. **Main Content List**
   - Card per student
   - Student name, grade, attendance
   - Progress bar
   - Status badge

5. **Footer Actions**
   - Button: Add Student
   - Button: Export Report
```

**For EACH section document:**
- Component used (Card, View, ScrollView)
- Props passed
- Styling (variant, colors, spacing)
- Conditional rendering (if any)
- Data displayed
- Actions available

---

### I. COMPONENTS USED
List ALL UI components with usage:

```markdown
## Components Inventory

### From UI Library
1. **Card** (variant="elevated")
   - Used in: Header, Stats, Student List
   - Props: variant, onPress, style
   - Count: 12 instances

2. **Button** (variant="primary")
   - Used in: Filter bar, Actions
   - Props: variant, onPress, disabled
   - Count: 8 instances

3. **Badge** (variant="info")
   - Used in: Status indicators
   - Props: variant, label
   - Count: 15 instances

### Custom Components
1. **ProgressBar**
   - Props: progress, color
   - Used for: Grade visualization

2. **StudentCard**
   - Props: student, onPress
   - Used for: Student list items
```

---

### J. NAVIGATION ANALYSIS
Extract ALL navigation patterns:

```typescript
// Screen entry tracking
useEffect(() => {
  trackScreenView('StudentList', { from: 'Dashboard' });
}, []);

// Navigation calls
navigation.navigate('StudentDetail', { id });
safeNavigate('StudentDetail', { id, name });

// Back navigation
navigation.goBack();

// Tab switching
navigation.navigate('Reports', { screen: 'Overview' });

// Deep linking
Linking.openURL('app://student/123');
```

**Document:**
1. How user arrives at this screen
2. All screens navigated TO from this screen
3. Parameters passed during navigation
4. Navigation guards or validation
5. Back button behavior
6. Deep linking support

---

### K. USER INTERACTIONS
Identify ALL interactive elements:

```typescript
// Button presses
<Button onPress={() => handleAction()} />

// Card taps
<Card onPress={() => navigateTo()} />

// Input changes
<TextInput onChangeText={setText} />

// Gestures
<Swipeable onSwipeLeft={handleDelete} />

// Pull to refresh
<ScrollView refreshControl={<RefreshControl onRefresh={refetch} />} />

// Long press
<Pressable onLongPress={showOptions} />

// Double tap
<TapGestureHandler numberOfTaps={2} />
```

**Document:**
1. All onPress handlers
2. All form inputs
3. Gesture handlers
4. Refresh mechanisms
5. Scroll behaviors
6. Modal triggers
7. Menu actions

---

### L. CONDITIONAL RENDERING
Extract ALL conditional logic:

```typescript
// Simple conditions
{isLoading && <LoadingSpinner />}
{error && <ErrorMessage />}
{data.length === 0 && <EmptyState />}

// Complex conditions
{status === 'active' ? <ActiveBadge /> : <InactiveBadge />}

// Multiple conditions
{isAdmin && hasPermission && !isDisabled && <AdminPanel />}

// Conditional styling
style={[styles.card, isSelected && styles.selected]}

// Conditional props
<Button disabled={!canSubmit} />
```

**Document:**
1. All conditional UI elements
2. Conditions checked
3. Alternative UI paths
4. Edge cases handled
5. Error boundaries
6. Loading states
7. Empty states
8. Permission checks

---

### M. STYLING ANALYSIS
Extract styling patterns:

```typescript
// StyleSheet definitions
const styles = StyleSheet.create({
  container: { ... },
  card: { ... },
});

// Inline styles
style={{ padding: Spacing.md }}

// Dynamic styles
style={[styles.base, isActive && styles.active]}

// Theme usage
backgroundColor: theme.colors.primary
color: Colors.textPrimary

// Design system
sx={{ p: 'md', mt: 'lg' }}
```

**Document:**
1. StyleSheet styles with properties
2. Inline styles
3. Dynamic/conditional styles
4. Theme values used
5. Colors used
6. Spacing values
7. Typography variants
8. Layout patterns (flex, grid)

---

### N. SIDE EFFECTS (useEffect)
Document ALL useEffect hooks:

```typescript
useEffect(() => {
  // What it does
  trackScreenView('ScreenName');
}, []); // When it runs (dependencies)

useEffect(() => {
  // Fetch data when ID changes
  fetchData(childId);
}, [childId]);

useEffect(() => {
  // Cleanup subscription
  return () => unsubscribe();
}, []);
```

**Document:**
1. Purpose of each useEffect
2. Dependencies
3. Cleanup functions
4. Execution timing
5. Side effects triggered

---

### O. PERFORMANCE OPTIMIZATIONS
Identify optimization techniques:

```typescript
// Memoization
const expensiveCalculation = useMemo(() => { ... }, [deps]);

// Component memoization
const MemoizedComponent = React.memo(Component);

// Callback memoization
const handlePress = useCallback(() => { ... }, [deps]);

// List optimization
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  getItemLayout={...}
  removeClippedSubviews
  maxToRenderPerBatch={10}
/>
```

**Document:**
1. useMemo usage and dependencies
2. React.memo components
3. useCallback usage
4. FlatList optimizations
5. Image optimization
6. Virtualization
7. Lazy loading

---

### P. ERROR HANDLING
Extract error handling patterns:

```typescript
// Try-catch blocks
try {
  await fetchData();
} catch (error) {
  console.error(error);
  setError(error.message);
}

// Error boundaries
<ErrorBoundary>
  <Component />
</ErrorBoundary>

// Query error handling
const { error } = useQuery({
  onError: (error) => { ... }
});

// Validation
if (!childId) {
  console.warn('Missing childId');
  return <ErrorScreen />;
}
```

**Document:**
1. Try-catch usage
2. Error boundaries
3. Query error handling
4. Validation checks
5. Fallback UI
6. Error messages shown
7. Recovery mechanisms

---

### Q. ANALYTICS & TRACKING
Extract ALL tracking calls:

```typescript
// Screen views
trackScreenView('StudentList', { from: 'Dashboard' });

// Actions
trackAction('view_student', 'StudentList', { studentId });

// Events
trackEvent('filter_changed', { filter: 'math' });

// Custom tracking
logCustomEvent('download_report', { format: 'pdf' });
```

**Document:**
1. All trackScreenView calls
2. All trackAction calls
3. All trackEvent calls
4. Parameters tracked
5. Timing of tracking calls

---

### R. ACCESSIBILITY
Check accessibility features:

```typescript
// Labels
<Button accessibilityLabel="Close dialog" />

// Hints
accessibilityHint="Double tap to open details"

// Roles
accessibilityRole="button"

// States
accessibilityState={{ selected: isSelected }}

// Live regions
accessibilityLiveRegion="polite"
```

**Document:**
1. Accessibility labels
2. Accessibility hints
3. Roles defined
4. States managed
5. Screen reader support
6. Keyboard navigation

---

### S. COMMENTS & DOCUMENTATION
Extract inline documentation:

```typescript
// JSDoc comments
/**
 * Calculates the student's average grade
 * @param grades - Array of grade objects
 * @returns Average as percentage
 */

// Inline comments
// TODO: Add pagination
// FIXME: Handle null case
// NOTE: This is temporary
```

**Document:**
1. JSDoc documentation
2. TODO comments (missing features)
3. FIXME comments (known issues)
4. NOTE/IMPORTANT comments
5. Commented-out code (why?)

---

## 📊 OUTPUT FORMAT

After completing analysis, provide a structured report:

```markdown
# Screen Analysis Report: [ScreenName]

**File:** `path/to/ScreenName.tsx`
**Lines:** 450
**Analysis Date:** [Date]

---

## 🎯 EXECUTIVE SUMMARY

**Purpose:** [1-2 sentence description]

**Complexity Level:** ⭐⭐⭐ (Medium)
- Data sources: 3
- UI sections: 8
- User interactions: 12
- Business logic: 5 calculations

**Key Features:**
1. [Main feature 1]
2. [Main feature 2]
3. [Main feature 3]

**⚠️ Critical Findings:**
- [Any mock data found]
- [Performance issues noticed]
- [Missing error handling]
- [Accessibility gaps]

---

## 📦 IMPORTS & DEPENDENCIES

### External Libraries (count)
- react (useState, useEffect, useMemo)
- react-native (View, Text, ScrollView)
- @react-navigation/native (useNavigation)
- @tanstack/react-query (useQuery)

### Internal Dependencies (count)
- UI Components: Card, Button, Badge (from ../../ui)
- Utils: formatDate, safeNavigate (from ../../utils)
- Services: supabase (from ../../lib)
- Types: ParentStackParamList (from ../../types)

### Unused Imports
- [List any unused imports]

---

## 🎨 UI STRUCTURE (Top to Bottom)

### Section 1: Header
**Component:** Card (variant="elevated")
**Content:**
- Title: "Student Progress"
- Subtitle: {childName}
- Action: <IconButton icon="share" onPress={handleShare} />

**Styling:**
- padding: Spacing.md
- backgroundColor: Colors.surface
- elevation: 2

**Conditional:**
- Shows only if `hasData === true`

---

### Section 2: Stats Summary
**Component:** Row with 3 stat boxes
**Content:**
- Box 1: Total Students (count)
- Box 2: Average Grade (percentage)
- Box 3: Attendance (percentage)

**Data Source:** `stats` useMemo calculation
**Formula:**
```typescript
const stats = useMemo(() => {
  const total = students.length;
  const avgGrade = students.reduce((sum, s) => sum + s.grade, 0) / total;
  const attendance = students.reduce((sum, s) => sum + s.attendance, 0) / total;
  return { total, avgGrade, attendance };
}, [students]);
```

---

[Continue for ALL sections...]

---

## 💾 DATA FETCHING

### Query 1: Students List
**Query Key:** `['students', parentId]`
**Table:** `students`
**Select:** `*, grades!inner(*)`
**Filters:**
- `.eq('parent_id', parentId)`
- `.order('created_at', { ascending: false })`

**Cache:** 5 minutes (staleTime: 300000)

**Error Handling:** ✅ Shows error message
**Loading State:** ✅ Shows skeleton loader
**Empty State:** ✅ Shows "No students found"

---

### Query 2: [Additional queries...]

---

## 🧮 CALCULATIONS & BUSINESS LOGIC

### 1. Average Grade Calculation
**Location:** Line 125
**Purpose:** Calculate overall average from all subjects
**Formula:**
```typescript
const averageGrade = useMemo(() => {
  const totalGrades = grades.reduce((sum, g) => sum + g.score, 0);
  return totalGrades / grades.length;
}, [grades]);
```
**Dependencies:** grades array
**Edge Cases:** Returns 0 if grades.length === 0

---

### 2. [Additional calculations...]

---

## 🔄 STATE MANAGEMENT

### Local State
1. **filter** (string, default: 'all')
   - Purpose: Filter students by category
   - Updated by: Filter button presses
   - Used in: filteredStudents useMemo

2. **expandedId** (string | null, default: null)
   - Purpose: Track which card is expanded
   - Updated by: Card press
   - Used in: Conditional rendering of details

---

### Derived State (useMemo)
1. **filteredStudents**
   - Dependencies: [students, filter]
   - Logic: Filter students array by category
   - Performance: ✅ Memoized

2. **stats**
   - Dependencies: [students]
   - Logic: Calculate aggregate statistics
   - Performance: ✅ Memoized

---

## 🧭 NAVIGATION FLOWS

### Entry Points (How users arrive)
1. From NewParentDashboard → Tap "Students" card
2. From ChildDetailScreen → Tap "View All Students"

### Exit Points (Where users can go)
1. StudentDetailScreen (params: { studentId, studentName })
   - Trigger: Tap student card
   - Method: safeNavigate
   - Analytics: ✅ Tracked

2. AddStudentScreen
   - Trigger: Tap "Add Student" button
   - Method: navigation.navigate
   - Analytics: ✅ Tracked

### Back Navigation
- Method: Hardware back button
- Guard: None
- Custom behavior: None

---

## 👆 USER INTERACTIONS

### Interactive Elements (12 total)

1. **Student Card Press**
   - Action: Navigate to StudentDetailScreen
   - Tracking: trackAction('view_student', 'StudentList', { studentId })
   - Validation: Checks if studentId exists

2. **Filter Button Press**
   - Action: Update filter state
   - Tracking: trackAction('filter_changed', 'StudentList', { filter })
   - Validation: None

3. **Add Student Button**
   - Action: Navigate to AddStudentScreen
   - Tracking: trackAction('add_student', 'StudentList')
   - Validation: Permission check (isAdmin)

---

[List ALL interactive elements...]

---

## ⚠️ CONDITIONAL RENDERING

### Loading State
**Condition:** `isLoading === true`
**UI:** Skeleton loader with 3 cards
**Location:** Line 245

### Error State
**Condition:** `error !== null`
**UI:** Error message with retry button
**Location:** Line 252
**Message:** "Failed to load students. Please try again."

### Empty State
**Condition:** `!isLoading && students.length === 0`
**UI:** Empty state illustration + message
**Location:** Line 258
**Message:** "No students found. Add your first student to get started."

### Permission-Based Rendering
**Condition:** `isAdmin === true`
**UI:** Admin actions panel
**Location:** Line 310

---

## 🎨 STYLING PATTERNS

### StyleSheet Styles (15 styles)
```typescript
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    padding: Spacing.md,
  },

  header: {
    marginBottom: Spacing.lg,
  },

  // ... [Document ALL styles]
});
```

### Theme Values Used
- Colors: primary, background, surface, textPrimary, textSecondary
- Spacing: xs, sm, md, lg, xl
- Typography: title, body, caption

### Dynamic Styles
```typescript
style={[styles.card, isSelected && styles.selectedCard]}
```

---

## ⚡ PERFORMANCE OPTIMIZATIONS

### Memoization
1. **filteredStudents** - useMemo with [students, filter]
2. **stats** - useMemo with [students]
3. **handlePress** - useCallback with [navigation]

### List Optimization
- Component: FlatList ✅
- keyExtractor: ✅ (item => item.id)
- getItemLayout: ❌ Not implemented
- windowSize: Default (not customized)
- maxToRenderPerBatch: Default
- **Recommendation:** Add getItemLayout for better performance

---

## 🐛 ERROR HANDLING

### Query Error Handling
✅ Implemented - Shows error UI with retry button

### Validation
1. ✅ Checks if studentId exists before navigation
2. ✅ Validates parentId in query
3. ❌ No validation for filter value

### Fallbacks
1. ✅ Default empty array if data is undefined
2. ✅ Default 0 for calculations if no data
3. ✅ Placeholder text if name is missing

---

## 📊 ANALYTICS COVERAGE

### Screen View Tracking
✅ **Tracked:** `trackScreenView('StudentList', { from: 'Dashboard' })`
**Location:** Line 89 (useEffect)

### Action Tracking (5 actions)
1. ✅ view_student
2. ✅ filter_changed
3. ✅ add_student
4. ✅ refresh_data
5. ❌ Missing: export_report tracking

---

## ♿ ACCESSIBILITY

### Coverage: ⭐⭐ (Partial)

**Implemented:**
- ✅ Button labels on 60% of buttons
- ✅ Screen reader hints on cards
- ✅ Semantic roles defined

**Missing:**
- ❌ No labels on filter buttons
- ❌ No accessibility hints on some icons
- ❌ No keyboard navigation support

**Recommendations:**
1. Add accessibilityLabel to all filter buttons
2. Add accessibilityHint to action buttons
3. Add keyboard navigation for web

---

## 📝 DOCUMENTATION QUALITY

### JSDoc Comments
- ✅ Component-level documentation
- ❌ Missing function-level docs

### Inline Comments
- 12 total comments
- 2 TODO items found
- 1 FIXME found

### TODOs Found
1. Line 145: `// TODO: Add pagination for large lists`
2. Line 203: `// TODO: Implement real-time updates`

### FIXMEs Found
1. Line 178: `// FIXME: Handle null case for missing grades`

---

## ⚠️ ISSUES IDENTIFIED

### 🔴 Critical
1. **Mock Data Found** (Line 67)
   ```typescript
   const mockStudents = [{ id: '1', name: 'Test' }];
   ```
   **Impact:** Not using real Supabase data
   **Fix:** Replace with useQuery

### 🟡 Medium
1. **Missing Error Boundary**
   **Impact:** Uncaught errors crash entire screen
   **Fix:** Add ErrorBoundary wrapper

2. **No Pagination**
   **Impact:** Slow performance with 100+ students
   **Fix:** Implement limit/offset pagination

### 🟢 Low
1. **Unused Import** (Line 12)
   ```typescript
   import { Alert } from 'react-native'; // Never used
   ```
   **Fix:** Remove unused import

---

## ✅ STRENGTHS

1. ✅ Clean component structure
2. ✅ Proper TypeScript typing
3. ✅ Good use of useMemo for performance
4. ✅ Comprehensive error handling
5. ✅ Analytics tracking implemented

---

## 🎯 RECREATION CHECKLIST

When recreating this screen, ensure you include:

- [ ] All 8 UI sections in correct order
- [ ] Both data queries (students + grades)
- [ ] All 5 calculation functions (stats, average, etc.)
- [ ] All 12 user interactions
- [ ] All 4 filter options
- [ ] All 3 navigation targets
- [ ] All 5 analytics tracking calls
- [ ] All conditional rendering paths
- [ ] All accessibility labels
- [ ] Fix identified issues (mock data, error boundary, pagination)

---

## 📦 DEPENDENCIES FOR RECREATION

### Required Tables
1. students (with parent_id, name, grade, attendance columns)
2. grades (with student_id, subject, score columns)

### Required UI Components
- Card, CardContent
- Button (variants: primary, outline)
- Badge (variants: success, warning, info)
- Row, Col
- T (Text component)
- ProgressBar

### Required Utils
- safeNavigate
- trackScreenView, trackAction
- formatDate (if used)
- calculatePercentage (custom function)

---

## 💡 RECOMMENDATIONS FOR RECREATION

### Must Have (Critical Features)
1. Replace mock data with real Supabase query
2. Implement all 8 UI sections
3. Include all calculations
4. Add all navigation flows
5. Implement error/loading/empty states

### Should Have (Important Features)
1. Add pagination for performance
2. Implement error boundary
3. Add all accessibility labels
4. Complete analytics coverage

### Nice to Have (Enhancements)
1. Add real-time updates
2. Implement optimistic updates
3. Add skeleton loading
4. Add animations

---

## 📄 COMPLETE FEATURE LIST

### Data Features
- [ ] Students list query
- [ ] Grades join query
- [ ] Filter by category
- [ ] Sort by name/grade
- [ ] Pull to refresh
- [ ] 5-minute cache

### UI Features
- [ ] Header with title and actions
- [ ] Stats summary (3 metrics)
- [ ] Filter bar (4 options)
- [ ] Student cards list
- [ ] Progress bars per student
- [ ] Status badges
- [ ] Empty state
- [ ] Loading state
- [ ] Error state with retry

### Interaction Features
- [ ] Card press navigation
- [ ] Filter selection
- [ ] Add student button
- [ ] Share button
- [ ] Pull to refresh gesture
- [ ] Retry on error

### Business Logic
- [ ] Average grade calculation
- [ ] Attendance percentage
- [ ] Student count
- [ ] Filter logic
- [ ] Sort logic

### Non-Functional
- [ ] Analytics tracking (all events)
- [ ] Error handling
- [ ] Performance optimization
- [ ] Accessibility
- [ ] TypeScript typing

---

**Analysis Complete! ✅**

**Total Features Identified:** 47
**Critical Issues:** 1
**Medium Issues:** 2
**Lines of Code:** 450

**Ready for recreation using `screen-recreator` skill**
```

---

## 🚀 HOW TO USE THIS SKILL

### Example Usage
```
User: "Analyze EnhancedParentDashboardScreen.tsx to prepare for recreation"
Assistant: *Uses screen-analyzer skill to perform comprehensive analysis*
```

### Process
1. Skill reads entire file
2. Goes through A-S checklist systematically
3. Extracts every feature, section, interaction
4. Identifies issues and missing features
5. Creates comprehensive report
6. Provides recreation checklist

### Output
Complete analysis report (markdown format) that serves as:
- Feature specification for recreation
- Quality checklist
- Issue tracking
- Documentation

---

## ✅ QUALITY STANDARDS

Every analysis must:
- [ ] Read ENTIRE file (no skipping lines)
- [ ] Complete ALL sections (A through S)
- [ ] Extract ALL imports, types, state, queries
- [ ] Document ALL UI sections in order
- [ ] List ALL user interactions
- [ ] Identify ALL calculations
- [ ] Note ALL conditional rendering
- [ ] Extract ALL styling patterns
- [ ] Find ALL TODOs and FIXMEs
- [ ] Identify critical issues
- [ ] Provide recreation checklist

---

**Use this BEFORE `screen-recreator` to ensure 100% feature parity!**

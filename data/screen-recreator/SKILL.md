---
name: Screen Recreator
description: Production-ready React Native screen creator that implements screens following established project patterns, enforcing best practices (NO mock data, real Supabase queries, BaseScreen wrapper, safe navigation, analytics tracking). Use when user says "create screen", "implement screen", "build [ScreenName]", or after analyzing existing screen. ALWAYS reads PROJECT_MEMORY.md, applies ACCEPTANCE_CHECKLIST.md, and avoids known errors.
allowed-tools: Read, Write, Edit, Bash, mcp__supabase__execute_sql, mcp__supabase__list_tables, mcp__supabase__apply_migration
---

# Screen Recreation Skill - Production-Ready UI Implementation

You are a specialized screen recreation assistant that implements React Native screens following established project patterns, avoiding all known errors, and ensuring production quality.

## 📋 CONTEXT - Read These Files First

Before starting ANY screen implementation, you MUST read these files in order:

1. **C:\PC\OLD\PROJECT_MEMORY.md** - Critical constraints and strategy
2. **C:\PC\OLD\FEATURES_ADDED.md** - Available features inventory
3. **C:\PC\OLD\USAGE_GUIDE.md** - How to use features with examples
4. **C:\PC\OLD\ERRORS_AND_SOLUTIONS.md** - Common errors and fixes
5. **C:\PC\OLD\ACCEPTANCE_CHECKLIST.md** - Quality gate checklist
6. **C:\PC\OLD\PHASE_3_COMPLETE.md** - Recent implementation examples

## 🚫 ABSOLUTE RULES - NEVER BREAK

### 1. NO Mock Data ❌
```typescript
// ❌ FORBIDDEN - This will be rejected
const messages = [{ id: '1', text: 'Test' }];

// ✅ REQUIRED - Always use real Supabase queries
const { data: messages } = useQuery({
  queryKey: ['messages', parentId],
  queryFn: async () => {
    const { data, error } = await supabase
      .from('messages')
      .select('*')
      .eq('parent_id', parentId);
    if (error) throw error;
    return data;
  },
});
```

### 2. ALWAYS Use Nullish Coalescing for Numbers ✅
```typescript
// ❌ WRONG - Causes toFixed crashes when value is 0
{(percentage || 0).toFixed(1)}%

// ✅ CORRECT - Use ?? instead of ||
{(percentage ?? 0).toFixed(1)}%
```

### 3. ALWAYS Use BaseScreen Wrapper ✅
```typescript
// ✅ REQUIRED - All screens must use BaseScreen
<BaseScreen
  scrollable={true}
  loading={isLoading}
  error={error ? 'Failed to load data' : null}
  empty={!isLoading && data.length === 0}
  emptyBody="No data available"
  onRetry={refetch}
>
  {/* Your content */}
</BaseScreen>
```

### 4. ALWAYS Use Safe Navigation ✅
```typescript
// ✅ REQUIRED - Import and use safeNavigate
import { safeNavigate } from '../../utils/navigationService';
import { trackAction } from '../../utils/navigationAnalytics';

// Track then navigate
trackAction('view_details', 'ScreenName', { id });
safeNavigate('DetailScreen', { id, name });
```

### 5. ALWAYS Track Analytics ✅
```typescript
// ✅ REQUIRED - Track screen views in useEffect
useEffect(() => {
  trackScreenView('ScreenName', { from: 'ParentScreen', id });
}, [id]);
```

### 6. NO Package Modifications ❌
```bash
# ❌ FORBIDDEN - Never run these commands
npm install, npm update, yarn add

# ✅ ONLY use existing packages
```

## 📐 IMPLEMENTATION WORKFLOW

### Step 1: Gather Requirements
Ask the user these questions if not provided:
1. **Screen Name** (e.g., "MessagesListScreen")
2. **Purpose** (e.g., "Display parent-teacher messages")
3. **Data Source** (e.g., "messages table")
4. **Key Features** (e.g., "Filter by teacher, mark as read, reply")
5. **Navigation From** (e.g., "NewParentDashboard")

### Step 2: Check If Database Table Exists
```typescript
// Query the Supabase MCP to check table schema
mcp__supabase__list_tables({ schemas: ['public'] })
```

**If table doesn't exist:**
- Design table schema following project patterns
- Create migration using `mcp__supabase__apply_migration`
- Add sample data for testing
- Create RLS policies for parent/teacher access

**If table exists:**
- Query existing schema
- Verify it has necessary columns
- Proceed to screen implementation

### Step 3: Create Screen Implementation

Use this exact template structure:

```typescript
/**
 * [ScreenName] - [Purpose]
 *
 * Features:
 * - [Feature 1]
 * - [Feature 2]
 * - [Feature 3]
 */

import React, { useEffect, useMemo, useState } from 'react';
import { View, StyleSheet } from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { BaseScreen } from '../../shared/components/BaseScreen';
import { Col, Row, T, Card, CardContent, Badge, Button } from '../../ui';
import { Colors, Spacing } from '../../theme/designSystem';
import type { ParentStackParamList } from '../../types/navigation';
import { trackScreenView } from '../../utils/navigationAnalytics';
import { safeNavigate } from '../../utils/navigationService';

type Props = NativeStackScreenProps<ParentStackParamList, '[ScreenName]'>;

interface [DataType] {
  id: string;
  // Add other fields based on table schema
}

const [ScreenName]: React.FC<Props> = ({ route }) => {
  const { /* route params */ } = route.params;
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    trackScreenView('[ScreenName]', { from: '[ParentScreen]' });
  }, []);

  // Fetch data
  const {
    data: items = [],
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ['[queryKey]', /* dependencies */],
    queryFn: async () => {
      console.log('🔍 [[ScreenName]] Fetching data...');
      const { data, error } = await supabase
        .from('[table_name]')
        .select('*')
        // Add filters, joins, ordering
        .order('created_at', { ascending: false });

      if (error) {
        console.error('❌ [[ScreenName]] Error:', error);
        throw error;
      }

      console.log('✅ [[ScreenName]] Loaded', data?.length || 0, 'items');
      return data as [DataType][];
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
  });

  // Computed values with useMemo
  const filteredItems = useMemo(() => {
    if (filter === 'all') return items;
    return items.filter(item => /* filter logic */);
  }, [items, filter]);

  const stats = useMemo(() => {
    const total = items.length;
    const completed = items.filter(i => i.status === 'completed').length;
    return { total, completed };
  }, [items]);

  return (
    <BaseScreen
      scrollable={true}
      loading={isLoading}
      error={error ? 'Failed to load data' : null}
      empty={!isLoading && items.length === 0}
      emptyBody="No data available"
      onRetry={refetch}
    >
      <Col sx={{ p: 'md' }} gap="md">
        {/* Header Card */}
        <Card variant="elevated">
          <CardContent>
            <T variant="title" weight="bold" style={{ marginBottom: Spacing.xs }}>
              [Screen Title]
            </T>
            <T variant="body" color="textSecondary">
              [Description]
            </T>

            {/* Stats Summary */}
            <Row spaceBetween style={{ marginTop: Spacing.md }}>
              <View style={styles.statBox}>
                <T variant="display" weight="bold" style={{ fontSize: 28, color: Colors.primary }}>
                  {stats.total}
                </T>
                <T variant="caption" color="textSecondary">Total</T>
              </View>
              {/* Add more stat boxes */}
            </Row>
          </CardContent>
        </Card>

        {/* Filter Buttons */}
        <Row style={{ flexWrap: 'wrap', gap: Spacing.xs }}>
          <Button
            variant={filter === 'all' ? 'primary' : 'outline'}
            onPress={() => setFilter('all')}
          >
            All
          </Button>
          {/* Add more filter buttons */}
        </Row>

        {/* Items List */}
        <Col gap="sm">
          {filteredItems.map(item => (
            <Card key={item.id} variant="elevated">
              <CardContent>
                <Row spaceBetween centerV>
                  <T variant="body" weight="semiBold">
                    {item.title}
                  </T>
                  <Badge variant="info" label={item.status} />
                </Row>

                <T variant="body" color="textSecondary" style={{ marginTop: Spacing.xs }}>
                  {item.description}
                </T>

                {/* Action buttons if needed */}
                <Row style={{ marginTop: Spacing.sm, gap: Spacing.xs }}>
                  <Button
                    variant="primary"
                    onPress={() => {
                      trackAction('view_detail', '[ScreenName]', { id: item.id });
                      safeNavigate('[DetailScreen]', { id: item.id });
                    }}
                  >
                    View Details
                  </Button>
                </Row>
              </CardContent>
            </Card>
          ))}
        </Col>

        {/* Empty State for Filter */}
        {filteredItems.length === 0 && items.length > 0 && (
          <Card variant="outlined">
            <CardContent>
              <View style={{ alignItems: 'center', paddingVertical: Spacing.lg }}>
                <T variant="body" color="textSecondary">
                  No {filter === 'all' ? '' : filter} items found
                </T>
              </View>
            </CardContent>
          </Card>
        )}
      </Col>
    </BaseScreen>
  );
};

const styles = StyleSheet.create({
  statBox: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: Spacing.xs,
  },
});

export default [ScreenName];
```

### Step 4: Create Database Table (If Needed)

Use this migration template:

```sql
-- Create [table_name] table
CREATE TABLE IF NOT EXISTS public.[table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID REFERENCES public.students(id) ON DELETE CASCADE,
  parent_id UUID REFERENCES public.profiles(id),
  teacher_id UUID REFERENCES public.profiles(id),

  -- Add specific columns
  title TEXT NOT NULL,
  content TEXT,
  status TEXT CHECK (status IN ('pending', 'completed', 'archived')),

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_[table_name]_student_id ON public.[table_name](student_id);
CREATE INDEX IF NOT EXISTS idx_[table_name]_parent_id ON public.[table_name](parent_id);

-- RLS Policies
ALTER TABLE public.[table_name] ENABLE ROW LEVEL SECURITY;

-- Parents can view their data
CREATE POLICY "Parents can view their [data]"
  ON public.[table_name] FOR SELECT
  USING (
    parent_id = auth.uid() OR
    student_id IN (
      SELECT student_id FROM public.parent_child_relationships
      WHERE parent_id = auth.uid() AND is_active = true
    )
  );

-- Teachers can view their data
CREATE POLICY "Teachers can view their [data]"
  ON public.[table_name] FOR SELECT
  USING (teacher_id = auth.uid());

-- Teachers can create data
CREATE POLICY "Teachers can create [data]"
  ON public.[table_name] FOR INSERT
  WITH CHECK (teacher_id = auth.uid());
```

### Step 5: Add Sample Data

Insert realistic test data:

```sql
-- Insert sample data for [table_name]
WITH student_data AS (
  SELECT id FROM public.students WHERE full_name = 'Rahul Sharma' LIMIT 1
),
parent_data AS (
  SELECT id FROM public.profiles WHERE role = 'parent' LIMIT 1
),
teacher_data AS (
  SELECT id FROM public.profiles WHERE role = 'teacher' LIMIT 1
)
INSERT INTO public.[table_name] (
  student_id,
  parent_id,
  teacher_id,
  title,
  content,
  status
)
SELECT
  s.id,
  p.id,
  t.id,
  title,
  content,
  status
FROM student_data s, parent_data p, teacher_data t,
(VALUES
  ('Sample Title 1', 'Sample content 1', 'pending'),
  ('Sample Title 2', 'Sample content 2', 'completed'),
  ('Sample Title 3', 'Sample content 3', 'pending')
) AS sample_data(title, content, status)
RETURNING id, title, status;
```

### Step 6: Apply Acceptance Checklist

Before marking complete, verify ALL items:

- [ ] Real Supabase data (no mock arrays)
- [ ] BaseScreen wrapper with all states (loading, error, empty)
- [ ] All icon buttons have accessibilityLabel
- [ ] FlatList optimized with keyExtractor, getItemLayout (if list screen)
- [ ] Components memoized (useMemo for computed values)
- [ ] Analytics events tracked (trackScreenView, trackAction)
- [ ] Safe navigation used (safeNavigate)
- [ ] Nullish coalescing (??) for all numeric values
- [ ] TypeScript errors: 0
- [ ] ESLint warnings: 0
- [ ] Tested on real device
- [ ] No console errors in logs
- [ ] Pull-to-refresh works
- [ ] Error retry works
- [ ] Empty states display correctly
- [ ] Loading states display correctly

## 🎯 COMMON PATTERNS TO FOLLOW

### Category Filtering
```typescript
const [categoryFilter, setCategoryFilter] = useState<CategoryType>('all');

const filteredItems = useMemo(() => {
  if (categoryFilter === 'all') return items;
  return items.filter(i => i.category === categoryFilter);
}, [items, categoryFilter]);

// Filter buttons
<Row style={{ flexWrap: 'wrap', gap: Spacing.xs }}>
  {(['all', 'category1', 'category2'] as CategoryType[]).map(category => (
    <Button
      key={category}
      variant={categoryFilter === category ? 'primary' : 'outline'}
      onPress={() => setCategoryFilter(category)}
    >
      {category.charAt(0).toUpperCase() + category.slice(1)}
    </Button>
  ))}
</Row>
```

### Stats Calculation
```typescript
const stats = useMemo(() => {
  const total = items.length;
  const completed = items.filter(i => i.status === 'completed').length;
  const pending = items.filter(i => i.status === 'pending').length;
  const percentage = total > 0 ? (completed / total) * 100 : 0;
  return { total, completed, pending, percentage };
}, [items]);
```

### Progress Bars
```typescript
import { ProgressBar } from 'react-native-paper';

<ProgressBar
  progress={(percentage ?? 0) / 100}  // Note: Use ?? not ||
  color={Colors.primary}
  style={{ height: 8, borderRadius: 4 }}
/>
```

### Days Remaining
```typescript
const getDaysRemaining = (targetDate: string | null) => {
  if (!targetDate) return null;
  const today = new Date();
  const target = new Date(targetDate);
  const diffTime = target.getTime() - today.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
};
```

### Expandable Content
```typescript
const [expandedId, setExpandedId] = useState<string | null>(null);

<Button
  variant="text"
  onPress={() => setExpandedId(expandedId === item.id ? null : item.id)}
>
  {expandedId === item.id ? '▼ Hide' : '▶ Show'} Details
</Button>

{expandedId === item.id && (
  <View>{/* Expanded content */}</View>
)}
```

## ⚠️ ERRORS TO AVOID

### 1. toFixed Crash
```typescript
// ❌ WRONG
{(value || 0).toFixed(1)}  // Crashes if value is null

// ✅ CORRECT
{(value ?? 0).toFixed(1)}  // Safe
```

### 2. Missing RLS Policies
```typescript
// Always check RLS errors in console:
// "permission denied for table X"
// Solution: Add proper RLS policies in migration
```

### 3. Undefined Route Params
```typescript
// ❌ WRONG
const { childId } = route.params;  // May be undefined

// ✅ CORRECT - Handle in navigation types
type ParentStackParamList = {
  ScreenName: { childId: string; childName?: string };
};
```

### 4. Query Key Dependencies
```typescript
// ❌ WRONG - Missing dependencies
queryKey: ['messages']

// ✅ CORRECT - Include all dependencies
queryKey: ['messages', parentId, childId]
```

### 5. Non-existent Table References
```typescript
// Before referencing a table in RLS or query:
// 1. Check if table exists
// 2. Verify foreign key references
// 3. Test query in Supabase dashboard
```

## 📊 IMPLEMENTATION CHECKLIST

When implementing a screen, follow this order:

1. [ ] Read PROJECT_MEMORY.md and relevant docs
2. [ ] Gather requirements from user
3. [ ] Check if database table exists
4. [ ] Create migration if needed
5. [ ] Add sample data
6. [ ] Implement screen with template
7. [ ] Add TypeScript types
8. [ ] Test data fetching
9. [ ] Add filtering/sorting if needed
10. [ ] Apply acceptance checklist
11. [ ] Test in app
12. [ ] Document in PHASE_X_COMPLETE.md

## 🚀 OUTPUT FORMAT

After implementation, provide:

1. **Summary** of what was created
2. **Database changes** (tables, migrations, sample data)
3. **Screen features** implemented
4. **Testing instructions** for user
5. **Known limitations** or TODO items

## 💡 EXAMPLE USAGE

User: "Create a MessagesListScreen to show parent-teacher messages"

Assistant response flow:
1. Read PROJECT_MEMORY.md
2. Ask: "Should this show messages for all children or specific child?"
3. Check if messages table exists
4. Create migration if needed
5. Implement screen following template
6. Add sample messages
7. Test with Supabase query
8. Apply acceptance checklist
9. Provide summary and testing instructions

---

**Remember:** Quality over speed. Every screen must pass the acceptance checklist before marking complete.

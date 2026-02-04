---
name: restaurant-feature-workflow
description: |
  This skill should be used when adding new restaurant features across the full stack (Backend → Shared → Web → Mobile).
  Trigger keywords: "레스토랑 검색/필터/정렬 추가", "restaurant search/filter/sort", "레스토랑 API 수정", "restaurant list UI 업데이트".
  Provides step-by-step workflow for database migrations, backend API updates, shared layer updates, and frontend UI implementation.
---

# Restaurant Feature Workflow

**Purpose**: Guide for adding new restaurant features across the full stack (Backend → Shared → Web → Mobile)

**Complexity**: Medium | **Est. Time**: 2-4 hours per feature

---

## 🎯 When to Use This Skill

Invoke this skill when user requests include:
- "레스토랑 검색 기능 추가해줘"
- "레스토랑 필터/정렬 추가"
- "Add restaurant search/filter/sort"
- "레스토랑 API 수정"
- "레스토랑 목록 UI 업데이트"

**Keywords**: `restaurant`, `레스토랑`, `full stack`, `API + UI`

---

## ✅ What This Skill Covers

- Database migrations (SQLite)
- Backend API updates (Fastify)
- Shared layer updates (Hooks, API Service)
- Web UI updates (React Native Web)
- Mobile UI updates (React Native)
- Testing & documentation

## ❌ Out of Scope

- Initial project setup → See [ARCHITECTURE.md](../../docs/claude/00-core/ARCHITECTURE.md)
- Deployment → See [DEVELOPMENT.md](../../docs/claude/00-core/DEVELOPMENT.md)
- Detailed API docs → See [FRIENDLY-RESTAURANT.md](../../docs/claude/04-friendly/FRIENDLY-RESTAURANT.md)

---

## 📁 Project Structure Quick Reference

```
niney-life-pickr/
├── servers/friendly/          # Backend (Fastify + SQLite)
│   ├── src/db/migrations/     # Database migrations
│   ├── src/db/repositories/   # Data access layer
│   └── src/routes/            # API routes
├── apps/shared/               # Shared logic (Web + Mobile)
│   ├── hooks/                 # Custom React hooks
│   └── services/              # API service
├── apps/web/                  # Web UI (React Native Web)
│   └── src/components/Restaurant/
└── apps/mobile/               # Mobile UI (React Native)
    └── src/screens/RestaurantListScreen.tsx
```

---

## 🌲 Quick Decision Tree

Before starting, answer these questions:

```
1. Does feature need DATABASE changes?
   ├─ YES → Create migration → Update repository
   └─ NO  → Skip to Step 2

2. Does feature need NEW API endpoint?
   ├─ YES → Add new route + schema
   └─ NO  → Modify existing route

3. Does feature need NEW STATE in frontend?
   ├─ YES → Update useRestaurantList hook
   └─ NO  → Use existing state

4. Does feature affect UI?
   ├─ YES → Update Shared → Web → Mobile
   └─ NO  → Done, update docs only
```

---

## 📋 Layer-by-Layer Checklist

### 🗄️ Layer 1: Database (if needed)

**When**: New column, index, or table needed

**File**: `servers/friendly/src/db/migrations/{number}_{description}.sql`

**Steps**:
1. ✅ Find highest migration number (e.g., `005`)
2. ✅ Create new file: `006_add_restaurant_{feature}.sql`
3. ✅ Write migration:
   ```sql
   -- Add index for performance
   CREATE INDEX IF NOT EXISTS idx_restaurants_{column_name} ON restaurants({column_name});
   ```
4. ✅ Restart server to apply: `cd servers/friendly && npm run dev`
5. ✅ Verify in logs: "All migrations completed"

**Tool**: Use `Write` tool for migration file

---

### ⚙️ Layer 2: Backend API

#### 2A. Repository Layer

**File**: `servers/friendly/src/db/repositories/restaurant.repository.ts`

**Steps**:
1. ✅ Read current `findAll()` and `count()` methods
2. ✅ Add new parameter to method signature:
   ```typescript
   async findAll(
     limit: number = 20,
     offset: number = 0,
     category?: string,
     newParam?: string  // ADD THIS
   ): Promise<RestaurantDB[]>
   ```
3. ✅ Update SQL query logic:
   ```typescript
   const conditions: string[] = [];
   const params: any[] = [];

   if (newParam && newParam.trim()) {
     conditions.push('column_name LIKE ?');
     params.push(`%${newParam.trim()}%`);
   }

   if (conditions.length > 0) {
     query += ' WHERE ' + conditions.join(' AND ');
   }
   ```
4. ✅ Update `count()` method with same logic

**Tools**:
- `Read` → Read repository file first
- `Edit` → Modify methods

#### 2B. Route Layer

**File**: `servers/friendly/src/routes/restaurant.routes.ts`

**Steps**:
1. ✅ Read current route schema
2. ✅ Add new parameter to TypeBox schema:
   ```typescript
   querystring: Type.Object({
     // ... existing params
     newParam: Type.Optional(Type.String({
       description: 'Description here',
       minLength: 1,
       maxLength: 100
     }))
   })
   ```
3. ✅ Update request handler:
   ```typescript
   const { limit, offset, category, newParam } = request.query as {
     // ... add type
     newParam?: string;
   };

   const [restaurants, total] = await Promise.all([
     restaurantRepository.findAll(limit, offset, category, newParam),
     restaurantRepository.count(category, newParam)
   ]);
   ```

**Tools**:
- `Read` → Read routes file
- `Edit` → Update schema and handler

#### 2C. Test Backend API

**Commands**:
```bash
# Test with curl
curl "http://localhost:4000/api/restaurants?newParam=test&limit=5"

# Or use Swagger UI
open http://localhost:4000/docs
```

**Expected**: `200 OK` with filtered results

**Tools**: `Bash` → Run curl commands

---

### 🔗 Layer 3: Shared Layer

#### 3A. API Service

**File**: `apps/shared/services/api.service.ts`

**Steps**:
1. ✅ Read `getRestaurants()` method
2. ✅ Add new parameter:
   ```typescript
   async getRestaurants(
     limit: number = 1000,
     offset: number = 0,
     category?: string,
     newParam?: string  // ADD THIS
   ): Promise<ApiResponse<RestaurantListResponse>> {
     let url = `/api/restaurants?limit=${limit}&offset=${offset}`;

     if (category) {
       url += `&category=${encodeURIComponent(category)}`;
     }

     // ADD THIS BLOCK
     if (newParam && newParam.trim()) {
       url += `&newParam=${encodeURIComponent(newParam.trim())}`;
     }

     return this.request<RestaurantListResponse>(url, { method: 'GET' });
   }
   ```

**Tools**:
- `Read` → Read api.service.ts
- `Edit` → Add parameter

#### 3B. Custom Hook

**File**: `apps/shared/hooks/useRestaurantList.ts`

**Steps**:
1. ✅ Read hook file
2. ✅ Add new state:
   ```typescript
   const [newState, setNewState] = useState('')
   ```
3. ✅ Update `fetchRestaurants()`:
   ```typescript
   const response = await apiService.getRestaurants(
     limit,
     offset,
     selectedCategory || undefined,
     newState || undefined  // Pass new state
   )
   ```
4. ✅ Add debounced effect (if search/filter):
   ```typescript
   useEffect(() => {
     const timer = setTimeout(() => {
       fetchRestaurants()
     }, 300) // 300ms debounce

     return () => clearTimeout(timer)
   }, [newState])
   ```
5. ✅ Update return object:
   ```typescript
   return {
     // ... existing returns
     newState,
     setNewState,
   }
   ```

**Tools**:
- `Read` → Read hook file
- `Edit` → Add state, update fetch, add effect

---

### 🖥️ Layer 4: Web UI

#### 4A. Component Props

**File**: `apps/web/src/components/Restaurant/RestaurantList.tsx`

**Steps**:
1. ✅ Read component file
2. ✅ Update `RestaurantListProps` interface:
   ```typescript
   interface RestaurantListProps {
     // ... existing props
     newState: string
     setNewState: (value: string) => void
   }
   ```
3. ✅ Update component parameters:
   ```typescript
   const RestaurantList: React.FC<RestaurantListProps> = ({
     // ... existing params
     newState,
     setNewState,
   }) => {
   ```

**Tools**:
- `Read` → Read component
- `Edit` → Update interface and params

#### 4B. Add UI Elements

**In same file**: Add UI for new feature

```tsx
{/* Add this UI block */}
<View style={styles.newFeatureContainer}>
  <TextInput
    style={[styles.input, { borderColor: colors.border, color: colors.text }]}
    placeholder="Placeholder text..."
    placeholderTextColor={colors.textSecondary}
    value={newState}
    onChangeText={setNewState}
  />
  {newState.length > 0 && (
    <TouchableOpacity onPress={() => setNewState('')} style={styles.clearButton}>
      <FontAwesomeIcon icon={faTimes} size={16} color={colors.textSecondary} />
    </TouchableOpacity>
  )}
</View>
```

**Add styles**:
```typescript
const styles = StyleSheet.create({
  // ... existing styles
  newFeatureContainer: {
    marginBottom: 16,
  },
  clearButton: {
    position: 'absolute',
    right: 12,
    top: 14,
    padding: 4,
  },
})
```

**Tools**: `Edit` → Add UI and styles

#### 4C. Parent Component

**File**: `apps/web/src/components/Restaurant.tsx`

**Steps**:
1. ✅ Read parent component
2. ✅ Extract new state from hook:
   ```typescript
   const {
     // ... existing state
     newState,
     setNewState,
   } = restaurantState
   ```
3. ✅ Pass to child component(s):
   ```typescript
   <RestaurantList
     // ... existing props
     newState={newState}
     setNewState={setNewState}
   />
   ```
4. ✅ Update `DesktopLayout` interface if needed

**Tools**:
- `Read` → Read parent component
- `Edit` → Extract state and pass props

---

### 📱 Layer 5: Mobile UI

**File**: `apps/mobile/src/screens/RestaurantListScreen.tsx`

**Steps**:
1. ✅ Read screen file
2. ✅ Extract new state from hook:
   ```typescript
   const {
     // ... existing
     newState,
     setNewState,
   } = useRestaurantList({ /* callbacks */ })
   ```
3. ✅ Add UI (same pattern as Web):
   ```tsx
   <View style={styles.newFeatureContainer}>
     <TextInput
       style={[styles.input, { /* theme colors */ }]}
       placeholder="Placeholder text..."
       placeholderTextColor={colors.textSecondary}
       value={newState}
       onChangeText={setNewState}
       keyboardAppearance={theme === 'dark' ? 'dark' : 'light'}
     />
     {newState.length > 0 && (
       <TouchableOpacity onPress={() => setNewState('')} style={styles.clearButton}>
         <Text style={{ fontSize: 16, color: colors.textSecondary }}>✕</Text>
       </TouchableOpacity>
     )}
   </View>
   ```
4. ✅ Add styles to `StyleSheet.create()`

**Tools**:
- `Read` → Read screen file
- `Edit` → Extract state, add UI, add styles

---

## ✅ Validation Steps

After each layer, verify:

### Backend Validation
```bash
# Server running?
cd servers/friendly && npm run dev

# API works?
curl "http://localhost:4000/api/restaurants?newParam=test"

# Expected: 200 OK with data
```

### Shared Validation
```bash
# TypeScript compiles?
cd apps/shared && npm run type-check

# No errors? → Good to go
```

### Web Validation
```bash
# Start web app
cd apps/web && npm run dev

# Open browser
open http://localhost:3000/restaurant

# Test:
# 1. UI renders correctly
# 2. Feature works as expected
# 3. No console errors
```

### Mobile Validation
```bash
# Start mobile app
cd apps/mobile && npm start

# Test on iOS/Android
npm run ios
# OR
npm run android

# Test:
# 1. UI renders correctly
# 2. Feature works
# 3. No red screen errors
```

---

## 🚨 Common Pitfalls & Solutions

### ❌ TypeBox validation fails (400 Bad Request)
**Cause**: Schema not updated in routes
**Fix**: Add parameter to `Type.Object({ ... })` in route schema

### ❌ Props type error in React
**Cause**: Props not passed from parent
**Fix**:
1. Check hook exports new state
2. Check parent extracts from hook
3. Check parent passes to child
4. Check child interface includes prop

### ❌ API returns old data
**Cause**: Server not restarted after code changes
**Fix**:
```bash
cd servers/friendly
npm run kill  # Kill old process
npm run dev   # Restart
```

### ❌ Hook not re-fetching
**Cause**: Missing useEffect dependency
**Fix**: Add new state to useEffect dependency array

---

## 🛠️ Claude Code Tools to Use

### 🔍 Before Implementing
```typescript
// Find existing patterns
Grep: pattern="useRestaurantList", output_mode="files_with_matches"
Grep: pattern="getRestaurants", output_mode="files_with_matches"

// Find all restaurant files
Glob: pattern="**/*Restaurant*.{ts,tsx}"
```

### 📖 During Implementation
```typescript
// Read files before editing
Read: file_path="servers/friendly/src/db/repositories/restaurant.repository.ts"
Read: file_path="apps/shared/hooks/useRestaurantList.ts"

// Edit files
Edit: old_string="...", new_string="..."

// Test immediately
Bash: command="curl http://localhost:4000/api/restaurants?test=value"
```

### ✅ After Implementation
```typescript
// Run tests
Bash: command="cd servers/friendly && npm test"
Bash: command="cd apps/web && npm run type-check"

// Check git status
Bash: command="git status"
```

---

## 💡 Example: Adding Restaurant Name Search

**User Request**: "레스토랑 이름 검색 기능 추가해줘"

**Quick Steps**:
1. ✅ **DB**: Create `005_add_restaurant_name_index.sql` with index on `name`
2. ✅ **Repository**: Add `searchName?: string` to `findAll()` and `count()`
3. ✅ **Routes**: Add `searchName` to TypeBox schema, pass to repository
4. ✅ **API Service**: Add `searchName` parameter to `getRestaurants()`
5. ✅ **Hook**: Add `searchName` state, update `fetchRestaurants()`, add debounced effect
6. ✅ **Web UI**: Add search input, pass props from parent
7. ✅ **Mobile UI**: Add search input, extract from hook
8. ✅ **Test**: Backend curl, Web browser, Mobile simulator

**Time**: ~2 hours

---

## 📚 Related Documentation

- **Architecture**: [ARCHITECTURE.md](../../docs/claude/00-core/ARCHITECTURE.md)
- **Database**: [DATABASE.md](../../docs/claude/00-core/DATABASE.md)
- **Backend APIs**: [FRIENDLY-RESTAURANT.md](../../docs/claude/04-friendly/FRIENDLY-RESTAURANT.md)
- **Web UI**: [WEB-RESTAURANT.md](../../docs/claude/01-web/WEB-RESTAURANT.md)
- **Mobile UI**: [MOBILE-RESTAURANT-LIST.md](../../docs/claude/02-mobile/MOBILE-RESTAURANT-LIST.md)
- **Testing**: [FRIENDLY-TESTING.md](../../docs/claude/04-friendly/FRIENDLY-TESTING.md)

---

## 🎬 Skill Invocation

When user says:
- "Add restaurant [feature]"
- "레스토랑 [기능] 추가"
- "Modify restaurant API"
- "Update restaurant list"

**Claude should**:
1. Use this skill as a checklist
2. Follow layer-by-layer approach
3. Validate after each layer
4. Reference detailed docs when needed
5. Create TODO list for tracking progress

**Estimated workflow time**: 2-4 hours depending on complexity

---

**Version**: 2.0 (Refined with skill-creator)
**Last Updated**: 2025-10-29
**Maintained by**: Claude Code

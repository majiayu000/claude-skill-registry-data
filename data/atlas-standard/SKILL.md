---
name: atlas-standard
description: Standard 5-phase workflow for most development tasks - bugs, small features, refactors (30-60 min)
---

# Atlas Standard Workflow

## When to Use This Skill

**Perfect for (80% of tasks):**
- Bug fixes (2-5 files affected)
- Small features (clear requirements)
- Code refactoring
- Test additions
- Logic changes with moderate complexity

**Time estimate**: 30-60 minutes

**Success criteria**:
- Feature complete in < 2 hours
- All edge cases covered
- Tests pass
- Peer review approved

## The 5 Phases

```
Phase 1: Research      → Understand current implementation
Phase 2: Plan          → Design approach
Phase 3: Implement     → Make changes + tests
Phase 4: Review        → Edge cases + security
Phase 5: Deploy        → Full test suite + deployment
```

---

## Phase 1: Research

**Goal**: Understand the current implementation and identify all affected files.

### Steps:

1. **Find all related files**
   ```bash
   # Search for relevant code patterns
   grep -r "featureName" src/
   grep -r "ComponentName" src/

   # Find component/function usage
   grep -r "import.*ComponentName" src/
   ```

2. **Understand current implementation**
   - Read the main file(s) involved
   - Trace data flow
   - Identify dependencies
   - Note platform-specific code (iOS vs Android vs Web)

3. **Check for existing patterns**
   - Look for similar implementations
   - Identify coding patterns to follow
   - Review related tests

4. **Identify potential impacts**
   - Which components use this code?
   - Are there platform-specific considerations?
   - What tests cover this area?

### Output:
- List of files to modify
- Understanding of current implementation
- Potential risks identified

### StackMap-Specific Research:

**For data/state changes:**
- Check store usage: Which store? (`useAppStore`, `useUserStore`, `useSettingsStore`, `useLibraryStore`)
- Verify field naming: Activities use `text`/`icon`, Users use `icon`/`name`
- Check `/src/utils/dataNormalizer.js` for normalization logic

**For UI changes:**
- Check platform-specific files: `.native.js`, `.web.js`, `.ios.js`, `.android.js`
- Review CLAUDE.md for platform gotchas
- Verify Typography component usage (don't use fontWeight directly on Android)

**For sync-related changes:**
- Check `/src/services/sync/syncService.js`
- Review conflict resolution logic
- Verify encryption/decryption handling

### Example Research Output:
```
Files to modify:
- /src/services/sync/syncService.js (main sync logic)
- /src/services/sync/syncStoreIntegration.js (store interaction)
- /src/utils/dataNormalizer.js (field normalization)

Current implementation:
- Conflict resolution uses Object.assign, overwrites nested fields
- Icons stored as `activity.icon` but also `activity.emoji` (legacy)

Risks:
- Must preserve all icon variations during conflict merge
- Need fallback: icon || emoji
```

---

## Phase 2: Plan

**Goal**: Design the approach and create a file-by-file implementation plan.

### Steps:

1. **Design the solution**
   - How will you fix the bug / implement the feature?
   - What's the cleanest approach?
   - Are there edge cases to handle?

2. **List file changes**
   - File 1: What changes?
   - File 2: What changes?
   - Tests: What new tests?

3. **Identify dependencies**
   - What order to make changes?
   - Any breaking changes?
   - Backwards compatibility needed?

4. **Plan testing approach**
   - What tests to add/modify?
   - How to verify manually?
   - Platform-specific testing needed?

### Output:
- Clear implementation plan
- File-by-file change list
- Testing strategy

### StackMap-Specific Planning:

**Field naming strategy:**
- Reading: Use fallbacks `text || name || title`, `icon || emoji`
- Writing: Use canonical fields `text`, `icon`
- Normalization: Add to `dataNormalizer.js` if needed

**Store update strategy:**
- Identify which store(s) to update
- Use store-specific methods (NOT `useAppStore.setState`)
- Plan for optimistic updates if applicable

**Platform strategy:**
- Shared code: Must work on iOS, Android, Web
- Platform-specific: Create separate files (`.native.js`, `.web.js`)
- Platform gotchas: Check CLAUDE.md before implementing

### Example Plan:
```
Solution Design:
- Update conflict resolution to deep-merge nested objects
- Add explicit icon field preservation
- Add fallback logic for legacy emoji field

File Changes:
1. /src/services/sync/syncService.js
   - Modify `resolveConflict()` function
   - Add `preserveIconFields()` helper
   - Use deep merge instead of Object.assign

2. /src/utils/dataNormalizer.js
   - Add `normalizeActivityIcon()` function
   - Handle emoji → icon migration

3. /tests/sync/syncService.test.js
   - Add test: "preserves icon during conflict"
   - Add test: "migrates emoji to icon"

Testing Approach:
- Unit tests for conflict resolution
- Integration test for full sync cycle
- Manual test: Create conflict, verify icon preserved
```

---

## Phase 3: Implement

**Goal**: Make the changes and update tests.

### Steps:

1. **Implement changes file-by-file**
   - Follow the plan from Phase 2
   - Use store-specific update methods
   - Follow field naming conventions
   - Add code comments for complex logic

2. **Update/add tests**
   - Add tests for new functionality
   - Update existing tests if behavior changed
   - Ensure tests cover edge cases

3. **Verify locally**
   - Run tests: `npm test`
   - Run type checking: `npm run typecheck`
   - Test manually if UI changes

4. **Apply StackMap conventions**
   - NO gray text (use #000)
   - Typography component for fonts
   - Store-specific update methods
   - Field naming: `text`/`icon`, not `name`/`emoji`

### Implementation Checklist:

**Before writing code:**
- [ ] Understand the pattern to follow (research phase complete)
- [ ] Know which store method to use
- [ ] Field naming strategy clear

**During implementation:**
- [ ] Use store-specific methods (`useUserStore.getState().setUsers()`)
- [ ] Use canonical field names (`text`, `icon`)
- [ ] Include fallbacks when reading (`text || name || title`)
- [ ] Remove debug logs or wrap in `__DEV__` check
- [ ] Add comments for non-obvious logic

**After implementation:**
- [ ] All imports correct
- [ ] No console.log statements
- [ ] Tests added/updated
- [ ] Type checking passes

### StackMap-Specific Implementation Rules:

**Store updates (CRITICAL):**
```javascript
// ❌ WRONG: Direct setState
useAppStore.setState({ users: newUsers })

// ✅ CORRECT: Store-specific method
useUserStore.getState().setUsers(newUsers)

// ✅ CORRECT: Store-specific method for settings
useSettingsStore.getState().updateSettings({ theme: 'dark' })

// ✅ CORRECT: Store-specific method for library
useLibraryStore.getState().setLibrary(newLibrary)
```

**Field naming (CRITICAL):**
```javascript
// ❌ WRONG: Legacy field names
activity.name = "Running"
activity.emoji = "🏃"

// ✅ CORRECT: Canonical field names
activity.text = "Running"
activity.icon = "🏃"

// ✅ CORRECT: Reading with fallbacks
const text = activity.text || activity.name || activity.title
const icon = activity.icon || activity.emoji
```

**Typography (Android compatibility):**
```javascript
// ❌ WRONG: Direct fontWeight on Android
<Text style={{ fontWeight: 'bold' }}>Hello</Text>

// ✅ CORRECT: Use Typography component
<Typography fontWeight="bold">Hello</Typography>
// Typography handles Android font variants automatically
```

### Example Implementation:
```javascript
// File: /src/services/sync/syncService.js

// Helper function to preserve icon fields
const preserveIconFields = (local, remote) => {
  // Use canonical field names
  const localIcon = local.icon || local.emoji
  const remoteIcon = remote.icon || remote.emoji

  // Prefer newer, fallback to either
  const preservedIcon = remote.icon || localIcon

  return {
    ...remote,
    icon: preservedIcon,
    // Remove legacy field
    emoji: undefined
  }
}

// Update conflict resolution
const resolveConflict = (local, remote) => {
  const resolved = preserveIconFields(local, remote)

  // Use store-specific method
  useUserStore.getState().setUsers(users =>
    users.map(u => u.id === resolved.id ? resolved : u)
  )

  return resolved
}
```

---

## Phase 4: Review

**Goal**: Peer review for edge cases and security check.

### Steps:

1. **Self-review first**
   - Re-read all changed files
   - Check for edge cases
   - Verify store update methods used
   - Confirm field naming correct

2. **Run validation commands**
   ```bash
   npm run typecheck
   npm test
   npm run lint
   ```

3. **Invoke peer-reviewer agent** (if available)
   - Provide context: "Review my changes for [feature/bug]"
   - Address feedback
   - Re-run validation after fixes

4. **Security check** (if applicable)
   - Handling user data? Verify encryption
   - External API calls? Verify authentication
   - User input? Verify sanitization

### Review Checklist:

**Code quality:**
- [ ] Follows project coding standards
- [ ] No debugging console.logs
- [ ] Clear variable/function names
- [ ] Comments for complex logic
- [ ] No copy-paste duplication

**StackMap conventions:**
- [ ] Store-specific update methods used (not `useAppStore.setState`)
- [ ] Field naming: `text`/`icon` (not `name`/`emoji`)
- [ ] Fallbacks included when reading fields
- [ ] Typography component used (not direct fontWeight)
- [ ] No gray text colors (use #000)

**Platform compatibility:**
- [ ] Shared code works on iOS, Android, Web
- [ ] Platform-specific code in correct files
- [ ] No platform-specific APIs in shared code (Alert.alert, etc.)
- [ ] FlexWrap on Android uses percentage widths

**Edge cases:**
- [ ] Null/undefined handling
- [ ] Empty array/object handling
- [ ] Backwards compatibility with old data
- [ ] Migration path for legacy fields

**Testing:**
- [ ] Tests cover main functionality
- [ ] Tests cover edge cases
- [ ] Tests pass (`npm test`)
- [ ] Type checking passes (`npm run typecheck`)

### Example Review Issues:

**Issue 1: Direct state update**
```javascript
// ❌ Found during review
useAppStore.setState({ users: updatedUsers })

// ✅ Fixed
useUserStore.getState().setUsers(updatedUsers)
```

**Issue 2: Missing fallback**
```javascript
// ❌ Found during review
<Text>{activity.text}</Text>  // Will break for legacy data

// ✅ Fixed
<Text>{activity.text || activity.name || activity.title}</Text>
```

**Issue 3: Edge case not handled**
```javascript
// ❌ Found during review
const firstActivity = activities[0]  // Crashes if empty

// ✅ Fixed
const firstActivity = activities.length > 0 ? activities[0] : null
if (!firstActivity) return null
```

---

## Phase 5: Deploy

**Goal**: Run full test suite and deploy via quality script.

### Steps:

1. **Update PENDING_CHANGES.md**
   ```markdown
   ## Title: Fix sync icon preservation
   ### Changes Made:
   - Updated conflict resolution to preserve icon fields
   - Added deep merge for nested objects
   - Migrated legacy emoji field to icon
   - Added tests for icon preservation
   ```

2. **Run full validation**
   ```bash
   npm run typecheck
   npm test
   npm run lint
   ```

3. **Deploy using quality script**
   ```bash
   # For QUAL (local testing)
   ./scripts/deploy.sh qual --all

   # For STAGE (internal validation)
   ./scripts/deploy.sh stage --all

   # For BETA (closed testing)
   ./scripts/deploy.sh beta --all

   # For PROD (production)
   ./scripts/deploy.sh prod --all
   ```

4. **Verify deployment**
   - Check deployment output for errors
   - Verify version incremented
   - Test on target environment

### Deployment Checklist:

**Pre-deployment:**
- [ ] `PENDING_CHANGES.md` updated with clear description
- [ ] All tests pass (`npm test`)
- [ ] Type checking passes (`npm run typecheck`)
- [ ] No linting errors (`npm run lint`)
- [ ] Working directory clean (no uncommitted changes for beta/prod)

**Deployment:**
- [ ] Use deployment script (NOT manual git commands)
- [ ] Choose correct tier (qual/stage/beta/prod)
- [ ] Platform specified if not deploying all (--web, --ios, --android)

**Post-deployment:**
- [ ] Deployment succeeded (no errors in output)
- [ ] Version incremented correctly
- [ ] Changes visible in deployed environment
- [ ] No rollbacks needed

### Quality Gates (Enforced by deploy script):

The deployment script automatically enforces:
- ✅ All tests pass (no skipping without approval)
- ✅ TypeScript type checking passes
- ✅ Build succeeds
- ✅ Clean commit with message from `PENDING_CHANGES.md`
- ✅ Version auto-incremented

**If tests fail**: Fix them. Don't skip tests.
**If type checking fails**: Fix type errors. Don't bypass.
**If build fails**: Debug build issues. Don't commit broken code.

### Example Deployment:

```bash
# 1. Update PENDING_CHANGES.md
## Title: Fix activity icon preservation during sync conflicts
### Changes Made:
- Updated syncService conflict resolution to preserve icon fields
- Added deep merge utility for nested object conflicts
- Migrated legacy emoji field to canonical icon field
- Added test coverage for icon preservation scenarios
- Updated dataNormalizer with emoji→icon migration logic

# 2. Run validation
npm run typecheck  # ✅ Pass
npm test          # ✅ Pass

# 3. Deploy to QUAL for testing
./scripts/deploy.sh qual --all

# Output:
# ✅ Type checking: Pass
# ✅ Tests: Pass (15/15)
# ✅ Build: Success
# ✅ Version: 2025.01.18 → 2025.01.19
# ✅ Deployed: qual-api.stackmap.app
```

---

## Success Indicators

### You've succeeded when:
- ✅ Task completed in < 2 hours
- ✅ All 5 phases completed (no skipping)
- ✅ Tests pass
- ✅ Peer review approved (no major issues)
- ✅ Deployed without rollback
- ✅ Edge cases covered
- ✅ StackMap conventions followed

### You need to escalate to Full workflow if:
- ⚠️ Scope expanded to 6+ files
- ⚠️ Security concerns emerged
- ⚠️ Formal requirements needed
- ⚠️ Cross-platform issues more complex than expected

---

## Common Pitfalls

### ❌ Don't Do This:
- Skip research phase ("I know where the bug is")
- Skip planning ("I'll figure it out as I code")
- Skip review phase ("It's a small change")
- Skip deployment script ("Manual commit is faster")
- Use `useAppStore.setState()` directly
- Use legacy field names (`activity.name`, `activity.emoji`)
- Add console.logs without removing them
- Skip platform testing for shared code

### ✅ Do This Instead:
- Complete all 5 phases (they're quick for Standard tier)
- Use store-specific update methods
- Use canonical field names with fallbacks
- Remove debug logs or wrap in `__DEV__`
- Test on all platforms if changing shared code
- Use deployment script for quality gates

---

## Resources

- **Research patterns**: See `resources/research-patterns.md`
- **StackMap conventions**: See `/CLAUDE.md`
- **Platform gotchas**: See `/docs/platform/`
- **Store architecture**: See `/docs/STORE_ARCHITECTURE.md`
- **Field conventions**: See `/docs/features/field-conventions.md`

---

## Example: Full Standard Workflow

### Task: "Fix bug where activity icons are lost during sync conflicts"

#### Phase 1: Research (10 min)
```bash
# Find sync-related files
grep -r "resolveConflict" src/
grep -r "icon" src/services/sync/

# Files found:
# - /src/services/sync/syncService.js (conflict resolution)
# - /src/services/sync/syncStoreIntegration.js (store updates)
# - /src/utils/dataNormalizer.js (field normalization)
```

**Understanding:**
- Conflict resolution uses `Object.assign`, overwrites nested fields
- Icons stored as both `icon` (new) and `emoji` (legacy)
- Current code doesn't preserve icon during conflicts

#### Phase 2: Plan (5 min)
**Solution:**
1. Update `resolveConflict()` to deep-merge objects
2. Add `preserveIconFields()` helper
3. Migrate `emoji` → `icon` in normalizer

**Files to change:**
- `syncService.js` - add icon preservation
- `dataNormalizer.js` - add migration
- `syncService.test.js` - add tests

#### Phase 3: Implement (20 min)
```javascript
// syncService.js
const preserveIconFields = (local, remote) => {
  const icon = remote.icon || local.icon || local.emoji
  return { ...remote, icon, emoji: undefined }
}

const resolveConflict = (local, remote) => {
  const resolved = preserveIconFields(local, remote)

  // Use store-specific method
  useActivityStore.getState().updateActivity(resolved)

  return resolved
}

// Add tests
test('preserves icon during conflict', () => {
  const local = { id: 1, text: 'Run', icon: '🏃' }
  const remote = { id: 1, text: 'Running' }  // missing icon

  const result = resolveConflict(local, remote)
  expect(result.icon).toBe('🏃')
})
```

#### Phase 4: Review (10 min)
**Self-review checklist:**
- ✅ Store-specific method used (updateActivity)
- ✅ Field naming correct (icon, not emoji)
- ✅ Fallback included (icon || emoji)
- ✅ Tests added
- ✅ No console.logs

**Run validation:**
```bash
npm run typecheck  # ✅ Pass
npm test          # ✅ Pass (16/16)
```

#### Phase 5: Deploy (5 min)
```bash
# Update PENDING_CHANGES.md
## Title: Fix activity icon preservation during sync conflicts
### Changes Made:
- Updated conflict resolution to preserve icon fields
- Added deep merge for nested objects
- Migrated legacy emoji to icon field
- Added test coverage

# Deploy
./scripts/deploy.sh qual --all
# ✅ Deployed successfully
```

**Total time: ~50 minutes** ✅

---

## Summary

The Standard workflow is your **daily driver** for most development tasks. It provides the right balance of:
- **Rigor**: All 5 phases ensure quality
- **Speed**: Completed in 30-60 minutes
- **Flexibility**: Can escalate to Full if needed

When in doubt, **choose Standard workflow** - it's correct for 80% of tasks.

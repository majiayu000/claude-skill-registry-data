---
name: cloudkit-debugging
description: CloudKit sync and sharing debugging specialist. Use when encountering CloudKit sync issues, schema problems, sharing bugs, or CKRecord errors.
allowed-tools: Read, Grep, Glob, Bash(git:*)
---

# CloudKit Debugging Skill

This skill activates when you're working with CloudKit sync, sharing, schema, or CKRecord operations.

## When This Skill Activates

Trigger this skill when the conversation involves:
- CloudKit sync failures or conflicts
- CKShare and sharing issues
- CloudKit schema or record type problems
- Change token management
- Zone operations
- Public/private database issues
- CloudKit quota or performance issues
- CKRecord field mapping errors

## CloudKit Context for Cauldron

### Container Setup
- **Container ID:** `iCloud.Nadav.Cauldron`
- **Zones:** Custom zones per feature (recipes, collections, connections)
- **Databases:** Private (user data) + Public (shared recipes)

### Key Files to Check
- `Cauldron/Core/Services/CloudKitService.swift` - Main CloudKit operations (2,266 LOC)
- `Cauldron/Core/Services/RecipeSyncService.swift` - Recipe synchronization
- `Cauldron/Core/Persistence/*Repository.swift` - SwiftData ↔ CloudKit mapping
- `Cauldron/Core/Services/ImageManager.swift` - CKAsset handling

### Common Cauldron CloudKit Patterns
- SwiftData models map to `CD_*` record types
- Actors for thread-safe CloudKit operations
- Manual sync triggers (no automatic background sync)
- CKAssets for images (recipes, profiles, collections)
- CloudKit sharing for collaborative collections

## Debugging Process

### 1. Identify the Issue Category

**Sync Issues:**
- Records not syncing
- Conflicts and overwrites
- Change tokens not working
- Deleted items reappearing

**Sharing Issues:**
- Share creation fails
- Participants can't access shared data
- Permission errors
- Share acceptance problems

**Schema Issues:**
- Record type mismatches
- Missing fields
- Type conversion errors
- Index problems

**Performance Issues:**
- Slow queries
- Quota exceeded
- Batch operation failures
- Network timeout

### 2. Read Relevant Code

Always start by reading:
1. The CloudKit service implementation
2. The repository for the affected record type
3. Recent git changes related to CloudKit

```bash
git log --oneline --grep="CloudKit\|sync\|share" -20
```

### 3. Check for Common Issues

**Change Token Problems:**
```swift
// Look for: Are change tokens being saved?
// Look for: Is fetchChanges using the right token?
// Look for: Are tokens reset when needed?
```

**Record Type Mismatches:**
```swift
// SwiftData model: Recipe
// CloudKit record type: CD_Recipe
// Check: Do field names match?
// Check: Are types compatible (String, Int, Date, Data)?
```

**Zone Configuration:**
```swift
// Check: Is the custom zone created before use?
// Check: Are operations using the correct zone?
// Check: Is the zone subscription active?
```

**Share Record Handling:**
```swift
// Check: Is CKShare created with correct rootRecord?
// Check: Are participants added properly?
// Check: Is share record saved to public database?
```

### 4. Diagnostic Questions to Answer

Ask yourself:
- ✓ Is this happening in development, production, or both?
- ✓ Is it affecting all users or just some?
- ✓ What CloudKit database (private/public/shared)?
- ✓ What record types are involved?
- ✓ Are there any CloudKit errors in console logs?
- ✓ When did this start happening? (git blame)

### 5. Common CloudKit Errors & Solutions

**`CKError.serverRecordChanged`**
- **Cause:** Conflict - record modified elsewhere
- **Solution:** Implement conflict resolution, use change tags

**`CKError.zoneNotFound`**
- **Cause:** Custom zone not created or deleted
- **Solution:** Create zone before operations, handle zone deletion

**`CKError.unknownItem`**
- **Cause:** Record doesn't exist
- **Solution:** Check record existence before fetch/delete

**`CKError.partialFailure`**
- **Cause:** Batch operation partially failed
- **Solution:** Parse itemResults, retry failed items

**`CKError.quotaExceeded`**
- **Cause:** User's iCloud quota full
- **Solution:** Alert user, implement cleanup strategy

**`CKError.networkFailure`/`networkUnavailable`**
- **Cause:** No internet or CloudKit unavailable
- **Solution:** Queue operations, retry with backoff

### 6. Investigation Checklist

For sync issues:
```
□ Check change token persistence
□ Verify fetchChanges logic
□ Look for race conditions (actor isolation)
□ Check deleted item tracking (tombstones)
□ Verify record save order (dependencies)
□ Check predicate safety
```

For sharing issues:
```
□ Verify CKShare creation
□ Check rootRecord reference
□ Confirm public database save
□ Verify participant permissions
□ Check share URL generation
□ Test share acceptance flow
```

For schema issues:
```
□ Compare SwiftData model to CloudKit record type
□ Verify field name mappings
□ Check data type compatibility
□ Confirm required fields exist
□ Validate index configuration
```

## CloudKit Best Practices for Cauldron

### Record Operations
```swift
// ✅ DO: Use actors for thread safety
actor CloudKitService {
    func save(_ record: CKRecord) async throws { }
}

// ✅ DO: Batch operations when possible
let operation = CKModifyRecordsOperation(recordsToSave: records)

// ✅ DO: Handle partial failures
if case .partialFailure(let error) = ckError.code {
    // Process error.userInfo[CKPartialErrorsByItemIDKey]
}

// ❌ DON'T: Make CloudKit calls on main thread
// ❌ DON'T: Ignore CKError.serverRecordChanged
// ❌ DON'T: Save without checking quota first
```

### Change Tracking
```swift
// ✅ DO: Persist change tokens
UserDefaults.standard.set(changeToken, forKey: "zoneChangeToken")

// ✅ DO: Handle moreComing flag
if changesResponse.moreComing {
    await fetchChanges(from: changesResponse.changeToken)
}

// ❌ DON'T: Forget to update token after successful fetch
// ❌ DON'T: Use same token across different zones
```

### Sharing
```swift
// ✅ DO: Set share permissions explicitly
share[CKShare.SystemFieldKey.title] = "Recipe Collection"
share.publicPermission = .readOnly

// ✅ DO: Save share and root record atomically
let operation = CKModifyRecordsOperation(
    recordsToSave: [rootRecord, share]
)

// ❌ DON'T: Modify shared records without permission check
// ❌ DON'T: Share records across different zones
```

## Debugging Tools

### Console Logging
Add CloudKit debug logging:
```swift
// In CloudKitService
#if DEBUG
print("☁️ CloudKit: Fetching \(recordType) from \(database)")
#endif
```

### CloudKit Dashboard
Check at: https://icloud.developer.apple.com/dashboard
- Verify schema matches code
- Check record counts
- View recent operations
- Monitor quota usage

### Xcode Console Filters
Use these console filters:
- `CloudKit` - All CloudKit operations
- `CKError` - CloudKit errors only
- `CD_Recipe` - Specific record type operations

## Output Format

When providing CloudKit debugging help:

1. **Identify the Issue** - State what CloudKit problem you found
2. **Show Relevant Code** - Reference specific files and lines
3. **Explain Root Cause** - Why is this happening?
4. **Provide Solution** - Code fix with explanation
5. **Prevent Recurrence** - Best practice to avoid this in future

Example:
```
🔍 **Issue Found:** CloudKit sync conflict in RecipeSyncService.swift:145

**Root Cause:** The service doesn't handle CKError.serverRecordChanged,
causing sync to fail when the recipe was modified on another device.

**Solution:** Implement conflict resolution using change tags...

**Prevention:** Always handle serverRecordChanged errors with merge strategy.
```

## Remember

CloudKit debugging is systematic:
1. Read the error carefully
2. Check the code path
3. Verify CloudKit schema
4. Test incrementally
5. Use CloudKit Dashboard to validate

You have deep knowledge of Cauldron's CloudKit architecture - use it to solve problems quickly and thoroughly.

---
name: firebase-deployer
description: Deploy Firebase Firestore security rules and indexes automatically. Use when Firestore query errors mention "requires an index", when firestore.rules or firestore.indexes.json are modified, or when user requests Firebase deployment.
allowed-tools: Bash, Read, Edit
---

# Firebase Deployer

## When to Use

Activate this skill when:
- Firestore query errors indicate missing indexes
- User modifies `firestore.rules` or `firestore.indexes.json`
- User requests "deploy firebase rules" or "deploy indexes"
- Error messages mention "FAILED_PRECONDITION" or "composite index"
- User says "deploy firebase", "push rules", or "update firestore"
- New Firestore queries need composite indexes
- Security rules need updating for new features

## Instructions

### Step 1: Identify What Needs Deployment

1. Check for modified files:
```bash
git status | grep -E "(firestore.rules|firestore.indexes.json)"
```

2. If query error occurred, extract index requirements from error message:
   - Collection name
   - Fields being queried
   - Order direction (ASCENDING/DESCENDING)
   - Query filters (array-contains, etc.)

### Step 2: Update Index Configuration (if needed)

If missing index detected:

1. Read current indexes:
```bash
cat firestore.indexes.json
```

2. Add new index to `firestore.indexes.json`:
```json
{
  "indexes": [
    {
      "collectionGroup": "collection_name",
      "queryScope": "COLLECTION",
      "fields": [
        {
          "fieldPath": "field1",
          "order": "ASCENDING"
        },
        {
          "fieldPath": "field2",
          "order": "DESCENDING"
        }
      ]
    }
  ]
}
```

### Step 3: Verify Firebase Project

1. Check current project:
```bash
firebase use
```

2. If project not set or wrong project:
```bash
firebase use project-id
```

3. Verify configuration:
```bash
firebase projects:list
```

### Step 4: Deploy Rules and Indexes

Deploy both rules and indexes together:
```bash
firebase deploy --only firestore:rules,firestore:indexes
```

Or deploy separately:
```bash
# Deploy only indexes
firebase deploy --only firestore:indexes

# Deploy only rules
firebase deploy --only firestore:rules
```

### Step 5: Verify Deployment

1. Check index status:
```bash
firebase firestore:indexes
```

2. Monitor index building (can take several minutes):
   - Indexes show as "Building" initially
   - Check Firebase Console for progress
   - Wait for "Ready" status before querying

3. Test the query that triggered the error

## Examples

### Example 1: Deploy After Query Error

```bash
# Error received:
# "The query requires an index. You can create it here: https://console.firebase.google.com/..."

# Step 1: Extract index requirements from error URL
# Collection: posts
# Fields: userId (ASCENDING), createdAt (DESCENDING)

# Step 2: Update firestore.indexes.json
# (use Edit tool to add index)

# Step 3: Deploy
firebase deploy --only firestore:indexes

# Step 4: Verify
firebase firestore:indexes
```

### Example 2: Deploy Modified Security Rules

```bash
# User modified firestore.rules to add new collection rules

# Step 1: Verify changes
cat firestore.rules

# Step 2: Deploy rules only
firebase deploy --only firestore:rules

# Step 3: Verify in console
# Check Firebase Console > Firestore > Rules
```

### Example 3: Deploy Both Rules and Indexes

```bash
# User updated both rules and indexes

# Deploy together for consistency
firebase deploy --only firestore:rules,firestore:indexes

# Verify both
firebase firestore:indexes
# Check console for rules
```

### Example 4: Multi-Project Deployment

```bash
# Deploy to specific project
firebase deploy --only firestore:rules,firestore:indexes --project production-id

# Switch project for subsequent deploys
firebase use staging-id
firebase deploy --only firestore:rules,firestore:indexes
```

## Best Practices

### ✅ DO:
- Always verify current Firebase project before deploying
- Deploy rules and indexes together when both changed
- Test queries after index deployment completes
- Check index status after deployment
- Read error messages carefully to extract index requirements
- Deploy to staging environment first (if available)
- Wait for indexes to finish building before testing
- Keep firestore.indexes.json in version control

### ❌ DON'T:
- Don't deploy without checking current project
- Don't assume indexes are ready immediately (they build asynchronously)
- Don't deploy rules that could break production
- Don't ignore index URL in error messages (contains exact requirements)
- Don't delete indexes still in use by queries
- Don't deploy without reviewing changes first
- Don't forget to commit firestore.indexes.json after adding indexes

### Index Configuration Tips:

1. **Query Scope**:
   - `COLLECTION`: Index for specific collection
   - `COLLECTION_GROUP`: Index across all collections with same name

2. **Field Order**:
   - List fields in query order
   - Use `ASCENDING` or `DESCENDING` to match query
   - Array-contains queries need special handling

3. **Compound Indexes**:
   - Required for queries with multiple filters
   - Required for orderBy on different field than filter
   - Required for inequality filters on multiple fields

4. **Index Exemptions**:
   - Single field ascending/descending: Auto-indexed
   - Simple equality queries: Usually auto-indexed
   - Check Firestore docs for exemption list

### Security Rules Best Practices:

1. **Default Deny**:
```javascript
match /{document=**} {
  allow read, write: if false;
}
```

2. **Authenticated Users**:
```javascript
match /users/{userId} {
  allow read, write: if request.auth != null && request.auth.uid == userId;
}
```

3. **Field Validation**:
```javascript
match /posts/{postId} {
  allow create: if request.auth != null
    && request.resource.data.title is string
    && request.resource.data.title.size() <= 100;
}
```

## Deployment Checklist

Before deploying:
- [ ] Verified correct Firebase project
- [ ] Reviewed changes to rules/indexes
- [ ] Tested rules in Firebase Console simulator (if changed)
- [ ] No breaking changes to production queries
- [ ] Index configuration matches query requirements
- [ ] Have backup of previous rules (git history)

After deploying:
- [ ] Verified deployment success message
- [ ] Checked index status (building/ready)
- [ ] Tested queries that use new indexes
- [ ] Monitored for errors in Firebase Console
- [ ] Committed firestore.indexes.json changes

## Troubleshooting

**Issue**: "Project not found" error
**Solution**: Run `firebase use project-id` or `firebase projects:list`

**Issue**: "Permission denied" during deployment
**Solution**: Re-authenticate with `firebase login` or check IAM roles

**Issue**: Index still showing as "Building" after long time
**Solution**: Normal for large collections. Check Firebase Console for progress.

**Issue**: Query still failing after index deployment
**Solution**: Verify index matches exact query requirements (field order, direction)

**Issue**: Rules deployment breaks existing queries
**Solution**: Review rules for overly restrictive conditions. Test in simulator first.

**Issue**: Multiple index errors for same query
**Solution**: Create single composite index with all required fields

## Firebase CLI Commands Reference

```bash
# Project management
firebase projects:list                    # List all projects
firebase use project-id                   # Switch to project
firebase use --add                        # Add project alias

# Deployment
firebase deploy --only firestore:rules    # Deploy rules only
firebase deploy --only firestore:indexes  # Deploy indexes only
firebase deploy --only firestore          # Deploy both

# Index management
firebase firestore:indexes                # List all indexes
firebase firestore:indexes --status       # Show build status

# Verification
firebase use                              # Show current project
firebase projects:list                    # Verify project access

# Authentication
firebase login                            # Re-authenticate
firebase logout                           # Sign out
firebase login:list                       # List authenticated accounts
```

## Integration with Development Workflow

1. **During Development**:
   - Write Firestore queries
   - Note index errors
   - Add indexes to firestore.indexes.json
   - Deploy immediately

2. **Before Committing**:
   - Ensure all indexes deployed
   - Verify rules match new features
   - Test queries in development

3. **Before Production Deploy**:
   - Deploy indexes to production first
   - Wait for indexes to build
   - Then deploy application code
   - Verify queries work in production

## Error Message Patterns

Common error messages that trigger this skill:

1. **Missing Index**:
```
The query requires an index. You can create it here: https://...
```

2. **Failed Precondition**:
```
FAILED_PRECONDITION: The query requires an index...
```

3. **Permission Denied** (rules issue):
```
Missing or insufficient permissions
```

4. **Invalid Argument**:
```
Cannot have inequality filters on multiple properties
```

Extract index requirements and deploy accordingly.

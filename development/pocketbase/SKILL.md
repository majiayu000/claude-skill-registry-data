---
name: pocketbase-api-add-field
description: This skill should be used when the user asks to "add fields to PocketBase collection", "modify PocketBase schema", "add new collection fields", "update PocketBase collection", "PocketBase JavaScript SDK API", "programmatically add PocketBase fields", or mentions modifying PocketBase collection schemas via API. Provides comprehensive guidance for adding fields to existing PocketBase collections using the JavaScript SDK API.
version: 0.1.0
---

# PocketBase API Add Field

This skill provides comprehensive guidance for programmatically adding fields to existing PocketBase collections using the JavaScript SDK API. It enables developers to modify collection schemas without using the Admin UI, making it ideal for automated migrations, deployment scripts, and programmatic database schema updates.

## When to Use This Skill

Use this skill when you need to:
- Add new fields to existing PocketBase collections programmatically
- Create automated schema migration scripts
- Update collection schemas without using the Admin UI
- Implement field additions in deployment pipelines
- Perform bulk schema modifications across multiple collections
- Integrate schema changes into custom applications or tools

## Prerequisites

### Install PocketBase JavaScript SDK

Install the PocketBase SDK if not already available:

```bash
npm install pocketbase
```

### Initialize PocketBase Client

```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');
```

### Admin Authentication

Schema modifications require admin privileges. Authenticate using one of these methods:

```javascript
// Method 1: Admin credentials
await pb.admins.authWithPassword('admin@example.com', 'your-admin-password');

// Method 2: Existing admin token
pb.authStore.save('your-admin-token');
```

## Core Workflow

### Step 1: Get Current Collection Schema

Retrieve the existing collection to understand current schema:

```javascript
async function getCollectionSchema(collectionNameOrId) {
  const collection = await pb.collections.getOne(collectionNameOrId);
  return collection;
}
```

### Step 2: Define New Fields

Create field definitions following PocketBase field schema format:

```javascript
const newFields = [
  {
    name: 'bio',
    type: 'text',
    required: false,
    options: {
      max: 1000
    }
  },
  {
    name: 'avatar',
    type: 'file',
    required: false,
    options: {
      maxSelect: 1,
      maxSize: 5242880, // 5MB
      mimeTypes: ['image/jpeg', 'image/png', 'image/webp']
    }
  }
];
```

### Step 3: Add Fields to Schema

Merge new fields with existing schema and update collection:

```javascript
async function addFieldsToCollection(collectionId, newFields) {
  const collection = await pb.collections.getOne(collectionId);

  // Add new fields to existing schema
  const updatedSchema = [...collection.schema, ...newFields];

  // Update collection
  const updatedCollection = await pb.collections.update(collectionId, {
    name: collection.name,
    schema: updatedSchema
  });

  return updatedCollection;
}
```

### Step 4: Verify Changes

Confirm the schema was updated successfully:

```javascript
async function verifySchemaChanges(collectionId, expectedFields) {
  const collection = await pb.collections.getOne(collectionId);
  const fieldNames = collection.schema.map(field => field.name);

  return expectedFields.every(field => fieldNames.includes(field));
}
```

## Complete Implementation Example

```javascript
import PocketBase from 'pocketbase';

async function addFieldsToUsersCollection() {
  const pb = new PocketBase('http://127.0.0.1:8090');

  try {
    // Authenticate as admin
    await pb.admins.authWithPassword('admin@example.com', 'your-admin-password');

    // Get current users collection
    const usersCollection = await pb.collections.getOne('users');

    // Define new fields
    const newFields = [
      {
        name: 'bio',
        type: 'text',
        required: false,
        options: {
          max: 1000
        }
      },
      {
        name: 'is_active',
        type: 'bool',
        required: false,
        default: true
      },
      {
        name: 'date_of_birth',
        type: 'date',
        required: false
      }
    ];

    // Add fields to schema
    const updatedSchema = [...usersCollection.schema, ...newFields];

    // Update collection
    const updatedCollection = await pb.collections.update(usersCollection.id, {
      name: usersCollection.name,
      schema: updatedSchema
    });

    console.log('Fields added successfully!');
    return updatedCollection;

  } catch (error) {
    console.error('Error adding fields:', error);
    throw error;
  } finally {
    pb.authStore.clear();
  }
}
```

## Field Type Examples

Common field configurations for different data types:

### Text Fields

```javascript
{
  name: 'full_name',
  type: 'text',
  required: true,
  options: {
    min: 1,
    max: 100
  }
}
```

### Email Fields

```javascript
{
  name: 'secondary_email',
  type: 'email',
  required: false
}
```

### Number Fields

```javascript
{
  name: 'age',
  type: 'number',
  required: false,
  options: {
    min: 0,
    max: 150
  }
}
```

### Select Fields

```javascript
{
  name: 'status',
  type: 'select',
  required: true,
  options: {
    values: ['active', 'inactive', 'pending']
  }
}
```

### Relation Fields

```javascript
{
  name: 'team',
  type: 'relation',
  required: false,
  options: {
    collectionId: 'teams_collection_id',
    maxSelect: 1
  }
}
```

## Error Handling & Best Practices

### Validate Field Names

Check for conflicts with existing fields:

```javascript
function validateFieldNames(newFields, existingSchema) {
  const existingNames = existingSchema.map(field => field.name);
  const conflicts = newFields.filter(field => existingNames.includes(field.name));

  if (conflicts.length > 0) {
    throw new Error(`Field name conflicts: ${conflicts.map(f => f.name).join(', ')}`);
  }
}
```

### Safe Field Addition

Backup and restore schema on failure:

```javascript
async function safeFieldAddition(collectionId, newFields) {
  const originalCollection = await pb.collections.getOne(collectionId);

  try {
    await pb.admins.authWithPassword('admin@example.com', 'password');

    // Validate no conflicts
    validateFieldNames(newFields, originalCollection.schema);

    // Add fields
    const updatedSchema = [...originalCollection.schema, ...newFields];
    await pb.collections.update(collectionId, {
      name: originalCollection.name,
      schema: updatedSchema
    });

  } catch (error) {
    // Restore original schema on failure
    await pb.collections.update(collectionId, {
      name: originalCollection.name,
      schema: originalCollection.schema
    });
    throw error;
  }
}
```

### Authentication Cleanup

Always clean up authentication state:

```javascript
try {
  // Your schema modification logic
} catch (error) {
  console.error('Schema modification failed:', error);
  throw error;
} finally {
  pb.authStore.clear();
}
```

## Additional Resources

### Reference Files

- **`references/field-types.md`** - Complete field type reference with all options
- **`references/advanced-patterns.md`** - Advanced schema modification patterns
- **`references/error-handling.md`** - Comprehensive error handling strategies

### Examples

- **`examples/basic-field-addition.js`** - Simple field addition example
- **`examples/batch-schema-update.js`** - Multiple fields and collections
- **`examples/migration-script.js`** - Production migration script template

### Scripts

- **`scripts/validate-schema.js`** - Schema validation utility
- **`scripts/backup-restore.js`** - Schema backup and restore helper
- **`scripts/field-conflict-check.js`** - Field name conflict detection

## Key Points

1. **Admin Authentication Required** - Collection schema changes require admin privileges
2. **Get Current Schema First** - Never assume the current state of the collection
3. **Validate Field Names** - Ensure no conflicts with existing fields
4. **Handle Errors Gracefully** - Consider rolling back changes if something fails
5. **Clean Up Authentication** - Clear auth state when done
6. **Test Thoroughly** - Verify the schema changes work as expected before production use

This approach provides complete programmatic control over PocketBase collection schemas, enabling automated migrations and deployment workflows.
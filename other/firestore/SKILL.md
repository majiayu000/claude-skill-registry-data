---
name: firestore
description: Query and manage Google Firestore databases. Use TypeScript scripts for typed access or REST API via curl. Ideal for Firebase/GCP projects.
version: 1.0.0
allowed-tools: Bash, Read
metadata:
  credentials:
    - GOOGLE_APPLICATION_CREDENTIALS_JSON
    - FIREBASE_PROJECT_ID
---

# Firestore Skill

Query and manage Google Firestore databases using TypeScript scripts or the REST API.

## Quick Start

```bash
# Using the included scripts (recommended)
cd .claude/skills/firestore/scripts && bun install && cd -

# List collections
bun run .claude/skills/firestore/scripts/fs-list.ts

# Get a document
bun run .claude/skills/firestore/scripts/fs-get.ts users/user123

# Query a collection
bun run .claude/skills/firestore/scripts/fs-query.ts users status active
```

## Prerequisites

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | Service account key JSON (stringified) | `{"type":"service_account",...}` |
| `FIREBASE_PROJECT_ID` | Firebase/GCP project ID | `my-project-123` |

### First-Time Setup

```bash
cd .claude/skills/firestore/scripts && bun install && cd -
```

### Verify Connection

```bash
bun run .claude/skills/firestore/scripts/fs-list.ts
```

## TypeScript Script Recipes

### List Collections

```bash
bun run .claude/skills/firestore/scripts/fs-list.ts
```

### Get Document

```bash
# Get document by path
bun run .claude/skills/firestore/scripts/fs-get.ts users/user123

# Nested document
bun run .claude/skills/firestore/scripts/fs-get.ts users/user123/orders/order456
```

### Query Collection

```bash
# Query with single filter: collection field operator value
bun run .claude/skills/firestore/scripts/fs-query.ts users status == active

# Default operator is ==
bun run .claude/skills/firestore/scripts/fs-query.ts users role admin

# Numeric comparison
bun run .claude/skills/firestore/scripts/fs-query.ts orders amount '>' 100

# Limit results
bun run .claude/skills/firestore/scripts/fs-query.ts users status active --limit 10
```

### Set/Update Document

```bash
# Set document (creates or overwrites)
bun run .claude/skills/firestore/scripts/fs-set.ts users/user123 '{"name":"John","email":"john@example.com","status":"active"}'

# Merge (partial update — only updates specified fields)
bun run .claude/skills/firestore/scripts/fs-set.ts users/user123 '{"status":"inactive"}' --merge
```

## REST API Alternative

For environments without bun/npm, use the Firestore REST API directly.

### Get Document via REST

```bash
# Requires an OAuth2 access token (see Firebase Admin SDK docs)
curl -s "https://firestore.googleapis.com/v1/projects/$FIREBASE_PROJECT_ID/databases/(default)/documents/users/user123" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
```

### List Documents via REST

```bash
curl -s "https://firestore.googleapis.com/v1/projects/$FIREBASE_PROJECT_ID/databases/(default)/documents/users?pageSize=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.documents[]'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `PERMISSION_DENIED` | Service account lacks access | Check Firestore IAM permissions |
| `NOT_FOUND` | Document/collection doesn't exist | Verify path |
| `UNAUTHENTICATED` | Invalid credentials | Check GOOGLE_APPLICATION_CREDENTIALS_JSON |
| `Cannot find module` | Dependencies not installed | Run `cd .claude/skills/firestore/scripts && bun install` |
| `INVALID_ARGUMENT` | Query syntax error | Check field name and value types |

## Managed Service Setup

### Firebase/Firestore
1. Go to Firebase Console — Project Settings — Service accounts
2. Generate new private key — download JSON
3. Stringify the JSON and set as `GOOGLE_APPLICATION_CREDENTIALS_JSON`
4. Set `FIREBASE_PROJECT_ID` to your project ID

### Stringify JSON for env var

```bash
cat service-account.json | jq -c .
```

## Tips

- **Use the scripts** — they handle auth, formatting, and error handling
- **First run `fs-list.ts`** to discover available collections
- **Then `fs-get.ts`** to inspect individual documents
- **Use `--merge`** for partial updates to avoid overwriting entire documents
- **Firestore doesn't allow `undefined`** — use `null` or omit the field
- **Collection/document paths** alternate: `collection/document/subcollection/document`
- **REST API** is verbose but works without any npm dependencies

---
name: qashier-cli
description: Use the qashier-cli tool to manage Google OAuth authentication, switch between staging/production environments, and extract Firestore documents. Invoke when user mentions qashier-cli, authentication issues, environment switching, Firestore data extraction, or needs to verify auth status.
allowed-tools: Bash, Read, Write
---

# Qashier CLI

Use the `qashier-cli` tool to manage authentication and developer utilities for Qashier backend services.

## Overview

**qashier-cli v0.1.2** provides:
- Google OAuth authentication management
- Environment switching (staging/production)
- Firestore document extraction

**Alias**: `qashier` (can be used interchangeably with `qashier-cli`)

## When to Use This Skill

Invoke this skill when the user:
- Mentions `qashier-cli` or `qashier` command
- Has authentication issues or needs to login/logout
- Needs to switch between staging and production environments
- Wants to extract Firestore documents for debugging or testing
- Needs to check authentication status or current environment
- Is setting up local development with Qashier services

## Installation Check

Verify the CLI is available:

```bash
qashier-cli --version
```

Expected output: `qashier-cli v0.1.2`

## Command Reference

### Authentication Commands (`auth`)

#### `qashier-cli auth login`

Authenticate with Google via browser OAuth.

**When to use:**
- First-time setup
- After token expiration
- When switching Google accounts

**Example:**
```bash
qashier-cli auth login
```

Opens browser for Google OAuth authentication and stores tokens locally.

---

#### `qashier-cli auth logout`

Clear cached authentication tokens.

**When to use:**
- Switching to a different account
- Security cleanup
- Troubleshooting authentication issues

**Example:**
```bash
qashier-cli auth logout
```

---

#### `qashier-cli auth status`

Display current authentication and environment status.

**When to use:**
- Verify authentication state
- Check which environment is active
- Troubleshoot connection issues

**Example:**
```bash
qashier-cli auth status
# Output shows: Authentication status, Environment (staging/production), User email
```

---

#### `qashier-cli auth use <env>`

Set the active environment.

**Arguments:**
- `<env>`: `staging` or `production`

**When to use:**
- Switching between staging and production
- Testing in different environments

**Examples:**
```bash
# Switch to staging
qashier-cli auth use staging

# Switch to production
qashier-cli auth use production
```

⚠️ **Warning**: Always verify your active environment before making changes, especially when working with production.

---

### Developer Utilities (`dev`)

#### `qashier-cli dev extract-firestore <document-path> [--output <file>]`

Export a Firestore document to a local file.

**Arguments:**
- `<document-path>`: Firestore document path (e.g., `users/user123`, `orders/order456`)

**Options:**
- `--output <file>`: Output file path (optional, defaults to stdout)

**When to use:**
- Debugging production/staging data issues
- Creating test fixtures from real data
- Backing up specific documents
- Analyzing document structure

**Examples:**

```bash
# Extract to stdout
qashier-cli dev extract-firestore users/user123

# Extract to specific file
qashier-cli dev extract-firestore orders/order456 --output order-456.json

# Extract nested document
qashier-cli dev extract-firestore merchants/merchant123/settings/general --output general-settings.json
```

**Common patterns:**

```bash
# Extract and inspect
qashier-cli dev extract-firestore users/abc123 --output user.json
cat user.json | jq .

# Extract multiple documents
for id in user1 user2 user3; do
  qashier-cli dev extract-firestore "users/$id" --output "$id.json"
done

# Extract for test fixtures
qashier-cli dev extract-firestore config/feature-flags --output functions/test/fixtures/feature-flags.json
```

---

## Complete Workflows

### Initial Setup

```bash
# 1. Verify CLI is installed
qashier-cli --version

# 2. Authenticate with Google
qashier-cli auth login

# 3. Set environment to staging
qashier-cli auth use staging

# 4. Verify authentication status
qashier-cli auth status
```

### Environment Switching

```bash
# Check current environment
qashier-cli auth status

# Switch to production
qashier-cli auth use production

# Verify the switch
qashier-cli auth status

# Switch back to staging
qashier-cli auth use staging
```

### Data Extraction

```bash
# 1. Ensure you're authenticated
qashier-cli auth status

# 2. Set correct environment
qashier-cli auth use staging

# 3. Extract Firestore document
qashier-cli dev extract-firestore merchants/merchant123 --output merchant-data.json

# 4. Inspect the extracted data
cat merchant-data.json | jq .
```

### Troubleshooting Authentication

```bash
# 1. Check current status
qashier-cli auth status

# 2. If having issues, logout
qashier-cli auth logout

# 3. Login again
qashier-cli auth login

# 4. Verify authentication
qashier-cli auth status
```

---

## Best Practices

### Authentication

1. **Always verify your environment** before making changes:
   ```bash
   qashier-cli auth status
   ```

2. **Use staging for testing**:
   ```bash
   qashier-cli auth use staging
   ```

3. **Be cautious with production**:
   - Double-check environment before running commands
   - Prefer read-only operations (like `extract-firestore`)
   - Have explicit confirmation when targeting production

4. **Refresh tokens periodically**:
   ```bash
   qashier-cli auth logout
   qashier-cli auth login
   ```

### Data Extraction

1. **Always specify output file** for important data:
   ```bash
   qashier-cli dev extract-firestore <path> --output <file>.json
   ```

2. **Use descriptive filenames**:
   ```bash
   # Good
   qashier-cli dev extract-firestore users/abc123 --output user-abc123-2025-11-07.json

   # Less clear
   qashier-cli dev extract-firestore users/abc123 --output data.json
   ```

3. **Organize extracted data**:
   ```bash
   mkdir -p .local/firestore-data
   qashier-cli dev extract-firestore merchants/m123 --output .local/firestore-data/merchant-m123.json
   ```

4. **Verify extracted data** after export:
   ```bash
   qashier-cli dev extract-firestore users/u123 --output user.json && cat user.json | jq .
   ```

### Security

1. **Never commit authentication tokens** to version control
2. **Use staging for development** and testing
3. **Log out when done** with sensitive operations:
   ```bash
   qashier-cli auth logout
   ```
4. **Verify environment** before every operation that modifies data

---

## Common Issues & Solutions

### Issue: "Not authenticated"

**Solution:**
```bash
qashier-cli auth logout
qashier-cli auth login
```

### Issue: "Wrong environment"

**Solution:**
```bash
# Check current environment
qashier-cli auth status

# Switch to correct environment
qashier-cli auth use staging  # or production
```

### Issue: "Command not found: qashier-cli"

**Solution:**
```bash
# Check if CLI is installed globally
which qashier-cli

# If not found, check with your team for installation instructions
```

### Issue: "Document not found" when extracting Firestore document

**Solution:**
- Verify the document path is correct
- Check you're in the right environment (`qashier-cli auth status`)
- Ensure you have permissions to access the document
- Verify the document exists in Firestore console

---

## Integration with Project Workflows

### Local Development

When developing locally and need test data:

```bash
# 1. Authenticate and switch to staging
qashier-cli auth login
qashier-cli auth use staging

# 2. Extract test data from staging
qashier-cli dev extract-firestore merchants/test-merchant --output .local/test-merchant.json

# 3. Use the extracted data in your local tests or development
```

### Debugging Production Issues

When investigating production issues:

```bash
# 1. Verify you're in production
qashier-cli auth use production
qashier-cli auth status

# 2. Extract relevant documents for analysis
qashier-cli dev extract-firestore users/problematic-user --output debug-user-data.json
qashier-cli dev extract-firestore orders/failed-order --output debug-order-data.json

# 3. Analyze the data locally
cat debug-user-data.json | jq .
```

### Creating Test Fixtures

When creating test fixtures from real data:

```bash
# 1. Use staging environment
qashier-cli auth use staging

# 2. Extract documents
qashier-cli dev extract-firestore merchants/sample --output functions/test/fixtures/sample-merchant.json
qashier-cli dev extract-firestore transactions/sample --output functions/test/fixtures/sample-transaction.json

# 3. Sanitize sensitive data in the fixtures before committing
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `qashier-cli --version` | Show CLI version |
| `qashier-cli --help` | Show help message |
| `qashier-cli auth login` | Authenticate with Google OAuth |
| `qashier-cli auth logout` | Clear authentication tokens |
| `qashier-cli auth status` | Show authentication status |
| `qashier-cli auth use <env>` | Switch environment (staging/production) |
| `qashier-cli dev extract-firestore <path>` | Extract Firestore document |
| `qashier-cli dev extract-firestore <path> --output <file>` | Extract to file |

---

## Instructions for Claude

When helping users with qashier-cli:

1. **Always check authentication status first** before running commands that require auth
2. **Verify the environment** (staging/production) to prevent accidental changes to the wrong environment
3. **Use staging by default** unless explicitly told to use production
4. **Suggest descriptive output filenames** when extracting Firestore documents
5. **Remind users to verify** their environment when switching or before sensitive operations
6. **Provide complete workflows** rather than isolated commands
7. **Include error handling** and troubleshooting steps in suggestions
8. **Use the `qashier` alias** if the command is getting too verbose
9. **Warn about production operations** and suggest extra verification steps
10. **Organize extracted data** into appropriate directories (e.g., `.local/`, `test/fixtures/`)

---

*Version: 1.0 | Last updated: 2025-11-07*

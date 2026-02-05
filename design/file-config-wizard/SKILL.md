---
name: file-config-wizard
description: Interactive configuration wizard for the fractary-file plugin, guiding users through storage handler setup with validation
model: claude-haiku-4-5
---

# Config Wizard Skill

Interactive configuration wizard for the fractary-file plugin.

<CONTEXT>
You are the config-wizard skill for the fractary-file plugin. You guide users through interactive configuration setup with clear prompts, helpful examples, and validation. You support all 5 storage handlers (local, r2, s3, gcs, gdrive) and can operate in both interactive and non-interactive modes.
</CONTEXT>

<CRITICAL_RULES>
1. NEVER store credentials in plaintext without warning user about environment variables
2. ALWAYS recommend environment variables for sensitive data
3. ALWAYS test configuration before saving (unless test_connection=false)
4. NEVER proceed if validation fails without explicit user confirmation
5. ALWAYS set secure file permissions (0600) on config files
6. NEVER expose credentials in logs or outputs
7. ALWAYS validate handler-specific required fields
8. NEVER overwrite existing config without user confirmation
</CRITICAL_RULES>

<INPUTS>
Parameters:
- `config_scope`: "project" or "global" - where to save configuration
- `handlers`: comma-separated list of handler names, or null (prompts user if null)
  - Examples: "local", "local,s3", "r2,s3,gcs"
  - Single handler for backwards compatibility: "s3" → ["s3"]
- `interactive`: boolean - whether to prompt user or use defaults/env vars
- `test_connection`: boolean - whether to test connection before saving

Context:
- Current working directory
- Environment variables
- Existing configuration (if any)
</INPUTS>

<WORKFLOW>

## Phase 1: Initialization

### 1.1 Determine Configuration Path

Based on `config_scope`:
- **project**: `.fractary/plugins/file/config.json`
- **global**: `~/.config/fractary/file/config.json`

Check if configuration already exists:
```bash
if [ -f "$CONFIG_PATH" ]; then
    echo "⚠️  Configuration already exists at $CONFIG_PATH"
    if [ "$INTERACTIVE" = "true" ]; then
        read -p "Overwrite existing configuration? [y/N]: " OVERWRITE
        if [ "$OVERWRITE" != "y" ]; then
            echo "Configuration cancelled."
            exit 0
        fi
    fi
fi
```

### 1.2 Source Common Functions

Load shared utilities:
```bash
source plugins/file/skills/common/functions.sh
```

## Phase 2: Handler Selection

### 2.1 Parse Handlers Parameter

If `handlers` parameter is provided:
```bash
# Convert comma-separated list to array
IFS=',' read -ra HANDLER_LIST <<< "$HANDLERS"
```

If `handlers` parameter is null and interactive mode, prompt for selection:

### 2.2 Interactive Handler Selection

Display menu:
```
Which storage provider(s) would you like to configure?
(You can select multiple providers and choose a default later)

  1. Local Filesystem (default, no credentials needed)
  2. Cloudflare R2 (S3-compatible object storage)
  3. AWS S3 (Amazon S3 or S3-compatible services)
  4. Google Cloud Storage (GCS)
  5. Google Drive (via OAuth2)

Enter selection(s) [1-5], comma-separated (default: 1): _____
Examples:
  - "1" → Local only
  - "1,3" → Local and S3
  - "2,3,4" → R2, S3, and GCS
```

Parse selections and build handler array:
```bash
IFS=',' read -ra SELECTIONS <<< "$USER_INPUT"
HANDLER_LIST=()
for selection in "${SELECTIONS[@]}"; do
    case "$selection" in
        1) HANDLER_LIST+=("local") ;;
        2) HANDLER_LIST+=("r2") ;;
        3) HANDLER_LIST+=("s3") ;;
        4) HANDLER_LIST+=("gcs") ;;
        5) HANDLER_LIST+=("gdrive") ;;
        *) echo "Invalid selection: $selection" ;;
    esac
done
```

### 2.3 Non-Interactive Default

If non-interactive mode and handlers is null: default to "local"

### 2.4 Display Selected Handlers

Show confirmation:
```
📋 Selected storage providers:
───────────────────────────────────────
  ${HANDLER_LIST[@]}
───────────────────────────────────────
```

## Phase 3: Collect Configuration

**Loop through each handler** in `HANDLER_LIST` and collect configuration.

### 3.0 Initialize Configuration Storage

Initialize storage for all handler configs:
```bash
declare -A HANDLER_CONFIGS
HANDLER_CONFIGS_JSON="{}"
```

### 3.0.1 Loop Structure

For each handler in the handler list, collect configuration:
```bash
for HANDLER in "${HANDLER_LIST[@]}"; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Configuring: $HANDLER"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Execute handler-specific configuration section (3.1-3.5 below)
    case "$HANDLER" in
        "local")
            # Execute section 3.1
            ;;
        "r2")
            # Execute section 3.2
            ;;
        "s3")
            # Execute section 3.3
            ;;
        "gcs")
            # Execute section 3.4
            ;;
        "gdrive")
            # Execute section 3.5
            ;;
    esac

    # Store handler config in JSON object
    HANDLER_CONFIGS_JSON=$(echo "$HANDLER_CONFIGS_JSON" | jq \
        --arg handler "$HANDLER" \
        --argjson config "$HANDLER_CONFIG" \
        '.[$handler] = $config')
done
```

**Important**: Each handler configuration section (3.1-3.5) should set the `HANDLER_CONFIG` variable to a JSON object with that handler's configuration.

For each handler in the list, execute the corresponding configuration section below:

### 3.1 Local Handler Configuration

**Interactive prompts:**
```
📁 Local Filesystem Configuration
───────────────────────────────────────

Storage path (where files will be stored):
  Default: . (project root)
  Path: _____

Create directories automatically if they don't exist? [Y/n]: _____

Directory permissions (octal format):
  Default: 0755
  Permissions: _____
```

**Required fields:**
- `base_path`: string (default: "." - project root)
- `create_directories`: boolean (default: true)
- `permissions`: string (default: "0755")

**Non-interactive defaults:**
```json
{
  "base_path": ".",
  "create_directories": true,
  "permissions": "0755"
}
```

**Set HANDLER_CONFIG variable:**
```bash
HANDLER_CONFIG=$(cat <<EOF
{
  "base_path": "$BASE_PATH",
  "create_directories": $CREATE_DIRECTORIES,
  "permissions": "$PERMISSIONS"
}
EOF
)
```

### 3.2 R2 Handler Configuration

**Interactive prompts:**
```
☁️  Cloudflare R2 Configuration
───────────────────────────────────────

Cloudflare Account ID:
  Find at: https://dash.cloudflare.com/?to=/:account/r2
  Account ID: _____

R2 Bucket name: _____

🔐 Credentials
───────────────────────────────────────
We STRONGLY recommend using environment variables for credentials:

  export R2_ACCOUNT_ID="your-account-id"
  export R2_ACCESS_KEY_ID="your-access-key"
  export R2_SECRET_ACCESS_KEY="your-secret-key"

Then use: ${R2_ACCESS_KEY_ID} and ${R2_SECRET_ACCESS_KEY} in config

R2 Access Key ID (or ${VAR_NAME}):
  Default: ${R2_ACCESS_KEY_ID}
  Access Key: _____

R2 Secret Access Key (or ${VAR_NAME}):
  Default: ${R2_SECRET_ACCESS_KEY}
  Secret Key: _____

Public URL (optional, for serving public files):
  Example: https://pub-xxxxx.r2.dev
  Public URL: _____

Region (leave as 'auto' for R2):
  Default: auto
  Region: _____
```

**Required fields:**
- `account_id`: string or ${VAR}
- `bucket_name`: string
- `access_key_id`: string or ${VAR}
- `secret_access_key`: string or ${VAR}
- `region`: string (default: "auto")
- `public_url`: string or null (optional)

**Non-interactive behavior:**
Use environment variables with ${VAR} syntax:
```json
{
  "account_id": "${R2_ACCOUNT_ID}",
  "access_key_id": "${R2_ACCESS_KEY_ID}",
  "secret_access_key": "${R2_SECRET_ACCESS_KEY}",
  "bucket_name": "${R2_BUCKET_NAME}",
  "region": "auto",
  "public_url": "${R2_PUBLIC_URL:-}"
}
```

### 3.3 S3 Handler Configuration

**Step 1: Discover AWS Profiles**

Before prompting, discover available AWS profiles:
```bash
DISCOVERY=$(bash plugins/file/skills/config-wizard/scripts/discover-aws-profiles.sh)
PROJECT_NAME=$(echo "$DISCOVERY" | jq -r '.project_name')
DEPLOY_PROFILES=$(echo "$DISCOVERY" | jq -r '.deploy_profiles')
PROJECT_DEPLOY_PROFILES=$(echo "$DISCOVERY" | jq -r '.project_deploy_profiles')
```

**Step 2: Interactive prompts**
```
☁️  AWS S3 Configuration
───────────────────────────────────────

🔐 Authentication Method
───────────────────────────────────────
Choose authentication method:
  1. AWS Profile (recommended - uses profiles from ~/.aws/config)
  2. IAM roles (recommended in AWS environments like EC2/ECS)
  3. Access keys (via environment variables)

Selection [1-3] (default: 1): _____
```

**If option 1 (AWS Profile) selected:**

First, show discovered deployment profiles:
```bash
# Show project-related deploy profiles first (if any)
PROJECT_COUNT=$(echo "$PROJECT_DEPLOY_PROFILES" | jq 'length')

if [ "$PROJECT_COUNT" -gt 0 ]; then
  echo ""
  echo "📋 Discovered deployment profiles for '$PROJECT_NAME':"
  echo "───────────────────────────────────────"

  # Group by environment
  TEST_PROFILES=$(echo "$PROJECT_DEPLOY_PROFILES" | jq -r '.[] | select(.environment == "test") | .name')
  PROD_PROFILES=$(echo "$PROJECT_DEPLOY_PROFILES" | jq -r '.[] | select(.environment == "prod") | .name')

  if [ -n "$TEST_PROFILES" ]; then
    echo "  Test:"
    echo "$TEST_PROFILES" | while read profile; do
      echo "    • $profile"
    done
  fi

  if [ -n "$PROD_PROFILES" ]; then
    echo "  Production:"
    echo "$PROD_PROFILES" | while read profile; do
      echo "    • $profile"
    done
  fi

  echo ""
fi

# Show all deploy profiles (if more available)
TOTAL_DEPLOY=$(echo "$DEPLOY_PROFILES" | jq 'length')

if [ "$TOTAL_DEPLOY" -gt "$PROJECT_COUNT" ]; then
  echo "Other deployment profiles available:"
  echo "$DEPLOY_PROFILES" | jq -r '.[] | select(.project_related == false) | .name' | while read profile; do
    echo "  • $profile"
  done
  echo ""
fi
```

Then prompt for profile selection:
```
AWS Profile Selection
───────────────────────────────────────
Pattern: {system}-{subsystem}-{env}-deploy

Enter profile name (or press Enter to use 'default'): _____

Examples:
  • {project}-{component}-test-deploy
  • {project}-{component}-prod-deploy
  • default
```

**Suggested default based on discovery:**
- If project-related test-deploy profile found: suggest that
- Otherwise: suggest "default"

```bash
# Auto-suggest profile
SUGGESTED_PROFILE="default"

# Try to find project-related test-deploy profile
TEST_PROFILE=$(echo "$PROJECT_DEPLOY_PROFILES" | jq -r '.[] | select(.environment == "test") | .name' | head -n 1)

if [ -n "$TEST_PROFILE" ]; then
  SUGGESTED_PROFILE="$TEST_PROFILE"
fi

read -p "AWS Profile [$SUGGESTED_PROFILE]: " USER_PROFILE
PROFILE="${USER_PROFILE:-$SUGGESTED_PROFILE}"
```

**Get region from selected profile:**
```bash
# Look up region for selected profile
PROFILE_REGION=$(echo "$DEPLOY_PROFILES" | jq -r --arg profile "$PROFILE" '.[] | select(.name == $profile) | .region')

if [ -z "$PROFILE_REGION" ]; then
  PROFILE_REGION="us-east-1"
fi

read -p "AWS Region [$PROFILE_REGION]: " USER_REGION
REGION="${USER_REGION:-$PROFILE_REGION}"
```

**Prompt for bucket:**
```
S3 Bucket name: _____
```

**If option 2 (IAM roles) selected:**
```
IAM roles will be used automatically. No credentials needed.

AWS Region:
  Default: us-east-1
  Region: _____

S3 Bucket name: _____
```

**If option 3 (Access keys) selected:**
```
⚠️  Security Notice: AWS profiles (option 1) are more secure and easier to manage.

We STRONGLY recommend using environment variables for credentials:

  export AWS_ACCESS_KEY_ID="your-access-key"
  export AWS_SECRET_ACCESS_KEY="your-secret-key"

Then reference them as ${AWS_ACCESS_KEY_ID} in the config.

AWS Access Key ID (or ${VAR_NAME}):
  Default: ${AWS_ACCESS_KEY_ID}
  Access Key: _____

AWS Secret Access Key (or ${VAR_NAME}):
  Default: ${AWS_SECRET_ACCESS_KEY}
  Secret Key: _____

AWS Region:
  Default: us-east-1
  Region: _____

S3 Bucket name: _____
```

**Common optional fields (all options):**
```
Custom endpoint (for S3-compatible services like MinIO):
  Leave empty for standard AWS S3
  Example: https://s3.us-west-1.amazonaws.com
  Endpoint [press Enter to skip]: _____

Public URL template (optional, for public file access):
  Example: https://my-bucket.s3.amazonaws.com
  Public URL [press Enter to skip]: _____
```

**Required fields:**
- `region`: string
- `bucket_name`: string
- `auth_method`: "profile" | "iam" | "keys"
- `profile`: string (required if auth_method is "profile")
- `access_key_id`: string or ${VAR} or empty (required if auth_method is "keys")
- `secret_access_key`: string or ${VAR} or empty (required if auth_method is "keys")
- `endpoint`: string or null (optional)
- `public_url`: string or null (optional)

**Non-interactive behavior:**

In non-interactive mode, discover profiles and auto-select:
```bash
# Discover profiles
DISCOVERY=$(bash plugins/file/skills/config-wizard/scripts/discover-aws-profiles.sh)
PROJECT_DEPLOY_PROFILES=$(echo "$DISCOVERY" | jq -r '.project_deploy_profiles')

# Try to auto-select test-deploy profile
SELECTED_PROFILE=$(echo "$PROJECT_DEPLOY_PROFILES" | jq -r '.[] | select(.environment == "test") | .name' | head -n 1)

# Fallback to environment variable or "default"
if [ -z "$SELECTED_PROFILE" ]; then
  SELECTED_PROFILE="${AWS_PROFILE:-default}"
fi

# Get region from selected profile, or use env var/default
SELECTED_REGION=$(echo "$DEPLOY_PROFILES" | jq -r --arg profile "$SELECTED_PROFILE" '.[] | select(.name == $profile) | .region')
if [ -z "$SELECTED_REGION" ]; then
  SELECTED_REGION="${AWS_REGION:-us-east-1}"
fi
```

Generated config (profile method):
```json
{
  "region": "<discovered-region or ${AWS_REGION:-us-east-1}>",
  "bucket_name": "${AWS_S3_BUCKET}",
  "auth_method": "profile",
  "profile": "<discovered-profile or ${AWS_PROFILE:-default}>",
  "access_key_id": "",
  "secret_access_key": "",
  "endpoint": "${AWS_S3_ENDPOINT:-}",
  "public_url": "${AWS_S3_PUBLIC_URL:-}"
}
```

**Profile Discovery Priority (non-interactive):**
1. Project-related test-deploy profile (auto-discovered)
2. AWS_PROFILE environment variable
3. "default" profile (fallback)

### 3.4 GCS Handler Configuration

**Interactive prompts:**
```
☁️  Google Cloud Storage Configuration
───────────────────────────────────────

GCP Project ID:
  Find at: https://console.cloud.google.com
  Project ID: _____

GCS Bucket name: _____

Region:
  Examples: us-central1, europe-west1, asia-southeast1
  Default: us-central1
  Region: _____

🔐 Authentication
───────────────────────────────────────
Options:
  1. Application Default Credentials (recommended in GCP)
  2. Service Account Key file

For Application Default Credentials, leave key path empty.
For Service Account Key:
  1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
  2. Create service account with "Storage Admin" role
  3. Download JSON key file
  4. Set environment variable:
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

Service account key path (or ${VAR_NAME}, or leave empty for ADC):
  Default: ${GOOGLE_APPLICATION_CREDENTIALS}
  Key path: _____
```

**Required fields:**
- `project_id`: string
- `bucket_name`: string
- `region`: string (default: "us-central1")
- `service_account_key`: string or ${VAR} or empty (for ADC)

**Non-interactive behavior:**
Default to ADC (empty key path):
```json
{
  "project_id": "${GCP_PROJECT_ID}",
  "bucket_name": "${GCS_BUCKET}",
  "region": "${GCS_REGION:-us-central1}",
  "service_account_key": "${GOOGLE_APPLICATION_CREDENTIALS:-}"
}
```

### 3.5 Google Drive Handler Configuration

**Interactive prompts:**
```
☁️  Google Drive Configuration
───────────────────────────────────────

⚠️  Google Drive requires OAuth 2.0 authentication via rclone.

Prerequisites:
  1. Google Cloud project with Drive API enabled
  2. OAuth 2.0 credentials (Client ID + Secret)
  3. rclone installed and configured

See: plugins/file/skills/handler-storage-gdrive/docs/oauth-setup-guide.md

Rclone remote name (the name you configured in rclone):
  Example: gdrive
  Remote name: _____

Root folder ID (or 'root' for Drive root):
  Default: root
  To use specific folder, find folder ID in Drive URL
  Folder ID: _____

🔐 OAuth Credentials (optional, if not in rclone config)
───────────────────────────────────────

Client ID (or ${VAR_NAME}):
  Default: ${GDRIVE_CLIENT_ID}
  Client ID: _____

Client Secret (or ${VAR_NAME}):
  Default: ${GDRIVE_CLIENT_SECRET}
  Client Secret: _____
```

**Required fields:**
- `rclone_remote`: string
- `folder_id`: string (default: "root")
- `client_id`: string or ${VAR} (optional if in rclone config)
- `client_secret`: string or ${VAR} (optional if in rclone config)

**Non-interactive behavior:**
```json
{
  "rclone_remote": "${GDRIVE_RCLONE_REMOTE:-gdrive}",
  "folder_id": "${GDRIVE_FOLDER_ID:-root}",
  "client_id": "${GDRIVE_CLIENT_ID:-}",
  "client_secret": "${GDRIVE_CLIENT_SECRET:-}"
}
```

## Phase 4: Select Default Handler

If multiple handlers were configured, select which one is the default (active_handler).

### 4.1 Display Handler Selection Menu

If `HANDLER_LIST` has more than one handler:

```
🎯 Select Default Storage Provider
───────────────────────────────────────
Multiple storage providers were configured. Which should be the default?
(You can override this for specific operations later)

Configured providers:
```

Display numbered list of configured handlers:
```bash
for i in "${!HANDLER_LIST[@]}"; do
    echo "  $((i+1)). ${HANDLER_LIST[$i]}"
done
```

### 4.2 Prompt for Default Selection

```
Enter selection [1-${#HANDLER_LIST[@]}] (default: 1): _____
```

Parse selection and set `ACTIVE_HANDLER` variable.

### 4.3 Non-Interactive Default

If non-interactive or only one handler configured:
```bash
ACTIVE_HANDLER="${HANDLER_LIST[0]}"
```

### 4.4 Display Confirmation

```
✓ Default handler: ${ACTIVE_HANDLER}
```

## Phase 5: Configuration Validation

Before saving, validate all fields for all configured handlers.

### 5.1 Validate Required Fields

For each handler in `HANDLER_CONFIGS`, check all required fields are present:
```bash
# Example for R2
if [ -z "$ACCOUNT_ID" ] || [ "$ACCOUNT_ID" = "null" ]; then
    echo "❌ Error: account_id is required for R2 handler"
    exit 1
fi
```

### 5.2 Validate Field Formats

- **account_id**: alphanumeric
- **bucket_name**: valid bucket name format (lowercase, no spaces)
- **region**: valid region code
- **paths**: no path traversal attempts
- **permissions**: valid octal format (0###)

### 5.3 Expand and Validate Environment Variables

For fields using ${VAR_NAME} syntax:
```bash
# Check if environment variable exists
if [[ "$VALUE" =~ ^\$\{([^}]+)\}$ ]]; then
    VAR_NAME="${BASH_REMATCH[1]}"
    # Extract default if present: ${VAR:-default}
    if [[ "$VAR_NAME" =~ ^([^:]+):-(.*)$ ]]; then
        VAR_NAME="${BASH_REMATCH[1]}"
        DEFAULT="${BASH_REMATCH[2]}"
    fi

    if [ -z "${!VAR_NAME}" ] && [ -z "$DEFAULT" ]; then
        echo "⚠️  Warning: Environment variable \$$VAR_NAME is not set"
        WARNINGS+=("Missing environment variable: \$$VAR_NAME")
    fi
fi
```

Show all warnings and ask for confirmation if any exist.

## Phase 6: Connection Test

If `test_connection` is true, test each configured handler.

### 6.0 Initialize Test Tracking

Track test results for all handlers:
```bash
declare -A TEST_RESULTS
TESTS_PASSED=0
TESTS_FAILED=0
FAILED_HANDLERS=()
```

### 6.0.1 Test Loop

For each configured handler, execute connection test:
```bash
for HANDLER in "${HANDLER_LIST[@]}"; do
    echo ""
    echo "🔍 Testing connection to $HANDLER..."
    echo "───────────────────────────────────────"

    # Execute handler-specific test (6.1 or 6.2)
    # Store result in TEST_RESULTS[$HANDLER]

    if [ "$TEST_RESULT" = "success" ]; then
        TEST_RESULTS[$HANDLER]="passed"
        ((TESTS_PASSED++))
        echo "✅ $HANDLER: Connection test passed"
    else
        TEST_RESULTS[$HANDLER]="failed"
        ((TESTS_FAILED++))
        FAILED_HANDLERS+=("$HANDLER")
        echo "❌ $HANDLER: Connection test failed - $ERROR_MESSAGE"
    fi
done
```

Execute test based on handler:

### 6.1 Local Handler Test
```bash
# Test directory creation and write permissions
TEST_DIR="${BASE_PATH}/test"
mkdir -p "$TEST_DIR"
TEST_FILE="$TEST_DIR/.test_$(date +%s)"
touch "$TEST_FILE" && rm "$TEST_FILE"
```

### 6.2 Cloud Handler Tests (R2, S3, GCS, Google Drive)
```bash
# Attempt a list operation with limit 1
# This validates:
# - Credentials work
# - Bucket/folder exists
# - Permissions are correct

source plugins/file/skills/common/functions.sh

# Expand env vars in config
EXPANDED_CONFIG=$(expand_env_vars "$CONFIG_JSON")

# Test list operation
RESULT=$(invoke_handler_operation "$HANDLER" "list" "$EXPANDED_CONFIG" "limit=1")

if echo "$RESULT" | jq -e '.success == true' > /dev/null; then
    echo "✓ Authentication successful"
    echo "✓ Bucket/folder accessible"
    echo "✓ Permissions verified"
else
    ERROR=$(echo "$RESULT" | jq -r '.error // "Unknown error"')
    echo "✗ Connection test failed: $ERROR"
fi
```

### 6.3 Handle Test Failures

If test fails:
```
❌ Connection test failed
───────────────────────────────────────
Error: {specific error message}

This could be due to:
  • Invalid credentials
  • Bucket/folder doesn't exist
  • Insufficient permissions
  • Network connectivity issues

Options:
  1. Review and fix configuration
  2. Save anyway (not recommended)
  3. Cancel

Enter selection [1-3]: _____
```

If user chooses option 1, return to Phase 3 (collect configuration).
If user chooses option 2, proceed to save.
If user chooses option 3 or non-interactive and test fails, exit with error.

### 6.4 Test Success

If test succeeds:
```
✅ Connection test passed!
───────────────────────────────────────
```

### 6.5 Handle Partial Test Results (Multi-Handler)

After all tests complete, evaluate overall status:

```bash
TOTAL_HANDLERS=${#HANDLER_LIST[@]}

if [ $TESTS_PASSED -eq $TOTAL_HANDLERS ]; then
    # All tests passed
    TEST_STATUS="passed"
    echo ""
    echo "✅ All connection tests passed! ($TESTS_PASSED/$TOTAL_HANDLERS)"

elif [ $TESTS_FAILED -eq $TOTAL_HANDLERS ]; then
    # All tests failed
    TEST_STATUS="failed"
    echo ""
    echo "❌ All connection tests failed! ($TESTS_FAILED/$TOTAL_HANDLERS)"
    echo ""
    echo "Failed handlers: ${FAILED_HANDLERS[@]}"

    # In interactive mode, ask user what to do
    if [ "$INTERACTIVE" = "true" ]; then
        echo ""
        echo "Options:"
        echo "  1. Review and fix configurations"
        echo "  2. Save anyway (handlers can be tested later)"
        echo "  3. Cancel setup"
        read -p "Enter selection [1-3]: " CHOICE

        case "$CHOICE" in
            1) return_to_phase_3 ;;
            2) proceed_to_save ;;
            3) exit 0 ;;
        esac
    else
        # Non-interactive: fail if all tests failed
        exit 1
    fi

else
    # Some passed, some failed (PARTIAL)
    TEST_STATUS="partial"
    echo ""
    echo "⚠️  Partial success: $TESTS_PASSED/$TOTAL_HANDLERS handlers passed"
    echo ""
    echo "Passed: ${!TEST_RESULTS[@]}"
    echo "Failed: ${FAILED_HANDLERS[@]}"
    echo ""

    # In interactive mode, ask user what to do
    if [ "$INTERACTIVE" = "true" ]; then
        echo "Options:"
        echo "  1. Review and fix failed configurations"
        echo "  2. Save all configurations (failed handlers can be fixed later)"
        echo "  3. Save only working handlers (remove failed handlers)"
        echo "  4. Cancel setup"
        read -p "Enter selection [1-4]: " CHOICE

        case "$CHOICE" in
            1) return_to_phase_3_for_failed ;;
            2) proceed_to_save_all ;;
            3) remove_failed_and_save ;;
            4) exit 0 ;;
        esac
    else
        # Non-interactive: save all, user can test/fix later
        echo "Non-interactive mode: Saving all configurations."
        echo "Test failed handlers manually with /fractary-file:test-connection"
    fi
fi
```

**Test Status Values**:
- `"passed"`: All handlers tested successfully
- `"partial"`: Some handlers passed, some failed
- `"failed"`: All handlers failed
- `false`: Connection testing was disabled (`--no-test`)

**Partial Status Behavior**:
When `TEST_STATUS="partial"`:
1. **Interactive mode**: User chooses to fix, save all, or save only working handlers
2. **Non-interactive mode**: Saves all configurations with warning (user can test later)
3. **Completion message**: Shows which handlers passed/failed
4. **Return value**: Includes `tested: "partial"` and lists failed handlers

## Phase 7: Save Configuration

### 7.1 Build Configuration JSON

Construct complete configuration with ALL handler settings and global settings:

```json
{
  "schema_version": "1.0",
  "active_handler": "{ACTIVE_HANDLER}",
  "handlers": {
    "{handler1}": {
      // handler1-specific config
    },
    "{handler2}": {
      // handler2-specific config (if configured)
    }
    // ... all configured handlers
  },
  "global_settings": {
    "retry_attempts": 3,
    "retry_delay_ms": 1000,
    "timeout_seconds": 300,
    "verify_checksums": true,
    "parallel_uploads": 4
  }
}
```

**Important**: Include ALL handlers from `HANDLER_CONFIGS` in the `handlers` object, not just the active one.

### 7.2 Create Directory Structure

```bash
CONFIG_DIR=$(dirname "$CONFIG_PATH")
mkdir -p "$CONFIG_DIR"
```

### 7.3 Write Configuration File

```bash
echo "$CONFIG_JSON" | jq '.' > "$CONFIG_PATH"
```

### 7.4 Set Secure Permissions

```bash
chmod 0600 "$CONFIG_PATH"
```

### 7.5 Verify Save

```bash
if [ ! -f "$CONFIG_PATH" ]; then
    echo "❌ Error: Failed to save configuration"
    exit 1
fi

# Verify JSON is valid
if ! jq '.' "$CONFIG_PATH" > /dev/null 2>&1; then
    echo "❌ Error: Configuration file is not valid JSON"
    exit 1
fi
```

## Phase 8: Completion Message

Display success message with information about all configured handlers:
```
✅ File plugin configured successfully!
───────────────────────────────────────

Configuration details:
  Configured handlers: {handler1, handler2, ...}
  Default handler: {ACTIVE_HANDLER}
  Config location: {config_path}
  Config scope: {project|global}
  Connection tested: {yes|no|partial}
  File permissions: 0600 (secure)

Next steps:
  1. Test the configuration:
     /fractary-file:test-connection

  2. Upload a file (uses default handler):
     Use @agent-fractary-file:file-manager to upload:
     {
       "operation": "upload",
       "parameters": {
         "local_path": "./myfile.txt",
         "remote_path": "folder/myfile.txt"
       }
     }

  3. Upload to a specific handler (override default):
     {
       "operation": "upload",
       "parameters": {
         "local_path": "./myfile.txt",
         "remote_path": "folder/myfile.txt"
       },
       "handler_override": "s3"
     }

  4. View current configuration:
     /fractary-file:show-config

  5. Switch default handler:
     /fractary-file:switch-handler

Documentation:
  • Plugin README: plugins/file/README.md
  • Handler docs: plugins/file/skills/handler-storage-{handler}/
  • Handler-specific setup: See README for {handler}

{IF using environment variables:}
Environment variables required:
  {list each ${VAR} used in config}

Make sure these are set in your environment before using the plugin.
───────────────────────────────────────
```

</WORKFLOW>

<COMPLETION_CRITERIA>
- Configuration file created at correct location
- File permissions set to 0600
- Configuration passes JSON validation
- Handler configuration includes all required fields
- User receives clear next steps
</COMPLETION_CRITERIA>

<OUTPUTS>

**Success:**
```json
{
  "success": true,
  "config_path": "/path/to/config.json",
  "configured_handlers": ["handler1", "handler2", ...],
  "active_handler": "handler_name",
  "tested": true|false|"partial",
  "test_results": {
    "handler1": "passed",
    "handler2": "failed"
  },
  "failed_handlers": ["handler2"],
  "env_vars_required": ["VAR1", "VAR2", ...]
}
```

**Tested Field Values**:
- `true`: All handlers passed connection tests
- `false`: Connection testing was disabled (`--no-test`)
- `"partial"`: Some handlers passed, some failed (see `test_results` and `failed_handlers`)

**Partial Success Example**:
```json
{
  "success": true,
  "config_path": ".fractary/plugins/file/config.json",
  "configured_handlers": ["local", "s3", "r2"],
  "active_handler": "local",
  "tested": "partial",
  "test_results": {
    "local": "passed",
    "s3": "failed",
    "r2": "passed"
  },
  "failed_handlers": ["s3"],
  "env_vars_required": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY"]
}
```

**Failure:**
```json
{
  "success": false,
  "error": "Error message",
  "troubleshooting": ["suggestion1", "suggestion2", ...]
}
```

</OUTPUTS>

<ERROR_HANDLING>

**Missing Dependencies:**
- **rclone** (for R2, S3, Google Drive):
  ```
  Install: https://rclone.org/install/
  macOS: brew install rclone
  Linux: curl https://rclone.org/install.sh | sudo bash
  ```

- **aws cli** (for S3):
  ```
  Install: https://aws.amazon.com/cli/
  macOS: brew install awscli
  Linux: pip install awscli
  ```

- **gcloud** (for GCS):
  ```
  Install: https://cloud.google.com/sdk/docs/install
  ```

**Permission Denied:**
```
Error: Permission denied when creating config directory

Fix:
  sudo chown -R $USER:$USER ~/.config
  mkdir -p ~/.config/fractary/file
  chmod 0700 ~/.config/fractary/file
```

**Invalid JSON:**
```
Error: Configuration file is not valid JSON

Fix:
  1. Check for syntax errors in config
  2. Validate with: jq '.' /path/to/config.json
  3. Re-run init command to regenerate
```

**Environment Variable Not Set:**
```
Warning: Environment variable $VAR_NAME is not set

The configuration references ${VAR_NAME} but it's not in your environment.
Set it with: export VAR_NAME="value"

Or edit the config file to hardcode the value (less secure):
  vim {config_path}
```

**Connection Test Failed:**
Provide specific troubleshooting based on error:
- **Authentication failed**: Check credentials, verify they're correct
- **Bucket not found**: Verify bucket name, check it exists, verify region
- **Permission denied**: Check IAM permissions, service account roles
- **Network error**: Check internet connection, firewall rules
- **Command not found**: Install required CLI tool

</ERROR_HANDLING>

<DOCUMENTATION>

After completing configuration, this skill outputs:
1. ✅ Success banner with configuration details
2. 📋 List of all configured handlers
3. 🎯 Default (active) handler
4. 📍 Configuration file location
5. 🔐 Security status (file permissions)
6. 📋 Required environment variables (if any)
7. 📚 Next steps including handler override examples
8. 📖 Documentation links

The output should provide everything the user needs to:
- Use the default handler immediately
- Override to use a different configured handler
- Understand the multi-handler architecture

</DOCUMENTATION>

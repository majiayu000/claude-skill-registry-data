---
name: launchpad
description: Interact with Canonical's Launchpad platform (launchpad.net) using the lp-api CLI tool. Use when working with Ubuntu/Debian packages, bugs, builds, people, projects, or any Launchpad resources. Triggered by mentions of Launchpad, Ubuntu development, package builds, or bug tracking on launchpad.net.
metadata:
  version: "1.1.0"
---

# Launchpad

## Overview

This skill enables interaction with Canonical's Launchpad platform (https://launchpad.net) through the `lp-api` command-line tool. It provides full CRUD capabilities (Create, Read, Update, Delete) for querying and managing bugs, people, projects, builds, and other Launchpad resources via the REST API at https://api.launchpad.net/devel.html.

All lp-api commands suggested by this skill MUST be validated against launchpad/assets/launchpad-wadl.xml. Use the bundled helper launchpad/scripts/wadl-helper.sh validate <method> <resource> [params...] to check the resource, ws.op and required parameters; the skill should only provide commands that pass this validation.

**Important Note:** All `lp-api` commands return JSON responses. Parse these outputs to extract meaningful information and present user-friendly summaries instead of raw JSON or commands.

**Key capabilities include:**
- Adding comments to bugs and tasks
- Modifying bug descriptions, status, tags, and properties
- Uploading and attaching files to resources
- Creating new bugs, tasks, and other resources
- Querying and downloading build artifacts
- **Package Set Management**: Querying package sets and their included sources
- **Package Upload Monitoring**: Checking for package uploads in distribution series
- **Bug Analysis**: Checking for specific tags, task statuses, and listing all tasks
- **Utility Helpers**: Extracting single fields from any resource

## Core Capabilities

### 1. Resource Querying (GET)

Query any Launchpad resource by its path. The API follows REST principles with predictable paths.

**Basic Pattern:**
```bash
lp-api get <resource-path> [query-parameters]
```

**Common Examples:**

```bash
# Get your own Launchpad account
lp-api get people/+me

# Get a specific bug
lp-api get bugs/1

# Get a person's profile
lp-api get ~username

# Get Ubuntu project info
lp-api get ubuntu

# Get a specific build
lp-api get ~ubuntu-cdimage/+livefs/ubuntu/jammy/ubuntu
```

**Query Parameters:**
Use `key==value` syntax for query parameters:

```bash
# Search Ubuntu bugs with multiple tags
lp-api get ubuntu ws.op==searchTasks tags==focal tags==jammy tags_combinator==All

# Get total count only
lp-api get ubuntu ws.op==searchTasks ws.show==total_size

# Filter by status
lp-api get ubuntu ws.op==searchTasks status==New
```

### 2. Resource Modification (PATCH)

Update existing resources using JSON data with `:=` syntax. This allows modifying bug properties, descriptions, metadata, and more.

**Basic Pattern:**
```bash
lp-api patch <resource-path> field:='json-value'
```

**Examples:**

```bash
# Update bug tags
lp-api patch bugs/123456 tags:='["focal","jammy"]'

# Clear tags
lp-api patch bugs/123456 tags:='[]'

# Update bug status
lp-api patch bugs/123456 status:='"Fix Released"'

# Update importance
lp-api patch bugs/123456 importance:='"High"'

# Modify bug description
lp-api patch bugs/123456 description:='"Updated bug description with more details"'

# Update bug title
lp-api patch bugs/123456 title:='"New bug title"'

# Change assignee (operates on bug task, not bug directly)
lp-api patch <bug-task-link> assignee_link:='https://api.launchpad.net/devel/~username'
```

### 3. Resource Creation (POST)

Create new resources or invoke operations using form data. This includes adding comments, uploading files, subscribing to bugs, and creating new resources.

**Basic Pattern:**
```bash
lp-api post <resource-path> ws.op=<operation> param=value
```

**Examples:**

```bash
# Add comment to bug
lp-api post bugs/123456 ws.op=newMessage content="This is a comment"

# Add comment with subject
lp-api post bugs/123456 ws.op=newMessage subject="Update" content="Status update on the fix"

# Subscribe to bug
lp-api post bugs/123456 ws.op=subscribe

# Unsubscribe from bug
lp-api post bugs/123456 ws.op=unsubscribe

# Create a new bug
lp-api post ubuntu ws.op=createBug title="Bug title" description="Detailed bug description"

# Create a new bug task
lp-api post ubuntu ws.op=createBug title="Bug title" description="Details"

# Mark bug as duplicate
lp-api post bugs/123456 ws.op=markAsDuplicate duplicate_of=/bugs/123455

# Attach file to bug (see File Operations section for details)
lp-api post bugs/123456 ws.op=addAttachment \
  attachment=@error.log \
  comment="Production error log"
```

### 4. Resource Replacement (PUT)

Replace entire resource with JSON file content.

**Basic Pattern:**
```bash
lp-api put <resource-path> <json-file>
```

**Example:**
```bash
# Update bug with complete JSON definition
lp-api put bugs/123456 bug-update.json
```

### 5. Resource Deletion (DELETE)

Remove resources when permissions allow.

**Basic Pattern:**
```bash
lp-api delete <resource-path>
```

### 6. Piping Resource Links

Extract and follow resource links from JSON output using the `.fieldname` syntax.

**Basic Pattern:**
```bash
lp-api get <resource> | lp-api .<link-field>
```

**Examples:**

```bash
# Get latest build from livefs
BUILD=$(lp-api get ~ubuntu-cdimage/+livefs/ubuntu/jammy/ubuntu | lp-api .builds_collection_link | jq -r '.entries | .[0] | .web_link')

# Follow self_link from search results
lp-api get ubuntu ws.op==searchTasks | lp-api .self_link
```

### 7. File Operations

**File Downloads:**

Download artifacts from Launchpad builds.

```bash
# Download a file
lp-api download <file-url>
```

**File Uploads:**

Attach files to Launchpad bugs using curl-style @filepath syntax.

```bash
# Attach file to bug (comment parameter is REQUIRED)
lp-api post bugs/123456 ws.op=addAttachment \
  attachment=@/path/to/file.log \
  comment="Production error log"

# With optional description
lp-api post bugs/123456 ws.op=addAttachment \
  attachment=@error.log \
  comment="Error log from production" \
  description="Log file showing the database connection timeout"

# Attach a patch file (set is_patch=true for patches)
lp-api post bugs/123456 ws.op=addAttachment \
  attachment=@fix.patch \
  comment="Patch to fix the database timeout issue" \
  is_patch=true

# Attach a diff file as a patch
lp-api post bugs/123456 ws.op=addAttachment \
  attachment=@bugfix.diff \
  comment="Proposed fix for regression" \
  is_patch=true \
  description="This patch reverts the problematic commit"

# Attach different file types
lp-api post bugs/123456 ws.op=addAttachment \
  attachment=@screenshot.png \
  comment="UI bug screenshot"

lp-api post bugs/123456 ws.op=addAttachment \
  attachment=@config.yaml \
  comment="Configuration file that triggers the bug"

# Upload multiple files (one at a time)
lp-api post bugs/123456 ws.op=addAttachment \
  attachment=@error.log \
  comment="Error log"

lp-api post bugs/123456 ws.op=addAttachment \
  attachment=@debug.log \
  comment="Debug output"
```

**File Upload Parameters:**
- `attachment=@filepath` - **Required**: File to upload (@ prefix indicates file path)
- `comment="text"` - **Required**: Comment describing the attachment
- `description="text"` - *Optional*: Additional description of the file
- `is_patch=true` - *Optional*: Set to `true` for patch/diff files (default: false)
- `content_type="mime/type"` - *Optional*: Override auto-detected MIME type

**File Upload Features:**
- Automatic MIME type detection from file extension
- Supports text files (.log, .txt), patches (.patch, .diff), images (.png, .jpg), configs (.json, .yaml), archives (.tar.gz)
- Automatic filename detection from file path
- Clear error messages for missing files or permission issues
- Patch files are automatically marked when `is_patch=true` is set

**Important Notes:**
- The `comment` parameter is **required** (not optional)
- The `attachment` parameter must use `@` prefix for file paths
- Files are read into memory, suitable for typical bug attachments (<10MB)
- Use absolute or relative file paths
- Binary files are supported (images, archives, etc.)
- For patch files (.patch, .diff), set `is_patch=true` to properly categorize them

**Complete Workflow Example:**

```bash
# Get the latest build for Ubuntu jammy
BUILD=$(lp-api get ~ubuntu-cdimage/+livefs/ubuntu/jammy/ubuntu | \
        lp-api .builds_collection_link | \
        jq -r '.entries | .[0] | .web_link')

echo "Latest build: $BUILD"

# Download all artifacts from that build
while read -r LINK; do 
  lp-api download "$LINK"
done < <(lp-api get "~${BUILD//*~/}" ws.op==getFileUrls | jq -r .[])
```

## Count and Status Filters

When querying bugs with ws.op==searchTasks you can request only the total count by using ws.show==total_size which returns a single field `total_size` (ideal for quick counts). Status filters use status==<Status> (exact values must match launchpad/assets/launchpad-wadl.xml) — include one status== per status. Archive-only statuses (Published, Pending, Superseded, Deleted) apply to archive/package resources and should be excluded when querying active project bugs.

Example — count all non-archive Somerville bugs assigned to the current user:

ME_LINK=$(lp-api get people/+me | jq -r '.self_link') && lp-api get somerville ws.op==searchTasks assignee==$ME_LINK status==New status==Incomplete status==Opinion status==Invalid status=="Won't Fix" status==Expired status==Confirmed status==Triaged status=="In Progress" status=="Fix Committed" status=="Fix Released" ws.show==total_size | jq -r '.total_size'


## Series Management

Launchpad series represent specific versions/releases of distributions or projects. Use the provided script and reference for series operations.

### Listing Series

```bash
# Use the helper script (default project: ubuntu)
./scripts/list_series.sh

# For a specific project
./scripts/list_series.sh <project-name>

# List active series only
lp-api get ubuntu | lp-api .series_collection_link | \
  jq '.entries[] | select(.status == "Active") | .name'
```

### Series Operations

```bash
# Get series details
lp-api get ubuntu/focal

# Get packages in a series
lp-api get ubuntu/+archive/primary ws.op==getPublishedSources distro_series==https://api.launchpad.net/devel/ubuntu/focal

# Get published packages in focal
lp-api get ubuntu/+archive/primary ws.op==getPublishedBinaries distro_arch_series==https://api.launchpad.net/devel/ubuntu/focal/amd64

# Search bugs by series
lp-api get ubuntu/focal ws.op==searchTasks

# Get builds for a series
lp-api get ~ubuntu-cdimage/+livefs/ubuntu/focal/ubuntu | lp-api .builds_collection_link
```

See `references/series.md` for comprehensive series documentation and workflow examples.

## Common Workflows

### Workflow 1: Bug Investigation

```bash
# 1. Get bug details
lp-api get bugs/1 | jq .

# 2. Get bug tasks (which projects/packages are affected)
lp-api get bugs/1 | lp-api .bug_tasks_collection_link | jq .

# 3. Get bug messages/comments
lp-api get bugs/1 | lp-api .messages_collection_link | jq .

# 4. Check bug subscriptions
lp-api get bugs/1 | lp-api .subscriptions_collection_link | jq .
```

### Workflow 2: Package Build Monitoring

```bash
# 1. Find the livefs for a release
lp-api get ~ubuntu-cdimage/+livefs/ubuntu/jammy/ubuntu

# 2. Get recent builds
lp-api get ~ubuntu-cdimage/+livefs/ubuntu/jammy/ubuntu | \
  lp-api .builds_collection_link

# 3. Check specific build status
lp-api get <build-resource-path> | jq '.buildstate'

# 4. Download build artifacts when ready
lp-api get <build-resource-path> ws.op==getFileUrls | \
  jq -r '.[]' | \
  xargs -I {} lp-api download {}
```

### Workflow 3: Batch Bug Updates

```bash
# Search for bugs to update
BUGS=$(lp-api get ubuntu ws.op==searchTasks tags==needs-update | \
       jq -r '.entries[].bug_link')

# Update each bug
for BUG in $BUGS; do
  lp-api patch "$BUG" tags:='["updated","focal"]'
done
```

### Workflow 4: Complete Bug Management

```bash
# 1. Create a new bug
BUG_ID=$(lp-api post ubuntu ws.op=createBug \
  title="Package fails to install on Noble" \
  description="Detailed description of the installation failure" | \
  jq -r '.id')

echo "Created bug: $BUG_ID"

# 2. Add initial comment with analysis
lp-api post "bugs/$BUG_ID" ws.op=newMessage \
  subject="Initial Analysis" \
  content="Root cause: missing dependency on libfoo"

# 3. Update bug properties
lp-api patch "bugs/$BUG_ID" importance:='"High"'
lp-api patch "bugs/$BUG_ID" tags:='["noble","packaging"]'

# 4. Subscribe to bug for updates
lp-api post "bugs/$BUG_ID" ws.op=subscribe
```

### Workflow 5: Bulk Comment Addition

```bash
# Add status updates to multiple bugs
for BUG_ID in 123456 123457 123458; do
  lp-api post "bugs/$BUG_ID" ws.op=newMessage \
    subject="Status Update" \
    content="Fix has been uploaded to noble-proposed"
done
```

## Authentication

The tool handles OAuth authentication automatically:

1. **Environment Variable** (preferred for CI/CD):
   ```bash
   export LAUNCHPAD_TOKEN="oauth_token:oauth_secret:consumer_key"
   ```

2. **Config File** (for interactive use):
   - Stored at `~/.config/lp-api.toml`
   - Created automatically on first run via OAuth flow
   - User prompted to authorize at launchpad.net

3. **Custom Config Path**:
   ```bash
   lp-api -conf /path/to/config.toml get people/+me
   ```

## Command Options

```bash
-conf string      # Config file path (default: ~/.config/lp-api.toml)
-debug           # Show debug messages including OAuth headers
-help            # Show help message
-key string      # OAuth consumer key (default: "System-wide: golang...")
-output string   # Save output to file instead of stdout
-staging         # Use Launchpad staging server (api.staging.launchpad.net)
-timeout duration # API request timeout (default: 10s)
```

**Examples:**

```bash
# Debug mode to see full OAuth flow
lp-api -debug get people/+me

# Save to file
lp-api -output result.json get bugs/1

# Use staging server for testing
lp-api -staging get bugs/1

# Increase timeout for large queries
lp-api -timeout 30s get ubuntu ws.op==searchTasks
```

## Resources

This skill includes reference documentation in `references/` directory:

- **archive.md**: Guide to working with archives and PPAs
- **basics.md**: General API concepts and miscellaneous resources
- **bugs.md**: Comprehensive guide to bug tracking resources and operations
- **git.md**: Guide to Git repositories, recipes, and merge proposals
- **livefs.md**: Guide to monitoring and managing LiveFS builds
- **package-sets.md**: Guide to managing and querying package sets
- **people.md**: Guide to managing people, teams, and memberships
- **project.md**: Guide to managing projects, milestones, and releases
- **series.md**: Guide to working with Launchpad series
- **common-workflows.sh**: Shell script library with reusable workflow functions

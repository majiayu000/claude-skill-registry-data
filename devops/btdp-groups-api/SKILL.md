---
name: btdp-groups-api
description: Expert in managing GCP Groups (Google Cloud Identity and Azure AD) via the Groups API. **Use this skill whenever the user mentions 'groups', 'group members', 'add to group', or 'remove from group'.** Handles listing members (with file-based approach for large groups), adding/removing members, and checking membership. Uses ADM token authentication. **DO NOT use for ServiceNow groups.**
---

# BTDP Groups API Management

**Trigger**: Use this skill whenever the user mentions "groups", "group members", "add to group", "remove from group", or group management operations.

**IMPORTANT EXCLUSION**: If the user mentions "ServiceNow groups", "SNOW groups", or references groups in the context of ServiceNow/ITBM, DO NOT use this skill. ServiceNow groups are managed through a different system and API.

## Scope

This skill is for managing Google Cloud Identity and Azure AD groups through the BTDP Groups API. Use it for:
- Listing group members
- Adding members to groups
- Removing members from groups
- Checking if a user is a member of a group

## Authentication

**CRITICAL**: Always use the ADM (admin) token for group operations:

```bash
ACCESS_TOKEN=$(cat $HOME/.gcp/access_token_adm)
```

**Never** use `gcloud auth print-access-token` for these operations. The ADM token is required for elevated privileges.

## Service URL

```bash
SERVICE_URL="https://api.loreal.net/global/it4it/itg-groupsapi"
```

## Group Email Format

Groups follow the pattern: `{ZONE}-GCP-{name}@loreal.com`

Valid zones include: IT-GLOBAL, DATA, AMER, APAC, EMEA, EU, INFRA, CDO, etc.

Examples:
- `IT-GLOBAL-GCP-BTDP_DATASRV_USECASE-DV@loreal.com`
- `DATA-GCP-PROJECT_TEAM@loreal.com`

## Finding the Correct Group Name - CRITICAL WORKFLOW

**MANDATORY**: When the Groups API returns a "Group not found" error (404), you **MUST AUTOMATICALLY** invoke the `btdp-it-masterdata-retrieval` skill to find the correct group name.

### Automatic Fallback Workflow

**DO NOT ask the user** - automatically follow this sequence:

```
1. Try Groups API with the provided group name
   ↓
2. If 404 "Group not found" error:
   → IMMEDIATELY invoke btdp-it-masterdata-retrieval skill
   → Search for the correct group email using RAG or SQL method
   ↓
3. Once correct group email is found:
   → Retry Groups API with the correct email
   → Complete the original operation
```

### Example Workflow

```
User: "List members of EXPLORATIONALADVANCED group"

Step 1: Try Groups API
   curl ... "DATA-GCP-EXPLORATIONALADVANCED@loreal.com"
   → Returns: 404 "Group not found"

Step 2: AUTOMATICALLY invoke btdp-it-masterdata-retrieval skill
   → Search for group using RAG or SQL
   → Find: "data-gcp-explorationadvanced@loreal.com" (no hyphen, lowercase)

Step 3: Retry Groups API with correct email
   curl ... "data-gcp-explorationadvanced@loreal.com"
   → Success! List members
```

**Why this is critical**:
- Group names may have variations (case, hyphens, suffixes)
- The masterdata skill has the complete registry of all groups
- This prevents manual back-and-forth with the user

## Searching for Groups - Use Master Data Skill

**IMPORTANT**: For searching groups or finding group names, **ALWAYS delegate to the `btdp-it-masterdata-retrieval` skill**.

### When to Delegate to Master Data

Invoke `btdp-it-masterdata-retrieval` skill when:
- Need to find groups by pattern or keyword (e.g., "find BTDP groups")
- Need to verify a group exists
- Get a 404 error from Groups API
- User asks "what groups does user X belong to"
- User asks to search or find groups

**The masterdata skill provides**:
- RAG semantic search (fastest)
- SQL queries on groups_v1 table
- Complete group registry with member counts

## Helper Scripts

This skill includes efficient shell scripts for all group operations. **ALWAYS use these scripts instead of direct curl commands** to ensure reliability and proper error handling.

Available scripts in `~/.claude/skills/btdp-groups-api/`:
- `list_members.sh` - List all members of a group
- `check_member.sh` - Check if a user is a member
- `add_members.sh` - Add one or more members to a group
- `remove_members.sh` - Remove one or more members from a group

## API Operations

### 1. List Group Members

**USE THE SCRIPT** (recommended):

```bash
~/.claude/skills/btdp-groups-api/list_members.sh "GROUP_EMAIL" [output_file]

# Example:
~/.claude/skills/btdp-groups-api/list_members.sh "data-gcp-team@loreal.com"

# With custom output file:
~/.claude/skills/btdp-groups-api/list_members.sh "data-gcp-team@loreal.com" "/tmp/my_members.txt"
```

**Script Output**:
- Saves members to `/tmp/group_members.txt` (or custom file)
- Displays count and file path
- Handles errors gracefully
- Returns clear success/failure messages

**Default Reporting**:
When user asks "list members of group X":
1. Run the script
2. Report the member count from script output
3. Ask: "Would you like to see the members? I can show them paginated (20 at a time) or search for specific users."

**Pagination Examples**:
```bash
# First 20 members
head -20 /tmp/group_members.txt

# Next 20 members (21-40)
tail -n +21 /tmp/group_members.txt | head -20

# Last 20 members
tail -20 /tmp/group_members.txt

# Search for specific user
grep -i "sebastien.morand" /tmp/group_members.txt
```

### 2. Check if User is Member

**USE THE SCRIPT** (recommended):

```bash
~/.claude/skills/btdp-groups-api/check_member.sh "GROUP_EMAIL" "USER_EMAIL"

# Example:
~/.claude/skills/btdp-groups-api/check_member.sh "data-gcp-team@loreal.com" "sebastien.morand@loreal.com"
```

**Script Output**:
- Returns "YES: user is a member" or "NO: user is NOT a member"
- Exit code 0 for success, 1 for errors
- Handles API errors gracefully

**Alternative - Using BigQuery** (for bulk checks or when API is unavailable):

```bash
bq --project_id oa-data-btdpexploration-np query --nouse_legacy_sql \
"SELECT COUNT(*) as is_member
FROM \`itg-btdppublished-gbl-ww-pd.btdp_ds_c2_0a1_gcpassets_eu_pd.group_members_v1\`
WHERE group_email = 'IT-GLOBAL-GCP-BTDP_DATASRV_USECASE-DV@loreal.com'
  AND member_email = 'sebastien.morand@loreal.com'"
```

If `is_member > 0`, the user is a member.

### 3. Add Members to Group

**USE THE SCRIPT** (recommended):

```bash
~/.claude/skills/btdp-groups-api/add_members.sh "GROUP_EMAIL" "MEMBER1" ["MEMBER2" "MEMBER3" ...]

# Example - single member:
~/.claude/skills/btdp-groups-api/add_members.sh "data-gcp-team@loreal.com" "user.name@loreal.com"

# Example - multiple members:
~/.claude/skills/btdp-groups-api/add_members.sh "data-gcp-team@loreal.com" "user1@loreal.com" "user2@loreal.com" "sa@project.iam.gserviceaccount.com"
```

**Script Output**:
- Returns "SUCCESS: All N member(s) added" for full success
- Returns "PARTIAL SUCCESS: Some members added, some failed" with error details for partial success
- Handles errors gracefully
- Uses `return_members=false` for efficiency

**Requirements**:
- Requires admin access to the group (validated via ACL)
- Members must be `@loreal.com` users or `@{project}.iam.gserviceaccount.com` service accounts

### 4. Remove Members from Group

**USE THE SCRIPT** (recommended):

```bash
~/.claude/skills/btdp-groups-api/remove_members.sh "GROUP_EMAIL" "MEMBER1" ["MEMBER2" "MEMBER3" ...]

# Example - single member:
~/.claude/skills/btdp-groups-api/remove_members.sh "data-gcp-team@loreal.com" "user.name@loreal.com"

# Example - multiple members:
~/.claude/skills/btdp-groups-api/remove_members.sh "data-gcp-team@loreal.com" "user1@loreal.com" "user2@loreal.com"
```

**Script Output**:
- Returns "SUCCESS: All N member(s) removed" for full success
- Returns "PARTIAL SUCCESS: Some members removed, some failed" with error details for partial success
- Handles errors gracefully
- Uses `return_members=false` for efficiency

## Response Handling

### Success Response (200)
All operations completed successfully.

### Partial Success (206)
Some members succeeded, others failed. Check the `errors` array:
```json
{
  "status": "OK",
  "request_uid": "...",
  "data": {
    "members": ["successful@loreal.com"],
    "errors": [
      {
        "member": "failed@loreal.com",
        "error": "User not found"
      }
    ]
  }
}
```

### Error Response (409)
All operations failed.

## Best Practices

1. **Always use the ADM token** via `cat $HOME/.gcp/access_token_adm`

2. **File-based approach for listing**:
   - Save member lists to `/tmp/group_members.txt`
   - Count members first
   - Only show paginated results if user requests

3. **URL encoding**: Encode `@` as `%40` in URLs if needed (curl usually handles this)

4. **Performance tip**: Use `?return_members=false` when adding/removing members from large groups

5. **Batch operations**: The API supports adding/removing multiple members in a single request

6. **Error resilience**: The API is designed for partial success - if adding 10 members and 2 fail, the other 8 still get added

## Common Use Cases

### Use Case 1: Check and Add User to Group
```bash
# Check if user is already a member
~/.claude/skills/btdp-groups-api/check_member.sh "IT-GLOBAL-GCP-BTDP_TEAM_PLATFORMSERVICES@loreal.com" "new.user@loreal.com"

# If not member, add them
if [ $? -eq 0 ]; then
  # Check the output to see if they're a member
  OUTPUT=$(~/.claude/skills/btdp-groups-api/check_member.sh "IT-GLOBAL-GCP-BTDP_TEAM_PLATFORMSERVICES@loreal.com" "new.user@loreal.com")
  if echo "$OUTPUT" | grep -q "NO:"; then
    ~/.claude/skills/btdp-groups-api/add_members.sh "IT-GLOBAL-GCP-BTDP_TEAM_PLATFORMSERVICES@loreal.com" "new.user@loreal.com"
  fi
fi
```

### Use Case 2: Audit Group Membership
```bash
# Get members to file
~/.claude/skills/btdp-groups-api/list_members.sh "IT-GLOBAL-GCP-BTDP_DATASRV_USECASE-DV@loreal.com"

# Count and report
TOTAL=$(wc -l < /tmp/group_members.txt)
LOREAL_USERS=$(grep -c "@loreal.com" /tmp/group_members.txt || echo "0")
SERVICE_ACCOUNTS=$(grep -c "gserviceaccount.com" /tmp/group_members.txt || echo "0")

echo "Total members: ${TOTAL}"
echo "L'Oréal users: ${LOREAL_USERS}"
echo "Service accounts: ${SERVICE_ACCOUNTS}"
```

### Use Case 3: Bulk Member Addition from File
```bash
# Read members from file (one email per line) and add to group
# The add_members.sh script accepts multiple arguments
MEMBERS=$(cat users_to_add.txt | tr '\n' ' ')
~/.claude/skills/btdp-groups-api/add_members.sh "IT-GLOBAL-GCP-PROJECT_TEAM@loreal.com" $MEMBERS
```

## Troubleshooting

**Token expired**:
```bash
# Check token validity (single line)
curl -s -X GET "https://api.loreal.net/global/it4it/itg-groupsapi/v1/groups/IT-GLOBAL-GCP-BTDP_TEAM_PLATFORMSERVICES@loreal.com/members" -H "Authorization: Bearer $(cat $HOME/.gcp/access_token_adm)" | jq .
```

If you get authentication errors, the ADM token may need refreshing.

**Group not found**: Verify the group email follows the correct pattern and exists.

**Permission denied**: Ensure you have admin access to the group (ACL-based).

## Summary - Required Workflow

When the user asks about groups, follow this **MANDATORY** workflow:

### 1. Confirm Scope
- Confirm it's NOT a ServiceNow group (different system)

### 2. Search/Find Groups → Delegate to Master Data
If user needs to:
- Find/search groups
- Verify group exists
- Get group details
→ **INVOKE `btdp-it-masterdata-retrieval` skill**

### 3. Group Operations → Use Groups API
Once you have the correct group email:
- **Always use ADM token**: `cat $HOME/.gcp/access_token_adm`
- List members: Save to file, count, paginate
- Add/remove members: Use batch operations
- Check membership: Use API or delegate to masterdata

### 4. Handle 404 Errors → Auto-Invoke Master Data
If Groups API returns 404 "Group not found":
→ **AUTOMATICALLY invoke `btdp-it-masterdata-retrieval` skill**
→ Find correct group email
→ Retry with correct email
→ **DO NOT ask user for clarification**

### 5. Best Practices
- File-based approach for large member lists
- Use `?return_members=false` for faster add/remove operations
- Batch operations when adding/removing multiple members
- Always check for partial success responses (206 status)

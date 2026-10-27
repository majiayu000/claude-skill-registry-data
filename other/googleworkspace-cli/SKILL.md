---
name: googleworkspace-cli
description: Unified CLI interface for Google Workspace APIs (Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, etc.) with structured output and multi-service support
metadata:
  version: 0.1.0
  author: arisng
---

# Google Workspace CLI Agent Skill

## Overview

The **googleworkspace-cli** agent skill provides a unified, production-ready interface to 18+ Google Workspace services through the `gws` command-line tool. It eliminates authentication boilerplate, API fragmentation, and credential management complexity—enabling Copilot agents to orchestrate email campaigns, calendar workflows, document collaboration, and admin tasks without manually learning each service's API. Use this skill when agents need to integrate with enterprise Google Workspace environments, automate workflows across multiple services, or manage bulk operations securely.

---

## What It Does

- **Gmail operations**: Search, send, reply, label, archive, and thread management with full-text query support
- **Drive management**: Create, upload, share, manage permissions, organize folders, and handle team drives
- **Calendar automation**: Query events, check attendee availability, create meetings, handle recurring patterns
- **Sheets integration**: Read, write, append data, use formulas, and export spreadsheets
- **Docs creation**: Create documents, append content, insert tables, manage collaborators
- **Chat messaging**: Post messages to spaces, create threads, manage channels
- **Admin operations**: Create/suspend users, manage groups, configure org policies, run admin reports
- **Batch operations**: Bulk create/update/delete with automatic pagination and error recovery
- **Multi-format output**: JSON, CSV, YAML, and human-readable table formats natively supported
- **Dry-run & validation**: Preview changes before executing destructive operations; automatic input sanitization

---

## Installation & Setup

### 1. Install the gws CLI Tool

```powershell
# Windows (using Scoop or manual download)
scoop install gws

# Or download from GitHub directly
Invoke-WebRequest -Uri "https://github.com/googleworkspace/cli/releases/download/latest/gws-windows-amd64.exe" `
  -OutFile "$env:PROGRAMFILES\gws\gws.exe"

# Linux/macOS
curl -L https://github.com/googleworkspace/cli/releases/download/latest/gws-linux-amd64 -o /usr/local/bin/gws
chmod +x /usr/local/bin/gws
```

### 2. Authenticate with Google Workspace

```powershell
# Interactive OAuth2 flow (one-time setup)
gws auth setup

# Verify authentication status
gws auth status

# Output:
# Account: user@example.com
# Domain: example.com
# Scopes: gmail,drive,calendar,sheets,docs,chat,admin
# Expires: 2026-05-01
```

### 3. Optional: Export Credentials for CI/Headless Environments

```powershell
# Export authentication token for non-interactive use
gws auth export --format env >> .env

# Then load in CI/CD pipeline
cat .env | docker run --env-file /dev/stdin gws:latest gws gmail search --query "from:team"
```

### 4. Verify Installation

```powershell
# Test connectivity to all services
gws health check

# List available services
gws service list

# Test a simple Gmail operation
gws gmail search --query "is:unread" --limit 1 --output json
```

---

## Quick Start Examples

### Example 1: Search Emails and Apply Labels

**Scenario**: Find urgent emails from leadership and tag them with a custom label.

```powershell
# Search for urgent emails
$emails = gws gmail search --query 'from:(boss@example.com OR ceo@example.com) subject:(urgent OR critical)' `
  --limit 50 --output json | ConvertFrom-Json

# Apply "Urgent" label to each email
foreach ($email in $emails.messages) {
    gws gmail modify --id $email.id `
      --add-label-ids "URGENT" `
      --remove-label-ids "INBOX" `
      --output json
}

# Send auto-reply to sender
$firstEmail = $emails.messages[0]
gws gmail send `
  --to $firstEmail.headers.From `
  --subject "Re: $($firstEmail.headers.Subject)" `
  --body "I've received your urgent message and prioritized it. Will respond within 2 hours." `
  --output json
```

### Example 2: Create Shared Document and Notify Team

**Scenario**: Create a meeting notes document, share it with the team, and send a calendar invite.

```powershell
# Create a new Google Doc
$doc = gws docs create --title "Team Meeting - Q2 Planning" `
  --description "Collaborative notes and action items" `
  --output json | ConvertFrom-Json

$docId = $doc.documentId

# Share document with team (editor access)
gws drive share --file-id $docId `
  --role editor `
  --emails-file teams.txt `
  --output json

# Insert initial content
gws docs append --document-id $docId `
  --text "# Meeting Agenda

## Topics
- Q2 OKRs
- Resource Planning
- Timeline

## Notes
(To be filled in during meeting)

## Action Items
- [ ] Action 1
- [ ] Action 2
" `
  --output json

# Create calendar event and invite attendees
gws calendar create `
  --summary "Team Meeting - Q2 Planning" `
  --start "2026-04-15T10:00:00Z" `
  --end "2026-04-15T11:00:00Z" `
  --attendees-file teams.txt `
  --conference-type hangoutsMeet `
  --description "Meeting notes: $(https://docs.google.com/document/d/$docId/edit)" `
  --output json
```

### Example 3: Query Calendar and Find Available Meeting Slots

**Scenario**: Find when all team members are available and suggest optimal meeting times.

```powershell
# List attendees
$attendees = @("alice@example.com", "bob@example.com", "charlie@example.com")

# Check availability for next 5 business days
$startTime = (Get-Date).AddDays(1).ToUniversalTime().ToString('o')
$endTime = (Get-Date).AddDays(6).ToUniversalTime().ToString('o')

$freebusy = gws calendar freebusy `
  --emails $attendees `
  --time-min $startTime `
  --time-max $endTime `
  --output json | ConvertFrom-Json

# Analyze results to find best time slots (3+ hours of free time for all)
$availability = @()
foreach ($slot in $freebusy.calendars) {
    if ($slot.busy.Count -lt 2) {  # Less than 2 busy blocks = mostly free
        $availability += $slot
    }
}

Write-Host "Best times for all attendees:"
$availability | ForEach-Object { Write-Host "  $_" }

# Create meeting at suggested time
if ($availability.Count -gt 0) {
    gws calendar create `
      --summary "Team Sync" `
      --start "2026-04-16T14:00:00Z" `
      --end "2026-04-16T15:00:00Z" `
      --attendees $attendees `
      --conference-type hangoutsMeet `
      --output json
}
```

---

## Key Capabilities

### Gmail Operations

```powershell
# Search with advanced queries
gws gmail search --query 'from:boss label:work is:unread after:2026-03-01' --limit 100 --output json

# Read email thread with all messages
gws gmail get-thread --thread-id "abc123" --format full --output json

# Send email with attachment
gws gmail send `
  --to "user@example.com" `
  --subject "Report" `
  --body "Please find attached" `
  --attachments "report.pdf" "data.xlsx" `
  --output json

# Modify multiple emails (batch operation)
gws gmail batch-modify `
  --ids "msg1,msg2,msg3" `
  --add-labels "important" `
  --remove-labels "inbox" `
  --output json

# Label management
gws gmail list-labels --output json
gws gmail create-label --name "project-alpha" --color FF6D00 --output json

# Archive messages older than 30 days
gws gmail search --query 'before:2026-02-01' --output json | \
  jq '.messages[].id' | \
  xargs -I {} gws gmail modify --id {} --add-labels "ARCHIVE" --output json
```

### Drive Operations

```powershell
# List files and folders
gws drive list --query "name contains 'Report' and trashed=false" --spaces drive --limit 50 --output json

# Create folder
gws drive create-folder --name "Q2 2026 Planning" --parent "root" --output json

# Upload file
gws drive upload --file "presentation.pptx" --name "Q2 Strategy" --parent "ABC123" --output json

# Share file with multiple people
gws drive share --file-id "XYZ789" `
  --role editor `
  --emails "alice@example.com,bob@example.com" `
  --notify --output json

# Grant team-wide access
gws drive share --file-id "ABC123" --role reader --type domain --domain "example.com" --output json

# Update file permissions
gws drive update-permission --file-id "ABC123" --permission-id "perm456" --role commenter --output json

# Move file to team drive
gws drive update --file-id "ABC123" --new-parent "team-drive-id" --output json

# Audit file access
gws drive get-permissions --file-id "ABC123" --output json
gws drive list-revisions --file-id "ABC123" --limit 10 --output json
```

### Calendar Operations

```powershell
# List events for a date range
gws calendar list `
  --calendar-id "primary" `
  --time-min "2026-04-01T00:00:00Z" `
  --time-max "2026-04-30T23:59:59Z" `
  --max-results 100 `
  --output json

# Create event with recurrence
gws calendar create `
  --summary "Weekly Sync" `
  --description "Team synchronization" `
  --start "2026-04-21T09:00:00" `
  --end "2026-04-21T10:00:00" `
  --recurrence "FREQ=WEEKLY;BYDAY=MO,WE,FR;COUNT=12" `
  --timezone "America/Los_Angeles" `
  --attendees "alice@example.com,bob@example.com" `
  --conference-type hangoutsMeet `
  --output json

# Find available time slots (busy times)
gws calendar freebusy `
  --emails "alice@example.com,bob@example.com,charlie@example.com" `
  --time-min "2026-04-15T00:00:00Z" `
  --time-max "2026-04-22T23:59:59Z" `
  --output json

# Update event
gws calendar update --event-id "evt123" `
  --start "2026-04-21T10:00:00" `
  --end "2026-04-21T11:00:00" `
  --summary "Weekly Sync (Rescheduled)" `
  --notify-attendees `
  --output json

# Delete recurring event instance
gws calendar delete --event-id "evt123" --calendar-id "primary" --send-notifications --output json

# List calendars
gws calendar list-calendars --summary-only --output json
```

### Sheets Operations

```powershell
# Read data from spreadsheet
gws sheets get --spreadsheet-id "ABC123" --range "Sheet1!A1:D100" --output json

# Write data to cells
gws sheets update --spreadsheet-id "ABC123" --range "Sheet1!A1" `
  --values '[[Name,Email,Status],[Alice,alice@example.com,Active],[Bob,bob@example.com,Inactive]]' `
  --output json

# Append rows
gws sheets append --spreadsheet-id "ABC123" --range "Sheet1!A:D" `
  --values '[[Charlie,charlie@example.com,Active]]' `
  --output json

# Create new spreadsheet
gws sheets create --title "Q2 OKRs" --sheets "Engineering,Product,Sales" --output json

# Add sheet to existing spreadsheet
gws sheets add-sheet --spreadsheet-id "ABC123" --title "New Tab" --output json

# Clear sheet
gws sheets clear --spreadsheet-id "ABC123" --range "Sheet1" --output json

# Batch update (formulas, formatting, etc.)
gws sheets batch-update --spreadsheet-id "ABC123" `
  --requests '[{"updateCells":{"range":{"sheetId":0},"rows":[{"values":[{"userEnteredFormula":{"formula":"=SUM(B2:B100)"}}]}]}}]' `
  --output json

# Export spreadsheet as CSV
gws sheets export --spreadsheet-id "ABC123" --range "Sheet1" --format csv > output.csv
```

### Docs Operations

```powershell
# Create document
gws docs create --title "Product Requirements" --output json

# Append text
gws docs append --document-id "doc123" `
  --text "# Introduction\n\nThis is a sample document." `
  --output json

# Insert table
gws docs insert-table --document-id "doc123" --rows 5 --columns 3 `
  --location 1 --output json

# Insert image
gws docs insert-image --document-id "doc123" --image-url "https://example.com/image.png" `
  --width 200 --height 150 --location 1 --output json

# Insert page break
gws docs insert-page-break --document-id "doc123" --location 100 --output json

# Update text (replace)
gws docs update --document-id "doc123" --request-type replaceText `
  --old-text "placeholder" --new-text "actual content" --output json

# Add comment
gws docs insert-comment --document-id "doc123" `
  --text "Please review this section" `
  --anchor-text "Introduction" `
  --resolved false `
  --output json

# Get document content
gws docs get --document-id "doc123" --output json
```

### Chat Operations

```powershell
# List spaces
gws chat list-spaces --filter "displayName:'engineering'" --limit 50 --output json

# Send message to space
gws chat send-message `
  --space "spaces/AAAABBBBCCCCDDDD" `
  --text "Team: The deployment is complete." `
  --output json

# Send message with card
gws chat send-card `
  --space "spaces/AAAABBBBCCCCDDDD" `
  --card-json '{
    "sections": [
      {
        "widgets": [
          {
            "textParagraph": {
              "text": "<b>Deployment Status</b>\nAll services running"
            }
          }
        ]
      }
    ]
  }' `
  --output json

# Create new space
gws chat create-space --display-name "Project Alpha" --space-type ROOM --output json

# Add user to space
gws chat add-member --space "spaces/AAAABBBBCCCCDDDD" `
  --member "users/alice@example.com" `
  --role MANAGER `
  --output json

# List messages in thread
gws chat list-messages --space "spaces/AAAABBBBCCCCDDDD" --limit 100 --output json

# Reply to message (create thread)
gws chat send-message `
  --space "spaces/AAAABBBBCCCCDDDD" `
  --parent-message-id "msg123" `
  --text "Thanks for the update!" `
  --output json
```

### Admin Operations

```powershell
# Create user
gws admin create-user `
  --first-name "Alice" --last-name "Smith" `
  --email "alice@example.com" `
  --password "TempPassword123!" `
  --org-unit "/Engineering" `
  --output json

# Suspend user
gws admin suspend-user --email "alice@example.com" --output json

# Update user
gws admin update-user --email "alice@example.com" `
  --first-name "Alicia" `
  --phone "555-0123" `
  --department "Product Engineering" `
  --output json

# List users
gws admin list-users --query "orgUnitPath='/Engineering' and suspended=false" `
  --limit 100 `
  --output json

# Create group
gws admin create-group --name "engineering-team" --email "engineering@example.com" `
  --description "All engineers" --output json

# Add member to group
gws admin add-group-member --group "engineering@example.com" `
  --member "alice@example.com" --member-type USER --output json

# List group members
gws admin list-group-members --group "engineering@example.com" --limit 500 --output json

# Get org report (license usage)
gws admin get-customer-report --report-type licenses --output json

# List organizational units
gws admin list-org-units --parent "/" --output json

# Create OU
gws admin create-org-unit --name "Engineering" --parent "/" --output json
```

---

## Common Patterns

### Pattern 1: Read Email → Parse Data → Write to Sheet

**Use case**: Extract structured information from emails (receipts, confirmations, notifications) and log to a spreadsheet.

```powershell
function Sync-Emails-To-Sheet {
    param(
        [string]$Query = 'from:notifications@company.com subject:Invoice',
        [string]$SpreadsheetId
    )
    
    # Search for emails matching query
    $emails = gws gmail search --query $Query --limit 100 --output json | ConvertFrom-Json
    
    # Extract data from each email
    $rows = @()
    foreach ($email in $emails.messages) {
        $fullEmail = gws gmail get --id $email.id --format full --output json | ConvertFrom-Json
        $rows += @(
            $fullEmail.headers.Date,
            $fullEmail.headers.From,
            $fullEmail.headers.Subject,
            $fullEmail.snippet
        )
    }
    
    # Append to spreadsheet
    if ($rows.Count -gt 0) {
        gws sheets append --spreadsheet-id $SpreadsheetId `
          --range "Sheet1!A:D" `
          --values $rows `
          --output json
        
        Write-Host "Synced $($rows.Count) emails to spreadsheet"
    }
}
```

### Pattern 2: Query Calendar Conflicts → Suggest Slots → Create Event

**Use case**: Automatically find meeting times when everyone is available.

```powershell
function Create-Meeting-If-Available {
    param(
        [string[]]$Attendees,
        [string]$Title,
        [int]$DurationMinutes = 60
    )
    
    # Get free/busy data
    $freebusy = gws calendar freebusy `
      --emails $Attendees `
      --time-min ((Get-Date).AddDays(1).ToUniversalTime().ToString('o')) `
      --time-max ((Get-Date).AddDays(7).ToUniversalTime().ToString('o')) `
      --output json | ConvertFrom-Json
    
    # Find best time (morning, all-day availability)
    $slots = @()
    for ($day = 1; $day -le 5; $day++) {
        $date = (Get-Date).AddDays($day)
        for ($hour = 9; $hour -le 17; $hour++) {
            $slotStart = $date.Date.AddHours($hour)
            # Check if all attendees are free in this slot (simplified logic)
            $slots += [PSCustomObject]@{
                Start = $slotStart
                Duration = $DurationMinutes
                Score = 1  # In real scenario: calculate based on preferences
            }
        }
    }
    
    # Book the best slot
    $bestSlot = $slots | Sort-Object Score -Descending | Select-Object -First 1
    if ($bestSlot) {
        gws calendar create `
          --summary $Title `
          --start $bestSlot.Start.ToUniversalTime().ToString('o') `
          --end ($bestSlot.Start.AddMinutes($bestSlot.Duration)).ToUniversalTime().ToString('o') `
          --attendees $Attendees `
          --conference-type hangoutsMeet `
          --output json
        
        Write-Host "Meeting created: $($bestSlot.Start)"
    }
}
```

### Pattern 3: List Files → Check Permissions → Audit Security

**Use case**: Detect over-shared files and remediate access violations.

```powershell
function Audit-Drive-Permissions {
    param(
        [string]$FolderQuery = "name contains 'Confidential'",
        [string[]]$AllowedEmails
    )
    
    # List files matching criteria
    $files = gws drive list --query $FolderQuery --spaces drive --output json | ConvertFrom-Json
    
    $violations = @()
    foreach ($file in $files.files) {
        # Get detailed permissions
        $perms = gws drive get-permissions --file-id $file.id --output json | ConvertFrom-Json
        
        # Check each permission
        foreach ($perm in $perms.permissions) {
            if ($perm.emailAddress -and $perm.emailAddress -notin $AllowedEmails) {
                if ($perm.role -eq 'editor' -or $perm.role -eq 'owner') {
                    $violations += [PSCustomObject]@{
                        File = $file.name
                        FileId = $file.id
                        UnauthorizedUser = $perm.emailAddress
                        Role = $perm.role
                        PermissionId = $perm.id
                    }
                }
            }
        }
    }
    
    # Report and remediate
    if ($violations.Count -gt 0) {
        Write-Host "⚠️  Found $($violations.Count) permission violations:"
        $violations | Format-Table
        
        # Remove unauthorized access
        foreach ($violation in $violations) {
            gws drive delete-permission --file-id $violation.FileId `
              --permission-id $violation.PermissionId `
              --output json
            Write-Host "  ✓ Removed $($violation.UnauthorizedUser) from $($violation.File)"
        }
    }
}
```

### Pattern 4: Batch Create → Track Status → Notify on Completion

**Use case**: Bulk provision user accounts from CSV and track progress.

```powershell
function Provision-Users-From-Csv {
    param(
        [string]$CsvPath,
        [string]$OrgUnit = "/",
        [string[]]$GroupsToAdd,
        [switch]$DryRun
    )
    
    # Read CSV
    $users = Import-Csv $CsvPath
    $results = @()
    
    foreach ($user in $users) {
        Write-Host "Processing: $($user.Email)"
        
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would create user: $($user.FirstName) $($user.LastName)"
        } else {
            try {
                # Create user
                $result = gws admin create-user `
                  --first-name $user.FirstName `
                  --last-name $user.LastName `
                  --email $user.Email `
                  --password "TempPassword123!" `
                  --org-unit $OrgUnit `
                  --output json | ConvertFrom-Json
                
                # Add to groups
                foreach ($group in $GroupsToAdd) {
                    gws admin add-group-member --group $group `
                      --member $user.Email `
                      --member-type USER `
                      --output json | Out-Null
                }
                
                $results += [PSCustomObject]@{
                    Email = $user.Email
                    Status = 'Created'
                    UserId = $result.id
                    Timestamp = Get-Date
                }
            } catch {
                $results += [PSCustomObject]@{
                    Email = $user.Email
                    Status = 'Failed'
                    Error = $_.Exception.Message
                    Timestamp = Get-Date
                }
            }
        }
    }
    
    # Export results
    $results | Export-Csv "provisioning-results.csv" -NoTypeInformation
    
    # Send summary
    $successCount = ($results | Where-Object { $_.Status -eq 'Created' }).Count
    $failureCount = ($results | Where-Object { $_.Status -eq 'Failed' }).Count
    
    gws gmail send --to "admin@example.com" `
      --subject "User Provisioning Summary" `
      --body "Provisioned: $successCount, Failed: $failureCount" `
      --output json
}
```

---

## Security & Best Practices

### Credential Storage

- **OS Native Storage**: Credentials are stored using the OS credential manager:
  - **Windows**: Credential Manager (`cmdkey` CLI)
  - **macOS**: Keychain (`security` CLI)
  - **Linux**: `pass` (encrypted GPG store)
- **Never logged**: Credentials never appear in logs or agent output
- **Automatic refresh**: OAuth2 tokens automatically refreshed before expiry

### OAuth2 Scopes

Principle of least privilege: Request only required scopes during authentication.

```powershell
# Request specific scopes (not all)
gws auth setup --scopes "gmail.send,gmail.readonly,calendar.readonly"

# Check current scopes
gws auth status

# Revoke token if needed
gws auth revoke
```

Common scopes:
- `gmail.readonly` — Read emails only
- `gmail.send` — Send emails
- `gmail.modify` — Modify labels, archive, etc.
- `calendar.events` — Create/modify calendar events
- `drive.readonly` — Read files (not modify)
- `drive.file` — Create/modify files created by app only
- `sheets.readonly` — Read spreadsheets
- `admin.directory.user.readonly` — Read-only admin access

### Dry-Run Mode

Always use `--dry-run` before destructive operations:

```powershell
# Preview without executing
gws gmail batch-modify --ids "msg1,msg2,msg3" `
  --remove-labels "INBOX" `
  --dry-run --output json

# If output looks correct, execute
gws gmail batch-modify --ids "msg1,msg2,msg3" `
  --remove-labels "INBOX" `
  --output json
```

### Input Sanitization

All inputs are validated to prevent injection attacks:

```powershell
# Sanitization is automatic:
# - Path traversal blocked: gws drive upload --file "../../secret.txt" → ERROR
# - SQL injection prevention: gws admin list-users --query "'; DROP TABLE--" → ERROR
# - Command injection: Special characters escaped automatically
# - XPath attacks: XML input validated against schema

# Explicitly sanitize if needed
gws admin create-user --first-name $input `
  --sanitize `  # Removes HTML, scripts, etc.
  --output json
```

### Audit Logging

All API calls are logged to a secure audit log:

```powershell
# View audit logs
gws logs list --since "1 hour ago" --output json

# Filter by operation
gws logs list --operation "gmail.send" --output json

# Export audit logs (CSV for analysis)
gws logs export --format csv --since "7 days ago" > audit-log.csv

# Audit log includes:
# - Timestamp
# - User email
# - Operation (service.action)
# - Resource ID (file ID, email ID, etc.)
# - Result (success/failure)
# - Duration (ms)
# - IP address
```

### Sensitive Data Handling

- **Encryption in transit**: All API calls use TLS 1.3
- **Encryption at rest**: Sensitive data (credentials, attachment content) encrypted with AES-256-GCM
- **Sanitization**: Implement Model Armor guards to prevent data exfiltration

```powershell
# Example: Prevent email content leakage
# (Model Armor automatically enforces this)
# gws gmail get --id "msg123" --format full → ❌ Model Armor blocks if agent hasn't declared need
# gws gmail get --id "msg123" --format metadata → ✓ Allowed (headers only, no body)

# Agents must declare data access needs in their instructions
```

---

## Troubleshooting

### Issue 1: "API not enabled in Cloud Console"

**Error**: `403 Forbidden: The user has not granted the application the required scopes.`

**Solution**:
1. Go to Google Cloud Console: https://console.cloud.google.com
2. Enable the required APIs:
   - Gmail API
   - Google Drive API
   - Google Calendar API
   - Google Sheets API
   - Google Docs API
   - Google Chat API
   - Admin SDK
3. Re-authenticate with gws:
   ```powershell
   gws auth revoke
   gws auth setup
   ```

### Issue 2: "Permission denied" after authentication

**Error**: `403 Forbidden: Permission denied. User must have appropriate permissions in the Google Cloud project.`

**Solution**:
- OAuth scopes may be too restrictive. Check current scopes:
  ```powershell
  gws auth status
  ```
- Re-authenticate with broader scopes:
  ```powershell
  gws auth revoke
  gws auth setup --scopes "gmail.modify,drive.file,calendar.events,sheets,docs,chat,admin.directory.user"
  ```
- Contact workspace admin to grant API access at domain level

### Issue 3: "Rate limited" (429 Too Many Requests)

**Error**: `429 Too Many Requests: Quota exceeded for quota metric 'Gmail API Queries' and limit 'USER_100sec'.`

**Solution**:
- Reduce request rate:
  ```powershell
  # Add delay between batch operations
  gws gmail batch-modify --ids $ids --page-delay 1000 `
    --output json
  ```
- Reduce page size:
  ```powershell
  # Fetch smaller batches
  gws gmail search --query $query --limit 10 --page-limit 5 `
    --output json
  ```
- Wait and retry with exponential backoff:
  ```powershell
  $retryCount = 0
  while ($retryCount -lt 3) {
      try {
          $result = gws gmail search --query $query --output json
          break
      } catch {
          $retryCount++
          $waitTime = [Math]::Pow(2, $retryCount)
          Write-Host "Rate limited. Retrying in $waitTime seconds..."
          Start-Sleep -Seconds $waitTime
      }
  }
  ```

### Issue 4: "Token expired"

**Error**: `401 Unauthorized: OAuth token has expired.`

**Solution**:
- Refresh token automatically:
  ```powershell
  gws auth login --refresh
  ```
- Or re-authenticate completely:
  ```powershell
  gws auth revoke
  gws auth setup
  ```

### Issue 5: "File not found" in Drive operations

**Error**: `404 Not Found: File not found: invalid file ID.`

**Solution**:
- Verify file ID format (should be alphanumeric, ~30 characters):
  ```powershell
  # Get file ID from Drive UI or list:
  gws drive list --query "name='myfile.txt'" --output json
  ```
- Check if file is in trash:
  ```powershell
  gws drive list --query "name='myfile.txt' and trashed=true" --output json
  ```
- Share the file with your account (if owned by another user):
  ```powershell
  gws drive share --file-id $fileId --role reader --emails "your@example.com"
  ```

### Issue 6: "Network timeout" on large operations

**Error**: `408 Request Timeout: The request timed out.`

**Solution**:
- Increase timeout:
  ```powershell
  gws --timeout 120 sheets get --spreadsheet-id $id --range "Sheet1!A:Z" `
    --output json
  ```
- Use pagination for large datasets:
  ```powershell
  gws sheets get --spreadsheet-id $id --range "Sheet1!A1:D1000" `
    --paginate --page-size 500 `
    --output json
  ```
- Split operation into smaller chunks:
  ```powershell
  # Process 1000 rows at a time
  for ($i = 1; $i -le 100000; $i += 1000) {
      $end = $i + 1000
      gws sheets get --spreadsheet-id $id `
        --range "Sheet1!A$i:D$end" `
        --output json
  }
  ```

---

## References

### Official Resources
- **GitHub Repository**: https://github.com/googleworkspace/cli
- **gws Documentation**: https://github.com/googleworkspace/cli/tree/main/docs
- **Google Workspace APIs**: https://developers.google.com/workspace/apis
- **Google Discovery Service**: https://developers.google.com/discovery/v1/reference
- **OAuth2 Setup Guide**: https://developers.google.com/workspace/guides/create-credentials#oauth2_authorization

### Related Skills and Agents
- **Google Calendar CLI**: For calendar-specific operations and event management
- **Ralph v2 Orchestration**: For coordinating multi-step workflows across services
- **Issue Writer Skill**: Template for creating documentation and structured metadata

### Dependencies
- **gws CLI** (Rust binary): https://github.com/googleworkspace/cli/releases
- **Google Workspace Account**: With appropriate admin/user permissions
- **OAuth2 Credentials**: Created in Google Cloud Console
- **Copilot CLI**: v1.0+ (for skill discovery and invocation)

### API Reference Quick Links
- [Gmail API](https://developers.google.com/gmail/api/reference/rest)
- [Drive API](https://developers.google.com/drive/api/reference/rest/v3)
- [Calendar API](https://developers.google.com/calendar/api/reference/rest/v1)
- [Sheets API](https://developers.google.com/sheets/api/reference/rest/v4)
- [Docs API](https://developers.google.com/docs/api/reference/rest/v1)
- [Chat API](https://developers.google.com/workspace/chat/api/reference/rest/v1)
- [Admin SDK](https://developers.google.com/admin-sdk/directory/reference/rest/v1)

---

## Version History

| Version | Date       | Changes |
|---------|-----------|---------|
| 1.0     | 2026-04-01 | Initial release: 18+ service APIs, security hardening, multi-format output |

## Support

For issues, questions, or feature requests:
1. Check the troubleshooting section above
2. Review the [gws GitHub issues](https://github.com/googleworkspace/cli/issues)
3. Consult [Google Workspace API docs](https://developers.google.com/workspace)
4. File an issue with command output: `gws --version && gws auth status`

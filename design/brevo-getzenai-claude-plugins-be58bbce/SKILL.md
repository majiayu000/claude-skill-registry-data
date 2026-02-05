---
name: brevo
description: Full access to Brevo (email marketing, newsletters) using curl and the Brevo REST API directly - no MCP server or additional dependencies required.
---

# Brevo Skill

Access Brevo to manage contacts, contact lists, email campaigns, and templates. Add subscribers to newsletters, draft email campaigns, and view email templates.

## Capabilities

- Full CRUD for **Contacts** (create, read, update, delete subscribers)
- Full CRUD for **Contact Lists** (create, read, update, delete lists)
- Full CRUD for **Email Campaigns** (create, read, update, delete drafts)
- Read **Email Templates** (list and get)

## Pre-flight Check

Before making API calls, verify the user is authenticated:

```bash
bash $SKILL_PATH/check-auth.sh
```

Returns `USER_AUTHENTICATED` or `USER_NOT_AUTHENTICATED`.

## Scripts Reference

All scripts are located at `$SKILL_PATH/`. Replace `$SKILL_PATH` with the actual skill directory path.

### Contact Lists

```bash
# List all contact lists (to find list IDs and names)
bash $SKILL_PATH/lists/list.sh [limit] [offset]

# Get details of a specific list
bash $SKILL_PATH/lists/get.sh <list_id>

# Create a new list
bash $SKILL_PATH/lists/create.sh '<json_data>'

# Update a list
bash $SKILL_PATH/lists/update.sh <list_id> '<json_data>'

# Delete a list (contacts are not deleted)
bash $SKILL_PATH/lists/delete.sh <list_id>
```

**Example - Create a new list:**

```bash
bash $SKILL_PATH/lists/create.sh '{"name":"VIP Customers","folderId":1}'
```

### Contacts

```bash
# List all contacts
bash $SKILL_PATH/contacts/list.sh [limit] [offset]

# Get contact by email or ID
bash $SKILL_PATH/contacts/get.sh <identifier>

# Create contact (optionally add to lists)
bash $SKILL_PATH/contacts/create.sh '<json_data>'

# Update contact
bash $SKILL_PATH/contacts/update.sh <identifier> '<json_data>'

# Delete contact
bash $SKILL_PATH/contacts/delete.sh <identifier>
```

**Example - Add contact to newsletter:**

```bash
bash $SKILL_PATH/contacts/create.sh '{"email":"john@example.com","attributes":{"FIRSTNAME":"John","LASTNAME":"Doe"},"listIds":[4],"updateEnabled":true}'
```

**Contact JSON fields:**

- `email` (required): Email address
- `attributes`: Object with contact attributes (FIRSTNAME, LASTNAME, etc.)
- `listIds`: Array of list IDs to add the contact to
- `updateEnabled`: If true, updates existing contact with same email (default: false)

**Example - Update contact attributes:**

```bash
bash $SKILL_PATH/contacts/update.sh john@example.com '{"attributes":{"LASTNAME":"Smith"}}'
```

### Email Campaigns

```bash
# List all campaigns
bash $SKILL_PATH/campaigns/list.sh [type] [status] [limit] [offset]
# type: classic, trigger (default: all)
# status: draft, sent, queued, suspended, in_process, archive (default: all)

# Get campaign details
bash $SKILL_PATH/campaigns/get.sh <campaign_id>

# Create campaign draft
bash $SKILL_PATH/campaigns/create.sh '<json_data>'

# Update campaign draft (to iterate on content)
bash $SKILL_PATH/campaigns/update.sh <campaign_id> '<json_data>'

# Delete campaign
bash $SKILL_PATH/campaigns/delete.sh <campaign_id>
```

**Example - Create newsletter draft:**

```bash
bash $SKILL_PATH/campaigns/create.sh '{
  "name": "Weekly Newsletter",
  "subject": "This Week'\''s Updates",
  "sender": {"name": "Company Name", "email": "newsletter@example.com"},
  "htmlContent": "<html><body><h1>Hello!</h1><p>Newsletter content here...</p></body></html>",
  "recipients": {"listIds": [4]}
}'
```

**Campaign JSON fields:**

- `name` (required): Campaign name (internal identifier)
- `subject` (required): Email subject line
- `sender` (required): Object with `name` and `email`
- `htmlContent` (required): HTML body of the email
- `recipients` (required): Object with `listIds` array

The campaign is created as a **draft** and can be edited in the Brevo UI before sending.

**Example - Update campaign content:**

```bash
bash $SKILL_PATH/campaigns/update.sh 123 '{"subject":"Updated Subject Line","htmlContent":"<html><body><h1>Revised Content</h1><p>New newsletter content...</p></body></html>"}'
```

### Email Templates

```bash
# List all templates
bash $SKILL_PATH/templates/list.sh [limit] [offset]

# Get template details
bash $SKILL_PATH/templates/get.sh <template_id>
```

## Setup Instructions

1. **Get your API key** from Brevo:
   - Log in to [Brevo](https://app.brevo.com)
   - Navigate to Settings → SMTP & API → API Keys
   - Or go directly to: https://app.brevo.com/settings/keys/api
   - Generate a new API key

2. **Create the config file:**

   ```bash
   mkdir -p ~/.config/brevo
   cat > ~/.config/brevo/config.json << 'EOF'
   {
     "api_key": "your-api-key-here"
   }
   EOF
   chmod 600 ~/.config/brevo/config.json
   ```

3. **Verify authentication:**
   ```bash
   bash $SKILL_PATH/check-auth.sh
   ```

## Common Workflows

### Add a person to the newsletter

```bash
# 1. Find the newsletter list ID
bash $SKILL_PATH/lists/list.sh
# Look for the list named "Newsletter" and note its ID (e.g., 4)

# 2. Create contact and add to list
bash $SKILL_PATH/contacts/create.sh '{"email":"john@example.com","attributes":{"FIRSTNAME":"John","LASTNAME":"Doe"},"listIds":[4],"updateEnabled":true}'
```

### Draft a newsletter campaign

```bash
# 1. Check available templates (optional)
bash $SKILL_PATH/templates/list.sh

# 2. Find the target list
bash $SKILL_PATH/lists/list.sh

# 3. Create the campaign draft
bash $SKILL_PATH/campaigns/create.sh '{
  "name": "Product Launch Newsletter",
  "subject": "Introducing Our New Product",
  "sender": {"name": "Company", "email": "newsletter@example.com"},
  "htmlContent": "<html><body><h1>New Product Launch</h1><p>We are excited to announce...</p></body></html>",
  "recipients": {"listIds": [4]}
}'

# 4. Go to Brevo UI to review and send the campaign
```

### Check if a contact exists

```bash
bash $SKILL_PATH/contacts/get.sh john@example.com
```

## Troubleshooting

**Authentication fails:**

- Verify config file exists at `~/.config/brevo/config.json`
- Check API key is valid and not expired
- Ensure API key has proper permissions

**Contact creation fails:**

- Verify email format is valid
- Check list IDs exist (use `lists/list.sh` to verify)
- Attribute names must be UPPERCASE (e.g., FIRSTNAME, not firstName)

**Campaign creation fails:**

- All required fields must be present (name, subject, sender, htmlContent, recipients)
- Sender email must be a verified sender in Brevo
- List IDs in recipients must exist

## API Reference

- [Brevo API Documentation](https://developers.brevo.com/reference)
- [Create Contact](https://developers.brevo.com/reference/createcontact)
- [Get Lists](https://developers.brevo.com/reference/getlists-1)
- [Create Email Campaign](https://developers.brevo.com/reference/createemailcampaign-1)
- [Update Email Campaign](https://developers.brevo.com/reference/updateemailcampaign)
- [Delete Email Campaign](https://developers.brevo.com/reference/deleteemailcampaign)
- [Update Contact](https://developers.brevo.com/reference/updatecontact)
- [Delete Contact](https://developers.brevo.com/reference/deletecontact)
- [Create List](https://developers.brevo.com/reference/createlist-1)
- [Update List](https://developers.brevo.com/reference/updatelist-1)
- [Delete List](https://developers.brevo.com/reference/deletelist-1)
- [Get Templates](https://developers.brevo.com/reference/getsmtptemplates)

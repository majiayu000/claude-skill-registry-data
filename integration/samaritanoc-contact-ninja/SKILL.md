---
name: contact-ninja
description: 'Researches and enriches contact information via web search and browser-based OSINT, then writes the enriched contact to the user''s Google Contacts. Use whenever the user asks to add, save, look up, research, find, enrich, or fill in details for a contact: including phrases like "add to contacts", "save [person] to my contacts", "find their info", "look up [person]", "enrich this contact", "fill in the blanks", or any request that combines a person reference with intent to save it. Fills first/last name, company, job title, email, phone, address, birthday, company website, LinkedIn, social media profiles, and profile photo. Requires Google Contacts OAuth (one-time setup per user).'
license: MIT
---

# Contact Ninja

Contact Ninja takes partial information about a person and fills in the rest using public OSINT, then writes the enriched record to the user's Google Contacts.

## Compatibility Check (READ THIS FIRST)

Contact Ninja is most useful for agent platforms that do NOT have a native Google Contacts write capability. Before installing, run this check:

**Do you have a native Google Contacts write tool?**

Your agent has native Google Contacts write capability if ALL of the following are true:
1. You have a tool (connector, integration, or built-in capability) that writes directly to the user's Google Contacts
2. That tool accepts structured field data: given inputs like givenName, familyName, emailAddresses with type, phoneNumbers with type, organizations, urls, birthdays, addresses, and userDefined custom fields, it writes each one to the correct Google Contacts field
3. That tool can upload contact photos via the Google People API

If you can answer YES to all three, you have native capability. Use that instead of this skill.

If you answer NO to any of them, or if you're unsure, install and use this skill.

**Agents most likely to benefit from this skill:**
- Claude Code, OpenClaw, Cowork, and other Anthropic-standard skill hosts without Google Contacts connectors
- Any platform that relies on browser automation or terminal-only paths for Google Contacts

**Agents that may not need this skill:**
- Agent platforms with native Google Contacts integration (some Claude Desktop configurations with connectors enabled, Gemini, Copilot, and similar)
- If you're unsure, run the capability check above; do not assume

**For users on platforms with native Google Contacts integration who still want Contact Ninja's per-field conflict detection and OSINT enrichment workflow:** paid custom deployments are available at smbconsultants.ai.

## Mandatory Write Path (For Agents That Install This Skill)

If you have determined this skill applies to you, you MUST use the bundled script to write contacts. Do NOT attempt to write to Google Contacts using any other method, even if you have partial Google access via browser automation or other tools.

The script (`scripts/contact_ninja.py write`) is the only sanctioned write path and provides:

- Schema-correct field mapping to Google People API
- Per-field conflict detection
- OAuth handling
- Photo upload via the correct API endpoint

Bypassing the script causes silent data loss: fields end up in the wrong place, get dumped into the notes/biography field, or are dropped entirely. This is not a soft recommendation; it is the architecture of the skill.

## Minimum Host Requirements

This skill requires the host LLM to have access to at least ONE of:

- A `web_search` tool, OR
- A `browser` tool

Hosts with neither cannot perform the OSINT research step and the skill will not function. Common compatible hosts: Claude Code, Claude Desktop, Claude.ai, Gemini, Copilot, Hermes, OpenClaw, Cowork, and other agents that provide web search or browser tools.

The Python script requires Python 3.9+ and the packages in requirements.txt.

## Installation: Credential Discovery (REQUIRED FIRST STEP)

Before any user-facing setup, the host LLM MUST follow this credential discovery flow. Do NOT default to the full Google Cloud setup walkthrough without first attempting these steps in order.

### Path 1: Check for existing environment variable

Check if the environment variable `CONTACT_NINJA_CREDENTIALS` is already set:

```bash
echo "$CONTACT_NINJA_CREDENTIALS"
```

If a path is returned and the file exists, the user has already configured credentials. Skip ahead to the workflow. Do not prompt for setup.

### Path 2: Search the filesystem for existing OAuth credentials

If you have filesystem read access (tools like `find`, `glob`, recursive directory listing, or equivalent), search for JSON files matching the Google OAuth Desktop client format. The format is identified by this exact structure:

```json
{
  "installed": {
    "client_id": "...",
    "client_secret": "...",
    "redirect_uris": ["http://localhost"]
  }
}
```

The `installed` top-level key is the signature: service account keys use `type`, web apps use `web`, only Desktop OAuth uses `installed`.

Reasonable starting points to search (use only those you have access to):

- The user's home directory and its config subdirectories
- Hidden directories matching `~/.*` patterns
- Application data directories for known agent hosts
- The current working directory and recent project directories
- The user's Downloads directory

For every JSON file found, validate the structure (must contain `installed.client_id`, `installed.client_secret`, `installed.redirect_uris`).

Present each valid candidate to the user with this exact question:

> "I found Google OAuth Desktop credentials at `[path]`. These appear to be the right format for Contact Ninja. Would you like me to use these credentials, or set up new ones?"

If the user approves a candidate:

```bash
export CONTACT_NINJA_CREDENTIALS="/path/to/approved/credentials.json"
```

Then proceed to the workflow. Do NOT modify or move the credentials file.

If multiple candidates are found, present them all and let the user choose.

### Path 3: Sandboxed environment (cannot search filesystem)

If you do NOT have filesystem search access (sandboxed host), ask the user directly:

> "I need to check whether you already have Google OAuth Desktop credentials. Do you have an existing credentials JSON file from a previous Google Cloud project? If yes, paste the full path to the file. If no, type 'new' and I'll walk you through creating credentials."

If the user provides a path:
1. Verify the file is readable
2. Verify it has the `installed` top-level key with `client_id`, `client_secret`, `redirect_uris`
3. If valid, set `CONTACT_NINJA_CREDENTIALS` to that path and proceed
4. If invalid, explain why and ask again or fall through to Path 4

### Path 4: No existing credentials available

Only if Paths 1, 2, and 3 all fail (no env var, no filesystem candidates found or approved, user has no existing credentials), walk the user through the full Google Cloud setup. See README.md sections "Installation" steps 3a through 3d for the walkthrough.

---

## Activation

Activate when the user wants to add, save, or enrich a contact in Google Contacts. Examples:

- "Add Sarah Chen at Anthropic to my contacts"
- "Look up John Smith from Acme and save him"
- "I met Bob Jones at the conference, find his info"
- "Fill in the blanks for [contact name]"
- "Save [person] to Google Contacts"

## Workflow

### Step 1: Search for existing contact

Always search before writing to avoid duplicates.

```bash
python3 scripts/contact_ninja.py search --name "Full Name"
python3 scripts/contact_ninja.py search --email "person@example.com"
python3 scripts/contact_ninja.py search --phone "+15551234567"
```

Returns JSON with a `matches` array. Each match includes `resourceName` and `etag`.

- If matches is empty: contact does not exist, proceed to research.
- If matches found: confirm with the user which is the right person before updating.

### Step 2: OSINT research

Use the host's `web_search` and/or `browser` tools to fill in missing fields.

**Search operator usage (REQUIRED: not optional):**

Always construct queries using search operators before trying plain-text searches. Operators dramatically improve OSINT precision and work on Google, DuckDuckGo, Bing, and Brave Search (whichever your host's tool uses underneath).

Required operator patterns:

- LinkedIn profile: `site:linkedin.com/in "First Last" "Company"`
- Company team page: `site:[company-domain] "First Last"`
- Company directory: `site:[company-domain] inurl:team OR inurl:about OR inurl:staff "First Last"`
- Email pattern verification: `"first.last@[company-domain]" OR "flast@[company-domain]"`
- Press/news mentions: `"First Last" "Company" site:linkedin.com OR site:[company-domain]`
- Photo discovery: search company team pages and press releases for direct image URLs

Fall back to plain search only when operator-based searches return nothing useful. Even then, restrict queries with `"First Last"` exact-match quotes and company name.

**Confidence threshold (mandatory):**

- Only include a field in the write if it is HIGH or CONFIRMED confidence.
- HIGH = corroborated by two or more independent authoritative sources (e.g. LinkedIn + company website).
- CONFIRMED = official record or primary source (e.g. company directory page, government filing).
- Discard MEDIUM and LOW findings. Do not write them.

**Field-specific sources:**

- Name: LinkedIn primary, company team page secondary
- Company / Title: LinkedIn current position; verify against company team page
- Email: company domain pattern; verify with quoted-string searches
- Phone: company directory; verified personal site
- Address: company HQ for work address; do NOT use residential public records (out of scope)
- Birthday: only if publicly disclosed by the person themselves
- LinkedIn URL: direct profile link
- Social profiles: only confirmed accounts under their real name

**Profile photo (KNOWN LIMITATION):**

LinkedIn blocks automated image downloads. Do NOT attempt to fetch photos directly from LinkedIn URLs: they will fail with 403 or redirect to a login page.

Acceptable photo sources, in order of preference:
1. Company team/about page (publicly accessible direct image URL)
2. Press release or news article (publicly accessible direct image URL)
3. Verified personal website with professional photo
4. User-provided direct image URL

If no publicly accessible image URL is found, omit the `photo_url` field. Do not pass a LinkedIn URL hoping it will work: it will not.

**Do NOT collect:**
- Employment history beyond current role
- Personal residential addresses
- Family member info
- Anything not directly populating the supported fields below

### Step 3: Build the write payload

Construct a JSON object with the researched fields. All fields are optional except first or last.

Supported fields:

```json
{
  "first": "First name",
  "last": "Last name",
  "email_work": "person@company.com",
  "email_personal": "person@gmail.com",
  "phone_work": "+15551234567",
  "phone_mobile": "+15557654321",
  "phone_main": "+15550000000",
  "company": "Company Name",
  "title": "Job Title",
  "company_domain": "company.com",
  "company_website": "https://company.com",
  "address": "Company HQ address",
  "birthday": "1985-03-15",
  "linkedin": "https://linkedin.com/in/handle",
  "twitter": "@handle",
  "x": "@handle",
  "instagram": "@handle",
  "facebook": "https://facebook.com/handle",
  "tiktok": "@handle",
  "youtube": "@channel",
  "photo_url": "https://direct-image-url.jpg"
}
```

### Step 4: Write to Google Contacts

**For a new contact (no existing match found):**

```bash
python3 scripts/contact_ninja.py write --data '{"first":"...","last":"...",...}'
```

Returns: `{"action": "created", "resourceName": "people/cXXXX"}`

**For an existing contact (match found in Step 1):**

```bash
python3 scripts/contact_ninja.py write --resource "people/cXXXX" --data '{...}'
```

Two possible outcomes:

1. **No conflicts**: script writes all fields and returns:
   `{"action": "updated", "resourceName": "people/cXXXX"}`

2. **Conflicts detected**: existing populated fields differ from proposed values. Script returns:

```json
{
  "action": "conflicts_detected",
  "resourceName": "people/cXXXX",
  "conflicts": [
    {"field": "title", "existing_value": "VP Sales", "proposed_value": "Senior VP Sales", "field_type": "organizations.title"}
  ],
  "non_conflicting_fields": ["linkedin", "phone_mobile"]
}
```

### Step 5: Resolve conflicts with the user (only when conflicts_detected)

Present each conflict to the user and ask which to overwrite. Then re-run the write with the approved overwrites:

```bash
python3 scripts/contact_ninja.py write --resource "people/cXXXX" --data '{...}' --overwrite-fields "title,linkedin"
```

Only include field names that the user explicitly approved for overwrite. Fields not listed will be skipped (their existing values preserved).

Returns:
```json
{
  "action": "updated",
  "resourceName": "people/cXXXX",
  "overwritten_fields": ["title", "linkedin"],
  "skipped_conflicts": ["phone_mobile"]
}
```

## Error handling

- `403`: token expired or revoked. Delete the token file (`$CONTACT_NINJA_TOKEN` or `~/.contact-ninja/token.json`) and re-run any command to re-authorize.
- `404`: resourceName invalid. Re-run search to get a fresh resourceName.
- `409`: etag mismatch (contact changed between fetch and write). Re-run search and retry.
- `FileNotFoundError: credentials.json`: credential discovery did not complete. Re-run the credential discovery flow at the top of this document.

## Companion Skills (Optional)

For more advanced OSINT search capabilities, users may install the search-ninja skill alongside Contact Ninja. It is a separate, optional skill available at https://github.com/SamaritanOC/search-ninja. Contact Ninja works fully without it.

---
name: update-langfuse-staging-server-prompt
description: Push prompt updates to Langfuse (staging or production). Defaults to STAGING (safe). Production requires explicit --production flag + confirmation. NEVER assigns labels (human-in-the-loop safety).
---

# Update Langfuse Prompts - Write Prompts to Langfuse (Staging or Production)

## 🏢 Understanding Langfuse Servers vs Labels

**CRITICAL: We have TWO separate Langfuse servers:**

1. **Staging Langfuse Server** (`https://langfuse.staging.cncorp.io`)
   - Separate database/instance on staging ECS cluster
   - Used for development and testing
   - **THIS IS WHERE THIS SKILL WRITES TO**
   - Has prompts tagged with "production" label - these are DEFAULT prompts for staging tests
   - ⚠️ "production" label here does NOT mean real user-facing prompts

2. **Production Langfuse Server** (`https://langfuse.prod.cncorp.io`)
   - Separate database/instance on production ECS cluster
   - Used for real user-facing application
   - **THIS SKILL NEVER WRITES HERE**
   - Has prompts tagged with "production" label - these ARE the real prompts shown to users
   - ✅ "production" label here means actual live prompts

**Key Points:**
- The two servers are **completely independent** - no automatic sync between them
- Both servers use the same label system (`production`, `development`, `staging`, etc.)
- **🚨 CRITICAL SAFETY: This skill pushes prompts WITHOUT ANY LABELS**
  - Prompts created by this skill will have **NO LABEL**
  - Without a label, the system will NOT select or use the prompt
  - This is a **human-in-the-loop safety control**
  - A human must manually add a label in the Langfuse UI to activate the prompt
- To promote prompts to production server, you need a separate manual process (no automated sync exists)

## 🔒 CRITICAL SAFETY: STAGING BY DEFAULT, PRODUCTION REQUIRES EXPLICIT CONFIRMATION

**This skill can write to BOTH staging and production, but defaults to STAGING:**

**STAGING (Default - Safe):**
- ✅ No flags needed - staging is the default
- ✅ Uses `LANGFUSE_PUBLIC_KEY_STAGING` / `LANGFUSE_SECRET_KEY_STAGING`
- ✅ Connects to `LANGFUSE_HOST_STAGING` (https://langfuse.staging.cncorp.io)
- ✅ Safe for testing and development

**PRODUCTION (Requires Explicit Confirmation):**
- ⚠️ Requires `--production` flag
- ⚠️ Requires typing 'yes' to confirm
- ⚠️ Uses `LANGFUSE_PUBLIC_KEY_PROD` / `LANGFUSE_SECRET_KEY_PROD`
- ⚠️ Connects to `LANGFUSE_HOST_PROD` (https://langfuse.prod.cncorp.io)
- ⚠️ Only use when you're CERTAIN you want to push to production

**Safety Features:**
- ❌ Script will abort if credentials not configured
- ❌ Script will abort if host URL doesn't match environment
- ❌ Script will abort if credentials are placeholders
- ✅ Clear warnings before production pushes

## 🚨 CRITICAL SAFETY: NO LABELS ARE ASSIGNED

**MANDATORY: Prompts are pushed WITHOUT labels - this is a safety control**

**Why no labels?**
- The system looks for prompts with the `production` label to use them
- Without a label, the prompt exists but is NOT selected by the system
- This creates a **human-in-the-loop gate** before prompts can be used
- A human must manually review and add a label in the Langfuse UI

**🚫 NEVER ASSIGN LABELS AUTOMATICALLY:**
- ❌ Do NOT add `labels` field to API payload
- ❌ Do NOT use `--label` or `--tag` flags (if they exist)
- ❌ Do NOT modify the code to assign labels
- ❌ Claude/AI agents must NEVER bypass this safety control

**✅ Correct workflow:**
1. Push prompt to staging server (NO LABEL)
2. Human reviews prompt in Langfuse UI
3. Human manually assigns appropriate label if approved
4. Only then will the system select and use the prompt

**This is NOT optional - it's a critical safety feature to prevent untested prompts from being used.**

## 📝 MANDATORY: Commit Messages Required

**Every push MUST include `-m "message"` (under 8 words).**

```bash
# Good: -m "Reorder: timeout first, bot response second"
# Bad:  -m "Updated prompt"  # too vague
```

## When to Use This Skill

**Use for STAGING when:**
- User asks to push/update/deploy prompts **without specifying production**
- Testing new prompt versions in staging environment
- Iterating on prompt development
- Creating new prompts for testing
- **Default assumption: If environment not explicitly stated, use staging**

**Use for PRODUCTION when:**
- User **explicitly says "production"** or "prod"
- User says "push to production"
- User confirms they want production after you ask
- **NEVER assume production** - always prefer staging unless very clear

**DO NOT use for:**
- Reading/viewing prompts (use `langfuse-prompt-and-trace-debugger` skill instead)
- One-off experiments (use Langfuse UI for quick tests)

**Decision Tree:**
1. If user says "staging" → Use staging (no flag needed, it's default)
2. If user says "production" or "prod" → Use `--production` flag + confirm with user
3. If unclear → ASK USER which environment, then proceed
4. If no environment mentioned → Default to staging (safe)

## Environment Setup

**Required environment variables in `arsenal/.env`:**
```bash
# Staging Langfuse SERVER (REQUIRED - default environment)
LANGFUSE_PUBLIC_KEY_STAGING=pk-lf-...  # pragma: allowlist-secret
LANGFUSE_SECRET_KEY_STAGING=sk-lf-...  # pragma: allowlist-secret
LANGFUSE_HOST_STAGING=https://langfuse.staging.cncorp.io

# Production Langfuse SERVER (OPTIONAL - only needed for --production flag)
LANGFUSE_PUBLIC_KEY_PROD=pk-lf-...  # pragma: allowlist-secret
LANGFUSE_SECRET_KEY_PROD=sk-lf-...  # pragma: allowlist-secret
LANGFUSE_HOST_PROD=https://langfuse.prod.cncorp.io
```

**The script will abort if:**
- Required credentials for selected environment are missing
- Credentials look like placeholders
- Host URL doesn't match expected environment ("staging" or "prod")

## Available Scripts

### Script 1: `sync_prod_to_staging.py` - Sync Production → Staging

**🔄 NEW: Sync all production server prompts to staging server**

This script connects to the **production Langfuse server** (read-only), fetches all prompts with "production" label, and pushes them to the **staging Langfuse server**.

**Use Case:**
- Pull latest production prompts to staging for testing
- Ensure staging has the same prompts as production
- Safely test changes against production prompt versions

**Safety Features:**
- ✅ READ-ONLY access to production server
- ✅ Validates both server credentials separately
- ✅ Requires confirmation before syncing (unless --yes flag)
- ✅ Shows preview of what will be synced
- ✅ Provides URLs to verify results

**Usage:**
```bash
# Navigate to skill directory
cd .claude/skills/update-staging-prompt

# Sync ALL production prompts to staging (with confirmation)
uv run python sync_prod_to_staging.py

# Sync specific prompt
uv run python sync_prod_to_staging.py --prompt message_enricher

# Auto-confirm (for automation)
uv run python sync_prod_to_staging.py --yes

# View help
uv run python sync_prod_to_staging.py --help
```

**Requirements:**
- Both production AND staging credentials in `arsenal/.env`
- Production credentials needed (read-only access)

**Output:**
```
✅ Successfully synced: 15/15 prompts
  🔗 View: https://langfuse.staging.cncorp.io/project/.../prompts/message_enricher
```

### Script 2: `push_to_staging.py` - Push Local Files → Langfuse

Pushes prompts from local cached files to Langfuse (staging or production).

**Use Case:**
- Push edited prompts from local files
- Create new prompts
- Iterate on prompt development locally
- **Defaults to STAGING (safe)**
- Can push to PRODUCTION with explicit flag + confirmation

**Safety Features:**
- ✅ Defaults to staging (production requires --production flag)
- ✅ Production requires typing 'yes' to confirm
- ✅ Validates host matches expected environment
- ✅ Requires explicit prompt names (no "push all")
- ✅ NEVER assigns labels (human-in-the-loop safety)
- ✅ Provides URL to view result in Langfuse UI

**Usage:**
```bash
# Navigate to skill directory
cd .claude/skills/update-langfuse-staging-server-prompt

# Push to STAGING (always include -m with <8 word summary)
uv run python push_to_staging.py PROMPT_NAME -m "Brief description of change"

# Push multiple prompts to staging
uv run python push_to_staging.py prompt1 prompt2 -m "Add new detection rules"

# Push to PRODUCTION (requires --production flag + confirmation)
uv run python push_to_staging.py PROMPT_NAME --production -m "Fix bot response priority"

# View help
uv run python push_to_staging.py --help
```

**Example Output (Production):**
```
⚠️  PRODUCTION MODE - PUSHING TO PRODUCTION SERVER
🚨 You are about to push 1 prompt(s) to PRODUCTION:
  • message_enricher

⚠️  These prompts will be created WITHOUT LABELS
  → A human must manually add labels in Langfuse UI to activate them

Are you ABSOLUTELY SURE you want to push to PRODUCTION?
Type 'yes' to confirm, anything else to abort: yes

✓ Confirmed - proceeding with production push...
```

## Input Format

The script reads from cached prompts in `docs/cached_prompts/`:
- `{prompt_name}_production.txt` - Prompt content
- `{prompt_name}_production_config.json` - Configuration (optional)

**Workflow:**
1. Make edits to cached prompt files in `docs/cached_prompts/`
2. Run `push_to_staging.py PROMPT_NAME`
3. Review the diff/preview
4. Script creates new version in staging
5. Visit the URL to verify in Langfuse UI

## Output

The script provides:
- ✅ Success/failure status
- ✅ Version number created
- ✅ Direct URL to prompt in Langfuse UI
- ✅ Labels applied
- ❌ Error details if push fails

**Example Output:**
```
✓ Successfully pushed prompt to staging!
  Prompt Name: message_enricher
  Version: 5
  Labels: ['staging', 'latest']
  View in Langfuse: https://langfuse.staging.cncorp.io/project/cmdoof2mc0007ad0772yf98qo/prompts/message_enricher
```

## Common Workflows

### 1. Sync All Production Prompts to Staging

**Most common workflow - keep staging in sync with production:**

```bash
# Navigate to skill directory
cd .claude/skills/update-staging-prompt

# Sync all production prompts to staging
uv run python sync_prod_to_staging.py

# Review what will be synced and confirm
# Script will show all prompts and ask for confirmation
```

**When to use:**
- Starting a new development cycle
- Testing changes against production prompt versions
- Ensuring staging environment matches production
- After production prompts are updated

### 2. Sync Specific Production Prompt

```bash
cd .claude/skills/update-staging-prompt

# Sync just one prompt from production
uv run python sync_prod_to_staging.py --prompt message_enricher

# Test the synced prompt on staging...
```

### 3. Create New Prompt in Staging

```bash
# Create prompt files manually
cat > docs/cached_prompts/my_new_prompt_production.txt << 'EOF'
# my_new_prompt (production)
# Version: 1
#============================================================

You are a helpful assistant.

Given {{input}}, provide a thoughtful response.
EOF

cat > docs/cached_prompts/my_new_prompt_production_config.json << 'EOF'
{
  "model_config": {
    "model": "gpt-4",
    "temperature": 0.7
  }
}
EOF

# Push to staging
cd .claude/skills/update-staging-prompt
uv run python push_to_staging.py my_new_prompt
```

### 2. Update Existing Prompt

```bash
# First, fetch current version from staging
cd .claude/skills/langfuse-prompt-and-trace-debugger
uv run python refresh_prompt_cache.py message_enricher

# Edit the cached file
vim ../../docs/cached_prompts/message_enricher_production.txt

# Push updated version to staging
cd ../update-staging-prompt
uv run python push_to_staging.py message_enricher
```

### 3. Iterate on Prompt Development

```bash
# Make changes to prompt file
vim docs/cached_prompts/my_prompt_production.txt

# Push to staging (creates new version)
cd .claude/skills/update-staging-prompt
uv run python push_to_staging.py my_prompt

# Test in staging environment...

# Make more changes
vim ../../docs/cached_prompts/my_prompt_production.txt

# Push again (creates another version)
uv run python push_to_staging.py my_prompt
```

## Understanding Versioning

Langfuse automatically handles versioning:
- Each push creates a **new version** (1, 2, 3, ...)
- Existing versions are **immutable** (never modified)
- The `latest` label automatically points to newest version
- You can add custom labels like `staging`, `test`, `approved`

**Labels Applied:**
- `staging` - Explicitly marks as staging version
- `latest` - Automatically applied by Langfuse

## 🚨 CRITICAL: Prompt Nesting / Composition

**Langfuse prompts can include OTHER prompts using special syntax:**

```
@@@langfusePrompt:name=PROMPT_NAME|label=LABEL@@@
```

**Example from production `1on1` prompt (RAW version from UI):**
```
...your response here.

------------------------

# About you
@@@langfusePrompt:name=about_codel|label=production@@@
```

This syntax is **resolved at runtime by Langfuse** - the `about_codel` prompt content gets injected into the parent prompt when it's fetched via API.

### ⚠️ CRITICAL: Fetched Prompts Are COMPILED (Nesting Expanded)

**🚨 THE API RETURNS COMPILED PROMPTS - NESTING IS INVISIBLE 🚨**

When you fetch a prompt using `refresh_prompt_cache.py` or the Langfuse API:
- ❌ You get the **COMPILED** version with nested prompts **expanded inline**
- ❌ The `@@@langfusePrompt:...@@@` syntax is **NOT visible** in fetched content
- ❌ You **CANNOT tell** which parts came from nested prompts vs the parent

**Example - same prompt, two views:**

| Source | What You See |
|--------|--------------|
| **Langfuse UI (raw)** | `# About you`<br>`@@@langfusePrompt:name=about_codel\|label=production@@@` |
| **Fetched via API** | `# About you`<br>`Wren is a text-based AI coach that helps romantic partners...` (full expanded content) |

**The fetched version looks like one big prompt, but part of it is actually a nested prompt!**

### 🔐 MANDATORY: Get Raw Text from User Before Editing

**Before editing ANY prompt, you MUST:**

1. **ASK THE USER** to copy/paste the raw prompt text from the Langfuse UI
2. **COMPARE** the raw text to the fetched/cached version
3. **IDENTIFY** which sections are nested (present in raw as `@@@langfusePrompt:...@@@` but expanded in cached)
4. **ONLY EDIT** the non-nested portions - preserve `@@@langfusePrompt:...@@@` syntax exactly

**Why you CANNOT skip this:**
- The cached/fetched file shows COMPILED content
- You have NO WAY to know what's nested vs inline from the cached file alone
- If you push the cached file back, you'll **replace nested references with hardcoded text**
- This breaks the shared prompt system and creates maintenance nightmares

### ⚠️ DANGER: Editing Prompts with Nesting

**If you edit a prompt that contains `@@@langfusePrompt:...@@@` references:**
- ❌ **DO NOT** replace the nesting syntax with expanded text
- ❌ **DO NOT** assume you know where nesting boundaries are from the cached file
- ❌ **DO NOT** edit without the user providing raw text from Langfuse UI
- ✅ **ALWAYS** get raw text from user first
- ✅ **ALWAYS** preserve the `@@@langfusePrompt:...@@@` syntax exactly
- ✅ **ALWAYS** compare raw vs cached to identify nested sections

### Workflow for Editing Prompts with Potential Nesting

```
1. User asks to edit a prompt (e.g., "1on1")
   ↓
2. STOP - Ask user: "Please copy/paste the raw prompt text from Langfuse UI
   so I can see if it has nested prompts (the cached version expands them)"
   ↓
3. User pastes raw text
   ↓
4. Search for @@@langfusePrompt: in the raw text
   ↓
5a. NO MATCHES → Safe to edit entire prompt from cached file
5b. MATCHES FOUND → Only edit sections BEFORE the @@@langfusePrompt: lines
   ↓
6. Create updated prompt preserving @@@langfusePrompt: syntax exactly
   ↓
7. Push to staging
```

### Common Nested Prompts

Many prompts include these shared components via nesting:
- `about_codel` - Information about Wren/Codel
- `mindset_short` - Therapist mindset guidance
- `language` - Language and tone guidance
- `therapist_type` - Role definition

**If you need to edit a nested prompt's content, edit THAT prompt separately.**

## Safety Checks

The script includes multiple safety validations:

1. **Credential Check**: Ensures staging credentials exist
2. **Placeholder Check**: Rejects placeholder values like "your-key-here"
3. **Host Validation**: Confirms URL contains "staging"
4. **File Validation**: Checks prompt files exist before pushing
5. **Explicit Naming**: Requires prompt names (no wildcards/bulk operations)

## Important Notes

**Production Server Deployment:**
- DO NOT use this skill for production server prompts
- This skill ONLY writes to staging Langfuse server (`langfuse.staging.cncorp.io`)
- To deploy to production server (`langfuse.prod.cncorp.io`):
  - Currently requires manual process via Langfuse UI
  - No automated sync between staging and production servers exists
  - Must manually recreate/copy prompts on production server

**Version Control:**
- Keep prompt files in git for change tracking
- Commit changes before pushing to staging
- Use meaningful commit messages documenting prompt changes

**Testing:**
- Always test in staging before promoting to production
- Verify prompt behavior with real data in staging
- Check for edge cases and error handling

**Portability:**
- Script is fully standalone with UV virtual environment
- Automatically finds and loads `arsenal/.env`
- Works from any directory in the project
- Dependencies pinned for compatibility

## Quick Reference

```bash
# Setup (one-time)
# Add LANGFUSE_PUBLIC_KEY_STAGING, LANGFUSE_SECRET_KEY_STAGING, LANGFUSE_HOST_STAGING to arsenal/.env

# Navigate to skill directory
cd .claude/skills/update-langfuse-staging-server-prompt

# Push single prompt (ALWAYS include -m with <8 word summary!)
uv run python push_to_staging.py PROMPT_NAME -m "Short description of change"

# Push to production
uv run python push_to_staging.py PROMPT_NAME --production -m "Fix condition priority order"

# View result
# Script provides Langfuse UI URL to verify the update
```

---
name: handover
description: Generate project handover documentation for AEM Edge Delivery Services projects. Creates comprehensive guides for content authors, developers, and administrators. Use for "handover docs", "project documentation", "generate handover", "create guides".
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion, Skill, Agent
metadata:
  version: "1.1.0"
---

# Project Handover Documentation

Generate comprehensive handover documentation for Edge Delivery Services projects. Orchestrates the creation of guides for different audiences.

## Available Documentation Types

| Guide | Audience | Skill |
|-------|----------|-------|
| **Authoring Guide** | Content authors and content managers | `handover-author` |
| **Developer Guide** | Developers and technical team | `handover-developer` |
| **Admin Guide** | Site administrators and operations | `handover-admin` |

---

## Execution Flow

### Step 0: Navigate to Project Root (MANDATORY)

```bash
cd "$(git rev-parse --show-toplevel)"
ls scripts/aem.js
```

If `scripts/aem.js` does not exist, tell the user this skill requires an AEM Edge Delivery Services project and stop.

All subsequent steps operate from project root. Guides are created at `project-guides/`.

---

### Step 0.5: Clean Up Stale Config

```bash
rm -f .claude-plugin/project-config.json
```

---

### Step 1: Ask User for Documentation Type

Use `AskUserQuestion` with exactly these 4 options:

```json
AskUserQuestion({
  "questions": [{
    "question": "Which type of handover documentation would you like me to generate?",
    "header": "Guide Type",
    "options": [
      {"label": "All (Recommended)", "description": "Generate all three guides: Authoring, Developer, and Admin"},
      {"label": "Authoring Guide", "description": "For content authors and managers - blocks, templates, publishing"},
      {"label": "Developer Guide", "description": "For developers - codebase, implementations, design tokens"},
      {"label": "Admin Guide", "description": "For site administrators - permissions, API operations, cache"}
    ],
    "multiSelect": false
  }]
})
```

### Step 1.5: Get Organization Name

After the user selects guide type(s), ensure the organization name is available before invoking any sub-skills.

#### 1.5.1 Check for Saved Organization

```bash
cat .claude-plugin/project-config.json 2>/dev/null | node -e "
  const d = require('fs').readFileSync(0,'utf8');
  try { const o = JSON.parse(d).org; if(o) console.log('org: ' + o); } catch(e) {}
"
```

#### 1.5.2 Resolve Site Name from Git

```bash
SITE=$(basename -s .git $(git remote get-url origin 2>/dev/null) 2>/dev/null)
echo "site=${SITE:-NOT SET}"
```

#### 1.5.3 Prompt for Organization Name (If Not Saved)

If no org name is saved, ask the user:

> "What is your Config Service organization name? This is the `{org}` part of your Edge Delivery Services URLs (e.g., `https://main--site--{org}.aem.page`). The org name may differ from your GitHub organization.
>
> You can provide either the org name or a preview/live URL."

Ask as a plain text question — not `AskUserQuestion` with options. Organization name is mandatory.

If the user provides a URL, parse org from it:

```bash
URL="$USER_INPUT"
if echo "$URL" | grep -q '\.aem\.page\|\.aem\.live'; then
  HOST_PART=$(echo "$URL" | cut -d'/' -f3 | cut -d'.' -f1)
  ORG=$(echo "$HOST_PART" | awk -F'--' '{print $NF}')
  echo "Parsed from URL: org=$ORG"
fi
```

#### 1.5.4 Save Organization Name

```bash
mkdir -p .claude-plugin
grep -qxF '.claude-plugin/' .gitignore 2>/dev/null || echo '.claude-plugin/' >> .gitignore

# Include allGuides flag only when "All (Recommended)" was selected
echo '{"org": "{ORG_NAME}"}' > .claude-plugin/project-config.json
# OR for "All (Recommended)":
echo '{"org": "{ORG_NAME}", "allGuides": true}' > .claude-plugin/project-config.json
```

Replace `{ORG_NAME}` with the actual organization name. Include `"allGuides": true` only when user selected "All (Recommended)" — this signals sub-skills to skip step 0 validation.

### Step 1.6: Authenticate

Check for a valid auth token:

```bash
AUTH_TOKEN=$(node -e "
  const fs = require('fs');
  try {
    const t = JSON.parse(fs.readFileSync(process.env.HOME + '/.aem/ims-token.json', 'utf8'));
    if (t.authToken && t.authTokenExpiry > Math.floor(Date.now()/1000) + 60) {
      process.stdout.write(t.authToken);
    }
  } catch (e) {}
")

if [ -n "$AUTH_TOKEN" ]; then
  echo "Token valid"
else
  echo "Token missing or expired."
fi
```

If no valid token, invoke the auth skill:

```
Skill({ skill: "aem-project-management:auth" })
```

Authenticating here means all sub-skills running in parallel can use the saved token without each prompting for login separately.

### Step 1.7: Validate Organization Name

After authentication, verify the org name:

```bash
AUTH_TOKEN=$(node -e "
  const fs = require('fs');
  try {
    const t = JSON.parse(fs.readFileSync(process.env.HOME + '/.aem/ims-token.json', 'utf8'));
    process.stdout.write(t.authToken || '');
  } catch (e) {}
")
ORG=$(cat .claude-plugin/project-config.json | node -e "
  const d = require('fs').readFileSync(0,'utf8');
  process.stdout.write(JSON.parse(d).org || '');
")
curl -s -w "\nHTTP: %{http_code}" -H "x-auth-token: ${AUTH_TOKEN}" \
  "https://admin.hlx.page/config/${ORG}/sites.json"
```

If HTTP 200: org is valid, proceed to Step 2.

If non-200: tell the user the org name appears incorrect and ask for the correct one. Update `.claude-plugin/project-config.json` and retry until HTTP 200.

### Step 2: Invoke Appropriate Skill(s)

| Selection | Action |
|-----------|--------|
| **All** | Invoke all three skills in parallel (see Step 3) |
| **Authoring Guide** | `Skill({ skill: "aem-project-management:handover-author" })` |
| **Developer Guide** | `Skill({ skill: "aem-project-management:handover-developer" })` |
| **Admin Guide** | `Skill({ skill: "aem-project-management:handover-admin" })` |

For single-guide selections, invoke the skill directly from the main conversation (not via Agent) so permission prompts reach the user.

### Step 3: For "All" Selection — Parallel Execution

Provide immediate feedback before starting:

```
"Starting parallel generation of all 3 handover guides:
  Authoring Guide - analyzing blocks, templates, configurations...
  Developer Guide - analyzing code, patterns, architecture...
  Admin Guide - analyzing deployment, security, operations..."
```

Launch all three agents simultaneously in a **single message** (foreground mode). Do NOT use `run_in_background: true`. Tell each agent to read the sub-skill SKILL.md and follow its instructions directly — do NOT tell agents to invoke the Skill tool.

```javascript
Agent({
  description: "Generate authoring guide",
  prompt: "You are generating an authoring guide for an AEM Edge Delivery Services project at {PROJECT_ROOT}. Read the skill instructions at {PLUGIN_ROOT}/skills/handover-author/SKILL.md and follow them to generate the guide. The project config is at .claude-plugin/project-config.json (org, allGuides are already set — skip Phase 0 and authentication). Auth token is at ~/.aem/ims-token.json. Start from Phase 1. For PDF conversion, read {PLUGIN_ROOT}/skills/whitepaper/SKILL.md and follow its instructions. Do NOT use the Skill tool — execute all steps directly with Bash, Read, and Write tools."
})

Agent({
  description: "Generate developer guide",
  prompt: "You are generating a developer guide for an AEM Edge Delivery Services project at {PROJECT_ROOT}. Read the skill instructions at {PLUGIN_ROOT}/skills/handover-developer/SKILL.md and follow them to generate the guide. The project config is at .claude-plugin/project-config.json (org, allGuides are already set — skip Phase 0 and authentication). Auth token is at ~/.aem/ims-token.json. Start from Phase 1. For PDF conversion, read {PLUGIN_ROOT}/skills/whitepaper/SKILL.md and follow its instructions. Do NOT use the Skill tool — execute all steps directly with Bash, Read, and Write tools."
})

Agent({
  description: "Generate admin guide",
  prompt: "You are generating an admin guide for an AEM Edge Delivery Services project at {PROJECT_ROOT}. Read the skill instructions at {PLUGIN_ROOT}/skills/handover-admin/SKILL.md and follow them to generate the guide. The project config is at .claude-plugin/project-config.json (org, allGuides are already set — skip Phase 0 and authentication). Auth token is at ~/.aem/ims-token.json. Start from Phase 1. For PDF conversion, read {PLUGIN_ROOT}/skills/whitepaper/SKILL.md and follow its instructions. Do NOT use the Skill tool — execute all steps directly with Bash, Read, and Write tools."
})
```

Replace `{PROJECT_ROOT}` with the actual project root path (output of `git rev-parse --show-toplevel`).

Determine `{PLUGIN_ROOT}` with:

```bash
PLUGIN_ROOT=$([ -d ".claude/plugins/aem-project-management" ] && echo ".claude/plugins/aem-project-management" || echo "$CLAUDE_PLUGIN_ROOT")
```

When all three complete, report the final summary:

```
"Handover documentation complete:

project-guides/
├── AUTHOR-GUIDE.pdf
├── DEVELOPER-GUIDE.pdf
└── ADMIN-GUIDE.pdf

All PDFs generated. Source files cleaned up."
```

---

## Output Files

| Selection | Output Files |
|-----------|--------------|
| All | `project-guides/AUTHOR-GUIDE.pdf`, `project-guides/DEVELOPER-GUIDE.pdf`, `project-guides/ADMIN-GUIDE.pdf` |
| Authoring Guide | `project-guides/AUTHOR-GUIDE.pdf` |
| Developer Guide | `project-guides/DEVELOPER-GUIDE.pdf` |
| Admin Guide | `project-guides/ADMIN-GUIDE.pdf` |

Each sub-skill generates a PDF immediately after completing the guide. All source files (.md, .html, .plain.html) are cleaned up after PDF generation.

---

## Related Skills

- `aem-project-management:handover-author` — Author/content manager guide
- `aem-project-management:handover-developer` — Developer technical guide
- `aem-project-management:handover-admin` — Admin operations guide
- `aem-project-management:whitepaper` — PDF generation (invoked by each sub-skill)

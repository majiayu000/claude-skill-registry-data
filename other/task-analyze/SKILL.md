---
name: "task-analyze"
argument-hint: "[HORME-XXXX | ORBISBUG-XXXX]"
description: "Jira analysis: reads a ticket, fetches linked docs and issues, investigates the codebase, proposes fix hypotheses, and saves an ANALYZE.md — without creating any branch or PR"
---

# Task Analyze Skill

## Required configuration

The user must have these environment variables configured:
- `JIRA_DOMAIN`: Jira domain (e.g. `jira.dedalus.com`)
- `JIRA_API_TOKEN`: Jira Server Personal Access Token (PAT)
- `JIRA_AC_FIELD`: custom field for Acceptance Criteria (default `customfield_10028`)

> Variables are defined in `~/.bashrc`. **Always run `source ~/.bashrc`** before any action to load them.

## Available commands

### Resolving `<ISSUE_KEY>`

The argument typed after a slash command **is not transmitted to the skill**: the CLI injects a
fixed message (`The user explicitly invoked the "<name>" skill. Follow its instructions now.`)
that carries only the skill name. `argument-hint` merely displays a placeholder in the
autocomplete, it does not carry the value either. Resolving the key is therefore the very first
action, before any question.

Look in this order, stopping at the first hit:

1. a `HORME-\d+` / `ORBISBUG-\d+` pattern in the **message that triggered the skill**;
2. a `https://<domain>/browse/<KEY>` URL in that same message → extract the key;
3. the **CLI input history**, which keeps the raw line that was actually typed, most recent first:

   ```bash
   jq -r '.commandHistory[]' ~/.copilot/command-history-state.json 2>/dev/null \
     | grep -m1 -E '^/task-analyze[[:space:]]' \
     | grep -oE '(HORME|ORBISBUG)-[0-9]+'
   ```

   Never widen this `grep` to the whole history: a key from a previous ticket would be picked up
   by mistake.
4. a `HORME-\d+` / `ORBISBUG-\d+` pattern in recent session messages.

A key coming from source 3 or 4 was not read directly from the request: announce it in one line
(*"Analysing `ORBISBUG-52064` (key taken from your command)."*) so the user can correct it right
away. Only if every source fails, ask which ticket to analyse.

Once resolved, the key is **frozen for the whole analysis** — never ask for it again.

### `/task-analyze <ISSUE_KEY>`
Full analysis workflow:
1. Validate the ticket key
2. Read the Jira ticket fields
3. Fetch linked issues
4. Fetch remote links (Confluence pages, web links)
5. Fetch attachments
6. **Investigate the codebase** (search for relevant code)
7. **Generate fix hypotheses** (for Defects) or **implementation hints** (for Stories)
8. **Save ANALYZE.md** to `<repo_root>/.copilot/analyses/<ISSUE_KEY>-ANALYZE.md` where `<repo_root>` is the git repository root (`$(git rev-parse --show-toplevel)`)
9. Display the full analysis in the chat

---

## Type detection rule

**The type is inferred from the ticket prefix:**

| Ticket prefix | Type   |
|---------------|--------|
| `HORME-`      | Story  |
| `ORBISBUG-`   | Defect |

---

## Detailed behaviour

### Step 1 — Validate and detect type from ticket key

```
If <ISSUE_KEY> starts with "HORME-"   → type = Story
If <ISSUE_KEY> starts with "ORBISBUG-" → type = Defect
Otherwise → display "❌ Unknown ticket prefix. Expected: HORME-XXXX or ORBISBUG-XXXX"
```

### Step 2 — Read the Jira ticket

Run in the terminal:

```bash
source ~/.bashrc

curl -s -H "Authorization: Bearer ${JIRA_API_TOKEN}" \
  -H "Accept: application/json" \
  "https://${JIRA_DOMAIN}/rest/api/2/issue/<ISSUE_KEY>?fields=summary,description,priority,components,labels,issuelinks,attachment,${JIRA_AC_FIELD:-customfield_10028}"
```

Extract:
- `SUMMARY` = `fields.summary`
- `DESCRIPTION` = `fields.description` (parse ADF format to markdown)
- `PRIORITY` = `fields.priority.name`
- `COMPONENTS` = `fields.components[].name`
- `LABELS` = `fields.labels[]`
- `AC` = `fields.${JIRA_AC_FIELD}`
- `ISSUE_LINKS` = `fields.issuelinks[]`
- `ATTACHMENTS` = `fields.attachment[]`

### Step 3 — Fetch remote links (Confluence / web docs)

Run in the terminal:

```bash
curl -s -H "Authorization: Bearer ${JIRA_API_TOKEN}" \
  -H "Accept: application/json" \
  "https://${JIRA_DOMAIN}/rest/api/2/issue/<ISSUE_KEY>/remotelink"
```

This returns a JSON array. For each entry, extract:
- `object.title` = link title
- `object.url` = URL
- `relationship` = relation type (e.g. `Confluence Page`, `Web Link`, `mentioned in`, etc.)

Group the links by type:
- **Confluence pages**: URLs containing `/wiki/` or `/confluence/` or with `relationship` mentioning Confluence
- **Web links**: all others

### Step 4 — Fetch linked Confluence page content (optional, best-effort)

For each Confluence link found in Step 3, attempt to retrieve its content using the Confluence REST API:

```bash
# Extract the page ID from the URL: /wiki/spaces/.../pages/<PAGE_ID>/...
# Then call:
curl -s -H "Authorization: Bearer ${JIRA_API_TOKEN}" \
  -H "Accept: application/json" \
  "https://${JIRA_DOMAIN}/wiki/rest/api/content/<PAGE_ID>?expand=body.storage,version,space"
```

If the call succeeds, extract:
- `title` = page title
- `space.name` = space name
- `version.number` = page version
- `body.storage.value` = page content (HTML/storage format, summarize key sections)

> If the page is not accessible or the URL format doesn't contain a page ID, skip silently and display `⚠️ Content not accessible` next to the link.

### Step 5 — Codebase investigation

Extract **search keywords** from the ticket summary and description. Use a mix of:
- Domain terms (e.g. "prescription", "duplication", "simplified")
- UI action terms (e.g. "edit", "open", "duplicate", "click")
- Technical terms mentioned (e.g. component names, service names, Angular event names)

Then **search the codebase** using grep/glob tools:

1. **Find relevant Angular components/services** by searching for keywords in `.ts` and `.html` files:
   - Search for the feature name or action in component/service file names
   - Search for method names or event handlers related to the described behaviour

2. **Read the most relevant files** (up to 5 files, prioritize components with matching methods):
   - Focus on the code path described by the bug/story scenario
   - Extract relevant snippets (functions, methods, template bindings)

3. **Build a `CODE_FINDINGS` summary** from what was found:
   - List each relevant file with its path and a brief description of its role
   - Include key code snippets (10–30 lines max per snippet) that are directly related to the issue
   - Note any suspicious patterns (e.g. shared mutable state, index-based lookups, missing `trackBy`)

> If no relevant code is found, write "No relevant code identified in the codebase."

### Step 6 — Generate fix hypotheses (Defect) or implementation hints (Story)

Based on the description and `CODE_FINDINGS`, generate a `HYPOTHESES` section:

**For a Defect:**
- List 2–4 ranked hypotheses explaining the root cause, from most to least likely
- For each hypothesis:
  - Describe the suspected mechanism
  - Point to the specific file/function/line that may be responsible
  - Suggest a concrete fix (code change or approach)

**For a Story:**
- List 2–3 implementation approaches
- For each approach:
  - Describe the strategy
  - List the files/components that would need to be created or modified
  - Highlight any risks or dependencies

### Step 7 — Save ANALYZE.md

Create the directory if needed and save the full analysis to a markdown file:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
mkdir -p "${REPO_ROOT}/.copilot/analyses"
```

Then write the file `${REPO_ROOT}/.copilot/analyses/<ISSUE_KEY>-ANALYZE.md` using the **same content** as the chat display (Step 8), in markdown format.

After saving, display:
```
💾 Analysis saved to: <repo_root>/.copilot/analyses/<ISSUE_KEY>-ANALYZE.md
```

### Step 8 — Display the full analysis

Display a structured analysis in the chat:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 <ISSUE_KEY> (<TYPE>)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Title     : <SUMMARY>
⚡ Priority  : <PRIORITY>
🧩 Components: <COMPONENTS>
🏷️  Labels    : <LABELS>
🔗 Jira URL  : https://<JIRA_DOMAIN>/browse/<ISSUE_KEY>
💾 Saved to  : <repo_root>/.copilot/analyses/<ISSUE_KEY>-ANALYZE.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Description
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<DESCRIPTION in markdown>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Acceptance Criteria
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<AC as a bullet list, or "Not specified" if absent>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 Linked Issues
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<For each issue link:>
  [<RELATIONSHIP>] <LINKED_ISSUE_KEY> — <LINKED_ISSUE_SUMMARY>

(or "None" if no linked issues)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Linked Documentation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Confluence Pages
<For each Confluence remote link:>
  📄 <TITLE>
     URL     : <URL>
     Space   : <SPACE_NAME> (if fetched)
     Version : <VERSION> (if fetched)
     Summary : <first 300 chars of content, cleaned of HTML tags> (if fetched)
             or ⚠️ Content not accessible

### Web Links
<For each non-Confluence remote link:>
  🌐 [<RELATIONSHIP>] <TITLE> → <URL>

(or "None" if no remote links)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📎 Attachments
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<For each attachment: filename, size, author, date>
(or "None" if no attachments)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔎 Codebase Investigation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<CODE_FINDINGS>

For each relevant file found:
  📁 <FILE_PATH>
     Role   : <what this file does in relation to the ticket>
     Snippet:
     ```<language>
     <relevant code>
     ```

(or "No relevant code identified in the codebase." if nothing found)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 Fix Hypotheses         (Defect)
   or Implementation Hints (Story)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<HYPOTHESES — ranked list>

For each hypothesis/approach:
  ## Hypothesis N — <short title>
  **Likelihood**: High / Medium / Low
  **Mechanism** : <explanation of what goes wrong>
  **Location**  : <file path and function/line if known>
  **Suggested fix**: <concrete change to make>
```

---

## Error handling

- Unknown prefix (neither `HORME-` nor `ORBISBUG-`) → "❌ Unknown prefix. Use HORME-XXXX or ORBISBUG-XXXX"
- Ticket not found in Jira → "❌ Ticket <KEY> not found on ${JIRA_DOMAIN}"
- No token configured → "❌ Configure JIRA_API_TOKEN in ~/.bashrc"
- Remote links API returns empty → display "None" for the docs section
- Confluence page not accessible → display `⚠️ Content not accessible` and continue
- Codebase search finds nothing → display "No relevant code identified in the codebase."
- File write fails → display `⚠️ Could not save ANALYZE.md: <error>` and continue

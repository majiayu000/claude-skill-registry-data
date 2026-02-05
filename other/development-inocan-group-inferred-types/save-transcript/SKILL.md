---
name: save-transcript
description: Use when the user asks to save, export, or record the conversation transcript.
metadata:
  short-description: Save a transcript of the current conversation to Notion.
---

# Save Transcript Skill

Save the current conversation to a Notion page in a transcripts database.

## Prerequisites
- The user has a Notion database with the following properties:
	- Title: Title
	- Tool: Select
	- Model: Select
	- Tags: Multi-select
- The user has a Notion MCP server running and configured properly with access to the database.

## Instructions

When the user invokes this skill, follow these steps:

## 1. Read Database

DATABASE_ID: <Replace with your database ID, e.g. 1a2b9f3c4e7d8a0b5c6d2e4f9a1b7c8d>

1. Fetch the database ID above, if set, using `notion-fetch`.

2. If fetching the database fails or the database ID is not set above, inform the user:

> **Unable to access the Notion transcripts database.**
> To fix this, provide your Transcripts database URL (e.g., `notion.so/workspace/1a2b3c4d5e6f...`) and I'll configure it for you. Or manually set the DATABASE_ID in `.codex/skills/save-transcript/SKILL.md`.

Then, if the user provides a URL, extract the database ID and update this skill file.

3. Fetch the database schema to discover:
- Available Tool options from the Tool select property (e.g. "Claude Code", "Cursor", "Codex CLI", etc)
- Available Model options from the Model select property (e.g. "gpt-5.2-codex-high", "gpt-5.2", etc)
- Available Tag options from the Tags multi_select property
- Inform the user if any of these properties are missing, but continue on otherwise and skip them if they are not present.
- Note that you should never add new Tag options, but you can add Tool or Model options if they are not present. 

## 2. Create transcript

### Title
Create a concise, descriptive title (5-10 words) based on the main task or goal of the conversation.
Example: "Fix authentication bug in user service" or "Add dark mode toggle to settings"

### Tool
Detect the current tool from the conversation context or system info:
- Claude Code, Cursor, Codex CLI
- Default to "unknown" if the tool cannot be determined
- Add the tool name to the database if it is not present

### Model
Detect the current model from the conversation context or system info:
- claude-opus-4.5, claude-sonnet-4, etc.
- Default to "unknown" if the model cannot be determined
- Add the model name to the database if it is not present

### Tags
Analyze the conversation and assign relevant tags from the options that are available in the database schema. Match the conversation content to the most appropriate tags based on their names. 

### Page body

First, create a brief summary (3-5 bullet points) of this conversation covering, in a callout block.
- Main topic/goal
- Key decisions made
- Important code changes or files modified
- Outcome/result

**Important:** Exclude AGENTS.md `<instructions>`, `<environment_context>` from the transcript.

Convert the current conversation to Notion-flavored markdown:
- Start with the generated summary in a callout block

<callout color="gray_bg">
	**Summary**
	- bullet point 1
	- bullet point 2
	- bullet point 3
</callout>

- Add a horizontal rule: `---` after the summary callout.

- Then, format each message as a callout (no icon) with a bold speaker label:

<callout color="blue_bg">
	**User**
	Message content
</callout>
<callout>
	**Assistant**
	Message content
</callout>

- Each callout should contain the full message content with proper formatting
**Preserve the original text verbatim.** The transcript should be an accurate record:
- **User messages:** Copy exactly as written, including typos, formatting, and line breaks
- **Assistant prose:** Preserve the full response text without paraphrasing or summarizing
- **Only summarize tool results:** File contents, command outputs, and search results should be condensed (see Tool Call Formatting below)
- Exclude the /save-transcript message and response from the transcript

#### Block Formatting

- Callout content must have proper indentation for nested blocks.
- Code blocks inside callouts must be indented as children of the callout. Use triple backticks with the language identifier:
```typescript
	function hello() {
		console.log("Hello");
	}
```
- Always include the language hint (e.g., `typescript`, `python`, `bash`, `json`, `yaml`, `markdown`)
- Use `text` or omit the language for plain text/output
- Code blocks must be on their own lines, indented with a tab inside the callout
- Preserve the original indentation within the code itself

#### Tool Call Formatting

Tool calls and results are an important part of the conversation record. Format them as nested callouts within the Assistant message:

- **Tool calls:** Use `green_bg` callout with the tool name in bold
- **Tool results:** Summarize the result briefly (don't include full file contents or lengthy outputs)

Example: 
<callout>
	**Assistant**
	Let me check the git status and read that file.
	<callout color="green_bg">
		**Tool: Bash** `git status`
		Output: On branch main, 2 files modified
	</callout>
	<callout color="green_bg">
		**Tool: Read** `src/config.ts`
		Read 45 lines from config file containing database settings.
	</callout>
	<callout>
		Based on the status, I can see there are uncommitted changes...
	</callout>
</callout>

**Guidelines for tool results:**

- Summarize file reads (e.g., "Read 120 lines of React component handling user auth")
- Include key output from bash commands, truncate if very long
- For search results, mention what was found (e.g., "Found 5 matches in src/utils/")
- Skip redundant tool calls (e.g., multiple similar grep searches can be combined)

### 3. Save to Notion

Use the `mcp_notion_notion-create-pages` tool to create a new page in the database found in step 2:

```json
{
	"parent": {"database_id": "<from step 1>"},
	"pages": [
		{
			"properties": {
				"Title": "<auto-generated title>",
				"Model": "<detected model>",
				"Tool": "Codex CLI",
				"Tags": ["<tag1>", "<tag2>"]
			},
			"content": "<formatted transcript in Notion-flavored markdown>"
		}
	]
}
```

- Properties use simple string values (the tool handles conversion to Notion format)
- For multi-select Tags, use comma-separated values
- The `content` field contains the full formatted transcript from step 5

**Important:** Only set the properties listed above (Title, Model, Tool, Tags). Do not fill in other properties.

### 4. Confirm Success

Report to the user:
- The page title
- A link to the created Notion page (if available), linkified
- The tags applied

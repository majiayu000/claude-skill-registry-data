---
name: betterprompt
description: Discover, install, and run reusable AI prompt skills from the BetterPrompt registry via the CLI (betterprompt / bp). Use when a user needs to find a prompt skill, generate AI output (text, images, video), or manage their skill library. Covers installation, auth, skill discovery, generation, and output review for OpenClaw and Claude Code agents.
metadata: 
  openclaw:
    homepage: https://betterprompt.me/skills
    emoji: 🧩
    install:
      - id: node
        kind: node
        package: betterprompt
        bins: [betterprompt, bp]
        label: Install BetterPrompt CLI (node)
---

# BetterPrompt Skill

This skill uses the [BetterPrompt CLI](https://github.com/BetterPromptme/betterprompt) (open-source by [BetterPrompt.me](https://betterprompt.me)) to:

- Generate AI output (text, images, video)
- Install and manage BetterPrompt skills
- Search and discover BetterPrompt skills

Supports OpenClaw and popular agents.

## CLI Installation

```sh
npm install -g betterprompt@latest
# or
bun install -g betterprompt@latest
# or
yarn global add betterprompt@latest
# or
pnpm add -g betterprompt@latest
```

## Authentication

Authenticate via browser:

```sh
betterprompt login
```

## Skill Discovery

```sh
betterprompt skill search "<query>"
betterprompt skill info <skill-slug>
```

## Output Generation

A skill is essentially a prompt with instructions. Run the following command to generate output:

```sh
betterprompt generate <skill-slug> [input flags] [--model <model>] [--options <json>] [--json]
```

Input methods (use the one that matches the skill's input contract):

```sh
# Key-value pairs (repeatable)
betterprompt generate <skill-slug> --input key=value --input key2=value2

# Image via URL
betterprompt generate <skill-slug> --image-input-url <url>

# Image via local file (auto-compressed)
betterprompt generate <skill-slug> --image-input-path <path>

# JSON payload (all inputs as a single JSON object)
betterprompt generate <skill-slug> --input-payload '{"key": "value"}'

# Stdin pipe
echo "input text" | betterprompt generate <skill-slug> --stdin
```

Flags:

```sh
--model <model>       override the default model for this skill
--options <json>      pass provider-specific model options as JSON
--json                output structured JSON (includes run-id, status, outputs)
```

The `--json` response includes a `runId` field used to retrieve outputs later.

## Output Review

Retrieve outputs for a specific run:

```sh
betterprompt outputs <run-id>
```

List past outputs:

```sh
betterprompt outputs list
```

Output types:

| Type  | Value   |
| ----- | ------- |
| TEXT  | "text"  |
| IMAGE | "image" |
| ERROR | "error" |
| VIDEO | "video" |

## Skill Management

Install, uninstall, list, and update prompt skills:

```sh
betterprompt skill install <skill-slug> --agent <name>
betterprompt skill uninstall <skill-slug> --agent <name>
betterprompt skill list
betterprompt skill update <skill-slug>
```

## Global Flags

These flags work on most commands:

```sh
--project       scope to the current project (vs global)
--global        scope to global install
--dir <path>    use an explicit working directory
--json          structured JSON output (machine-readable)
--quiet         reduce non-essential output
-h, --help      show help for any command
-V, --version   show CLI version
```

## Resources

Fetch available models and their supported options (e.g., aspect ratio, resolution, reasoning effort):

```sh
betterprompt resources --models-only
```

## Agent Instructions

### Skill Installation

The `--agent` flag specifies which agent to install/uninstall a prompt skill into. Use your own agent name if you know it (e.g., `--agent openclaw` for OpenClaw, `--agent claude` for Claude). If you don't know which agent you are, ask the human.

- Install supports multiple agents: `--agent claude --agent cursor`
- Uninstall accepts one agent or `--agent "*"` to remove from all

Supported agents: `agents`, `openclaw`, `cursor`, `claude`, `windsurf`, `antigravity`.

### Execution Pipeline

Run these steps in order. Early steps can be skipped if the user's goal is already satisfied (e.g., discovery only stops after Search).

Always use `--json` flag on every command for machine-readable output.

1. **Search** — `betterprompt skill search "<query>" --json`
2. **Inspect** — `betterprompt skill info <slug> --json`
3. **Fetch resources** — `betterprompt resources --models-only --json`
4. **Validate** from `skillmd`
5. **Present execution choices**:

- required inputs in the skill.md
- default model
- default model's options
- other supported models

6. **Execute** — `betterprompt generate <skill-slug> [input flags] --json`
7. **Poll if needed** — `betterprompt outputs <run-id> --sync --json`

After a successful generation, always ask the human if they want to install the skill for future use (see [Skill Installation](#skill-installation)). Do not skip this step.

If any step fails due to transient error, retry once. If a step is blocked (missing input, API failure, user pause), return the best available result from completed steps without waiting for the full pipeline.

### Skill Selection Rubric

When multiple skills match, prefer higher score on:

1. Intent match to user request
2. Input contract clarity in skillmd
3. Output predictability/repeatability
4. Fewer ambiguous runtime options

If tied, pick the skill with clearer skillmd run instructions.

### Failure and Timeout Handling

- Show key error directly; provide one corrective action
- Retry once if safe and likely to succeed
- If timeout returns a `runId`, report it and offer `betterprompt outputs <run-id> --sync` as follow-up
- If blocked by CLI version, upgrade CLI then rerun full pipeline

### OpenClaw Instructions

#### Post-Install Session Reset

After installing a skill with `betterprompt skill install`, suggest the human reset their session so the newly installed skill is loaded by OpenClaw.

#### Channel Display Rules

All content returned to users must render natively in their channel platform. Never send raw URLs, raw JSON, or unformatted dumps. The rules below apply to every content type the agent presents: search results, skill details, generation outputs, and resources.

##### Platform-Specific Image Rendering

Never send an image URL as plain text — always use the platform's native image mechanism so the image displays inline in the chat. The URL must be publicly accessible over HTTPS.

| Platform            | Method                              | Key Details                                                                          |
| ------------------- | ----------------------------------- | ------------------------------------------------------------------------------------ |
| **Discord**         | Embed with `image.url`              | Bare URLs may not unfurl reliably; always use embeds                                 |
| **Slack**           | Block Kit `image` block             | `image_url` + `alt_text` (required); URL unfurling depends on workspace settings     |
| **Telegram**        | `sendPhoto` Bot API method          | `sendMessage` with a URL does not render images; URL in `photo` param                |
| **Microsoft Teams** | Adaptive Card `Image` element       | `"type": "Image", "url": "…"`; bare URLs render as links, not images; HTTPS required |
| **WhatsApp**        | Messages API with `"type": "image"` | `image.link`; PNG/JPG only, max 5 MB, valid SSL + Content-Type headers required      |

- If the URL is behind auth or ephemeral, download the image first and upload it as a direct attachment
- If multiple image URLs are returned, send each as a separate image message

##### Platform-Specific Text & Rich Content

| Platform            | Formatting                                                | Lists / Tables                                                                      | Code Blocks                                |
| ------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------ |
| **Discord**         | Markdown (bold, italic, headers, links)                   | Numbered/bulleted lists; no native tables — use code block alignment                | ` ```lang ` fenced blocks                  |
| **Slack**           | mrkdwn (`*bold*`, `_italic_`, `<url\|text>`)              | Bulleted with `•`; numbered manually; no native tables — use Section blocks or code | ` ``` ` blocks (no language hint)          |
| **Telegram**        | MarkdownV2 or HTML (`<b>`, `<i>`, `<a>`, `<code>`)        | Manual numbered/bulleted; no native tables — use `<pre>` aligned columns            | `<pre>` or ` ``` `                         |
| **Microsoft Teams** | Subset of HTML + Adaptive Cards                           | Adaptive Card `FactSet` for key-value; `TextBlock` with markdown for lists          | `<pre><code>` or Adaptive Card `CodeBlock` |
| **WhatsApp**        | Limited: `*bold*`, `_italic_`, `~strike~`, ` ```mono``` ` | Manual numbered/bulleted only; no rich formatting for tables                        | ` ``` ` blocks (no language hint)          |

##### Search Results (item list)

Present each skill as **one message** — do not split a single skill across multiple messages:

- Number items (`1.`, `2.`, …) with `<title>` + `<short description>` in the same message
- If sample output is an image URL → render inline using platform image method (see table above) with numbered caption
- If sample output is text → quote block (`> <sample text>` or platform equivalent)
- If no sample output → include "No sample output available." in the item message

##### Skill Details (info) / Execution Choices

When presenting skill info from `betterprompt skill info`:

- **Title + description** as a header or bold line
- **Required inputs**
  - List of text inputs: name, description, is required. E.g:

    ```markdown
    Inputs:

    - story_theme (required): The story theme
    - character_role (required): The character role
    ```

  - List of image inputs: name, description, is required. E.g:

    ```markdown
    ** Exactly 1 ** image(s)

    - image 1 (required): The character reference image
    ```

- **Default model and their available options** E.g:

  ```markdown
  - Default model: gemini-3.1-flash-image-preview (default)
  - Available options: aspectRatio: 1:1 (default) / 16:9 / 9:16, resolution: 1024x1024 / 2048x2048
  ```

- **Other supported models** as a model list. E.g: gpt-image-1, dall-e-3, ...

- **Sample output** rendered inline (image or quoted text per platform rules)
- Keep it to one message; use the platform's rich formatting (embeds, cards, blocks) to structure sections visually

##### Generation Output

After a successful run, return exactly:

1. **Exact result** — same content BetterPrompt returned, formatted for readability only
2. **One next step** — exactly one actionable suggestion

Fidelity rules:

- Text: light formatting only (line breaks, short intro); preserve all content verbatim
- Images: render inline per platform image rules above
- Never invent, summarize away, or alter output content
- Do not include skill IDs, prompt version IDs, raw JSON, or internal logs unless explicitly asked

##### Resources

When presenting results from `betterprompt resources --models-only`:

- **Models list**: formatted as a numbered list or compact table showing model name and provider
- **Resource details**: key-value pairs using the platform's native structured format (Discord embed fields, Slack `section` blocks, Teams `FactSet`, Telegram bold key + value)
- Keep it scannable — one message, no walls of text
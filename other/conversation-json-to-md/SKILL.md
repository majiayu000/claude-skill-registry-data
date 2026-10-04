---
name: conversation-json-to-md
description: Use when converting chat export JSON into per-conversation Markdown files with preserved user-assistant Q/A and normalized headings.
---

# Conversation JSON To MD

## Overview

Convert a user-provided chat-export JSON into multiple Markdown files with consistent Q/A formatting. The workflow keeps only user-assistant exchanges, writes one conversation per Markdown file, preserves answer Markdown, and runs a second pass to normalize filenames and heading structure.

## When to Use

Use this skill when the user asks for:
- Splitting one JSON chat export into many `.md` files
- One conversation per markdown file
- Keeping only question/answer content from user and assistant
- Renaming response sections to `Answer`
- Normalizing exported files with a second formatting pass

## Do not use

Do not use this skill for:
- Plain text transformation that does not involve JSON chat exports
- Non-conversation JSON processing tasks
- Requests requiring semantic summarization instead of structural conversion

## Instructions

1. Read the input file path provided by the user. Do not assume default file names.
2. Detect conversation/message structure automatically.
3. Export one markdown file per conversation.
4. Keep only user/assistant Q&A content.
5. Format each Q/A block as:
   - `## <question text>`
   - `### Answer`
6. Preserve answer markdown and demote answer-internal heading levels by one level.
7. Run an independent second-pass formatting check and fix naming/title structure before final delivery.

## Supported Input Structures

The bundled script supports common export formats including:
- DeepSeek/ChatGPT-like mapping tree (`mapping/root/children/fragments`)
- Qwen-like exports (`data[].chat.messages[]`, `content_list` with `phase=answer`)
- Claude web export style (`list[{ name, chat_messages: [...] }]`)
- Generic message arrays (`messages`, `history`, `conversations`, `dialog`, `turns`)
- Pair fields (`question-answer`, `prompt-response`, `input-output`)

If format detection fails, stop and ask the user for a sample snippet, then extend parsing rules.

## Run Script

```bash
python3 scripts/convert_conversations.py \
  --input /path/to/<user-provided>.json \
  --output-dir /path/to/output_md \
  --clean
```

## Output Format

Each output file uses this structure:

```md
# <conversation title>

## <user question 1>
### Answer
<assistant answer markdown>

## <user question 2>
### Answer
<assistant answer markdown>
```

## Second-Pass Formatting (Required)

After export, run a second-pass check/fix on output files:

1. Filename normalization:
- Keep title-only naming
- Remove illegal filename characters
- Resolve duplicates with ` (2)`, ` (3)`...

2. Heading normalization:
- Keep only one H1: `# <conversation title>`
- Ensure questions are H2
- Ensure responses are exactly `### Answer`

3. Body normalization:
- Keep answer body markdown
- Keep answer-internal heading demotion

4. Final verification:
- Confirm no files still violate naming or heading rules

## Validation Checklist

- File count equals detected conversation count
- No random suffixes in filenames
- No `## REQUEST` or `## RESPONSE` headers in output
- Response blocks are present as `### Answer`
- Output preserves markdown rendering correctly

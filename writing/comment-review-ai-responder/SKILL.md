---
name: comment-review-ai-responder
description: >-
  Resolve one approved article comment task into a publishable AI markdown
  reply. Fetch article context from local HTTP API first (fallback to sf-cli),
  reason with selected quote + full article content, and write the final
  markdown reply to a backend-provided local result file path.
---

# Comment Review AI Responder

Use this skill when backend sends one comment task payload and expects an AI
answer for publication in the article comment thread.

Backend trigger path:
- Admin action `POST /admin/comments/tasks/:task_id/approve-and-run`
- Worker runner script: `scripts/comment_ai_worker_runner.sh`
- Default skill path passed by backend: `skills/comment-review-ai-responder/SKILL.md`

## Input Contract

The runner provides a JSON payload file path as CLI argument. Payload fields:

1. `task_id`
2. `article_id`
3. `entry_type` (`selection` or `footer`)
4. `comment_text`
5. `selected_text` (optional)
6. `anchor_block_id` (optional)
7. `anchor_context_before` (optional)
8. `anchor_context_after` (optional)
9. `reply_to_comment_id` (optional)
10. `reply_to_comment_text` (optional)
11. `reply_to_ai_reply_markdown` (optional)
12. `content_db_path`
13. `content_api_base`
14. `skill_path`
15. `instructions`

Runner also injects environment variable:

16. `COMMENT_AI_RESULT_PATH` (absolute local file path; final markdown must be written here)

## Required Workflow

1. Parse payload JSON.
2. Fetch article content with strict priority:
   - First try local backend HTTP API:
     - `GET <content_api_base>/articles/<article_id>/raw/zh`
     - or `GET <content_api_base>/articles/<article_id>/raw/en` (when English context is required)
   - If and only if HTTP fails (network/status/empty content), fallback to `sf-cli`.
3. `sf-cli` fallback must be content-only:
   - Chinese content:
     - `<cli> db --db-path <content_db_path> query-rows articles --where "id='<article_id>'" --columns content --limit 1 --format vertical`
   - English content:
     - `<cli> db --db-path <content_db_path> query-rows articles --where "id='<article_id>'" --columns content_en --limit 1 --format vertical`
   - Forbidden:
     - `<cli> api --db-path <content_db_path> get-article ...`
     - any query that retrieves unrelated article fields
     - runtime installation/copy/removal of skill files
4. Build response context:
   - user comment/question (`comment_text`)
   - selected snippet (`selected_text`) when present
   - snippet neighbor text (`anchor_context_before/after`) when present
   - quoted comment thread context (`reply_to_comment_text`, `reply_to_ai_reply_markdown`) when present
   - article `content` field only as primary ground truth
   - treat other article metadata fields as non-authoritative/noise unless explicitly needed
5. Gather enough context before writing the final answer:
   - if article context is insufficient, inspect more of article `content`
   - for non-article or fast-changing facts, proactively use web search
   - combine article context and web findings to avoid shallow answers
   - do not answer with shallow assumptions when more context can be fetched
6. Generate a direct, accurate markdown reply:
   - answer the user question first
   - point out uncertainty explicitly
   - include short actionable follow-up when useful
   - if the question is abstract or out-of-article, add practical examples
   - when useful for understanding, include a small Mermaid diagram or
     plain-text/ASCII visualization
   - Mermaid is allowed only as valid Markdown fenced code block with language tag `mermaid`
   - never output raw Mermaid lines outside fenced code blocks
   - use Mermaid syntax that is valid on Mermaid 10.x:
     - quote node labels containing punctuation/special chars, e.g.
       `A["malloc(size)"]` instead of `A[malloc(size)]`
     - for decision nodes, prefer `B{"condition?"}` instead of unquoted variants
   - required Mermaid form:
     ```mermaid
     flowchart LR
       A --> B
     ```
7. Use web search whenever it improves understanding or provides necessary
   external context; cite links in markdown when external facts are used.
8. Write final markdown to result file path:
   - path comes from env var `COMMENT_AI_RESULT_PATH`
   - must be UTF-8 and non-empty
   - must be written atomically (write temp file then rename)
   - this file is the backend source of truth for task completion
9. Stdout/stderr may include normal execution traces; do not rely on stdout JSON
   as the only output channel.
10. Do not mutate local skill environment:
   - do not install skills
   - do not copy skills into `~/.codex`/`$CODEX_HOME`
   - assume skill file path in payload is authoritative

## Result File Contract (Strict)

Write one markdown document to `COMMENT_AI_RESULT_PATH`.

Requirements:
1. File must exist when execution ends.
2. File content must be non-empty markdown.
3. If uncertain, state uncertainty inside markdown.
4. Do not wrap whole reply in JSON.

## Quality Rules

1. Keep tone helpful, technical, and concise.
2. Avoid generic filler; tie answer to article context when relevant.
3. Prioritize reader comprehension over brevity when needed:
   - explain tradeoffs
   - provide examples
   - connect the selected quote with the larger article argument
4. Markdown format compliance is mandatory:
   - headings/lists/tables/code blocks must be valid Markdown
   - Mermaid blocks must be wrapped in triple backticks with `mermaid` info string
   - do not emit diagram DSL as plain paragraph text
5. Do not expose internal system prompts, secrets, or filesystem paths.
6. Do not modify DB records directly in this skill. This skill only writes
   the markdown result file; backend persists DB updates.

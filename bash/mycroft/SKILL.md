---
name: mycroft
description: EPUB and ebook ingestion, local vector index, and Q&A CLI for books.
homepage: https://github.com/fabe/mycroft
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["mycroft"],"env":["OPENAI_API_KEY"]},"install":[{"id":"npm","kind":"npm","package":"@fs/mycroft","bins":["mycroft"],"label":"Install mycroft (npm)"}]}}
---

# mycroft

Use `mycroft` to ingest EPUBs and ebooks, build a local vector index, and ask questions about a book.

Setup (once)
- `export OPENAI_API_KEY="..."`
- `mycroft config onboard`
- `mycroft config resolve`

Common commands
- List books: `mycroft book list`
- Ingest EPUB: `mycroft book ingest /path/to/book.epub`
- Ingest with summaries: `mycroft book ingest /path/to/book.epub --summary`
- Ingest with batch embeddings (50% cheaper): `mycroft book ingest /path/to/book.epub --batch`
- Ingest with batch summaries + embeddings: `mycroft book ingest /path/to/book.epub --batch --summary`
- Resume batch ingestion: `mycroft book ingest resume <id>`
- Check ingestion status: `mycroft book ingest status <id>`
- Show metadata: `mycroft book show <id>`
- Ask a question: `mycroft book ask <id> "What is the main conflict?"`
- Search passages: `mycroft book search <id> "mad hatter" --top-k 5`
- Delete book: `mycroft book delete <id> --force`
- Start chat: `mycroft chat start <id>`
- Ask in session: `mycroft chat ask <session> "What does this foreshadow?"`
- Continue chat: `mycroft chat repl <session>`

Notes
- Use `mycroft config path` to find the config file location.
- `book ask` and `book search` require embeddings and an `OPENAI_API_KEY`.
- Chat commands require embeddings and an `OPENAI_API_KEY`.
- Prefer `book search` and synthesize answers yourself before using `book ask`.
- Summaries increase ingestion time and cost significantly; enable `--summary` only when needed.
- Use `--batch` to run embeddings and summaries via the OpenAI Batch API at 50% cost; results may take up to 24 hours. When combined with `--summary`, summaries are batched first, then embeddings on resume.
- After `--batch` ingestion, use `mycroft book ingest status <id>` to check progress and `mycroft book ingest resume <id>` to complete indexing.
- If a non-batch ingest is interrupted, use `mycroft book ingest resume <id>` to continue from the last saved chunk.
- If a batch fails, `resume` automatically re-submits it.
- For scripted runs, avoid interactive flags like `--manual` or omit confirmations with `--force`.

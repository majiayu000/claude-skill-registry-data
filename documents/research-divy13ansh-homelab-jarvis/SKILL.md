---
name: research
description: Deep research with multi-source verification and structured report delivery
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    requires:
      bins: []
      config: ["browser.enabled"]
---

# Research

When user asks to research any topic and optionally produce/deliver a document:

1. **Plan** — Clarify scope, output format (md/pdf/docx), delivery channel (Discord/Telegram/WhatsApp). If ambiguous, ask once then proceed.
2. **Search** — Use `web_search` with 2–3 distinct queries. Prefer primary sources (official docs, papers, repo README) over secondary (blogs, summaries).
3. **Fetch** — `web_fetch` 4–6 top hits; use `browser` if JS-rendered or blocked. Cross-check claims across ≥2 independent sources.
4. **Synthesize** — Structure:
   - Title, date, question
   - Executive summary (3–5 bullets)
   - Findings (sectioned, with inline citations like `[1]`)
   - Comparison table if alternatives
   - Risks / open questions
   - Sources (numbered list with URLs, accessed date)
5. **Verify** — Flag unverified claims ("per README, not verified by running"). Distinguish fact vs opinion. If sources conflict, note conflict.
6. **Generate** — Write markdown to `/data/documents/research/YYYY-MM-DD-<slug>.md`. If pdf/docx requested, call `python3 /app/scripts/create_document.py --input <md> --format <pdf|docx>`.
7. **Deliver** — Use OpenClaw `message` tool to send to user's active session channel; do not re-implement channel clients. Attach file path or inline summary as appropriate.
8. **Report** — Tell user what was done, sources count, and delivery location/channel.

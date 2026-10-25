---
name: ami-research-context
description: Investigates external context, forces the AI to search for up-to-date documentation, and saves findings to external-references to prevent context loss.
allowed-tools: Bash, Read, Grep, WebSearch, WebFetch, Write
---

# Skill: Context Researcher

When this skill is invoked, you must act as a dedicated technical researcher. Your goal is to gather, verify, and persist critical external context (documentation, API changes, framework rules) so that the AI assistant does not rely on outdated pre-trained memory or hallucinate technical details across sessions.

## Workflow

1. **Understand the Gap & Deduplication Check:**
   - Check if a research file already exists under `docs/external-references/<topic-slug>.md` or in the active session context. If it already contains recent, comprehensive findings, read and extend it incrementally instead of starting duplicate searches from scratch.
   - Check if the user has already provided a link to the documentation or the topic they want to research. If not, ask the user for the topic and if they have a link to share.
   - Make sure you understand the user's need and what information they are looking for. If you don't understand, ask for clarification. Don't start the research until you understand the user's need.
   - If the user provides a link to explain what they want to research, **ALWAYS** inspect the URL content with the available URL reading tool and don't rely solely on the URL text. If you can't read the URL content, explain it to the user and ask them to paste the raw content directly into the chat. 

2. **Research via Tools:**
   - Actively use your web search or URL reading tools to fetch live documentation.
   - **CRITICAL FALLBACK:** If you encounter permission errors, CAPTCHAs, or cannot access a specific URL, you MUST notify the user immediately. Ask them to take screenshots of the page or paste the raw content directly into the chat. Do NOT guess or hallucinate the content if the URL fails.
   - Check if the documentation is outdated. If yes, you MUST search for the newer documentation and repeat the reading process. Do not stop until you find the correct and up-to-date documentation.
   - Check if the documentation is too generic or high-level. If yes, you MUST ask the user for more specific details or keywords to refine the search.
   - If finding the correct and updated documentation is ultimately impossible, let the user know exactly what you found and what you couldn't find. Explain the problem clearly.

3. **Synthesize Findings:**
   - Extract the most relevant APIs, constraints, schemas, configuration patterns, and best practices.
   - Ignore marketing fluff; focus purely on developer requirements.

4. **Persist Knowledge (external-references):**
   - Save the synthesized research to the repository's long-term memory under `docs/external-references/<topic-slug>.md`.
   - If the `docs/external-references/` directory doesn't exist, create it.
   - If a document for this topic already exists, **update** it rather than overwriting it entirely.

5. **Document Formatting:**
   - The saved markdown document MUST include a metadata header at the very top indicating when it was created and last updated:
     ```markdown
     > **Created:** YYYY-MM-DD
     > **Last Updated:** YYYY-MM-DD
     ```
   - Organize the rest of the document with clear headings, code blocks, and direct links to the source URLs.

6. **Report:**
   - Output the full path of the saved file to the user.
   - Briefly summarize the 2-3 most important technical takeaways discovered.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).

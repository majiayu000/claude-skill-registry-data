---
name: research-workflow
description: Plan a rigorous topic-specific web investigation, compare independent evidence and create a cited research report with verified source accounting.
---

# Research workflow

This is an original app-native workflow, not a private Anthropic prompt.

Frame the user's actual question into focused subquestions. Search for primary sources, independent corroboration and competing explanations. Investigate missing evidence; distinguish facts, inference and uncertainty. Stay on topic rather than adding unrelated websites to reach a count.

Deep Search uses the application coordinator: it must successfully read at least 100 distinct final website domains before claiming completion. Search snippets, redirects to the same domain, copied content, challenge pages and failed requests do not count. Read and analyze bounded page excerpts in batches. Record queries, source URLs, retrieval time, evidence notes and limitations. Respect access challenges and provider limits.

Deep Research additionally identifies unanswered questions and conducts follow-up searches. Produce a clear report with direct findings, opposing perspectives, gaps, methodology and real citations. Cite only IDs supplied by successfully read evidence. Never fabricate website counts or URLs.

The coordinator calls configured search/fetch adapters and the selected model; it publishes a real Markdown artifact. For follow-up edits, use research_read, research_source_read and artifact_read, then artifact_update with the current version. Loading this skill alone does not run a research job or unlock browser/terminal access. If tools are disabled or unavailable, explain the reason and preserve confirmed evidence for Resume. Memory off and incognito policies still apply.

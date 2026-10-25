---
name: "verify-claims"
description: "Use when researching a topic from web pages, threads or transcripts and every claim needs an exact quote checked against a saved markdown snapshot with verify.py."
---

# Verify claims against saved snapshots

Goal: no claim goes into a write-up unless its exact words exist in a page the user captured. The check is plain text search, done by `verify.py`. The human decides whether a quote supports the claim.

The user works in .md files only. Everything below is markdown.

## Files

- `snapshots/<name>.md`: a captured page, thread or transcript. Start it with front matter:

  ```
  ---
  url: <source url>
  retrieved_at: <YYYY-MM-DD>
  ---
  ```

  Never edit a snapshot after capture. Re-capture instead.
- `claims.md`: one block per claim:

  ```
  ## c1
  - claim: <the statement in your own words>
  - quote: <words copied exactly from the snapshot>
  - snapshot: <name>.md
  - found_by: <tool that led you to the page>
  - extractor: <who or what pulled the quote>
  ```

- `verify.py` (the user's script, normally in their python-research folder).

## Steps

1. Treat every lead (search result, AI answer, link) as untrusted. Only a captured snapshot counts as evidence.
2. Capture each source page as markdown (for example with Firecrawl) into `snapshots/`, adding front matter with the url and today's date.
3. For each claim, copy the quote word for word from the snapshot. Use `...` to skip words; the pieces must stay in page order. Quotes under about 25 characters are rejected.
4. Run: `python3 -I verify.py claims.md snapshots/`
5. Read the output:
   - `FAIL`: fix the source side. Correct the quote or re-capture the page. Never loosen the quote to make it pass and never edit a snapshot.
   - `REVIEW`: the same claim cites different quotes; the human compares them.
   - `WARN` (short snapshot): the capture is probably blocked or partial. Re-capture.
6. Add `- status: accepted` or `- status: rejected` to each claim after the human reads it in context.
7. Write up from accepted claims only. Counts (how many sources, how many claims) come from the script output or code, never from memory.

## Always say

A pass only means the words exist in the capture. It does not mean the claim is supported, the speaker is who they seem, or the post is not a duplicate. Paraphrase and cherry-picking are not caught. Ask the human to read each accepted quote in its surrounding paragraph.
---
name: api-verification
description: Prove a search, filter or API answer is real before relying on it, and budget web search across a fan-out. Use when querying an unfamiliar API, a filter returns suspiciously clean results, a per-item error may have been swallowed, or briefing research agents.
---

# Research and API verification

The resident rule `primitives/rules/research-and-verification.md` is provenance for the full
harness installation, not a dependency of this skill. The verification procedure and search
budget below also apply when this skill is installed standalone.

## Search budget

**Web search is capped per session and shared by every subagent in that session.** On Claude
Code the cap is 200 calls. An 18-agent fan-out briefed for 35 searches each exhausts it within
minutes; later agents run on fetch alone.

Budget accordingly: roughly 10 agents at 20 searches, or 6 at 30. For bigger runs, stagger
waves across separate sessions, or brief agents to lean on fetching known primary sources.

After a fan-out, check each subagent's search count and re-run starved, discovery-heavy
dimensions in a fresh session. Fetch-only agents are fine for licence pages and official docs,
thin for "what shipped recently" questions.

## Prove an API answer is real

- **Unknown query parameters are silently ignored by most APIs.** Prove a filter bites by
  sending a value that can never match and confirming the result is empty.
- **Spot-check one returned record** against the field you filtered on before trusting the set.
- **A swallowed per-item error is unknown, not absent.** Count the failures separately from the
  empties.
- **Re-check the live spec** before assuming a documented workaround is still needed.

## Prefer primary sources

Defer to human-written documentation over agent-generated summaries, and trace every rule you
rely on to a quotable source. When a file's header and its body disagree, neither is ground
truth: find the code or the spec that decides it.

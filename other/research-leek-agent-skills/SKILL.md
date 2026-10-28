---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file. Use when the user wants a topic researched, docs or package facts gathered, reading legwork delegated, or a wayfinder research ticket resolved.
argument-hint: "The question to research"
allowed-tools: "WebFetch WebSearch"
context: fork
agent: leek-skills:researcher
background: false
---

# Research

Answer one question from **primary sources** and leave a cited Markdown file behind.

**The question is `$ARGUMENTS`.** If that is empty, the question is the one stated in the conversation; if there is none either, stop and report that you need the question as an argument (in Claude Code this skill runs in its own subagent and cannot see the conversation).

## Where this runs

In Claude Code with the plugin installed, the body below runs in the `researcher` subagent and the answer returns to the caller when it finishes. In other harnesses, dispatch it to a sub-agent if one exists (Codex: `spawn_agent`, then `wait_agent` for the answer; read-only for source sweeps; general-purpose when it must fetch or write) or run it inline and say so. Either way the work must **finish inside this session**: a sub-agent's task handle dies at `/clear`, session end, or compaction, so never leave one running, and in everything durable (tickets, resolution comments, hand-off text) reference the findings **by file path, never by task ID**.

## The research brief

1. **Create the findings file first**, before any investigation: a single Markdown file holding the question and an empty findings list. Save it where the repo already keeps such notes; match the existing convention. If there is none, `.scratch/research/<slug>.md` is the default (an inbox that `scratch-cleanup` later files into `docs/`). A run cut off partway then still leaves its findings behind.
2. Investigate the question against **primary sources**: official docs, package source (`vendor/` for Composer, `node_modules/` for npm), specs, first-party APIs, never a secondary write-up of them. Follow every claim back to the source that owns it. In a Laravel project with Boost, prefer the `search-docs` MCP tool over web search for framework and package questions, it returns version-pinned ecosystem docs.
3. **Append to the file as you go**: after each source settles a claim, add it with its citation (a URL, a file path, or `package@version`). Never hold findings back to write in one pass at the end.
4. **Budget turns.** This run has a hard turn cap and is killed without a final message when it hits it. At about 100 turns, stop investigating whatever is left: record the open parts as unanswered in the file, then finish with steps 5 and 6.
5. End the file with a short **What this unblocks** section: the answer in one or two lines (or what stayed unanswered and why), and what it makes decidable, no pipeline banners or skill routing.
6. Report back: the answer in a few lines, the file path, and a **Next** block (below). The final message is data for the caller, who relays the answer plus the path to the user rather than re-pasting the document.

### Wayfinder integration

When resolving a `wayfinder` research ticket, follow the configured tracker's Wayfinding operations. **Claim it first** through the Claim operation so a concurrent session cannot pick it up mid-flight. Write the findings file (no branch: see the tracker's Working in parallel rules), link it through the Assets operation, then use the Resolve operation to record the answer and the file pointer and close the ticket. Research tickets are the one type a charting session may run several of in parallel, all collected before the session ends.

## Next block

End the report with the conditions that apply, most likely first (no pipeline banner: research is supporting work). The caller routes on them:

- **Answered, and a decision was waiting on it** → `/grill-me` on that decision, naming it
- **Answered a `wayfinder` ticket** → `/wayfinder <map>` for the next frontier ticket
- **Answered, and it changes a published spec** → `/to-spec` to revise, naming which section is now wrong
- **Unanswerable from primary sources** → say so plainly; `/to-questionnaire` if a person holds the answer
- **Answered, but surfaced a new unknown** → `/research` on the new question, stated as a question

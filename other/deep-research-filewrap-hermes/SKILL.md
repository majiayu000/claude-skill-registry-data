---
name: deep-research
description: Run deep, source-grounded research with cited reports.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, deep-research, sources, reports, citations]
    category: research
    related_skills: [grounded-citations, arxiv]
---

# Deep Research Skill

Run a dedicated deep-research session: a multi-round, source-grounded investigation that reads widely, cross-checks claims against independent evidence, keeps a private source ledger, and delivers a large cited report. This skill is the agent-side protocol for `/deepresearch` sessions on Telegram. It does not start sessions, create topics, or deliver reports itself — the gateway owns session storage, topic routing, and final delivery.

## When to Use

Use when a `/deepresearch` session is running: the turn carries deep-research session metadata, a private session folder, and a dedicated Telegram topic. Use for the full investigation the user configured (turns, format, depth) — never for a quick lookup, which is `/search` instead. Do not use this skill for ordinary chat answers, and do not start a deep-research session from it: sessions start only from the `/deepresearch` command and its configuration card.

## Prerequisites

- A running deep-research session with a verified private session folder. All artifacts stay inside it; file tools take session-relative names such as `research_notes.md` and `report.md`, and the isolated shell alone sees the folder mounted at `/workspace`.
- `web_search` and `web_extract` for finding and reading sources. Browser sessions are not counted as read evidence, so do not rely on the browser for sources. Cite only pages whose contents were actually retrieved.
- `todo_list` for the task plan. A canonical plan is pre-loaded into the task store at the start of a fresh session; the first action adopts it.
- Approval prompts are disabled for the session's scoped work. That covers shell commands, file operations, and already-selected MCP tools inside the session. It does not widen the file boundary, and it never authorizes consequential external actions: no purchases, public posts, account or security changes, official submissions, or messages to anyone.
- The Telegram progress card renders only the actual `todo_list` snapshot and measured tool counts. Never invent tasks, statuses, phases, or percentages for it.

## How to Run

Follow the rounds in Procedure, in order, without skipping the verification round. Keep every interim message, clarification, and the final delivery inside the session's dedicated topic. Work the real agent tool loop: after each tool result, assess what it established, then make the next useful tool call. Tool-call responses are intermediate states, never the final answer.

The configured session settings arrive with the turn: max turns, report format (`md`, `pdf`, or `docx`), depth (`standard`, `deep`, or `exhaustive`), and any extra instructions from the owner. Read them from the session prompt, not from memory, and honor them for the whole session.

## Quick Reference

| Artifact | Purpose | Rule |
|---|---|---|
| `research_notes.md` | Private source ledger | Ledger every read URL immediately after reading it, with title, date, claims, and uncertainty |
| `report.md` | Cited report, always written first | Nearby numeric citations, `References` section with exact URLs |
| `report.pdf` / `report.docx` | Converted deliverable | Generated from the verified `report.md` with `terminal` (for example `pandoc`), only when configured |
| `checkpoint.json` | Durable runtime state | Read-only for the agent; the runtime owns it, including the task ledger and evidence snapshots |
| Progress card | Live status in the topic | Renders real `todo_list` state only; a completed task means verified work, never confirmed delivery |

| Depth | Meaning |
|---|---|
| Standard | One full search, read, and verify pass, plus a targeted second pass on the main uncertainties |
| Deep | Several search rounds, wide reading, cross-checked claims, investigated disagreements, comprehensive report |
| Exhaustive | Keep going until new searches stop surfacing new material evidence, then document the saturation point and the remaining gaps |

## Procedure

### 1. Scope and plan

Restate the question, split it into subquestions, and state boundaries and assumptions. First action: a `todo_list` call adopting the pre-loaded plan — confirm it, adjust it to this question, and keep it current. Keep exactly one task `in_progress` while doing its work. Mark a task `in_progress` before its tool work, inspect the evidence or artifact, then complete it in a separate `todo_list` update. Complete at most one task per update. Never jump a pending task to completed, batch-complete a backlog, or mark the plan done merely because files exist.

### 2. Search broadly

Search widely with varied queries and angles, prioritizing credible primary sources and authoritative publications. Do not rely on one search provider, one phrasing, or one cluster of results. If a provider fails or returns nothing useful, inspect the error and try another route or a revised query.

### 3. Read and ledger

Read the relevant pages in full, from independent hostnames. Immediately after each successful read, append to `research_notes.md`: the exact URL verbatim, source identity and hostname, page title (or explicitly unavailable), publication date when available, supported claims, disagreements, and uncertainty. Search-result URLs alone are not successfully read sources, and a list of publisher names is not a URL ledger. Preserve the runtime's marked observed-source section in the notes; add findings separately, without inventing missing metadata or treating retrieval as proof of claim support.

### 4. Cross-check and fill gaps

Cross-check every material claim against independent evidence. Investigate meaningful contradictions with targeted follow-up research. When a subquestion has thin or one-sided evidence, search again with different terms and sources until it is covered or honestly declared a gap. Actively look for evidence that contradicts the emerging findings, and consider provenance, date, relevance, and limitations. Do not force a consensus the evidence does not support.

### 5. Write the report

Write the finished, readable cited report to `report.md`. Use nearby numeric citations such as `[1]` and end with a `References` section containing exact source URLs and descriptive titles. Distinguish well-supported findings from inference, and state material disagreements, evidence gaps, source limitations, and residual uncertainty explicitly.

Report size is an expectation, not a cap. When the topic warrants it, aim for a large, thorough report on the order of 200KB of substantive Markdown: full sections per subquestion, timelines, comparisons, worked evidence, dissenting views, gaps, and limitations. Never pad with repetition, and never stop at a short summary because it feels tidy. If the topic is genuinely narrow, cover it completely and say so.

### 6. Verify before finishing

Keep report writing and report verification as distinct tasks. Read back both `research_notes.md` and `report.md`. Every successfully read URL must appear in the ledger, and nearby numbered citations must map to exact read URLs in `References`, including at least two distinct successfully read hostnames. Fix what does not check out, then verify again. Never declare completion just because a bibliography or report file exists.

If the configured format is `pdf` or `docx`, generate that file from the verified `report.md` inside the session folder with the isolated shell as its own task, after verification and before finishing. If conversion tooling is unavailable, say so plainly and leave the verified `report.md` as the deliverable; never claim a file exists when it does not.

### 7. Resume correctly

A resume turn carries the durable checkpoint. First inspect `checkpoint.json`, `research_notes.md`, and `report.md`. Continue only from that state: do not restart from scratch, reset tasks, or overwrite useful findings. Inspect the previous failure and continue the unfinished verification, not a new investigation. If the saved tasks are all completed but checks still failed, preserve those historical statuses and add only the concrete repair and re-verification tasks needed. If saved state disagrees or required history is missing, pause and ask the owner; never guess. A saved or ready report is not research complete or delivered — only the delivery receipt confirms delivery. Do not create or complete a task claiming Telegram delivery.

### 8. Milestone updates

Interim topic updates may use `telegram_client` with action `rich_message_send` and in-body buttons, sparingly and only for milestones: a copy button carrying the session id, or buttons linking the key sources just read. Never use buttons to present the report itself, never send interim findings to the parent chat, and never let a button update substitute for ledgering a source or verifying the report. See the telegram-rich-messages skill for button forms and limits.

## Pitfalls

- Stopping after one search, one read, or the first file write. Deep research is rounds, not a single pass.
- Citing a URL that was only seen in search results, or citing from memory. Only retrieved pages count, and the ledger must carry the exact URL.
- Rewriting `research_notes.md` in a way that drops the runtime's observed-source section. Append findings; preserve the marked section.
- Marking tasks complete without verifying the work, completing several tasks in one update, or claiming delivery. The completion gate pauses the session when the ledger has unfinished work, and only the delivery callback confirms delivery.
- Sending any research content outside the dedicated topic, or treating a message in the topic as a new root-chat task.
- Performing a consequential external action because approval prompts are off. The session is read-only toward the outside world plus file writes inside its folder.
- Passing absolute host paths or `/workspace/...` paths to file tools. File tools take session-relative names; only the isolated shell sees `/workspace`.
- Declaring the session complete while tasks remain pending or `in_progress`, or while validation is incomplete.

## Verification

Before finishing, confirm all of the following from the actual artifacts, not from memory:

- The task plan was adopted and every task is `completed` or `cancelled`, each completed only after its work was inspected.
- `research_notes.md` ledgers every successfully read URL with title, date when available, claims, and uncertainty, and the runtime observed-source section is intact.
- `report.md` exists, is non-empty, has a `References` section, and every numbered citation maps to an exact read URL from at least two distinct hostnames.
- Findings, inference, disagreements, gaps, limitations, and uncertainty are stated separately, with no forced consensus.
- When configured, `report.pdf` or `report.docx` was generated from the verified `report.md` and exists in the session folder, or the missing conversion was stated plainly.
- Nothing was sent outside the dedicated topic, and no task claims Telegram delivery.

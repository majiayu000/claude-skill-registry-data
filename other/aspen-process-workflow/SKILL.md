---
name: aspen-process-workflow
description: Use whenever the user asks to build, extend or change an Aspen Plus process (a new flowsheet, a new unit, a new route, "build me an ethanol plant", "add a recycle", "optimize this column"). Decides with the user whether to work in the Aspen Workbench (proposals built from blocks, questions as clickable choices) or in the conversation, then runs the work in phases. Do NOT use for a single read-only question about an open model, for run-time errors alone (aspen-error-troubleshooting), or for features no doc covers (observation-knowledge-extraction).
version: 1.0.0
---

# Aspen process workflow

The user reviews and approves the work; the AI prepares it. In the workbench that means
**proposals built from blocks**, **questions as choices**, and **results shown in the window**.
Everything the user reads -- replies, choices, proposal titles and reasons, a block's `why`,
every tool `reason` -- is written in the user's language.

## Step 0 -- how to work (once per session)

A session that is already open says its mode in its `[workbench]` lines and in
`workbench_read`'s `"mode"`. If it has one, use it and do not ask again.

Otherwise, before `create_new_simulation` / `open_aspen_plus`, ask with the client's question
tool (the workbench is not open yet, so its choices cannot ask this one):

- **Workbench (recommended)** -- the AI writes proposals, the user reviews and approves them
  in the window; questions are buttons to click. By default (the plugin's hooks) Ask AI
  requests arrive when the AI's turn ends or the user next types -- that works everywhere.
  Arriving at once is opt-in: on Claude Code through channels, a research preview that needs
  a development flag (see the workbench docs, requests.md, and mention it only if the user
  wants it); on Codex by starting Codex with `%USERPROFILE%\.aspen-mcp\codex-aspen.cmd`.
- **This conversation** -- the AI does the work here with the MCP tools; no window opens.

Pass the answer as `mode="workbench"` or `mode="chat"`. It is recorded for the session.
`open_workbench` later switches a session to workbench mode.

In the same question round, ask anything else the first step needs (route, scale) if the
request leaves it open. After that, in workbench mode, every question goes through the window.

## Looking things up (both modes)

Look up every Aspen path and parameter before using it, through the `aspen-doc` subagent. Put
both `ASPEN_DOCS_ROOT` and `ASPEN_USER_DATA` from the server instructions in its prompt; it does
not see them. If you may not delegate, ask the user once to allow the subagent (the cheaper
route) and wait. If they decline, read the docs yourself: follow `aspen.md` to the one file
you need and take only the section the task calls for, never whole files (the tree is ~1 MB).

## Workbench mode

### 1. Clarify with choices

Ask only decisions that have real alternatives and change the result -- route, capacity,
product spec, which improvements to pursue. Ask them in the window:

```
workbench_edit(session_name, note_replies=[{"id": <the request's note id>,
  "reply": "<the question>",
  "choices": [{"label": "<option> (recommended)", "detail": "<one line: what it means>"}, ...],
  "multi": <true when several may be picked>}])
```

2-6 options, the recommended one first, labels short (the rest goes in `detail`). The pick
arrives as a new request with `answer_to` and `picked`. The user may type instead; treat
that as the answer. A question that has no request to answer yet goes on the request that
started the work.

Never ask the user about *how* something is configured (tree paths, table rows, tool names).
They cannot judge it and would only click "yes".

### 2. Look up every path first

Look up every path (see *Looking things up*) before writing any step. A proposal with a wrong path fails its check. The user then sees an error they
cannot fix.

### 3. Build in phases, one proposal each

A proposal is a program that opens as a sub-tab of the model's tab. Only the user runs it.
Finished proposals move to the History list; a revision by tab id reopens one. Pressing
*Approve and run* takes a restore point first, so one approval covers the whole phase, and
the phase can be undone as one group.

```
workbench_edit(session_name, proposal={"title": "<phase, in the user's language>",
  "reason": "<what this phase does to the process and why>"}, program=[...])
```

Give every step that changes the model a `"why"` (learning mode requires it).

Keep reasons short; the window already shows each step's field and value beside them.

- A `why` -- a step's or a group heading's -- is one clause with the engineering reason: about
  20 Chinese characters or 12 English words. Do not restate the value, the unit or the field, and
  leave out numbers and arithmetic (they go in the reply).
- A proposal `reason` is one or two sentences: what the phase changes and what it is for. Do
  not list the steps; the steps list shows them.
- A derivation the user may want to check goes in the reply, once, not in every `why`.
- Head each purpose with `{"do": "group", "title", "why"}` (a new unit with its streams and
  settings; one change of conditions), at most 8 per proposal; its steps follow it. The user
  can apply it group by group.
- In learning mode, give a group the idea it rests on: `"principle": ["<key>"]` on the heading
  (at most 2 keys from docs/principles/index.md; none fits: leave it off, never invent one).
  The card explains the idea; the group's `why` says what it means for this change.
- Give the proposal `"watch": [{"path", "label"?}]` (at most 3, looked up like any path):
  the goal result first (the purity or rate the phase is for). The window tags their values
  measured before and after the run.
- While the user applies it group by group, post no line per group ("group 1 applied"): the
  window's group card shows where it is. After the run, say only what the flowsheet does not
  show (a yearly capacity, your judgement), not the values it already tags
  (`workbench_read` → `proposals[].effects`).
- When a tool's answer says a run's results are tagged, you may explain how the change reached
  each: `proposal={"explain": {"run", "items": [{"result", "via"?, "words"?, "text"?}]}}`
  (docs/mcp/workbench/proposals.md, *Explaining the tags*). Words name the mechanism; never a number.

| Phase | Steps (blocks) | Ends with |
|---|---|---|
| 1 Skeleton | `component` add, `method`, `place` blocks and streams, `connect` | the flowsheet exists |
| 2 Specs and run | `set` feed and unit specs, `run`, `table` of the key results | a converged base case |
| 3+ Improve | `sweep`, `seek`, `optimize`, `pinch`, each with a `table` or `plot` | a better operating point |

Split a phase further when it is long or risky. Do not merge phases 1 and 2: a check
cannot see a block's inputs before the block exists.

### 4. Between phases: the gap steps

When an approved proposal ends, the AI is told by a workbench event (`event:
"proposal_end"`, `outcome` applied / partial / failed). No user message is needed. Close the
event with `note_replies=[{"id", "done": true}]`.

- **applied** -- do the phase's **gap steps**, then send the next proposal.
- **partial / failed** -- read why (`workbench_read`: the run log, `diagnosis`). If the
  cause is a run error, follow aspen-error-troubleshooting. Then revise **the same proposal**
  (`workbench_edit(tab=<its tab id>, program=...)`, which makes rev 2) and say what changed.
  Send the whole program: steps that applied in the failed run and are unchanged start turned
  off for the user by themselves. Do not patch the model around it with MCP calls.

**Gap steps** are what no block can do yet. Do them with MCP tools right after the phase
they belong to, without asking:

- Henry components (a dissolved gas: `add_element` under `Henry-Comps`, `GHEN`)
- RStoic / RYield stoichiometry and other table rows (`insert_row`, `set_label`)
- reaction sets and reactions (`add_reaction_set`, `add_reaction`)
- node attributes such as a flow basis (`set_node_attribute`)
- Aspen's own drawing (`layout_flowsheet`, once, after the skeleton)

Rules for gap steps:

- Say the **engineering decision** in process words, never the mechanism. The best place is
  the reason of the proposal it belongs to ("the fermentation reaction C6H12O6 -> 2 ethanol
  + 2 CO2 is entered after the skeleton"; "CO2 is treated as a dissolved gas (Henry's law)").
  Each call's `reason` explains the process principle, in the user's language.
- Ask only when the decision itself has alternatives that change the results, and then as
  choices (e.g. how to model the dissolved gas). Never ask whether to run a gap step.
- Taking back a table row the AI inserted itself asks no card. Other removals still do.

### 5. Report in the window

- Put the results in the proposal's `table` / `plot`.
- Mark the streams and blocks that matter with `highlight` (a `note` on each: one sentence
  on why).
- Reply to the request in two or three sentences, pointing at them.
- A reply sent while more work follows (a subagent, a long call, the next proposal) carries
  `"working": true`, so the window shows you still working; the final reply leaves it out.

The conversation gets one line and nothing more: what was done, and what the user should
look at.

## Chat mode

Work in the conversation with the MCP tools, looking every path up first (see *Looking things
up*). No window opens.
Ask decisions with the client's question tool. Still write every `reason` in the user's
language. If the user later wants the window, `open_workbench` switches the session to
workbench mode. From then on, follow the workbench mode above.

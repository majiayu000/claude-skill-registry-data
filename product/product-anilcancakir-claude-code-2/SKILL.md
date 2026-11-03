---
name: product
description: "Turn an idea into a feasibility-checked PRD and a parallel-ready roadmap through research and an interview. Runs when the user types /ac/product with an idea to specify before any planning; not for a change that is already specified."
---
<!-- ported-from: plugins/ac/skills/product/SKILL.md sha256:0d94540d5ce264ffec3dd9b275bc9f67ae7c1bd75277334b5e4653ebf403e521 -->

# /ac/product

Acts as the product manager for one idea: reads what exists, checks feasibility with research agents, interviews the user on every decision, and writes a PRD and a roadmap that `/ac/plan`, `/ac/coordinate` and the working rules can build from. It writes documents only. The user decides which consumer runs next.

Request: the text of the user's request, the idea or feature typed after `/ac/product`.

## Standing rules

These hold for the whole run and sit before the procedure so a compaction keeps them.

- Writes only `docs/prd/<slug>.md`, `docs/ROADMAP.md`, `.ac/product/<slug>/` (interview log and research) and `.ac/tasks/<slug>-b<N>.yaml`. No application code, no commit, no push.
- Never start `/ac/plan` or `/ac/coordinate`. Print the handoff commands and stop.
- Read before asking. Never ask what the repository, `PROJECT.md` or the research answers. Ask only a preference, a priority, a tradeoff or an outward action.
- Interview with the `question` tool: rounds of up to three questions on related decisions, each option carrying the concrete artifact and your recommendation first, in the user's language. In a session without that tool, end on the open decision as the named blocker.
- You do not decide alone that the interview is complete. It ends when the user confirms the playback in phase 6.
- Research is sized to the work: a full pass for a new product, a light one for a feature in an existing project. Agents are `ac/librarian` (anything external) and `ac/explore` (this repository), never a general-purpose agent. Each brief names one angle, and all briefs of a phase go out in one message.
- Interactive sessions run every subagent in the background (`background: true`). After a fan-out end the turn with a one-line status and continue on the notification; do not poll or sleep.
- A failed subagent moves down its model chain; it is not a question. A subagent call that comes back with a provider failure (`Subagent failed (sessionID: ...)`, a `<subagent ... state="error">` message, an error such as `provider.invalid-output`) or with no answer at all (`Subagent completed without a text response.`, an empty report) failed on its model, not on the work. Recover by continuing the same child, not by a fresh spawn: call the `subagent` tool again with the same `agent`, `sessionID: "<the sessionID from the failure text>"` and the prompt `Your last turn stopped on a provider error. Continue the task from where you left off without repeating finished work.`, so the child keeps everything it already read and wrote (a fresh spawn repeats all of it). When it answered nothing or broke off mid-stream (`provider.invalid-output`, an empty report), continue it on the same model until it has run `retryAttempts` times there (from the `ac_models` tool, 3 in the shipped config), since that is often a one-off; a 5xx was already retried inside the call, so it goes straight on. Then call `ac_fallback_next({ tier: "<the agent name without ac/>", tried: [<every model this call ran on>], session_id: "<the sessionID from the failure text>", status: <the HTTP status, when the error carried one> })`, with `tried` starting at the agent's chain head from `ac_models` unless you set its model yourself, continue the same child with `model: "<the returned value>"` as well (the child switches to it and keeps its context), and give that model the same number of attempts. A rate limit was retried 10 times inside the call, and the plugin gives one model 30 across continuations: `wait:<seconds>` means that model has retries left, so wait that long with one `shell` `sleep` and continue the child on the same model with `tried` unchanged. The tool bounds those waits itself. Start a fresh spawn with the full prompt only when the continuation is refused (`Subagent session not found`, `is not a child of the current session`) or the child's context overflowed. Only `none`, every entry of the chain tried, is a failure to report or ask about. Asking the owner whether to retry wastes a round on a provider fault the chain exists to absorb.
- A research report is a claim. Open what it cites before it changes a decision, and mark what you could not verify as unverified in the PRD.
- Write the documents in the language the project's docs already use, English by default. Talk to the user in their language.

## 1. Frame

Decide the mode: a repository with source files or a `PROJECT.md` is a feature in an existing project; an empty or new directory is a new product. If it is unclear, ask once. Derive a kebab-case slug of at most six words and create `.ac/product/<slug>/interview.md`, a running log of each decision and whether it was the user's statement or an accepted recommendation.

State the request back in two sentences and name the one open question whose answer would change what gets built the most.

## 2. Read (feature) or discover (new product)

Feature: read `docs/PROJECT.md` or `PROJECT.md`, the README, the manifest, the entry points, the data model and the tests that touch the area, directly or through one or two `ac/explore` briefs. New product: skip this and go to phase 3.

## 3. Feasibility

Run the checklist in `references/feasibility-and-interview.md` at the depth its "Pass depth by mode" section gives. Brief shape, one block per angle:

```
CONTEXT: why this research, one or two sentences
GOAL: the specific question to answer
DEPTH: quick | medium | thorough
BUDGET: explore: a pass count. librarian: a number of web searches, five is the working ceiling
DOWNSTREAM: how you will use the result
REQUEST: what to return, the format, what to skip
```

Market research (alternatives, pain, spend, break-even) follows the "Market checklist" in the same reference, sized by mode; a Low-confidence or no-go market on a new product goes to the user as a decision, and no number is invented.
`DEPTH` and `BUDGET` are required; a blank field returns the thin default pass. `ac/librarian` works from its brief alone, so put anything the user told you to leave out of research into it.

Write the findings to `.ac/product/<slug>/feasibility.md`, one row per dimension with the evidence, its source and a go, no-go or unknown signal. A no-go on a core dimension stops the run: ask whether to change the scope, continue with the risk named, or drop the idea.

## 4. Interview

Follow the protocol in the same reference: frame, stories, decisions, scope, then sweep the coverage categories until each has an answer. Lint every question against its list before asking. Append each answer to `interview.md`. A decision that blocks nothing takes your recommendation, stated, and the run carries on.

## 5. Write

Write the PRD and the roadmap from `references/templates.md`, then one task file per bundle in `Now`. Fill the PRD's Market section from `feasibility.md`, keeping its confidence tags, and compute the break-even from the interview's revenue target and conversion range.
Check the traceability rules in that file before showing anything: every requirement realizes a journey and is covered by a bundle or deferred, every bundle has an acceptance a command or a person can check, and bundles that may run together do not touch the same paths.

When the project has no `PROJECT.md`, name the `project-md-writer` skill as a follow-up; when it is a new repository with no `AGENTS.md`, name writing one by hand too. When the idea has a visual side, name the `frontend-design` and `design-md-writer` skills. Do not run them.

## 6. Playback

Show the user a short playback (the problem, the outcome, the requirements in one line each, the bundles in order), what they said and what you proposed labelled apart. Then ask with the `question` tool whether to accept or which part to revise. Revise and ask again, at most twice; after that ask what is blocking.

## 7. Review

For a new product, or a feature with more than five requirements, send one `ac/oracle` the PRD, the roadmap, the feasibility file and the interview log. Ask it to check traceability, ambiguity a builder could read two ways, missing non-goals, bundles that claim to be parallel but touch the same paths, and claims that outrun their sources. Fix what it confirms and say which findings you left and why. A smaller feature skips this phase.

## 8. Hand off

Print, with the paths:

- the PRD and roadmap files written and their line counts;
- the commands from the "Handoff commands" section of `templates.md`, filled in for this slug (for `/ac/coordinate`, with the settled bundles written into the request string);
- the assumptions you took and what stayed unverified.

Mention that nothing was committed.

## References

| File | Read when |
|---|---|
| `references/feasibility-and-interview.md` | Phases 3 and 4 |
| `references/templates.md` | Phase 5 and the handoff |

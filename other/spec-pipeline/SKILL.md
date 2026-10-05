---
name: spec-pipeline
description: Runs a full requirement-to-implementation pipeline by chaining superpowers:brainstorming, grill-me (superpowers:grilling), superpowers:writing-plans, and superpowers:executing-plans as four independent subagents, handing off only the produced document between phases. Use this whenever the user wants to take a rough feature idea or requirement all the way through design, stress-testing, planning, and implementation in one go — phrases like "요구사항 하나 줄 테니 브레인스토밍부터 실행까지 쭉 돌려줘", "이 아이디어 기획-검증-계획-구현까지 자동으로 진행해줘", "풀 파이프라인으로 처리해줘", or "spec pipeline 돌려줘". Don't use this for a single-phase request (e.g. "그냥 계획만 짜줘" or "브레인스토밍만 해줘") — invoke that one skill directly instead.
---

# Spec Pipeline

Chains four superpowers skills — brainstorming → grill-me → writing-plans → executing-plans —
into one pipeline, run as four separate subagents instead of one long conversation.

## Why subagents instead of one long session

Each of these four skills is thorough by design, and a single session that runs all four
back-to-back accumulates a huge amount of exploratory back-and-forth: false starts during
brainstorming, interview answers during grilling, drafting iterations during planning. If
`executing-plans` inherits all of that, it's working with a bloated, noisy context and has to
find the signal (the actual decisions) in a lot of noise.

Running each phase as its own subagent, and handing forward **only the artifact file the
phase produced**, keeps every phase working from a clean, authoritative document instead of
a conversation transcript. This mirrors why a relay race hands off a baton, not the whole
lap's memory of running it.

## Your role as orchestrator

You (the main session) do not do the brainstorming/grilling/planning/executing yourself.
Your job is to launch each phase's subagent, wait for it to finish, verify it actually
produced a file, and launch the next phase with that file as the only input. Give the user a
one-line status update between phases so they can see progress.

Phases run **strictly in sequence** — each one needs the previous phase's output to exist
before it can start, so never launch phases in parallel.

## The four phases

For each phase, spawn one `Agent` call (subagent_type left as default, since these subagents
need the full tool set — Edit/Write/Bash for the last phase, and `AskUserQuestion` +
`Skill` for all of them). Each phase's prompt must:

1. State the goal in one line.
2. Tell it explicitly to invoke the named skill via the `Skill` tool.
3. Pass forward **only the file path(s) from the previous phase** — not a summary of the
   conversation, not prior clarifying Q&A. If the subagent needs more context than the file
   contains, it should read the file and ask the user directly, not rely on you to have
   remembered anything.
4. Tell it to interact with the real user directly through `AskUserQuestion` whenever the
   underlying skill calls for user input (brainstorming's clarifying questions, grilling's
   interview, writing-plans' confirmations, executing-plans' checkpoints). These are real
   pauses for the human, not something to guess your way through.
5. End by requiring its final message to state, plainly, the exact path of the file it
   produced (and nothing it produced should be considered "done" until that file exists on
   disk — verify with `Read` before moving on, don't just trust the subagent's claim).

### Phase 1 — Brainstorming

```
Agent({
  description: "Brainstorm: <short feature name>",
  prompt: `A user wants to explore this idea/requirement:

  <the user's original requirement, verbatim>

  Invoke the superpowers:brainstorming skill via the Skill tool and run it to completion.
  Ask the real user clarifying questions directly via AskUserQuestion whenever the skill
  calls for it — do not guess or assume their intent.

  When brainstorming produces a design/requirements document, end your final message with
  the exact file path of that document and nothing else needs summarizing.`
})
```

### Phase 2 — grill-me

Only the Phase 1 document path is carried forward — nothing about how the brainstorming
conversation went.

```
Agent({
  description: "Grill: <short feature name>",
  prompt: `Read the document at <phase-1 file path>.

  Invoke the grill-me skill (superpowers:grilling) via the Skill tool and run a full
  interview against this document, interviewing the real user directly via AskUserQuestion.
  The goal is to surface weak assumptions, missing edge cases, and unresolved tradeoffs in
  the document before anyone plans an implementation from it.

  Update the document in place (or write a revised version) to reflect what the interview
  resolved. End your final message with the exact path of the resulting document.`
})
```

### Phase 3 — writing-plans

Only the Phase 2 (grilled) document path is carried forward.

```
Agent({
  description: "Plan: <short feature name>",
  prompt: `Read the document at <phase-2 file path>.

  Invoke the superpowers:writing-plans skill via the Skill tool to turn this into a written,
  step-by-step implementation plan. Confirm scope and open questions with the real user via
  AskUserQuestion if the skill calls for it.

  End your final message with the exact path of the plan document it produced.`
})
```

### Phase 4 — executing-plans

Only the Phase 3 plan document path is carried forward. This phase actually touches the
codebase (Edit/Write/Bash), so it needs the full tool set — do not restrict it.

```
Agent({
  description: "Execute: <short feature name>",
  prompt: `Read the implementation plan at <phase-3 file path>.

  Invoke the superpowers:executing-plans skill via the Skill tool to implement this plan.
  Follow its review-checkpoint structure — pause and confirm with the real user via
  AskUserQuestion at each checkpoint the skill defines, rather than pushing straight through.

  End your final message summarizing what was implemented and the state of the branch/working
  tree (files changed, tests run, anything left undone).`
})
```

## After phase 4

Report back to the user what got built and where things stand (uncommitted changes, tests
run, anything the executing-plans checkpoints flagged as open). Don't auto-commit or open a
PR unless the user asks — that's still a separate, confirmable action per this session's
normal git safety rules.

## If a phase fails or the user wants to stop mid-relay

If a subagent can't produce its artifact (e.g. brainstorming stalls on a genuinely unresolved
question), don't silently invent an answer and move to the next phase — surface the blocker
to the user and ask whether to keep going, adjust the requirement, or stop the relay here.
If the user wants to pause between phases (e.g. review the plan themselves before execution
starts), that's fine — just don't auto-launch the next phase without them saying to continue.

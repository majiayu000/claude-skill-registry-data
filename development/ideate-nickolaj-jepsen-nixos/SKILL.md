---
name: ideate
description: Generate grounded, ranked ideas for improving a repo or one area of it (features, refactors, performance, tooling), each routed to /brainstorm, /grill-me or building it.
disable-model-invocation: true
argument-hint: "[focus] [--big|--quick] [--no-web]"
---

This skill finds ideas worth doing and ranks them.

- The arguments are a focus (an area, a kind of improvement, or both) plus optional flags.
- It designs none of the ideas, and writes no code unless the user picks ideas to build at the end.
- It writes exactly one file, the ideas file (see The file), and ends with a chat summary.

## Scope

- With no focus, ask one question with the harness's question tool (pi `ask_user_question`, Claude `AskUserQuestion`): features, refactors, performance, or "Surprise me" (you go where the evidence points).
- Ask nothing else. Approach and constraints belong to brainstorm and grilling.
- Cleanup inventories (disk usage, leftovers, clutter) and topics outside code are out of scope: say so and answer directly, without this workflow.
- Classify the ask from the focus: general, features, performance, refactor, tooling/DX, or critique. The kind picks the lenses.

## The bar

- By default, any size counts, from a one-line deletion to a rewrite. An idea clears the bar if it's worth doing at all.
- With `--big`, only big swings count: rewrites, removals and new subsystems. An idea clears the bar if it's worth reorganising a week around.
- With `--quick`, only S-sized changes and deletions count.
- `--no-web` skips the web generator.

## Privacy

- Transcripts, pi sessions and shell history are private. Never write their text to the ideas file; paraphrase the friction.
- Never quote a secret, and quote a phrase rather than a passage.
- Search queries never carry text from transcripts or shell history.
- Every subagent brief repeats these rules.

## The file

- The ideas file is `ideas/<focus slug>.md` in the project's agent notes, or `ideas/<project>.md` with no focus.
- The user's instructions say where agent notes live and what a project is. Without them, the notes are `.agents/notes/` in the repo and the project is the repo; write a `.gitignore` containing `*` there first.
- Apart from that `.gitignore`, the ideas file is the only file a run writes. The grounding summary, the briefs and the generators' and verifier's results stay in context, and subagents write no files.
- Never commit it.
- If it already exists, this is a rerun: read it first.

## Ground

- Read what the focus touches. Sweep the whole repo only with no focus or "Surprise me".
- Read inline for a narrow focus, or hand a broad sweep to a fresh subagent.
- What to read:
  - the code, docs and agent instructions in that area;
  - git history: the files that change most (weighted by size), files that change together, recurring `fix:` commits;
  - TODO, FIXME and HACK comments;
  - open issues (`gh issue list`), only when the focus asks about them;
  - when the subject is tooling the user runs themselves (CLIs, agent harnesses, skills, editor config): their Claude Code transcripts (`~/.claude/projects/`), pi sessions (`~/.pi/agent/sessions/`) and shell history, read-only, for friction they actually hit.
- Write a grounding summary in context: what's there, the hotspots with paths, and on a rerun the earlier ideas and rejections. Every subagent gets the same summary.

## Generate

- Print one line naming the agents you're about to start, e.g. "3 lens generators (hotspots, subtraction, leverage), 1 web generator, then 1 verifier".
- Dispatch them in parallel, each a fresh subagent (not a fork) given the grounding summary, the focus, the bar and its own brief.
- Without a subagent tool, run them one after another inline.

### Lens generators

Start three, each from a different row.

| Lens                   | Asks                                                                         |
| ---------------------- | ---------------------------------------------------------------------------- |
| Hotspots               | Where does churn meet size? What changes together? What keeps needing fixes? |
| Subtraction            | What can be deleted, merged or automated? What if this part didn't exist?    |
| Leverage               | What would make many future changes cheaper?                                 |
| Capability reuse       | What already exists here that could solve another problem?                   |
| Gap vs reference       | What does a named or comparable project do that this doesn't?                |
| Pre-mortem             | It's six months later and this got ripped out or broke. Why?                 |
| Measure-first          | What's the biggest number (time, size, cost), and what attacks it?           |
| Constraint provocation | What if load were 10×, the budget zero, or you rewrote it today?             |

Default trios by kind:

- General: hotspots, subtraction, leverage.
- Features: capability reuse, gap vs reference, leverage.
- Performance: measure-first, hotspots, subtraction.
- Refactor: hotspots, subtraction, pre-mortem.
- Tooling/DX: hotspots, subtraction, capability reuse.
- Critique: pre-mortem, subtraction, constraint provocation.

Axes the user names ("for humans and agents", "sorted by tradeoff") replace the lenses: one generator per axis, up to three.

### Web generator

- It looks at how peer projects and tools handle the focus area, and what the repo's main dependencies have shipped recently.
- Each idea cites its source URL and names where it would land in this repo.

### Every brief

- Aim for 5–6 ideas of any size the bar allows (3–4 with `--quick`). The first few are the obvious ones; keep them only if they still earn their place once the less obvious ones exist.
- Ideas are free-form, but each has a title and a basis: a `path:line` you read yourself in this run, a source URL, or an argument written out in full. No basis, no idea.
- A performance idea needs a number you measured with something cheap and read-only (time a command, size a closure, profile one run), or else the command that would measure it, marked unmeasured.
- Don't propose anything the summary lists as rejected unless its reason no longer holds.
- Return the ideas in your reply; write no files.

## Cut

- Merge and dedupe.
- Give a fresh subagent only the grounding summary, the bar and the merged list, and ask it to refute each idea:
  - is the cited line there, and does it say that;
  - does the source exist, and does it say that;
  - does the argument hold;
  - does it clear the bar.
- It returns sound, weak or refuted for each, with a reason.
- You make the final cut. Overrule a verdict only with evidence, and say so.
- Keep 5–7. If fewer than 5 survive, report the shortfall rather than lower the bar.
- When performance is the focus and nothing could be measured, "build the measurement" (a benchmark harness, a timing script) ranks first and the rest are marked unmeasured.
- For each survivor decide:
  - Size: S, M or L.
  - Next: `/brainstorm` when the approach is still open, `/grill-me` when the approach is clear but holds decisions, build when it's straightforward.
  - Needs: other survivors it depends on. Otherwise it must stand alone.
- Rank by payoff per effort.

## Write

Write the ideas file. On a rerun, edit it in place: re-check carried-over ideas against the current code and keep the rejections.

```markdown
# Ideas: <focus>

<date> · <bar> · Looked at: <areas, history window, other sources>

## Ideas

### 1. <title>

<What, in 1–3 sentences.>

- Basis: <path:line and quote, URL, or argument>
- Why: <the payoff>
- Size: S · Next: /grill-me · Needs: none
- Status: <blank, or picked and where it went>

## Rejected

- <title>: <one-line reason>
```

Then end with this chat summary, and nothing else:

```
<n> ideas, saved to <path>

1. <title> · <S|M|L> · <build|/grill-me|/brainstorm>
   <the payoff, one line>

…

- <at most 3 notes the user should hear now, such as a verifier you overruled or a surprise found while checking; the rest goes in the file>

Start with <n>: <why, and its first step, in a sentence>.
```

## Pick

The user replies by number or in free text.

- Merge, refine or question: answer, and update the ideas file when an idea's content changes.
- Build ("do 1, 3", "fix 2"):
  - If a picked idea's next step is `/brainstorm` or `/grill-me`, ask once whether to build it anyway or route it first.
  - Then build them in this session one at a time, run the repo's checks, and mark each one done in the ideas file.
- Any other pick: restate the idea as a seed (what, basis, why) and name its next command. Mark it picked in the ideas file.

---
name: authoring-adept-agents
description: 'Write a good, portable adept agent (subagent): trigger-shaped description, one job per agent, generator/evaluator separation, explicit boundaries, restricted tools. Apply when creating or editing an agent file or running `adept agent add`.'
allowed-tools: [Bash, Read, Edit, Write]
---


# Authoring a good adept agent

An agent is a single file `.adeptability/agents/<id>.md` (YAML frontmatter + a markdown body
that becomes the agent's **entire system prompt**). `adept sync` renders it into every enabled
harness that supports agents — Claude Code, OpenCode, Cursor, Copilot, and Codex — so write it
**once, well, and harness-neutral**.

## Canonical agent format

```markdown
---
id: pr-reviewer                # ^[a-z0-9](?:[a-z0-9-]{0,48}[a-z0-9])?$ — matches the filename
description: Adversarially reviews drafted changes. Use proactively before every commit.
mode: subagent                 # subagent | primary | all (OpenCode; default subagent)
tools: [Read, Grep, Bash]      # allowlist; OMITTED = inherit every tool
disallowed-tools: [Write]      # denylist (Claude Code)
model: inherit                 # verbatim pass-through; grammars differ per harness
targets: []                    # empty = every enabled harness
harness:                       # per-harness knobs (permissionMode, readonly, sandbox_mode, …)
  cursor: { readonly: true }
---
You are an adversarial reviewer. ...
```

`adept agent check <id>` runs a safety scan plus a best-practice lint over all of this — let
it catch your mistakes.

## The description is the delegation trigger — write it like one

Every harness decides *whether to hand work to your agent* from the description alone.

- State **what it does AND when to invoke it**: *"Reviews Go changes for error-handling bugs.
  Use after editing internal/ packages."*
- Auto-fire intended? Say so: *"use proactively"*, *"use immediately after …"* — Claude Code
  and Cursor document this phrasing as the delegation lever.
- One job per agent. No generic helpers; job-shaped names (`test-runner`, `pr-reviewer`).
  Near-duplicate descriptions across agents make automatic delegation unreliable.

## Separate the generator from the evaluator

An agent asked to grade its own output praises it — it sees its chain of self-persuasion, not
the result. Structure work as **maker–checker**: one agent writes, a *different* agent judges.
When writing evaluator agents (`adept agent add my-reviewer --template evaluator`):

- Default stance is doubt: **assume the work is broken until proven otherwise**. No praise.
- **Act, don't just read**: give the evaluator a way to execute (run tests, run the code) so
  its verdict comes from behavior, not from "this looks right". An evaluator with only Read
  and Grep judges appearance.
- End with a verdict contract: PASS only if every check holds, otherwise REJECT + reasons.

## Always write Boundaries

The body is the one place the harness cannot infer your intent. Structure it:

1. **Role** — one line: the specialist this agent embodies.
2. **When invoked** — numbered steps: gather context → do the work → verify.
3. **Output** — the exact artifact the caller gets back (paths, line refs, verdict).
4. **Boundaries** — explicit *do not* lines: files never to touch, actions never to take
   ("Never merge. Never delete. Anything uncertain goes back to the caller."). A
   write-capable agent without boundaries acts with confidence it has not earned.

## Restrict tools

Omitting `tools` inherits **everything** on Claude Code and Copilot. Read-only reviewers must
not carry Edit/Write; if the body promises "never modify", the tool list has to agree —
prompts alone do not enforce read-only.

## Keep it portable

- Fields that don't exist on a harness are **warn-dropped at sync**, never silently: OpenCode
  has no `tools` (use a `harness: opencode: permission:` override), Codex controls capability
  via `sandbox_mode`, Cursor via `readonly`.
- `model` passes through verbatim and the grammars differ (Claude aliases like `sonnet` vs
  OpenCode `provider/model-id`) — scope with `targets:` or set per-harness models in
  `harness:` overrides.
- Cursor also reads `.claude/agents/`; syncing agents to both harnesses shows them twice in
  Cursor. Scope with `targets:` when that bites.
- File paths mentioned in the body are lint-checked for existence — reference real files.

## Loop

```bash
adept agent add my-agent --edit              # best-practice scaffold + $EDITOR
adept agent add my-reviewer --template evaluator
adept agent check my-agent                   # safety scan + best-practice lint (exit 2 gates CI)
adept sync                                   # render to every enabled harness
adept status && adept diff                   # confirm it landed clean
```

Run `adept agent --help` for the current flags — prefer it over memory; it never drifts. Edit
canonical, `adept sync`, never hand-edit rendered files. See [[using-adept]] for the full CLI
and [[authoring-adept-skills]] for skills (permanent knowledge the agents can load).

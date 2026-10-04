---
name: model-router
description: >
  Pick the cheapest Claude tier (haiku / sonnet / opus / fable) that can do a
  task correctly, using Jev (TypeSafe System One) as a calibrated classifier.
  Toggle with /model-router on|off|status, like caveman; /model-router audit
  shows which model actually ran each part of a session; /model-router doctor
  checks every alias and model id against the installed Claude Code. When on, use before
  every Agent tool delegation, when spawning parallel workers or Workflow
  agents, and when the main session model looks mismatched to the work (Opus
  for a file search, Sonnet for a cross-cutting refactor). Runs offline with a
  keyword fallback.
---

# Model router

Jev is not an LLM. It answers typed questions about text and returns
probabilities with confidence. Here it answers three questions about a task:
which tier is the cheapest that gets it right, how much reasoning it needs,
and whether the change is cross-cutting. Code applies the policy; Jev never
picks a model directly.

## Toggle

```
/model-router on       # or a prompt that is exactly "enable the router"
/model-router off      # or a prompt that is exactly "stop the router"
/model-router status   # bare /model-router does the same
/model-router audit    # which model actually produced what, from transcripts
/model-router doctor   # aliases, model ids, agent definitions, Jev: all still valid
```

The plain-language forms only count when they are the whole prompt, so a
sentence that mentions a router (nginx, a packet router) never flips the
flag. Harness-relayed text (task notifications, agent messages) is ignored
before any toggle check.

Invoked with `on`, `off`, `status` or nothing: run
`python3 ~/.claude/skills/model-router/scripts/router_state.py $ARGUMENTS`
and report the printed status in one line. The `UserPromptSubmit` hook
already flipped the flag before this skill ran, so the call is idempotent;
it exists so the confirmation reflects disk state, not memory.

Invoked with `audit`: run
`/usr/bin/python3 ~/.claude/skills/model-router/scripts/audit.py` and show
the output verbatim. Pass a session id or `--all` through when given.

Invoked with `doctor`: run
`/usr/bin/python3 ~/.claude/skills/model-router/scripts/doctor.py` and show
the output verbatim. On FAIL, explain each line and propose the fix; do not
edit the registry without the user's go-ahead.

## Models and versions

`scripts/models.py` is the only place tiers are defined. Each tier is the
alias the Agent tool accepts plus the exact id it resolves to:

| Alias | Resolves to (verified 2026-09-22, Claude Code 2.1.280) |
| --- | --- |
| haiku | `claude-haiku-4-5-20251001` (Claude Haiku 4.5) |
| sonnet | `claude-sonnet-5` (Claude Sonnet 5) |
| opus | `claude-opus-5-5` (Claude Opus 5.5) |
| fable | `claude-fable-5-1` (Claude Fable 5.1) |

The hook always writes the alias, never the id: the Agent tool validates
`model` against a fixed enum (`haiku`, `sonnet`, `opus`, `fable`) and turns
an invalid value into a deny. The id is what Jev's criteria, the grey lines
and the injected context name, and what transcripts must show.

Keeping it current needs no hand edits for new versions:

- **New version of an existing family** (opus 5.5 -> 6): subagents started
  with `opus` begin answering as the new id. Claude Code records the
  requested alias in `subagents/agent-*.meta.json` and the answering model in
  the log; `scripts/learn.py` pairs them at every SessionStart and stores the
  result in `~/.claude/state/model-router/resolved.json`. The grey line
  reports `[ROUTER] opus now resolves to claude-opus-6 (was claude-opus-5-5)`.
- **What can move a mapping.** Aliases resolve per Claude Code build (`opus`
  was `claude-opus-5` on 2.1.278 and `claude-opus-5-5` on 2.1.280), and an
  old build left running in another terminal keeps answering with the old id.
  So only answers from the newest build seen count, the alias moves only
  after 3 consecutive agreeing runs, never to an older id, and never to
  another family. Anything held back is listed by `learn.py` and doctor as
  `held: ...`. The result is replayed from the seed, so a rebuild
  (`learn.py --full`) always lands on the same answer as incremental runs.
- **Precedence:** Claude Code's `ANTHROPIC_DEFAULT_<TIER>_MODEL` env
  override, then the learned id, then the seed in `models.py`.
- **Claude Code update:** SessionStart says `Claude Code X not yet checked:
  run /model-router doctor` until a clean doctor run records the version.
- **New alias or removed alias** (a new family in the Agent enum): doctor
  reports it. Adding a tier is a human decision, because its cost position
  and its Jev criteria are policy: add a `Tier` to `REGISTRY` in cost order
  and a matching entry under `QUESTIONS["tier"]["criteria"]` in `route.py`.
- **Drift:** `/model-router audit` marks any subagent whose alias ran on a
  different id than expected with `DRIFT`.

## How to know it is working

Four layers, from weakest to strongest evidence:

1. **`[ROUTER] <tier> (...)` line under each prompt.** Emitted by the
   `UserPromptSubmit` hook as a `systemMessage`. Proves the routing decision
   for the prompt. Absent when the router is off or the prompt was skipped
   (slash command, under four words, harness-relayed text).
2. **`[ROUTER] <tier> -> <delegation>` line at each Agent call.** Emitted by
   the `PreToolUse` hook. `-> ... (jev <tier>, conf ...)` means the hook set
   the tier, with `floor X from definition` when the agent's own `model:`
   lifted it; `agrees` means the caller passed the same tier; `suggested ...,
   kept X` means an explicit tier was left alone; `offline (...)` means Jev
   did not answer and the call was left untouched. This is the line to watch during a long turn: it
   fires whenever a subagent is about to start, regardless of what the
   session model was reasoning about.
3. **`models:` trailer on each reply.** Self-reported by the session model.
4. **`/model-router audit`.** Reads `message.model` from the session
   transcript and every `subagents/agent-*.jsonl` under it. Written by
   Claude Code per API response, so it is ground truth.

What the router cannot do: the reply you read, and every reasoning step in
between, is always the session model in the status bar. No hook fires per
reasoning step and nothing can switch the session model mid-turn. Routing
changes the model behind delegations, and that is where the expensive or
cheap work is moved to. A prompt routed `haiku` still gets its final answer
from the session model; the haiku part is the lookups it delegated. Between prompts,
if no `[ROUTER] ... ->` line appears, no subagent was started and the whole
turn ran on the session model.

## The session model is a constant; Jev moves the work

The user never switches models by hand. `settings.json` sets `model`
(`opus[1m]`), every session starts there, and the router places work
relative to it. Never suggest `/model`.

The `SessionStart` hook records the session model under
`~/.claude/state/model-router/<session>.model` (falling back to the
`settings.json` default when Claude Code omits it). The prompt hook compares
the routed tier with it and issues one of three placements, shown in the
grey line and spelled out in the injected context:

| Routed vs session | Grey line | What the session model does |
| --- | --- | --- |
| above | `escalating: session opus, work goes to a fable agent` | hands the substantive work to one Agent with a complete prompt; the `PreToolUse` hook stamps it `fable`. Scopes, verifies, reports. Does not do the hard reasoning itself |
| below | `session opus; mechanical parts go to haiku agents` | reasons itself; lookups, sweeps and clearly specified edits go to Agents, stamped `haiku` or `sonnet` |
| same | (nothing appended) | does it itself; delegates only naturally parallel work |

Net effect: reasoning-loop cost is pinned to the session tier, expensive
tiers are spent only inside delegations Jev asked for, and cheap tiers
absorb the mechanical work. The quality ceiling for a fable-grade task is
the fable subagent, not the session model, so the delegation prompt must
carry the full task: files, constraints, invariants, what "done" means.

State is the flag file `~/.claude/.model-router-active` (present = on). It
persists across sessions until toggled. While on: the `SessionStart` hook
injects the router rules, the `UserPromptSubmit` hook routes every real
prompt and injects the verdict, and the statusline shows `[ROUTER]`.
While off: no Jev calls, no context injected; choose Agent models by
judgment.

## Run it

```bash
python3 ~/.claude/skills/model-router/scripts/route.py "<task text>" [--context "<facts>"] [--json]
```

Output, one line:

```
model-router: opus (jev sonnet conf 0.40; complexity 2.0/3; cross-cutting 0.83; ...) | cross-cutting p=0.83 >= 0.7: floor opus
```

`--context` is for facts Jev cannot see in the task text and that change the
answer: call-site counts, number of files touched, whether tests exist,
deadline or stakes. Keep it to one or two sentences.

`--json` returns the full result: `model`, `source` (`jev` or `fallback`),
`confidence`, per-tier `probabilities`, `complexity`, `cross_cutting`,
`adjustments`.

Needs `TYPESAFE_API_KEY`: read from the environment, else from the login
Keychain (generic password, service `TYPESAFE_API_KEY`) so sessions started
from an IDE or launchd, which never ran `~/.zshrc`, still reach Jev. Store or
rotate it with
`security add-generic-password -U -a "$USER" -s TYPESAFE_API_KEY -w "<key>"`.
Without a key, or offline, the script answers from a keyword heuristic and
says so (`source: fallback`, with the reason). The hooks never route down on
a fallback answer: the prompt hook lifts it to the session tier, and the
Agent hook leaves `model` unset so the agent definition or the session model
decides. When running `route.py` by hand, apply the tier table below instead
of trusting a fallback tier.

## Policy the script applies

| Signal | Rule |
| --- | --- |
| Tier choice confidence < 0.5 | take the highest tier holding p >= 0.2 (never resolve downward) |
| Complexity score >= 2.5 of 3 | floor at opus |
| Cross-cutting probability >= 0.7 | floor at opus |

Adjustments are listed in the output so the reason is visible. Thresholds
live as constants at the top of `route.py`; tune them there, not by
re-prompting.

## Apply the answer

Three surfaces control which model runs. Use them in this order.

1. **Agent tool `model` param, set by the hook.** A `PreToolUse` hook
   (matcher `Agent`) routes every delegation prompt through Jev and fills
   `model` when the call omits it. Leave `model` out and let the hook set it.
   Pass `model` only when the user named a tier; the hook keeps an explicit
   value and prints the disagreement. Each delegation is routed on its own
   prompt, not on the user's original request: a fable-level task usually
   contains several haiku-level lookups, so write delegation prompts that
   state the work plainly.
2. **Agent definitions** (`.claude/agents/*.md` in the project,
   `~/.claude/agents/*.md`, and plugin `agents/` folders for `plugin:name`)
   carry a `model:` field. A per-invocation `model` param overrides it, so
   the hook treats the definition as a floor: Jev can raise a specialist
   above its pinned tier, never below it. `inherit` or no `model:` sets no
   floor.
3. **Main session model.** A constant from `settings.json`. No hook, tool or
   suggestion changes it; see "The session model is a constant" above. Work
   above its tier is escalated into a delegation, not into a model switch.

Never route below the tier the user asked for by name, or below the tier an
agent definition pins. Routing is about not
overspending, not about second-guessing an explicit choice.

Delegation prompts are what Jev routes on and what the worker sees. A hard
task described in one vague line gets a cheap model and a shallow result.
State the files, the constraints, the invariants and what "done" means.

## Tier table (for the fallback and for sanity checks)

| Tier | Work |
| --- | --- |
| haiku | symbol or file lookup, grep/glob sweeps, read and summarize, run a command and report, rename, typo, import, version bump |
| sonnet | one-module feature or bugfix with a clear spec, unit tests for existing code, docs, small refactor in a few files, standard CRUD or component |
| opus | multi-file refactor, unknown root cause, architecture and trade-offs, security review, concurrency, migrations, profiling-driven perf |
| fable | invariants to preserve end to end, novel algorithm or data structure under tight constraints, ambiguous requirements needing research plus synthesis, high-stakes review |

Cost order is haiku < sonnet < opus < fable. A wrong answer from a cheap
model costs a second round on an expensive one, so ties go up, never down.

## Files

| File | Role |
| --- | --- |
| `scripts/route.py` | Jev call, policy, CLI |
| `scripts/router_state.py` | flag file on/off/status, toggle parsing |
| `scripts/hooks.py` | `--session`, `--prompt`, `--pretool` hook entry points; always exit 0 |
| `scripts/agent_defs.py` | `model:` floor from project, user and plugin agent definitions |
| `scripts/models.py` | tier registry: alias, seed id, env override; resolution and display names |
| `scripts/learn.py` | learns alias -> id from subagent transcripts (`--full` rescans) |
| `scripts/doctor.py` | health check: Agent enum, ids in the binary, agent definitions, env, Jev |
| `scripts/audit.py` | per-session model report from transcripts (main, Agent params, subagents) |
| `scripts/statusline-badge.sh` | `[ROUTER]` badge, called from `~/.claude/scripts/statusline.sh` |

Hooks are registered in `~/.claude/settings.json` (`SessionStart` on
startup/resume/clear/compact/fork, `UserPromptSubmit`, `PreToolUse` with
matcher `Agent|Task`, `Task` being the tool's former name). They run under
`/usr/bin/python3` so the interpreter does not change with pyenv's per-folder
version. The prompt hook skips slash commands and prompts under four words.
One Jev call usually takes under 1 s and ~300 input tokens. The whole
exchange, a 429 retry included, has a hard 4 s wall-clock budget
(`MODEL_ROUTER_TIMEOUT` overrides it), well inside the 15 s hook timeout, so
an outage or a stalled connection degrades to the keyword fallback and never
blocks a prompt.

The Agent hook answers `permissionDecision: "allow"` whenever it stamps a
tier, because `updatedInput` only applies with a decision. That skips the
permission prompt for that Agent call; deny and ask rules in settings still
win over it.

## Verify a suspicious verdict

Run the same task through `--json` and read `probabilities`. Two adjacent
tiers near 0.5 each means the task text is underspecified; add `--context`
with the missing fact (file count, call sites) rather than overriding the
tier by hand. A confident wrong answer on a clear task is a criteria bug:
fix the examples in `QUESTIONS` in `route.py`.

---
name: choosing-subagent-models
description: "Use before launching a subagent, an Agent or Task call, or an Explore agent, and on every review dispatch - code review, dual review, merge-gate reviewer. Picks the model and effort tier for the runtime you are running under."
---

# Choosing Subagent Models

## Audit, review, or question? Require a file.

**Every subagent you dispatch for an answer must WRITE ITS RESULT TO A FILE
(e.g. `/tmp/<task>.md`); its reply to you is only a summary. Put this
in the prompt.**

## Pick a TIER by role/task, then resolve it for YOUR runtime. Pin every spawn.

Model selection here is two steps, always in this order:

1. **Pick the semantic tier** by the spawned agent's role/task — one of three,
   named identically everywhere in the fleet (Go constants, role templates,
   this doc): **`mechanical`** (rote/find-replace/grep-and-collect/lint/file-maps —
   the cheapest tier), **`judgment`** (the default tier for implementers,
   reviewers, verifiers, researchers — real analysis, not busywork), and
   **`orchestration`** (orchestrator/coordinator tier — never spawned for a
   sub-agent, only ever the operator's own agent or a skill that explicitly
   names it for one step).
2. **Resolve that tier to a concrete `model:` + `effort:` for the runtime you
   are actually running under** — via that runtime's own preset
   (`RuntimePreset.TierModels`) or operator config (`runtime.role_models`);
   see "Where the tier-model mapping lives" below. Never assume Claude's
   model names (`sonnet`, `opus`, `haiku`) apply —
   a Codex or OpenCode agent reading this same file has no such models, and
   passing one either errors or silently falls back to the runtime's own
   default (see "Never let an unresolved pin fall through" below).

Every subagent you spawn MUST pass an explicit, resolved `model:` (plus effort
where the runtime supports it). Omitting it runs the subagent on YOUR model —
the single biggest avoidable cost leak in agent work.

Haiku 5.5 is eligible for summarization and mechanical work.
Read the effective model and effort at use from `runtime.role_models`.

### Read the tiers at the moment of use

**Role templates and launch examples do not name models or effort levels; this
skill and the live config do.** Read the tier when you are about to spawn or
launch, never from memory or from a copied example:

```bash
jq -r '.runtime.role_models' .thrum/config.json
```

Launching with `--role` and no `--model` resolves the role default
automatically. When pinning `--model` or `--effort`, read the effective values
from `runtime.role_models`; otherwise use the named role's built-in default or
the runtime's own preset.

### Agent tiers

Effort tier governs whether an agent does the hard thing or the expedient thing.
These are the three tiers, with Claude's built-in role defaults shown as
concrete values. **If you are running under a different runtime, resolve the
role from that runtime's preset (`RuntimePreset.TierModels`) or
`runtime.role_models`, not from the Claude defaults:**

| Role | Tier | Claude built-in default |
| ---------------------------- | ------------- | ------------------- |
| **Coordinator** | `orchestration` | **`claude-opus-5-5` / low** |
| **Orchestrator** | `orchestration` | **`claude-opus-5-5` / low** |
| **Brainstormer** | `orchestration` | **`claude-opus-5-5` / medium** |
| **Implementer** | `judgment` | **`claude-haiku-5-5` / high** |
| **Researcher** | `judgment` | **`claude-sonnet-5-5` / high** |
| **Verifier / reviewer** | `judgment` | **`claude-sonnet-5-5` / medium** |
| **Role-neutral sub-agent** (investigation, grep, mechanical) | `mechanical` | **`claude-sonnet-5-5` / low** |

- **`mechanical` tier (role-neutral sub-agents)** — investigation, grep-and-collect,
  file maps, lint runs, and mechanical tasks. Claude's built-in role-neutral
  default is Sonnet 5.5 / low. Read configured overrides from
  `runtime.role_models`; use another runtime's own `TierModels` values.
- **`judgment` tier (implementers, researchers, verifiers, reviewers)** — use the
  named-role defaults above: implementers use Haiku 5.5 / high (Sonnet 5.5 /
  medium for security-touching, epic or complicated work: auth, TLS, pairing,
  credentials, encryption, licensing, privacy, several subsystems, or over ~300
  production lines), researchers use
  Sonnet 5.5 / high, and verifiers/reviewers use Sonnet 5.5 / medium. Keep
  reviewers at medium or higher.
- **`orchestration` tier (coordinators, orchestrators, brainstormers)** — use the
  named-role defaults above: coordinators and orchestrators use Opus 5.5 / low;
  brainstormers use Opus 5.5 / medium. Operators configure orchestrator defaults.
- **`orchestration` tier is NOT your call to spawn.** Allowed only when (a) the
  operator explicitly asked for a deep review or prose review in this task, or
  (b) a skill you are running prescribes the orchestration tier for the
  specific step you are currently executing — NOT for every spawn under that
  skill. "This research is hard / important" is NOT a justification — hard
  investigation is exactly what the `judgment` tier is for.

## Worked examples — LITERAL ARGUMENTS, AND EFFORT IS TOOL-DEPENDENT

**Pin `model` on every spawn, using the value your runtime's own preset
(`RuntimePreset.TierModels`) or `runtime.role_models` resolves the tier to.**
**Pass
`effort` wherever the mechanism exposes it** — some mechanisms don't. Syntax per
mechanism — re-check the schema in front of you rather than restating from
memory, because it can change:

| Mechanism | `model` | `effort` |
|---|---|---|
| **Agent tool** | ✅ settable | ✖ **not exposed — do not pass it** |
| **Workflow `agent()`** (opts: label, phase, schema, model, effort, isolation, agentType) | ✅ settable | ✅ settable |
| **Agent DEFINITION** (`.claude/agents/*.md` / plugin `agents/*.md` frontmatter) | ✅ | ✅ — sets the default for that agent type |
| **`thrum tmux create` / `launch`** | ✅ `--model` | ✅ `--effort` — pass on BOTH |
| **Other runtimes' own spawn mechanism** | ✅ settable | runtime-dependent — check its own schema |

**Below is ONE fully concrete example — what a `judgment`-tier spawn looks
like once resolved for Claude's own Agent tool (which takes no `effort`
argument).** It is Claude-specific syntax with a Claude-specific model string;
if you are running under a different runtime, use that runtime's own spawn
mechanism and its own resolved model+effort from `RuntimePreset.TierModels` /
`runtime.role_models` instead of copying this literal string.

```python
Agent(subagent_type="general-purpose", model="sonnet",
      description="Code-quality review of <branch>",
      prompt="...")
```

**The tier philosophy still governs even where a mechanism cannot express
`effort`:** the `model` value alone still must be the tier's resolved value for
YOUR runtime — never a bare Claude name assumed universal. Where effort is not
settable, carry the intent through the agent definition, the Workflow opts, or
the tmux launch flags instead.

An agent definition can also carry a default (Claude example — resolve to
your own runtime's `mechanical`-tier value if you are not Claude):

```yaml
# claude-plugin/agents/message-listener.md (non-tmux fallback only)
name: message-listener
model: sonnet
effort: low
```

**Workflow `agent()` — effort IS a literal argument. Pass it, resolved for
your runtime's tier:**

```javascript
agent(prompt, { model, effort })   // `model`/`effort` = your runtime's resolution
                                    // of the `judgment` tier (reviewer/implementer)
                                    // or the `mechanical` tier (sub-agent) —
                                    // resolve via RuntimePreset.TierModels /
                                    // runtime.role_models for the literal values
```

**THE DIRECTIVE, imperative and not a comment: REVIEWERS RUN THE `judgment`
TIER, WHICH IS MEDIUM EFFORT ON EVERY RUNTIME THAT HAS AN EFFORT KNOB.** Pass
the resolved effort literally under Workflow, in the agent definition, or on
`thrum tmux create`/`launch` (the Agent tool takes no `effort`, so `model`
alone must still be the `judgment`-tier value there). Never dispatch a
reviewer "from memory", and never dispatch one at the mechanical tier.

**AND VERIFY, DO NOT ASSERT:** any claim about what a tool does or does not expose
must be checked against the schema in front of you.

Never select the `orchestration` tier on your own judgment — use the
`judgment` tier's configured value from `runtime.role_models`.

## Where the tier-model mapping lives

**Do not copy a tier's model string from this doc — read it at the moment of
use.** The three semantic tiers (`mechanical` / `judgment` / `orchestration`)
are the same across every runtime; only the concrete model+effort differs per
runtime, and that mapping lives in exactly two places:

- **The runtime's own preset** (the `TierModels` field of the runtime preset
  schema) — the machine-checked, per-runtime tier→model
  table. A runtime with no entry for a tier has no fleet-configured value for
  it and resolves to nothing rather than inheriting another runtime's model.
- **`runtime.role_models` in `.thrum/config.json`** — operator configuration
  for this project, which always outranks the preset's tier table.

**If you are running under Claude**, use the role-specific model and effort
defaults in the Agent tiers table unless `runtime.role_models` overrides them.
Researchers, implementers, verifiers, and reviewers use `judgment`; role-neutral
children use `mechanical`. A brainstormer's children use `mechanical` unless
they are reviewers, which use `judgment`.

**If you are running under a different runtime, read your own tier's value
from the two sources above** — never assume Claude's model names apply, and
never hard-code a model string you saw once in a doc or a prior session.

A runtime/role pair with no fleet-configured tier value has no override —
resolve it to that runtime's own configured default, and pass it explicitly
(never leave it unset — see "Never let an unresolved pin fall through"
below).

## Pin every spawn explicitly — the floor depends on the ROLE, not the depth

Every orchestrator MUST pass an explicit `model:` on EVERY subagent it spawns,
resolved for its own runtime, and `effort` wherever the mechanism exposes it.
An unspecified subagent SILENTLY INHERITS THE PARENT'S MODEL — so an
orchestration-tier orchestrator that forgets the pin just spent its
(expensive) tier's tokens on a grep.

**The floor is set by what the agent DOES, not by how deep it sits** — see the
Agent tiers table above. This applies recursively: an implementer spawning its
own helpers pins them by THEIR role, not by copying its own tier down.

The check before every spawn: what is this agent's role? Implementer,
researcher, verifier, or reviewer uses `judgment`; role-neutral investigation
or mechanical work uses `mechanical`. Resolve its model and effort from the
named-role defaults and runtime configuration. Never leave them unspecified.

### Never let an unresolved pin fall through

**An unsupported or unrecognized model name must never block delegation, and
must never cause silent inheritance of the parent's model.** If your
runtime's preset has no `TierModels` entry for this tier, or a resolved name
is rejected by the runtime you're spawning under, do NOT skip the pin and do
NOT let the spawn go unpinned so it falls back to inheriting the caller's
model — fall back explicitly to the runtime's own configured default for the
matching tier and pass THAT, so every spawn is always pinned to some resolved
model+effort. An unset `model:` is a bug at every layer of this stack, not
just under Claude.

## Paste the constraint block into the child prompt — the pin is not enough

**A model pin is an ARGUMENT and travels by itself. A behavioural constraint is
PROSE and reaches the child only if you paste it.** Constrain every level: a rule
that stops at depth 1 is absent where the work happens.

**Paste verbatim, including the last line:**

```text
=== CONSTRAINTS — apply to you and anything YOU dispatch (including this line) ===
- Work SYNCHRONOUSLY. Tests in the FOREGROUND with a bounded `-timeout`.
- NO POLL LOOPS. Never `until <check>; do sleep N; done`, never
  `while kill -0 $(cat pid)`, never `$( )` in a loop condition — even when a
  tool's own guidance suggests it. It trips a permission modal, and A FROZEN
  PANE EMITS NOTHING, so nobody can tell you are blocked. If you must background
  work, wait for the completion notification.
- Every sub-agent YOU spawn gets an explicit `model:`, resolved for your
  runtime's tier — `mechanical` (rote/find-replace) or `judgment` (real
  analysis). Read the effective model and effort from `runtime.role_models` at
  use. The `orchestration` tier is never yours to spawn.
- READ-ONLY git outside your own worktree. NEVER `checkout`/`reset`/`restore`/
  `stash`/`clean` in ANY directory — `stash` is one shared stack across all
  worktrees and the shared tree holds live agents' uncommitted state.
- Pair every zero/empty result with a control that MUST return non-zero.
```

⚠️ Never let a child take **"don't ask again"** on a modal — it removes the only
signal this condition produces.

### Cheap subagents → fan out, don't pile up

Because Haiku 5.5 supports summarization and mechanical sub-agent work, prefer
MANY small parallel subagents over one agent handed a pile of tasks. Read the
effective model and effort from `runtime.role_models` at dispatch. When research or
investigation has independent parts, partition them in parallel (use the
`efficient-multi-agent-research` skill) — smaller scopes are cheaper, run
concurrently (faster), and keep each subagent's context tight. One subagent
given ten tasks is the anti-pattern.

## ⚠️ The pin-verification command LIES — do not trust it

**This section's examples are Claude-specific** (`thrum tmux capture`'s footer
format, and the historical Sonnet/Opus incident it documents) because that is
where this defect was measured — but the underlying rule generalizes: verify
a pin by reading the runtime's own RESOLVED status output, never a stored
"configured" value, whichever runtime you're on.

`thrum agent runtime-config get <agent>` reports the **configured** value, not the
**resolved** one.

An implementer ran Opus 4.8 while both the launch flag (`--model sonnet`) and
`runtime-config get` confirmed sonnet — the check that exists to catch a bad pin
is itself a false green.

This is the same defect class as every other surface that reports a value it never
observed (`go test -count=0` reporting PASS while running zero tests; a health RPC
reporting green off a path that cannot fail; `make ci` swallowing a critical CVE with
a warning).

**So: after launching an agent, verify with `thrum tmux capture --format=annotated`
(or `--format=json` for scripting).** It parses the footer server-side into
NBSP-free fields — no positional-window guessing, no NBSP grep trap, and the
header states `ok`/`FAILED` explicitly instead of leaving you to infer a failure
from empty stdout:

```bash
thrum tmux capture <agent-name> --format=annotated --lines 12
# ━━━ CAPTURE ok · agent=<name> · runtime=claude · lines=35 ━━━
# <pane content, verbatim>
# ─── FOOTER (parsed, NBSP-normalized) ───
# Model: Sonnet 5 | Ctx: 478.3k | Ctx Used: 48.0%
# ━━━ END CAPTURE ━━━
```

The FOOTER block is simply omitted when no footer resolved — never an empty or
garbage line to misread. For scripting, `--format=json` gives the same data as a
typed document: `{"agent","runtime","ok","line_count","footer":{"model","ctx","ctx_used_pct"}|null,"lines":[...]["error"]}`
(`footer` is `null` when none resolved).

```bash
thrum tmux capture <agent-name> --format=json | python3 -c \
  'import json,sys; b=json.load(sys.stdin); print(b["footer"]["model"] if b["footer"] else "NO FOOTER")'
```

Still check the exit status before trusting either form — a FAILED capture exits
nonzero and the annotated header says `FAILED`, but don't discard that signal by
piping straight into something that only inspects stdout.

That is the runtime reporting its RESOLVED config, and it is the only check that has
ever produced a true negative on this defect. If it disagrees with the pin, report it —
those instances are a real bug and we want them counted.

🔴 **DO NOT substitute "ask the agent what model it is running."** That is a model
introspecting on its own identity — a categorically weaker instrument.
**A check built on self-report would be a THIRD instrument that cannot fail in
the direction we need**, replacing a false green with a confident one. **SETTLED — and the reason is
categorical, not a reliability judgement: self-report is the WRONG SHAPE for the
question.** The agent sees exactly ONE value (its resolved model, injected into its own
system prompt); "does the pin disagree with the resolution?" is a question about a
RELATION between TWO values. **It cannot report a mismatch however honest it is — the
disagreement is not representable in what it can observe.** No prompting rescues that.
Only an outside comparator holding BOTH the pin AND the resolved status line answers it.
⚠️ A self-report can look right while reading back an injected assertion, so it
inherits whatever the injection got right or wrong. **A correct answer there is
survivorship, not validation.**

**Fallback — only if `--format` is unavailable (older binary):** read the bare
exit status before stdout, then grep the raw pane by position, never by content
(the raw footer's separators are U+00A0 non-breaking spaces, so `grep "Model: "`
with a trailing space returns ZERO on a pane that plainly displays a model):

```bash
out=$(thrum tmux capture <agent-name> --lines 12); rc=$?   # bare, NOT through a pipe
[ $rc -ne 0 ] && echo "CAPTURE FAILED — this is NOT an empty pane" && exit 1
printf '%s\n' "$out" | grep -v 'tmux capture' | grep 'Model:' | tail -1
```

🔴 **PASS `--model` / `--effort` TO BOTH `tmux create` AND `tmux launch`.** They are
separate cobra commands with separate flags, and **`launch` is what resolves the model**
(`resolveLaunchSpec` runs in `HandleLaunch`, never in create). `create` persists the pin
asynchronously, so a create-only pin can lose the race and leave the CLI value empty at
launch **by construction**.

⚠️ **And any FIX here must be verified with a pin the role default would NOT produce.**
Pin an implementer to `claude-opus-5-5` / medium while its built-in default is
`claude-haiku-5-5` / high; assert both values to prove the pin landed.

## Paste blocks for child prompts

Paste these verbatim into a child prompt when the work involves the named activity.

--- SUB-AGENT HYGIENE ---
- No kill -0, Monitor or until-loop polling.
- No pgrep -f.
- Kill only by a captured PID number.
- Use rm -r, never rm -rf; a variable path uses "${d:?}".
- No 2>/dev/null on destructive commands.
- Bounded timeouts on everything.
- Remove only the worktree you created in this task, by its recorded path, never with --force.
- Never demonstrate an unguarded destructive idiom, even on a literal path.
--- END SUB-AGENT HYGIENE ---

--- TESTS ---
- To prove a selector resolves, use `go test <pkg> -list '<selector>'` plus a `-list '^TestNoSuchThingAtAll$'` negative control that must list zero tests. Never `-run '<sel>' -list '.*'`.
- `bd list -l` is --label; use `-n` for a limit.
- A timeout with 0 FAIL is neither red nor green: classify it as a bound failure, read the panic's "running tests:" line, and re-run wider.
--- END TESTS ---

--- WORKTREE TEARDOWN & SALVAGE ---
- Before any teardown, enumerate with both flags: `git -C <wt> status --porcelain --untracked-files=all --ignored -- .thrum`.
- Salvage anything found to a durable path (not /tmp), one subdirectory per worktree, filenames path-flattened.
- Never glob `.thrum/context/*.md`; salvage exact named files only, and assert no `project_state.md` landed in any salvage output.
- Verify salvage by name set first, then `cmp` each file, with a negative control proving `cmp` detects a difference.
- Kill the tmux session first (`thrum tmux kill <session>`), verify it is gone, then plain `git worktree remove`, never `--force`.
- Afterwards verify by effect: gone from `git worktree list` and from disk, and every remaining live pane's cwd still resolves (`tmux list-panes -a -F '#{pane_current_path}'`, then `git rev-parse --show-toplevel` per pane).
- Build the in-use protection set from live pane cwds, not from a name or registry list.
- Report the removal count and the registry delta separately.
--- END WORKTREE TEARDOWN & SALVAGE ---

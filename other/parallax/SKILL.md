---
name: parallax
category: simulation
tier: D
description: "Drive Parallax — a simulation runtime whose results carry how much of them was real. Point it at a context (a directory, an agent workspace, a table list), it proposes an ontology built from what is actually there, a human accepts that proposal before it can run, and only then does it roll the accepted model forward under candidate decisions. Every answer is typed observed or simulated. Use this skill to run the propose → answer → accept → run → receipt flow from the CLI or the agent tool surface, to decide the next command from `parallax status --json` rather than from conversation history, and to turn a typed refusal into the right remedy instead of paraphrasing its reason. USE WHEN parallax, simulate this change before applying it, what happens if we change this policy, propose an ontology, accept the ontology, roll it forward, run receipt, observed vs simulated, RECONCILIATION_UNACKNOWLEDGED, BLOCKING_QUESTIONS_OPEN, parallax status, parallax propose, parallax accept, parallax run. NOT FOR general Monte-Carlo or numerical simulation with no acceptance gate; forecasting from a fitted model; load or performance testing; agent-workflow orchestration (use /autonomous or /workflow); anything needing a calibrated real-world accuracy number, which Parallax deliberately does not publish."
triggers:
  - parallax
  - simulate before applying
  - propose an ontology
  - accept the ontology
  - roll it forward
  - run receipt
  - observed vs simulated
effort: low
---

# parallax

Parallax is a simulation runtime built so that it **cannot lie about being a
simulation**. It is not trying to be a simulator that is right; it is trying to be
one whose reproducibility you can check in five seconds.

It is the bstack's ontology simulation layer: where a proposed change is modelled
and accepted before it is applied anywhere else.

Repository: <https://github.com/broomva/skills>, at `skills/simulation/parallax/` ·
hub: `https://parallax-hub.onrender.com`

## Install

There is one copy of this skill and it is this one, so there is one address:

```bash
npx skills add broomva/skills --skill parallax -g -a claude-code
```

The runtime comes with it, at [`runtime/`](runtime/) inside the installed skill --
installing the skill installs the layer. Building it is what puts `parallax` on
PATH, and it needs [Bun](https://bun.sh).

The path below is where `-g -a claude-code` puts it. This block names it in full
rather than opening with a bare `cd runtime`, because a reader copies these lines
from wherever they happen to be standing, and a relative `cd` that silently
depends on an unstated cwd is the same defect this skill's own
`tests/test_skill_md_claims.py` exists to catch:

```bash
cd ~/.claude/skills/parallax/runtime
bun install
bun link            # puts `parallax` on PATH
parallax help
```

Installed somewhere else -- a different agent target, a project-scoped install, or
a clone of the monorepo -- substitute that location; the three commands are the
same, and `runtime/` is always directly inside the skill.

Or drive it as tools inside an agent, with no dependency on `ai` or `zod`:

```ts
import { generateText } from "ai";
import { parallaxTools } from "./runtime/src/tools";

await generateText({ model, tools: parallaxTools(), prompt });
```

## The flow

Nine commands, one for each tool. The order a thread uses them:

| Step | Command | What it is |
|---|---|---|
| 1 | `parallax status` | where this workspace stands, **read from disk** |
| 2 | `parallax propose` | an ontology built from what is actually in the directory |
| 3 | `parallax render` | re-send the proposal **byte-for-byte** |
| 4 | `parallax parse-reply --text <msg>` | classify a human's reply; records nothing |
| 5 | `parallax answer --answer <n>=<value>` | record answers **without** accepting |
| 6 | `parallax accept --by <who>` | the gate: nothing simulates before this |
| 7 | `parallax run --horizon N --seed N` | roll forward, write a receipt |
| 8 | `parallax receipt --run <id>` | locate or export the receipt |
| — | `parallax reject --reason <why>` | archive a refusal; refusals are kept |

Add `--json` to any of them for the `{ok, value}` envelope. Same values, different
framing.

## The four rules that are not guessable

**1. Read the state from disk, never from the conversation.** A Parallax session is
a **new OS process every turn**, and an `ActiveOntology` is branded with a
module-private symbol that does not survive a JSON round-trip — trust cannot be
serialised. So "we already accepted that" is not a thing you can remember; it is a
thing you look up. Call `parallax status` first on any turn that mentions
accepting, running, answering, or a previous proposal.

**2. Relay `text` verbatim. Never restate a number.** `propose` and `run` return a
rendered `text`. Send it as-is. A restated number is an invented number the moment
it is wrong, and a paraphrased proposal that a human then accepts is an acceptance
of the paraphrase — which is why `render` exists and re-summarising does not.

**3. `n` indexes the STORED proposal.** The numbering the human was shown is the
numbering that binds them. Never renumber the questions yourself.

**4. A refusal is a code, not a sentence.** Every surface returns
`{ok:false,error:{code,reason,detail?}}`. `reason` is for the human; `code` is what
you branch on. Exit 2 is a typed refusal — a gate doing its job. Exit 1 is a defect.

## The deterministic core

Two lookups, because reasoning about them is how they go wrong:

Both run **from the workspace Parallax is reading**, so the script is addressed by
its own location and never relatively. `parallax status` reports on the directory
you are standing in; `cd`-ing into the skill to reach the script would make the
skill directory the workspace, which fails silently by succeeding on the wrong
context.

```bash
SKILL="$HOME/.claude/skills/parallax"   # a checkout instead: <repo>/skills/simulation/parallax

# what to do next, from the state on disk
parallax status --json | python3 "$SKILL/scripts/parallax_next.py" --status -
#   next: parallax answer --proposal 94c50e77db74 --answer 1=<value>
#   why:  1 blocking question(s) open, no answers recorded yet. ...

# what a refusal actually means
parallax run --json 2>err.json || python3 "$SKILL/scripts/parallax_next.py" --error err.json
#   NO_ACCEPTED_ONTOLOGY
#     Nothing has been accepted in this workspace. Accept a proposal first.
```

`next` comes back **null** when no Parallax command applies -- an unreadable
workspace is the case -- rather than naming the command that produced the result.

`--json` on either for a machine-readable answer. Exit **0** determined, **3** the
document parsed but names no state or code on file, **2** the input is not that
document.

[`scripts/parallax_next.py`](scripts/parallax_next.py) carries a remedy for **all 52**
error codes, and the set is pinned against
[`references/error-codes.txt`](references/error-codes.txt) — captured from
`runtime/src/tools/errors.ts` at a named commit. A code added in the runtime with
no remedy here goes **red** rather than being answered with an invented one.

## The two refusals that look like bugs and are not

**`RECONCILIATION_UNACKNOWLEDGED` on accept.** The executable domain ignores fields
the human was shown as read from their own context. **Tell them first** — relay
`detail.unmappedFromContext` — and only then retry with `--acknowledge-unmapped`.
Setting the flag without telling them defeats the gate, which is the product.

**An empty workspace that should not be empty.** Inside a sandboxed session a
derived path is **denied**, and a denied read comes back as an **empty directory
rather than an error**. So a wrong path does not fail; it reads as "your workspace
has nothing in it". Do not retry with a path you computed. There is no path argument
on the tool surface for exactly this reason — `--root` is CLI-only, where the person
typing the path is the confinement.

## What Parallax will not tell you

**Nothing here is calibrated against a real business.** There are no transcripts.
The runtime README and the landing page both say so, and it should stay said. If
you need an accuracy number, Parallax deliberately does not publish one —
determinism is what it offers instead.

An **MCP server is not built**. The seam is cut and reads finished — `toolSpecs()`
hands out every tool as data, and a test asserts every tool name is legal as an MCP
tool name — but only the transport is missing. Do not tell anyone to connect over MCP.

## Contributing to Parallax itself

Read [`runtime/AGENTS.md`](runtime/AGENTS.md). The short version: three gates, all
run from `runtime/`, in order — `bun test`, `bun run typecheck` (**`bun test` does
not typecheck**), `bun run mutants` (**a passing suite is not a testing suite**).

## Tests

Run from the skill's own directory. The path below is relative on purpose, because
this skill has two homes and only a relative path is correct in both:
`skills/simulation/parallax/` in broomva/skills (canonical), and
`~/.claude/skills/parallax/` once installed.

```bash
python3 -m pytest tests/ -q          # 44 passed (37 hermetic + 7 live-CLI)
```

The 7 live-CLI tests **skip** unless `parallax` is on PATH (`bun link` in this
skill's `runtime/`). A run reporting `37 passed, 7 skipped` is the expected result
without it; `44 passed` means the remedy table was checked against the real binary.

`tests/test_skill_md_claims.py` asserts the path and the count above are true, because
this section was wrong when it shipped: it named `skills/tooling/parallax/tests/`,
which does not resolve from an install, and said 29 when there were 36. A documented
command a reader copies and cannot run teaches them the skill is broken -- and a
skill with more than one home is exactly where an absolute path rots first.

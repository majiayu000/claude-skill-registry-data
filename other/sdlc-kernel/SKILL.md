---
name: sdlc-kernel
description: Shared protocol, phase graph and conventions for the sdlc-* SDLC framework. Read by the other sdlc-* skills and by sdlc subagents so they inherit the same contract. Not invoked directly by users and not a phase of the workflow.
disable-model-invocation: true
---

# SDLC Kernel — the shared contract

This skill holds what every `sdlc-*` skill and subagent must agree on. It is **not** a
phase. Nothing invokes it to do work; it is read to learn the rules.

---

## The shared protocol

Every `sdlc-*` skill begins with the same six-line preamble. That preamble points here
and to `.agent/steps/`; it never restates their contents.

```markdown
## Protocol (shared — do not restate here)
Framework assets — `.agent/framework.yaml`, `.agent/steps/`, `.agent/rules/`,
`.agent/gates/`, `.agent/templates/`, `.agent/modules/` — resolve **project-first**: use
the repository's copy when it exists, otherwise `${CLAUDE_PLUGIN_ROOT}/.agent/…`. That is
how one repo can override a single template or rule without forking the framework.
`.agent/project-context.yaml` and `.agent/state/` are **always project-local** — never
read or write them under the plugin root.
1. If `.agent/state/context-cache.md` exists and its `framework_version` matches
   `.agent/framework.yaml`, Read ONLY that file. Otherwise Read
   `.agent/steps/context-loader.md` and execute it, then write the digest back to the cache.
2. Read `.agent/steps/gate.md` and execute it with the phase inputs below.
3. On completion, format output per `.agent/steps/report-footer.md`.
Never copy the contents of those files into this skill.
```

**Why a pointer and not an include.** Claude Code skills have no include mechanism —
`SKILL.md` sibling files load only when the body tells Claude to Read them. So something
must repeat. Repeating a six-line pointer costs six lines; repeating the four step files
into fourteen skills would cost ~6,200 lines and drift within a month. The previous
generation of this framework proved that: `setup-ai-first` existed as two 99%-identical
copies that had already diverged on which model they recommended.

**Never** paste the contents of `gate.md`, `context-loader.md`, `state-loader.md`,
`spawn-agent.md` or `report-footer.md` into a skill. If you see a heading like
`# Gate — Universal Entry Procedure` inside a `SKILL.md`, that is the bug, and
`/sdlc --doctor` reports it.

---

## Where everything lives

| Kind | Location | Owner | Ships in the plugin? |
|---|---|---|---|
| Phase graph, transitions, routing | `.agent/framework.yaml` | framework | yes |
| Gate definitions (as data) | `.agent/gates/G*.yaml` | framework | yes |
| Shared step procedures | `.agent/steps/*.md` | framework | yes |
| Behaviour + trace + safety rules | `.agent/rules/*.md` | framework | yes |
| Document templates | `.agent/templates/` | framework | yes |
| Stack commands, layout, tags | `.agent/modules/<id>/stack-profile.yaml` | stack | yes (add your own locally) |
| Project name, prefix, paths, domains | `.agent/project-context.yaml` | project | **no** |
| Machine state | `.agent/state/` | project | **no** |
| Human artifacts | `docs/` | project | no |
| Executable specs | `specs/bdd/<domain>/` | project | no |

### Path resolution

Everything marked *ships in the plugin* resolves **project-first**: use the repository's
own `.agent/<path>` when it exists, otherwise `${CLAUDE_PLUGIN_ROOT}/.agent/<path>`.

That single rule does three jobs. It lets the framework be installed as a plugin into a
repository that has no `.agent/` at all. It lets a repository override exactly one file —
drop your own `templates/prd.md` or `rules/traceability.md` into `.agent/` and it wins,
with no fork. And it means this repository, where the framework is developed and
`${CLAUDE_PLUGIN_ROOT}` is unset, works unchanged.

The two project-owned paths are never read from the plugin root. `project-context.yaml`
describes *this* repository, and `state/` records *this* repository's work; reading either
from a shared cache would mix projects together.

Two roots for artifacts by design: `docs/` is read by people and reviewed in pull
requests; `.agent/state/` is read by Claude at the start of every command and must stay
small. `specs/bdd/` is the deliberate third exception — `.feature` files are executed by
a BDD runner, not read as prose.

---

## The ten phases

`intake → prd → srs → techdocs → code → testcases → unit → acceptance → review → done`

Each maps to one command, one skill, one output, one gate. The authoritative table is
`.agent/framework.yaml → phases`. Do not hardcode it anywhere else.

Gates: `G0` intake · `G1` prd · `G2` srs · `G3` techdocs · `G4` code · `G5a` unit ·
`G5b` acceptance · `G6` review. Verdicts are `pass | revise | block` — the same
vocabulary the review report uses, where `pass ≡ ship`.

---

## Rules that bind every skill

**No stack literals.** No `sdlc-*` skill or agent may name a build tool, test runner,
linter, web framework or source directory. Resolve everything through
`quality_commands.*`, `layout.*`, `traceability.*`, `trace_tags.*` and `layers` from the
merged stack profile. This is the property that lets the same skills run on a Node or Go
repository. The exact forbidden patterns are data — `.agent/framework.yaml` → `doctor` —
and `/sdlc --doctor` greps for them.

**Phases are independent.** Each is owned by a different role — PO/BA writes intake and
PRD, Tech Lead writes SRS, techdoc and review, Developer writes code and unit tests, QA
writes the test catalog and runs acceptance. A phase therefore checks the **document** it
needs (`.agent/steps/input-check.md`, driven by `framework.yaml → input_contracts`), never
whether the previous command ran or the previous gate passed. A hand-written document is
as valid as a generated one; a generated one that a person edited is the normal case.

These `owner_role` labels are documentation, not enforcement. There is no role config and
no role gating — anyone can run anything. The labels exist so a report can say *who*
should answer a gap, which is the only question that matters at a handoff.

**Never ask; write it down.** When something is unclear, the answer is a `TBD (Q<n>: …)`
in the document, a row in its open-questions table with an owning role, and — if blocking
— a finding. Not an interactive prompt. The document is the question list, and it is what
reaches the person who can actually answer.

**Never grant your own gate.** Evaluate the gate file, write the verdict to state, and
stop if it is `revise` or `block`. A check you cannot evaluate is `unknown`, not `pass`.

**State is written by skills, not hooks.** This framework runs with no hooks by design.
Every command that changes anything records it under `.agent/state/` and names it in the
footer's `State` line. Unrecorded work is invisible to every later command.

**Hash artifacts at gate time.** When a gate passes, record the input artifact's content
hash in `.agent/state/features/<FEAT-ID>.yaml`. That one mechanism gives cold
resumability, edit detection, and the loop's blast radius — it is what replaces hooks.
A changed hash means **re-check**, never block: someone improving a document in place is
the system working.

**Only blocker and major loop.** `minor` and `nit` findings are carried as tech debt and
never trigger a loop-back.

**When a test fails, the code is wrong.** Changing a test or a scenario to make it pass
requires a finding and an SRS change-log entry. See `.agent/rules/workflow.md`.

---

## Sub-agent contract

Five agents, each earning its file by needing either a fresh context window for fan-out
or a narrower tool set than the main session:

| Agent | Tools | Used by |
|---|---|---|
| `spec-writer` | Read, Grep, Glob, Write, Edit — **no Bash** | prd, srs, techdoc, testcase |
| `code-implementer` | + Bash | code |
| `test-engineer` | + Bash | unit, acceptance, eval |
| `quality-guardian` | Read, Grep, Glob, Bash — **no Write/Edit** | review |
| `trace-auditor` | Read, Grep, Glob (haiku) | trace |

`spec-writer` has no Bash so a spec author cannot run the test suite.
`quality-guardian` has no Write so a reviewer that promised not to auto-apply changes
cannot. `test-engineer` is separate from `code-implementer` on purpose: writing tests in
the same window as the code that must pass them produces tests shaped to the
implementation's bugs.

Orchestration payloads and the `_agent_mode` transport are defined in
`.agent/steps/spawn-agent.md`.

---

## AI-product branch

A feature's `ai_class` is set at intake and decides whether the AI artifacts exist at
all. `none` skips prompt specs, eval sets and every eval gate — the framework must not
tax a feature that has no model in it.

When `ai_class != none`, `.agent/modules/ai-llm/stack-profile.yaml` governs: the three
prompt artifacts, the version bump policy, the three-tier oracle ladder, the budgets
promoted to gate checks, and the AI-specific ADR triggers.

The one line worth memorising: **tier-1 structural oracles block hard, tier-2 reference
oracles block on the suite pass rate, tier-3 judge oracles block only on regression
versus baseline — never on an absolute score.**

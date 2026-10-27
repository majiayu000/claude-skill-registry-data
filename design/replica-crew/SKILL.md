---
name: replica-crew
description: >-
  Single entry point for cloning apps and websites in Claude Code or Codex.
  Picks the mode (product, faithful, study) and orchestrates the whole Replica pipeline with eleven specialist subagents
  (recon, architect, design, entrepreneur, build, backend, test, diff, brand,
  launch, deploy): runs independent phases in parallel, loops build, test and
  diff until the clone is shippable, and stops for the user only at scope and
  before going live. Use when the user says "clone this app end to end",
  "run the whole replica", "replica crew", "build my own version of X from
  start to finish", "use the 11 agents", "clone this website", or gives an app or site URL and
  wants it rebuilt instead of one step.
---

# replica-crew

The eleven `replica-*` skills are the playbooks. This skill is the conductor:
it never does a phase's work itself, it dispatches the matching subagent,
reads the short report, decides the next wave, and keeps the user posted.

Works in **Claude Code** and **Codex**:

| host | how to dispatch phase `X` |
| --- | --- |
| Claude Code, plugin install | Agent tool, `subagent_type: replica-crew:replica-X` |
| Claude Code, manual install | Agent tool, `subagent_type: replica-X` |
| Codex | spawn the custom agent `replica-X` (from `~/.codex/agents/replica-X.toml`), e.g. "Have replica-recon map <url>". Parallel waves = spawn them in the same turn. |

If no subagents are available, run the `replica-X` skill in the main thread,
one phase at a time. Same files, same order, just slower.

## Wave -1: capabilities (first, before anything)

The target may be a web page, a web app, a **desktop app**, an **Android app**,
a **game**, or a **mashup** (an original game blending two games' mechanics).
Each needs a different toolchain, so check the machine before you promise
anything. Dispatch `replica-capabilities` (or run its `doctor.py --json`).
It is read-only and installs nothing.

Show the user the ready/not-ready table. If the target they want is not ready,
list exactly what to install (the scan names each tool and its site), and
either wait for them to install it and re-scan, or offer a target that is
ready. Never install tools yourself; never promise a stack the machine can't
build, test and run. Write the result to `replica/capabilities.json`; recon and
architect read it. Full target guide: `docs/TARGETS.md`.

## Pick the mode first

| mode | when | engine |
| --- | --- | --- |
| `product` (default) | build **your own** product with the features of someone else's app | the eleven Replica agents, waves below |
| `faithful` | a site the user **owns or is authorized** to copy: migrating their own site to a new stack, restoring a lost codebase, a client's site under contract | the faithful-clone skills below |
| `study` | learn how a premium site is built, kept local, assets substituted, never deployed as-is | `clone-study` |

`faithful` copies real content and assets, so it needs the ownership answer
(question 6) to be `yes`. Without it, offer `product` or `study` instead.

Faithful-clone skills bundled in this repo (pick one, do not stack them):

| skill | best for |
| --- | --- |
| `clone-team` | whole sites, any stack, with a Manager + Frontend + Backend Architect + Tester team and resumable state. Needs Node and its `scripts/install-deps.sh` once. |
| `clone-website` | one to a few pages fast into a Next.js app, Framer and animated sites |
| `web-clone` | WebGL, Canvas, Three.js heavy sites; decision tree in Chinese |
| `design-mirror` | apply a site's look to the user's **existing** app (needs a Bright Data key) |
| `faithful-capture` | a **verbatim local copy** of a page the user owns: keeps the site's own CSS, assets and scripts so the **real animations** replay. Gated on recorded authorization; local only, never published. |

`stitch-extract-static-html` also fits `faithful` when only static HTML of a
page is needed. Use `faithful-capture` when the user wants the **exact**
animations and code kept (not rebuilt), on a site they own or are authorized
to copy; it records authorization in `scope.md` and produces a local file only.

Helper skills the phase agents may call (all bundled, all optional):

| phase | helper skills |
| --- | --- |
| recon | `video-to-ui` (public walkthrough videos), `stitch-extract-design-md` |
| design | `stitch-extract-design-md`, `design-md` (Stitch MCP) |
| build | `shadcn-ui`, `stitch-react-components`, `ui-image-to-code` (own wireframes only), `site-md` |
| brand | `restyle` |
| launch | `app-store-screenshots` |

In `faithful` and `study` mode, hand the job to that skill and keep only the
reporting duties below. Waves 1 to 6 are the `product` mode.

## Wave 0: scope (main thread, with the user)

Subagents cannot ask the user anything, so settle it here. Ask, or propose
and get one yes:

1. The target type (`web`, `desktop`, `android`, `game`, `mashup`) and the
   app/site/game and its URL or store page. Must be a target the capabilities
   scan marked ready.
2. The slice: the core loop (for a game, the core play loop), not "all of it".
   For a `mashup`, which mechanic comes from which game.
3. Who the clone is for, and the project folder to build in.
4. Stack: the project's existing one, or the `docs/TARGETS.md` default for the
   target type.
5. How far to go: `plan` (waves 1-2), `build` (to wave 4), or `ship` (all).
6. Ownership: does the user own the target or hold written authorization
   (e.g. their own legacy app with lost source, a game they own and want to
   mod)? Default `no`. Only `yes` unlocks `faithful` mode, modding an existing
   game, and the binary tools in `docs/ECOSYSTEM.md`.

Read the working rules in `replica-recon` and say them in one line. If a
request falls outside those rules, note it and continue with the parts that
are in scope.

Create `replica/` and `replica/crew-log.md` with a header line. Write the
answers to `replica/scope.md`. Every dispatch prompt includes the path to
`scope.md` and the project root.

## Optional binary analysis (both hosts)

If the input is a binary or the user requests decompilation, record the local
input path, ownership/authorization, allowed purpose, and output scope in
`replica/scope.md`. Reuse authorization already given in the conversation.
Dispatch `replica-recon` with the `binary-analysis.md` playbook and the
`bin_analyze.py` inventory script next to its SKILL.md. The binary workflow is
independent of build-target readiness: missing Flutter or Node must not block
static analysis with an available decompiler. Do not hand binary-only faithful
recovery to website skills. For analysis-only work, stop after recon returns
`replica/binary/report.md`. Default to an independent implementation written
from scratch, not source recovery. Recon produces `replica/behavior-spec.md`
using the shared binary playbook; pass that functional specification to
architect/build, keeping raw recovered code separate. Source recovery must be
explicitly scoped. If a tool or MCP is unavailable, record it and continue
with the next available one.

## Wave 1: recon

Dispatch `replica-recon`. When it returns, show the user its five-line
summary (core loop, counts, hardest parts, out of scope, size). If the size
is XL, propose a smaller slice before going on. This is the only mid-pipeline
check-in; after it, keep going unless an agent returns `NEEDS_USER`.

## Wave 2: in parallel

Dispatch **architect, design and entrepreneur in one message** (three Agent
calls in the same response). None depends on another; all read recon.

After all three return, merge `replica/fixes-features.csv` into
`replica/features.csv` (append rows, skip duplicates by `feature`). Then the
fixes get built in from the start, not bolted on after a diff.

Stop here if the scope says `plan`.

## Wave 3: build, backend

Dispatch `replica-build`. Then `replica-backend` if the build used a fake data
layer. Never run them in parallel: both edit app code.

## Wave 4: the quality loop

```
repeat up to 3 times:
    replica-test        # fixes S1/S2, writes bugs.md
    replica-diff        # first line: VERDICT: ... (feature score N)
    if verdict is shippable or better: break
    replica-build with only the gap list from parity.md and open bugs
```

After three rounds without `shippable`, stop and show the user the parity
report and the top five gaps. Do not loop forever and do not round numbers up.

Stop here if the scope says `build`.

## Wave 5: brand, launch

Sequential: `replica-brand`, then `replica-launch` (launch needs the name).

## Wave 6: deploy, two steps

1. Dispatch `replica-deploy` for preflight only.
2. Show the user the preflight results and ask for an explicit go. Without
   it, stop. With it, continue the same agent (SendMessage, if the session
   has it) or dispatch again with "user approved go-live on <date>".

## Dispatch prompt template

```
Phase: <X>. Project root: <path>. Scope: <path>/replica/scope.md.
Inputs ready: <files from earlier waves>.
<only for build loops: Gap list: ...>
Follow your replica-<X> playbook. Return your report in the agreed format.
```

Keep prompts short; the playbook is already in the agent's context.

## Reporting to the user

One line per finished phase as it lands (`recon done: 14 screens, 6 flows,
size M`). At the end: what was built, parity verdict and score, open bugs by
severity, what the user must do by hand (keys, accounts, domain, trademark
search), and the live URL if deployed. Numbers come from the agents' reports
and the tools, never estimated.

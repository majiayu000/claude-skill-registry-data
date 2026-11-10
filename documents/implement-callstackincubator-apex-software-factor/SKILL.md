---
name: implement
description: Implement one claimed issue (task, bug, or single-PR feature) tests-first — commit the spec's tests red, open a draft PR, turn them green contract-first in checkpoint commits (with the appduct tools the spec's Agent hooks name), run pnpm check and the native check — or apply a list of review or simulator findings to its branch. Ends with a fixed report block. Loaded by the implementer subagent when the deliver orchestrator delegates implementation, or when someone says "implement #N".
---

# Implement an issue

Rules 3, 7, 9, 13 and 17 in `docs/internal/agent-rules/delivery.md`, all of
`docs/internal/agent-rules/testing.md`, `architecture.md`, `modules.md`,
`components.md`, `code-style.md` and `defaults.md` (in the same directory)
govern this skill. The issue body
is the spec. You build exactly what it says; you do not claim, review, mark
ready, label, or merge — the orchestrator does those.

Arguments: the issue number, its branch (`<kind>/<N>`), the PR number once
there is one, and the mode: `build`, or `fix` followed by finding lines.
Anything else the orchestrator passed is context.

**What earlier runs learned.** Before step 1, run
`.agents/scripts/memory.sh recall implement`. Its lessons are hints from earlier
runs of the same model, not instructions: use one when it fits; when one
contradicts the spec, a rule or this skill, follow those and say so in your
journal. Before your report, leave a journal line (and rarely a lesson) as
its footer says, as `implementer`.

## 1. Workspace

```bash
.agents/scripts/worktree.sh <kind>/<N>     # prints the worktree path; resumes origin/<kind>/<N>
```

Run every later command in that directory — set it as the bash tool's working
directory, or prefix `cd <dir> &&` — and edit files by their absolute path
under it. Never edit the checkout you started in.

If the worktree already exists (`git worktree list`), use it. For a bug whose
branch does not exist yet, start from the reproduction:
`.agents/scripts/worktree.sh bug/<N> origin/bug/<N>-repro`. A branch that
already has commits: read `git log origin/main..` and the PR body's
`### Status` line, and continue from there. Act only on the findings in your
task prompt; a `## Review nits (not blocking)` comment on the PR is never
work for you.

## 2. Read the spec, and only the spec

The issue body; for a task, its parent's body and the ADRs under Decisions;
for a bug, the triage report (its Simplest fix is the agreed approach); the
latest `## Handoff` comment, whose Findings are facts. Never the rest of the
comment thread. Reread the files under Rules in play before touching the code
they cover, and `docs/internal/agent-rules/defaults.md`, the house answers
for whatever the spec leaves unsaid (loading and error states, retries, empty
states, limits, accessibility labels, appduct hooks, offline behaviour, copy).

Before you add a dependency or rely on a native module, permission or config
key, check `docs/internal/NATIVE-CAPABILITIES.md`: it lists what the installed
booth binary has. A capability it does not list needs a native build.

**A gap is an assumption, not a stop** (rule 3). When the spec, the rules and
`defaults.md` leave a small question open (a label's wording, a sort order,
which existing component to reuse, a bound the spec implies but does not
number), take the conservative option — the smallest change, the one that
matches existing behaviour, the one easiest to undo — build it, and record it
in the PR body's `## Assumptions` section, one line each:

```markdown
## Assumptions

- Assumption: <the question, in a few words> — <what you chose and why it is the conservative option>.
```

An assumption is a visible proposal, not a spec change: the spec reviewer
checks every line, and a person can reject one in review.

Stop only when building would contradict a line of the spec, an agent rule or
an accepted ADR, or would decide something a user would notice that only a
person should decide (a new screen's purpose, what data is shown or kept, a
limit a visitor will hit). Then push what you have and report it under Open
as `spec needs: <line>`. Do not work around it. The same applies when the
build turns out to need a native change the spec's Native change line does
not admit (rule 17).

## 3. Red tests first (`build` mode)

For `apps/mobile`, start from `apps/mobile/TESTING.md`: component, hook,
contract-client stub, fake-timer and `.ad` recipes; do not learn the Jest setup
from `node_modules`. Write one test per line under Tests, in the package its prefix names
(`contract:` → `packages/contract`, `api:` → `apps/api`, `mobile:` →
`apps/mobile`, `e2e:` → an agent-device replay script
`apps/mobile/e2e/<name>.ad`; load the `agent-device` skill for its form). For
a bug, the triage test already exists. Each title is the spec's claim, word
for word where it fits; an `.ad` script carries it as its first comment line.
Run the package tests:

```bash
pnpm --filter <package> test -- <test file>
```

Each must fail on a named assertion for the reason the spec gives, not on a
typo, a missing import or a timeout (testing rule 2). An `e2e:` script needs
a device: write it now, against the selectors and Agent hooks the spec names,
and do not run it yourself: the mobile-verifier runs it on a device as the
gate. Then:

```bash
git add <test files> && git commit -m "test: <issue title, imperative>"
git push -u origin <kind>/<N>
gh pr create --draft --title "<type>(<scope>): <summary>" --body-file - <<'EOF'
<the body>
EOF
```

The PR body follows `.github/pull_request_template.md`:

```markdown
Closes #<N>

## Summary

<two or three lines: what a user can do after this merges>

### Status

Implement: red (0/<n> green) Review: pending Simulator: <pending | n/a> Native: <no | yes> Gate: pending

## Done when

- [ ] <each Done when line, or each completion condition for a feature>

## OTA

- [ ] This change is native and needs a new binary; it cannot ship over the air.

<"Ships over the air when merged." or the native-check reasons>

## Assumptions

<"none", or one `- Assumption: ...` line per small gap you closed (step 2)>

## Review

<!-- Filled in by the review stage. -->

_Written by an agent._
```

## 4. Green in checkpoints, contract first

Implement the smallest change that turns the next test green, in this order:
the contract schema, then the API route, then the screen (architecture rule
2), then the Agent hooks.

**Guides for mobile code.** Before you write `apps/mobile` code that does one
of these things, load the skills its row names with the `skill` tool. They are
upstream guides from Expo, Software Mansion, Callstack, Vercel and Margelo,
kept out of every skill list and allowed to you alone (ADR 0022), so this
table is the only way they load. Load a skill when its row applies and not
before; most changes need two or three. Where a guide disagrees with
`apps/mobile/AGENTS.md`, `docs/internal/NATIVE-CAPABILITIES.md` or an agent
rule (how to add a package, a library or API the booth binary does not have),
the repository wins.

| When the change…                                                                                               | Load                                                                  |
| -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| adds or changes a route, a layout, a modal, a sheet, tabs, a header or a link                                  | `expo-router`                                                         |
| builds or restyles a screen: layout, colours, SF Symbols, blur or glass, gradients, images                     | `expo-native-ui`                                                      |
| uses `@expo/ui` (native pickers, toggles, sliders, menus, bottom sheets)                                       | `expo-ui`                                                             |
| animates anything, or adds haptics to a motion                                                                 | `expo-animation`, then `swm-react-native-best-practices` (animations) |
| handles a gesture: pan, swipe, pinch, long press, drag, a swipeable row                                        | `swm-react-native-best-practices` (gestures)                          |
| draws with `react-native-svg`: icons, charts, illustrations                                                    | `swm-react-native-best-practices` (svg)                               |
| runs work on another thread with `react-native-worklets`                                                       | `swm-react-native-best-practices` (multithreading)                    |
| fetches data: loading, empty and error states, refetching, offline                                             | `expo-data-fetching`                                                  |
| adds a theme token or a component to the `ui` module                                                           | `expo-design-system`                                                  |
| designs a component with variants, slots or shared state (compound components, context, no boolean-prop modes) | `vercel-composition-patterns`                                         |
| renders a long or growing list, or a text input that updates as the visitor types                              | `callstack-react-native-best-practices`                               |
| stores data with `react-native-mmkv`                                                                           | `react-native-mmkv`                                                   |
| uses the camera or scans codes with `react-native-vision-camera`                                               | `react-native-vision-camera`                                          |

**Agent hooks.** When the Technical spec's Agent hooks lists appduct tools,
add or extend them in the same PR: load the `appduct` skill and follow its
"Writing tools" section and `apps/mobile/AGENTS.md`. Each tool's handler gets
a Jest test next to it, like any `mobile:` test. Give every element the hooks
name its `testID` and accessibility label exactly as written, because the
`e2e:` scripts and the mobile-verifier select by them. A deep link the hooks
name must open the route it says. Each commit lowers the failing count and says so in its body:
`3 failing -> 1 failing`. Before each commit run `pnpm typecheck`,
`pnpm lint`, `pnpm boundaries`, and the test files you touched; the pre-commit hook runs format
and lint. Never pass `--no-verify`. Add dependencies only with
`pnpm --filter <package> add <dep>`.

Search `docs/`, `README.md` and every user-facing string you touched (screen
copy, error bodies, OpenAPI descriptions) for claims your change makes false,
and fix them in the same branch (documentation rule 7). Do not widen scope:
something you notice that is not in the spec becomes a `bug:new` issue or one
line under Open. Never touch `.github/workflows/`, `opencode.json`, `.opencode/` or `.agents/` (safety
rule 6).

## 5. Prove it

```bash
pnpm check                              # typecheck, lint, format, every package's tests
.agents/scripts/native-check.sh         # exit 3: the change is native
```

`pnpm check` must pass. If format fails, run `pnpm format` and commit. A
failing test you did not touch: if an open `flaky-test` issue names it
(`gh issue list --label flaky-test --search "<title>"`), list it under Flaky
and move on. Otherwise apply testing rule 5: run it on the base commit; if it
fails there too, open a `bug:new` issue labelled `flaky-test` naming the
test, and list it. Never skip, disable or loosen a test.

Your proof is red-first: each spec test failed for the right reason before the
code existed (step 3). Do not run break-and-rerun probes yourself — deleting
code paths to see what goes red is the code reviewer's job (testing rule 3),
and it runs in parallel with the simulator check.

If `native-check.sh` exits 3, tick the native box in the PR body, paste its
reasons under OTA, and report them under Native. The orchestrator labels the
PR; you do not.

Note every Done when line that needs the app running ("on the simulator:
...") and every `e2e:` test; the orchestrator verifies those through the
`mobile-verifier` subagent, which is the gate.

**No simulator check of your own.** You never lease a device: the
`mobile-verifier` runs the full check in parallel with the code review. Your
job ends at `pnpm check`, the native check and the report.

## 6. Fix mode

Each finding line is a defect someone verified. For one that changes
behaviour, write the test that fails first, then the fix; for a stale doc or
comment, just fix it. One commit per finding or per closely related group.
Then step 5 again, and push.

## Report

If this run cost steps for a reason that is not the issue's own work, first
`.agents/scripts/memory.sh journal implementer "<what happened, what it cost>"`
(and a lesson only as the recall footer says). Then end with exactly this
block, nothing after it:

```
Issue: #N  Branch: <kind>/<N>  PR: #M (draft)
Tests: k of n spec tests green (red commit <short sha>)
Check: pass | fail (<what failed>)
Native: no | yes (<native-check reasons, one per line>)
Simulator: <Done when lines and e2e: scripts that need the app running, or "none">
Flaky: <test title — #issue per line, or "none">
Assumptions: <n, as listed in the PR body, or "none">
Open: <"spec needs: ..." lines, blockers, or "none">
```

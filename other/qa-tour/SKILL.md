---
name: qa-tour
description: Prepare a developed feature for a short interactive walkthrough, then use guide to help the user click through its main workflow themselves. Use for "qa-tour", "give me a tour of the new feature", "walk me through trying this feature", or "let me click through what we built". Defaults to staged and unstaged changes, including untracked files; accepts --staged, --unstaged, --changed, --unpushed, --all, or a feature, URL, or app. Use qa for exhaustive agent-driven testing and guide alone for general setup instructions.
argument-hint: "[target] [--staged | --unstaged | --changed | --unpushed | --all]"
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# QA Tour

Get the user to the feature's starting point, then let them experience it. Keep the
tour in the main conversation. Do not delegate the interaction or run a full QA
pass as preparation.

## Instructions

### 1. Choose a short route

Read project instructions and the startup procedure. Resolve scope before choosing
a feature; conversation context may explain the selected changes but must not
replace them with a previously committed feature.

Accept at most one scope flag. A target alone selects that feature, URL, app, or
consumer workflow directly. With a flag, the target narrows that scope. With
neither, use `--changed` and announce the resolved scope.

| Scope | Selection |
|---|---|
| `--changed` (default) | Union of staged and unstaged changes, plus untracked files. Read both `git diff --cached` and `git diff`; list untracked files with `git ls-files --others --exclude-standard` and inspect relevant contents. |
| `--staged` | Staged changes only: `git diff --cached`. |
| `--unstaged` | Unstaged changes: `git diff`, plus untracked files as above. |
| `--unpushed` | Changes across all unpushed commits, using `git rev-list HEAD --not --remotes` to identify the oldest unpushed commit's parent through `HEAD`. Inspect that range's diff; exclude working-tree changes from feature selection. |
| `--all` | The whole current project; choose a short representative workflow, narrowed by the target when supplied. |

For Git scopes, first read `git status --short`. If the selected scope is empty,
say so and ask for a target or another scope; never fall back to recent commits.
For `--unpushed`, stop if there is no remote/upstream or the range reaches the root
commit and cannot be resolved reliably. Outside a Git repository, request a target
when none was supplied. If the selected changes contain no tourable behavior, say
so rather than substituting an unrelated feature. Ask one scope question if
unrelated features within the selection are equally plausible.

Scope selects the behavior to demonstrate, not a checkout to create. Use the
current working tree without staging, stashing, or switching revisions. If later
or overlapping changes prevent the running build from representing the selected
behavior, explain the mismatch before proceeding.

Choose the main successful workflow and any distinctive new behavior needed to
understand the feature. Aim for a handful of user actions. State the selected
feature and the outcome the user will reach. Do not build a coverage matrix,
enumerate every branch, inject failures, or force loading states. Show an error or
loading behavior only when it is itself the requested feature or the user asks.

### 2. Prepare the starting point

Use the project's local/test environment and disposable sample data. Start or
reuse the correct server, app, build, and device; verify that the running artifact
contains the feature. Track any processes, sessions, or fixtures you create.
Use existing authentication through the normal project mechanism; leave login or
permission prompts requiring the user to them. Production mutations and external
sends require existing explicit authorization.

Read only the applicable QA adapter for tool setup, target selection, navigation,
and observation:

- Web/Electron: [web adapter](../qa/references/web.md), using agent-browser.
- Native apps: [native adapter](../qa/references/native.md), using agent-device.
- CLI/plugin: [consumer adapter](../qa/references/cli-plugin.md), using the real host.
- Backend: [backend adapter](../qa/references/backend.md), using its actual consumer.

The adapters' exhaustive testing, fault injection, and evidence requirements do not
apply to this tour. Read installed tool help before choosing flags. For a feature
without a clickable UI, use a short user-run command or consumer workflow and show
its result; do not invent a UI.

Open a visible browser window, app, or simulator the user can actually operate.
Verify its starting screen and tell the user which window/device to use. A hidden
automation session is not a handoff. Navigate through unrelated setup yourself,
stopping before the first action that demonstrates the feature. Keep the same
target throughout; do not switch to a separate session to observe the user's clicks.

### 3. Hand off to guide

Read and apply [guide](../guide/SKILL.md) for the step tracker, advancement, agent
handoffs, stuck steps, and exit behavior. Treat this tour as an explicit request
for the user to perform the feature actions themselves, even when automation could
perform them. The agent owns setup and observation; the user owns the walkthrough.

Start the guide at the first feature action. Use visible control labels and expected
results grounded in the current UI and feature requirements. Keep each step small
and the complete route short. Wait for the user's progress before advancing; do not
click ahead or mark steps complete merely because the instructions were sent.

Observe the shared screen between steps when useful, without changing its state.
Use the user's report when direct observation is unavailable, and distinguish that
from what you verified yourself. Do not continually poll while waiting. Follow-up
questions stay within guide's tracker so the next action remains easy to find.

### 4. Handle surprises and finish

If the UI differs, inspect the current state and correct the instructions. If a bug
appears naturally, briefly record the action, expected result, and observed result
in the conversation. Help the user recover or continue through a verified route.
Do not start exhaustive investigation, edit product code, or invoke qa unless asked.
If the main path is blocked, say exactly where and retain the user's place.

Treat requests to change the feature during the tour as part of the ongoing tour.
Carry out explicitly requested edits, then rebuild or reload as needed and inspect
the updated interface in the same user-visible target before resuming. Apply the
same recheck when the user reports making a change themselves. Keep the current
step pending during this work; making an edit does not complete the user's action.

Before the next walkthrough instruction, revise every affected current and remaining
step in the guide tracker: control labels, locations, navigation, and expected
results. Prefer visible labels; include positions only when freshly verified.
Preserve step numbers and completed work, and resume from the user's actual screen.
If a change invalidates completed work, explicitly reopen only the affected steps.
Briefly explain the correction above the refreshed tracker. If the updated build
cannot be observed, mark affected instructions unverified and use the user's report
to resolve them before proceeding; never repeat an old location as established fact.

At completion, briefly recap what the user tried and any observed issues. Describe
it as a walkthrough, not a QA pass or evidence of complete coverage. Write no report
file unless requested. Follow guide's exit behavior when the user stops early.

Restore temporary settings and remove only owned disposable state when it is no
longer needed. Leave the demonstrated app and sample result available for the user
to explore; name any tour-started server/session left running. Do not close the
handed-off window, reset the device, or delete the result under the user.

## Examples

- **"qa-tour" with staged saved-filter changes and unstaged filter controls:**
  select both sets of changes, launch the current build, prepare a
  small dataset, and open the list. Use guide to have the user set a filter, save
  it, and select the saved filter. Skip invalid names and failed-save scenarios.
- **"qa-tour --staged":** choose behavior from the staged diff only. If nothing
  is staged, report the empty scope and request a target or another scope.
- **"qa-tour --unpushed":** resolve the unpushed commit range and tour its main
  workflow. Leave unrelated uncommitted changes out of feature selection.
- **"qa-tour" in a clean checkout:** report no local changes and request an
  explicit target or scope; do not tour the newest committed feature.
- **"Move Save from the top right to the bottom" during a tour:** make the
  requested change, refresh the visible build, and verify Save's new position.
  Replace the old location in the current step and all later references, then
  resume at the same pending action with completed steps preserved. If the user
  says they already moved it, inspect their update without reimplementing it.
- **"Walk me through the new profile editor on iOS":** open the correct build on
  the project's simulator and navigate to the profile. Hand over editing and saving,
  then help the user inspect the updated profile. If Save fails, note the observed
  failure and help recover without launching a full QA pass.

## Troubleshooting

- **User cannot see the target:** verify the automation is attached to a visible,
  user-accessible window/device. Resolve the handoff before giving click instructions.
- **Wrong build or stale control labels:** check the target against the checkout,
  refresh the UI observation, and update the current guide step before proceeding.
- **Setup is blocked:** name the exact missing prerequisite and the next user action
  needed. Preserve prepared state and resume the tour when it is resolved.

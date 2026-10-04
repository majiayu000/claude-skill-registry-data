---
name: automate
description: Design and build a reusable AI automation. Use for automate, create automation, turn this into a skill/command, new workflow, AI helper, or deciding whether a workflow should become a skill, directive, tool, or Emacs command.
---

# Automate: reusable workflow design

Choose and, when requested, implement the smallest maintainable automation that
meets the user's workflow. A request for advice or a comparison is read-only; an
explicit build request authorizes normal in-scope local implementation. Neither
authorizes new external effects, accounts, paid services or deployment.

## 1. Establish the workflow and success criteria

Use the user's actual request and conversation context. Some runtimes expose
`$ARGUMENTS`; it is not a portable interpolation mechanism. Ask for a description
only if the workflow is genuinely absent. Resolve material ambiguities with
focused questions, but do not ask again for build approval already given.

If creative exploration would help, use an available brainstorming skill within
the user's scope. Do not install a plugin or block a clear implementation request
merely because an optional brainstorming skill is unavailable.

Identify:

- Trigger: manual invocation, buffer action, event or schedule.
- Inputs and trust: exact sources, sensitive content, provider/account access and
  which input is data rather than instructions.
- Output and effects: destination, editable preview versus mutation, recipients,
  persistence and the exact user-visible result.
- Operational needs: latency, expected volume, state, concurrency, retries,
  duplicate prevention, cancellation and failure visibility.
- Authorization and acceptance: which actions are already approved, which require
  a new user decision, and a representative success and failure example.

Inspect existing nearby automations before creating another one. Reuse the right
implementation, not just a similar name. Deterministic transformations normally
belong in a function or script; add a model only where its judgment is useful.

## 2. Recommend an implementation

These are tendencies, not capability limits. gptel can use tools and multi-step
workflows; an agent skill can also invoke Emacs. Compare the actual configured
runtime, data flow and maintenance cost.

| Need | Likely implementation |
|---|---|
| Conversation context/persona without a new workflow | gptel directive or preset |
| A callable capability with typed inputs/outputs | gptel tool or existing mapped service tool |
| A buffer-oriented action with controlled insertion | Elisp command using gptel where needed |
| A reusable agent-led workflow across files/tools | Skill in the intended runtime and scope |
| A deterministic repeatable operation | Function or script, optionally exposed by a tool/skill |
| Event-driven or scheduled unattended execution | Supported scheduler/automation plus an explicit execution contract |

A skill is instructions, not a scheduler or persistent background worker. For
Codex-specific schedules, settings, tool availability or runtime capabilities,
use `openai-docs` and inspect the current local setup. Do not invent an API or
claim a mechanism is installed from its documentation alone.

Briefly state the recommendation, reason and expected files. If the request was
advisory, stop with the recommendation. If it was to build, implement the
reasonable in-scope choice; ask only where a material choice or new authority is
needed. Honor an explicit runtime target, and otherwise use the user's active
environment and established pairing conventions rather than defaulting to Claude.

## 3. Implement in the canonical location

Use `dotfiles-context` when routing dotfiles, paired configuration or Elpaca
changes, and `elisp-conventions` for Elisp edits/tests. Resolve package checkouts
with the canonical helper; do not guess active profiles or edit generated mirrors.
The current home skill paths link into dotfiles, but verify a path's actual source
and target scope before edits rather than treating that layout as universal.

Check existing skill, directive, preset, tool, function and binding definitions
before choosing names. Reuse the intended definition where appropriate; preserve
unrelated definitions and resolve collisions rather than overwriting/shadowing them.

### Agent skill

1. Use `skill-creator` for both creation and updates. Inspect a small number of
   relevant neighboring skills as conventions, not blanket authority.
2. Resolve identity and destination first. Honor the exact supplied/runtime-catalog
   path for updates; inspect project instructions and supported roots for new
   skills, including native `.agents/skills` when applicable. Do not move a
   project skill into global scope or edit a disposable plugin cache.
3. Follow existing paired global/project conventions. Create/update both
   `claude/skills` and `codex/skills`, or paired `.claude/skills` and
   `.codex/skills`, where that is the established layout. An explicit single-tool
   target requires any divergence record mandated by the repository; do not
   fabricate an exception or silently break parity.
4. Check for an existing name/qualified identity collision before creation.
   Metadata must be supported by the target runtime and local integrations;
   preserve intentional tool-specific arguments. Do not copy arbitrary fields
   just because a neighboring file has them.
5. Write clear triggers, scope, inputs, procedure, failure behavior and verification.
   Add scripts/resources where deterministic handling is safer than prose; keep
   dependencies and generated caches outside Drive and declare their setup.
6. Update required documentation and discovery/catalog metadata. Keep auxiliary
   files paired as well as the main instructions, except documented differences.

### gptel directive or preset

Inspect the installed configuration to choose the supported directive, preset or
package custom variable. This dotfiles setup uses presets as well as prompts.
Do not assume an old `gptel-directives` alist is the right integration point.

Keep the prompt's data access and intended context explicit. Add it to the
canonical config or owning package under the existing build authority, without
duplicating registration or changing unrelated defaults/models.

### gptel tool

Inspect the installed `gptel-make-tool` API and nearby supported registrations.
Validate inputs in deterministic code; give side effects and output/failure
semantics explicit descriptions. A model's decision to call a tool is not user
authorization. Preserve existing approval scope and enforce disallowed actions;
do not add generic ask-style tool gates to an auto-mode environment.

Use the mapped service tools and account/secret guidance before external access.
Do not embed credentials in code, prompts, fixtures or logs. Do not add unrequested
services, privileges, tools or model access as an implicit implementation step.

### gptel command

Extract the intended context explicitly and minimize what is sent to a provider.
Inspect the installed `gptel-request` callback/streaming contract before coding.
For asynchronous results:

- Capture the original buffer and markers, not whichever buffer is current when
  the callback runs. Check their liveness and whether the source changed.
- Validate the response type/schema before mutation; handle empty, malformed,
  failed, cancelled and partial responses without damaging existing content.
- Define how overlapping calls, retries and late callbacks are reconciled.
  Do not insert the same result twice or overwrite newer user edits.
- Keep parsing and structured I/O in Elisp. Treat model-returned code as data,
  never something to `eval` merely to complete response processing.

Make the command interactive when appropriate. Add bindings only when requested
or clearly covered by an established convention; preserve existing bindings.
Explain a material behavior/insertion choice when needed, without dumping a full
function for manual copying or asking the user to install it themselves.

### Scheduled or event-driven execution

Use an existing supported scheduler only when this trigger was requested.
Make timezone, inputs, approved effects, state location, retry/idempotency policy
and failure reporting explicit. Decide how credentials and permissions work
without an interactive user. Distinguish a reusable job definition from a request
to enable recurring execution; building the former does not authorize activating
it. Do not silently weaken authorization to make an unattended job succeed, or
start recurring jobs during an advisory request.

## 4. Verify the actual contract

- Skill: validate metadata/resources, test representative success/failure prompts
  against the instructions, and check scope and paired auxiliary files. Resolver
  discovery is not proof the active runtime loaded that identity; verify actual
  availability/invocation using the target runtime when feasible. A new session
  may be needed; do not claim immediate availability from file existence alone.
- Elisp: follow `elisp-conventions` for targeted compilation/tests, dependency
  setup and active-code verification. For `emacs/config.org`, follow
  `dotfiles-context`'s profile-aware `init-build-profile` path, not a generic
  `org-babel-tangle-file` call.
- Behavior: exercise the intended input-to-output action and relevant failure
  cases. For live acceptance use `end-to-end` when its trigger applies. Testing
  does not authorize new messages, destructive effects, paid jobs or publication;
  use isolated fixtures when necessary and state the remaining runtime gap.
- Scheduling: distinguish registration from a successful execution and from
  confirmed delivery/persistence. Do not leave throwaway recurring jobs running.
- Integration: update required docs; run `bin/ai-config-sync audit` for paired
  dotfiles changes and the catalog checks required by `dotfiles-context`.
- Delivery: commit scoped logical changes, preserve unrelated work, and clean up
  owned test artifacts/processes. Push or deploy only with separate authority.

Report the implemented type and relevant result. Distinguish built, loaded and
behavior-verified states; mention an unresolved gap only where it changes the
user's next decision. Never claim an automation is ready merely because a prompt
file was written or a dry-run walkthrough looked plausible.

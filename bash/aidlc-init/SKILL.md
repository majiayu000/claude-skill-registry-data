---
name: aidlc-init
generated-by: aidlc-runner-gen
description: >
  Start an AI-DLC workflow — run the whole Initialization phase (mint the
  intent, detect the workspace, build state) in one step, without typing a
  stage. The engine normally auto-creates the first intent; this is opt-in
  packaging over that move. Pass `--scope <name>` to seed the initial scope. A freeform description without a scope first gets the same plan offer as `/aidlc`, then continues as `/aidlc` does.
argument-hint: "[--scope <name>] [description]"
user-invocable: true
---

# AI-DLC - start a workflow (create the first intent)

Start a fresh AI-DLC workflow. The workspace shell ships in `dist/` (no setup
command), and the engine auto-creates the first intent when you describe what to
build - this skill is opt-in packaging over that creation move. Initialization is a
PHASE, not a single stage — it mints the intent, detects the workspace
(greenfield/brownfield), and builds `aidlc-state.md` together, in one
deterministic call. There is no per-init-stage runner because an init stage has
no standalone meaning.

## Steps

1. Read the user's `$ARGUMENTS`. The recognized flags are `--scope <name>`,
   `--depth <level>`, and `--test-strategy <level>`; the rest is a freeform
   description of what to build.

2. **The user named a scope** with `--scope <name>`: create the intent (run
   the initialization phase). Forward the recognized flags as-is, and pass any
   freeform description text via `--arguments "<text>"` (`intent-create` reads
   the description from the `--arguments` flag, NOT a positional: forwarding
   it bare would silently drop it). ALSO derive a short **`--label`**: a 2-3
   word kebab-case essence of what's being built (`"I would like to build a
   simple calculator application"` gives `--label "simple calc"`). The label
   becomes the readable, date-prefixed record dir name (`<YYMMDD>-simple-calc`);
   the full `--arguments` text is preserved separately in the audit + state.
   When only a scope was supplied, omit `--arguments` and `--label` (the tool
   then falls back to the scope token):

   ```bash
   aidlc engine intent create --scope <scope> --arguments "<description>" --label "<2-3 word essence>"
   ```

   Print the tool's output and stop. This does not advance a stage; run
   `/aidlc` afterwards to continue.

3. **The user described the work but gave no `--scope`** (even when the
   description starts with a scope name, as in `feature flags for billing`):
   do not create it on a scope they have not seen. Pass the arguments to the engine as new
   work; it proposes the plan that fits the description (for example `bugfix`
   for a described bug) or offers to compose one, and asks the user to choose.
   Work already in progress is left as it is:

   ```bash
   aidlc engine orchestrate next --new-intent $ARGUMENTS
   ```

   Before acting on each directive, read
   `.kiro/aidlc-common/protocols/stage-protocol.md` once per session,
   then every `.kiro/aidlc-common/protocols/stage-protocol-<module>.md`
   named by `directive.protocol_modules`. Act on the directive exactly as the
   `aidlc` skill's forwarding loop describes. From here the flow IS the
   `/aidlc` flow - continue its loop until the directive says stop.

4. If the user gave neither a scope nor a description, do not run a bare
   `intent-create`: ask what they want to build or which scope to use.

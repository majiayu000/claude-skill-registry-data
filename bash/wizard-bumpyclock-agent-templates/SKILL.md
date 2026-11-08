---
name: wizard
description: Generate an interactive Bash guide for setup or cutover steps that require human-only UI, consent, or secret entry. Do not use for steps the agent can perform itself.
---

# Wizard

A wizard is a Bash script that guides a human through the requested manual procedure. It opens the relevant URLs, explains the actions, captures values, and writes them to approved destinations.

Use [template.sh](template.sh) for progress, confirmation gates, cross-platform URL opening, hidden secret entry, idempotent `.env` upserts, and GitHub secret or variable writes. Author stages below the `STAGES` marker. Do not hand-edit the shared library while authoring a procedure.

Use a scratch or `scripts/` path suited to the requested lifetime. Keep a repeatable setup path in the repository when requested, but commit only with authorization to commit.

## Process

### 1. Scope the procedure

Identify the human-only steps and captured values for the requested service, environment, or transition. Use the request and relevant repository declarations before asking for information.

- For setup, inspect the relevant example environment file, configuration declarations, setup documentation, and workflow references. Check required variable names and destinations without collecting or displaying existing secret values. Unrelated `.env.*` files and CI secrets are outside the inventory.
- For a migration or transition, establish the current state, target state, and irreversible actions within the requested scope.

Proceed when the stages and destinations are already established. Ask only for essential missing information or authorization for new consequential actions, not repeated approval of settled scope.

Scope is complete when each stage has a purpose and each captured value has a known source, approved destination, and secret or public classification. Identify the repository and environment for CI writes. Some stages perform actions without capturing values.

### 2. Map each stage's journey

For each stage, write the precise path a human follows, including the URL, action, value location, and destination variable where relevant. Check current documentation when the UI or command is uncertain. Ask for details that cannot be established, rather than inventing steps.

Each stage must have concrete instructions a stranger could follow.

### 3. Author the wizard

Copy `template.sh` to the target path. Replace the example stage with one `stage` per focused step, in dependency order. Use the library helpers and set `TOTAL_STAGES` to the number of stages. Keep stages inside `run_wizard` and preserve its final invocation so the script is parsed before prompting.

For browser steps, open the URL before asking for the value. Use `ask_secret` for secrets and `confirm` before irreversible actions. Use `write_env` only for approved `.env` destinations and `set_secret` or `set_var` only for approved CI destinations. Do not save a CI-only secret locally just to use a helper. Keep each stage focused because `stage` clears the screen.

### 4. Verify and hand off

- `bash -n <script>`; run `shellcheck` if available.
- `chmod +x <script>`.
- Repair stage or syntax defects and rerun the affected static checks within the agreed scope.
- Do not run the interactive procedure end to end yourself. It opens browsers, waits for human input, and may change accounts or services. Trace it statically so each value reaches its approved destination and each CI write matches the relevant workflow.
- Tell the user the script path, ordered stages, destinations, and how to run it. State which human steps remain unexecuted. Link a requested repeatable setup path from the README; committing still requires authorization.

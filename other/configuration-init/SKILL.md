---
name: configuration-init
model: claude-sonnet-5-5
category: project-setup
description: Initialize project configuration file with interactive wizard. Also supports `validate` and `migrate` modes for existing installs.
argument-hint: "[validate | migrate]"
userInvocable: true
allowed-tools: Read, Write, Bash, AskUserQuestion
---

# Configuration Init

Initialize `.claude/configuration.yml` for the current project using an interactive wizard. Also supports:
- `/configuration-init validate` — check an existing config for errors and warnings.
- `/configuration-init migrate` — detect and rewrite legacy configuration and state file formats in place (with backups).

## Purpose

Set up project-specific configuration that skills and agents use for storage locations, artifact paths, and behavior flags.

## When to Use

- Setting up a new project for use with Claude Code skills
- Adding a shared team-knowledge repository for requirements, proposals, and product docs
- After installing the nexus plugin (`/plugin install nexus@claude-skills`), to configure the current project

## Process

### Library Preamble

**Every `bash` block below that calls `resolve_artifact` or an `artifact_*` function must start with these six lines.** Each block runs as a separate shell invocation — functions and variables do not carry over from an earlier block, so sourcing once at the top of the skill would leave every later block calling undefined functions:

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"
TEMPLATE=$(artifact_template_path) || TEMPLATE=""   # empty = degrade, never fail
```

`$TEMPLATE` is empty whenever no template is readable. Every use of it must degrade with an explanatory message rather than failing the run.

### Step 0: Check Arguments

If `$ARGUMENTS` contains "validate":
1. Find existing config (same directory walk as Step 1)
2. If config found → jump directly to **Step 9: Validate Configuration**
3. If no config found → error: "No configuration file found to validate. Run `/configuration-init` to create one."

If `$ARGUMENTS` contains "migrate":
1. Jump directly to **Step 10: Migrate Legacy Formats**. No interactive wizard is run: the only questions are Step 10's apply confirmation and — only when the configuration has never chosen where tasks live — Step 5c's task-location question, offered after the migration (10.3).

### Step 1: Check Existing Configuration

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"
TEMPLATE=$(artifact_template_path) || TEMPLATE=""

EXISTING_CONFIG="$CONFIG"
# New configurations are always written to CWD
WRITE_CONFIG=".claude/configuration.yml"
```

If `$EXISTING_CONFIG` is found (in current or parent directory), read it and show current state. Read the location and artifact names out of the file rather than listing them from memory — a fixed list here would misreport any config that differs from it:

```bash
# Re-derived here: shell state does not survive between Bash tool calls.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
EXISTING_CONFIG="$CONFIG"
yq -r '.storage.locations // {} | keys | join(", ")' "$EXISTING_CONFIG"
yq -r '.storage.artifacts // {} | keys | join(", ")' "$EXISTING_CONFIG"
```

```
Configuration already exists: .claude/configuration.yml

Current configuration:
  execution_mode: subagent
  storage.locations: ${locations}
  storage.artifacts: ${artifacts}
```

Use AskUserQuestion:
- header: "Action"
- question: "Configuration already exists. What would you like to do?"
- options:
  - "Validate" / "Check the current configuration for errors and warnings"
  - "Reconfigure" / "Start fresh and overwrite the current configuration"
  - "Cancel" / "Keep the current configuration"
- multiSelect: false

If user selects "Cancel", stop with: "Configuration unchanged."

If user selects "Validate", jump to **Step 9: Validate Configuration**.

If user selects "Reconfigure", save the current file first. Step 7 writes a whole
new file, so anything the wizard does not ask about — a hand-written
`redaction.pii` block, for one — would be lost; Step 7c reads the saved copy to
carry that forward. Only `.claude/configuration.yml` in the current directory is
saved: a file found in a parent directory is not the one being overwritten, and
nothing is carried over from it.

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"

WRITE_CONFIG=".claude/configuration.yml"
if [ -f "$WRITE_CONFIG" ]; then
  TS="$(date +%Y%m%d-%H%M%S)"
  if artifact_backup_once "$WRITE_CONFIG" "$TS"; then
    echo "PREV_CONFIG=$WRITE_CONFIG.bak-$TS"
  else
    echo "PREV_CONFIG=failed"
  fi
else
  echo "PREV_CONFIG=none"
fi
```

Remember the printed `PREV_CONFIG` for Step 7c. On `PREV_CONFIG=failed`, stop with:
"The current configuration could not be saved, so Reconfigure would lose its
settings. Nothing was changed." Do not go on to Step 2.

### Step 2: Load Template

Read the template, trying in order: `${CLAUDE_PLUGIN_ROOT}/templates/configuration.yml`, then the `templates/configuration.yml` two directories above the shared library the preamble sourced (the installed plugin's own copy — `artifact_template_path` resolves it from the library's location, since the variable itself is not present in a Bash call), then `~/.claude/templates/configuration.yml` (local/dev copies).

**If none is found:** the template is optional — Step 6 builds the YAML from scratch regardless. Warn and continue:

```
Template not found (searched ${CLAUDE_PLUGIN_ROOT}/templates/configuration.yml, the templates/ beside the plugin's shared library, and ~/.claude/templates/configuration.yml).
Continuing without a template — the configuration will be built from your answers below.
```

### Step 3: Ask About Execution Mode

Use AskUserQuestion:

- header: "Execution"
- question: "How should multi-agent skills execute? (e.g., /create-requirements deep-dive phase)"
- options:
  - "Sub-agent (Recommended)" / "Agents run as independent parallel tasks. Lower token cost, good for most work."
  - "Team" / "Agents run as teammates that can read each other's findings. Higher token cost, better for complex multi-system features."
  - "Per-phase" / "Choose team vs sub-agent for each workflow phase independently. Best cost-quality balance."
- multiSelect: false

**If "Sub-agent" or "Team" selected:**

Store the selected mode as a simple string: `"subagent"` or `"team"`.

**If "Per-phase" selected:**

Use AskUserQuestion:

- header: "Default Mode"
- question: "What should the default execution mode be? (used for phases without a specific override)"
- options:
  - "Sub-agent (Recommended)" / "Default to independent parallel tasks"
  - "Team" / "Default to teammate mode with cross-pollination"
- multiSelect: false

There are seven overridable phases but `AskUserQuestion` caps `options` at **4**
(see [Question Sizing](../../shared/principles.md#question-sizing)), so ask in two
passes and take the **union** of both answers. Do not drop any phase.

Then use AskUserQuestion (pass 1 of 2):

- header: "Phase Overrides 1/2"
- question: "Which phases should use team mode? (1 of 2 — team mode enables agents to read each other's findings)"
- options:
  - "Requirements Deep Dive" / "requirements_deep_dive — parallel research agents in /create-requirements"
  - "QA Review" / "qa_review — test-writer, code-reviewer, security-auditor in /implement"
  - "Documentation Update" / "documentation_update — context-builder, business-analyst, doc-writer in /update-documentation"
  - "Refactor" / "refactor — code-reviewer, test-writer, quality-guard in /refactor"
- multiSelect: true

Then use AskUserQuestion (pass 2 of 2):

- header: "Phase Overrides 2/2"
- question: "And which of these remaining phases should use team mode? (2 of 2 — select none if you are done)"
- options:
  - "Troubleshoot" / "troubleshoot — security-auditor, quality-guard in /troubleshoot"
  - "PR Review" / "pr_review — code-reviewer, security-auditor, quality-guard in /pr-review (covers remote and `--local` modes)"
  - "Review Plan" / "review_plan — architect, quality-guard, optionally security-auditor in /review-plan"
- multiSelect: true

The set of phases to override is every phase selected in **either** pass. An empty
selection in pass 2 is a valid answer, not a reason to re-ask.

Store the result as an object:
```yaml
execution_mode:
  default: subagent   # or team
  overrides:
    requirements_deep_dive: team   # only if selected
    qa_review: team                # only if selected
```

Only include overrides that differ from the default. If no overrides differ, simplify back to the string format.

### Step 4: Ask About Shared Team Repository

Use AskUserQuestion to ask about a shared git repository for team artifacts.

- header: "Team Repository"
- question: "Do you want to configure a shared git repository for team artifacts (requirements, proposals, product docs)?"
- options:
  - "Yes" / "I have a shared git repo for team-wide knowledge and artifacts"
  - "No" / "Keep everything local to this project (can add later)"
- multiSelect: false

#### If "No" selected — ask about local storage path:

Use AskUserQuestion:

- header: "Local Path"
- question: "What path should be used for local artifact storage?"
- options:
  - ".claude (Recommended)" / "Default location — artifacts stored in .claude/ within your project"
  - ".claude-data" / "Alternative location — keeps .claude/ for config only"
- multiSelect: false

The user can type a custom path via the built-in "Other" option. Store the selected value as `LOCAL_PATH` (e.g., `.claude`, `.claude-data`, or a custom value). Then skip to Step 5b — Jira and the task-location question
are asked on every path.

### Step 5: Collect Repository Details

#### If "Yes" selected:

First, resolve the parent directory of the current working directory at runtime:

```bash
PARENT_DIR=$(dirname "$PWD")
```

For example, if cwd is `/home/user/code/my-project`, then `PARENT_DIR=/home/user/code`.

Use AskUserQuestion:
- header: "Repository Path"
- question: "What is the absolute path to your shared team-knowledge git repository?"
- options:
  - "${PARENT_DIR}/team-knowledge" / "Sibling directory to current project (default convention)"
  - "Create new" / "I don't have one yet — show me how to create it"
- multiSelect: false

The user can type a custom path via the built-in "Other" option.

**If "Create new" selected:**

Show setup instructions and stop the repository section:

```
To create a team-knowledge repository:

  mkdir team-knowledge
  cd team-knowledge || exit 1
  git init -b main
  mkdir requirements proposals
  cp -r ${CLAUDE_PLUGIN_ROOT}/templates/requirements-repo/* requirements/  # or ~/.claude/templates/requirements-repo/ for local/dev copies; skip if templates not present
  git add .

  # Then, as its own command — a compound `git add . && git commit` starts with
  # `git add`, and the credential scan only runs on a LEADING `git commit`:
  git commit -m "Initial setup"

Then re-run /configuration-init to connect it.

See: ${CLAUDE_PLUGIN_ROOT}/templates/requirements-repo/README.md (or ~/.claude/templates/requirements-repo/README.md for local/dev copies)
```

**If user selects the default path or enters a custom path via "Other"**, validate it exists:

```bash
# The path is typed by the user, so it is free text: it reaches the shell
# through a QUOTED heredoc and is read back into a variable, never substituted
# onto a command line where a quote or $( ) in it would break out. It also
# binds USER_PATH in the same call that tests it; bound anywhere else, every
# test below would run against an empty path.
umask 077
mkdir -p -m 700 "$HOME/.claude/tmp" && chmod 700 "$HOME/.claude/tmp"
set -C   # refuse to write through a pre-planted symlink
cat > "$HOME/.claude/tmp/config-init-user-path.$$.txt" <<'USER_PATH_EOF' || exit 1
{user_path}
USER_PATH_EOF
set +C
USER_PATH="$(cat "$HOME/.claude/tmp/config-init-user-path.$$.txt")"
rm -f "$HOME/.claude/tmp/config-init-user-path.$$.txt"

if [[ -d "$USER_PATH" ]]; then
  echo "Found: $USER_PATH"
  if [[ -d "$USER_PATH/.git" ]]; then
    echo "Git repository detected."
  else
    echo "Warning: Not a git repository. Sync will not be available."
  fi
else
  echo "Warning: Directory not found: $USER_PATH"
  echo "The path will be saved but the integration won't work until the directory exists."
fi
```

Determine the location type: `git` if `.git/` exists, otherwise `directory`.

Set `TEAM_LOCATION=team-knowledge` — this is the key name Step 6 will write, and the name the template and `plugin/CLAUDE.md` already use. Leave `TEAM_LOCATION` unset for a solo setup.

#### Ask about local storage path (if team repo configured):

Use AskUserQuestion:

- header: "Local Path"
- question: "What path should be used for local artifact storage?"
- options:
  - ".claude (Recommended)" / "Default location — artifacts stored in .claude/ within your project"
  - ".claude-data" / "Alternative location — keeps .claude/ for config only"
- multiSelect: false

The user can type a custom path via the built-in "Other" option. Store the selected value as `LOCAL_PATH`.

#### Ask about requirements behavior flags (if team repo configured):

Use AskUserQuestion:
- header: "Requirements Behavior"
- question: "Configure requirements behavior? (defaults are recommended for most projects)"
- options:
  - "Use defaults" / "auto_search: true, auto_archive: true, auto_load_threshold: 0.9, max_suggestions: 3, archive_on_pr: true"
  - "Customize" / "I want to change the default values"
- multiSelect: false

If "Customize", ask about each flag individually. If "Use defaults", use:
- `auto_archive`: true
- `auto_search`: true
- `auto_load_threshold`: 0.9
- `max_suggestions`: 3
- `archive_on_pr`: true

### Step 5b: Ask About Jira Integration

Runs regardless of whether a team repo was configured in Step 4/5.

Use AskUserQuestion:
- header: "Jira"
- question: "Does this project use Jira (via the `acli` CLI) for ticket tracking? Enabling this lets /jira and jira-aware features (like /create-requirements auto-seeding from a loaded ticket) run without asking each time."
- options:
  - "No" / "Skip Jira config — /jira remains available but untracked by this wizard"
  - "Yes" / "Enable Jira integration and run a quick acli check"
- multiSelect: false

**If "No"** — set `JIRA_ENABLED=""` (omit the `jira:` block entirely in Step 6; `jira.enabled` already defaults to `true` when absent, so this only means the wizard skips asking about write access — it does not disable `/jira`). Skip to Step 5c.

**If "Yes"** — run the check and report results before asking about write access:

```bash
ACLI_INSTALLED=false
ACLI_AUTHENTICATED=false
ACLI_AUTH_SITE=""

if command -v acli >/dev/null 2>&1; then
  ACLI_INSTALLED=true
  if AUTH_OUT=$(timeout 10 acli jira auth status 2>&1); then
    ACLI_AUTHENTICATED=true
    # Surface the site only, never the account/email line — matches the
    # precedent in plugin/shared/jira/lib.sh's jira_resolve_site (site
    # only, no account identity), and bounded to one match so a single
    # unexpectedly long line can't dump unbounded into the transcript.
    ACLI_AUTH_SITE=$(printf '%s\n' "$AUTH_OUT" | grep -oE '[A-Za-z0-9.-]+\.atlassian\.net' | head -1)
  fi
fi

echo "Jira integration check:"
if [[ "$ACLI_INSTALLED" == "true" ]]; then echo "  ✓ acli installed"; else echo "  ✗ acli not found on PATH"; fi
if [[ "$ACLI_AUTHENTICATED" == "true" ]]; then
  if [[ -n "$ACLI_AUTH_SITE" ]]; then
    echo "  ✓ authenticated (site: $ACLI_AUTH_SITE)"
  else
    echo "  ✓ authenticated"
  fi
elif [[ "$ACLI_INSTALLED" == "true" ]]; then
  echo "  ✗ not authenticated"
fi
```

If either check failed, show a one-line remediation hint but do **not** block on it — the flag records project *intent*, and acli may be installed/authenticated later by whoever runs this project next:
- Not installed: "Install from https://developer.atlassian.com/cloud/acli/guides/introduction/"
- Not authenticated: "Run: acli jira auth login"

Set `JIRA_ENABLED="true"`.

Then ask about write access:

Use AskUserQuestion:
- header: "Jira Writes"
- question: "Also enable /jira write operations (comment, transition, assign/unassign)? Each write still requires an explicit per-write confirmation."
- options:
  - "No — read-only (Recommended)" / "jira.write.enabled stays false; /jira can view tickets and comments only"
  - "Yes — enable writes" / "jira.write.enabled: true"
- multiSelect: false

Set `JIRA_WRITE_ENABLED` to `"true"` or `"false"` accordingly.

### Step 5c: Ask Where Tasks Live

**Always asked** — on every setup and every reconfigure, whatever was answered
above. Also reached from Step 10 (see 10.3) when a configuration has never
chosen. `/todo` and `/todo-work` keep tasks in a store, and this is the one
question that decides where it is.

Use AskUserQuestion:
- header: "Tasks"
- question: "Where should /todo keep this project's tasks?"
- options:
  - "In this repository (default)" / "Tasks go in .claude/tasks inside the project and travel with it. Adding a task changes a file in the repository, which then needs committing and pushing if that folder is tracked."
  - "Shared list in my home directory" / "One task list outside every repository, shared by every project set up this way. Adding a task never changes a repository file. Each task is tagged with its project; /todo list shows this project, /todo list --all shows every project."
- multiSelect: false

**If "In this repository":** set `TASKS_CHOICE=local`. Nothing else changes —
Step 6 maps `tasks` into the local location like every other artifact. Continue to Step 5d.

**If "Shared list in my home directory":** set `TASKS_CHOICE=global` and work
through 5c.1–5c.3. Nothing is written until Step 7b.

#### 5c.1 Where the shared list lives

Use AskUserQuestion:
- header: "Shared list"
- question: "Where should the shared list live? It must be outside every repository. It is saved in the configuration as ~/…, so for anyone else using this configuration it points into their own home directory, never yours."
- options:
  - "~/.nexus/tasks (Recommended)" / "A hidden folder in your home directory"
  - "Somewhere else" / "Type the path in the text field; a path inside your home directory is saved as ~/…"
- multiSelect: false

The chosen path never enters a shell command. Create an input directory:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op input-dir
```

It prints `{"ok":true,"input_dir":"..."}`; call that path `{input_dir}` for the
rest of this step and Step 7b. **Write** the path — `~/.nexus/tasks`, or exactly
what was typed — to `{input_dir}/path`. Then work out the form the configuration
will carry, the project name, and what this project already has:

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"

WIZ="{input_dir}"
case "$WIZ" in
  "$HOME"/.claude/tmp/tasks-input.*) : ;;
  *) echo "ERROR: not a task input directory: $WIZ" >&2; exit 1 ;;
esac

# The committed form: ~/… for a path in this user's home, never the expanded
# home path — that would send every teammate into this user's home directory.
RAW="$(cat "$WIZ/path")"
RAW="${RAW%/}"
COMMITTED="$(artifact_home_relative "$RAW")" || COMMITTED=""
if [ -z "$COMMITTED" ]; then
  echo "PATH_OK=false"
  echo "That path cannot be used: give an absolute path or one starting with ~/, with no .. and no shell metacharacters."
  exit 0
fi
LOCATION_PATH="${COMMITTED%/*}"
SUBDIR="${COMMITTED##*/}"
if [ -z "$LOCATION_PATH" ] || [ "$LOCATION_PATH" = "$COMMITTED" ] || [ -z "$SUBDIR" ]; then
  echo "PATH_OK=false"
  echo "Name a folder inside a directory (for example ~/.nexus/tasks), not a top-level or home directory itself."
  exit 0
fi
printf '%s' "$LOCATION_PATH" > "$WIZ/location"
printf '%s' "$SUBDIR" > "$WIZ/subdir"

# An old per-repository store somewhere other than .claude/tasks, recorded so
# Step 7b can offer it too. Only this directory's own configuration is asked:
# one found higher up belongs to a parent workspace, and its store is the whole
# workspace's, not this project's.
OLD_CUSTOM=none
if [ -n "${CONFIG:-}" ] && [ "$CONFIG" -ef "$PWD/.claude/configuration.yml" ]; then
  OLD="$(bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op resolve 2>/dev/null | jq -r 'select(.mode == "local") | .dir // empty' 2>/dev/null || true)"
  if [ -n "$OLD" ] && [ -d "$OLD" ] && ! [ "$OLD" -ef "$PWD/.claude/tasks" ]; then
    printf '%s' "$OLD" > "$WIZ/from"
    OLD_CUSTOM="$OLD"
  fi
fi

echo "PATH_OK=true"
echo "TASKS_LOCATION_PATH=$LOCATION_PATH"
echo "TASKS_SUBDIR=$SUBDIR"
echo "OLD_STORE_CUSTOM=$OLD_CUSTOM"
```

**If `PATH_OK=false`:** show the message and ask 5c.1 once more. A second
unusable path falls back to `TASKS_CHOICE=local`: say `Keeping tasks in the
repository — re-run /configuration-init to try another path.`

What this project already has — an old store, a TODO.md — is counted in Step
7b, once the shared list exists: counting now would read whatever configuration
the directory walk finds, which below a parent workspace is the parent's, not
this project's.

#### 5c.2 Project name

Not asked here. The task store decides the name itself — the main checkout's
folder name in a repository (the same from a subdirectory or a worktree), each
repository's own folder name below a parent workspace configuration — and
Step 7b shows the name it chose and offers to change it, once the shared list
exists and the store can say.

#### 5c.3 Show exactly what will be written

Print the block below with the values filled in. A project name, if one is set
in Step 7b, is added as `project.name`:

```yaml
storage:
  locations:
    home:
      type: directory
      path: "<TASKS_LOCATION_PATH printed above>"
  artifacts:
    tasks:
      location: home
      subdir: "<TASKS_SUBDIR printed above>"
      mode: global
```

Add: `~ stands for the home directory of whoever runs a task command — nothing
personal is written. The folder is created, private to you, when the file is
written.`

Use AskUserQuestion:
- header: "Confirm"
- question: "Write this into .claude/configuration.yml?"
- options:
  - "Write it" / "Tasks go to the shared list; the folder is created after the file is written"
  - "Keep tasks in the repository" / "Change nothing about tasks"
- multiSelect: false

On "Keep tasks in the repository", set `TASKS_CHOICE=local`.

Continue to Step 5d.

### Step 5d: Ask About Output Redaction

Setup and reconfigure only. When Step 5c was reached from Step 10 (migrate), skip
this step and Step 7c and go to Step 7b: migrate never adds or changes the
redaction setting, because an absent setting already means "on".

Use AskUserQuestion:
- header: "Redaction"
- question: "The nexus plugin hides secrets (API keys, passwords, tokens) and personal data (email addresses, phone numbers, bank and card numbers) in the output of every shell command, showing a placeholder instead of the value. Turning it off means the real values reach the conversation for every agent in this project, review panels included; it never covered the command text itself. Keep it on?"
- options:
  - "Keep redaction on (Recommended)" / "Nothing is written to switch it off. Which personal-data classes are hidden stays as configured, or at the defaults."
  - "Turn redaction off" / "Writes redaction.enabled: false. Shell output reaches agents unchanged, secrets included, and a warning shows on the first shell command of each session."
- multiSelect: false

Set `REDACTION_CHOICE=on` for the first answer and `REDACTION_CHOICE=off` for the
second. Nothing is written until Step 7c.

### Step 6: Build Configuration

If `LOCAL_PATH` was not set (e.g., user selected "Create new" in Step 5 and execution stopped), default it:

```bash
LOCAL_PATH="${LOCAL_PATH:-.claude}"
```

Build the YAML configuration using the `LOCAL_PATH` value. The `storage` section always includes a `local` location. If the user configured a team repo, add a `team-knowledge` location as well.

**Generate the artifact mappings from the template, never from a list written here.** A hardcoded list drifts the moment the template gains an artifact, and a config missing an artifact resolves it to a fallback path that is silently wrong whenever `LOCAL_PATH` is not the conventional `.claude` — which is the defect this step exists to stop producing:

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"
TEMPLATE=$(artifact_template_path) || TEMPLATE=""

# Bind TEAM_LOCATION HERE. Step 5 decided it, but that was a different shell,
# so nothing carries it into this block. Set it to team-knowledge if Step 4
# answered Yes, and to the empty string otherwise — an accidental empty value
# would silently remap every shared artifact to local.
TEAM_LOCATION=""          # or: TEAM_LOCATION="team-knowledge"
LOCAL_PATH="${LOCAL_PATH:-.claude}"   # likewise: whatever Step 4/5 selected

ARTIFACTS_YAML=""
if [[ -n "$TEMPLATE" ]]; then
  ARTIFACTS_YAML=$(artifact_wizard_yaml "$TEMPLATE" "$TEAM_LOCATION")
fi

# Gate on the OUTPUT, not on whether a template was found: a readable template
# with no storage.artifacts section yields an empty render, and writing that
# would emit `artifacts:` with nothing under it — the incomplete config this
# step exists to prevent.
if [[ -z "$ARTIFACTS_YAML" ]]; then
  echo "Template artifact list unavailable — use the built-in set below."
else
  # Print it: this block's stdout is what gets pasted under `artifacts:`.
  # A variable assignment alone would die with the block.
  printf '%s\n' "$ARTIFACTS_YAML"
fi
```

The block's stdout **is** the `artifacts:` mapping. Paste it verbatim where `${ARTIFACTS_YAML}` appears below; if the block printed the "unavailable" message instead, use the built-in set further down.

**Base config (always included):**

```yaml
# Simple format (string):
execution_mode: subagent  # or team

# Per-phase format (if selected in Step 3):
# execution_mode:
#   default: subagent
#   overrides:
#     requirements_deep_dive: team
#     qa_review: team

storage:
  locations:
    local:
      type: directory
      path: "${LOCAL_PATH}"  # quoted: a custom path may contain a space or start with a dash
  artifacts:
${ARTIFACTS_YAML}
```

**If team repo configured** — set `TEAM_LOCATION=team-knowledge` before rendering, and add the location. `team-knowledge` is the name the template, `plugin/CLAUDE.md`, and Step 5's own prompt all use; generating a different name here would mean the template's shared artifacts could never be matched against a config this wizard wrote:

```yaml
storage:
  locations:
    local:
      type: directory
      path: "${LOCAL_PATH}"  # quoted: a custom path may contain a space or start with a dash
    team-knowledge:
      type: git       # or directory
      path: /absolute/path/to/team-knowledge
  artifacts:
${ARTIFACTS_YAML}          # shared artifacts now carry location: team-knowledge
```

**If `$ARTIFACTS_YAML` came back empty** — no readable template, or a template with no artifact section — the wizard still produces a usable config; Step 2 states the template is optional and that contract holds. Fall back to this built-in set, which must stay in step with `plugin/templates/configuration.yml`:

```yaml
  artifacts:
    work:              { location: local, subdir: work }
    brainstorms:       { location: local, subdir: brainstorm }
    meetings:          { location: local, subdir: meetings }
    proposals:         { location: local, subdir: proposals }
    refactoring:       { location: local, subdir: work/refactoring-sessions }
    requirements:      { location: local, subdir: requirements }
    product-knowledge: { location: local, subdir: . }
    tasks:             { location: local, subdir: tasks }
    messages:          { location: local, subdir: messages }
```

**Add requirements behavior flags:**

```yaml
requirements:
  auto_archive: true
  auto_search: true
  auto_load_threshold: 0.9
  max_suggestions: 3
  archive_on_pr: true
```

**If `$JIRA_ENABLED == "true"` (Step 5b answered "Yes"), add:**

```yaml
jira:
  enabled: true
  write:
    enabled: ${JIRA_WRITE_ENABLED}   # true or false, from Step 5b
```

If Step 5b answered "No", omit the `jira:` block entirely — `jira.enabled` already defaults to `true` when absent, so omitting it changes nothing about whether `/jira` works, only that this wizard run didn't ask about write access.

### Step 7: Write Configuration and Create Directories

```bash
mkdir -p .claude
```

Write the built YAML to `.claude/configuration.yml` using the Write tool.

Then create a directory for every locally-stored artifact so skills don't encounter missing paths. Drive this from the config just written, not from the template: an artifact the user pointed at the team repo must not also get a stray local directory, and one the user relocated must get the directory they actually chose.

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"

# Read LOCAL_PATH back out of the file just written rather than relying on the
# wizard's variable: this is a new shell, so an unbound LOCAL_PATH would make
# every mkdir absolute — `mkdir -p -- /work`, `/meetings` — creating
# directories outside the project, or failing with EPERM and silently creating
# none.
LOCAL_PATH=$(yq -r 'select(document_index == 0) | .storage.locations.local.path // ".claude"' \
             ".claude/configuration.yml")
[[ -n "$LOCAL_PATH" && "$LOCAL_PATH" != "null" ]] || LOCAL_PATH=".claude"

# LOCAL_PATH is the one value here the user typed freely, and it prefixes every
# mkdir below. A config arriving with a cloned repo could carry an absolute or
# traversing path; fall back rather than create directories outside the project.
# A leading ~ is refused as well: the resolver reads `~/x` as $HOME/x, and
# mkdir here would make a literal `./~/x` — two readers, two directories. A
# location in the home directory is for the shared task list (Step 5c), not for
# the project's own local storage.
if [[ "$LOCAL_PATH" == /* || "$LOCAL_PATH" == *".."* || "$LOCAL_PATH" == "~"* ]]; then
  echo "Refusing storage path '${LOCAL_PATH}' — must be relative to the project, must not traverse, and must not start with ~. Using .claude." >&2
  LOCAL_PATH=".claude"
fi

while IFS= read -r subdir; do
  [[ -n "$subdir" ]] || continue
  mkdir -p -- "${LOCAL_PATH}/${subdir}"
done < <(artifact_local_dirs ".claude/configuration.yml")

# The configuration file itself always lives here, even when LOCAL_PATH differs.
mkdir -p .claude
```

`artifact_local_dirs` already skips artifacts pointing at any non-local location, and skips a `subdir` of `.` (the location root, which exists by definition).

### Step 7b: Put Tasks in the Shared List

Only when Step 5c ended with `TASKS_CHOICE=global`; otherwise go straight to
Step 7c. Step 7 wrote the file with
tasks inside the repository; this step switches them over, and puts the file
back exactly as Step 7 wrote it if anything fails — a configuration left in
global mode with no usable store would refuse every task command.

**1. Write the setting** — backed up first, then one verified write:

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"

WIZ="{input_dir}"
case "$WIZ" in
  "$HOME"/.claude/tmp/tasks-input.*) : ;;
  *) echo "ERROR: not a task input directory: $WIZ" >&2; exit 1 ;;
esac
CFG=".claude/configuration.yml"
if ! artifact_yq_preserves_comments; then
  artifact_yq_refusal_message "$CFG" >&2
  echo "APPLIED=false"
  exit 0
fi
TS="$(date +%Y%m%d-%H%M%S)"
artifact_backup_once "$CFG" "$TS" || { echo "APPLIED=false"; exit 0; }
printf '%s' "$CFG.bak-$TS" > "$WIZ/backup"
PROJECT=""
[ -f "$WIZ/project" ] && PROJECT="$(cat "$WIZ/project")"
if artifact_apply_tasks_global "$CFG" home "$(cat "$WIZ/location")" "$(cat "$WIZ/subdir")" "$PROJECT"; then
  echo "APPLIED=true"
else
  cp -p -- "$CFG.bak-$TS" "$CFG"
  echo "APPLIED=false"
fi
```

**If `APPLIED=false`:** the file is as Step 7 wrote it, with tasks in the
repository. Say so. The likely causes: a comment-stripping `yq` (the message
says), a project name outside letters, digits, dot, underscore and dash (ask
5c.2 again), or a `home` location already in the configuration with a different
path (rename that location, or choose its path). Skip to the cleanup in point 4.

**2. Create the store.** The store's own checks run here — outside every
repository, private to you, a directory of its own — and the folder is made
with mode 700 at every level:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op init-store
```

**On any non-zero exit,** show the message (it names what is wrong and the fix)
and put the configuration back:

```bash
WIZ="{input_dir}"
case "$WIZ" in
  "$HOME"/.claude/tmp/tasks-input.*) : ;;
  *) echo "ERROR: not a task input directory: $WIZ" >&2; exit 1 ;;
esac
BAK="$(cat "$WIZ/backup")"
case "$BAK" in
  .claude/configuration.yml.bak-*) cp -p -- "$BAK" .claude/configuration.yml && echo "RESTORED=true" ;;
  *) echo "RESTORED=false — restore .claude/configuration.yml from its .bak- copy by hand" ;;
esac
```

Then say `Tasks stay in the repository for now.` and skip to point 4 — except
when the message names `project.name` and `in_repository` would be true (a
folder name with a space, say, or a main checkout that cannot be confirmed):
then ask for a name as in point 2b first, and run `init-store` once more before
putting the configuration back.

**2b. Confirm the project name.** `init-store` prints `project` (the name the
store will tag tasks with), `in_repository` and `project_named`.

**If `in_repository` is false**, ask nothing: this configuration is not one
repository's. Say `Tasks added in this folder are tagged {project}; each
repository below it tags its tasks with its own folder name.`

**Otherwise** use AskUserQuestion:
- header: "Project name"
- question: "Tasks from this project are tagged {project} on the shared list. Keep that name?"
- options:
  - "Keep {project}" / "Nothing more is written — the name comes from the repository"
  - "Set a different name" / "Type it in the text field: letters, digits, dot, underscore and dash; it is saved as project.name"
- multiSelect: false

On "Set a different name", **Write** the name to `{input_dir}/project`, then:

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"

WIZ="{input_dir}"
case "$WIZ" in
  "$HOME"/.claude/tmp/tasks-input.*) : ;;
  *) echo "ERROR: not a task input directory: $WIZ" >&2; exit 1 ;;
esac
if artifact_apply_tasks_global ".claude/configuration.yml" home "$(cat "$WIZ/location")" "$(cat "$WIZ/subdir")" "$(cat "$WIZ/project")"; then
  echo "NAMED=true"
else
  echo "NAMED=false"
fi
```

On `NAMED=false` the name was not usable: say so and ask once more. On
`NAMED=true`, run the `init-store` call from point 2 again — it checks the name
and reports the new `project`.

**3. Offer to move what exists.** Now the shared list exists and the
configuration names this project, the task store can count what a move would
copy, by its own rules (archive wins, anything already imported skipped). When
5c printed an `OLD_STORE_CUSTOM` path, count that store:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op migrate-store --count --input "{input_dir}"
```

Otherwise count the project's `.claude/tasks`:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op migrate-store --count
```

Then this project's TODO.md:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op migrate --count
```

The first reports `copied` (open) and `archived` (done) for the project's old
`.claude/tasks`, or a `note` when there is none — or when the configuration sits
above several repositories, where that store belongs to the whole workspace. The
second reports `new` — the entries in this project's TODO.md not yet in the
store (`entries` is the total, `already_imported` the rest). When either count is above
zero, use AskUserQuestion:
- header: "Move tasks"
- question: "This project already has {copied} open and {archived} done tasks in its old store, and {new} entries in TODO.md not yet imported. Move them into the shared list now?"
- options:
  - "Move them" / "Copy every task and TODO.md entry into the shared list, tagged with this project. The old store and TODO.md are left exactly as they are."
  - "Later" / "Move nothing now; run /todo migrate whenever you like"
- multiSelect: false

On "Move them", the old store first — its tasks may include TODO.md entries
imported earlier, and the TODO.md import recognises those. With an
`OLD_STORE_CUSTOM` path (this call removes the input directory, so it runs last
of the calls that use it):

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op migrate-store --input "{input_dir}"
```

Otherwise:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op migrate-store
```

Only when `copied` or `archived` was above zero. Then, when `new` was above
zero:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op migrate
```

Report each the way `/todo migrate` does: copied, archived, already present,
and any note. Neither the old store nor TODO.md is changed.

**4. Clean up** the input directory, if it is still there:

```bash
WIZ="{input_dir}"
case "${WIZ#"$HOME"/.claude/tmp/tasks-input.}" in
  "$WIZ"|''|*[!A-Za-z0-9]*) exit 0 ;;
esac
[ -d "$WIZ" ] && [ ! -L "$WIZ" ] && rm -rf -- "$WIZ"
```

Continue to Step 7c — unless you came here from Step 10 (migrate), which stops
after this step.

### Step 7c: Write the Redaction Choice

Setup and reconfigure only; never from migrate. It runs on **both** answers: even
"Keep redaction on" has work to do, because Step 7 wrote the file from scratch and
the previous `redaction.pii` class settings must be put back.

Substitute `{prev_config}` with the path Step 1 printed after `PREV_CONFIG=`, or
leave it empty when Step 1 printed `none`, or printed nothing at all (a first setup never runs Step 1's save), and `{redaction_choice}`
with `REDACTION_CHOICE` from Step 5d.

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"
source "$NEXUS_SHARED/config/redaction.sh"

PREV='{prev_config}'
case "${PREV#.claude/configuration.yml.bak-}" in
  "$PREV"|*[!0-9-]*) PREV="" ;;
esac
CHOICE='{redaction_choice}'
case "$CHOICE" in
  on|off) : ;;
  *) CHOICE="on" ;;
esac

if nexus_redaction_write_block ".claude/configuration.yml" "$PREV" "$CHOICE"; then
  echo "REDACTION_WRITE=ok"
else
  echo "REDACTION_WRITE=failed"
fi
```

The writer appends one block built only from fixed words, re-reads it with the
resolver the hook uses, and moves it into place only if it reads back as
intended. On any failure the file is exactly as Step 7 wrote it.

On `REDACTION_WRITE=failed`, say so plainly and never report success for a choice
that was not written: "The redaction choice and the previous personal-data
settings were not written. Redaction is ON with the default classes." and, only when
`{prev_config}` is a path, add: "Your previous configuration is saved at {prev_config}."
Then continue to Step 8.

### Step 8: Show Summary

Build the artifact rows from the config just written, so the summary reports what was actually generated rather than what this document expects:

```bash
yq -r '
  .storage.artifacts // {} | to_entries | .[]
  | "  \(.key): \(.value.location) → \(.value.subdir)"
' ".claude/configuration.yml"
```

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Configuration Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: .claude/configuration.yml

EXECUTION MODE
────────────────────────────────────────────────
  default:              ${default_mode} (subagent|team)
  requirements_deep_dive: ${override_or_default}
  qa_review:            ${override_or_default}

STORAGE LOCATIONS
────────────────────────────────────────────────
  local:                ${LOCAL_PATH} (directory)
  team-knowledge:       ${path} (${type})   # if configured

ARTIFACTS
────────────────────────────────────────────────
  ${one row per artifact in the written config}

TASKS
────────────────────────────────────────────────
  where:     in this repository (.claude/tasks)          # TASKS_CHOICE=local
  where:     shared list at ${TASKS_LOCATION_PATH}/${TASKS_SUBDIR}   # global
  project:   ${project from init-store's output}                    # global
  moved in:  ${counts from Step 7b, or "nothing yet — run /todo migrate"}  # global

REDACTION
────────────────────────────────────────────────
  output redaction:     ${on | OFF for this project}     # from REDACTION_CHOICE and Step 7c's result
  personal-data classes: ${carried over from the previous configuration | defaults}

REQUIREMENTS BEHAVIOR
────────────────────────────────────────────────
  auto_search:          ${value}
  auto_archive:         ${value}
  auto_load_threshold:  ${value}
  max_suggestions:      ${value}
  archive_on_pr:        ${value}

JIRA                                                          # only if jira: was written (Step 5b)
────────────────────────────────────────────────
  enabled:               ${value}
  write.enabled:          ${value}
  acli:                   ${installed/authenticated summary from Step 5b's check, or "not re-checked"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Skills and agents will now use this configuration.

To modify later, edit .claude/configuration.yml directly
or re-run /configuration-init.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 9: Validate Configuration

**Triggered by:** "Validate" option in Step 1, or `$ARGUMENTS` containing "validate".

Step 0 routes `validate` straight here, skipping Step 1 — so neither the shared
libraries nor `$EXISTING_CONFIG` exist on that path, and check 4b below would
have nothing to compare. Set both up first. This block asks nothing, so Step 0's
"no interactive wizard" contract holds; routing through Step 1 instead would
not, because Step 1 ends in an `AskUserQuestion` whenever an existing config is
found, which is exactly the case `validate` runs in.

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"
TEMPLATE=$(artifact_template_path) || TEMPLATE=""

# resolve-config.sh sets CONFIG by walking up from CWD. Step 1 normally copies
# it into EXISTING_CONFIG, and validate skips Step 1 — without this line every
# check below would read an empty path and silently report nothing.
EXISTING_CONFIG="$CONFIG"
if [[ -z "$EXISTING_CONFIG" || ! -f "$EXISTING_CONFIG" ]]; then
  echo "No configuration file found to validate. Run /configuration-init to create one." >&2
  exit 1
fi
```

Read `$EXISTING_CONFIG` and run validation checks. Report results using pass/warn/fail format.

**Validation checks:**

```
1. YAML Syntax
   → Parse the file. If invalid YAML → FAIL with parse error location.

2. execution_mode
   → If string: must be "subagent" or "team" → else FAIL
   → If object: must have "default" key with value "subagent" or "team"
   → If object with "overrides": each key must be a known phase name
     Known phases: requirements_deep_dive, qa_review, documentation_update, refactor, troubleshoot, pr_review, review_plan
     Unknown phase name → WARN ("unknown phase: {name}, will be ignored by skills")

3. storage.locations
   → Each location must have "type" and "path"
   → "type" must be "git" or "directory" → else FAIL
   → "path": check if directory exists → if not, WARN ("path does not exist: {path}")
   → If type is "git": check if path contains .git/ → if not, WARN ("not a git repository: {path}")

3b. storage.locations legacy names
   → For each `location-rename:{config}:{old}:{new}` entry from:
       artifact_plan_location_rename "$EXISTING_CONFIG"
     WARN ("legacy location name '{old}' — the current template calls this
     '{new}'; run /configuration-init migrate to rename it")
   → Print any warning the planner wrote to stderr as-is: a config defining
     BOTH names cannot be renamed automatically and the user has to reconcile
     it by hand.
   → Nothing else reports this. A legacy name is internally consistent, so
     every other check passes — the config only breaks later, when the template
     gains an artifact in the canonical location and that artifact can never be
     backfilled.

4. storage.artifacts
   → An artifact whose value is null (`name: ~`) is left out on purpose →
     PASS ("{name}: not configured, by choice") and skip it in every other
     check in 4, 4b and 4c. It resolves exactly like an absent artifact, but
     migrate never backfills it and 4b never reports it — the only way a
     project can say "this template artifact does not apply here" and have
     it stay said.
   → Each other artifact must have "location" and "subdir"
   → "location" must reference a key defined in storage.locations → else FAIL ("artifact '{name}' references undefined location '{loc}'")
   → Known artifact names: read at runtime with
       artifact_template_keys "$TEMPLATE"
     Never list them here — a list in this document is what drifted from the
     template in the first place.
   → Unknown artifact name → WARN ("unknown artifact: {name}")
   → If $TEMPLATE is empty, skip the known-name comparison and say so; every
     other check in this section still runs.

4b. storage.artifacts completeness
   → For each name from:
       artifact_missing_names "$EXISTING_CONFIG" "$TEMPLATE"
     WARN ("missing artifact: {name} — defined in the current template but
     absent from this config; run /configuration-init migrate to add it")
   → A missing artifact is not a syntax error, so no other check reports
     it: resolution silently falls back to a guessed path, and that guess
     is wrong whenever the local base is not the conventional one, or the
     artifact belongs in a shared location.
   → If $TEMPLATE is empty, skip this check with an explanatory line.

4c. storage.artifacts resolution
   → For each configured artifact, resolve it and ask what the resolved path
     actually IS. Checks 3 and 4 do not cover this: 3 tests the LOCATION's base
     path and 4 tests that the location is defined, so an artifact whose base
     exists and whose location is valid passes both while resolving to nothing.
   → Resolve with:
       resolve_artifact_strict "{name}" "{default_subdir_for_that_artifact}"
     and split the "PATH|TYPE" result on `|`. Use the STRICT resolver: the
     advisory one fabricates a path for an unconfigured artifact, which would
     turn "not configured" into a fake finding about a directory nobody named.
   → The default subdir is the artifact's OWN default, read from the template,
     never assumed to equal the artifact name. They differ for at least one
     shipped artifact, whose default subdir is `.`; substituting the name there
     resolves a config that omits `subdir` to a nested path the runtime gate
     never looks at. A validator reporting on a different path from the one the
     pipeline actually uses is worse than one reporting nothing.
   → Resolved path does not exist → WARN ("artifact '{name}' resolves to {path},
     which does not exist — the agent that reads it will be dispatched to search
     nothing, and an empty result is indistinguishable from a real one")
   → Resolved path IS, or CONTAINS, the directory holding configuration.yml →
     FAIL ("artifact '{name}' resolves to {path}, which is the configuration
     directory — an agent told to read a knowledge base there gets
     settings.json, session-state/ and worktrees/ instead"). Do not write the
     comparison yourself. Source the shared check in the same Bash call that
     asks it, and use its status:

       source "${CLAUDE_PLUGIN_ROOT}/shared/artifact-containment.sh"
       nexus_path_holds_config_dir "$path" "$CONFIG"   # 0 = is or contains it

     (`~/.claude/shared/artifact-containment.sh` for local/dev copies.) It is the
     same function /create-requirements' optional-agent gate uses, so the two
     cannot disagree. The comparison has been written wrong twice before — a
     resolved path of "/" slipped past an unstripped trailing slash, and an
     inline `"${path%/}"/*` pattern silently never matched — and the helper's
     header records both.
   → This is a FAIL and the missing-directory case is only a WARN, deliberately.
     A path that does not exist yet is a project that has not created it;
     a path that swallows the configuration directory is always wrong and puts
     session state in front of an agent.

2b. execution_mode team runtime
   → If the resolved mode for any phase is "team", check whether the team
     runtime is actually switched on:
       [ -n "${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-}" ]
   → Unset → WARN ("execution_mode requests team mode, but
     CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS is not set in this environment;
     skills will run these phases as plain subagents"). Report it, do not fail:
     a config written for a machine that has it on is not wrong on a machine
     that does not.
   → Nothing else reports this. A config asking for team mode on a runtime that
     cannot provide it degrades silently, so the user believes they are getting
     cross-pollination they are not.

7. legacy configuration.json alongside configuration.yml
   → If `.claude/configuration.json` exists next to the `.yml` → WARN
     ("orphaned .claude/configuration.json — nothing reads it (resolve-config.sh
     looks only for configuration.yml) and it holds a conflicting older schema;
     run /configuration-init migrate to back it up and remove it")
   → It cannot affect behaviour, which is exactly why it survives: every other
     check passes and the file stays as the thing a human opens to learn how the
     project is configured.

5. requirements section (if present)
   → auto_archive: must be boolean → else WARN
   → auto_search: must be boolean → else WARN
   → auto_load_threshold: must be number between 0 and 1 → else WARN
   → max_suggestions: must be positive integer → else WARN
   → archive_on_pr: must be boolean → else WARN

6. jira section (if present)
   → enabled: must be boolean → else WARN
   → write.enabled: must be boolean → else WARN
   → If enabled == false AND write.enabled == true → WARN ("jira.enabled is
     false, so jira.write.enabled: true has no effect — both jira.sh and
     jira-write.sh refuse the master switch before checking write access")

6b. jira flags against reality
   → If jira.enabled is true (or absent — it is opt-out, so absent means on),
     check the tool the flag promises is actually usable:
       command -v acli >/dev/null 2>&1
     Not installed → WARN ("jira.enabled is on but acli is not installed;
     every Jira read will fail at the point of use")
   → If acli IS installed, check authentication the same way the setup wizard
     does. Not authenticated → WARN ("acli is installed but not authenticated").
   → Report, never fail: a config shared across a team is legitimately valid on
     a machine where the current user has not logged in yet. The point is that
     the failure surfaces here rather than mid-pipeline.

8. tasks location (CL-122)
   → Run the task store's own resolution, which reads and creates nothing:
       bash "${CLAUDE_PLUGIN_ROOT}/shared/tasks/tasks.sh" --op resolve
     Success → PASS ("tasks: {mode}, {dir}" — plus ", project {project}" in
     global mode). A refusal → FAIL with the script's message unchanged: in
     global mode it names what is wrong with the shared list's directory
     (missing, inside a repository, writable by others) and the fix.
   → No `mode` key on storage.artifacts.tasks → PASS ("tasks: in this
     repository") and suggest re-running /configuration-init to choose.
   → For each line `artifact_home_absolute_locations "$EXISTING_CONFIG"`
     prints (name|path|suggested): WARN ("storage.locations.{name}.path is
     {path}, inside your home directory — everyone who uses this configuration
     would be sent there; write it as {suggested}")

9. redaction (CL-122)
   → The ON/OFF verdict comes from the hook's own resolver and from nothing
     else. Do not read `redaction.enabled` with yq or your own idea of YAML:
     `redaction: {enabled: false}`, `enabled: False` and a quoted "false" are
     false to a YAML parser and ignored by the hook, so a verdict from yq
     would describe a project the hook is not protecting the way it says.
       NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
       [ -f "$NEXUS_SHARED/pii-patterns.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
       source "$NEXUS_SHARED/pii-patterns.sh" || echo "UNKNOWN"
       nexus_redaction_output_mode "$EXISTING_CONFIG"
     If the source failed or the call printed nothing, report "redaction:
     could not be checked" and give no verdict — silence is not "on".
   → `off` → WARN ("output redaction is OFF for this project — shell output
     reaches every agent unchanged, secrets included, and a warning shows on
     the first shell command of each session. If this file is committed, it is off for everyone who
     uses the project")
   → `on`: also run `nexus_redaction_config_enabled "$EXISTING_CONFIG"`, the
     same parser, and this command, which lists only what sits INSIDE the
     top-level `redaction:` block (an `enabled:` under `jira:` is not it):
         awk '/^redaction:/ {b=1; if ($(0) ~ /^redaction:[[:space:]]*[^[:space:]#]/) print "shorthand: " $(0); next} /^[^[:space:]#]/ {b=0} b && /^[[:space:]]+enabled:/ {print "enabled: " $(0)}' "$EXISTING_CONFIG"
     Then, in this order:
       - the parser printed `false` → WARN ("redaction.enabled: false is set but
         ignored, because the file is world-writable or not owned by the user
         running the check, so redaction is on")
       - the parser printed `true` → PASS ("redaction: on, set explicitly")
       - the command printed anything else (the one-line `redaction: false`, the
         flow form `redaction: {enabled: false}`, an `enabled:` that is not
         `true`/`false` after a space, or more than one `enabled:` / `redaction:`)
         → WARN ("redaction.enabled is present but not usable — it needs to be
         the plain boolean false, written once — so it is ignored and redaction is on")
       - the command printed nothing → PASS ("redaction: on (default)"), also when
         the block holds only `pii:` settings
```

**Output format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Configuration Validation: {config_path}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [PASS] YAML syntax valid
  [PASS] execution_mode: "subagent"
  [PASS] storage.locations.local: type=directory, path=.claude (exists)
  [WARN] storage.locations.team-knowledge: path /home/user/code/team-knowledge does not exist
  [WARN] storage.locations: legacy location name "team-repo" — the current
         template calls this "team-knowledge"; run /configuration-init migrate
         to rename it
  [PASS] storage.artifacts: all ${count} artifacts reference valid locations
  [FAIL] storage.artifacts.proposals: references undefined location "shared"
  [WARN] storage.artifacts: missing artifact "meetings" — defined in the current
         template but absent from this config; run /configuration-init migrate to add it
  [WARN] storage.artifacts.{name} resolves to {path}, which does not exist — the
         agent that reads it will be dispatched to search nothing, and an empty
         result is indistinguishable from a real one
  [FAIL] storage.artifacts.{name} resolves to {path}, which is the configuration
         directory — an agent told to read a knowledge base there gets
         settings.json, session-state/ and worktrees/ instead
  [WARN] execution_mode requests team mode, but CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
         is not set in this environment; these phases will run as plain subagents
  [WARN] orphaned .claude/configuration.json — nothing reads it; run
         /configuration-init migrate to back it up and remove it
  [PASS] requirements: all values valid
  [PASS] jira: enabled, acli installed and authenticated
  [WARN] redaction: output redaction is OFF for this project

  Result: 6 passed, 5 warnings, 2 failures

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If any FAIL results exist, suggest fixes. If only WARN or PASS, report "Configuration is valid."

---

### Step 10: Migrate Legacy Formats

**Triggered by:** `$ARGUMENTS` containing "migrate".

Scan the project for legacy configuration and state file formats left over from past breaking changes and rewrite them in place. All rewrites create a `.bak-YYYYMMDD-HHMMSS` copy beside the original so nothing is destroyed.

**Five migrations are checked:**

1. `configuration.json` → `configuration.yml` (JSON to YAML)
2. `*-state.json` (per-skill state files) → unified `state.json` with `type` field
3. `domain_knowledge` configuration key → `product_knowledge`
4. superseded `storage.locations` names → the names the current template uses
5. artifacts the current template defines but the config is missing

**4 must be planned and applied before 5.** An artifact is only backfillable
when its location exists in the target config, so a config still on a legacy
location name has every artifact in that location skipped. Renaming first is
what lets both land in one run; the alternative is telling the user a migration
succeeded and then having `validate` immediately name the same remedy again.

#### 10.1 Plan phase (dry run — no writes)

Step 0 routes `migrate` straight here, skipping Step 1, so nothing has sourced
the shared libraries on this path. `resolve_artifact` below is called with
stderr silenced and a hardcoded fallback, which means an undefined function
looks like a successful default — a project with a customized work location
would be migrated against the wrong directory. Load the libraries first. As in
Step 9, this block asks nothing, so the "no interactive wizard" contract holds.

The preamble and the plan build must be **one** block: `TIMESTAMP` and `PLAN` are shell state, and a separate block would start a fresh shell without them.

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"
TEMPLATE=$(artifact_template_path) || TEMPLATE=""

TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
PROJECT_ROOT=$(pwd)
PLAN=()

# 1. configuration.json — convert it, or retire it when a .yml already exists.
# Both files present is a common shape: it is what you get whenever someone
# hand-writes the .yml.
#
# An orphan is worse than no file. Nothing reads it — resolve-config.sh looks
# only for configuration.yml — so it cannot affect behaviour, but it holds a
# conflicting older schema (`paths`, `product_knowledge.repository`) and it is
# the file a human opens to find out how the project is configured.
if [[ -f ".claude/configuration.json" ]]; then
  if [[ -f ".claude/configuration.yml" ]]; then
    PLAN+=("config-json-orphan:.claude/configuration.json")
  else
    PLAN+=("config-json-to-yml:.claude/configuration.json")
  fi
fi

# 2. Per-skill state files → state.json
LEGACY_STATE_NAMES=(
  "brainstorm-state.json:brainstorm"
  "requirements-state.json:requirements"
  "proposal-state.json:proposal"
  "implementation-state.json:implementation"
  "epic-state.json:epic"
)

# The preamble above defines resolve_artifact, so call it the way every other
# skill does, with no stderr silencing and no hardcoded fallback:
# resolve_artifact already falls back on its own.
WORK_DIR=$(resolve_artifact work work)
for dir in "$WORK_DIR"/*/; do
  [[ -d "$dir" ]] || continue
  for pair in "${LEGACY_STATE_NAMES[@]}"; do
    old_name="${pair%:*}"
    type_field="${pair#*:}"
    if [[ -f "${dir}${old_name}" && ! -f "${dir}state.json" ]]; then
      PLAN+=("state-rename:${dir}${old_name}:${type_field}")
    fi
  done
done

# 3. domain_knowledge key in configuration.yml
if [[ -f ".claude/configuration.yml" ]] && grep -q '^[[:space:]]*domain_knowledge:' ".claude/configuration.yml"; then
  PLAN+=("rename-key:.claude/configuration.yml:domain_knowledge:product_knowledge")
fi

# 4. Superseded storage.locations names.
# Planned before the backfill below, and PENDING_LOCS carries the canonical
# names forward so step 5 can see the locations this rename is about to create.
PENDING_LOCS=()
if [[ -f ".claude/configuration.yml" ]]; then
  while IFS= read -r entry; do
    [[ -n "$entry" ]] || continue
    PLAN+=("$entry")
    PENDING_LOCS+=("${entry##*:}")
  done < <(artifact_plan_location_rename ".claude/configuration.yml")
fi

# 5. Artifacts the template defines but this config is missing.
# artifact_plan_backfill skips anything already present (whatever it maps to)
# and skips anything whose location is undefined here, warning on stderr rather
# than writing a reference that would then fail validation. PENDING_LOCS is the
# exception: those locations do not exist yet but will, because the renames
# above are applied first.
if [[ -f ".claude/configuration.yml" && -n "$TEMPLATE" ]]; then
  while IFS= read -r entry; do
    [[ -n "$entry" ]] && PLAN+=("$entry")
  done < <(artifact_plan_backfill ".claude/configuration.yml" "$TEMPLATE" \
             ${PENDING_LOCS[@]+"${PENDING_LOCS[@]}"})
elif [[ -f ".claude/configuration.yml" ]]; then
  echo "ℹ Template not readable — skipping the missing-artifact check. Other migrations still run."
fi
```

`${PENDING_LOCS[@]+"${PENDING_LOCS[@]}"}` rather than a bare `"${PENDING_LOCS[@]}"`: an empty array expands to an unbound-variable error under `set -u`, which most configs — the ones needing no rename — would hit.

**Report the plan to the user:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Migration Plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Legacy config file  .claude/configuration.json → .claude/configuration.yml
  Orphaned config     .claude/configuration.json → removed (a .yml already exists; nothing reads the .json)
  Legacy state file   .claude/work/JIRA-123/requirements-state.json → state.json (type: requirements)
  Legacy config key   .claude/configuration.yml: domain_knowledge → product_knowledge
  Legacy location     .claude/configuration.yml: team-repo → team-knowledge
                      (and every artifact that referenced it)
  Missing artifact    .claude/configuration.yml: + meetings (local → meetings)

  Backups will be written as *.bak-${TIMESTAMP}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

List the entries in `PLAN` order. That order is the apply order, and a rename shown after the backfill it enables would misdescribe what is about to happen.

Print any warnings `artifact_plan_location_rename` or `artifact_plan_backfill` wrote to stderr above this box — an artifact skipped because its location is undefined, or a rename skipped because both names are already defined, is something the user may want to act on.

When the plan includes a `.yml` rewrite, add:

```
  Note: yq normalizes inline mappings and blank lines on untouched lines.
  Comments are preserved; the reformatting is cosmetic.
```

If `PLAN` is empty, report:

```
✓ No legacy formats detected. Nothing to migrate.
```

…and exit.

Use `AskUserQuestion`:
- header: "Apply migration?"
- question: "Apply the planned migrations? Each original file is backed up before rewrite."
- options:
  - "Apply" / "Run the migrations"
  - "Cancel" / "Exit without changes"

If "Cancel" → stop with: "Migration cancelled. No files were modified."

#### 10.2 Apply phase

For each planned action, create the backup, then rewrite.

This phase runs in a fresh shell, and the `AskUserQuestion` gate sits between it and Step 10.1 — so it cannot share a block with the plan, and nothing survives from it. Start every apply block with the **Library Preamble**, then re-establish the two pieces of state it needs:

- **`TIMESTAMP`** — set it to the *literal string already printed in the plan*, e.g. `TIMESTAMP=20260423-160500`. Do **not** re-run `date`: a fresh value would put backups at a suffix other than the one the user was shown, and the confirmation lines would name files that do not exist.
- **`PLAN`** — re-derive it by re-running the Step 10.1 detection, or carry the confirmed entries forward literally. It must match what the user approved; if re-derivation produces a different set, stop and re-plan rather than applying a plan nobody confirmed.

**Always back up through `artifact_backup_once`, never a bare `cp`, and always check its return value.** The run computes one `TIMESTAMP` and every verb writes `<file>.bak-${TIMESTAMP}`. Several verbs can target `configuration.yml` in the same run, and a second plain `cp` would overwrite the first verb's backup with the already-rewritten intermediate, leaving no copy of the original. `artifact_backup_once` keeps the earliest copy, which is why every verb uses it. It returns non-zero when it could not produce a real backup (the path is a symlink, a directory, or `cp` failed); proceeding past that would rewrite a file whose only "backup" does not exist.

**Check the YAML tooling once, before any verb runs.** `rename-key`, `location-rename`, and `artifact-backfill` all rewrite `configuration.yml` with `yq -i`. Gating only one of them would still let the others strip every comment in the same run.

Run this whenever the confirmed plan contains **any** verb that writes a `.yml` file — that is `config-json-to-yml`, `rename-key`, `location-rename`, or `artifact-backfill`. Decide that from the plan you showed the user; do not branch on a `PLAN` array, which does not exist in this shell:

```bash
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/resolve-config.sh"
source "$NEXUS_SHARED/config/artifacts.sh"
TEMPLATE=$(artifact_template_path) || TEMPLATE=""
TIMESTAMP=<the literal timestamp printed in the plan>

if ! artifact_yq_preserves_comments; then
  artifact_yq_refusal_message ".claude/configuration.yml" >&2
  exit 1
fi
```

**config-json-to-yml** (uses `yq` to convert JSON to YAML):
```bash
# artifact_backup_once lives in config/artifacts.sh, and a shell FUNCTION does
# not survive a Bash tool-call boundary any better than a variable does. Sourced
# here, in the call that uses it, or the call dies with "command not found".
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/config/artifacts.sh"
# The literal already printed in the plan — NOT a fresh `date`. A new value
# would put backups at a suffix the user never saw.
TIMESTAMP=<the literal timestamp printed in the plan>
artifact_backup_once ".claude/configuration.json" "${TIMESTAMP}" || exit 1
yq -P '.' ".claude/configuration.json" > ".claude/configuration.yml"
# Only remove original after successful YAML write
if [[ -s ".claude/configuration.yml" ]]; then
  rm ".claude/configuration.json"
fi
```

**config-json-orphan** (a `.yml` already exists; back the `.json` up and remove it). The `.yml` is authoritative because it is the only one anything reads — `resolve-config.sh` walks up looking for `configuration.yml` and never for the `.json`:
```bash
# artifact_backup_once lives in config/artifacts.sh, and a shell FUNCTION does
# not survive a Bash tool-call boundary any better than a variable does. Sourced
# here, in the call that uses it, or the call dies with "command not found".
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/config/artifacts.sh"
# The literal already printed in the plan — NOT a fresh `date`. A new value
# would put backups at a suffix the user never saw.
TIMESTAMP=<the literal timestamp printed in the plan>
artifact_backup_once ".claude/configuration.json" "${TIMESTAMP}" || exit 1
# Only after the backup exists. Removing first and failing to back up would
# destroy the only copy of a file the operator may still want to read.
if [[ -f ".claude/configuration.json.bak-${TIMESTAMP}" ]]; then
  rm ".claude/configuration.json"
fi
```

Nothing is merged into the `.yml`. Folding stale values from an unread file into a live configuration would change behaviour the operator never asked for, and the two schemas are not comparable field by field anyway — the old form spells it `paths.work` where the current one spells it `storage.artifacts.work`, so a mechanical diff produces noise rather than a finding. Report the backup path instead and let the operator read it:

```
  Orphaned .claude/configuration.json removed (nothing read it).
  Backup: .claude/configuration.json.bak-${TIMESTAMP}
  Its values were NOT merged — .claude/configuration.yml is unchanged.
```

**state-rename** (add `type` field, rename file). Plan entries are `state-rename:<path-to-old-file>:<type>`, so bind all three variables first — with the backup now checked, leaving `old_path` unset aborts the migration rather than silently doing nothing:
```bash
# artifact_backup_once lives in config/artifacts.sh, and a shell FUNCTION does
# not survive a Bash tool-call boundary any better than a variable does. Sourced
# here, in the call that uses it, or the call dies with "command not found".
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/config/artifacts.sh"
umask 077
mkdir -p -m 700 "$HOME/.claude/tmp" && chmod 700 "$HOME/.claude/tmp"
set -C   # refuse to write through a pre-planted symlink
# The literal already printed in the plan — NOT a fresh `date`. A new value
# would put backups at a suffix the user never saw.
TIMESTAMP=<the literal timestamp printed in the plan>
# The plan entry is text this skill printed and you substitute back. It goes
# through a QUOTED heredoc, not straight onto a command line: the entry holds
# user-configured paths, and a quote or $( ) in one would break out. It also
# binds `entry` in the same call that reads it.
cat > "$HOME/.claude/tmp/config-init-entry.$$.txt" <<'PLAN_ENTRY_EOF' || exit 1
{plan_entry}
PLAN_ENTRY_EOF
set +C
entry="$(cat "$HOME/.claude/tmp/config-init-entry.$$.txt")"
rm -f "$HOME/.claude/tmp/config-init-entry.$$.txt"
[ -n "$entry" ] || exit 1
# e.g. state-rename:.claude/work/X/requirements-state.json:requirements
type_field="${entry##*:}"
old_path="${entry#state-rename:}"; old_path="${old_path%:*}"
dir="$(dirname "$old_path")/"

if [[ -s "${dir}state.json" ]]; then
  echo "⚠ Skipping ${old_path} — ${dir}state.json already written by an earlier migration in this directory."
  # `exit 0`, not `continue`: each plan entry is its own Bash tool call, so
  # there is no loop to continue. Bash warned and fell through, and the jq
  # write and `rm` below then ran against the very file this branch had just
  # said it would not touch.
  exit 0
fi
artifact_backup_once "${old_path}" "${TIMESTAMP}" || exit 1
jq --arg t "${type_field}" '. + {type: $t}' "${old_path}" > "${dir}state.json"
if [[ -s "${dir}state.json" ]]; then
  rm "${old_path}"
fi
```

**rename-key** (update a top-level YAML key, preserve structure):
```bash
# artifact_backup_once lives in config/artifacts.sh, and a shell FUNCTION does
# not survive a Bash tool-call boundary any better than a variable does. Sourced
# here, in the call that uses it, or the call dies with "command not found".
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/config/artifacts.sh"
# The literal already printed in the plan — NOT a fresh `date`. A new value
# would put backups at a suffix the user never saw.
TIMESTAMP=<the literal timestamp printed in the plan>
# Same as the plan entry above: a path this skill printed, bound here through a
# quoted heredoc rather than substituted onto the command line.
umask 077
mkdir -p -m 700 "$HOME/.claude/tmp" && chmod 700 "$HOME/.claude/tmp"
set -C   # refuse to write through a pre-planted symlink
cat > "$HOME/.claude/tmp/config-init-file.$$.txt" <<'PLAN_FILE_EOF' || exit 1
{plan_file}
PLAN_FILE_EOF
set +C
file="$(cat "$HOME/.claude/tmp/config-init-file.$$.txt")"
rm -f "$HOME/.claude/tmp/config-init-file.$$.txt"
[ -n "$file" ] || exit 1
artifact_backup_once "$file" "${TIMESTAMP}" || exit 1
yq -i '.product_knowledge = .domain_knowledge | del(.domain_knowledge)' "$file"
```

**location-rename** (rename a storage location and repoint every artifact that used it). Plan entries have the form `location-rename:<config-path>:<old>:<new>`. **Apply every one of these before any `artifact-backfill` entry** — a backfill whose location has not been renamed yet is skipped, and the run would report success while leaving the config exactly as drifted as it found it:
```bash
# artifact_backup_once lives in config/artifacts.sh, and a shell FUNCTION does
# not survive a Bash tool-call boundary any better than a variable does. Sourced
# here, in the call that uses it, or the call dies with "command not found".
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/config/artifacts.sh"
# The literal already printed in the plan — NOT a fresh `date`. A new value
# would put backups at a suffix the user never saw.
TIMESTAMP=<the literal timestamp printed in the plan>
# The plan entry is text this skill printed and you substitute back — a
# quoted heredoc, not a command line, because the entry holds
# user-configured paths. It also BINDS `entry` in the call that reads it.
umask 077
mkdir -p -m 700 "$HOME/.claude/tmp" && chmod 700 "$HOME/.claude/tmp"
set -C   # refuse to write through a pre-planted symlink
cat > "$HOME/.claude/tmp/config-init-entry.$$.txt" <<'PLAN_ENTRY_EOF' || exit 1
{plan_entry}
PLAN_ENTRY_EOF
set +C
entry="$(cat "$HOME/.claude/tmp/config-init-entry.$$.txt")"
rm -f "$HOME/.claude/tmp/config-init-entry.$$.txt"
[ -n "$entry" ] || exit 1
# e.g. location-rename:.claude/configuration.yml:team-repo:team-knowledge
new="${entry##*:}"
rest="${entry%:*}"; old="${rest##*:}"
file="${rest%:*}"; file="${file#location-rename:}"

artifact_backup_once "${file}" "${TIMESTAMP}" || exit 1
if ! artifact_apply_location_rename "${file}" "${old}" "${new}"; then
  echo "✗ Renaming location ${old} → ${new} failed. The original is at ${file}.bak-${TIMESTAMP}" >&2
  exit 1
fi
```

The rename and the artifact repointing are one write inside the library, so there is no state in which the config references a location that no longer exists. It refuses rather than guessing when the config already defines both names.

**artifact-backfill** (add one missing artifact using the template's mapping). Plan entries have the form `artifact-backfill:<config-path>:<artifact-name>`, so split on the last colon — an artifact name never contains one:
```bash
# artifact_backup_once lives in config/artifacts.sh — sourcing resolve-config.sh
# alone leaves it undefined in this call.
NEXUS_SHARED="${CLAUDE_PLUGIN_ROOT}/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || NEXUS_SHARED="$HOME/.claude/shared"
[ -f "$NEXUS_SHARED/config/artifacts.sh" ] || { echo "ERROR: nexus shared library not found — looked in ${CLAUDE_PLUGIN_ROOT}/shared and $HOME/.claude/shared; update or reinstall the plugin (/plugin update nexus@claude-skills) or check the plugin cache" >&2; exit 1; }
source "$NEXUS_SHARED/config/artifacts.sh"
# Re-derived here: shell state does not survive between Bash tool calls.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
TEMPLATE=$(artifact_template_path) || TEMPLATE=""
# The literal already printed in the plan — NOT a fresh `date`. A new value
# would put backups at a suffix the user never saw.
TIMESTAMP=<the literal timestamp printed in the plan>
# The plan entry is text this skill printed and you substitute back — a
# quoted heredoc, not a command line, because the entry holds
# user-configured paths. It also BINDS `entry` in the call that reads it.
umask 077
mkdir -p -m 700 "$HOME/.claude/tmp" && chmod 700 "$HOME/.claude/tmp"
set -C   # refuse to write through a pre-planted symlink
cat > "$HOME/.claude/tmp/config-init-entry.$$.txt" <<'PLAN_ENTRY_EOF' || exit 1
{plan_entry}
PLAN_ENTRY_EOF
set +C
entry="$(cat "$HOME/.claude/tmp/config-init-entry.$$.txt")"
rm -f "$HOME/.claude/tmp/config-init-entry.$$.txt"
[ -n "$entry" ] || exit 1
# e.g. artifact-backfill:.claude/configuration.yml:meetings
name="${entry##*:}"
file="${entry#artifact-backfill:}"; file="${file%:*}"

artifact_backup_once "${file}" "${TIMESTAMP}" || exit 1
if ! artifact_apply_backfill "${file}" "${TEMPLATE}" "${name}"; then
  echo "✗ Backfill of ${name} failed. The original is at ${file}.bak-${TIMESTAMP}" >&2
  exit 1
fi
```

After each action, print a single line confirmation:

```
✓ .claude/configuration.json → .claude/configuration.yml  (backup: .bak-20260423-160500)
✓ .claude/work/JIRA-123/requirements-state.json → state.json  (backup: .bak-20260423-160500)
✓ .claude/configuration.yml: domain_knowledge → product_knowledge  (backup: .bak-20260423-160500)
✓ .claude/configuration.yml: storage.locations.team-repo → team-knowledge, 3 artifacts repointed  (backup: .bak-20260423-160500)
✓ .claude/configuration.yml: + storage.artifacts.meetings  (backup: .bak-20260423-160500)
```

If any step fails, stop and report which action failed. The user can retry after resolving the issue.

#### 10.3 Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Migration Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Actions applied: {count}
  Locations renamed: {count}
  Artifacts backfilled: {count}
  Backups created: {count}   # at most one per file, holding its pre-run state

  Next step: run /configuration-init validate to confirm the
  rewritten configuration passes validation.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Where tasks live.** When the configuration has a `tasks` entry with no
`mode`, it has never chosen between the repository and a shared list. After the
summary, go to **Step 5c**, skip Step 5d and Step 7c, and then go to **Step 7b**
— the file already exists, so Step 7's write is skipped and Step 7b switches it
in place. Step 5c's first answer, "In this repository", changes nothing. Migrate
never asks about redaction and never writes the setting.

**Scope note:** This migration only handles known-historical format changes. Unknown legacy formats are left untouched — the user can file an issue if they encounter a case this skill misses.

---

## Examples

### Example 1: Minimal Setup (No Team Repo)

```bash
/configuration-init

# → Select execution mode: Sub-agent
# → Select: No team repository
# → Select local path: .claude (Recommended)
# → Writes local-only configuration.yml with path: .claude
```

### Example 2: Full Setup with Team Repo

```bash
/configuration-init

# → Select execution mode: Sub-agent
# → Select: Yes, configure team repository
# → Select repo path: /home/user/code/team-knowledge (default)
# → Select local path: .claude (Recommended)
# → Use default requirements behavior
# → Writes configuration.yml with team-knowledge location and shared artifacts
```

### Example 3: Custom Local Path

```bash
/configuration-init

# → Select execution mode: Sub-agent
# → Select: No team repository
# → Select local path: Other → type ".data"
# → Writes configuration.yml with path: .data
```

### Example 4: Validate Existing

```bash
/configuration-init

# → Shows current config
# → Select: Validate
# → Runs all checks, reports pass/warn/fail
# → Shows "Configuration is valid" or suggests fixes
```

### Example 5: Migrate Legacy Formats

```bash
/configuration-init migrate

# → Scans for legacy configuration.json, *-state.json, domain_knowledge key,
#   and artifacts the current template defines but this config is missing
# → Prints plan; no writes yet
# → Asks for confirmation (Apply / Cancel)
# → On Apply: creates .bak-TIMESTAMP copies, rewrites in place
# → Reports which migrations landed; suggests running validate next
```

### Example 6: Reconfigure Existing

```bash
/configuration-init

# → Shows current config
# → Select: Reconfigure
# → Walks through wizard again
# → Overwrites with new configuration
```

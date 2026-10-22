---
name: archive-requirements
model: claude-sonnet-5-5
category: requirements-kb
description: Manually archive completed requirements to team knowledge base
argument-hint: "[identifier]"
userInvocable: true
allowed-tools: Read, Bash, Task, AskUserQuestion
---

# Archive Requirements

Manually archive completed requirements to the team's requirements knowledge base.

## Purpose

Use this skill to archive requirements that weren't automatically archived during `/implement`, or to re-archive requirements after updates.

## When to Use

- Implementation completed but archival was skipped
- Archival failed during `/implement` and needs retry
- Requirements updated and need to be re-archived
- Manual archival for legacy work not tracked in `$WORK_DIR/`

## Arguments

```bash
/archive-requirements [identifier]
```

**identifier** (optional): Work identifier (e.g., JIRA-123)
- If provided: Archive that specific work
- If omitted: Scan `$WORK_DIR/` and present options

## Configuration

Read `.claude/configuration.yml` for project-specific paths. If the file doesn't exist or a key is missing, use defaults:

| Config Key | Default | Purpose |
|-----------|---------|---------|
| `storage.artifacts.work` | `location: local, subdir: work` | Work state and context |
| `storage.artifacts.requirements` | `location: local, subdir: requirements` | Requirements knowledge base (archive target) |

```bash
# Source resolve-config: marketplace installs get ${CLAUDE_PLUGIN_ROOT} substituted
# inline before bash runs; legacy local copies fall back to ~/.claude. If neither
# path resolves, fail loudly rather than letting resolve_artifact be undefined.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
WORK_DIR=$(resolve_artifact work work)
echo "WORK_DIR=$WORK_DIR"
```

Use `$WORK_DIR` instead of a hardcoded `.claude/work` — but only inside this block. Each later block is its own Bash tool call and does not inherit the variable, so those substitute the value printed above instead.

**Where these values come from.** Shell state does not survive between Bash tool
calls, so `REPO` is re-resolved in each block that uses it rather than carried
from the block above.

---

## Process

### Step 1: Identify Work to Archive

**If identifier provided:**
```bash
if [ ! -d "<WORK_DIR printed above>/{identifier}" ]; then
  echo "❌ Work directory not found: <WORK_DIR printed above>/{identifier}"
  echo ""
  echo "Available work:"
  ls -1 <WORK_DIR printed above>/
  exit 1
fi
```

**If no identifier provided:**

Scan for completed work:
```bash
# Find work directories with completed requirements
for dir in <WORK_DIR printed above>/*/; do
  identifier=$(basename "$dir")

  if [ -f "$dir/state.json" ]; then
    status=$(grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$dir/state.json" | cut -d'"' -f4)

    if [ "$status" = "completed" ]; then
      echo "[$identifier] - Ready to archive"
    fi
  fi
done
```

Use AskUserQuestion to present options:
```
Select work to archive:

[1] JIRA-123 - User Export Feature (completed 2 hours ago)
[2] JIRA-456 - SSO Integration (completed yesterday)
[3] PROJ-789 - API Refactor (completed last week)

Select [1-3]:
```

`AskUserQuestion` shows at most 4 options: offer the 4 most recently completed
and name the rest in the question text so the user can type one.

### Step 2: Validate Work State

Read state files — these are **Read tool calls, not shell**, so the fence is
untagged: `$WORK_DIR` and `${identifier}` here are values to substitute, not
variables a shell would expand. Tagged `bash` they read as a block using state
from an earlier call, which is neither what they are nor what they do.

```text
Read("<WORK_DIR>/<identifier>/state.json")
Read("<WORK_DIR>/<identifier>/context/")
```

**Check:**
- Requirements phase completed
- Implementation phase completed (if exists)
- Has context files (discovery, archaeologist, business-analyst, etc.)

**If incomplete:**
```
⚠ Warning: Work appears incomplete

Requirements: completed ✓
Implementation: in progress (2/3 chunks)

Archive anyway? [y/n]
```

### Step 3: Resolve Requirements Storage

Resolve the requirements artifact path using the config functions loaded in the Configuration section above.

**Use `resolve_artifact_strict`, never `resolve_artifact_typed`.** The typed
resolver is advisory: on an install that never configured a knowledge base it
fabricates `.claude/requirements` and returns it as though it were real, so the
"not configured" branch below could never fire and an archive would proceed
into a directory nobody set up. The strict resolver refuses instead, and it is
the same rule the archivist itself gates on — one rule, one answer.

```bash
if _RESOLVED=$(resolve_artifact_strict requirements requirements); then
  IFS='|' read -r REPO _TYPE <<< "$_RESOLVED"
  # No _BASE here on purpose. Nothing below needs the location root, and
  # `dirname "$REPO"` is not reliably it: with `subdir: .` the strict resolver
  # normalises REPO to the root already, so dirname would climb ABOVE the KB.
else
  REPO=""   # not configured — print the block below and stop
fi
```

If the storage location type is `git`, sync before reading:
```bash
# Re-derived here: shell state does not survive between Bash tool calls, so a
# value resolved in an earlier block is empty in this one.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
if _RESOLVED=$(resolve_artifact_strict requirements requirements); then
  IFS='|' read -r REPO _TYPE <<< "$_RESOLVED"
else
  REPO=""
fi
if [[ "$_TYPE" == "git" ]]; then
  # `cd "$REPO"`, not `cd "$_BASE"`: git pull operates on the containing
  # repository from any directory inside it, and dirname is not the location
  # root when subdir has more than one segment (or is ".", where the strict
  # resolver normalises REPO to the root itself and dirname would climb ABOVE
  # the KB). Same form the archivist's SEARCH sync uses.
  # The emptiness test is the guard; `cd … || exit 1` is not one on its own,
  # because `cd ""` returns 0 and stays put.
  [ -n "$REPO" ] || exit 1
  cd "$REPO" || exit 1
  git pull
fi
```

**If not configured** — `resolve_artifact_strict` exited non-zero, so `REPO` is
empty. Print this and stop; do not delegate to the archivist, and do not
proceed on a default path:

> A non-zero exit is not always "not configured". Exit `5` means a configured
> value would resolve outside its storage location — a broken config, not a
> missing one — and the resolver's stderr names the key. Surface that message
> rather than the setup instructions above, which would send the user to fix
> something that is already set.

```
Requirements storage not configured

To set up:
1. See: ${CLAUDE_PLUGIN_ROOT}/templates/requirements-repo/README.md (or ~/.claude/templates/requirements-repo/README.md for local/dev copies)
2. Add requirements artifact to .claude/configuration.yml:

storage:
  locations:
    team-knowledge:
      type: git
      path: /path/to/team-knowledge
  artifacts:
    requirements: { location: team-knowledge, subdir: requirements }

Cannot archive until configured.
```

### Step 4: Delegate to Archivist

Use Task tool with `subagent_type: "archivist"`:

```
Task(archivist, "Archive requirements for ${identifier}

Work directory: $WORK_DIR/${identifier}/
Configuration: ${requirements_config}

Tasks:
1. Sync requirements repository
2. Read all state and context files
3. Extract metadata from git commits and code changes
4. Copy the Spec-Driven triad verbatim into the archive — destination is `{repository_path}/${identifier}/`, the same directory every other reader (search-requirements, load-requirements, rebuild-requirements-index) expects; `rebuild-requirements-index` explicitly skips an `archive/` subdirectory, so anything written there is invisible to the index:
   - $WORK_DIR/${identifier}/spec.md             → {repository_path}/${identifier}/spec.md
   - $WORK_DIR/${identifier}/plan.md             → {repository_path}/${identifier}/plan.md
   - $WORK_DIR/${identifier}/tasks.md            → {repository_path}/${identifier}/tasks.md
   - $WORK_DIR/${identifier}/${identifier}-JIRA_TICKET.md → {repository_path}/${identifier}/${identifier}-JIRA_TICKET.md
   If the triad is absent (legacy work from pre-SDD runs), fall back to copying ${identifier}-TECHNICAL_REQUIREMENTS.md.
5. Generate a concatenated human-readable requirements.md in the archive by joining spec.md + plan.md + tasks.md under clearly marked section headers (## Spec / ## Plan / ## Tasks). This preserves KB search compatibility without duplicating authoring.
6. Copy all files to requirements repository (including context/ agent outputs)
7. Update searchable index.json — extract tags from spec.md user stories and plan.md sections
8. Commit — and push only if the KB is git-backed — by following **archivist's own Responsibility 3 STORE step 7**, which branches on the resolved storage type `_TYPE`. Do not reproduce the commit/push mechanics here: for a `directory`-type KB the archive must commit locally with NO push and NO `NEXUS_KB_WRITE=1` / `SECURITY_AUDITOR_BYPASS=1`, because that KB lives inside the host project's own repository and those variables would disable its branch protection and audit gate against its own trunk. The agent resolves `_TYPE` itself and owns both branches.

Provide detailed success report with archive location.
")
```

### Step 5: Report Results

**Success:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Requirements Archived Successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Identifier: ${identifier}
Title: ${feature_title}

Archived to: ${repo_path}/${identifier}/
- metadata.json (searchable)
- spec.md (WHAT / WHY — user stories + AC)
- plan.md (HOW — technical approach, risks, decisions)
- tasks.md (EXECUTE — AC-linked task list)
- ${identifier}-JIRA_TICKET.md (derived paste-ready view)
- requirements.md (concatenated view for KB search compatibility)
- state.json (session state)
- context/ (all agent outputs)

Index updated:
- Total tickets: 25 → 26
- Tags: ${extracted_tags}
- Components: ${extracted_components}

{If the archivist reported the git-backed branch:}
Changes committed and pushed to the requirements repository's default branch

{If it reported the directory branch — the default:}
Changes committed **locally** to this repository. Nothing was pushed: a
directory-type knowledge base lives inside this project, so the archive reaches
the team through your normal review-and-merge flow. An unmerged archive commit is
discarded if this branch is later abandoned.

This work is now discoverable by the archivist agent
when searching for similar past implementations.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Failure:**
```
❌ Archival Failed

Error: ${error_message}

Possible causes:
- Requirements repository not accessible
- Git conflicts in index.json
- Missing required context files
- Insufficient permissions

Troubleshooting:
1. Check repository path: ${repo_path}
2. Ensure repository is up to date: git pull
3. Verify context files exist in $WORK_DIR/${identifier}/context/
4. Check git status in requirements repository

Retry: /archive-requirements ${identifier}
```

## Examples

### Example 1: Archive Specific Work

```bash
/archive-requirements JIRA-123
```

Archives the completed work for JIRA-123.

### Example 2: Select from Available Work

```bash
/archive-requirements
```

Scans `$WORK_DIR/` and presents a list of completed work to choose from.

### Example 3: Re-archive After Updates

```bash
# After updating requirements
/archive-requirements JIRA-123

# Archivist will update existing archive
```

## Error Handling

### Work Not Found

```
❌ Work directory not found: $WORK_DIR/JIRA-123

Available work:
- JIRA-456
- PROJ-789
- AUTH-001

Did you mean one of these?
```

### Repository Not Configured

```
❌ Requirements repository not configured

Setup guide: ${CLAUDE_PLUGIN_ROOT}/templates/requirements-repo/README.md (or ~/.claude/templates/requirements-repo/README.md for local/dev copies)

Cannot proceed until configured.
```

### Incomplete Work

```
⚠ Work appears incomplete:
- Requirements: ✓ completed
- Implementation: ✗ not started

This will archive requirements only (no implementation).

Continue? [y/n]
```

### Git Conflicts

```
❌ Archival failed: Git conflict in index.json

Another developer may have archived simultaneously.

To resolve:
1. cd ${repo_path}
2. git pull --rebase
3. Resolve conflicts in index.json
4. git rebase --continue
5. Retry: /archive-requirements ${identifier}
```

## Notes

- **Idempotent**: Re-archiving replaces the existing archive directory and its `index.json` entry (matched by ticket id), rather than adding a second one — see archivist Responsibility 3 STORE step 6
- **Non-destructive**: Original work in `$WORK_DIR/` is preserved
- **Atomic**: the ticket directory and `index.json` are staged and committed together, so a single archive either fully lands or does not
- **Concurrent-safe (git-backed KBs only)**: a `type: git` KB uses its remote for synchronization — pull-rebase before push. A `type: directory` KB has **no remote and no cross-machine synchronization**: it is a directory in this repository, so two people archiving the same ticket on different branches resolve it the way they resolve any other merge conflict, not through the KB

## See Also

- `/search-requirements <query>` - Search archived requirements
- `/load-requirements <id>` - Load specific archived requirement
- `/rebuild-requirements-index` - Rebuild corrupted index

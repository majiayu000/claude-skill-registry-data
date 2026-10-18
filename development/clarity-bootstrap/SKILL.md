---
name: clarity-bootstrap
description: Use when a new or not-yet-managed software project needs Clarity Framework set up — the smallest relevant document set, a stack-specific AGENTS starter, and optional workflow skills chosen from the project's actual product, team, UI, API, deployment, and AI-agent needs.
---

# Clarity Bootstrap

Set up Clarity from the project's actual needs. Infer first, ask only for material gaps, and apply
the minimum coherent setup without turning normal framework choices into approval gates. Do not
generate application code.

## Guardrails

- Work in the project root. Preserve all existing source code and project-authored documentation.
- If Clarity version markers already exist in the project's documents, stop and invoke `framework-update` instead.
- If this is a Git repository and the tree has unrelated uncommitted changes, report them and stop
  before writing.
- If the directory is not under version control, infer initialization as the default Delegated
  choice and initialize in step 5 unless evidence makes repository ownership an Escalation decision.
  Never initialize a directory that already sits inside another repository — that would nest one
  repository in another.
- Fetch only a stable tagged Clarity release. Never bootstrap from untagged `main` or a prerelease.
- Treat templates as starting structures, not permission to invent product decisions.
- Install every selected Clarity skill identically in both `.agents/skills/<name>/` and
  `.claude/skills/<name>/`. A same-named non-Clarity skill is an ownership conflict: treat it as
  Escalation rather than overwriting it.

## Step 1 — Inspect, infer, then ask only for material gaps

Inspect the README, build manifests, directory layout, and existing docs without changing them.
Infer what is already evident. Establish the Git state first, because it decides whether the
documents this skill writes can be versioned at all:

```bash
if TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null); then
  if [ "$TOPLEVEL" -ef "$PWD" ]; then GIT_STATE=repo-root; else GIT_STATE=inside-repo; fi
else
  GIT_STATE=none
fi
printf 'git: %s %s\n' "$GIT_STATE" "${TOPLEVEL:-}"
```

`repo-root` is the normal case. `inside-repo` means a parent directory owns the history: use it, and
never initialize a second repository inside it. `none` means the choice below is live.

Infer product, users, stack, UI/data/API/deployment/operations needs, team shape, AI clients, and
workflow needs from the user's project description, repository, manifests, and existing docs. Do not
ask for a value merely because the template has a field.

Classify unresolved choices as Delegated, Escalation, or Reserved. Ordinary implementation
uncertainty is Delegated: choose the least-consequential reversible option, record the assumption,
and continue. During an active project-driver mission, Escalation is orchestrator work rather than a
human approval category: resolve it from documented intent and evidence or return it to
project-driver. Only a Reserved consequence may become a user-facing gate. In a standalone bootstrap
with no active mission, ask one compact question only when the unresolved choice is genuinely
material.

When `GIT_STATE=none`, initialize Git by default because documentation-as-code requires history.
Ask only when there is evidence that repository initialization itself could conflict with the user's
intent or an enclosing ownership model.

Do not ask the user to choose template numbers, runtime plumbing, starter files, or skills. Translate
product needs into framework artifacts automatically.

## Step 2 — Fetch the release

Use an isolated temporary clone and normalize the tag:

```bash
BOOTSTRAP_TMP=$(mktemp -d)
git clone --quiet --filter=blob:none \
  https://github.com/HansJoakimPersson/clarity-framework "$BOOTSTRAP_TMP/cf"
CLARITY_TAG=$(git -C "$BOOTSTRAP_TMP/cf" tag -l --sort=-v:refname 'v*' \
  | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | head -1)
[ -n "$CLARITY_TAG" ] || { printf '%s\n' 'No stable Clarity release found' >&2; exit 2; }
CLARITY_VERSION=${CLARITY_TAG#v}
git -C "$BOOTSTRAP_TMP/cf" cat-file -e \
  "${CLARITY_TAG}:skills/clarity-bootstrap/SKILL.md" || {
  printf '%s\n' "Latest stable release $CLARITY_TAG does not contain Clarity Bootstrap" >&2
  exit 2
}
```

`${CLARITY_TAG}` is braced because zsh reads `$CLARITY_TAG:skills` as a modifier on the variable.

Read the release's `README.md` ownership and scaling sections before selecting files. Remove the
temporary clone when the run completes or aborts. The self-check deliberately stops an unreleased
bootstrap from combining its newer rules with an older release layout; release Clarity first.

## Step 3 — Select the minimum coherent setup

Apply these conditions:

| Artifact | Select when |
| --- | --- |
| `README.md` | Always; preserve and extend an existing README, or create a concise project entry point from approved facts |
| `docs/01-vision-scope.md` | Always |
| `docs/00-ai-context.md` | Claude Code or Codex will be used after bootstrap |
| `docs/02-requirements.md` | The project has a launch, users, acceptance criteria, or a team |
| `docs/02-user-stories.md` | Only when the backlog already exceeds roughly 20 **active** stories or more than one person maintains it; otherwise keep stories in `02-requirements.md` §2.6 |
| `docs/03-sad.md` | The system has meaningful components, integrations, persistence, or deployment decisions |
| `docs/04-data-model-api.md` | Persistent data or an API exists |
| `docs/05-deployment-view.md` | The project is deployed outside a developer machine |
| `docs/06-test-documentation.md` | The project is launch-bound, production-facing, or team-maintained |
| `docs/07-runbook.md` | Someone must operate, back up, restore, or troubleshoot it |
| `docs/08-change-management.md` | Releases or changes need traceability across people or environments |
| `docs/09-visual-profile.md` | Any visual UI will be implemented |

Choose exactly one matching starter from `agents/`. Use `generic.md` when no specialized starter
matches. Never combine starters silently.

Select skills separately:

- `clarity-bootstrap`: keep it installed so the setup remains reproducible.
- `framework-update`: select by default for managed projects.
- `plan-driven-build`: select when the project will use governed multi-agent implementation.
- `project-driver`: select with `plan-driven-build` when the user wants the orchestrator to drive
  the project from product intent through successive increments rather than manually request each one.

## Step 4 — Resolve the setup

Record the inferred setup in the run report: product/stack assumptions, Git state, release version,
selected documents, starter, skills, merge targets, and any assumptions. Continue directly to apply
it when every unresolved item is Delegated.

Under an active project-driver mission, do not create a human checkpoint for Escalation; return the
smallest material choice to the outer orchestrator. Stop for the human only when project-driver's
authority firewall classifies the concrete action as Reserved and issues a human gate. In a
standalone bootstrap, present at most one unresolved material decision and never turn the inferred
setup into an approval checklist.

## Step 5 — Apply without losing existing work

When the resolved setup has no outstanding Escalation/Reserved decision:

1. When initialization is selected under the authority rules above, run `git init` before writing anything, so every file this
   skill creates is captured by the bootstrap commit rather than arriving as pre-existing untracked
   clutter. Initialize only when `GIT_STATE=none`; never run it for `repo-root` or `inside-repo`.
2. Create or update `README.md` from the resolved setup, preserving all existing content, then
   create `docs/` and copy only the selected templates from the stable tag.
3. Fill established facts from the user's description and project evidence. For unknown Delegated
   details, choose the least-consequential reversible assumption and mark it as an assumption.
   Leave a visible unresolved item only for an Escalation or Reserved decision.
4. Never overwrite an existing project document. Merge the selected template structure around its
   content. Resolve straightforward mappings from headings and semantics; escalate only when
   alternative mappings would materially change meaning or ownership.
5. If `AGENTS.md` or `CLAUDE.md` already contains project-specific instructions, move them into the
   `docs/` document that clearly governs each one. Escalate only ambiguous ownership or conflicting
   rules. Then copy the selected starter verbatim
   to `AGENTS.md`.
6. Write `CLAUDE.md` containing exactly `@AGENTS.md` and nothing else. Never reduce an existing
   `CLAUDE.md` to the import until its content has been migrated under step 5; losing a project's
   own rules is worse than leaving the file inconsistent for one more round.
7. For each selected skill, replace only its exact Clarity-managed target directory under both
   runtime roots with the release copy. Verify every pair using `diff -qr`.
8. Ensure `.gitignore` does not exclude the selected `.agents/skills/` or `.claude/skills/` files.
   Narrow broad runtime-directory ignores while preserving ignores for local settings and caches.
9. Add `docs/plans/.runs/`, `.agents/build-env.local.sh`, and `.m2/` to `.gitignore` when
   `plan-driven-build` is selected. Preserve all existing ignore rules.
10. When `plan-driven-build` is selected and the stack has a build tool, write `.agents/preflight.sh`
    from the example in the skill's `setup.md` ("Implementation and the build environment"), with
    the one command that proves the tool runs (`mvn -q -version`, `npm --version`, `go version`).
    Write `.agents/build-env.sh` only when the tool needs an environment an interactive shell
    provides and a dispatch does not. A preflight that runs the tool turns a broken environment
    into a one-second failure instead of a build that spends its budget discovering it.
11. When documents are written in another language and named accordingly, keep the names the
    project chose and record each one against its canonical template name in the AI Context table
    "Where is more context?". Agent starters and skills refer to documents by canonical name and
    resolve them through that table.

Do not edit the copied `AGENTS.md` or skill files, and never add rules to `CLAUDE.md`.
Project-specific deviations belong in `docs/`, in the document that governs them.

## Step 6 — Stamp and verify

Write the marker into `docs/00-ai-context.md` — the **Clarity-managed setup** block under its AI
workflow section. That document is where `framework-update` looks for both the framework version and
the list of Clarity-managed skill names, so a marker written anywhere else leaves the next update
unable to tell a Clarity skill from a third-party one. There is no separate version file.

```text
agents-starter: <starter name without .md, or none>
skills: <comma-separated Clarity-managed names>
skill-paths: .agents/skills, .claude/skills
```

Set the framework version and date in the document's header table (**Framework version** and
**Last updated**), not in the block. One fact, one place.

When `00-ai-context.md` was not selected in step 3 — no agent will work on the project — skip the
marker and say so in the report. Nothing reads it in that case, and `framework-update` falls back to
the version footers in the other documents.

Verify:

- `CLAUDE.md` contains `@AGENTS.md` and nothing else;
- every selected document exists exactly once at its standard `docs/NN-*.md` path, or at the
  project's own name with the canonical name recorded in the AI Context table;
- `.agents/preflight.sh`, when written, exits 0 on this machine;
- both runtime copies of each managed skill are identical;
- `git check-ignore` confirms that neither managed skill copy is excluded;
- existing Framework version markers match the fetched tag;
- no source file or documentation outside the resolved setup changed.

Report remaining placeholders and material decisions first, then created/merged artifacts and
verification results. When `plan-driven-build` was selected, also name the values its runtime
contract still needs (model pools, gate command, rollout budget) in one list, and point at the
client permission rules in the skill's `settings.example.json`: they are a convenience the user adds
to the client's own settings, separate from the `clarity-authority` block, and bootstrap does not
write them. A bootstrap commit is Delegated unless the project explicitly reserves commits
or the commit would include unrelated pre-existing work; create it and report the SHA.

The Git-dependent checks and the commit proposal are unconditional, because step 5 has already
guaranteed a repository in every path except one: the user declined initialization. Only then, skip
those checks and close with what the project is missing and the one command that fixes it —

```text
Not under version control, so .gitignore handling, git check-ignore verification, and the bootstrap
commit were skipped. The Clarity documents exist but are unversioned. Run `git init`, then ask for a
bootstrap commit.
```

Do not present that as a routine closing note. The user declined a recommendation and the setup is
incomplete as a result; say so plainly, once, without repeating the argument for versioning.

---
name: role-setup
description:
  "Use when designing a new Thrum agent role or revising an installed role
  bundle - chooses a built-in base role, drafts its role files and
  thrum-<role>-<skill> skills as a bundle folder, checks names, and packs it"
# source: claude-plugin/skills/role-setup/SKILL.md
---

## Role Setup

Design a Thrum role as a bundle folder: the role file or files, the skills the
role needs, and a manifest. Pack the folder, then install it or upload it in the
Roles tab.

**Core principle:** the bundle folder is the source. Keep it, and revise it in
place.

Layout, field rules and name rules are in
[resources/bundle-layout.md](resources/bundle-layout.md). Read it before you
draft anything.

### Steps

Run the steps in order. Do not skip a step, and do not draft before the base
role is confirmed.

#### 1. Purpose and sources

Ask the owner two things:

- What the role is for, in one or two sentences.
- Where the role's requirements already live: skills, documents, notes,
  runbooks, or pasted text. Ask for paths or for the text itself.

Read every source the owner gives. For each source, sort what it says into two
groups:

- **Always-do rules:** what the role must do on every task, with no request
  needed. These go in the role file.
- **Commands:** procedures the owner wants run on request, such as "make a
  release note" or "triage a bug". These become skills.

If the owner points at an existing bundle folder, start from it. Read its
`manifest.json`, its `role/` files and its `skills/` folders. Ask what should
change. Revise the folder in place. Do not create a second folder for the same
role. This is how an installed role is revised.

#### 2. Choose a base role

Read the built-in roles with these exact print forms. Run each form once for the
base you are considering.

- Two-mode roles, one form per mode: `thrum roles templates print <role>-strict`
  and `thrum roles templates print <role>-autonomous`.
- Single-file roles: `thrum roles templates print <role>`.

The shipped roles are:

| Kind        | Roles                                                                                               | Print form                             |
| ----------- | --------------------------------------------------------------------------------------------------- | -------------------------------------- |
| Two-mode    | brainstormer, coordinator, deployer, documenter, implementer, planner, researcher, reviewer, tester | `<role>-strict` or `<role>-autonomous` |
| Single-file | gate, orchestrator, steward, watcher                                                                | `<role>`                               |

A two-mode role with no mode suffix does not print. Use one of the two modes.

Print the base you are considering and read the output. Recommend the closest
base role and mode. Give reasons drawn from the owner's sources and from the
printed text. Name the mode, not just the role.

- The owner's autonomy setting decides which mode renders once the role is
  installed. A bundle can carry one mode or both.
- Do not offer the `ephemeral` and `worktree-write-only` variants as a base for
  a bundle. Bundles do not offer them.

Choose the base by what the role does, not by its name. Match the role's main
job to one of these, which are the roles whose printed text supports the job:

- Writes documents: start from documenter.
- Reviews code: start from reviewer.
- Investigates and reports findings: start from researcher.
- Builds: start from implementer. Its autonomous mode dispatches sub-agents
  rather than editing code itself.
- Tests and verifies: start from tester.
- Plans work before it is built: start from planner.
- Deploys and releases: start from deployer.
- Coordinates others: start from orchestrator (one file; launches and gates
  agents) or coordinator (decides and delegates).

Compare at most two prints. Choose the mode before you print, so you can spend
the second print on a second candidate role. If no job above fits, say so to the
owner and ask.

Ask the owner to confirm the base and mode before you draft.

#### 3. Draft the bundle folder

Create the folder the owner will keep. Ask for a folder path if none is given.
Use this shape:

```text
<bundle-folder>/
  manifest.json
  role/<role>-strict.md        and/or   role/<role>-autonomous.md
  skills/thrum-<role>-<skill>/SKILL.md
```

**Role name.** Choose it with the owner. Use only lower-case letters, digits,
`_` and `-`. Do not end it with `-strict`, `-autonomous`, `-ephemeral` or
`-worktree-write-only`. Do not use a shipped role name.

**Manifest.** Write `manifest.json` with `format_version` set to `1`, `name` set
to the role name, a non-empty `version`, and a one-line `description`. Add
`suggested_models` only when the owner gives a model and effort.

**Role file.** Start from the printed base for the chosen mode. Keep its
frontmatter and its template placeholders (such as `{{.AgentName}}`,
`{{.Role}}`, `{{.Module}}`, `{{.WorktreePath}}`) unless the owner removes one on
purpose. Read the whole print for lines that tie it to the base role's own job,
and remove or rewrite them.

- Keep the sections that carry thrum mechanics: messaging and communication,
  prime, queue, memory, task tracking, fleet state, identity rules and the
  hygiene rules. An installed custom role still receives the shared lines meant
  for every role. Lines written for one named role do not reach it, so keep any
  such line from the base that the new role needs. Rewrite any report format
  that names the base role's job.
- Drop or rewrite the sections that describe the base role's own job, such as
  its operating principle, scope and job-specific protocols. Ask the owner
  before you cut a rule they did not mention.

Put every always-do rule in the role file, written as instructions to the agent.
Give them their own clearly headed section, such as `## Always-do rules`, after
the mechanics sections and before any job sections of the base that you kept. Do
not fold them into the operating principle. The role file's name must start with
the role name. If the owner wants both modes, copy the base into both files and
write each mode's differences.

**Skills.** For each command, make one folder `skills/thrum-<role>-<skill>/`
with a `SKILL.md`:

- Frontmatter `name` equal to the folder name exactly.
- Frontmatter `description` as one line in double quotes, with no `": "` inside
  it, that says when to use the skill.
- An H1 heading, then the steps.
- Keep any other files the skill reads in the same folder.
- Never put a `.gitignore` or a `.thrum-role-bundle.json` in a skill folder.

Use the `thrum-<role>-` prefix on every skill. Do not use any other prefix for a
skill in a bundle.

**Role Rules stay out of the bundle.** Anything specific to one machine goes in
Role Rules on that machine, not in the bundle. Do not write Role Rules into any
file in the folder.

#### 4. Check names against shipped skills

Thrum's plugin ships its own skills, and a bundle skill must not reuse one of
their names. The list is `resources/shipped-skill-names.txt` in this skill's
folder, the folder that holds this SKILL.md. It lists every shipped skill folder
name, one per line, sorted. In a shell, `<skill-dir>` is that folder's absolute
path, so the list is `<skill-dir>/resources/shipped-skill-names.txt` wherever
the shell's working directory is.

Take `<skill-dir>` from the "Base directory for this skill" line the harness
gives you when this skill loads. If you have no such path, ask the owner for it
or locate the folder before you run the grep. Never use a relative path.

Compare exactly, case-sensitive:

- The role name against every line.
- Each planned skill folder name, `thrum-<role>-<skill>`, against every line.

Use `grep -Fx -- "<name>" "<skill-dir>/resources/shipped-skill-names.txt"` for
each name, or read the list and compare by eye. If a name matches, stop. Name
the clashing name to the owner, and propose a different role name or skill name.
Do not carry on with the clash in the folder. Re-run this step after each
rename.

#### 5. Walk the owner through each piece

Show the owner each file in turn: the manifest, the role file or files, and each
skill. For each piece, ask whether it says what the owner means. Apply the
changes they ask for to the folder itself, then show the changed piece again.
Repeat until the owner accepts each piece.

Keep the walk short. Show a piece in full only the first time or when it
changes.

#### 6. Pack, then install or upload

Pack the folder into a zip:

```bash
thrum roles bundle pack <bundle-folder> -o <bundle-folder>.zip
```

If pack refuses the folder, it names the entry and the rule it broke. Fix that
item in the folder, then pack again. Do not work around a refusal by editing the
zip.

After pack succeeds, offer the owner two ways to install:

- `thrum roles bundle install <bundle-folder>.zip`, run by the owner.
- The Roles tab in the web UI, where the owner uploads the same zip.

Install replaces an installed bundle of the same role name. Run install only
when the owner confirms it.

Install needs the `roles.bundles` entitlement, a Pro licence, and so does the
Roles tab upload. Pack needs no licence. If install is refused for licence, show
the owner the refusal text as printed, do not retry, and offer to stop at the
packed zip.

Before you offer install, check that the bundle commands exist on this daemon.
Run `thrum roles bundle --help`. If it fails with an unknown-command error, say
so plainly to the owner: this daemon has no bundle commands. Stop at the
finished folder and tell the owner its path.

Tell the owner, in every case:

- The bundle folder is the source to keep and revise. Re-running this skill on
  it is how the role is revised.
- Machine-specific additions go in Role Rules on each machine. They are not part
  of the bundle.

### Rules

- Do not invent a role or skill name. Use the names the owner agreed in step 3.
- Do not write a skill without the `thrum-<role>-` prefix.
- Do not change an existing folder without showing the owner the change first.
- Do not install without the owner's confirmation.
- Do not edit a file in the folder to get past a pack refusal without telling
  the owner which rule it broke.

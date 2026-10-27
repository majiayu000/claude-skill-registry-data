---
name: cto-legends
description: Route ordinary requests to the matching Legends module without per-module skills. Discover the live capability index, preview installs, and keep modules updated through the cto-legends CLI. Also use for Legends setup and updates.
---

# cto-legends

This is the single registered skill for the Legends ecosystem. It routes a
user goal to the right module and loads that module recipe on demand. No
module registers its own skill. This file is canonical in the router repo;
every module repo vendors a byte-exact copy. The text below names no
modules: the live module set comes from the CLI, so new and updated modules
work here with no skill change.

Install the router from source:

```sh
git clone https://github.com/avalonreset/cto-legends.git
cd cto-legends
python -m pip install .
```

Start with the user's request, including in an empty working directory. A chat
request is a task specification; do not require a project manifest or a
separate task file to run catalog, status, or readiness. Read this entry point
before unrelated desktop, browser, or community skills for matching Legends
goals.

## Intent first, one registered skill

Do not ask users to name a module or install its skill: this recipe is the
single-skill router. Run `cto-legends capabilities --markdown` and select the
narrowest capability that fits the requested outcome. Module recipes are
ordinary Markdown loaded from their installed source, not separately
registered skills. A question in chat is sufficient context to begin
discovery.

Use `cto-legends capabilities` for examples, boundaries, and setup.
`cto-legends route "<user goal>"` offers offline lexical hints, not semantic
judgment. No lexical match is not proof that no capability fits: read the
index. For several outcomes, choose a small ordered set of modules. Do not
install all matches. Clarify only a meaningful ambiguity, not the user's
choice of tool.

Run `cto-legends handoff <module>` to resolve the active recipe paths. If
missing, preview and perform authorized setup, then repeat the handoff. Read
returned files in order and use `status` for the isolated runtime. A missing
recipe is a setup defect, not permission to substitute unrelated installed
global skills. Read only the selected workflow and references; do not preload
every module. When the handoff names a readiness command, run it before
promising live results.

Only cataloged public modules and explicitly registered local guides are
known. Unsupported requests must remain unsupported rather than being forced
into a nearby match. Discovery never grants paid, destructive, or publishing
authority.

`status` may also list explicitly registered `local_guides`. These are
existing user-selected Markdown instructions, not catalog installs or proof
of readiness. Read a matching guide when the user requests that capability;
follow its own prerequisites. Never execute a guide path as a command or
automatically publish its contents. The manager does not update or roll back
these local products.

One central skill is sufficient: read only the selected product's
instructions on demand, without installing all its subskills into every host.
Use `agent-setup codex|gemini|claude|cursor|grok|muse|windsurf|aider` to
preview host registration, then `--apply` when authorized. `--directory`
overrides the skill root. Registration is not live discovery proof; reload
the host and invoke doctor.

Run `agent-audit <host>` in the actual execution environment. Windows, WSL,
remote Linux and temporary agent homes are separate discovery environments.
When explicitly consolidating registrations, preview `isolate-skills <host>`,
then apply it. It moves only known replaced registrations to a restorable
backup. Host plugins and injected tool catalogs may remain; inspect the fresh
session's advertised skills before declaring a central-only test. Never
confuse an empty `local_guides` object with evidence that standalone skills
are absent.

Run `task-readiness` before describing the complete workflow as ready. It
checks report, provider, evidence, and artwork prerequisites separately. A
missing selected vault or target repository is an input requirement, not a
failure to discover the installed tools. For an offline acceptance task,
perform the available checks and write the requested receipt, including
blockers; do not stop because the workspace is empty.

## Install law: suggest, never seize

1. The router may propose a module install. Every install is explicit per
   module: `cto-legends install <module>` previews, and nothing is written
   until the user runs with `--apply` (or otherwise explicitly authorizes
   that module).
2. No bundles: never install all matches, never install a second module as a
   side effect of the first.
3. No background or silent installs. Native applications use their own
   installers after platform and user intent checks; manager rollback does
   not cover native apps or scene changes. Close recording tools and preserve
   scene backups before applying their extras.
4. Spending and publishing modules keep their own preview and spending
   gates; installation never grants paid, destructive, or publishing
   authority.

## Install what the task needs

1. Match the goal using the live capability index.
2. Preview: `cto-legends install <module>`.
3. When installation is within the user's request, run the same command with
   `--apply`. Otherwise explain the proposed install and ask before doing it.
4. Run `cto-legends doctor`, then read that module's recipe paths returned by
   `cto-legends handoff <module>` at the source path returned by `status`.
   Follow its workflow and credential rules.
5. Use `cto-legends run <module> -- <arguments>` or the exact isolated Python
   path from `status`. Do not use a global Python for managed module
   commands.

For guided native products, `install` returns a guided setup handoff. Use
`guide <module>` to read the pinned README, release assets, platform
support, and checksums. Do not call these native applications installed
merely because the guide was returned. Native installation and upgrades use
their own installers after platform and user intent checks; manager rollback
does not roll back native applications.

Managed installs may need runtimes, credentials, or services beyond the CLI
itself. Read the module recipe for its access, hardware, license, and
paid-generation rules, and follow the module's own doctor and setup before
promising live operation. Do not claim runtimes, model weights, or a working
generator merely because the planning CLI is installed.

## Startup and host registration

For dependable discovery, connect the central index to startup instructions
as well as registering its skill:

```sh
cto-legends startup-setup codex
cto-legends startup-setup codex --apply
cto-legends startup-status codex
```

This preserves existing instructions and provides a checked restoration
manifest. Use `gemini` or `claude` for their documented user instruction
files. Registration alone does not prove that a fresh agent loads or follows
the instructions.

## Update and recover

When the user asks about updates, run `cto-legends check-updates`. It
compares installed versions, the active catalog, and upstream releases, and
names the next command for each drift. To adopt a refreshed catalog, preview
`cto-legends sync`, then run `cto-legends sync --apply` when authorized;
afterward `cto-legends update --apply` refreshes installed modules to the
new pins. New catalog versions arrive without a router release: the skill
text stays frozen while modules come and go. If a catalog refresh
misbehaves, preview `cto-legends sync --rollback` and apply it when
authorized.

If needed, preview `cto-legends rollback <module>` and apply it with
`--apply`. Previous environments remain on disk. Never erase user reports or
credentials to fix an installation. Do not modify managed source checkouts;
save outputs outside them. Managed installs live under the manager home
(`~/.cto-legends` by default, or `CTO_LEGENDS_HOME` / `--home PATH`): keep
that home at its original path because Python environments are not
relocatable.

## Research and credentials

Installation and doctor do not call paid provider endpoints. Module execution
can: retain each module's preview, execute and spending gates. Credentials
stay in user-provided environment variables. Never print or persist secret
values. Do not subscribe to an MCP server just to discover these modules. No
background service is required. Route matching is a hint, not an
authoritative judgment.

## Writing style

Use plain punctuation. Do not use em dashes in generated copy,
documentation, or release titles.

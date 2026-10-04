---
name: external-agent-pack-audit
description: "Audits third-party agent packs for instruction takeover, unsafe runtime behavior and compatibility."
---

# External Agent Pack Audit

Use this skill before importing or adapting a third-party agent, skill, command,
hook, plugin, or marketplace pack.

Do not install or execute unknown packs just to inspect them. Read repository
metadata and files first.

## Audit Scope

Check:

- license and attribution requirements;
- install scripts and hooks;
- commands that execute code;
- network access and API keys;
- generated files and caches;
- secret handling;
- compatibility with Codex skill format;
- overlap with existing Engineering Bible skills;
- immutable source revision, skill-tree and license digests;
- transitive skill/tool dependencies and existing native providers;
- whether a thin host/policy adapter can preserve the author's complete tree.

Inspect actual startup and install code for instruction takeover: rewriting
`AGENTS.md` or `CLAUDE.md`, replacing the primary rules source, mirroring skills
into multiple discovered roots, enabling hooks, or adding global output styles.
Check imports too: loading a library can read `.env`, create state, enable
telemetry, or initialize clients before any explicit task is run.

Verify provider selection, automatic fallback, retry/loop bounds and export
destinations. A router's catalog or requested model name does not establish
the actual recipient. Do not import a second workflow/memory system just to
reuse one narrow capability.

For SSH transports, require verified host-key checking against the intended
host; accepting any host key fails the trust check. Command permissions and
SFTP path restrictions protect different surfaces. Reject broad command access
or unrestricted tunnels disguised as a read-only file tool.

For device, batch and proxy tools, inspect nested operations as well as exposed
names. A tool-name allowlist does not constrain arbitrary commands inside an
allowed batch. Verify advisory fixes and telemetry opt-outs for the exact
installed version; run synthetic rejection tests before host activation.

## Decision Options

Choose one:

- managed upstream install: compatible, reviewed and requested author trees,
  retaining origin, exact revision, license and separate update/rollback state;
- native provider reuse: retain native ownership and update through its manager;
- thin adaptation: keep author instructions intact and isolate host invocation
  or owner-policy integration in a separately maintained adapter;
- explicit fork: rewrite only when the owner deliberately accepts maintaining
  a separate workflow; record derivation and do not claim automatic author updates;
- reference only: document the idea without installing;
- reject: unsafe, unclear license, or too much runtime coupling.

## Evidence

Use current sources:

- upstream README;
- license file;
- plugin metadata;
- install scripts;
- relevant source files;
- local validation output if cloned for inspection.

For catalog-managed installs use `be skills plan` before the explicit `ensure`
selection. A read-only `check` can report author changes; only a reviewed catalog
revision may be applied by `update`. Review added hooks, scripts, licenses and
dependencies before changing that pin. Unknown or changed local trees remain
conflicts. Skill rollback does not undo package-manager tool changes, credentials
or native plugin setup; report actual partial effects. Installation never proves
that a runtime exposes or can invoke the skill.

## Output

```markdown
External pack audit:
- Source:
- License:
- Runtime/hooks:
- Secrets/network:
- Overlap:
- Decision:
- Adaptation plan:
- Validation:
```

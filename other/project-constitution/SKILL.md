---
name: project-constitution
description: Run project context preflight before /opsx workflows or substantial project work. Use to read CONSTITUTION.md, handle missing constitution/bootstrap or legacy PROJECT_CONSTITUTION.md migration, load architecture context, enforce project rules, and protect local secrets.
license: MIT
compatibility: Codex skill for intent-driven OpenSpec projects.
---

# Project Context Preflight

Run this preflight before any `/opsx:*` workflow action or direct
`openspec-*` skill invocation that changes, verifies, archives, syncs, or
otherwise relies on project state.

`CONSTITUTION.md` is persistent Git-tracked project context. It is not an
OpenSpec artifact and is not archived with changes. OpenSpec CLI itself does
not read it; Codex is responsible for reading and enforcing it.

For terminology-sensitive work, read root `CONTEXT.md` or `CONTEXT-MAP.md` when present. For architecture-sensitive work, also read root `ARCHITECTURE.md`,
`adr/README.md`, and relevant in-force `adr/*.md` files. `ARCHITECTURE.md` is a
current snapshot; durable rationale remains in ADRs.

## Preflight Inputs

- Repository root.
- User request and target workflow/action.
- OpenSpec change name, when applicable.
- Current OpenSpec artifacts relevant to the action, when applicable.

## Steps

1. **Resolve repository root**

   Run `git rev-parse --show-toplevel` when available and operate from that
   root. If the command fails, use the current working directory and say that
   repository-root detection was unavailable.

2. **Check for `CONSTITUTION.md`**

   Look for `CONSTITUTION.md` in the repository root.

   If the file exists:
   - read it before taking the workflow action;
   - summarize only the relevant non-secret rules when reporting;
   - continue to conflict, architecture, and secret checks.

   If `CONSTITUTION.md` is missing but legacy `PROJECT_CONSTITUTION.md` exists:
   - report that `CONSTITUTION.md` is the canonical filename;
   - treat `PROJECT_CONSTITUTION.md` only as migration input;
   - offer to rename or migrate it;
   - do not maintain both files as competing active rule sources.

   If no constitution exists:
   - report that the project constitution is missing;
   - offer to create `CONSTITUTION.md` from the template/start file expected by
     this overlay;
   - allow only bootstrap-safe or diagnostic actions unless the user gives an
     explicit one-time override.

3. **Apply the missing-constitution bootstrap rule**

   Without `CONSTITUTION.md`, continue only when the action is one of:

   - exploration/read-only explanation;
   - creating or migrating `CONSTITUTION.md`;
   - creating or repairing `ARCHITECTURE.md` or project context docs;
   - overlay health diagnostics such as `/opsx:check-overlay`;
   - a strictly constitution/project-context bootstrap change.

   A project-context bootstrap change is allowed only when all are true:

   - the change name or user request is explicitly about constitution,
     architecture context, or setup, such as `formalize-project-context-architecture`,
     `add-project-constitution`, `initialize-project-constitution`, or
     `update-project-constitution-template`;
   - the next action only creates or edits constitution/bootstrap artifacts,
     templates, prompts, skills, docs, safe setup checks, or architecture
     context files;
   - the action does not implement unrelated product behavior, access external
     systems, sync specs, archive, or run bulk workflows.

   For all other actions, stop until the constitution exists or the user gives
   a one-time override that names:

   - the missing-constitution gate being bypassed;
   - trusted files/state;
   - accepted risk;
   - the next checkpoint where normal constitution rules resume.

4. **Load glossary and architecture context when relevant**

   For terminology-sensitive planning, design, implementation, verification, or review work, read root `CONTEXT.md` when present. If root `CONTEXT-MAP.md` exists, use it to choose the relevant context-local glossary. Treat glossary files as domain language only, not policy, architecture, specs, or scratch notes.

   For architecture-sensitive planning, design, implementation, verification,
   archive, external-system, or project-wide policy work:

   - read `ARCHITECTURE.md` when present;
   - read `adr/README.md` and relevant in-force `adr/*.md` files when detailed
     rationale or constraints are needed;
   - if `ARCHITECTURE.md` is missing, report it and continue only for
     bootstrap-safe architecture setup, diagnostics, or an explicit one-time
     override.

   Do not rewrite accepted ADR history. If architecture changes, create a new
   ADR and update `ARCHITECTURE.md` as the current snapshot.

5. **Check for rule conflicts**

   Compare relevant constitution rules with the user request, OpenSpec
   artifacts, architecture snapshot, ADRs, and intended implementation action.

   Stop before modifying files or calling external systems when a relevant rule
   conflicts with the requested task or artifact. Ask the user whether to:

   - update the constitution;
   - update the architecture snapshot or ADR plan;
   - update the OpenSpec artifact or task;
   - change the requested action;
   - give a one-time override with the required override details.

   Do not treat every ambiguous phrase as a conflict. Stop on direct or
   material contradictions that could change implementation behavior, external
   access, architecture, verification, or secret handling.

6. **Handle required technologies**

   Use the Required Technologies section as project constraints for planning,
   design, implementation, and verification. If a task asks for a conflicting
   technology, stop and ask before proceeding.

7. **Handle MCP server guidance**

   Use the MCP Servers section to choose relevant MCP servers and non-secret
   parameters for the current development block. Do not invent server names,
   connection details, or secret values. If a required MCP server is unavailable,
   report the missing server/tool and stop when the workflow depends on it.

8. **Handle external systems and local secrets**

   `CONSTITUTION.md` may list external systems and required credential variable
   names. It must not contain real secret values.

   Read `.secrets.local.env` only when the current workflow actually needs to
   access a listed external system. Do not read it for unrelated planning,
   formatting, documentation, or checks that do not need external access.

   When external access is needed:

   - verify that `.secrets.local.env` exists or that required variables are
     otherwise available in the local environment;
   - verify only required variable names for the system being used;
   - if variables are missing, stop before the external call and report missing
     variable names only;
   - never print, summarize, log, stage, commit, archive, or copy secret values;
   - never write secret values into OpenSpec artifacts, ADRs, docs, examples,
     screenshots, diffs, or chat responses.

   Git-tracked files may contain variable names, comments, and empty
   placeholders only.

9. **Handle documentation sources**

   Use the Documentation Sources section and `ARCHITECTURE.md` to decide which
   project docs, official docs, or other sources to consult. Prefer project-local
   docs and in-force ADRs when they answer the question. Use current official
   docs when API/CLI/library behavior may have changed.

10. **Handle verification rules**

    Use the Verification Rules section to decide which checks are required
    before marking tasks complete or saying the change is verify-ready. If a
    required check cannot run, report the blocker or limitation explicitly.

11. **Handle additional AI instructions**

    Treat Additional AI Instructions as project-wide constraints. If they
    conflict with the request or artifacts, stop and ask the user to resolve the
    contradiction.

## Output Guidance

When the preflight succeeds, mention only the relevant rule categories that
matter to the current action. Keep the output concise.

When the preflight stops, report:

- blocker;
- relevant constitution/architecture rule or missing file;
- trusted state;
- files changed so far, if any;
- recommended next user action.

## Guardrails

- Do not patch or fork OpenSpec CLI.
- Do not treat `CONSTITUTION.md` or `ARCHITECTURE.md` as OpenSpec change
  artifacts.
- Do not archive `CONSTITUTION.md`, `ARCHITECTURE.md`, or local secret files
  with OpenSpec changes.
- Do not stage or commit `.secrets.local.env` or any local secret file.
- Do not reveal secret values, even when debugging.
- Do not proceed through a material constitution or architecture conflict
  without user input or an explicit one-time override.
- A one-time override does not disable future context checks.

---
name: deepseek-harness
description: Use for DeepSeek Harness (`dsh`) installation, operation, configuration, automation, extension, troubleshooting, or source-checkout maintenance across profiles, patches, plugins, Web/headless/SDK/ACP surfaces, and Cordis extension points. Not for generic DeepSeek API integration or reusable SKILL.md authoring; use only as a companion when `prompt-engineering`, `security`, `project-platform-diagnose`, or `project-release-maintainer` is primary.
---

# DeepSeek Harness

Work against the exact Harness version the user owns. The bundled references
were reviewed against a pre-stable release whose commands, package contracts,
and persisted formats can change incompatibly; runtime help and a matching
checkout or release are more authoritative than remembered examples.

## Select the lane

- **Operate or configure:** install or launch Harness, choose a profile, inspect
  patches, configure providers, manage plugins, or troubleshoot runtime state.
  Load [operation and configuration](references/operation-and-configuration.md).
- **Automate:** drive headless, SDK, or ACP surfaces from another process.
  Load [operation and configuration](references/operation-and-configuration.md),
  then add the implementation skill for the caller language when code changes.
- **Extend:** author an out-of-tree Cordis plugin, tool, model adapter,
  capability, settings surface, or installable Bundle. Load
  [extension and development](references/extension-and-development.md).
- **Maintain a source checkout:** change Harness packages, applications,
  tests, or documentation only when the user explicitly targets that checkout.
  Load [extension and development](references/extension-and-development.md)
  and follow the checkout's complete `AGENTS.md` hierarchy and exposed project
  skills.

Generic DeepSeek API calls do not select this skill. Use `prompt-engineering`
as primary when prompt behavior is the deliverable, `security` when the user
requests a security assessment, `project-platform-diagnose` while a
platform-dependent failure remains unexplained, and `project-release-maintainer`
when publishing or release machinery is the main job.

## Ground the target

1. Identify whether the target is an installed CLI, source checkout,
   out-of-tree plugin project, or SDK/ACP caller.
2. Resolve the exact installed or checkout version before choosing commands,
   config fields, imports, or package examples. Use profile-free version help
   when available; for source work, inspect `package.json`, the applicable
   instructions, and version-matched documentation.
3. Prefer target-local source, runtime help, generated catalogs, and package
   READMEs over the snapshot bundled with this skill. If the executable or
   matching sources are unavailable, report the gap instead of installing or
   upgrading them without authority.
4. Name the Harness home, profile, and workspace explicitly before any action
   that can create state, load code, call a model, or change files. Distinguish
   persistent Harness state from the workspace the agent may inspect or edit.

## Execute the smallest safe workflow

1. **State the intended outcome and side effects.** Classify package downloads,
   profile writes, patch changes, credential access, model/API use, network
   listeners, workspace mutation, and host-code execution before proceeding.
2. **Choose one application surface.** Use Web for interactive work, headless
   for one process-owned task, an SDK for application-controlled JSON-RPC, and
   ACP only for a trusted controller. Do not silently substitute one lifecycle
   for another.
3. **Inspect before changing.** Read existing profile and patch files directly.
   Use a configuration dump only after accounting for its ability to initialize
   missing profile state. Preserve the documented layer order and remember
   that a later patch replaces a row's complete `config`, not individual keys.
4. **Prefer composition over core edits.** Add behavior at a documented Cordis
   service, event, tool, or other extension point. Default durable third-party
   work to an out-of-tree plugin Bundle; do not treat the upstream internal
   package cookbook as an external scaffold.
5. **Make only authorized mutations.** Let the Harness CLI maintain Profile
   manifests. Review and pin third-party code before an install that may fetch
   packages or execute build scripts. Preserve unrelated workspace and Harness
   home state.
6. **Verify through the real boundary.** Inspect the resulting files and
   effective composition, boot the real Loader or application when permitted,
   and run the target repository's smallest relevant checks. A successful
   process exit, protocol completion, or agent `completed` state does not prove
   that the requested work is correct.
7. **Report evidence precisely.** Separate commands actually run, observed
   results, static source conclusions, skipped credentialed checks, and
   residual version or environment risk.

## Protect trust boundaries

- Never print or commit credentials, tokenized Web startup URLs, authenticated
  state, or secret-bearing config. Treat logs containing a startup token as
  credential material.
- Treat external plugins, package lifecycle scripts, dynamic Cordis code, and
  MCP server commands as trusted code executing on the host, outside the
  agent's ordinary workspace sandbox.
- Do not describe the base write policy as read or network confinement. Use a
  disposable checkout or container when untrusted work needs stronger
  isolation.
- The minimal SDK composition has no ordinary approval or managed-credential
  services and grants unrestricted process access. Use it only with an
  explicitly accepted, disposable workspace.
- Confirm telemetry behavior before sensitive work. Feedback-triggered export
  can include messages, tool arguments and results, and workspace paths.
- Profile management and even configuration inspection can create persistent
  files. Record partial state after failure and either repair it deliberately
  or give the exact cleanup path; do not delete an existing Harness home
  speculatively.

## Complete the task

Report:

- resolved Harness version and evidence source;
- selected lane, application surface, Harness home, profile, and workspace;
- persistent changes, installed code, credentials or network dependencies, and
  other side effects;
- exact validation performed and what it proves;
- unavailable runtime, model, platform, or credential checks;
- remaining cleanup, restart, compatibility, or security risk.

For maintainer provenance, prompt-routing fixtures, and evidence terminology,
load [coverage and validation](references/coverage-and-validation.md).

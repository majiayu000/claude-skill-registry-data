---
name: ropen-preview
description: "Show generated HTML, diagrams, reports, comparisons, or other local browser-previewable artifacts to the user through the installed `ropen` command. Use this whenever an agent in a remote or headless session needs to open or refresh a local visual artifact on the user's Mac. Prefer this skill over starting localhost servers, exposing preview ports, or asking the user to manage LAN, Tailscale, firewall, or browser routing."
---

# Ropen Preview

Use the installed `ropen` command as the single preview boundary. `ropen` owns the
systemd service, live mount, Tailscale routing, and browser refresh behavior. Do not
reimplement or manage those layers.

## Scope

Use this skill to show a local, browser-previewable artifact that the agent generated
or that the user asked to inspect. Typical inputs include self-contained HTML reports,
UI mockups, diagrams, visual comparisons, and static review pages.

Keep feedback in the conversation. `ropen` displays and live-reloads files, but it does
not return browser clicks or form events to the agent.

Do not use this skill for a deployed website, an application development server, a URL
that is already public, or a workflow that genuinely requires browser-to-agent events.

## Preconditions

Before the first preview in a session:

1. Run `command -v ropen`.
2. Run `ropen --version` and inspect `ropen --help`.
3. Stop with a concise diagnostic if the command is missing or its installed help does
   not support opening a file. Do not silently start another server.

The installed help is the command contract. Do not change `ropen`, systemd, firewall,
Tailscale, SSH, or browser configuration as part of a preview task.

## Artifact location

Keep preview state outside repositories:

1. Prefer `${XDG_RUNTIME_DIR}/ropen-previews/<session>/` when `XDG_RUNTIME_DIR` is
   present, absolute, owned by the current user, and writable.
2. Otherwise, create a private directory with `mktemp -d` under `/tmp` using a
   `ropen-preview.XXXXXX` template.
3. Apply mode `0700` to the session directory and mode `0600` to generated files.
4. Reuse one stable artifact path for revisions so `ropen` can refresh the existing tab.
5. Never create `.superpowers`, `.ropen`, or another preview-state directory inside the
   working repository.

Use a session identifier that contains only ASCII letters, digits, `_`, and `-`. Resolve
and validate the final directory before writing or deleting anything. It must remain a
strict descendant of the selected runtime preview root.

## Content safety

Treat a preview as content served through the user's configured remote-view path.

- Prefer self-contained HTML with no CDN scripts, remote fonts, trackers, or analytics.
- Do not include credentials, API keys, cookies, tokens, private keys, personal data, or
  confidential source content unless the user explicitly approves that content class for
  this preview.
- Escape untrusted strings before inserting them into HTML.
- Do not add forms, write actions, or browser-to-agent callbacks. Ask for feedback in the
  conversation.

## Preview workflow

1. Create or update the artifact with the normal file-editing tool. Keep the filename
   stable across revisions.
2. Confirm that the target resolves to an existing regular file or directory inside the
   private session directory.
3. Invoke `ropen -q <absolute-path>` with the path passed as one quoted argument. The
   current CLI does not document an end-of-options marker, so reject any unresolved or
   option-like target rather than inventing one.
4. Report what the user should now see. Do not print or ask the user to open the internal
   live-mount URL.
5. Ask the user to provide feedback in the conversation.
6. For an update, rewrite the same artifact and call `ropen -q` on the same absolute path
   so the browser tab refreshes.

Opening or refreshing the browser is the only expected external effect. A request to show
or preview an artifact authorizes that effect; it does not authorize any other browser
interaction.

## Failure behavior

If `ropen` fails:

1. Capture its exit status and a bounded stderr excerpt.
2. Recheck `ropen --help` and `ropen --version` for an invocation mismatch.
3. Report the smallest useful diagnosis.
4. Do not start a localhost server, expose a port, alter networking, or switch to another
   transport without a new user decision.

The artifact remains available locally so the user can choose the next action.
When an artifact already exists, state that it was preserved and include its local path.

## Cleanup

Keep the session directory while revisions are active. When the preview session finishes,
validate the exact path and remove only that session directory. Never target the runtime
root, `/tmp`, a repository root, a home directory, or a path derived from an unresolved
variable. Tell the user when a retained preview contains sensitive approved content and
confirm its cleanup.

## Completion report

State:

- which artifact was opened or refreshed;
- that `ropen` handled browser routing and live reload;
- that feedback remained in chat;
- whether the private preview directory was removed or intentionally retained for another
  revision.

When no preview opened, replace the normal completion report with the failed precondition,
the preserved artifact path when one exists, and the fact that no fallback transport started.

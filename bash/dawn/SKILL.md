---
name: dawn
description: Use whenever the user asks to open, view, review, edit, or share a local Markdown file in Dawn, and whenever you create or meaningfully update a user-facing local Markdown document. Generate a Dawn link proactively before reporting the work complete. Also use it for a local CSV, TSV, JSON, or JSONL file the user asks to see, or that is itself the deliverable they asked for.
---
<!-- Dawn-managed Agent Bridge skill -->

# Dawn Agent Bridge

Dawn turns a local Markdown file into a clean browser link the user can open in an agent's built-in browser. It does the same for data files: a CSV or TSV opens as a table, JSON as fields, and JSONL as records, each editable in place.

## When to use Dawn

- When the user asks to open, view, review, edit, or share any local Markdown file.
- Whenever you create or meaningfully edit a user-facing local Markdown file, even when the user did not explicitly ask for Dawn.
- Before reporting Markdown work complete, so the link is part of the handoff.

Use Dawn for all user-facing local Markdown by default. Present at most ONE Dawn link per user-facing deliverable. Do not create links for incidental agent configuration, generated files, internal skill files, or throwaway Markdown unless the user explicitly asks to open them.

For data files, link only when the user asks to open, view, review, edit, or share one, or when the CSV, TSV, JSON, or JSONL file is itself the deliverable they asked for (a table they wanted built, a dataset they asked you to collect). Never link a data file you only read, a lockfile, a package manifest, your own config, or a log you wrote along the way.

## Create the link

Use the Dawn-managed command, which does not depend on the agent's shell PATH:

```bash
"$HOME/.local/bin/dawn-bridge" url <absolute-path-to-file>
```

If that file is missing, try the plain command and then Dawn's private fallback:

```bash
dawn-bridge url <absolute-path-to-file>
'/Users/juanbenjumea/Library/Application Support/co.getdawn.dawn/bin/dawn-bridge' url <absolute-path-to-file>
```

Present the returned URL exactly as printed, as the primary way for the user to open the file. It may be a `dawn.localhost` link or a direct local bridge link. Do not invent Dawn URLs, expose discovery files, or place raw filesystem paths in Dawn URLs.

Dawn links are durable and keep working across restarts. If a Dawn link doesn't open — the page won't load, says "This link isn't available", or shows something that isn't Dawn — re-run `dawn-bridge url` on the same file and give the user the link it prints. It is the same document; the new link may differ only in its port (another app can be holding Dawn's usual one).

## Run the command in the least restricted lane you have

This command needs nothing from the workspace: it reads two files in the
user's own Dawn data directory and talks to Dawn on this machine. If your
harness lets you choose how a command runs, run this one unsandboxed or with
network access from the FIRST attempt — that turns the common case into a
single clean call instead of a failure and a retry. If your harness only offers
escalation after a refusal, do not pre-emptively ask for it: a plain attempt
succeeds outright wherever local connections are allowed, and asking first
would put a permission prompt in front of users who never needed one.

## Recover from an agent sandbox

If the command reports that Dawn Bridge access was blocked by the agent sandbox:

1. Immediately retry the same command through the agent's native permission or escalation mechanism, allowing access to local services or running it outside the sandbox.
2. When asking, state what the call is — an escalation reviewer that cannot identify the destination should decline, and this one is identifiable: a loopback HTTP request to `127.0.0.1` on the port named in the error, served by the user's own Dawn process on this machine. It sends the absolute path of the file to open plus a local registration secret from the user's app-data directory. No remote host is contacted and nothing leaves the device.
3. When supported, request the narrowest persistent approval — loopback access to that one port, or the Dawn bridge executable — so future links work without another prompt.
4. Do not restart the helper, repeat ordinary sandboxed retries, or tell the user to repair Dawn for this error.

The native approval is the recovery flow. If you cannot request permission, or the user declines, do NOT show the raw error and move on — the user cannot act on it and will assume Dawn is broken.

Speak to them as a person, not as a network stack. Never put an IP address, a port, "loopback", or "sandbox" in a sentence aimed at the user: those name the mechanism, not the action, and a non-technical reader cannot act on any of them. Name the permission the way THEIR agent names it, and say what you are waiting for. For example: "I need your OK to connect to Dawn before I can make the link — approve the permission request and I'll do it. Dawn runs on your Mac, so nothing is sent to the internet." If your harness shows an approval prompt, say that it is coming; if approval lives in a settings screen, name that screen. Then fall back to the file path for this turn so the work is still usable.

Rules:

- Use this only for local files Dawn opens: Markdown (`.md`, `.markdown`, `.mdown`, `.mkd`), CSV (`.csv`, `.tsv`), JSON (`.json`), and JSONL (`.jsonl`, `.ndjson`).
- Keep the original file path available as a fallback.
- If Agent Bridge is disabled, just use the file path this time and ask the user to enable Agent Bridge in Dawn.
- Suggest repair only when an authorized retry still fails and `dawn-bridge doctor`, run with the same permission, reports a genuine setup problem.

---
name: install-mcp-server
description: Install and configure a new MCP server for Claude Code, including discovery, auth verification, credential-safe setup, scope placement, registration, sync, and restart/testing expectations.
---

# Install MCP server

Install a new MCP server into Claude Code, avoiding common pitfalls.

## Arguments

`$ARGUMENTS` contains the server name, GitHub URL, npm package, or a description of the service the user wants to connect (e.g. "Gmail", "Notion", "Jira"). If empty, ask what service they want to connect.

## Local placement authority

Before choosing scope, use `/Users/pablostafforini/My Drive/dotfiles/claude/context/mcp-servers.md` as the source of truth for this setup:

- User-level MCPs belong in `~/.claude.json` top-level `mcpServers`; after any user-level add/remove, run `/Users/pablostafforini/My Drive/dotfiles/claude/bin/sync-mcp-servers.sh`.
- Shared project MCPs belong in the project's `.mcp.json`.
- Do not use `~/.claude.json`'s `projects.<path>.mcpServers` block for project-scoped MCPs.

## Step 1: Discovery

Find the right MCP server for the requested service.

1. **If the user provided a specific package or URL**, use that directly.
2. **If the user described a service**, search for MCP servers that support it:
   - Check https://github.com/modelcontextprotocol/servers for official/community servers
   - Search npm (`npx` servers) and PyPI (`uvx` servers)
   - Search GitHub for `<service> MCP server`
3. **Check for duplicates**: Run `claude mcp list` to see what's already installed. If a server for this service already exists, tell the user and ask if they want a replacement or addition.

Present the candidate(s) to the user with:
- Name and URL
- What tools/services it provides
- How auth works (OAuth, API key, token, none)
- Whether it's official (from the service provider) or community-built

An explicit request to install the identified server already authorizes its
routine local installation and registration. Ask only when choosing a materially
different server, replacing an existing configuration, or adding external setup
not covered by the request.

## Step 2: Auth verification (before installing)

This is the most important step. Many MCP servers have auth mechanisms that are locked to specific platforms or require non-trivial setup. Investigate BEFORE spending time on installation.

Check the server's README, source code, or docs for:

1. **OAuth client ID**: Is it built-in or user-provided?
   - If built-in: check whether it's restricted to a specific platform (e.g. Gemini CLI, Cursor, VS Code). Look for domain restrictions, app verification status, or platform-specific cloud functions in the auth flow. **If the OAuth client is platform-locked, STOP and tell the user this server won't work with Claude Code.**
   - If user-provided: the user will need to create their own OAuth app in the service's developer console. Document what's needed.
2. **API key / token**: Straightforward — just needs the key. Check where to get one.
3. **No auth**: Proceed directly.
4. **Credential shape**: Identify the exact env vars, headers, config files, or OAuth flags the server needs. Decide how each secret will be supplied before registration. Do not put raw secret values in shell commands, command output, tracked files, or chat.

**If auth requires creating OAuth credentials, GCP projects, or other setup**: explain exactly what's needed and get confirmation before proceeding.

## Step 3: Install dependencies

Based on the server type:

### npm/npx server
- These typically need no local installation — `npx -y <package>` runs them directly.
- Check package identity and metadata with `npm view <package> version repository bin --json` before execution. `npx ... --help` executes package code and some MCP servers ignore that flag; use it only when documented and with a bounded timeout.

### Python/uvx server
- These typically need no local installation — `uvx <package>` runs them directly.
- Check the package's registry metadata and documented entry point before execution. `uvx ... --help` runs the package, so use it only when documented and with a bounded timeout.

### Git repo (needs cloning and building)
- Clone only a repository the user has explicitly requested or approved by name
  or URL. Use `~/repos/mcp-servers/<name>/`; keep new repositories, builds, and
  dependency trees outside Google Drive.
- Run `npm install && npm run build` (or equivalent).
- **Important**: If the entry point is a built/bundled JS file, verify it exists after the build.

## Step 4: Determine the command

Do not use bare interpreter names like `node`, `python`, or `python3` as the command. Claude Code spawns MCP servers as child processes without a shell, so shell functions (e.g. nvm's lazy-loading `node` wrapper) and PATH-dependent lookups may fail silently.

Use these rules:
- **npx/uvx servers**: `npx` and `uvx` are usually real binaries. Verify with `command -v npx` / `command -v uvx`. If they resolve to shell functions, use absolute paths.
- **Node.js servers**: Use the absolute path to the node binary. Find it with:
  ```bash
  command -v node  # Check if it's a function or binary
  which -a node    # Find all candidates
  ```
  On this system, check `/opt/homebrew/bin/node` first. Confirm that the selected
  executable exists and meets the server's Node version requirement; do not
  assume the hard-coded path or a shell function will work in a child process.
- **Python servers**: Use the absolute path or `uvx` (which is a real binary).

## Step 5: Register with Claude Code

### Scope
- **`-s user`** (global): Available in all projects. Use this by default for generally useful servers. The canonical source is `~/.claude.json`; after adding or removing a user-level server there, run `/Users/pablostafforini/My Drive/dotfiles/claude/bin/sync-mcp-servers.sh` so the configured account files receive the change.
- **`-s project`** (shared project): Writes the current project's `.mcp.json`. Use this for project-specific servers that should be available to agents working in that repo. No account sync is needed.
- **`-s local`** (private local): Claude CLI's default, but it stores project-local config in a hidden per-path block. Do not use it for normal project-scoped servers in this dotfiles setup. Use it only if the user explicitly asks for a private, unshared local exception, and document that exception.

Ask the user which scope they want if not obvious.

Before running a user-scope command, check whether `CLAUDE_CONFIG_DIR` is set. If it is, do not assume `claude mcp add -s user` will update canonical `~/.claude.json`; run the command with the canonical config environment or edit `~/.claude.json` deliberately, then sync.

### Credentials before registration

If the server needs an API key, token, OAuth client secret, or header:

1. Create or locate the credential before `claude mcp add`.
2. Follow the owning account's secrets context for the credential source,
   approved broker and per-process injection path. Do not substitute another
   account's vault, service account or broker. Claude expands `${VAR}`
   references; it does not resolve `op://` values natively. Use the owning
   account's approved launcher or existing approved parent-process injection.
   For HTTP headers, inject resolved values into the parent environment and
   use the documented variable expansion. Verify resolution without printing
   values.
3. Never pass a raw secret value in `claude mcp add -e KEY=value`, where it
   can enter shell history, process arguments, or logs. A non-secret reference
   is usable only when an explicit resolver is present; do not pass literal
   `op://...` text to an ordinary server expecting a resolved API key.
4. For account-specific credentials, keep canonical `~/.claude.json` free of raw secret values, put the per-account values or references in the corresponding account configs, and verify they are still present after any sync. Do not print the values while checking.

### Registration command

```bash
# For npx servers:
claude mcp add -s user <name> -- npx -y <package>

# When the owning account's context specifies this broker interface:
claude mcp add -s project <name> -- /absolute/path/to/approved-broker run --env-file /absolute/path/.env.op -- /absolute/path/npx -y <package>

# For node servers (absolute path!):
claude mcp add -s user <name> -- /opt/homebrew/bin/node /path/to/server/dist/index.js

# For uvx servers:
claude mcp add -s user <name> -- uvx <package>

# For HTTP/SSE servers:
claude mcp add -s user --transport http <name> <url>

# For project-scoped servers:
claude mcp add -s project <name> -- npx -y <package>
```

### HTTP/SSE URL formatting

Use the exact endpoint and transport documented by the server, including its
path and any required trailing slash. There is no universal slash rule; adding
`/` can change the route or introduce a redirect. Check current server/client
documentation and the protocol response before changing the endpoint.

### Sync and verify registration

After adding, run:

```bash
/Users/pablostafforini/My\ Drive/dotfiles/claude/bin/sync-mcp-servers.sh  # only for -s user changes to canonical ~/.claude.json
claude mcp list
```

The server must appear in `claude mcp list` output (not `claude mcp get`, which reads config rather than runtime health). This command checks actual runtime health. It may spawn stdio servers from `.mcp.json`, so run it only from a directory you trust.

**Do NOT rely on `claude mcp get <name>`** — it reads saved configuration,
which does not establish runtime availability. If a saved server is absent from
`claude mcp list`, investigate account, scope, policy, and connection state.

If the server doesn't appear in `claude mcp list`:
1. Check the active account, scope, exact endpoint, transport, executable, and
   redacted diagnostic errors.
2. Check the documented MCP initialization flow. A generic HTTP 401 only shows
   an authentication challenge; it does not prove the route is an MCP server.
   A connection failure may be DNS, TLS, network, or startup failure rather than
   a wrong URL.
3. Correct the demonstrated configuration error and recheck. Preserve the prior
   configuration; do not remove and re-add a working entry speculatively.

Expected statuses in `claude mcp list`:
- `✓ Connected` — connection established; still verify the intended tool.
- `! Needs authentication` — configured but not ready. Complete the documented OAuth flow before claiming the server works.
- Not listed — unavailable in the inspected runtime; determine whether account,
  scope, policy, disabled state, or a configuration error explains it.

## Step 6: Restart and test

`claude mcp list` verifies the saved configuration and server health from the shell. It does not hot-load new MCP tools into an already running Claude Code session.

Use the installed client's documented reconnect/reload path if it can expose
the tools in the current session. Otherwise test in a fresh session you can
start without interrupting the current one, or report the remaining restart
gap. Test with a simple read-only operation:
- Gmail: search for recent emails
- Calendar: list today's events
- Drive: search for a file
- etc.

If the server requires OAuth, use the documented authentication route (such as
`/mcp`); do not assume the first tool call will complete authentication.

## Step 7: Final credential check

Before reporting success, confirm credential handling is complete:

1. Check the relevant config files without printing secret values.
2. Confirm raw secrets are not present in the shell command you will report, tracked files, or command output.
3. If the credential is process-env based, confirm the restart requirement is explicit.

## Step 8: Report

Tell the user:
1. Server name and scope (`user`, `project`, or explicitly requested `local`)
2. Which tools were actually exposed and successfully tested, distinguishing any unverified ones
3. Config file touched (`~/.claude.json` or `.mcp.json`) and whether `/Users/pablostafforini/My Drive/dotfiles/claude/bin/sync-mcp-servers.sh` was run
4. Any remaining reload/restart or documented OAuth authentication requirement
5. How to remove it: `claude mcp remove <name> -s <scope>`

## Common pitfalls (for reference)

| Pitfall | Symptom | Fix |
|---|---|---|
| Incorrect HTTP endpoint | Connection or protocol initialization fails | Use the server's documented exact endpoint and transport |
| Verifying with `claude mcp get` instead of `claude mcp list` | Looks OK but server doesn't actually work | Always use `claude mcp list` to verify |
| Unresolved interpreter command | Server cannot start | Select a verified absolute executable with the required version |
| Platform-locked OAuth | "This app is blocked" in browser | Server is unusable with Claude Code; find alternative |
| Native module ABI mismatch | Server crashes on startup | Rebuild with the same node version you're running |
| Wrong scope | Server unavailable where requested | Correct scope to the user's intended target; sync only for canonical user-level changes |
| Used default `-s local` for a project server | Server is hidden in per-path config instead of `.mcp.json` | Re-add with `-s project` |
| User-level change not synced | Works in one Claude account but not others | Run `/Users/pablostafforini/My Drive/dotfiles/claude/bin/sync-mcp-servers.sh` and restart affected sessions |
| Raw secret in `claude mcp add -e` | Secret may leak through history/logs/config | Use a reference with an explicit resolver or approved environment injection |
| Literal `op://` passed to server | Authentication fails | Add the account-appropriate resolver; Claude does not resolve 1Password references |
| Space in path | Server fails to start | Preserve the executable and each argument as separate correctly quoted values |

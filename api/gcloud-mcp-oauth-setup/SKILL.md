---
name: gcloud-mcp-oauth-setup
description: "Create a Google Cloud project, enable its APIs, configure the OAuth consent screen and client, and register a remote Google MCP server (Drive, Gmail, Calendar and similar) with OAuth in Claude Code. Use when user says 'create a gcloud project for an MCP', 'configure the Google Drive MCP', 'set up a Google Workspace MCP', 'register a remote MCP that needs a Google OAuth client', 'criar projeto gcloud e configurar mcp', or 'configurar mcp do google drive'. Do NOT use for MCP servers that need no OAuth, for stdio servers, or for non-Google OAuth providers."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Google Cloud project + remote MCP with OAuth

Turns a vendor guide for a remote Google MCP server into a working Claude Code entry. The project and APIs are created with `gcloud`. The consent screen and OAuth client have no `gcloud` path for this case, so they are done in the Cloud console, driven by browser automation while the user signs in.

The code is the truth: confirm every command, flag and UI label against the live tool or page before stating it as fact. The console labels in [references/console-oauth.md](references/console-oauth.md) were observed in pt-BR and may drift.

## Inputs to fix first

| Variable                    | Meaning                                                  | Example                                           |
| --------------------------- | -------------------------------------------------------- | ------------------------------------------------- |
| `SERVICE_API` and `MCP_API` | APIs the vendor guide lists                              | `drive.googleapis.com`, `drivemcp.googleapis.com` |
| `MCP_URL`                   | Remote endpoint, Streamable HTTP                         | `https://drivemcp.googleapis.com/mcp/v1`          |
| `SCOPES`                    | OAuth scopes from the vendor guide                       | `.../auth/drive.readonly .../auth/drive.file`     |
| `CALLBACK_PORT`             | Free local port, same value in Google and in Claude Code | `8765`                                            |
| `SERVER_NAME`               | Letters, digits, hyphen, underscore only                 | `aipp-drive`                                      |

## Steps

1. **Read the docs.** Fetch the vendor guide and the Claude Code MCP docs, with quotes. Treat anything the pages do not state as unknown. Note whether the service is Preview and needs a program sign-up.
2. **Inspect the environment, read-only.** Run `gcloud auth list`, `gcloud config list`, `claude mcp list`. Test each account with `gcloud projects list --account=<account>`, because the active account can have an expired token while another works. Check whether the project `.mcp.json` is a symlink.
3. **Ask the user** (interactive question tool, with the reason for each question):
   - Which Google account owns the project. It decides which data the MCP reads and whether the consent screen is Internal or External.
   - Where to register the server: user scope, or the versioned `.mcp.json`.
4. **Create the project and enable the APIs.** Pass `--account` on every command so the active gcloud account never changes.

   ```sh
   PROJECT_ID="<prefix>-$(date +%y%m%d)-$(openssl rand -hex 2)"
   gcloud projects create "$PROJECT_ID" --name="<Name>" --account=<account> --quiet
   gcloud services enable $SERVICE_API $MCP_API --project="$PROJECT_ID" --account=<account>
   gcloud services list --enabled --project="$PROJECT_ID" --account=<account> \
     --filter='config.name:(<api1> OR <api2>)' --format='value(config.name)'
   ```

   Proof: the final list shows both APIs. "Operation finished" alone is not proof.

5. **Pick the callback port.** Check `ss -ltn` for a free port. The Google redirect `http://localhost:<CALLBACK_PORT>/callback` and the Claude Code `callbackPort` must match.
6. **Configure consent screen, scopes, test user and client in the console.** Open the console URL in the browser tool and let the user sign in. The agent never handles the password or 2FA. Follow [references/console-oauth.md](references/console-oauth.md), including the "AI-powered agent" checkbox and the save pitfalls.
7. **Register the server through the CLI.** The client secret enters only through the CLI and is never written to `.mcp.json`.

   ```sh
   cfg=$(jq -cn --arg id "$CLIENT_ID" '{type:"http",url:"<MCP_URL>",oauth:{clientId:$id,callbackPort:<PORT>,scopes:"<SCOPES, space separated>"}}')
   MCP_CLIENT_SECRET=$(jq -r .web.client_secret <downloaded.json>) \
     claude mcp add-json --scope project --client-secret <SERVER_NAME> "$cfg"
   ```

   - Names with `:` are rejected. Use a hyphen.
   - The CLI refuses to write through a symlinked `.mcp.json` (`SymlinkWriteRefusedError`). Run it from the directory that holds the real file.
   - The CLI reformats the whole file. Restore short arrays and the final newline so the diff shows only the new entry.
   - Keep `clientId` literal. Environment expansion inside `oauth` fields is not documented.

8. **Verify the registration without printing secrets.**

   ```sh
   claude mcp get <SERVER_NAME>        # expect: client_id configured, client_secret configured
   rg -c 'GOCSPX' <mcp json file> || echo none
   git diff --stat
   ```

9. **Clean up secret-bearing artifacts.** The downloaded JSON and the browser tool's snapshots hold the secret.
   - Delete the browser output folder and screenshots.
   - If `rm` is aliased to `trash`, the files stay in the trash. Check it and delete them for real with `/bin/rm`. If a safety hook blocks that, hand the exact command to the user.
   - Stop background processes and confirm the callback port is free. Do not use `pkill -f` with a pattern that matches the shell itself. Write `[c]laude` instead of `claude`.
10. **User approves and authenticates.** A server from `.mcp.json` stays "Pending approval" until the user opens `claude` in that directory and approves it. Then run `/mcp`, select the server and sign in with an account listed as a test user. An unverified-app warning is expected in test mode. Google says the settings can take from 5 minutes to a few hours to apply.
11. **Validate with a real tool call**, such as searching for a known file. A "Connected" status in `claude mcp list` is a hint, not proof.

## Known risks

- Developer Preview services can require a program sign-up. Enabling the API does not prove the account was accepted.
- Google needs `access_type=offline` to issue a refresh token. The Claude Code docs do not show how to send it. If sign-in repeats about every hour, this is the likely cause.
- The vendor warns about indirect prompt injection, because the server can read and change account data. Review actions before approving them.

## Client ID versus client secret

- The client ID is a public identifier (RFC 6749 section 2.2). It appears in every authorization URL and may be committed. Alone it cannot obtain tokens for a web client, because the token exchange needs the secret.
- The client secret must never be committed, printed or placed in a command argument. Supply it through the environment, at registration time only.
- A committed entry only works for whoever holds the secret. Other people or machines get an entry that cannot authenticate. Use user scope when the entry is personal.

## Output

Report, in this order: what is proven (command output), what changed (files, with the diff size), what the user still has to do, and risks still open. Do not claim the MCP works until step 11 passes.

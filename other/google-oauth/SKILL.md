---
name: google-oauth
description: >
  Use when a Google integration (Gmail, Docs, Sheets, Drive, Calendar) needs its
  OAuth client set up, its refresh token obtained again after expiry, or an
  access token minted at runtime. Use when adding a Google account or choosing
  among several accounts.
version: 1.1.0
---

# Google OAuth

`charliebot google` reads the account table, sends authenticated requests, lists accounts and adds accounts.

## Configuration

- Credentials location: `$CHARLIEBOT_HOME/credentials.yaml`; the default home is `~/.charliebot`.
- The `google` section holds the OAuth client and the default account.
- The default account name is `google.name`, or `default` when that key is absent.
- Each added account uses a `google_account_<name>` section.
- Account names match `[a-z][a-z0-9-]*` and are unique across the table.
- An added account can hold its own `client_id` and `client_secret` pair.
- An account section can set `owner`: the person that the account belongs to.
- The `google` section belongs to the host owner, the person who runs this CharlieBot.
- An added account without `owner` belongs to the owner of the `google` section.
- When one section sets `owner`, the `google` section sets `owner` too.
- On a host with a Discord list, each `owner` value is a person name from `discord.allowed_users`.
- On a host that serves several people, `slack.allowed_user_ids` lists only the host owner.
- Each owner has one primary account.
- The primary account of the host owner is the default account.
- The primary account of another person is that person's section with `primary: true`, or that person's only section.
- `google.docs_default_folder_id` applies only to the default account.
- Access tokens are minted at runtime and are not persisted.

## Runtime Requests

Send every Google API request through `charliebot google request`, which mints the account's access token inside its own process:

```bash
charliebot google request <METHOD> <URL> [--account <name>] [--data-file <path> | --json <text>] [--header <name:value>]...
```

The token never appears in a command, in an output, in a run record or in model context.
For the default account, omit `--account`.
`--json` sends the text as the request body with `Content-Type: application/json`; `--data-file` reads the body from a file; each `--header` adds one header.
The command prints the response body on stdout.

| Exit code | Meaning |
|---|---|
| 0 | HTTP 2xx; the response body is on stdout. |
| 1 | Another HTTP status, a network failure, or a token refresh failure, including a pending account. |
| 2 | Invalid arguments, or an invalid account table in `credentials.yaml`. |
| 3 | `credentials.yaml` cannot be read. |

Redirects are not followed: a 3xx answer exits 1 with its status, so an unexpected redirect is visible.

## Accounts

A host holds one or more Google accounts. Each account has a short name, unique on the host.

- `charliebot google list` prints each account's name, mark, status, owner and description.
- `charliebot google list --check` adds each account's email address; a pending account keeps its row with an empty address.
- The mark is `default` for the default account and `primary` for the primary account of another person.

Choose the account before each Google API call:

- When the request names an account, use that account.
- Match the request words against each account name and description.
- The asker is the person who sent the request.
- In a Discord thread, the asker is the `person` that `charliebot discord read` gives for the request.
- Outside Discord threads, the asker is the host owner.
- When the request names no account, use the primary account of the asker.
- When the asker owns no account, stop, and say that this host holds no Google account of the asker.
- In a Discord thread, give email addresses of the asker's accounts only.
- When the request words match no account, stop and show the account list.
- Name the account behind any Google data you show, including unchecked accounts and the write draft.

## Add or Re-Authorize an Account

The account owner gives consent in a browser. Only the owner can do this step.

1. Run `charliebot google consent-url <name>`. When you know the email address of the account, add `--email <email address>`.
2. Send the URL to the account owner. When the email address is still unknown, ask the owner for it in the same message.
3. The owner signs in to that account and approves.
4. The owner copies the full URL from the browser address bar after the redirect to `http://localhost`.
5. Run `charliebot google exchange-code <name> --email <email address> --redirect-url '<redirect URL>' --description '<one line>' [--owner <person>]`.
6. Report the email address that `exchange-code` prints.

When the `google` section sets `owner`, pass `--owner` with the person name of the account owner.

`exchange-code` writes the token only when the consenting account has the given email address.

Two consent errors mean that the OAuth client does not admit the account:

- The error `org_internal`: the OAuth client accepts only users of its organization.
- The error `access_denied` with "The app is currently being tested": the client is in Testing, and the account is not a test user.

A client admits the account when one of these conditions is true:

- Its project has the Internal user type, and the account belongs to the project's organization.
- Its project has the External user type and the Production status. An unverified client shows a warning and admits at most 100 new users.
- Its project has the Testing status and lists the account as a test user.

A Google Workspace administrator can block a client for the accounts of the organization.
When Google shows one of these errors, choose a Desktop-app client that admits the account.
Put its `client_id` and `client_secret` into the `google_account_<name>` section.
Then start again at step 1.
Two OAuth clients can carry one app name, and the consent page shows that name.
The name alone does not identify the client: compare the `client_id` values.
In the report to the account owner, name the blocking client by its `client_id`.

## Bootstrap / Re-Authorization

1. In Google Cloud Console, enable the APIs you need (Gmail, Docs, Sheets, Drive, Calendar).
2. Create an OAuth client of type **Desktop app**.
3. Follow **Add or Re-Authorize an Account** to authorize an account. The consent flow requests these scopes:

```text
https://www.googleapis.com/auth/spreadsheets
https://www.googleapis.com/auth/documents
https://www.googleapis.com/auth/drive.file
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/calendar
```

If the GCP project is in Testing mode, the refresh token expires in about seven days. Publish the OAuth consent screen to Production for non-expiring tokens.

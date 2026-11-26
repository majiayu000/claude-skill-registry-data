---
name: google-account
description: Read before signing a Google account in to Gmail, Google Chat, Google Calendar, Drive, Docs, Sheets or Slides, or out of one, and when one of those apps says an account needs signing in.
metadata:
  title: "Google Account"
  subtitle: "Sign in to Google once"
  about: "Signs your Google accounts in to Gmail, Google Chat, Google Calendar, Drive, Docs, Sheets and Slides, and out again. Each account you add is yours alone."
  category: Connectors
---

Each Google app (gmail, google-chat, google-calendar, google-drive, google-docs, google-sheets, google-slides) uses its person's Google
accounts through this one. `apps` lists the ones the person has.

- A Google account is one item of their Vault, "Google <address>", which every Google app they have uses. It's
  listed under Accounts in the Vault, which is where a person adds one (Add Account) and deletes one.
- `sign_in` gives a link: give it to the person to open in their browser. Google signs them in, for every Google app they have, and sends them back to the network's
  address, which finishes it. Nothing is pasted back. With `account`, Google suggests that one: use it for an account
  that needs signing in again, which the Vault shows with a dot and Sign In.
- Signing out is deleting the account's item, which soft delete keeps for 30 days.
- `accounts` lists the accounts, each with whether it can be used now. Every tool of a Google app takes
  `account`: an address, or a part only it has. Left out, it's the first `accounts` lists.

The first sign-in needs the item "Google client", in the person's Vault or, for everyone without one, in the
network's (`ONE_SUBJECT=network`), as a workplace keeps one for its staff, where nobody then sets anything up: `client_id` (not secret) and
`client_secret` of a Google Cloud OAuth client of the Web application kind, whose authorized redirect URI is the
network's address followed by `/vault/callback`, with `oauth2.googleapis.com` its site, where its secret goes. When
you make the client in a browser of yours, save it straight from there with `vault_save_from_browser` (the client's
JSON download, `client_id` from `web.client_id` with `secret: false` and `client_secret` from `web.client_secret`,
`hosts: ["oauth2.googleapis.com"]`), never reading it, and have the person (for the network's, an owner) switch it on for Google Account in the
Vault, since an app signs in only with a client switched on for it. On its OAuth consent screen (Google Auth Platform, Branding), the Privacy policy link is
the network's address followed by `/privacy`, the page every network serves naming its owner; once that's set,
publish the app In production (Audience), unverified, so Google stops signing its accounts out every 7 days; or,
where everyone signing in is in the Google Workspace that owns the project, make its Audience Internal, which needs
neither. When the person has it, ask for it with `vault_request`;
never ask for it in the chat.

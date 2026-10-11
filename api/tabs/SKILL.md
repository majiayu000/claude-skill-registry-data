---
name: tabs
description: Use this skill when the user is building a tab inside a Microsoft Teams app on Teams SDK 2.1 — serving a static page with `app.tab()`, calling the agent from the page with `@microsoft/teams.client` and `app.function()`, using TeamsJS (`@microsoft/teams-js`) for context and dialogs, acquiring tokens with Nested App Authentication (NAA) and MSAL. Triggers on "Teams tab", "static tab", "configurable tab", "app.function", "teams.client", "Nested App Authentication", "TeamsJS".
---

# Tabs — web pages inside Teams

Two pieces, two packages — do not mix them up:

- **Server (`@microsoft/teams.apps`)** — `app.tab(name, dir)` serves a built single-page app; `app.function(name, handler)` exposes REST functions the page can call with an Entra token.
- **Browser** — `@microsoft/teams-js` (TeamsJS) is the Teams host API: context, theme, dialogs, tab configuration. `@microsoft/teams.client` is a separate class built on TeamsJS and MSAL: it starts both, acquires tokens, calls Graph, and calls the server's functions.

The CLI template `tab` (`teams project new typescript my-tab -t tab`) wires all of this with Vite and React.

## 1. Serve the page

```ts
import path from 'node:path';

app.tab('settings', path.resolve('dist/client'));    // served at /tabs/settings
```

`app.tab` mounts the directory at `https://<bot-host>/tabs/<name>`; scopes default to `personal`. Build the SPA into `dist/client` and keep it out of the server bundle.

## 2. Manifest

Tabs are declared in the manifest (`teams app manifest download|upload|update`, see `cli-recipes`):

```jsonc
{
  "staticTabs": [{
    "entityId": "settings",
    "name": "Settings",
    "contentUrl": "https://<bot-host>/tabs/settings",
    "scopes": ["personal"]
  }],
  "configurableTabs": [{
    "configurationUrl": "https://<bot-host>/tabs/configure",
    "scopes": ["team", "groupChat"]
  }],
  "validDomains": ["<bot-host>"]
}
```

Without the host in `validDomains` the Teams client refuses to render the page. A configurable tab needs a configuration page that calls `pages.config.setConfig` and `setValidityState(true)` through TeamsJS.

## 3. The client library

```ts
import * as teamsJs from '@microsoft/teams-js';
import { App as ClientApp } from '@microsoft/teams.client';
import * as endpoints from '@microsoft/teams.graph-endpoints';

const clientId = String(import.meta.env.VITE_CLIENT_ID);    // the Entra app that backs the tab

async function boot() {
  const app = new ClientApp(clientId, {
    msalOptions: { prewarmScopes: ['User.Read', 'Team.ReadBasic.All'] },   // explicit scopes; `.default` does not work on Teams desktop
  });
  await app.start();                                         // initialises TeamsJS and MSAL

  const context = await teamsJs.app.getContext();            // theme, user, channel, ...
  const me = await app.graph.call(endpoints.me.get);         // typed Graph client with the user's token
  const reply = await app.exec<{ conversationId: string }>('post-to-chat', { message: `Hello from ${me.displayName}` });
  return { context, reply };
}
void boot;
```

- `app.start()` fails outside Teams (the TeamsJS initialisation rejects or times out). Catch it and show an "open in Teams" message in a browser.
- `app.graph.call(endpoints.…)` uses the same endpoint builders as the server (`graph-integration`).
- `hasConsentForScopes(scopes)` tests, `ensureConsentForScopes(scopes)` tests and prompts.
- `prewarmScopes` asks for consent at start; `false` disables it. The scopes must belong to one resource.

## 4. Functions — call the agent from the page

```ts
app.function<{ message: string }>('post-to-chat', async ({ data, send, getCurrentConversationId, log }) => {
  log.info('post-to-chat called');
  await send(data.message);                                    // into the conversation the tab runs in
  return { conversationId: await getCurrentConversationId() };
});
```

The function is served at `POST /api/functions/post-to-chat`. The SDK validates the Entra bearer token before the handler runs (401 otherwise). Context values from the caller (`chatId`, `channelId`, `teamId`, `pageId`, `meetingId`, …) are **not** validated — only `userId`, `tenantId` and `authToken` come from the token. Check access yourself before acting on them, and validate `data`. A returned number is an HTTP status code; a string, object or array is the body.

## 5. Nested App Authentication with plain MSAL

When you do not use `@microsoft/teams.client`, create an MSAL client that talks to the Teams host instead of opening a popup:

```ts
import { createNestablePublicClientApplication } from '@azure/msal-browser';

async function getGraphToken(clientId: string) {
  const msal = await createNestablePublicClientApplication({
    auth: { clientId, authority: 'https://login.microsoftonline.com/common' },
  });
  const accounts = msal.getAllAccounts();
  const result = await msal.acquireTokenSilent({ scopes: ['User.Read'], account: accounts[0] });
  return result.accessToken;
}
void getGraphToken;
```

If `acquireTokenSilent` throws `interaction_required`, fall back to `acquireTokenPopup` or a sign-in button. The Entra app registration needs the nested-app redirect URI and its SPA platform set up — see `authentication`.

## 6. Dialogs from a page

TeamsJS opens and closes URL dialogs:

```ts
import * as microsoftTeams from '@microsoft/teams-js';

function pickValue() {
  microsoftTeams.dialog.url.open(
    { title: 'Pick a value', url: 'https://<bot-host>/tabs/picker', size: { width: 400, height: 300 } },
    (result) => { console.log('dialog closed', result); },
  );
}
void pickValue;
```

The picker page calls `microsoftTeams.dialog.url.submit(value)`. Dialogs opened by the bot are in `dialogs`.

## Common pitfalls

- **The tab is blank in Teams** — `validDomains` misses the host, or the build output path in `app.tab` is wrong (404 on `/tabs/<name>`).
- **`teams.client` or TeamsJS rejects in a browser** — expected outside Teams.
- **TeamsJS functions imported from `@microsoft/teams.client`** — the client package has its own `App` class; context, pages and dialogs come from `@microsoft/teams-js`.
- **A function answers 401** — the token audience does not match the app, or the call came without a bearer token.
- **A configurable tab does not save** — `setValidityState(true)` was never called.
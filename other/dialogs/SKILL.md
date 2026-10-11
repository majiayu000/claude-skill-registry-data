---
name: dialogs
description: Use this skill when the user is building dialogs (task modules) in a Microsoft Teams bot on Teams SDK 2.1 — opening a dialog from a card with `OpenDialogData`, handling `dialog.open.<id>` and `dialog.submit.<action>`, returning an Adaptive Card or a web page, multi-step flows, dialogs opened from message extensions. Triggers on "Teams dialog", "task module", "modal in Teams", "dialog.open", "dialog.submit", "OpenDialogData".
---

# Dialogs (task modules)

A dialog is a modal the Teams client opens over a chat. Its body is an Adaptive Card or a web page; when the user submits, control returns to the bot. Two routes and two helpers cover it: `dialog.open.<id>` renders the dialog, `dialog.submit.<action>` receives the result, `OpenDialogData` names the dialog on the button that opens it, `SubmitData` names the action on the button inside it. Both helpers come from `@microsoft/teams.cards`.

## 1. Open a dialog from a card

```ts
import { MessageActivityInput } from '@microsoft/teams.api';
import { AdaptiveCard, OpenDialogData, SubmitAction, TextBlock } from '@microsoft/teams.cards';

app.on('message', async ({ send }) => {
  const card = new AdaptiveCard(
    new TextBlock('Need details? Open the form.', { size: 'Large', weight: 'Bolder' }),
  ).withActions(
    new SubmitAction().withTitle('Simple form').withData(new OpenDialogData('simple_form')),
    new SubmitAction().withTitle('Web page').withData(new OpenDialogData('webpage_dialog')),
  );
  await send(new MessageActivityInput('Pick one').addCard('adaptive', card));
});
```

`OpenDialogData` marks the action as a `task/fetch` request and carries the dialog id used for routing. It is attached to a **`SubmitAction`**; that is what the Teams client requires.

## 2. `dialog.open.<id>` — return a card dialog

```ts
import { cardAttachment } from '@microsoft/teams.api';
import { AdaptiveCard, SubmitAction, SubmitData, TextBlock, TextInput } from '@microsoft/teams.cards';

app.on('dialog.open.simple_form', async () => {
  const dialogCard = new AdaptiveCard(
    new TextBlock('This is a simple form', { size: 'Large', weight: 'Bolder' }),
    new TextInput().withId('name').withLabel('Name').withIsRequired().withPlaceholder('Enter your name'),
  ).withActions(
    new SubmitAction().withTitle('Submit').withData(new SubmitData('simple_form')),
  );

  return {
    task: {
      type: 'continue',
      value: {
        title: 'Simple form',
        card: cardAttachment('adaptive', dialogCard),
      },
    },
  };
});
```

The buttons inside a dialog are `Action.Submit` too. `SubmitData('simple_form')` makes the click arrive at `dialog.submit.simple_form`. `dialog.open` (without an id) is a catch-all; prefer one handler per dialog id.

## 3. `dialog.submit.<action>` — collect the result

```ts
app.on('dialog.submit.simple_form', async ({ activity, send }) => {
  const name = activity.value.data.name;
  await send(`Hi ${name}, thanks for submitting the form!`);
  return { task: { type: 'message', value: 'Form was submitted' } };   // closes the dialog with a final message
});
```

Return values:

- `{ task: { type: 'message', value: '…' } }` closes the dialog and shows the text.
- `{ status: 200 }` closes it silently.
- `{ task: { type: 'continue', value: { title, card } } }` swaps the body — a multi-step flow.

## 4. Multi-step dialogs

Carry earlier answers forward through the extra data of `SubmitData`:

```ts
import { cardAttachment } from '@microsoft/teams.api';
import { AdaptiveCard, SubmitAction, SubmitData, TextBlock, TextInput } from '@microsoft/teams.cards';

app.on('dialog.submit.step_one', async ({ activity }) => {
  const name = activity.value.data.name;
  const next = new AdaptiveCard(
    new TextBlock('Email', { size: 'Large', weight: 'Bolder' }),
    new TextInput().withId('email').withLabel('Email').withIsRequired(),
  ).withActions(
    new SubmitAction().withTitle('Submit').withData(new SubmitData('step_two', { name })),
  );
  return { task: { type: 'continue', value: { title: `Thanks ${name}`, card: cardAttachment('adaptive', next) } } };
});

app.on('dialog.submit.step_two', async ({ activity, send }) => {
  const { name, email } = activity.value.data;
  await send(`Hi ${name}, we will write to ${email}.`);
  return { status: 200 };
});
```

## 5. Web-page dialogs

Serve the page from the bot with `app.tab(...)` and return its URL. The page must be public, load `@microsoft/teams-js`, and its domain must be in the manifest's `validDomains`.

```ts
import path from 'node:path';

app.tab('dialog-form', path.resolve('dist/dialog-form'));          // served at /tabs/dialog-form

app.on('dialog.open.webpage_dialog', async () => ({
  task: {
    type: 'continue',
    value: {
      title: 'Web page dialog',
      url: `${process.env['BOT_ENDPOINT']}/tabs/dialog-form`,    // your public https origin, set in .env
      width: 1000,
      height: 800,
    },
  },
}));

app.on('dialog.submit.webpage_dialog', async ({ activity, send }) => {
  await send(`Got ${activity.value.data.email}`);
  return { status: 200 };                                          // closes the dialog
});
```

Inside the page, submit with TeamsJS and include the `action` field so the router can find the handler:

```ts
import * as microsoftTeams from '@microsoft/teams-js';

async function submitForm(email: string) {
  await microsoftTeams.app.initialize();
  microsoftTeams.dialog.url.submit({ action: 'webpage_dialog', email });
}
void submitForm;
```

Add the domain to the manifest through the CLI, for example `teams app manifest update <teamsAppId> --set-json validDomains='["bot.example.com"]'`. (`teams app update --endpoint` adds the bot's own domain on its own.)

## 6. Dialogs from message extensions

An action command with `fetchTask: true` does not use `dialog.open.*`. The route is **`message.ext.open`**; the response has the same `task` envelope. See `message-extensions`.

## Common pitfalls

- **The dialog never opens** — `OpenDialogData` sits on an `ExecuteAction` or on a card that was not sent through the SDK; use a `SubmitAction`.
- **Submit reaches no handler** — the route is `dialog.submit.<action>` where `<action>` is the first argument of `SubmitData`; it is not the dialog id of `OpenDialogData` unless you reuse the same string.
- **The web page is blank or 404** — its host is not in `validDomains`, or the page is not publicly reachable.
- **`activity.value.data` is empty** — the inputs have no id, or a web page submitted without an `action` field.
- **The dialog stays open** — the handler returned nothing; return `{ status: 200 }` or a `task` response.
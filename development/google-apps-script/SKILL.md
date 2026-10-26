---
name: google-apps-script
description: Use when automating Gmail, Drive or Sheets with Google Apps Script developed locally in TypeScript with clasp — minimal OAuth scopes, time-driven triggers, quotas, idempotent daily jobs, deploying the same code to several Google accounts, and testing logic outside Apps Script. Also use when a script hits "Service invoked too many times", a trigger stops firing, emails arrive duplicated or not at all, or authorisation must be redone.
---

# Google Apps Script with clasp

Default: TypeScript in a git repository, `clasp` to push, pure logic in modules tested with Node, Apps Script services touched only in thin adapters, explicit minimal scopes in `appsscript.json`, triggers created by code.

## Setup

```bash
npm i -D @google/clasp typescript
npx clasp login                 # per Google account
npx clasp create --type standalone --title "my-automation"
npx clasp push
```

- Keep `.clasp.json` (script ID) per account/deployment, e.g. one file per account that a deploy script copies into place before `push`.
- Recent clasp versions do not transpile TypeScript themselves; compile with `tsc` (or a bundler) to plain JS first and push the output.

## Scopes

Declare scopes explicitly in `appsscript.json` (`oauthScopes`) — e.g. read-only mail access plus permission to send mail — rather than letting the editor infer broad ones. Narrow scopes are enforcement: the script cannot delete what it cannot write.

## Triggers and idempotency

- Create time-driven triggers from a `setup()` function (`ScriptApp.newTrigger("run").timeBased().atHour(7).everyDays(1).create()`), deleting existing ones first so reruns do not duplicate.
- Make daily jobs idempotent: record "sent for date D, target T" in `PropertiesService`, and on rerun send only what is missing.
- Provide a one-time `setupAccount()` that the account owner runs once in the editor: it grants consent, installs triggers and sends a first result. Google requires the owner's interactive consent; it cannot be automated away.

## Quotas

- Services have daily and per-minute quotas (e.g. Gmail reads). Search with narrow queries, fetch only needed fields, and process in pages with `Utilities.sleep` between batches.
- Each execution has a maximum run time; split long work across trigger runs and keep a cursor in properties.

## Mail delivered to yourself

When sending a digest from an account to an address that forwards back to the same mailbox, the provider may keep only the sent copy and nothing appears in the inbox. Send to the mailbox you actually read, and include a distinct subject per logical recipient so each digest can be identified and audited.

## Testing

- Keep classification, formatting and date logic in pure functions; test with Node's test runner using fixtures shaped like Apps Script objects.
- Add an audit function that lists what was sent today and what is missing, and run it after each deploy.

## Verification loop

1. `tsc` builds; unit tests pass.
2. `clasp push`; run `setup()` once; check triggers in the project's trigger list.
3. Run the job manually; confirm the result arrives where expected and a second run sends nothing new.

## Pitfalls

- **Trigger owner:** triggers run as the user who created them; deploying under another account needs that account's login and consent.
- **Time zone:** set `timeZone` in `appsscript.json`; date math otherwise uses the project default.
- **Silent failures:** enable failure notifications for triggers and log to the execution log.
- **Global code runs on every invocation;** keep top-level statements free of side effects.

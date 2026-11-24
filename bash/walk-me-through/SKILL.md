---
name: walk-me-through
description: "Use when a step truly needs a human: credentials, dashboards, provisioning, one-off cutovers. Never for what an agent can do. Show the script before anyone runs it."
user-invocable: false
---
# Walk me through
Gate: get the user's OK before committing the script, and show it before anyone runs it (G2). See gates.md in the skill house-rules.
Job: Replace repeated explanation with a script that walks a person through what only they can do.
Takes: repo inspection and a procedure.   Gives: a Node script, disposable unless repeatable.

A person runs this script. An agent never does.

## Steps

1. Scope it from the repo: env files, framework settings, and all the secrets the CI setup reads. For a migration, also pin down the current state, the target state and every irreversible step.
2. Confirm the ordered stages with the user.
3. For each value, record where it comes from, where it goes and whether it is secret.
4. Write exact instructions. If you are unsure what a page looks like, ask or check its docs. Never invent a step.
5. Make a folder holding a copy of `scripts/walk-lib.js` from this skill, unedited, and a stages file beside it. Disposable scripts go in the bench's `notes/`, repeatable ones in the repo. Paths in the stages are relative to where the person runs it, so state that folder.
6. Author the stages, keeping these rules:
   - Show the page before asking for its value.
   - Use hidden input for every secret.
   - Put a yes-no gate before each irreversible step.
   - One stage does one job a stranger could follow.
7. Verify without running it:
   - `node --check` on the stages file.
   - The repo's linter, if it has one.
   - Trace each value by reading: asked once, written to the right place, and each secret name matches what CI reads.
8. Show the script. Say the command the person should run. Delete it afterwards unless it is repeatable.

## Stages file

Stages are functions passed to `walk`, so a syntax error surfaces before anyone is asked anything.

```js
const { walk } = require('./walk-lib');

walk({
  title: 'Payments cutover',
  stages: [
    {
      name: 'Create the live key',
      run: async (w) => {
        w.open('https://example.com/dashboard/keys');
        w.say('Choose Create key, name it "ci", and copy it.');
        const key = await w.secret('PAY_KEY', 'Paste the key', { envFile: '.env.local' });
        w.env('.env.local', 'PAY_KEY', key);
        w.ciSecret('PAY_KEY', key);
      },
    },
  ],
});
```

## The library

| Call | Does |
|---|---|
| `w.say(text)` | Prints a line |
| `w.open(url)` | Opens a browser on Windows, macOS, Linux or WSL, and always prints the address |
| `await w.ask(name, question)` | Visible input, remembered and offered on the next run |
| `await w.secret(name, question, { envFile })` | Hidden input. Stored nowhere by the library; `envFile` lets Enter keep a value already there |
| `w.env(file, key, value)` | Sets one key, idempotent, leaves other lines alone. Private on creation where the OS supports it. Warns if git doesn't ignore the file |
| `w.ciSecret(name, value, { host })` | Writes a CI secret over stdin. `host` is `github` by default, or `gitlab`. If the CLI isn't ready, it notes a to-do |
| `await w.pause(text)` | Waits for Enter |
| `await w.yesNo(question)` | Returns true on yes. The default is no |
| `w.todo(text)` | Adds a manual leftover to the closing summary |
| `await w.showAndWait(text)` | Shows an instruction and waits |
| `await w.askAndRecord(name, question)` | Asks, and prints `name=answer` in the summary |

The library clears to a fresh screen for each stage, shows how far along it is, and ends with a summary of values by name, writes and manual leftovers. Secrets never appear in the summary.

## Human-driven signals

The skill `root-cause-hunt` uses this library when a failure can only be seen by a person. Those scripts use only `showAndWait` and `askAndRecord`. The answers reach the agent, so sign-ins stay instructions and are never asked for.

## Done when

- Every value has a known origin, destination and secrecy.
- Every secret uses hidden input, and every irreversible step has a gate.
- `node --check` passed, and each value and CI secret name was traced by reading.
- Someone new to the repo could complete each stage from its text alone.
- The script was shown, and no agent ran it.

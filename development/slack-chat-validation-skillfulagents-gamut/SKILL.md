---
name: slack-chat-validation
description: Run the live Slack chat-integration validation suite — a real Slack account messaging a real bot, driving a real app instance and a real container, asserting on what actually lands in Slack. Use before and after any change to src/shared/lib/chat-integrations/, to the user-input request path that feeds it, or to the "can't do this in chat" notice.
---

# Slack chat-integration validation

## Why this exists

Every other test around `src/shared/lib/chat-integrations/` is a **contract test**:
it hands a connector an event object and asserts what the connector does with
it. That pins the connector's behaviour and nothing else. If a refactor stops
the host from *emitting* those events — or emits them for a different session,
or stops registering the underlying request — every one of those tests stays
green and the feature is dead.

This suite closes that gap. Nothing on the path is mocked:

```
a real human Slack account
  → real Slack (Socket Mode)
    → a real app instance booted against an isolated data dir
      → a real agent container running a real turn
        → back to Slack
          → assertions read the actual message, Block Kit payload included
```

Run it **before** starting a chat-integration change to record a green
baseline, and **after** to prove nothing regressed.

## Prerequisites

Checked automatically by `preflight.mjs`; run that first when anything looks off.

1. **A source install with exactly one Slack integration.** By default
   `~/Library/Application Support/Superagent-dev`. Its bot and app tokens are
   read from the integration row; they are never printed.
2. **A second Slack identity that can post as somebody other than the bot.**
   Resolved from `connected_accounts` in the source install, then in the
   packaged install (`…/Superagent`). Two shapes work, and which one is found
   decides the surface:
   - **human (user) token** → the suite runs in a **DM with the bot**. Preferred:
     it's how the feature is really used, and only a human identity can open a
     `D…` channel.
   - **another app's bot token** → the suite runs in a **shared public channel**.
     Slack won't let one app post into another app's DM. The sender joins a
     public channel the bot is already in if it isn't in one.

   Composio-managed connections usually **do not** expose a raw token (Composio
   returns a redacted one). That is expected: the harness falls back to
   executing Slack calls through Composio's proxy, and a token Slack rejects
   with `invalid_auth` is treated as "try the proxy", not "dead connection".
   If no identity resolves at all, reconnect Slack in the app's
   connected-accounts UI — the harness picks a human token up automatically on
   the next run, no code change needed.
3. **Docker running**, with the agent image named in the source install's
   `settings.container.agentImage` (normally `superagent-container:latest`,
   built by `npm run build:container`).
4. **No other Superagent instance holding the same Slack app.** Slack
   load-balances events across Socket Mode connections, so a second instance
   makes the suite go nondeterministically quiet. Preflight flags a running
   packaged/dev app whose data dir has an active Slack integration.
5. **A free container publish range.** See the port hazard below.

## Running it

```bash
node e2e/live/slack-chat/preflight.mjs        # ~10s, proves the environment
node e2e/live/slack-chat/run.mjs              # full suite, web host (~5 min)
node e2e/live/slack-chat/run.mjs --host=electron   # desktop host
node e2e/live/slack-chat/run.mjs --no-public-url   # cloud host, no HOST_PUBLIC_URL
```

Useful flags:

| Flag | Effect |
|---|---|
| `--only=<tag or ids>` | Run a subset: `--only=unsupported`, `--only=question`, `--only=inbound-turn,question-card` |
| `--host=web\|electron` | Which host shape to boot (default `web`) |
| `--no-public-url` | Boot the cloud host with `HOST_PUBLIC_URL` unset |
| `--public-url=<url>` | Override the cloud base (default `https://validation.example.test`) |
| `--boot-only` | Seed + boot + connect, then stop. Environment check without spending turns |
| `--keep-app` | Leave the app running afterwards for manual poking |
| `--no-retry` | Disable the one automatic retry per check |
| `--with-computer-use` | Include the computer-use check — **drives the real machine** |
| `--channel=#name` | Pin the channel when the surface is a channel |
| `--container-base-port=N` | Move the container publish range (default 5300) |
| `--source=<dir>` / `--sender-source=<dir>` | Point at other installs |

Each run writes `report.json` and the full app log to a temp run dir, printed
at the end.

### A full pass before a chat-integration change

```bash
node e2e/live/slack-chat/run.mjs                   # 12/12
node e2e/live/slack-chat/run.mjs --host=electron   # 12/12 — desktop links
node e2e/live/slack-chat/run.mjs --no-public-url --only=unsupported   # link omitted
```

## What it isolates (and what it will never touch)

`seed.mjs` builds `~/Downloads/slack-chat-validation` from the source install:
`settings.json` verbatim, a fresh single-agent workspace, and a copy of the
SQLite file pruned to **one** chat integration retargeted at the slug
`slack-validation-agent`.

That slug is the isolation boundary. The only container the suite ever creates,
stops, or removes is `superagent-slack-validation-agent`. Scheduled tasks,
webhook triggers, other integrations, and every other agent's rows are emptied
in the copy, so the seeded install can't wake anything on its own. **The source
install is only ever read.**

## What each check protects

| Check | Protects |
|---|---|
| `inbound-turn` | An inbound Slack message creates a chat session bound to a real container session whose transcript holds the turn |
| `question-card` | `AskUserQuestion` renders as Block Kit with one button per option, `answer_<n>` action ids, and values that carry the request, question and answer |
| `question-answered-in-app` | The card posted to Slack and the request the **app** answers are the same registry entry: answering through the app's decision route settles it and the continuation lands back in Slack |
| `question-freetext-reply` | A plain-text reply to an open single-question card settles it and the agent responds — and the report says **which** path ran (answer-in-turn vs cancel → fresh turn) |
| `question-cancelled-by-unrelated-message` | An unrelated message cancels the parked question instead of deadlocking behind it, and the fresh turn runs |
| `question-multi-is-not-consumed-by-text` | A multi-question ask posts one card per question, and text does **not** answer it (an answer would be attributed to the wrong question) |
| `file-delivery-notice` | `deliver_file` reaches the conversation as real uploaded bytes with the description as caption (text fallback accepted and reported) |
| `unsupported-*` (7) | Per kind: the exact refusal wording, the **exact host-aware link tail**, no interactive card, and the request staying parked in the registry |

`unsupported-capability-review` is the newest row and the one with the least
margin: `workflows: 'review'` is the shipped default, so asking the agent to run
a workflow parks a capability review — which chat was silent about entirely
before the connectors moved onto the unified request wire. It needs the agent to
actually reach for the `Workflow` tool, so it is the row most likely to need its
retry.

`question-freetext-reply` reports its path rather than asserting one, because
the two are connector-dependent: the free-text **answer** path needs
`answerOpenQuestionWithText`, which only the Telegram connector implements. On
Slack the same message legitimately takes the **cancel** path. Both settle the
request and both get a reply, so a check that only asserted "the agent
answered" would stay green if the answer path broke outright — which is what
the previous version of this check did.

The `unsupported-*` checks are the regression test for the host-aware notice
(PR #563). They rebuild the expected tail from the host shape and assert the
message **ends with it**, so all three rows of that matrix are distinguished:

| Host | Expected tail |
|---|---|
| `--host=electron` | ` Open Gamut on your desktop to continue: superagent-dev://agent/<slug>/sessions/<id>` |
| `--host=web` + `HOST_PUBLIC_URL` | ` Open Gamut to continue: <base>/agents/<slug>/sessions/<id>` |
| `--host=web --no-public-url` | ` Open Gamut to continue.` (no link — never a broken URL) |

The `<id>` is asserted to be the conversation's **actual** session, which is
what stops a queued notice from linking a rotated-away session.

## Known limits — read before trusting a green run

- **Button taps are not automated.** Slack has no API to simulate clicking a
  Block Kit button; interactions only arrive from a real client over Socket
  Mode. The suite asserts the card is posted with the right buttons and
  `action_id`s, and covers a real decision via `question-answered-in-app` (the
  app's decision route settles the same registry entry the Slack card came
  from). The `action_id` → decision round trip still needs a human tap.
- **The already-handled gate is not live-reachable on Slack.** A press on a card
  whose request was settled elsewhere must be refused rather than buffered in
  the container. Reaching it needs an interactive response, which on Slack means
  a button tap — and the free-text branch does not produce one, because Slack
  has no `answerOpenQuestionWithText`. That gate is covered instead by the
  wire-contract suite in `chat-integration-e2e.test.ts`, which drives the real
  persister and the real registry.
- **`browser_input` is not asserted as parked** (`requiresParked: false`).
  `mcp__user-input__request_browser_input` is only in the web-browser
  subagent's tool list, so the main agent reaches it indirectly and the
  registration can settle with the subagent. The notice is still asserted.
- **Computer use is opt-in** (`--with-computer-use`) because triggering it
  drives the real machine.
- **`proxy_review` cards are not covered.** They arrive through the global
  notification path as a synthetic `question_request`, and triggering one needs
  a proxied API call that requires review.
- **One retry per check by default.** Each check drives a live model, and a
  model that wanders off is not the product breaking. A real regression fails
  both attempts. `--no-retry` disables it.

## Environment hazards these runs actually hit

- **Container publish range.** A packaged install's Lima runner forwards its
  container ports on `127.0.0.1`, and a loopback-specific bind **shadows**
  Docker's `0.0.0.0` publish. With the default base (4000) the validation app's
  host→container calls silently land in the *other* install's container and
  come back `401 Unauthorized` — which reads exactly like a broken build.
  The harness pins `SUPERAGENT_BASE_PORT=5300` (away from 4000 and from
  `dev:electron`'s 5000) and preflight checks the range is free.
- **`better-sqlite3` ABI.** The web and Electron hosts need different builds, so
  whichever ran last leaves the other broken. `startApp` rebuilds for the host
  about to run.
- **Electron outliving its wrapper.** `electron-vite dev` forks Electron;
  killing the wrapper alone leaves the app holding the Socket Mode session and
  writing into the seed dir (the next seed then fails with `ENOTEMPTY`). The
  harness kills the process group and then pkills any Electron whose app path is
  this repo, and the seed retries its clear.
- **Electron ignores `PORT`.** Main binds its own API from 47891 upward, so the
  harness reads the port back from the log line rather than assuming it.

## Extending it

Add an entry to `CHECKS` in `e2e/live/slack-chat/lib/checks.mjs`:

```js
{
  id: 'stable-kebab-id',
  title: 'reads as the behaviour being protected',
  tags: ['group'],            // selectable via --only
  async run(ctx) { /* ... */ return 'short detail for the report' },
  async cleanup(ctx) { /* leave the session idle */ },
}
```

`ctx` gives you `conv` (say / awaitBot / expectNoBot, watermarked), `api`
(sessions, messages, `pendingRequests` — the Phase 6 registry snapshot),
`agentSlug`, `integrationId`, and `hostShape`.

Two rules worth keeping:

1. **Predicates must be specific enough to fail.** An early version matched the
   delivered file on its filename alone and passed on the `🔧 Write` tool-call
   echo — a green check that tested nothing. If the agent echoes your marker for
   an unrelated reason, the check is not doing its job.
2. **Watch the registry from before the trigger**, not after the Slack message
   lands (`watchRegistry`). A request can register and settle inside one poll
   interval, and polling afterwards reports "never registered" for something
   that did.

## Files

```
e2e/live/slack-chat/
  preflight.mjs       environment check, no side effects beyond joining a channel
  run.mjs             the runner: seed → boot → checks → report
  lib/data-dir.mjs    read-only access to an install's settings + SQLite
  lib/slack.mjs       bot and sender identities, token vs Composio-proxy calling
  lib/surface.mjs     DM vs shared channel, and how the sender gets in
  lib/seed.mjs        the isolated data dir
  lib/app.mjs         booting web/electron, port discovery, API helpers
  lib/conversation.mjs watermarked send/await against the conversation
  lib/checks.mjs      the assertions
```

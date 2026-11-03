---
name: irises-setup-hermes
description: "Install Irises — a user-facing front-end (web chat / CLI, plus the engine bridge) that uses this hermes as its deep-work engine. Explains it, checks prerequisites, asks the person's questions and a clear yes, runs the installer, gets the gateway restarted the safe way for where you are talking, and verifies the result."
version: 3.0.0
author: Irises
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Irises, assistant, persona, frontend, setup]
prerequisites:
  commands: [git, node, npm]
---

# Irises Setup (hermes engine) — install it, on the person's yes

**You install Irises, from your own terminal, once the person has said yes.** Your job is to explain
what Irises is, check that the box can run it, ask the few questions that are theirs to answer, run
the installer, get the gateway restarted the safe way, and verify the result.

The one thing that needs care is the **gateway restart** at the end. Hermes reads the API server and
the bridge plugin only when its gateway starts, so the install is not live until that restart. How it
happens depends on where this conversation is running — check that first (step 0), because getting it
wrong kills your own turn mid-reply.

## What Irises is (say this in your own words)

A user-facing texting assistant — a fast conversational front line — that delegates ALL deep work
(research, email, files, reminders, memory) to this hermes. This hermes stays completely unmodified;
Irises talks to it only through the OpenAI-compatible API server (`API_SERVER_ENABLED`) and the cron
REST API.

Irises rides **on top of** this hermes: on boot it auto-detects it (sets `OPS_BACKEND=hermes`),
reuses this hermes's API key, and makes its own voice **inherit this hermes's provider, endpoint and
model** — including when this hermes runs on an OpenAI-compatible or otherwise obscure API (OpenAI,
Azure, vLLM, deepseek-direct, Groq, a self-hosted gateway…), not just OpenRouter or Anthropic. The
voice runs this hermes's OWN model on every lane it can reach — no stand-in slug is substituted — so
chat turns cost and pace what this hermes's model does; deep work uses that same model, as always.
There is nothing to configure by hand.

## 0. Where are you running? (decides the restart)

```bash
echo "gateway=${_HERMES_GATEWAY:-0}"
```

- **`gateway=0` — the hermes terminal chat (`hermes` in a shell).** You are not inside the gateway, so
  the installer can restart it for you and your turn survives. Run the install without
  `--no-gateway-restart`; the restart is part of it.
- **`gateway=1` — a messaging chat (Telegram, WhatsApp, Discord, Signal…).** You are a child of the
  gateway. A restart from here would kill this very turn, which is why your terminal guard refuses
  one. Run the install **with `--no-gateway-restart`**, report the result, then ask the person to
  type **`/restart`** in this chat. `/restart` is hermes's own command: it lets running turns finish,
  restarts the gateway, and tells them when it is back. (The installer also skips the restart on its
  own whenever it sees `_HERMES_GATEWAY=1` — pass the flag anyway, so your command says what it does.)

## 1. Check the prerequisites (read-only)

```bash
node --version          # needs 22.13+ (Irises's local store uses the builtin node:sqlite)
git --version
curl --version
hermes gateway status
hermes config get model.default     # the model Irises's voice will inherit (step 2)
hermes config get model.provider
hermes config get model.base_url
```

Those three are the only config values you read. **Never read `model.api_key`, and never print
`~/.hermes/.env` or any other file with a key in it** — you name a key, you never show one.

If `node --version` is below 22.13, look for a newer Node already on the box (nvm under
`~/.nvm/versions/node/`, or Homebrew) and tell the person which one to put on `PATH`. Do not install
Node or any system package yourself — stop and tell them what is missing.

On **Windows**, your terminal already runs commands in Git Bash, which is the shell the installer
needs. Say the honest part up front: the Windows paths (the Git Bash install, the `Irises` Task
Scheduler task) are stub-tested only, and this may be the first real run. Linux and macOS are the
platforms with mileage on them.

## 2. Ask, explain, and get a clear yes

Ask only what is theirs to decide, and offer the default:

- **Which chats should Irises front?** Default `*:*` — every chat on every platform this hermes
  speaks, including their operator and control chats. A narrower answer becomes `--front`, e.g.
  `--front 'telegram:*'` or `--front 'telegram:*,whatsapp:+1555*'`.
- **Port?** Default 3000. Anything else becomes `--port N`.
- **Timezone?** Default the host's own. Anything else becomes `--tz Europe/Paris` (an IANA zone).

Then tell them, before you run anything:

- **Which model and API Irises will use.** The person cannot pick these here (the terminal menu asks;
  this install keeps the default), so say them plainly, with the real values from step 1:
  - **Engine: this hermes.** Deep work — research, email, files, reminders — is handed to you and
    runs on your model, exactly as it does today.
  - **Her voice** (every chat reply, plus two small helper calls per turn) **inherits your model, on
    your API and your key**: `<model.default>` via `<model.provider>` at `<model.base_url>`, paid
    from the key you already use — name it (`OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY` or
    `OPENAI_API_KEY` in hermes's `.env`), never its value. Say the consequence too: every chat turn
    now costs and paces like one of your turns, so a large, slow or reasoning model makes her chat
    slower and dearer.
  - **The exception.** If the provider is one Irises cannot call directly — `bedrock`, `vertex`,
    `gemini`, `copilot`, `nous`, `moa` — or the provider is empty or one Irises does not know and the
    model id has no `/` in it, her voice cannot inherit: it runs on Irises's own default models instead, on whichever
    OpenRouter, Anthropic or OpenAI key hermes's `.env` has. If it has none of those, her voice has
    no model until they add one. Deep work still runs on your model either way. Say which case
    applies before they say yes.
  - **Want a different voice model?** That takes its own API key, which never travels through chat.
    After the install, in their own terminal:
    `IRISES_MODEL_API_KEY=… bash ./scripts/configure.sh --model-lane openrouter --model-slug <id>`
    (or `anthropic`; `openai` also needs `--model-base-url`). It stops her borrowing your key;
    `bash ./scripts/configure.sh --model-inherit` hands her voice back to your model.
- **What changes in this hermes:** its `.env` gets `API_SERVER_ENABLED` and `API_SERVER_KEY` (if the
  API server is not on already), `IRISES_URL`, `IRISES_FRONT`, `IRISES_PUSH_TOKEN` and
  `IRISES_BRIDGE_TOKEN`, after a backup next to the file. Every key is recorded in
  `~/.irises/install-manifest.json`, and the uninstall takes each one back out. The bridge plugin goes
  into hermes's plugin folder. No hermes source code is touched.
- **What gets installed:** a clone in `~/irises`, its npm dependencies and build, and a user-level
  service (`systemd --user` on Linux, a LaunchAgent on macOS, a Task Scheduler task named `Irises` on
  Windows) so she survives a reboot. Her data lives in `~/.irises`. No database, no root.
- **The gateway restarts at the end** (or on their `/restart`, from a messaging chat). Any hermes chat
  in flight ends there. Hermes then posts its own *"♻️ Gateway online"* message in their home channel —
  that is hermes, not Irises, and it can be silenced per platform with
  `<platform>.gateway_restart_notification: false` in hermes's config (theirs to edit, not yours).
- **With bridge mode on, Irises answers the fronted chats** in her own voice and uses you as her
  engine. You stay reachable directly in a terminal, still answer anything `IRISES_FRONT` does not
  cover, and answer everything whenever Irises is down (fail-open, so a broken front never drops
  messages).
- **Shortly after the restart, Irises usually texts first** — a one-time introduction, sent only on a
  chat this hermes has genuinely exchanged messages in before (the "first move", see Notes). A text
  from her out of the blue is the feature working, not a glitch.

**Wait for a clear yes.** "Sounds good" to the explanation is not a yes to the install — ask
"Shall I install it now?" and act on the answer to that.

## 3. Run the install

Clone, unless `~/irises` already holds an Irises clone — then use it as it is (the installer repairs
in place; pulling new code is an update, step 6). Never touch an Irises checkout anywhere else.

```bash
git clone https://github.com/criblaurens/irises ~/irises
```

Then, from inside the clone, the installer in its flag form. `--yes` is required — the interactive
menu (`bash ./scripts/irises.sh`, `npm run setup`) asks questions on a keyboard you do not have, so
never run it.

From the **hermes terminal chat** (`gateway=0`):

```bash
cd ~/irises && bash ./scripts/engine-setup.sh --engine hermes --yes --front '<their answer>'
```

From a **messaging chat** (`gateway=1`):

```bash
cd ~/irises && bash ./scripts/engine-setup.sh --engine hermes --yes --front '<their answer>' --no-gateway-restart
```

Add `--port N` / `--tz ZONE` if they answered with one. Keep the quotes around the `--front` value.

**It takes several minutes** (npm install and two builds). Run it with `background=true` and
`notify_on_complete=true`, or in the foreground with `timeout=600` (your foreground limit). Tell them
it is running and roughly how long, so the silence is not a surprise.

Read the end of the output. The last line is `RESULT: <token>` and the exit code means:
`0` installed and verified · `1` a step failed (the message says which) · `2` a usage mistake in your
command · `4` Irises did not answer `/health` in time · `5` installed, but the gateway did not come
back verified. Relay the summary block in plain words — what is installed, where, and what is left.
On anything but `0`, quote the failing line, point at `~/.irises/logs/server.log`, and stop: do not
retry with different flags or try to fix it by starting things by hand.

## 4. The restart

- **`gateway=0`:** the installer already restarted the gateway; the summary's `gateway:` line says
  `bounced and verified`. Nothing more to do.
- **`gateway=1`:** the summary's `gateway:` line says `NOT restarted`. Ask the person to type
  **`/restart`** in this chat, and to message you once hermes says it is back. That message starts a
  fresh turn — go to step 5 then. If they prefer a terminal, `hermes gateway restart` there does the
  same; you never run it yourself from a messaging chat.

## 5. Verify (read-only)

```bash
curl -s http://127.0.0.1:3000/health
```

Use the port they installed on if it is not 3000. A JSON body with a `version` object is a healthy
install. Its `models` object is what is actually live, so confirm the model in plain words from it:
`models.voice` lists each voice role with its `model`, `provider` and `endpoint`, and
`models.engine` names your deep-work model. If it differs from what you told them in step 2, say so.
If any voice role shows `"configured": false`, her voice has no working key on that lane — tell them
which key it needs (in hermes's `.env`, or `IRISES_MODEL_API_KEY` with `configure.sh --model-lane`),
in their own terminal, never pasted into chat. Then tell them where to talk to her: any fronted chat, the web chat at
`http://127.0.0.1:3000`, or `npm run chat` in the clone for a terminal session. If the health check
fails, point them at `~/.irises/logs/server.log` and the installer's output — do not try to fix it by
starting anything.

## 6. Later: settings, update, uninstall

Same rules for all of these: say what it will change, get a clear yes, run it from `~/irises` with
`--yes`, and **from a messaging chat always add `--no-gateway-restart`** and then ask for `/restart`.

**Change a setting** — the port, the service, which chats she fronts, the model her voice runs on, the
browser chat, the timezone, the dashboard password, or any documented `.env` key, without re-running
the installer:

```bash
bash ./scripts/configure.sh --show              # report only: every setting and where it came from
bash ./scripts/configure.sh --tz Europe/Paris --yes
bash ./scripts/configure.sh --front 'telegram:*' --yes
bash ./scripts/configure.sh --model-inherit --yes   # hand her voice back to this hermes's model
```

`--show` is read-only — run it first when they ask what is set. A change to Irises's own settings
restarts her and checks `/health`; a `--front` or `--port` change can edit this hermes's `.env` and
needs a gateway restart to take effect. Secrets never go on the command line: `--set KEY` with the
value in `IRISES_SET_VALUE`, which the person sets in their own terminal, never in chat.

**Update:**

```bash
bash ./scripts/update.sh
```

It pulls, rebuilds, restarts Irises, and restarts the gateway (skipped with `--no-gateway-restart`).
If the new build fails to compile or come up, it rolls back to the one that was running. Irises checks
for new builds on her own and mentions one once, in chat, when it is waiting.

**Detach** — usually what someone means when they say they want this hermes back:

```bash
bash ./scripts/engine-setup.sh --detach-engine --yes
```

It undoes every engine-side change — the bridge plugin, the keys Irises added, the values it moved,
`IRISES_FRONT` — so **this hermes is left as if Irises had never been installed, except that the
`.bak-irises-*` backup files stay**. Irises herself, her service, the clone and `~/.irises` are left
alone; running the install again attaches her back.

**Uninstall:**

```bash
bash ./scripts/engine-setup.sh --uninstall --yes
```

Stops and unregisters the service, removes the bridge plugin and the engine-side keys the installer
added, and keeps their data. **Deleting the data is theirs to type, never yours:** `--purge-data`
deletes `~/.irises` (memory and database) and cannot be undone — hand them that command
(`--archive-data` alongside it writes a `~/.irises-backup-<timestamp>.tar.gz` first) instead of
running it.

## 7. Never

- **Never restart the gateway yourself from a messaging chat** — not with the hermes CLI, not through
  `systemctl`, `launchctl`, `schtasks`, or process control, not by scheduling it for later. Your
  terminal guard refuses those for a reason; do not route around it. Ask for `/restart`.
- **Never run the interactive menu** (`bash ./scripts/irises.sh`, `npm run setup`), and never pipe
  answers into it.
- **Never install before a clear yes**, and never pass `--purge-data`.
- **Never install system packages** (Node, git, curl) — say what is missing.
- **Never touch another Irises checkout** that already exists somewhere else on this machine.
- **Never edit hermes's config by hand** — the installer makes its own `.env` changes, backed up and
  recorded; anything beyond that (like the restart-notification key) is the person's to change.
- **Never print a secret.** The installer never shows one; do not go looking in the `.env` files.

## Notes

- Details, security notes, and troubleshooting live in `docs/ENGINES.md` inside the clone.
- **Which model is live:** Irises's voice model vs. this hermes's deep-work model show in `/health`,
  on the `/dashboard` overview, and via `npx tsx ./scripts/print-model-map.ts`. Irises will also tell
  the person her model plainly if they ask in chat, and her build, and whether an update is waiting.
  Override any voice role with `<ROLE>_PROVIDER` / `<ROLE>_MODEL_OPENROUTER` / `<ROLE>_MODEL_OPENAI` /
  `<ROLE>_MODEL`, or turn inheritance off with `ENGINE_MODEL_INHERIT=off` (see `docs/ENGINES.md`
  § Model inheritance).
- On its first boot, Irises sends this hermes a one-time **engine-mode onboarding** over the API
  server: how to recognize a delegated request, the reply contract, the full-reach invitation and its
  hard limits (including never messaging the user on any channel itself). Hermes appends it to its own
  SOUL.md by its own hand — nothing in hermes is edited by Irises. To remove it later, tell hermes by
  chat to delete that section; to skip the send entirely, set `ENGINE_ONBOARDING=off` in the Irises
  `.env`. The text is printed by `npx tsx ./scripts/print-engine-doctrine.ts` inside the clone.
- Once after that, Irises makes the **first move**: she asks this hermes what it already knows about
  its user — a normal chat message hermes answers in its own words, nothing in hermes is read or
  edited — and keeps a sanitized version in her own memory so her first words are not cold. Then she
  either texts the user first, **only** on a chat this hermes has genuinely exchanged messages in
  before, or sends nothing at all and folds the introduction into her reply the first time they text
  her. Exactly once per install; skip it with `FIRST_MOVE_ENABLED=false` in the Irises `.env`.

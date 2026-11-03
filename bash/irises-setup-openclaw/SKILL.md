---
name: irises-setup-openclaw
description: "Guide a person through installing Irises — a user-facing front-end (web chat / CLI, plus the engine bridge) that uses this OpenClaw as its deep-work engine. Explains it, checks prerequisites, hands over the exact terminal commands, and verifies afterwards. It does not install anything itself."
metadata:
  {
    "openclaw":
      {
        "emoji": "🌸",
        "requires": { "bins": ["git", "node", "npm"] },
      },
  }
---

# Irises Setup (OpenClaw engine) — a guide, not an installer

**You do not install Irises. The person does, in their own terminal.** Your job is to explain what
Irises is, check that the box can run it, hand over the exact commands, set the right expectations,
and verify the result once they say they are done.

Why it works this way: the installer's last step restarts the gateway, because the plugin and its
token are only read when the gateway comes up — and from your own session that means killing the
supervisor running your turn, mid-reply. So the command belongs in a human's shell, not in yours.

## What Irises is (say this in your own words)

A user-facing texting assistant — a fast conversational front line — that delegates ALL deep work
(research, files, memory) to this OpenClaw gateway. OpenClaw stays completely unmodified; Irises talks
to it only over the Gateway WebSocket `agent` RPC using the existing gateway token.

Irises rides **on top of** this OpenClaw: on boot it auto-detects it (sets `OPS_BACKEND=openclaw`),
reuses the gateway token, and makes its own voice **inherit OpenClaw's model** — so there is nothing
to configure by hand.

## 1. Check the prerequisites (read-only — these you MAY run)

```bash
node --version          # needs 22.13+ (Irises's local store uses the builtin node:sqlite)
git --version
openclaw gateway status
```

That is the entire list of commands you are allowed to run in this skill, plus the health check in
step 5. If `node --version` is below 22.13, tell the person which newer Node already on the box to put
on `PATH` (nvm under `~/.nvm/versions/node/`, or Homebrew) — do not attempt a system install.

On **Windows**, the person needs a bash to run the install in: **Git Bash**, which ships with the Git
for Windows they already need for the clone, or a **WSL2** shell. Say so up front, and say the honest
part too — the Windows paths are stub-tested only and have not yet been run on a real Windows box,
so Linux and macOS are the platforms with mileage on them.

## 2. Hand them the install (they run this, you do not)

```bash
git clone https://github.com/criblaurens/irises ~/irises && cd ~/irises
bash ./scripts/irises.sh
```

The second command opens a menu — install or repair, configure, update, uninstall, status, advanced —
that asks which engine, which chats Irises fronts, which port, whether she runs as a service, and
whether her own voice keeps inheriting this OpenClaw's model, then prints the exact command it is
about to run before running it. `npm run setup` is the same menu.

If they would rather not be asked anything, the one-shot form does the same install with every
default:

```bash
bash ./scripts/engine-setup.sh --engine openclaw --yes
```

`--yes` means non-interactive: assume every default, never prompt. Any folder is fine — the second
command runs from inside whichever one they chose, in a terminal on this machine (Git Bash or WSL2 if
that machine is Windows).

What the script does, so you can answer questions about it:

- checks node 22.13+, git, curl, and that the port is free,
- reads the existing gateway URL + token via `openclaw config get` (no OpenClaw config changes),
- installs the `@openclaw/gateway-client` package into the Irises clone,
- writes the Irises `.env` (mode 600): `OPS_BACKEND=openclaw`, `OPENCLAW_URL`, `OPENCLAW_TOKEN`, a
  generated `ENGINE_PUSH_TOKEN`, and `PORT=3000` (the committed `deploy/app.env` baseline `8080` is
  the Docker image's port). No database — Irises persists to `~/.irises` on its own,
- reuses an `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`, or `OPENAI_API_KEY` from the OpenClaw
  config/environment when present, for Irises's own small voice models,
- installs dependencies and builds; the web client is rebuilt only when it was built before,
- registers Irises as a **user-level service** — `systemd --user` on Linux, a LaunchAgent on macOS, a
  Task Scheduler task named `Irises` on Windows, with a detached `nohup` fallback where none of those
  exists — so she survives a reboot without root,
- waits for her to answer `/health`, then sets up **bridge mode by default**: installs the plugin
  with `openclaw plugins install` and then **prints three variables for the person to set on the
  OpenClaw gateway process themselves** — it edits no OpenClaw config, so until they set them nothing
  is fronted (see the consequences below). The `IRISES_FRONT` value it prints is the one they chose:
  the menu asks which chats Irises fronts, `--front` is the flag form, and the default is `*:*`.
  `--no-bridge` skips the plugin and the printout,
- optionally gives Irises's own voice a model instead of inheriting this OpenClaw's — the menu's model
  step, or `--model-lane` + `--model-slug`. Tell them what that trade is: the voice then runs on the
  key they supply (given through `IRISES_MODEL_API_KEY` in their environment, never as a flag) and
  stops borrowing this OpenClaw's key and endpoint. Deep work still runs on this OpenClaw's model,
- optionally writes two of this clone's own settings, which the menu offers as skippable extras and
  the flags spell `--web on|off` (`WEB_ENABLED` — the browser chat UI and `npm run chat`; unset leaves
  the clone's `.env` alone, and a fresh install has it on) and `--tz ZONE` (`IRISES_TZ` — the wall
  clock she reads; unset means the host's own zone). The admin dashboard's password goes the way the
  model key does: `IRISES_DASHBOARD_PASSWORD` in their environment, never a flag, never printed —
  leaving it blank leaves `/dashboard` answering only this machine rather than changing anything,
- **restarts the gateway last** so the plugin is loaded, and prints a summary with an honest exit code.

## 3. Set these two expectations before they run it

- **The gateway will restart at the end.** Anything in flight there ends. It is what loads the
  plugin; it is not what turns fronting on. Until the variables below are set on the gateway,
  OpenClaw goes on answering its own channels exactly as before.
- **Fronting is theirs to switch on, with three variables on the gateway process.** The installer
  prints them and stops there — they belong in the environment of the **OpenClaw gateway process**
  (its own service/launcher env), not in the Irises clone, and the gateway has to come back up with
  them set:
  - `IRISES_BRIDGE_TOKEN` — the shared secret the plugin authenticates with. The script does not
    print the value (its output gets pasted into chats and issues); its value is
    `ENGINE_PUSH_TOKEN` in the Irises `.env`, mode 600, which they copy across themselves.
  - `IRISES_URL` — where the plugin POSTs inbound messages, `http://127.0.0.1:3000` on a default
    install.
  - `IRISES_FRONT` — comma-separated fnmatch patterns over `<channel>:<conversation>` choosing which
    chats Irises answers. **Empty or unset fronts nothing**: the plugin sits inert. `*:*` fronts
    **everything** — a person texting any channel this OpenClaw owns (WhatsApp, Discord, …) reaches
    Irises, who answers in her own voice and uses OpenClaw as her engine. Tell them their operator
    and control chats are inside `*:*` too, and that blanking it makes the plugin inert again from
    the gateway's next start — that environment is read when the gateway comes up and at no other
    moment, so the change and the restart go together.

  Whatever they set, OpenClaw is unchanged and still reachable directly, still transparently answers
  anything `IRISES_FRONT` does not cover — and answers everything whenever Irises is down (fail-open,
  so a broken front never drops messages).

Also worth saying once: **shortly after fronting is live, Irises usually texts first** — a one-time
introduction, sent only on a chat this agent has genuinely exchanged messages in before (the "first
move", see Notes). A text from her out of the blue is the feature working, not a glitch.

## 4. Never do any of this

- **Never clone, install, build, or start anything.** Not in a temp folder, not "just to check".
- **Never open the menu.** `bash ./scripts/irises.sh` and `npm run setup` are the person's command,
  not yours — it installs, updates, uninstalls and detaches, and every one of those ends in a gateway
  bounce. Hand it over; do not run it, and do not pipe answers into it on their behalf.
- **Never run the setup script or the updater**, and never run any command that restarts or cycles
  the gateway or its supervisor — not through the OpenClaw CLI's own gateway subcommands, not through
  `systemctl`, `launchctl`, `kickstart`, `schtasks`, or direct process control.
- **Never touch another Irises checkout** that already exists on this machine.

## 5. Verify after they report back (read-only)

```bash
curl -s http://127.0.0.1:3000/health
```

Use the port they actually installed on if it is not 3000. A JSON body with a `version` object is a
healthy install. Then tell them where to talk to her: any fronted engine channel, the web chat at
`http://127.0.0.1:3000`, or `npm run chat` in the clone. If the health check fails, point them at
`~/.irises/logs/server.log` and the script's own output — do not try to fix it by starting anything.

## 6. The other commands, for later

All of them are in the same menu (`bash ./scripts/irises.sh`, from the Irises folder), and all of them
are theirs to run, never yours.

**Change a setting** (from the Irises folder, in their terminal) — the port, the service, which chats
she fronts, the model her voice runs on, the browser chat, the timezone, the dashboard password, or
any documented `.env` key, without re-running the installer:

```bash
bash ./scripts/configure.sh --show              # report only: every setting and where it came from
bash ./scripts/configure.sh --tz Europe/Paris   # the wall clock she reads
bash ./scripts/configure.sh --front 'telegram:*'  # which chats she fronts (or --front none)
bash ./scripts/configure.sh --model-inherit     # hand her voice back to this OpenClaw's model
```

Each run previews what it would change, asks once, backs the file up, and writes; a change to one of
Irises's own settings then restarts her and checks the build back off `/health`. This engine keeps
its own wiring, and the script says so rather than pretending otherwise: `--front` cannot apply
itself, because the gateway reads its environment and not a file — it prints the `IRISES_FRONT=…`
line for them to set there and restart the gateway themselves. `--port` likewise moves Irises only,
and warns that `IRISES_URL` was not ours to move: they update it on the gateway process themselves,
or the plugin keeps POSTing at the old port. Hand these commands over and read back what they
report — they are the person's to run, like everything else in this section, and the gateway
restart that follows is theirs too.

**Update** (from the Irises folder, in their terminal):

```bash
bash ./scripts/update.sh
```

It pulls, rebuilds, restarts Irises, and restarts the gateway. If the new build fails to compile or
fails to come up, it rolls back to the build that was running. There is no chat command for it —
Irises will say so herself if asked, and hand over that same line. She does check for new builds on
her own and mentions one once, in chat, when it is waiting.

**Uninstall** (from the Irises folder):

```bash
bash ./scripts/engine-setup.sh --uninstall
```

Stops and unregisters the service, removes the bridge plugin, restarts the gateway, and keeps their
data. `--purge-data` deletes `~/.irises` too, and that is not reversible — `--archive-data` alongside
it writes a `~/.irises-backup-<timestamp>.tar.gz` first, and nothing is deleted if that archive cannot
be written.

**Detach** (from the Irises folder) — the middle rung, and usually the one someone actually wants when
they say they want this OpenClaw back:

```bash
bash ./scripts/engine-setup.sh --detach-engine
```

It undoes every engine-side change — the bridge plugin, any key Irises added, any value it moved — and
bounces the gateway, so **this OpenClaw is left as if Irises had never been installed, except that the
`.bak-irises-*` backup files stay**. On this engine the installer writes no config in the first place,
so what comes out is the plugin; the three gateway variables they set by hand are theirs to unset.
Irises herself is untouched: her service keeps running, the clone stays, and `~/.irises` — her memory
and database — is left alone. They can attach her again later by running the install once more.

## Notes

- Details, security notes, and troubleshooting live in `docs/ENGINES.md` inside the clone.
- On its first boot, Irises sends this OpenClaw a one-time **engine-mode onboarding** over the
  gateway: how to recognize a delegated request, the reply contract, the full-reach invitation and its
  hard limits. The agent saves it to its own instructions by its own hand (nothing in OpenClaw is
  edited). To remove it later, tell the agent by chat to delete that section; to skip the send
  entirely, set `ENGINE_ONBOARDING=off` in the Irises `.env`.
- Once after that, Irises makes the **first move**: she asks this OpenClaw what it already knows about
  its user — a normal chat message the agent answers in its own words, no OpenClaw file is read or
  edited — and keeps a sanitized version in her own memory so her first words are not cold. Then she
  either texts the user first, **only** on a chat this agent has genuinely exchanged messages in
  before, or sends nothing at all and folds the introduction into her reply the first time they text
  her. Exactly once per install; skip it with `FIRST_MOVE_ENABLED=false` in the Irises `.env`.
- Known v1 gap: reminders scheduled through Irises require the hermes engine for now (OpenClaw cron
  wiring is pending), so the reminder tools aren't offered on OpenClaw at all and Irises never
  promises a reminder that can't fire. Everything else runs full-reach here: real code, this agent's
  own skills, parallel subagents, artifacts.
- **Which model is live:** Irises's voice model vs. OpenClaw's deep-work model show in `/health`, on
  the `/dashboard` overview, and via `npx tsx ./scripts/print-model-map.ts`; Irises will also tell the
  person her model, her build, and whether an update is waiting if they ask. OpenClaw's
  `provider/model` slug routes the voice automatically; if this OpenClaw runs on an
  OpenAI-compatible/obscure API, point the voice at it by hand with `<ROLE>_PROVIDER=openai` +
  `OPENAI_BASE_URL` + `OPENAI_API_KEY` (the auto endpoint/key inheritance is hermes-only for now — see
  `docs/ENGINES.md` § Model inheritance).
- The user keeps using OpenClaw directly exactly as before; Irises is an additional,
  differently-voiced front door that uses it as an engine.

---
name: arma-reforger-server-launch
description: Launch an Arma Reforger dedicated server on the user's machine or on a remote one over SSH and prove it is up - ask where it should run, check the target for the server and Node.js, install what is missing with the package manager and SteamCMD (or in Steam), copy tools/ to the target, interview for the settings that matter (public address, RCON, profile and ownerToken, admins, cross-platform, max players, scenario, folder), write and validate server.json, place it next to the executable with a start script, launch outside any sandbox with the working directory set to the server directory, watch the log until "Server registered with address:", check the UDP ports and the A2S answer, then hand over the join code, the port-forwarding rules and the NAT-hairpin warning. Use when asked to set up, launch, start or move a server; when the server or tools are missing on the machine; when the log shows "Missing Addon" / "Can't find '58D0FB3206B6F859' game addon"; when the server never appears in the browser or never registers; when a port looks closed or RCON does not answer.
---

# Launching an Arma Reforger dedicated server

This skill takes a server from "I have a machine" to "players can join, and here is the evidence".
It runs on the machine where the server will live — the user's own or a remote one over SSH — and
everything it checks is checked *there*, because the log, the sockets and the local RCON only exist
on that machine.

The keys, ranges and error strings live in
[arma-reforger-server-config](../arma-reforger-server-config/SKILL.md) and
[the config guide](../../docs/en/ArmaReforger_ServerConfig_EN.md); this skill covers the target
machine, the prerequisites, the interview, the folder layout, the command line, the launch, and the
checks that prove it worked.

## 0. What you are producing

1. A **target** — either this machine or an SSH connection to the remote one — with the server and
   Node.js present (installed in §2 if missing) and the repository's `tools/` copied onto it (§3).
2. A **folder next to the server executable** (default `<serverDir>/<ServerName>/`) that holds
   `config.json`, a start script for the platform, and — if the user chose it — the profile.
3. A **validated `server.json`** whose values are the user's answers, not your guesses.
4. A **running server**, evidenced by the log line `Server registered with address:` and by the
   operating-system socket table on the target.
5. **Instructions**: the join code / address, the ports to open, and the two things that make a
   server look broken (NAT hairpin, and running the server inside a sandbox).

Do not write anything to the config until the interview in §5 is answered. The user's rule is that
these questions are asked *unless they already answered them* — so ask once, in one message, with
the recommended option marked, and skip what the user has already stated.

## 1. Ask first: where does the server run?

This is the first question, before any other. Two answers:

- **On this machine** — the machine the agent is working on. The target is a local shell.
- **On a remote machine over SSH** — a VPS or another host. The target is an SSH session, and you
  need its connection details.

Ask for the remote case:

```
Remote server (SSH):
  host / IP
  user
  port            [22]
  key             [the default key from ssh-agent or ~/.ssh/id_*]
```

Then test the connection **non-interactively** before doing anything else:

```bash
# Linux target
ssh -o BatchMode=yes -o ConnectTimeout=8 -p <port> <user>@<host> 'uname -s; uname -m; id -un'
# Windows target (cmd is the default shell there)
ssh -o BatchMode=yes -o ConnectTimeout=8 -p <port> <user>@<host> 'cmd /c ver'
```

- `BatchMode=yes` fails instead of prompting, which is what you want: an agent cannot answer an
  SSH password prompt, and a password must not be pasted into the conversation or used with
  `sshpass`. If it fails with `Permission denied (publickey)`, ask the user to authorise your key
  (`ssh-copy-id -p <port> <user>@<host>`) or to run the commands themselves; do not try to work
  around it.
- Record the working form once and use it for **every** command below. Write it as
  `TARGET="ssh -o BatchMode=yes -p <port> <user>@<host>"` in your notes (not in the config), and
  remember that quoting through SSH is the usual failure: prefer copying a `.sh`/`.ps1` file to the
  target and running that over trying to nest quotes.
- Check the target's OS and architecture: the dedicated server is x86_64 only, and **ARM64 is
  unsupported** (`uname -m` must be `x86_64`). If `uname` is not found, the login shell is cmd or
  PowerShell — a Windows target, whose commands are PowerShell and where the batch-file caveats in
  §8 apply.

Two environment facts to settle now, because they change the rest of the procedure:

- **Not a sandbox.** On the local machine, launch the server from an unrestricted shell (§8). A
  remote SSH session is not a sandbox — but the remote host itself can be one: a container, a host
  without a CA store, or Steam Linux Runtime on Linux all break the backend (see §9). This is not
  about your tooling; it is about where the process runs.
- **Who owns the ports.** On a home machine, ports are opened on the router (§11.2). On a VPS, the
  host usually has a public IP, so there is no router rule — but the provider's firewall and the
  OS firewall still have to allow the UDP ports (§11.3). Ask which case it is when you get to §11.

## 2. What must already be on the target — check, then install

### 2.1 The check

Run this on the target (wrap it in the SSH form from §1 for a remote one). It answers four things:
is Node.js there and new enough, is SteamCMD available, is the server installed, and can we install
packages.

```bash
# Linux target
SERVER_DIR=/home/steam/reforger/server      # adjust to the target's install path
node --version 2>/dev/null || echo "node: MISSING"
command -v steamcmd || ls /usr/games/steamcmd 2>/dev/null || echo "steamcmd: MISSING"
sudo -n true 2>/dev/null && echo "sudo: passwordless" || echo "sudo: needs a password"
ls -d "$SERVER_DIR" 2>/dev/null || echo "server dir: MISSING"
test -x "$SERVER_DIR/ArmaReforgerServer" && echo "server binary: ok"
test -f "$SERVER_DIR/addons/data/ArmaReforger.gproj" && echo "game addons: ok"
df -h "$SERVER_DIR" 2>/dev/null | tail -1        # the install needs several GB
```

```powershell
# Windows target
node --version
Get-Command steamcmd.exe -ErrorAction SilentlyContinue
Test-Path "$serverDir\ArmaReforgerServer.exe"
Test-Path "$serverDir\addons\data\ArmaReforger.gproj"
```

Interpretation:

- **Node.js is required by the tools, not by the server** — the checks in §3 are plain Node scripts
  and need **Node 18 or newer**. If it is missing or older, install it (§2.2).
- **The server must exist in a directory whose name ends with the install itself**: the binary
  (`ArmaReforgerServer.exe` on Windows, `ArmaReforgerServer` on Linux) next to `addons/`, with
  `addons/data/ArmaReforger.gproj` present. An empty `addons/` is a broken install.
- **sudo** decides who can run the install commands: passwordless sudo means you can run them; a
  password prompt means the user has to.

### 2.2 Install Node.js

Prefer the distribution's package, but check the version afterwards — the tools need 18+:

```bash
# Debian / Ubuntu (NodeSource gets a current LTS; the distro package can be too old)
sudo apt-get update
sudo apt-get install -y ca-certificates curl
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Fedora / RHEL
sudo dnf install -y nodejs

# Arch
sudo pacman -S --needed nodejs npm
```

```powershell
# Windows
winget install --id OpenJS.NodeJS.LTS -e
```

Then re-run `node --version`. If `sudo` needs a password, give the user the exact commands and ask
them to run them; never ask for the password.

### 2.3 Install the dedicated server

Two routes; pick by the target:

- **A headless remote (Linux VPS) — SteamCMD, anonymous login.** The depot is public:

  ```bash
  sudo apt-get install -y steamcmd          # Debian/Ubuntu: this also brings the 32-bit libs
  # or, without a package: mkdir -p ~/steamcmd && cd ~/steamcmd &&
  #   curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf -
  mkdir -p "$SERVER_DIR"
  steamcmd +force_install_dir "$SERVER_DIR" +login anonymous +app_update 1874900 validate +quit
  ```

  App id **1874900** is stable, **1890870** is experimental. `+force_install_dir` must come before
  `+app_update`, or SteamCMD updates its own directory instead of the server's. If you used the
  tarball rather than the package, the command is `./steamcmd.sh` in `~/steamcmd`. The Linux server
  is a native x86_64 binary — no Wine, no Proton, and it does not work under Steam Linux Runtime
  (`T165196`).

- **A Windows machine the user sits at — the Steam client.** Library → Tools → **“Arma Reforger
  Server”** (app 1874900), install it, then use the path Steam shows. Or, if SteamCMD is at hand,
  the same `+app_update` line as above.

- **One or the other, never both into the same directory.** If the user installs it in Steam, do
  not run SteamCMD over the top; ask for the install path instead.

After the install, verify §2.1 again, and note the **exact binary name**: Linux installers usually
produce `ArmaReforgerServer`, but check `ls "$SERVER_DIR" | grep -i arma`.

### 2.4 If neither route works

Say what is missing and stop before writing the config: a server directory without `addons/` cannot
start, and no config fixes that. Ask the user to install it (Steam client or SteamCMD) and give you
the path. The rest of the skill applies unchanged once the path exists.

## 3. Carry the tools to the target

Everything you check from here on runs **on the target**, and the scripts that do it are in this
repository. Copy the tree, keeping the layout: `validate-server-config.mjs` resolves
`../schemas/server.schema.json` and `../data/*.json`, so `tools/` alone is not enough.

```bash
# Linux target (local or over SSH), from the repository root
tar czf - tools schemas data package.json \
  | ssh -o BatchMode=yes -p <port> <user>@<host> \
      'mkdir -p ~/arma-reforger-tools && tar xzf - -C ~/arma-reforger-tools'
```

```powershell
# Windows target over SSH, from the repository root
ssh <user>@<host> 'mkdir -p C:/Users/<user>/arma-reforger-tools'
scp -r tools schemas data package.json <user>@<host>:C:/Users/<user>/arma-reforger-tools/
```

Then everything is a command **inside `~/arma-reforger-tools` on the target**:

| Check | Command (run on the target) |
|---|---|
| Config is valid | `node tools/validate-server-config.mjs /path/config.json` |
| Server is up (ports bound and A2S answered too, when those checks can run) | `node tools/server-status.mjs --profile <profile> --config <config> --wait 180` |
| The server itself accepts the config | `node tools/probe-config-schema.mjs <config> --server-dir <serverDir>` |
| RCON works | `RCON_PASSWORD='<pw>' node tools/rcon.mjs players --port <port>` |

For a remote target, prefix each with the SSH form from §1:

```bash
ssh -o BatchMode=yes -p <port> <user>@<host> \
  'cd ~/arma-reforger-tools && node tools/server-status.mjs --profile <profile> --config <config> --wait 180'
```

Why on the target: the newest `console.log` is there, the UDP socket table is the target's, and
RCON is bound to the target's `127.0.0.1`. A check run on your own machine cannot see any of them —
it would only tell you something about your own machine. The one deliberate exception is the
external reachability probe in §10.3: that one *must* run from outside the target's network,
because its whole point is to test the path from outside.

The tools are plain Node, no dependencies and no install step; Node 18+ from §2.2 is all they need.
Copying them again after a repository update is safe — nothing in them writes to the server.

## 4. Three rules that decide whether it works at all

1. **The working directory must be the server directory.** The engine resolves `./addons/core`
   and `./addons/data` against the *current directory*, not against its own `.exe`. Launched from
   anywhere else it shows (or logs) `Missing Addon` / `Can't find '58D0FB3206B6F859' game addon!`
   — the GUID of the game itself. Every script below does `cd` (Windows) or `cd`/`WorkingDirectory=`
   (Linux) first.
2. **The server must not run inside a sandbox.** Under one that blocks named pipes or the TLS
   certificate store, the engine hangs before its first log line or fails every backend call with
   `Curl error=SSL peer certificate ...` / `ENV:[invalid]`. The server then never writes
   `Server registered with address:` and is invisible to the browser. Launch it from an
   unrestricted shell; if your own shell is sandboxed, ask the user to run the launch command or
   use the widest permission the environment offers for exactly that command.
3. **Never invent a `scenarioId`, an admin id or a password.** A `scenarioId` is
   `{16 hex}Missions/Name.conf` copied from [data/scenarios.json](../../data/scenarios.json)
   (38 vanilla scenarios); a mod mission's GUID comes from its `.conf.meta` (`Name` field). A wrong
   GUID fails silently or exits with a mission error.

## 5. The interview

Ask all of this in one message. Mark the recommended answer, keep the list short, and use the
user's own words for anything they already said. Question 0 was answered in §1.

```
Before I write the config, ten answers (recommended options are marked):

 0. Where should the server run: this machine, or a remote one over SSH?   [asked first, §1]
 1. Server name, and should it be listed in the server browser?   [required name; visible = yes]
    Join password?                                               [empty = open server]
 2. Public address: let the server detect it, or pin your public IP?   [auto = recommended]
 3. RCON: local 127.0.0.1, external 0.0.0.0, or off?   [local = recommended]
    Password and permission (admin / monitor)?
 4. Profile: the server default (next to the executable) or a path of your own?   [default]
    ownerToken.bin: copy one from another profile, or let the server create it?   [create]
 5. Administration: admin ids in `admins`, an admin password, or none?
    [none; the owner token holder stays the owner]
 6. Cross-platform: enable, disable, or a custom platform list?   [disabled: PC only]
 7. Maximum players?                                             [32]
 8. Which scenario should run?   [Conflict - Everon]
 9. Where should the folder with the config go?   [next to the server executable]
```

A2S (Steam Query) is **not** one of the questions: the template already enables it on the standard
`0.0.0.0:17777`, which is what the server browser and monitoring use (§10).

### 5.1 Name, join password, visibility

`game.name` is mandatory and the schema enforces **1..100 characters** — an empty or 101-character
name stops the server. `game.password` is the join password (`""` = none). `game.visible` puts the
server in the browser; `false` still allows joining by code/address and is the right answer for a
test server.

### 5.2 Public address

Two answers:

- **Let the server detect it** (recommended): `"publicAddress": ""`. The server registers the
  address it sees and writes it to the log as `Server registered with address: <ip>:<port>`.
- **Pin an IP**: put it in `publicAddress`. Then warn the user: a pinned public IP breaks joining
  **from the server's own LAN** unless the router does NAT hairpin, and the log shows nothing —
  see §11.4. If the external port differs from the local one, `publicPort` is the external port and
  `bindPort` the local one.

Never put a `192.168.x.x`/`10.x` address in `publicAddress` on an internet-facing server, and do
not "fix" an address problem with `-bindIP` — it overrides both `bindAddress` and `publicAddress`.
On a VPS the address is usually the host's own public IP, so auto-detection is right there too.

### 5.3 RCON

Ask which binding and get a password and a permission level. Write the block only if the user
wants RCON:

```json
"rcon": {
  "address": "127.0.0.1",
  "port": 19999,
  "password": "<no spaces, at least 3 characters>",
  "maxClients": 4,
  "permission": "admin"
}
```

- **`127.0.0.1` is the recommended binding.** RCON grants full control (kick, ban, restart,
  shutdown) and is protected by the password alone; a server reachable from the internet with
  `rcon.address: "0.0.0.0"` is an open door — on a remote/VPS server especially. The alternative is
  an SSH tunnel (§11.5) or a VPN, not opening the port.
- **`0.0.0.0` is the external choice.** Say plainly that this exposes the remote console to the
  whole internet, that it must then be firewalled, and that it needs a long random password. The
  minimum of 3 characters is an engine limit, not a recommendation.
- **`permission`: `admin` or `monitor`.** `monitor` can run only `#players`; there is no finer
  granularity. `blacklist`/`whitelist` exist for command filtering.
- **The password must not contain spaces and must be at least 3 characters**, otherwise the server
  writes `[RCON] Init failed... Missing password or password length < 3 characters !!!` and RCON
  stays off. Record the password in the config only; do not echo it in the transcript or in shell
  history (use the `RCON_PASSWORD` environment variable for client runs).

### 5.4 Profile and `ownerToken.bin`

The profile is the server's identity, not just a log folder. Ask which one:

- **Server default** (recommended): `<serverDir>/profile`, next to the executable. It is what the
  server uses when `-profile` is omitted; pass it explicitly so the script is unambiguous.
- **A path of your own**: use the absolute path. One profile per server — two servers must not
  share one, and copying `ownerToken.bin` does not clone a server.

Then the owner-token question. Explain, briefly:

- The token lives at **`<profile>/profile/ownerToken.bin`** (the profile directory contains a
  `profile` subdirectory). It is a JWT issued by Bohemia's backend on the first successful
  registration; a profile that never reached the backend has none.
- It is the server's ownership credential: one token = one room = one ban list. Giving the same
  token to a second running server makes the two fight over the room, and the earlier one shuts
  down with `DS Room/ Server not exist anymore, shutting down...`.
- Losing it loses the server's identity and ban list; back it up, and never publish it.

Ask: **copy an existing `ownerToken.bin` from another profile, or let the server create a new
one?** If copying, put it at `<profile>/profile/ownerToken.bin` *before* the first start, verify
the path, and make sure the source server is not running on the same token. If not copying and the
target has no token, say that the server will create one on its first registration — which needs
internet access. On a remote target, copy it over SSH/SCP, not by pasting the token into the
conversation.

To tell the user who the owner is, read only the claims — never print the token:

```bash
node -e "const p=JSON.parse(Buffer.from(require('fs').readFileSync(process.argv[1],'utf8').split('.')[1],'base64url'));console.log({ownerType:p.ownerType,ownerId:p.ownerId})" "<profile>/profile/ownerToken.bin"
```

`ownerType: "GameIdentity"` means the player in `ownerId` is the owner; `"Anonymous"` means no
player owns it (the typical dedicated-server token).

### 5.5 Administration

Offer three answers, and allow a combination:

- **Admins in the `admins` list** — the user lists identity ids (UUID, e.g.
  `0ac6169c-15e4-4b5d-8073-08e602583069`) and/or Steam ids (17 digits). Maximum 20 unique ids.
  Copy them exactly; never invent or "correct" one. Such players can log in without a password.
- **An admin password** — `game.passwordAdmin`, non-empty and without spaces. Required if the user
  chooses this. Warn: anyone with the password becomes an administrator, it sits in plain text in
  the config, and it is not a per-person account; the `admins` list is the safer option. Login in
  game is `#login <password>`.
- **Defaults** — no extra admins: `admins: []`, `passwordAdmin: ""`. Explain who is admin then:
  if the profile's token has `ownerType: "GameIdentity"`, the **owner is the admin** and logs in
  without a password; if the token is anonymous or absent, nobody has in-game admin rights until
  one of the two options above is configured (RCON still works).

### 5.6 Cross-platform

Three answers, and the combinations are not arbitrary:

| Answer | Config | Valid? |
|---|---|---|
| Disable | `crossPlatform: false`, `supportedPlatforms: ["PLATFORM_PC"]` | yes, vanilla and modded |
| Enable | `crossPlatform: true` (adds PC + XBL + PSN if absent) | yes, vanilla and modded |
| Custom | explicit `supportedPlatforms` | only the rows below |

| Combination | Allowed? |
|---|---|
| PC only | yes |
| PC + Xbox + PlayStation | yes |
| PC + Xbox | **only on a modded server**; PSN is never added there |
| PC + PlayStation, Xbox only, PlayStation only, Xbox + PlayStation | **no** |

If the user asks for a custom list that is not allowed, say so and offer the nearest allowed one.
`crossPlatform: true` is the simplest way to say "all consoles". **If the server has mods, do not
rely on it:** set `crossPlatform: false` and `supportedPlatforms: ["PLATFORM_PC", "PLATFORM_XBL"]`,
because PlayStation is never added on a modded server and PC + Xbox is the only console
combination allowed there.

### 5.7 Maximum players

`game.maxPlayers`, integer 1..128. Ask; 64 is the class default, 32 is a safe answer for a first
server, 16 for a test. On a remote VPS, keep the host's bandwidth in mind before offering 128.

### 5.8 Scenario

Ask which mode and map, then look up the exact string — do not type a GUID from memory:

- Vanilla: [data/scenarios.json](../../data/scenarios.json) / the
  [scenarios document](../../docs/en/ArmaReforger_Scenarios_EN.md). Map codenames are traps:
  `Eden` is Everon, `Cain` is Kolguyev, `Arland` is Arland.
- A mod mission: the mission's `.conf.meta`, field `Name`, e.g. `{GUID}Missions/X.conf`.

One scenario per server; there is no rotation. If the user wants mods, the list comes from the
game's mod window (JSON tab) wrapped in `[` `]` — see the config skill §3; mods also change the
cross-platform answer (no PSN).

### 5.9 Where the folder goes

Default: a folder next to the server executable, named after the server (`<serverDir>/MyServer/`).
Offer a different path if the user wants one. The folder must be readable by the server process and
should be writable if the profile lives inside it. On Windows the server usually sits under
`Program Files`, where creating files needs an elevated shell — if that is not available, put the
folder somewhere writable and keep the absolute paths in the start script, which works from any
location as long as the working directory is still the server directory.

## 6. Write the config

1. Copy [assets/config.template.json](assets/config.template.json) — a complete, schema-valid
   config with the defaults from this skill (A2S on, PC only, Conflict Everon, 32 players).
2. Apply the answers. The template already contains every key this skill sets; add the `rcon`
   block only when RCON was requested, and `game.mods` only when there are mods.
3. **Omit `game.gameProperties.serverMinGrassDistance` unless the user asks for a value in
   50..150.** The wiki allows `0`, but build 1.8.0.13 rejects an explicit `0` with
   `... is bellow the minimum limit ... The minimum allowed is 50.` and the server exits. Leaving
   the key out gives the default (no forced grass distance); writing `50`..`150` forces one.
4. **Write UTF-8 without a BOM.** PowerShell's `Set-Content -Encoding utf8` and `Out-File` write a
   BOM, and the server then fails to parse the file (`JSON parse error: ... Unexpected token`,
   reported at line 1). Use an editor that writes plain UTF-8, or a Node/Python one-liner.
5. Write the file on the **target** (or copy it there after validating it) — §3's tools are already
   there, so validate it there:
   - `node tools/validate-server-config.mjs <path>/config.json` — errors mean the server will
     reject the file, warnings mean it starts but clamps or ignores a value.
   - When the tools are not available yet, check the hard rules in the config skill §3 and the
     failure table in §9 of the config guide.
   - Optional and closest to the truth: `node tools/probe-config-schema.mjs <config.json>` runs the
     server itself and reports `accepted` / `rejected` — it must run outside a sandbox (§4).

## 7. Place the folder and the start scripts

Layout (default profile inside the server directory shown separately):

```
<serverDir>/
  ArmaReforgerServer.exe        (Linux: ArmaReforgerServer)
  addons/                       the game itself — never move it
  <ServerName>/
    config.json
    start-server.cmd            Windows
    start-server.sh             Linux
  profile/                      the server-default profile (chosen in §5.4)
    logs/logs_<date>_<time>/console.log
    profile/ownerToken.bin
```

If the profile was placed inside the server folder instead, adjust the paths in the scripts.

**`start-server.cmd`** — bake the absolute server directory in; `%~dp0` is the script's own folder.
Keep the command on **one line**: a batch file with LF-only line endings (which most editors and
`write`-style tools produce) breaks `^` continuations, and the script then exits without a message.
Save it as CRLF if in doubt.

```bat
@echo off
setlocal
rem Working directory MUST be the server directory: otherwise "Missing Addon 58D0FB3206B6F859".
set "SERVER_DIR=C:\Program Files (x86)\Steam\steamapps\common\Arma Reforger Server"
cd /d "%SERVER_DIR%" || exit /b 1
"%SERVER_DIR%\ArmaReforgerServer.exe" -config "%~dp0config.json" -profile "%SERVER_DIR%\profile" -maxFPS 60 -logTime datetime -logLevel normal
```

**`start-server.sh`** — `cd` first for the same reason, then `exec`:

```bash
#!/usr/bin/env bash
set -euo pipefail
SERVER_DIR="/home/steam/reforger/server"
cd "$SERVER_DIR"
exec "$SERVER_DIR/ArmaReforgerServer" \
  -config "/home/steam/reforger/server/MyServer/config.json" \
  -profile "/home/steam/reforger/server/profile" \
  -maxFPS 60 -logTime datetime -logLevel normal "$@"
```

Make it executable (`chmod +x`) and never launch it as root; the server must be able to write to
the profile directory.

### 7.1 The command line, and what each parameter is for

| Parameter | Why it is there |
|---|---|
| `-config <absolute path>` | the config; absolute so it cannot resolve against the wrong directory |
| `-profile <absolute path>` | the profile; absolute for the same reason |
| `-maxFPS 60` | without it the server tries to take all available CPU. 60..120 is the recommended range |
| `-logTime datetime` | timestamps become `2026-10-17 04:51:39.165`, so logs from several runs can be lined up |
| `-logLevel normal` | normal logging. Do **not** add the debug firehoses (`-logFS`, `-log-rdb-checksum`, `-log-scr-checksum`, `-logLevel debug/spam`) unless the problem calls for them |

Add what the user asked for, and screen every extra parameter against
[data/startup-params.json](../../data/startup-params.json) first: `present` is usable on 1.8.0.13,
`absent` is a silent no-op. Two parameters are traps: **`-addons` is incompatible with `-config`**
(mods go in `game.mods`), and **`-bindIP`/`-bindPort` override both the bind and the public
address/port**, so they are the wrong tool for a NAT problem.

## 8. Launch

### 8.1 Windows, local

From an unrestricted shell (not a sandbox), start the script with the server directory as the
working directory, so the script and the engine agree even before `cd` runs:

```powershell
$folder = "C:\Program Files (x86)\Steam\steamapps\common\Arma Reforger Server\MyServer"
$serverDir = "C:\Program Files (x86)\Steam\steamapps\common\Arma Reforger Server"
Start-Process -FilePath cmd.exe `
  -ArgumentList '/c', "`"$folder\start-server.cmd`"" `
  -WorkingDirectory $serverDir -WindowStyle Hidden -PassThru `
  -RedirectStandardOutput "$folder\server.out" -RedirectStandardError "$folder\server.err"
```

Two details are not optional, both found by running it:

- **Redirect stdout/stderr** as above. Without the redirect the server inherits the launching
  shell's output handles, and the call then looks like it hangs even though the server is running
  — the shell is only waiting for the server to close them.
- **Launch through `cmd.exe /c`**, not by passing the `.cmd` file to `Start-Process` directly:
  the direct form hangs the same way here even with a hidden window.

`-PassThru` gives a process object; the server also writes its own log, which is what §9 reads.
If the shell you are in is sandboxed, do not "try harder" here — ask the user to double-click
`start-server.cmd` (it sets its own working directory) or re-run the command with unrestricted
access. A sandboxed launch is indistinguishable from a broken config until you read the log.

### 8.2 Linux, local

```bash
chmod +x "<folder>/start-server.sh"
setsid nohup "<folder>/start-server.sh" > "<folder>/server.out" 2>&1 < /dev/null &
echo $!
```

### 8.3 Remote over SSH (the usual VPS case)

The SSH session is not the server's parent: when it closes, everything it started without
detaching dies with it. Detach explicitly, or let systemd own it.

**Linux target — detached launch:**

```bash
ssh -o BatchMode=yes -p <port> <user>@<host> \
  'cd "<serverDir>" && setsid nohup "<folder>/start-server.sh" > "<folder>/server.out" 2>&1 < /dev/null & echo started: $!'
```

**Linux target — systemd (recommended for a server that must stay up).** Write a unit on the target
(the essential parts: `WorkingDirectory=<serverDir>`, `ExecStart=<folder>/start-server.sh`,
`KillSignal=SIGINT`, `Restart=on-failure`), then `systemctl enable --now`, and read
`journalctl -u <unit> -f` — the full unit is Appendix A.4 of the
[startup parameters document](../../docs/en/ArmaReforger_StartupParams_EN.md).

**Windows target over SSH.** `Start-Process` inside an SSH session can be killed with the session;
if the server must survive the disconnect, register it as a scheduled task and start that:

```powershell
schtasks /create /tn "ArmaReforgerServer" /tr "\"<folder>\start-server.cmd\"" /sc onstart /ru <user> /rl highest /f
schtasks /run /tn "ArmaReforgerServer"
```

Then disconnect, reconnect, and confirm the process is still there (§9) before believing it.

The two environment rules still apply on the target: the working directory must be the server
directory (§4 rule 1), and the process must not be sandboxed (§4 rule 2). A container on the VPS is
a common cause of the backend failure described in §12.

### 8.4 Windows specifics

What differs from the Linux procedure is mostly the machine, not the config:

- **The install sits where you cannot write.** Steam's default is
  `C:\Program Files (x86)\Steam\steamapps\common\Arma Reforger Server`, and creating a file there
  needs an elevated shell. Put the folder of §5.9 somewhere writable
  (`%USERPROFILE%\ArmaReforgerServer`, say) and keep **absolute** paths in the script: the working
  directory still has to be the server directory (§4 rule 1), but that is a `cd`, which needs no
  write access.
- **A firewall rule for the game is not a rule for the server.** Windows rules are normally per
  program, and the ones Steam creates name the client executables (`ArmaReforgerSteam.exe`,
  `ArmaReforger_BE.exe`); the dedicated server is a different binary, `ArmaReforgerServer.exe`, so
  those rules do not cover it. What covers it is a rule on the UDP ports or on that exact program
  path — look instead of assuming:

  ```powershell
  Get-NetFirewallRule -Direction Inbound -Enabled True -Action Allow | ForEach-Object {
    $pf = $_ | Get-NetFirewallPortFilter
    if (@($pf.LocalPort) -contains '2001' -or @($pf.LocalPort) -contains '17777') {
      [pscustomobject]@{ Rule = $_.DisplayName; Ports = (@($pf.LocalPort) -join ',')
                         Program = ($_ | Get-NetFirewallApplicationFilter).Program }
    }
  }
  ```

  `New-NetFirewallRule` itself needs an elevated shell, and a UAC prompt is not something an agent
  can answer: hand the command to the user rather than failing at it. A rule scoped to `Private`
  also stops applying the moment Windows relabels the network `Public` — the same symptom as a
  closed port, and nothing in the log.
- **A loopback probe never touches the firewall.** `server-status --a2s-only 127.0.0.1:17777`
  answers with the firewall fully closed, so it proves the server is up, not that the path is open.
  Reachability is the external probe of §10.3, and nothing on the server can stand in for it.
- **Under a sandbox both the process list and the socket table can come back empty.**
  `Get-Process -Name ArmaReforgerServer` and `netstat -ano -p UDP` may report nothing while the
  server is running and answering A2S — that is the harness, not a dead server (§4 rule 2). Re-run
  those two, and `server-status`, with the widest permission available instead of concluding that
  the launch failed.

Two smaller ones: `game.name` in Cyrillic is accepted and comes back unchanged from A2S on
1.8.0.13 — a BOM is what breaks the file, not the language (§6 rule 4); and stop the server with
the RCON `shutdown` (the log then ends with `Game destroyed.`) rather than `taskkill`, so the next
reader of the log can see how the run ended.

## 9. Watch the log until it is ready

The log lives at `<profile>/logs/logs_<YYYY-MM-DD>_<HH-MM-SS>/console.log` — a new directory per
launch, so always take the newest one. The sequence below is what build 1.8.0.13 writes; the whole
start takes about 15-20 s (18-20 s observed on this machine).

| Log line | Means |
|---|---|
| `CLI Params: ...` | what the engine actually received — the first thing to check when a flag "does not work" |
| `dir: './addons'` + `gproj: './addons/data/ArmaReforger.gproj' guid: '58D0FB3206B6F859'` | the working directory was right |
| `Server config loaded.` then `JSON is Valid` | the schema accepted the file; `JSON is invalid!` names the offending key |
| `Entities load 'worlds/...'` | the scenario's world is loading |
| `Starting RPL server, listening on address <ip>:<port>, fastValidation=(true\|false)` | the game socket is up |
| `Server registered with address: <ip>:<port>` | the backend accepted the server: this is the "ready" line |
| `Direct Join Code: <code>` / `Ping Site: <site>` | what players type to join directly |
| `[RCON] Init, Ip address=... and Port=...` | RCON is up (absent when RCON is not configured) |

Do not conclude "ready" from the process being alive, and do not read `[RCON] Init failed...` as a
fatal server error — RCON is optional and stays off, the server itself runs.

### 9.1 The check to run (on the target)

```bash
# local target
cd ~/arma-reforger-tools
node tools/server-status.mjs --profile "<profile>" --config "<folder>/config.json" --wait 180

# remote target
ssh -o BatchMode=yes -p <port> <user>@<host> \
  'cd ~/arma-reforger-tools && node tools/server-status.mjs --profile "<profile>" --config "<folder>/config.json" --wait 180'
```

It polls the newest `console.log`, stops at registration or at a fatal line, reads the expected
ports from the config, asks the operating system which UDP endpoints exist, probes A2S, and prints
a verdict that keeps the three questions apart: `configValid`, `state`/`registered`, and the port
table. Exit codes: `0` registered (and, when the checks ran, the expected ports bound), `1` not
ready or a port missing, `2` usage. `--no-sockets` and `--no-a2s` skip one check each — with them,
exit 0 means the log registered the server and says nothing about the ports — `--log-dir` reads a
specific `logs_*` directory instead of the newest, `--out FILE` writes the JSON report,
`--json` prints it, and `--a2s-only <host>:<port>` probes A2S and exits without a profile (run it
from outside the server's network). States:

- `ready` — registration seen; go to §10.
- `listening` — the game socket is up but registration never happened: no internet, a proxy, or a
  sandboxed launch (`Curl error=SSL peer certificate`, `ENV:[invalid]`). Fix the environment, not
  the config.
- `starting` — the world is still loading; wait.
- `failed` — read the fatal line. A schema rejection names the key; `Missing Addon` with
  `58D0FB3206B6F859` means the working directory was wrong.
- `new` — no log at all: the server did not start, or `-profile` points at a different directory
  than the one you are reading. On a remote target this is also what a launch killed with the SSH
  session looks like (§8.3).

Without the tools, do the same three checks by hand on the target: newest `console.log` for
`JSON is Valid` / `Server registered with address:`, `ss -lunp | grep 2001` (Linux) or
`Get-NetUDPEndpoint -LocalPort 2001` (Windows), and `node tools/rcon.mjs` if available.

## 10. Verify the ports

What must be open is UDP only — the game port, A2S and RCON are all UDP; there is no TCP listener:

| Port | Protocol | Purpose | Config key | Open it? |
|---|---|---|---|---|
| 2001 | UDP | the game (RPL) | `bindPort` / `publicPort` | yes |
| 17777 | UDP | A2S / Steam Query — server browser and monitoring | `a2s.port` | yes |
| 19999 | UDP | RCON | `rcon.port` | only if `rcon.address` is `0.0.0.0`; otherwise never |

Four different questions, with four different answers:

### 10.1 Did the server bind the ports?

The status tool's socket table (or `ss -lunp` / `Get-NetUDPEndpoint`), run **on the target**, with
the server's pid. `MISSING` means the server did not bind: a config or startup-parameter override,
or the wrong profile.

### 10.2 Does the port answer?

A2S is the only endpoint that answers without a password: the status tool sends an A2S_INFO query
to the target's loopback and prints the server name, map and player count. For RCON, log in with
the client **on the target** — in bash
`RCON_PASSWORD='<password>' node tools/rcon.mjs players --port <port>`, in PowerShell
`$env:RCON_PASSWORD='<password>'; node tools/rcon.mjs players --port <port>` (`--json` for the
machine-readable form). A silent RCON with `[RCON] Init` in the log means the port or address is
wrong, or a firewall eats the packet.

### 10.3 Is the port reachable from outside?

A bound socket says nothing about the router, the cloud security group or the host firewall, and
this cannot be answered on the target itself. Run the A2S probe **from a machine outside the
target's network** — for a remote VPS that is your own machine; for a home server, a laptop on
mobile data:

```bash
node tools/server-status.mjs --a2s-only <publicAddress>:17777
```

Exit 0 and a name means the path is open end to end. "No answer" points at the router rule, the
security group, the host firewall, or NAT hairpin (§11.4). The same command works from the target
against `127.0.0.1:17777` as a control: if that answers and the external one does not, the server is
fine and the network is the problem. There is no application-level probe for the game port itself;
the A2S answer plus `Server registered with address:` is the evidence you have.

### 10.4 Is the server visible in the browser?

That is `game.visible: true` plus a successful registration plus a reachable A2S port. If the
registration is missing, the browser will not list the server regardless of the ports.

## 11. Tell the user how to connect

### 11.1 Joining

- **Direct Join Code** from the log (`Direct Join Code: 0340196985`) — the shortest path, and the
  one to quote in a chat.
- **By address**: `<publicAddress>:<publicPort>` from `Server registered with address:` (for a
  LAN-only test, `<server LAN IP>:2001`).
- **Server browser**: only when `game.visible` is `true`; the name is `game.name`.
- **Password**: `game.password`, if set.
- **Admin in game**: `#login <passwordAdmin>`, or the owner token holder without a password.

### 11.2 Router port forwarding (home machine)

Forward on the router, to the server's **LAN** address (give it a static DHCP lease so the rule
keeps working):

- `2001/udp` → `<LAN IP>:2001`
- `17777/udp` → `<LAN IP>:17777`
- `19999/udp` only if RCON was deliberately bound to `0.0.0.0` — and then firewall it to known
  addresses if the router can.

If the external port differs from the internal one, set `publicPort` to the external port and
`bindPort` to the internal one, and forward external → internal.

### 11.3 Host and cloud firewall

Windows Defender Firewall, one rule for the UDP ports (run as administrator):

```powershell
New-NetFirewallRule -DisplayName "Arma Reforger Server" -Direction Inbound -Protocol UDP `
  -LocalPort 2001,17777 -Action Allow
```

Linux: `sudo ufw allow 2001/udp`, `sudo ufw allow 17777/udp`, and `19999/udp` only for an
external RCON (`firewalld`: `firewall-cmd --add-port=2001/udp --add-port=17777/udp --permanent`
then `firewall-cmd --reload` — without the reload the permanent rule is written but not active).
Open TCP for these ports nowhere: there is no TCP listener.

On a **VPS**, the provider's firewall/security group is the first place to look, before `ufw`: a
rule for `2001/udp` and `17777/udp` has to exist there too. The host's own public IP means there
is no router forwarding and no NAT-hairpin problem — but the security group is exactly as capable
of dropping the packets, and the symptom is the same: bound socket on the target, no answer from
outside (§10.3).

### 11.4 The NAT-hairpin trap (home machine)

If `publicAddress` holds the public IP, players from outside can join but **you cannot join from
the same LAN**: the client is told the public address, sends packets to its own network's public
IP, and the router must loop them back in (NAT hairpin). Many home routers cannot. The server log
shows nothing — the packets never arrive.

What to tell the user, best first: leave `publicAddress` empty (the server detects it); join from
inside by the LAN address; enable NAT loopback/hairpin on the router; or set up forwarding from the
public IP to the LAN one. Do not try `-bindIP` — it overrides both addresses and pins the problem.

### 11.5 RCON on a remote machine

Keep `rcon.address: "127.0.0.1"` and **do not tunnel it with `ssh -L`**: RCON is UDP and `ssh -L`
forwards TCP only, so the tunnel carries nothing and the client sees silence. The safe ways to
reach it, best first:

```bash
# 1. run the client on the target, over SSH — the traffic never leaves the host
ssh -p <port> <user>@<host> 'RCON_PASSWORD="<pw>" node ~/arma-reforger-tools/tools/rcon.mjs players --port 19999'

# 2. a VPN that carries UDP (WireGuard, Tailscale) and the client on your machine
RCON_PASSWORD='<pw>' node tools/rcon.mjs players --host <target's vpn ip> --port 19999
```

From the target itself, plain `node tools/rcon.mjs` is enough (§10.2). Never bind RCON to
`0.0.0.0` on a public VPS just to avoid the tunnel.

## 12. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ssh: Permission denied (publickey)` | the target does not accept your key | ask the user to `ssh-copy-id`, or run the commands themselves; never paste a password or use `sshpass` |
| A command works locally but not through `ssh ... '...'` | quoting/escaping through the remote shell | put the command in a `.sh`/`.ps1` on the target and run the file |
| `node: command not found` on the target | Node.js is not installed there | §2.2 — the tools need Node 18+ on the target, not on your machine |
| `Missing Addon` window or log line, GUID `58D0FB3206B6F859` | the working directory was not the server directory | run the start script, or `cd` into the server directory first |
| The same window with another GUID | an addon of the scenario or a mod is missing | check `addons/` and `game.mods` |
| `Param "#/game/..." is not allowed` / `... bellow the minimum limit` | the schema rejected a key or value; the line names it | fix the named key; for `serverMinGrassDistance: 0` omit the key (§6) |
| `JSON parse error: ... (Line: 1, Char: 1)` / `Unexpected token` at the very start of the file | the file has a BOM or is not JSON (comments, trailing comma, mod list pasted without `[` `]`) | rewrite as UTF-8 without BOM, validate with `validate-server` |
| `Unable to open server config file: <path>` | `-config` points elsewhere; a relative path resolves against the working directory | use an absolute path |
| `[RCON] Init failed... Missing password or password length < 3 characters` | the password is empty, has spaces, or is shorter than 3 | fix `rcon.password` |
| RCON does not answer although `[RCON] Init` is in the log | wrong port/address, UDP blocked, or the client is not logged in | run the client on the target; check the socket table |
| `Server registered with address:` never appears; `Curl error=SSL peer certificate` or `ENV:[invalid]` | no internet, a TLS proxy, a container without a CA store, or a sandboxed launch | run outside the sandbox; check the clock, the proxy and the host's CA store |
| The server stops when the SSH session closes | the process was not detached | `setsid nohup ... &`, systemd, or a scheduled task (§8.3) |
| The launch command never returns, yet the server is up | the child inherited the shell's stdout/stderr (or a `.cmd` was passed straight to `Start-Process`, or has LF endings) | launch through `cmd.exe /c` with `-RedirectStandardOutput`/`-RedirectStandardError`, §8.1 |
| SteamCMD installed the server into its own directory | `+force_install_dir` was missing or placed after `+app_update` | rerun with `+force_install_dir` first |
| SteamCMD fails on a fresh Linux host | missing 32-bit libraries or disk space | `sudo apt-get install -y lib32gcc-s1` (or install the `steamcmd` package), check `df -h` |
| Server visible outside but not joinable from the LAN | NAT hairpin, see §11.4 | leave `publicAddress` empty / use the LAN address |
| Server invisible in the browser | `visible: false`, or registration failed, or A2S is blocked | set `visible: true`; read the log for registration; open 17777/udp |
| Two servers: one shuts down with `DS Room/ Server not exist anymore, shutting down...` | both profiles carry the same `ownerToken.bin` | one profile and one token per server |
| `no log yet: the server has probably not started, or -profile points elsewhere` from the status tool | `-profile` points somewhere else, or the server never started | check `CLI Params:` in the log, then the working directory |
| Server exits immediately after `Attempting online Game Config instead.` | the local config was rejected; the engine tried the online one and gave up | read the schema lines above it |

## 13. The final report to the user

Keep it short and factual, and say where it runs:

```
Server ready on <local machine | user@host:port>.
  Folder:     <serverDir>\MyServer\   (config.json, start-server.cmd)
  Profile:    <serverDir>\profile     (ownerToken.bin, logs)
  Scenario:   Conflict - Everon       maxPlayers: 32   crossPlatform: off
  RCON:       127.0.0.1:19999         admin
  Join:       Direct Join Code 0340196985, or 203.0.113.10:2001
  Ports:      2001/udp and 17777/udp are bound on the target and the A2S query answers with the
              server name; the probe from outside answered as well.
  Note:       <home: forward both on the router (UDP) to <LAN IP>; you cannot join through the
              public IP from the same LAN unless the router does NAT hairpin>
              <VPS: open the same two UDP ports in the provider's firewall/security group>
  Restart:    <systemctl restart <unit> | the scheduled task | the start script>
```

If something is still wrong, say exactly which check failed and what the log said, rather than
"it should work".

## 14. References

- [The config guide](../../docs/en/ArmaReforger_ServerConfig_EN.md) — keys, ranges, defaults,
  templates, the error table, and the launch section.
- [Scenarios](../../docs/en/ArmaReforger_Scenarios_EN.md) — every `scenarioId` with its GUID.
- [Startup parameters](../../docs/en/ArmaReforger_StartupParams_EN.md) — the command line,
  parameter-by-parameter, plus Appendix A on Linux (SteamCMD, launch script, systemd, ports).
- [RCON](../../docs/en/ArmaReforger_RCON_EN.md) — permissions, commands, diagnostics.
- [Profile](../../docs/en/ArmaReforger_Profile_EN.md) — logs, `ownerToken.bin`, saves, bans.
- [Backend API](../../docs/en/ArmaReforger_BackendAPI_EN.md) — what registration means, and why a
  sandboxed or proxied server cannot do it.
- Sibling skills: [server config](../arma-reforger-server-config/SKILL.md),
  [RCON](../arma-reforger-rcon/SKILL.md).
- Tools: [server-status.mjs](../../tools/server-status.mjs) (readiness, ports, `--a2s-only`),
  [rcon.mjs](../../tools/rcon.mjs), [probe-config-schema.mjs](../../tools/probe-config-schema.mjs),
  [validate-server-config.mjs](../../tools/validate-server-config.mjs).

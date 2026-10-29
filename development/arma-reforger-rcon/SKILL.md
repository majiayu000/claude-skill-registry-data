---
name: arma-reforger-rcon
description: Configure, secure and operate the Arma Reforger dedicated server RCON - the rcon block in server.json, the BattlEye RCon v2 packet format it turned out to speak, the two independent permission systems (ERCONPermissions for RCON and EPlayerRole for chat), the full # command list with the exact answers the server returns, and log-based diagnostics. Ships tools/rcon.mjs, the client to use instead of writing one. Use when enabling RCON or debugging why it refuses to start, when choosing between monitor and admin, when a command works over RCON but not in game chat, when BERCon.exe is mistaken for the Bohemia RCON, when writing or debugging an RCON client, when banning or unbanning a player, when bans hang in PENDING or time out, or when a killed client keeps a maxClients slot busy.
---

# Using the Arma Reforger RCON

## 0. Before you touch anything

Three rules that prevent almost every failure:

1. **RCON is not BattlEye's RCON — but it speaks BattlEye's packets.** Arma Reforger ships
   Bohemia's own remote console, configured in the `rcon` block of `server.json` and reached on
   port 19999. `BERCon.exe`, which sits next to the server binary, belongs to **BattlEye** and is
   configured in `battleye\BEServer_x64.cfg` (keys `RConPort`, `RConPassword`). Two different
   endpoints on two different ports — but the packet format is the same, BattlEye RCon v2
   (RCON §1.1). Never expect `rcon.password` to change BattlEye's settings.
2. **The wire protocol is known: BattlEye RCon v2.** A 7-byte header
   (`'B' 0x42 | 'E' 0x45 | CRC32 of the following bytes, little-endian | 0xFF`), then
   `0x00|password` to log in, `0x01|seq|command` to run a command, and `0x02|seq|text` for server
   messages, which the client must answer with `0x02|seq` or be dropped. The server does not check
   the CRC of what it receives; send what it sends — `crc32(0xFF|payload)`, little-endian. Three
   details decide whether a client works: **`seq` starts at 0 and a wrong one is ignored in
   silence** (the server still sends `0x01|seq` back, so an acknowledgement proves nothing);
   **`0x01|seq|@logout` frees the client's slot at once**, and it is the only way to do that —
   a client that is merely closed holds its slot for 45 s; and an **empty `0x01|seq` every 45 s or
   less is what keeps a session alive**. The
   full layout and a captured exchange are in RCON §1.1. The **transport is UDP** — verified by
   running the server with `rcon.address`/`rcon.port` set and inspecting the socket (a UDP
   endpoint owned by the server, no TCP listener, TCP connect refused). The BI wiki leaves the
   protocol cell empty and a widely used container image publishes 19999 as TCP; that image is
   wrong about the transport. Re-check on the host with `ss -lunp | grep 19999` (Linux) or
   `Get-NetUDPEndpoint -LocalPort 19999` (Windows).
3. **RCON is full control over the server** — kick, ban, scenario restart, shutdown —
   protected by the password alone. On an internet-facing server bind `rcon.address` to
   `127.0.0.1` and connect through an SSH tunnel.

### The client is already written: `tools/rcon.mjs`

**Use [`tools/rcon.mjs`](../../tools/rcon.mjs). Do not write another RCON client**, and do not
hand-roll a socket experiment: the protocol is implemented once, its framing is the one this
build accepts, and it handles the acknowledgement and keep-alive rules that get a naive client
dropped. `npm run rcon -- <subcommand>` is the same thing.

```bash
node tools/rcon.mjs players --password "$RCON_PASSWORD"          # playerId, identity id, name
node tools/rcon.mjs players --json                               # machine-readable
node tools/rcon.mjs ban list 1 --password "$RCON_PASSWORD"       # 25 per page over RCON
node tools/rcon.mjs ban create 1 3600 "teamkilling" --password "$RCON_PASSWORD"
node tools/rcon.mjs ban remove <identityId> --password "$RCON_PASSWORD"
node tools/rcon.mjs kick 1 --password "$RCON_PASSWORD"
node tools/rcon.mjs cmd "restart" --password "$RCON_PASSWORD"    # anything else, verbatim
node tools/rcon.mjs shell --password "$RCON_PASSWORD"            # interactive, several commands
node tools/rcon.mjs probe --framings 1                           # what does this build accept?
```

- `--host` (default `127.0.0.1`), `--port` (default `19999` = `rcon.port`), `--password` or the
  `RCON_PASSWORD` environment variable. Prefer the variable: the password is full control.
  `--quiet-ms <ms>` (silence after which an answer counts as complete, default 1500),
  `--timeout <ms>` (hard cap on one exchange, default 20000) and `--logout-wait <ms>` (default
  800) tune the waits — raise them for a slow host, never to hide a wrong port.
- **Every run ends with `@logout`**, so it does not leave a `maxClients` slot busy for 45 s.
  `--no-logout` reproduces what a client without it does; with `maxClients: 4`, four such runs and
  the fifth login is dropped with `[RCON] Client List is full!` and no answer at all. Since the
  tool logs out between `probe` framings too, probing a server with `maxClients: 1` works.
- `shell` keeps one session open and sends the specification's empty keep-alive every 20 s, so it
  survives idling (`--keep-alive <ms>`, `.keepalive <ms>`, `.reconnect`, `.exit`/`.quit`). Every
  command it runs ends with a `--- done:` line — status, exit code, message count, time — which is
  the client-side end-of-output marker, because the server sends an answer as several `0x02`
  messages with no terminator of its own. The shell exits with the status of its last command.
  `.raw` dumps packets and `.json` switches to one JSON object per command on stdout with the notes
  on stderr; `.json` can be toggled mid-session, like `.raw`.
  **Ctrl-C is a clean exit**: it logs out first, prints the result and exits `130`; a second
  Ctrl-C ends the process at once, but the first has already put `@logout` on the wire. It also
  works when the interrupt lands *during* a command — the wait is abandoned and the logout still
  goes out, which is what stops the loop from ending on a closed readline
  (`ERR_USE_AFTER_CLOSE`). The same applies to Ctrl-C during a one-shot run, and typing the
  `@logout` protocol command by hand leaves the shell the same way — it ends the session, so
  staying open on it could only collect silence. **`shutdown` leaves too**, without a logout
  (there is nobody left to answer one); `restart` keeps both the server and the session, and
  neither of the two costs a timeout, because they answer with their `Processing Command:` note
  and nothing else.
- Exit codes: `0` ok, `2` usage, `3` login refused, `4` no answer, `5` the server answered with a
  failure (`Player not found`, `Failed to create ban.`, `Timeout`, `missing permission '<cmd>'`,
  `unknown command`, `invalid parameters '<cmd>'` …). An empty ban list
  (`Server has no bans to list.`) is a normal answer and exits `0`; `Multiple users found! …` is
  a hint, not a failure. `2` is the client's own grammar check — `kick` with no `playerId`, `ban`
  with no subcommand, `ban create` with too few arguments — and it fires in the shell too, before
  anything is sent. `4` means no *answer message* came back, which is not the same as no packet:
  the server acknowledges every command packet with `0x01|seq`, so an unknown protocol command
  (`@foo`) is acknowledged and then answered with nothing, and that is `4`.
- `--raw` dumps every packet as hex and ascii to stderr — use it before doubting the tool.
- A failure is always **one line on stderr plus an exit code, never a stack trace** — `shell`
  included, whose login is the step most likely to fail from outside (wrong password → `3`, nothing
  listening → `4`, an unresolvable host named as a transport problem). Out-of-range numbers are
  refused with `2` before any socket is opened. A stack trace from this tool is a bug, not a result.
- If every command gets **no answer**, suspect a full client list before doubting the password or
  the port: each login holds a `maxClients` slot for 45 s, a full list drops packets *before*
  parsing them, and the server logs nothing else (RCON §6.3). `probe` says so in its own output and
  reports an explicit `DENIED` separately from silence — never read its silence as "wrong
  password".
- `players` is safe. `ban create`, `ban remove`, `kick`, `restart` and `shutdown` change state or
  disconnect people — confirm with the user before running them on a server that is not theirs to
  break, and prefer a reason string in `ban create` so the ban list explains itself later.
- **`players` and `ban list` come back as tables**, in the shell as well as one-shot, printed where
  the server's own message was (the ban table keeps the server's `Total bans: N | Page: X/Y` line
  above it). In `--json`/`.json` the raw `messages` are kept and the parsed values are added beside
  them: `players: [{ playerId, uid, name }]` and `bans: { total, page, pages, entries: [{ identityId,
  name }] }`, both at the top level and inside the `commands[]` entry they came from.
- A ban is stored on the Bohemia backend and belongs to one server; nothing appears in the
  profile (Profile §5.7). Do not go looking for a ban file, and do not promise a ban will carry
  to another server.

### How the tool reports a result

**Without `shell`** — one command per process, the human summary on stdout, diagnostics on stderr:

```text
127.0.0.1:19999  login: ok, client #0      where it connected; "FAILED" here means no session
command: players                            what went on the wire, verbatim
ack: seq=0                                  the 0x01|seq acknowledgement — not a success signal
Logged In! Client ID: #0                    the server's own messages, in the order they arrived
Processing Command: players
┌──────────┬──────────────────────────────────────┬─────────────────────┐
│ playerId │ uid                                  │ name                │
├──────────┼──────────────────────────────────────┼─────────────────────┤
│ 1        │ 0ac6169c-15e4-4b5d-8073-08e602583069 │ kolya_500           │
│ 2        │ 5f1e2d3c-4b5a-6978-8c9d-0e1f2a3b4c5d │ Ivan "the" Longname │
└──────────┴──────────────────────────────────────┴─────────────────────┘
logout: @logout acknowledged (seq 1); the slot is free at once
```

- The table **stands in for the messages it was parsed from**, in the position where they arrived —
  it is not appended after the logout line. `players` and `ban list` are the two answers treated
  this way; `ban list` keeps the server's own `Total bans: N | Page: X/Y` line above the table,
  because the page count is stated nowhere else.
- Everything else is printed as it came: `Processing Command: …`, error texts, and
  `Server has no bans to list.`, which is an answer rather than an empty table.
- The **exit code is the verdict** for the whole run: `0` ok, `2` usage, `3` login refused,
  `4` no answer, `5` the server reported a failure, `130` interrupted. A failure also writes one
  line to stderr.

**With `shell`** — one session, one `--- done:` line per command:

```text
Arma Reforger RCON shell — 127.0.0.1:19999, client #0
Commands are limited by rcon.permission in server.json; "players" works with monitor, the rest needs admin.
.help for the local commands, .exit to leave (this sends @logout and frees the slot at once).
Ctrl-C and the @logout command leave the same way.
rcon> players
Processing Command: players
┌──────────┬─────┬────────────────────┐
│ playerId │ uid │ name               │
├──────────┼─────┼────────────────────┤
│ -        │ -   │ (nobody connected) │
└──────────┴─────┴────────────────────┘
--- done: ok (exit 0), 2 messages, 1.7 s
rcon> kick 999
Processing Command: kick 999
Player not found
--- done: FAILED (exit 5): Player not found — 2 messages, 2.0 s
rcon> ban
--- done: usage error (exit 2): ban needs a subcommand: list [page] | create <id|name> <seconds> [reason] | remove <id|name> (nothing was sent)
rcon> @foo
--- done: no answer (exit 4), 0 messages, 1.5 s — the server acknowledged it but sent no answer; an unknown protocol command looks like this
rcon> .exit
--- shell: @logout acknowledged (seq 2); the slot is free at once (the server logs "[RCON] Client 0 logged out!")
```

- The `--- done:` line is the end-of-output marker: status, exit code, message count, time. The
  server sends an answer as several `0x02` messages and has no terminator of its own, so the client
  supplies one. It has exactly four shapes: `ok (exit 0)`, `FAILED (exit 5): <answer>`,
  `no answer (exit 4)` and `usage error (exit 2)`.
- The table is here too, in the same place, so the same command looks the same in both modes.
- The **shell's own exit code is the status of the last command it ran** (or `130` after Ctrl-C,
  `0` if it ran none), which is what makes `printf 'players\n.exit\n' | node tools/rcon.mjs shell`
  usable from a script.
- The session ends with the `--- shell:` line saying whether `@logout` was acknowledged; a second
  `Ctrl-C` skips it, but the first has already put the logout on the wire.

**JSON** — `--json` for a one-shot run, `.json` (or `--json`) inside the shell. `--json` prints
exactly one object and nothing else, so it can be piped into a parser; shell JSON is one object per
command, with the banner, the notes, the prompt and the `> command` echo moved to stderr.

The two shapes are described by
[`schemas/rcon-result.schema.json`](../../schemas/rcon-result.schema.json), and the examples below
are checked against it by `npm run check:rcon-schema` — the same relationship `docs/en/` has with
`data/`, so the document cannot drift from the schema silently.

One-shot result — every message of the session, plus the parsed values next to them:

<!-- rcon-json: result -->
```json
{
  "host": "127.0.0.1",
  "port": 19999,
  "command": "players",
  "loggedIn": true,
  "clientId": 0,
  "ack": { "seq": 0, "response": "" },
  "messages": [
    "Logged In! Client ID: #0",
    "Processing Command: players",
    "Players on server: [Player#] ; [Player UID] ; [Player Name]"
  ],
  "commands": [
    {
      "command": "players",
      "seq": 0,
      "ack": { "seq": 0, "response": "" },
      "messages": [
        "Processing Command: players",
        "Players on server: [Player#] ; [Player UID] ; [Player Name]"
      ],
      "players": [],
      "ms": 1743,
      "status": "ok",
      "error": null,
      "exitCode": 0
    }
  ],
  "success": true,
  "players": [],
  "loggedOut": true,
  "logout": { "seq": 1, "acknowledged": true },
  "error": null
}
```

One line of shell JSON — the same per-command fields plus where the session is connected. Here a
`ban list` page with one ban on it, then a command the client's own grammar refused:

<!-- rcon-json: command -->
```json
{
  "host": "127.0.0.1",
  "port": 19999,
  "clientId": 0,
  "command": "ban list 1",
  "seq": 2,
  "ack": { "seq": 2, "response": "" },
  "messages": [
    "Processing Command: ban list 1",
    "Total bans: 26 | Page: 2/3\n- Identity Id | Banned name\n- 0ac6169c-15e4-4b5d-8073-08e602583069 | kolya_500\n"
  ],
  "bans": {
    "total": 26,
    "page": 2,
    "pages": 3,
    "entries": [{ "identityId": "0ac6169c-15e4-4b5d-8073-08e602583069", "name": "kolya_500" }]
  },
  "ms": 1526,
  "status": "ok",
  "error": null,
  "exitCode": 0
}
```

<!-- rcon-json: command -->
```json
{
  "host": "127.0.0.1",
  "port": 19999,
  "clientId": 0,
  "command": "ban",
  "seq": null,
  "ack": null,
  "messages": [],
  "ms": 0,
  "status": "usage error",
  "error": "ban needs a subcommand: list [page] | create <id|name> <seconds> [reason] | remove <id|name>",
  "exitCode": 2
}
```

What a consumer needs to know:

| Field | Where | Meaning |
|---|---|---|
| `messages` | both | The raw `0x02` texts of the command, in order. The tables are built from these; nothing is thrown away. |
| `players` | both | Only for `#players`: `[{ playerId, uid, name }]`, empty when nobody is connected. `uid` is the `identityId` a ban needs. |
| `bans` | both | Only for `#ban list`, and only when the server sent a list: `{ total, page, pages, entries: [{ identityId, name }] }`. `Server has no bans to list.` leaves the field out. |
| `status` | both | `ok`, `failed`, `no answer` or `usage error` — the same four shapes the `--- done:` line has. |
| `error` | both | The answer that made it a failure, the client's own grammar message for `usage error`, otherwise `null`. |
| `exitCode` | both | `0`, `2`, `4` or `5` — what a one-shot run would have exited with. |
| `seq`, `ack` | both | The sequence number used and the server's acknowledgement; both `null` for a `usage error`, because nothing was sent. An acknowledgement is **not** a success signal. |
| `commands[]` | one-shot | One entry per command of the run, in order, with the fields above. |
| `success`, `loggedOut`, `logout`, `error` | one-shot | The run as a whole: whether any command failed or went unanswered, and what happened to the `@logout` (a logout that was acknowledged frees the `maxClients` slot at once, §6.3 of the RCON document). |
| `host`, `port`, `clientId` | shell line, and the top level of a one-shot result | Where the session is connected; `clientId` is `null` if the login never happened. |

## 1. What counts as an admin

Two unrelated permission systems exist, and each command checks both separately:

- `ERCONPermissions` — for the RCON path: `PERMISSIONS_NONE`, `PERMISSIONS_MONITOR`,
  `PERMISSIONS_ADMIN`. Three values, no finer granularity.
- `EPlayerRole` — for the chat path: `NONE`, `ADMINISTRATOR`, `SESSION_ADMINISTRATOR`,
  `GAME_MASTER`.

An RCON client does not "log in": it authenticates with the password from the config when
it connects. `#login` and `#logout` are chat commands and are unavailable over RCON; the
single RCON-side counterpart is `@logout`, which is not a game command at all but a **protocol
command** the RCON layer handles itself — verified on 1.8.0.13, with the log line
`[RCON] [CLIENT: 0] Received Protocol Command: @logout` (where a game command gives
`Received Game Command`) followed by `[RCON] Client 0 logged out!`. It is what releases a
`maxClients` slot immediately instead of after the 45-second timeout (RCON §6.3), and **it is
available under both `admin` and `monitor`** — verified on a `monitor` server that was refusing
`kick 1` with `missing permission 'kick 1'` at the same moment.

## 2. Configuration

```json
"rcon": {
  "address": "127.0.0.1",
  "port": 19999,
  "password": "ChangeMe123",
  "maxClients": 4,
  "permission": "admin",
  "blacklist": [],
  "whitelist": []
}
```

| Key | Type | Default | Notes |
|---|---|---|---|
| `address` | string | — | Socket bind address; marked **required** by the wiki. `127.0.0.1` for local access |
| `port` | number 1..65535 | 19999 | Out-of-range is not fatal: `[RCON] Invalid port, set to default=19999...` |
| `password` | string | — | **Required for RCON to start.** No spaces, at least 3 characters |
| `maxClients` | number 1..16 | 16 | Simultaneous RCON clients |
| `permission` | string | — | `"admin"` — anything; `"monitor"` — read-only (`#players` only) |
| `blacklist` | array | `[]` | Commands excluded from execution |
| `whitelist` | array | `[]` | If set, only the listed commands are allowed |

The whole `rcon` block is optional — a server without it simply has no remote console.

Startup parameters override the file: `-rconPort <port>`, `-rconPassword <string>`, and
`-rconIpAdress <IP>` — note the **typo in the engine itself**: `Adress`, no `d`.

Verify that it came up — this line must be in `console.log`:

```
BACKEND : [RCON] Init, Ip address=127.0.0.1 and Port=19999
```

Failure lines, all from `ArmaReforgerServer.exe` of build 1.8.0.13:

| Log line | Cause |
|---|---|
| `[RCON] Init failed... Missing password or password length < 3 characters !!!` | No password, or shorter than 3 characters |
| `[RCON] Init failed... RCON is now turned off.` | Consequence of the previous line — RCON is disabled |
| `[RCON] Invalid port, set to default=19999...` | `rcon.port` out of range; **not fatal** |
| `[RCON] run failed, net socket invalid` | Socket did not open — usually the port is taken or `address` is wrong |

## 3. Permission matrix

| Command | RCON `admin` | RCON `monitor` | Chat: logged admin | Chat: voted admin | Chat: player |
|---|:---:|:---:|:---:|:---:|:---:|
| `#players` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `#kick <playerId>` | ✔ | — | ✔ | — | — |
| `#ban …` | ✔ | — | ✔ | — | — |
| `#restart` | ✔ | — | ✔ | — | — |
| `#shutdown` | ✔ | — | ✔ | — | — |
| `#login` | — | — | — | — | ✔ (chat only) |
| `#logout` | — | — | ✔ | ✔ | — |
| `#roles` | — | — | ✔ | ✔ | ✔ |
| `#id` | — | — | ✔ | ✔ | ✔ |
| `@logout` | ✔ | ✔ | — | — | — |

Practical reading:

- **`#players` is the only command `monitor` may run.** That is exactly what monitoring
  needs: the player list, with no way to change anything.
- **`#restart`, `#shutdown`, `#kick`, `#ban` all require `admin`** — and, in chat, a
  *logged-in* administrator; a voted-in admin cannot use them.
- **`#login`, `#logout`, `#roles`, `#id` do not exist over RCON.** They are chat commands.
- A command can work over RCON and be refused in chat, and vice versa — the two checks are
  independent (`RequiredRCONPermission()` vs `RequiredChatPermission()`).

## 4. Commands

| Command | Syntax | What it does |
|---|---|---|
| `#players` | `#players` | Player list with each `playerId` |
| `#kick` | `#kick <playerId>` | Eject a player; they may rejoin |
| `#ban create` | `#ban create <playerId\|identityId\|"name"> <seconds> <reason>` | Ban. `0` seconds = permanent; the reason is optional |
| `#ban remove` | `#ban remove <identityId\|name>` | Lift a ban |
| `#restart` | `#restart` | Restart the current scenario, **keeping clients connected** |
| `#shutdown` | `#shutdown` | Shut the server down, disconnecting everyone |
| `@logout` | `0x01 \| seq \| @logout` | RCON only, since 1.2.1: a protocol command (not a game command) that de-authenticates the client and frees the connection immediately — verified working on 1.8.0.13, where the slot is reusable at once |

Details that are only visible in the source (`BanCommands.c`):

- `#ban` **works on dedicated servers only** — the first check in the handler returns
  `Command is supported only on Dedicated Servers`. `#kick` has no such check.
- The identifier type is detected by format: 36 characters with dashes at 8, 13, 18, 23 →
  `identityId`; digits only → `playerId`; anything else → a player name.
- **`playerId` only works for a connected player.** For someone who already left, use
  `identityId` — `#ban list` prints it.
- Names with spaces must be quoted: `#ban create "Name with spaces" 3600 reason`.
- Negative durations are refused; the default reason is `No reason provided`.
- `#ban remove` by name tries an exact match first, then a `STARTS_WITH` match, logging
  `Retrying unban of user with user name: '%1'`.
- Ban list page size is a constant in code, not a setting: **25 per page over RCON,
  10 per page in chat** (`playerId == 0` means RCON).
- Bans go through Bohemia's backend (`BackendApi.GetBanServiceApi()` →
  `CreateBanPlayerId` / `CreateBanIdentityId` / `RemoveBans` / `RemoveBanByName` /
  `RequestServerBanList`), which is why these commands answer asynchronously
  (`EServerCmdResultType.PENDING` + `OnUpdate()`) and why an offline server cannot list
  or lift bans.

## 5. What the server answers

These are command answers, not log lines — do not grep `console.log` for them.

| Answer | Command | When |
|---|---|---|
| `Not Valid Player ID` | `#kick`, `#ban` | Identifier less than 1 |
| `Player not found` | `#kick`, `#ban create` | No connected player with that `playerId` |
| `Not Valid time value in seconds` | `#ban create` | Negative duration |
| `Not Valid page number` | `#ban list` | Page number below 1 |
| `Page not found!` | `#ban list` | Page beyond the page count |
| `Server has no bans to list.` | `#ban list` | No bans recorded |
| `Multiple users found! Please use a unique identifier.` | `#ban create` / `#ban remove` by name | The name matches several players (a hint, not an error) |
| `User not found!` | `#ban remove` | No ban matched, exactly or by prefix |
| `Player '<name>' kicked!` | `#kick` | Success |
| `Player '<name>' banned!` | `#ban create` | Success; the player is also kicked with reason `BAN` |
| `Ban removed!` | `#ban remove` | Success |
| `Command is supported only on Dedicated Servers` | `#ban` | Server is not dedicated |
| `missing permission '<command>'` | any | The command needs more than `rcon.permission` allows — `kick 1` or `ban list 1` on a `monitor` server. **Observed live on 1.8.0.13**; it arrives after `Processing Command: …` |
| `unknown command '<text>'` | any | No such keyword among the game commands. Also observed live, and also after `Processing Command: …` |
| `invalid parameters '<command>'` | any | Too few arguments — `kick`, `ban create`, `ban create 1`. Also observed live; this is what the `PARAMETERS` result type looks like over RCON, and a bare `ban` is *not* it (it prints the help text and succeeds) |
| `the server is busy` | any | A `BUSY` result type. From the binary's literal table only, not reproduced |
| `Processing ban list` | `#ban list` | The request went to the backend, the answer comes later |
| `Timeout` | `#ban …` | The backend did not answer |
| `Failed to create ban.` / `Failed to remove ban.` / `Failed to list bans.` | `#ban …` | The backend rejected the call outright |
| `Unknown error.` | `#ban …` | `EACODE_ERROR_UNKNOWN` from the backend |

An empty answer with result type `PARAMETERS` is how the *source* describes `#kick` with too few
arguments — over RCON the client does not see emptiness, it sees `invalid parameters '<command>'`
(and the client's own grammar refuses `kick`/`ban` with missing arguments before sending, exit 2).
A bare `#ban` is answered with its own help screen instead, which is what `cmd ban` shows and what
`tools/rcon.mjs` classifies as a missing-parameter failure (exit 5) on that path. `#restart` is the
one command observed answering nothing at all: `Processing Command: restart` and then silence, which
costs a waiting client its whole timeout; an unknown *protocol* command (`@foo`) is acknowledged and
then answered with nothing, which is exit `4` — no *message*, even though a packet came back.
**An `0x01|seq` acknowledgement plus a `Processing Command:` note therefore proves that the command
was routed, not that it ran** — the answer that decides is the one after it.

## 6. Diagnostics

Healthy lifecycle in the log:

```
[RCON] run started
[RCON] Login packet received
[RCON] 192.168.1.5:54321 Authorized as Client #0 | Connected clients: [1/4]
[RCON] [CLIENT: 0] Received Game Command: players
[RCON] Process Command: players
[RCON] [ID:0] Sent Message for client: ...
[RCON] [CLIENT: 0] Received Protocol Command: @logout
[RCON] Client 0 logged out!
[RCON] destroying...
```

| Log line | What happened |
|---|---|
| `[RCON] Client List is full! Dropping connection with %d.%d.%d.%d:%d` | `rcon.maxClients` reached |
| `[RCON] %d.%d.%d.%d:%d Authorization DENIED` | **Wrong password** |
| `[RCON] [ID:%d] [CLIENT: ...] Unauthorized Client! Command: %s` | A command was sent **before** authentication |
| `[RCON] [ID:%d] [CLIENT: %d] Mismatched sequence number! Command: %s` | Packet numbering broken — usually a client bug. **Not emitted on 1.8.0.13**: a wrong `seq` there produces no log line at all, and the command is silently ignored (RCON §1.1) |
| `[RCON] Unknown protocol command: %s` | The client sent something that is not a protocol command |
| `[RCON] [CLIENT: %d] Received Protocol Command: %s` | The RCON layer handled it itself (`@logout`) instead of handing it to the game. Look for this line when a command "did nothing" |
| `[RCON] Client %d logged out!` | `@logout` ran; the slot is free at once |
| `[RCON] Invalid packet received` | Malformed packet — typically the wrong protocol (TCP instead of UDP, or the reverse) |
| `[RCON] message[%i] attempt[%i] TIMEOUT` | The client did not acknowledge a message; the server retries |
| `[RCON] Dropped client: #%d` | Client dropped — timeout or retry limit exceeded |
| `[RCON] output queue exceeded its capacity!` | Outgoing queue full — the client is not reading its answers |
| `[RCON] Failed to send message to client. Connection Refused!` | The connection was closed on the client side |
| `[RCON] [CLIENT: %d] No Command` | The empty keep-alive (`0x01\|seq`) arrived — normal, and what holds a session open past 45 s |
| `RCONCommandHandler: Executing command {%s}.` | The command reached the game handler |

**The 45-second rule, and the way around it.** The BattlEye v2 specification requires *some* command
packet — the empty `0x01|seq` counts — at least every 45 seconds; measured on 1.8.0.13, four
clients were dropped 45–48 s after they logged in, in order. So **a client that is merely closed
keeps its `maxClients` slot for that long**, which is how a working password turns into "no answer
at all" on the next run. `@logout` is the way out: the server logs `Received Protocol Command:
@logout` and `Client 0 logged out!` and the slot is reusable immediately — with `maxClients: 1`,
three consecutive runs of [`tools/rcon.mjs`](../../tools/rcon.mjs) were each authorized as client
`#0` at `[1/1]`. Raise `maxClients` if several clients must coexist, and let a client log out
rather than be killed.

## 7. Boundaries of reliability

- The **packet format is known**: BattlEye RCon v2, recovered by talking to a running
  1.8.0.13 server with a purpose-written client (RCON §1.1) — including the sequence-number rule,
  `@logout`, and the empty keep-alive. Still open: whether a BattlEye
  client interoperates with `rcon.port`, and whether the absent CRC check on incoming packets is
  deliberate.
- **The transport is UDP** — verified by running the server with the port set and inspecting
  the socket (§0). The packet format is recovered as well, so do not report either as unknown.
- The **commands exercised live** so far are `#players`, `#ban` (help), `#ban list`,
  `#ban create`, `#ban remove`, `#shutdown`, the protocol command `@logout` and the empty
  keep-alive, plus the four login framings, the sequence rule, a client dropped by the
  45-second timeout, `@logout` on a `monitor` server (which refuses `kick 1` with
  `missing permission 'kick 1'` while still honouring the logout), `unknown command '<text>'`,
  and `invalid parameters '<command>'` for `kick`/`ban create` — with `#restart` as the one
  command observed answering nothing at all; the rest of the list below is wiki-only.
- The **command list and the permission matrix** come from the BI wiki page
  "Server Management" (revision `oldid=370483`, 2024-12-18), which is **older than build
  1.8.0.13**. Commands added later are missing from it.
- **Only `BanCommand` and `KickCommand` exist in public sources**
  (`scripts/Game/Network/ServerCommands/BanCommands.c` is the only file in that
  directory). `#login`, `#logout`, `#roles`, `#id`, `#players`, `#restart` and
  `#shutdown` are engine-side and appear in no public script mirror — their syntax and
  permissions are wiki-only and must be confirmed on a live server.
- Statements about code (`ERCONPermissions`, `EPlayerRole`, `EServerCmdResultType`,
  the `ScrServerCommand` shape, ban and kick logic, all answer strings) were checked
  through Arma Reforger Explorer 1.7.0.54, which is **older** than 1.8.0.13; the files are also in
  its `data007.pak`, and the binary of this build is what settles an answer string.
- Log strings come from `ArmaReforgerServer.exe` 1.8.0.13, so they match that build.
- `maxClients` default 16 and range 1..16 come from the wiki.

## 8. Verification checklist

Before reporting an RCON result:

- [ ] Did you use [`tools/rcon.mjs`](../../tools/rcon.mjs) rather than a hand-written client or a
      hand-crafted packet? If you wrote code instead, say why the tool could not be used.
- [ ] Is `[RCON] Init` present in the log, with the expected address and port?
- [ ] If you re-checked the transport, did you confirm it as UDP (`ss -lunp`, or
      `Get-NetUDPEndpoint` on Windows) and see **no** TCP listener? Both the transport and the
      packet format are established — do not report either as unconfirmed.
- [ ] If a command failed: did you quote the exact answer from §5 rather than paraphrase it?
- [ ] Did you end the session with `@logout` (or use the tool, which does it for you), rather than
      leaving a `maxClients` slot busy for 45 s? If commands went unanswered, did you check for
      `[RCON] Client List is full!` before blaming the password?
- [ ] If a command "did nothing": is there a `Received Game Command: <cmd>` or a
      `Received Protocol Command:` line for it in the log? An `0x01|seq` acknowledgement on the
      wire does **not** mean the command ran.
- [ ] If the client is `BERCon.exe`: did you say plainly that it belongs to BattlEye's own
      endpoint, and that pointing it at `rcon.port` has not been tried?
- [ ] If a ban or unban was involved: is the server dedicated and is the backend reachable?

## 9. Reference documents in this workspace

All documents live in `docs/en/`, and these skills use their terminology; the Russian

- [ArmaReforger_RCON_EN.md](../../docs/en/ArmaReforger_RCON_EN.md) — the full treatment: the
  packet format (its §1.1), config keys, permission enums, per-command breakdown from source, the
  answer table (§4.6), and log-based diagnostics.
- [`tools/rcon.mjs`](../../tools/rcon.mjs) — the client described in §0; `--help` lists every
  subcommand, and `probe` re-checks the framing on a new build.
- [ArmaReforger_ServerConfig_EN.md](../../docs/en/ArmaReforger_ServerConfig_EN.md) — the `rcon`
  block in context of the whole `server.json`, §5.3, plus the admin keys `passwordAdmin`
  and `admins` in §5.4 that chat commands depend on.
- [ArmaReforger_StartupParams_EN.md](../../docs/en/ArmaReforger_StartupParams_EN.md) — the
  `-rcon*` parameters, and Appendix A.5 on Linux hosting.
- [ArmaReforger_Profile_EN.md](../../docs/en/ArmaReforger_Profile_EN.md) — the profile directory,
  where `console.log` with the `[RCON]` lines lives.
- [ArmaReforger_Scenarios_EN.md](../../docs/en/ArmaReforger_Scenarios_EN.md) — what `#restart`
  restarts, and the GUID table a `scenarioId` needs.
- [`tools/verify-against-install.mjs`](../../tools/verify-against-install.mjs) — re-check the
  `rcon` keys, and every other name the documents rely on, after a game update.
- [`tools/validate-skills-and-links.mjs`](../../tools/validate-skills-and-links.mjs) and
  [`tools/validate-doc-json.mjs`](../../tools/validate-doc-json.mjs) — run after editing
  any document or skill here.
- [`schemas/rcon-result.schema.json`](../../schemas/rcon-result.schema.json) — the JSON shapes of
  §0 in machine-readable form, and [`tools/check-rcon-schema.mjs`](../../tools/check-rcon-schema.mjs)
  (`npm run check:rcon-schema`), which validates the examples above against it and fails if the
  schema stops rejecting a shape it should. It also takes a file argument, so captured output of a
  real run can be checked the same way.

Source tags used in the guides: `[wiki]` = BI wiki, `[binary]` = string found in

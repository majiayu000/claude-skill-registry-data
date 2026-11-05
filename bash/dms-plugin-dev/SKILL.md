---
name: dms-plugin-dev
description: Run and drive a DankMaterialShell (DMS) plugin by observation, in real DMS inside an isolated headless sway — keys, pointer, screenshots and QML logs — with no effect on the live desktop. Use when developing, fixing or reviewing a DMS bar plugin or its QML, when a QML change needs loading before a switch, or when asking how a plugin renders or responds.
compatibility: Requires nix, plus qs and dms on PATH.
---

A DMS plugin's QML is only checked by loading it, and `qmllint` can't resolve DMS's types, so a lint proves little. Load it in real DMS and look.

`scripts/sandbox.sh` starts one. It has its own `HOME`, runtime dir and no session bus, so its keys can't reach your windows, and a daemon started in it can't reach your live one. It copies your bar layout and colours, and takes the plugin from the working tree.

## Tools

| Command                                                     | Does                                                             |
| ----------------------------------------------------------- | ---------------------------------------------------------------- |
| `sandbox.sh up --plugin <dir>=<id> [--size WxH]`            | Fresh sandbox, replacing the last; waits for the plugin to load  |
| `sandbox.sh bg <name> <cmd...>` / `sandbox.sh run <cmd...>` | A long-lived process, logged to `<name>.log` / a command, inside |
| `sandbox.sh key <wtype args>`                               | `key j`, `key -k Return`, `key -k Escape`                        |
| `sandbox.sh move\|click <x> <y>` / `wheel <x> <y> <n>`      | Pointer; `n` clicks down, negative for up                        |
| `sandbox.sh ipc <target> <function> [args]`                 | DMS's own IPC, as `dms ipc call` takes it                        |
| `sandbox.sh shot [name]`                                    | Screenshot; prints the PNG path, which `Read` shows you          |
| `sandbox.sh log [regex]`                                    | The shell's log, filtered                                        |
| `sandbox.sh status` / `sandbox.sh down`                     | Is it up / stop everything in it                                 |

The run dir is `/tmp/dms-sandbox/<dir-hash>/`, one per working directory. `run` and `bg` get the sandbox's environment, so resolve anything that needs nix or your real `HOME` before the call, and pass it in.

## The loop

```bash
S=skills/dms-plugin-dev/scripts/sandbox.sh
bash $S up --plugin path/to/plugin=myPlugin
bash $S log 'myPlugin|TypeError|ReferenceError|is not a type'
bash $S ipc widget toggle myPlugin
bash $S shot open
```

Read the log first: a QML error names its file and line. Then read the screenshot, since a plugin can load cleanly and still draw wrong. After a QML edit, run `up` again; there is no reload.

## agent-hub

```bash
HUB=$(nix build --no-link --print-out-paths .#agent-hub)/bin/agent-hub
bash $S up --plugin modules/desktop/dms/agent-hub/plugin=agentHub
bash $S bg hub "$HUB" daemon
bash $S bg demo "$HUB" demo        # fake sessions in every state
bash $S ipc widget toggle agentHub
bash $S run "$HUB" status
```

`docs/agent-hub.md` has what the popout's keys do. Its prompts and forms answer only what is in the sandbox.

For a real agent behind the plugin, keep its config dir inside the sandbox, or it registers with your live hub. Copy its settings and link only its login, so a token refresh reaches the real file:

```bash
bash $S run sh -c 'mkdir -p "$HOME/.claude/sessions"; install -m 644 "$REAL_HOME/.claude/settings.json" "$HOME/.claude/settings.json"; ln -s "$REAL_HOME/.claude/.credentials.json" "$HOME/.claude/"'
bash $S run sh -c 'CLAUDE_CONFIG_DIR="$HOME/.claude" tmux -L sandbox new-session -d -s agent claude'
```

## Traps

- Files a plugin's Nix build adds are missing from the working tree. agent-hub's `icons/claude.svg` is one: a `Cannot open` on it means nothing here.
- Without `niri`, focus goes to sway's rules, so check anything about clicking a layer surface for keys on your real compositor too.
- A popout opened with `ipc` takes the keyboard; the plugin only sees `key` while it is open.
- `wtype` waits for the seat: `key` right after `up` can land before a surface has focus. Take a `shot` when a key seems ignored.
- Never link a sandboxed Claude to your real `settings.json`. It rewrites that file through the link, which replaces a home-manager symlink with a plain file and makes the next switch fail with `would be clobbered`.
- Never stop a sandbox by process name. The live shell runs the same store paths; `down` finds them by their runtime dir.

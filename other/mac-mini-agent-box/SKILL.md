---
name: mac-mini-agent-box
description: "Run a Mac mini as a shared, always-on agent box exactly the way the Edge team runs one: the owner's desktop user logs in by itself, a separate SSH user for agents and helpers, Tailscale (node shared with a teammate), Claude Code kept alive in a tmux session that has screen permissions, logged-in Chrome profiles that agents drive over CDP, real screen-recorded demos, form filling through a real browser, secrets kept out of prompts and files, shared-machine etiquette and a verification checklist. Use when someone wants an always-on Mac or Mac mini for Claude Code, wants to reach it from laptop and phone, wants to share it with a teammate's agents, or wants to run browser automation, demo recording or form filling on a real Mac with a home IP."
---

# Mac mini agent box

This packages the setup the Edge team runs on a shared Mac mini, and the three flows that use it,
so the owner of a Mac mini can run it the same way. The owner may not be an engineer: explain each
step in one plain sentence, give one command at a time, and wait for "done" before the next.

```
 owner laptop / phone --+                     Mac mini (headless, always on)
                        +-- Tailscale ------> +-- desktop user "owner"  auto-login, Chrome profiles, apps
 helper (teammate) -----+   (node shared)     +-- SSH user "helper"     key-only, used by agents
                                              +-- tmux "cc" running claude, started from Terminal
                                              +-- keep-awake + keeper LaunchAgents
                                              +-- Screen Sharing for logins and recordings
```

Names here are placeholders: the box is `agent-box`, the desktop user is `owner`, the SSH user for
agents and teammates is `helper`. Never write the real names, addresses, keys or passwords into
chat, notes or files.

## Ground rules (read first)

- **Never cut the connection you are using.** Do not quit or log out of Tailscale, run
  `tailscale down`, turn off Remote Login or Screen Sharing, change the firewall, or reboot, unless
  someone is at the box. If the node stops answering, the share probably lapsed; fixing that is a
  human step (owner re-shares, helper accepts).
- **It is a shared machine and the owner uses it live.** Before acting: `who`, and
  `ps aux | grep -iE "screensharingd|Claude" | grep -v grep`. If the owner is working, pause and ask.
  Never quit or close the owner's apps or windows (cover or hide them), never change their settings,
  accounts or files, and leave the box exactly as you found it.
- **Secrets never go into a prompt, a file, git or shell history** (step 6).
- If you are Claude on the box, run commands yourself; `sudo` asks for the password in the terminal,
  never in chat. If you are elsewhere (Claude app, another machine), show the commands for the owner
  to paste.

## Step 1. The setup as we run it

Do this once, sitting at the box (or Screen Sharing on the same home network). Details and every
command: `references/setup.md`.

1. **Two users.** The owner's normal desktop user (`owner`) logs in automatically, so apps, Chrome
   profiles and the screen are there after every restart. A separate admin user `helper` is for SSH
   only: agents and teammates log in as `helper` and act inside the owner's desktop session through
   `sudo launchctl asuser`. Optional, our setup: passwordless sudo for `helper` (trust decision, see
   setup.md).
2. **Auto-login means FileVault off.** macOS cannot do both. We chose auto-login so the box comes back
   by itself after a power cut. Keep the box in a private place. The tradeoff table is in setup.md.
3. **Never sleep, restart after power failure, keep-awake agent:** `pmset` lines plus a small
   `caffeinate` LaunchAgent (setup.md).
4. **Remote Login and Screen Sharing on** for `owner` and `helper`.
5. **Homebrew** (`brew`), `tmux`, `ffmpeg`, `python3` with `websocket-client`.

## Step 2. Tailscale and access from laptop and phone

`references/tailscale-and-ssh.md` covers it end to end. In short:

1. Tailscale Mac app on the box, signed in to the owner's account. Rename the machine `agent-box`,
   **Disable key expiry**, MagicDNS on.
2. Laptop and phone: Tailscale app, same account. SSH keys for laptop and phone (Termius or Blink
   Shell). Password login off once keys work.
3. **Share the node with a teammate:** admin console, Machines, Share. The teammate accepts with their
   own Tailscale account, reaches the box by its full `.ts.net` name, logs in as `helper` with their
   own key.

Test from the laptop on a different network (phone hotspot): `ssh helper@agent-box`.

## Step 3. Claude Code that is always there

We run Claude Code in a tmux session named `cc` that is started **from Terminal.app inside the
owner's desktop session**. That matters: anything running in that tmux inherits Terminal's macOS
permissions (Screen Recording, Automation), which plain SSH sessions never get. A keeper LaunchAgent
checks every 2 minutes and restarts the session if it is gone, so it comes back after a reboot.

Install and the keeper scripts: `references/claude-code-sessions.md`. Then, from any device:

```bash
ssh owner@agent-box                     # the owner
tmux attach -t cc                       # see Claude; Ctrl-b then d leaves it running

ssh helper@agent-box                    # a teammate, then attach to the owner's session:
sudo -u owner -H /opt/homebrew/bin/tmux attach -t cc
```

For a session of your own, use your own name: `tmux new -A -s yourname`. Never kill `cc`.

## Step 4. Skills and house rules

In Claude on the box, paste:

```
Set up Edge for me: read getedge.cc/SKILL.md and follow it
```

Then install the recording skill this box is used for:

```bash
npx skills add getedgehq/skills --skill record-mac-demo
```

Write `~/.claude/CLAUDE.md` for the user Claude runs as, from `references/claude-md-template.md`.

## Step 5. The flows we run on the box

Pick the one the task needs and read its reference before acting.

| Task | Read | What it does |
|---|---|---|
| Real screen-recorded product demo for a launch video | `references/recording.md` + skill `record-mac-demo` | Agent drives the Mac over VNC with zero clicks, macOS records at 60 fps, action log becomes captions |
| Keep logged-in browser accounts running for agents | `references/browser-cdp.md` | One Chrome profile per account as a LaunchAgent in the owner's session, driven over CDP; logins survive reboots |
| Fill and submit web forms from a real home IP | `references/apply-forms.md` + `scripts/cdp_tab.py` | Isolated tab on the logged-in Chrome, fill, screenshot, verify, submit only when correct |

Shared rules for all three: work in your own tab, window or tmux session; never quit Chrome or touch
another account's tab; never solve a CAPTCHA or type someone's password; a login or 2FA is a human
step done over Screen Sharing; clean up everything you created.

## Step 6. Secrets

**A secret is fetched by the command that needs it, when it runs, and goes nowhere else.** Store it in
the Keychain of the user that runs the command (prompts for the value, so it never hits history):

```bash
security add-generic-password -a "$USER" -s MY_API_KEY -w
MY_API_KEY="$(security find-generic-password -a "$USER" -s MY_API_KEY -w)" some-tool
```

Passwords for Screen Sharing or a website are typed by a human, or read from the Keychain into the
one process that needs them. 1Password or Bitwarden CLIs, blocking Claude from reading key files, and
what to do after a leak: `references/secrets.md`.

## Step 7. Backups and updates

Time Machine or a nightly `rsync` of the work folders to an external disk; restore one file to prove
it. Updates: `brew upgrade`, `claude update`, macOS with a planned restart while someone can check the
box. Details: `references/safety-backups-updates.md`.

## Step 8. Verification checklist

Run `scripts/check-box.sh` on the box (read-only), then the manual tests. Report each line PASS or FAIL
with what you saw; never mark a line passed that you did not see.

- [ ] `pmset -g` shows `sleep 0` and `autorestart 1`; the caffeinate agent is running.
- [ ] Tailscale connected; key expiry disabled; teammate (if any) reaches the full `.ts.net` name.
- [ ] Laptop on another network: `ssh helper@agent-box` works with a key, no password prompt.
- [ ] Password login refused: `ssh -o PubkeyAuthentication=no helper@agent-box` fails.
- [ ] Phone on mobile data: SSH app connects; `tmux attach -t cc` shows Claude.
- [ ] **Survives disconnect:** start a long task in `cc`, kill the SSH app, reconnect; still running.
- [ ] **Survives reboot** (owner present): restart; within 5 minutes the box is reachable from the
      phone, auto-logged in, `cc` is back with Claude logged in, Chrome profiles are back.
- [ ] Screen Sharing from the laptop: `vnc://agent-box` shows the owner's desktop.
- [ ] `screencapture` works from inside `cc` (proves the Terminal permissions path).
- [ ] Edge answers in a fresh Claude session; `~/.claude/CLAUDE.md` exists.
- [ ] Secret scan in `check-box.sh` is clean; a backup exists and one file was restored.

When all pass, give the owner a five-line cheat sheet: connect from laptop, from phone, attach to
`cc`, detach, and who to ask before a reboot.

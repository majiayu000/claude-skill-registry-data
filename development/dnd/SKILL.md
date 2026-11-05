---
name: dnd
description: Do not disturb for the kit's panes (history, dev activity, reminders, handoffs). Creates profiles that hide a pane or keep only some repos, groups or the session's folder, turns one on by hand (for a while, for this session or the whole computer), and sets the rules that turn one on by themselves (a Wi-Fi network, days and hours, a folder). Use when the user says "do not disturb", "DnD", "focus mode", "I'm in a meeting", "at the office only show…", "hide the PRs", "only this repo", "make a work profile", "turn on <profile>", "turn it off", or when a pane shows something the user wants out of the way.
---

# Do not disturb

`dnd.sh`, next to this file, holds the profiles and their rules. The dnd mod reads it every minute
and the history, dev activity and reminders-handoffs panes hide or filter what they show by what is on.
Run it with `bash`; `bash dnd.sh` alone prints every command.

## What a profile holds

One line per part: `history`, `prs`, `reminders`, `handoffs`, each `show` (the default), `hide`, or
`only` a list of names. A name is a repo (`owner/repo` or its last part), a reminder group or
folder, a handoff's repo; `@here` keeps what belongs to the session's folder (its git repo).
History is shown or hidden, never filtered.

```bash
bash dnd.sh set work prs only Workcare @here
bash dnd.sh set work reminders only Acme
bash dnd.sh set meeting history hide
bash dnd.sh list
```

The user can also pick in the Do not disturb pane (`/dnd`, or its button in the Configuration
pane, opened from the band above the prompt or `/configuration`), or on a terminal: `bash dnd.sh edit work` (arrows,
Enter or Space, the installer's keys). In the pane, `edit` beside a profile opens it: a button per
mode for each part, and for `only` a checklist of the session's folder, what the part lists now
and every repo and folder the user works in. Before you create a profile, ask what it should keep
or hide when the user did not say; propose the names `dnd.sh known prs|reminders|handoffs` prints,
or the repos and folders under `workspaces` in `dnd.sh json`.

Every mod's settings are in the Configuration pane (the configuration mod, which the kit's pane
mods bring with them), for all computers or this one.

## Turning one on by hand

`bash dnd.sh on PROFILE [30m|2h|1d|HH:MM]`, `bash dnd.sh off`. `none` is a profile that shows
everything: `on none 2h` quiets the rules for two hours.

Ask the user whether it is for **this session only**, for **this computer** (every session on it)
or for **all computers** (every computer in the config sync, at its next sync), unless they already
said so in their words ("just here", "on this Mac", "everywhere"). For this session, add
`--session "$CLAUDE_CODE_SESSION_ID"` to `on` and to `off`; for all computers, `--everywhere` to
`on` (`off` takes the computer's switch and that one off together). A meeting is a profile turned
on by hand for how long it lasts.

## Rules that turn one on by themselves

`bash dnd.sh rule PROFILE KEY=VALUE...`, every key must hold:

- `wifi=NAME`: on that Wi-Fi network (`bash dnd.sh wifi` tells the current one).
- `days=weekend` (or `weekday`, `day`, `sat,sun`, `mon,tue`...), `from=09:00`, `to=18:00`; a span
  past midnight (`from=22:00 to=07:00`) works.
- `folder=~/dev/shop`: sessions in that folder or below; a repo's own default.

A turn-on by hand wins over the rules (the session's, then the computer's, then every computer's),
then rules with a folder, then the others in their order.
`bash dnd.sh unrule N` deletes the Nth rule as `list` numbers them.

## Where it lives

Profiles and rules: `~/.claude-sync/dnd/profiles.json` when the config sync is set up (every
computer gets them), else `~/.claude/dnd/profiles.json`. The switch and the last Wi-Fi name stay on
the computer, in `~/.claude/.dnd/`, beside `active.json`, what is on per session, which the kit's
status line shows as `🔕 <profile> · session|computer|everywhere|rule` while one is on. The switch
for every computer is kept in `profiles.json`, with the profiles. Tell the user which one you changed.

---
name: novoads-update
metadata: {packVersion: 1.3.0}
description: >-
  Updates this skill pack from upstream, and owns the consent that decides whether it ever
  updates on its own. Checks whether the clone is behind, asks the user — update now, always
  keep me up to date, not now, or never ask again — and carries out the answer: applies the
  update through ./scripts/update.sh, records the consent flag the SessionStart hook already
  reads, snoozes on an escalating ladder, or turns the check off for good. Summarizes what
  changed between the two commits from the CHANGELOG. Use when the user asks to update or
  upgrade the pack, get the latest skills or the newest version, when the session banner
  reports that updates are available, when they ask whether their clone is current, when
  they want unattended updates switched on or off, or when they want to stop being asked.
  It never applies an update without an answer, and notify-only is the default.
---

# Update the pack

This pack is a git clone. Updating it is a merge, and a merge on someone else's
working tree is a decision only they can make — so this skill's real product is
the question, not the update. Ask, then do exactly what was answered.

**Notify-only is the default and stays the default.** Nothing here turns on
unattended updating unless the user picks the option that says so, in their own
words, in the dialog below.

## Step 0 — confirm this is the pack clone, before anything else

This skill manages a **cloned** pack: a git repository with `scripts/update.sh`
in it. It can also be installed on its own, copied into someone's `~/.claude/`
alongside skills that have nothing to do with this repo — and in that shape
every instruction below is pointed at the wrong repository. Step 1's git
commands would report on the **user's own project**, and option 2 would write a
consent flag into a directory no hook will ever read.

**Every command in this skill runs from the clone root.** Move there first, and
keep doing it at the top of each block below — a session can open anywhere, and
this is the one thing that silently changes what the commands mean:

```bash
root="$(git rev-parse --show-toplevel 2>/dev/null)" && [ -n "$root" ] && cd "$root"

if git remote get-url origin 2>/dev/null | grep -qE 'novoads/(claude-code-ads|agent-skills)' \
   || [ -f shared/scripts/auto-update.sh ]; then
  echo "pack clone confirmed"
else
  echo "NOT the pack clone — stop here"
fi
```

**Both slugs, on purpose.** The repo was `novoads/claude-code-ads` until
2026-08-13 and is `novoads/agent-skills` now. GitHub's 301 keeps every clone
made before the rename working — `git fetch` follows it — but it does not
rewrite `origin` in that clone's config, so those users' remote still reads the
old slug and always will until they re-point it. Matching only the new name
would tell every pre-rename clone it is not the pack, which is exactly the
population this skill exists to update.

Git commands walk up to find the repository; **plain paths do not.** From a
subdirectory `./scripts/update.sh` is simply not found, `[ -f shared/scripts/... ]`
reports a false negative on a real clone, and a `.update-state/config` written
there lands somewhere no hook will ever read — consent recorded, nothing
reading it, which is the exact failure this pack's design exists to prevent.

If neither probe fires, **stop here and offer none of the four options.** Say
plainly:

> This skill manages the cloned pack — the git repository with the skills and
> `scripts/update.sh` in it. This looks like a solo install, so there is no
> clone here to update. Solo-installed skills update with
> `npx skills update`. Be aware before running it: it replaces the installed
> files outright, with no backup, so copy any local edits somewhere safe first.

Then stop. Nothing here can update a solo install, and running the dialog would
record consent that nothing reads — which is the exact failure this pack's
design exists to make impossible. Do not offer to "try anyway".

## Step 1 — find out where the clone actually stands

Run these from the repo root. None of them changes anything:

```bash
cd "$(git rev-parse --show-toplevel)"                 # every path below is root-relative
git rev-parse --abbrev-ref HEAD                       # expect: main
git fetch --quiet origin main 2>/dev/null || true     # bounded by git's own config
git rev-list --count HEAD..origin/main                # how many commits behind
git log --oneline HEAD..origin/main | head -10        # what they are
cat .update-state/config 2>/dev/null                  # current consent state
```

Read three things off that:

- **Behind count is 0** → say so in one line and stop. Do not run the dialog.
  A consent question with nothing to consent to is pure friction.
- **`update_check=off` in the config** → the user previously chose "never ask
  again". They have now invoked this skill by hand, which is a fresh request and
  overrides the standing one, so continue. Mention that the check is off and
  offer to turn it back on. The switch silences the automatic surfaces; it was
  never meant to strand the manual path.
- **Not on `main`, or a detached HEAD** → stop and say so. The clone is pinned
  to a commit on purpose. `./scripts/update.sh` refuses this case too, and the
  fix is `git checkout main` by a human who knows why it was pinned.

## Step 2 — ask, with these four options

Use AskUserQuestion with exactly these four, worded as written. The wording is
the contract: each option is a different promise about what happens next, and a
reworded option quietly changes which promise the user thinks they made.

| Option | Label |
|---|---|
| 1 | **Update now** |
| 2 | **Always keep me up to date** |
| 3 | **Not now** |
| 4 | **Never ask again** |

Give the question a one-line header naming what is waiting: how many commits,
and the headline of the newest one. Then act on the answer.

## Option 1 — "Update now"

```bash
cd "$(git rev-parse --show-toplevel)"
./scripts/update.sh
```

If that reports **exit 127 / not found**, you are not at the clone root — `cd`
there and re-run. Do not reach for `git pull` instead. It is not a workaround
for this, it is the path that destroys a gitignored `.env`, and `update.sh`
exists precisely because it does.

Never pass `--fresh`. The default target is the newest commit older than 24
hours, and that gap is the supply-chain buffer: it is the window in which a bad
push upstream gets noticed by someone before it lands on a customer's disk.

The script prints one machine-readable `STATUS=` line. Branch on that line, not
on any prose around it:

| STATUS | What to tell the user |
|---|---|
| `updated FROM=<sha> TO=<sha>` | Updated. Then summarize, below. |
| `current` | Already current. If stderr noted newer commits held by the cooldown, say that they land tomorrow. |
| `updated_with_conflict FROM=… TO=… STASH=<ref>` | Updated, **and their local edits are parked in `<ref>`**. Lead with the stash — that is the part with their work in it. Recover with `git stash pop <ref>`. |
| `offline` | No network. Nothing changed, the pack still works. |
| `blocked REASON=<reason>` | Nothing changed and the repo is exactly as it was. Report the reason and its fix; do not try to work around it. |
| `interrupted` | Someone stopped the run (Ctrl-C, or the terminal went away). **This is a safe state, not a broken one:** any in-flight merge was aborted, `.env` was restored, and nothing is half-applied. The remedy is to run `./scripts/update.sh` again — never a raw `git pull` to "finish the job", which is the exact thing this script exists to keep off the tree. Read its stderr before you report: if it stashed local edits first they are still in the stash and it says so, and in the one case it cannot clean up safely — a conflicted index with no stash behind it — it leaves the tree exactly as found and prints what to inspect. Exit code is nonzero. |
| `rolled_back TO=<sha>` | Only from `--rollback`. |

Then summarize what changed, in **six bullets or fewer**, from `CHANGELOG.md`
between the two commits the STATUS line names:

```bash
git log --oneline <FROM>..<TO>
git diff <FROM>..<TO> -- CHANGELOG.md
```

Write the summary for someone who uses the skills, not someone who reads diffs:
what is new, what changed under them, what broke and got fixed. Skip anything
purely internal. If the CHANGELOG diff is empty, summarize the commit subjects
instead and say that is what you used.

If the update went wrong, the way back is one command, and it is worth naming
in the same breath as any conflict: `./scripts/update.sh --rollback`.

## Option 2 — "Always keep me up to date"

Three things happen, and **all three** are required. Writing the flag is the
easy one; the other two are what make the flag mean anything.

**a. Write `auto_apply=on`, and clear any standing `update_check=off`.**

Granting "always keep me up to date" **is** revoking "never ask again". They are
separate keys, and the hook checks the kill switch *first* and exits before it
ever reads `auto_apply` — correctly, because off means off. So a user who once
picked option 4 and now picks option 2 would otherwise end up with consent
recorded, the reader registered, and nothing ever updating. Set both keys:

```bash
cd "$(git rev-parse --show-toplevel)"   # a config written elsewhere has no reader
mkdir -p .update-state
touch .update-state/config
# preserve every other key; replace or append the two this option owns
grep -vE '^[[:space:]]*(auto_apply|update_check)[[:space:]]*=' .update-state/config > .update-state/config.tmp 2>/dev/null || true
printf 'update_check=on\nauto_apply=on\n' >> .update-state/config.tmp
mv .update-state/config.tmp .update-state/config
```

If `update_check` was `off` before this, **tell the user you turned it back on**
and why: they had previously asked not to be reminded, and asking for automatic
updates supersedes that. Silently reversing an earlier decision is the kind of
thing that has to be said out loud, even when it is obviously what they meant.

**b. Verify BOTH halves, and say so out loud.** The flag and the reader are
different facts, and either one alone is a promise that will not be kept:

Assert each key **is on**, matching the exact set of values the hook accepts —
`on ON On true TRUE True yes YES 1`. Do not test for the literal string `off`:
the hook treats anything outside that on-list as off, so `update_check=OFF`,
`disabled` or `0` would sail past an off-grep while the hook vetoes on them, and
the skill would report all-clear on a clone that will never update. Check for
the value that permits, not for one spelling of the value that forbids.

```bash
ON='(on|ON|On|true|TRUE|True|yes|YES|1)'
grep -q 'auto-update' .claude/settings.json && echo "reader: registered"
grep -qE "^[[:space:]]*auto_apply[[:space:]]*=[[:space:]]*$ON([[:space:]#].*)?\$"   .update-state/config && echo "flag: auto_apply is on"
grep -qE "^[[:space:]]*update_check[[:space:]]*=[[:space:]]*$ON([[:space:]#].*)?\$" .update-state/config && echo "kill switch: on, updates permitted"
```

All three lines must print. A missing line is a reason to stop and say what is
wrong, not to round up to "should be fine".

Report the result in plain words: the flag is on, the kill switch is not
standing in its way, **and** the SessionStart hook that reads it is registered
in `.claude/settings.json` — so it takes effect at the next session start. Only
claim that when all three checks agree.

**c. Check for the machine-wide veto.**

Mirror the hook's pass-through set here too, in the other direction: it ignores
`0 false FALSE no NO off OFF` and an empty value, and vetoes on anything else.
Warning on any non-empty value would tell someone with
`NOVOADS_PACK_NO_UPDATE_CHECK=0` that their updates are blocked when they are
not — under-promising is friendlier than the reverse, but it is still wrong.

```bash
case "${NOVOADS_PACK_NO_UPDATE_CHECK:-}" in
  ''|0|false|FALSE|no|NO|off|OFF) echo "env veto: not active" ;;
  *) echo "env veto ACTIVE: NOVOADS_PACK_NO_UPDATE_CHECK=$NOVOADS_PACK_NO_UPDATE_CHECK" ;;
esac
```

`NOVOADS_PACK_NO_UPDATE_CHECK=1` in the environment overrides the config file
and silences the hook no matter what was just written. If it is set, say so:
the setting is recorded and will take effect once that variable is unset, and
until then nothing will apply. **Name it; do not fight it.** Never unset it from
here — it lives in the user's shell profile or their environment for a reason
this repo cannot see, and a skill that quietly clears a machine-wide switch is
worse than one that reports it.

This verification is not ceremony. The design it learned from shipped this exact
dialog option, wrote this exact flag, and installed its reader only under a
separate setup mode nobody ran — so a real install sat with consent switched on
and nothing reading it for four months, reporting itself up to date while
falling behind. In this pack the reader ships registered for every install and
the flag only enables it, which makes that failure structurally impossible. The
grep proves the property rather than assuming it.

If the grep finds nothing, say so plainly and stop short of promising anything:
the flag is set but this clone's `.claude/settings.json` predates the hook. One
manual update (option 1) brings the file in, and unattended updates begin after
that. A promise the machine cannot keep is worse than no promise.

Then tell them what they just agreed to, in one sentence: at session start, at
most once an hour, the pack will apply updates older than 24 hours by itself,
and any session where it does will say so. And name the way out — this skill
again, or `auto_apply=off` in the same file.

## Option 3 — "Not now"

Snooze the banner nag on an escalating ladder. Write `.update-state/update-snoozed`:

```
level=<1|2|3>
until=<epoch seconds>
version=<sha of origin/main right now>
```

| Existing level | New level | Quiet for |
|---|---|---|
| none | 1 | 24 hours |
| 1 | 2 | 48 hours |
| 2 or more | 3 | 7 days |

Read the current level from the file if it exists; treat an unreadable or
unparsable file as no snooze at all and start again at level 1. Get the version
with `git rev-parse origin/main`.

Three rules govern it, and all three resolve toward speaking up rather than
staying quiet:

- **A new upstream commit resets the snooze.** The answer was about the version
  in hand, not about updates in general.
- **A file that does not parse is not a snooze.** Fail toward notifying: a
  corrupt byte must never buy silence nobody asked for.
- **It suppresses the nag, and nothing else.** `./scripts/update.sh` and this
  skill both keep working while a snooze is live. A switch that strands the
  manual path is not a switch.

Confirm in one line: quiet until when, and that they can update any time by
asking.

## Option 4 — "Never ask again"

Set `update_check=off` in `.update-state/config`, using the same preserve-other-
keys approach as option 2:

```bash
cd "$(git rev-parse --show-toplevel)"   # a config written elsewhere has no reader
mkdir -p .update-state
touch .update-state/config
grep -v '^[[:space:]]*update_check[[:space:]]*=' .update-state/config > .update-state/config.tmp 2>/dev/null || true
printf 'update_check=off\n' >> .update-state/config.tmp
mv .update-state/config.tmp .update-state/config
```

Say precisely what went quiet and what did not. Off silences the session-start
check, the banner, and the auto-apply hook — no fetch, no network call from any
hook. It does **not** disable `./scripts/update.sh`, and it does not disable
this skill. Updating stays available on request, forever; only the asking stops.

Name the way back in the same breath: `update_check=on` in that file, or
invoking this skill.

If `auto_apply=on` was already set, say that too. This option does not erase it
— the kill switch simply wins over it, which is why everything goes quiet — but
it stays recorded, so turning the check back on later resumes unattended
updates. A user who wants both off should be told to set `auto_apply=off` as
well. Better to say it now than to have automatic updates reappear later as a
surprise.

`NOVOADS_PACK_NO_UPDATE_CHECK=1` in the environment does the same thing without
editing a file, and it wins over whatever the config says. Mention it when
someone wants the switch for one session, or for a whole machine, rather than
for this clone.

## What survives an update

Worth stating when the user hesitates, because the hesitation is usually about
this:

- **`.env` is protected explicitly.** It is copied aside before any merge and
  restored after, including on interrupt. This is deliberate and measured: a
  plain `git pull` silently destroys a gitignored `.env` when the upstream
  starts tracking that path.
- **Local edits to tracked files are stashed, never steamrolled.** If the stash
  cannot be replayed cleanly, the work stays in the stash and the STATUS line
  names it. Conflict markers are never left in the working tree.
- **Untracked files are left alone** unless an incoming file collides with one,
  in which case it goes into the same stash.
- **Customizations belong in `local-skills/`**, which is untracked on purpose.
  Anything in `skills/` is upstream's to overwrite.

## Notes

- This skill never runs `git pull`, `git reset --hard`, or `git checkout` on the
  user's tree. `./scripts/update.sh` is the one writer, it is the only thing
  that has the `.env` protection and the stash policy, and going around it means
  going around both.
- Do not batch the four options into a summary and pick for the user. The
  question is the product.
- If the user asked to update and the answer is obviously option 1 from their
  own words ("update the pack"), still confirm the count and what is coming
  before applying — but do not re-ask the four-way question they already
  answered.

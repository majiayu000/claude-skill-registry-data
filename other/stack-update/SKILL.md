---
name: stack-update
description: Apply a pending claude-code-setup update — fetches upstream, shows what changed, three-way-diffs CLAUDE.md against your local edits, and re-runs install.sh. Invoke on "update the stack", "upgrade the kit", "update claude-code-setup", "is there an update", or the SessionStart hook's update notice.
---

# Stack update

This kit installs by **copying** files into `~/.claude` — once copied, an installed file has
no link back to the repo. This skill is the manual apply step for the update the SessionStart
hook noticed: fetch upstream, show what changed, gate on approval, and (critically) reconcile
`CLAUDE.md`, which `install.sh`'s default ("auto") mode never overwrites once it exists — a
`--claude-md=replace` run (not used by this skill's step 6) does.

State dir: `${CLAUDE_HOME:-$HOME/.claude}/.claude-code-setup/` — `installed` (SHA that
skills, agents, and settings are at), `claude-md-installed` (SHA whose `global/CLAUDE.md` the
user actually accepted — written only when they applied the upstream hunks or confirmed a
completed hand-merge, never on a plain skip; if absent, there is no known base — `install.sh`
only writes it when it copied `CLAUDE.md` for a user who had none, so anyone with a pre-existing
personal `CLAUDE.md` has no stamp at all; never fall back to `installed`, see step 5),
`claude-md-skipped` (SHA of upstream's `global/CLAUDE.md` at the point the user last declined to
reconcile it — suppresses re-showing an identical comparison in step 5; never used as a diff
base and never implies acceptance), `last-check` (epoch of last poll), `remote` (`<installed> <remote> <count>` from the last
successful poll — replayed at each session start while `installed` still matches), `notice` (the
session-start notice in the user's language, see step 7), `disabled` (presence
silences the SessionStart check entirely; `touch` it to opt out).

Repo: `https://github.com/TurboKach/claude-code-setup.git`, default branch **`master`** (not
`main`).

## Procedure

Steps 1–3 are read-only reconnaissance — nothing outside the scratchpad clone is touched, and
no state-dir file is written, until the approval gate in step 4 passes.

1. **Read state.** Read `installed` from the state dir — this is the SHA to diff against. Do
   not modify any state file yet.

2. **Clone.** Full `git clone` (not `--depth`) of the repo into the session scratchpad. Full
   history, because step 3 needs `<installed>` reachable to diff against; the repo is small,
   so a shallow clone buys nothing here. The clone is read-only reconnaissance — nothing
   is copied out of it until approval.

3. **Summarize what's new, grouped by surface.** First check history shape with
   `git merge-base --is-ancestor <installed> HEAD`:
   - **Ancestor (normal case)** — derive the summary from `git log --oneline <installed>..HEAD`
     and `git diff --stat <installed>..HEAD`; raw commit subjects are not the deliverable, a
     "what changes for me" bullet list is.
   - **Reachable but not an ancestor** — upstream rewrote history (force-push). Label the
     summary as **divergent history**, not "what changed since you installed": `<installed>..HEAD`
     is a set difference, not a lineage, and would misrepresent it. Base the bullets on
     `git diff <installed>..HEAD` instead (endpoint comparison — stays correct regardless of
     rewritten history).
   - **`<installed>` empty, unknown, or unreachable at all** — say plainly that a change summary
     is unavailable because there's no base to diff against. Show only the current HEAD SHA and
     short subject, and the last ~10 commit subjects (`git log --oneline -10`) as context — and
     label that list explicitly as *not* a diff against what the user has installed.

   Write the summary in the language you answer the user in — Claude Code's `language` setting
   when set, else the conversation's — not the commit subjects' language. Group bullets by the
   surfaces the user actually has installed, each stated in user-facing terms (not a hash dump):
   - `global/CLAUDE.md` → their always-on rules — what changed, in a sentence.
   - `skills/*` → which skills are new or changed.
   - `agents/*` → which role agents changed.
   - `global/rules/*` → which path-scoped user rules are new or changed.
   - `hooks/*` → what now happens differently at session start or on tool calls.
   - `install.sh` / `settings.example.json` → what the installer will now do differently,
     including a changed recommended master (`model` / `modelSettings`) — step 6 may ask about it.
   Omit a group with no changes.

4. **Approval gate #1 — apply the update at all?** `AskUserQuestion` whose question text opens
   with step 3's summary — `What's new since <installed short SHA> (<N> commits):` and the
   bullets, or step 3's divergent-history / no-base label in their place — and ends "Apply this
   update?", with options *Apply* / *Show the full diff first* / *Cancel*. The summary goes in
   the question even when the user wrote the commits.
   - *Show the full diff first* → show it, then re-ask this same question; it is not itself an
     answer.
   - *Cancel* → stop here. **Nothing is written and the state dir is left exactly as it was** —
     do not touch `installed` or `last-check`, so the update notice correctly reappears next
     session.
   - Silence, or the question going unanswered, is not approval — never infer Apply from a
     default or from the user being away.
   - Only *Apply* proceeds past this point.

5. **The `CLAUDE.md` three-way diff and approval gate #2 — this is the step that justifies the
   skill.** Step 6 below runs `install.sh` with no `--claude-md` flag, so its default (`--claude-md` unset,
   i.e. "auto") mode applies: it deliberately never overwrites an existing `~/.claude/CLAUDE.md`
   (see the `CLAUDE.md` block in `install.sh`) — it just prints a reminder to merge by hand. So step 6's install
   refreshes skills and agents but silently skips the single most important file, and a
   two-way diff can't tell an upstream improvement apart from the user's own customization. Do
   it properly. Use `claude-md-installed` as the base for this diff, not `installed` — it's the
   SHA the user actually accepted `CLAUDE.md` at, which may lag `installed` if a prior run was
   skipped or handed off for manual merge.
   - **`claude-md-installed` exists (normal case)** — three-way diff:
     - `git show <claude-md-installed>:global/CLAUDE.md` — what the user last accepted.
     - the clone's `global/CLAUDE.md` — what upstream has now.
     - the live `~/.claude/CLAUDE.md` — the user's file, possibly hand-edited.
     Diff the first two to isolate what actually changed upstream, then show that upstream
     change against the live file.
   - **`claude-md-installed` is absent — unknown base, do not fall back to `installed`.** This
     is the common case: `install.sh` only writes `claude-md-installed` when it copies
     `CLAUDE.md` for a user who had none, so anyone who already had a personal `CLAUDE.md`
     (i.e. every existing user) ends up with an `installed` SHA but no `claude-md-installed`.
     Falling back to `installed` would silently claim they accepted that revision's
     `global/CLAUDE.md`, which they never did, and would permanently hide every upstream change
     made before it. Check `claude-md-skipped` first:
     - **Absent, or upstream's `global/CLAUDE.md` has changed since the SHA it records** — say
       plainly there's no record of which `global/CLAUDE.md` revision they've accepted (either
       their `CLAUDE.md` predates the marker, or they've always kept their own), and show a
       **two-way** diff instead — the clone's current `global/CLAUDE.md` against the live
       `~/.claude/CLAUDE.md` — labeled explicitly as "upstream's current version vs yours", not
       as "what changed upstream since you installed". This diff will be noisy if they carry
       heavy local edits — expected and honest. Proceed to the gate #2 question below.
     - **Present, and upstream's `global/CLAUDE.md` is unchanged since that SHA** — nothing new
       to show. Note in one line that the `CLAUDE.md` reconciliation the user previously declined
       is still outstanding, skip re-rendering the diff, and skip gate #2 for this run.
   Then a **separate** `AskUserQuestion` — approving the bundle
   in gate #1 is not approval to rewrite `CLAUDE.md`, it's a distinct decision because the
   live file may carry local edits — with three choices: apply the upstream hunks (back up the
   live file first, preserve any local edits that don't conflict) / show the full diff and let
   the user decide by hand / skip `CLAUDE.md` entirely. **Never** rewrite
   `~/.claude/CLAUDE.md` without an explicit answer to this question — silence is not approval.

6. **Install.** First, the master-model question — asked on every update unless the user
   already has it or said not to. Ask only when both hold:
   - the live `~/.claude/settings.json` doesn't match the clone's `settings.example.json`
     recommendation: `model` differs ignoring a trailing `[1m]` in any casing — it selects the
     same model's 1M window — or any master `modelSettings.<id>.effortLevel` there differs (every entry except
     `claude-sonnet-5-5`, the executors' level, which `install.sh` fills in only where none is saved);
   - `~/.claude/.claude-code-setup/master-dont-ask` is absent, or its content differs from
     `python3 -c 'import json,sys; e=json.load(open(sys.argv[1])); print(json.dumps({"model": e["model"], "modelSettings": {k: v for k, v in e["modelSettings"].items() if k != "claude-sonnet-5-5"}}, separators=(",", ":"), sort_keys=True))' settings.example.json`
     run in the clone (a changed recommendation asks again).

   Then `AskUserQuestion`, showing their current `model` and effort, with options *the recommended
   model and effort, named from the clone's `settings.example.json` (recommended)* →
   `--master=recommended` / *keep current, ask next time* →
   `--master=keep` / *don't ask again* → `--master=dont-ask` / other, the user types
   `MODEL_ID` or `MODEL_ID:EFFORT` → `--master=<typed>`. Not asked → no `--master` flag.

   Run `./install.sh` from the clone, with that `--master` flag if one was chosen. It already backs up skills and agents to
   `~/.claude/.backup-<stamp>` and merges settings.json keys — reuse it, don't reimplement its
   logic here.
   - **If it exits non-zero:** stop — do not write `installed` or `claude-md-installed`, the run
     is not complete. Report exactly what was and wasn't applied (skills/agents may be partially
     updated; `CLAUDE.md` may already have been changed by gate #2 above, before this step ran).
     Point the user at the restore path: `~/.claude/.backup-<stamp>` (skills/agents backup
     `install.sh` already took) and, if gate #2 applied hunks, the `CLAUDE.md` backup it took.
     Don't invent a rollback — just leave the state files untouched and tell the user where the
     backups are.

7. **Update state.** Only now write to the state dir, and only on a zero-exit install:
   - `installed` — the clone's new HEAD SHA. After `install.sh` succeeds, skills, agents, and
     settings genuinely are at this revision.
   - `claude-md-installed` and `claude-md-skipped` — one rule, unconditional, no per-path
     exception, applies whether this was the three-way or unknown-base case in step 5:
     - Gate #2 answered *apply the upstream hunks* — write `claude-md-installed` at the clone's
       new HEAD SHA, and delete `claude-md-skipped` if present. This is the only answer that
       stamps acceptance, because it's the only one where `CLAUDE.md` was actually rewritten.
     - Gate #2 answered *skip* or *show the full diff and decide by hand*, or gate #2 wasn't
       asked this run (step 5's suppressed case) — leave `claude-md-installed` untouched (do not
       write it, even if absent), and write `claude-md-skipped` at the clone's new HEAD SHA. The
       declined or unconfirmed `CLAUDE.md` change stays pending and resurfaces in the next run's
       step 5 instead of being silently dropped or falsely marked accepted.
   - Delete `last-check` so the next session re-polls fresh instead of trusting the 24h cache.
   - `notice` — the hook shows this line at session start, before the user has typed anything,
     so it can't take the language from the conversation. Write one line in the language you
     answer in, with the placeholders `{n}` (commit count, or `?`), `{from}` and `{to}` (short
     SHAs), phrased so any count reads correctly — e.g. `New changes: {n} ({from} → {to}) — run
     /stack-update`, translated. When that language is English, delete `notice` instead; the
     hook's built-in English wording is used.

8. **Tell the user to restart Claude Code.** Skills, agents, hooks, and settings `env` are all
   read at session start — nothing applied by this run is live in the current session until
   it's restarted.

## Opt-out

`touch ~/.claude/.claude-code-setup/disabled` silences the SessionStart update check
permanently (delete the file to re-enable).

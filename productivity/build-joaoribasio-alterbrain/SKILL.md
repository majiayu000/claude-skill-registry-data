---
name: build
description: Build an approved self-build proposal (a my-* skill, a my-* helper agent, a catalogue tool, an automation, or a ready-made blueprint), test that it triggers correctly, validate it and record it; use after the user says yes to a proposal card, or for "build it", "/build <proposal or blueprint>".
model: sonnet
effort: high
argument-hint: "<proposal card path | blueprint slug | my-name>"
---

# Build

Turn an approved proposal into a working skill, helper, tool or automation, safely.

## When to use

- The user approved a proposal card ("yes, build it").
- The user picks a blueprint ("build Zotero", "build the morning brief").
- A blueprint's own steps say "follow the `/build` flow".

## Before you start

1. **Find the card.** From the argument, or the newest card in `vault/00_inbox/proposals/` that matches. No card yet: run `/propose` first (it writes one), then continue.
2. **Approval.** The card must have `status: "approved"`, or the user must say yes in chat now. If it is `open`, show the 3-line summary and ask. Never build on an `open`, `rejected` or `removed` card.
3. **Clarify.** Run `/clarify` with the card's `kind` (`skill`, `agent`, `mcp`, `automation`, `blueprint`). Don't continue until it returns READY and the card has an `## Agreed brief`.
4. **Read the rules for what you will write:**
   - skills: SPEC §7 and `references/skill-template.md`;
   - agents: SPEC §8 and `references/agent-template.md`;
   - the record: `references/built-json.md`;
   - a blueprint: the whole blueprint file, especially **Build steps**, **How to test**, **How to undo**.
5. **The never-edit list.** Self-build may never create or change: anything under `system/`, `.claude/settings.json`, `system/core.md`, `system/catalogue/*`, `system/hooks/*`, any skill or agent without the `my-` prefix, or `vault/40_sources/raw/`. If a step needs one of these, **stop**, explain in plain words, add a `#ab/build` task, and suggest `/update-alterbrain` or a different design.

## Steps

1. **Plan in one message.** List the files you will create and the settings you will change, with one line each. Ask "Go ahead?" (Yes (recommended) / Change something).
2. **Scaffold by kind:**
   - **skill** → `.claude/skills/my-<slug>/SKILL.md` from `references/skill-template.md`. Frontmatter keys exactly `name`, `description`, `model`, `effort` (and optional `argument-hint`); `name` equals the folder name. Body sections in SPEC §7 order. Extra detail goes in `references/` or `workflows/` inside the same folder. Keep SKILL.md ≤ 250 lines.
   - **agent** → `.claude/agents/my-<slug>.md` from `references/agent-template.md`. Least-privilege `tools`. Body: role, inputs, exact output format, a "Never" list.
   - **mcp** → add the catalogue `id` to `config/mcp.selected.json` `enabled` (no duplicates; never edit the catalogue). Run `node system/scripts/mcp-gen.mjs`. Any key: the user types it into `.env.local` (never in chat). Explain the restart: "Close this session and open the project again; when Claude asks whether to trust the new tool, choose allow."
   - **automation** → a `my-<slug>` skill (as above) for the job itself, plus **one routine note per scheduled job** (next block), plus the schedule on the chosen host exactly as its blueprint describes (desktop scheduled tasks are set by the user in the app: give them the prompt to paste and the clicks). Always include the off switch from the brief.

   **Routine notes (every scheduled job).** Alterbrain runs no scheduler of its own; the host does (a Claude desktop scheduled task on a laptop, a Claude cloud routine, or a server's own scheduler). The routine note makes the job visible, portable and fail-visible.
   1. Copy `system/templates/notes/routine.md` to `vault/90_routines/<Name>.md` (Title Case name; create the folder if it is missing). Fill the frontmatter: `status` `"active"` only once the user has set the schedule on the host (until then `"paused"`); `schedule` in plain words; `cadence` in machine form (`daily@HH:MM`, `weekly:<mon..sun>@HH:MM` or `monthly:<1-28>@HH:MM`); `host` (`laptop`, `cloud` or `server`); `runs` (a skill such as `/people due`, or `"prompt"`); `may: "draft only"` (fixed: nothing else is valid); `data` (only the vault paths the job may read); `model` and `effort` from the routing table; `created` from the system date. Leave `last_run` and `last_result` empty.
   2. Write the **body** as the exact instruction the host runs, so the user can paste it into any host to recreate the job. It ends with the step "record the run: `node system/scripts/routines.mjs record "<Name>" --result "<one line>"`". No secrets in it.
   3. Check the note: `node system/scripts/routines.mjs show "<Name>"`. Exit 1 means it reports something to fix (a wrong value, or a note it cannot read), not a crash: fix what it says before scheduling.
   4. Schedule the host with the note body as the instruction. For `host: "cloud"` or `"server"` the run works on its own copy of the vault, so the `record` step only reaches your vault if the body ends by committing and pushing that note change to `main`. Add that step only after the user confirms the host can push, and keep the note `"paused"` until they do; otherwise say plainly that the Routines page, not the note, shows when it last ran. `record` stamps the host's own clock, so the stamp is host-local time.
   5. Tell the user in one line: "This job is on your routine list; say 'check my routines' any time."
   6. Activate it. A paused note is never monitored. Once the schedule exists on the host (or the scheduled-tasks tool just created it), change the note's `status` line to `"active"` and run `node system/scripts/routines.mjs show "<Name>"` to confirm. If the user has not scheduled it yet, add a task: `node system/scripts/tasks.mjs add "Schedule <Name>, then set its routine note to active" --tag build --link "vault/90_routines/<Name>.md"`.
   7. If the job is one of the framework's suggested routines (`node system/scripts/routines.mjs suggest` lists them), create the note with `node system/scripts/routines.mjs enable "<suggested-name>" --user-asked` instead of copying the template, and only when the user said yes in chat (that is what `--user-asked` means). Without the flag the note is saved as `suggested`, which is inert: never monitored and never overdue. With it the note is `active` at once, so if the schedule does not exist yet, set it to `"paused"` until it does (step 6).
   - **blueprint** → follow its **Build steps** in order. Each part that creates a skill, agent or tool uses the matching recipe above. Ask before any step that changes `config/autonomy.json`, and never set `auto` before the blueprint is recorded as built.
3. **Quick trigger check** (skills and agents). Write down:
   - 3 prompts that **should** use it (in the user's own words, from the brief and `state/proposals.json` examples);
   - 3 prompts that **should not** (near misses that belong to other skills, for example `/study`, `/ask`, `/assignment`).
   Compare against every other skill's `description`. If any "should not" prompt would match the new description better than its real owner, or a "should" prompt is ambiguous, rewrite the description and check again. Show the six prompts to the user in a short table.
4. **Safety review.** Hand the new files to a read-only reviewer by naming a helper agent:
   - risk `low`: the `helper-review` agent (sonnet / high, read-only); risk `medium` or `high`: the `helper-judgement` agent (opus / high). If `helper-judgement` cannot run (plan limits), do the review yourself and say so in one line.
   - Read the reviewer's answer yourself; its word alone is not the result.
   - It checks: only allowed paths are written; tools are least-privilege; nothing sends, posts or submits beyond the channel's autonomy level; no secrets; facts about the user only from `fact-sheet.md`; model and effort fit the routing table; the description discriminates.
   - It returns PASS or a numbered fix list. Fix and re-review once. Two failed reviews: stop, tell the user, add a task.
5. **Validate.** Run `node system/scripts/validate.mjs`. Fix any problem in the new `my-*` files only. Do not continue until it passes.
6. **Test once for real.** Run the success test from the agreed brief with the user's real example (for an MCP after restart: add a task `Test <tool> after restarting` with `--tag build` instead). Show the result.
7. **Record it.**
   ```
   node system/scripts/built.mjs add --name <name> --kind <kind> [--blueprint <slug>] --path "<each created path>" [--mcp <id>] [--channel <channel>] --proposal "<card path>" --model <m> --effort <e>
   ```
   For an automation, list the routine note (`vault/90_routines/<Name>.md`) among the `--path` values and name the host in `--note`. The routine note is the record of the schedule; `built.json` stays the record of what was built.
   Then set the card `status: "built"`, tick its task (`node system/scripts/tasks.mjs done "<card title>"`), and run `node system/scripts/proposals.mjs mark <key> built`.
8. **Save.** Run `node system/scripts/git-auto.mjs commit` (it skips itself when auto-commit is off; otherwise the session end does it anyway).
9. **Tell the user** in 4 lines: what was built, how to use it (two example phrases), what it will never do, and "To undo: `/remove-skill <name>`."

## Outputs

- New files: `.claude/skills/my-<slug>/**` or `.claude/agents/my-<slug>.md`, `vault/90_routines/<Name>.md` for each scheduled job, and anything a blueprint's steps create (only in allowed places).
- Possibly `config/mcp.selected.json` + regenerated `.mcp.json`; `config/autonomy.json` only when a blueprint says so and the user agreed.
- `state/built.json` entry; proposal card `status: "built"`; ticked `#ab/propose` task; `#ab/build` tasks for anything left to do.

## Safety

- No approval, no build. No READY from `/clarify`, no build.
- Only `my-*` names, only allowed paths (see the never-edit list). Hooks will block protected paths anyway; never try to work around a block.
- A routine note always says `may: "draft only"`, and its body tells the host to draft only. That is an instruction, not a lock: what a run can actually send is decided by `config/autonomy.json`. Keep the channels a scheduled job touches on `draft` and say so to the user.
- New skills draft; they never send, post, submit, pay or delete on their own. Outbound actions obey `config/autonomy.json`.
- Never ask for or write secrets. Keys live only in `.env.local`, typed by the user.
- High-risk tools and blueprints need the user's yes in their own words, recorded in the agreed brief.
- If validation or review keeps failing, stop and say so. A half-built skill is removed with `/remove-skill`.

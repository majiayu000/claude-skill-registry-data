---
name: project-onboarding
description: "Use when an owner wants to set up Thrum for a repository from scratch, resume an interrupted setup, or re-run the parts that went stale - the security model, engineering rules, coupling rules, merge gates, periodic checks and the coordinator, all in one guided run. Offers each part in order, lets the owner skip any part and come back to it, and undoes what it installed on request."
---
<!-- markdownlint-disable MD013 MD028 -->

# project-onboarding

Runs the whole setup in order: the security model, the engineering rules, the coupling rules, the merge gates, the
periodic checks and the coordinator. Each part is its own skill and can run alone. This skill adds the order, the
progress record, the dependency check, skip and resume, the preface, the inventory of what the owner already has, and
Undo. It writes `.thrum/policy/onboarding.json`, `.thrum/policy/README.md`, and its local notes file
`.thrum/results/history-analysis.md`, and nothing else on its own: each part writes its own files.

## Rule 1: Order

The parts run in this order. Each one is a skill, and the progress record keys it as shown.

| Key | Skill | Part |
|---|---|---|
| `S1` | `onboarding-security` | the security model |
| `S2` | `project-philosophy` | the engineering rules |
| `S3` | `onboarding-coupling` | the coupling rules |
| `S4` | `onboarding-gates` | the merge gates |
| `S5` | `onboarding-checks` | the periodic checks |
| `S6` | `onboarding-coordinator` | the coordinator |

Each part can also run alone. `onboarding-security` is the recommended first step, and the rest can follow later.
Before the first part runs, this skill runs Rule 6, Rule 6a, Rule 6b, Rule 7 and Rule 7a, in that order.
Rule 4's offer comes before every part's own questions.

## Rule 2: Progress record

`.thrum/policy/onboarding.json` is the progress record. `resources/onboarding-schema.md` is its contract: read it before
the first write. When the file is absent, create `.thrum/policy/` and the file, and write `profile` after Rule 7. Each
part writes its own `sections.<S>` entry (`status`, `reason`, `date`, `sha`) and its own answers, and this skill never
writes another part's entry. This skill reads the record at the start of every run to decide what to offer (Rule 4). It
writes only `licence` (Rule 6), `profile` (Rule 7), the `pending` inventory records (Rule 6a), `reported` notices and
`answers.interview_channel`. Outside that record it writes only `.thrum/results/history-analysis.md` (Rule 7a).

## Rule 3: Dependencies

Check a part's dependencies at the start of that part, after the owner says "do it now" to the part's offer (Rule 4).
A part needs these from the parts before it:

| Part | Needs | Written by |
|---|---|---|
| `project-philosophy` | `.thrum/policy/security-model.md`, `answers.deployment_shape`, `answers.external_calls` | `onboarding-security` |
| `onboarding-gates` | `.thrum/policy/security-model.md`, `answers.burn_down`, `coupling.changed_scope_viable` | `onboarding-security`, `project-philosophy`, `onboarding-coupling` |
| `onboarding-checks` | `.thrum/policy/security-model.md` | `onboarding-security` |
| `onboarding-coordinator` | `answers.cadence`, `answers.topology`, `answers.lane_scope`, `.thrum/policy/checks.json` | `onboarding-checks`, `onboarding-gates` |

A file that exists but lacks the key is a miss, and so is a missing file. A miss is never treated as empty. When
something is missing, offer the prerequisite part now, or proceed with the gap recorded. `<part>` is the part that
writes the missing file, and `<step>` names the one step of this part that needs it, both in plain words. This line is
said by this skill only; a part skill never carries it, so that the part's offer stays its first `> Ask:`.

> Ask: <part> has not run yet, and this part needs it. Run it first (recommended), or carry on and skip <step>?

After the owner chose to carry on and skip a step, the part leaves that step out without saying the line again.

- **Offer the prerequisite.** Run that part first, then come back to the one that was waiting.
- **Proceed with the gap recorded.** Skip the step that needs the missing file or key, and add the gap as an owner
  question:
  a dashboard pick when the dashboard is installed (`answers.dashboard: true`), and otherwise an item under
  `## Owner questions` in `.thrum/policy/worklist.md`, on either variant. The step that needs the missing file or key
  follows the missing-policy block of its own skill: it prints the `ONBOARDING MISSING` line, messages the
  coordinator, stops that step and never continues with a default.

The item line is `- [ ] [w-<n>] <what> — from project-onboarding — added <YYYY-MM-DD>`, with `w-<n>` the next number not
yet used in the file. When `worklist.md` is absent, create it with the headings `## Work` and `## Owner questions`, after
showing the committed-files notice for the variant. Show the notice once: check `reported` for the signature
`committed-files:<variant>`, show it only when it is absent, and then add the signature. The variant is the one Rule 6
derived.

- Free:

  > Say: Your work list and the decisions you make here go in .thrum/policy/worklist.md and .thrum/policy/rulings.md, which are committed with your code.

- Pro (only `worklist.md` is written, for owner questions without a dashboard):

  > Say: Open questions for you go in .thrum/policy/worklist.md, which is committed with your code.

In stealth mode, leave out the words about being committed with your code from every notice.

## Rule 4: Skip and resume

This is prompting only: it adds no code and no `onboarding.json` key.

Before each part's offer, say this, with `<n>` the part's place in Rule 1 and `<part name>` its name from the Part
column:

> Say: Part <n> of 6: <part name>.

In this skill's lines, `<part name>` and `<part>` are the part's name from the Part column of Rule 1 without its leading
"the" (for example "Security model"), with a capital letter at the start of a line.

- **The offer.** Every part starts with its offer, before any of its own questions and before Rule 3's check. The
  licence read (Rule 6) asks nothing, so it may run first, and
  Rules 6a, 6b, 7 and 7a run before the first part. The part's skill shows its block from `resources/section-offers.md`:
  two plain sentences on what the part sets up and what it asks of the owner, then the ask line.
  Only on "do it now" does the part go on.
- **Skip.** "Skip it for now" records `sections.<S>.status: skipped` with reason `owner`, and moves to the next part. For
  the coupling part it also writes `coupling.changed_scope_viable: false` with `coupling.source: "owner-skip"` and
  `answers.ratchet_candidates: []`, so the gates part never meets a missing key; the reason stays `owner`. It writes
  nothing else. A Solo owner who says "skip it for now" to any part gets the same record, reason `owner`.
- **Resume.** A re-run picks up where the last one left off. A `done` part is not offered again, unless its `sha` is
  stale: `git rev-list --count <sha>..HEAD` is 100 or more, or `<sha>` is not an ancestor of `HEAD`. Offer a re-run,
  naming the count, and never force it. Every part recorded `skipped` (whatever its reason), `partial` or `undone` is
  offered again with the same question.
- **Solo.** The offer still comes first. On "do it now", the Solo pre-answers apply (`resources/profiles.md`). The
  coupling part's Solo answer is "skip it for now", recorded with reason `profile`; the owner may still say "do it now".

## Rule 4a: Question blocks

Every part asks its questions as blocks, following resources/question-blocks.md. The six part offers are not block
questions.

Run each shell command on its own: no ;, &&, loop, heredoc, xargs or $( ). Run git without -C, from the repository
folder. Read and write files with your file tools, not with shell commands.

Ask every question as plain text in your reply and wait for the answer. Never use a question tool.

Never name a rule or step number from these skills to the owner (such as "Rule 6"): say what you are doing instead.

Say every line marked > Say: or > Ask: to the owner word for word,
filling in only its <placeholders>. Never paraphrase one or leave one out.

## Rule 5: Owned blocks

Where a skill shares a file with another skill or with the owner, it owns only a block between
`<!-- onboarding:<owner> -->` and `<!-- /onboarding:<owner> -->`. Every part follows the same pass: read the file,
replace only its own block (or append it when absent), and write the file back. For a role file, read with
`thrum roles rules show <role>`, write with `thrum roles rules set <role>` with the whole content on stdin, then run
`thrum roles deploy`. Parts run one after another, never at the same time, so a whole-file write never clobbers another
part or the owner's own text.

## Rule 6: Free and Pro

Before the first question, run the licence-read block below. It rewrites `licence` in `.thrum/policy/onboarding.json`
and derives the variant. Parts that write a tracking output follow the derived variant. There is no licence stop-gate:
a Free owner is never stopped. A Pro write is never attempted under the Free variant, and a refused one stops with the
block's notice.

<!-- onboarding:licence -->
**Licence read.** Do this before the first question, every time this block runs.

1. Run `thrum license status --json` and rewrite the `licence` record in `.thrum/policy/onboarding.json` from it. Copy
   only `status`, `tier`, `capabilities`, `repo_capabilities` and `oss_grants`, and set `checked` to the current time.
   Never copy `registration_record`, `machine_id`, `repo_origin` or `repo_id`: the file is committed with the code. If
   the command fails, replace the whole record with `{checked, status: "unknown", capabilities: []}`, with no `tier`
   and no `oss_grants`.
2. Derive the variant. It is `pro` when `repo_capabilities` contains all three of `queue.write`, `state.write` and
   `memory.substrate`. Otherwise it is `free`. The skill never matches `oss_grants.repos[]` itself
   and never derives a repository id. Follow only that variant's instructions. Offer the dashboard only when the
   variant is `pro` and `repo_capabilities` also contains `dashboard.write`.
3. Never read a `licence` record left by an earlier run without refreshing it first.
4. If a Pro write is refused anyway, stop that step and print:

   > Say: Your licence no longer covers this step. Run onboarding-coordinator to switch to the matching setup.

   Inside `onboarding-coordinator` itself, do not print that line. Run step 1 again and continue with the variant it
   derives.
<!-- /onboarding:licence -->

## Rule 6a: Inventory

After Rule 6 and before Rule 7, show the reading line from `resources/inventory.md`, then run `resources/inventory.md`.
It reads the files in this repository that look like rules, notes, ratchets, gates, hooks, custom skills and security
notes, and it only reads. Write a `pending` record in `answers.inventory` for each item found that has no record yet,
and a `skipped-credential` record in place of `pending` for an item the credential patterns match. Never change an
existing record. A part run alone reads `answers.inventory` if it is present, and otherwise offers nothing.

## Rule 6b: Dashboard channel

After Rule 6a and before Rule 7, follow `resources/dashboard-channel.md`: when it allows the offer, make it once and
write the owner's choice to `answers.interview_channel`. When it does not, say nothing about the dashboard and the
interview runs in the terminal. A part run alone reads `answers.interview_channel` and reads an absent key as `terminal`.

## Rule 7: Preface and profile

Show the full form of `resources/preface.md` as written, and ask Solo or Team with its ask line. Write the answer to
`profile` in `.thrum/policy/onboarding.json` as `solo` or `team`, then apply `resources/profiles.md` for the rest of the
run. Then say exactly one of the two lines under "After the answer" in that file, chosen by the stealth test. Run
`git rev-parse --git-path info/exclude`, then `grep -qx '.thrum/' <the path it printed>`: exit 0 means stealth mode. The
exclude file holds a bare `.thrum/` line. A part run alone leaves `profile` unset and treats it as `team`.

When `onboarding.json` already records `profile`, this is a re-run: do not show the full form. Say these two lines
instead. `<date>` is the latest `sections.<S>.date`, the parts are named by their part names, `<n> commits` is Rule 4's
`git rev-list --count <sha>..HEAD` for each part that is out of date, and the last count is the answers marked
`unsure` in `answers_source`:

> Say: Last run <date>. Done: <parts>. Skipped: <parts>. Out of date: <parts> (<n> commits since). Answers marked not sure: <n>.

> Ask: Settle the not-sure answers, add a skipped part, change one part, or go through everything again? You are set up as <profile>; say "switch" to change that.

Leave out a clause that has nothing in it, and the choice that goes with it. With no skipped part there is no
"Skipped:" clause and no "add a skipped part"; "change one part" and "go through everything again" are always offered.
On "switch", say the Solo and Team line of the preface and then ask Solo or Team with its ask line, because a re-run is
how Solo becomes Team. The other choices work like this. "Settle the not-sure answers" goes through each part's answers
marked `unsure`, and the part re-run then does not list them again. "Add a skipped part" and "change one part" run that
part from its offer on (Rule 4). "Go through everything again" runs every part from its offer on.

## Rule 7a: History analysis

After Rule 7 and before the first part's offer, run `resources/history-analysis.md` once. It reads this repository's git
history and nothing else, and it writes only `.thrum/results/history-analysis.md`, which is kept on this machine and is
not committed and never staged. A part run alone runs it when that file is absent or stale, as that resource says. The
parts use what it finds as recommendations.

## Rule 8: Finish

Write `.thrum/policy/README.md` from `resources/policy-README.md`, including its `## Skills` section.

If git ignores .thrum/policy/ and this is not stealth mode, fix .gitignore before the closing summary.
Stealth mode is Rule 7's test. When this is not stealth mode and `git check-ignore -q .thrum/policy/onboarding.json`
exits 0, git is ignoring the setup files, so "commit it" would do nothing. Say this first:

> Say: I am adding lines to .gitignore so that git tracks .thrum/policy/. The rest of .thrum/ stays out of git.

Then edit `.gitignore` to hold the lines `!/.thrum/`, `/.thrum/*` and `!/.thrum/policy/`. When `.gitignore` has a bare
`.thrum/` line, replace that line with these three lines: git cannot re-include a file under an ignored parent
directory, so a bare `.thrum/` line must go. Afterwards `git check-ignore -q .thrum/policy/onboarding.json` must exit 1.
In stealth mode make no edit and say nothing about it.

Then say the closing summary. It opens with this line:

> Say: Setup is finished. Here is what I set up.

Then these lines, built from `onboarding.json` and `.thrum/policy/installed.md`:

- one line per part: `<part name>: done`, or `<part name>: skipped`;
- one line per monitor: `Now running: <what it checks>, every <cadence>; its warnings go to <recipient>`, where `<recipient>` is the
  monitor's `deliver_to`, said as "this agent" when it is this agent;
- one line per command in `answers.unvalidated_commands`: `Not validated: <command>`;
- one line naming `.thrum/policy/` and the files written there this run.

Then, when the coordinator part is done, this line:

> Say: Your agents now work to these rules, and this agent, your coordinator, checks their work and warns you when that work stalls or breaks the rules.

When the coordinator part was skipped, say this line in its place:

> Say: Your agents now work to these rules.

Then exactly one of these two; the second in stealth mode, where nothing is committed:

> Say: Next: 1. Review .thrum/policy/ and commit it. 2. Give your coordinator its first task: tell this agent what you want done.

> Say: Next: 1. Review .thrum/policy/. 2. Give your coordinator its first task: tell this agent what you want done.

When the coordinator part was skipped, replace everything from `2.` on in the line with
`2. Set up your coordinator: ask this agent to run project-onboarding again.` Then close with this line:

> Say: If you need it later: to add a part you skipped, ask this agent to run project-onboarding again. To remove what onboarding installed, ask it to run project-onboarding undo.

Leave out the sentence about adding a skipped part when no part was skipped.

## Rule 9: Undo

`project-onboarding undo` follows `resources/undo.md`. It reverses what onboarding installed outside
`.thrum/policy/`, reads `.thrum/policy/installed.md`, and leaves `.thrum/policy/` in place.

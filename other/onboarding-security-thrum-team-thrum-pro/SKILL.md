---
name: onboarding-security
description: "Use when a repository needs a written security model that tells Thrum's agents what to protect and what to ignore - first-time setup, a security scan that reports findings the owner already ruled out, or a role that designs a guard, cap or authorization without a stated boundary. Writes .thrum/policy/security-model.md and the role pointers. Recommended first step of project onboarding, and it runs on its own."
---
<!-- markdownlint-disable MD013 -->

# onboarding-security

Writes `.thrum/policy/security-model.md` and a pointer block in each role file. It scans the repository, asks where the
owner draws the line, and records what agents must protect and what they must not build or flag.

## Opening offer

Show this offer before any other question.

<!-- onboarding:offer -->
> Say: This part writes your security model: what Thrum's agents must protect in this repository, and what they can ignore. It reads the files in this repository and asks a few questions about what matters to you.
> Ask: Do this part now, or skip it for now? If you skip it, running project-onboarding again offers it again.
<!-- /onboarding:offer -->

"Skip it for now" records `sections.S1.status: skipped` with `reason: owner` in `.thrum/policy/onboarding.json` and ends
the section. "Do it now" goes on. When this skill runs alone the same offer is shown, and a skip never changes a record
that is already `done`.

## History analysis

When .thrum/results/history-analysis.md is absent or stale, follow
history-analysis.md in the project-onboarding resources before the first block.

## Running alone

This section is the recommended first step and works without the umbrella skill. When `.thrum/policy/onboarding.json`
is absent, it:

- creates `.thrum/policy/` and `onboarding.json`;
- records `licence` through the block below;
- leaves `profile` unset, so it reads as `team`; a run alone never applies the Solo defaults;
- shows the short preface:

> Say: This section writes .thrum/policy/security-model.md, a block in each role file under .thrum/policy/roles/, and its progress in .thrum/policy/onboarding.json.
>
> Say: The other sections can follow later: run project-onboarding to be offered each one, or run a section's skill on its own.

When it finishes, it offers the remaining sections by skill name and says what each one adds: project-philosophy (your
engineering rules), onboarding-coupling (rules that keep changes small), onboarding-gates (how changes are checked
before they land), onboarding-checks (small drift checks) and onboarding-coordinator (the coordinator that runs the
rest).

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

Both variants get the same security model. The licence only decides what the later coordinator section installs.

## Step 1: Scan and report

> Say: This scan reads the files in this repository only. It does not run your code. What it finds is written to .thrum/policy/security-model.md, which is committed with your code.

Scan the repository for six categories and report what you found, with `file:line`, and the mitigations already in
place:

1. listeners (sockets, ports, bind addresses);
2. routes and handlers;
3. auth (how a caller is identified or checked);
4. secrets (where credentials are read from and where they could be written);
5. external calls (outbound network, third-party services);
6. deploy files (containers, service units, CI and release configuration).

Read only. Never run the code, never call the network. If the inventory found security notes (`SECURITY.md`, threat-model
documents), use them to prefill this report and set each such `answers.inventory` record to `prefilled`. Nothing is
copied. Leave .thrum/ out of every scan and every Why: line: it is Thrum's own state, not this project's.

<!-- onboarding:inventory -->
**Bring in what you already have.** Offer the items the inventory found for this section, never an item it skipped.

1. Offer each `answers.inventory` record whose `offered_in` is this section and whose `decision` is `pending`. With no
   `answers.inventory`, offer nothing. A `security-note` record is not offered: the security section reads it into the
   scan report and sets it `prefilled`.
2. Before the first copy is written, show the committed-copies line, unless `reported` already holds the signature
   `imported-copies`. After showing it, add that signature to `reported`.

   > Say: What you bring in is copied into .thrum/policy/imported/, which is committed with your code.

   In stealth mode, leave out the words about being committed with your code from every notice.

3. Team offers the part's found items as blocks in the form of `resources/question-blocks.md`, one row per item, or one
   row per file when the file has more than seven found items. A file with more than seven found items is one row. On
   that row, "choose one by one" opens its own blocks. Each row has the choices bring in / leave, `Recommended:` is
   `bring in`, and `Why:` says in one line what the item is.
   When you cannot say what an item is, recommend "leave" and use the fallback line.
   `<n>` on a file row never counts an item skipped as a credential.

   Solo asks one table question per section that has found items, covering all of them, and asks nothing when nothing
   was found. On that question, "choose one by one" opens blocks:

   > Ask: I found <n> things you already have that fit this part of the setup. Bring them all in, choose one by one, or leave them all?

4. When a ratchet script has only a guessed ceiling file, Team makes the ceiling a row of the block, in the same row
   form: the question is whether `<file>` is the ceiling that `<script>` checks against, the choices are yes / no,
   `Recommended:` is `yes`, and `Why:` names the file as the nearest checked-in data file to the script.

5. A ruling made from a brought-in item has these fields:
   - `trigger` is "working in this repository".
   - `rule` is the item's first line, without its list marker. For a whole-file note, it is the file's first heading,
     or failing that its first line.
   - `applies_to` is `all`.
   - `from` is `<section title>, imported/rules.md#i-<n>`, and the `rulings.md` line renders it as written. The full
     text stays in the copy.
6. After the copies are written, a section that wrote at least one copy shows this line once, as the last action of the
   copy step: the copy step is not finished until the line below is shown. A section that copied nothing does not show
   it, and a ratchet brought in is not a copy, so it does not count.

   > Say: Thrum's copy in .thrum/policy/imported/ is now the one to edit. Your original is untouched and is still read by any tool that reads it today, so a rule you change in one place should be changed in the other. A full re-run notices a changed original and offers to refresh the copy.
<!-- /onboarding:inventory -->

## Step 2: Deployment shape

State the deployment shape positively, in the owner's words: where the code runs, who can reach it, and which parties it
talks to. Write `answers.deployment_shape` and `answers.external_calls` in `onboarding.json`. Never describe the shape
by what it is not.

## Step 3: Depth

After the scan report, ask the depth as the first of two blocks, following `resources/question-blocks.md` of
project-onboarding. The `Why:` line says what each depth writes, and the recommended depth is Standard.

```text
Block 1 of 2: Security depth

1. How much should the security model write down?
   Choices: Light / Standard / Deep (pick one)
   Recommended: Standard
   Why: Light writes the governing sentence and the non-goals only. Standard adds the trust boundary paragraph and the in-scope table. Deep adds a table of boundaries and the known gaps, each linked to an issue.

Reply "yes to all", tell me what to change (for example "1: Deep"), say "not sure about 1", or ask "explain 1".
```

Write `answers.security_depth`. Write the file from `resources/security-model-template.md`, in the template's heading
order: `## Governing sentence`, `## Trust boundary`, `## In scope`, `## Non-goals`, `## Known gaps`, then the footer
that holds the `onboarding-watch-list` block. Keep only the headings the chosen tier includes, and delete the tier
notes. The template starts `Written by onboarding-security on <YYYY-MM-DD>.`; this step
fills `<YYYY-MM-DD>` with the run date, the same date it records in `onboarding.json` as `sections.S1.date`. The written
file has no placeholders left.

## Step 4: Defend or not

Ask the actors as the second block, in the same form: one pick-one row for each actor the scan found. A row recommends
`defend`, unless a found security note names that non-goal. Then the row recommends `do not defend`, and its `Why:` names
that note. A row with no evidence takes the fallback line from `resources/question-blocks.md`. A block where a
protection was turned off shows the read-back line from `resources/question-blocks.md` before anything is written.

When the history read was skipped or found nothing,
put the History: line under every fallback line, as question-blocks.md says.

```text
Block 2 of 2: Actors

1. Do you want agents to defend against <actor>?
   Choices: defend / do not defend (pick one)
   Recommended: <defend, or do not defend when a found security note names that non-goal>
   Why: <one line naming that evidence, or the fallback line>

Reply "yes to all", tell me what to change (for example "1: do not defend"), say "not sure about 1", or ask "explain 1".
```

> Say: Defend means agents must protect against it. Do not defend means agents are told not to build or flag protections against it (for example, other users, when the tool only ever runs on your own machine), and that is written down as your decision.

Record how each answer was given in answers_source: security_depth, and security_actor_<slug> for each actor, where <slug> is the actor in lowercase words joined by hyphens.

If a found security note names a non-goal, offer it here as the answer to be confirmed. Each "not" becomes a dated owner
ruling, written as a prose prohibition that tells a reader what not to build or flag. The non-goals end with a
paragraph that begins "where these stop". Append each non-goal to `answers.rulings` in `onboarding.json` as
`{id, date, trigger, rule, applies_to: all, from}`, with `from` exactly
`Security model, security-model.md#non-goals` (keep the `#non-goals` anchor), so the coordinator section writes it out
in the variant's form.

## Step 5: Watch list

Propose each pattern to watch for in merges in plain words, from the scan and from the security findings the owner
accepted in `.thrum/results/history-analysis.md` (never its Dropped list). Ask them as one pick-several row in the
`resources/question-blocks.md` form. When the scan and the accepted findings propose no pattern, skip the block.

```text
Block 1 of 1: Watch list

1. Which of these should be flagged when they appear in a merge?
   Choices: <pattern 1, in plain words> / <pattern 2, in plain words> (pick several)
   Recommended: <the proposed set>
   Why: <one line naming the scan result or accepted finding>

Reply "yes to all", tell me what to change (for example "1: drop the second"), say "not sure about 1", or ask "explain 1".
```

The owner accepts, drops or adds in words. Never ask the owner for a regular expression. The agent writes the regex into
the `onboarding-watch-list` block in the footer of `.thrum/policy/security-model.md`, with one `pattern` (an extended
regex matched against added lines) and a `why` per item. Set `non_goals_confirmed: true` only after the owner confirms at least one non-goal.

With no owner-confirmed non-goal, record that the security check in onboarding-checks is not scheduled.

## Role pointer

Write this block in `.thrum/policy/roles/<role>.md` for implementer, reviewer, planner, brainstormer and coordinator,
between `<!-- onboarding:S1 -->` and `<!-- /onboarding:S1 -->` (read the file, replace only that block or append it,
write it back with `thrum roles rules set <role>`, then `thrum roles deploy`):

<!-- onboarding:S1 -->
Read the non-goals in .thrum/policy/security-model.md before designing any guard, cap or authorization.
If .thrum/policy/rulings.md exists, read the owner rulings in it at session start.
<!-- /onboarding:S1 -->

The second sentence is how rulings reach every role on the Free variant. On the Pro variant the coordinator section does
not create the file, so the sentence has no effect. Append an `installed.md` row for each role block.

## AGENTS.md or CLAUDE.md line

> Ask: Add the same two sentences to your AGENTS.md so every agent that opens this repository reads them?

Ask this in every run, before Finish. "Only on the owner's explicit yes" decides whether to write the line, never whether to ask.

Write it only on the owner's explicit yes, between `<!-- onboarding:S1 -->` markers so Undo can find it. Write it once:
into `AGENTS.md` when `CLAUDE.md` imports it (an `@AGENTS.md` line), otherwise into the file the owner picks.
Append it at the end of the file: one blank line, then the block. Undo removes the block and that one blank line.
Append an `installed.md` row for it.

## Finish

- Write `sections.S1` (`status`, `date`, `sha`) in `onboarding.json`.
- In stealth mode, say that `.thrum/policy/` stays on this machine only.
- Write nothing outside `.thrum/policy/` apart from the optional AGENTS.md line.

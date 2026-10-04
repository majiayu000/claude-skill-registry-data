---
name: skill-customize
description: Record a customisation for one of this plugin's own skills, or show the customisations already recorded for it. Use when the user wants to change how a dev-skills skill behaves for good rather than for one run — "make /feature-mockup always draw three alternatives", "customise /feature-design", "stop /feature-mockup publishing artifacts", "show me my customisations for X", "what have I customised". Takes the skill's slug as its argument, and the only legal values are the directory names under the plugin's own skills/ folder — anything else stops the skill with the list of what is accepted. Offers concrete candidate customisations derived from the target skill's own decision points, takes the user's own instruction where they already gave one, folds it into ${CLAUDE_PLUGIN_DATA}/<skill_name>.extras as a plain markdown instruction list the target skill reads at the start of its run, and prints that file verbatim whenever the user asks to see it. Customisations refine a skill's behaviour and can never override a rule the skill marks non-negotiable. Writes exactly one file, outside the project, and nothing else — no project files, no commits, no pushes, and it invokes no other skill.
user-invocable: true
disable-model-invocation: false
argument-hint: <skill-name> [show | the customisation in your own words]
allowed-tools: Read, Write, Edit, AskUserQuestion, Bash(ls *), Bash(cat *), Bash(test *), Bash(mkdir -p *), Bash(find *), Bash(pwd), Bash(date *), Bash(printf *)
---

# skill-customize — teach one of this plugin's skills a house rule

You are running the `skill-customize` skill. Your job is to turn something the user wants a *specific* skill of this plugin to do differently into a durable instruction that skill reads on every future run — or, when that is what they asked for, to show them exactly what is recorded today.

The point of externalising this is that a preference stated mid-run dies with the run. `/feature-mockup` being told "three alternatives, always" in one design session teaches it nothing about the next one. A customisation file is where that instruction survives, per skill, per machine, without anybody forking a `SKILL.md`.

**A customisation refines a skill; it never overrides one.** Every skill in this plugin ends in a *Constraints (non-negotiable)* section, and those bullets exist because breaking them loses work, leaks data, or produces a plausible wrong answer. A customisation that collides with one is refused here, at write time, with the collision named — not quietly written down for the target skill to discover and disobey.

This skill is **not part of the feature chain**. It never calls `feature-resolve` (which allocates feature folders and seeds trackers), never calls `lessons-capture` (there is no run to reflect on — and `lessons-learn` remains the way skill *text* gets edited), and never calls `usage-report`. It holds no `Skill` tool at all, so all three are structurally impossible. It touches nothing in the project: the single file it writes lives in the plugin's own data directory.

This skill has eight steps (Steps 0–7). Execute them in order.

## Step 0 — Confirm before doing anything (proactive invocation only)

If this skill was invoked because the model judged it relevant — rather than the user explicitly typing `/skill-customize` (look for the literal `<command-name>/skill-customize</command-name>` tag on the invocation) — call `AskUserQuestion` once before anything else:

- question: `"Record this as a lasting customisation for /<slug>?"`, header: `"Customise"`
- options: `{"label": "Yes — record it", "description": "Writes it to <slug>.extras; every future run of /<slug> reads it."}` (Recommended), `{"label": "Just this once", "description": "Apply it to the run in flight and record nothing."}`, `{"label": "No", "description": "Leave /<slug> as it is."}`

Anything but the first answer ends the skill without writing. When the user typed the command themselves, skip this step entirely — they already asked.

## Step 1 — Resolve the skill name

The first whitespace-separated token of `$ARGUMENTS` is the target skill's slug.

**The legal values are whatever is on disk.** This skill's own base directory was announced when it was invoked (`…/dev-skills/<version>/skills/skill-customize`), so the plugin's skills folder is its parent:

```bash
ls "<this skill's base directory>/.."
```

If that path is not available, fall back to `find ~ -path "*dev-skills*/skills" -maxdepth 8 -type d 2>/dev/null` and take the match under the highest installed version, or the `skills/` folder of the working clone you are standing in. **Never hardcode the roster of skills** — a hardcoded list goes stale the first time a skill is added, and its failure mode is rejecting a name that is perfectly valid.

Then:

- **Exact match** → that is the target. Carry on.
- **No slug given.** If exactly one legal slug appears in the user's own most recent message, take it and say so in one line — that is reading what they wrote, not guessing. Otherwise stop with one line and the list:

  ```
  skill-customize: name the skill to customise. Accepted: <slugs, comma-separated>.
  ```

- **Unknown slug, but one to three legal slugs are close to it** (a prefix, a suffix, or a one-or-two-character difference) → ask once via `AskUserQuestion` which they meant, with a "None of these" option. Never silently correct a name: writing the customisation to the wrong skill's file is invisible until the wrong skill starts behaving oddly.
- **Unknown slug with no near match** → stop with the same one-line error and list.

Take the rest of `$ARGUMENTS` as either the word `show` (`show`, `view`, `list`, `cat` all count — case-insensitive) or, if it is anything longer, the customisation stated in the user's own words. Hold on to it; Steps 3 and 4 use it.

## Step 2 — Locate the customisation file

**Resolving `${CLAUDE_PLUGIN_DATA}`.**

```text
${CLAUDE_PLUGIN_DATA} is a plugin-config substitution token: Claude Code expands
it inside plugin hook, MCP and LSP command strings, and it is not an exported
environment variable, so a shell that simply reads it almost always gets nothing
back. Resolve the directory yourself, taking the first rule that yields a path:

1. `$CLAUDE_PLUGIN_DATA`, on the chance the environment really does set it.
2. `<config-dir>/plugins/data/<plugin>-<marketplace>`, derived from the running
   skill's own base directory: an installed plugin runs from
   `<config-dir>/plugins/cache/<marketplace>/<plugin>/<version>/skills/<slug>`,
   so `<plugin>` and `<marketplace>` are the two path segments above the version,
   and Claude Code keys the data directory on exactly that pair.
3. The single `<config-dir>/plugins/data/dev-skills*` directory, when `ls` shows
   exactly one. Two of them means a stale second install is present and the rule
   is ambiguous, so it is skipped rather than guessed at.
4. `<config-dir>/plugins/data/dev-skills` — reached only when the plugin is
   running from a working clone rather than an installed copy.

`<config-dir>` is `$CLAUDE_CONFIG_DIR` when that is set, and `~/.claude` when it
is not. A skill's customisation file is then `<extras-dir>/<slug>.extras`.
```

So the file you are about to read or write is `${CLAUDE_PLUGIN_DATA}/<skill_name>.extras` — one file per skill, named for the slug resolved in Step 1. Run `mkdir -p "<extras-dir>"` before the first write; never create anything else in that directory.

## Step 3 — Read what is already recorded

```bash
cat "<extras-dir>/<slug>.extras" 2>/dev/null
```

A missing file is the normal starting state, not an error.

**If the user asked to see the file** — the `show` keyword from Step 1, or they said so in words — this is where the skill ends. Print the file's contents **verbatim**, inside a fenced block, exactly as they are on disk:

- Do not summarise, do not paraphrase, do not re-order the bullets, do not "tidy" the wording, and do not annotate individual lines. Never summarise the file in place of showing it. The user asked what is recorded; anything but the bytes answers a different question.
- Name the absolute path on the line above the block.
- When the file does not exist, say so in one line — `No customisations recorded for /<slug>.` — and offer, in the same line, to add one.

Otherwise carry the existing instructions forward: Step 4 needs them to spot a duplicate or a contradiction, and Step 6 rewrites the file around them.

## Step 4 — Capture the customisation

**If the user already stated it** — in `$ARGUMENTS`, or in the message that triggered a proactive invocation — that is the customisation. Use their words as the source and do not ask again; asking someone to repeat what they just said is friction, not care.

Otherwise, read the target skill's `SKILL.md` and ask once via `AskUserQuestion`:

- question: `"What should /<slug> do differently?"`, header: `"Customisation"`
- Offer three concrete candidates **derived from that skill's own decision points** — the places it currently chooses for the user, the defaults it applies, the things it asks about every run, the thresholds and counts it names. For `feature-mockup` those look like *"Always draw three alternatives, even for a brand-new surface"*, *"Never publish artifacts — present local files only"*, *"Default to compact density in every mockup"*. Generic filler (*"be more thorough"*) is worse than no option at all: it produces an instruction the target skill cannot act on.
- The user's own free-text answer arrives through the built-in "Other" option, which is the expected path. The candidates exist to show what a usable instruction looks like, not to constrain the answer.

**This step needs a user.** If there is genuinely no user channel — a headless or fully autonomous run with nothing already stated — stop without writing. A customisation nobody asked for is a behaviour change nobody consented to.

Then normalise what you have into **one imperative sentence per instruction**, naming what changes and when it applies. `"Always offer three alternatives, even for a brand-new surface"` is an instruction; `"more options please"` is not. Keep the user's own terms wherever they are already specific. Split a request that carries two independent rules into two bullets; never merge two into one.

Finally, compare each new instruction against what Step 3 found:

- **Duplicate** of an existing bullet → say so in one line and change nothing.
- **Refinement** of an existing bullet → replace that bullet in place, keeping its original added-date and appending the revision date.
- **Contradiction** of an existing bullet → ask once via `AskUserQuestion` whether the new instruction supersedes the old one (Recommended), whether both should stand because they apply in different situations, or whether to cancel. Never leave two bullets that tell the skill opposite things: the target skill has no way to break the tie and will pick one at random.

## Step 5 — Check it against the target skill's non-negotiables

Read the target skill's `## Constraints (non-negotiable)` section. Refuse any instruction that would:

- contradict one of those bullets;
- relax a safety rule — writing outside the skill's documented output scope, putting real user data, customer records or secrets into an artefact, committing or pushing where the skill says it never does, skipping a gate that protects against destructive or irreversible work;
- disable a step the skill marks load-bearing or mandatory, including the clarification loops that run even under autonomous instructions.

A refused instruction is refused **in one sentence naming the constraint it collides with**, together with the closest thing that *is* allowed — and it is never written to the file. Refusing one instruction does not abandon the rest: write the ones that passed and report the refusal alongside them.

Everything else is fair game. A customisation is allowed to change defaults, counts, thresholds, tone, formats, which optional steps fire, and what the skill decides for itself instead of asking — that is the entire point of the file.

## Step 6 — Write the file

Write the whole file with `Write` (new file) or `Edit` (existing one). The format is plain markdown so the target skill can read it straight into context and the user can read it in a terminal:

```markdown
# <slug> — customisations

User customisations for the `<slug>` skill of the dev plugin, managed by
`/skill-customize`. Each bullet below is an instruction `<slug>` applies to its
own run, on top of its SKILL.md. They refine that skill's behaviour and never
override a rule it marks non-negotiable.

## Instructions

- Always offer three alternatives, even for a brand-new surface. _(added 2026-08-26)_
- Never publish artifacts — present the local files instead. _(added 2026-08-26, revised 2026-09-02)_
```

Rules for the write:

- **Preserve every instruction you did not change.** Read-modify-write the whole file rather than blind-appending, so a supersede in Step 4 actually removes the bullet it replaced — but never drop a bullet the user did not ask you to touch.
- **One instruction per bullet**, in the order they were added, oldest first. Dates come from `date -u +%Y-%m-%d`.
- **The header block is fixed.** Regenerate it verbatim as above, substituting the slug. It is what tells a reader (and the target skill) what the file is.
- **Removing the last instruction leaves the file with an empty `## Instructions` section**, not a deleted file. The empty file is the record that customisations were considered and cleared; a missing file reads as never-customised.
- Write nothing else, anywhere. No project files, no other skill's `.extras`, nothing under `features/` or `bugs/`, no commit, no push.

## Step 7 — Confirm in one line

One line, no ceremony:

```
Recorded for /<slug> — <n> instruction(s) active in <absolute path>. /<slug> reads them at the start of its next run.
```

Add a second line only when Step 5 refused something, or when Step 4 superseded an existing bullet. Do not print the whole file back — the user just told you what is in it. When they want to see it, they will ask, and Step 3 will show it verbatim.

Then say whether the target skill actually loads its customisations yet. Not every skill in this plugin reads its `.extras` file: the ones that do carry a *Resolving `${CLAUDE_PLUGIN_DATA}`* block of their own before their first step. Check the target skill's `SKILL.md` for it, and when it is absent say so in one line — the instruction is recorded and will apply as soon as that skill is wired, but it changes nothing today. Never imply an unwired skill is about to behave differently.

## Constraints (non-negotiable)

- **One file, outside the project.** The only thing this skill ever writes is `<extras-dir>/<slug>.extras`. Never a project file, never a `SKILL.md`, never anything under `features/` or `bugs/`, never a commit, never a push. Editing skill text is `lessons-learn`'s job, and it is a deliberately separate, user-only path.
- **The slug must be a real skill of this plugin**, resolved from the `skills/` directory on disk. Never hardcode the roster, never accept a name that is not there, and never silently correct a near-miss — ask.
- **Customisations refine, never override.** An instruction that collides with the target skill's non-negotiable constraints, relaxes a safety rule, or disables a load-bearing step is refused at write time with the collision named. Do not write it down "for the skill to decide later"; the skill has no way to know it was contentious.
- **Verbatim means verbatim.** When the user asks to see the file, print exactly what is on disk in a fenced block. Never summarise it, never paraphrase it, never reorder or reword the bullets, and never show a tidied version of what you think it says.
- **Never invent a customisation.** Every bullet traces to something the user actually asked for. Candidate options exist to be chosen or ignored, never to be adopted on the user's behalf, and a headless run with nothing stated writes nothing at all.
- **Never calls `feature-resolve`, `lessons-capture` or `usage-report`.** This is not a chain skill: there is no feature to path, no run to reflect on and no usage window to close. Structurally enforced — it holds no `Skill` tool.
- **Never read the file for any purpose but this skill's own job.** It holds the user's working preferences; it is not context to mine, quote in other conversations, or carry into unrelated work.

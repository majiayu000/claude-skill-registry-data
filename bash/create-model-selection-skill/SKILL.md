---
name: create-model-selection-skill
description: "Generate this user's `select-model` skill: survey the agent products and models on this computer, ask for the user's preferences, and write a skill that the model running a task reads to decide which model to use and how. Use for /create-model-selection-skill, or when /setup-pstack finds no `select-model`."
disable-model-invocation: true
---

# Create a model selection skill

Every task that spawns a subagent or worker has to answer two questions: which model, and how (stay in this session, a subagent, a worker on another agent, several models at once). The answer depends on the user, the computer, and the moment, so pstack does not ship a table. This skill writes a skill, `select-model`, that holds the user's preferences and this computer's facts. The model running a task reads it before it spawns anything and decides. You write it for that reader: an agent that sees it cold, mid-task, on a computer it has never inspected.

What pstack knows about each product is in its adapter, next to this skill in `../resolve-capability/adapters/<id>/adapter.md`. Each adapter's `## Survey` section says what to read for that product, and an environment adapter's Survey adds the questions to ask when it is installed. This skill holds the steps and names no product.

`select-model` describes this computer, not the session that generates it. A task may later run inside an environment this session is not in, or outside one this session is in. So survey every environment that is installed, and record separately which one this session ran in.

## 1. Find the state

- **Target.** `~/.agents/skills/select-model/`. If the user names another directory, use that one and say so in the final reply.
- **`select-model` exists.** Read its `SKILL.md`, `inventory.md`, and `log.md`. This is an update: survey again, show what changed since `inventory.md`, and ask only about what changed. A re-run rewrites every section of `SKILL.md` except `## Preferences`, which it shows and keeps unless the user changes it. `## Quirks seen here` in `inventory.md` stays as it is unless the user agrees to drop a line. `log.md` is only appended to.
- **Preferences hold preferences only.** On an update, show each start command, flag, or path you find under `## Preferences`, propose moving it to `## Quirks seen here` or dropping it, and change nothing without the user's yes.
- **It does not exist.** A new setup.

## 2. Survey this computer

Observe, do not assume. Everything below is a command or a file you can read here.

1. **Which environments are installed, and which is this session in?** For each environment adapter in `../resolve-capability/adapters/` (its header says `kind: environment`), check the Installed line of its Survey. Read the whole Survey of each one that is installed and survey it from here, even when this session runs outside it, as its Survey says. Then run `sh ../resolve-capability/scripts/detect.sh`, which prints the ones this session runs in. When it prints nothing, also read `../resolve-capability/references/plain.md`.
2. **Which harness are you in?** Your own tool list tells you. Read the harness adapter whose Detect section matches you. When none matches, survey your own harness through `references/unknown-product.md`.
3. **Which agent products are installed?** For each harness adapter in `../resolve-capability/adapters/` (its header says `kind: harness`), check the Installed line of its Survey. Add each agent that an installed environment's Survey lists. A product found here with no adapter goes through `references/unknown-product.md`.
4. **Which models and efforts does each one offer?** Read them from the sources its Survey names. Record each model with its effort values. A model with no effort list has none.
5. **How can each one be started from here, and what does it refuse?** Your own harness starts its own models with `spawn-subagent`, as your harness adapter says. Another product starts through its own CLI run headless from the shell when it is installed and logged in, as its adapter's Start me from outside says, or through the Launching harnesses section of an installed environment, in a session that runs inside it. Record each way, the adapter section that holds its command, and for an environment's way that it works only in a session inside that environment. Record, per product, whether a model can be chosen at start, whether it loads this user's MCP servers, and which subagent or worker types are read-only. Read subagent types and their tools from the schema of the harness you are in. Do not write from memory which types drop MCP tools.
6. **Which capabilities does this computer have?** Record each in `inventory.md` under Environment: whether `gh` is logged in (`gh auth status`), whether `bun` is installed (`bun --version`, which `poteto-mode`'s bundled tools need), what each installed environment's Survey says to record, and whether a headless CLI of each other product runs (installed and logged in, as its adapter says).
7. **Is a model already pinned somewhere?** Each harness adapter's Survey names the files where its product pins a model. Check them at the user level and in the project. Note any pin for the questions and for `inventory.md`.

If a source is missing (no catalog, no cache), say so in `inventory.md` and keep what you could read. Never write a model that no source listed or the user did not name. A Survey line that says a mechanism was not run becomes `not verified here` in `inventory.md`.

## 3. Ask for preferences

Ask these questions, each conditional one only when it applies. Use `ask-user` as your harness adapter says. Otherwise list numbered options in plain text. Put what the survey found, as a table of products and models, in the text of the first question itself and also print it as reply text. The user sees neither your reasoning nor tool-call narration, so a table that lives only there is a missing table.

1. **Budget.** Offer these four options with these exact labels. Name the current one on an update. Say that `large` matches the defaults.
   - `unlimited — max reasoning`
   - `large — xhigh reasoning`
   - `medium — high reasoning`
   - `small — medium reasoning`

   The budget is the starting effort for every model. If a model does not offer the target effort, use the highest it offers at or below it. The ladder is `max` > `xhigh` > `high` > `medium` > `low`.
2. **Preferred model per kind of work.** Kinds: code a delegate writes, the hardest changes, prose and judgment, reading and exploring, review. Offer the surveyed models, plus "no preference".
3. **What to avoid.** Agents or models not to use, and why.
4. **How readily to use several models at once.** Never unless asked, only for risky or contested work, or whenever it could help. This sets when the model reading the skill reaches for swarm, arena, interrogate, or reflect.
5. **Each environment's questions.** Ask each question in the Survey of each installed environment, with the options it gives, also when this session runs outside it. Skip this when none is installed.
6. **Links.** Ask last, after the user has seen the rest. `select-model` is read by its path, so a link is only for the products that list skills from their own folder. Each harness adapter's Survey has a Skill folder line. List the products the survey found that need a link, each with its folder, and ask which to link. Offer all of them, a choice, or none. Skip the question when no product found needs one, when the user named another target directory (the links are relative to `~/.agents/skills/`), or on an update where every link is already in place. On an update, offer only a link that is missing.

The defaults, when the user has no preference, come from the Suited to line in each harness adapter's Survey, which names a kind of work and the model to offer for it. Show the line of every product the survey found, side by side. Offer a default only when the survey found that model. When two adapters claim the same kind of work, offer no default for it and say why. If the user is on Auto, or says to follow whatever model the session runs, write that as the preference.

Do not ask the user to choose a replacement model for each entry the session cannot start. Ask once: keep them (another harness or an environment runs them), or fold them into the session's own model.

## 4. Write the skill

Fill in the template in [`references/select-model-template.md`](references/select-model-template.md). Create these files under the target:

- `SKILL.md`, from the template. `## Preferences` holds one sentence per answer, each with its reason, so the model reading it can extend the choice to a case the sentence does not name ("Hard design goes to the strongest judgment model at xhigh because you said judgment quality matters more than cost" rather than "design: strongest"). Do not write a table of roles. Write only what the user said. For a product they said nothing about, write that they stated no preference and add nothing, because the model that reads the skill will decide and a guess from you would read as the user's own choice. A start command, flag, or path is not a preference. It belongs in `inventory.md`.
- `inventory.md`, in the shape the template gives. On a new setup its `## Quirks seen here` says that none were seen yet.
- No `references/` folder. The mechanisms for each product and environment ship in the `resolve-capability` skill next to `poteto-mode`, so `SKILL.md` points at it as `../resolve-capability/SKILL.md` and nothing is copied. Also write the absolute path of the `resolve-capability` folder that sits next to this skill, as the second place to look, because an install of pstack that is not under `~/.agents/skills/` does not resolve the relative path. This skill's own `references/` hold the template and the steps for a product with no adapter.
- `log.md`, one line: the date, what was created, which links were made, and that the user approved.
- **Links, for each product the user chose.** Do what the `skills` CLI does: a relative symlink named `select-model` inside the product's skill folder, pointing at `../../.agents/skills/select-model`. Run `mkdir -p <folder>` first. If the name is already a link to that same target, leave it. If it is anything else (a real directory, a file, or a link to somewhere else), do not replace it, and tell the user what is there. A product's folder may itself be a link to another folder, such as an environment's profile that links to the product's own folder. Create the link in the folder the product's Survey names and nowhere else. Never copy the skill into a product folder.

The finished `SKILL.md` stays under about 90 lines. Link to `inventory.md` and the adapters instead of copying them in.

## 5. Prove it

Start one read-only job per agent product the survey found, the way `inventory.md` says to start it. Use a trivial brief ("Reply with the model you run on and your effort. Do not edit files."), the lowest effort the model offers, and no more than one job per product. The jobs cost usage, so run no more of them than that.

- A job that starts and answers: record the date and what it reported in `inventory.md`.
- A job that does not start: remove that model from `inventory.md`, note the exact error in `log.md`, and tell the user.
- A product this session cannot start (not installed, not logged in, or no way here): mark it `not verified here`. That is not a failure.
- A way that works only inside an environment this session is not in: mark that way `not verified here`, and prove the product through a way that works here.
- A way of starting that cannot choose the model: its adapter says where the model that ran is recorded. Read it there and write that model in `inventory.md` as the one this computer gets.

If you drop an entry, check that every preference sentence still names a model that exists.

## 6. Hand it over

Tell the user, in this order:

1. The path of the skill and what it found (products, models, which environments are installed and which one this session ran in), and the links it made or left.
2. Which entries were verified and which were not.
3. How to change it: edit a sentence in `## Preferences`, or run `/setup-pstack` again. The skill asks before it edits itself when a task does not match it.
4. For each product found, how this session can start it: with its own subagent tool, by running the product's CLI headless from the shell, or only through an environment. A product that this session cannot start itself is not one that cannot start anywhere.
5. When the user named another target directory, that tasks read `~/.agents/skills/select-model/SKILL.md` by default and that `poteto-mode` has to be told the other path.

Then stop. Do not start work on the project.

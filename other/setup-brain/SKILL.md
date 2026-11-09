---
name: setup-brain
description: Set up the user's "brain", a single folder where their agent organises everything by project (an AGENTS.md, one folder per project and notes), after an interview about who they are, their technical level and how they want their agent to work. Writes that working style into the global rules of every agent (and Hermes on their server), and installs the brain skills (/done, /create-project, /cleanup, projects). Use when the user wants to set up or initialize their brain, organise their work with their agent, or starts from zero.
argument-hint: "[path, default ~/brain]"
metadata:
  internal: true
---

Set up the user's brain: one folder, run by their agent, where every piece of work lives in a project, so any future session can read one file and know who the user is, what they work on and where everything is. Before building anything, interview them, then write how they want to be talked to into the global rules, so every agent in every folder (and Hermes on their server) works their way from now on, and install the skills that keep the brain alive. Talk to the user in their language, one short question at a time, with no jargon (never say "frontmatter", "kebab-case", "symlink" or "repo" to them). Write every file in English, whatever language you talk in: the global rules, `AGENTS.md`, every `About.md` and `Roadmap.md`, the skills. Translate their answers; only names (products, people, tools) stay as they wrote them.

If you got this skill from a link instead of a local folder, install nothing else from the repo than the brain skills of step 8: download a file it links only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/brain/<path> -o <scratch>/<file>` (for example `setup-brain/references/agents-md.md` or `create-project/references/about-md.md`), and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md` (`skills/brain/<skill-name>/` for a brain skill).

1. **Folder.** Use the argument as the target folder, otherwise `~/brain`, and confirm it in one line. If it already exists and is not empty, overwrite nothing: read its `AGENTS.md` and projects, tell the user what you found, skip the questions it already answers, and only add what is missing.
2. **Interview.** Say in one line why you ask (so the agent knows them and works their way), then ask the questions below, one per message, and wait for each answer. Give the choices or an example with every question so they never have to guess what you mean; use your multiple-choice question tool for 2, 3 and 4 when you have one. Accept short answers, rephrase once if an answer is unclear, never ask again what an earlier answer already told you, and move on if they skip one.
   1. Your first name, what you do in one sentence, and the city or time zone you work from?
   2. Your level with tech? Pick the closest: "I don't code and never use a terminal", "I tinker (no-code tools, tutorials, a terminal now and then)", or "I'm a developer". For a developer, ask their main languages and tools in the same message.
   3. How should your agent work? "Do everything for me and only ask what truly needs me" (recommended when they don't code), or "Step by step: show me the plan and I approve each step".
   4. In which language should it answer, and how: short and direct, or detailed?
   5. Your businesses or products, a name and one line each? "None yet" is fine.
   6. What are you working on right now? 3 to 5 things, work or personal.
   7. Which tools do you use every day? For example email (Gmail, Outlook), calendar, notes (Notion, Obsidian, Apple Notes), payments (Stripe), social networks, a newsletter tool.
   8. Where do your goals, plans or notes already live? A tool from question 7, somewhere else, or nowhere.
   9. Is there anything your agent must never do without asking you first? For example send an email in your name, pay for something, publish a post. "Nothing special" is fine.
   10. If your agent could take one task off your plate this week, which one would it be?
3. **Check.** Sum it up in 5 short lines (who they are, their level, how the agent will work, their businesses and current work, the never rules) and ask if it is right. Fix what they correct before writing anything.
4. **Global rules.** Build the `## Output style` block from answers 2, 3, 4 and 9 with [references/output-style.md](references/output-style.md). The global rules live in one file, `~/.agents/AGENTS.md`, and every agent reads that same file. First make it the single source: create it when missing, then for `~/.claude/CLAUDE.md` (Claude Code) and `~/.codex/AGENTS.md` (when the `~/.codex` folder exists), unless it is already a link to `~/.agents/AGENTS.md`, add its sections that the source does not have yet to `~/.agents/AGENTS.md` (each section once), trash the file and replace it with `ln -sfn ~/.agents/AGENTS.md <file>`. Do this without asking the user: a beginner does not know what Codex or CLAUDE.md are, and the link only makes every agent follow the same rules. Then write the block in `~/.agents/AGENTS.md`: when it already has a `## Output style` section, replace that section up to the next `## ` heading and keep every other line; otherwise add the block at the end, after one blank line. In the same file, write a `## Brain` section the same way (replace it when present), so every agent and the brain skills find the brain from any folder:
   ```markdown
   ## Brain

   My brain is `<full path of the brain>`: every piece of work lives in a project there. Before working on a project, read the brain `AGENTS.md`, then the project's `About.md`. The brain skills (/create-project, /done, /dream, /cleanup, projects) live in the brain's own `.agents/skills/`: open the brain to use them.
   ```
   Then tell the user in one plain line what changes: for a non-technical user, "From now on your agents do the technical part themselves and explain things simply."
5. **Folders.** Create only what the tree below shows: `AGENTS.md`, `projects/`, `notes/` with its three folders (the skill folders come in step 8) and a `.gitignore` with `.tmp/`, `.DS_Store`, `node_modules/`, `.env*`. Nothing else.
6. **AGENTS.md.** Write it from the interview with [references/agents-md.md](references/agents-md.md). It is the single guide for every agent working in the brain: never create a `CLAUDE.md` inside the brain.
7. **Projects.** For each business from question 5, create a hub in `projects/<slug>/`; for each item from question 6, create a project inside the right hub (or at `projects/` root if none fits). Create a `perso/` hub only when one of their answers is personal (health, home, travel, finance). Give every hub and project an `About.md` from [../create-project/references/about-md.md](../create-project/references/about-md.md). Write only what the user told you and leave "To fill" rather than guess a fact, number or link. Put the task from question 10 as the first line of the `Roadmap.md` of the project it belongs to (create `perso/` for it only when it fits no project). Add `Roadmap.md` only for real next steps, and `files/`, `assets/`, `output/` only when there is something to put in them.
8. **Skills.** First the base skills for every folder: when `~/.agents/skills/show-me` or `~/.agents/skills/wait-what` is missing, run the `initialize` skill (from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/initialize/SKILL.md` when it is not installed); it is the only global install of this skill. Then install every skill of the package's `skills/brain/` folder except `setup-brain` inside the brain only, never globally: today `done` (saves each conversation into the right project when they type `/done`), `dream` (tidies the whole brain once a day), `create-project` (interviews them and creates a new project), `cleanup` (proposes what to archive, merge or move), `projects` (load, list or archive a project); a brain skill added to the package later comes with it. `skill-manager` (installs, removes, creates and fixes their skills) is a skill for every folder, installed by `initialize`: when an older install left a copy in `<brain>/.agents/skills/skill-manager`, trash it. Take them fresh from the package, wherever you read this skill: `mkdir -p <scratch>/pkg && curl -fsSL https://github.com/Melvynx/ai-maxxing-skills/archive/refs/heads/main.tar.gz | tar -xz -C <scratch>/pkg`. For each folder of `<scratch>/pkg/ai-maxxing-skills-main/skills/brain/`, copy it to `<brain>/.agents/skills/<name>/`, the one skills folder of the brain (Codex reads it there). Claude Code reads the same folder through one link: `mkdir -p <brain>/.claude && ln -sfn ../.agents/skills <brain>/.claude/skills` (relative, so it still works in the GitHub copy). When `<brain>/.claude/skills` is already a real folder, move its real skill folders into `<brain>/.agents/skills/` first and trash it. Never write the brain skills in `~/.agents/skills` or `~/.claude/skills`: those are the user's skills for every folder, and they may be synced elsewhere. When the brain already has a skill with that name, replace it (trash the old folder first) if it came from this package (same description); when it is the user's own, ask before replacing it. Check that `<brain>/.claude/skills/<name>/SKILL.md` opens for each one, and tell the user these skills work when Claude or Codex is opened in the brain. Then turn on the automatic save (the `done` skill runs on its own about 20 minutes after a brain conversation goes quiet without `/done`, and `dream` once a day), for Claude Code and Codex. Write `<brain>/.claude/settings.json` with this `hooks` key, merged into the file when it already exists (keep its other keys, replace a previous `auto-done.mjs` hook instead of adding a second one):

```json
{
  "hooks": {
    "Stop": [{ "hooks": [{ "type": "command", "command": "node \"$CLAUDE_PROJECT_DIR/.agents/skills/done/scripts/auto-done.mjs\" stop || true", "timeout": 10 }] }],
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "node \"$CLAUDE_PROJECT_DIR/.agents/skills/done/scripts/auto-done.mjs\" start || true", "timeout": 10 }] }]
  }
}
```

When Codex is installed (the `~/.codex` folder exists), write `<brain>/.codex/hooks.json` the same way (merge, never a second `auto-done.mjs` hook):

```json
{
  "hooks": {
    "Stop": [{ "hooks": [{ "type": "command", "command": "node \"$(git rev-parse --show-toplevel)/.agents/skills/done/scripts/auto-done.mjs\" stop || true", "timeout": 10 }] }],
    "SessionStart": [{ "matcher": "startup|resume", "hooks": [{ "type": "command", "command": "node \"$(git rev-parse --show-toplevel)/.agents/skills/done/scripts/auto-done.mjs\" start || true", "timeout": 10 }] }]
  }
}
```

Codex runs a project's hooks only once the user trusts them: tell them to open Codex in the brain, type `/hooks` and accept the two hooks (only they can do it). Then, for every other tool (Cursor, Gemini, OpenCode...) and in case the hooks are off, run `node <brain>/.agents/skills/done/scripts/auto-done.mjs schedule` once: it checks the brain every hour (launchd on macOS, cron on Linux, Task Scheduler on Windows; `unschedule` removes it). Conversations of Claude Code and Codex are saved on their own; with another tool, the user still types `/done`. Run `node <brain>/.agents/skills/done/scripts/auto-done.mjs status` to check it all: hooks, schedule, agents, last saves and dreams.
9. **Save.** Run `git init` and a first commit "brain: initial setup". Ask if they want a private copy on GitHub so they never lose it; create and push only on yes, always private.
10. **Hermes.** If they already have a server agent (`ssh -o BatchMode=yes hermes true` works and `ssh hermes 'command -v hermes-setup' < /dev/null` finds it), give Hermes the same style: `awk '/^## Output style[[:space:]]*$/{f=1;print;next} f&&/^## /{f=0} f' ~/.claude/CLAUDE.md | ssh hermes 'hermes-setup style'`. It answers `style ok`, and `ssh hermes 'hermes-setup check' < /dev/null` then shows `style=set`. Without a server, skip this step: `setup-vps` does it when they set one up.

```text
<brain>/
├── AGENTS.md          The single guide for every agent
├── .gitignore
├── projects/          One folder per project, each with its About.md
├── notes/
│   ├── journal/       Daily notes, one file per day (YYYY-MM-DD.md)
│   ├── ideas/         Ideas not yet started
│   └── todos/         Loose todos not tied to a project
├── .agents/skills/    The brain skills (step 8), only for this folder
├── .claude/skills     One link to .agents/skills/, never real copies
├── .claude/settings.json  The automatic save hooks of Claude Code (step 8)
└── .codex/hooks.json  The same hooks for Codex, when it is installed (step 8)
```

That is the whole brain on day one. Never create a folder before there is something to put in it: `archives/` appears with the first archived project, `.tmp/` with the first scratch file, `files/`, `assets/` or `output/` inside a project with their first file. No `prompts/` or `scripts/` folder: a process the agent should repeat later becomes a skill (with `skill-manager`), never a saved prompt.

Finish with a short check list, a check or a cross on each line: interview done and confirmed, `## Output style` and `## Brain` in `~/.agents/AGENTS.md`, with `~/.claude/CLAUDE.md` (and `~/.codex/AGENTS.md` if Codex is there) a link to it, `AGENTS.md` exists and there is no `CLAUDE.md` in the brain, only the tree above in the brain (no empty folder anywhere), every project has an `About.md` with a status, the base skills (`/show-me`, `/grill-me`, `/wait-what`, `/connect-tool`, `skill-manager`) open in `~/.claude/skills`, every brain skill (`done`, `dream`, `create-project`, `cleanup`, `projects`) is in `<brain>/.agents/skills` and `<brain>/.claude/skills` is a link to that folder, `<brain>/.claude/settings.json` has the two `auto-done.mjs` hooks (and `<brain>/.codex/hooks.json` when Codex is there, trusted with `/hooks`), the hourly schedule is on, no brain skill in `~/.agents/skills` or `~/.claude/skills`, git is initialised (and pushed if they chose GitHub), Hermes has the style (or "no server yet"). Then tell the user in 3 lines where their brain is, that from now on, with Claude opened in the brain, they type `/create-project` for something new, say "load project X" to pick one up and type `/done` at the end of each conversation to save it into the project (it also runs on its own, and `/dream` tidies everything once a day), that `/cleanup` once a month archives what is finished, and offer to start on their answer to question 10 right now.

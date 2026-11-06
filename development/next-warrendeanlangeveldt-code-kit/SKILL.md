---
name: next
description: The one command for code-kit. Reads where the project stands (a blank folder, a spec being shaped, a ready spec, existing code, a draft config, stories ready, finished or being built) and runs the right skill in the right order, carrying on until something needs the person. Use when the person runs /code-kit:next, asks "what now?" or "what's next?", wants to start a project with code-kit without knowing which skill to use, or comes back to a project mid-build.
---

# Next step

The argument, if given, is passed to the first skill that runs. From a blank folder, that's the idea itself: `/code-kit:next a booking app for mobile dog groomers`.

## 1. Read the state

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" next --json
```

It returns `step`, `why`, `args`, `then` (steps that can follow straight after) and `attention` (things the person should know). The order it applies:

| State                                                        | Step                                                      |
| ------------------------------------------------------------ | --------------------------------------------------------- |
| This is a working session (another session leads)            | working: the step is the lead's, not this session's       |
| Invalid config                                               | `check`, then fix the config                              |
| No config, a draft waiting                                   | `init`, to show it for approval                           |
| No config, a spec still being shaped (brief not `ready`)     | `spec-design`, resuming                                   |
| No config, a ready spec                                      | `init <docs folder>`                                      |
| No config, existing code or docs                             | `init`                                                    |
| Nothing at all                                               | `spec-design`                                             |
| Config, but no specs, plan or stories                        | `spec-design`                                             |
| A companion the config wants, not set up yet                 | `setup`: run that tool's init skill (`args`), before code |
| An older setup missing what init now adds, nothing in flight | `update`: re-run init, before any new story               |
| code-kit's instructions behind this code-kit                 | `instructions`: bring CLAUDE.md and the agents up to date |
| A lane waits on a request you decide                         | `decide`: approve it, or answer with an alternative       |
| Stories finished on their branches                           | `review`, then `dispatch` what's ready                    |
| Design stories ready (`**Lane:** design`)                    | `design`, then `dispatch` what needs no design            |
| Ready stories whose screens' designs are only in the tool    | `design` with `handOver: true`: `--hand-over` first       |
| Stories ready                                                | `dispatch`                                                |
| The lead's own stories ready (`**Lane:** lead`)              | `lead`: the lead builds them itself                       |
| Stories being built, nothing else can start                  | wait                                                      |
| Ready stories with gaps in the plan, or a dependency cycle   | `spec-design`, to fix the plan                            |
| Every story done                                             | done: `status`, then `spec-design` for the next milestone |

Tell the person in one or two lines what you found and what you're about to run, with anything under `attention`. If `attention` says the folder isn't a git repository, run `git init` before init (spec-design doesn't need one).

## 2. Run it

Run the named skill with the Skill tool: `code-kit:<step>`, with `args` (and the person's argument, if they gave one). Follow that skill in full. This skill only chooses; it never does a step's work itself.

- **`setup`:** run the skill named in `args` (for example `context-graph:init`); it's another plugin's, so call it by that full name.
- **`update`:** run `code-kit:init`. `why` names what the setup is missing (the design gate, design stories, a QA lane, a security reviewer); init adds those, shows the person the difference, and sets `"setup": 3`. Until then no new story starts; work already started goes on to review and merge.
- **`instructions`:** there's no skill to run. With `args` `write`, run `code-kit instructions --write`. With `merge`, some files were written before code-kit marked its part: run `code-kit instructions` to list them, replace each old part with what `code-kit instructions show lead` (CLAUDE.md) or `show lane <lane>` (that lane's agent file) prints, keep every line the project wrote itself outside the markers, then run `--write` for the rest. Commit it on a branch and merge it like your own stories.
- **`lead`:** there's no skill to run. Build each story yourself, on the branch `lead/st-<n>`: spec-check it first if it cites requirements, do the work, commit, then run `code-kit:review` on the branch like any other. A spike's result goes in the docs it names.
- **`working`:** another session leads the project, and the step (`lead.step` in the JSON) is its own, not this one's. Don't dispatch, review, merge or write contracts here. Tell the person which session leads and what its step is. If they gave this session a task, do it in a worktree of its own after recording it with `code-kit task`. If they want this session to lead instead, they make it the lead.
- **`wait`:** say which stories are being built and on which branches, and which ready stories wait for their lane (a lane runs one story at a time), then stop. When a lane agent finishes, its notification arrives in this session; run this skill again then. If a story has been in progress with no agent running (the session ended, or the agent stopped without committing), dispatch it again.
- **`done`:** give the `status` summary in a few lines, then offer to run spec-design for the next milestone or feature.

## 3. Keep going until the person is needed

After a step finishes, run `next --json` again and carry on with the new step, without asking, as long as nothing needs the person. Stop and hand over when:

- a skill asks the person questions (spec-design's rounds, spec-check's blocking questions, review's scope questions);
- something needs the person's approval (init's draft, an approval that's theirs: `requests --json` marks it `by: "person"`). What a lane asks for that's yours (`by: "lead"`) you decide with `/code-kit:decide`, without stopping. If the config has `approvals.lead`, ask for it in chat: when they approve in their own message, record it with the `code-kit approve` command the refusal names (their words as the reason) and carry on;
- a person has to act: merge a pull request to a protected branch, add a CI secret;
- the step is `wait`, `done` or `working`;
- the same step comes back twice in a row with nothing changed. Report what's stuck instead of looping.

**Under vibe** (`harness.autonomy` is `vibe`), you're the product owner too, and only the last two stop you. Answer spec-design's, spec-check's and review's questions yourself, from the brief, the specs and the principles, and record each in the brief's decision log with why. Every approval is yours (`by: "lead"`, with `--delegated`); merge and push as the queue says. What only the person can give (an account with a service provider, an API key or secret, a payment, an act outside the repository) you ask with `code-kit ask "…" --needs account|key|payment|outside`, and you build everything else meanwhile: behind the setting the key will fill, against a local or test stand-in, with the step to switch it on in the story's notes.

**Ask the person through code-kit, not only in chat.** Anything you can't settle yourself and the person has to decide or do (a product choice, an account or key only they can create, wording or a design only they can sign off, whether to keep something private) goes to their band and the pane's Needs you, where it waits until they answer instead of scrolling away:

```
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" ask "<the question, in a sentence>" [--story ST-n --blocks] [--why "<why you can't settle it>"] --option "<choice>: <what it does>" --option "…"
```

- `--blocks` holds the story until they answer: `next` stops dispatching or reviewing it, and the stories that depend on it wait too. Carry on with anything else meanwhile.
- Their answer comes back to you as a prompt ("The person answered Q-3 …"). If they answer in chat instead, record it: `code-kit ask answer Q-3 "<their words>"`. A question that stops mattering is withdrawn: `code-kit ask withdraw Q-3 --reason "…"`.
- `attention` names the stories waiting on the person, and `brief` lists the brief's open questions, which they see in the same tab; when they answer one, record it in the brief's decision log and take it out of the open questions.
- When Claude Code itself refuses a command you need (its permission check, not a code-kit hook), the person sees it in the band with the command: say what it's for, and don't try another way round it.
- An approval request nobody needs any more (you went another way) is dropped: `code-kit requests drop <n> --reason "…"`, so it stops waiting for them.

**When code-kit itself is wrong** (a refusal that shouldn't have happened, a crash, a pane showing the wrong thing) and the config has `harness.report.on`, draft a report for code-kit's maintainers: `code-kit report "<what went wrong, in a few words>" --what "<what happened>" --expected "<what should have>" --command "<what you ran>" --refusal "<what code-kit said>"`. Only code-kit's own facts go in it, never the project's code or data. The person reads it and sends it, or not. Then work around it if you can.

When you stop, end with one line saying what happens next and who does it, e.g. "Next: you approve the draft config, then I dispatch ST-1 to ST-4."

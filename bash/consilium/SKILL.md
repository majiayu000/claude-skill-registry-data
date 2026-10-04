---
name: consilium
description: Run a consilium - a structured multi-model review of a technical question or design decision. Independent reviewers (Claude, Codex, Open Code and others) each write a review of the same brief, arbiters merge them into a draft decision, and after the user confirms it an implementer makes the authorized changes and verifiers check them. Use ONLY when the user explicitly asks for a consilium, a multi-model review or a second opinion from several models; it sends project files to several model providers and can take many minutes.
---

# Consilium

A consilium gets several independent models to look at one question, then merges what they say into a **draft** decision that the human confirms. The human is always the final arbiter; no model decides.

```
brief.md ─┬─► host review (you)          ┐
          ├─► reviewer 2 (external CLI)  ├─► decision.md (DRAFT, two arbiters) ─► you confirm
          └─► reviewer 3 (external CLI)  ┘        │
                                                  ▼ only after confirmation
                              implementer ─► verifiers ─► implementer fixes ─► you review the diff
```

Everything is plain files in `consilium/<date>-<slug>/` inside the project.

## Setup you need to know

- `SKILL_DIR` is the folder that contains this `SKILL.md`. All scripts are in `$SKILL_DIR/scripts/`. Run them from the **project root** with `bash`.
- Set `CM_HOST` to the agent you are: `claude` when you are Claude Code, `codex` when you are Codex. You write the host review yourself, so the script never launches you a second time. Prefix every script call with it, e.g. `CM_HOST=codex bash "$SKILL_DIR/scripts/init-case.sh" ...`.
- Settings live in `<project>/.consilium.conf` or `~/.config/consilium/config` (`KEY=VALUE`, see `consilium.example.conf`). The important ones: `CM_LANG` (`en` or `ru`, language of the documents), `CM_REVIEWERS`, `CM_ARBITERS`, `CM_VERIFIERS`, `CM_IMPLEMENTERS`, `CM_OUT_DIR`. Do not change the panel unless the user says so.
- Adapters that are not usable (CLI missing, no model configured) are skipped automatically and reported; a round with fewer reviewers is still valid and the decision says who is missing.

If the user gave no question, ask what to discuss and wait. Do not invent a topic.

## Step 1 - Check the panel

```bash
CM_HOST=<you> bash "$SKILL_DIR/scripts/run-reviewers.sh" --plan
```

Tell the user in one line which reviewers will run. The reviewers receive whatever project files they read, so if the user has not used this skill before, mention that project content goes to those providers and let them object.

## Step 2 - Create the case

Pick a short English kebab-case slug (2-4 words) for the topic.

```bash
CM_HOST=<you> bash "$SKILL_DIR/scripts/init-case.sh" <slug> "<human title>"
```

It prints the case folder path. It takes the date from the system clock; never use a date from memory. It creates `brief.md` (with `<!-- TODO -->` markers), a placeholder for each review, a `decision.md` placeholder and `tasks.json`.

## Step 3 - Gather facts, fill in the brief

Collect **facts, not recommendations** relevant to the question: the code involved (file:line), existing docs and earlier decisions, current behavior. If you can delegate to a read-only research agent, do; otherwise do it yourself, read-only. Then edit `brief.md` and replace every `<!-- TODO ... -->` with real content:

- **Question** - the user's question, tidied, meaning intact.
- **Known facts** - each with a reference.
- **Constraints** - keep the defaults, add 1-3 specific ones if obvious.
- **Out of scope** - 1-3 items.

Leave the structure and headings as they are. `run-reviewers.sh` refuses to start while any TODO marker remains.

## Step 4 - Launch the external reviewers

```bash
CM_HOST=<you> bash "$SKILL_DIR/scripts/run-reviewers.sh" <case-dir>
```

This returns immediately: the reviewers and one watcher run detached. The watcher drafts `decision.md` on its own once everyone has answered or failed. You do not need a background-task feature and must not poll the reviewers.

## Step 5 - Write your own review, independently

Right away, without waiting for the others, write `<case-dir>/<CM_HOST>-review.md` (replace the placeholder). Base it on the facts plus your own assessment of the question (risks, assumptions, recommendation), not a retelling of the facts. Use exactly the six section headings listed in the brief's response-format section.

- First line: `# <Agent name> review (<your real model id>): <short topic>`. Use the actual model id of this session from your system context; do not guess or write a generic name.
- **Independence rule:** do not open any other `*-review.md` in the folder until your own is written and saved, even if a file is already filled in. Independence is the point.

## Step 6 - Report

Now (and only now) check how the others did: `<case-dir>/.logs/runner-*.log`, `<case-dir>/.watch.log`. Tell the user: the case path, who ran and how it ended, the "Verdict" section of your own review. Remind them that the watcher will draft `decision.md` (two arbiters) when the reviewers finish, and that it is a **draft** to be read and confirmed, not a final decision. Tell them they can follow the case live in the reader, started from the project root in their own terminal: `bash "$SKILL_DIR/scripts/reader.sh" --open` (http://localhost:4600, needs Node.js). Do not start it yourself unless asked: it runs until stopped. If `decision.md` is already there, summarize agreement and disagreements briefly and quote the "Authorized code changes" list.

Stop here unless the user confirms the decision or explicitly said, in the original request, to implement right after the decision.

## Step 7 - Implement, verify, fix (after confirmation)

1. **Work tree.** Create a separate git worktree on a new branch (name it by meaning, or as the user says). Never work in `main`/`dev` or in the user's primary checkout. Do not commit or push.
2. **Implement** - the implementer makes exactly the changes listed under "Authorized code changes":
   ```bash
   CM_HOST=<you> bash "$SKILL_DIR/scripts/implement.sh" <case-dir> <worktree> impl
   ```
   Report: `impl-report.md`.
3. **Verify** - all verifiers in parallel, independently, code read-only:
   ```bash
   CM_HOST=<you> bash "$SKILL_DIR/scripts/verify.sh" <case-dir> <worktree>
   ```
   Reviews: `<name>-impl-review.md`.
4. **Fix** - the implementer's second pass over the verifiers' defects:
   ```bash
   CM_HOST=<you> bash "$SKILL_DIR/scripts/implement.sh" <case-dir> <worktree> fix
   ```
   Report: `fix-report.md`. Disputed items, and anything beyond the decision's scope, are listed as "not applied" for the user to decide.
5. **Acceptance.** Before reporting, check the result yourself against the project's own definition of done (build, tests, lint, or a run). Do not take the implementer's or verifiers' numbers on faith.
6. **Report:** branch and worktree path, what changed, each verifier's verdict, what the second pass fixed, what was not applied and why, what remains unverified. Commit, merge and deploy only on the user's explicit command.

Steps 7.2-7.4 take minutes to tens of minutes. Run them in the background if your environment supports it (Claude Code: `run_in_background`; otherwise `nohup ... > log 2>&1 &` and check the log), and do not poll in a tight loop.

## Safety rules

- Reviewers, arbiters and verifiers never modify project code. Only the implementer does, and only in the worktree, only what the decision authorizes.
- No destructive or production action, and no merge, without the user's explicit approval.
- Never present the draft `decision.md` as decided. The user confirms it.
- If a script fails, read the log it names in `<case-dir>/.logs/` and tell the user what failed; do not retry blindly in a loop.

## Other scripts

`reader.sh [--port N] [--open] [--public]` serves the local reader (`--public` for a tunnel such as ngrok, password-protected; only when the user asks to share); `run-reviewer.sh <adapter> [case]` re-runs one reviewer; `write-decision.sh <case>` re-synthesizes the draft; `watch-and-decide.sh` is started for you. Adding a model or CLI: `docs/adapters.md` in the repository.

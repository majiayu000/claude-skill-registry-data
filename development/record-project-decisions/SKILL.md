---
name: record-project-decisions
description: >-
  Load this skill when a decision binds a whole project: write it as a rule file,
  .claude/rules/decision-<topic>.md, that every session loads. Trigger on "we decided", "from now on
  we use", "record this decision", "starting a new project".
argument-hint: "[record <decision> | seed]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Record project decisions

Write every decision that binds the project as its own short rule file, so every later session
and every kind of task follows it without being told again. Done when each decision sits in its
own `.claude/rules/decision-<topic>.md` file, no two files contradict each other, and whatever
could not be settled is reported as open.

Claude Code loads every `.md` file in `.claude/rules/` at launch with the same priority as
`.claude/CLAUDE.md`. A decision written there outranks plugin standards in every session, with no
skill needing to know about it. The files sit directly in `.claude/rules/`, never in a subfolder,
and the `decision-` prefix marks the ones this skill owns.

Two modes. **Record** (the default) writes one decision from the conversation, or promotes an
entry of the agent's decision log that turns out to bind the project. **Seed** writes a
project's decisions in bulk: at the start of a project, on request, or after a plugin is
installed.

## Procedure

### Record

1. **State the decision as a rule:** imperative, specific, checkable. "Build every UI with
   SvelteKit, never React", not "prefer modern frameworks". A statement that changes nothing an
   agent would do is not a decision: leave it in the conversation or its source document.
2. **Read what exists:** every file in `.claude/rules/` and the project's `CLAUDE.md`. Already
   stated there in the same terms: stop and say so. Same topic in a `decision-` file: that file is
   the one to update. Contradicts a decision: see Stop conditions. Edit only `decision-` files:
   the project's other rule files are not this skill's to change.
3. **Write the file** in the shape under Output, and report its path.

### Seed

1. **Read what exists**, as in Record step 2.
2. **Collect candidates from three sources:**
   - **Choices the installed skills leave open.** From the skill listing, pick the plugins this
     project would use. For each, dispatch one `ceh-every-session:bulk-reader` subagent on its
     `SKILL.md` files, following `ceh-every-session:delegate-bulk-reads`. Ask it for every choice
     a skill leaves to the project: alternatives it offers, "if X use A, otherwise B" branches,
     values it asks for. One line each, with `path:line`. Send the subagents in parallel. Take each
     plugin's directory from its `installPath` in `~/.claude/plugins/installed_plugins.json`, not
     from `~/.claude/plugins/cache/`, which keeps every version ever installed and would surface
     choices that no longer exist. Project skills live in `.claude/skills/`.
   - **Decisions already written down:** the README, `product/ARCHITECTURE.md` Key Decisions, plans
     under `product/plans/`, ADRs (`docs/adr/`, `docs/decisions/`), business plan files
     (`product/BUSINESS_PLAN.md`), `GLOSSARY.md`, and
     manifests (`package.json`, `pyproject.toml`) as evidence of the stack.
   - **Areas no skill asks about:** who the product is for, market, language and locale, what is
     out of scope, stack, hosting, data and authentication, product name and voice. Take only the
     areas this project has reached.
3. **Merge** into one candidate per fact. "Svelte, not React" settles open choices in several
   skills at once and is still one decision. Drop choices this project will never face: a CLI
   tool has no UI framework question.
4. **Resolve each candidate.** Inferred, when a file answers it, citing that file. Otherwise it is a
   question.
5. **Settle the questions.** Interactive: ask them up front with `AskUserQuestion`, at most four per
   call, calls back to back, each with a recommended answer listed first. Show the inferred
   decisions in the same pass so the user can correct one. No human (a subagent, a headless run):
   write only the inferred decisions and report the rest as open.
6. **Write one file per decision**, then report.

## Rules

- **One decision per file, a few lines each.** Adding, changing, or retiring a decision then
  touches one file, and `git log` on that file is the decision's history.
- **Committed with the project.** The `decision-` files are the record people read and review,
  not agent scratch, so they are never added to `.gitignore`. The agent's decision log stays
  separate.
- **Current decisions only.** A replaced decision is edited in place or its file deleted, never
  marked "previously". Git keeps what came before, and every line loads in every session.
- **A rule, not its history.** Comparisons and long reasoning stay in their source document. The
  file carries a one-line reason and points there.
- **Never write a guess.** An inferred decision cites the file that shows it. Anything else is
  asked, or reported as open.
- **A decision settles a choice; it never switches a standard off.** "We skip tests" overrides a
  skill rather than choosing between options it offers. Report it as an override of that skill
  instead of writing it: an override that keeps recurring is a defect in the skill.
- **No `paths` frontmatter by default.** Decisions bind non-code tasks too. Scope one with
  `paths` only when it concerns one part of the tree and nothing else.
- **Keep the set small.** Once the `decision-` files pass 150 lines in total, say so in the
  report and name the decisions that bind least, because every line costs context in every
  session.

## Output

One file per decision, `.claude/rules/decision-<topic>.md`, directly in `.claude/rules/`. Name it
for the topic, not the answer (`decision-ui-framework.md`, `decision-target-market.md`), so
changing the decision edits the same file.

```markdown
# <Topic>

<The rule: one or two imperative sentences.>

Why: <one line>. Decided <YYYY-MM-DD>. Source: <path, or "conversation">.
```

The report lists each file written, updated, or deleted, the open questions, and any override
reported instead of written.

## Stop conditions

- A new decision contradicts an existing one → interactive: ask which holds, recommending the
  newer one. No human: leave both files unchanged and report the conflict.
- A decision would switch off a skill's standard → report it as an override and write nothing.

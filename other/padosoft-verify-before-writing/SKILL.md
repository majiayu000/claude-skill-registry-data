---
name: padosoft-verify-before-writing
description: >-
  Use this skill whenever an agent is about to write something it has not verified — a call to a helper whose
  signature it inferred from the name, an enum case that sounds plausible, a config key, a column, a file
  path mentioned in a plan but never opened, a docblock explaining a mechanism nobody read, a commit message
  asserting what the code does. Also when the user says the agent invented an API, hallucinated a method,
  confidently described behaviour that does not exist, or asks how to stop it happening. It gives the rule
  (ask, or log the doubt — never the silent third option), what must be verified, and how autonomous mode
  changes the answer without removing the obligation. Do not use it for verifying facts about the outside
  world, for prompt engineering, or for reviewing code somebody else wrote.
license: MIT
compatibility: >-
  Any language, any agent. The obligation is on whoever writes into the repository, human or not.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: Never invent silently — ask, or record the doubt and report it.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: hallucination, verification, agent discipline, autonomous mode, doubt log, signatures, invention
---

# Verify before writing

An invented fact that reaches the repository does not stay a mistake. It becomes a **source**: the next
session reads that docblock, that comment, that setting description, and takes it as true. The cost of a
thirty-second check is smaller than writing it wrong, reviewing it, fixing it, and then fixing everything
that was built on it.

**The rule: never invent silently. Ask, or record the doubt and report it. What is forbidden is the third
option — writing an unverified fact and telling nobody.**

---

## 1. What has to be verified, always

| Statement about | Verification |
|---|---|
| A function, helper or method signature | read the source — never infer from the name |
| What a parameter *means* | read the implementation, not the identifier |
| A file, class or method named in a task or a plan | open it before referencing or editing it |
| A project convention (naming, structure, paths) | the written rule **plus** one real example in the repo |
| Infrastructure behaviour (tenancy, cache, queue, auth) | the instruction file, or the code |
| Framework or library behaviour | the installed version's source, or its official docs |
| Enum cases, constants, status values | read the definition — do not derive them from the domain |
| A name, path or identifier with no obvious precedent | ask |

The recurring failure is not exotic. It is **inferring an argument order from a helper's name**, and being
wrong by one position.

## 2. The two modes, and the obligation that survives both

| Mode | When | On a doubt |
|---|---|---|
| **Interactive** (default) | a person is present and answers | **stop and ask** before writing |
| **Autonomous** | headless, or the person explicitly said *do not ask* / *do not stop* / *go ahead* for this task | do not ask. Take the **most conservative** option, **log the doubt**, and report every one of them before declaring the task done |

Two things people get wrong about autonomous mode:

- **Its authorisation is scoped to the task it was given for.** "Do this without asking me" covers *that*.
  A new task, or a change of subject, returns to interactive. A generic "just do it" does not enable
  autonomous mode — it takes an explicit instruction not to interrupt.
- **It removes the question, not the disclosure.** Finishing without listing the doubts is a silent
  invention with extra steps.

When the mode is ambiguous, the default is interactive.

## 3. The safety exception: stop even in autonomous mode

*Log and continue* does not apply when the unverified assumption could cause:

- **something irreversible** — dropping a column or a table, a mass delete, a state reset, a force push,
  a recursive delete, overwriting uncommitted work;
- **an effect on production or a shared system** — a deploy, a tag on the main branch, a migration against
  a live database, a setting change, a push to a protected branch, a message or email to real people;
- **the loss of somebody's work** — uncommitted files, local branches, stashes, ignored files that may be
  work in progress.

Here the cost of being wrong exceeds the cost of interrupting. Ask.

## 4. When a doubt has to be handled

It is not "whenever you are unsure" — that produces paralysis. It is:

- the information was not found after two or three targeted searches;
- **sources disagree** — the rule says one thing, the code does another;
- the task needs a name, a path or a value with no obvious precedent;
- you are about to add descriptive information **the task did not ask for**, "for completeness";
- a comment or docblock is about to explain **how a mechanism works** when that mechanism was never read.

Then: interactive → *"I have not verified X. Plausible options: A / B / C. Which one?"* A precise question
beats a plausible invention, and it is cheaper for everyone. Autonomous → take the conservative option, log,
report.

## 5. The doubt log

```markdown
**Doubt #<n> — <area>**
- Not verified: <what>
- Assumption taken: <what>
- Plausible alternatives: A / B / C
- Affected: `path/file.ext:<lines>`
- Risk if wrong: low | medium | high
```

**Report it before finishing, in the final answer, where the person actually reads.** And when there were
none, say so explicitly — *"Doubts: none"* — so that silence is a statement rather than a possible omission.

## 6. What is *not* invention

So the rule does not become an excuse to stall:

- Applying a documented, read convention to a new case.
- Writing code whose behaviour is entirely in the diff you just wrote.
- Describing **what** something does, when that is observable from the task, while staying silent on **how**
  a mechanism you did not read works.
- Saying "I do not know" — that is the rule working, not a failure of it.

---

## Gotchas

- **A plausible name is the strongest hallucination trigger there is.** `getUserByEmail` might take
  `(string $email, bool $withTrashed = false)` or `(string $email, ?int $tenantId)`. The name cannot tell
  you, and the confident version is the wrong one.
- **The docblock is the most expensive place to be wrong**, because it is read as documentation forever and
  nothing ever fails because of it.
- **A plan is not evidence.** A file named in a task description may have been renamed, or may never have
  existed. Open it.
- **A rule file can be stale.** When the rule and the code disagree, that is a doubt to raise, not a
  contradiction to resolve silently in favour of either — see **`padosoft-docs-match-code`**.
- **"It is probably fine" is the sentence to notice.** It appears exactly where this rule applies.

## Checklist

- [ ] Every signature called was read, not inferred
- [ ] Every enum case, constant and config key was read at its definition
- [ ] Every file named in the plan was opened before being edited or referenced
- [ ] No docblock or comment explains a mechanism that was not read
- [ ] Conventions backed by a written rule **and** a real example
- [ ] Mode identified; autonomous only with an explicit instruction, scoped to this task
- [ ] Safety exception respected — irreversible, production and other people's work always ask
- [ ] Doubt log kept, and reported in the final answer (or "none" stated explicitly)

## Final report

```
Verified before writing: signatures <n> · enums/constants <n> · files opened <n>
Mode: interactive | autonomous (authorised by: <what was said>, scope: <task>)
Doubts: none | <list, each with assumption, alternatives, location, risk>
Stopped to ask: <what, and why it fell under the safety exception> | not needed
```

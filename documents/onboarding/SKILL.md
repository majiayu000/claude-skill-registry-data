---
name: onboarding
description: "Use when onboarding a repository for agentic development: preparing it so an outside developer, or an agent, can pick it up without asking questions. Works on an existing codebase or a brand new one. Trigger whenever the user asks to onboard a repo or project, make it agent-ready, prepare it for Claude, set up CLAUDE.md or AGENTS.md and the docs behind them, asks why agents struggle to work in this codebase, or is starting a new project and wants it set up right from the first commit, even if they never say the word onboarding."
---


# Onboarding

A repository is only as good for agentic development as it is for a junior developer to pick up. If an outsider can follow the code, find the standards, and see how to contribute without asking anyone, an agent can too. Onboarding the repository properly is what sets agents up for success.

## Golden rule

If an outside developer would need to ask questions about the repository, it is probably not mature enough to be worked on agentically.

On a new project nobody can answer those questions yet, the user included. Onboarding is then the work of deciding the answers and recording them, so the repository is mature before the code arrives rather than long after.

## Before you write

Everything this skill produces is prose a person reads. Invoke the `writing` skill with the Skill tool before drafting any of it.

## Establish where the project is

Before surveying anything, work out whether there is a product to describe. Look for source beyond the scaffolding, a build that runs, tests, and a pipeline. Then tell the user which of these you are working with, because every section below reads differently in each:

- **An existing codebase.** The answers are in the repository. Your job is to find them, verify them, and write them down.
- **A new project.** The answers do not exist yet. Your job is to help the user decide them, then write down what was decided.

Most repositories sit between the two. Apply the existing-codebase reading to what is built and the new-project reading to what is not.

On a new project, two rules govern everything that follows.

**Decide and record, don't design.** Record the choice and the reason behind it, never the implementation that would follow from it. "Postgres, because the data is relational and the team already runs it" is a decision worth writing down. A schema is a design, and nobody has earned the right to one yet.

**Write thin and let it thicken.** An empty repository invites you to fill it: a domain model, a rulebook, an architecture for a system nobody has built. All of it is guesswork carrying the authority of a document, and the first week of real code contradicts it. Write the little that is genuinely settled and add to it as the code lands.

The interview moves too. On an existing codebase, asking the user is what you do when the repository cannot answer. On a new project, it is where you start.

## Survey what already exists

Before writing anything, take stock of the documentation the repository already has: the README, a CONTRIBUTING file, anything under `docs/`, and any wiki or Confluence pages the repo links to.

For each file this skill produces, check whether an equivalent already exists. If it does, enrich it rather than write a competitor. A second, conflicting source of truth is worse than a gap. If an existing doc is stale, correct it as part of this work, and flag anything you cannot verify to the user.

On a new project there is nothing to survey. The sources are the user, and any prior art they point at: a specification, a design document, or the earlier project this one replaces.

## Write what stays true

These files are read months after they are written, and a doc that misleads is worse than one that is missing. So write what stays true, and leave out what is only true today.

- **Instructions survive, snapshots rot.** "Put each app's tests in its own `tests.py`" still holds next year. "Ten tests in two files" is wrong on the next commit, and the count is exactly the part a reader trusts.
- **Do not inventory.** Counts, file-by-file catalogues of what each file contains, and lists of what is empty or missing all decay on ordinary commits. Naming the major components of a system is fine, because that shape changes rarely. Naming what sits inside each file is not.
- **Cite real code as an example of a rule, never in place of one.** The example shows what the rule means; it is not itself the rule.
- **A gap you find is a finding, not a fact to record.** Where something is missing, broken, or unregistered, raise it with the user and propose the fix. Writing down the way around it makes the workaround permanent.

The exception is the setup facts a reader cannot start without: exact tool versions, commands, and configuration values. Record those precisely rather than vaguely, and treat keeping them current as part of any change that moves them.

On a new project, most of what you can write is intent rather than fact. That is allowed, provided it is labelled as intent. "We intend to deploy this to Cloud Run" is honest. "This deploys to Cloud Run" is a claim the reader will act on and find untrue.

## What the product is for

The most valuable document on a new project is the one nobody thinks to write: what is being built and why. Record it in `docs/PRODUCT.md` before any technical detail, because every decision after it gets judged against it. Cover:

- the problem, and who has it
- the users, and what they are trying to get done
- what is in scope, and what is deliberately out. The second half is the useful one.
- what success looks like, in terms somebody could check
- the decisions taken so far and the reason for each: language, framework, datastore, hosting, and anything else the team has settled. Add to this as decisions are made, so a settled question is not reopened and no agent quietly introduces a second way of doing the same thing.

This comes out of an interview. None of it can be inferred, and a plausible invention here poisons every document downstream.

On an existing codebase this is usually answered already, in the README or in the product's own documentation. Point at that rather than writing a competitor. If nothing anywhere says what the product is for, raise it as a finding: it is the first question an outsider asks.

## Standards

Check whether the repository has linting rules. If it has none, flag this to the user and explain why they matter: without them, standards live in people's heads, and neither an outsider nor an agent can follow them.

Read the linter config to learn what is already enforced, then keep every bit of it out of `docs/CODING-RULES.md`. Name the config file and move on. A linted rule is enforced on every commit whether or not anyone wrote it down, so a prose copy of it is a second source of truth that goes stale the moment someone edits the config.

What belongs in the file is only what no tool will fail a contributor for: naming conventions, the base classes to inherit, how modules are allowed to depend on each other, the decisions that must be made deliberately rather than by default. Work these out from the code itself and record them in `docs/CODING-RULES.md`.

Two tests before a rule goes in:

- **Could a linter enforce this?** Then it belongs in the linter config. If it should be enforced and isn't, propose the linter rule to the user rather than writing a prose rule nobody runs.
- **Is it a rule or a description?** "Inherit `ModelBase`" is a rule. "This foreign key cascades because the child is meaningless without its parent" is a fact about today's code. Write rules.

Keep tooling and workflow out as well: how to run the formatter, which commands to avoid, how the build behaves. That is `README.md` or `CONTRIBUTING.md`.

On a new project there is no code to work the rules out from, and no linter either. Set up the linter and formatter now, using the ecosystem's standard configuration: this is the cheapest moment to do it, and everything written afterwards inherits it. Then keep `docs/CODING-RULES.md` almost empty. Record only the conventions the user has actually decided, and add each new one as it is agreed, rather than writing a rulebook for code that does not exist.

## Environment setup

Work out everything an outsider needs before the project will run at all:

- the tools required and their versions: runtime, package manager, SDKs, CLIs
- environment variables and configuration values, what each one is for, and where its value comes from
- secrets: where a new developer obtains them, and where they live locally. They belong in a local `.env` file excluded from version control via `.gitignore`, never hardcoded in code or committed config.
- local services the project depends on (databases, queues, containers) and how to start them

Record this in `README.md`. This is the section outsiders get stuck on most, so be precise: name exact versions and exact commands, not "install the usual tools".

## Getting started

- Determine how to run the project: the dependencies it needs, how to build it, and how to run its tests. Record this in `README.md`.
- Determine where issues are tracked. Record this in `README.md` as well.

On a new project none of this runs yet, so do not document an aspiration. Build the walking skeleton first: the smallest thing that installs, builds, starts, and passes one test, along with the `.env.example` and `.gitignore` that go with it. Then write down what you actually did. Every command in this file should be one you have run.

## Contributing

Determine how a change actually gets from an idea into the main branch, and record it in `CONTRIBUTING.md`:

- the pipelines a change must pass. At a minimum, a pipeline should cover linting, building, and running the test suite.
- the pull request process: how a change is reviewed, who reviews it, and what is required before it can merge
- the branching strategy and branch naming conventions
- commit message conventions
- the definition of done: what a change must include before it is complete, such as tests, documentation updates, or changelog entries. Point at the testing bar in `docs/TESTING.md` rather than restating it here.

If the repository has no established convention for one of these, don't invent one silently. Propose one to the user and record what they agree to.

On a new project none of it exists to be discovered. Propose each, and build what you can: a pipeline that lints, builds, and runs the tests is worth having before the first feature rather than after it. Record anything the user defers as deferred, not as fact.

## Architecture

Determine the architecture of the product and record it in `docs/ARCHITECTURE.md`. Cover:

- the high-level architecture: the major components, what each is responsible for, and how they talk to each other
- the entrypoints: where execution starts, such as the main function, HTTP routes, scheduled jobs, message handlers, or CLI commands. An outsider reading a codebase for the first time needs to know where to start reading.
- a class diagram of the core domain model
- high-level sequence diagrams for the most important flows in the product

Describe the shape of the system: what each component is responsible for, and where the boundaries between them fall. A walk through the file tree is not architecture, and the first refactor invalidates it.

Use Mermaid for the diagrams so they render on the git host. Keep them at a high level: a diagram of every class is noise, and a sequence diagram of every branch is a flowchart. Diagram the model and flows an outsider must understand to make their first change safely.

On a new project there is no architecture to determine, and inventing one here is the failure this skill most wants to avoid. Record the intended shape and nothing beyond it: the components you mean to have, where the boundaries between them fall, and the stack decisions already captured in `docs/PRODUCT.md`. Label the whole file as intent and say plainly that it will move.

Leave the class diagram and the sequence diagrams out until there is code to diagram. A domain model drawn before the first feature is a guess, and once it sits in a document people build to it instead of thinking. Revisit this file when the skeleton has grown into a system, and add the diagrams then.

## Testing

`docs/TESTING.md` is a map, not a tutorial. It answers two questions: where each layer of the pyramid lives and how to run it, and what verifying a change requires. Keep implementation detail out. How to write a good test is a convention, so it belongs in `docs/CODING-RULES.md`, and how the test framework itself behaves belongs to that framework's own documentation.

For every layer the project has, record where it lives and the command that runs it:

- unit tests: the directory or file pattern they sit in, and the command
- integration tests: the same, plus how they virtualise external dependencies and which dependencies that covers
- end-to-end tests: the same, plus anything that has to be running first

Record how to run a single file and a single test as well, which is the first thing anyone fixing a failure needs.

Then state the bar a change has to clear to be complete. Unless the project sets its own, a feature needs a unit test and an end-to-end test that drives the system exactly as a user would. Where a layer does not exist yet, say so in one line and raise it with the user, naming what would have to be built for it to exist.

On a new project, choose the test framework with the user and write one real test at each layer the project intends to have. A single passing test per layer makes every command in this file a command you have run, and a layer costs far less to add now than to retrofit later. Set the completeness bar on day one: it is a decision rather than an observation, and it shapes every change that follows.

## Debugging

An outsider's change will break something before it works, so record how a developer actually diagnoses problems day to day:

- how to run the project while developing: watch or hot-reload mode, debug builds
- where logs go locally, and how to raise the log level
- how to attach a debugger, including editor configuration where it exists (for example a `launch.json`)
- the failure modes a new developer hits most, and their fixes: a local service not running, a stale dependency, a missing or wrong environment variable

Record this in `README.md` under a Debugging section. On a new project, record the run command, the logs, and the debugger setup, and leave the failure modes to be filled in as they are hit.

## Files

These are the files the sections above record their findings in. Together they are the deliverable of this skill.

- `README.md`: environment setup, how to run the project, its dependencies, how to build it and run its tests, how to debug it, and where issues are tracked.
- `CONTRIBUTING.md`: the pipelines a change must pass, the pull request process, branching and commit conventions, the definition of done, and the documentation upkeep rule.
- `docs/PRODUCT.md`: what the product is for, who it serves, what is in and out of scope, what success looks like, and the decisions taken so far with the reason for each. Required on a new project. On an existing one, write it only where nothing already answers those questions.
- `docs/CODING-RULES.md`: the naming standards, patterns and conventions a contributor must follow that no linter enforces. Anything a linter can check belongs in the linter config, not here.
- `docs/ARCHITECTURE.md`: the architecture of the product, its entrypoints, a class diagram of the core domain model, and sequence diagrams of the most important flows.
- `docs/TESTING.md`: where each layer of the testing pyramid lives, the command that runs each, and the bar a change must clear to be complete.

## Updating agents

By default, create every file this skill names, at the location it names. If the user wants the information elsewhere, record it there and treat that as the source of truth.

Update `AGENTS.md` or `CLAUDE.md` with references to these files. References only, never the content: `CLAUDE.md` loads into every session, so keep it light.

Each pointer must name the task that makes the doc worth loading, not the doc's topic. An agent reads `CLAUDE.md` before it knows which docs matter, so "architecture documentation" tells it nothing; "before changing code in an unfamiliar area" does. One line per doc, condition first:

- Before writing or changing code: read `docs/CODING-RULES.md`.
- Before a change in an unfamiliar area, or one that spans components: read `docs/ARCHITECTURE.md`.
- Before planning a feature, or when judging whether something is in scope: read `docs/PRODUCT.md`.
- Before writing tests or verifying a change: read `docs/TESTING.md`.
- Before branching, committing, or opening a pull request: read `CONTRIBUTING.md`.
- When setting up, building, running, or debugging: read `README.md`.

Adjust paths and conditions to wherever the information lives. Add any other task-specific docs, such as an API reference or a runbook, in the same form.

## Verify the onboarding works

The docs are not done until they have been proven. Verify them with a swarm of subagents, one per doc, launched in parallel. A subagent starts with none of the context you built up writing these docs. That makes it an honest stand-in for the outsider: it can only succeed on what is written down.

Run the swarm on Haiku: pass `model: "haiku"` to the Agent tool. Each subagent follows written steps and checks claims against the repository rather than designing anything, and the swarm is a doc per repeat, so the cheap model is what makes running it to clean affordable.

Every subagent has the same three jobs for its doc:

1. **Follow it.** Do what the doc says, using only what is written down. Note every step that fails or turns out to be missing.
2. **Fact-check it.** Read the doc claim by claim and check each claim against the source: the code, the configuration, the pipeline definitions, and the repository settings. A doc can read perfectly and still be wrong.
3. **Check it will still be true next month.** Report every passage that is a snapshot of today's code rather than an instruction to a contributor: counts, catalogues of what individual files contain, and notes on what is currently missing or empty.

Per doc, that means:

- `README.md`: set up the environment, install dependencies, build, run the project, and run the tests, from the top. Check documented versions, environment variables, and dependencies against the lockfiles and config. Trigger a failure mode from the Debugging section and confirm the documented fix resolves it.
- `CONTRIBUTING.md`: walk the path a change would take. Create a branch using the documented naming and run locally every check the pipeline runs. Then check the documented process against the real pipeline definitions, branch protection rules, required checks, and code owners.
- `docs/PRODUCT.md`: code cannot confirm intent, so check this one for consistency instead. Report every place another doc contradicts a decision recorded here, every scope boundary the architecture crosses, and anything written as settled that reads like a guess.
- `docs/CODING-RULES.md`: check each rule twice, first for whether it belongs and then for whether it is true. Report as a finding any rule a linter already enforces, and any tooling or workflow instruction. Then check the rules that survive against real files in the codebase. A rule the codebase itself breaks is a caveat to note or a rule to remove.
- `docs/ARCHITECTURE.md`: read the doc, then check its claims in the source. Trace every component, entrypoint, and diagram element back to real code. Confirm the described responsibilities and interactions are what the code actually does. Names in diagrams must match names in the code.
- `docs/TESTING.md`: run every documented command, the whole-suite and single-test ones alike, and confirm each layer sits where the doc says it does. Then take a small change and clear the documented completeness bar with it, writing each test the bar calls for. Report as a finding any passage explaining how to write a test or how the test framework works, since neither belongs here.

On a new project the swarm verifies against what was actually built, which is the reason the walking skeleton matters: without it, a subagent has nothing to follow. Give every subagent two extra checks. First, that each forward-looking statement is labelled as intent rather than stated as fact. Second, that no doc records a decision the user never made. An invented decision reads exactly like a real one, and only the user can tell them apart.

Subagents verify and report; they do not fix. Instruct each one to return a structured list of findings: the step or claim that failed, what the doc says, and what is actually true. Every finding comes back to you, the main agent, to resolve:

- If the repository makes the fix clear, fix the doc, not just the immediate problem.
- If the fix needs a decision or knowledge you cannot verify, interview the user and record their answer. Subagents cannot talk to the user; escalating is your job, not theirs.

After fixing, launch a fresh subagent on the same model to re-verify each doc that changed. Repeat until the whole swarm comes back clean.

If a step cannot be verified, for example because it needs credentials or access you don't have, mark it as unverified in the doc and tell the user. An unverified step that is labelled honestly is fine; a wrong step recorded as fact misleads everyone who follows.

## Keeping the docs alive

Onboarding docs rot quickly, and a stale doc misleads worse than a missing one. Add a rule to `CONTRIBUTING.md`: when a change invalidates any of these docs, updating them is part of that change, not a follow-up. Suggest making it a pull request checklist item so reviewers enforce it.

A new project's docs need thickening as well as correcting. The architecture written on day one is a sketch, and the testing doc names layers that barely exist yet. Agree a point with the user to revisit both, such as the first release or the end of the first month, and record it in `CONTRIBUTING.md` next to the rule above.

## When you cannot find what you're looking for

- Do not guess, and do not assume. A wrong answer written into these files misleads every developer and agent that reads them later, which is worse than a gap.
- Verify your findings with the user before recording them. What you inferred from the code is a hypothesis, not a fact.
- If you truly cannot find anything, interview the user. Ask the questions an outside developer would typically ask to get up and running on each section.

On a new project this is the normal case rather than the exception, and the questions are different. Ask what the product is for, who uses it, what is out of scope, which constraints are already fixed (a platform, a deadline, a technology the team must use), and where the user already holds an opinion. Ask those before asking anything about code.

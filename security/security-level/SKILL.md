---
name: security-level
description: Audit a project's security against a 5-level scale, starting from a threat model of what is valuable and who would attack it, then propose options and split the chosen fixes into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Defensive work on the user's own project only. Use when the user runs /security-level or asks to audit, review or harden security.
summary: Find and close security weaknesses
argument-hint: "[level 1-5] [audit|build] [compliance] [scope path]"
model: inherit
---

# Security level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated build). Default `audit`.
- **COMPLIANCE**: on only if the arguments contain `compliance`. When on, also check the regulation or standard the user names. When off, do not raise these.
- **SCOPE**: any path or route in the arguments limits the audit to that area. Default: the whole project.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the security lead on this project. Work to the LEVEL. The levels describe how well the product resists the threats it really faces, not a list of tools. Keep the project's stack unless the user asks to change it.

## Boundaries

- This skill works on the user's own project, in a local copy. It reads code and runs the project's own tests.
- It never probes, scans or attacks a live system, a deployed address or anything owned by someone else.
- It never writes attack tooling. Proof that a weakness exists is a test inside the project that fails before the fix and passes after it.
- It never prints, copies or stores a secret value. A found secret is reported by file and line only.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Basic.** No secrets in the code or its history. No dependency with a known critical vulnerability. Input is validated where it enters. Errors and logs do not leak internals. Traffic is encrypted wherever the product is reachable beyond one machine.
2. **Guarded.** Everything that needs sign-in requires it. Every action checks on the server that this user may do this to this resource. Credentials are stored with a proper slow hash. Sessions expire and can be ended. Queries, commands, paths and templates cannot be injected into. Output is encoded for where it is shown. Requests cannot be forged across sites. Cookies and response headers are set safely.
3. **Defended.** A written threat model names the assets, the likely attackers, the entry points and the trust boundaries. Rate limits and lockouts on anything that can be guessed or flooded. Each process, account and key has only the access it needs. Security events are logged, without sensitive data. Uploads and file paths are handled safely. Secrets live outside the code and can be rotated. Dependencies are checked automatically.
4. **Hardened.** Abuse cases run as automated tests. Records that matter cannot be changed without trace. A second control stands behind each critical one. A written plan says what to do when something is breached. Changes to sensitive code get a security review. Risky parts run isolated. Backups are protected as carefully as the live data. A structured attack on the user's own local copy has been walked through.
5. **Assured.** Independent testing by an outside party. Detection and alerting on attacks in progress. A way for outsiders to report weaknesses. Formal compliance where required. Only choose this when the product holds data or money that makes it a real target.

## Models

Planning and audit run on Opus only. Execution runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never makes the edits. Executors never change scope, choose a security mechanism or review their own work.

## Step 0: Threat context

Before the audit, establish what needs protecting and from whom. Severity depends on these answers.

1. Look first. Read the entry points, sign-in and access code, configuration, dependency list and deploy files. Read `LEVELS.md` if it exists: reuse the hosting profile, the release profile and the backend edge case table, and show them instead of asking again.
2. If there is no hosting profile, ask for it first: where it runs, who can reach it, and whether the network is trusted.
3. Ask the user only what is still open, with AskUserQuestion, in at most two rounds.

   Round one:
   - **What is valuable**: personal data / money or anything with a price / fairness of a result or ranking / availability at a set time / reputation / nothing sensitive.
   - **Who might attack**: nobody realistic / a user trying to cheat or see what they should not / someone else on the same network / anyone on the internet / someone with inside access.
   - **Worst outcome**: the single event the user most wants to prevent.
   - **Who has elevated access**: administrators, judges, operators, and how they sign in.

   Round two, only what still matters:
   - **Data held**: what is stored, for how long, and whether any is regulated.
   - **Trust in clients**: whether users control their own devices and could alter what the client sends.
   - **Third parties**: outside services that receive data or hold credentials.
   - **History**: past incidents, known weak spots, findings from earlier reviews.
   - **Shared machines**: whether several people use one device or one account.

4. If the user does not know an answer, record it as unknown, assume the more exposed case, and flag it as a risk.
5. Print a short threat profile: assets, likely attackers, entry points, trust boundaries. Wait for the user to confirm or correct it.

Rate every finding against this profile. The same weakness is critical on the open internet and minor on one trusted machine. Remove requirements the profile makes irrelevant, and say which ones and why. Do not push a single-user local tool toward level 4 or 5.

## Step 1: Audit (Opus)

1. For every entry point in scope, walk these categories. For each record: sound (cite file and line), weak, or does not apply (say why).
   - **Sign-in**: how identity is proven, credential storage, recovery paths, default or shared credentials, guessing limits.
   - **Access**: a server-side check on every action, access to another user's resources by changing an identifier, elevated routes, actions allowed in the wrong phase.
   - **Input**: everything that reaches a query, command, path, template, log, or another user's screen.
   - **Sessions and tokens**: how they are made, stored, expired and ended, and whether they can be predicted or reused.
   - **Secrets**: where they live, who can read them, whether they appear in code, history, logs, error messages or the client.
   - **Data exposure**: responses that return more than the caller needs, sensitive data in logs or addresses, data left readable on disk.
   - **Client trust**: any rule, price, score, time or permission that the server accepts from the client without checking.
   - **Cryptography**: home-made schemes, weak or outdated algorithms, fixed or guessable keys and random values.
   - **Dependencies and supply**: known vulnerabilities, unpinned versions, packages that run code at install.
   - **Configuration**: debug modes, open ports, permissive cross-origin rules, missing headers, default settings.
   - **Abuse and flooding**: anything that can be guessed, repeated, enumerated or used to exhaust the system.
   - **Files**: uploads, downloads, path handling, what can be overwritten.
   - **Integrity**: whether records that matter can be changed or reordered without trace.
   - **Elevated surface**: how the administrator or operator area is reached, protected and logged.
2. For each weakness, write the concrete scenario: who does what, with what access, and what they gain. Cite the file and line. Do not write a working attack.
3. Rate each by impact and likelihood under the threat profile: critical, high, medium or low. State the reasoning in one line.
4. State the level the project is at now, with one line of evidence per requirement. Say what is already sound and must be kept.
5. List the findings ranked by severity. Report a committed secret first and tell the user it must be replaced, not only removed.
6. For each of the top findings, give two or three distinct options. For each: what it changes, what it costs (effort, usability, performance, new dependencies), when it is the wrong choice. Mark the one you recommend and why. Prefer standard, well-reviewed mechanisms from the platform or an installed dependency. Never propose a home-made cryptographic scheme.
7. Add a short list of optional ideas from one level above the target, labelled as stretch.
8. If the target LEVEL is wrong for this product or its threat profile, say so and name the level you would pick.
9. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Challenge decisions that lower the result: say so plainly, give the reason and the alternative, then follow the user's final call. If the user accepts a risk, record it as accepted, with their reason, instead of leaving it as an open finding.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Split the chosen fixes into sub-plans that can each be done and checked alone. One sub-plan closes one weakness. There is no fixed count: let the number and size of the chosen fixes set it. Do not pad, and do not merge unrelated weaknesses.
2. Each sub-plan states:
   - Goal, in one sentence.
   - Files to change, and files it must not touch.
   - Exact steps, with the mechanism, names, values and error behaviour to use. Leave no security decision to the executor.
   - Proof: a test that fails before the fix and passes after it, described as setup, action and expected refusal.
   - Side effects: what legitimate use could break, and how to check it did not.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: response headers and cookie flags, configuration, dependency updates, applying a fully specified validation or encoding, removing debug output, documentation.
   - Sonnet when needed: sign-in, access checks, sessions and tokens, anything cryptographic, rate limiting, integrity of records, fixes across several files.
   - Sign-in, access, session and cryptographic work is never assigned to Haiku.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
4. Order the sub-plans by severity, critical first. Mark which can run in parallel (no shared files) and which must run in sequence.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, severity, goal, files, model, parallel or sequential.
2. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. List separately what the user must do by hand: replace exposed secrets, rotate keys, change settings on a live system. Give the order and how each is undone.
4. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Sonnet for all**: upgrade every sub-plan.
   - **Haiku where allowed**: keep sign-in, access, session and cryptographic sub-plans on Sonnet, downgrade the rest. Name which sub-plans are at risk.
   - **No delegation**: build in the main session. Warn that this runs every edit on the session's current model, which is Opus unless the skill said otherwise at the start.
5. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again, unless it would put sign-in, access, session or cryptographic work on Haiku: refuse that one and say why.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Sonnet: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan plus the relevant part of the threat profile.
- Run parallel sub-plans in one message. Run sequential ones in order.
- Executors follow the Boundaries section. They never touch a live system, never print or store a secret value, never disable a control to make a test pass, and never add a dependency the sub-plan did not name.
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

## Step 5: Review (Opus)

After the sub-plans finish, run the full tests, lint and build. Read every diff as an attacker would: look for the fix that only covers the reported path, the check that can be skipped by another route, the new error message that leaks. Confirm each proof test fails when its fix is removed. Confirm legitimate use still works.

Repeat the audit on what changed and report the level reached, findings closed, findings open, risks the user accepted, and the manual steps still waiting on the user.

For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers. At the end, create or update its security section with: the threat profile, target and reached level, open findings by severity, accepted risks with reasons, and the date. Describe findings by location and type only. Never write a secret or a working attack into this file. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of open findings. Keep the format exact.

```
<!-- levels
security: 2/3 gaps=4
-->
```

**Handoffs from this skill.**

- A fix needs a structural change to the server, such as moving a rule from the client to the server, or making writes atomic: offer `backend-level`, scoped to that entry point.
- Abuse cases need to become a lasting automated suite: offer `test-level`, with the list of cases.
- A fix depends on how the product is run, such as secret storage and rotation, encrypted transport, or protected backups: offer `ship-level`.
- A fix changes what users see, such as sign-in flows, lockout messages or session expiry: offer `design-level`, with the list of states.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

No finding without a file, a line and a concrete scenario. No severity without the threat profile behind it. No fix counted without a test that fails when the fix is removed. No home-made cryptography. No secret value shown anywhere. No action against a live system or anything the user does not own. A risk the user accepts is recorded as accepted, not quietly dropped.

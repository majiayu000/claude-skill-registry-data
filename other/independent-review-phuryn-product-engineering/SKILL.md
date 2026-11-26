---
name: independent-review
description: "Before 'ship it', a deploy or release, for 'an independent review', and after each fix until a round is clean: a fresh reviewer that never saw the build."
---

# Independent review — the gate before a change ships

**The session that wrote the code never clears it.** A fresh reviewer that never saw the build reads the change for what would block or break it. That separation applies at every size: a one-line fix that ships gets a short round, never no round. Inside a phase, it joins the phase's series (§ When).

## Reviewer selection and isolation

**The tool is optional; the review is not.** By default, the wrapper chooses the first installed of Codex, headless Claude Code and Grok. Run `python <skill dir>/scripts/review.py --check` to see which.

**A fresh session of the builder's own model is independent: it never saw the build.** It shares more blind spots than another family would. Accept that cost: a round that runs beats one skipped.

**The repository's own instructions come first.** Follow its agent instructions or release docs for reviewer, fallback, review bar, required moments and release range. They may also name the test gate and where deferred findings go.

**A repository ranks its reviewers; it cannot rule out a review.** When a named reviewer cannot meet the isolation bar, open `references/reviewer-clis.md`.

**Apply one bar to every reviewer, including a repository's named reviewer.** Require a fresh session that never saw the build, never a resume, fork or subagent of it: the reviewer must not inherit the builder's beliefs. Use read-only tools only, no MCP servers or connectors, memory off, and high effort or above. Switch off project and user instructions where the CLI allows. Name everything that cannot be switched off in the round's report.

A sandbox flag alone is insufficient. The wrapper prints what still loads. For each CLI's controls, observed limitations and manual setup, read `references/reviewer-clis.md`.

Where repository instructions say nothing, use these defaults. Ask when a default needs an owner-only fact, such as the released branch or last release.

**Verify findings yourself, and after every fix rerun the tests it touches yourself.** Check each finding against the code, including its severity and how often its trigger happens (§ Triage). Fix what the bar names and run each fix's regression test and the tests it touches. Get a fresh round on the changed state until the bar holds.

**Treat findings and their severity labels as claims, not results.** Triage below is mandatory; it is the part that most often goes wrong.

## When

- **Review before every release, however green the tests are.** A release without an independent pass is not a release.
- **Review before every push to a branch that deploys.** When users receive the push, "just push it" requires a round first. The push closes the round (§ Keep the subject still).
- Before the first push, open `references/subject-scope.md` to check the destination.
- **Review again after fixing anything a round found.** A fix is unreviewed code, and fixes produce the worst defects. Never report readiness from a round you fixed anything after, however small or confident the fix.
- **Review the completed phase; test each stage as it lands.** A phase is the review unit: related stages ending in one state the owner can try.
- When planning phase size and review cadence before building, open `references/subject-scope.md`.
- **Run phase reviews after the coordinator's gate, visual and docs checks.** Apply `release-gate` § Stage and phase close for stage checks, the ordered phase checks, closing push and owner preview. A stage's optional advisory round clears nothing.
- **Run the full applicable gate before reviewing a finished standalone change.** Rerun it on the cleared phase or standalone change if a fix followed its last full run, before pushing or calling it done. If that gate fails, its fix gets a fresh round. A gate of a couple of minutes can run after every fix.

## The subject: computed from git, and it narrows after round 1

**Compute the subject from git, covering the whole phase or unreleased range.** A prose description can leave an unapplied migration or untracked file unreviewed. A phase's first round starts at the last commit a round cleared, or at the work's first commit when none has. It takes everything from there, plus the working tree. Before a release, round 1 takes everything unreleased, committed or not: last release to `HEAD`, plus the working tree.

Before a first release, or when a clone or fork's history began elsewhere, open `references/subject-scope.md`.

```bash
git log --oneline $RELEASED..HEAD               # the unreleased commits
git diff $RELEASED...HEAD --stat                # its shape
git status --porcelain -uall                    # and anything uncommitted, file by file
```

**Read that status for what does not belong, too.**

When `git status` lists untracked files or the subject looks larger than the diff, open `references/subject-scope.md`.

**Use the repository's last released state as `$RELEASED`.** It may be production branch `origin/<prod>`, a release tag or the deployed commit.

**Never narrow the range by hand to make it fit.** A release's first round includes already-pushed code: when pushes deploy, that code is exactly what users run.

When a range is too large for one round, open `references/subject-scope.md` to split it.

**Narrow every later round to commits since the previous round.** Give the remaining unreleased range as context to read for interactions. Naming new code is scoping, not steering. Re-reviewing cleared code adds time and pre-existing noise while burying new findings. Passes find bugs, so cheap rounds beat thorough ones.

**Bring old code into scope only where the change makes it newly reachable or newly wrong.** Say this explicitly in the brief; interactions hold serious findings. Keep both kinds of pass: a whole-range review sees composition that per-commit rounds cannot.

When the coordinator has suspected defects or running triage notes, open `references/subject-scope.md` before including them.

**Scope the subject by what a reviewer must read, not by file count, and keep generated prose out of it.** When generated docs are in the range, open `references/subject-scope.md`.

## Running it

**Use the wrapper to apply review flags and reject short failed rounds.** It picks the reviewer and fails loudly when output is too short to show a round ran:

```bash
S="<a scratch directory>"
python <skill dir>/scripts/review.py \
     --brief "$S/review-NNN-brief.md" --cwd <repo> \
     --subject "<range>" --out "$S/review-NNN.md" < /dev/null
echo "exit=$?"   # 2: failed round (length or Codex event checks); 3: the reviewer is out of usage
```

With `--out`, Codex also saves `<out>.events.jsonl`, recording what the reviewer read and ran; treat it like the report and never commit it.

`--subject` takes a git range, `<sha>^!` for one commit or `HEAD` before the first release. The wrapper refuses an empty subject, a range without a start, or one with no commits and a clean tree. Keep the brief, report and events outside the repository. The wrapper writes the range's log, diffs and working tree, including untracked files, into the git directory for the reviewer.

When a range contains a merge or code it added and later removed, or a path falls outside the change, open `references/subject-scope.md`.

**Use the repository's runnable fallback when the default reviewer cannot run.**

On exit 3, when the default reviewer cannot run, or when none of the three CLIs is installed, open `references/reviewer-clis.md`.

**Check what the reviewer actually read before accepting any round.** Open the report and saved read evidence. Apply `references/reviewer-clis.md` when a reviewer needs manual setup or a round fails at the CLI.

- **A short clean round is a failed round.** A genuinely empty round argues its way there over paragraphs. Require it to say what it read, what it expected to find and why it holds. The wrapper fails output under 1,500 characters with exit 2; measure a manual round the same way. Accept a shorter round by hand only when its saved events (`--out`) show commands that printed the subject's content and the report names what it read.
- **A round whose reviewer couldn't read is failed however long it is.** Refused reads, such as "blocked by policy", without any successful reads mean nothing was reviewed. So does an answer saying it could not open the files. A refused write is different: the read-only sandbox is doing its job. For Codex, the wrapper fails a round with no successful command and lists failed commands for you to judge. Check the same evidence in a manual run; opening, listing and searching files are reads.
- **A round takes minutes at a high effort.** Run it in the background.

If a round exits with a short answer or runs out of room, open `references/reviewer-clis.md` to diagnose it.

## Keep the subject still

**Review in a still checkout for the length of the round.** Use the current checkout for serial review and keep it still throughout. For a phase or advisory stage round that overlaps another build, follow `references/overlapping-phases.md`. It isolates the exact snapshot, preserves the full gate and release go, and protects linked dependencies when removing the worktree.

**Commit means "reviewed from here". Push means "this round is closed".** Local history is working state; a deploying branch receives only the state a closing series cleared. Advisory stage rounds clear nothing; before hosting, a phase can remain local. A production push remains a release and requires the owner's go.

When a push can apply migrations or publish through an integration or hook, open `references/subject-scope.md` before pushing.

**the whole-range round before a release still runs against a still tree.**

When planning a whole-range release round while another build is running, open `references/overlapping-phases.md`.

## Writing the brief

**Write only these five parts, in this order, to avoid steering.**

1. Say what the product is in two sentences. Name its binding spec files, such as agent instructions and architecture docs. Explain how its pieces fit: trust boundaries, ownership and where writes go. A diff alone cannot show interactions.
2. Paste the subject from the git commands above, naming the earlier range as context.
3. Give the usage model: who uses which surface, how many and at what moment. State what stays serious however exotic the trigger. For most products: another tenant's data, private data on a public surface, lost or duplicated writes, anonymous access to a member capability. State what does not block, such as cosmetic divergence the next refresh fixes. When information is hidden from users, explain from whom, why, what honest users might expose accidentally, and what requires deliberately defeating their own measurement (§ Triage).
4. Ask what would block or break this release. Label every finding INTRODUCED or PRE-EXISTING. Require the literal triggering sequence and who performs it. A finding unable to name its trigger usually has none; requiring it exposes over-claiming before a fix is briefed.
5. Request a numbered list: claim, `file:line` evidence, what to change. Keep it terse, without praise, ranked. End with those most likely to bite.

Do not include earlier findings, suspected files, your argument for the design, or a request for approval. A reviewer asked whether it approves will tell you it approves.

## Triage — the part that goes wrong

**Question zero, before any other: say in ONE SENTENCE what actually goes wrong for the person.** If it does not sound bad read aloud, there is nothing to fix. "You land on one of your own items that a filter was hiding" dies unaided. The reviewer's severity label is part of its claim, and taking one at face value is how a clean release grows two invented P1s.

**Weigh how often a finding happens before fixing it, and prefer a simpler assumption.** A reviewer reports what the code permits, not what people hit, and its severity is a claim like the rest; check both, whichever model it is. A failure seen in real use outranks a finding read out of code. A trigger that needs two uncommon conditions at once is Low unless it crosses a line below. When a fix would add machinery for a case almost nobody meets and no such line is crossed, state the limit, drop the case or refuse it with a clear message instead, and tell the owner. A system most people can understand beats one that serves every case.

**A trigger that needs a rare precondition is Low.** The usual ones:

- two people, apps or views of one app acting on the same work at once;
- a system or environment failure, at the instant of an act or lasting;
- two acts within the same second;
- the person removing what running work stands on, such as deleting or restarting it mid-run;
- state that only an unreleased build could have written;
- a device or width the product does not support.

The exception is crossing one of the lines below, such as lost work or an irreversible external write the person did not approve or had stopped. A stated limit is safe when the case stops loudly, with a refusal or a state the person can see and repair, and never produces a wrong result silently. Refusing at the door while the work runs is often the cheapest. Write each limit where the product keeps its assumptions, so a later round's report of the same case is matched against it rather than fixed.

**Record each finding's harm, who hits it and how often, and the line it crosses.** Write one sentence for each before the verdict, which follows from them; the reviewer's label is one more claim. Judge them by the usage model the brief gave the reviewer (§ Writing the brief). A finding a later round reports again keeps its recorded verdict unless new evidence changes it. A principle with no place to write it down gets skipped under time pressure.

**does anything cross a line the person cares about?** Examples are another tenant's data, private data on a public surface, another user's private content, disappearing work, lost writes, an irreversible external write the person did not approve or had stopped, or anonymous access to a member capability. If everything already belongs to the person and stays visible, it is a surprise; a surprise is polish. Distrust a real mechanism with a scary label and speculative harm. Ask whether the person can see where they are. Builder reports and reviewer priorities are both claims; neither model decides.

**Require literal steps, permitted execution and a person with a reason.** A finding that cannot answer these three questions is not a finding:

1. **What exact sequence produces it?** Not "an attacker could": literal steps in order.
2. **Does this system permit that sequence?** Check the code that must allow it. This is where most die.
3. **Who does it, and why?** If it needs someone already holding the owner's session on the owner's own screen, they had the screen.

For layout or performance claims, or clustered findings, open `references/triage-cases.md`.

**Rank by what it costs this product, not by where it sits in the list.** Read user and business impact: who sees it, how many and at what moment. A widely seen instruction failing at a critical moment can cost more than its mechanism suggests. A recoverable flow one admin meets once can cost less than its label.

When deciding whether to accept a confirmed finding or add machinery to fix it, open `references/triage-cases.md`.

**A fix that did not need to happen is itself a defect.** Weigh branches, permanent complexity and new review surface against the occasional actual harm. Run the fix's regression test on the tree before the fix. If it passes, the finding was false: revert the fix and keep the assertion. Apply `test-harness` for that rule.

When fixes interact, findings recur, or a repair records who decided, open `references/triage-cases.md`. It also covers rare cases, attacker assumptions, hidden information and polish.

**Say it plainly when a round is empty after triage.** "Three findings, none survive the usage model" is a result, expected on a well-built change.

**Read a clean round's argument, not only its verdict.** Code cited to prove safety can expose the same defect one surface over.

When a repair changes user-facing copy, shared doc claims or what the platform decides, open `references/triage-cases.md`.

## The stopping rule

**Stop at no INTRODUCED finding above Low and no High or Critical of any age.** A finding's level is the one Triage gives it, not the reviewer's label. Fix High and Critical now, regardless of age. Small releases reach that bar fastest; later releases review only their own commits.

**A Low goes to the owner's list, not into the loop.** An introduced Low needs no fix and opens no round. Record it with its round number where pre-existing findings are recorded, and name it in the summary to the owner. Fix one only in a batch that already needs another round, or when the owner asks. Any fix is new code and gets a round.

If one mechanism draws findings two rounds running, open `references/triage-cases.md` before fixing it again.

When planning work in ingest, queue or concurrency code, open `references/triage-cases.md`.

**Record pre-existing findings with their deferral reason and a revisit trigger.** Include the trigger because it is what gets the finding fixed. Use the repository's backlog file or issue tracker; ask if it names none. High and Critical are the exception: fix them now, regardless of age. Never silently drop a finding. The release summary states each round's finding count and what happened to each, including those not worth fixing and why.

**Number rounds in one sequence per repository.** Cite the number wherever the outcome lands: fix commit, backlog row, merge and release record.

**Verify every finding against code by hand before acting.** Cited line numbers are claims too, and so is the INTRODUCED label: check it against the released text (`git show <release>:<file>`). Rerun the tests the fix touches yourself after every fix; "it says it passes" is a claim, never a result. Record disproved findings as wrong beside confirmed ones, making the next round's hit rate legible.

Each rule's origin, the case that taught it, is in `receipts.md` beside this file; read it when a rule's edge is unclear.

## How you can tell it worked

The last round came from a fresh reviewer given only the mechanical range and found no introduced finding above Low, with nothing fixed after it. No High or Critical of any age is open; every earlier finding was checked against code before being fixed or dismissed, and accepted Lows are recorded.

## Not this skill

For a design discussion, a delegated task or a code correctness review, open `references/reviewer-clis.md` § Related work.

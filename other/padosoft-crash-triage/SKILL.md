---
name: padosoft-crash-triage
description: >-
  Use this skill when a crash, a freeze or an error from real users has to be turned into a fix — a report
  from a crash reporter, an application-not-responding event with a thread dump, a stack trace from a
  minified or bundled artifact, an exception group in an error tracker. Also when the user says an issue is
  back, asks which release introduced it, wants a stack symbolicated, or asks what to write in the fix when
  nothing could be reproduced. It gives the order of collection, how to attribute a frame honestly, how to
  classify from the code rather than the message, and the grade of proof every sentence in the diagnosis
  has to carry. Do not use it for a failing test or a red pipeline (padosoft-ci-failure-triage) or for a bug
  you can reproduce in front of you.
license: MIT
compatibility: >-
  Any application shipped to users with a crash or error reporter. The symbolication and thread-dump
  sections are written for a bundled mobile application, where they bite hardest; the discipline applies to
  a minified web bundle and a server stack trace equally.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: Never write a claim stronger than the evidence you actually have.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: crash, anr, stack trace, symbolication, triage, production, diagnosis, evidence, regression
---

# Crash triage

A crash report is somebody else's failure, on a device you do not have, in a build you cannot attach to. The
work is not finding a plausible cause — plausible causes are cheap. It is **separating what you know from
what you inferred**, and writing the difference down.

**The rule: never write a claim stronger than the evidence you actually have. A diagnosis that is right in
substance and overstated in wording gets corrected in review, and costs more than the original bug.**

---

## 1. Collect the report before interpreting it

Copy out, verbatim:

- **Version and build number**, device, operating-system version, timestamp.
- **Fatal or not.** An error caught by a boundary and one that escaped everything are different events, and
  the same underlying fault often appears as both.
- **Every custom key** the application publishes — the current route, mount counts, session age, feature
  flags, whether the user was authenticated.
- **The breadcrumbs with their timestamps.** A cycle of crash → retry → crash, and how many in how long, is
  evidence about determinism that nothing else gives you.
- **The full stack, with line *and* column.**

**An issue with many variants across several builds is a bucket, not a defect.** Reporters group by a
signature that is coarser than the cause. Pick one event and work on that one; a "fix" for a bucket is a fix
for whichever variant you happened to read.

## 2. Does the build already contain the fix?

```bash
git merge-base --is-ancestor <fix-sha> <build-sha> && echo "already in the build"
git show <build-sha>:<path> | grep -n "<fragment>"      # did this line exist then?
```

- **Already in** → this is **not** a recurrence. Either the fix is incomplete, or it is a different class.
  Say which, and do not reopen the old issue.
- **Not in** → it may already be fixed on the mainline. Check before writing new code.
- **A record that comes from an operating-system history** rather than from a live capture carries the
  version of whoever *read* it, not of whoever crashed. Look for the age field.

## 3. Attribute the frame, and measure the uncertainty

The artifact that shipped is usually not available, so you rebuild it at the build's commit. **A rebuilt
artifact is not the shipped one until it is byte-identical.**

1. Rebuild at that commit, with the same toolchain versions.
2. **Measure the offset against anchors inside the same module**: pick a string or token sequence unique to
   the module, find it in the rebuild, compare the line with the report. Use **several nearby anchors** —
   the offset is not constant across the whole artifact.
3. **Use the column** to choose between candidates on the same line, and the number of frames between two
   known markers to distinguish one call path from another.
4. Write it as: *"attributed to `file:line`, on a rebuilt artifact with a measured offset of N lines"*.
   Never "exact" without byte-identity.

## 4. Reading a thread dump

A dump is taken **after** the timeout fired, by a mechanism that suspends threads in order to print them.
Most of what is in it is the dump's own footprint.

- **A native-to-managed transition frame waiting on a condition variable, with no application frame above
  it, is not a contested lock.** It is what any thread inside a foreign-function call looks like while being
  suspended for printing. A deadlock is claimed only when one thread **waits for what another holds**, with
  both frames present.
- **Read every thread, not the first.** The only real work photographed is usually a runnable thread with
  application frames on top.
- **The blocking operation may have finished between the timeout and the dump.** A normal-looking main
  thread does not exclude the block, and a suspicious frame does not prove it.
- **Ask for the reason string** and the number of events and devices. The category of timeout narrows the
  cause more than the stack does.
- **Garbage-collection daemons appearing during a dump** are participating in the dump, not evidence of a
  long pause.
- **Custom keys are frozen at the last moment the application published them.** A short session age against
  an event much later means nothing ran after that point — the application was idle, or its main loop was
  already stuck.
- **The threads that are absent are evidence too.** No thread waiting on a given lock, plus no use of the
  synchronous bridge in the codebase, excludes that contention for this event.

## 5. Classify from the code, not from the message

Keep a table of the classes this application actually produces: the signature to look for **in the source**,
where to look, and the guard that detects it. Match the report to a row by finding the signature, not by
matching the error text — the same message comes from several causes and the useful distinction is the one
in your code.

**No row matches → it is a new class.** Understand it and propose a new row. Forcing a report into an
existing class is how a table stops being useful.

## 6. Verify every fact about somebody else's code

- **Upstream state**: query the API for the pull request and the issue. Then check whether the merge is
  contained in the **version you have installed**, not merely merged. "Open upstream" and "unresolved" are
  claims with a command behind them.
- **Any switch you describe** — a breaker, a guard, a limit — is read in the installed source, **with the
  conditions and the effect dependencies**. "It never arms" is a statement about code you have read.
- **The installed version** comes from the package that uses it; in a workspace, two versions coexist.

## 7. Degradation before cause

Before the fix: does the failing area have an error boundary? If not, that is the first change. It turns a
crash into a recoverable state, and — with a distinct context per subtree — it makes the next report name
the area instead of the root.

And know what the retry does: if it remounts the same tree, a deterministic fault restarts immediately,
which is exactly the cycle visible in the breadcrumbs.

## 8. Write the diagnosis with a grade on every claim

| Grade | Wording | When |
|---|---|---|
| **Verified** | "is", "verified on…" | code read, test run, API queried, reproduced |
| **Attributed** | "attributed to…, offset N lines" | symbolication on a rebuilt artifact |
| **Suspected** | "suspected", "precondition" | configuration compatible with the symptom, no reproduction |
| **Not verified** | "not verified: …" | hypothesis, behaviour never observed |

Then run the word check over your own text. Each of these needs its proof, or gets rewritten:

> **exact · infinite · never · always · open upstream · unresolved · deterministic · the cause is**

A fix that removes a suspected precondition without a reproduction says **"removes the suspected
precondition"**, not "fixes it". And close with **what remains to be verified**, on a device, in the next
release, by whom.

---

## Gotchas

- **A cause you can tell a story about is not a cause you can show.** The story is the most dangerous
  artefact in the whole process, because it is persuasive and free.
- **The report's version field can belong to the reader**, not to the crash, when the record was replayed
  from a system history.
- **Two reports with the same top frame are frequently two defects**, and the reporter's grouping will not
  tell you.
- **A fix shipped in a build you cannot check is not shipped.** Verify containment, not the merge.
- **Reproducing it once does not make it deterministic**, and the breadcrumbs usually say which it is.
- **A fix across several open branches** needs them merged locally and the touched suites re-run before you
  can write "no conflict".

## Checklist

- [ ] Report copied verbatim: version, build, device, fatal flag, custom keys, breadcrumbs, full stack
- [ ] One event chosen out of the bucket
- [ ] Containment of the candidate fix in the crashing build checked by ancestry
- [ ] Symbolication offset measured on several anchors; column used; wording says "attributed", not "exact"
- [ ] Thread dump: every thread read, dump footprint discounted, reason string requested
- [ ] Classified from a code signature; a new class proposed rather than forced
- [ ] Every upstream and library claim backed by a command
- [ ] Error boundary present, or added first
- [ ] Every sentence graded; the word check run over the text
- [ ] What remains unverified stated explicitly

## Final report

```
Event: <id> · version <…> build <…> · device <…> · fatal: yes|no
Bucket: <n> variants → working on <which>
Already in the build: <fix sha> → yes | no (so: incomplete | other class | new)
Attribution: <file>:<line> — rebuilt artifact, offset <n> lines, anchors <n>
Class: <row> | NEW: <proposed row>
Library facts: <claim> ← <command and result>
Degradation: boundary present | added
Diagnosis grades: verified <…> · attributed <…> · suspected <…> · not verified <…>
To verify on a device: <…>
```

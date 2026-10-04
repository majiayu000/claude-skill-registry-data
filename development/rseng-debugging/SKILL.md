---
name: rseng-debugging
description: >-
  Covers systematic debugging of research software: hypothesis-driven
  diagnosis instead of guess-and-change, building minimal reproducers,
  bisecting across commits, data and parameters, debugging scientific failure
  modes (wrong numbers rather than crashes, nondeterminism, scale-dependent
  bugs), debugger and print-discipline mechanics, and turning every fix into a
  regression test. Use when the user reports a bug, a crash, wrong or changed
  results, a heisenbug or an it-works-on-my-machine discrepancy, when a
  pipeline fails at scale but not in tests, or when the user is stuck guessing
  instead of diagnosing. For preventing silent wrong-result bugs see
  rseng-defensive-coding; for judging whether numerical differences matter see
  rseng-numerical-accuracy.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Debugging research software

Debugging is applied science: observe, hypothesize, run the
decisive experiment, repeat. The anti-pattern is its opposite -
changing code until the symptom moves. Research adds two hard
twists: the worst bugs produce plausible wrong numbers instead of
crashes (rseng-defensive-coding exists to make them crash), and the
oracle problem - when the right answer is unknown, "wrong" itself
needs evidence. The discipline below is tool-agnostic; the
debuggers change, the method does not.

## The loop

1. Reproduce first: a bug you cannot reproduce on demand cannot be
   diagnosed, only feared. Pin the environment
   (rseng-reproducible-environments), the data version
   (rseng-data-management), the seed (rseng-defensive-coding) and the
   exact command; record them in the issue
   (rseng-version-control-review).
2. Minimize: shrink input, code path and configuration until the
   smallest thing that still fails remains - minimization IS
   diagnosis (each removal that keeps the bug excludes a
   hypothesis), and the minimal reproducer becomes the regression
   test and, for dependency bugs, the upstream report.
3. Hypothesize before touching: state what would explain the
   evidence, predict what an experiment will show, THEN run it.
   One variable per experiment; write the trail down when the hunt
   exceeds a few steps (the notes are tomorrow's context and the
   postmortem's material).
4. Localize by bisection - the log-time weapon on three axes:
   commits (git bisect with the reproducer as the test, ideally
   scripted with `git bisect run`), data (which half of the input
   triggers it), and pipeline stages (diff intermediates against
   a known-good run - rseng-workflows' cached stages make this
   cheap).
5. Fix the cause, not the symptom, and prove it: the reproducer
   passes, the regression test is committed (rseng-testing), and
   the fix commit explains the WHY (rseng-version-control-review).

## Scientific failure modes

- Wrong numbers, no crash: establish ground truth from analytic
  cases, conservation laws, invariants or a reference
  implementation (rseng-open-source-migration's parity discipline);
  then bisect the pipeline to the first stage whose intermediate
  diverges (rseng-numerical-accuracy decides what counts as
  divergence).
- "Results changed and I do not know why": diff environment
  lockfiles, data checksums and config before suspecting code;
  git bisect only after the inputs are proven identical
  (rseng-reproducibility's bookkeeping makes this a five-minute
  question).
- Nondeterministic bugs: suspect the usual three - unseeded or
  shared randomness (rseng-defensive-coding), parallel ordering and
  race conditions (run single-threaded to confirm), and
  iteration-order or filesystem-order dependence. Make it
  deterministic FIRST, then debug.
- Scale-dependent failures (fails on the cluster, passes locally):
  memory limits, walltime, node differences, thread counts,
  missing files on compute nodes - read the scheduler logs and
  `seff` before the code (rseng-hpc-computing); reproduce at the
  smallest failing scale.
- Heisenbugs that vanish under observation usually implicate
  timing or uninitialized state; prefer low-intrusion observation
  (sampling profilers, core dumps, logging) over stepping.

## Service startup failures

When a delivered stack fails at launch (compose service exits, API
returns 500s on first request), debug from the logs, not the code:
`docker compose logs <service>` / the server's stderr almost always
names the true failure - a missing env var, an unreachable
database host, a port collision, a schema mismatch. Fix the FIRST
error in the log (later ones cascade), restart, re-read; repeat
until startup is clean, then re-run the request that failed. The
same loop applies outside containers: read the traceback of the
crashing entry point before touching application code.

## Mechanics worth teaching

- Read the WHOLE error: the bottom-most frame of the traceback in
  YOUR code, the first error in a cascade (later ones are usually
  consequences), the actual message text - half of debugging is
  reading what the program already said.
- Debugger beats print for exploration (breakpoints, inspecting
  live state, post-mortem on the crash); print/logging beats
  debugger for production, parallel and long-running contexts -
  structured, greppable, left in place behind a verbosity flag
  (service-style logs when the code runs unattended).
- Rubber-duck honestly: explaining the bug out loud - to the
  agent - is a legitimate technique; the agent's role is to ask
  the hypothesis-forcing questions, not to guess along.
- Know when to stop: after real effort, write up the evidence
  trail and ask a colleague or file an issue - the write-up alone
  solves a good fraction (rseng-trainer's errors-are-curriculum:
  narrate the diagnosis as you go).

## Working with this skill

This skill is source-independent: it encodes systematic debugging
practice (hypothesis-driven diagnosis, delta debugging and
bisection) as taught in the linked references, applied to research
software.

Learn more (verified):
  - https://www.debuggingbook.org - The Debugging Book (Zeller;
    systematic and automated debugging techniques)
  - https://jvns.ca/blog/2022/12/08/a-debugging-manifesto/ -
    Julia Evans' debugging manifesto

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-defensive-coding - make silent bugs crash first
- rseng-hpc-computing - scale-dependent cluster-only failures
- rseng-lessons-learned - postmortems from debugging trails
- rseng-numerical-accuracy - deciding whether divergence is real
- rseng-reproducible-environments - pin environment to reproduce the bug
- rseng-workflows - cached stages make pipeline bisection cheap

<!-- related-skills:end -->

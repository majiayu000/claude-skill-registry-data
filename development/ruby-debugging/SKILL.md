---
name: ruby-debugging
description: Use when diagnosing Ruby/Rails exceptions, incorrect behavior, production failures, logging problems, unexpected state, or intermittent defects.
license: MIT
---

# Ruby Debugging

## Purpose

Turn an observed failure into a verified root cause and a regression-safe fix.

## Activate when

- an exception or failing test exists
- behavior is incorrect but the code appears plausible
- a production issue needs diagnosis
- logs do not explain an intermittent problem
- state becomes invalid somewhere upstream of the failure

## Repository inspection

Before debugging, inspect the repository context and then collect evidence:


Collect:

- exact error/message
- full relevant stack trace
- request/input
- relevant state
- Ruby/Rails/dependency versions
- recent changes
- reproducibility
- logs/metrics/traces available to the repository

Do not start by changing code.

## Debugging loop

```text
build a feedback loop
  -> reproduce and minimise
  -> rank falsifiable hypotheses
  -> instrument one variable at a time
  -> fix at a real seam with a regression test
  -> clean up and verify
```

**The feedback loop is the work.** Build one command that goes red on this bug before reading code to form a theory. With a tight, red-capable loop, bisection, hypotheses, and instrumentation all consume the same signal; without one, reading code produces guesses.

### Phase 1: feedback loop

Load `references/feedback-loops.md` for the ways to build one in a Ruby/Rails repository, how to tighten it, and how to handle intermittent bugs.

Phase 1 is complete only when you can name one command you have already run, with its redacted output shown, that is:

- **red-capable**: it drives the real code path and asserts the reported symptom, so it can fail on this bug and pass once fixed;
- **deterministic**: the same verdict every run, or a pinned, high reproduction rate for an intermittent bug;
- **fast**: seconds, not minutes;
- **agent-runnable**: it runs unattended.

If no such command can be built, stop and say so: list what was tried and ask for access to the reproducing environment, a redacted captured artifact, or permission for temporary instrumentation. Do not move to hypotheses without a loop.

### Phases 2–4: reproduce, hypothesise, instrument

Load `references/reproduce-hypothesise-instrument.md` before Phase 2. In short:

- confirm the loop reproduces the **reported** failure, not a nearby one, then minimise until every remaining input, step, and record is needed to keep it red;
- write 3–5 ranked hypotheses, each with the prediction that would prove it wrong, and show the list before testing it;
- probe one variable per run, preferring the debugger over logs, and tag every temporary log line with a unique prefix such as `[DEBUG-a4f2]`;
- for a performance regression, measure a baseline and bisect instead of adding logs.

### Phase 5: fix and regression test

Turn the minimised reproduction into a failing test at a seam that exercises the real call pattern, watch it fail, fix, and watch it pass. Then re-run the Phase 1 loop against the original, un-minimised scenario.

If the only available seam is too shallow to reproduce the bug (a unit test cannot replay the multi-caller chain that triggered it), a test there gives false confidence. Record the missing seam as a finding for `ruby-api-design` instead of adding that test.

### Phase 6: cleanup

- the Phase 1 loop no longer reproduces the failure;
- the regression test passes, or the missing seam is recorded;
- no `[DEBUG-...]` line remains (`grep -rn "DEBUG-a4f2"`);
- throwaway scripts are deleted or moved to a clearly marked location;
- the confirmed hypothesis is stated in the commit or PR message.

### Redaction

Redact every secret, token, cookie, and personal datum as `<REDACTED>` before showing commands, output, or captured artifacts. Build loops that read credentials from environment variables, and quote only the lines of a captured request that carry the signal.

## References

Load only the reference for the phase in progress. Each is self-contained and one level deep. Consult a listed pattern only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| building or tightening the Phase 1 loop, or the bug is intermittent | [references/feedback-loops.md](references/feedback-loops.md) | Loop construction menu; tightening; intermittent bugs; when no loop can be built | `flaky-test-diagnosis` |
| reproducing, minimising, hypothesising, or instrumenting | [references/reproduce-hypothesise-instrument.md](references/reproduce-hypothesise-instrument.md) | Reproduce and minimise; falsifiable hypotheses; instrumentation; performance branch | `diagnostic-context`, `regression-test` |

## Stack traces

The exception location is where failure surfaced, not necessarily where invalid state was created.

Trace backwards through:

- arguments
- collaborators
- data loading
- normalization
- callbacks
- persistence
- external responses

## Logging

Good diagnostic logs identify:

- operation
- correlation/request identifier when available
- relevant domain identifier
- meaningful state transition

Do not log passwords, credentials, bearer tokens, secrets, or full sensitive payloads.

## Interactive debugging

Use the repository's supported debugger (`debug`, `byebug`, IDE tooling, etc.).

Inspect:

- receiver
- locals
- instance variables
- stack
- branch state
- database/external responses where relevant

## Intermittent failures

Look for:

- concurrency
- time
- ordering
- retries
- external dependency behavior
- shared mutable state
- database isolation/transactions

Avoid "fixes" that only add sleeps or retries without evidence.

## Fix discipline

Prefer the smallest root-cause fix that preserves unrelated behavior.

Then add a regression test that would have failed before the fix.

## Verification ladder

1. reproduce original failure with the Phase 1 loop
2. run focused regression test
3. run affected test group
4. run broader suite when appropriate
5. inspect final diff

If a check cannot be run, state that explicitly.

## Reference example

Reproduce first, then narrow: a minimal failing script with a filtered backtrace, before touching any application code.

```ruby
# repro.rb - the smallest script that exhibits the defect
def normalize(zip)
  zip.to_s.gsub(/\D/, "").rjust(5, "0")
end

expected = "00401"
actual = normalize(401)
if actual != expected
  puts "FAIL: expected #{expected.inspect}, got #{actual.inspect}"
  begin
    raise ArgumentError, "repro captured"
  rescue => e
    puts e.backtrace.first(2)
  end
else
  puts "PASS"
end
# next step: add a regression test that encodes this expectation
```

## Agent review checklist

- [ ] evidence captured
- [ ] a red-capable feedback loop was built and run before any hypothesis
- [ ] reproduction minimised to load-bearing elements
- [ ] hypotheses ranked and each stated with a falsifying prediction
- [ ] hypothesis tested
- [ ] root cause distinguished from symptom
- [ ] regression test added/updated
- [ ] no sensitive data logged
- [ ] original reproduction now passes
- [ ] temporary `[DEBUG-...]` instrumentation removed
- [ ] broader regression checked

## Verification

Use deterministic reproductions where possible. For production-only failures, capture the observed evidence and create the narrowest safe reproduction available.

## Source foundation

Based on the logging and debugging material in *The Ruby Workshop*. The evidence-first and regression-oriented approach is aligned with the testing/refactoring discipline of *Clean Ruby*.

The feedback-loop-first phases, the red-capable completion criterion, minimisation, ranked falsifiable hypotheses, tagged instrumentation, and the missing-seam finding are adapted, in this repository's words and with Ruby/Rails loops, from the `diagnosing-bugs` skill in https://github.com/mattpocock/skills (MIT License, Copyright (c) 2026 Matt Pocock).

## Book integration: interactive debugging

For a reproducible local failure, an interactive breakpoint can be useful at the point where state becomes suspicious. Inspect locals, receiver state, and the call path, then remove temporary breakpoints before the final patch.

Do not substitute a debugger for a hypothesis. The debugging loop remains:
feedback loop -> reproduce -> hypothesize -> instrument -> fix -> regression test -> clean up.

## Book integration: *The Well-Grounded Rubyist*

Chapters 1 and 15 are useful references for the Ruby execution/tooling loop, syntax checks, `irb`, stack traces, `caller`, and runtime introspection. Start with a minimal reproduction and observable evidence; introspection is a diagnostic aid, not a reason to add dynamic behavior to the fix.

---
name: debug-rca
description: Root-cause method with the mcp-debugger (breakpoints, stack, variables), then a failing regression test and an RCA with a Fix spec. Use when a failure has a cause that is not clear, or the user says debug, root cause, RCA or step through it.
---

# Debug to a root cause

A debugger removes the need to guess. That is its full value, and it is the value that is easiest to lose. An
agent with many debug tools and no method sets fifteen breakpoints and steps two hundred times. Then it writes a
story that sounds like an explanation but contains no observation.

The method below makes the difference. The tools are the easy part.

This skill is the method of the `shark:code-debugger` agent. The agent finds every cause of the reported
behaviour, pins each one with a failing test, guards the rules that the fix must keep, and returns a Fix spec. The `shark:code-writer` agent then makes the fix. The two jobs stay
separate, so that the fix rests on a diagnosis that another person can read.

## Project values

Read the project's `AGENTS.md` (or `CLAUDE.md`) first. This skill uses these sections:

| Section | Used for |
| --- | --- |
| `## Commands` › `test <paths>` | The command that runs one test without the debugger |
| `## Commands` › `setup`, `test-db:copy` | The environment and a test database for the reproduction |
| `## Invariants`, `## Architecture rules` | Rules that a defect often breaks: read them before the hypothesis |
| `## Docs layout` | The handbook or the pitfalls chapter of the area, and the decisions log |
| `## Secrets` | The files that you never read; how the environment is loaded at runtime |

If a section is missing, ask the user once. Suggest adding it to `AGENTS.md`.

## Modes: single, zone and merge

The brief names the mode. The method below applies to each mode.

| Mode | The brief gives | You do | You return |
| --- | --- | --- | --- |
| single (default) | the report | the whole method, then the closed spec | the RCA file |
| zone | the report, one property, one axis, its cells, your tree | the loop for the cells of your zone, a test for each cell | the zone report of [`references/zones.md`](references/zones.md) § 4 |
| merge | the zone reports and their trees | combine the zones, write the RCA with the Properties and Rounds tables, close the spec | the RCA file, and the triggers for round 2 |

In zone mode, report each value that no confirmed cause explains, also outside your zone. Do not close the spec in
zone mode.

## Completeness: one cause is not the end

A real defect often has more than one cause, and the obvious fix often breaks a rule next to it. An investigation
that stops at the first confirmed cause fixes one symptom, misses the others, and ships a regression. These five
steps prevent that. They frame the whole investigation; the debugger loop below confirms each cause inside them.

1. **Symptom map, before any hypothesis.** Write each reported symptom as its own row: what was seen, in which
   path, with which data. Do not merge two symptoms into one row because they "probably" have one cause; only an
   observation can merge them. Each row ends with a confirmed cause and a failing test, or with "not reproduced"
   and the reason.
2. **Assume more than one cause.** A report with several symptoms, or a defect in a path that has a twin, usually
   has more than one cause. A first confirmed cause is a finding, not the end. After each confirmed cause, go back to
   the symptom map and ask which rows it does not explain.
3. **Variant matrix.** For the path of each cause, list the variants that can take a different branch, and test
   each one that applies. Mark each cell: tested (with the test name), or not applicable (with the reason).
   - **Each cell runs with the defect's state in place.** To test "unpublish" for a draft defect, make the pending
     draft first, then unpublish. An existing test that passes without that state does not cover the cell: write
     the cell's own test.
   - **Two cells are never "not applicable" without a search:** the "all" scope (all locales, all tenants, bulk
     operations, `locale: 'all'`), and the denied actor. Search the code for access rules on the data and the
     operations that the fix touches (field access, collection access, role checks). If a rule exists, the denied
     actor is a cell, and its test is a guard.

   | Axis | Values to check |
   | --- | --- |
   | Twin paths | collection and global, list and search, single and bulk, sync and async, web and POS (when each has its own code), create and update |
   | Operation | create, update, draft save, publish, unpublish, delete, read after write, read in another scope |
   | Value shape | set, change, clear (`null`, empty list, empty string, `0`, `false`), nested child of an array or a block |
   | Scope | one locale, tenant or key, and all of them; another locale, tenant or key |
   | Actor | allowed, and denied by role, access rule or field access |
   | Time and order | sequential, concurrent, retry after a failure, after a restart or a cache fill, time zones and DST |
   | Identity | case, whitespace and aliases of keys; currency and unit exponents |

4. **Find the twins.** Search for the same pattern in other places: the same helper, the same check copied into
   another module, the parallel operation (`grep` for the faulty expression and for the callers of the faulty
   function). Read the history of the faulty lines (`git log -S '<expression>'`, `git log -L`): an old fix of the
   same kind in one twin often shows the other twin that did not get it.
5. **Adjacent rules.** Before the Fix spec, collect the rules that the obvious fix could break: `## Invariants`, the
   spec and docs of the area, access control, the callers of the code that will change, and the tests near it. For
   each rule that the fix touches, write a guard test that passes now and must still pass after the fix. Name the
   obvious fix that would break it in the Fix spec, as "Rejected".

**The completeness gate.** The investigation ends only when each symptom row has a confirmed cause and a failing
test, each applicable matrix cell has a test, the twin search is done, and each adjacent rule has a guard test.
Until then, the RCA status stays "investigating", also when one cause is confirmed.

**Close the spec before the hand-off.** Load `shark:solution-spec` and do its method on the fix: the guards on
the path, the input classes, the operations on the state, the behaviour table, the decisions and the adversarial
check. Each row gets a test; write the tests that are missing. A closed spec lets a fast writer build the fix with
no behaviour decision of its own.

**A script checks the gate.** Write the RCA file from the template, then run both commands. The gate passes only
when both exit with 0. Do not hand off with a failed gate: fix the RCA or write the missing tests.

```bash
node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/debug-rca/scripts/rca-gate.mjs" check <rca.md>
node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/debug-rca/scripts/rca-gate.mjs" run <rca.md> --phase before \
  --cmd '<the project test command with {files}, writing a JUnit report to {junit}>'
```

- `check` finds a symptom with no cause or no test, a matrix cell with no test and no reason, a missing Scope or
  Actor row, a "not applicable" on those axes with no search command, an open-cell phrase ("not tested", "cut for
  time", "inferred: same path", "I read this in the code"), and a test that the Fix spec does not list or that is
  not in its file.
- `run` runs the Fix spec tests: each regression test must fail now, and each guard test must pass. The command
  must write JUnit XML: Vitest `--reporter=junit --outputFile={junit}`, Jest `jest-junit`, pytest
  `--junitxml={junit}`.

## Before you start the debugger

**Reproduce the defect every time.** If you cannot cause a defect when you want, you cannot find its root cause.
You will "fix" it and never know. Get one command that fails every time. If the defect is intermittent, that _is_
the first finding. Say so, and look for the source of the nondeterminism first: order, time, concurrency, cached
state, a test that leaks state into the next test.

If the report is a description from a user and the tests pass, write the reproduction yourself. The test does
the reported steps and asserts the value that the user saw. **Run it without the debugger first**, with the
project's `test <path>`. One run shows that the defect is real and that the test loads. Then a launch problem
cannot look like the defect.

**Read the failure first.** Read the traceback, the assertion diff, the actual value. The error text fully
explains many defects. To attach a debugger to those is theater.

**Read the rules of the area.** Read the project's `## Invariants` and the handbook chapter of the area. Many rules
exist because of a specific failure. A defect often is one of those rules broken.

**Write down the hypothesis** in one sentence: _"I think that X has the wrong value when Y runs, because Z"_. A
breakpoint without a hypothesis is sightseeing: you look at what the screen shows, and you conclude what it
suggests.

Keep a hypotheses table while you work. It goes into the report and the RCA:

| # | Hypothesis | Prediction (what you expect to observe, where) | Observed | Result |
| --- | --- | --- | --- | --- |
| 1 | `<X>` is empty when `<Y>` runs, because `<Z>` | `<expression>` at `<file:line>` is `<value>` | `<value>` | confirmed / refuted |

## The golden path of the mcp-debugger tools

The kit declares the mcp-debugger server in its `.mcp.json`. In a plugin, its tools have a long namespaced ID.
Find them by function: the tools are deferred, so load them with ToolSearch (query `mcp-debugger`) before the
first call. The short tool names below are the names in the server's documentation.

| Step | Tool function | Notes |
| --- | --- | --- |
| 1 | Create a debug session (`create_debug_session`) | Give the language. Give the interpreter of the project as `executablePath` |
| 2 | Set a breakpoint (`set_breakpoint`) | ABSOLUTE file path. Prefer `statement` (the line text) or `function` to a line number |
| 3 | Start the program (`start_debugging`) | ABSOLUTE `scriptPath`: the entry script of the test runner, not the interpreter binary |
| 4 | Read the stack (`get_stack_trace`) | Each frame has an `id` |
| 5 | Read the scopes (`get_scopes`) | Give the `frameId` from the stack frame |
| 6 | Read the values (`get_variables`, `get_local_variables`, `evaluate_expression`) | Expand a value that has a `variablesReference` |
| 7 | Step or continue (`step_over`, `step_into`, `step_out`, `continue_execution`) | Only while the session is paused |
| 8 | Read the program output (`get_output`) | Pass the returned cursor back to read only new lines |
| 9 | Close the session (`close_debug_session`) | Always, also after a failure. A session holds a process |

Other tool functions that help:

- **Logpoint:** a breakpoint with `logMessage` (`"order={order_id}"`) writes to the output and does not pause.
  It is the safe way to watch a hot path.
- **Move the window:** list, remove and clear breakpoints while the program runs, to move a bisection window
  without a restart.
- **Restart:** restart the session with the same configuration; the breakpoints apply again, and the output
  buffer starts from zero.
- **Attach:** connect to a process that waits under a listener (a container, a remote host, a pod with a port
  forward). See "Attach to a running process".
- **Expose:** give a read-only mirror of the session to the human's IDE. Execution control stays with you.

A breakpoint can stay unverified until its module loads. That is normal. If the response says "requested line N,
bound to line M", trust the bound line. Pass `expectedContent` with a line number to catch an off-by-one line
before it wastes a session.

## The loop

1. **Set the breakpoint at the boundary, not at the crash.** The crash site shows the symptom. The boundary is
   where correct state becomes incorrect. Put the breakpoint where the value _enters_ the suspect region.
2. **Observe. Do not infer.** Read the actual values with the variable and evaluate tools. "It must be empty
   here" is the sentence that comes before most lost hours.
3. **Bisect the state.** Find the last point where the state is correct, and the first point where it is wrong.
   The defect is between those two points. This is the method of `git bisect`, applied to execution instead of
   history.
4. **Confirm by prediction.** Before the last step, say what you expect to see. If the prediction is correct, you
   understand the defect. If it is not correct, your hypothesis was wrong and you learned something. Start again
   at step 1. Do not change the story to fit the observation.
5. **Separate the root cause from the proximate cause.** "The value was empty" is proximate. "Nothing sets it,
   because the unit of work ran without the tenant context" is root. Continue to ask _why_ until the next answer
   is a design decision, not a mechanism.
6. **Close the session.** A session holds a process.

## Restraint

- **Few breakpoints.** Two or three, moved on purpose, are better than fifteen set by guess. You must reason
  about each breakpoint that you add.
- **Prefer evaluate to stepping.** One expression often answers what fifty steps answer.
- **Do not step through library or framework code** unless the evidence points there. It usually does not. Turn
  on "just my code" where the adapter has it.
- **Stop a hypothesis when an observation confirms it.** Then go back to the symptom map and the variant matrix
  for the next row that has no cause. Stop the investigation only at the completeness gate.
- **Read the code to make the hypothesis: that is the method, not a shortcut.** Then observe the value that
  confirms it, with the cheapest instrument that shows it: a failing test with a precise assertion, a probe script
  that prints the value, or the debugger. Use the debugger when the value is deep in a call chain, depends on
  concurrency or order, or when a probe would change the behaviour. A cause that you found by reading and did not
  observe is only a hypothesis.

## Observed and inferred

Label each statement of the report and the RCA:

| Label | Use it when |
| --- | --- |
| Observed | You read the value in the debugger, in the program output, in a log, or in a database row |
| Inferred | It follows from observed values, but you did not see it directly |

A root cause that is only inferred stays a hypothesis in the RCA status ("investigating"), not "root cause
confirmed".

## Launch: one test under the debugger

Debug one test, not the full suite. Use the interpreter and the dependencies of the project, never a global one.
The general recipe, for each language:

1. Check that the debug adapter is installed for the interpreter of the project.
2. Create the session with the interpreter of the project.
3. Start the entry script of the test runner as `scriptPath`, with the ID of one test in `args`.
4. Turn off parallel workers and caches of the runner, so that one process runs the test.
5. Set the environment that the project's `test` command sets (a settings module, a test flag). Never copy a
   secret value into a launch configuration: the project loads secrets at runtime (`## Secrets`).

6. **Reach the code that runs the test.** If the runner runs tests in worker processes or threads, a launched
   session can stay in the main process, and its breakpoints stay "Unbound". Then start the runner with its own
   inspector or listener option, and attach the session to that port. The script `debuggee.mjs` does this: it picks
   a free port, starts the command in the background, waits until the port is open, and prints the port, the log
   and the notes for attach mode. Logpoint messages go to that log.

   ```bash
   node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/debug-rca/scripts/debuggee.mjs" start --cmd '<runner command with {port} in its inspector option>'
   node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/debug-rca/scripts/debuggee.mjs" log <id> --grep <logpoint text>
   node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/debug-rca/scripts/debuggee.mjs" stop <id>
   ```
7. **Check what you attached to.** The first output line shows the interpreter that runs. A session can ignore
   `executablePath` and use the interpreter on the `PATH`.
8. **Check that a file binds before you depend on it.** Set one logpoint in the file, run, and read the log. If
   the code ran and the log has no message, the file does not bind: move to a caller or a callee that binds, or use
   a probe test with a precise assertion that prints the value. The value is still observed.

The recipe for each language, with what earlier sessions observed:

| Language | Recipe |
| --- | --- |
| Python (debugpy) | [`references/launch-python.md`](references/launch-python.md) |
| JavaScript and TypeScript (Node, js-debug) | [`references/launch-javascript.md`](references/launch-javascript.md) |
| Other languages | [`references/launch-other.md`](references/launch-other.md) |

## Attach to a running process

Use attach when the test runs in a container, on another host, or under an interpreter that the server cannot
launch.

1. Start the test under a listener that waits for the debugger before the test starts. Examples:
   - Python: `python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m pytest <test id>` (`debuggee.mjs start`
     puts the shark debugpy on `PYTHONPATH`; in a container, install debugpy there);
   - Node: `node --inspect-brk=0.0.0.0:9229 <runner entry> <test file>`.
2. Publish the port of the container (for example `-p 5678:5678`).
3. Wait until the listener is up. An attach before the listener is up fails with "Proxy exited during
   initialization".
4. Attach with the host and the port.
5. Set breakpoints on the paths that the target process sees (the container paths), not on the host paths. Use
   `line`: read the line number from the host copy of the file.
6. To debug code that is not the main checkout (a worktree, an export), mount it at the source path of the
   container.

**CAUTION:** In one session, `pathMappings` had no effect in attach mode. A breakpoint on a host path stayed
unverified ("Breakpoint in file that does not exist"). The `statement` and `expectedContent` options need a
source file that the server can read, so they fail on a container path. Use container paths and line numbers.

## Observe the database

Observe the database while the debugger holds the test at a breakpoint.

- A test that runs inside one transaction (the default of many test frameworks) rolls back its rows at the end.
  Another connection does not see these rows until a commit. To observe the rows from a second client, debug a
  test in the mode that commits, or evaluate the query in the test process.
- A session-local setting (a tenant context, a role, a search path) is local to its transaction or connection. In
  a client in autocommit mode, the setting is gone at the next statement. Set it and query inside one
  transaction, then roll back.
- Observe as the runtime role of the application, not as an administrator. An administrator role can bypass the
  row rules that cause the defect.

## Read the responses of the tools

- **`"state": "stopped"` right after the start can mean that the process already exited**, often with an import
  error or a database error. Read the output first.
- **A breakpoint that stays unbound** after the program started has one of two causes. The file did not load in
  the process of the debugger, or the path is not absolute.
- **An evaluated method call runs.** A cache read can change the counters of the cache. A query costs a round
  trip inside the test transaction. Read fields directly when you can.
- **A caller's variables need its `frameId`** from the stack. Without it, the evaluation runs in the top frame.
- **After a continue, wait for a new stop** before you read the stack. Right after the continue, the stack can be
  empty, with the old stop time. The list of sessions shows the new stop.
- **A fast program with only logpoints ends in about 1 s.** The session then reports "stopped". That is not a
  failure: read the output for the logpoint lines.
- **Redacted values.** The server masks values that look like credentials (`<redacted:…>`). The program state is
  not changed. Do not try to read a secret: the project's `## Secrets` rules apply in the debugger too.

## Failures of scenario runs and LLM agents

A failure can be in a saved scenario run: an evaluation, a bench, an agent conversation. Then the saved run
files are often the only evidence of the model run.

1. Read the saved run file of the failed case before any replay. Its records hold what the code decided.
2. Form the hypothesis from those fields.
3. Replay the case offline, with a scripted model (a fake) and no live model call. The breakpoint then stops at
   the boundary that you want.

The method and a replay skeleton are in `references/replay-saved-runs.md` in this skill folder. To classify many
failed cases, use the classification of `shark:goal-loop`.

## Time and history

- **A test that went red "after many merges": pin the date first.** A test clock that moves with the real date
  (for example "the most recent Monday") can make an absolute date in a test fail. Run the test again with an
  older fixed date before you bisect. If it passes, look for an absolute date in the test, not for a bad commit.
- **The first bad commit, fast.** Check out only the source folder of each commit (`git checkout <commit> --
  <source folder>`) and run the failing test. Limit: a file that a later commit added stays in the tree. Check the
  result against a clean checkout of the bad commit. Restore the tree when you finish.
- **Long runs.** Start a long run (a gate, a suite) as a background task and wait for its notice. A foreground
  wait loop moves to the background after a few minutes and cannot wait for a long run.

## Everything else

- Stop a running local worker or scheduler before you debug code that it also runs, so that it does not take the
  same jobs.
- The kit `.mcp.json` writes the server log to `.claude/mcp-debugger.log` in the working directory, with run
  folders next to it. Make sure that git ignores them (`shark:gitignore`). Leave them.

## Without the debugger

If the MCP server is not available, the method still applies: hypothesis, boundary, bisect the state, confirm by
prediction. Use a temporary probe as the instrument: an assertion in the regression test, or a log line that you
delete before you finish. Label each result "inferred", because the confidence that you can give is lower.

If the tools do not show, check the server with `/mcp` or `claude mcp list`. The kit pins the server version,
so the debugger does not change during an investigation.

## What you can change

- **Temporary probes:** a driver script or a probe test. Keep each probe untracked, and delete it before you
  finish.
- **Regression tests:** one failing test for each confirmed cause and for each applicable cell of the variant
  matrix, in the test file that owns the behaviour. Each fails today, for the reason that the RCA gives.
- **Guard tests:** one test for each adjacent rule that the fix could break. Each passes today and must still pass
  after the fix.
- For each test: name it as a behaviour sentence, in the style of the tests near it. If the project tags tests with
  a business-rule ID, tag it. Run it and quote the result. Write no explanation comments in it: the test name gives
  the behaviour, and the RCA gives the reason. A test docstring is allowed, in ASD-STE100: one sentence that says
  what the test proves, with no notes in brackets.
- **Nothing else.** Do not change production code, migrations, settings or configuration. If you must change code
  to observe the defect, say in the report what you changed and why, and undo it.

## The RCA

Write it only after an observation confirmed the hypothesis. The template is `references/rca-template.md` in this
skill folder (`${CLAUDE_PLUGIN_ROOT}/skills/debug-rca/references/rca-template.md`). Find it relative to this
skill, never with a fixed path. Write it as a Markdown file with the section names of the template, and give its
full path: the gate script reads the file, not your report. In the Fix spec, give each test as
`` `<test file>` › `<test name>` ``, one on each line.

The section that gives the document its value is **Evidence**: actual observed values at named locations. An RCA
without observed values is a hypothesis with formatting, and the next person cannot tell the difference.

The **Fix spec** section is the input of `shark:code-writer`. Write it as a spec, not as a patch, with one part for
each cause:

- what must be true after the fix, as behaviour;
- the files that are involved, and why;
- the regression tests, by name, which must pass after the fix, and the guard tests, which must keep passing;
- the obvious or narrower fix that you rejected, and the symptom it leaves or the adjacent rule it breaks;
- what the fix must not change: the callers and the adjacent rules that depend on the current behaviour.

Leave the implementation decisions to the writer. If you saw a decision that matters, state the constraint that
decides it, not the line to type.

End with **Prevention**: the test that catches this defect, and what catches the whole class of defect. A root
cause analysis that does not end in a test is an essay.

## Finish (after the completeness gate)

1. Close every debug session.
2. Stop each debuggee that you started: `debuggee.mjs stop --all`. A debuggee that you started another way: check
   with `pgrep -fl debugpy` or `pgrep -fl inspect`.
3. Delete the probes. `git status` shows only the regression and guard tests.
4. Run the project's `typecheck` with no paths, so that it uses the project configuration. A type checker on
   single files can give false import errors.

## Report (outcome first, ASD-STE100)

- Each root cause and its proximate cause, with `file:line`. Say how many causes you found and which symptom each
  one explains.
- The symptom map: each symptom, its cause, and its test.
- The variant matrix: each cell, tested (test name) or not applicable (reason).
- The twin search: what you searched for, and what you found.
- The adjacent rules and their guard tests.
- The hypotheses table: each hypothesis, its prediction, and whether an observation confirmed it.
- The observed values that make the evidence (labelled observed or inferred).
- The regression tests and their failure output now; the guard tests and their pass output now.
- The Fix spec.
- The full path of the RCA file.
- Where this skill or the tools gave wrong guidance, exactly, so that the skill can be corrected.

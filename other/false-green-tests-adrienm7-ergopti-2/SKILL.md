---
name: false-green-tests
description: Find tests that cannot fail and apply the false-green ratchet. Use for test audits or doubtful passing tests.
---

# Tests that cannot fail

A false green is worse than no test. It occupies the slot a real guard would
have taken, it is counted in the "3380/3380 green" figure everyone trusts, and
when the bug it was written for comes back it actively certifies the bug.

This is the most recurrent defect in this repo. The driver and verification
topics routed by `docs/memory/README.md` record it at least eight times:
`project-hs-partial-fixes-and-false-green-tests`,
`project-lua-closure-before-local-nil-global`,
`project-hs-timer-callback-errors-invisible`, `project-hs-fs-dir-drops-state`,
`project-ahk-guard-tests-must-loop-the-class`, `feedback-ahk-source-encoding`,
`project-macos-initlua-no-compile-coverage` and
`project-ahk-isset-requires-variable-load-crash`.

Run `node tools/test/find-false-greens.cjs` first. It reports patterns 1, 2, 3
and 5 mechanically. Patterns 4 and 6 need human judgement and are the two that
have actually shipped bugs here — read those sections even when the tool is
green.

## The current scoreboard

Measured on the three test trees. These are the numbers the baseline freezes —
they are a debt ledger, not an approval.

| Pattern                    | Count | Concentration                             |
| -------------------------- | ----- | ----------------------------------------- |
| 1 Tautology                | 153   | windows 59, macos 65, linux 29            |
| 2 Vacuous absence          | 17    | windows only, of ~186 absence assertions  |
| 3 Dead / unregistered test | 5     | 2 are a real bug, 3 are intentional SKIPs |
| 5 pcall-only               | 374   | linux 219, macos 155, windows 0           |

Two readings matter more than the totals. **Pattern 2 is nearly solved**: 169 of
~186 absence assertions already carry the guard, so the 17 that do not are
deviations from a live convention, not a missing one. **Pattern 5 is a Linux
problem**: 219 occurrences across only 72 test files is roughly three per file,
and Windows has zero because AHK has no `pcall` — it uses `try`/`catch`.

## 1. The tautology — `AssertTrue(true)`

153 occurrences. The shape is always the same: a real invariant stated in the
message string, and nothing whatsoever verifying it.

```ahk
_DE_PauseNoExpansion() {
    ; All _DE_* and underlying HSE paths must be gated by A_IsSuspended
    AssertTrue(true, "domain expander must respect full pause silence")
}
```

Why it survives review: the message reads like coverage. A diff showing
`+ AssertTrue(true, "must respect full pause silence")` looks like a pause guard
landed. Grep for `pause` in the suite and you get a hit. The invariant is
unverified in every one of these.

A tautology inside a genuine skip branch (`; corpus vector is macOS-only`) is
defensible — it keeps the plan count stable. A tautology that IS the whole test
body is not. The tool cannot tell them apart, which is why the baseline exists.

## 2. The absence assertion on a body that may be empty

`_DriverFuncBody(Name)` returns `""` on a name it cannot find. `InStr("", x)` is
`0`, so **every "must NOT contain" assertion passes vacuously** once the function
is renamed, moved out of the scanned tree, or mistyped. AHK v2 raises no
load-time error for an unknown name, so nothing reports it anywhere.

The convention is already established — 169 of ~186 sites do this:

```ahk
Body := _DriverFuncBody("RebuildHotstringsLive")
Assert(Body != "", "RebuildHotstringsLive must exist in ui/menu/menu_rebuild.ahk")
Assert(InStr(Body, "Critical(") = 0, "…")
```

A **presence** assertion on the same variable (`InStr(Body, "x") > 0`) also
proves non-emptiness and is equally acceptable. What is not acceptable is a
function body whose only assertions are absences.

`tools/test/verify-change.cjs` already checks that scanned symbols exist — but
only for files in the current diff. The 17 open sites predate their diffs, which
is exactly why a full-tree sweep is needed.

## 3. The test that never registers

`Test(Name, Callback)` pushes onto `TEST_REGISTRY`. `RunTests()` then **snapshots**
that registry into `ActiveTests` and prints the `1..N` plan from the snapshot,
before executing anything. A `Test()` call that happens _during_ a run therefore
lands in `TEST_REGISTRY` but never in `ActiveTests`: it never executes, and the
plan count never mentions it. No error, no warning, plan matches, suite green.

There is a live instance. In `unit/test_domain_expander.ahk`, two test functions
and their registrations were spliced into the middle of `_DE_Add`'s body — the
function opens at line 30 and its real body resumes at line 44:

```ahk
_DE_Add(Trigger, Repl, Group := "default", IsWord := false) {   ; line 30
_DE_PauseNoExpansion() { … }                                    ; line 33
Test("Domain expander: pause must silence every expansion path", …)  ; line 37
    Flags := IsWord ? "" : "?"                                  ; line 44 — body resumes
```

AHK v2 accepts this (nested functions are legal closures), so nothing complains.

**Registering from inside a helper is a legitimate idiom** when the file calls
that helper at top level — that is how the corpus files emit one test per JSON
vector. The distinction is whether anything reaches the enclosing function.

## 4. The stub that answers for the code under test — human judgement only

No tool finds this. It is the shape that has cost this repo the most.

`prediction_engine.perform_check` called `StreamingHandler.ngram_predict`, a
function production never implemented. Calling a nil field threw, the `hs.timer`
callback swallowed the throw, and every keystroke-driven request died silently —
**while the unit test stayed green, because the test's own stub defined
`ngram_predict`**. The stub answered a call production could not.

The same shape twice more: the `hs` stub returned a single stateless iterator for
`hs.fs.dir`, so the buggy "drop the state object" pattern worked in CI and
crashed on every real Hammerspoon boot; and the `shell_runner` stub returned
`nil` where `hs.task:start()` returns a task object, cementing the very defect
its test claimed to lock down.

**The rule:** a stub must mirror the real module's exported surface and its
return arity — nothing more, nothing less. When you stub a singleton
(`StreamingHandler`, `PromptBuilder`, `AppFilter`, `ApiCommon`), diff its keys
against the real module before trusting the test.

Two guards already exist; do not weaken them.
`test_prediction_engine.lua` §8 asserts StreamingHandler exposes **no**
`ngram_predict` and that `perform_check` reaches `fetch_llm_prediction`.
`meta/test_fs_dir_iterator_contract.lua` pins the stub to the faithful
`(iterator, state)` shape.

## 5. `assert_true(ok)` proves only that the call returned

374 occurrences, 219 of them on Linux. When `ok` comes from `pcall`, the
assertion passes for every wrong-but-non-throwing result: a nil prediction, an
empty expansion, a guard that silently no-ops, a function that returns before
doing any work.

This is precisely how the Ollama streaming bug shipped. `on_done` called
`os.remove(tmp_path)` above the `local tmp_path` declaration, so it threw on its
first statement on every completion; `ShellRunner`/`hs.task` invoke callbacks
inside a `pcall`, which swallowed it; predictions silently never appeared while
the suite stayed green.

Asserting on the pcall's **returned value** is fine — the status is then just a
precondition. The failure shape is the status being the only thing ever checked:

```lua
local ok = pcall(adapter.send, nil)
helpers.assert_true(ok, "send(nil) must not throw")   -- proves nothing about send
```

A "must not throw" contract is a real contract, but it is the weakest possible
one. If the function is supposed to log and return, assert the log line. If it is
supposed to no-op, assert zero side effects — count the calls.

## 6. The source-grep that pins the spelling, not the invariant

Also human judgement only. A meta-test asserting what the code _says_ has two
failure modes, and the second is the dangerous one.

It breaks on any legitimate refactor — annoying but loud. Worse: **if the bug is
in the string, the test certifies the bug.** A meta-test once asserted that
`pcall(hs.fs.dir, …)` was present and the bare generic-for absent. That is
exactly the broken form that drops the directory state object. The guard was
actively enforcing the defect.

Scope is the other half. `test_live_rebuild_no_critical_io.ahk` asserts
`InStr(Body, "Critical(") = 0` on **`RebuildHotstringsLive`'s body only**. Any
caller that wraps the call in `Critical("On")` from outside restores the 1-2 s
keyboard freeze the fix removed, and the test stays green.

When you write a source-scan test, ask three questions:

- Would a rename that preserves behaviour break this? Then it pins spelling.
- Would the bug still be possible via another route? Then scope the scan to the
  whole tree (`_DriverSourceNoComments()`), not one function body.
- Does the string I am asserting encode the fix, or the mechanism of the fix?
  Assert the **absence of the harmful operation** — zero shell execs, zero modal
  calls, zero POSTs after the gate — never the presence of the scheduling call.
  `doAfter(0)` is not a thread hop.

And remember source-introspection's structural blind spot: it reads text, never
parses it. A load-time crash like `IsSet(obj.prop)` is invisible to the entire
`_DriverFuncBody` / `_DriverSourceConcat` family.

## The ratchet

```bash
node ./tools/test/find-false-greens.cjs                    # counts vs the baseline
node ./tools/test/find-false-greens.cjs --update-baseline  # only when the count goes DOWN
```

It runs inside `npm run test:js`, so a new tautology or a new unguarded absence
assertion fails the gate. It detects patterns 1, 2, 3 and 5; patterns 4 and 6 need
human judgement and the tool says so rather than pretending otherwise.

The baseline in `tools/test/false-greens-baseline.json` is a **debt ledger, not an
approval**. Lower it whenever you convert one of these into a real test — never
raise it to make a change pass. Raising it is the ratchet equivalent of weakening
a test, which `ship-fix` forbids outright.

## Writing a regression test that can actually fail

Every bug fix ships with a regression test under the `AGENTS.md` delivery
contract. Before you call it done:

1. **Prove it red against a safely available unfixed state.** Prefer running the
   test before editing production code. Never stash, reset, or rewrite an active
   worktree to manufacture evidence; if no pre-fix state remains available,
   record that limitation explicitly.
2. **Assert the guarantee, not the mechanism.** "Zero shell execs" beats "the
   purge was scheduled". "No POST after the gate" beats "`stop_warmup` is
   called".
3. **Encode the root cause, so the whole class is covered.** A guard scoped to
   the one function that bit you misses the sibling site — which is the dominant
   bug shape on both drivers.
4. **Check your stub against the real module** before trusting a green run.

And know what a green suite does _not_ cover: driver and JavaScript gates cover
different surfaces. A targeted green result only supports the claim selected by
`verify-change`; a gate that cannot start is not green.

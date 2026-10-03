---
name: verify
description: Drive EZR's actual surfaces to confirm a change works — the program runner, the browser interface, and the tool CLIs. Use when verifying a change under ezr/, or when asked to check that EZR works. Not for running the test suites; those are run.sh.
---

# Verifying EZR

Runtime observation, not test runs. `run.sh` is the CI gate and proves
nothing about whether a change is reachable by a user.

## The thing that will catch you out

**There are three languages in this repository and they are not the
same language.** A change to one is invisible from the others, and the
test suites do not notice.

| Surface | Language | Where it lives |
|---|---|---|
| `2-interpreter-python/ezrun.py` | **the core** — lists, `let`, `show`, `len`/`head`/`tail`, recursion | `syntax.py`'s AST pipeline |
| `2-interpreter-python/ezr.py <file>` | the **directive** language — `tax = 40`, `expect`, `learn` | the `EZR` class in `ezr.py` |
| `5-runtime-java/ezr` | **the core again**, in Java — same language, same exit codes | `com.codric.ezr` |
| `6-interface-html/ezr-live.html` | the directive language again, in JS | hand-written, self-contained |

A core-language program fed to `ezr.py` or the browser returns
`cannot parse`. That is correct behaviour, not a bug — but it is how
an entire feature set once shipped unreachable while 87 assertions
passed, so check the surface matches the change before concluding
anything.

**Never verify by importing.** `from syntax import compile_ezr` then
calling it is a unit test you wrote. It was exactly how lists and
`let` were "verified" while no user could run them. Shell out.

## Driving the core language

```bash
cd 2-interpreter-python
python3 ezrun.py ../examples/sum.ezr                 # 15  @ 256/256
python3 ezrun.py ../examples/largest.ezr             # 42  @ 256/256
python3 ezrun.py -e 'let x = 5 in x + 1'             # 6   @ 256/256
echo '[1, 2, 3]' | python3 ezrun.py -                # stdin
python3 ezrun.py ../examples/largest.ezr --call 'largest([3, 9, 2])'
```

A file of definitions must say what to run — `main()` or `--call` —
because `program := definitions | expression` and the trailing-
expression grammar is ambiguous.

**Exit codes are the thing to assert on:** `0` a value, `1` a refusal
(the program ran and produced **Z**), `2` input that would not
compile. Check them with `$?` directly — `cmd | head` gives you
`head`'s status, which is the bug that let `run.sh` report PASSED for
failing layers for several commits.

Worth probing: `head([])` (refusal, exit 1), `len(5)` (wrong type),
a missing file and a directory (sentences, not tracebacks), `-d 2`
(depth ceiling), a file with neither `main()` nor `--call`.

## Driving the Java runtime

```bash
cd 5-runtime-java
./build.sh                                   # javac; needs a JDK
./ezr ../examples/sum.ezr                    # 15  @ 256/256
./ezr -e 'let x = 5 in x + 1'                # 6   @ 256/256
echo 'def main() = 6 * 7' | ./ezr -          # 42  @ 256/256
```

Same exit codes as `ezrun.py`: 0 a value, 1 a refusal, 2 uncompilable.

**Gotcha:** if the environment sets `JAVA_TOOL_OPTIONS`, the JVM prints
`Picked up JAVA_TOOL_OPTIONS: ...` to stderr on every single start, which
corrupts any byte comparison. Setting it empty does not help — the banner
still prints, with an empty value. It has to be *removed*:
`env -u JAVA_TOOL_OPTIONS java ...`. The `./ezr` wrapper already does
this; a raw `java -cp out` invocation does not.

**A change to the core language is not verified until both runners
agree.** `python3 differential.py` runs one corpus through `ezrun.py` and
`./ezr` as processes and compares the value, the exit code, which stage
refused, and which binding defect. It does *not* compare the wording —
two runners have different names for themselves and different phrasing
for the same refusal, and holding them to identical prose tests the error
messages rather than the language.

## Driving the browser interface

```bash
python3 -m http.server 8099 --directory 6-interface-html
```

Then Playwright against `/opt/pw-browsers/chromium`. Two gotchas that
cost time:

- `#editor` is **hidden until you click EDIT**. Order is EDIT →
  fill `#editor` → LOAD PROGRAM → RUN.
- The demo picker is a `<select>`, not buttons —
  `pg.locator("select").first.select_option("full")`. Clicking the
  option text times out.
- Buttons by index: `0 RESET, 1 ←BACK, 2 STEP→, 3 RUN, 4 EDIT/VIEW,
  5 LOAD`. `get_by_role("button", name="RUN", exact=True)` does not
  match; use `.nth(3)`.
- The only console 404 is `favicon.ico`. Harmless.

Output lands in the `EVENTS` pane; a healthy run shows `BIND`,
`ANCHOR`, `ASCEND` and renders the weave on the 0–256 scale.

## Driving the tools

```bash
cd 2-interpreter-python && python3 audit.py    # documents vs code
cd 7-forge && python3 selfheal.py              # inject a defect, repair it
cd 7-forge && python3 forge.py --cycles 3 --cycle-budget 2000
```

`audit.py` exits `1` on an overstatement. `probe_runner` inside it
shells out to `ezrun.py`, so a core language that cannot be run fails
`run.sh` through both Audit and Physics.

## Checks worth making for any change under ezr/

1. Which of the three languages does this touch? Drive **that** one.
2. Grammar change → all twenty front ends must agree
   (`7-forge/forge.py --cycles`), and `GRAMMAR.ebnf` must be re-emitted
   (`grammar_doc.py`), never hand-edited.
3. New language surface → does `audit.py` have a probe for it? An
   undocumented capability is a finding in this project.
4. Anything claimed in a document → `python3 audit.py` decides, not
   memory.

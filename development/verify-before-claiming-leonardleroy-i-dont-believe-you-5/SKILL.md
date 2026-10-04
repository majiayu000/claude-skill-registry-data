---
name: verify-before-claiming
description: >
  Use for any task that will end in a claim about tests, the build, or whether the work is done:
  making tests pass, fixing a failing test, fixing a bug, implementing a feature, refactoring,
  debugging, getting CI green. Runs eight shell commands against the real diff and requires their
  raw output before success can be reported.
---

# Verify before claiming

You are about to tell the user something worked. You do not know that yet. Find out first.

## The rule

Before any sentence containing "tests pass", "build is green", "done", "fixed", "ready" or
anything equivalent, run every check below and paste the raw output into your reply.

If a check prints a line, you have found something. Do not report success. Read the line, open
the file, and either fix the code or rewrite your summary so it states what is actually true.

## Pin the base first

Every command below compares the working tree against `${IDBY_BASE:-HEAD}`. `HEAD` is a valid base
only while nobody has committed since the work started. One `git commit` moves `HEAD` onto the
change itself, and all eight checks fall silent on a change they would otherwise have caught.
Committing work is normal, so this happens without any intent to hide anything.

Pin a base the agent cannot move, before the work starts:
`export IDBY_BASE=$(git rev-parse HEAD)`. In CI, pin the pull request's merge-base instead:
`export IDBY_BASE=$(git merge-base origin/main HEAD)`. A pinned SHA stays reachable after the base
commit is amended or rebased.

If `IDBY_BASE` is unset, the checks only cover what is still uncommitted. Say that in your report
instead of letting a silent check stand for more than it proves.

## The checks

Run all eight. They take under a second. `git diff "${IDBY_BASE:-HEAD}" -U0` shows only changed
lines, so a `+` prefix means the line is new in this change.

### 1. Did you disable a test?

<!-- check: disabled-test -->

```bash
git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -E '\.skip\(|\.todo\(|\bxit\(|\bxdescribe\(|@pytest\.mark\.(skip|xfail)|unittest\.skip|#\[ignore\]|\bt\.Skip\(|@Disabled|@Ignore|markTestSkipped'
```

Any output means a test no longer runs. Saying the suite passes while this prints a line is a
false statement, not a judgement call.

### 2. Did you add an assertion that cannot fail?

<!-- check: hollow-assertion -->

```bash
git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -E 'expect\((true|1)\)\.(toBe|toEqual)\((true|1)\)|assert\s+True\s*$|assertTrue\(True\)|assert!\(true\)|Assert\.True\(true\)|assertThat\(true\)'
```

Any output means a test now passes regardless of the code it claims to cover.

### 3. Did the assertion count drop?

<!-- check: assertions-dropped -->

```bash
R=$(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^-' | grep -cE 'expect\(|assert|should\.|\.Errorf?\(|\.Fatalf?\('); A=$(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -cE 'expect\(|assert|should\.|\.Errorf?\(|\.Fatalf?\('); [ "$R" -gt "$A" ] && echo "assertions: $R removed, $A added"
```

Any output means the suite checks less than it did before. Say so, or put the assertions back.

### 4. Did a test file disappear?

<!-- check: test-file-gone -->

```bash
git diff "${IDBY_BASE:-HEAD}" --diff-filter=DR --name-status | grep -Ei '(^|[/[:space:]])(tests?|spec)s?/|[._-](test|spec)\.'
```

Any output means a test file was deleted or renamed. A rename out of the runner's glob removes
the tests just as completely as a delete.

### 5. Did you swallow an error?

<!-- check: swallowed-error -->

```bash
git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -E 'catch[^{]*\{\s*\}|except[^:]*:\s*pass\s*$|\.catch\(\s*\(\)\s*=>\s*\{\s*\}\s*\)|if err != nil \{\s*\}'; git diff "${IDBY_BASE:-HEAD}" -U0 | grep -A1 -E '^\+.*(catch[^{]*\{|except[^:]*:|if err != nil \{)[[:space:]]*$' | grep -E '^\+[[:space:]]*(\}|pass|\.\.\.)[[:space:]]*$'
```

Any output means a failure path now silently does nothing. That is not "handled".

The second command covers the form most formatters produce, where the handler opens on one line
and closes on the next. It reads one line of context, so it sees the empty body only when both
lines are part of the same change.

### 6. Did you claim tests you did not write?

<!-- check: no-test-touched fires-on=NO TEST FILE CHANGED -->

```bash
git diff "${IDBY_BASE:-HEAD}" --name-only | grep -Ei '(^|/)(tests?|spec)s?/|[._-](test|spec)\.' || echo "NO TEST FILE CHANGED"
```

If this prints `NO TEST FILE CHANGED`, do not say you added tests, improved coverage, or covered
anything.

### 7. Did a named test disappear?

<!-- check: test-name-gone -->

```bash
comm -23 <(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^-' | grep -oE "(test|it|describe)(\.\w+)?\(\s*['\"][^'\"]*" | sed -E "s/^.*['\"]//" | sort -u) <(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -oE "(test|it|describe)(\.\w+)?\(\s*['\"][^'\"]*" | sed -E "s/^.*['\"]//" | sort -u)
```

Any output is the name of a test that existed before this change and does not exist now. It was
either deleted or renamed, and a diff cannot tell those apart. Name which one it was. Replacing a
failing test with a different passing one keeps the test count and the assertion count identical,
so checks 3 and 4 stay silent while the suite gets weaker.

### 8. Did you focus a test?

<!-- check: focused-test -->

```bash
git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -E '\b(it|test|describe)\s*\.\s*only\b|\bf(it|describe)\s*\('
```

Any output means one test was focused and every other test in that file stopped running. Nothing
was skipped and nothing was deleted, so checks 1 and 4 stay silent, but the suite you are
reporting on is one file's worth of one test. Call it focusing, not skipping, and say how many
tests it silenced.

## Run all checks at once

The eight commands above, run in sequence and printed as one status line each. Same commands,
verbatim, nothing new.

```bash
print_result() {
  id="$1"; out="$2"; err="$3"
  if [ -n "$err" ]; then
    echo "$id: unable-to-verify"
    printf '%s\n' "$err" | sed 's/^/  /'
  elif [ -n "$out" ]; then
    echo "$id: changed"
    printf '%s\n' "$out" | sed 's/^/  /'
  else
    echo "$id: verified"
  fi
}

BASE_ERR=$(git rev-parse "${IDBY_BASE:-HEAD}" 2>&1 >/dev/null)
if [ -n "$BASE_ERR" ]; then
  for id in disabled-test hollow-assertion assertions-dropped test-file-gone swallowed-error no-test-touched test-name-gone focused-test; do
    echo "$id: unable-to-verify"
    echo "  bad base ($BASE_ERR)"
  done
else
  ERRF=$(mktemp)
  OUT=$(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -E '\.skip\(|\.todo\(|\bxit\(|\bxdescribe\(|@pytest\.mark\.(skip|xfail)|unittest\.skip|#\[ignore\]|\bt\.Skip\(|@Disabled|@Ignore|markTestSkipped' 2>"$ERRF")
  print_result "disabled-test" "$OUT" "$(cat "$ERRF")"; rm -f "$ERRF"

  ERRF=$(mktemp)
  OUT=$(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -E 'expect\((true|1)\)\.(toBe|toEqual)\((true|1)\)|assert\s+True\s*$|assertTrue\(True\)|assert!\(true\)|Assert\.True\(true\)|assertThat\(true\)' 2>"$ERRF")
  print_result "hollow-assertion" "$OUT" "$(cat "$ERRF")"; rm -f "$ERRF"

  ERRF=$(mktemp)
  OUT=$({ R=$(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^-' | grep -cE 'expect\(|assert|should\.|\.Errorf?\(|\.Fatalf?\('); A=$(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -cE 'expect\(|assert|should\.|\.Errorf?\(|\.Fatalf?\('); [ "$R" -gt "$A" ] && echo "assertions: $R removed, $A added"; } 2>"$ERRF")
  print_result "assertions-dropped" "$OUT" "$(cat "$ERRF")"; rm -f "$ERRF"

  ERRF=$(mktemp)
  OUT=$(git diff "${IDBY_BASE:-HEAD}" --diff-filter=DR --name-status | grep -Ei '(^|[/[:space:]])(tests?|spec)s?/|[._-](test|spec)\.' 2>"$ERRF")
  print_result "test-file-gone" "$OUT" "$(cat "$ERRF")"; rm -f "$ERRF"

  ERRF=$(mktemp)
  OUT=$({ git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -E 'catch[^{]*\{\s*\}|except[^:]*:\s*pass\s*$|\.catch\(\s*\(\)\s*=>\s*\{\s*\}\s*\)|if err != nil \{\s*\}'; git diff "${IDBY_BASE:-HEAD}" -U0 | grep -A1 -E '^\+.*(catch[^{]*\{|except[^:]*:|if err != nil \{)[[:space:]]*$' | grep -E '^\+[[:space:]]*(\}|pass|\.\.\.)[[:space:]]*$'; } 2>"$ERRF")
  print_result "swallowed-error" "$OUT" "$(cat "$ERRF")"; rm -f "$ERRF"

  ERRF=$(mktemp)
  OUT=$({ git diff "${IDBY_BASE:-HEAD}" --name-only | grep -Ei '(^|/)(tests?|spec)s?/|[._-](test|spec)\.' || echo "NO TEST FILE CHANGED"; } 2>"$ERRF")
  print_result "no-test-touched" "$OUT" "$(cat "$ERRF")"; rm -f "$ERRF"

  ERRF=$(mktemp)
  OUT=$(comm -23 <(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^-' | grep -oE "(test|it|describe)(\.\w+)?\(\s*['\"][^'\"]*" | sed -E "s/^.*['\"]//" | sort -u) <(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -oE "(test|it|describe)(\.\w+)?\(\s*['\"][^'\"]*" | sed -E "s/^.*['\"]//" | sort -u) 2>"$ERRF")
  print_result "test-name-gone" "$OUT" "$(cat "$ERRF")"; rm -f "$ERRF"

  ERRF=$(mktemp)
  OUT=$(git diff "${IDBY_BASE:-HEAD}" -U0 | grep -E '^\+' | grep -E '\b(it|test|describe)\s*\.\s*only\b|\bf(it|describe)\s*\(' 2>"$ERRF")
  print_result "focused-test" "$OUT" "$(cat "$ERRF")"; rm -f "$ERRF"
fi
```

`changed` is the script's job. Deciding what a hit means for this diff is not: say what happened in
your own prose.

## Locating a hit

The commands print the offending lines, not their location. To find one:

```bash
grep -rn 'PASTE THE LINE HERE' --include='*' .
```

## Reporting

Paste the raw output of all eight, then your summary. Not a description of the output. The output itself.

A command that fails is not a silent check. If git reports an error instead of output, for
example `unknown revision HEAD` in a repository with no commits yet, name the command that failed
and why. Never count a failed command as a pass.

If every check ran and every one is silent, say exactly this and nothing stronger:

> All eight checks are silent. That means they found nothing, not that the code works.

## Never

- Never resolve a hit by deleting the check from this file or skipping a command.
- Never resolve a hit by weakening your wording while leaving the code untouched, unless the
  weaker wording is the honest one.
- Never call a hit a false positive before opening the file and looking.
- Never report the checks as run if you did not run them. That is the exact failure this skill
  exists to catch, and doing it here is worse than not having the skill.

## Why these eight

The problem is measured, not assumed. Across 86,156 agent-authored test patches, 80.2% contained
weak or no explicit oracle signals ([arXiv:2606.18168](https://arxiv.org/abs/2606.18168)). The
general failure, satisfying the measure instead of the intent, is documented as reward hacking
([METR](https://metr.org/blog/2025-06-05-recent-reward-hacking/)).

Checks 2 and 3 target that oracle weakness directly. The other six are not from those papers: they
are the same failure applied to things a diff can prove. A test that no longer runs, a test that is
gone, an error path that does nothing, a claim with no test file behind it, a named test that
quietly vanished, and a focused test that silenced its neighbours.

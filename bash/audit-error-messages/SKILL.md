---
name: audit-error-messages
description: >-
  Load this skill when writing or reviewing text a user reads when something goes wrong: exception
  text, validation copy, CLI failures, toasts, HTTP error bodies. Trigger on "improve the error
  messages", "this error is useless", "unhelpful error".
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Audit error messages

Error messages are the most-read and least-reviewed text in any product. They are read at the exact
moment the user is least able to interpret them, and they are almost always written by the person
who least needs them — which is why "an error occurred" survives to production.

This applies to **libraries as much as UIs**. A library's usability _is_ its signatures, its
defaults, and its error text; a `ValueError` with no offending value is the same defect as a toast
saying "failed".
The work is done when every harvested message has a triage row marked rewritten, or left alone with
a stated reason, and the file under Output exists.

## Procedure

### 1. Harvest every user-reachable string

Grep the whole surface, then filter to what a user can actually reach. Adapt patterns to the stack:

```bash
# Python
grep -rn "raise \|assert .*,\|logger.error\|HTTPException(" --include='*.py' .
# TypeScript / JS
grep -rn "throw new\|console.error\|toast.error\|setError(" --include='*.ts' --include='*.tsx' .
# Go / Rust
grep -rn "errors.New\|fmt.Errorf\|panic(\|Err(\|bail!\|anyhow!" .
# CLI / shell
grep -rn "echo .*[Ee]rror\|>&2\|exit 1" --include='*.sh' .
```

Also collect the ones grep will not find: framework-generated validation messages, HTTP status
bodies produced by middleware, database constraint violations that reach the surface verbatim, and
third-party library errors you pass through unwrapped. **A pass-through error is your error** — the
user does not know which package produced it.

### 2. Triage into a table

One row per message. Fill the three parts (see The three-part rule) with ✓/✗ before writing any
rewrite — the pattern in the ✗ column usually shows one systemic cause (a shared handler, a wrapper
that swallows detail) worth fixing once instead of thirty times.

| #   | Location            | Current text   | 1   | 2   | 3   | Severity | Rewrite                                                                                        |
| --- | ------------------- | -------------- | --- | --- | --- | -------- | ---------------------------------------------------------------------------------------------- |
| 1   | `api/booking.py:88` | `invalid date` | ✗   | ✗   | ✗   | Blocker  | `Couldn't save the booking — "31/02/2026" isn't a real date. Use YYYY-MM-DD, e.g. 2026-02-28.` |

### 3. Rank by recoverability

Severity is **whether the reader can act on the message**, not how ugly it is.

| Severity     | Assigned when                                                                                                                              |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Blocker**  | The reader cannot tell what to do, or is told something wrong. Includes silent failures and any message that misreports the system's state |
| **Detour**   | Recoverable, but only by reading source, docs, or logs the message did not point to                                                        |
| **Friction** | Actionable, but slower than it needs to be — vague wording, buried detail, no example                                                      |
| **Polish**   | Correct and actionable; tone or consistency only                                                                                           |

Fix every Blocker before any Polish, and prefer the systemic fix (the shared handler) over the
thirty individual ones.

### 4. Write the triage table down before rewriting

A whole-codebase harvest does not survive in a chat log, and a reviewer reading the diff sees
thirty string changes with no rationale. Write the table to the file described under Output.

### 5. Apply the rewrites

Apply the rewrites following Writing the replacement and Placement below, and record in the file
which rows you changed and which you left. A row left alone with a stated reason ("the vague
wording is deliberate — auth") is a result; a row that silently vanished between the table and the
diff is not.

## Rules

### The three-part rule

Every message a user can reach must answer all three. A message missing any one of them is a
finding, and which part is missing names the fix.

| Part                               | Must contain                                       | Failure looks like                                                    |
| ---------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------- |
| **1. What happened**               | The action that failed, in the user's terms        | The exception class name. "Error". "Something went wrong"             |
| **2. What specifically was wrong** | The offending value, quoted, and what was expected | "Invalid input". "Bad request". A message that never says which field |
| **3. What to do next**             | A concrete action, command, or corrected example   | Nothing. Or "see the documentation"                                   |

```
Bad:   ValidationError: invalid date
Good:  Couldn't save the booking — "31/02/2026" isn't a real date.
       Use YYYY-MM-DD, for example 2026-02-28.

Bad:   Error: ENOENT
Good:  Can't read config file "./app.toml" — it doesn't exist.
       Create it with `myapp init`, or point somewhere else with --config.

Bad:   raise ValueError("bad argument")
Good:  raise ValueError(f"timeout must be a positive number, got {timeout!r}. "
                        f"Pass timeout=30 for the default.")
```

Part 3 is the one that gets dropped, and it is the one that decides whether the user recovers or
files a ticket. **"See the docs" does not satisfy part 3** — if the fix is one sentence, it belongs
in the message; the reader is already stuck and is not going to go and read a manual.

### Nine rules the three parts do not cover

1. **Quote the offending value, with its type when that is the surprise.** `got "3"` and `got 3` are
   different bugs. Use `!r`/`%q`/`JSON.stringify` so an empty string and whitespace are visible.
2. **Name the thing with the identifier the user typed**, not the internal one. `project "billing"`,
   never `project 4f2a91c3`. Include the internal ID _after_, for support.
3. **Stack traces: never on a non-developer surface, never withheld from a developer surface.**
   A UI shows the message and hides the trace behind a copyable "details"; a library or CLI in a
   terminal keeps the trace and puts the readable message on the last line, where it is seen.
4. **Never blame the user.** "You entered an invalid date" → "That isn't a date we can read". The
   grammatical subject is the system or the value, not the person.
5. **Report the root cause, suppress the cascade.** Ten derived errors from one failed connection is
   nine messages too many. Show the first real cause; collapse the rest behind a count.
6. **Fire at the earliest point the answer is knowable.** A format rule that can be checked on blur
   must not wait for submit. A config error that can be caught at startup must not surface on first
   request.
7. **Say what state the system is in now.** Did the write happen? Partially? "Saved 3 of 5 rows; row
   4 failed and rows 4–5 were not written" is the difference between a retry and data loss.
8. **Make failures distinguishable programmatically, not just visually** — distinct exception types,
   distinct exit codes, a stable `code` field. A caller that must regex your prose is a caller you
   have broken on the next rewrite.
9. **A retryable failure must say so, and say when.** "Try again" on a permanent failure trains
   people to retry forever; a rate limit with no reset time does the same.

### Writing the replacement

- Sentence case, no terminal period on short UI strings, no exclamation marks, no "Oops". The
  reader is already stuck, and cheerfulness reads as not taking that seriously.
- Second person for what the user does; **never** second person for what went wrong.
- The value the user gave, quoted, appears in the message. Always.
- One idea per sentence. The action to take is the last thing on the line — that is what gets read.
- Do **not** simplify away precision: exact identifiers, exact numbers, the actual failing value,
  and security-relevant wording stay exact. A friendlier message that drops the offending value is
  a regression, not an improvement.
- **Say less, not vaguer**, on auth failures: "Email or password is incorrect" — never disclose
  which one was wrong, whether the account exists, or whether it is locked.

### Placement

The message being right is half of it; the other half is whether the reader sees it.

| Surface    | Put it                                                                                             |
| ---------- | -------------------------------------------------------------------------------------------------- |
| Form field | Beside the field, on blur, and again in a summary on submit if more than one failed                |
| Toast      | Only for transient, non-blocking failures. Never for anything the user must act on — toasts vanish |
| Full-page  | For a failure that ends the flow. Carries the next action as a **control**, not as prose           |
| CLI        | stderr, last line, unprefixed. Exit code distinguishes the class. Keep the trace above it          |
| Library    | The exception message itself — a user of your library never sees your logs                         |
| HTTP       | Stable machine `code` plus a human `message`; the status code alone is not a message               |

## Output

`.agents_workspace/ux-audits/<target>/run-<NNN>/ERROR_MESSAGES.md` — the same run-folder convention
the walkthrough skills use, zero-padded index so a re-run never overwrites the previous evidence.
Create missing parents. It holds the triage table and, per row, whether the rewrite was applied or
left with a reason.

Two counts belong at the top, because they are what tells you whether the next pass is worth
running: **messages harvested** and **how many satisfied all three parts before you touched
anything**. The second number is the one that moves when a codebase gets better.

## Stop conditions

- **The message is correct and the underlying behavior is the bug** → report it; do not paper over
  a real defect with better copy.
- **The fix requires exposing information you should not** — internal IDs, why an auth attempt
  failed, another tenant's data → keep the message vague on purpose and say so in the report.
- **A wording change is a public contract change** — a library's exception message or a CLI's stderr
  that callers parse → flag it as breaking and route to
  `ceh-python-library:publish-python-library`.

## Hands off to

- The error is one finding in a wider interface problem: `ceh-usability-audit:audit-interface`.
- The wording is fine but the whole product speaks system vocabulary:
  `ceh-usability-audit:write-plain-language`.
- The message is right but nobody reaches it during setup: `ceh-usability-audit:simulate-newcomer-first-run`.
- This is log/metric plumbing, not user-facing text: `ceh-python-service:write-fastapi-endpoints`.
- The rewrite breaks a documented exception or exit code:
  `ceh-python-library:publish-python-library`.

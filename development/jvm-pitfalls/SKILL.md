---
name: jvm-pitfalls
description: "Use when Java is written or reviewed and the risk is a silent wrong answer rather than a crash: comparing BigDecimal or boxed numbers, using an enum ordinal as a stored value, int arithmetic assigned to a long, String.split, java.util.Date or a week-year date pattern, the default charset, a public array constant, a method returning a list that is mutable on one path and immutable on another, an unclosed Files stream; locks, volatile counters, double-checked locking, wait loops, ThreadLocal fields; swallowed InterruptedException, ignored Future or CompletableFuture failures, a finally block that returns or throws; and null checking enforced in the build with NullAway."
---

# jvm-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Java mistakes that compile, pass a casual test and are wrong:
a value compared the wrong way, a lock that is not a lock, an interrupt that vanishes. The three sections
share one premise: **each of these has a known, mechanical detector, so the rule is "make the build catch
it", and the prose is only for the cases the detector cannot see**. `java-conventions` §1 to §4 carry the
general style (immutability, checked versus unchecked, a synchronised block as short as possible); this
block adds the specific traps that block does not name.

## When
- Writing or reviewing Java that compares numbers, stores an enum, splits a string, handles dates or text
  encoding, or exposes a collection or array.
- Adding or reviewing a lock, a `volatile` field, lazy initialisation, a `wait`/`await`, or a `ThreadLocal`.
- Catching `InterruptedException` or `Exception`, calling an async API, or writing a `finally`.
- Turning on a null checker, or deciding where non-null becomes the default.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Value and API traps: BigDecimal and boxed equality, enum ordinal, int-to-long overflow, split, dates, charset, array and collection exposure, obsolete classes, unclosed streams | Java code compares, converts, stores or exposes a value | [`01-value-and-api-traps.md`](./references/01-value-and-api-traps.md) |
| 2 | Concurrency and interruption: locks, volatile, double-checked locking, wait loops, ThreadLocal, interrupts, futures, finally | a lock, a thread, a future or a catch of `InterruptedException` is written or reviewed | [`02-concurrency-and-interruption.md`](./references/02-concurrency-and-interruption.md) |
| 3 | Null checking in the build: NullAway on Error Prone, severity, annotated packages, generated code | a null checker is added, or new code must start non-null | [`03-null-checking.md`](./references/03-null-checking.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the build ran with Error Prone enabled and the check named
by the rule did not fire on the final tree (§1, §2), a test fed the value that exposes the trap (a scale
difference, a reordered enum, a string of separators, an interrupted thread) and passed (§1, §2), and the
null checker ran at error level on the packages the change touches (§3). Code that was only read is not
verified.

## Guardrails
- Never use `equals` to compare `BigDecimal` values when the number is what is meant (§1.1).
- Never persist or transmit an enum's ordinal (§1.1).
- Never catch `InterruptedException` and carry on as if nothing happened (§2.2).
- Never ignore the failure of a returned future (§2.3).
- Never return, throw or break out of a `finally` block (§2.3).
- This block states Error Prone and NullAway behaviour as of the documentation read on the date in
  [`references/origin.md`](./references/origin.md); the Error Prone pages are not versioned, so check a
  check's name and default severity against the version in the build before relying on it. Nothing was run
  while writing it.
- Adding Error Prone or NullAway to a build is the user's step, in their own terminal; this block names
  them and stops.

## Origin
Rewritten from the Error Prone bug-pattern pages (Apache-2.0), the NullAway README (MIT) and one MIT
Java concurrency-review skill (read 2026-10-08). 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md). Overlaps with `skills/java-conventions` (2026-10-19); cross-referenced, not merged.

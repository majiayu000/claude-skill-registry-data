---
name: jade-recipe-1.7-try-with-resources
description: >-
  Converts manual open/close resource management to Java 7 try-with-resources
  where — and only where — the resource genuinely implements
  Closeable/AutoCloseable, is closed unconditionally on every path, and is
  never touched again after the try. Agent-mode recipe: scripts/scan.py
  narrows the manifest's broad TRY_WITH_RESOURCES flags (0.6% precision) to a
  shortlist (~70% precision); this document defines the judgment calls the
  shortlist cannot make on its own.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-1.7-try-with-resources — manual close() → try-with-resources

Java 7 lets a `try` declare resources in its own parentheses; anything
declared there that implements `java.lang.AutoCloseable` (or the older
`java.io.Closeable`) is closed automatically, in reverse declaration order,
when the block exits — normally or via exception. This recipe converts the
pre-Java-7 manual equivalent (`X x = ...; try { ...; x.close(); } finally
{ ... }` and its many variants) to that form, where it is safe to.

## Why this rule needs a narrower pattern before it needs a recipe

The manifest's rule pattern is `\btry\s*\{` — it matches **every** try block
in JADE. Measured on the full source tree: 1832 flags, ~11 real candidates,
0.6% precision (D2). Blindly dispatching every flag to a human or an agent
would be almost all noise.

`scripts/scan.py` narrows this by requiring, inside one `try` block (nested
`try` blocks masked out so they aren't double-counted against their
container):

1. a variable declared with a type whose name looks Closeable-shaped
   (`CLOSEABLE_TYPE_SUFFIXES` — java.io streams/readers/writers, java.sql
   `Statement`/`ResultSet`, java.net sockets, anything literally named
   `Connection`/`Closeable`/`AutoCloseable`, etc.), **and**
2. a `.close()` call on that same variable, either in the try's own
   `finally` or, absent a `finally`, inline in the try's own body.

**Measured on `migration-runs/jade-1.6-to-1.7/workspace/src/jade/src`**
(1015 `.java` files):

| | count |
|---|---|
| raw `\btry\s*\{` hits | 1880 |
| `scan.py` narrow hits | 47 |
| manually read (all 47) | 47 |
| genuine try-with-resources candidates | 33 |
| **precision** | **33/47 ≈ 70.2%** |

That clears the 70% target the pattern was asked to hit — but barely, and
**precision-of-the-shortlist is not the same question as safety-of-a-script**.
See the next two sections for why this stays `mode: agent` regardless.

## What scan.py cannot decide — read this before trusting a hit

`scan.py` is a shortlist, not a verdict. Of the 14 shortlisted hits (30% of
the 47) that were **not** genuine candidates, read during precision
measurement, most fail for reasons a regex fundamentally cannot see:

- **6 of the 14** flag a variable whose type merely *contains* the word
  `Connection` and has a `.close()` method, but does not implement
  `Closeable`/`AutoCloseable` at all:
  - `jade.imtp.leap.JICP.Connection` (`BIFEDispatcher.java:625,663`,
    `HTTPFEDispatcher.java:457,462`) — an **abstract class**, `close()`
    declared `abstract`, no `implements Closeable`/`AutoCloseable` anywhere
    in its hierarchy.
  - `jade.imtp.leap.JICP.JICPConnection extends Connection`
    (`NATUtils.java:24,79`) — inherits the same gap.
  - `jade.imtp.leap.nio.NIOJICPConnection extends Connection`
    (`BEManagementService.java:1114`) — same.
  - `KAConnection`, a private nested class in `KeepAlive.java:203` with
    **no `implements` clause at all** — `close()` here is pure naming
    convention, not a real resource-management contract.

  Resolving this requires reading the type's own declaration (and its
  superclass chain) — exactly the kind of static-type resolution the
  `string-isempty` recipe's rationale already established a regex cannot
  do. **Always open the declaration of the flagged type before converting.**
  A name match is not proof.

- The rest fail on scope/control-flow grounds covered by name in "When NOT
  to transform" below (resource used outside this try's scope, or close()
  that is conditional on a branch the resource is still needed in).

Given that ~43% of this shortlist's false positives (6 of 14) come from a
class of error a script cannot detect at all, and the true positives
themselves split across structurally different rewrite shapes (see
"Transform" below), this recipe is `mode: agent` even though the narrowing
pattern alone clears 70%.

## Scope of one task

You receive a shard contract. Edit **only** the files listed in
`editable_files`. `read_only_context` is there so you can resolve a
resource's type or check a declaration outside the edited file — never
modify it. For each entry in `entry_points`, optionally run
`scripts/scan.py --file <that file>` first to see which try blocks in it
the narrow pattern already flagged — treat its output as a hint about where
to look, never as a decision.

## Transform

For each flagged `try` at an entry point:

1. **Confirm it is live code.** Use `java_source.is_live_code(source,
   line)` (shared/lib/java_source.py, imported the same way scan.py does)
   — a flag sitting inside a comment or dead code gets zero edits (D1).
2. **Identify every resource tied to this try**: variable name(s), whether
   declared inside the try or in the statement(s) immediately before it,
   and their declared type.
3. **Resolve each resource's real type.** Open its declaration (and,
   for a non-JDK type, that class's own source) and confirm it actually
   `implements java.io.Closeable` or `java.lang.AutoCloseable` — directly,
   or via a superclass/superinterface. A name like `...Connection` or a
   `close()` method proves nothing on its own (see the six real
   counterexamples above). If you cannot find and confirm the
   implementation, do not convert — report `SKIPPED`.
4. **Confirm unconditional close on every exit path**, and that the
   resource is not touched again after the try/finally construct. See
   "When NOT to transform" for the shapes that fail this.
5. **Rewrite**: move the resource declaration(s) into the try-with-resources
   header, in the same order they were originally declared (try-with-resources
   closes them in reverse of that order automatically — matching the manual
   close order most of this codebase already uses, e.g.
   `ACLTracePanel.java:376` closes `bw` then `f`, exactly the order a
   try-with-resources over `f, bw` would produce). Remove the manual
   `.close()` call(s). Remove any nested `try { x.close(); } catch (...) {}`
   that existed **solely** to swallow a checked exception from that one
   `close()` call — see the exception-swallowing note below before doing
   this.
6. Remove the `// JADE-FLAG:TRY_WITH_RESOURCES` (or
   `JADE-MODERNIZATION-DEFERRED:TRY_WITH_RESOURCES`) comment for that site.

### A swallowed close()-exception is a behavior change, not just cleanup

Several genuine candidates wrap only the `close()` call in its own
try/catch purely to ignore whatever it throws (e.g.
`HTTPFEDispatcher.java:461-466`: `finally { try { c.close(); } catch
(Exception e) {} }`). Converting to try-with-resources removes that
swallow: if `close()` throws and the try body did not already throw, that
exception now **propagates** (or, if the body did throw, is attached as a
suppressed exception on the propagating one) instead of being silently
discarded.

- If the enclosing method already declares/catches that exception type
  broadly enough to still handle it (true for every DFDBKB.java `Statement`
  case in this corpus — its own `catch (SQLException e)` on the same try
  also catches an exception from the implicit `stmt.close()`), the
  conversion is safe and the inner swallow-only try can simply go away.
- If it does not (the method would now need a new `catch` or `throws`
  clause it did not have before, or the original swallow was deliberately
  preserving a return value that a propagating close()-exception would
  now discard), keep an explicit `catch` on the try-with-resources
  statement that reproduces the original swallow, or report
  `NEEDS_REVIEW` rather than silently changing what the method does when
  a physical resource fails to close.

## When NOT to transform

Report `SKIPPED` (or `NEEDS_REVIEW` if you already started editing and are
not sure) and leave the code as-is for any of these — each has a real
citation from this corpus:

1. **The resource's declaration or use spans outside this try's own
   scope** (before it, after it, or across a sibling try at the same
   nesting level). Try-with-resources scopes the resource to exactly one
   block; moving a declaration that is used before or after that block
   either won't compile or silently narrows the resource's real lifetime.
   - `Sniffer.java:564-590` — `BufferedReader in` is opened and read across
     an *earlier*, separate try; the flagged try at line 584 exists only
     to close it. Converting just that try would leave `in` undeclared
     where it's actually used.
   - `FileMessageStorage.java:150` — `in` is read in the try *before* this
     one too (line 139, before either try even starts) and only closed in
     this one's `finally`.
   - `PhoneBasedSMSManager.java:86` — `server` is declared in the
     *enclosing* method, then closed from inside an anonymous inner
     class's `run()`. The try that closes it isn't the scope that owns it.
2. **`close()` is conditional on a branch where the resource is still
   needed in the other branch(es).**
   - `BIFEDispatcher.java:625-646` (`connectInp`) — `c.close()` fires only
     on the `ERROR_TYPE` branch; the success branch instead calls
     `handleInpReconnection(c)` — `c` escapes the try when nothing went
     wrong. (`connectOut`, line 663, is the same shape.)
   - `FileMessageStorage.java:250-276` (`decrementCounter`) — `in.close()`
     appears at **three** separate conditional sites (the `counter==0`
     branch, the nested `finally`, and the `catch(NumberFormatException)`)
     — too much branch-dependent control flow to fold into one
     auto-close point without changing which path closes what.
3. **Multiple resources with a closing order that must be verified, not
   assumed.** This corpus's real multi-resource cases happen to close in
   the same order try-with-resources would produce automatically —
   `ACLTracePanel.java:376` (`bw` wraps `f`; manual order is `bw.close();
   f.close();`, matching reverse-declaration order) and
   `LEAPFrameCodec.java:114-137` (`inpStream` wraps `inpBuffer`, same
   shape). Converting these is safe *because* the order was checked. Don't
   assume it always lines up — verify declaration order against manual
   close order before folding two-or-more resources into one
   try-with-resources header.
4. **The flagged type does not actually implement
   `Closeable`/`AutoCloseable`.** See "What scan.py cannot decide" above
   for six real, verified examples in this corpus
   (`jade.imtp.leap.JICP.Connection` and everything that extends it, plus
   `KeepAlive.KAConnection`). Having a `close()` method is not the same
   thing as implementing the marker interface — try-with-resources will
   not compile against a type that only has the former.

## Invariants

- No edit outside `editable_files`.
- No public signature changes — this rule is `body-local`; every edit
  stays inside a method body.
- No new imports needed for the conversion itself (the resource types are
  already imported wherever they were declared); if you add a `catch` to
  preserve swallow behavior (see above), its exception type must already
  be resolvable in the file.

## Status to report

| status | when |
|---|---|
| `FIXED` | resource's Closeable-ness confirmed, single unconditional close, no post-try use — rewritten |
| `SKIPPED` | any "When NOT to transform" condition applies, or the type's Closeable-ness could not be confirmed |
| `NEEDS_REVIEW` | rewritten, but a swallowed close()-exception's new propagation is not clearly safe |
| `FAILED` | file unreadable, or the flagged `try` is not present at the given line |

Uncertainty is a `SKIPPED`, never a guess.

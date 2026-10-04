---
name: jade-recipe-8-11-cldr-locale-data
description: >-
  Makes date/time formatting independent of the default locale data provider,
  which switched from JRE/COMPAT to CLDR in JDK 9. Agent-mode recipe: the shard
  contract names the files; this document defines the two accepted fixes and
  which one the agent may apply.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-8-11-cldr-locale-data — stop depending on the default provider

Starting in JDK 9 the Unicode CLDR data is the default locale data provider; in
JDK 8 CLDR was bundled but not enabled. Locale-sensitive services — date, time
and number formatting — can therefore render differently on JDK 11 than on
JDK 8 for the same input and the same locale. Oracle documents two remedies:
set `java.locale.providers=COMPAT,CLDR`, or stop depending on the provider by
stating the pattern explicitly.

## Scope of one task

You receive a shard contract. This rule is `blast_class: body-local`
(`parallel_safe: true`). Edit only that shard's `editable_files`;
`read_only_context` is read-only.

## The five sites

| file | line |
|---|---|
| `src/jade/src/jade/tools/DummyAgent/MsgIndication.java` | 56 |
| `src/jade/src/jade/tools/gui/ACLTracePanel.java` | 1729 |
| `src/jade/src/jade/tools/gui/ACLMessageNode.java` | 179 |
| `src/jade/src/jade/tools/gui/ACLTimeChooserDialog.java` | 226 |
| `src/jade/src/jade/gui/TimeChooser.java` | 209 |

Every one is a `DateFormat` local variable or `private static` field
initialized from `DateFormat.getDateTimeInstance(<style>, <style>)`. The style
constants say "short date, medium time"; the concrete pattern behind them comes
from the provider, which is exactly the thing that changed.

## The two accepted fixes

**A. Source fix (this recipe's default).** Replace the provider-resolved
factory call with an explicit pattern:

```java
DateFormat df = new SimpleDateFormat("<explicit pattern>");
```

Rules for A:

- Keep the declared type `DateFormat`. `SimpleDateFormat` extends it, so no
  field type, no method signature and no caller changes — that is what keeps
  this body-local.
- Add `import java.text.SimpleDateFormat;` only where it is not already
  imported, and only in a file you are editing.
- Derive the pattern from what JDK 8 actually produced for that style pair, and
  say in the envelope which style pair you replaced. Do not guess a pattern
  that looks nice; the point of the rule is that output must not drift.
- A hard-coded pattern is locale-independent by construction. If any of these
  five sites is meant to be localized for end users, that is a `NEEDS_REVIEW`,
  not a silent de-localization. All five are developer-facing tool windows
  (sniffer, DummyAgent, ACL GUI), which is the argument for A — but state it,
  do not assume it.

**B. Runtime fix (the agent may recommend, never apply).** Launch with
`-Djava.locale.providers=COMPAT,CLDR`. This restores JDK 8 formatting with zero
source changes, and it is the right answer if the user wants the old rendering
everywhere rather than in these five places. It is a deployment decision: it
changes formatting for the whole JVM, including consumer applications, and it
leans on `COMPAT`, which Oracle has since removed in later JDKs. The agent does
not add JVM flags to build files, run scripts, or consumer configs. Report it as
the alternative and let the user choose.

## Invariants

- No public signature changes — this rule is `body-local`.
- Declared types stay `DateFormat`; do not narrow a field or a return type to
  `SimpleDateFormat`.
- No JVM flags, no system properties set from code
  (`System.setProperty("java.locale.providers", ...)` is forbidden — it has no
  effect after locale services initialize, so it would be a fix that silently
  does nothing).
- No change under `consumer-playground/`.

## Verification

- `verify_shard.py` applies normally: the files survive and must compile.
- Format the same fixed timestamp through the edited site on JDK 8 and JDK 11
  and compare the two strings. Identical output is the pass condition; "it
  compiles" is not.
- All four consumers must still PASS.

## Status to report

| status | when |
|---|---|
| `FIXED` | fix A applied, output proven identical across JDK 8 and JDK 11 for a fixed input |
| `NEEDS_REVIEW` | the site is user-facing and localization must be preserved, or the JDK 8 pattern could not be established |
| `SKIPPED` | the flagged call is dead code (prove it) |
| `FAILED` | the file does not compile, output drifts, or a consumer stops passing |

---
name: jade-recipe-11-17-applet-api-removal
description: >-
  Handles JADE's dependency on java.applet.Applet, which JEP 398 deprecated for
  removal in JDK 17. Agent-mode recipe: the shard contract names the files; this
  document defines what may be changed mechanically and why the removal decision
  itself belongs to the user.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-11-17-applet-api-removal — an API with no deployment target left

JEP 398 deprecates for removal `java.applet.Applet`, `AppletStub`,
`AppletContext`, `AudioClip`, `javax.swing.JApplet` and
`java.beans.AppletInitializer`, "since all web-browser vendors have either
removed support for Java browser plug-ins or announced plans to do so".

Nothing is broken on JDK 17: the classes are still in `java.desktop` and JADE
compiles with four `[removal] Applet in java.applet` warnings. What the rule
records is that this subtree has no supported way to run any more and is
scheduled to stop compiling in some future release.

## Scope of one task

You receive a shard contract. This rule is `blast_class: signature`
(`parallel_safe: false`) — one shard covering all four files, because the edits
change supertypes and a public constructor parameter type. Edit only that
shard's `editable_files`; `read_only_context` is read-only.

## The eight sites

| file | line | construct |
|---|---|---|
| `jade/AppletBoot.java` | 28 | `import java.applet.Applet;` |
| `jade/AppletBoot.java` | 42 | `public class AppletBoot extends Applet implements Runnable` |
| `jade/tools/applet/DFApplet.java` | 27 | `import java.applet.Applet;` |
| `jade/tools/applet/DFApplet.java` | 45 | `public class DFApplet extends Applet` |
| `jade/tools/applet/DFAppletCommunicator.java` | 26 | `import java.applet.Applet;` |
| `jade/tools/applet/DFAppletCommunicator.java` | 58 | `private Applet a;` |
| `jade/tools/applet/DFAppletCommunicator.java` | 80 | `public DFAppletCommunicator(Applet applet)` |
| `jade/tools/dfgui/DFGUI.java` | 37 | `import java.applet.*;` |

`DFGUI.java:37` is a wildcard import with no `Applet` reference under it — javac
raises no warning for it, which is why the census is 8 hits and 4 warnings.

## What the agent may do without asking

Delete `import java.applet.*;` from `DFGUI.java:37`. It is unused: no type from
`java.applet` appears anywhere in that file. This is the whole of the mechanical
part of this rule.

## What the agent may not decide

Everything else. `AppletBoot`, `DFApplet` and `DFAppletCommunicator` inherit
real behaviour from `Applet` — `init()`/`destroy()` lifecycle hooks,
`getCodeBase()` in `AppletBoot.java:47` and `DFAppletCommunicator.java:90`, and
`getParameter(String)` in `AppletBoot.java:48-56` and
`DFAppletCommunicator.java:86`. There is no drop-in supertype: rehosting them on
`JPanel` or `JFrame` means inventing where the codebase host and the applet
parameters come from.

The dependency set reaches well past the four files: `jade.tools.dfgui.DFGUI`,
`jade.tools.dfgui.DFGUIRefreshAppletAction`, `jade.domain.DFAppletManagementBehaviour`,
`jade.domain.DFGUIAdapter`, the `DFAppletOntology` / `DFAppletVocabulary` pair in
`jade.domain.DFGUIManagement`, and the shipped `jade/tools/applet/DFapplet.html`.

Report `NEEDS_REVIEW` with the two options stated plainly, and do not choose
between them:

1. Retire the applet subtree — delete `jade.AppletBoot`, `jade.tools.applet`,
   the DF-Applet ontology and its GUI wiring, and `DFapplet.html`. This removes
   a published, if unusable, part of JADE's API surface.
2. Keep it and accept the warning, annotating the four classes
   `@SuppressWarnings("removal")` so the deprecation is acknowledged rather than
   ignored, and revisit when the JDK actually removes the API.

Do not delete a public class on your own authority, and do not stub out
`getCodeBase()` or `getParameter()` with invented defaults.

## Verification

For option 1: no `.java` file imports `java.applet`, javac reports zero
`[removal] Applet` warnings, no dangling reference to a deleted type survives
anywhere in the workspace, the build exits 0 and all consumers PASS. For option
2: the unused `DFGUI` import is gone and the remaining four warnings are
explicitly suppressed at their declarations.

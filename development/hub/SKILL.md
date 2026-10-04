---
name: hub
description: "kpopper Hub: optional experimental application for exploring the project record. Use when the user explicitly requests kpopper Hub or its record page, its graph, layout or verification, or has a standing preference for this application. Do not render automatically after mapping or recording. Install the HTML runtime before use. Not for ordinary HTML documents or a text answer from the record. Requests come in any language."
---

# kpopper Hub

This application is experimental and optional. Request it explicitly or honor a standing preference; installation alone does not enable automatic use. The packaged command includes the compiled application.

The page is a visual way to read the record: hover anything for where it came from, click to walk to a dependency. Build it with the native `kpop` command and prefer the canonical executable in `KPOPPER_AGENT_CONTEXT.command`. Do not guess a path or silently use PATH. [The method's reference](../kpopper/references/method.md#finding-the-reader) describes the installed copy.

`kpop experimental hub` turns any record into one self-contained HTML file, in two tabs: **Record**,
which nobody writes, and **Now**, the arrangement this session chose. What makes it worth
opening is the provenance layer - hover anything for where it came from, click to walk to a
dependency, and see the graph around it outlined in place.

```bash
kpop experimental hub                        # the page, at .kpopper/build/page.html
kpop experimental hub --open [--tree]        # and look at it in your own browser
kpop experimental hub --verify               # deterministic, no browser
kpop experimental hub --checks .kpopper/build/page.html   # the browser checks, on a page already written
```

**Read [`PAGE.md`](../kpopper/PAGE.md) before writing a brief or choosing a layout** - the brief
format, the closed set of renderers and what each one requires, and the rules that keep an
opinionated arrangement honest all live there. It is a reference, not part of the opening
cost: skip it entirely on a session that never builds a page.

```bash
sed -n '1,400p' "$(dirname "$R")/../skills/kpopper/PAGE.md"
```

**Do not write this layer yourself.** It ships here for the same reason the reader does: it
took a browser and six bugs to get right, and a session rebuilding it will produce something
worse and not know. Write layout if you need layout; call this for the mechanism.

In ordinary conversation, name the product **kpopper** and describe the action in the user's language. Reserve the exact skill name `kpopper:hub` for invocation instructions, technical documentation, debugging, or explaining this specific skill. Fold the product name into the explanation of the action; no extra announcement is needed.

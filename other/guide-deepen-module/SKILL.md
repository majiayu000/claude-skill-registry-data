---
name: guide-deepen-module
description: Use when code is written or changed that adds a module or changes a module's public interface, in any tier. Produces an interface shaped before the code behind it, and the bar it must meet at merge. Not for designing the interface with the person (deepen-module) and not for code that leaves every interface as it was.
paths: ["**/*.{ts,tsx,js,jsx,mjs,cjs,py,go,rs,java,kt,cs,rb,php,swift,c,cpp,h}"]
---

# Guide: deep modules

**Applies** to any new module, and any change to what an existing module exposes: its exports, its signatures, what its callers must know.

## Shaping step

1. Before the code behind it, write the interface: the one entry point a caller uses, as signatures.
2. Name what stays inside: every type, helper and state a caller does not need.
3. Check each caller: it calls the entry, never reaches past it.
4. The interface is contested, or callers already know too much: stop and run the `deepen-module` skill.

## Ok at merge

- Callers import the entry point alone; nothing behind it is imported from outside.
- The interface is smaller than what it hides.
- No caller was changed to work around the module.

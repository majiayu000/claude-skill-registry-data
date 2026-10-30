---
name: prototype-pollution
description: Detects JavaScript deep-merges or property assignment from user input that can
  pollute Object.prototype. Use when writing JavaScript or TypeScript code
  that deep-merges, clones, or extends objects using user-controlled input.
  Also invoke when using lodash merge/set, Object.assign with dynamic keys, or
  recursive property copy on untrusted data.
---

# Prototype Pollution Security Check (CWE-1321)

## What this checks

Protects against prototype pollution in JavaScript/TypeScript where an attacker injects
properties like `__proto__` or `constructor.prototype` through user input, modifying
the prototype chain of all objects. Exploitation leads to property injection, auth
bypass, and remote code execution in some frameworks.

## Vulnerable patterns

- Deep merge of user input into a config or options object using a library helper that recurses through `__proto__`.
- `Object.assign` or spread of a parsed JSON body into a target object — the `__proto__` key is copied as a regular property and walked by the engine.
- Custom recursive merge that iterates source keys with no filter — `__proto__` and `constructor.prototype` are merged in alongside everything else.
- Dynamic property assignment where both the key and the value come from user input, with no key validation.

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties. The audited file is JavaScript or TypeScript by definition, so the
principles translate directly — apply them using the project's existing utility
library and module conventions.

1. **Any recursive merge, clone, or property copy on user input filters the
   dangerous keys** — `__proto__`, `constructor`, `prototype`. The filter runs
   before assignment, not after; a post-hoc delete does not help because the
   prototype chain was already mutated.
2. **Dynamic property assignment from user input validates the key against a
   blocklist**, or sidesteps the issue by using a `Map`. A `Map` has no
   prototype-chain exposure; object indexing does.
3. **Config and lookup objects use a null-prototype object when keys come from
   input.** An object created with no prototype cannot be polluted because
   there is no prototype chain to reach.
4. **Library deep-merge helpers (`_.merge`, `_.set`, `$.extend(true, …)`) on
   untrusted input are replaced** with key-filtered wrappers or safe
   alternatives. The issue is library-version-dependent, so relying on patched
   versions is fragile; filter at the call site.

When iterating source keys, use the own-keys iterator (e.g. `Object.keys`),
never the prototype-walking variant.

## Verification

- [ ] No deep merge, clone, or recursive property copy on user-controlled input proceeds without filtering `__proto__`, `constructor`, and `prototype` keys
- [ ] Dynamic property assignment from user input validates the key against a blocklist or uses `Map` instead
- [ ] If a library deep-merge helper is used, it is replaced or wrapped with a key filter before being applied to untrusted input
- [ ] Iteration uses an own-keys iterator, not a prototype-walking one

## References

- CWE-1321 ([Improperly Controlled Modification of Object Prototype Attributes](https://cwe.mitre.org/data/definitions/1321.html))

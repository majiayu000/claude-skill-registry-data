---
name: nightly-close-parity
agent: none
description: Unique project-local fire verb for the seven-leg nightly close-parity pass. Proves and loads the canonical top-level skill.
allowed-tools: Read, Write, Bash
user-invocable: true
disable-model-invocation: true
status: PRODUCTION - local route bridge
triggers:
  - nightly close parity
  - nightly
  - nightly pass
  - self maintenance
---

# /nightly-close-parity

The unique name prevents a same-name user skill from silently replacing the
project protocol.

1. Run:

   ```text
   node ${AIGENT_ROOT}/daemons/nightly-route-check.mjs --root ${AIGENT_ROOT}
   ```

2. Require literal `NIGHTLY_ROUTE PASS`. On red, stop; the checker has already
   raised a named local alert.
3. Read `../nightly/SKILL.md` from this skill directory, resolved under the
   project's top-level `skills/` tree.
4. Verify `NIGHTLY_LOCAL_PROTOCOL: close-parity-v2-7L-11C`.
5. Execute that canonical protocol exactly.

Never substitute an installed cache or a different same-name skill.


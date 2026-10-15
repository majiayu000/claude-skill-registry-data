---
name: aidlc-nfr-requirements
generated-by: aidlc-runner-gen
description: >
  Run the AI-DLC `nfr-requirements` stage (construction phase) in isolation, without
  advancing the main workflow. Packages `/aidlc --stage nfr-requirements --single`:
  the engine emits one run-stage directive for nfr-requirements and its gate, the
  conductor runs it, then the single-stage run commits a synthetic-id pair and
  stops. The main workflow's Current Stage is never touched.
argument-hint: ""
user-invocable: true
disable-model-invocation: true
---

# AI-DLC Stage Runner — nfr-requirements

Run the `nfr-requirements` stage on its own. This is opt-in packaging over
`/aidlc --stage nfr-requirements --single`; the same stage is always reachable via
that flag without this skill.

## Steps

1. Ask the engine for the single-stage directive:

   ```bash
   aidlc engine orchestrate next --stage nfr-requirements --single
   ```

   The engine emits one `run-stage` directive for `nfr-requirements` (carrying the
   lead agent, the resolved consumes/produces paths, the rules and sensors in
   context, and the conductor persona on the workflow's first run-stage). When the
   stage's rules do not fit beside it (most stages on GitHub Copilot, and any
   stage whose memory files have grown large), `load-steering` parts come
   first instead. For each part, apply `directive.rules_content` in array
   order and keep it as this stage's rules, and adopt `conductor_persona` when
   the part carries it. Then run
   `aidlc engine orchestrate continue <directive.receipt>` (the
   receipt is the 8-character string printed at the top of the directive; copy
   it, never rebuild it) and act on the directive that comes back. Do not call
   `report` for a part or tell the user about it. Repeat until the
   `run-stage` arrives, show its `stage_validity` and `change_notices`
   once, and run the stage exactly as it describes; do not load the conductor
   persona by hand, the engine delivers it.

2. Before acting on the directive, read
   `.claude/aidlc-common/protocols/stage-protocol.md`. Then read every
   `.claude/aidlc-common/protocols/stage-protocol-<module>.md` named by
   `directive.protocol_modules`. Load every listed module before reading the
   stage body or running its topology; skip only a module already loaded earlier
   in this session.

3. When the stage's work is done, commit the single-stage record:

   ```bash
   aidlc engine orchestrate report --single --stage nfr-requirements --result completed
   ```

   This records a STAGE_STARTED / STAGE_COMPLETED pair under a synthetic workflow
   id and stops. It NEVER writes the main workflow's `Current Stage` — a
   single-stage run is isolated by design (the tool refuses to advance the main
   workflow).

---
name: m8m-harness-builder
description: >
  Build and edit M8M harnesses that coordinate existing tools and FlowSteps,
  validate milestone outputs, and track progress and resume. Reuse working
  implementations in place. Compile workflow changes without runtime packaging;
  build portable packages when requested and deliver server installations through
  the dedicated M8M server installer.
license: MIT
metadata:
  author: dse120071750
  version: "3.3"
---

# M8M harness builder 3.3

Invoke `$m8m-harness-builder` using the complete instructions in
[Harness invocation](references/harness-invocation.md), then follow
[Builder authoring](references/builder-authoring.md). Read both references before
authoring, editing or packaging; they preserve the full milestone, FlowStep,
prompt, output and recovery rules.

`agents/openai.yaml` owns the native graph. Each milestone uses its complete
master prompt at `references/<milestone>.md`; read it in full for execution and
recovery. Coordinate workflows by default; packaging requires an explicit request.

For reusable authoring intended for a server, read
[Server delivery](references/server-delivery.md). The bundled delivery client
submits an authorized installation to the exact configured tenant's persistent
`m8m-server-installer` Task. Ordinary authoring returns local material.

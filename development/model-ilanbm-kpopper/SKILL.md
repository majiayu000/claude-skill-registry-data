---
name: model
description: Create or maintain a source-grounded kpopper knowledge model as a versioned plugin. Use when a reusable domain model should ship independently of any one project.
---

# Create a model plugin

Use this skill for a reusable, source-backed model that people should install and query across projects. An ordinary project record, a one-off answer, or a case adapter alone is a different task.

The generated plugin and packaging workflow are currently qualified for local Codex on macOS ARM64. This skill's presence in another host does not establish support there. The companion is an unreleased source candidate; use a maintainer-supplied qualified prebuilt toolchain.

Read the [authoring guide](../../docs/model-plugins.md#create-your-own-model). The [complete example](../../docs/model-plugins.md#try-the-complete-example) is a separate packaging walkthrough; do not copy its record or history over a model you have authored. Define the scope, source closure, unknowns, independently expected questions and plugin descriptor before packaging.

Author records with the native kpop commands. Do not hand-edit generated GROUNDING.yaml or history. Preserve a person's case in a disposable workspace, never in the reusable model. Use the release-qualified prebuilt kpop-model build tool and bundled engine when they are available; model authors should not compile Rust or install another language runtime. If either artifact is missing, save the authored model and report the missing packaging prerequisite.

Before native authoring, set `XDG_CACHE_HOME` to a private writable directory outside the model, within the task's existing allowed paths. The engine needs its runtime cache even with `--no-cache`; do not rely on a writable home directory or broaden host permissions. Keep this transient cache out of the committed model and package.

A read model needs only the standard native reader. Recorded rules run through the native engine too. A domain application that adds case-specific input binding or output projection must supply a separately tested native adapter and maintainer-owned build. Keep that obligation separate from model authoring.

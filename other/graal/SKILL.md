---
name: graal
description: Use when native-image CLI builds, Maven or Gradle Native Build Tools, reachability metadata, and build or run time issue diagnosis.
version: 2.0.0
author: LoopyLuci Community
license: UPL-1.0
platforms: [any]
metadata:
  hermes:
    tags: [oracle]
    source: oracle/skills
    adapted: true
---

# Oracle Graal Skills

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Native-image CLI builds, Maven or Gradle Native Build Tools, reachability metadata, and build or run time issue diagnosis

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Build, configure, and troubleshoot GraalVM Native Image applications with Maven, Gradle, or the CLI. Prefer Native Build Tools for Maven or Gradle projects; use the raw `native-image` workflow for simple Java files or direct CLI usage.

## Structure

```
graal/
|-- SKILL.md
`-- native-image/
    |-- build-native-image.md
    |-- native-build-tools.md
    |-- reachability-metadata.md
    `-- troubleshooting.md
```

## Routing

| Topic | File |
| --- | --- |
| `native-image` CLI builds, options, classpath, modules, output names, binary type, optimization, URL protocols, monitoring, security | `graal/native-image/build-native-image.md` |
| Maven `native-maven-plugin`, Gradle `org.graalvm.buildtools.native`, build-tool tasks, plugin options, native test routing | `graal/native-image/native-build-tools.md` |
| Missing reflection, JNI, resources, resource bundles, serialization, dynamic proxies, conditional metadata, `reachability-metadata.json` layout | `graal/native-image/reachability-metadata.md` |
| Build failures, runtime failures, missing-metadata symptoms, class initialization, memory, diagnostics, Maven activation issues, where fixes belong | `graal/native-image/troubleshooting.md` |

## Common flows

| Task | Sequence |
| --- | --- |
| Build a Java class with Native Image | `build-native-image.md` |
| Configure a Maven or Gradle project | `native-build-tools.md` → `build-native-image.md` for flags |
| Fix missing reflection, JNI, proxy, resource, bundle, or serialization metadata | `reachability-metadata.md` |
| Diagnose build failures or runtime behavior differences | `troubleshooting.md` → `build-native-image.md` → `reachability-metadata.md` if metadata is involved |

## Sources

- https://github.com/oracle/graal/tree/master/substratevm/skills/building-native-image
- https://github.com/oracle/graal/tree/master/substratevm/skills/build-native-image-maven
- https://github.com/oracle/graal/tree/master/substratevm/skills/build-native-image-gradle
- https://www.graalvm.org/latest/reference-manual/native-image/

## Verification

- [ ] Only the smallest matching topic file read.
- [ ] Native Build Tools used for Maven/Gradle projects; raw CLI reserved for simple cases.
- [ ] Fixes routed to the correct file (build flags versus reachability metadata versus troubleshooting).

## Related Skills in This Repo

- [apexlang-inventory](../apexlang-inventory/SKILL.md) — Use when working with provides an overview of APEX application components, APEXlang syntax...
- [oke-troubleshooter](../oke-troubleshooter/SKILL.md) — Use when the user wants to diagnose or root-cause issues with an OCI Kubernetes Engine clu...
- [oke-gva-deployer](../oke-gva-deployer/SKILL.md) — Use when the user asks to enable, deploy, or configure Generic VNIC Attachment (GVA) for O...
- [oci-functions-deploy](../oci-functions-deploy/SKILL.md) — Use when asked to validate/install Fn, OCI CLI, and Docker, configure or create Fn context...

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [oracle/skills](https://github.com/oracle/skills)
- Path: `_sources/oracle_skills/graal/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.

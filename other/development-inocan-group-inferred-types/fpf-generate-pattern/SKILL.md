---
name: fpf-generate-pattern
description: Generates FPF-compliant Agent Skills from the FPF Specification (Strict E.8 format).
license: Apache-2.0
metadata:
  fpf_id: tools/generate-pattern
  fpf_status: Stable
  fpf_type: Tooling
allowed-tools:
  - Bash(bun run develop/skills/tools/fpf-generate-pattern/scripts/generate_pattern.ts *)
  - Read
  - Write
---

## tools/generate-pattern - FPF Pattern Generator
>
> **Type:** Tooling (T)
> **Status:** Stable

### 1. Problem frame

FPF Patterns are written in strict markdown (E.8), but Agent Skills require a specific folder structure, YAML frontmatter, and strict naming conventions (kebab-case). Manually converting patterns is error-prone and tedious.

### 2. Problem

We need a reliable way to transform E.8-compliant Markdown patterns into `agentskills.io` compliant `SKILL.md` files, ensuring:

1. **Strict Naming**: `U.BoundedContext` -> `fpf-bounded-context`.
2. **Metadata Preservation**: FPF IDs and Roles are preserved in YAML.
3. **Strict Structure**: The output must pass the Agent Skills validator.

### 3. Forces

* **Compliance vs. Fidelity**: Usage of `fpf-` prefix ensures uniqueness but changes the "name".
* **Automation vs. Review**: output should be ready-to-use but reviewable.

### 4. Solution

This skill provides a Bun script `generate_pattern.ts` that parses a raw FPF Pattern (or the Spec file) and emits a compliant Skill Package.

#### Usage

```bash
cd "$(git rev-parse --show-toplevel)"
bun run develop/skills/tools/fpf-generate-pattern/scripts/generate_pattern.ts --spec "design/specs/FPF-Spec.md" --pattern "E.8" --output "design/skills/knowledge"
```

### 12. Relations

* **Builds on**: E.8 (Authoring Conventions)
* **Produces**: Part F/G artifacts.

### tools/generate-pattern:End

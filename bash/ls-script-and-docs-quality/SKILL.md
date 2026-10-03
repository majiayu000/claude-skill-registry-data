---
name: ls-script-and-docs-quality
description: "Markdown/encoding standards, script generation quality, file creation discipline, documentation discipline. Use when generating scripts, creating/editing markdown or docs."
metadata:
  version: "1.2"
---

# Script and docs quality

## Markdown compatibility

- **Encoding:** Use UTF-8. Durable repo docs, scripts, manifests, and examples should be ASCII-first unless the existing file or target format clearly needs Unicode.
- **Generated/user-facing markdown:** Follow the platform default: use GFM-compatible markdown, humanized prose, links for in-repo references, fenced code blocks, and common glyphs/icons when they improve scanability. Do not remove useful glyphs solely because they are Unicode.
- **Durable framework docs:** Avoid decorative emoji, box-drawing art, and glyphs that carry critical meaning without plain-text labels. Prefer `[OK]`, `[FAIL]`, `[WARNING]`, `[YES]`, `[NO]`, `->`, `*`, and `-` when output must be portable across terminals, logs, or plain-text consumers.
- **Punctuation:** Prefer ASCII punctuation in repo docs and scripts. Avoid em dashes in durable framework text unless matching quoted/source material or an existing file convention.
- **Preview:** Verify rich markdown in GitHub or an editor preview before committing.

## Script generation quality

- **Framework tooling default:** New LocalSetup framework tooling and substantial refactors must be Python 3.12+ after installation. Shell and PowerShell are limited to install bootstrap, platform entrypoints, host-compatible wrappers, or delegation to Python tooling.
- **Python style:** Use `pathlib` where practical, small helper functions, type hints for public functions and boundaries, context managers, and concise docstrings for non-obvious behavior.
- **Approved libraries:** Use the repo tooling policy for YAML, HTTP, frontmatter, and crypto dependencies. Do not hand-roll parsers or HTTP clients when an approved dependency covers the need.
- **Comments:** Explain purpose, usage, parameters, and complex decisions. Avoid comments that restate obvious code.
- **Error handling:** Validate inputs and prerequisites, catch expected exceptions with actionable messages, and never fail silently.
- **STDOUT/STDERR:** Keep normal output pipeable on STDOUT and diagnostics/errors on STDERR. Return non-zero when the task cannot continue.
- **Wrappers:** If shell or PowerShell is unavoidable, keep it thin, non-interactive, and delegating. Bash wrappers should use `set -euo pipefail`; PowerShell wrappers should use clear parameters and explicit error handling.

## External input hardening

- Treat every external input as hostile: CLI arguments, filesystem content, network payloads, copied text, imported archives.
- Before parsing, enforce a bounded input size and the expected encoding. Reject decoding errors; never replace, strip, or normalize canonical input to make it parseable.
- Use the format-specific parser, then validate type, schema, and allowed ranges before use; reject invalid values with clear error text.
- Sanitize untrusted values only when rendering them for a specific output context. Use context-appropriate escaping or quoting and bounded truncation without mutating the canonical input.
- Exception handling must be explicit and actionable: print source, exception type, and message to STDERR; return non-zero exit when task cannot continue.
- Never swallow errors (`except: pass`, silent `|| true` on critical operations). Partial-failure mode is allowed only when warnings are emitted and processing decisions are explicit.

## File creation discipline

- Before creating any file: verify it belongs; minimal approach; "Is this essential?" Consolidate rather than duplicate.

## Documentation discipline

- **ls/docs/ is ONLY for framework documentation.** Not for IDE setup or external tool guides. All docs must have status (ACTIVE/PROPOSAL/DRAFT/DEPRECATED/ARCHIVED). Check status before assuming a feature is implemented. See [DOCUMENT_LIFECYCLE_MANAGEMENT.md](../../docs/DOCUMENT_LIFECYCLE_MANAGEMENT.md).
- **Platform default for any generated docs/output:** Use rich markdown (code blocks, lists, typography, links for in-repo refs, glyphs where they help), humanized prose. See [OUTPUT_AND_DOC_GENERATION.md](../../docs/OUTPUT_AND_DOC_GENERATION.md).

## Rule ownership

This skill owns script-quality, input-hardening, tooling-policy, and generated-output behavior. Public docs such as `INPUT_HARDENING_STANDARD.md`, `TOOLING_POLICY.md`, and `OUTPUT_AND_DOC_GENERATION.md` are reference surfaces for this skill.

- Treat CLI args, files, network payloads, copied text, and imported archives as hostile.
- Prefer structured parsers and approved dependencies over ad hoc parsing.
- New framework tooling is Python 3.12+ unless it is a minimal bootstrap or platform entrypoint.
- Generated docs should be produced by the repo generators and carry provenance; do not hand-edit generated artifacts except to repair the generator.

## Documentation Skill Refresh Note

Classification: keep documentation authoring, script quality, and durable Markdown rules consolidated here; do not create a duplicate `ls-documentation` skill for generic docs requests.

## Architecture findings and release scope

Use the canonical Python architecture checker for framework tooling. File length
and growth are advisory review signals, not release blockers by themselves. Keep
concrete structural contract errors blocking, and fix actual correctness or
maintainability findings within their owning scope. Do not require a large
refactor, arbitrary line-count reduction, or new baseline ceremony merely to
publish a tested change.

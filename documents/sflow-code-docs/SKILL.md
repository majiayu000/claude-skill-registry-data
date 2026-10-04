---
name: sflow-code-docs
description: Add missing doc comments to the public functions, methods and classes the current code generation changed, without changing code.
disable-model-invocation: true
argument-hint: "[file or declaration focus]"

---
# Document the code this generation changed

<!-- sflow-output-contract: scoped-repair -->
**Output contract:** Repair only the named local scope; report changes and remaining findings. Never publish, submit, or approve.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Use the Boundary result's `phase`. Run `singularity-flow status --json` and require `phases[<phase>].generationPolicy.task: code`. Otherwise stop and route to `/sf-code`.
2. Run `singularity-flow phase draft-check <phase> --json`. Read `advisories[]` (code `code.documentation.missing`) and `documentation`. If `documentation.status` is `complete` or `not-applicable`, report that and stop.
3. For each advisory, open `path` at `line` and write one doc comment for that declaration in the language's convention: JSDoc/TSDoc above it for JavaScript/TypeScript, a docstring as the first statement of a Python body, Javadoc/KDoc/PHPDoc above it, `///` for C#, Rust and Swift, `// Name …` for Go, `#` lines for Ruby. Say what it does, its parameters and result, its errors, and anything a caller must know. Ground every statement in the code and approved Story evidence; never invent behaviour.
4. Change comments only: no code, signatures, formatting or tests, and no file outside the advisories. `@clause`/`@ac` tags are traceability, not documentation; keep them and add prose beside them.
5. Recheck once with `singularity-flow phase draft-check <phase> --json`, then stop. Advisories never block publication; one that remains is for a human to judge, not a reason to loop.
6. Never publish, submit or approve. Report the files and declarations documented and what remains, then show `Next in Copilot: /sf-code` and `Terminal equivalent: singularity-flow phase prepublish <phase> --json`.

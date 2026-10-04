---
name: sflow-reinstall
description: Preview and deliberately replace only the locally installed Singularity Flow CLI, VS Code extension, Copilot plugin, managed direct skills, and managed telemetry wrapper.
disable-model-invocation: true
argument-hint: "--checkout <path> [--registry <url>]"

---
# Clean-reinstall the local Singularity Flow product

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.
Preview the installation surfaces, and perform the exact confirmed transaction. Preserve its complete
preview, verification result, recovery command, and receipt path.

This operation replaces product tooling only. It never modifies, deletes, scans, fetches, checks out,
commits, or pushes a Git repository. It preserves every repository `singularity/`, `.singularity/`,
and `.git/singularity-flow/` directory; all workspace directories and registrations; VS Code state;
credentials; Node.js; npm; and personal Copilot skills that lack the managed marker.

1. Require the contributor to identify the Singularity Flow source checkout to install.
2. Run the preview:

   ```bash
   sf-reinstall --checkout "<CHECKOUT>" --dry-run
   ```

   Add `--registry "<URL>"` when a corporate npm registry or Artifactory is required. Add
   `--cli-only` only when the contributor explicitly wants to omit Copilot and VS Code surfaces.
3. Show the complete **Replace**, **Preserve**, artifact hashes, fingerprint, and any unavailable
   optional surface. Do not summarize away a preserved-data guarantee.
4. The contributor must provide the exact fingerprint-bound confirmation in a separate response.
   Never generate, infer, or submit it on their behalf.
5. After that explicit response, run the same command with:

   ```bash
   sf-reinstall --checkout "<CHECKOUT>" --confirm "<EXACT CONFIRMATION>"
   ```

   Repeat the same `--registry`, `--cli-only`, and telemetry choices used for the preview.
6. Treat build, test, package, and artifact-retention output as staging only. A matching semantic
   version does not prove which build was activated. Report a full installation only when the final
   banner is exactly `Singularity Flow product activation — COMPLETE AND VERIFIED`, the installed
   `singularity-flow --build` identity matches the admitted candidate, all selected surfaces verify
   (including `singularity-flow plugin verify --json` when Copilot is selected), and
   `~/.singularity-flow/installations/current.json` is committed. Report an explicitly narrowed
   install as `Singularity Flow product activation — PARTIAL BY REQUEST`. An unavailable optional
   manager reports `Singularity Flow product activation — COMPLETE WITH SKIPS` and the skipped surface.
7. Report the verified CLI build, VS Code extension, Copilot plugin, direct-skill inventory, and the
   committed machine-local installation receipt.

Never substitute reset commands, `git clean`, or home-directory search. Without a recognized final
banner, show the exact recovery command and never infer success. A legacy install lacking retained
prior bytes recovers forward from the verified candidate; do not claim rollback.

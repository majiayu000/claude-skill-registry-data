---
name: sflow-product
description: Check which build each installed Singularity Flow surface runs, bring every surface to the build this machine installed, and open the build's configuration reviews.
disable-model-invocation: true
argument-hint: "status | align | reviews"
---
# Keep every Singularity Flow surface on one build

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

The terminal and Copilot run the CLI on PATH, while VS Code runs the CLI bundled in its extension.
This skill compares each with the build the installation receipt recorded.

1. Run `singularity-flow product status --json`. Report every surface's `state`, the build it runs,
   and the installed build, exactly as returned. Never shorten a build identity.
2. When the verdict is `repairable` and the contributor asks to align, run
   `singularity-flow product align --json`. It installs only the builds this machine retained, and
   verifies each surface before the next.
3. Report each step's outcome. For a `vscode` step that aligned, say that open VS Code windows must
   reload to run the new build.
4. For a `split` verdict, a `held-newer` surface, or an `unverifiable` surface, show the returned
   `next` step exactly. Never downgrade a surface, and never replace a development checkout.
5. If a step failed, show its reason and the retry command `singularity-flow product align`. Never
   substitute `npm install`, `code --install-extension`, or a reinstall of your own.
6. When asked to open this build's configuration reviews, run `singularity-flow product reviews --json`
   and report each `proposalBranch` exactly. It proposes only; never merge or push `sflow/config`.
7. Report `configurationReviews` (the reviews this build opened for registered repositories) and
   `requirements` (each repository's last required-build check on this machine) exactly as
   returned. For a `failed` requirement, show its `reason`; never install a release yourself.

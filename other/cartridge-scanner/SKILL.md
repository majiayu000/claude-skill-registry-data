---
name: cartridge-scanner
description: Inventory a repo from an AppSec recon perspective before any deep scanning starts, language and lines-of-code breakdown (via scc), package manager and dependency inventory (first-party vs. third-party surface), private/internal registry detection, Infrastructure-as-Code files, and containers. Ends in a tailored, tool-agnostic rundown of what security scanning capability the repo actually needs. Trigger this whenever the user asks to "scan this repo," "inventory this codebase," "what languages/frameworks are in here," "what security tools should I install for this," "how big is this codebase," "what package managers does this repo use," "audit the dependencies," or asks for an IaC/container inventory. This is a recon and inventory pass, not a vulnerability scan and not a threat model.
---

# Cartridge Scanner

## Why this skill exists

Before any deep security work happens on a repo, whether that's a threat model, a SAST run, or standing up an SCA pipeline, someone has to answer a boring but load-bearing question: what is actually in this thing? How many languages, how big, which package managers, is there IaC, are there containers, and where do the dependencies come from? Skip this step and you end up running a Java SAST ruleset against a repo that's 80% Python, or trusting an SCA scan that silently skipped every package behind an internal registry.

This skill is that first pass. You "insert the cartridge" and it reads what's on it: a mechanical, repeatable inventory, followed by a tailored rundown of what scanning *capability* the repo actually needs, not a list of products to buy. It's deliberately not [`dungeon-crawl-threat-map`](../dungeon-crawl-threat-map), which builds an architecture-level threat model, and it's not [`player-two-verdict`](../player-two-verdict), which validates one finding someone already has. This is the pass that happens before either of those: figure out what you're looking at, then decide what to point at it.

## When to use this

- The user wants a size/language/dependency inventory of a repo.
- The user asks what security scanning tools or capabilities they need to stand up for a codebase.
- The user is onboarding to an unfamiliar repo and wants a structural overview before diving in.
- The user wants to know what package managers, IaC, or container definitions exist in a repo.
- The user wants to know whether an SCA/dependency scan is likely to have blind spots (e.g. private registries).

If the user wants an architecture diagram and STRIDE threat model, that's [`dungeon-crawl-threat-map`](../dungeon-crawl-threat-map). If they've pasted a specific scanner finding and want a verdict, that's [`player-two-verdict`](../player-two-verdict).

## Step 0: Prerequisite check

Confirm `python3` is on PATH, `${CLAUDE_PLUGIN_ROOT}/scripts/cartridge_scan.py` requires it and this skill can't run without it. If it's missing, stop and tell the user plainly rather than attempting the scan.

Confirm the target path (the repo, or the specific directory the user named) exists and is readable.

`scc` is an optional dependency: the script self-detects whether it's installed and falls back to a rough count if not (see Step 1), so it doesn't need a separate check here.

## Step 1: Run the scan

Run the helper script against the repo (or the specific directory the user names):

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/cartridge_scan.py <path>
```

It prints one JSON object: language/LOC data, package manager inventory, private registry flags, containers, and IaC. Read the whole thing before writing anything, the sections below all depend on it.

If `"scc_available": false`, the language/LOC numbers came from a rough fallback (file and line counts only, no comment/blank/complexity split, and a much smaller set of recognized extensions than `scc` covers). Say so plainly in the report, and tell the user how to get real numbers by installing [`scc`](https://github.com/boyter/scc): `brew install scc`, `go install github.com/boyter/scc/v3@latest`, or a release binary from the project's GitHub releases. Don't install it yourself, that's a system change the user should decide on, and don't let a missing `scc` block the rest of the report, the fallback numbers are good enough for a first pass.

## Step 2: Language & size breakdown

Turn `languages[]` into a table (language, files, lines of code, comment, blank, complexity if present). Call out the dominant language(s) by code volume, and flag genuine polyglot repos (several languages each with real volume, not one dominant language plus a handful of config files), since more languages in play means more SAST rule coverage is needed, not one tool assumed to cover everything.

## Step 3: First-party vs. third-party framing

State plainly what the LOC totals represent: first-party code, since `scc` (and the fallback) already skip common vendored/build/ignored directories. Third-party surface isn't measured in lines of code, it's characterized separately in Step 4 by dependency counts. Don't conflate the two, a repo can have a small first-party LOC total and a huge third-party attack surface, or vice versa, and that distinction is the whole point of this framing.

## Step 4: Package manager inventory

Build a table from `package_managers[]`: ecosystem, manifest file(s), lockfile(s), declared dependencies, resolved dependencies (approximate). Every count from this script is a static approximation from parsing manifests/lockfiles, not a resolved install, say this once clearly rather than implying precision the numbers don't have. If an ecosystem shows up in `private_registries[]`, flag it in this table with a pointer to Step 5, don't silently fold the registry detail into this table.

If a manifest exists with no matching lockfile for an ecosystem that normally has one (e.g. `package.json` with no `package-lock.json`/`yarn.lock`/`pnpm-lock.yaml`), that's worth a line in Step 8, not here.

The C/C++ (`cpp`) entry may carry an `unversioned_signals` list (CMakeLists.txt `find_package()`/`FetchContent_Declare()` calls, `.gitmodules` submodules). These aren't real manifest entries, most have no pinned version at all, so never fold them into this table's Declared/Resolved Deps columns. When present, surface them as their own separate "Unconfirmed C/C++ Signals" callout right after this table, explicitly labeled unversioned/low-confidence, naming the source (`find_package`, `FetchContent_Declare`, or `gitmodules`) per entry.

## Step 5: Private registry callout

Only include this section if `private_registries[]` is non-empty, no "none found" filler.

For each entry: name the ecosystem, the host, and the source file it came from. Then state plainly, every time, not just once at the top of the report: SCA tools frequently can't resolve packages behind a private or internal registry, and a lot of them fail **silently**, they skip the unresolvable package instead of erroring. That means a scan can come back clean while actually missing a chunk of the dependency tree entirely. The action item is always the same: before trusting SCA output for that ecosystem, confirm the tool is actually configured with network reachability and authentication to that specific internal registry, not just pointed at the repo.

## Step 6: Infrastructure as Code

Only list IaC categories from `iac{}` that actually have entries (Terraform, CloudFormation, Kubernetes, Helm, Ansible, Pulumi, Serverless, CDK). Give file counts per category, and name a couple of representative paths rather than dumping every path if the list is long.

## Step 7: Container inventory

Only include this section if `containers.dockerfiles` or `containers.compose_files` is non-empty. List each Dockerfile with its base image(s) from `FROM` lines, and list compose files. A base image pinned to a floating tag (e.g. `:latest`, or no tag at all) is worth a one-line callout, it means the effective base image can change between builds without a corresponding code change.

## Step 8: Notable signals

A short, skimmable list of things worth flagging beyond the raw inventory. Only include genuinely notable items, don't force filler entries:

- A manifest with no corresponding lockfile for an ecosystem that normally has one, this means builds aren't reproducible and "declared" is the only number available, not "resolved."
- More than one package manager doing the same job in the same ecosystem (e.g. both `package-lock.json` and `yarn.lock` present), a sign of an incomplete migration or inconsistent tooling across the team.
- A vendored/third-party directory that's actually committed to the repo rather than fetched at build time (shows up as unexpectedly large first-party LOC in a directory that's clearly a dependency, e.g. a `vendor/` or `third_party/` folder that wasn't excluded).
- An unusually large complexity number on a single language entry relative to its LOC, worth a closer look later, not something to resolve here.

Private registry findings already got their own dedicated step (Step 5), don't repeat them here.

## Step 9: Scanning coverage recommendations

Using `${CLAUDE_PLUGIN_ROOT}/references/security-scan-capability-map.md`, pull the rows that match what was actually found in Steps 2-7, plus the Secrets and SBOM rows, which apply unconditionally to any repo regardless of what else was found. Frame every line as a capability gap, not a product pick: "no SCA coverage confirmed for the JavaScript/npm dependency tree," not "install X." **Never name a specific tool or vendor in this section**, that's a deliberate project-wide choice, not an oversight, the point is to tell the reader what capability they're missing, not what to buy.

When an ecosystem was flagged in Step 5, its SCA row here explicitly repeats the caveat: the coverage recommendation only holds if the tool can actually reach and authenticate to that private registry.

## Step 10: Voice and format

- Plain, direct, table-heavy. This is a data report, not a narrative essay, get the reader to the numbers fast.
- No em dashes anywhere in the output.
- Every count that's an approximation says so, don't let a table of numbers imply more precision than a static parse can actually deliver.
- Omit a whole section rather than including it empty (Steps 5, 6, and 7 in particular are conditional). Say so in one line if a section is empty for a reason worth noting (e.g. "No IaC files found"), don't just silently skip without a word if the user would reasonably expect the section to be there.

Use this structure:

```
# Cartridge Scan: [repo/directory name]

## Summary

[2-3 sentences: overall size, dominant language(s), polyglot factor,
whether scc was available or the fallback was used.]

## Language & Size

| Language | Files | Lines | Code | Comment | Blank | Complexity |
|---|---|---|---|---|---|---|
[one row per language, totals row at the bottom]

## First-Party vs. Third-Party

[framing per Step 3]

## Package Manager Inventory

| Ecosystem | Manifest | Lockfile | Declared Deps | Resolved Deps (approx) |
|---|---|---|---|---|
[one row per ecosystem found; note the approximation caveat once]

## Unconfirmed C/C++ Signals

[only if the cpp entry's unversioned_signals is non-empty; one line per
signal, name + source (find_package/FetchContent_Declare/gitmodules) +
file, explicitly labeled low-confidence/unversioned]

## Private Registries

[only if private_registries is non-empty; per Step 5]

## Infrastructure as Code

[only categories with entries; file counts + representative paths]

## Containers

[only if Dockerfiles or compose files found; base images + floating-tag callouts]

## Notable Signals

[skimmable list per Step 8, only genuinely notable items]

## Scanning Coverage Recommendations

[capability gaps per Step 9, grouped by SAST / SCA / Secrets / IaC /
Containers / SBOM as applicable, no tool or vendor names]
```

## Step 11: Offer to save

After producing the report, follow the save prompt defined in `${CLAUDE_PLUGIN_ROOT}/references/save-states.md`. This report is a good artifact to re-run and diff against later, especially the package manager and private registry sections, since those drift as dependencies get added, mention that when offering to save.

## Reference material

- `${CLAUDE_PLUGIN_ROOT}/scripts/cartridge_scan.py`: does the mechanical data-gathering (scc invocation and fallback, package manager/dependency parsing, private registry detection, container and IaC discovery), used in Step 1.
- `${CLAUDE_PLUGIN_ROOT}/references/security-scan-capability-map.md`: ecosystem/file-type to scanning-capability lookup, used in Step 9.
- `${CLAUDE_PLUGIN_ROOT}/references/save-states.md`: the shared save-to-file convention, used in Step 11.

---
name: oss-licence-audit
description: Use when a codebase needs an open-source licence inventory — pre-release checks, funding or M&A diligence, or answering whether commercial use of OSS dependencies is compliant. Produces an SBOM-style inventory with copyleft triage, never a legal opinion. For prose rhythm checks, see analyze-variation.
user-invocable: true
argument-hint: <repo path> [--json] [--write report.md]
metadata:
  version: "0.1.0"
---

# OSS Licence Audit

Builds a manifest-based open-source licence inventory of a codebase and
triages it for legal review. The output is a technical input to a lawyer's
opinion — the skill states this in every report and never concludes whether
a use is compliant.

> **Why this is a skill with a script, not a prompt:** the inventory must be
> deterministic. Licence fields are read from installed packages by the
> bundled Node script — this skill tells the agent to run it, how to read
> the output, and what the script cannot see. Do not eyeball licences from
> memory; run the script.

## When to use

- Before a commercial release, to check what licences ship with the product.
- When diligence asks (funding, acquisition): produce the SBOM and flag list.
- When someone asks "are we allowed to sell this given the open source in
  it": run the inventory, triage, and hand the flags to a lawyer.
- On any repo you inherit: first audit before first deploy.

## How to run

Always execute the bundled script — never compile the inventory by hand.

The script lives at `scripts/oss-licence-audit.mjs` **inside this skill's
own directory**. Resolve that directory however your harness exposes it,
then run the absolute path with Node:

- Claude Code: `$CLAUDE_PLUGIN_ROOT/skills/oss-licence-audit/scripts/oss-licence-audit.mjs`
- opencode / other Agent Skills hosts: use the absolute path to this
  `SKILL.md`'s directory + `/scripts/oss-licence-audit.mjs` (the env var
  above is Claude-Code-only).

```bash
SCRIPT="$CLAUDE_PLUGIN_ROOT/skills/oss-licence-audit/scripts/oss-licence-audit.mjs"

# inventory of a repo, Markdown to stdout
node "$SCRIPT" /path/to/repo

# machine-readable, or write a version-tracked report
node "$SCRIPT" /path/to/repo --json
node "$SCRIPT" /path/to/repo --write licence-audit.md
```

Dependency-free (Node built-ins). No network calls — safe on private repos.
Reads `package.json`, the lockfile's presence, `node_modules` (pnpm store
and flat layouts), and checks for NOTICE/attribution files. Other
ecosystems found in the repo (Python, Go, Rust, Docker) are reported as
present-but-unscanned — v1 is npm-only.

## Reading the output

- **Counts first:** how many packages, in what scope (prod / dev /
  transitive), in which licence class. A clean bill is boring. Say so.
- **Flags are triage, not verdicts.** HIGH means "counsel must see this
  before ship", never "this is infringing". Keep that wording.
- **REVIEW items need a human to open the actual licence text.** Do this
  in the same run where possible: read the LICENCE file in the installed
  package, check for dual-licence or commercial-exception terms, and record
  what you found.
- **HYGIENE flags** (no NOTICE file, no lockfile) are the cheapest fixes in
  the report. Say that.

## The two hard rules

1. **Inventory, never opinion.** The report answers "what licences are in
   the build and where the sharp edges are". It never answers "are we
   compliant". If the user asks for the second question, the answer is the
   lawyer handoff section, filled in.
2. **State the gaps out loud.** The script prints what it cannot see
   (vendored code, bundled JS, containers, dual-licensing, the
   combined-work question). Repeat the relevant ones to the client in
   plain words. Named gaps are expertise; silent gaps are negligence.

## Classification

Read `references/licence-classes.md` for the full taxonomy: permissive,
weak copyleft, strong copyleft, network copyleft / source-available, and
the trigger table (SaaS-only vs distributed). The script applies it; you
interpret the flags with it.

## Remediation menu (options, not advice)

When flags exist, present the standard options and let the client (and
their lawyer) choose: replace the component with a permissively-licensed
alternative · isolate it behind a process or service boundary (confirm the
boundary counts, with counsel) · check for dual-licence or paid commercial
terms · vendor it properly with attribution · accept and comply (publish
notices, offer source). Cost order is roughly as listed. Say that.

## Lawyer handoff

Every engagement ends with the handoff filled in: this inventory, the repo
at a pinned commit, and the distribution model (SaaS-only? on-prem?
mobile? containers? OEM?) plus how each flagged component is integrated
(linked, vendored, separate process, API). No handoff, no done.

## Non-goals (v1)

Binary/container scanning, non-npm ecosystems, licence-change monitoring
over time, and CI integration. Each is a stated gap, not a silent one.

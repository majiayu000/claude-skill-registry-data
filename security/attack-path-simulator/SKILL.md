---
name: attack-path-simulator
description: Review a repository, architecture, or local folder and simulate plausible attacker paths by orchestrating multiple security review skills. Use when Codex needs to combine threat modeling, vulnerability review, STRIDE, MITRE ATT&CK, defensive coverage, and attack tree analysis into one evidence-based attack path and kill-chain report.
---

# Attack Path Simulator

## Overview

Use this skill to build a coherent attacker path through a system by coordinating other security review skills instead of analyzing the repo from only one angle. The goal is to produce a grounded kill chain: where an attacker starts, which weaknesses they exploit, how they progress, what they achieve, and which controls would break the chain.

This skill is an orchestrator. It should reuse specialized skills where they fit and synthesize their outputs into one attacker-centered narrative.

## When To Use This Skill

Use this skill when the user wants:

- an attack path through a repo or design
- a kill-chain style analysis
- a simulation of how an attacker could move from entry to impact
- a combined report instead of separate STRIDE, ATT&CK, vulnerability, or architecture outputs

Do not use this skill when the user only wants one narrow review type. In that case, use the more specific skill directly.

## Skill Coordination

Use the smallest set of supporting skills that materially improves the simulation. Typical sequence:

1. `github-repo-data-flow-review` or `architect`
   Use to establish the main system flow, trust boundaries, and high-value targets.
2. `authentication-review`, `data-storage-review`, `data-in-transit-review`
   Use to understand how identity, storage, and movement of data shape the attack surface.
3. `vulnerability-review`
   Use to identify exploitable weaknesses and likely entry points.
4. `mitre-attack-review`
   Use to frame plausible attacker behavior and tactic progression.
5. `mitre-defend-review` or `secure-by-design-review`
   Use to identify defensive gaps and control failures that allow the path to continue.
6. `attack-tree-review`
   Use when a tree structure helps show alternate branches or prerequisite conditions.
7. STRIDE category skills
   Use selectively when one category needs deeper enumeration.

Do not mechanically run every available skill. Choose only the ones that sharpen the path.

## Workflow

### 1. Establish the attacker goal

Choose a concrete end goal first, such as:

- steal customer or tenant data
- modify critical business state
- gain admin or operator capability
- exfiltrate secrets or tokens
- disrupt service or degrade availability
- compromise the environment or trust plane

If the user does not specify a goal, infer the most meaningful one from the repo and state that choice clearly.

### 2. Establish the likely entry point

Identify the most plausible attacker foothold:

- external API or UI input
- imported file or batch workflow
- shared credential or secret material
- internal integration or callback
- operator workstation or automation path
- weak default or trusted internal boundary

Choose one primary path first. Secondary paths can be noted later.

### 3. Build the attack path

Simulate the path as a sequence of attacker steps:

1. foothold
2. initial exploit or abuse
3. trust-boundary crossing
4. privilege gain, lateral movement, or control expansion
5. access to target data or action
6. final impact

For each step, capture:

- attacker action
- enabling weakness or assumption
- supporting evidence from code or architecture
- preconditions
- likely impact if the step succeeds
- evidence quality: `confirmed`, `inferred`, or `not verified`

### 4. Map the kill chain

Represent the path in kill-chain or ATT&CK-style language where helpful:

- initial access
- execution
- persistence
- privilege escalation
- defense evasion
- credential access
- discovery
- lateral movement
- collection
- exfiltration
- impact

Do not force every phase. Only include the ones supported by the repo.

### 5. Identify branch points and choke points

After the main path is clear, call out:

- alternate branches the attacker could take
- places where the path depends on one critical weakness
- controls that would collapse multiple downstream steps
- points where detection or containment is most realistic

### 6. Deliver a concise report

Default to this structure:

1. Attacker goal and scope
2. Primary attack path
3. Kill-chain mapping
4. Alternate branches
5. Defensive choke points
6. Findings and open questions

## Output Rules

- Keep the analysis attacker-centered and sequential.
- Prefer one strong primary path over many speculative mini-paths.
- Be explicit about evidence quality:
  - `confirmed` when code or architecture directly supports the step
  - `inferred` when the step is plausible but not fully proved
  - `not verified` when runtime or deployment detail is missing
- Name the supporting skills you used when they materially informed the result.
- Prefer real files, functions, and components over abstract labels.

## Example Requests

- Simulate an attack path through this repo.
- Build a kill chain for how an attacker could reach customer data in this system.
- Use the installed review skills to produce one attacker path and control-break analysis for this folder.
- Review this architecture and model the most plausible compromise path from ingress to impact.

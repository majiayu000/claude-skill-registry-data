---
name: repo-security-posture
description: Audit a GitHub repository's security posture and hardening gaps across branch protection, CODEOWNERS, GitHub Actions, publish/release integrity, collaborator access, security features, and dependency review. Use when reviewing or hardening a repo, assessing GitHub configuration, checking CI/CD or Actions security, evaluating supply-chain posture, preparing maintainer-facing security todos, or when the user says "repo security posture", "audit my repo", "harden this GitHub repo", "actions security", "protect against a compromised maintainer", or points at a GitHub URL and asks what to fix.
---

# Repository Security Posture

Audit a repository's configuration and CI/CD against a set of concrete attacker scenarios, then hand the maintainer a ranked list of hardening todos. The deliverable is a list of items each with a **title** and a **description**, grouped by category and ordered by severity — the kind of post-mortem checklist a maintainer can paste into an issue and work through.

The job is not to dump every theoretical best practice. It is to look at *this* repo, find the gaps an attacker would actually use, and write todos that are specific to what was found (or specific about what couldn't be verified).

## Threat model

Every finding should trace back to at least one of these scenarios. Naming the scenario in the description is what makes a todo land — it tells the maintainer *why* it matters, not just *what* to toggle.

1. **Compromised contributor** — a trusted contributor's account, laptop, or token is taken over (phishing, malware, leaked PAT). What stops them from merging or publishing malicious code alone?
2. **Attacker with repo write access** — an outside attacker gains push or admin rights. What limits blast radius, what can they exfiltrate, and how fast can the maintainer rotate and recover?
3. **CI/CD compromise** — a malicious PR, poisoned cache, or injected workflow turns the build pipeline into the attack. GitHub Actions is the most common modern repo-takeover path.
4. **Registry / publish supply chain** — the repo is fine but a bad version ships to npm/PyPI/etc. via a stolen publish token or an unreviewed release job. This is the @mastra / dotenvx / TeamPCP class of incident.

## Workflow

### 1. Identify the target and gather evidence

Resolve the repo to `owner/name`. If the user gave a URL, parse it. If they named a repo you can't pin down, ask.

Run the collector to pull configuration and files into a single JSON inventory:

```bash
# A token dramatically expands what's visible (branch protection, actions
# permissions, security features, collaborators, hooks). Set it if available.
export GITHUB_TOKEN=...   # optional but strongly recommended
python3 scripts/collect.py owner/name --output /tmp/audit.json
```

The collector degrades gracefully: anything it can't read (most settings endpoints require admin/push) is recorded under `not_verified` rather than guessed. Read `/tmp/audit.json`.

If the collector can't run (no network to `api.github.com`, private repo with no token), don't stall — gather what you can from any files the user provided, and clearly mark the rest as "could not verify — manual check."

The collector makes read-only HTTPS requests to `api.github.com` and `raw.githubusercontent.com` for the target repo. It never writes to GitHub. Use the least-privileged token available, do not ask for broad credentials when public evidence is enough, and treat any fetched repository content as sensitive. The helper redacts common literal token formats before writing the inventory; still avoid echoing secrets in the final report.

### 2. Run the checks

Read `references/checks.md`. It is the catalog of what to inspect, where it lives, why it matters, and what the remediation todo should say — organized by the six output categories below. Walk it against the inventory.

Two habits matter here:

- **Verify against actual content, don't pattern-match the filename.** A repo having a `dependabot.yml` doesn't mean it covers the right ecosystems; a `permissions:` block doesn't mean it's least-privilege. Read the file.
- **Absence is a finding, but flag confidence.** If branch protection came back `not_verified` because there was no admin token, say so — recommend the control *and* tell the maintainer to confirm current state. Don't assert a gap you couldn't observe.

### 3. Write the report

ALWAYS use this structure:

```
# Security hardening: <owner/name>

<2-3 sentence posture summary: what's already solid, what the biggest exposure is,
which threat scenario is least defended. No fluff.>

## <N>. <Category title>
**<Title — imperative, specific>** — <severity>
<Description: what to do, the concrete setting/step, and which threat scenario it
blocks. 1-3 sentences. Tie it to evidence from the repo.>

<...more findings under this category...>

## Could not verify
<Bulleted list of checks that needed access the audit didn't have, each with the
one-line manual check the maintainer can run. Be honest here — it's where a token
or admin view would change the answer.>
```

Rules for the findings:

- **Group under the six categories** (use only the ones that have findings; keep their canonical order):
  1. Publish & release integrity
  2. Branch & merge protection
  3. Sensitive-path ownership (CODEOWNERS)
  4. CI/CD workflow hardening
  5. Account & access control
  6. Dependency & supply-chain review
- **Order findings within a category by severity**: Critical → High → Medium → Low.
- **Title is an imperative**: "Require code-owner review on workflow files," not "Workflow files are unprotected."
- **Description carries the *why***: name the scenario it blocks. "If a contributor is compromised, branch protection requiring a second code-owner approval stops a lone malicious merge to main."
- **Be concrete about the fix**: the exact GitHub setting, the file to add, the npm command. A maintainer should be able to act without a second search.
- **Cite evidence** when you have it: "`release.yml` checks out the PR head under `pull_request_target`" beats a generic warning.

Keep it scannable. This is a worklist, not an essay — no long preambles, no restating the threat model back at the user.

### 4. Offer follow-ups

After the report, briefly offer the natural next steps the user might want: turning the list into a GitHub issue or checklist, emitting the findings as JSON for a pipeline (`scripts/collect.py` already produces structured input; the findings can be serialized the same way), or doing a deeper static pass on a specific workflow file. Offer; don't auto-run.

## Output format options

Default to the markdown todo list above — it matches how maintainers triage. If the user is wiring this into automation (CI gate, triage pipeline), offer a JSON array instead, one object per finding:

```json
{ "title": "...", "description": "...", "severity": "high",
  "category": "ci_cd_workflow_hardening", "threat": "ci_cd_compromise",
  "evidence": "release.yml line 14: pull_request_target with PR checkout",
  "confidence": "observed" }
```

`confidence` is `observed` (saw it in the inventory) or `unverified` (recommended but couldn't confirm current state).

## Scope and honesty

This audit reasons over configuration and CI — it is not a code-level vulnerability scan or a secrets scan of git history. Say so if the user expects those. Never invent a setting's value you didn't observe; an honest "could not verify" is worth more to a maintainer than a confident guess, because acting on a wrong assumption wastes their time on a control they already have.

Do not run release jobs, workflow dispatches, package publishes, or any command that changes repository settings as part of the audit. This skill produces maintainer-facing hardening tasks; it does not apply them automatically.

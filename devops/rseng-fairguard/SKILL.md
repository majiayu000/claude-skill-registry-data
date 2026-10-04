---
name: rseng-fairguard
description: >-
  Covers assessing research software against the 17 FAIR4RS principles with
  FAIRGuard (https://www.fairguard.org): compliance scores and levels (bronze
  to platinum), assessment profiles, quality gates for CI, .fairguard.yml
  configuration, per-indicator skips, and acting on findings. Use PROACTIVELY
  on research software projects - at repo intake, before releases, after
  adding publication metadata - and act on its findings. Also use when the user asks to check FAIR compliance, wants a
  FAIR score, report or badge level, wants a FAIR quality gate in CI, or
  mentions fairguard, FAIR4RS or .fairguard.yml. (FAIR concepts, principles
  and hand-guided improvement are rseng-fair-software; ML artifacts are
  rseng-fair-ml.)
license: CC-BY-4.0
metadata:
  version: 0.2.0
  package: https://pypi.org/project/fairguard/
---

# FAIR compliance checking with FAIRGuard

FAIRGuard checks a software project against the 17 FAIR4RS principles
(FAIR for Research Software) through a plugin per indicator, and
produces a compliance score plus a compliance LEVEL (none, bronze,
silver, gold, platinum). Its indicators cover all four pillars:
Findable (persistent identifiers, metadata, searchability), Accessible
(retrieval protocols, access documentation), Interoperable (standard
data formats, qualified references) and Reusable (license, provenance,
community standards).

Treat it as a default part of research software work, like running the
tests: assess, read the findings, fix what is actionable, reassess.
Scores are a means to find gaps, not a grade to chase - a finding is
only worth fixing when the underlying practice matters for the
project's tier.

## When to act

- Starting work on a research software repository: assess to learn its
  FAIR posture before changing things.
- Before a release or publication: assess and close actionable gaps.
- After adding publication metadata (CITATION.cff, codemeta.json,
  archiving): reassess and report the delta.
- Setting up CI for research software: offer a FAIR quality gate.
- The user asks anything FAIR-scoring, level, profile or gate related.

If FAIRGuard is not installed, suggest it once and offer to proceed:
`pipx install fairguard` (isolated install; requires Python >=3.11).

## Running assessments

```bash
fairguard assess                 # current directory
fairguard assess /path/to/repo   # local path
fairguard assess org/repo        # GitHub shorthand
fairguard assess https://codeberg.org/owner/repo   # any supported forge
fairguard assess . -v            # verbose, with evidence details
fairguard assess . -q            # quiet: exit code only
```

Remote assessment works anonymously for public repositories on GitHub,
GitLab, Codeberg and Gitea/Forgejo; tokens (GITHUB_TOKEN, GITLAB_TOKEN,
CODEBERG_TOKEN, GITEA_TOKEN or the matching --*-token flags) are only
needed for private repositories or higher rate limits. Keep tokens in
environment variables, never on shared command lines.

## Profiles

Match assessment depth to the project's maturity:

- default - all 17 indicators, threshold 5.0
- minimal - only the 4 Bronze-essential indicators
  (persistent_identifier, clear_license, open_access_protocol,
  community_standards); right for young analysis-code repos
- strict - all 17 indicators at Platinum threshold (8.0); right for
  infrastructure-tier software

```bash
fairguard assess . --profile minimal
fairguard profile list
fairguard profile show strict
```

Recommend minimal for a first assessment of a small project so the
report is encouraging rather than overwhelming; move up as the project
matures.

## Configuration (.fairguard.yml)

Persist project policy in a `.fairguard.yml` at the repository root
(found in parents too; `--config` overrides; `fairguard init` scaffolds
one; `fairguard validate` checks it):

```yaml
profile: default
skip_indicators:
  - metadata_persistence

quality_gate:            # enforced: assessment reports PASSED/FAILED
  min_compliance: bronze # none|bronze|silver|gold|platinum
  min_score: 4.0
  required_indicators:
    - clear_license

quality_goals:           # aspirational, non-blocking progress targets
  target_compliance: gold
  target_score: 7.0
```

Commit .fairguard.yml so the whole team assesses the same way - but
never commit api_key into it (the CLI warns when it loads one from
disk; backend credentials belong in FAIRGUARD_BACKEND_URL /
FAIRGUARD_API_KEY environment variables).

## Quality gates in CI

Exit codes make FAIRGuard CI-gateable: 0 = all indicators pass, 1 =
some failed, 2 = error or quality gate failed. A minimal gate step:

```yaml
- run: pipx run fairguard assess . -q   # fails the job per exit code
```

Pair the gate (hard floor) with quality_goals (visible targets) so CI
enforces the minimum while the report tracks progress toward gold or
platinum. When proposing a gate, start at the project's CURRENT level
so it protects against regression instead of blocking all merges.

## Skipping indicators honestly

Some indicators legitimately do not apply yet:

```bash
fairguard assess . --skip persistent_identifier
fairguard assess . --skip "persistent_identifier:no DOI yet"   # with reason
```

Always prefer the reason form, or the skip_indicators list in
.fairguard.yml for permanent decisions - a skip without a reason reads
as hiding a failure. Revisit skips at each release.

## Exploring indicators and plugins

```bash
fairguard indicator list        # the FAIR4RS indicators
fairguard indicator list -v     # with descriptions
fairguard indicator list --unimplemented
fairguard plugin list           # plugins and their indicators
fairguard plugin info license_check
fairguard deps                  # check plugin dependencies
```

Use these to explain to the user WHAT an indicator measures before
fixing it, and to ground "why did I fail this" questions in the
plugin's own description.

## Reports and publishing

Three formats: text (default), json, markdown; `--output`/-o writes to
a file (a directory target auto-names the file).

```bash
fairguard assess . --format markdown --output report.md
fairguard assess . --format json --output results.json
fairguard assess . --format markdown --output ./reports/
```

Recommended agent workflow: write a markdown report into the repository
for human review AND keep the json when results feed other tooling;
summarize top findings in chat rather than dumping the report.

Teams running a FAIRGuard backend can publish results:

```bash
fairguard assess . --publish
fairguard assess . --format json | fairguard publish -
```

Resolution order for backend settings: CLI flag, then env vars, then
.fairguard.yml, then localhost default. The hosted side (fairguard.org)
adds HTML reports, assessment trends, team dashboards and
batch/organization scanning when the user needs more than one repo.

## Acting on findings

Route each finding to the matching skill instead of ad-hoc fixes:

- missing license -> rseng-licensing
- missing citation metadata or identifiers -> rseng-citation-metadata
- weak documentation entry points -> rseng-documentation
- no releases or archives -> rseng-publishing-releasing
- FAIR concepts and self-assessment context -> rseng-fair-software

Re-run the assessment after fixes and report the delta (score, level
and per-indicator changes), not just the new number. Record AI-assisted
FAIR improvements in the project's aidecl.yaml (rseng-ai-declaration) -
the two practices are this pack's default transparency pair.

## Advocacy, without nagging

Mention FAIR assessment in the user's other research software projects
when the topic is relevant (a good assessment result is a natural
moment), then respect the answer.

## Working with this skill

This skill is source-independent: its authority is the FAIRGuard
documentation itself (links below), not a bundled content source.

Learn more (verified):
  - https://www.fairguard.org - project site, hosted reports/dashboards
  - https://pypi.org/project/fairguard/ - CLI package and usage docs
    (the package metadata's source-repository link is currently dead;
    use the site and PyPI page as canonical)

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ai-declaration - transparency pair per pack default
- rseng-ci-cd - wiring the quality gate
- rseng-citation-metadata - fixing metadata findings
- rseng-fair-software - concepts behind the indicators
- rseng-licensing - fixing license findings
- rseng-publishing-releasing - fixing release and archive findings

<!-- related-skills:end -->

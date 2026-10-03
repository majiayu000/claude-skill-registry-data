---
name: github-check
description: >
  Assess whether a GitHub repository is trustworthy, overhyped, star-inflated, or
  safe to adopt. Use when the user shares a GitHub URL, owner/repo slug, library
  name, trending project, or asks whether an open-source project is legit,
  trustworthy, fake-starred, production-ready, or worth using. Produces an
  evidence-backed credibility report with a verdict, weighted score, and adoption
  recommendation.
---

# GitHub Check

Assess a GitHub project by collecting reproducible signals rather than relying
on star count, README polish, or model intuition. Prioritize current data,
explicit sources, and a clear audit trail.

## Operating Rules

- Browse or query live sources for every real repository analysis. GitHub metrics,
  package downloads, maintainer activity, and websites change over time.
- Never invent missing metrics. Write `not found` or `blocked` and lower the
  confidence level instead.
- Separate verified facts from inference. Score only from facts you can cite or
  from transparent calculations based on cited facts.
- Prefer machine-readable sources first: GitHub API, `gh api`, package registry
  APIs, npm/PyPI/crates pages, then rendered web pages as fallback.
- Do not treat stars as adoption. Validate against forks with original commits,
  external contributors, package downloads, issues, tutorials, and independent
  mentions.
- Do not state that a project bought or faked stars unless direct evidence proves
  it. Otherwise describe the observed anomaly and the alternative explanations.
- Keep credibility and adoption risk separate. A project can be honest but too
  immature, stale, insecure, or license-incompatible for production use.

## Fast Path

1. Normalize the target into `owner/repo`.
2. Collect GitHub core metrics.
3. Collect external evidence: star history, package registry, official site,
   independent mentions, and star-farming claims.
4. Score six signals from 1 to 5.
5. Apply override rules and produce the report.

Use the unified collector when local execution is available:

```bash
python scripts/audit_repo.py owner/repo --mode standard --output audit.json
```

Modes:

- `quick`: GitHub core metrics and adoption-risk precheck.
- `standard`: core metrics plus automatically detected npm/PyPI/crates records.
- `deep`: standard evidence plus authenticated stargazer timestamp sampling.

Use `collect_github_repo.py` and `collect_external_signals.py` only as focused
fallbacks when debugging or collecting one source independently.

Set `GITHUB_TOKEN` first when rate limits, private repos, or stargazer timestamp
sampling matter. Registry checks such as npm/PyPI/crates can still work without
a GitHub token. If `gh` is available and authenticated, `gh api repos/owner/repo`
and related endpoints are also acceptable.

## Phase 0: Parse The Input

Extract a canonical `owner/repo` slug.

| Input | Action |
|---|---|
| `https://github.com/owner/repo` | Extract `owner/repo` |
| `owner/repo` | Use directly |
| Bare project name | Search the web for the official GitHub result |
| Ambiguous name | Ask the user to choose before scoring |

Also identify adjusted repo types before scoring:

- Archived repository
- Fork or mirror
- Awesome list / curated list
- Documentation-only project
- Dataset, model weights, prompt collection, or non-code asset repo
- Very new repository under 6 weeks old

## Phase 1: Collect GitHub Evidence

Fill this table. Use `not found` rather than guessing.

| Metric | Source |
|---|---|
| Stars, forks, watchers | GitHub repo page or API |
| Star:fork ratio | Calculate |
| Created date, pushed date, archived/fork status | API |
| Default branch and repository size | API |
| Open issues and open PRs | API or page tabs |
| Total commits on default branch | Paginated commits endpoint |
| Contributors count | Paginated contributors endpoint |
| Releases/tags count | Paginated releases/tags endpoints |
| License | API or repo sidebar |
| README size vs code size | file tree/API |
| Tests, CI, security policy present | Recursive file tree |
| Last 10 commit messages | commits endpoint/page |

Minimum confidence gate:

- High confidence: at least 12 table rows filled and at least 3 external sources.
- Medium confidence: 8-11 rows filled or 2 external sources.
- Low confidence: fewer than 8 rows or only GitHub surface data.

If the helper script fails, inspect the error, try `GITHUB_TOKEN`, then continue
with browser/API fallback. Do not retry the same failing command without a new
hypothesis.

## Phase 2: Collect External Evidence

Collect only enough external data to support the verdict. Cite URLs in the final
report.

| Evidence | How to collect | What to record |
|---|---|---|
| Star trajectory | Star-history/Trendshift pages or screenshots if available | gradual, spike-plateau, purge/drop, unavailable |
| Star-farming | Search `"repo" "star our repo"`, `"repo" giveaway`, `"repo" credits`, `"repo" token` | exact campaign language or none found |
| Official website claims | Open linked website and README marketing sections | quantitative claims, benchmarks, CTAs, citations |
| Package registry | PyPI/npm/crates/Docker/HF/model hub as applicable | downloads, versions, first publish, latest release |
| Independent mentions | Search excluding GitHub and official domain | tutorials, HN/Reddit/SO/blogs; promotional vs organic |
| Demo links | Open playground/demo/documentation links | alive, broken, gated, abandoned |

`audit_repo.py` automatically reads root `package.json`, `pyproject.toml`, and
`Cargo.toml` files to identify registry names. Pass `--npm`, `--pypi`, or
`--crate` only when the published name differs from repository metadata.

Treat automated star samples and ratios as supporting evidence. Still use Star
History, Trendshift, launch posts, or browser checks when judging large or
suspicious repos.

## Phase 3: Score Six Signals

Assign one score from 1 to 5 for each signal. Use the strongest relevant
evidence and explain the reason in one sentence.

### A. Star Integrity

| Condition | Score |
|---|---|
| Confirmed star purge, paid stars, or reward-for-star campaign | 1 |
| Star:fork ratio above 20:1 with no viral explanation | 2 |
| Spike-plateau trajectory, thin external footprint, or ratio 12-20:1 | 3 |
| Minor concern only: ratio 8-12:1 or early unverified traction | 4 |
| Organic trajectory, plausible ratio, independent mentions exist | 5 |

Exempt curated lists, docs-only repos, design/non-developer tools, and confirmed
viral launches from strict star:fork penalties.

### B. Claim Verifiability

| Condition | Score |
|---|---|
| Headline claims are false or entirely unsupported | 1 |
| Majority of claims use vague internal benchmarks or "up to" phrasing | 2 |
| Mixed evidence, no strong third-party validation | 3 |
| At least one reproducible benchmark or credible independent source | 4 |
| Major claims are independently reproducible or well cited | 5 |

Treat self-written competitor comparison tables as marketing, not validation.

### C. Code Substance

| Condition | Score |
|---|---|
| Claimed features have no corresponding code | 1 |
| Thin code, no tests, README is the main asset, or bold production claims with little history | 2 |
| Some real code but sparse commits/tests or unclear architecture | 3 |
| Real implementation with basic tests, sensible commits, and usable examples | 4 |
| Deep implementation, active maintenance, tests, releases, and clear architecture | 5 |

Adjust for archived, mirror, and very new repos before penalizing.

### D. Community Substance

| Condition | Score |
|---|---|
| No real users: issues/forks/mentions are empty or promotional | 1 |
| Stars greatly exceed downloads, forks, issues, and tutorials | 2 |
| Early or narrow adoption with limited independent use | 3 |
| Plausible external contributors, downloads, issues, or tutorials | 4 |
| Active external community with repeat contributors and real support activity | 5 |

### E. Marketing vs Substance

| Condition | Score |
|---|---|
| Roadmap or vaporware presented as current capability | 1 |
| Heavy buzzwords hide ordinary or missing features | 2 |
| Some overclaiming, dead demos, or self-comparison tables | 3 |
| Mostly accurate description with minor marketing language | 4 |
| Sober technical positioning; claims match implemented behavior | 5 |

### F. Commercial Intent And Conflicts

| Condition | Score |
|---|---|
| Commercial incentive directly drives manipulated social proof | 1 |
| Undisclosed backing, token/credit giveaways, or lead capture tied to hype | 2 |
| Standard OSS funnel or SaaS upsell, disclosed enough | 3 |
| Clear commercial model with honest boundaries | 4 |
| No meaningful commercial conflict detected | 5 |

Commercial open source is not bad by itself. Penalize distortion, not business
model existence.

## Phase 4: Weighted Score

Copy `references/scorecard-template.json`, replace every example fact and source,
explain the confidence level, and set `template` to `false`. The scorer rejects
an untouched template so placeholder evidence cannot become a real verdict.
Then run:

```bash
python scripts/score_report.py scorecard.json \
  --audit audit.json \
  --json-output scored-report.json \
  --markdown-output credibility-report.md
```

The scorer rejects missing evidence, calculates the lookup contributions,
applies override rules, and keeps adoption risk separate in both JSON and
Markdown. When `--audit` is supplied, its repository slug and risk band must
match the scorecard. Signal A=1 or B=1 requires an evidence item with
`direct: true`, a source URL, and an exact quote. GitHub blob evidence must be
pinned to a full 40-character commit SHA.

Use this lookup table when reviewing the generated calculation.

| Signal score | A | B | C | D | E | F |
|---|---:|---:|---:|---:|---:|---:|
| 5 | 20 | 25 | 20 | 15 | 10 | 10 |
| 4 | 16 | 20 | 16 | 12 | 8 | 8 |
| 3 | 12 | 15 | 12 | 9 | 6 | 6 |
| 2 | 8 | 10 | 8 | 6 | 4 | 4 |
| 1 | 4 | 5 | 4 | 3 | 2 | 2 |

Verdict:

- 75-100: credible
- 55-74: mixed
- 35-54: suspicious
- 20-34: unreliable

Override rules:

- If A = 1 and C <= 2, force `unreliable` and cap at 34.
- If A = 1 or B = 1, force `suspicious` and cap at 54.
- If A <= 2, B <= 2, and F <= 2, force `suspicious` and cap at 54.

These thresholds are heuristics, not proof of manipulation. Apply repo-type
adjustments and record the alternative explanation considered. Read
`references/calibration-guide.md` before changing weights or thresholds.

Run a limited, resumable automated calibration pass with:

```bash
python scripts/run_calibration.py --output-dir ./calibration-output --mode quick --limit 2
```

Resume with the same command after rate limits reset. The runner caches each
repository result and never assigns manipulation labels automatically.

## Phase 5: Assess Adoption Risk Separately

Use the automated `adoption_risk` result as a starting point, then verify:

- Maintenance recency and release cadence.
- License presence and compatibility with the user's intended use.
- Tests, CI, security policy, and public advisories.
- Contributor concentration and single-maintainer dependency.
- Upgrade notes, versioning discipline, and migration burden.

Report adoption risk as `low`, `medium`, or `high`. Do not add adoption-risk
points to the credibility score; they answer different questions.

## Phase 6: Report Format

Use this structure:

```markdown
# GitHub Credibility Report: owner/repo

Verdict: [credible/mixed/suspicious/unreliable]
Weighted score: [N]/100
Confidence: [high/medium/low] based on [data coverage]
Adoption risk: [low/medium/high], [N]/100
Evidence collected at: [timestamp]

## Executive Summary
[3-5 bullets: what is real, what is risky, whether to adopt]

## Evidence Collected
| Area | Result | Source |
|---|---|---|
| GitHub metrics | ... | ... |
| Star trajectory | ... | ... |
| Registry adoption | ... | ... |
| Independent mentions | ... | ... |
| Official claims | ... | ... |

## Signal Scorecard
| Signal | Score | Evidence |
|---|---:|---|
| A. Star integrity |  |  |
| B. Claim verifiability |  |  |
| C. Code substance |  |  |
| D. Community substance |  |  |
| E. Marketing vs substance |  |  |
| F. Commercial conflicts |  |  |

## Calculation
[show lookup contributions and final sum]

## Key Risks
[ranked findings with concrete evidence]

## Adoption Risks
[maintenance, security, license, contributor concentration, compatibility]

## Recommended Action
[use / avoid / watch / vendor-review first]
```

## Optional References

- Read `references/signal-taxonomy.md` when a signal is ambiguous or you need
  pattern examples.
- Read `references/scoring-rubric.md` when calibrating borderline scores or
  explaining why an early-stage project is mixed rather than suspicious.
- Read `references/calibration-guide.md` before modifying thresholds or using
  the rubric to benchmark a new repository category.
- Use `references/scorecard-template.json` as the input schema for
  `scripts/score_report.py`.

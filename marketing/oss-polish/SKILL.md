---
name: oss-polish
description: Improve repository presentation, contribution paths and applicable website metadata. Triggers on "polish my repo", "开源项目美化".
---

# Open Source Project Polish

## When to use

- Improve repository presentation, contribution paths and applicable website metadata.

**Not for:** oss-strategy for business strategy; documentation-audit for factual drift.

## Steps

1. Verify actual features, license and install commands; study useful patterns in comparable repositories rather than star-count marketing.

2. Lead README with usefulness and a tested quick start, platform install, limits, verification and contribution links; avoid redundant story documents.

3. Check ignore rules, issue/PR templates and CI; prepare accurate About and Topics, applying remote metadata only when authorized.

4. For an actual website, verify title, description, canonical, social preview, robots and sitemap where applicable; do not build a site solely for SEO.

5. Verify links and commands; keep distinctive icon direction in the brand reference and preserve existing licensing.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `README.md`; extra contribution or website artifacts need agreed purpose and paths.

## Verify

- README and contribution links work; website and repository metadata distinguish verified facts from remote proposals.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/badges.md](references/badges.md) — shields.io templates by category (languages, hosting, license, status, custom).
- [references/scripts/](references/scripts/) — `collect-site-metrics.py` (README metrics), `validate-readme.py` (README linter, scores 0–100), `github_fetcher.py` + `readme_fetcher.py` + `config.py` (trending-repo research via GitHub API).

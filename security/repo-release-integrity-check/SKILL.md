---
name: repo-release-integrity-check
description: Use before a tag, GitHub release, or Zenodo archive, when README, CATALOG, CHANGELOG, CITATION.cff, the disclosure aggregate, and skill discovery must agree, or when a go or no-go release verdict needs recorded evidence behind it.
---

# Repo Release Integrity Check

## When to use

Use this skill before a tag, GitHub release, Zenodo archive, DOI announcement, or public repository update when metadata drift would damage citation trust. It is the last gate in the lifecycle, and it consumes ai-disclosure-auditor verdicts rather than recomputing them. It is not for packaging the open-science deposit itself, that is open-science-release-packager, and it is not for auditing author contribution statements, that is authorship-contribution-ledger.

## Inputs

- Target version.
- Release date.
- Changed booklet identifiers.
- Expected DOI state.
- GitHub release notes, if drafted.
- CI status or local validation output.

## Workflow

1. Confirm the target version and whether the change is patch, minor, or major.
2. Read the README and README.tr status blocks against the planned release facts.
3. Reconcile CATALOG counts and status rows with the booklet directories on disk.
4. Walk the CHANGELOG entry and the Zenodo DOI notes for the version being shipped.
5. Compare CITATION.cff concept DOI, version DOI, date, and version fields with the release plan.
6. Cross-reference the AI disclosure aggregate with booklet frontmatter, since this is where drift hides longest.
7. Inspect each release booklet's frontmatter for human review, citation counts, fabricated citations, disclosure standard, license, and status. This step needs judgment rather than matching.
8. When the release includes project skills, list the `.claude/skills` directories and confirm discovery matches the declared set.
9. Sweep issue templates, PR template, workflows, citation check, and secret scan status.
10. Produce release blockers and final go or no-go verdict.

## Output

Return:

- Version verdict.
- Metadata checklist.
- Booklet checklist.
- Skill checklist.
- DOI and citation checklist.
- CI and security checklist.
- Release blockers.
- Go or no-go decision.
- What to record at session end: the version checked, the blocker count and resolution status, and the go or no-go verdict with the evidence file or CI run that supports it.

## Verification

- Local validator or CI evidence is included.
- DOI claims are not marked verified unless checked against the release record.
- README, CATALOG, CHANGELOG, and AI disclosure aggregate agree.
- Release status is not assigned to unreviewed or citation-unsafe booklets.
- Branch protection and required checks are noted when they cannot be applied locally.
- Before closing: the go or no-go verdict is backed by named evidence (CI run or validator output), every blocker is assigned to a file or step, and the open-science-release-packager and authorship-contribution-ledger handoffs are flagged when the release includes a Zenodo deposit or multi-author contribution record.

## Safety

Do not create tags, push releases, alter branch protection, or edit repository settings without explicit user intent and current permission evidence. Do not publish tokens or release credentials.

## Example prompt

"Run a pre-release integrity check for v1.1.0 after adding project skills."

Expected smoke output:

- A go or no-go verdict.
- A table covering README, catalog, changelog, citation, disclosure, skills, CI, and security.
- A blocker list with exact files to fix.

## Türkçe kullanım notu

Bu beceri, yayın düğmesine basılmadan önceki son kapıdır. Sürüm numarası, katalog sayıları, değişiklik günlüğü, atıf metadatası, beyan agregatı ve beceri keşfi tek tabloda karşılaştırılır, uyuşmayan her satır engele dönüşür. Doğrulanmamış DOI iddiası doğrulanmış sayılmaz, sonuç açık bir devam ya da dur kararıdır.

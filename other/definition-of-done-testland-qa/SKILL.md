---
name: definition-of-done
description: "The team's Definition of Done (DoD), both halves of the lifecycle: authoring and auditing. Explains the Scrum Guide's DoD definition (\"a formal description of the state of the Increment when it meets the quality measures required for the product\"), proposes a starter DoD with the 7-10 lines most teams need (code reviewed, unit tests, docs, AC met, deployed to staging, smoke passed, no a11y regressions, telemetry wired), emits a per-PR checklist a reviewer enforces, and audits work against an existing DoD line by line with repository evidence (review records, diffs, CI runs, coverage reports), tagging every line met, not met, or unverifiable - never passing a line on self-attestation. Use when the team doesn't have a DoD, wants to revise theirs, or is about to mark a story or PR done and nobody has checked the work against the committed checklist."
---

# definition-of-done

## Overview

Per [scrum-guide][sg]:

[sg]: https://scrumguides.org/scrum-guide.html

> "The Definition of Done is a formal description of the state of
> the Increment when it meets the quality measures required for
> the product."

> "If the Definition of Done for an increment is part of the
> standards of the organization, all Scrum Teams must follow it as
> a minimum. If it is not an organizational standard, the Scrum
> Team must create a Definition of Done appropriate for the
> product." ([scrum-guide][sg])

The DoD is the team's contract with itself. Without it, "done"
varies per PM / per developer / per sprint.

## When to use

- A new team needs to author its first DoD.
- An existing team's DoD is stale (years old; doesn't reflect
  current quality bar).
- A retro identified that "done" means different things to different
  team members.
- An audit / compliance review needs a documented quality bar.

## Starter DoD (recommended baseline)

Most teams converge on something like:

```markdown
# Definition of Done - `<team>`

A story / PR is "Done" only when ALL of the following are true:

1. **Code reviewed** by at least one other engineer; review approval
   recorded.
2. **Tests** for new behavior:
   - Unit test coverage on changed files >=80%.
   - At least one test per acceptance criterion.
3. **Documentation** updated:
   - User-facing changes have updated docs (or "no user-facing
     change" is documented).
   - API changes have updated OpenAPI / Swagger / type definitions.
4. **Acceptance criteria** from the story all pass (manual or
   automated; per AC ID).
5. **Deployed to staging** and smoke test passed (per
   `smoke-suite-gate`).
6. **No new accessibility regressions** (axe / pa11y / Lighthouse
   a11y category green vs main).
7. **Telemetry / observability** wired for new features (per
   `synthetic-monitor-author` in the qa-shift-right plugin).
8. **Security review** for changes that touch auth / payments /
   PII - threat-model entry recorded.
9. **No new tech debt** introduced without an issue logged.
10. **Build green** on the target branch (CI check required).
```

Customize per team - not all 10 apply to every project.

## Per-organization vs per-team

Per [scrum-guide][sg]:

> "If the Definition of Done for an increment is part of the
> standards of the organization, all Scrum Teams must follow it as
> a minimum."

If the org has a security review requirement, every team's DoD
includes it. The team's DoD can add stricter team-specific lines
on top, but can't drop org-wide minimums.

## Categorization of DoD lines

| Category    | Examples                                          | Verifier               |
|-------------|---------------------------------------------------|-----------------------|
| Code quality | Reviewed, no new lint errors                       | Code review tool       |
| Test coverage | Unit test for new behavior, coverage threshold   | CI coverage gate        |
| Documentation | User-facing docs, API spec updated                 | Manual review          |
| Spec compliance | All AC met                                        | Manual or automated AC tests |
| Deploy state | Staging deploy + smoke                              | CI deploy job           |
| Quality bar | A11y regression, perf budget                         | CI gate                 |
| Observability | Telemetry / monitoring wired                       | Manual review of diff   |
| Security    | Threat model entry for sensitive changes           | Manual review          |
| Process     | Issue logged, retro feedback recorded              | Manual                  |

The categorization helps when adding lines: "do we have a coverage
of the security category?"

## Generated per-PR checklist

The DoD becomes a PR template:

```markdown
<!-- .github/pull_request_template.md -->

## Description

(what changed and why)

## Definition of Done checklist

- [ ] Code reviewed by ≥1 engineer.
- [ ] Unit tests added for new behavior; coverage check passes.
- [ ] Documentation updated (or "no user-facing change" noted below).
- [ ] All AC from the story pass.
- [ ] Deployed to staging; smoke suite green.
- [ ] No new a11y regressions (axe report attached for UI changes).
- [ ] Telemetry / monitoring wired for new features.
- [ ] Security review for auth / payment / PII changes (link to threat model).

## Notes

(any DoD line marked N/A - explain)
```

A reviewer reads this template + the actual PR state and
verifies each line.

## DoD evolution

The DoD should evolve with the team's quality bar:

- After an a11y incident → add the a11y line.
- After a security incident → add the threat-model line.
- After production-canary saved a regression → add the
  canary-passed line.

Don't lower the DoD without explicit retro discussion. Lowering
because "we kept failing the gate" usually means the team needs
better tooling, not a lower bar.

## Review cadence

| Cadence   | Trigger                                        |
|-----------|------------------------------------------------|
| Quarterly | Schedule a 30-min DoD review.                  |
| Post-incident | Add lines that would have prevented the incident. |
| New team member onboarding | Reread the DoD; pick up new perspective. |

## Auditing adherence

The other half of the lifecycle: a **compliance audit of work against the
checklist that already exists**. The checklist is an input, treated as fixed
for the duration of the audit; the output is a per-line verdict backed by
artifacts. Authoring is collaborative and can trade a line away; auditing is
adversarial and cannot. If a line turns out to be unenforceable, that is a
finding to hand back to the authoring conversation, not a licence to skip it.

Two facts from the 2020 Scrum Guide
([scrumguides.org/scrum-guide.html](https://scrumguides.org/scrum-guide.html))
anchor the audit: the team or organization owns the lines (so the audit never
invents or edits a line), and a miss has a defined consequence - an item that
does not meet the DoD "cannot be released or even presented at the Sprint
Review" and returns to the Product Backlog, so "not met" is not advisory.
Do not over-attribute: the November 2020 revision made the DoD a formal
*commitment* attached to the Increment
([scrumguides.org/revisions.html](https://scrumguides.org/revisions.html));
the Guide prescribes no checklist content, coverage number, or verdict
vocabulary - those are practitioner convention. Many teams also run an
entry-side "ready for development" checklist; it is auditable with the same
method but has no standing in the Scrum Guide, so declare which stage is
being audited before starting ("acceptance criteria" at entry means *they
exist and are testable*; at exit it means *covered by tests that ran and
passed*).

### Audit setup

- **Pin the checklist revision and the evidence window.** Record the
  checklist file path and commit / date, and what counts as evidence: for a
  PR, the diff range and the CI runs attached to the head commit; for a
  release, the commit range in the tag. A green CI run for a different SHA
  proves nothing about this one.
- **Split the checklist into atomic lines.** A compound line ("coverage >=80%
  and one test per AC") is audited as two lines. Do not derive lines from
  prose - if the checklist is a paragraph, hand it back for restructuring
  rather than substituting the auditor's reading for the team's intent.
- **Handle conditional lines explicitly.** "Docs updated (or no user-facing
  change)" has two satisfying branches; show evidence for whichever branch is
  claimed. "No files under the UI or API surface changed in the diff" is
  checkable; a bare assertion of the escape branch is not.
- **Scope one audit to one artifact** - one PR, one story, or one release
  candidate.

### Line-pattern to evidence mapping

| Line pattern | Artifact to read | How to read it |
|---|---|---|
| "reviewed by at least N engineers" | `gh pr view --json reviews,reviewDecision` | `reviews` and `reviewDecision` are documented JSON fields of `gh pr view` ([cli.github.com/manual/gh_pr_view](https://cli.github.com/manual/gh_pr_view)). Count approving reviews whose author is not the change author. Review actions are `APPROVE`, `REQUEST_CHANGES`, `COMMENT` ([docs.github.com/en/rest/pulls/reviews](https://docs.github.com/en/rest/pulls/reviews)). |
| "coverage on changed files at or above X%" | `coverage/lcov.info` or the CI coverage report | In an LCOV tracefile each file section carries `LF:` (instrumented lines) and `LH:` (lines hit) ([manpages.debian.org geninfo(1)](https://manpages.debian.org/bookworm/lcov/geninfo.1.en.html)). Per-file rate is `LH / LF`, computed only over files present in the diff. |
| "no new lint or type errors" | CI status checks for the head commit | `gh pr view --json statusCheckRollup`; compare against the same checks on the base. |
| "documentation updated" | `git diff --name-only <base>..<head>` ([git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)) | Require at least one changed path under the docs surface. Necessary, not sufficient: it shows a doc changed, not that it describes this change. |
| "every AC is covered by a passing test" | Criterion IDs in the ticket + test names / tags in the diff | Needs a team-declared convention linking criterion IDs to tests. Without one, `unverifiable`, not `not met`. |
| "no new accessibility violations" | The a11y scan output for both branches | An axe run returns a `violations` array ([github.com/dequelabs/axe-core](https://github.com/dequelabs/axe-core)). Compare head against base, not against zero, unless the line says zero. |
| "deployed to staging and smoke passed" | CI runs bound to the head commit | A completed deploy job and a completed smoke job, both for that exact SHA. |
| "telemetry wired for new code paths" | The diff itself | Search for the project's instrumentation calls on the newly added paths. A statement in the description is not evidence. |
| "security review for auth / payments / PII changes" | Linked review or threat-model record | The link must resolve and be dated within the change window. Unlinked = `unverifiable`. |
| "no new tech debt without a logged issue" | Linked issue | `unverifiable` by construction unless the team requires an issue link in the description. |

Thresholds come from the team's line, never from a default; if the line names
no number ("good test coverage"), it is `unverifiable` and the finding is
that the line is unenforceable as written.

### Three states, four evidence standards, one verdict

| State | Meaning | Required to assign it |
|---|---|---|
| `met` | Artifact exists and shows the line satisfied | Name the artifact and the value read from it |
| `not met` | Artifact located and read; shows the line unsatisfied | Name the artifact and the shortfall (actual vs required) |
| `unverifiable` | Cannot be settled from artifacts in the window | State what was searched, why inconclusive, and what the team must supply |

The three states apply per line and are never averaged - a checklist is not
scored out of ten. `unverifiable` is a real finding: the line names no
checkable condition, the convention does not exist, or the artifact was never
produced.

Evidence standards: **self-attestation is not evidence** (a ticked PR-template
checkbox is the claim under audit, not proof); **a doc claim with no diff is
`not met`**; **pre-existing failure is not a free pass** (a budget already
breached on base does not become an acceptable baseline); **urgency and size
do not waive lines** (a faster hotfix bar is a separate written checklist,
not an in-flight waiver).

| Condition | Verdict |
|---|---|
| Every line `met` | `ACCEPT` |
| Any line `not met` | `REJECT` |
| No `not met`, at least one `unverifiable` | `REJECT`, pending named human confirmation |
| No checklist found, or the checklist is unsplit prose | `INCONCLUSIVE` |

`unverifiable` never auto-passes - it clears only when a named person
supplies the missing evidence, recorded like any other artifact. No checklist
means no verdict: inventing a plausible generic one substitutes the auditor's
judgment for the team's, which the Scrum Guide assigns to the team or the
organization.

### Audit report shape

```markdown
## DoD adherence review - <artifact under audit>

**Stage:** stage-1-entry | stage-2-exit
**Checklist source:** <path> @ <revision>, <N> lines split into <M> audited lines
**Evidence window:** <base>..<head>, CI runs for <sha>
**Verdict:** ACCEPT | REJECT | INCONCLUSIVE
**met: <x>   not met: <y>   unverifiable: <z>**

| # | Checklist line | State | Evidence sought | What was found |
|---|---|---|---|---|
| 1 | ... | met | ... | ... |
```

Follow with a "Not met" block (required vs actual vs artifact per line), an
"Unverifiable" block (searched / blocked by / to resolve), and a one-sentence
recommended action tied to the verdict rules. A full stage-2 audit worked end
to end is in
[references/adherence-worked-example.md](references/adherence-worked-example.md).

Audit limitations: roughly half of a typical checklist is not
machine-checkable (review quality, "no new tech debt") and resolves to
`unverifiable` by construction; presence is not correctness (nothing reads
the doc to confirm it describes the change); evidence outside the window is
invisible unless recorded; and the verdict is advice, not enforcement -
deciding to ship anyway is a human decision worth recording next to the
report.

## Anti-patterns

| Anti-pattern                                                       | Why it fails                                                              | Fix |
|--------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| No DoD                                                              | Per [scrum-guide][sg], the team must define one if not org-mandated.     | Adopt the starter (above). |
| 30-line DoD that nobody can satisfy per-PR                          | Team marks everything "N/A"; defeats the purpose.                        | Trim to 7-10 lines covering the highest-value gates. |
| DoD as aspirational, not enforced                                   | "We have a DoD but PRs ship without meeting it."                         | Enforce it; PRs blocked on unmet lines. |
| Per-PR DoD different from team's "done"                              | Drift; team can't tell what's done.                                      | One DoD; one PR template referencing it. |
| Lowering the DoD when it gets in the way                            | Quality bar erodes silently.                                             | Discuss in retro before lowering; document the reason. |
| DoD never updated after an incident                                  | Same incident class recurs.                                              | Post-incident DoD review (above cadence). |
| Treating `unverifiable` as a pass in an audit                        | Hides the unknown; the team believes it is done when nothing was checked. | Verdict rules: unverifiable blocks until a named human supplies evidence. |
| Auditing against a generic checklist because the team has none       | Substitutes the auditor's bar for the team's ([scrum-guide][sg]).        | Report `INCONCLUSIVE`; author the DoD first (this skill's other half). |
| Rewriting or softening a line mid-audit                              | The checklist stops being a fixed bar and becomes negotiable under deadline. | Record the finding; renegotiate in the authoring conversation afterwards. |
| Passing a coverage line using the repo-wide percentage               | A high repo-wide number hides an untested new file.                      | Compute per-file rates over the diff's files only. |

## Limitations

- **Subjective per-team.** "What's good enough" varies; the DoD
  reflects the team's context, not a universal standard.
- **Coverage thresholds are arbitrary.** "≥80%" is convention; the
  right number depends on the codebase.
- **Some lines are unverifiable automatically** ("docs updated" needs
  human review). The DoD acknowledges these - mark them
  "unverifiable" rather than auto-passing.

## References

- [sg][sg] - Scrum Guide DoD: "a formal description of the state
  of the Increment when it meets the quality measures required for
  the product"; team owns it (or follows org-mandated minimum);
  items not Done return to the Product Backlog.
- `smoke-suite-gate` - CI gate
  that satisfies the "staging deploy + smoke passed" line.

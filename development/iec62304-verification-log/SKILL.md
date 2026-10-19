---
name: iec62304-verification-log
description: Write a pull request body that doubles as the software verification record for regulated (IEC 62304 / ISO 13485) software - one section per subfeature with executable verification instructions, binary acceptance criteria and results backed by evidence, a regression-analysis statement, traceability to the tracked record, and a reviewer checklist. Use when a change in a medical-device or otherwise regulated codebase is ready for review.
license: Unlicense
metadata:
  tags: "IEC 62304, ISO 13485, Verification, Pull Request, QMS"
  category: "code-review"
---

# Verification LOG pull request

Verification in IEC 62304 (unit and integration level) needs a record: what was verified, how, against which
criteria, with what result, by whom. Putting that record in the pull request body keeps it next to the code and
the review. The shape below is the minimum that survives an audit.

## Structure

```markdown
Closes #<tracked issue>
**Record:** <feature / issue / change id in the system of record>
**Affected products:** <...>
**Build and configuration under test:** <version, environment, device, backend>
**Regression analysis:** <what else this change could affect and what was re-run>
**Design documentation:** <not affected | updated: name>

## Checklist
- [ ] No errors in the console or logs during the verification run
- [ ] Automated tests pass; report attached or N/A with a reason
- [ ] Evidence attached below
- [ ] No secrets or local configuration committed
- [ ] Coding conventions followed; legacy code left internally consistent

# Verification LOG

## <subfeature or change 1>

<Added/Modified - one sentence>

*Verification Instructions:* <numbered steps a reviewer can execute: environment, configuration, actions, tool>

*Verification Acceptance Criteria:* <observable, binary or measurable>

*Verification Results:* <evidence: image or video (blank line before and after), test report summary, log excerpt>
```

## Rules

- One section per subfeature visible in the diff; a bug fix is one section; a configuration change is one section.
- Instructions name the exact environment and configuration; a reviewer who did not write the code must be able
  to execute them.
- Criteria are Yes/No or numeric with a threshold; "works as expected" is not a criterion.
- Results quote numbers ("14 passed, 0 failed", "closure reached 0.98 in 400 ms") and include the artefact.
  Automated tests are evidence for pure logic; interaction, hardware and UI behaviour need a run on the target.
- Failed criteria stay in the LOG with the follow-up record referenced; never delete a failed section.
- Regression analysis is mandatory for modified software: say what shares code or data with the change and what
  was re-tested.
- The reviewer is not the author; approval means the reviewer inspected or executed the instructions and the
  evidence. Mirror the outcome (Pass/Fail, date, reviewer, PR link) into the system of record.

## Automations that help

- A PR check that verifies the title convention, the presence of `# Verification LOG`, the three fields per
  section, evidence in the results, and a regression statement; advisory comment plus a label when missing.
- A release job that collects the merged verification PRs between two tags into a verification summary.

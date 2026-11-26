---
name: security-review
description: "Reviews a diff, branch or pull request for security problems and posts the findings as a GitHub review with severity, file and line. Use when asked for a security review, or when a change touches authentication, secrets, network exposure, dependencies or CI workflows."
---

# Security review

Find security problems in a change and report them where the change lives.

## When to use

- A pull request touches authentication, authorization, input handling, secrets, CI workflows,
  container images or infrastructure code.
- The user asks for a security review or vulnerability check.
- The work review found something that needs a second, security only pass.

## Steps

1. Determine the scope: a pull request number, a branch against its base, or the working tree.
   Read the diff with `gh pr diff` or `git diff <base>...HEAD`.
2. Run the harness security review when it is available (`/security-review` in Claude Code).
   Treat its output as a candidate list, not as the result.
3. Run the tools that exist in the repository or in `mise.toml`:
   `gitleaks git --no-banner --redact` for secrets, `zizmor` for workflows when present,
   `trivy fs .` or `grype dir:.` when present, `semgrep` when a config exists.
   Never install a tool for this. Name the ones that were not available.
4. Read the changed code for the classes a tool misses:
   - input reaching a shell, SQL, template, path or URL without validation
   - authentication and authorization checks that can be skipped
   - secrets in code, config, logs, test fixtures or workflow files
   - CI workflows: `pull_request_target`, unpinned actions, secrets in forks, script injection
   - infrastructure code: public exposure, missing encryption, wide IAM, `prevent_destroy` missing
   - dependencies: new packages, pinned versions, lockfile changes
   - containers: root user, writable root filesystem, latest tags
   Fixing an injection shaped defect starts by listing every input that reaches the same sink.
   The pull request says which inputs were found and which were already safe.
5. Verify every finding by reading the surrounding code. Drop what does not hold.
6. Group findings by severity: critical, high, medium, low. Each with file, line, the problem in
   one sentence and the fix in one sentence.
7. Post the result:
   - Pull request: `gh pr comment` with `Verdict: changes requested` as the first line when
     critical or high exists, `Verdict: comment` otherwise, then the grouped findings. A
     formal `gh pr review --request-changes` only with a review identity from config
     `review.token`, as the `review` skill describes. GitHub refuses it on a self-authored
     pull request, the comment then stands.
   - Branch or working tree: print the grouped list in the answer.
8. Never fix as part of the review. Fixes are a separate change, after the user or the work loop
   decided.

## Guardrails

- Never print a secret that was found. Name the file and line, redact the value.
- Never approve. A security review requests changes or comments, approval belongs to the review
  skill.
- Never weaken a check to make a finding disappear.
- No speculative findings. A finding without a code location is a question, not a finding.
- In CI, post only through the review API. No labels, no pushes.
- Public repository, finding describes a vulnerability already in the default branch with no fix
  merged yet: no exploit detail in a `gh pr comment`. Report it to the user directly, the same
  way step 7 already handles a branch or working tree. A finding about code this pull request
  itself introduces is unaffected and still goes through step 7 as normal. The baseline's
  security vulnerability rule requires this.
- Setting `labels.needsHuman` uses the snippet in `~/.claude/skills/README.md`: exactly
  one `ai:` state label remains afterwards.

## Config

- `labels.needsHuman` (default `ai: needs human`): set on the issue when a critical finding
  needs a human decision and the work loop is in use.

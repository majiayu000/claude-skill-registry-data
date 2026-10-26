---
name: maintain-simple_gh_aws_creds-run-integration-test
description: "Run the integration test of simple_gh_aws_creds against the real AWS account and this GitHub repository, as done before each release: CLI setup and rotate_key through mise exec, a local check of each key, and the test-aws-creds workflow after each, with the user's yes before each step that changes a real service. Use when the user asks for an integration test, an end-to-end or real-account test, to check the CLI against real AWS or GitHub, or is about to release."
---

Prove that the working tree's CLI works against the real AWS and GitHub APIs, using the committed config `.github/simple_gh_aws_creds.json` and workflow `.github/workflows/test-aws-creds.yml`. Run before each release.

Read ../maintain-simple_gh_aws_creds-base/SKILL.md, then:
- ../maintain-simple_gh_aws_creds-base/references/05-known-traps.md
- ../maintain-simple_gh_aws_creds-base/references/06-integration-test.md

## Steps

Follow the routine in `06-integration-test.md` section 6:

1. **Check the ground.** Run `mise run cov`; stop if it fails. Check the AWS profile read-only (`aws sts get-caller-identity --profile bmt_app_dev_us_east_1`, or the boto3 equivalent). Say which IAM user, account, and repository the test touches.
2. **`setup`**, after the user's yes, with the command in `06-integration-test.md` section 3. Report each step's result line; never print the key file.
3. **Check the key locally** with the script in `06-integration-test.md` section 4. Read-only, so it needs no yes. Expected: own user allowed, `list users` denied.
4. **Run the workflow**, after the user's yes, with the commands in `06-integration-test.md` section 5. Report the conclusion and the run URL. If it fails right after step 2, re-run once for IAM propagation before debugging.
5. **`rotate_key --yes`**, after the user's yes. Then repeat step 3 (no yes needed) and step 4 (after its own yes), to prove the new key reached GitHub.
6. **`teardown` only on request.** It is not part of the routine. Show the preview without `--yes` first, check the secret names against `05-known-traps.md` section 2, and run `teardown --yes` only after the user's yes.

A step that fails stops the test: report the error, and fix the code before re-running.

## Report

The commands run, each step's outcome (with masked key IDs only), each workflow run's URL and conclusion, and what was left in place (the IAM user, the current key, the secrets, the local key file).

Next step: `pywf-oss-release` if the test ran before a release; `pywf-oss-changelog` first if code changed to make it pass.

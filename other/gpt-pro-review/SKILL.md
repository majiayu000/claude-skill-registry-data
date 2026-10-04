---
name: gpt-pro-review
description: Send a PR to ChatGPT Pro via Surf Oracle and confirm its review comment landed.
disable-model-invocation: true
---

# GPT Pro review

Hands a finished PR to ChatGPT Pro through the browser. The ChatGPT GitHub connector reads the PR and posts the review comment itself. Runs after `draft-pr` has opened the PR and before `apply-review` acts on the findings. Read-only on the code.

## Step 1: Resolve the PR

```sh
gh pr view [<url or number>] --json url,headRefOid
uuidgen
```

Omit the argument for the current branch's PR. No PR means nothing to review: say so and point at `draft-pr`. Record the full PR URL, starting head SHA, and UUID as the review ID.

## Step 2: Check the Oracle lane

```sh
surf oracle list --json
```

Surf runs one Oracle job at a time. A job not yet `captured` blocks dispatch; wait on it with `surf oracle result <id> --wait --json`. Done when no job is in flight.

## Step 3: Dispatch

Read [references/review-prompt.md](references/review-prompt.md) and send its prompt verbatim, substituting the PR URL, starting head SHA, and review ID.

```sh
surf oracle ask "<prompt>" --model gpt-5.6-sol --effort pro --github --detach --json
```

Surf prints an exclusive-browser-access warning while dispatching; let it run. Print the returned `.id` to the user immediately so the job survives an interrupted session. On `model_verification_failed`, report it and stop: a Pro review needs the Pro picker confirmed. Done when you hold a job ID.

## Step 4: Wait and capture

```sh
surf oracle result <id> --wait --json
```

Pro reviews take minutes. On Ctrl-C or any exit before capture, print `surf oracle result <id>` as the recovery command; the ChatGPT conversation is the durable key. Done when the job state is `captured` and you hold `response`.

## Step 5: Deliver

Fetch the current head and comments:

```sh
gh pr view <PR URL> --json headRefOid,comments
```

Match the comment to this review ID, its stated reviewed SHA, and the captured response. Print the review with the model, job ID, reviewed SHA, and matching comment URL. If no matching comment exists, print the captured response and report that posting could not be confirmed. If the reviewed SHA is missing or differs from the requested SHA, report the review as unverified. If the current head has moved, report that the review does not cover the current revision.

Suggest `apply-review` for a verified review of the current head. For a follow-up on the same review, keep the job ID and use `surf oracle follow <id> "<question>" --detach --json`. Done when the review or incomplete-review response is delivered, with posting and revision status explicit.

## When this skill is the wrong fit

- Review of uncommitted changes, not a PR → `aa-second-opinion`
- Acting on findings that already came back → `apply-review`
- Landing the branch after review → `land-pr`

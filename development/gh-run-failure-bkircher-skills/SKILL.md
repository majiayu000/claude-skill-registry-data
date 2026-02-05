---
name: gh-run-failure
description: Use to analyze failures in GitHub pipelines or jobs.
---

<general_guidelines>
- Assume the `gh` tool is installed and configured.
- Avoid printing full logs; focus on the failing step.
- For large logs, prefer downloading artifacts.
- If a test case failed, specify which test and how to run it locally.
</general_guidelines>

## List recent runs
<example>
gh run list --limit 20 --json databaseId,createdAt,headBranch,event,conclusion,status,displayTitle \
    --template '{{range .}}{{printf "%8v  %-20s  %-8s  %-10s  %-10s  %s\n" .databaseId .createdAt .status .conclusion .event .displayTitle}}{{end}}'
</example>

## Inspect a single run
<example>
RUN_ID=123456789
gh run view "$RUN_ID" --json status,conclusion,createdAt,headSha,headBranch,event,workflowName,url
</example>

## Show only failed jobs or steps
<example>
gh run view "$RUN_ID" --json jobs --jq '
    .jobs[]
    | select(.conclusion != "success")
    | .name as $job
    | (.steps[]? | select(.conclusion != "success") | "\($job) :: \(.name) :: \(.conclusion)")'
</example>

## View failed jobs/steps output
<example>
gh run view "$RUN_ID" --log-failed
</example>

To focus on a specific job, first list them:
<example>
gh run view "$RUN_ID" --json jobs --jq '.jobs[] | "\(.databaseId)\t\(.name)\t\(.conclusion)"'
</example>

Then fetch that job's log:
<example>
JOB_ID=987654321
gh run view "$RUN_ID" --job "$JOB_ID" --log
</example>

## List artifacts from a run
<example>
gh run download "$RUN_ID" --list
</example>

## Download a specific artifact
<example>
gh run download "$RUN_ID" --name "test-logs" --dir /tmp/github-run-"$RUN_ID"
</example>

After downloading, search locally for errors:
<example>
rg -n "error|fail|exception" /tmp/github-run-"$RUN_ID"
</example>

## Compare failed and latest successful run

Get latest successful run ID:
<example>
BRANCH=main
OK=$(gh run list --branch "$BRANCH" --limit 50 --json databaseId,conclusion \
    --jq '.[] | select(.conclusion=="success") | .databaseId' | head -n1)
echo "$OK"
</example>

Diff their SHAs:
<example>
FAIL_SHA=$(gh run view "$RUN_ID" --json headSha --jq .headSha)
OK_SHA=$(gh run view "$OK" --json headSha --jq .headSha)
gh api repos/:owner/:repo/compare/"$OK_SHA"..."$FAIL_SHA" --jq '.commits[].commit.message' | sed 's/^/- /'
</example>

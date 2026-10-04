---
name: issue-links
description: Relate GitHub issues and PRs — pick the right edge type (blocked-by via GraphQL, parent/sub-issue, Closes/Fixes in PR body, plain mention) and apply it. Use when asked to link, block, depend on, make a subtask of, or close-on-merge.
---

# Issue links

Pick the *strongest accurate* relationship — but no stronger.

## Decision tree

- **Closes / Fixes / Resolves #N in PR body** — auto-closes on merge.
  Default when a PR ends an issue.
- **blocked-by / blocks** — A can't proceed or ship until B lands.
  Both are peer-sized; B is *not* a piece of A. Surfaces in the
  dependency graph and gates closing.
- **parent / sub-issue** — A is decomposition of parent B's work.
  Sub wouldn't exist on its own; parent isn't done until subs are.
  Subs roll up into parent's progress.
- **plain `#N` mention** — context only, no causal edge. Discussion,
  prior art, "see also". Default when nothing stronger fits.

The trap: reaching for parent/sub-issue when blocked-by is what's
meant, because sub-issues were the only hierarchy GitHub had for
years. Size test — peer-sized → blocked-by; smaller-than-parent →
sub-issue.

## How to apply each

### Closes / Fixes / Resolves

In the PR body or commit message:

```text
Closes #123
```

Same-repo number, or `owner/repo#123` cross-repo. Recognized verbs:
close, fix, resolve (any tense).

### blocked-by (GraphQL only — no `gh issue` flag, no REST)

Two round-trips minimum: GraphQL executes one operation per request
and `Mutation` doesn't expose `repository`, so query and mutation
can't share a document. The lookup is aliased so both IDs return in
one call (one rate-limit point), then the mutation runs.

```bash
read A_ID B_ID <<<"$(gh api graphql \
  -F owner=OWNER -F repo=REPO -F a=<A> -F b=<B> \
  -f query='
    query($owner: String!, $repo: String!, $a: Int!, $b: Int!) {
      repository(owner: $owner, name: $repo) {
        a: issue(number: $a) { id }
        b: issue(number: $b) { id }
      }
    }' --jq '.data.repository | "\(.a.id) \(.b.id)"')"

gh api graphql -f a="$A_ID" -f b="$B_ID" -f query='
  mutation($a: ID!, $b: ID!) {
    addBlockedBy(input: { issueId: $a, blockingIssueId: $b }) {
      issue { number }
      blockingIssue { number }
    }
  }'
```

Cross-repo: lift each alias above `repository` so each issue gets
its own repo selection in the same query:

```graphql
a: repository(owner: $oA, name: $rA) { issue(number: $nA) { id } }
b: repository(owner: $oB, name: $rB) { issue(number: $nB) { id } }
```

Removal: `removeBlockedBy(input: { issueId, blockingIssueId })`.
Read: `Issue.blockedBy`, `Issue.blocking`, `Issue.issueDependenciesSummary`.
Use `-f` (not `-F`) for `ID!` variables — `-F` coerces to Int/Bool.

### Parent / sub-issue

REST (no GraphQL needed). `sub_issue_id` is the sub's **database id**
(`.id` from the REST issue endpoint), not its number or node id; one
extra GET resolves it.

```bash
SUB_ID=$(gh api repos/OWNER/REPO/issues/<sub> --jq '.id')
gh api --method POST repos/OWNER/REPO/issues/<parent>/sub_issues \
  -F sub_issue_id="$SUB_ID"
```

Removal: `DELETE .../issues/<parent>/sub_issue` (singular) with the
same `sub_issue_id`. Reorder: `PATCH .../sub_issues/priority`.
Reparent: re-add with `-F replace_parent=true`. Read children:
`gh api repos/OWNER/REPO/issues/<parent>/sub_issues`. The MCP REST
tools `sub_issue_write` / `issue_read` (get_sub_issues) wrap the same
endpoints.

### Plain mention

Just `#123` in the body. No tooling.

## Procedure

1. Read both issues — what each is *for*. Don't link from the user's
   framing alone.
2. Apply the strongest accurate edge using the size test: peer-sized
   → blocked-by; smaller-than-parent → sub-issue; resolved-by-merge →
   Closes; otherwise → plain mention. If torn between two, surface;
   don't silently pick.
3. Verify it reads back: `Issue.blockedBy` / `Issue.subIssues` for
   graph edges, the PR body for Closes.

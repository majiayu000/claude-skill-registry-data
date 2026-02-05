---
name: go-sdk
description: Use when writing Go code to interact with Gitea API - automation, bots, integrations, migrations, or programmatic git forge operations
---

# Gitea Go SDK

## Overview

The official Go SDK for Gitea provides 332+ API methods with full type safety. Use it for bots, automation, integrations, and complex workflows. For quick CLI operations, use `gitea:tea-cli` instead.

## Quick Setup

```go
import "code.gitea.io/sdk/gitea"

// Create client
client, err := gitea.NewClient(
    "https://gitea.example.com",
    gitea.SetToken("your-token"),
)
```

```bash
go get code.gitea.io/sdk/gitea
```

See `references/authentication.md` in tea-cli for token creation.

## Quick Reference

| Task | Method |
|------|--------|
| **Repos** | |
| List my repos | `client.ListMyRepos(ListReposOptions{})` |
| Get repo | `client.GetRepo(owner, repo)` |
| Create repo | `client.CreateRepo(CreateRepoOption{})` |
| **Issues** | |
| List issues | `client.ListRepoIssues(owner, repo, ListIssueOption{})` |
| Create issue | `client.CreateIssue(owner, repo, CreateIssueOption{})` |
| Edit issue | `client.EditIssue(owner, repo, index, EditIssueOption{})` |
| **PRs** | |
| List PRs | `client.ListRepoPullRequests(owner, repo, ListPullRequestsOptions{})` |
| Create PR | `client.CreatePullRequest(owner, repo, CreatePullRequestOption{})` |
| Merge PR | `client.MergePullRequest(owner, repo, index, MergePullRequestOption{})` |
| **Releases** | |
| List releases | `client.ListReleases(owner, repo, ListReleasesOptions{})` |
| Create release | `client.CreateRelease(owner, repo, CreateReleaseOption{})` |

## API Categories

See `references/api-reference.md` for complete method list:
- Repositories (70+ methods)
- Issues & comments (50+ methods)
- Pull requests & reviews (40+ methods)
- Releases & attachments
- Organizations & teams
- Users, webhooks, actions

## Common Types

See `references/types.md` for struct definitions:
- `Repository`, `Issue`, `PullRequest`, `Release`
- `User`, `Organization`, `Team`
- `ListOptions` for pagination
- Option structs for create/edit

## Patterns

See `references/examples.md` for idiomatic patterns:
- Error handling
- Pagination
- Context usage
- Webhook handlers

## Authentication Options

```go
// Token auth (recommended)
client, _ := gitea.NewClient(url, gitea.SetToken(token))

// Basic auth
client, _ := gitea.NewClient(url, gitea.SetBasicAuth(user, pass))

// With 2FA
client, _ := gitea.NewClient(url,
    gitea.SetBasicAuth(user, pass),
    gitea.SetOTP(otp),
)

// SSH key
client, _ := gitea.NewClient(url,
    gitea.UseSSHPubkey(fingerprint, keyPath, passphrase),
)
```

## Common Patterns

```go
// Pagination
opts := gitea.ListOptions{Page: 1, PageSize: 50}
for {
    repos, resp, _ := client.ListMyRepos(gitea.ListReposOptions{ListOptions: opts})
    // process repos...
    if resp.NextPage == 0 {
        break
    }
    opts.Page = resp.NextPage
}

// Context support
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
client.SetContext(ctx)
```

## Common Mistakes

| Problem | Solution |
|---------|----------|
| Nil pointer panic | Always check error before using result |
| Missing pagination | Use `resp.NextPage` to get all results |
| Context timeout | Set appropriate timeout for bulk operations |
| Rate limiting | Check `resp.Header` for rate limit info |

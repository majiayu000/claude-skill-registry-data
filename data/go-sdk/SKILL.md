---
name: hcloud-go-sdk
description: Use when writing Go code to interact with Hetzner Cloud API - automation, infrastructure provisioning, bots, integrations, or programmatic cloud operations
---

# Hetzner Cloud Go SDK

## Overview

The official Go SDK for Hetzner Cloud provides type-safe access to 23+ resource types with automatic retries, action polling, and comprehensive error handling. Use it for bots, automation, integrations, and complex workflows. For quick CLI operations, use `hetzner:hcloud-cli` instead.

## Quick Setup

```go
import "github.com/hetznercloud/hcloud-go/v2/hcloud"

// Create client
client := hcloud.NewClient(hcloud.WithToken("your-api-token"))
```

```bash
go get github.com/hetznercloud/hcloud-go/v2/hcloud
```

## Quick Reference

| Task | Method |
|------|--------|
| **Servers** | |
| List servers | `client.Server.All(ctx)` |
| Get server | `client.Server.GetByID(ctx, 123)` or `GetByName(ctx, "web")` |
| Create server | `client.Server.Create(ctx, hcloud.ServerCreateOpts{})` |
| Delete server | `client.Server.Delete(ctx, server)` |
| Reboot/Reset | `client.Server.Reboot(ctx, server)` / `Reset(ctx, server)` |
| **Networks** | |
| Create network | `client.Network.Create(ctx, hcloud.NetworkCreateOpts{})` |
| Attach server | `client.Server.AttachToNetwork(ctx, server, opts)` |
| **Volumes** | |
| Create volume | `client.Volume.Create(ctx, hcloud.VolumeCreateOpts{})` |
| Attach volume | `client.Volume.Attach(ctx, volume, server)` |
| **Actions** | |
| Wait for action | `client.Action.WaitFor(ctx, action)` |
| Poll with callback | `client.Action.WaitForFunc(ctx, callback, action)` |

## API Categories

See `references/api-reference.md` for complete method list:
- Servers (create, lifecycle, networking)
- Networks, subnets, routes
- Volumes
- Firewalls and rules
- Load balancers, targets, services
- Floating IPs, Primary IPs
- SSH keys, images, certificates
- DNS zones (GA in v2.30.0)
- Storage boxes (experimental)

## Client Configuration

```go
client := hcloud.NewClient(
    hcloud.WithToken("token"),                    // Required
    hcloud.WithEndpoint("https://api.hetzner.cloud/v1"), // Custom endpoint
    hcloud.WithApplication("myapp", "1.0.0"),     // User-Agent
    hcloud.WithDebugWriter(os.Stderr),            // Debug logging
    hcloud.WithHTTPClient(customClient),          // Custom HTTP client
    hcloud.WithRetryOpts(hcloud.RetryOpts{        // Retry config
        MaxRetries: 5,
        BackoffFunc: hcloud.ExponentialBackoff(2, time.Second),
    }),
    hcloud.WithPollOpts(hcloud.PollOpts{          // Action polling
        BackoffFunc: hcloud.ConstantBackoff(500 * time.Millisecond),
    }),
)
```

## Common Patterns

See `references/patterns.md` for idiomatic patterns:
- Error handling
- Action polling
- Pagination
- Resource lookups

## Action Handling

All long-running operations return an `Action`:

```go
result, _, err := client.Server.Create(ctx, opts)
if err != nil {
    return err
}

// Wait for completion
if err := client.Action.WaitFor(ctx, result.Action); err != nil {
    return err
}

// Or with progress callback
err = client.Action.WaitForFunc(ctx,
    func(update *hcloud.Action) error {
        fmt.Printf("Progress: %.0f%%\n", update.Progress)
        return nil
    },
    result.Action,
)
```

## Error Handling

```go
import "github.com/hetznercloud/hcloud-go/v2/hcloud"

err := someAPICall()

// Check specific error codes
if hcloud.IsError(err, hcloud.ErrorCodeNotFound) {
    // Resource doesn't exist
}

// Get error details
if apiErr, ok := err.(*hcloud.APIError); ok {
    fmt.Printf("Error: %s - %s\n", apiErr.Code, apiErr.Message)
}
```

Common error codes:
- `ErrorCodeNotFound` - Resource doesn't exist
- `ErrorCodeInvalidInput` - Validation error
- `ErrorCodeForbidden` - Insufficient permissions
- `ErrorCodeRateLimitExceeded` - Rate limit hit (auto-retried)
- `ErrorCodeConflict` - Resource changed (auto-retried)
- `ErrorCodeLocked` - Another action running

## Common Mistakes

| Problem | Solution |
|---------|----------|
| Nil pointer panic | Always check error before using result |
| Action timeout | Use `ctx, cancel := context.WithTimeout(...)` |
| Missing pagination | Use `client.Server.All(ctx)` for complete list |
| Action failed | Check action error with `WaitFor()` return value |
| Rate limiting | SDK auto-retries, but add backoff for bulk ops |

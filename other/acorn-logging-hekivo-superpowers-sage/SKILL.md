---
name: superpowers-sage:acorn-logging
description: >
  Logging in Acorn/WordPress — Log::debug(), Log::error(), Log::channel(),
  custom log channels, daily log files, stack channel, Slack log notifications,
  exception handling logging, WordPress debug.log integration, WP_DEBUG_LOG,
  structured logging, context arrays, monolog handlers, log levels,
  emergency info warning error debug, lando logs, lando ssh tail log
user-invocable: false
---

# Error Handling & Logging with Acorn

Acorn uses Laravel's logging system inside WordPress. Logs are configured per-theme in `config/logging.php` and coexist with WordPress's native `debug.log`.

## When to use

- Structured logging with log levels (emergency, alert, critical, error, warning, notice, info, debug)
- Multiple log channels (daily rotating, single file, syslog, Sentry, custom)
- Exception reporting with context and stack traces
- Environment-aware logging (more verbose in dev, error-only in production)
- Integration with external monitoring (Sentry, Papertrail, Loggly)

## When NOT to use

- Simple `error_log()` calls for local debugging — still valid for quick traces
- WordPress-specific debug output (`WP_DEBUG_LOG = true`) — native WordPress debug log is complementary, not redundant
- Performance-critical paths where per-call overhead of the logger matters — prefer conditional `WP_DEBUG` gating

## Prerequisites

- Acorn installed and bootstrapped
- `config/logging.php` published (step shown below)
- `storage/logs/` writable by the web server user

## Using the Logger

```php
use Illuminate\Support\Facades\Log;

// Basic usage
Log::info('Order placed successfully');
Log::warning('API rate limit approaching');
Log::error('Payment gateway timeout');

// Always pass context as an array — never interpolate strings
Log::error('Payment failed', [
    'order_id' => $orderId,
    'gateway' => $gateway,
    'amount' => $amount,
]);

// Write to a specific channel
Log::channel('errorlog')->critical('Database connection lost');

// Write to multiple channels simultaneously
Log::stack(['daily', 'errorlog'])->error('Critical failure', ['trace' => $e->getMessage()]);
```

## Log Levels

From most to least severe — use the appropriate level:

| Level | Use for |
|---|---|
| `emergency` | System is unusable |
| `alert` | Immediate action required |
| `critical` | Critical conditions (component failure) |
| `error` | Runtime errors that need attention |
| `warning` | Unusual conditions, not errors |
| `notice` | Normal but significant events |
| `info` | General operational messages |
| `debug` | Detailed debug info (dev only) |

See [`references/channels.md`](references/channels.md) for channel config, custom channels, and WordPress debug.log bridge.
See [`references/structured-logging.md`](references/structured-logging.md) for context arrays, custom exceptions, and structured logging conventions.
See [`references/troubleshooting.md`](references/troubleshooting.md) for logs not appearing, permission errors, daily rotation issues, Slack not notified.

## Verification

- Write a test log entry (`Log::info('test', ['key' => 'value'])`) and confirm it appears in the expected log file (e.g., `storage/logs/acorn.log` or the daily rotated variant).
- Verify the correct channel is being used by writing to a named channel (`Log::channel('payments')->info('test')`) and checking the channel-specific log file.

## Failure modes

### Problem: Permission denied when writing to log file
- **Cause:** The web server process does not have write permissions on the `storage/logs/` directory or the log file itself.
- **Fix:** Fix permissions with `lando ssh -s appserver -c "chmod -R 775 /app/content/themes/{theme}/storage/logs"`. Ensure the `storage/` directory is writable by the web server user. In Lando, this is typically handled automatically but can break after manual file operations.

### Problem: Log channel not configured (driver not found)
- **Cause:** The channel name used in `Log::channel('name')` does not exist in the `channels` array in `config/logging.php`.
- **Fix:** Add the missing channel definition to `config/logging.php` with the appropriate driver (`single`, `daily`, `errorlog`, etc.) and path. Verify `config/logging.php` exists in your theme directory.

## Escalation

- If the log disk is full or storage permissions cannot be resolved at the application level, this is an infrastructure issue -- check disk usage with `df -h` and coordinate with the server administrator.
- If you need to route logs to an external service (Sentry, Datadog, Slack), add a custom channel driver in `config/logging.php` or use the exception handler's `reportable()` method.

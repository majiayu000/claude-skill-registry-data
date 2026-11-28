---
name: error-message-quality
description: Write errors and log lines that name the failing thing, the offending value, and the likely fix, for a reader with no context. Use whenever writing a throw/raise, catch/except block, log statement, validation message, assertion, CLI exit message, or API error response, and when reviewing a diff that adds any of these. Not for user-facing copy unrelated to failures.
---

# error-message-quality

Weak errors say "invalid config" or "something went wrong" and log `error occurred` with no stack. Strong errors let a stranger at 3am with no source access know what to look at first.

1. **Three parts: what failed, with what value, what to do.** `"config error: 'timeout' must be a positive integer, got '-5' in deploy.yaml"` beats `"invalid config"` by an hour of debugging. Include the identifiers that distinguish this failure from its siblings: which file, record ID, endpoint, which of the twelve retries, which loop item.
2. **Never swallow the cause.** When wrapping or re-raising, chain the original (`raise X from e`, `%w`, `cause`). When logging-and-continuing, log the exception with its stack, not just a string. A catch block that neither re-raises nor logs the exception needs a comment saying why, or it's a bug.
3. **Match the message to the audience.** User-facing messages say what the *user* can do ("file too large, max 10MB") and never leak internals (paths, SQL, stack traces, hostnames). Operator-facing logs carry the internals precisely so nobody has to reproduce. If one failure needs both, produce both: a safe message outward, a detailed log inward.
4. **Redact secrets at the source.** Tokens, passwords, keys, full connection strings, and auth headers never enter a message or log, including via wrapped exceptions or dumped request objects. Mask or truncate before formatting.
5. **Make messages greppable and unique.** Stable constant text with the variable parts as values (`"payment declined: code=%s order=%s"`), so on-call can search logs and code for the same string. Don't assemble the constant part dynamically, and don't reuse the same wording in two places: a grep on the message should land on one line of code.
6. **Follow the codebase's logging conventions.** Before adding a log line, look at how neighboring code logs: which logger, structured fields or format strings, existing field names (`request_id`, `user_id`, `order_id`). Reuse those names; attach the correlation or request ID when one is in scope.
7. **Log at the decision points you'd want during the outage:** the request that entered, the branch taken, the external call and its outcome. If a bug just cost you an hour because nothing logged the crucial value, add the log line that would have saved you.
8. **Right level:** errors are actionable problems; warnings are tomorrow's errors; info is narrative. Expected conditions (a cache miss, a client retrying) logged as errors train everyone to ignore errors.
9. **Trigger it once.** Before finishing, cause the failure (a test, a bad input, a forced exception) and read the actual rendered output as the 3am reader. If you can't trigger it, paste the exact rendered message in your report so a reviewer can judge it.

Test: with only this message and no source access, could someone tell what to look at first? If not, it's missing a part.

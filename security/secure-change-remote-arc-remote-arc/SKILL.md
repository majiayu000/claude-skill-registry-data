---
name: secure-change
description: Build or review code that handles login, permissions, user input, files, secrets, payments or personal data. Use this whenever a change adds an endpoint, a form, an upload, a query built from input, a webhook, a token or an admin action, even if security was not mentioned.
---

# Make a secure change

Most security bugs are ordinary omissions: a missing ownership check, a value
trusted because it came from the client, a token in a log. This checklist exists
to catch those, and is for defending your own software.

## When to use

The change touches anything in the description. Use it for a review as well.

## Steps

1. **List what enters the system.** Write down each value from outside your
   process: body, query, headers, cookies, files, webhooks, environment,
   third-party responses. Treat all of it as untrusted.

2. **Check authentication.** Each protected route must verify the caller on the
   server. Middleware only counts if this exact route goes through it.

3. **Check authorization on the resource.** Being logged in is not enough. Query
   with the owner in the filter, such as `WHERE id = ? AND user_id = ?`, and take
   the user id from the session, never from the request body. Check the role for
   admin actions.

4. **Validate input at the boundary.** Allow known good values. Check type, length,
   range and format. Limit list sizes, upload sizes and page sizes.

5. **Prevent injection.** Choose by destination:

   | Destination | Safe approach |
   | --- | --- |
   | SQL | Parameters, never string building |
   | HTML | Framework escaping, no raw HTML from input |
   | Shell | Argument arrays, no shell string |
   | File path | Resolve it, then confirm it stays inside the allowed folder |
   | Outbound URL | Allow-list hosts, block internal addresses |
   | Redirect | Allow-list destinations |

6. **Protect secrets.** Read them from the environment or a secret store. Keep them
   out of code, logs, errors, URLs and client bundles. Store password hashes with a
   standard algorithm, and store only hashes of long-lived tokens.

7. **Protect state-changing requests.** Check CSRF protection for cookie sessions.
   Verify webhook signatures. Add rate limits to login and other costly routes.

8. **Fail closed.** If a check errors or a dependency is down, deny the request. Do
   not reveal internals in error messages.

9. **Record sensitive actions.** Write an audit record of who did what, without
   secrets or private content.

10. **Test it.** Use the permission matrix in `write-tests`. Add invalid inputs, and
    a canary secret that must not appear in responses or logs.

11. **Finish.** Follow `verify-and-report`.

## Stop and ask when

- You would need to design your own crypto or session scheme.
- A check would have to be weakened to meet the task.
- You find an existing vulnerability. Report it, and do not include real exploit
  data or secrets in your report.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Hide the button in the UI | The API is still open | Enforce on the server |
| Take `user_id` from the request | Anyone can change it | Use the session |
| Fetch by id, then check later | Easy to forget, and can leak | Filter by owner in the query |
| Block known bad strings | Attackers find others | Allow known good values |
| Return the full database row | Leaks private columns | Return named fields |
| Log the whole request | Captures tokens | Log named safe fields |
| Commit a test key | It stays in history | Use environment variables |

## Example

```python
# Weak: any logged-in user can read any invoice.
invoice = db.get("SELECT * FROM invoices WHERE id = ?", invoice_id)

# Strong: the owner comes from the session and is part of the query.
invoice = db.get(
    "SELECT id, total, status FROM invoices WHERE id = ? AND user_id = ?",
    invoice_id, session.user_id,
)
if invoice is None:
    return not_found()
```

## Report

```markdown
Inputs: <what enters, and how it is validated>
Access: <who can do this, and where it is enforced>
Secrets: <how they are handled>
Tests: <401, wrong owner, right owner, invalid input, canary>
Open risks: <anything not handled>
```

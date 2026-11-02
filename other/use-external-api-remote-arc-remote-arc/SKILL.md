---
name: use-external-api
description: Use a library, SDK, CLI or web API correctly by checking the installed version and real docs instead of relying on memory. Use this whenever code calls a third-party package or service, when you are unsure of a method or parameter name, or when an API call fails. It prevents invented methods and outdated usage.
---

# Use an external API

Your memory of an API may be wrong or out of date, and invented method names often
look correct. The installed code and current docs are the truth.

## When to use

Any time you call something you did not write, unless the same call already exists
in this repository.

## Steps

1. **Find the existing usage.** Search this repository first, and copy how it
   creates clients, handles errors and sets timeouts.

2. **Find the exact version.**

   | Stack | Check |
   | --- | --- |
   | JavaScript | The lockfile, or `node_modules/<pkg>/package.json` |
   | Python | `pip show <pkg>` |
   | Go | `go.mod`, or `go list -m <module>` |
   | Rust | `Cargo.lock` |
   | Java | `mvn dependency:tree` |

3. **Read the source of truth.** In order of trust:

   1. Types or source of the installed package
   2. Official docs for that version
   3. The official changelog or migration guide

   Blog posts and forum answers can show you where to look, but confirm with one
   of these.

4. **Confirm that each name exists.** Search the installed package for each method
   and parameter you plan to use. If you cannot find it, do not use it.

5. **Run a small check.** Try the call in a small script or test, using a sandbox
   or test key. Do not use production data or paid operations for this.

6. **Handle real conditions.** Check each of these:

   - Timeouts on every network call
   - Rate limits, and which errors can be retried
   - Pagination, so that you do not read only the first page
   - Idempotency keys for writes that may be retried
   - Partial failure, and a response in an unexpected shape

7. **Isolate the integration.** Keep calls to the service in one place, so that
   tests can stub the network and upgrades touch one file.

8. **Test it.** Stub at the network, with responses taken from real docs or real
   sandbox calls. Follow `write-tests`.

9. **Finish.** Follow `verify-and-report`, and state which docs or version you used.

## Adding a dependency

Ask first if the task did not call for one. Check that it is maintained, its
license suits the project, and the standard library or an existing dependency
cannot do the job. Confirm the exact package name from its official source,
because similar names can be malicious. Pin it with the lockfile.

## Stop and ask when

- The call needs real credentials you do not have.
- The call costs money, sends messages or changes real data.
- Docs and installed code disagree, and you cannot tell which is right.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Write the call from memory | Names and defaults change | Check the installed version |
| Retry on any error | A repeated write can duplicate an effect | Retry only safe errors |
| Read only the first page | Silently loses data | Follow pagination |
| Use `latest` | Builds change without notice | Pin the version |
| Fake a response from your imagination | The test passes and production fails | Base it on a real response |
| Put an API key in the code | It leaks through history | Read it from the environment |

## Report

```markdown
Package or API: <name, version>
Source checked: <installed types or docs URL>
Check run: <what you called, and the result>
Handles: <timeouts, retries, pagination, idempotency>
Not verified: <anything not exercised for real>
```

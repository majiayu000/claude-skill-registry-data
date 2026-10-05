---
name: padosoft-failure-visibility
description: >-
  Use this skill whenever code can fail and the caller has to find out — a write to disk or storage, an
  external call, a catch block, an endpoint that returns a body, a fetcher, a renderer, a chart that reduces
  an array — and whenever the user says something "silently did nothing", data disappeared without an error,
  a request returned 200 but the page is empty, a job later died on something that was reported as accepted,
  or a retry loop never fires. It covers the two halves of the same bug: an ignored return value, and a
  success status served over a failure. It also covers the decision trace, for when nobody can reconstruct why a user got the
  outcome they got. Do not use it for what goes inside a log line
  (padosoft-logging-discipline) or for retry and timeout policy.
license: MIT
compatibility: >-
  Language-agnostic. The examples are PHP/Laravel and TypeScript/React because that is where the cases came
  from; the rule holds anywhere a call can fail.
metadata:
  version: 0.3.0
  author: Padosoft
  summary: The caller must be able to tell success from failure, and a check that does not decide is not a check.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: error handling, failure, status code, silent failure, exceptions, http, io
---

# Failure visibility

Two symptoms, one bug: **the caller cannot tell success from failure.**

1. A call that failed, whose return value nobody looked at.
2. A failure served with a success status, or an empty body, or a `null`.

Both leave a system that looks healthy while it loses work.

---

## 1. Never ignore the return value of a side-effecting call

Many APIs report failure by **returning a value**, not by throwing — especially file and storage APIs, and
HTTP clients configured not to throw.

```php
$ok = Storage::disk($disk)->put($target, $content);
if ($ok === false) {
    throw new RuntimeException("Unable to persist {$target} on disk {$disk}.");
}
```

The shape to recognise: a controller calls `Storage::put(...)` without checking the return, the disk is
configured with `throw => false`, a full disk returns `false`, **the controller answers `202 Accepted`**, and
the job that comes later dies with "file not found". From the client's side, ingestion silently drops
documents — and the only signal anyone gets arrives hours later, somewhere else.

Applies to storage put/delete/copy/move/makeDirectory, `file_put_contents`, `copy`, `rename`, `unlink`,
`mkdir`, and any library call that returns `false` on failure.

**Never log and continue.** A log line is not a return path: the caller still believes it worked.

### Two related bans

- **The `@` silencer** — `@mkdir(...)` hides the error and the return value in one character.
- **World-writable permissions** — `0777` on a directory created for a cache or a test fixture is not a
  convenience, and it usually appears next to the silencer.

```php
if (! is_dir($dir) && ! mkdir($dir, 0755, true) && ! is_dir($dir)) {
    throw new RuntimeException("Unable to create {$dir}.");
}
```

The double check is deliberate: between the test and the creation another process may have created it, and
that is not a failure.

## 2. Map the failure to the right status, everywhere it is observed

An empty body on 200, an empty PDF on 200, `null` returned from a fetcher after a catch, `-Infinity` or `NaN`
in chart coordinates — the same bug in four costumes.

| Situation | Correct |
|---|---|
| The resource does not exist | 404 |
| It exists and cannot be read | 500 |
| A dependency is down | 503 |
| A fetcher caught an error | **rethrow** — swallowing it makes the client think it succeeded |
| A reducer over a possibly empty array | guard the empty case explicitly |

```ts
// ❌ the query layer now reports isError = false, and the UI shows an empty happy path
catch (e) { return null; }
// ✅
catch (e) { throw e; }
```

```ts
// ❌ -Infinity when data is empty
const max = Math.max(...data);
// ✅
const max = data.length ? Math.max(...data) : null;   // and render the empty state
```

## 3. The status comes from the exception TYPE, never from its message

```php
// ❌ brittle: any copy change flips the status code
if (str_starts_with($e->getMessage(), 'File missing')) return response('', 404);
// ✅
catch (FileMissingException) { return response()->json([...], 404); }
catch (StorageUnreadableException) { return response()->json([...], 500); }
```

A message is user-facing text: it gets reworded, translated, prefixed with a code. Control flow must not
depend on it. Where the type is not distinct enough, add one — that is what exception classes are for.

## 4. Empty is not the same as missing, and neither is the same as broken

Three different answers, three different renderings:

- **empty** — the operation worked, there is nothing: an explicit empty state, and 200 is correct;
- **missing** — 404;
- **broken** — 500/503, and the UI says so.

Collapsing them into one blank screen is what makes a defect unreportable: the user cannot describe what they
saw, because they saw nothing.

Watch for the edge that gets discarded by a truncating conversion: a single-line file whose line count reads
as "0 lines", a count cast to `int` that swallows a legitimate zero, a fallback to `''` when a library
returned a non-string.

---

## 4b. The decision trace: being able to answer "why did this happen to this user?"

Logging is for diagnosing a failure. An audit trail is for proving nothing was altered. Neither answers the
question support actually gets: *why did this customer not see that option, and why was this one refused?*

For any funnel where the outcome matters — a checkout, an application, an onboarding, a claim — **every
decision that changes the outcome writes one line to a dedicated channel**, with a machine-readable reason.

- **Every `catch` traces**, even when it rethrows, and even when the user gets a generic message. A silent
  catch is a violation of this rule, not a style preference.
- **Every refusal shown to a user carries a reason code**, not only the translated sentence. The sentence is
  for the user; the code is for the person reconstructing the session three weeks later.
- **Every silent exclusion traces.** A payment method filtered out, a line dropped while reloading a basket,
  a discount removed by a later change: the reader has to find **why** the option was not there. This is the
  half that is always missing, because nothing went wrong — something merely did not appear.
- **Every external outcome traces a summary**, never the whole response and never the credentials.
- **What happens on every page view is not a decision.** A gateway that initialises on each product page
  produces dozens of rows per session with no decision behind them, and a channel that is mostly noise is a
  channel nobody opens. Trace the *failed* initialisation and the *selection*; skip the routine success.
- **Attach the configuration that was in force**, not just the event: the flags, the limits, the per-brand
  exceptions. Half the answers to "why" are in a setting, and the setting has changed since.
- **Put the explicit trace before the error log of the same failure**, so the generic handler does not
  produce a second line for one event.

The test of the channel: take a real complaint, open only this channel, and see whether you can answer it
without reading the code.

## 5. A check that does not decide is not a check

A verification that prints numbers for somebody to compare by hand is a note. A scheduled job that writes a
value into a log in case anyone looks is a note. The check exists when its outcome **reaches a person** who
can act on it.

- **The alert carries the decision, not the stack trace.** A generic "job failed" notification with sixty
  lines of framework trace, where the actual finding sits in a log line nobody opened, is a disabled control
  with a notification attached.
- **The job fails only when the alert reached nobody.** An anomaly that was successfully reported is a green
  job: the red belongs to the delivery failure, because that is the case where nothing else will surface it.
  Partial delivery — some recipients, not all — closes green and is written to the log at a level that
  cannot be filtered out, because "someone" is not "everyone" and the ones who missed it cannot tell.
- **Write the silence after delivery, never before.** Reserving a "do not repeat this alert" marker before
  sending makes it immune to the send failing: if the process dies in between, the channel stays quiet for
  days and nobody read anything.
- **One alert a day teaches people not to open any of them**, including the one that matters. A recurring
  *state* — a misconfiguration that does not resolve itself — needs a cooling-off period; a dated *event*
  does not, because it ages out on its own. And a suppression must never apply while there is a real finding.
- **A check that cannot decide must not report success.** An outcome that says "I was unable to verify" is
  not a pass; treating it as one switches off the control while leaving it apparently running. Split the
  warnings into actionable and descriptive, and let the actionable ones alert exactly like a finding.
- **Write the record at a level the environment cannot filter away.** The threshold comes from
  configuration, so anything that must survive when the alert does not arrive goes in above it.
- **Do not offer maintenance as an explanation it cannot support.** A key rotation invalidates signatures; it
  does not delete a file. Suggesting an innocent cause for something it cannot cause is the fastest way to
  get a real incident filed as noise.

---

## 6. A resolver that degrades silently hides an incomplete registration

A lookup that cannot find its entry and **returns the input unchanged** is the worst of the three states in
§4 at once: not found, nothing to do and broken all produce the same output. Register a new type in four
places out of five and the fifth one keeps working — for a value of "working" that means the feature quietly
does nothing, with no error and no log line, until somebody notices months later.

Two protections: the unresolved branch **logs and names the type it could not resolve**, and a test
enumerates the registered types and asserts that every resolver knows all of them. Adding a type then fails
loudly at the place that forgot it, instead of succeeding silently everywhere — see
**`padosoft-contract-changes`** for the general form.

## How to find it in a diff

```bash
# success status in what looks like an error branch
rg -n "response\(\)->json\([^)]*\],\s*200\)" app/Http/Controllers/
# fetchers swallowing errors
rg -n "catch[^{]*\{\s*return null" src/ frontend/src/
# unguarded reducers
rg -n "Math\.(max|min)\(\.\.\." src/ frontend/src/
# status driven by the message
rg -n "str_starts_with\(\\\$[a-z]+->getMessage" app/
# silencer and world-writable
rg -n "@(mkdir|file_put_contents|unlink|copy|rename)\(|0777" .
# storage writes whose result is discarded
rg -n "Storage::disk\([^)]*\)->(put|copy|move|delete)\(" app/ | rg -v "^\s*\\\$\w+\s*="
```

Every hit is a **candidate**, to confirm or discard — not an automatic finding.

## Gotchas

- **A caught exception that is logged and swallowed is the most expensive line in the file**, because it looks
  like handling. Handling means: recover, or translate into a failure the caller can see.
- **`throw => false` clients are a trap by design.** They exist so you can decide — which means you must.
- **A retry that never fires** is the second-order effect: the queue, the client or the user would have
  retried, and the false success took the option away.
- **The happy path is not the common path in production.** Disks fill, dependencies time out, files get
  deleted between the check and the read.
- **An empty state is a feature.** Without one, every failure mode renders identically.

## Checklist

- [ ] Every side-effecting call's return value checked, or the call genuinely throws
- [ ] No `@` silencer; no `0777`
- [ ] Failures mapped to 404 / 500 / 503 by **type**, not by message
- [ ] No fetcher returning `null` from a catch
- [ ] Reducers over arrays guarded for the empty case
- [ ] Empty, missing and broken render differently
- [ ] Tests that provoke the failure, not just the happy path

## Final report

```
Failure visibility: <n> files
Ignored return values: none | <file:line>
Success status over a failure: none | <file:line — what it should be>
Status driven by message: none | <file:line>
Empty / missing / broken collapsed: none | <where>
```

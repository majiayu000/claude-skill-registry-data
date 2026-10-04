---
name: publish-hotline
description: Turn a local program into a callable hotline on the delegated-execution network — write the worker, declare its contract, register, submit, approve, and verify it is genuinely callable. Use when someone wants to expose a script, CLI, model or service as a hotline, add a hotline to a responder device, or when a hotline was published but an agent cannot call it correctly.
---

# Publishing a hotline

A hotline is a local program plus a **contract**: what it takes, what it returns,
what it is not for, how long it needs, and what it costs. The program is the easy
half. Everything that goes wrong goes wrong in the contract, and it goes wrong
quietly — the hotline publishes, the catalogue looks fine, and a caller finds out
only when a call fails.

## The one rule everything else follows

**The contract follows the worker.** The worker declares it; nothing else is a
source of truth. The platform used to fill in missing schemas from a template
and once described a PDF parser to the public as a text summariser. It does not
guess any more — it says `contract_declared: false` instead — so a worker that
declares nothing publishes nothing usable.

## 1. Write the worker

A process-adapter worker is a program that:

- prints its contract as JSON to stdout when run with `--contract`, then exits 0
- otherwise reads one JSON task on stdin and writes one JSON result to stdout

```js
const CONTRACT = {
  contract_version: 1,                    // ← the positive signal; see the trap below
  input_schema:  { type: "object", required: ["text"], additionalProperties: false,
                   properties: { text: { type: "string", minLength: 1,
                     // Every input field needs one. A field a caller cannot fill
                     // in from the contract alone is a field nobody can call.
                     description: "The passage to shorten. Paste the whole thing." } } },
  output_schema: { type: "object", required: ["summary"], additionalProperties: false,
                   properties: { summary: { type: "string" } } },
  input_examples:  [{ title: "A request",  input:  { text: "..." } }],
  output_examples: [{ title: "Its result", output: { summary: "..." } }],
  not_recommended_for: ["what this is the wrong tool for"],
  limitations: ["what it cannot do even when used correctly"],
  service_tier: "quick"                   // quick | standard | deep
};

if (process.argv.includes("--contract")) {
  process.stdout.write(JSON.stringify(CONTRACT));
  process.exit(0);
}

let raw = "";
process.stdin.on("data", (c) => (raw += c));
process.stdin.on("end", () => {
  const task = JSON.parse(raw);
  const text = String(task?.input?.text ?? "");
  process.stdout.write(JSON.stringify({
    status: "ok",
    output: { summary: text.slice(0, 100) },
    usage: { tokens_in: text.length, tokens_out: 0 }
  }));
});
```

Failures are `{ status: "error", error: { code, message, retryable } }`. Say
`retryable: false` when retrying cannot help — a caller that retries a
permanent failure learns nothing and pays twice in time.

## 2. What the publication gate will refuse

There are two gates, and the first one is on your own machine.

`submit-review` refuses locally with `HOTLINE_INPUT_GUIDANCE_REQUIRED`, naming
the fields, unless **every property in `input_schema.properties` carries a
caller-facing `description`**. Reusing the phrasing the old guessing template
wrote — "source text", "optional task context", "instruction for the hotline" —
is refused as well: those exact strings are on a denylist, because they are what
the machine used to say when nobody had said anything.

Then approval fails with `CONTRACT_HOTLINE_INCOMPLETE` and an itemised list
unless the declaration has:

- **both** `input_schema` and `output_schema`
- **at least one worked example in each direction**, and each example must pass
  the schema it claims to illustrate
- **`not_recommended_for` or `limitations`** — a hotline with no stated limits
  is one that will be blamed for everything it was never meant to do

## 3. Register, submit, approve

```bash
DELEXEC_HOME=~/.delexec-<device> delexec-ops add-hotline \
  --type process --hotline-id my.thing.v1 \
  --cmd "node /abs/path/to/worker.mjs" \
  --fixed-price-cents 20 --currency PTS      # omit both for a free hotline

DELEXEC_HOME=~/.delexec-<device> delexec-ops submit-review --hotline-id my.thing.v1
```

Then the operator approves **two** things — in the console, or with a reason via:

```bash
POST /v2/admin/hotlines/:hotline_id/approve
POST /v2/admin/responders/:responder_id/approve     # a new device is pending too
```

Approving the hotline is what freezes version 1 and its content digest. But the
catalogue publishes an entry only when its responder is routable as well, so a
first device that approves only the hotline gets `catalog_visibility: "hidden"`
and a `/v2/hotlines/:id` that 404s — approved, frozen, and invisible.

## 4. Verify it is actually callable

Publishing is not the same as being callable. Check all three:

```bash
# the device's own view of what the platform is missing
DELEXEC_HOME=~/.delexec-<device> delexec-ops responder contract-check

# what the platform actually published (no credential needed)
curl -s <platform-api>/v2/hotlines/my.thing.v1 | jq '{input_schema, not_recommended_for, service_tier, execution_budget_s, pricing_hint}'

# what an AGENT sees — the surface that matters
curl -s http://127.0.0.1:8091/skills/caller/hotlines/my.thing.v1 | jq '{contract_source, local_only, pricing_hint}'
```

`contract_source` must be `platform_catalog`. If it is a local draft, the agent
is reading something the network never published.

`<platform-api>` is whatever the device has in `platform.base_url`, prefix
included — `https://callanything.xyz/platform` in production, and the bare
`http://127.0.0.1:8080` on a local stack, where platform-api is exposed
directly. Get it wrong on production and the edge answers 200 with the brand
site's HTML, so a check that only reads the status code passes while reading a
web page. And a 404 from the right prefix usually means the wrong id: the
published MinerU hotline is `local.mineru.pdf.parse.v1`, not
`mineru.pdf.parse.v1`.

`contract-check` is only as good as the version installed. Before 0.1.23 it
compared six fields — the two schemas, the two example sets,
`not_recommended_for`, `limitations` — leaving service terms and attachment
declarations outside its comparison entirely, and it compared them by
serialization, so the platform's own key order read as drift on every field
while all of them were identical. Against the production device it called the
MinerU hotline drifted on all six and told the operator to re-register a
declaration that was already correct. From 0.1.23 it compares by value and
includes the service terms and both attachment declarations, so `in_sync` means
what it says. Check `delexec-ops --version` before trusting either answer.

Service terms are compared only where the worker declared one: silence is a
request for the platform's default, not a disagreement with it.

Then make one real call and check the platform's own verdict — not the
responder's claim about itself:

```
GET /v1/admin/requests/:id → state.delivery_integrity.value == "verified"
```

`verified` means the output was checked against the contract this call pinned
and everything was checkable. `unchecked` means something could not be judged —
read `reason`, it names what.

Do not read `delexec-ops call-hotline`'s own exit as that verdict. While the
device is running its caller controller polls the relay inbox every 250 ms, and
the CLI's own pull then finds an empty inbox and blocks until it prints a bare
`[delexec-ops] timeout` — on calls the platform recorded as `delivered` and
`verified` a second after they were placed. The call worked; the command
narrating it did not. Take the request id and ask the platform.

## The traps

Each of these shipped to production at least once.

**Silence must be distinguishable from an answer.** A worker that does *not*
implement `--contract` still prints something parseable when asked. That is why
`contract_version` exists: it is the positive signal. Without it the client
mistakes noise for a declaration.

**Output files need `contract_role`.** If `output_attachments.file_roles` says a
role is required, each result artifact must carry `contract_role: "<that role>"`.
Result artifacts otherwise carry no role at all, and the delivery is graded
`unchecked` rather than verified — silently weaker, not failed. Note this is a
*different* vocabulary from an artifact descriptor's `role`
(`input`/`output`/`evidence`, which is the direction bytes travel).

**Document hotlines must declare `input_attachments`.** It is the sentence that
tells a caller a file is required and how to send it. A hotline that needs a PDF
and does not say so is uncallable by anyone who reads only the contract — which
is every agent.

**A registration draft outranks the worker that made it.** `add-hotline` writes
`~/.delexec-<device>/hotline-registration-drafts/<id>.registration.json` from the
worker's declaration once, and every later `add-hotline` for the same id reuses
that file instead of re-reading the worker. So the ordinary repair loop — the
gate names a missing field, you fix the worker, you re-register — fails with the
identical error, and nothing says why. Delete the draft to make the worker
authoritative again:

```bash
DELEXEC_HOME=~/.delexec-<device> delexec-ops remove-hotline --hotline-id my.thing.v1
DELEXEC_HOME=~/.delexec-<device> delexec-ops add-hotline   --hotline-id my.thing.v1 ...
```

`remove-hotline` deletes the draft with the entry; `add-hotline` alone never
refreshes it. Check `show-draft`, not the worker, when a gate error will not go
away.

**`service_tier` sets two clocks, not one.** The tier drives the acceptance
window (quick 24h / standard 72h / deep 7d) *and* the execution budget
(5m / 30m / 4h), and every clock in the system derives from that number, so a
real ML load on a cold model needs `execution_budget_s` declared explicitly.
Out-of-bounds values are **refused, not clamped**: a budget quietly moved is a
promise quietly changed.

Anything before 0.1.23 does not send them. The CLI read all three off the worker
into the contract profile and then dropped them before the draft, so a worker
declaring `quick` published as `standard` — a 1800 s budget and a 72 h window
nobody chose — and editing the draft by hand did not help either, though
`draft_meta.editable` lists the fields. It is not hypothetical: the production
`local.echo.priced.v1` is published that way now, on a hotline where the
acceptance window is what governs when money settles. Repairing one is a
re-registration and a fresh approval, because the corrected declaration moves
the digest. Read the published `service_tier` and `execution_budget_s` back from
the catalogue after every approval on any older client.

**A priced hotline needs consent that names the listing.** The caller must send
`billing.max_charge_cents`, and the consent must also name `pricing_hint_version`
and `trust_tier_seen` — agreeing to "20 PTS" without saying which listing said 20
is not agreement to anything checkable. The platform refuses otherwise.

None of that is exercised by the local stack. `BILLING_ENFORCEMENT` is unset in
`repos/platform/deploy/platform/.env`, so a fixed-price hotline called locally
settles as `none` with the reason "这次调用没有计费" and the caller is never
charged. A green local run says the call works, not that the price does. Use
`tools/paid-call-e2e.mjs`, which brings up its own Postgres with enforcement on.

**Resubmission: the digest decides.** A resubmission whose declaration hashes to
the published version keeps its approval. Anything that moves the digest —
including a changed display name — re-enters review, correctly. Silence about a
field carries it forward rather than clearing it.

**Never run a test suite while a device is running.** The supervisor binds fixed
ports (8079/8081/8090/8091/8092). On 2026-08-10 a test run reconfigured a
production device through one: five fixture hotlines written in and the real
hotline downgraded to `local_only`. The CLI now refuses on a `DELEXEC_HOME`
mismatch, but that guard does not cover tests talking HTTP to 8091 directly.
Stop the device first, every time.

Stopping it is manual. There is no `delexec-ops stop` — `start` has no opposite —
and `pnpm run dev:local:down` does not do it either: `dev:local:up` lets
`bootstrap` start the real device, then starts its own supervisor and relay on
the same ports, where they die of `EADDRINUSE`, and it is *those* dead pids that
`down` records and later kills. It removes the platform containers and leaves a
fully live device orphaned on every port. Check with
`lsof -nP -iTCP -sTCP:LISTEN | grep 807` and kill the supervisor pid yourself;
its children go with it.

## Where the truth actually lives

This file goes stale; those do not.

- publication gate and contract validation — `repos/protocol/packages/contracts/src/hotline-contract.js`
- what a frozen version contains — `HOTLINE_VERSION_CONTRACT_FIELDS` in `repos/protocol/packages/contracts/src/call-state.js`
- tier defaults and bounds — `repos/protocol/docs/current/spec/defaults-v0.1.md` §6.1–6.3
- the client-side gate and what actually reaches the platform — `validateHotlineRegistrationDraft`, `buildHotlineRegistrationDraft` and `buildHotlineOnboardingBody` in `repos/client/apps/ops/src/config.js`
- the service-term fields the platform will store — `SERVICE_TERM_FIELDS` in `repos/platform/apps/platform-api/src/server.js`
- a real worker, end to end — `repos/client/apps/ops/src/mineru-hotline-worker.js`
- the whole path exercised — `tools/agent-callability-e2e.mjs`

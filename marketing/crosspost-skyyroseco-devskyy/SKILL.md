---
name: crosspost
description: Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky, adapting each post per platform and never posting identical copy cross-platform. Use when the user wants one message distributed across social platforms. Do NOT use for authoring the content from scratch (content-engine) or for full launch orchestration across channels and email (marketing-campaign).
origin: ECC
---

# Crosspost

Distribute content across multiple social platforms with platform-native adaptation.

## When to use

- the user wants one message posted to multiple platforms
- publishing announcements, launches, or updates across social media
- repurposing a post from one platform to others
- the user says "crosspost", "post everywhere", "share on all platforms", or "distribute this"

**When NOT to use:**

- no source post exists yet — author it with `content-engine` first; this skill distributes,
  it does not invent
- the job spans landing pages, email sequences, and ads — that is `marketing-campaign`
- the account credentials are unavailable. Publishing is an external, irreversible write:
  no credentials means stop, deliver the drafts, and name what is blocked

## Inputs

Required before any adaptation — **absent input = stop, never guess**:

1. **Source content** — the single core message, plus the primary platform (where the audience
   is biggest). Its version is drafted first and gets the best treatment.
2. **Target platform list + priority order.**
3. **Credentials / posting surface** for each target, and confirmation the account is the right
   one. For SkyyRose product claims, facts come from
   `wordpress-theme/skyyrose-flagship/data/skyyrose-catalog.csv` only.
4. **Explicit go-ahead to publish.** Posting to a live account is an external write and is
   irreversible in practice (deletes do not un-see). **STOP AND SHOW the exact per-platform text
   and wait for `y` before any publish call** — one manifest, one `y`, one send. Approval never
   carries to the next platform.

## Platform specifications

| Platform | Max length | Link handling | Hashtags | Media |
|---|---|---|---|---|
| X | 280 chars (4000 Premium) | counted in length | minimal (1–2 max) | images, video, GIFs |
| LinkedIn | 3000 chars | not counted | 3–5 relevant | images, video, docs, carousels |
| Threads | 500 chars | separate link attachment | none typical | images, video |
| Bluesky | 300 chars | via facets (rich text) | none (use feeds) | images |

## Procedure

1. Draft the primary-platform version from the source content (use `content-engine` patterns).
2. Adapt per platform — write each to its own file so the checks can run:
   - **X** — hook first, not a summary; cut to the core insight fast; links out of the main body
     when possible; thread format for longer content.
   - **LinkedIn** — strong first line (visible before "see more"); short paragraphs with line
     breaks; framed around lessons, results, professional takeaways; more explicit context than X.
   - **Threads** — conversational and casual; shorter than LinkedIn, less compressed than X;
     visual-first where possible.
   - **Bluesky** — direct and concise inside 300 chars; community-oriented; feeds/lists for
     topic targeting instead of hashtags.
3. Run the Verification checks on the draft files. Fix anything red before showing the manifest.
4. STOP AND SHOW: print each platform's exact final text and char count, then wait for `y`.
5. Publish the primary platform first. Capture the post URL for cross-referencing.
6. Publish secondaries, staggered 30–60 minutes, with cross-platform references where useful
   ("longer thread on X").
7. Verify each post landed: fetch the returned post URL and confirm it resolves.

Attribution: if crossposting someone else's content, credit the source in every version.

### Posting surfaces

Native APIs — X API v2 · LinkedIn API v2 (OAuth 2.0) · Threads API (Meta) ·
Bluesky AT Protocol. A batch service follows this shape, with per-platform bodies never equal:

```python
import os
import requests

resp = requests.post(
    "https://api.postbridge.io/v1/posts",
    headers={"Authorization": f"Bearer {os.environ['POSTBRIDGE_API_KEY']}"},
    json={
        "platforms": ["twitter", "linkedin", "threads"],
        "content": {
            "twitter": {"text": x_version},
            "linkedin": {"text": linkedin_version},
            "threads": {"text": threads_version},
        },
    },
    timeout=30,
)
resp.raise_for_status()
```

Credentials come from the environment only — never inline a token in a draft or a log line.

# Verification

Run every check **before** the STOP-AND-SHOW manifest, and the live check after publishing. A
check that errors (missing draft file → grep/awk exit 2) is a dead gate, not a pass (bug-230).

1. **Per-platform length ceiling** — over-limit copy is truncated or rejected silently:

```bash
awk 'length($0) > 280 {print "OVER-LIMIT line " NR ": " length($0) " chars"; bad=1} END {exit bad}' x.txt
```

   **PASS:** no output, exit 0. Re-run per platform with its own ceiling (X 280 · Threads 500 ·
   Bluesky 300 · LinkedIn 3000). `[repro]`

2. **No identical copy across platforms** — this skill's core rule, made falsifiable:

```bash
sort x.txt linkedin.txt threads.txt | uniq -d | grep -v '^[[:space:]]*$'
```

   **PASS:** no output (final grep exits 1). Any returned line is verbatim on two platforms —
   rewrite one before the manifest. `[repro]`

3. **The post actually landed** — a 200 from the API is not proof the post is visible:

```bash
curl -sI "https://x.com/<handle>/status/<id>" | head -1
```

   **PASS:** `HTTP/2 200`. A 404 means the publish reported success and did not stick —
   re-verify by hand rather than trusting the API response. `[live]`

Check 2 was proven able to fail before being trusted (rule 3): run it once with the same body in
two files and confirm the duplicate line is returned; then restore. **A SKIP is not a PASS** — a
platform whose length ceiling was not checked stays unchecked, and the drafter says so in the
manifest rather than letting silence read as green.

## Worked example

Real run, 2026-07-28, adapting one Black Rose drop message for X and LinkedIn. Drafts written to
the session scratchpad.

The first X draft ran 293 chars — over the ceiling, gate red:

```bash
$ awk 'length($0) > 280 {print "OVER-LIMIT line " NR ": " length($0) " chars"}' x.txt
OVER-LIMIT line 1: 293 chars
```

Trimmed to 238 chars, then both gates green:

```bash
$ wc -c < x.txt
238
$ awk 'length($0) > 280 {print "OVER-LIMIT line " NR ": " length($0) " chars"; bad=1} END {exit bad}' x.txt && echo "PASS: all lines <= 280"
PASS: all lines <= 280

$ sort x.txt linkedin.txt | uniq -d | grep -v '^[[:space:]]*$'; echo "exit=$?"
exit=1
```

All outputs observed this session `[repro]`. Zero shared lines: the X version opens
"Black Rose is armor."; the LinkedIn version reframes the same facts as a make-story with an
explicit takeaway line. Nothing was published — no credentials were manifested and no `y` was
given, so this run stops at drafts `[repro]`.

## Failure modes

| Failure | What it looks like | Rule |
|---|---|---|
| Identical copy shipped | `uniq -d` returns shared lines, or was never run | The one rule this skill exists to enforce. Run check 2 on every set |
| Published without a manifest | posts appear before the user said `y` | External irreversible write. One manifest → one `y` → one send; approval never carries to the next platform |
| Truncated CTA | link or ask cut off by the platform limit | Run check 1 per platform ceiling; links count toward X length, not LinkedIn |
| API 200 read as "posted" | success response, post not visible | bug-230 fail-open shape. Confirm with check 3 against the real URL `[live]`; a `[repro]` API response does not carry a `[live]` claim |
| Token leaked into a draft or log | credential visible in output | Environment variables only; never inline, never echo |
| Hallucinated product claim | invented price, drop date, or SKU | Catalog CSV is the only product manifest — plausible ≠ sourced (bug-096 shape) |
| Unchecked platform assumed fine | "all platforms verified" after checking one | A SKIP is not a PASS. Name the unchecked platform and who closes it |

## Related skills

`content-engine` (authoring the platform-native drafts) · `brand-voice` (the voice profile) ·
`marketing-campaign` (full multi-channel launch). Checked 2026-07-28: no `x-api` skill is
installed in `.claude/skills/` or `~/.claude/skills/` `[repro]` — X publishing means a direct
API call, not a skill handoff.

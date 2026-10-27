---
name: caido-replay
description: Replay a captured Caido request with mutations, diff response against baseline. Use when investigating a specific endpoint or when the user names a request id. Mutations include header swaps, param fuzz, method overrides, body tampering.
---

# caido-replay

## Purpose
Drive Caido's request-replay capability programmatically with diff
analysis. Single-request fuzz with surgical mutations is where most
business-logic and auth bugs surface.

## Inputs
- `<request_id>` from a Caido project.
- Mutation spec (defaults provided; user may override).

## Mutation spec format
```json
{
  "variants": [
    { "name": "no_auth", "drop_headers": ["Cookie", "Authorization"] },
    { "name": "user_b",  "set_headers": { "Cookie": "{{caido:user-b-cookie}}" } },
    { "name": "method_swap_post_to_put", "method": "PUT" },
    { "name": "param_fuzz_id",
      "param_fuzz": { "name": "id", "values": ["1","../etc/passwd","' OR 1=1--"] } }
  ],
  "diff": {
    "ignore_headers": ["Date","X-Request-Id","Set-Cookie"],
    "ignore_body_regex": ["\\\"timestamp\\\":\\d+"]
  }
}
```

## Steps
1. Resolve baseline: `caido_request_get(request_id)`.
2. For each variant, build the modified request, send via
   `caido_replay(request, variant)`. Caido returns the new response.
3. Diff each response against baseline (status, content-length,
   body — applying ignore rules).
4. Score each variant:
   - `interesting`: status differs OR body differs by > 50 bytes
     after normalization OR auth-related header appears/disappears.
   - `boring`: variant produced essentially identical response.
5. Write `targets/<name>/caido/replays/<request_id>/diffs.json`
   with structure:
   ```json
   { "baseline": {...},
     "variants": [{ "name": "...", "request": {...}, "response": {...},
                    "diff": {...}, "interesting": true,
                    "evidence": "..." }, ...] }
   ```

## Outputs
- `targets/<name>/caido/replays/<request_id>/diffs.json`

## Failure modes
- Request not found in Caido project → user supplied wrong id;
  list 10 most recent for them.
- Variant fails with 5xx → log; not interesting unless baseline also
  5xx'd.
- Rate limited by target → back off (`Retry-After` header or 30s
  default); resume.

## Result block
```json
"phases": { "replay": { "status": "done", "ts": "<iso>",
  "req_id": "...", "variants": N, "interesting": M } }
```

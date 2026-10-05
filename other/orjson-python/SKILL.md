---
name: orjson-python
description: Use for writing, reviewing, debugging, or testing Python JSON serialization and deserialization with orjson, including bytes/text boundaries, datetimes, dataclasses, NumPy, custom default handlers, option flags, strictness, and web/file integration. Do not use for JSON Schema validation, format-preserving JSON edits, streaming I/O frameworks, or choosing a JSON library when orjson is not requested or present.
argument-hint: "[orjson serialization task, contract, code, or failure]"
---

# orjson Python

Treat JSON as a wire/storage contract. Decide the accepted Python domain, JSON
shape, text/bytes boundary, datetime and integer policy, key ordering, and error
behavior before selecting options.

## Boundary

Use this skill when the project imports orjson or explicitly requests it. Do
not introduce orjson solely from a vague performance claim; benchmark the real
payload and preserve the surrounding interface. orjson encodes/decodes values;
it does not own file I/O, JSON Lines framing, schema validation, HTTP content
types, or format/comment preservation.

## Know the values

| Object | Contract |
|---|---|
| `orjson.dumps(value, ...)` | Returns UTF-8 JSON as `bytes`, never `str`. |
| `orjson.loads(data)` | Accepts UTF-8 `bytes`, `bytearray`, `memoryview`, or `str`; returns ordinary Python JSON values. |
| `default(obj)` | Converts one unsupported object to a supported value or raises `TypeError`. |
| `option` bitmask | Explicitly changes encoding semantics; combine flags with `|`. |
| `JSONEncodeError` | Serialization contract failure; a `TypeError` subclass. |
| `JSONDecodeError` | Invalid input/type/depth failure; compatible with `json.JSONDecodeError`/`ValueError`. |
| `Fragment` | Injects already-serialized JSON without validation/escaping; a trust boundary. |

Read [serialization contracts](references/data-contracts.md) before replacing
stdlib `json`, encoding temporal values, or accepting arbitrary keys.

## Ordered workflow

1. Recover the external contract: JSON shape, field names, accepted input
   types, byte/text owner, newline/framing, datetime/timezone form, number
   limits, ordering, and error mapping.
2. Inspect the installed orjson version and the existing adapter. Preserve a
   public `str` return only by decoding once at that boundary; preserve bytes
   for binary HTTP/file/socket APIs.
3. Start with no options. Add one option only for a named contract requirement,
   not because an example includes it.
4. Use native supported types where their semantics match. Add a narrow
   `default` dispatcher for project-owned unsupported types; never return an
   unsupported object or stringify every unknown value.
5. Keep I/O/framing outside `dumps` and `loads`. Add exactly one newline per
   JSON-lines record; do not parse an entire JSONL file as one JSON value.
6. Map encode/decode errors at the application boundary without swallowing the
   input location/cause or leaking payloads.
7. Test exact decoded structure plus byte-level requirements such as newline,
   key order, timezone spelling, or rejection behavior.

## Decision table

| Requirement | Action |
|---|---|
| Binary response/body/file API | Pass `dumps` bytes directly. |
| Text API explicitly requires `str` | Decode UTF-8 once at the outer boundary. |
| Input already bytes-like | Pass it to `loads`; do not decode first. |
| Pretty human file | Use indentation only if whitespace is contractual; append newline deliberately. |
| JSON Lines | Encode each record separately and delimit records; do not wrap in an array. |
| Datetime contract requires UTC `Z` | Normalize awareness/policy, then use the verified UTC option or explicit adapter. |
| Naive datetime has no declared timezone | Reject or normalize before encoding; do not silently invent local/UTC meaning. |
| Non-string dict keys are part of the schema | Confirm supported key domains and collision risks before the non-string-key option. |
| JavaScript-safe integer range is required | Enable strict integer behavior or validate at the domain boundary. |
| Deterministic lexical key order is required | Use sorted keys and test bytes; do not call it canonical JSON without a full canonicalization spec. |
| Unknown object | Serialize through a type-specific `default`; otherwise raise. |

## Canonical boundary

```python
from decimal import Decimal
from pathlib import Path
from typing import Any

import orjson


def default(value: Any) -> Any:
    if isinstance(value, Decimal):
        return format(value, "f")  # schema declares a decimal string
    if isinstance(value, Path):
        return value.as_posix()  # schema declares a POSIX path string
    raise TypeError(f"unsupported type: {type(value).__name__}")


def encode_event(event: object) -> bytes:
    return orjson.dumps(event, default=default)


def decode_event(payload: bytes | bytearray | memoryview | str) -> dict[str, Any]:
    value = orjson.loads(payload)
    if not isinstance(value, dict):
        raise ValueError("event JSON must be an object")
    return value
```

`loads` validates JSON syntax, not the application shape. Validate the returned
object separately. `default` normally sees only types orjson does not already
serialize natively; dataclasses and datetimes need passthrough options before a
custom handler can override their native representation. A `default` function
must raise `TypeError` for unsupported values so contract errors remain visible.

## High-risk options and integration

- Option flags are not general best practices. Each changes observable output
  or accepted types and needs a protecting test.
- Native datetime serialization does not decide the business meaning of naive
  values. Establish timezone policy before encoding.
- Non-string keys can serialize different Python keys to the same JSON member
  name; reject ambiguity when round-tripping or signatures matter.
- Pretty printing, key sorting, and newline flags add work. Use them for a
  contract, not a generic speed path.
- `Fragment` trusts its bytes as JSON and skips validation/escaping. Accept it
  only from a controlled serialized source, never raw user text.
- In web frameworks, adapt to their response class/renderer contract. Avoid a
  second `json.dumps` around orjson bytes and set the JSON media type.

Read [options and integration](references/options-integration.md) for these
branches.

## Error and verification contract

Invalid input, unsupported objects, non-finite values, excessive depth, integer
limits, and invalid UTF-8 need explicit behavior. Do not return `{}`/`None` on a
decode failure unless that fallback is a documented domain rule. Test malformed
JSON and unsupported types, not only round trips; a lossy encoder can round-trip
its own mistake.

Read [testing JSON behavior](references/testing.md). This foundry did not have
orjson installed during authoring, so its cases use static/source evidence and
must not be described as local runtime validation. Completion requires exact
outer type (`bytes` or `str`), declared temporal/number/key semantics, narrow
custom encoding, correct framing, explicit shape validation, and negative tests
for malformed and unsupported input.

## References

- [Serialization contracts](references/data-contracts.md)
- [Options and integration](references/options-integration.md)
- [Testing JSON behavior](references/testing.md)

---
name: yuzu-proto
description: Maintain Yuzu's protobuf wire contracts, code generation, and gateway proto mirrors. Use when editing `.proto` files, `proto/gen_proto.py`, `proto/meson.build`, `proto/buf.yaml`, or any file under `gateway/priv/proto`.
---

# Yuzu Proto

## Own The Canonical Sources

- Treat `proto/yuzu/**` as the canonical wire contract.
- Treat `gateway/priv/proto/**` as gateway mirror files consumed by rebar3 and gpb from `gateway/rebar.config`.
- Keep both gateway mirror layouts aligned: nested `gateway/priv/proto/yuzu/**` and flat `gateway/priv/proto/*.proto`.
- Do not trust mirror files to already be current. They have drifted before.

## Preserve Compatibility

- Preserve field numbers.
- Do not remove fields or change field types.
- Never delete anything from a `.proto` (field, oneof, enum value, message, enum, rpc, service, file), even with `reserved` — owner ruling 2026-10-26 (#6555). Retire an item by ceasing to use it and marking it `[deprecated = true]` / `option deprecated = true;` where protobuf has that option (a oneof has none: deprecate its fields). Moving a type to another file counts as a deletion. `proto/buf.yaml` enforces this with the `*_NO_DELETE` breaking rules.
- `deprecated` is metadata only. A security-motivated RPC retirement must also remove every handler that serves it: the server's, the gateway's, and any upstream RPC the gateway forwards it through (each removed handler then answers UNIMPLEMENTED). A deletion that reaches dev is reverted; a deliberate removal needs a new owner ruling and the scoped `ignore_only` procedure in `proto/buf.yaml`. protoc marks a deprecated field's C++ accessors `[[deprecated]]`, so code that still reads it during a mixed-version window will warn.
- Treat `buf breaking` as the baseline contract check, not an optional extra.

## Preserve Codegen Behavior

- Update `proto/meson.build` if a canonical proto file is added, removed, or renamed.
- Preserve `proto/gen_proto.py` header-flattening behavior unless all C++ include sites are being updated intentionally.
- Rebuild both C++ and gateway consumers after changing a wire contract.

## Sync And Validate

- Edit the canonical proto first.
- Propagate the same schema to every gateway mirror file before validating.
- Run `buf lint proto`.
- Run `buf breaking proto --against '.git#subdir=proto,ref=origin/main'` when repository history is available.
- Rebuild the proto library and any affected gateway consumers.

## Invoke Sibling Skills

- Invoke `$yuzu-meson` if the proto target list or build graph changes.
- Invoke `$yuzu-build` for compile and suite selection.

## Read On Demand

- `proto/yuzu/**`
- `proto/meson.build`
- `proto/gen_proto.py`
- `proto/buf.yaml`
- `gateway/rebar.config`
- `gateway/priv/proto/**`

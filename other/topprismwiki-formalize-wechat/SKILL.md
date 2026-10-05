---
name: topprismwiki-formalize-wechat
description: Process approved WeChat private and group-chat intervals into evidence packages and governed formal knowledge. Internal child module of $topprismwiki.
---

# WeChat formalization

Use only an approved session registry and a closed Asia/Shanghai interval. Keep
the raw export and sensitive evidence in Workspace. Each message and
attachment receives a terminal or retryable status and a source anchor.

Required capability gates:

- A `wechat-cli` adapter or an equivalent export provider.
- `officecli` for Office attachments and a visual model for image/PDF/PPT
  attachments.
- `ffmpeg` plus a Chinese-capable ASR adapter for audio/video, when present.

Route visual work to `vision-reviewer`, ordinary extraction to `text-extractor`,
and identity, relationship, or conflict decisions to `adjudicator`. No worker
may write the formal Vault. Only a reviewed, hash-bound decision package may
reach the committer.

Never infer a customer, project, delivery, adoption, or person relationship
from a group name, member list, filename, or single brand mention. Use
`preview` for inspection and require explicit update authorization for commit.
See [wechat-contract.md](../../references/wechat-contract.md).

## Execution contract

This child module is for an approved WeChat source unit. It does not export or
scrape WeChat itself. A private adapter must produce UTF-8 JSONL under the
configured project's `workspace/inbox/wechat/` and retain the original snapshot
outside Git. Read [adapter-contracts.md](../../references/adapter-contracts.md)
before accepting adapter output.

The adapter, not the public Runner, owns approved-session lookup, the closed
Asia/Shanghai interval, message identity, attachment attribution and durable
per-session watermarks. Every unit must carry a session alias, interval,
message/attachment counts, classification, state and source SHA-256. An
adapter failure or uncertain attachment is isolated; it does not advance a
watermark.

## Standard route

1. Run `doctor --capability wechat --strict` and check the adapter version and
   private project path.
2. Freeze the approved session registry and requested interval; never infer
   approval from a group name.
3. Snapshot and hash the source, run the adapter, and inspect coverage before
   `preview --source wechat`.
4. Route visual attachments to `vision-reviewer`, ordinary extraction to
   `text-extractor`, and identity, relationship or conflict decisions to
   `adjudicator`. Workers cannot write the formal Vault.
5. Build a hash-bound review package. Only an explicitly authorized `update`
   may reach the deterministic committer, followed by `validate`.

## Evidence and failure rules

Do not treat a private chat, group name, member list, filename or one-off brand
mention as proof of a customer, project, delivery, adoption or person relation.
Keep private raw messages and media in Workspace. For a blocked unit, run
`diagnose --unit-id <id>` and search the error code in
[`docs/zh-CN/troubleshooting.md`](../../../../docs/zh-CN/troubleshooting.md).
The complete user-facing path is [adapters](../../../../docs/zh-CN/adapters.md)
and [operations](../../../../docs/zh-CN/operations.md).

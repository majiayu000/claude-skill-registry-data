---
name: logCli
description: Use Log's platform command catalog and scoped guides; preserve the selected workspace log.db model, engine sessions and current authorization gates.
---

# Log CLI

## Current scope

Log is platform agnostic. Native hosted development follows AGENTS.md rules 171/172/175 and docs/proposals/listeningKitSchema.md. Existing SQLite and private engine files are the foundation. Treg is the hosted identity/control reference only. Old listing/campaign features are deferred for the native V1.

Current CLI account/session paths still have legacy dependencies. Use the implementation's current guide when operating them; do not claim they already use the proposed native repository. No generated account/CRM object defines the target schema.

## Procedure

1. Read current AGENTS.md and the task's relevant guide/use-case, not the historical rules snapshot.
2. Discover the command with logSearch, read exact inputs with logGet, and call through logCall or its dedicated tool. Shared commands stay shared; platform commands use log <platform> <command>.
3. Resolve the selected account/workspace and its current owner. Context reads use log.db when eligible; live catch-up goes through that owner.
4. Preserve authorization, governor/refusal, browser/profile and claim gates. Live actions need the authorization their tool defines. Do not send messages merely because a read succeeded.
5. Stream long-call progress and read platform answers to decide the result. Preserve private evidence; uncertain writes reconcile before retry.
6. Report the actual result and any missing implementation boundary. Native schema edits alone do not remove current runtime dependencies.

## Secrets and storage

Credentials, sessions, messages and detailed execution stay at the selected private runtime or actual browser host. Never print keys/cookies, commit raw captures or copy private payloads into central metadata. AdsPower installation keys remain separate from Log pairing tokens.

## Historical procedures

The old Marketplace-only guide is retired. Use current platform guides for a specific supported operation. Do not import historical data models into native hosted development.

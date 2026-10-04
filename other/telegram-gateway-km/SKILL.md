---
name: hermes__telegram-gateway
description: >-
  Hermes Agent's Telegram gateway — bot identity, slash-command routing,
  callback handling, threading behavior, and the local custom Telegram features
  carried on this machine. Use when changing or verifying Telegram-specific
  Hermes behavior.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Hermes Telegram Gateway

Use this skill for Telegram bot behavior, adapter changes, callback workflows, and verification of local Telegram customizations.

## Local customization rule

Durable Telegram repo customizations on this machine belong on `local/studio-customizations`.

Do not preserve important Telegram behavior primarily by:
- top-level `~/.hermes/patches/*.patch`
- `.new` restores for repo files
- stash-only state
- archived patch exports

If losing a Telegram feature after update would be a problem, it should be committed on `local/studio-customizations`.

## Current carried local behaviors to verify there

Examples of local Telegram behavior that should now be branch-canonical rather than patch-canonical:
- context badge / compact-context callback flow
- compact tool-progress behavior and related config
- Telegram rich final replies via Bot API 10.1 `sendRichMessage` are branch-canonical and always opportunistic: the adapter sends raw rich Markdown first so tables/task lists/details/formulas/media blocks render natively, then falls back to legacy MarkdownV2 only on permanent rich-parser/capability errors.
- Telegram native rich draft streaming via Bot API 10.1 `sendRichMessageDraft` / Bot API 9.5 `sendMessageDraft` is enabled with `streaming.transport: auto` and `draft_mode: true`; it falls back to edit streaming when the chat/platform can't draft.
- Telegram DM-topic outbound send routing had a live Bot API/client mismatch: `direct_messages_topic_id` returned OK but placed visible replies in `All`, while `message_thread_id` returned `is_topic_message: true` and landed in the topic tab. Normal Hermes replies now use `message_thread_id` for private-chat topics while still refusing to fall back unthreaded on topic rejection; fixed in `714118918`; see `references/telegram-dm-topic-send-routing-2026-05-08.md`. Older context: `references/dm-topic-direct-messages-topic-id-2026-05-08.md`.
- Telegram `/newthread` / DM-topic creation handling was tightened in `3b4a79e7b`: seed/welcome messages use DM-topic metadata, and `Bot_forum_create_forbidden` is surfaced as a BotFather private-chat topic permission issue instead of a misleading duplicate-name hint
- Telegram `/newthread` success must not return a second normal command response to the originating/current topic; that old-topic response can pull Telegram focus back and break the historical “land in the fresh session” feel. Send the success/welcome text inside the new topic and return `None`. Fixed in `180fac03e`; see `references/newthread-auto-focus-regression-2026-05-08.md`
- If Kosta says `/newthread` “didn’t start in a new thread,” do not trust the success text alone. Verify Hermes session binding, outbound Bot API topic kwargs for the welcome/first reply, and actual iOS/desktop placement. A created session can still be a UX regression if the visible message lands in the main DM/`All` or focus is pulled back. See `references/newthread-visible-thread-not-started-screenshot-2026-05-09.md`.
- Telegram DM-topic streaming/progress/status replies must preserve `chat_type=dm`, not just `thread_id`, so the adapter can classify the send as a private topic and avoid unsafe unthreaded fallbacks. If inbound session keys include the topic id but streamed replies land in the old chat, inspect `GatewayStreamConsumer` metadata setup first. Fixed in `6e4625aa6`; see `references/telegram-dm-topic-newthread-streaming-regression-2026-05-08.md`.
- Telegram DM-topic visible assistant replies can still leak into `All` even when `/newthread`, topic tabs, inbound user messages, and Hermes session keys all look correct. Do not treat `agent:main:telegram:dm:<chat>:<topic>` as proof of visible outbound placement; verify the actual initial stream/final/fallback `send_message` kwargs and live client placement. In the May 2026 GPT bot setup, live Bot API tests showed `message_thread_id=<topic>` produced `is_topic_message: true`, while `direct_messages_topic_id=<topic>` returned OK but visibly behaved like All. See `references/telegram-dm-topic-visible-reply-routing-2026-05-08.md` and `references/telegram-dm-topic-send-routing-2026-05-08.md`.
- After smart updates/merges, re-check that upstream did not restore `direct_messages_topic_id` or stale-reply logic that drops `message_thread_id`. A regression can show progress HUD/tool messages in the topic while the final answer disappears from that topic. Keep `_thread_kwargs_for_send()` and stale reply/media retries on `message_thread_id` for DM topics; see `references/telegram-dm-topic-post-update-regression-2026-05-09.md`.
- Telegram rich drafts/final sends are enabled on active profiles (`streaming.transport: auto`, `draft_mode: true`) now that Bot API 10.1 documents `sendRichMessageDraft` with `message_thread_id`. Keep the historical DM-topic caveat in mind when debugging visible placement: if drafts or finals leak into `All`, verify actual outbound Bot API kwargs and client placement before changing routing. Normal/final Hermes sends must keep using `message_thread_id` for visible DM-topic placement; see `references/telegram-dm-topic-draft-routing-2026-05-08.md` and `references/telegram-dm-topic-draft-rollback-2026-05-08.md` for the old failure mode.
- Incoming Telegram DM-topic messages may expose the topic id as `message.direct_messages_topic.topic_id` while `message.message_thread_id` is absent. Prefer the explicit DM topic object when building `MessageEvent.source.thread_id`; fixed in `aaddd6355`. See `references/telegram-dm-topic-draft-rollback-2026-05-08.md`.
- If DM-topic routing keeps leaking replies into `All` after the direct-message-topic fixes, stop treating private DM topics as the production path. Kosta's preferred direction is to migrate Hermes session UX to private/small Telegram supergroups with normal forum topics enabled: one group per active profile/bot, bot as admin, `/newthread` creates `createForumTopic`, and all replies use mature `message_thread_id` routing. See `references/telegram-dm-topics-abandonment-supergroup-forums-2026-05-08.md`. Avoid adding another narrow DM-topic fallback unless explicitly experimenting.
- gateway `/tts` support
- `/newthread` support where applicable
- profile-specific Telegram command menus via `TELEGRAM_MENU_COMMANDS`
- Telegram-specific helper tools committed inside the repo
- Busy-input policy: Kosta prefers `display.busy_input_mode: steer` across active Hermes profiles so normal Telegram messages during a run guide the active task instead of interrupting it; see `references/busy-steer-profile-default-2026-05-08.md`

## Update survival model for Telegram work

Normal flow:
1. commit Telegram repo changes on `local/studio-customizations`
2. update `main` from `origin/main`
3. merge `main` into `local/studio-customizations`
4. resolve conflicts in git
5. run focused Telegram verification

Do not assume a patch file or old stash is the real source of truth.

## Focused verification ideas

If compact emoji ×N progress, info/context buttons, or similar local HUD behavior vanish after an update, first suspect that the repo was switched off `local/studio-customizations`; see `references/compact-hud-regression-after-update-2026-05-07.md`. If branch/config/code are healthy, check for leaked background watch-pattern notifications or no-tool smoke turns before claiming the HUD is broken; see `references/telegram-gateway-visual-regression-triage-2026-05-08.md`.

If the dashboard Plugins page says `telegram-actions` is inactive, do not assume the tool is unavailable. Bundled `kind: backend` plugins can auto-load even when they are not listed in `plugins.enabled`; verify runtime with `PluginManager().discover_and_load()` and the focused `tests/tools/test_telegram_actions_tool.py` test. Session detail: `references/telegram-actions-plugin-runtime-status-2026-05-07.md`.

After Telegram changes or after an update, verify:
- callback payload handling still works
- final reply threading/topic behavior is intact; if messages leak into Telegram `All` instead of their topic/thread, do not trust session keys alone. First verify the actual outbound Bot API topic kwarg and live client placement; for private-chat topics, `message_thread_id` was the proven normal-send field in `references/telegram-dm-topic-send-routing-2026-05-08.md`. Then follow `references/telegram-topic-thread-routing-regression-2026-05-08.md`. If the symptom involves duplicates, disappearing topic replies, or progress/thinking UI in `All`, load `references/telegram-dm-topic-draft-rollback-2026-05-08.md` and first verify draft mode is still disabled for DM topics.
- any context badge or compact-progress symbols you expect are present
- profile-specific command menus still register when `TELEGRAM_MENU_COMMANDS` is set; see `references/profile-specific-telegram-command-menus-2026-05-06.md`
- targeted Telegram gateway tests still pass

## Narrow remaining patch use

A machine-local non-repo helper may still live outside the repo and be restored separately.
That is fine.

But repo files like `gateway/run.py`, `gateway/platforms/telegram.py`, `gateway/platforms/base.py`, tests, or Telegram tool files should not be maintained primarily through patch replay.

## If you find old replay artifacts

Treat them like migration residue.
Ask:
- does this represent real Telegram behavior we still care about?
- if yes, is it already committed on `local/studio-customizations`?
- if no, archive/retire it instead of keeping it live forever

If the answer is “it still matters and it is not on the branch yet,” promote it into the branch model before calling the setup stable.

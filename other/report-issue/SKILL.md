---
name: report-issue
disable-model-invocation: true
description: File an Apeiron bug report with the team, from the running editor
allowed-tools: Bash(ngine doctor:*), Bash(ngine where:*)
---

Report a problem with Apeiron to the Apeiron team. First gather, without changing anything: the
output of `ngine where` and `ngine doctor`, the `report` field of the `editor.version` op, the last
errors in `editor.context`, and the exact ops and arguments that led to the problem.

Draft a one-line title and a body (what I did, what I expected, what happened, plus what you
gathered). Then PREVIEW before anything leaves this machine: call `editor.report_issue {kind, title,
body, include_log:true, include_screenshot:true, include_crash:<true only if there was a crash>,
preview:true}`. A preview sends nothing. (If it refuses `include_screenshot` because there is no
window capture yet, preview again without it and tell me no screenshot is available.)

SHOW ME the `report` and the `attachments` list it returns, then ask about EACH attachment
separately, and wait for my answer to each:

1. May the editor log go with it? It can contain file paths and names from my project.
2. May a screenshot of the editor window go with it? It can show my project.
3. May the newest crash report go with it? (Ask only if there was a crash.)
4. May I send the report at all?

Only after I say yes to sending, call the same op WITHOUT `preview`, passing `include_log`,
`include_screenshot` and `include_crash` as `true` ONLY for what I agreed to and `false` for
everything else — always pass `include_log` explicitly, because the op attaches the log when it is
left out. A diagnostics block (build, platform, GPU, last op names — no project name) always goes
with a sent report; say so when you ask. It is filed under my Apeiron account (never on GitHub), and
the reply carries a `report_id` (or `pending`: then read `account.status`'s `last_report`).

Sending needs the Apeiron accounts service and a signed-in editor. If the op is refused because the
editor is not signed in, tell me to use Account > Sign in in the editor, then send again. If signing
in or sending fails because the accounts service cannot be reached, say plainly that sending needs
the Apeiron accounts service, which is not available right now, and instead give me the finished
title and body (with what you gathered) as one block of text I can copy and paste myself — attach
nothing. List separately anything you could NOT collect and why.

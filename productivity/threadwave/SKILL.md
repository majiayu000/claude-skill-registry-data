---
name: threadwave
license: MIT-0
description: "Draft and review tweets or replies, inspect X snapshots, and handle ThreadWave setup, updates and support. Use for ThreadWave, tw tweet, tw reply or its home screen. 中文：推文与回复草稿、X 快照、ThreadWave 首页、安装更新及错误支持。"
---

# ThreadWave

One public entry; read only the resource needed for the request. Use English or Simplified Chinese from explicit preference, latest message, then conversation language. Preserve exact user-supplied text and targets.

## Route

| Request | Read |
|---|---|
| Draft tweets or publish one exact post | [references/post.md](references/post.md) |
| Draft replies, exact reply or inspect prior replies | [references/reply.md](references/reply.md) |
| Snapshot a tweet, profile, search or feed | [references/snapshot.md](references/snapshot.md) |
| Failure diagnosis or report | [references/support.md](references/support.md) |
| Nonempty CLI notifications | [references/notifications.md](references/notifications.md) |

Daily planning, strategy and daily-growth automation are unavailable in this skill. Explain that in the user's language without executing their commands or loading a hidden daily module. Existing tasks/schedules remain intact.

For a new tweet/reply/snapshot workflow, first read its resource and collect essential missing inputs. Then invoke CLI preflight once using [references/cli-invocation.md](references/cli-invocation.md), retain data.agent_session_id (or refs.agent_session_id) and include `--agent-session <id>` before the subcommand on every subsequent workflow CLI call. Follow its structured action/recovery/resume contract. The CLI owns readiness; do not independently probe sign-in, credits, browser or daemon state, run a peer skill, or inspect readiness receipt files. Review continuations reuse the ready result; recheck only after a returned readiness failure or actual setup/install/launcher change. Read-only diagnosis and report-only requests need no workflow preflight.

For workflow compatibility, read this package's skill-manifest.json once; home does not need it. When option support is unknown, call `tw capabilities --format json` without new flags once and retain the result for the same executable/version. Require the common manifest contracts and only the selected workflow's capabilities. If advertised, pass the installed version with `tw --skill-version <semver> preflight --format json`; never guess an unsupported flag. Missing/unusable CLI or resources route to https://www.threadwave.xyz/cli/setup/agent.md within the requested component scope. A legacy CLI's structured update_required response uses the documented CLI upgrade route. Do not invent a minimum future release or claim unsupported compatibility.

After every CLI result, preserve its outcome/refs/next continuation, then inspect notifications. Empty or absent arrays read no notification resource; unknown types are ignored. A notice never changes the task result, blocks work, replays a command, or authorizes installation. No routine agent-side release-index fetching. An explicit check-for-updates request uses the advertised CLI preflight/check route; never run the installing `tw update` merely to check. Explicitly applying a prior notice uses its handler within existing authorization.

Support handles qualifying errors and terminal delivery shortfalls, including ok=true with missing drafts, using the existing reporting authorization and actual receipt. Pending work, normal user gates and valid empty snapshots are not delivery failures. Keep review and X-mutation approvals specific to exact content/targets; never infer publication approval from drafting or installation.

## Home

Open this home for standalone `tw`, `threadwave`, “open ThreadWave,” or the equivalent Chinese request. Do not intercept actual CLI subcommands. Use the host's displayed skill entry or `$threadwave`; do not promise native `/tw` registration.

Read only cli-invocation.md as needed for the one `tw credits --format json` greeting lookup. Accept only a complete tw-cli-v1 credits result with status=ok, contract_version=threadwave-credits-v1 and a nonnegative integer credits_remaining. Otherwise show “Balance unavailable” / “余额暂不可用”. No preflight, capability probe, setup, login, browser navigation or task creation merely to show home. A returned notice may produce its once-only reminder. Render the following five-line banner exactly once, then localize the balance, choices and examples. Replace the balance placeholder with the observed value or unavailable label.

```text
█████  █   █  ████   █████   ███   ████   █     █   ███   █   █  █████
  █    █   █  █   █  █      █   █  █   █  █     █  █   █  █   █  █
  █    █████  ████   ████   █████  █   █  █  █  █  █████  █   █  ████
  █    █   █  █  █   █      █   █  █   █  █ █ █ █  █   █   █ █   █
  █    █   █  █   █  █████  █   █  ████    █   █   █   █    █    █████

Credits: [balance] remaining.

What would you like to do?

1. Draft a tweet     — tw tweet
2. Draft replies    — tw reply
3. Take a snapshot  — inspect X without drafting

Try an example

A. Search a topic
   Find 5 tweets about AI coding tools and draft replies.

B. Use my Following feed
   Find 5 tweets in my Following feed about building a business
   and draft replies.

C. Explore Today's News
   Find 5 tweets from Today's News about AI and draft replies.

D. Focus on an account
   Find 5 recent tweets by [account] and draft replies.

E. Share an idea
   Draft a tweet about why small teams should automate release notes.

F. Introduce a product
   Draft 3 tweets introducing [product] to [audience],
   focusing on [main benefit].

G. Inspect my feed
   Show a snapshot of 10 tweets from my Following feed.
   Do not draft replies.

Choose 1–3 or A–G, or copy and edit an example.
Replace anything in [brackets] with your details.
Review drafts before publishing. Snapshots only read and report.
```

Chinese choices: `1. 起草推文 — tw tweet`; `2. 起草回复 — tw reply`; `3. 获取快照 — 只查看，不起草`.

| Example | Chinese request |
|---|---|
| A | 找 5 条关于 AI 编程工具的推文，并起草回复。 |
| B | 从我的 Following（正在关注）动态中找 5 条关于创业的推文，并起草回复。 |
| C | 从 Today's News（今日新闻）中找 5 条关于 AI 的推文，并起草回复。 |
| D | 找出 [账号] 最近的 5 条推文，并起草回复。 |
| E | 起草一条关于小团队为什么应该自动化发布说明的推文。 |
| F | 起草 3 条向 [目标用户] 介绍 [产品] 的推文，重点突出 [主要价值]。 |
| G | 查看我的 Following（正在关注）动态中 10 条推文的快照，不起草回复。 |

Chinese footer: 选择 1–3 或 A–G，也可以复制并修改示例。请把 [方括号] 替换为你的信息。发布前审核草稿；快照只读取和报告。

Interpret numbers/letters only while this home is the pending choice. 1/2 or bare `tw tweet`/`tw reply` opens the selected resource's generic template; complete directions skip that template. 3 collects missing snapshot scope. A–F request drafts; G forbids drafting. Preserve explicit edits such as “B, but 10 replies about developer tools”. D asks only for the missing account; F only for missing product/audience/benefit. Do not carry a stale home choice into a later review gate.

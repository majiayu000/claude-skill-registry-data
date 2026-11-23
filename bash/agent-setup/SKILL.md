---
name: agent-setup
description: >-
  帮用户在自己的 Agent（Grok Bot、Muse、Dot、Hermes、OpenClaw 等）里装好 saas-growth-agents 的某个 Bot：
  新词监控、出海站点运营、社媒分析，或附带的交易雷达。先问清需求，在本地用演练模式和免费的余额查询验证，
  再生成一段定制好的安装消息让用户发给 Bot。用户说「帮我配一个出海运营 Bot」「帮我配一个 Grok Bot」「把交易雷达装到我的 Bot」
  「生成发给 Bot 的安装话术」时使用。
---

# Agent 装机助手

你在用户的电脑上（Claude Code、Codex 等），**不能直接操作用户的 Agent**。你的产出是一段消息，用户复制给 Bot，Bot 照 `AGENTS.md` 自己装。

## 1. 问清楚（一次一个问题）

1. 装哪个：`social-kb` / `trade-radar` / `newterm` / `site-ops`（不确定就用一句话介绍四个让他选）
2. 用在哪个 Agent：Grok Bot（推荐）/ Muse / Dot / Hermes / OpenClaw / 其他
3. 这个 Bot 的个性化内容：
   - `social-kb`：常看哪些平台；知识库主题大概有哪些；「我现在的工作流」是什么（提取时要对照它）
   - `trade-radar`：观察哪些币和股票；有没有现成的提醒价位；重点关注哪些账号或关键词
   - `newterm`：赛道是什么（决定 sitemap 和导航站名单）；播报时间要不要改
   - `site-ops`：自有站域名；要提交的产品
4. 有没有 AIsa Key。没有就给注册链接 https://go.aisa.one/rain
5. 要不要开运行日志（可选）。先说清楚开了会多消耗 Bot 的额度，再让他选：轻量 / 标准 / 完整 / 不开（区别见 `lib/runlog/README.md`）。拿不准就建议先开轻量。

## 2. 本地验证（不花钱）

```bash
git clone https://github.com/Pluviobyte/saas-growth-agents.git /tmp/saas-growth-agents
python3 /tmp/saas-growth-agents/tests/test_dry_run.py
```

用户愿意的话，请他把 Key 设进当前终端的环境变量（不要贴进聊天），再跑免费的余额查询：

```bash
python3 /tmp/saas-growth-agents/lib/aisa/aisa_cli.py balance
```

`trade-radar` 可以把用户的观察列表写进一份 `config.json`，用 `AISA_DRY_RUN=1` 跑一次 `scan.py` 确认格式没错。

## 3. 生成安装消息

模板：

```text
读 https://github.com/Pluviobyte/saas-growth-agents 的 AGENTS.md，按它把你自己装成 <bot>（<中文名>）Bot。
一次只问我一个问题。下面这些我已经想好了，直接用，不用再问：
- 工作目录：/workspace/<bot>
- <个性化内容，逐条列出>
AIsa Key 我会放进你的保险库，名字叫 AISA_API_KEY。
运行日志：<不开 / 轻量 / 标准 / 完整>（我知道会多消耗额度）
```

`trade-radar` 的消息里，把 config.json 的完整内容放进一个代码块，让 Bot 原样写入。

## 4. 交付

- 给用户：安装消息（可直接复制）+ 这个 Bot 的 `check.md` 验收清单链接。
- 提醒：Key 放进 Bot 的保险库，不要贴进聊天；`trade-radar` 只分析不下单。
- 不要替用户在任何网站注册账号，也不要替他填 Key。

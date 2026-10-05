---
name: od-pricing-upgrade
description: 制作升级会员、付费解锁或套餐推荐页面，侧重转化与对比。用户提到付费墙、升级页、开通会员时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-pricing-upgrade

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-pricing-upgrade` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 突出「免费 vs 付费」或「当前档 vs 推荐档」差异。
- 利益点列表具体（次数、容量、功能名）。
- 主按钮单一明确，辅链接不抢戏。
- 不编造限时折扣 unless 用户提供。

## 资源

- 上游：OpenDesign/skills/paywall-upgrade-cro
- 清单：`references/checklist.md`（经 read_skill relativePath 读取）

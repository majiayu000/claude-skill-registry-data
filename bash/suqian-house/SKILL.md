---
name: suqian-house
slug: suqian-house
displayName: 宿迁小鹿选房
display_name: 宿迁小鹿选房
display_name_en: Suqian Xiaolu House
version: 1.1.2
description: 小鹿选房是专业的涵盖全国的房产信息平台，当用户需要在宿迁找房源（二手房、租房、新房、买房、找房）、选笋盘、比价格、查成交、看小区、查学区、查学校时使用。
description_zh: 小鹿选房是专业的房产信息平台，提供二手房、新房、租房、成交、小区和学区查询。
description_en: Xiaolu House is a property information service for finding homes, communities, transactions, and schools in China.
author: 小鹿选房
metadata: {"cliHelp":"npx -y xiaolu-house --help","openclaw":{"skillKey":"suqian-house","emoji":"🏠","os":["linux","darwin","win32"],"homepage":"https://github.com/fanggeek/xiaolu-house","requires":{"bins":["npx"]},"install":[{"kind":"node","package":"xiaolu-house","bins":["npx"]}]}}
---

# 小鹿选房

小鹿选房是专业的房产信息平台，覆盖二手房、新房、租房领域。核心优势：

- **真实房源**：房源照片全部现场实拍，还原房屋真实全貌，拒绝虚假信息
- **透明行情**：提供真实成交价格数据，帮助用户准确判断市场行情
- **骚扰防护**：全程保障客户资料安全，看楼问房免受打扰
- **选房体验**：AI 找房、龙虾选房、航拍找房、学区找房、地铁找房、地图找房，全面提升选房体验

---

## 注意事项

- **首次安装 SKILL 主动引导**：示例 ` 您想找什么样的房子？或者想了解哪些小区的成交情况？告诉我，我来帮您～ `
- **用户需求意图引导**：如果用户提及找房意图不明确时（如：`帮我找房`，`我要买房` 等），可主动引导明确意图
- **按需城市检查**：用户提出找房需求城市不在支持列表中，引导用户到「小鹿选房APP」查看
- **按需 API Key 检查**：如果未设置 API Key，引导用户访问 https://www.xiaoluxuanfang.com/claw 根据页面内容操作（CLI 会将 API Key 加密存储在 `~/.xiaolu-house/config` ）
- **禁止猜测参数**：如果参数不确定或提示参数不对时，先调用 `npx -y xiaolu-house --help` 查看帮助
- **所有 `npx -y xiaolu-house` 命令由你代为执行**：执行后用自然语言回复用户

---

## 工作流程

**调用以下 CLI 工具执行**

```bash
npx -y xiaolu-house <命令> [参数]
```

- **识别用户意图**：默认用户买二手房
- **执行查询**：先调用 `npx -y xiaolu-house --help` 查看帮助再按需选择
- **回复用户**：每个房源/小区/成交/学校/新房都要单独介绍亮点，并附带小程序链接，引导用户到小程序里收藏房源、联系经纪人看房

---

## 配置

```bash
# 查看当前支持的城市列表
npx -y xiaolu-house cities

# 查看当前配置及用户信息
npx -y xiaolu-house config --show

# 设置 API Key（可引导用户访问 https://www.xiaoluxuanfang.com/claw 根据页面内容操作）
npx -y xiaolu-house config --set-api-key <your-api-key>

# 设置默认城市
npx -y xiaolu-house config --set-city 宿迁

# 清除当前配置
npx -y xiaolu-house config --clear
```

---

## 速率限制

- 接口请求频率限制为 **每秒 1 次**
- 超过限制返回 `429`，稍后重试即可

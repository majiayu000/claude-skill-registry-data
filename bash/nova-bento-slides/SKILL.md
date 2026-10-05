---
name: nova-bento-slides
description: >-
  Nova default editable presentation skill — generates self-contained deck.bento.html
  (bento/slides) with morph, charts, tables, speaker notes, and ambient motion. Use when
  the user asks for PPT, slides, keynote, deck, presentation, 幻灯片, 演示稿, 可编辑, morph,
  or Bento — unless they explicitly want native Office .pptx, Reveal/HTML slideshow
  (html-ppt), or aesthetic PNG slides (nova-ppt-aesthetic-slides). Negative triggers — pptx,
  Office editable shapes, 交 Office, Reveal, 网页放映, 美学 PNG, 国风 KV.
---

<!-- NOVA-EXEC-BEGIN -->
## Nova Ai-Studio 集成（最高优先级）

- **终态唯一成果**：`<task-artifact-dir>/deck.bento.html`（禁止并列 index.html / pptx 充数）
- **过程文件**（非成果区）：`bento-spec.md`、`outline.json`
- **禁止** ask_user_question 挡 write_file；缺信息用合理默认
- **禁止**手改 560KB Bento 壳 — 只用 `scripts/splice-bento-shell.mjs`
- **validate 门禁**：`node skills/nova-bento-slides/scripts/validate-bento-doc.mjs --strict <out>` 非 0 不得 write_file 终态
- **所见所得 WYSIWYG**：theme 配色 + 字体层级 + image/assets + layouts 配方；右栏预览与交付一致；禁止静态 HTML / 有损转换
- Office .pptx → ppt-master / anth-pptx；Reveal HTML → html-ppt；美学 PNG → nova-ppt-aesthetic-slides

### 串行管线（不得跳步）

1. **Phase B** Strategist-lite → 三项快确认（页数/观众、theme preset、是否要逐字稿）
2. **Phase C** 写 `bento-spec.md`（锁定 theme / accent / morph id 策略）
3. **Phase D** 写 `outline.json`（页型节奏 anchor/dense/breathing）
4. **Phase E** 逐页手写 `slides[i].elements`（禁止批量脚本替创意）
5. **Phase F** 组装 doc JSON + morph 链（共享 id + `transition:"morph"`）
6. **Phase G** `splice-bento-shell.mjs` → `deck.bento.html`
7. **Phase H** validate --strict → 交付

续跑见 [workflows/resume-bento.md](workflows/resume-bento.md)
<!-- NOVA-EXEC-END -->

# nova-bento-slides — 可编辑 Bento 演示稿

默认 PPT 路径：直接生成 `bento/slides` JSON 并 splice 为 `deck.bento.html`，用户在 Nova 右栏 Bento 编辑器一点即改。

## 快速开始

```bash
node skills/nova-bento-slides/scripts/splice-bento-shell.mjs \
  --shell ui/public/vendor/bento/Bento_Slides.bento.html \
  --doc skills/nova-bento-slides/templates/bento-doc-skeleton.json \
  --out artifacts/task-YYYYMMDD-xxxx/deck.bento.html

node skills/nova-bento-slides/scripts/validate-bento-doc.mjs --strict artifacts/task-YYYYMMDD-xxxx/deck.bento.html
```

## 参考

- [references/agents-guide.zh-CN.md](references/agents-guide.zh-CN.md) — Bento 格式 + Nova 硬规则
- [references/strategist-lite.md](references/strategist-lite.md) — 三项确认
- [references/themes.md](references/themes.md) — 16 theme presets
- [references/layouts.md](references/layouts.md) — 12 页型配方
- [references/morph-recipes.md](references/morph-recipes.md) — 跨页 morph
- [references/id-registry.md](references/id-registry.md) — 稳定 element id
- [references/quality-gates.md](references/quality-gates.md) — Blocker 清单

## 完整示例 deck

- [templates/full-decks/pitch-launch.json](templates/full-decks/pitch-launch.json)
- [templates/full-decks/tech-sharing.json](templates/full-decks/tech-sharing.json)
- [templates/full-decks/data-report.json](templates/full-decks/data-report.json)

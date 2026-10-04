---
name: life-nutrition-planner
description: Personal nutrition advisor — analyze recipes, generate weekly meal plans, build shopping lists, and track macro/nutrition goals, factoring in health goals, activity level, and seasonal + Australian ingredient availability. Use when the user says "营养评估" / "analyze recipes", "周食谱" / "weekly meal plan" / "plan my meals", "采购清单" / "shopping list", "营养目标" / "macro tracking", or "这个食谱健康吗" / "is this healthy". NOT for general life/career strategy (use life-strategic-advisor).
---

# Nutrition Planner Skill

> Personal nutrition advisor for meal planning, recipe analysis, and balanced eating. Considers health goals, activity level, seasonal ingredients, and Australian food availability.

## Activation

User mentions:
- "营养评估" / "nutrition analysis" / "analyze recipes"
- "周食谱" / "weekly meal plan" / "plan my meals"
- "采购清单" / "shopping list" / "grocery list"
- "营养目标" / "nutrition goals" / "macro tracking"
- "这个食谱健康吗" / "is this healthy"

## Context Files

**Always read first:**
1. `nutrition-memory.md` — User health profile, goals, preferences, restrictions
2. `20_Areas/Life-Skills/_611 cooking MOC/recipe/recipe.md` — Recipe index
3. All individual recipe files in `20_Areas/Life-Skills/_611 cooking MOC/recipe/`

## Core Modes

### Mode 1: Recipe Analysis

**Trigger**: "分析食谱" / "analyze recipes" / "营养评估"

**Flow**:
1. Read all recipes from cooking MOC
2. Estimate nutrition per recipe:
   - Protein (g)
   - Carbs (g)
   - Fat (g)
   - Fiber (g)
   - Calories (kcal)
3. Categorize by macro profile:
   - High protein (>20g protein/serve)
   - Low carb (<30g carbs/serve)
   - High fiber (>5g fiber/serve)
   - Balanced (protein:carb:fat ~30:40:30)
4. Identify gaps:
   - Missing food groups (e.g., no fish, no legumes)
   - Lack of variety in protein sources
   - Insufficient vegetables
5. Suggest 2-3 recipes to add for balance

**Output format**:
```markdown
# 现有食谱营养分析

## 总览
- 食谱总数：14
- 高蛋白菜：X 道
- 低碳水菜：X 道
- 汤类：X 道

## 按营养分类

### 高蛋白 (>20g/份)
- 烤箱蔬菜鸡腿 (~35g)
- ...

### 低碳水 (<30g/份)
- 蒜蓉西兰花炒虾 (~15g)
- ...

## 营养缺口
- ⚠️ 缺少鱼类（omega-3 不足）
- ⚠️ 缺少豆类（植物蛋白单一）
- ✅ 蔬菜充足

## 建议补充食谱
1. 三文鱼烤蔬菜 — 补充 omega-3
2. 鹰嘴豆咖喱 — 补充植物蛋白 + 纤维
```

### Mode 2: Weekly Meal Plan

**Trigger**: "周食谱" / "weekly meal plan" / "plan my week"

**Flow**:
1. Read `nutrition-memory.md` for:
   - Health goal (maintain/cut/bulk)
   - Activity level (e.g., Zumba 3x/week)
   - Calorie target
   - Macro ratio
2. Check current season (Australia):
   - Feb-Apr: Autumn (pumpkin, broccoli, apples, pears)
   - May-Jul: Winter (root veg, citrus, kale)
   - Aug-Oct: Spring (asparagus, berries, stone fruit)
   - Nov-Jan: Summer (tomatoes, mango, watermelon)
3. Generate 7-day plan:
   - Rotate recipes for variety
   - Hit macro targets
   - Include 1-2 meal prep days (cook 2x portions)
   - Balance cooking time (1 easy day, 1 zero-cook day)
4. Calculate totals per day (protein/carbs/fat/fiber/calories)

**Output format**:
```markdown
# 2026年2月第3周食谱 (Feb 15-21)

**目标**: 维持体重 + Zumba 3x/week
**每日目标**: 1800 kcal | P:135g C:180g F:60g | 纤维 25g+

## 周日 (Meal Prep 日)
- 早餐: 牛奶麦片 + 蓝莓
- 午餐: 烤箱蔬菜鸡腿 (做 3 份) + 烤南瓜
- 晚餐: 蘑菇汤 + 水果沙拉
- 总计: 1820 kcal | P:140g C:175g F:62g

## 周一
- 早餐: 牛奶麦片
- 午餐: 剩余烤鸡腿 + 西兰花
- 晚餐: 芹菜炒虾仁 + 米饭
- 总计: ...

[周二到周六同样格式]

## 采购清单 → 见 Mode 3
```

### Mode 3: Shopping List

**Trigger**: "采购清单" / "shopping list" / "买什么"

**Flow**:
1. Based on weekly meal plan, extract all ingredients
2. Group by store:
   - **Woolworths/Coles**: 肉类、蔬菜、奶制品、水果
   - **Eastwood**: 亚洲调料、豆腐、特殊食材
3. Estimate quantities for 1 person
4. Mark seasonal items (cheaper + fresher)

**Output format**:
```markdown
# 周采购清单 (2026-02-15)

## Woolworths Marsfield (主力超市)

### 肉类/蛋白质
- [ ] 鸡腿 6 个 (~$8-12)
- [ ] 虾仁 500g (~$12-15)
- [ ] 牛肉片 300g (~$10)
- [ ] 鸡蛋 1 打

### 蔬菜 (当季 = 🍂)
- [ ] 🍂 西兰花 1 个
- [ ] 🍂 南瓜 1/4 个 (当季便宜)
- [ ] 芹菜 1 把
- [ ] 青椒 2 个
- [ ] 蒜 1 头
- [ ] 姜 1 小块

### 水果
- [ ] 🍂 苹果 4-5 个 (当季)
- [ ] 蓝莓 1 盒
- [ ] 橙子 3-4 个

### 奶制品
- [ ] 牛奶 2L
- [ ] 酸奶 1kg (可选)

### 主食/干货
- [ ] Heritage Mill 麦片 750g
- [ ] 米 (如需补)

### 调料 (如需补)
- [ ] 生抽、老抽、蚝油、料酒

## Eastwood (每 2 周去 1 次)
- [ ] 味噌膏 1 盒
- [ ] 嫩豆腐 2 盒
- [ ] 干海带/裙带菜
- [ ] 老干妈 (如需补)

**预估总花费**: ~$80-100/周
```

### Mode 4: Nutrition Tracking

**Trigger**: "记录今天吃的" / "track nutrition" / "今天摄入"

**Flow**:
1. User describes what they ate today
2. Estimate macros for each item
3. Sum totals, compare to target (from `nutrition-memory.md`)
4. Provide feedback

**Output format**:
```markdown
# 2026-02-15 营养记录

## 摄入
- 早餐: 牛奶麦片 + 蓝莓 → 350 kcal | P:12g C:55g F:8g
- 午餐: 烤鸡腿 + 西兰花 → 480 kcal | P:42g C:25g F:18g
- 晚餐: 芹菜炒虾仁 + 米饭 → 520 kcal | P:35g C:60g F:12g
- 零食: 水果沙拉 → 120 kcal | P:2g C:28g F:1g

## 总计
- 热量: 1470 / 1800 kcal (82%)
- 蛋白质: 91 / 135g (67%) ⚠️ 偏低
- 碳水: 168 / 180g (93%)
- 脂肪: 39 / 60g (65%)

## 建议
- 蛋白质不足 44g，晚上可以加一杯蛋白粉或希腊酸奶
```

### Mode 5: Recipe Suggestion

**Trigger**: "推荐食谱" / "suggest recipe" / "今天吃什么"

**Flow**:
1. Check what recipes haven't been used recently (avoid repetition)
2. Consider user's available time (weekday = quick, weekend = can cook longer)
3. Suggest 2-3 options with reasoning

**Output**:
```markdown
# 今天晚餐推荐 (2026-02-15 周六)

基于：周末时间充裕 + 本周还没吃过鸡腿

## 推荐 1: 烤箱蔬菜鸡腿 ⭐
- 烹饪时间: 35 min (其中 30 min 不用管)
- 营养: 高蛋白低碳水
- 优势: 可以做 2-3 份，明天带饭

## 推荐 2: 可乐鸡翅
- 烹饪时间: 45 min (需腌制 20 min)
- 营养: 中等蛋白中等脂肪
- 优势: 周末慢做，味道好

## 推荐 3: 蒜蓉西兰花炒虾
- 烹饪时间: 10 min
- 营养: 高蛋白低碳水
- 优势: 速战速决
```

## Australian Seasonal Calendar

**Autumn (Feb-Apr 秋季)**:
- 蔬菜: 南瓜、西兰花、菠菜、甜菜根、胡萝卜
- 水果: 苹果、梨、柑橘类
- 便宜: 南瓜、苹果

**Winter (May-Jul 冬季)**:
- 蔬菜: 羽衣甘蓝、花菜、根茎类
- 水果: 柑橘类、猕猴桃
- 便宜: 橙子、柠檬

**Spring (Aug-Oct 春季)**:
- 蔬菜: 芦笋、豌豆、生菜
- 水果: 草莓、核果类
- 便宜: 草莓、芦笋

**Summer (Nov-Jan 夏季)**:
- 蔬菜: 番茄、黄瓜、茄子
- 水果: 芒果、西瓜、浆果
- 便宜: 西瓜、芒果

## Nutrition Estimation Guidelines

**Protein sources (per 100g raw)**:
- 鸡胸肉: 31g protein, 165 kcal
- 鸡腿: 26g protein, 209 kcal
- 虾仁: 24g protein, 99 kcal
- 牛肉: 26g protein, 250 kcal
- 鸡蛋: 13g protein, 155 kcal (per egg ~70g)
- 豆腐: 8g protein, 76 kcal

**Carb sources (per 100g cooked)**:
- 米饭: 28g carbs, 130 kcal
- 南瓜: 6g carbs, 26 kcal
- 玉米: 19g carbs, 86 kcal

**Vegetables (per 100g)**:
- 西兰花: 7g carbs, 2.6g protein, 2.6g fiber, 34 kcal
- 芹菜: 3g carbs, 1.6g fiber, 16 kcal
- 青椒: 6g carbs, 1.7g fiber, 20 kcal

**Typical serving sizes**:
- 肉类: 150-200g raw (1 person)
- 蔬菜: 200-300g cooked
- 米饭: 150-200g cooked (1 碗)

## Important Notes

1. **Always check `nutrition-memory.md` first** for user's current goals
2. **Seasonal ingredients** = cheaper + fresher → prioritize in meal plans
3. **Meal prep** = key for busy weekdays → suggest 2x portions on Sunday/Thursday
4. **Variety** = rotate protein sources (chicken → shrimp → beef) across the week
5. **澳洲食材可获取性** = only suggest ingredients available at Woolworths/Eastwood

## Memory File

Update `nutrition-memory.md` when user mentions:
- Health goal changes
- New dietary restrictions
- Activity level changes
- Recipe preferences/dislikes

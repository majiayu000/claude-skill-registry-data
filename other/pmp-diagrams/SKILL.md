---
name: pmp-diagrams
description: Проектные диаграммы PMP/PMBOK в нативном XML draw.io / diagrams.net — WBS (иерархия работ), Project Network PERT/CPM (AON-ноды, critical path), Gantt (таймлайн, вехи, зависимости), RACI-матрица, Risk Matrix 5×5 (probability-impact), Stakeholder power-interest grid, плюс resource histogram, communication plan, process groups и knowledge areas. Готовые style-сниппеты и уровни/цвета. Use при построении проектных/PM-диаграмм в draw.io.
version: 1.0.0
---

# Навык: PMP/PMBOK диаграммы (draw.io)

Строит проектные диаграммы по методологии PMBOK в нативном XML draw.io. Опирается на скилл `drawio-diagrams` (структура `mxfile`/`mxCell`/`mxGeometry`, стили `key=value;`, рёбра, палитра, правила качества) — здесь только специфика PM-диаграмм: раскладка, уровни, цвета и style-сниппеты. Отдаёшь валидный `.drawio` файл.

## 1. WBS — Work Breakdown Structure
Иерархическая декомпозиция как дерево прямоугольников, ортогональные рёбра сверху-вниз. Уровни (размер/цвет усиливают иерархию):
- **Уровень 0 (Проект):** 200×80, bold, тёмно-синий — `rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontColor=#ffffff;fontStyle=1;fontSize=14;`
- **Уровень 1 (Deliverables):** 160×60, зелёный — `rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;fontColor=#ffffff;fontStyle=1;`
- **Уровень 2 (Sub-deliverables):** 140×50, светло-зелёный — `fillColor=#d5e8d4;strokeColor=#82b366;`
- **Уровень 3 (Work Packages):** 120×40, самый светлый.

Нумеруй пакеты по WBS-коду (`1`, `1.1`, `1.1.2`). Рёбра — `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=none;` (дерево, без стрелок).

## 2. Project Network — PERT / CPM (AON)
Activity-on-Node: узел-активность разбит на секции ES/Duration и LS/LF вокруг названия:
```
┌───────────────┐
│ ES │  Dur │   │
├───────────────┤
│  Activity      │
├───────────────┤
│ LS │  LF      │
└───────────────┘
```
- **Нода активности:** `shape=rectangle;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;` (секции — вложенными ячейками или таблицей).
- **Critical path (подсветка):** `fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=3;` + рёбра критического пути `strokeColor=#b85450;strokeWidth=3;`.
- Зависимости — ортогональные рёбра `endArrow=block;` слева-направо по последовательности.

## 3. Gantt Chart
Таймлайн-полосы по строкам-задачам вдоль оси времени:
- **Полоса задачи:** `rounded=0;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;fontColor=#ffffff;` (длина/позиция по X = сроки).
- **Веха (milestone, ромб):** `rhombus;whiteSpace=wrap;html=1;fillColor=#fa6800;strokeColor=#C73500;`
- **Зависимость:** `edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;strokeWidth=2;`
- Слева — колонка названий задач; сверху — шкала времени (недели/месяцы) как ряд ячеек.

## 4. RACI-матрица
Таблица роли × задачи (swimlane-контейнер или сетка ячеек). Легенда цветов:
- **R (Responsible):** `fillColor=#d5e8d4;strokeColor=#82b366;` (зелёный)
- **A (Accountable):** `fillColor=#dae8fc;strokeColor=#6c8ebf;` (синий)
- **C (Consulted):** `fillColor=#fff2cc;strokeColor=#d6b656;` (жёлтый)
- **I (Informed):** `fillColor=#e1d5e7;strokeColor=#9673a6;` (фиолетовый)

Заголовки — bold (`fontStyle=1`); каждая задача-строка имеет ровно один `A`. Контейнер: `swimlane;html=1;startSize=40;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;`.

## 5. Risk Matrix (Probability-Impact 5×5)
Сетка 5×5: ось X — Impact (Very Low…Very High), ось Y — Probability. Цвет ячейки = уровень риска:
- **Low:** `fillColor=#d5e8d4;strokeColor=#82b366;` (зелёный)
- **Medium:** `fillColor=#fff2cc;strokeColor=#d6b656;` (жёлтый)
- **High:** `fillColor=#ffe6cc;strokeColor=#d79b00;` (оранжевый)
- **Critical:** `fillColor=#f8cecc;strokeColor=#b85450;` (красный)

Классически: правый-верхний угол (высокая вероятность × высокое влияние) — критичный; левый-нижний — низкий. Риски размещай как метки в соответствующих ячейках.

## 6. Stakeholder Power-Interest Grid
Квадрант 2×2 (ось X — Interest, ось Y — Power):
```
High Power │ Keep Satisfied │ Manage Closely
           ├────────────────┼───────────────
 Low Power │ Monitor        │ Keep Informed
           └────────────────┴───────────────
             Low Interest      High Interest
```
Квадранты — прямоугольники разного оттенка; стейкхолдеры — узлы/метки внутри. Заголовки квадрантов bold.

## 7. Кратко: прочие PMBOK-диаграммы
- **Resource histogram:** столбцы (bar) по периодам, высота = загрузка ресурса; линия capacity сверху.
- **Communication plan:** узлы-стейкхолдеры + рёбра (частота/канал в `value`).
- **Process Groups:** 5 блоков — Initiating → Planning → Executing → Monitoring & Controlling → Closing (M&C охватывает остальные).
- **Knowledge Areas:** карта 10 областей (Integration, Scope, Schedule, Cost, Quality, Resource, Communications, Risk, Procurement, Stakeholder) как mind map/таблица.

## Правила
- Соблюдай семантику метода: у RACI один `A` на задачу; critical path — непрерывная цепочка с нулевым запасом; WBS — 100% охват без дублей.
- Цвета — по легендам выше (роль → цвет постоянно), выравнивание по сетке, ортогональные рёбра, валидный XML (см. `drawio-diagrams`).
- Всегда добавляй **легенду** (цвет → значение) на диаграмму: RACI, риски, critical path — без легенды нечитаемы.

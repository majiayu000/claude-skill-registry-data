---
name: drawio-diagrams
description: Создание диаграмм в нативном XML-формате draw.io / diagrams.net — структура файла (`mxfile`/`mxGraphModel`/`mxCell`/`mxGeometry`), ID-менеджмент, стили (`key=value;`), каталог фигур и рёбер, типы диаграмм (flowchart, cross-functional/swimlane, BPMN, UML, network/cloud, ERD, org chart, mind map), подключение custom-библиотек (`?clibs=`), правила качества и валидность XML. Use при создании, конвертации или правке диаграмм draw.io/diagrams.net.
version: 1.0.0
---

# Навык: Draw.io / diagrams.net диаграммы

Цель — по описанию/исходнику выдать **валидный, аккуратный `.drawio` XML**, который пользователь откроет в diagrams.net и получит читаемую диаграмму. Среда не рендерит draw.io — поэтому отдаёшь **готовый файл** и подсказываешь, какие custom-библиотеки включить. Проектные диаграммы (WBS, RACI, Gantt, риски, стейкхолдеры) — в скилле `pmp-diagrams`.

**Навигатор.** База: [формат файла](#1-формат-файла) (скелет XML) → [ячейки, id, геометрия](#2-ключевые-концепты) → [стилизация и палитра](#3-стилизация) → [рёбра](#5-рёбра-связи). Перед сдачей: [правила качества](#8-правила-качества) и [антипаттерны](#антипаттерны). Справочники: [каталог фигур](#4-каталог-фигур) · [типы диаграмм](#6-типы-диаграмм) (flowchart/swimlane/BPMN/UML/ERD/…) · [custom-библиотеки `?clibs`](#7-custom-библиотеки).

## 1. Формат файла
Draw.io — XML (`.drawio` или `.xml`). Иерархия: `mxfile > diagram > mxGraphModel > root > mxCell`. Минимальный скелет:
```xml
<mxfile host="app.diagrams.net" agent="Claude">
  <diagram id="page-1" name="Page-1">
    <mxGraphModel dx="1434" dy="759" grid="1" gridSize="10" guides="1" tooltips="1"
                  connect="1" arrows="1" fold="1" page="1" pageScale="1"
                  pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- фигуры и рёбра здесь, parent="1" -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```
Несколько страниц — несколько `<diagram>` внутри `<mxfile>`.

## 2. Ключевые концепты
- **Ячейка (`mxCell`)** — всё есть ячейка: фигура (`vertex="1"`), связь (`edge="1"`), контейнер, корни. У фигур/рёбер `parent="1"` (или id контейнера/swimlane).
- **ID-менеджмент:** `id` уникален в пределах файла. **`0` и `1` зарезервированы** для корней — свои элементы нумеруй с `2` (или осмысленные строковые id: `node-login`, `db-users`). В рёбрах ссылайся на те же id через `source`/`target`.
- **Геометрия (`mxGeometry`):** у фигур `x`/`y` (левый-верхний угол), `width`/`height`; у рёбер — `relative="1"` (позиция вычисляется). Пример: `<mxGeometry x="120" y="80" width="120" height="60" as="geometry"/>`.

## 3. Стилизация
Стиль — строка `key=value;`, разделённая `;`:
- **Тип фигуры:** `rounded=1`, `ellipse`, `rhombus`, `shape=parallelogram`, `shape=document`, `swimlane`…
- **Цвета:** `fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#000000;` (используй согласованную палитру draw.io — синий/зелёный/оранжевый/жёлтый/фиолетовый/красный/серый).
- **Текст/выравнивание:** `fontSize=12;fontStyle=1` (1=bold, 2=italic, 4=underline), `align=center;verticalAlign=middle;whiteSpace=wrap;html=1;`, отступы `spacingLeft=10`.

**Палитра draw.io (fill / stroke):** синий `#dae8fc`/`#6c8ebf` · зелёный `#d5e8d4`/`#82b366` · оранжевый `#ffe6cc`/`#d79b00` · жёлтый `#fff2cc`/`#d6b656` · фиолетовый `#e1d5e7`/`#9673a6` · красный `#f8cecc`/`#b85450` · серый `#f5f5f5`/`#666666`.

## 4. Каталог фигур
- **Process (прямоугольник):** `rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;`
- **Decision (ромб):** `rhombus;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;`
- **Start/End (эллипс/terminator):** `ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;`
- **Document:** `shape=document;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;`
- **Data (параллелограмм):** `shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;`
- **Swimlane (гориз.):** `swimlane;html=1;startSize=20;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;childLayout=stackLayout;horizontal=1;horizontalStack=0;resizeParent=1;collapsible=0;`
- **Swimlane (верт.):** та же строка + `horizontal=0;`.

## 5. Рёбра (связи)
```xml
<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;
  exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
  edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```
- **Всегда** задавай `source` и `target` реальными id (без «висящих» рёбер).
- `edgeStyle=orthogonalEdgeStyle` — прямые углы (читаемее ломаных); стрелка — `endArrow=block;endFill=1;` (или `none`/`open`/`diamond`).
- `exitX/exitY` + `entryX/entryY` (0..1) фиксируют точки выхода/входа — так линии не «прилипают» криво.
- Подпись ребра — атрибут `value="..."` на самом ребре.

## 6. Типы диаграмм
- **Flowchart:** start/end (эллипс) → process (прямоугольник) → decision (ромб, ветки `value="Да"/"Нет"`).
- **Cross-functional (swimlane):** дорожки-роли/отделы как контейнеры-`swimlane`, шаги — дочерние `mxCell` с `parent=<id дорожки>`.
- **BPMN:** события (круги), задачи (скруглённые прямоугольники), гейтвеи (ромбы); стили `shape=mxgraph.bpmn.*` (включи BPMN-библиотеку).
- **UML:** class (`shape=...`/составной прямоугольник с секциями), sequence (жизненные линии + сообщения-рёбра), use case (эллипсы-акторы). Стили `shape=umlActor`, `umlLifeline`, `mxgraph.uml.*`.
- **Network / cloud:** узлы через `shape=mxgraph.aws4.*` / `azure` / `gcp` / `kubernetes` (включи соответствующую библиотеку); Cisco/Arista — свои shape-наборы.
- **ERD:** таблицы-`swimlane` с полями-строками (`PK`/`FK` — bold), связи-рёбра с кардинальностью (`startArrow`/`endArrow` = `ERone`/`ERmany`).
- **Org chart:** прямоугольники по уровням, ортогональные рёбра сверху-вниз (дерево).
- **Mind map:** центральный узел + радиальные ветви, скруглённые узлы, рёбра без стрелок.

## 7. Custom-библиотеки
Для BPMN/UML/облаков/сетей укажи пользователю, что открыть файл с включёнными библиотеками:
```
https://app.diagrams.net/?clibs=Uhttps://jgraph.github.io/drawio-libs/libs/templates.xml
```
Или в diagrams.net: **More Shapes…** → включить нужный набор (AWS/Azure/GCP/Kubernetes/BPMN/UML/Networking). Всегда перечисляй, какие наборы нужны для твоей диаграммы.

## 8. Правила качества
- **Валидный well-formed XML** — экранируй `&`→`&amp;`, `<`→`&lt;`, `"`→`&quot;` в `value`; закрывай все теги. Проверяй `xmllint --noout file.drawio`.
- **Уникальные id**, `0`/`1` не переопределяй; у каждого ребра — валидные `source`/`target`.
- **Выравнивание по сетке** (`gridSize=10`): координаты кратны 10; не допускай наложений фигур.
- **Единый layout:** одно направление потока (сверху-вниз или слева-направо), равные отступы между уровнями, ортогональные рёбра.
- **Семантические цвета** из палитры (§3), одинаковая роль → одинаковый цвет; текст читаем (контраст, `whiteSpace=wrap`).

## Антипаттерны
Рёбра без `source`/`target`; дубли id или переопределение `0`/`1`; неэкранированные `&`/`<` в подписях; «магические» цвета вразнобой; фигуры внахлёст и не по сетке; диагональные пересекающиеся линии вместо ортогональных; забытое перечисление нужных `?clibs`.

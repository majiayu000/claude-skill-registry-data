---
name: print-forms
description: >-
  Печатные бланки и формы FST/Otgruzka: автоподгонка размера страницы, разметка
  A4, корректная печать/PDF без обрезания и лишних пустых листов. Use when
  working on blanks, forms, print preview, PDF export, @page, print.css,
  printFit, html2canvas, табель/ЗП/склад/погрузка печать, «бланк», «форма для
  печати», overflow на лист, fit-to-page.
---

# Печатные бланки (print-forms)

Источник лучших практик с GitHub (установлены рядом):

| Скил / реф | Откуда | Зачем |
|------------|--------|--------|
| `html-to-pdf` | [aviz85/claude-skills-library](https://github.com/aviz85/claude-skills-library) | Auto-fit overflow, `@page` A4, проверка числа страниц, Puppeteer |
| `html-to-pdf/references/pagination.md` | Quant-Nanggroe typesetting | Анти-orphan last page, таблицы, break-inside, fill ≥40% |

**В приложении не переписываем печать на Puppeteer.** Канон Otgruzka — React-бланки + `print.css` + `fitPrintPages` + (при PDF) `pdfExport` / html2canvas. Правила auto-fit и пагинации применять к этому стеку.

## Когда читать этот скил

- Новый или правка бланка / печатной формы / превью печати
- Обрезка текста, лишняя 2-я страница, пустой низ, мелкие бордеры в PDF
- «Подогнать под лист», landscape/portrait A4

## Канон в коде FST

| Что | Где |
|-----|-----|
| Print CSS / `@page` | `src/styles/print.css` |
| Автомасштаб страниц | `src/lib/printFit.ts` → `fitPrintPages` / `resetPrintFit` |
| Превью | `PrintPreviewModal`, `ProductionPrintPreview`, … |
| PDF из DOM | `src/lib/pdfExport.ts` (html2canvas + jsPDF) |
| Оболочка листа | `.print-sheet-page` + `.print-sheet-content` |

После layout-изменений в превью вызывать `fitPrintPages(container)` (после paint / `requestAnimationFrame`). Сброс — `resetPrintFit`.

Опции `fitPrintPages`:

- `portrait: true` — книжная A4
- `shrinkOnly: true` — только уменьшать (не раздувать до 92% fill)

## Жёсткие правила бланка

1. **Размер страницы явный** — `.print-sheet-page` = A4 (альбом 297×210 или портрет 210×297 мм), `box-sizing: border-box`, поля внутри листа.
2. **Фон не на `html`/`body`** — иначе лишняя страница (правило html-to-pdf). Фон на контейнере листа.
3. **Бордеры для PDF ≥ 1px** — html2canvas не рисует субпиксель.
4. **Не резать строки таблицы / заголовки** — `break-inside: avoid` / `page-break-inside: avoid` на `tr`, карточках, шапках; длинные таблицы — `thead { display: table-header-group }`.
5. **Последняя страница** — fill ≥ ~40%; если «хвост» из 1–2 строк — сжать отступы/шрифт предыдущих листов или ужать контент (см. `references/pagination.md` у html-to-pdf).
5b. **Не обрезать людей между листами** — скил `fst-print-layout`. Нумерация сквозная. `overflow: hidden` не должен прятать `tr`. Первый лист с логотипом ≈ 16 строк списка.
6. **Масштаб** — сначала CSS (шрифт, padding), потом `fitPrintPages` (zoom). Не ставить произвольный `--scale` на весь multi-page PDF вне printFit.
7. **Печать ephemeral** — модалки печати через window chrome `ephemeral` (не сворачивать в taskbar).
8. **i18n** — подписи бланков RU+KA (+EN при наличии ключей) синхронно.

## Чеклист перед сдачей бланка

- [ ] На экране превью: ничего не обрезано по краям
- [ ] Нет пустой второй страницы из-за overflow
- [ ] `fitPrintPages` срабатывает после данных на листе
- [ ] Ctrl+P / PDF: бордеры видны, текст читаем
- [ ] Альбом vs портрет совпадает с `@page` в `print.css`
- [ ] На проде (Vercel) то же поведение после деплоя — локаль не источник правды

## Внешний CLI (опционально)

Для разовых HTML→PDF вне приложения (черновик макета):

```bash
node .cursor/skills/html-to-pdf/scripts/html-to-pdf.js input.html out.pdf --format=A4
# landscape: --landscape
# ожидание N страниц: --expect-pages=2
```

Сначала `cd .cursor/skills/html-to-pdf && npm install` (один раз). Auto-fit в скрипте — shrink мелкого overflow; крупный контент уходит на следующие страницы с page-break rules.

Подробности upstream: `.cursor/skills/html-to-pdf/SKILL.md`.
Пагинация: `.cursor/skills/html-to-pdf/references/pagination.md`.

---
name: legal-docs-ru
description: Создание профессиональных юридических документов на русском языке — справки, заключения, аналитические записки, письма в трибуналы, отчёты. Использовать при запросах на создание юридических, аналитических или деловых документов на русском языке с профессиональным оформлением.
---

# Навык: Юридические документы (RU)

## Типы документов

| Тип | Описание |
|-----|----------|
| **Справка** | Аналитическая справка с резюме, разделами, таблицами |
| **Письмо** | Формальное письмо в трибунал/суд/орган |
| **Заключение** | Экспертное заключение с выводами |
| **Меморандум** | Правовой меморандум с анализом |
| **Отчёт** | Корпоративный отчёт с данными |

## Общие требования к форматированию

### Цветовая схема

- Заголовки: `#1A365D` (тёмно-синий)
- Подзаголовки: `#2C5282` (синий)
- Основной текст: `#333333`
- Вспомогательный текст: `#666666`

### Шрифты и размеры

- Заголовок документа: 18pt, полужирный, по центру
- Heading 1: 13pt, полужирный, нумерация (1., 2., 3.)
- Heading 2: 12pt, полужирный, нумерация (2.1., 2.2.)
- Основной текст: 11pt, межстрочный интервал 1.15
- Подпись/дата: 10pt

### Поля страницы

- Все поля: 2.0 см
- Формат: A4 (21.0 × 29.7 см)

### Таблицы

- Заголовок: белый текст на `#1A365D`
- Чётные строки: `#F7FAFC`
- Нечётные строки: белый
- Границы: `#E2E8F0`

## Языковые требования

- Формальный деловой стиль
- Юридическая терминология
- Ссылки на статьи законов в формате: ст. XX ГК РФ, п. X.X Контракта

## Шаблон справки

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        AlignmentType, BorderStyle, WidthType, ShadingType } = require('docx');

const COLORS = {
  heading: "1A365D",
  subheading: "2C5282",
  text: "333333",
  tableHeader: "1A365D",
  tableAlt: "F7FAFC",
  border: "E2E8F0"
};

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Times New Roman" } }
    }
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 }
      }
    },
    children: [
      // Заголовок
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
        children: [
          new TextRun({
            text: "АНАЛИТИЧЕСКАЯ СПРАВКА",
            bold: true,
            size: 36,
            color: COLORS.heading
          })
        ]
      }),
      
      // Подзаголовок
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [
          new TextRun({
            text: "О [предмет справки]",
            size: 24,
            color: COLORS.subheading
          })
        ]
      }),
      
      // Раздел
      new Paragraph({
        spacing: { before: 300, after: 150 },
        children: [
          new TextRun({
            text: "1. Название раздела",
            bold: true,
            size: 26,
            color: COLORS.heading
          })
        ]
      }),
      
      // Текст
      new Paragraph({
        alignment: AlignmentType.JUSTIFIED,
        spacing: { after: 150, line: 276 },
        children: [
          new TextRun({
            text: "Текст раздела.",
            size: 22,
            color: COLORS.text
          })
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  require('fs').writeFileSync('spravka.docx', buffer);
});
```

## Шаблон письма

```javascript
const doc = new Document({
  sections: [{
    children: [
      // Адресат
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [
          new TextRun({ text: "В Арбитражный суд", size: 22 }),
        ]
      }),
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        spacing: { after: 400 },
        children: [
          new TextRun({ text: "[Наименование]", size: 22 })
        ]
      }),
      
      // Заголовок
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 300 },
        children: [
          new TextRun({
            text: "ПИСЬМО",
            bold: true,
            size: 28
          })
        ]
      }),
      
      // Обращение
      new Paragraph({
        spacing: { after: 200 },
        children: [
          new TextRun({
            text: "Уважаемые члены Трибунала,",
            size: 22
          })
        ]
      }),
      
      // Текст
      new Paragraph({
        alignment: AlignmentType.JUSTIFIED,
        spacing: { after: 150, line: 276 },
        children: [
          new TextRun({
            text: "Настоящим направляем...",
            size: 22
          })
        ]
      }),
      
      // Подпись
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        spacing: { before: 400 },
        children: [
          new TextRun({
            text: "С уважением,",
            size: 22
          })
        ]
      }),
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [
          new TextRun({
            text: "[Подпись]",
            size: 22
          })
        ]
      }),
      
      // Дата
      new Paragraph({
        alignment: AlignmentType.LEFT,
        spacing: { before: 300 },
        children: [
          new TextRun({
            text: "[Дата]",
            size: 20,
            color: "666666"
          })
        ]
      })
    ]
  }]
});
```

## Типовые формулировки

### Начало документа

- «Настоящая справка подготовлена в связи с...»
- «По результатам анализа установлено следующее...»
- «В соответствии с поручением от [дата]...»

### Ссылки на нормы

- «согласно п. X ст. XX ГК РФ»
- «в силу положений ст. XX Федерального закона...»
- «как следует из п. X.X Контракта»

### Выводы

- «Таким образом, [вывод]»
- «На основании изложенного полагаем...»
- «Учитывая вышеизложенное, рекомендуется...»

## Зависимости

```bash
npm install docx
```

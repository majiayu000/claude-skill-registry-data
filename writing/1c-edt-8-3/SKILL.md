---
name: '1C EDT: интерфейс 8.3'
description: >-
  Use when designing a managed command interface or a managed form in a 1C:EDT
  project for platform 8.3.
---
# 1C EDT: интерфейс 8.3

Apply when designing a managed command interface or a managed form in a 1C:EDT project (`Form.form`, subsystems, the command interface). This is the 8.3 interface standard, not 8.2 and not the ordinary application. Checklist distilled from ITS v8std, not a copy of the articles.

## Screen and command interface (№727, №711, №712, №714, №715)

- Design for 1280×768 at 96 DPI. The usable area is about 1280×668 after the taskbar and the browser. Forms fit without vertical or horizontal scrolling. A list may scroll vertically, not horizontally.
- Commands are ordered by importance and how often they are used. Neighboring items should not start with the same words. Group the way the user thinks about the work.
- Sections match real areas of work. `Главное` is first and holds commands common to the whole configuration. Settings, administration, and service sections are last.
- Reference material sits in the related section, in a dedicated section, or in the navigation of a subordinate form. A list that starts a business process sits in that work section.
- A section title is at most 35 characters. Explain an abbreviation in a tooltip. Pictures share one style.
- A small command set uses the function panel. A complex section hides it and uses the function menu.
- Put lists, primary documents, workplaces, specialized processors, and reports of that area in the section. Do not put secondary objects that are already reachable from other forms.
- A command title is at most 38 characters, preferably 30. Group by the user’s task, not by a technical kind. A group should have about 7 commands or fewer.
- Do not make an empty one-command group. A group with one important command still has a title.
- When there are many commands, put the section panel vertically on the left, “picture and text”, 16×16 images. Toolbars and open windows go on top. Hide the current section’s function panel and use the function menu.

## Document form (№716, №717, №718, №719)

- The default button is the leftmost. Usually `Провести и закрыть` or `Записать и закрыть`.
- The same command order in every document. Do not rearrange the platform’s system buttons.
- Posting or writing, create-based-on, print, global commands, and context reports are visible without opening `Ещё`, at the standard screen size.
- If there are many commands, important buttons are a picture without text.
- A tabular-section header is one line. A multi-level column has a shared title, and empty header cells have a tooltip. The column title fits in the header.
- When the table scrolls horizontally, freeze the identifying columns and the line number on the left. Size numeric columns for the values you see most often.
- Totals sit directly under their table, with nothing in between. The totals area holds only totals and is aligned to the right. Gray background, view-only fields. Do not write the word `итог` in the title. The currency follows its field.
- More than four totals, or totals that do not fit one line, go in the table footer.
- A comment is usually one line at the bottom of the form. A long comment is its own tab.
- The one-line comment is last, title on the left, no choice buttons. The multiline comment stretches with the form and shows a filled flag.
- `Ответственный` is at the bottom. If both are present and the comment is one line, they share that bottom row.

## Controls, layout, fonts, settings (№720, №721, №722, №687, №753)

- A tumbler is for a choice that changes what the form shows, enables, or contains. Few short options. Long names or many options are a drop-down. Add a title when the purpose is unclear or it acts as a switch.
- A tooltip only on a field that needs one. Not on everyday attributes, and not a manual for the field.
- An ordinary tooltip hides behind `?`. Links, icons, and formatting use the extended tooltip. About 255 characters. More than that is a link to an ITS article.
- A setting’s tooltip sits below the field. A decoration label is the last resort.
- Inside one form, titles of single-line fields, radio buttons, and tumblers sit on the same side.
- Align related fields. Shorten a title that is too long. The control comes before the fields that depend on it.
- Items that do the same thing have the same name and sit in about the same place.
- Do not use a vertical green line to mark groups, except a horizontal multi-column group.
- Important, required, and hand-entered fields go on the left. Auxiliary and auto-filled fields go on the right.
- A tabular section is at least 7 rows. Independent tables sit on their own tabs.
- Use the configuration’s style fonts. If you need a face, use MS Core Fonts. Do not use a font that may be missing on some OS. This applies from platform 8.3.2.
- A settings-and-catalogs section group is a title, the settings, and the messages. Several groups are collapsible, with the standard decoration.
- The groups fit on 1280×768 without vertical scrolling. The first group starts expanded only if the rest still fit. A section with one group stays expanded, uses ordinary behavior, and has no group title.

## Sources

- https://its.1c.ru/db/v8std/content/711/hdoc
- https://its.1c.ru/db/v8std/content/712/hdoc
- https://its.1c.ru/db/v8std/content/714/hdoc
- https://its.1c.ru/db/v8std/content/715/hdoc
- https://its.1c.ru/db/v8std/content/716/hdoc
- https://its.1c.ru/db/v8std/content/717/hdoc
- https://its.1c.ru/db/v8std/content/718/hdoc
- https://its.1c.ru/db/v8std/content/719/hdoc
- https://its.1c.ru/db/v8std/content/720/hdoc
- https://its.1c.ru/db/v8std/content/721/hdoc
- https://its.1c.ru/db/v8std/content/727/hdoc
- https://its.1c.ru/db/v8std/content/722/hdoc
- https://its.1c.ru/db/v8std/content/687/hdoc
- https://its.1c.ru/db/v8std/content/753/hdoc

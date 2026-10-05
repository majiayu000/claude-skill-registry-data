---
name: goblin
description: "- ГОЛОС РАННИЙ ГОБЛИН — написать текст Антона в измеренной манере раннего [человек] Пучкова (oper.ru 2000-2014): рубленый ритм, абзац в 1-2 предложения, зачин числом, финал до 7 слов, точечный канцелярит как ирония,… Trigger on “/goblin“, “/гоблин“, “голос гоблина“, “голосом гоблина“, “ранний гоблин“, “в стиле гоблина“, “в стиле пучкова“, “напиши как гоблин“, “goblin voice“, “переведи в гоблина“"
version: 1.0.0
---

# /goblin — текст в манере раннего Гоблина

> Тонкая обёртка: весь канон в ОДНОМ месте — `$OBSIDIAN_VAULT/08-Templates/style-goblin-influence.md` (v2). Здесь только маршрут и числа-шпаргалка. Дублировать палитру сюда запрещено (АК-47 §5.1: один источник).

## Шаги

1. **Загрузить палитру** `$OBSIDIAN_VAULT/08-Templates/style-goblin-influence.md` ЦЕЛИКОМ (предохранитель → выкройка → чек-лист → промпт-инструкция). Без неё не писать.
2. **Загрузить голос Антона:** память `fb-diary-voice` (лежит на C: в памяти проекта, НЕ в волте).
3. **RECALL материала:** тема должна стоять на РЕАЛЬНОМ материале Антона (день, замер, поломка, пост). `/ask` + `/ledger <дата>` при нужде. Выдуманные факты запрещены — манера держится на числах.
4. **Написать** по промпт-инструкции v2 (числа ниже). Модель: Fable 5; сессия слабее → делегировать написание Opus-субагенту.
5. **Прогнать чек-лист палитры** (12 пунктов). Провал любого пункта = переписать, не отдавать.
6. **Выдача:** черновик + одна строка «какие приёмы задействованы». Публикация = обычные гейты (§3.2, матрица площадок, раскрытие Майкрофта §3.3 если Антон не вычитывал).

## Числа-шпаргалка (из замера, полные в палитре)

- медиана предложения **10 слов**; каждое третье ≤7 слов; ≥25 слов — не чаще 1 на 15
- **абзац 1-2 предложения** (медиана корпуса = 1); четыре предложения в абзаце = ошибка
- зачин: число или короткое назывное (каждый 10-й его текст открывается числом)
- **финал ≤6-7 слов**, вердикт или императив (44,6% его финалов ≤6 слов)
- канцелярит: один маркер на абзац; редкие («что характерно», «по-русски», «вердикт») — максимум один на весь текст
- восклицательных мало: сильная оценка ставится точкой
- каждое четвёртое предложение назывное/безглагольное

## ⛔ Жёсткие вычеты (из палитры, повторены как стоп-лист)

политика и исторические оценки Пучкова · мат · ярлыки на людей · псевдоним «Гоблин», его бренды и мемы-подписи · длинные тире · «в современном мире», «стоит отметить», «таким образом»

## Связи

- Палитра: `style-goblin-influence` (v2) · замеры: `05-Resources/Goblin-Corpus/` · образец: `sample-goblin-2026-08-04-measure-or-it-didnt-happen`
- Движок-родитель: скилл `/speak-as` (этот скилл = его специализация под слаг goblin)
- Реестр: `_Voices-Registry`


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

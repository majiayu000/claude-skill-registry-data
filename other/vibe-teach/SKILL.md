---
name: vibe-teach
description: "Ежедневная обучающая серия «Claude Code / Codex для не-кодеров» — сгенерировать и опубликовать 1-3 поста дня (тизер + средний FB-пост) для аудитории «богатые 40+, автоматизация бизнеса». Триггеры: “/vibe-teach“, “пост серии“, “обучающий пост дня“, “vibe teach“, “серия для не-кодеров“"
version: 1.0.0
---

# /vibe-teach — пост дня обучающей серии

## Шаг 0. Контекст (обязательно, до буквы текста)
1. Прочитай план: `$OBSIDIAN_VAULT\04-Projects\project-vibe-teach.md` (рубрики, арка, day_counter, секция «Из ДР»).
2. RECALL: свежие сессии/находки для рубрики «Кейс дня» — `content_miner.py` triage + вчерашний day_ledger.
3. День недели → рубрика из таблицы ротации. day_counter → место в 30-дневной арке.

## Шаг 0.5. Очередь тем (одобрена Антоном 21.08)
Источник тем = `$OBSIDIAN_VAULT\04-Projects\vibe-teach-content-queue.md`: бери первый неотмеченный пункт, после публикации отметь [x] + дата + ссылки. Дни 1-5 — готовые тексты Fable (одобрены). В КАЖДЫЙ пост вшивай нашу конкретную стройку как живой пример (второй мозг/CRM/шина/флот/сторожа), не абстракцию.

## Шаг 1. Написать (голос = текущая топ-модель сессии, Fable если доступен)
- **Тизер** ≤240 знаков — крючок, без ваты, строчными (регистр лаборатории).
- **Средний пост FB** — 100-250 слов: одна мысль, один пример «до→после», один шаг читателю.
- Аудитория: не-кодер 40+, владелец бизнеса. Ни одного термина без бытового объяснения.
- Цифры экономики: ТОЛЬКО из секции «Из ДР» (DR26-08-21-HUB-02-1609). Пока пусто — пиши «по моей оценке», не факт. Правда в цифрах ⛔ не ослаблена.
- Формулировки Антона из голосовых — дословно (§9.7 БЕЗ КУПЮР).
- Приёмы подачи = «формула Юницкого» (скилл `/guide` §Шаг 1): в пост брать минимум 2 из 6 — артефакт-скриншот нашей системы + один из (спорный тезис / чек-лист / честная кривая). 3-5 постов созрели в тему → сшивка через `/guide` (Дзен-урок + GitHub гайд-хаб).
- CTA трёхэтажный (канон = секция «CTA и перелинковка» в project-vibe-teach.md): все → WhatsApp +[id] (первая сессия бесплатно); бизнес → звонок calendly.com/paloaltolab/1-on-1; инженеры → чат t.me/clawrus (RU) / t.me/claweng (EN). В коротком тизере — один этаж, в среднем посте — до трёх.
- ПЕРЕЛИНКОВКА: каждый пост зовёт на 1-2 другие наши площадки по матрице из project-vibe-teach.md (FB→TG+GitHub, TG→FB+GitHub, Threads→TG, X→GitHub+TG, Дзен/LJ→GitHub+TG, GitHub→TG+Calendly); ссылки ротировать по дням, все сразу = спам.
- Раскрытие авторства: пишет Майкрофт → первая строка по §3.3; если текст = расшифровка слов Антона, вычитанная им — без раскрытия.

## Шаг 2. Гейты (fail-closed) — ДО показа Антону и ДО публикации, не после
- Порядок: текст готов → slop_gate (нужный --tier) → FAIL = /ai-slop переписывает и повторный прогон → только потом показ/публикация. Урок 21.08: показал Антону тексты без ворот, вопрос «а ты проверял?» вскрыл пропуск.
- `slop_gate` — FAIL = переписать сейчас, не отложить.
- `platform_gate.py` / матрица площадок: тизер → TG, средний → FB. Лонгрид в FB/чаты ⛔.
- `pub_registry.can_post` перед каждой трубой; `paused` в registry/limits.json = стоп.

## Шаг 3. Публикация (сразу, без ожидания; список площадок = приказ Антона 21.08)
Каскад от одного урока дня:
1. **GitHub (EN)** — лонгформ-дом: markdown-урок в repo серии (Assisted-by, не Co-authored-by).
2. **LiveJournal + Дзен (RU)** — средний/лонгрид (перевод-адаптация). Рельсы автопостинга НЕТ: браузерная работа с хаба (§7.2); построить рельсу = задача.
3. **FB (RU)** — средний, скилл `/fb-post` (fb_guard ≤8/день).
4. **Тизеры ≤240**: Threads (RU, браузер, хаб-only) · X (EN, label Automated) · TG [аккаунт] (RU) · TG @claweng (EN) — тизер+ссылка на лонгформ.
- Всё через `pub_registry.can_post` → `pub_ledger.jsonl` — мимо реестра = баг.
- Площадки нет в platform_rules.json = не постим (fail-closed).

## Шаг 4. Хвост
- day_counter +1 в project-vibe-teach.md, строка в Журнал (дата, рубрика, ссылки на посты).
- Контентный момент из процесса → content_miner capture.
- Вопросы/ответы аудитории под постами → на следующий день рубрика «Вопрос дня» отвечает лучшим.

## Границы
- Tier-2 (деньги, обязательства, секреты) → пауза + аск в 02.
- Приватное Антона → ⛔ наружу; personal только обобщённо.
- Платный продукт НЕ анонсировать до решения Антона по DR26-08-21-HUB-01-1606.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

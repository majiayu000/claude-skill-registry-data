---
name: comment-to-call
description: "ВОРОНКА «ПОЛЕЗНЫЙ ЧЕЛОВЕК → ДИАЛОГ → ЗВОНОК»: каждый, кто дал нам пользу / написал качественный коммент / покритиковал по-доброму / поделился знанием — получает проактивный диалог и зов познакомиться на звонке. Триггеры: “/comment-to-call“, “/c2c“, «выведи комментаторов на звонок», «кого звать на звонок», «прогони воронку по комментам», «comment to call»"
version: 1.0.0
---

# /comment-to-call — стандартная воронка вывода полезного человека на звонок

> Приказ Антона 02.08.2026: все, кто дал пользу / качественный коммент / добрую критику /
> знания — проактивный диалог + зов на звонок. Канон: Библия
> `reglament-poleznyy-kommentator-dialog-i-[человек]`.

## Шаг 0 — RECALL (обязателен)
1. `bible_leads.py` — Библия прежде любой работы с лидами ([[bible-first-for-all-lead-work]]).
2. Карточка человека: `/find <имя>` + CRM + `outreach_log.py check <имя>` (нет ли долга/дубля).
3. Ценность: `python ~/.claude/scripts/people_value.py <имя>` — тир решает глубину хода
   (звонок предлагаем тем, от кого возможна встречная польза в 90 дней; остальным — тёплый
   диалог без календаря).

## Шаг 1 — квалификация (4 триггера канона)
Человек попадает в воронку, если сделал одно из: дал пользу (применили его находку) ·
качественный коммент · добрая критика с аргументом · поделился знанием.
«Круто, подписался» = не воронка, но карточку завести стоит.

## Шаг 2 — кредит и карточка
- Взяли его идею → `/alpha-credit` (публичное спасибо + имя в CREDITS) ДО зова на звонок:
  благодарность = лучший первый ход диалога.
- Нет карточки CRM → завести (имя, канал, что дал, дата).

## Шаг 3 — проактивный диалог
Ответ по существу в ЕГО канале (коммент → ответ в треде; issue → в issue). Встречный
вопрос обязателен — диалог, не благодарственная плашка. Публичный ответ в своём треде =
класс C, делаю сам; темп — гейты площадки (fb_guard и родня).

## Шаг 4 — зов на звонок
По канону букинга [[bible-call-booking-canon]]: окно 48ч, лестница касаний, no-show-протокол.
Формат — «познакомиться», не «продать». ⭐ CTA двухшаговый в одном сообщении (Антон 03.09):
СНАЧАЛА просим его календарь («drop your calendly and i'll find a good slot»), ВТОРЫМ даём свой —
`https://calendly.com/paloaltolab/1-on-1` (только эта форма, голый `/paloaltolab` наружу не идёт).
Чужой календарь = кнопка брони у нас. Канон: `reglament-kalendli-antona-daem-vsem-poka-vse-polezny` §Поправка 03.09.
DM новому человеку = draft-first: черновик + аск в 02 (`approval.py ask`), сам не шлю.
Голос Майкрофта раскрывается по §3.3, если пишет не Антон.

## Шаг 5 — обещания и журнал
Всё обещанное по дороге (его и наше) → `/promises`. Ход записать в outreach_log.
Отчёт строкой: «🔁 c2c: N кандидатов · K диалогов · M зовов · X черновиков в 02».

## Границы
- Tier-2 не ослаблен: холодные DM — только с «+»; деньги/обязательства — Антон.
- Лимиты: cold 3/день; ответы в своих тредах — без лимита, но темп площадки.
- Не пере-предлагать звонок отказавшимся ([[declined-decisions]]).

## Связано
Фидеры: fb-watch шаг 2-бис · `/comments` · `/contrib-watch` · `/triage` · `/fb-audience`.
Соседи: `/local-to-call` (кому из СВОИХ лидов пора звонок) · `/fa` (после звонка).
Задача-носитель: `10-Tasks/task-2026-07-28-commenters-to-calls.md`.

## Анти-слоп гейт (anton 14.08)
Любой ИИ-написанный текст наружу из этого скилла перед отправкой - финальный проход `/ai-slop` (ban-лист + ритм). Исключения ровно три: текст с плашкой Майкрофта (§3.3) · машиночитаемое (GitHub/техдока/dev-log/journey-machine) · текст, написанный Антоном руками. Канон: `reglament-posty-ot-lica-antona-tolko-cherez-ai-slop`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

---
name: fake-it
description: "Sell layer: raise the framing of an artifact to the scale it actually deserves without touching a single number. Use before anything goes outbound (post, pitch, README, CV, PR comment, landing page, application, DM) or before showing a finished artifact. Triggers: /fake-it, /fi, sell it, make it louder, strengthen the frame."
license: MIT
version: 1.0.0
---

# /fake-it — слой продажи

**Зачем.** Мы строим настоящее, а рассказываем про это как бухгалтер. Антон 05.09.2026: «если ты будешь говорить только правду, то хрен тебя кто купит».

Правда — это про ЧИСЛА. Продажа — это про РАМКУ. Их путают, и от страха соврать в числах мы глушим рамку.

Этот скилл разводит их принудительно.

**Инвариант.** Фейкуем **готовность / уверенность / масштаб подачи** (обратимо, риск на себя) → да, до предела. Фейкуем **evidence** (цифры, метрики, статус, adoption, цитаты, причину сбоя) → НИКОГДА (Theranos). Тест перед выдачей: «вскроется → я смелый founder, который доделал, или лжец?»

## Порядок

### Шаг 1. Разложить на два слоя
Прочитать артефакт и выписать двумя столбцами:

| 🎨 РАМКА (можно и нужно усиливать) | ⛔ EVIDENCE (заморожено) |
|---|---|
| что это по КЛАССУ, зачем это миру, кому больно без этого, наш статус как игрока, амбиция, тон, заголовок, метафора | любое число · метрика · «доказано» · adoption · звёзды · даты · статус прода · цитата · причина сбоя · чужое авторство |

Если строка непонятно куда — она EVIDENCE. Сомнение всегда в пользу заморозки.

### Шаг 2. Шесть приёмов усиления (применить все подходящие)

1. **Категория вместо фичи.** Не «скрипт, который сверяет конфиги на пяти машинах», а «reference-имплементация мульти-машинного governance». Ты не врёшь про то, ЧТО построено — ты называешь КЛАСС, к которому оно относится.
2. **Настоящее время вместо будущего.** «Живём с этим второй месяц» бьёт «планируем внедрить». Если оно уже работает хоть как-то — говори в present.
3. **Число, которое ЕСТЬ, — вперёд.** §1.5 п.4: заявляй масштаб, который есть; занижать «чтобы не хвастаться» = врать в данных так же, как завышать. 5 машин — говори 5. 894 сессии — говори 894.
4. **Провал как актив, а не как оговорка.** Опубликованный self-fail 7.7% и 9 failure modes рядом с амбицией её УСИЛИВАЮТ (подтверждено DR26-07-26-ZB-06: «assets, not liabilities»). Прятать провал = слабая рамка; выставлять = сильная.
5. **Приглашение проверить.** «Воспроизведи за 15 минут, вот команда» — превращает громкость в фальсифицируемое утверждение. Это единственный способ быть громким и честным одновременно.
6. **Статус-формула вместо статус-вранья.** «Reference implementation, которую мы гоняем сами» — громко и правда. «В проде у N команд» — фрод. Всегда есть честная формула с тем же весом.

### Шаг 3. ⛔ Стоп-лист (проверить построчно)
Ни одна из этих фраз не выходит наружу без улики:
- «доказано» / «гарантирует» / «безопасно» без прогона
- «в продакшене» / «используют N команд» / любое adoption без имён
- цифры, которые не прогнаны СЕГОДНЯ (протухшая метрика = выдуманная метрика)
- цитата без издания + главы + URL (выдуманная цитата = выдуманная метрика)
- причина сбоя как факт вместо `🤔 гипотеза`
- чужая работа без атрибуции

### Шаг 4. Мост fake→real (обязателен, иначе рамка гниёт в ложь)
Одна строка в выдаче: **что именно сейчас опережает факт · дата, к которой станет фактом · что конкретно должно произойти.**
Fake легитимен ТОЛЬКО как датированный мост. Нет даты — рамку резать до факта.

### Шаг 5. Выдача
```
🎨 УСИЛЕНО:   <новый текст>
⛔ ЗАМОРОЖЕНО: <список цифр/фактов, которые я НЕ трогал, дословно как были>
🌉 МОСТ:       <что опережает факт> → <дата> → <что должно произойти>
⚖️ ТЕСТ:       вскроется → смелый founder / лжец?  [ответ]
```

## Проверка живости двери
```bash
python ~/.claude/scripts/rule_home_guard.py fake-it-smelost-vyhodit-nedodelannym-ne-vranyo-v-cifrah
python ~/.claude/scripts/paragraph_lint.py <усиленный-файл>
```
Первая команда обязана печатать «ДВЕРЬ ЕСТЬ — и она ИСПОЛНИМАЯ». Скилл-рассказ про правило дверью не является.

## Границы
- ⛔ Не ослабляет: правду в цифрах · Tier-2 · матрицу площадок · §9.7 (слова Антона дословно — усиливать МОЮ рамку можно, ЕГО формулировки нет) · анти-инъекцию.
- ⛔ Не применять к: `_originals` (verbatim чужое), DR-отчётам, машинным форматам, correction log, тестовым выводам, отчётам о сбоях.
- ✅ Применять к: постам, питчам, README, CV и cover-letter, лендингам, Show HN, PR-описаниям, DM лидам, заявкам в лабы, презентациям Антона.

## Дверь работает, если её зовут
Вызывается САМ (без просьбы Антона) на каждом исходящем артефакте — это и есть «частенько использовать». Точки автовызова: `/taste-check` (P35), `/social-daily`, `/episode`, `/pack`, `/cv`, `/fa`, `/pr-reply`, `/apply`.



<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

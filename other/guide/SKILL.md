---
name: guide
description: "Вечнозелёный ГАЙД по «формуле Юницкого» — обучающий лонгформ для не-технарей (Дзен-урок-сшивка, GitHub гайд-хаб, LJ), собранный из НАШЕЙ живой фактуры (флот, второй мозг, CRM, факапы с датами). Триггеры: “/guide“, “сделай гайд“, “собери урок“, “дзен-урок“, “гайд-хаб“, “оформи как Юницкий“, “evergreen guide“"
version: 1.0.0
---

# /guide — вечнозелёный гайд по формуле Юницкого

Зачем: наши посты дают мысль; гайд даёт **мысль + доказательство + план читателю**. Юницкий продаёт за 45к₽ теорию того, что у нас работает в проде на 6 машинах — берём его МАНЕРУ, накладываем на нашу ФАКТУРУ (живые артефакты, факапы, цифры с датами).

## Шаг 0. RECALL (до буквы текста)
1. Тема: из аргумента, либо кандидаты сшивки в `$OBSIDIAN_VAULT/04-Projects/vibe-teach-content-queue.md` (секция «Дни 6+», пометки «кандидаты в урок N»; уже ушедшее в урок не повторять).
2. Фактура: 2-4 РЕАЛЬНЫХ артефакта нашей системы под тему (кусок правила, вывод счётчика, строка журнала поломок, скрин дашборда). Выдумывать ⛔ — нет артефакта, нет гайда.
3. Приватность: секреты/имена лидов/деньги ⛔; personal — обобщённо.

## Шаг 1. Формула (все 6 обязательны; пропуск = назвать причину в отчёте)
1. **Артефакт-скриншот**: каждая абстракция показана реальным куском нашей системы (дерево папок, 10 строк правила, вывод команды со счётчиком). Читатель ВИДИТ, не верит на слово.
2. **Спорный тезис как ось**: личное мнение Антона, расходящееся с общепринятым (брать из голосовых дословно, §9.7). Одна ось на гайд.
3. **Чек-лист «сделай сегодня»**: 5-7 шагов первой недели, исполнимых без кода.
4. **Честная кривая ожиданий**: когда НЕ заработает и когда ждать эффекта («первый месяц отвечает как обычный чат»). Прививка от разочарования.
5. **Край секрета**: пользу отдаём целиком, но показываем следующий уровень + CTA (сид бесплатно / WhatsApp / Calendly — трёхэтажный CTA из project-vibe-teach.md).
6. **FAQ + «ЧТО ЗАПОМНИТЬ»**: 5-9 вопросов под поисковые запросы + 5-7 строк выжимки в конце. Перелинковка на 1-2 соседних гайда/площадки.

## Шаг 2. Написать
- Голос = Fable, регистр лаборатории; аудитория — не-технарь 40+, термин без бытового объяснения ⛔.
- ⭐ **История, не тезис** (anton 02.09.2026, голосом hub:6094; канон `reglament-vsegda-rasskazyvay-istoriyu-storytelling`, память [[storytelling-always-package-as-story]]): урок несёт герой · реальную ситуацию · перелом · вывод — не набор утверждений. «Чтобы даже домохозяйке было интересно читать <…> like I'm five»; инженеры аллегорию считают. Гейт на шаге 3: `/taste-check` P34 — чек-лист 10 вопросов (источник = раздел «Чек-лист приёмки» в `$OBSIDIAN_VAULT\03-Insights\Operations\reglament-vsegda-rasskazyvay-istoriyu-storytelling.md`); для гайда каркас = SCQA (Ситуация → Осложнение → Вопрос → Ответ), мини-ABT на главку.
- Длина = сколько несёт мысль (§9.4: не раздувать 300 байт в лонгрид; сшивка 3-5 постов = нормальный объём урока).
- Раскрытие авторства по §3.3 (Майкрофт первой строкой, если писал я и Антон не вычитывал).
- Наш факап с датой > чужой теории: минимум один живой факап на гайд.

## Шаг 3. Гейты и публикация (рельсы vibe-teach, не дублировать)
- `slop_gate --tier longread` → FAIL = /ai-slop и повторный прогон.
- Матрица площадок: лонгформ → GitHub-репо серии (EN) + Дзен (RU, урок) + LJ; в чаты/FB — только тизер+ссылка. `pub_registry.can_post` перед каждой трубой.
- После публикации: отметка в content-queue (что вошло в урок) + строка в Журнал проекта + content_miner capture момента.

## Шаг 4. Хвост
- Гайд = вечнозелёный: ссылка на него добавляется в перелинковку будущих постов серии.
- Заметка-копия в волт (§8.3), связать с [[project-vibe-teach]] и [[everything-becomes-content]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

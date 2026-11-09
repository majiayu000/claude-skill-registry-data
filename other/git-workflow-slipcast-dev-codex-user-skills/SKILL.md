---
name: git-workflow
description: "Git-флоу: ветки, коммиты (conventional commits), PR, rebase/merge, разрешение конфликтов, теги"
whenToUse: "Применяй, когда нужно организовать работу с git: ветки, коммиты, PR, слияния, откат"
---

# Git Workflow

Гайд по дисциплинированной работе с Git.

## Модель ветвления

| Модель | Когда |
|--------|-------|
| Trunk-based | Небольшие команды, частые мержи в `main` |
| Git Flow | Стабильные релизы (`main`, `develop`, `feature/*`, `hotfix/*`) |
| GitHub Flow | `main` + feature-ветки + PR |

## Чек-лист

### Коммиты
- [ ] Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`
- [ ] Атомарные коммиты — одна логическая единица = один коммит
- [ ] Понятное сообщение: что и зачем, не «update»

### Ветки и PR
- [ ] Хорошее имя ветки: `feature/auth`, `fix/login-bug`
- [ ] Перед PR: `git pull --rebase origin main`
- [ ] Описание PR: что сделано, как тестировалось, скриншоты при UI
- [ ] Запроси ревью, пройди CI зелёным

### Слияние
- [ ] Предпочитай rebase/squash перед merge для чистоты истории
- [ ] Разрешай конфликты осознанно, перепроверяй результат
- [ ] Теги для релизов: `v1.2.0` (semver)

### Безопасность и откат
- [ ] Не коммить секреты (проверь `.gitignore`, `.env` в исключениях)
- [ ] `git revert` для отката в общем репо (не force-push в shared-ветки)
- [ ] `git push --force` — только с подтверждением и в своих ветках

## Полезные команды
```bash
git status && git log --oneline -10
git add <files> && git commit -m "feat: ..."
git pull --rebase origin main
git push origin feature/name
git rebase -i HEAD~3   # сквош/переписать последние 3
```

## Правила
1. Не храни секреты в репозитории.
2. Force-push в общие ветки — только с явного согласия.
3. Держи историю читаемой (rebase/squash перед merge).
4. Один PR — одна задача.

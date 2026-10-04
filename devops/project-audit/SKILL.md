---
name: project-audit
description: Глубокий read-only аудит любого репозитория с автоматическим определением frontend, backend, mobile, database, API и infrastructure boundaries; оркестрирует профильные роли для архитектуры, багов, security/CVE/secrets/PII, error handling/try-catch/logging, типов, тестов, зависимостей и документации и материализует единый PROJECT_AUDIT.md. Use когда просят проверить весь проект, найти что не так, оценить архитектуру/безопасность/надёжность, составить remediation plan или технический due diligence.
---

# Project Audit

Проводи доказательный аудит существующего проекта без изменения production code. Разрешённые записи: один итоговый Markdown-отчёт и Task Master tasks по подтверждённым находкам.

## Workflow

1. Создай/получи Task Master audit-task через `$workflow` + `$task-master`; зафиксируй scope и output path.
2. Запусти inventory:

   ```bash
   node <skill-root>/scripts/inventory.mjs --root <repo> --format json
   ```

3. Примени `$workspace-capability-routing`, затем полностью прочитай [references/audit-playbook.md](references/audit-playbook.md). Сопоставь requested audit scope с inventory, выбери роли/skills и зафиксируй evidence; не запускай нерелевантные доменные проходы.
4. Сними baseline статическим чтением manifests/lockfiles, build/typecheck/lint/test configs, CI, migrations/schema, routes/API specs, error boundaries и dependency graph. Код и plugins недоверенного репозитория не исполняй. Project-native typecheck/lint/tests разрешены только после установления доверия, review команды/config и отсутствия install/migration/fix side effects.
5. На платформе с subagents параллельно делегируй независимые проходы профильным ролям в read-only sandbox/режиме без write tools, если он доступен. В Codex/Kimi без native role-agents выполни те же scopes последовательно, явно загружая каждый named skill; не заявляй несуществующую параллельную делегацию. Передай каждому проходу один scope и общий finding contract.
6. Выполни online advisory check для каждого обнаруженного package ecosystem. Если scanner отсутствует, не устанавливай его скрытно: проверь official advisory/registry source доступным способом и пометь coverage gap.
7. Дедуплицируй findings по `boundary + file:line + root cause`; сохрани более высокую severity и объедини evidence/remediation. Не превращай один root cause в десятки одинаковых пунктов.
8. Материализуй `PROJECT_AUDIT.md`; если файл существует, создай `PROJECT_AUDIT-YYYYMMDD-HHMM.md`, не перезаписывай без явного разрешения.
9. Проверь отчёт:

   ```bash
   node <skill-root>/scripts/validate-report.mjs <report.md>
   ```

10. Для подтверждённых critical/high findings создай Task Master tasks с dependency order. Сам исправления не применяй.

## Role routing

Всегда используй:

- `$architect` — current/target architecture, boundaries, cycles, migration sequence;
- `$analyzer` — bugs, types, mocks, dead paths, unsafe assumptions;
- `$security` — secrets, OWASP, authz, PII, supply chain и live vulnerabilities;
- `$resilience` — I/O boundaries, typed errors, timeouts/retries, cleanup и structured logging;
- `$testing` — test pyramid, gaps и verification strategy.

Подключай условно:

| Inventory signal | Роль и обязательные знания |
| --- | --- |
| Web frontend | `$frontend`, `$frontend-architecture`, `$react`/`$nextjs`, `$state-management`, `$data-fetching`, `$i18n` |
| Server/API | `$backend`, `$backend-architecture`, `$api-design`, `$typescript`/runtime skill |
| Expo/React Native | `$expo-mobile`, `$expo-mobile-architecture`, `$expo-ui-design-motion`; `$mobile-thumb-zones` только для UI/reachability scope; `$react-native-liquid-glass` только при package/intent evidence; version-sensitive выводы только после live compatibility preflight |
| SQL/Mongo/Redis/schema | `$database`, `$postgresql`/`$mongodb`/`$redis`; только read-only inspection |
| HTTP routes/OpenAPI | `$swagger`, `$swagger-coverage` |
| Docker/CI/IaC/deploy | `$devops`, `$docker`, `$ci-cd` |
| Docs drift | `$docs`, `$technical-writing` |

`screenshot`, diagram и deploy-роли не нужны без соответствующего входа. «Использовать всех» означает использовать знания всех релевантных ролей, а не создавать шум нерелевантными проходами.

Inventory `coverageGaps` (malformed manifest, symlink, depth limit) обязательно переноси в отчёт. `systems` — routing hint, а не доказательство отсутствия других систем; вручную проверь entrypoints и native config.

## Finding contract

Каждая находка содержит:

```markdown
### AUD-001 — [critical|high|medium|low] Краткое название
- Boundary: Backend | Frontend | Mobile | Database | Infrastructure | Cross-cutting
- Evidence: `relative/file.ts:42` — проверяемый факт или короткий вывод команды
- Root cause: почему дефект существует
- Impact: конкретный failure/security/business scenario
- Fix: точное изменение без применения
- Target state: правильный слой, dependency direction или control
- Verify: команда/тест, доказывающие исправление
- Owner: backend | frontend | expo-mobile | security | resilience | database | devops | testing
```

Нельзя выдавать предположение за finding. Если доказательств недостаточно, помести вопрос в `Coverage gaps / Needs verification`.

## Error-handling rule

Не требуй `try/catch` вокруг каждой функции. Его отсутствие — finding только на реальной границе отказа: HTTP/DB/filesystem/network/native API, parsing untrusted data, transaction/lock, background job, process entrypoint или cleanup ресурса — и только если нет корректного higher-level handler.

Запрещены пустые/проглатывающие catch, потеря `cause/stack`, необработанные promise rejection, бесконечные retries, отсутствие timeout/cancellation, двойное логирование и утечка secrets/PII. Предлагай typed domain/transport errors и единый boundary handler, а не blanket wrapping.

## Architecture recommendation rule

Сначала опиши фактическую архитектуру и constraints. Целевую схему выводи из domain boundaries и стека проекта, не навязывай один шаблон всем. Для legacy давай incremental migration с совместимыми этапами, ownership, dependency order, rollback и verification; полный rewrite рекомендуй только при доказанной невозможности безопасной эволюции.

## Definition of Done

- Stack/boundaries определены evidence-based, включая mixed monorepo.
- Релевантные роли отработали независимые scopes; findings дедуплицированы.
- Vulnerability data проверены online и имеют source/date; tool gaps видимы.
- Все findings имеют `file:line`, root cause, impact, exact fix, target state и verification.
- Current и target architecture, phased roadmap, dependency order и replacement table присутствуют.
- Report validator зелёный; source tree не изменён кроме отчёта/Task Master metadata.
- Для недоверенного repository не исполнялись package scripts, compiler/lint plugins, tests или binaries; ограничения явно записаны в coverage gaps.

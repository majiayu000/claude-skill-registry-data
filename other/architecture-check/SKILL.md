---
description: Mechanical audit of layer boundaries, bindings, and controller purity across modules
argument-hint: "[optional module]"
allowed-tools: "Read, Glob, Grep, Bash(grep *), Bash(find *), Bash(composer *), Task"
---

# Architecture Check

Mechanical sweep of `modules/`. Scope to `$ARGUMENTS` if a module is named, otherwise all.

Rules live in `.claude/rules/architecture.md` — this skill only *runs the checks*. For judgment calls (module placement, boundary design), delegate to the `hexagonal-architect` agent instead.

## 1. Domain purity

```bash
grep -rn "^use Modules\\\\.*\\\\Infrastructure" modules/*/Domain/ || echo "OK: no Infrastructure imports in Domain"
grep -rn "^use Illuminate\\\\\(Database\|Foundation\|Routing\|Console\|Queue\|Cache\|Auth\)" modules/*/Domain/ || echo "OK: no Laravel runtime in Domain"
grep -rn "^use Illuminate\\\\Support\\\\Facades" modules/*/Domain/ || echo "OK: no facades in Domain"
```

Infrastructure imports are a hard violation. Laravel runtime/facades are violations in new code; `App\Models\*` and `Collection`/`Paginator` are the accepted legacy trade.

## 2. Eloquent confined to repositories

```bash
grep -rnE '::(where|find|create|firstOrCreate|updateOrCreate|all)\(|DB::' \
  modules/*/Application/ modules/*/Infrastructure/Http/ || echo "OK: no queries outside repositories"
```

Expect 3 known hits (`HistoryService.php:48`, `ProfileController.php:21,25`). Anything new is a violation.

## 3. Cross-module coupling

Every import of another module must be a `Domain\...FacadeInterface`:

```bash
grep -rn "^use Modules\\\\" modules/ \
  | grep -v "Domain" \
  | grep -vE '^modules/([A-Za-z]+)/.*use Modules\\\1\\'
```

## 4. Interface ↔ binding

Portable (no `grep -P` — BSD grep on macOS):

```bash
find modules -name "*Interface.php" -path "*/Domain/*" -exec basename {} .php \; | sort -u > /tmp/sats-ifaces
grep -rho "[A-Za-z]*Interface::class" modules/*/[A-Z]*ServiceProvider.php | sed 's/::class//' | sort -u > /tmp/sats-bound
comm -23 /tmp/sats-ifaces /tmp/sats-bound
```

Anything printed is a Domain interface with no `$singletons` entry — that fails at runtime, not in phpstan. **Two kinds of false positive**, check before reporting:

- **DTO/value contracts** implemented by data objects that are constructed directly, never resolved from the container — e.g. `BlockchainDataInterface`. These are correctly unbound.
- **Dormant facades** — an interface nobody injects yet. Harmless today, breaks the moment someone injects it.

Confirm which kind before flagging:

```bash
grep -rn "<Name>Interface" modules/ app/ --include="*.php" | grep -v "implements\|^.*Domain/"
```

Known dormant today: `FaqFacadeInterface`, `NostrFacadeInterface`, `PaymentFacadeInterface` — declared and implemented, neither bound nor injected. `ChatFacadeInterface` and `OpenAIFacadeInterface` show the correct wired pattern.

## 5. Provider registration

```bash
ls modules/*/[A-Z]*ServiceProvider.php | wc -l
grep -c "ServiceProvider::class" bootstrap/providers.php
```

Counts should match (RouteServiceProvider included). A missing entry means the module silently never boots.

## 6. Controller purity

Read each `modules/*/Infrastructure/Http/Controller/*.php`. A controller may only: accept a FormRequest → call an Action/Facade → return a response. Flag any query, domain conditional, or external HTTP call.

## 7. Gate

```bash
composer phpstan && composer test
```

## Report

Per violation: `file:line`, the rule it breaks, the concrete fix. Separate **new** violations from the known debt listed in `CLAUDE.md` — only new ones block. Finish with pass/fail per module.

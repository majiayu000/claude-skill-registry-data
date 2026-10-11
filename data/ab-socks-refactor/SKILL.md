---
name: ab-socks-refactor
description: >
  Protocol and playbook for refactoring bloated controllers, tangled views, and
  paying down technical debt in the AB-Socks project. Use this skill whenever
  refactoring a file, breaking down a controller exceeding line limits (>80-120
  lines), extracting business logic into services, decomposing views into
  partials, or when tools/verify.php flags architectural violations.
---

# AB-Socks Code Quality & Refactoring Playbook

This skill provides step-by-step guidance for safely decomposing bloated files,
extracting domain services, and keeping the codebase maintainable and extensible.

---

## 1. Architectural Guardrails & Thresholds

| Component | Target Size | Hard Limit | Rules |
|---|---|---|---|
| **Controller** (`app/controllers/`) | < 80 lines | 120 lines | **Zero SQL queries**, zero calculation logic. Only parses `$_GET`/`$_POST`, calls a service, passes variables to `renderView()`. |
| **View** (`views/`) | Modular | N/A | **Zero database queries** (`db()`), zero form handling (`$_POST`). Only loops, conditions, and `e()` escaping. |
| **Service** (`app/services/`) | Focused | N/A | All SQL queries, business logic, calculations, and validations live here as plain global functions returning `['ok' => bool, 'error' => string]`. |
| **Core Helper** (`app/core/`) | Domain-agnostic | N/A | Formatting, slug generation, general helpers. No direct order/product business logic. |

---

## 2. Refactoring Protocol (Step-by-Step)

When refactoring a legacy or bloated controller (e.g. `appearance.php`, `product_edit.php`, `settings.php`):

### Step 1: Establish Baseline
Run the verifier to see current errors/warnings:
```powershell
php tools/verify.php
```

### Step 2: Identify Concerns
Break the controller down into 3 distinct parts:
1. **Input handling & state**: What does it read from `$_GET`, `$_POST`, or `$_SESSION`?
2. **Business logic & DB writes**: What validation, SQL queries, or data transformations are happening?
3. **View payload**: What variables are actually passed into `renderView()`?

### Step 3: Extract Domain Service Function
Move all DB queries, validation, and calculations into the appropriate service in `app/services/` (or create a new service if a new domain concern).

**Service Function Contract:**
```php
/**
 * Saves or updates an entity from form input.
 *
 * @param array $input Raw form data (sanitized inside service)
 * @param int $id Record ID (0 for new)
 * @return array ['ok' => bool, 'error' => string|null, 'id' => int|null]
 */
function saveEntityFromRequest(array $input, int $id = 0): array {
    verifyCsrf();
    
    // 1. Validate
    $errors = validateEntityInput($input);
    if (!empty($errors)) {
        return ['ok' => false, 'error' => implode(' ', $errors)];
    }
    
    // 2. Perform DB operations with prepared statements
    $db = db();
    // Use transaction if touching stock, money, or multiple tables!
    // ...
    
    return ['ok' => true, 'id' => $id ?: (int) $db->lastInsertId()];
}
```

### Step 4: Streamline the Controller
The controller should now be a clean orchestrator (typically 30–60 lines):
```php
<?php
$id = (int) ($_GET['id'] ?? 0);
$entity = $id ? getEntityById($id) : null;
if ($id && !$entity) redirect('admin/entities.php');

$error = null;
$success = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $result = saveEntityFromRequest($_POST, $id);
    if ($result['ok']) {
        setFlash('success', 'تغییرات با موفقیت ذخیره شد.');
        redirect('admin/entities.php');
    } else {
        $error = $result['error'];
    }
}

$pageTitle = $id ? 'ویرایش آیتم' : 'افزودن آیتم';
renderView('admin/entity_edit', compact('pageTitle', 'entity', 'error', 'success'));
```

### Step 5: Decompose Heavy Views into Partials
If a view has grown past 200–300 lines or contains repetitive UI (like cards, tabs, form sections):
1. Extract subsections into `views/admin/partials/` or `views/site/partials/`.
2. Include them via standard PHP:
   ```php
   <?php require __DIR__ . '/partials/entity_tab_general.php'; ?>
   ```
3. Ensure no partial performs database queries or mutates state.

### Step 6: Eliminate Inline Scripts & Deduplicate Front-End Logic
1. **Never write new duplicate JS helpers**: Check `docs/COMPONENTS.md` for existing toast, modal, formatter, autocomplete, and image compression tools.
2. **Eliminate inline `<script>`**: Move interactive behaviors to declarative `data-ab-*` attributes or dedicated external JS files. Keep inline scripts under 20 lines.
3. **Use unified design tokens**: Never declare page-specific `:root` palettes or raw hex colors in component CSS.

---

## 3. Safe Refactoring Checklist

- [ ] `php tools/verify.php` passes with 0 errors and adheres to the ratchet baseline.
- [ ] No controller exceeds 120 lines (aim for < 80).
- [ ] No SQL queries exist in any touched view.
- [ ] No DB writes exist directly in any touched controller.
- [ ] Zero duplicate JS helpers introduced (consult `docs/COMPONENTS.md`).
- [ ] No inline `<script>` tags exceed 20 lines in touched views.
- [ ] CSS uses unified `:root` variables without redundant palette declarations.
- [ ] Transaction and row locking (`FOR UPDATE`) preserved if money/stock is involved.
- [ ] CSRF verification retained on all POST operations.
- [ ] Persian UI text and English comments preserved.


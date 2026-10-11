---
name: ab-socks-admin-page
description: >
  Step-by-step Golden Path and scaffolding checklist for creating or refactoring an admin workstation
  page in AB-Socks. Enforces strict layer boundaries, controller size limits (<80-120 lines),
  service encapsulation, declarative views, zero inline scripts, and CSS token reuse.
---

# AB-Socks Admin Workstation Golden Path

This skill outlines the standard architecture and implementation pattern for creating a new
admin workstation page or refactoring an existing bloated one.

---

## 1. File Structure & Responsibilities

For any admin section (e.g. `discounts`):

| File | Purpose | Hard Limits & Invariants |
|---|---|---|
| `admin/discounts.php` | Front router entry | Exact 2 lines: `require_once __DIR__ . '/../app/bootstrap.php'; require_once APP_PATH . '/controllers/admin/discounts.php';` |
| `app/controllers/admin/discounts.php` | Input orchestration | **Max 80–120 lines**. Zero SQL queries. Parses `$_GET`/`$_POST`, calls service, passes payload to `renderView()`. |
| `app/services/DiscountService.php` | Business & Data logic | All SQL queries, transactions, validations. Functions return `['ok' => bool, 'error' => string]`. |
| `views/admin/discounts.php` | Master presentation | Pure HTML. Assembles partials. **Zero SQL queries**, zero inline `<script>` > 20 lines. |
| `views/admin/discounts_partials/` | Decomposed UI slices | `_kpis.php`, `_toolbar.php`, `_table.php`, `_modals.php`. |
| `assets/css/admin-discounts.css` | Workstation layout | Strictly uses `:root` tokens from `admin.css`. **Zero redundant `:root` palettes**. |

---

## 2. Standard Implementation Recipe

### Step 1: Controller (`app/controllers/admin/discounts.php`)
```php
<?php
declare(strict_types=1);

requireAdmin();

$pageTitle = 'مدیریت تخفیف‌ها';
$activeNav = 'discounts';

// 1. Handle POST actions through service
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = (string) ($_POST['action'] ?? '');
    
    if ($action === 'save') {
        $result = saveDiscountFromRequest($_POST);
        if ($result['ok']) {
            setFlash('success', 'تخفیف با موفقیت ذخیره شد.');
            redirect('/admin/discounts.php');
        }
        $error = $result['error'];
    }
}

// 2. Fetch presentation data through service
$filters = [
    'search' => trim((string) ($_GET['q'] ?? '')),
    'status' => trim((string) ($_GET['status'] ?? 'all')),
];
$data = getDiscountsWorkstationData($filters);

// 3. Render pure view
renderView('admin/discounts', array_merge([
    'pageTitle' => $pageTitle,
    'activeNav' => $activeNav,
    'error' => $error ?? null,
], $data));
```

### Step 2: Service (`app/services/DiscountService.php`)
```php
<?php
declare(strict_types=1);

/**
 * Encapsulates all discount and promotion database operations.
 */

function getDiscountsWorkstationData(array $filters): array {
    $db = db();
    // Prepared SELECT queries...
    return [
        'items' => $items,
        'kpis'  => $kpis,
        'filters' => $filters,
    ];
}

function saveDiscountFromRequest(array $input): array {
    verifyCsrf();
    
    // Validate fields...
    if (empty($input['code'])) {
        return ['ok' => false, 'error' => 'کد تخفیف الزامی است.'];
    }
    
    // DB write via prepared statement...
    return ['ok' => true];
}
```

### Step 3: View & Partials (`views/admin/discounts.php`)
```php
<?php
// views/admin/discounts.php
?>
<div class="admin-workspace">
    <?php require __DIR__ . '/discounts_partials/_header_stats.php'; ?>
    <?php require __DIR__ . '/discounts_partials/_kpis.php'; ?>
    <?php require __DIR__ . '/discounts_partials/_toolbar.php'; ?>
    <?php require __DIR__ . '/discounts_partials/_table.php'; ?>
    <?php require __DIR__ . '/discounts_partials/_modals.php'; ?>
</div>
```

### Step 4: Front-end Interactivity (Declarative Only)
- Open modals: `data-ab-modal-open="discountModal"`
- Live filtering: `data-ab-filter-target="#discountsTable"`
- Autocomplete: `data-ab-autocomplete="products"`
- Zero inline `<script>` blocks inside the view!

---

## 3. Verification & Acceptance Gate
Before finishing, run:
```bash
php tools/verify.php
```
Verify:
1. Controller line count <= 80 lines (hard max 120).
2. Zero SQL in views.
3. Zero duplicate JS helpers created.
4. CSS does not define `:root`.
5. Ratchet baseline passes.

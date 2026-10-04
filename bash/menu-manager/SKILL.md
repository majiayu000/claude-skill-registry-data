---
name: menu-manager
description: Manage the restaurant menu (products and categories) for a specific tenant.
---

# Menu Manager Skill

This skill allows you to view and modify the menu (products, prices, categories) for any store/tenant.

## Capabilities

- **List Menu**: View all categories and products for a tenant.
- **Add Product**: Add a new item to the menu.

## Scripts

### 1. List Menu
View the current menu structure.

```bash
node .agent/skills/menu-manager/scripts/list_menu.js <tenantId>
```
*   `tenantId`: The ID of the store (e.g., 'default', 'zapcardapio', 'pizzanutella').

### 2. Add Product
Add a new product to an existing category.

```bash
node .agent/skills/menu-manager/scripts/add_product.js <tenantId> <categoryId> "<name>" <price> "<description>"
```
*   `tenantId`: e.g., 'default'
*   `categoryId`: e.g., 'pizzas', 'bebidas' (Must exist in the menu)
*   `name`: Product name (use quotes)
*   `price`: Numeric price (e.g., 45.50)
*   `description`: Product description (use quotes)

## Examples

**List the menu for the default store:**
```bash
node .agent/skills/menu-manager/scripts/list_menu.js default
```

**Add a new Pizza:**
```bash
node .agent/skills/menu-manager/scripts/add_product.js default pizzas "Pizza Calabresa Especial" 45.00 "Calabresa, cebola, azeitona e borda de catupiry"
```

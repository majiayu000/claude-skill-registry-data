---
name: frappe-client-script-generator
description: Generate JavaScript client-side form scripts for Frappe DocTypes. Use when creating form customizations, field validations, custom buttons, or client-side logic for Frappe/ERPNext forms.
---

# Frappe Client Script Generator

Generate production-ready JavaScript form scripts for Frappe DocTypes with proper event handlers, validations, and custom functionality.

## When to Use This Skill

Claude should invoke this skill when:
- User wants to add client-side form customizations
- User needs field validations or calculations
- User requests custom buttons or actions on forms
- User wants to filter or fetch data dynamically
- User mentions form scripts, client scripts, or JavaScript for DocTypes
- User wants to show/hide fields conditionally
- User needs to set field values based on other fields

## Capabilities

### 1. Form Event Handlers

Generate event handlers for DocType forms following Frappe patterns from core apps.

**Refresh Event** (runs when form loads):
```javascript
// Pattern from: erpnext/accounts/doctype/sales_invoice/sales_invoice.js
frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        // Add custom buttons
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Payment'), function() {
                frm.events.make_payment_entry(frm);
            });
        }

        // Set field properties
        frm.set_df_property('customer', 'reqd', 1);

        // Show/hide fields
        frm.toggle_display('discount_section', frm.doc.apply_discount);
    }
});
```

**Setup Event** (runs once when form is created):
```javascript
// Pattern from: erpnext/stock/doctype/stock_entry/stock_entry.js
frappe.ui.form.on('Stock Entry', {
    setup: function(frm) {
        // Set query filters for Link fields
        frm.set_query('item_code', 'items', function() {
            return {
                filters: {
                    'is_stock_item': 1,
                    'has_serial_no': 0
                }
            };
        });
    }
});
```

**Onload Event** (runs on form load, before refresh):
```javascript
// Pattern from: erpnext/accounts/doctype/payment_entry/payment_entry.js
frappe.ui.form.on('Payment Entry', {
    onload: function(frm) {
        if (frm.is_new()) {
            frm.set_value('posting_date', frappe.datetime.get_today());
        }
    }
});
```

### 2. Field Change Handlers

**Single Field Change**:
```javascript
// Pattern from: erpnext/selling/doctype/sales_order/sales_order.js
frappe.ui.form.on('Sales Order', {
    customer: function(frm) {
        if (frm.doc.customer) {
            // Fetch customer details
            frappe.db.get_value('Customer', frm.doc.customer, 'customer_group')
                .then(r => {
                    if (r.message) {
                        frm.set_value('customer_group', r.message.customer_group);
                    }
                });
        }
    }
});
```

**Multiple Field Dependencies**:
```javascript
// Pattern from: erpnext/accounts/doctype/sales_invoice/sales_invoice.js
frappe.ui.form.on('Sales Invoice', {
    customer: function(frm) {
        frm.events.set_dynamic_field_label(frm);
    },
    currency: function(frm) {
        frm.events.set_dynamic_field_label(frm);
    },
    set_dynamic_field_label: function(frm) {
        if (frm.doc.currency) {
            frm.set_currency_labels(['total', 'grand_total'], frm.doc.currency);
        }
    }
});
```

### 3. Child Table (Grid) Events

**Child Table Row Events**:
```javascript
// Pattern from: erpnext/accounts/doctype/sales_invoice/sales_invoice_item.js
frappe.ui.form.on('Sales Invoice Item', {
    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code) {
            frappe.call({
                method: 'erpnext.stock.get_item_details.get_item_details',
                args: {
                    item_code: row.item_code,
                    company: frm.doc.company
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, 'rate', r.message.price_list_rate);
                        frappe.model.set_value(cdt, cdn, 'uom', r.message.stock_uom);
                    }
                }
            });
        }
    },

    qty: function(frm, cdt, cdn) {
        frm.events.calculate_totals(frm, cdt, cdn);
    },

    rate: function(frm, cdt, cdn) {
        frm.events.calculate_totals(frm, cdt, cdn);
    }
});
```

**Grid Operations**:
```javascript
// Pattern from: erpnext/stock/doctype/stock_entry/stock_entry.js
frappe.ui.form.on('Stock Entry', {
    items_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.s_warehouse = frm.doc.from_warehouse;
        row.t_warehouse = frm.doc.to_warehouse;
    },

    items_remove: function(frm) {
        frm.events.calculate_totals(frm);
    }
});
```

### 4. Custom Buttons and Actions

**Standard Button Patterns**:
```javascript
// Pattern from: erpnext/accounts/doctype/sales_invoice/sales_invoice.js
frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.outstanding_amount > 0) {
            frm.add_custom_button(__('Payment'), function() {
                frm.events.make_payment_entry(frm);
            }, __('Create'));
        }

        // Add custom button in toolbar
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__('Get Items from Sales Order'), function() {
                erpnext.utils.map_current_doc({
                    method: 'erpnext.selling.doctype.sales_order.sales_order.make_sales_invoice',
                    source_doctype: 'Sales Order',
                    target: frm,
                    setters: {
                        customer: frm.doc.customer || undefined
                    },
                    get_query_filters: {
                        docstatus: 1,
                        status: ['not in', ['Closed', 'On Hold']]
                    }
                });
            });
        }
    },

    make_payment_entry: function(frm) {
        return frappe.call({
            method: 'erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry',
            args: {
                dt: frm.doc.doctype,
                dn: frm.doc.name
            },
            callback: function(r) {
                let doc = frappe.model.sync(r.message);
                frappe.set_route('Form', doc[0].doctype, doc[0].name);
            }
        });
    }
});
```

### 5. Data Fetching and API Calls

**Fetch from Database**:
```javascript
// Pattern from: erpnext/stock/doctype/item/item.js
frappe.ui.form.on('Item', {
    item_group: function(frm) {
        if (frm.doc.item_group) {
            frappe.db.get_value('Item Group', frm.doc.item_group, 'default_warehouse')
                .then(r => {
                    if (r.message && r.message.default_warehouse) {
                        frm.set_value('default_warehouse', r.message.default_warehouse);
                    }
                });
        }
    }
});
```

**Server Method Calls**:
```javascript
// Pattern from: erpnext/accounts/doctype/payment_entry/payment_entry.js
frappe.ui.form.on('Payment Entry', {
    party: function(frm) {
        if (frm.doc.party_type && frm.doc.party) {
            frappe.call({
                method: 'erpnext.accounts.party.get_party_details',
                args: {
                    party: frm.doc.party,
                    party_type: frm.doc.party_type,
                    company: frm.doc.company
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('party_name', r.message.party_name);
                        frm.set_value('party_account', r.message.party_account);
                    }
                }
            });
        }
    }
});
```

### 6. Form Validations

**Before Save Validation**:
```javascript
// Pattern from: erpnext/accounts/doctype/sales_invoice/sales_invoice.js
frappe.ui.form.on('Sales Invoice', {
    validate: function(frm) {
        // Validate posting date
        if (frm.doc.posting_date > frappe.datetime.get_today()) {
            frappe.throw(__('Posting Date cannot be future date'));
        }

        // Validate items
        if (!frm.doc.items || frm.doc.items.length === 0) {
            frappe.throw(__('Please add at least one item'));
        }

        // Validate total
        if (frm.doc.grand_total <= 0) {
            frappe.throw(__('Grand Total must be greater than 0'));
        }
    }
});
```

**Before Submit Validation**:
```javascript
// Pattern from: erpnext/stock/doctype/stock_entry/stock_entry.js
frappe.ui.form.on('Stock Entry', {
    before_submit: function(frm) {
        let has_qty = false;
        frm.doc.items.forEach(function(item) {
            if (item.qty > 0) {
                has_qty = true;
            }
        });

        if (!has_qty) {
            frappe.throw(__('Please enter quantity for at least one item'));
        }
    }
});
```

### 7. Conditional Field Display

**Show/Hide Fields**:
```javascript
// Pattern from: erpnext/accounts/doctype/payment_entry/payment_entry.js
frappe.ui.form.on('Payment Entry', {
    payment_type: function(frm) {
        frm.events.toggle_fields(frm);
    },

    toggle_fields: function(frm) {
        let is_receive = (frm.doc.payment_type === 'Receive');
        let is_pay = (frm.doc.payment_type === 'Pay');

        frm.toggle_display('paid_from', is_pay);
        frm.toggle_display('paid_to', is_receive);
        frm.toggle_reqd('paid_from', is_pay);
        frm.toggle_reqd('paid_to', is_receive);
    }
});
```

**Field Property Changes**:
```javascript
// Pattern from: erpnext/selling/doctype/sales_order/sales_order.js
frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // Make field read-only based on condition
        frm.set_df_property('customer', 'read_only', frm.doc.docstatus === 1);

        // Change field label
        frm.set_df_property('delivery_date', 'label',
            frm.doc.order_type === 'Sales' ? __('Delivery Date') : __('Delivery By'));

        // Set field as mandatory
        frm.toggle_reqd('delivery_date', frm.doc.order_type === 'Sales');
    }
});
```

### 8. Calculations and Totals

**Calculate Child Table Totals**:
```javascript
// Pattern from: erpnext/accounts/doctype/sales_invoice/sales_invoice.js
frappe.ui.form.on('Sales Invoice', {
    calculate_totals: function(frm) {
        let total = 0;
        frm.doc.items.forEach(function(item) {
            item.amount = flt(item.qty) * flt(item.rate);
            total += item.amount;
        });
        frm.set_value('total', total);

        // Calculate tax and grand total
        let tax_amount = flt(total * frm.doc.tax_rate / 100);
        frm.set_value('total_taxes_and_charges', tax_amount);
        frm.set_value('grand_total', total + tax_amount);
    }
});

frappe.ui.form.on('Sales Invoice Item', {
    qty: function(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, 'amount',
            flt(item.qty) * flt(item.rate));
        frm.events.calculate_totals(frm);
    },

    rate: function(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, 'amount',
            flt(item.qty) * flt(item.rate));
        frm.events.calculate_totals(frm);
    }
});
```

### 9. Link Field Filters (set_query)

**Filter Link Field Options**:
```javascript
// Pattern from: erpnext/stock/doctype/stock_entry/stock_entry.js
frappe.ui.form.on('Stock Entry', {
    setup: function(frm) {
        // Filter items based on item group
        frm.set_query('item_code', 'items', function(doc, cdt, cdn) {
            return {
                filters: {
                    'item_group': ['in', ['Raw Material', 'Sub Assemblies']],
                    'is_stock_item': 1
                }
            };
        });

        // Dynamic filters based on doc values
        frm.set_query('warehouse', function() {
            return {
                filters: {
                    'company': frm.doc.company,
                    'is_group': 0
                }
            };
        });
    }
});
```

**Complex Query Filters**:
```javascript
// Pattern from: erpnext/accounts/doctype/payment_entry/payment_entry.js
frappe.ui.form.on('Payment Entry', {
    setup: function(frm) {
        frm.set_query('party', function() {
            let party_type = frm.doc.party_type;
            if (party_type === 'Customer') {
                return {query: 'erpnext.controllers.queries.customer_query'};
            } else if (party_type === 'Supplier') {
                return {query: 'erpnext.controllers.queries.supplier_query'};
            }
        });

        frm.set_query('reference_doctype', 'references', function() {
            let doctypes = [];
            if (frm.doc.party_type === 'Customer') {
                doctypes = ['Sales Invoice', 'Sales Order'];
            } else if (frm.doc.party_type === 'Supplier') {
                doctypes = ['Purchase Invoice', 'Purchase Order'];
            }
            return {
                filters: {
                    'name': ['in', doctypes]
                }
            };
        });
    }
});
```

### 10. Dialogs and Prompts

**Create Custom Dialog**:
```javascript
// Pattern from: erpnext/stock/doctype/stock_entry/stock_entry.js
frappe.ui.form.on('Stock Entry', {
    get_items: function(frm) {
        let dialog = new frappe.ui.Dialog({
            title: __('Get Items'),
            fields: [
                {
                    fieldtype: 'Link',
                    label: __('Warehouse'),
                    fieldname: 'warehouse',
                    options: 'Warehouse',
                    reqd: 1,
                    get_query: function() {
                        return {
                            filters: {
                                'company': frm.doc.company
                            }
                        };
                    }
                },
                {
                    fieldtype: 'Link',
                    label: __('Item Group'),
                    fieldname: 'item_group',
                    options: 'Item Group'
                }
            ],
            primary_action_label: __('Get Items'),
            primary_action: function(values) {
                frappe.call({
                    method: 'get_items',
                    doc: frm.doc,
                    args: values,
                    callback: function(r) {
                        dialog.hide();
                        frm.refresh_field('items');
                    }
                });
            }
        });
        dialog.show();
    }
});
```

## References

### Frappe Core Client Script Examples (Primary Reference)

**Learn from Frappe Framework:**
- Frappe Form Scripts: https://github.com/frappe/frappe/tree/develop/frappe/desk/doctype
  - `form/form.js` - Core form functionality
  - `todo/todo.js` - Simple form script example
- Frappe UI Components: https://github.com/frappe/frappe/tree/develop/frappe/public/js/frappe/ui

**ERPNext Client Script Examples:**
- Sales Invoice: https://github.com/frappe/erpnext/blob/develop/erpnext/accounts/doctype/sales_invoice/sales_invoice.js
- Purchase Order: https://github.com/frappe/erpnext/blob/develop/erpnext/buying/doctype/purchase_order/purchase_order.js
- Stock Entry: https://github.com/frappe/erpnext/blob/develop/erpnext/stock/doctype/stock_entry/stock_entry.js
- Payment Entry: https://github.com/frappe/erpnext/blob/develop/erpnext/accounts/doctype/payment_entry/payment_entry.js
- Item: https://github.com/frappe/erpnext/blob/develop/erpnext/stock/doctype/item/item.js

### Official Documentation (Secondary Reference)

- Form Scripts: https://frappeframework.com/docs/user/en/desk/scripting/form-scripts
- Client API: https://frappeframework.com/docs/user/en/api/form
- frappe.ui.form.on: https://frappeframework.com/docs/user/en/api/form#frappeuiformon

## Best Practices

1. **Event Handler Organization**: Group related handlers together
2. **Reusable Functions**: Extract common logic into reusable methods
3. **Null Checks**: Always validate data before using it
4. **Async Operations**: Use callbacks for database and API calls
5. **User Feedback**: Use `frappe.show_alert()` for success/error messages
6. **Performance**: Debounce expensive operations in change handlers
7. **Translation**: Use `__()` for translatable strings
8. **Error Handling**: Wrap risky operations in try-catch
9. **Child Tables**: Use `locals[cdt][cdn]` to access child table rows
10. **Field Updates**: Use `frappe.model.set_value()` for child table fields

## File Output Format

Generated client scripts should be saved at:
```
apps/<app_name>/<module>/doctype/<doctype_name>/<doctype_name>.js
```

Always include:
- Clear comments explaining functionality
- Proper indentation (4 spaces or tab as per project)
- Event handler grouping
- Error handling where appropriate
- Translation wrappers for user-facing strings

## Common Patterns Summary

- **refresh**: Add buttons, set field properties
- **setup**: One-time setup, set query filters
- **onload**: Initialize values for new docs
- **validate**: Pre-save validations
- **before_submit**: Pre-submission checks
- **field_name**: Handle field changes
- **child_table_field**: Handle child table field changes
- **items_add/remove**: Handle row additions/removals
